"""Log strutturati per ogni ciclo della redazione automatica.

I log sono JSON Lines: una riga per evento, facili da leggere a occhio e da
interrogare. Nessun valore di variabile d'ambiente viene mai registrato: i
segreti non devono comparire nei log nemmeno per errore.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Valori da oscurare se comparissero per sbaglio dentro un messaggio.
_SECRET_ENV_NAMES = ("OPENAI_API_KEY", "GITHUB_TOKEN", "NETLIFY_AUTH_TOKEN", "NETLIFY_BUILD_HOOK")
_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
)


def scrub(value: Any) -> Any:
    """Rimuove segreti noti da qualunque struttura destinata ai log."""
    if isinstance(value, str):
        cleaned = value
        for name in _SECRET_ENV_NAMES:
            secret = os.getenv(name)
            if secret and len(secret) >= 8 and secret in cleaned:
                cleaned = cleaned.replace(secret, "[REDACTED]")
        for pattern in _SECRET_PATTERNS:
            cleaned = pattern.sub("[REDACTED]", cleaned)
        return cleaned
    if isinstance(value, dict):
        return {key: scrub(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [scrub(item) for item in value]
    return value


class CycleLogger:
    """Raccoglie gli eventi di un ciclo e produce un riepilogo finale."""

    def __init__(self, cycle: str, log_dir: Path | None = None, echo: bool = True):
        self.cycle = cycle
        self.started_at = time.time()
        self.echo = echo
        self.events: list[dict[str, Any]] = []
        self.counters: dict[str, int] = {}
        self.log_dir = log_dir
        if log_dir is not None:
            log_dir.mkdir(parents=True, exist_ok=True)
            day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            self._path = log_dir / f"{day}.jsonl"
        else:
            self._path = None

    def count(self, name: str, amount: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + amount

    def event(self, kind: str, **fields: Any) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "cycle": self.cycle,
            "event": kind,
            **scrub(fields),
        }
        self.events.append(record)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        if self.echo:
            print(json.dumps(record, ensure_ascii=False), file=sys.stderr)

    def summary(self, status: str, **fields: Any) -> dict[str, Any]:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "cycle": self.cycle,
            "event": "cycle_summary",
            "status": status,
            "duration_s": round(time.time() - self.started_at, 2),
            "counters": dict(self.counters),
            **scrub(fields),
        }
        self.events.append(payload)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        print(json.dumps(payload, ensure_ascii=False))
        return payload
