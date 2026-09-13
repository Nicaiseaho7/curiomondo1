"""Quante notizie supererebbero davvero il filtro, in una giornata normale.

La regola delle due testate distinte e giusta ma stringe: senza numeri non si
puo sapere se la redazione pubblichera tre pezzi al giorno o nessuno. Questo
strumento fa una scansione vera, raccoglie il materiale come farebbe il worker
e dice quanti candidati arriverebbero alla verifica — senza chiamare il modello
e senza spendere un centesimo.

    python3 -m automation.newsroom.resa --quanti 15
"""
from __future__ import annotations

import argparse
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .editor import url_citabili
from .extract import gather
from .normalize import dominio
from .state import SEEN, Store
from .watcher import run_watch

ROOT = Path(__file__).resolve().parents[2]


def _esamina(candidato) -> dict[str, object]:
    urls = [candidato.url] + [c["url"] for c in candidato.corroborations]
    estratti = gather(urls, limit=3)
    citabili = url_citabili(estratti, candidato.corroborations)
    testate = sorted({dominio(u) for u in citabili} - {""})
    leggibili = [e for e in estratti if e.ok]
    return {
        "titolo": candidato.title[:70],
        "fonte": candidato.source,
        "conferme": len(candidato.corroborations),
        "leggibili": len(leggibili),
        "testate": testate,
        "passa": len(testate) >= 2 and bool(leggibili),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resa attesa della redazione")
    parser.add_argument("--quanti", type=int, default=15, help="candidati da esaminare")
    parser.add_argument("--articles", default=str(ROOT / "notizie"))
    args = parser.parse_args(argv)

    stato = Path(tempfile.mkdtemp()) / "state"
    run_watch(stato, cadence="deep", articles_dir=Path(args.articles))
    candidati = sorted(Store(stato).by_status(SEEN), key=lambda c: c.score, reverse=True)
    candidati = candidati[: args.quanti]

    with ThreadPoolExecutor(max_workers=6) as pool:
        esiti = list(pool.map(_esamina, candidati))

    passati = [e for e in esiti if e["passa"]]
    print("## Resa attesa della redazione\n")
    print(f"- candidati esaminati: **{len(esiti)}**")
    print(f"- arriverebbero alla verifica: **{len(passati)}**\n")
    print("| esito | testate | conferme | fonte | titolo |")
    print("|---|---|---|---|---|")
    for e in sorted(esiti, key=lambda x: not x["passa"]):
        testate = ", ".join(e["testate"]) or "—"  # type: ignore[arg-type]
        print(f"| {'passa' if e['passa'] else 'ferma'} | {testate} | {e['conferme']} "
              f"| {e['fonte']} | {e['titolo']} |")

    motivi = Counter(
        "nessuna fonte leggibile" if not e["leggibili"] else "una sola testata"
        for e in esiti if not e["passa"]
    )
    print("\n**Perche si fermano:** " + (", ".join(f"{k}: {v}" for k, v in motivi.most_common()) or "—"))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
