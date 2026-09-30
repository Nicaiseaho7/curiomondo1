#!/usr/bin/env python3
"""Ripara e completa il pacchetto quotidiano del 30 settembre 2026.

La domanda pubblicata coincide con la voce canonica n. 1013. Questa procedura
corregge la registrazione della fonte e sostituisce il collegamento provvisorio
con un eBook dedicato, senza rigenerare la homepage o le notizie.
"""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re

from lxml import etree, html

import build_v501_daily as shared
from daily_question_auto import site_header
from publish_daily_question_20260930 import PACKAGE as ANSWER_PACKAGE
from v722_content import PACKAGE as BOOK_PACKAGE


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-30"
DATE_LABEL = "30 settembre 2026"
QUESTION_NUMBER = 1013
QUESTION = "Se il successo non fosse visibile a nessuno, quale obiettivo continueresti a inseguire?"
SLUG = "se-il-successo-non-fosse-visibile-a-nessuno-quale-obiettivo-continueresti-a-inseguire"
QUESTION_URL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"


def render_long_book() -> str:
    pages = []
    for index, page in enumerate(BOOK_PACKAGE["book_pages"]):
        body = "".join(f"<p>{escape(paragraph)}</p>" for paragraph in page["paragraphs"])
        active = " is-active" if index == 0 else ""
        hidden = "" if index == 0 else ' aria-hidden="true"'
        title = f'<h1>{escape(BOOK_PACKAGE["book_title"])}</h1>' if index == 0 else ""
        pages.append(
            f'<section class="cm-book-page{active}" data-book-page{hidden}>'
            f'{title}<h2>{escape(page["title"])}</h2>{body}</section>'
        )
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(BOOK_PACKAGE["book_title"])} | eBook CurioMondo</title><meta name="description" content="{escape(BOOK_PACKAGE["book_deck"], quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="https://curiomondo.it{BOOK_URL}"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=346"><link rel="stylesheet" href="/assets/css/biblioteca-book-reader-v1.css?v=273"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><script defer src="/assets/js/ga4-v714.js"></script></head><body>{site_header()}<main class="cb-shell"><article class="cm-book-shell"><div class="cm-book-stage">{''.join(pages)}</div><nav class="cm-book-controls" aria-label="Navigazione eBook"><button data-book-prev type="button">← Indietro</button><button data-book-next type="button">Avanti →</button></nav><a class="cm-book-back" href="{QUESTION_URL}">← Torna alla Domanda del giorno</a></article></main><noscript><style>.cm-book-page{{display:block!important;min-height:0;margin-bottom:20px}}</style></noscript><script defer src="/assets/js/biblioteca-book-reader-v1.js?v=273"></script><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def repair_question_page() -> None:
    path = ROOT / QUESTION_URL.strip("/") / "index.html"
    text = path.read_text(encoding="utf-8")
    doc = html.fromstring(text)
    if QUESTION not in " ".join(doc.xpath("//h1//text()")):
        raise SystemExit("La pagina del 30 settembre non contiene la domanda canonica n. 1013")
    links = doc.xpath('//a[contains(concat(" ", normalize-space(@class), " "), " cm-daily-book-link ")]')
    if len(links) != 1:
        raise SystemExit("Collegamento eBook della risposta non riconoscibile")
    old_href = links[0].get("href")
    text = text.replace(old_href, BOOK_URL)
    text = text.replace("La misura invisibile di una vita piena", BOOK_PACKAGE["book_title"])
    path.write_text(text, encoding="utf-8")


