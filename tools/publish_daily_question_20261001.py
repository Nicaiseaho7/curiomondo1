#!/usr/bin/env python3
"""Pacchetto editoriale quotidiano CurioMondo del 1 ottobre 2026."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re

from lxml import etree

import build_v501_daily as shared
from daily_question_auto import render_question_page, site_header, update_home
from v723_content import PACKAGE as BOOK_PACKAGE


ROOT = Path(__file__).resolve().parents[1]
VERSION = 722
DATE = "2026-10-01"
DATE_LABEL = "1 ottobre 2026"
QUESTION_NUMBER = 1014
QUESTION = "Quanto siamo liberi nelle scelte che facciamo per non deludere chi amiamo?"
SLUG = "quanto-siamo-liberi-nelle-scelte-che-facciamo-per-non-deludere-chi-amiamo"
QUESTION_URL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"
PACKAGE = {
    "excerpt": BOOK_PACKAGE["excerpt"],
    "book_title": BOOK_PACKAGE["book_title"],
    "book_deck": BOOK_PACKAGE["book_deck"],
    "answer_paragraphs": [
        "Siamo liberi in misura diversa, e raramente del tutto. Le persone che amiamo partecipano alle nostre scelte perché condividono tempo, progetti, denaro e conseguenze. Tenere conto di loro non significa automaticamente rinunciare a noi stessi: una responsabilità scelta può essere una forma di libertà. Il punto critico arriva quando non distinguiamo più ciò che desideriamo offrire da ciò che facciamo soltanto per evitare colpa, conflitto o perdita di approvazione.",
        "La paura di deludere contiene spesso più elementi. Può ricordarci una promessa reale, il bisogno legittimo di chi dipende da noi oppure un costo che stavamo ignorando. Ma può anche ripetere una regola antica: essere amabili significa non creare problemi, cambiare idea o prendere una direzione diversa. L’emozione è importante, ma non decide da sola se una scelta sia giusta. Occorre chiedere quale danno concreto produrrebbe e quale aspettativa, invece, verrebbe soltanto contraddetta.",
        "Una scelta è più libera quando possiamo nominarla senza mentire, ascoltare le obiezioni senza consegnare loro un veto automatico e assumerci la parte di conseguenze che ci appartiene. Se una decisione cambia stabilmente la vita comune, serve negoziazione; se riguarda soprattutto la nostra identità o il nostro corpo, le persone care possono offrire informazioni e preoccupazioni, ma non diventare proprietarie della scelta. Il confine dipende da chi pagherà davvero il costo.",
        "Deludere non equivale a ferire. Qualcuno può essere triste perché non confermiamo il futuro che immaginava, e quella tristezza merita rispetto senza trasformarsi in obbligo. Allo stesso tempo, chiamare libertà una decisione che scarica lavoro, debiti o rischi sugli altri sarebbe un modo di rendere invisibile la responsabilità. Autonomia e cura non sono nemiche: diventano più credibili quando entrambe accettano di essere specifiche.",
        "Può aiutare separare tre righe: che cosa voglio, che cosa devo davvero, che cosa temo succeda se dico la verità. Poi occorre verificare i fatti. Esiste un accordo esplicito? Chi subirà conseguenze? Quali alternative riducono il costo? La relazione tollera un no, o usa silenzio, colpa e ricatto per ottenere obbedienza? Se sono presenti violenza o dipendenza grave, la libertà non si costruisce con una conversazione più coraggiosa, ma cercando prima sicurezza e sostegno competente.",
        "Essere liberi senza smettere di appartenere significa accettare che una scelta onesta non renderà tutti contenti. Possiamo comunicare con gentilezza, modificare ciò che è negoziabile e restare fermi su ciò che riguarda la nostra voce. La misura non è quanta delusione evitiamo, ma se il rapporto permette a più volontà di esistere. Un passo concreto può essere formulare una preferenza, indicare il costo che ci assumiamo e fissare un momento in cui verificare insieme gli effetti reali.",
    ],
}


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


def add_feed_entries(dt: datetime) -> None:
    path = ROOT / "feed.xml"
    tree = etree.parse(str(path))
    channel = tree.getroot().find("channel")
    if channel is None:
        raise SystemExit("Canale RSS non trovato")
    entries = [
        (QUESTION, QUESTION_URL, PACKAGE["excerpt"]),
        (PACKAGE["book_title"], BOOK_URL, PACKAGE["book_deck"]),
    ]
    urls = {f"https://curiomondo.it{url}" for _, url, _ in entries}
    for item in list(channel.findall("item")):
        if item.findtext("link") in urls:
            channel.remove(item)
    first = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    for title, url, description in entries:
        node = etree.Element("item")
        full = f"https://curiomondo.it{url}"
        for tag, value in (
            ("title", title), ("link", full), ("guid", full),
            ("pubDate", format_datetime(dt)), ("description", description),
        ):
            etree.SubElement(node, tag).text = value
        channel.insert(first, node)
        first += 1
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def update_search() -> None:
    path = ROOT / "assets/data/search-index-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["items"] = [item for item in data.get("items", []) if item.get("url") not in {QUESTION_URL, BOOK_URL}]
    data["items"].insert(0, {"title": QUESTION, "excerpt": PACKAGE["excerpt"], "url": QUESTION_URL, "section": "Domanda del giorno"})
    data["items"].insert(1, {"title": PACKAGE["book_title"], "excerpt": PACKAGE["book_deck"], "url": BOOK_URL, "section": "Biblioteca / Vita e relazioni"})
    data["version"] = VERSION
    shared.dump(path, data)


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for url, priority in ((QUESTION_URL, "0.7"), (BOOK_URL, "0.6")):
        full = f"https://curiomondo.it{url}"
        if full not in text:
            block = f"  <url><loc>{full}</loc><lastmod>{DATE}</lastmod><changefreq>daily</changefreq><priority>{priority}</priority></url>\n"
            text = text.replace("</urlset>", block + "</urlset>")
    path.write_text(text, encoding="utf-8")


def validate() -> tuple[int, int, int]:
    source = json.loads((ROOT / "automation/state/daily-questions.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "curiomondo-site-manifest.json").read_text(encoding="utf-8"))
    used = {int(number) for number in manifest["daily_state"].get("used_question_source_numbers", [])}
    expected = next((item for item in source if int(item.get("number", -1)) not in used), None)
    if not expected or int(expected.get("number", -1)) != QUESTION_NUMBER or expected.get("question") != QUESTION:
        raise SystemExit("La domanda non coincide con la prossima voce canonica non utilizzata")
    answer_chars = len(" ".join(PACKAGE["answer_paragraphs"]))
    words = len(re.findall(r"\S+", " ".join(
        paragraph for page in BOOK_PACKAGE["book_pages"] for paragraph in page["paragraphs"]
    )))
    chapters = len(BOOK_PACKAGE["book_pages"])
    if not 1000 <= answer_chars <= 3000:
        raise SystemExit(f"Risposta fuori standard: {answer_chars} caratteri")
    if not 22000 <= words <= 32000 or not 8 <= chapters <= 12:
        raise SystemExit(f"eBook fuori standard: {words} parole, {chapters} capitoli")
    return answer_chars, words, chapters


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit(f"Data Europe/Rome inattesa: {now.date().isoformat()}")
    answer_chars, words, chapters = validate()

    page = render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL)
    page = page.replace("biblioteca-v1.css?v=346", "biblioteca-v1.css?v=526")
    page = page.replace("<small>Continua la riflessione</small>", "<small>Libertà, legami e scelte condivise</small>")
    page = page.replace("<strong>Leggi l'eBook collegato</strong>", f'<strong>{escape(PACKAGE["book_title"])}</strong>')
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": PACKAGE["excerpt"],
        "mainEntityOfPage": f"https://curiomondo.it{QUESTION_URL}",
        "datePublished": now.isoformat(timespec="seconds"),
        "dateModified": now.isoformat(timespec="seconds"),
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT", "isPartOf": {"@type": "WebSite", "name": "CurioMondo", "url": "https://curiomondo.it/"},
        "relatedLink": f"https://curiomondo.it{BOOK_URL}",
    }
    page = page.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script><script defer src="/assets/js/ga4-v714.js"></script></head>')
    shared.write(ROOT / QUESTION_URL.strip("/") / "index.html", page)
    shared.write(ROOT / BOOK_URL.strip("/") / "index.html", render_long_book())
    update_home(SLUG, now, DATE_LABEL)

    shared.prepend_card(
        ROOT / "domanda-del-giorno/index.html", "cb-qday-grid",
        f'<a class="cb-subcard" href="{QUESTION_URL}"><span class="cb-kicker">{DATE_LABEL}</span><h2>{escape(QUESTION)}</h2><p>{escape(PACKAGE["excerpt"])}</p><b>Leggi →</b></a>',
        QUESTION_URL,
    )
    book_card = f'<a class="cb-subcard" href="{BOOK_URL}"><span class="cb-kicker">{DATE_LABEL} · eBook</span><h2>{escape(PACKAGE["book_title"])}</h2><p>{escape(PACKAGE["book_deck"])}</p><b>Sfoglia →</b></a>'
    shared.prepend_card(ROOT / "biblioteca/index.html", "cb-qday-grid", book_card, BOOK_URL)
    shared.prepend_card(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid", book_card, BOOK_URL)
    update_search()
    update_sitemap()
    add_feed_entries(now)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.setdefault("site", {}).update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
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
    manifest["last_release"] = {
        "version": VERSION, "date": DATE, "type": "daily-editorial-package",
        "news_added": [], "news_updated": [], "daily_question_added": SLUG,
        "ebook_added": SLUG, "guides_added": [],
        "change": "Domanda canonica n. 1014 ed eBook lungo dedicato; riparato anche il pacchetto canonico n. 1013 senza modificare notizie.",
    }
    shared.dump(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
            "date": DATE, "release_date": DATE, "last_daily_question_date": DATE,
            "last_update": f"daily-package-v{VERSION}",
        })
        shared.dump(path, state)

    shared.write(ROOT / f"RELEASE-NOTES-v{VERSION}.md", f'''# CurioMondo v{VERSION} — {DATE_LABEL}

- Pubblicata la Domanda del giorno canonica n. {QUESTION_NUMBER}: “{QUESTION}”.
- Pubblicato l’eBook dedicato “{PACKAGE["book_title"]}” con {chapters} capitoli e {words} parole.
- Riparato il pacchetto del 30 settembre: la domanda n. 1013 ora ha il proprio eBook ed è registrata correttamente.
- Aggiornati homepage, risposta, Biblioteca, archivi, ricerca, feed, sitemap, manifest e stati di rilascio.
- Nessuna notizia modificata.
''')
    print(json.dumps({
        "status": "ok", "version": VERSION, "question_number": QUESTION_NUMBER,
        "answer_characters": answer_chars, "book_words": words, "book_chapters": chapters,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
