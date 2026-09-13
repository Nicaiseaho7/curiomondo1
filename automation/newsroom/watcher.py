"""Watcher: il componente che gira spesso e costa quasi nulla.

Non genera articoli e non chiama modelli a pagamento. Interroga le fonti,
riconosce le novità, elimina i doppioni e lascia in coda soltanto i candidati
che meritano davvero una verifica editoriale.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import filters
from .observability import CycleLogger
from .normalize import title_similarity
from .sources import fetch_all, load_feeds
from .state import Candidate, Store, existing_site_titles, _now

ROOT = Path(__file__).resolve().parents[2]
SOURCES_PATH = Path(__file__).resolve().parent / "sources.json"


def run_watch(
    state_dir: Path,
    cadence: str = "fast",
    sources_path: Path = SOURCES_PATH,
    articles_dir: Path | None = None,
    max_new: int = 25,
    max_age_hours: float = 36.0,
    min_score: float = 0.45,
    timeout: int = 12,
    logger: CycleLogger | None = None,
) -> dict[str, Any]:
    """Esegue un ciclo di sorveglianza e aggiorna lo stato persistente."""
    log = logger or CycleLogger(f"watch:{cadence}", log_dir=state_dir / "logs")
    store = Store(state_dir)
    feeds = load_feeds(sources_path, cadence=cadence)
    log.event("watch_start", cadence=cadence, feeds=len(feeds))

    cache = store.meta.setdefault("feed_cache", {})
    items, health, cache = fetch_all(feeds, cache=cache, timeout=timeout)
    store.meta["feed_cache"] = cache

    ok = sum(1 for h in health if h["status"] == "ok")
    unchanged = sum(1 for h in health if h["status"] == "not_modified")
    broken = [h for h in health if h["status"] == "error"]
    log.count("fonti_interrogate", len(health))
    log.count("fonti_con_novita", ok)
    log.count("fonti_invariate", unchanged)
    log.count("fonti_in_errore", len(broken))
    log.count("elementi_grezzi", len(items))
    for failure in broken:
        log.event("source_error", feed=failure["feed"], error=failure.get("error", ""))

    site_titles = existing_site_titles(articles_dir or (ROOT / "notizie"))
    now = datetime.now(timezone.utc)

    accepted: list[Candidate] = []
    seen_this_cycle: set[str] = set()

    # Le fonti più autorevoli vengono valutate per prime: se due testate
    # raccontano lo stesso fatto, teniamo quella con la fonte migliore. A parità
    # conta prima chi si lascia leggere: la testata che tiene il testo dietro un
    # abbonamento resta buona come conferma, ma non puo fornire il materiale.
    items.sort(key=lambda i: (i.materiale, filters.TIER_WEIGHT.get(i.source_tier, 0.6)), reverse=True)

    for item in items:
        key = item.url_key
        if not key:
            continue
        if key in seen_this_cycle:
            log.count("duplicati_stesso_ciclo")
            continue
        seen_this_cycle.add(key)

        if store.knows_url(key):
            log.count("gia_noti")
            continue

        topic = item.topic_key

        def remember_rejected(reason: str) -> None:
            """Registra lo scarto: così il link non viene rivalutato ogni ciclo."""
            store.add(Candidate(
                url_key=key, topic_key=topic, url=item.url, title=item.title,
                source=item.source, source_tier=item.source_tier, trust=item.trust,
                published_at=item.published_at, status="rejected", reason=reason,
            ))

        if any(title_similarity(item.title, known) >= 0.62 for known in site_titles):
            remember_rejected("gia_pubblicato_sul_sito")
            log.count("scartati_gia_sul_sito")
            continue

        twin = store.knows_topic(topic) or store.find_similar(item.title, threshold=0.62)
        if twin is not None:
            # Una seconda testata sullo stesso fatto non è rumore: è una conferma
            # indipendente, e la verifica editoriale la pretende per i temi
            # delicati. La registriamo sul candidato già noto.
            if twin.status in ("seen", "drafted", "queued") and twin.add_corroboration(
                item.source, item.url, item.title
            ):
                twin.updated_at = _now()
                log.count("conferme_raccolte")
            remember_rejected(f"duplicato_di:{twin.url_key}")
            log.count("duplicati_stessa_notizia")
            continue

        decision = filters.screen(
            item.title, item.summary, item.source_tier, item.trust, item.published_at,
            max_age_hours=max_age_hours, min_score=min_score, now=now,
        )
        candidate = Candidate(
            url_key=key, topic_key=topic, url=item.url, title=item.title,
            source=item.source, source_tier=item.source_tier, trust=item.trust,
            published_at=item.published_at,
            status="seen" if decision.accepted else "rejected",
            reason=decision.reason,
            priority=decision.priority,
            score=round(decision.score, 3),
        )
        if decision.high_risk:
            candidate.article["high_risk"] = True
        store.add(candidate)

        if decision.accepted:
            accepted.append(candidate)
            log.count("candidati_accettati")
        else:
            log.count(f"scartati_{decision.reason or 'senza_motivo'}")

    # Teniamo i migliori: il worker editoriale non deve ricevere una valanga.
    accepted.sort(key=lambda c: (c.priority == "breaking", c.score), reverse=True)
    if len(accepted) > max_new:
        for extra in accepted[max_new:]:
            store.update(extra.url_key, status="rejected", reason="oltre_limite_ciclo")
        accepted = accepted[:max_new]
        log.count("oltre_limite_ciclo", 1)

    removed = store.prune()
    if removed:
        log.count("stato_ripulito", removed)

    store.note_cycle(f"watch_{cadence}", {
        "feeds": len(feeds), "raw_items": len(items), "accepted": len(accepted),
    })
    store.save()

    breaking = [c for c in accepted if c.priority == "breaking"]
    summary = log.summary(
        "ok",
        cadence=cadence,
        nuovi_candidati=len(accepted),
        di_cui_breaking=len(breaking),
        candidati=[{"title": c.title, "source": c.source, "score": c.score, "priority": c.priority}
                   for c in accepted[:10]],
        fonti_in_errore=[h["feed"] for h in broken],
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watcher notizie CurioMondo")
    parser.add_argument("--state", required=True, help="cartella dello stato persistente")
    parser.add_argument("--cadence", choices=["fast", "deep"], default="fast")
    parser.add_argument("--sources", default=str(SOURCES_PATH))
    parser.add_argument("--articles", default=str(ROOT / "notizie"))
    parser.add_argument("--max-new", type=int, default=25)
    parser.add_argument("--max-age-hours", type=float, default=36.0)
    parser.add_argument("--min-score", type=float, default=0.45)
    parser.add_argument("--timeout", type=int, default=12)
    args = parser.parse_args(argv)

    summary = run_watch(
        state_dir=Path(args.state),
        cadence=args.cadence,
        sources_path=Path(args.sources),
        articles_dir=Path(args.articles),
        max_new=args.max_new,
        max_age_hours=args.max_age_hours,
        min_score=args.min_score,
        timeout=args.timeout,
    )
    # Il codice di uscita resta 0 anche senza candidati: "nessuna novità" non è
    # un errore, e un fallimento del watcher non deve tingere di rosso la CI.
    return 0 if summary.get("status") == "ok" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
