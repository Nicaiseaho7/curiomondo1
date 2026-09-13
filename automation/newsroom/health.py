"""Controllo di salute del registro fonti.

Va eseguito dove la rete esiste davvero (i runner GitHub Actions). Dice quali
feed rispondono, quanti elementi restituiscono e quali sono da disattivare,
così il registro resta onesto invece di elencare fonti morte.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .sources import fetch_feed, load_feeds

SOURCES_PATH = Path(__file__).resolve().parent / "sources.json"


def _check_one(feed, timeout: int) -> dict:
    items, report = fetch_feed(feed, cache={}, timeout=timeout, retries=1)
    return {
        "id": feed.id,
        "name": feed.name,
        "tier": feed.tier,
        "cadence": feed.cadence,
        "direct": feed.direct,
        "status": report["status"],
        "items": report.get("items", 0),
        "error": report.get("error", ""),
        "sample": items[0].title[:80] if items else "",
    }


def check_all(sources_path: Path = SOURCES_PATH, timeout: int = 15, workers: int = 8) -> dict:
    """Interroga tutte le fonti in parallelo: in sequenza servirebbero minuti."""
    feeds = load_feeds(sources_path, cadence="deep")
    rows = []
    if feeds:
        with ThreadPoolExecutor(max_workers=max(1, min(workers, len(feeds)))) as pool:
            futures = {pool.submit(_check_one, feed, timeout): feed for feed in feeds}
            for future in as_completed(futures):
                feed = futures[future]
                try:
                    rows.append(future.result())
                except Exception as exc:
                    rows.append({"id": feed.id, "name": feed.name, "tier": feed.tier,
                                 "cadence": feed.cadence, "direct": feed.direct,
                                 "status": "error", "items": 0,
                                 "error": type(exc).__name__, "sample": ""})
    rows.sort(key=lambda r: (r["status"] != "error", r["tier"], r["id"]))
    healthy = [r for r in rows if r["status"] in ("ok", "not_modified") and r["items"] > 0]
    empty = [r for r in rows if r["status"] == "ok" and r["items"] == 0]
    broken = [r for r in rows if r["status"] == "error"]
    return {
        "totale": len(rows),
        "funzionanti": len(healthy),
        "vuote": len(empty),
        "in_errore": len(broken),
        "da_disattivare": [r["id"] for r in broken + empty],
        "dettaglio": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verifica quali fonti rispondono davvero")
    parser.add_argument("--sources", default=str(SOURCES_PATH))
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--out", default="", help="file JSON dove salvare il report")
    parser.add_argument("--fail-under", type=float, default=0.0,
                        help="esci con errore se la quota di fonti funzionanti scende sotto questo valore (0..1)")
    args = parser.parse_args(argv)

    report = check_all(Path(args.sources), timeout=args.timeout)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.fail_under and report["totale"]:
        ratio = report["funzionanti"] / report["totale"]
        if ratio < args.fail_under:
            print(f"Fonti funzionanti {ratio:.0%}, sotto la soglia {args.fail_under:.0%}")
            return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
