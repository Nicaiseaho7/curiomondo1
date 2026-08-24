#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "automation" / "config.json"
LOG_DIR = ROOT / "automation" / "logs"

CFG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
MODE = sys.argv[1] if len(sys.argv) > 1 else "articles"

LOG_DIR.mkdir(parents=True, exist_ok=True)


def report(status: str, **extra):
    payload = {
        "time": datetime.now(timezone.utc).isoformat(),
        "mode": MODE,
        "status": status,
        **extra,
    }

    log_file = LOG_DIR / f"{MODE}-latest.json"
    log_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(payload, ensure_ascii=False))


if MODE not in {"articles", "library", "health"}:
    report("blocked", reason="unknown_mode")
    sys.exit(2)


if MODE == "health":
    report("ok", message="CurioMondo automation healthy")
    sys.exit(0)


if MODE == "library":
    report(
        "ready",
        message="Library automation available",
        target_guides=CFG.get("library", {}).get("target_guides", 3),
    )
    sys.exit(0)


# ============================================================
# CURIOMONDO ARTICLE AUTOMATION
# ============================================================

article_cfg = CFG.get("articles", {})

interval_hours = article_cfg.get("interval_hours", 3)
max_articles = article_cfg.get("max_articles_per_cycle", 8)
max_deploys = article_cfg.get("max_deploys_per_cycle", 1)

editorial_contract = (
    ROOT / "automation" / "prompts" / "editorial-contract.txt"
)

if not editorial_contract.exists():
    report(
        "blocked",
        reason="editorial_contract_missing",
        expected=str(editorial_contract.relative_to(ROOT)),
    )
    sys.exit(3)


# The actual editorial worker is executed separately.
# This controller validates the repository configuration
# before the scheduled GitHub workflow starts publication.

possible_workers = [
    ROOT / "automation" / "article_worker.py",
    ROOT / "automation" / "articles.py",
    ROOT / "automation" / "publisher.py",
]

worker = next((p for p in possible_workers if p.exists()), None)

if worker is None:
    report(
        "waiting_for_worker",
        interval_hours=interval_hours,
        max_articles=max_articles,
        max_deploys=max_deploys,
        editorial_contract=True,
        message="Controller ready. Article worker must be installed.",
    )
    sys.exit(0)


report(
    "ready",
    interval_hours=interval_hours,
    max_articles=max_articles,
    max_deploys=max_deploys,
    editorial_contract=True,
    worker=str(worker.relative_to(ROOT)),
)
