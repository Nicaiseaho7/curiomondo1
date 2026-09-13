"""Diagnosi della lettura delle fonti: quante notizie sono davvero leggibili.

La verifica editoriale costa; leggere una pagina no. Prima di spendere
un'altra prova a pagamento conviene sapere quali fonti si lasciano leggere da
un runner e quali no, e per quale motivo esatto. Questo strumento lo misura
senza chiamare mai il modello.

    python3 -m automation.newsroom.extract_check --per-fonte 2
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import googlenews
from .extract import extract
from .sources import Feed, fetch_feed

ROOT = Path(__file__).resolve().parents[2]


def _esamina(voce: tuple[str, str, str]) -> dict[str, object]:
    fonte, titolo, url = voce
    risoluzione = googlenews.risolvi(url) if googlenews.e_google_news(url) else None
    if risoluzione is not None and not risoluzione.risolto:
        return {"fonte": fonte, "titolo": titolo[:60], "metodo": "",
                "ok": False, "motivo": f"non_risolto:{risoluzione.motivo}", "parole": 0}
    reale = risoluzione.url if risoluzione else url
    esito = extract(reale)
    return {
        "fonte": fonte,
        "titolo": titolo[:60],
        "metodo": risoluzione.metodo if risoluzione else "diretto",
        "ok": esito.ok,
        "motivo": esito.reason,
        "parole": esito.words,
        "dominio": reale.split("/")[2] if "//" in reale else reale[:40],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quante fonti sono leggibili davvero")
    parser.add_argument("--per-fonte", type=int, default=2)
    parser.add_argument("--fonti", default=str(ROOT / "automation/newsroom/sources.json"))
    args = parser.parse_args(argv)

    registro = json.loads(Path(args.fonti).read_text(encoding="utf-8"))
    feeds = [Feed.from_dict(f) for f in (registro["feeds"] if isinstance(registro, dict) else registro)]
    feeds = [f for f in feeds if f.enabled]

    voci: list[tuple[str, str, str]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for feed, (items, _salute) in zip(feeds, pool.map(lambda f: fetch_feed(f), feeds)):
            for item in items[: args.per_fonte]:
                voci.append((feed.name, item.title, item.url))

    with ThreadPoolExecutor(max_workers=8) as pool:
        esiti = list(pool.map(_esamina, voci))

    leggibili = [e for e in esiti if e["ok"]]
    motivi = Counter(str(e["motivo"]).split(":")[0] for e in esiti if not e["ok"])
    metodi = Counter(str(e["metodo"]) for e in esiti)

    print(f"## Lettura delle fonti\n")
    print(f"- pagine esaminate: **{len(esiti)}**")
    print(f"- leggibili: **{len(leggibili)}** ({len(leggibili) * 100 // max(1, len(esiti))}%)\n")
    print("| fonte | esito | parole | dettaglio |")
    print("|---|---|---|---|")
    for e in sorted(esiti, key=lambda x: (not x["ok"], str(x["fonte"]))):
        segno = "leggibile" if e["ok"] else "no"
        print(f"| {e['fonte']} | {segno} | {e['parole']} | {e['metodo']} {e['motivo']} |")
    print("\n**Motivi di scarto:** " + ", ".join(f"{k}={v}" for k, v in motivi.most_common()))
    print("\n**Metodi di risoluzione:** " + ", ".join(f"{k or 'fallito'}={v}" for k, v in metodi.most_common()))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
