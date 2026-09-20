#!/usr/bin/env python3
"""Corregge correlati editoriali e invalidazione cache, senza cambiare il design."""
from __future__ import annotations

import json
import re
from pathlib import Path

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
VERSION = 450
DATE = "2026-09-20"
STAMP = "2026-09-20T07:38:00+02:00"

RELATED = {
    "australia-albanese-tim-cook-sicurezza-social-minori-20-settembre-2026": [
        ("/notizie/ue-social-media-divieto-sotto-13-anni-proposta-von-der-leyen-16-settembre-2026.html", "Politiche digitali", "EU Kids Act, adottata la proposta sul divieto social sotto i 13 anni"),
        ("/notizie/come-funziona-coppa-privacy-minori-online.html", "Privacy digitale", "Come funziona la tutela della privacy dei minori online"),
        ("/notizie/meta-accordo-1668-miliardi-danni-minori-social-26-agosto-2026.html", "Piattaforme e minori", "Meta, accordo sulle accuse di danni ai minori"),
    ],
    "russia-elezioni-duma-voto-kamchatka-18-settembre-2026": [
        ("/notizie/russia-ripresa-colloqui-ucraina-stati-uniti-7-settembre-2026.html", "Russia e diplomazia", "Il Cremlino non esclude nuovi colloqui con Ucraina e Stati Uniti"),
        ("/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html", "Sanzioni", "Trump firma la legge sulle sanzioni a Russia e Iran"),
        ("/notizie/meloni-alleanze-sostegno-ucraina-12-settembre-2026.html", "Italia e Ucraina", "Meloni: sostegno all’Ucraina decisivo per le alleanze"),
    ],
    "cina-zona-volo-vietato-pechino-in-vigore-20-settembre-2026": [
        ("/notizie/cina-nuove-restrizioni-all-espatrio-per-proteggere-tecnologia-e-sicurezza-15-09-2026.html", "Cina e sicurezza", "Cina, nuove restrizioni all’espatrio per tecnologia e sicurezza"),
        ("/notizie/cina-industria-al-5-2-ma-consumi-e-investimenti-restano-deboli-15-09-2026.html", "Economia cinese", "Cina, industria in crescita ma consumi e investimenti restano deboli"),
        ("/notizie/cina-taiwan-forum-isole-pacifico-palau-1-settembre-2026.html", "Asia-Pacifico", "Cina, tensioni sulla presenza di Taiwan al vertice del Pacifico"),
    ],
    "giochi-asiatici-aichi-nagoya-prime-medaglie-20-settembre-2026": [
        ("/notizie/rybakina-vince-us-open-sabalenka-numero-uno-wta-13-settembre-2026.html", "Tennis internazionale", "Rybakina vince gli US Open e conquista il numero uno mondiale"),
        ("/notizie/kimi-antonelli-vince-gp-spagna-madrid-madring-13-settembre-2026.html", "Formula 1", "Antonelli vince il primo GP di Madrid e allunga nel Mondiale"),
        ("/notizie/marc-marquez-vince-aragon-secondo-mondiale-30-agosto-2026.html", "MotoGP", "Márquez vince ad Aragón e sale al secondo posto nel Mondiale"),
    ],
}


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_related(slug: str, links: list[tuple[str, str, str]]) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    sections = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," curio-related ")]')
    if not sections:
        raise SystemExit(f"sezione correlati assente: {slug}")
    section = sections[0]
    section.set("data-curated-related", "true")
    grids = section.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," curio-related-grid ")]')
    if not grids:
        raise SystemExit(f"griglia correlati assente: {slug}")
    grid = grids[0]
    for child in list(grid):
        grid.remove(child)
    for url, label, title in links:
        if not (ROOT / url.lstrip("/")).exists():
            raise SystemExit(f"correlato inesistente: {url}")
        anchor = etree.SubElement(grid, "a", href=url)
        etree.SubElement(anchor, "small").text = label
        etree.SubElement(anchor, "strong").text = title
    rendered = '<!doctype html>\n' + html.tostring(doc, encoding="unicode", method="html")
    path.write_text(rendered, encoding="utf-8")


def main() -> None:
    for slug, links in RELATED.items():
        update_related(slug, links)

    article_script = re.compile(r"curiomondo-article-v210\.js\?v=\d+")
    changed = 0
    for slug in RELATED:
        path = ROOT / "notizie" / f"{slug}.html"
        text = path.read_text(encoding="utf-8")
        updated = article_script.sub(f"curiomondo-article-v210.js?v={VERSION}", text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    for relative in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
        path = ROOT / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = VERSION
        save_json(path, data)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "related-and-cache-fix",
        "news_added": [],
        "news_updated": list(RELATED),
        "change": "Correlati editoriali preservati e cache HTML/dati impostata a rivalidazione immediata",
        "design_changed": False,
    }
    save_json(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": DATE,
            "release_date": DATE,
            "last_update": "related-cache-fix-v450",
        })
        save_json(path, state)

    save_json(ROOT / "automation/logs/editoriale-20260920T073800-Europe-Rome.json", {
        "run_at": STAMP,
        "type": "related-and-cache-fix",
        "articles_with_curated_related": list(RELATED),
        "article_pages_cache_busted": changed,
        "cache_policy": "HTML and JSON revalidate immediately; versioned static assets remain immutable",
    })
    print(json.dumps({"version": VERSION, "related_fixed": len(RELATED), "articles_cache_busted": changed}))


if __name__ == "__main__":
    main()
