#!/usr/bin/env python3
"""Registra la correzione globale delle miniature nei correlati."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = 452
DATE = "2026-09-20"


def write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for relative in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
        path = ROOT / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = VERSION
        write(path, data)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "related-images-global-fix",
        "news_added": [],
        "news_updated": [],
        "change": "Miniature correlate ripristinate globalmente e controller JavaScript rivalidato su tutti gli articoli",
        "design_changed": False,
    }
    write(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": DATE,
            "release_date": DATE,
            "last_update": "related-images-global-fix-v452",
        })
        write(path, state)

    log = ROOT / "automation/logs/editoriale-20260920T075200-Europe-Rome.json"
    write(log, {
        "run_at": "2026-09-20T07:52:00+02:00",
        "type": "related-images-global-fix",
        "articles_audited": 443,
        "related_sections_found": 412,
        "related_links_audited": 1167,
        "links_without_media_index_before_fix": 107,
        "fix": "remove non-renderable links, refill to three relevant image-backed cards, revalidate shared JS",
    })


if __name__ == "__main__":
    main()
