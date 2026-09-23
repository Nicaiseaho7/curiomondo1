#!/usr/bin/env python3
"""Fail closed when deploy inputs are truncated, mis-encoded or malformed."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SURFACES = (
    "index.html",
    "notizie/index.html",
    "feed.xml",
    "sitemap.xml",
    "news-sitemap.xml",
    "curiomondo-site-manifest.json",
    "CURIOMONDO-RELEASE-STATE.json",
    "RELEASE-STATE.json",
)
IMAGE_SIGNATURES = {
    ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".webp": lambda data: len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP",
}


def main() -> int:
    errors: list[str] = []

    json_paths = sorted(path for path in ROOT.rglob("*.json") if ".git" not in path.parts)
    for path in json_paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            raw = path.read_bytes()
            if not raw:
                raise ValueError("file vuoto")
            text = raw.decode("utf-8")
            json.loads(text)
        except UnicodeDecodeError as exc:
            errors.append(f"JSON non UTF-8: {relative} ({exc})")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"JSON non valido: {relative} ({exc})")

    for relative in TEXT_SURFACES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"superficie obbligatoria assente: {relative}")
            continue
        try:
            if not path.read_bytes().decode("utf-8").strip():
                errors.append(f"superficie obbligatoria vuota: {relative}")
        except UnicodeDecodeError as exc:
            errors.append(f"superficie non UTF-8: {relative} ({exc})")

    for path in sorted((ROOT / "assets/images/editorial-auto").glob("*")):
        validator = IMAGE_SIGNATURES.get(path.suffix.casefold())
        if validator is None or not path.is_file():
            continue
        data = path.read_bytes()
        if not validator(data):
            errors.append(f"immagine corrotta o formato errato: {path.relative_to(ROOT).as_posix()}")

    result = {
        "repository_integrity": "pass" if not errors else "fail",
        "json_checked": len(json_paths),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
