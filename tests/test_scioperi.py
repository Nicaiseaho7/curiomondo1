#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "assets/data/scioperi.json").read_text(encoding="utf-8"))
EXPECTED_REGIONS = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana",
    "Trentino-Alto Adige", "Umbria", "Valle d’Aosta", "Veneto",
]
ALLOWED_STATUS = {"proclamato", "confermato", "modificato", "rinviato", "revocato"}
ALLOWED_SECTORS = {"treni", "aerei", "tpl", "marittimo", "scuola", "sanita", "pa", "altri"}


def test_files() -> None:
    for relative in (
        "scioperi/index.html", "scioperi/archivio/index.html",
        "assets/css/scioperi-v1.css", "assets/js/scioperi-v1.js",
        "assets/data/scioperi.json", "README_AGENTE.md",
    ):
        assert (ROOT / relative).is_file(), relative


def test_regions() -> None:
    names = [region["name"] for region in DATA["regions"]]
    assert names == EXPECTED_REGIONS
    slugs = [region["slug"] for region in DATA["regions"]]
    assert len(slugs) == len(set(slugs)) == 20


def test_events() -> None:
    region_slugs = {region["slug"] for region in DATA["regions"]}
    ids = [event["id"] for event in DATA["events"]]
    assert len(ids) == len(set(ids))
    for event in DATA["events"]:
        assert event["status"] in ALLOWED_STATUS
        assert event["sector"] in ALLOWED_SECTORS
        assert event["regions"] and set(event["regions"]) <= region_slugs
        assert event["source"]["url"].startswith("https://")
        assert event["verifiedAt"]
        assert datetime.fromisoformat(event["startsAt"]) <= datetime.fromisoformat(event["endsAt"])
        if event["national"]:
            assert set(event["regions"]) == region_slugs


def test_current_and_archive_split() -> None:
    reference = datetime.fromisoformat("2026-11-16T22:48:00+01:00")
    current = [e for e in DATA["events"] if datetime.fromisoformat(e["endsAt"]) >= reference]
    archived = [e for e in DATA["events"] if datetime.fromisoformat(e["endsAt"]) < reference]
    assert len(current) == 26
    assert len(archived) == 5
    assert not ({e["id"] for e in current} & {e["id"] for e in archived})


def test_accessibility_and_controls() -> None:
    html = (ROOT / "scioperi/index.html").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/scioperi-v1.js").read_text(encoding="utf-8")
    for token in ("periodFilter", "sectorFilter", "statusFilter", "searchFilter", "resetFilters"):
        assert f'id="{token}"' in html
    assert 'class="skip-link"' in html
    assert 'aria-expanded="false"' in js
    assert "state.openRegions" in js
    assert "Al momento non risultano scioperi programmati per questa regione." in js
    assert "overflow-x" not in (ROOT / "assets/css/scioperi-v1.css").read_text(encoding="utf-8")


def test_no_duplicate_layout_data() -> None:
    html = (ROOT / "scioperi/index.html").read_text(encoding="utf-8")
    assert "mit-2026-" not in html
    assert html.count("/assets/data/scioperi.json") == 1  # fallback noscript


def test_installer_idempotence() -> None:
    source = (ROOT / "tools/install-scioperi.py").read_text(encoding="utf-8")
    namespace = {"__name__": "installer_test"}
    exec(compile(source, "install-scioperi.py", "exec"), namespace)
    fixture = '<nav class="mx-index" aria-label="Menu principale"><a href="/">Home</a></nav>'
    first, changed = namespace["insert_menu_link"](fixture)
    second, changed_again = namespace["insert_menu_link"](first)
    assert changed and not changed_again
    assert first == second
    assert first.count('href="/scioperi/"') == 1


def run() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
        print(f"OK {test.__name__}")
    print(f"\n{len(tests)} controlli completati con successo.")


if __name__ == "__main__":
    run()