def replace_library_card(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    doc = html.fromstring(text)
    matches = doc.xpath(f'//a[@href="{QUESTION_URL}"]')
    if len(matches) != 1:
        if BOOK_URL in text:
            return
        raise SystemExit(f"Card provvisoria non trovata in {path.relative_to(ROOT)}")
    card = matches[0]
    replacement = (
        f'<a class="cb-subcard" href="{BOOK_URL}"><span class="cb-kicker">{DATE_LABEL} · eBook</span>'
        f'<h2>{escape(BOOK_PACKAGE["book_title"])}</h2><p>{escape(BOOK_PACKAGE["book_deck"])}</p>'
        '<b>Sfoglia →</b></a>'
    )
    raw = etree.tostring(card, encoding="unicode", method="html")
    if raw not in text:
        raise SystemExit(f"Card provvisoria non sostituibile in {path.relative_to(ROOT)}")
    path.write_text(text.replace(raw, replacement, 1), encoding="utf-8")


def update_search(version: int) -> None:
    path = ROOT / "assets/data/search-index-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["items"] = [item for item in data.get("items", []) if item.get("url") not in {QUESTION_URL, BOOK_URL}]
    data["items"].insert(0, {
        "title": QUESTION,
        "excerpt": ANSWER_PACKAGE["excerpt"],
        "url": QUESTION_URL,
        "section": "Domanda del giorno",
    })
    data["items"].insert(1, {
        "title": BOOK_PACKAGE["book_title"],
        "excerpt": BOOK_PACKAGE["book_deck"],
        "url": BOOK_URL,
        "section": "Biblioteca / Vita e relazioni",
    })
    data["version"] = max(version, int(data.get("version", 0)))
    shared.dump(path, data)


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    full = f"https://curiomondo.it{BOOK_URL}"
    if full not in text:
        block = f"  <url><loc>{full}</loc><lastmod>{DATE}</lastmod><changefreq>daily</changefreq><priority>0.6</priority></url>\n"
        text = text.replace("</urlset>", block + "</urlset>")
    path.write_text(text, encoding="utf-8")


def update_feed() -> None:
    path = ROOT / "feed.xml"
    tree = etree.parse(str(path))
    channel = tree.getroot().find("channel")
    if channel is None:
        raise SystemExit("Canale RSS non trovato")
    full = f"https://curiomondo.it{BOOK_URL}"
    for item in list(channel.findall("item")):
        if item.findtext("link") == full:
            channel.remove(item)
    node = etree.Element("item")
    stamp = datetime(2026, 9, 30, 23, 58, tzinfo=ZoneInfo("Europe/Rome"))
    for tag, value in (
        ("title", BOOK_PACKAGE["book_title"]),
        ("link", full),
        ("guid", full),
        ("pubDate", format_datetime(stamp)),
        ("description", BOOK_PACKAGE["book_deck"]),
    ):
        etree.SubElement(node, tag).text = value
    first = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    channel.insert(first, node)
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def update_state(version: int) -> None:
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.setdefault("site", {}).update({"current_site_version": version, "site_version": version})
    manifest.update({"site_version": version, "version": f"v{version}", "release_version": f"v{version}"})
    daily = manifest["daily_state"]
    used = [int(number) for number in daily.get("used_question_source_numbers", [])]
    if QUESTION_NUMBER not in used:
        used.append(QUESTION_NUMBER)
    daily.update({
        "current_question_source_number": QUESTION_NUMBER,
        "used_question_source_numbers": used,
        "last_question_date": DATE,
        "last_question_slug": SLUG,
        "last_daily_package_date": DATE,
        "last_daily_guides": [],
        "last_question_ebook_url": BOOK_URL,
    })
    daily.pop("current_question_owner_override", None)
    owner_questions = [
        item for item in daily.get("used_owner_questions", [])
        if item.get("date") != DATE and item.get("slug") != SLUG
    ]
    if owner_questions:
        daily["used_owner_questions"] = owner_questions
    else:
        daily.pop("used_owner_questions", None)
    manifest["last_release"] = {
        "version": version,
        "date": DATE,
        "type": "daily-editorial-package-repair",
        "news_added": [],
        "news_updated": [],
        "daily_question_added": SLUG,
        "ebook_added": SLUG,
        "guides_added": [],
        "change": "Registrata la domanda canonica n. 1013 e pubblicato l’eBook lungo dedicato; nessuna notizia modificata.",
    }
    shared.dump(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": version,
            "site_version": version,
            "version": str(version),
            "date": DATE,
            "release_date": DATE,
            "last_daily_question_date": DATE,
            "last_update": f"daily-package-repair-v{version}",
        })
        shared.dump(path, state)

    shared.write(ROOT / f"RELEASE-NOTES-v{version}.md", f'''# CurioMondo v{version} — {DATE_LABEL}

- Corretta la registrazione della Domanda del giorno canonica n. {QUESTION_NUMBER}: “{QUESTION}”.
- Pubblicato l’eBook dedicato “{BOOK_PACKAGE["book_title"]}” con 10 capitoli.
- Corretti i collegamenti dalla risposta, dagli archivi, dalla ricerca, dal feed e dalla sitemap.
- Nessuna notizia modificata.
''')


def validate_source() -> None:
    source = json.loads((ROOT / "automation/state/daily-questions.json").read_text(encoding="utf-8"))
    match = next((item for item in source if int(item.get("number", -1)) == QUESTION_NUMBER), None)
    if not match or match.get("question") != QUESTION:
        raise SystemExit("La domanda n. 1013 non coincide con la fonte privata canonica")


def main() -> None:
    validate_source()
    words = len(re.findall(r"\S+", " ".join(
        paragraph for page in BOOK_PACKAGE["book_pages"] for paragraph in page["paragraphs"]
    )))
    chapters = len(BOOK_PACKAGE["book_pages"])
    if not 22000 <= words <= 32000 or not 8 <= chapters <= 12:
        raise SystemExit(f"eBook fuori standard: {words} parole, {chapters} capitoli")

    manifest = json.loads((ROOT / "curiomondo-site-manifest.json").read_text(encoding="utf-8"))
    versions = [
        int(manifest.get("site", {}).get("current_site_version", 0)),
        int(manifest.get("site", {}).get("site_version", 0)),
        int(manifest.get("site_version", 0)),
        int(str(manifest.get("version", "0")).lstrip("v") or 0),
    ]
    version = max(versions) + 1

    repair_question_page()
    shared.write(ROOT / BOOK_URL.strip("/") / "index.html", render_long_book())
    replace_library_card(ROOT / "biblioteca/index.html")
    replace_library_card(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html")
    update_search(version)
    update_sitemap()
    update_feed()
    update_state(version)
    print(json.dumps({
        "status": "ok",
        "version": version,
        "question_number": QUESTION_NUMBER,
        "book_words": words,
        "book_chapters": chapters,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
