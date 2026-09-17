#!/usr/bin/env python3
"""Sincronizza il secondo aggiornamento del 17 settembre alla guida cinema."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 405
SLUG = "cinema-uscite-italia-14-20-settembre-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
PUBLISHED = "2026-09-15T20:34:20+02:00"
UPDATED = "2026-09-17T11:43:30+02:00"
TITLE = "Cinema, sette uscite tra 16 e 17 settembre: film e streaming in Italia"
SUMMARY = (
    "Da The Invite a Resident Evil, Cars, Normal e due film italiani: sette titoli selezionati "
    "sono ora nelle sale. Su Netflix arrivano Monster: La storia di Lizzie Borden e Plastic Beauty."
)
SECTION = "Film e serie TV"

SOURCES = [
    "https://eaglepictures.com/resident-evil",
    "https://www.sonypictures.com/movies/residentevil8",
    "https://apnews.com/article/82a73a5e863c0b726fcbf001038323a0",
    "https://www.fandango.it/film/ritorno-a-buenos-aires/",
    "https://www.visiondistribution.it/film/dove-la-fiesta/",
    "https://www.youtube.com/watch?v=02vPLxm9PME",
    "https://www.mymovies.it/film/2026/i-figli-della-scimmia/",
    "https://www.comingsoon.it/film/normal/69204/scheda/",
    "https://www.youtube.com/watch?v=ozH3cvq6ppE",
    "https://www.netflix.com/it/title/82068293",
    "https://www.netflix.com/tudum/articles/monster-season-4-lizzie-borden-release-date-cast-news",
    "https://ew.com/charlie-hunman-teases-next-monster-story-mafia-roy-de-meo-12116493",
    "https://about.netflix.com/en/news/plasticbeauty-maintrailer-and-keyart",
    "https://www.avmagazine.it/news/cinema/netflix-tutte-le-novita-in-uscita-in-italia-a-settembre-2026_25172.html",
    "https://www.aboutamazon.com/news/entertainment/watch-neagley-reacher-prime-video",
    "https://www.primevideo.com/-/it/detail/0RZB1U1IL8TB1J9Z2UN3UF7H2C",
]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prime_feed() -> None:
    path = ROOT / "assets/data/home-feed-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data.get("items", []):
        if item.get("url") == URL:
            item.update({"title": TITLE, "excerpt": SUMMARY, "section": SECTION})
            break
    else:
        raise RuntimeError("guida cinema assente dal feed")
    write_json(path, data)


def update_state() -> None:
    state_path = ROOT / "automation/state/cinema-pending/guida-uscite-cinema-14-20-settembre-2026.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "titolo": TITLE,
        "sommario": SUMMARY,
        "categoria": SECTION,
        "category_full": SECTION,
        "updated": UPDATED,
    })
    state["verifica"].update({
        "publication_state": "updated_pending_deploy",
        "last_checked_at": UPDATED,
        "coverage_note": "Guida ampliata senza modificare la data originaria; immagine esistente conservata perché ancora pertinente.",
        "valore_aggiunto": [
            "Correzione dell'elenco con quattro uscite italiane verificate aggiuntive",
            "Distinzione tra prima uscita, riedizione e disponibilità streaming in Italia",
        ],
    })
    write_json(state_path, state)

    write_json(ROOT / "contenuti/notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": TITLE,
        "excerpt": SUMMARY,
        "category": SECTION,
        "published_at": PUBLISHED,
        "updated_at": UPDATED,
        "development_at": UPDATED,
        "status": "UFFICIALE",
        "status_note": "Date e territorio italiano verificati sulle fonti dei distributori e su programmazioni editoriali correnti.",
        "sources": SOURCES,
        "public_url": CANONICAL,
    })


def update_release_records() -> None:
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-update",
        "news_added": [],
        "news_updated": [SLUG],
        "change": "Guida cinema ampliata a sette uscite verificate e aggiornata per lo streaming italiano",
        "image_policy_applied": "existing-relevant-image-preserved-for-article-update",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-17",
            "release_date": "2026-09-17",
            "last_update": "cinema-uscite-italia-settimana-v405",
        })
        write_json(path, data)

    write_json(ROOT / "automation/logs/cinema-20260917T114330-Europe-Rome.json", {
        "run_at": UPDATED,
        "production_branch": "main",
        "production_base_commit": "7f852271c885298d30e7e16b34369af49331f47d",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 14,
            "distinct_domains_read": 10,
            "headlines_or_snippets_excluded_from_count": True,
            "target_reached": False,
            "note": "Conteggio prudenziale delle pagine aperte e lette; risultati di ricerca, duplicati e sole anteprime esclusi. Copertura 500 non raggiunta per limiti della sessione.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "substantive_update_existing_guide",
            "editorial_score": 8.6,
            "category": SECTION,
            "status": "UFFICIALE",
            "development_at": UPDATED,
            "sources": SOURCES,
            "public_url": CANONICAL,
            "publication_state": "pending_deploy",
        }],
        "new_publications": 0,
        "substantive_updates": 1,
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })


def qa(items: list[dict]) -> None:
    item = next(i for i in items if i["url"] == URL)
    assert item["title"] == TITLE
    assert item["excerpt"] == SUMMARY
    assert item["section"] == SECTION
    for rel in ("index.html", "notizie/index.html", "feed.xml", "sitemap.xml", "news-sitemap.xml"):
        assert TITLE in (ROOT / rel).read_text(encoding="utf-8") or rel == "sitemap.xml"
    category = ROOT / "categorie/cultura/index.html"
    assert category.exists() and TITLE in category.read_text(encoding="utf-8")


def main() -> None:
    prime_feed()
    metadata = {
        "slug": SLUG,
        "parole_chiave_titolo": ["sette uscite", "streaming in Italia"],
        "dati_chiave": [
            {"icona": "◆", "valore": "7 film", "etichetta": "selezionati in sala"},
            {"icona": "●", "valore": "2 serie", "etichetta": "in arrivo su Netflix"},
            {"icona": "↗", "valore": "8 episodi", "etichetta": "Neagley su Prime Video"},
        ],
    }
    items = site.sync_surfaces([metadata], "", VERSION)
    update_state()
    update_release_records()
    qa(items)
    position = next(i for i, item in enumerate(items, 1) if item["url"] == URL)
    print(json.dumps({"version": VERSION, "updated": URL, "feed_position": position, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
