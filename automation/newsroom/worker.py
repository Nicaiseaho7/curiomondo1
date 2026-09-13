"""Worker editoriale: dal candidato all'articolo pronto.

Non pubblica. Prepara: legge le fonti, chiede la verifica, scrive il pezzo e lo
mette in stato "bozza". La pubblicazione è una fase separata, con la coda e il
deploy a lotti, perché un articolo pronto non deve costringere a un deploy.

Ogni passaggio può fermare il candidato, e quando lo ferma registra il motivo:
un articolo che non nasce deve lasciare traccia del perché, altrimenti non si
capisce mai se la redazione automatica sta lavorando o sta solo tacendo.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import editor
from .extract import gather
from .observability import CycleLogger
from .openai_client import BudgetExceeded, BudgetGuard, Client, OpenAIError
from .state import DRAFTED, REJECTED, SEEN, Store, existing_site_titles

ROOT = Path(__file__).resolve().parents[2]


def _carica_config() -> dict[str, Any]:
    percorso = ROOT / "automation/config.json"
    try:
        return json.loads(percorso.read_text(encoding="utf-8"))
    except Exception:
        return {}


def lavora(
    state_dir: Path,
    massimo: int = 1,
    modello_verifica: str = "gpt-5",
    modello_stesura: str = "gpt-5",
    tetto_giornaliero: float = 5.0,
    articles_dir: Path | None = None,
    solo_prova: bool = False,
    logger: CycleLogger | None = None,
) -> dict[str, Any]:
    """Elabora i candidati migliori fino a produrre ``massimo`` bozze."""
    log = logger or CycleLogger("worker", log_dir=state_dir / "logs")
    store = Store(state_dir)
    budget = BudgetGuard(state_dir, daily_limit_usd=tetto_giornaliero)
    client = Client(budget=budget)

    if not client.available:
        log.event("chiave_assente")
        return log.summary("blocked", motivo="OPENAI_API_KEY non configurata")

    if budget.near_limit():
        log.event("budget_in_esaurimento",
                  speso=round(budget.spent_today, 3), tetto=tetto_giornaliero)

    candidati = sorted(
        store.by_status(SEEN),
        key=lambda c: (c.priority == "breaking", c.score),
        reverse=True,
    )
    if not candidati:
        return log.summary("ok", bozze=0, motivo="nessun candidato in attesa")

    titoli_esistenti = existing_site_titles(articles_dir or (ROOT / "notizie"), limit=60)
    bozze: list[dict[str, Any]] = []
    esaminati = 0

    for candidato in candidati:
        if len(bozze) >= massimo:
            break
        esaminati += 1
        log.event("esame", titolo=candidato.title[:90], fonte=candidato.source,
                  conferme=len(candidato.corroborations), priorita=candidato.priority)

        # 1. Materiale reale: senza testo delle fonti non si scrive nulla.
        urls = [candidato.url] + [c["url"] for c in candidato.corroborations]
        estratti = gather(urls, limit=3)
        leggibili = [e for e in estratti if e.ok]
        log.count("fonti_lette", len(leggibili))
        if not leggibili:
            store.update(candidato.url_key, status=REJECTED, reason="fonti_non_leggibili")
            log.event("scartato", motivo="fonti_non_leggibili", titolo=candidato.title[:70])
            continue

        # 2. Verifica editoriale.
        try:
            verdetto, _ = editor.verifica(
                client, modello_verifica, candidato.title, candidato.source,
                estratti, candidato.corroborations,
                alto_rischio=bool(candidato.article.get("high_risk")),
                gia_pubblicati=titoli_esistenti,
                tier=candidato.source_tier,
                trust=candidato.trust,
            )
        except BudgetExceeded as exc:
            log.event("budget_esaurito", dettaglio=str(exc))
            break
        except OpenAIError as exc:
            store.update(candidato.url_key, attempts=candidato.attempts + 1)
            log.event("errore_verifica", dettaglio=str(exc)[:200])
            continue

        log.event("verdetto", pubblicare=verdetto.pubblicare, motivo=verdetto.motivo,
                  formato=verdetto.formato, categoria=verdetto.categoria)
        if not verdetto.pubblicare:
            store.update(candidato.url_key, status=REJECTED,
                         reason=f"editoriale:{verdetto.motivo[:80]}")
            log.count("scartati_dalla_verifica")
            continue

        # 3. Stesura.
        try:
            articolo, _ = editor.scrivi(
                client, modello_stesura, candidato.title, candidato.source,
                estratti, verdetto, candidato.corroborations,
            )
        except BudgetExceeded as exc:
            log.event("budget_esaurito", dettaglio=str(exc))
            break
        except OpenAIError as exc:
            store.update(candidato.url_key, attempts=candidato.attempts + 1)
            log.event("errore_stesura", dettaglio=str(exc)[:200])
            continue

        # 4. Controllo del contratto, prima di spendere altro.
        problemi = editor.controlla_articolo(articolo)
        if problemi:
            store.update(candidato.url_key, attempts=candidato.attempts + 1,
                         reason="articolo_non_conforme")
            log.event("articolo_non_conforme", problemi=problemi, titolo=articolo.get("titolo", "")[:70])
            log.count("articoli_scartati_dal_controllo")
            continue

        articolo["fonte_originale"] = candidato.url
        articolo["conferme"] = [c.get("source") for c in candidato.corroborations]
        articolo["verifica"] = {
            "motivo": verdetto.motivo,
            "valore_aggiunto": verdetto.valore_aggiunto,
            "fonte_primaria": verdetto.fonte_primaria,
            "sensibile": verdetto.sensibile,
        }

        if not solo_prova:
            store.update(candidato.url_key, status=DRAFTED, article=articolo)
        bozze.append(articolo)
        log.count("bozze_prodotte")
        log.event("bozza_pronta", titolo=articolo["titolo"][:90],
                  parole=len(" ".join(articolo["paragrafi"]).split()),
                  formato=articolo["formato"], categoria=articolo["categoria"])

    if not solo_prova:
        store.save()

    return log.summary(
        "ok",
        esaminati=esaminati,
        bozze=len(bozze),
        costo_usd=round(client.usage.cost_usd, 4),
        token=client.usage.input_tokens + client.usage.output_tokens,
        speso_oggi_usd=round(budget.spent_today, 4),
        tetto_usd=tetto_giornaliero,
        titoli=[b["titolo"] for b in bozze],
        anteprima=bozze if solo_prova else [],
    )


def main(argv: list[str] | None = None) -> int:
    config = _carica_config().get("newsroom", {})
    parser = argparse.ArgumentParser(description="Worker editoriale CurioMondo")
    parser.add_argument("--state", required=True)
    parser.add_argument("--max", type=int, default=1, help="quante bozze produrre al massimo")
    parser.add_argument("--modello-verifica", default=config.get("modello_verifica", "gpt-5"))
    parser.add_argument("--modello-stesura", default=config.get("modello_stesura", "gpt-5"))
    parser.add_argument("--tetto-giornaliero", type=float,
                        default=float(config.get("tetto_giornaliero_usd", 5.0)))
    parser.add_argument("--articles", default=str(ROOT / "notizie"))
    parser.add_argument("--solo-prova", action="store_true",
                        help="non salva nulla nello stato: serve al test controllato")
    args = parser.parse_args(argv)

    esito = lavora(
        state_dir=Path(args.state),
        massimo=args.max,
        modello_verifica=args.modello_verifica,
        modello_stesura=args.modello_stesura,
        tetto_giornaliero=args.tetto_giornaliero,
        articles_dir=Path(args.articles),
        solo_prova=args.solo_prova,
    )
    return 0 if esito.get("status") == "ok" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
