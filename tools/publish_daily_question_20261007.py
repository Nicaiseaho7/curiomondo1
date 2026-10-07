#!/usr/bin/env python3
"""Domanda del giorno del 7 ottobre 2026, indicata dal proprietario.

Non è una diagnosi e non assegna un numero del PDF: il file privato non è
nel workspace. Le affermazioni cliniche restano quelle della scheda OMS.
"""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-07"
DATE_LABEL = "7 ottobre 2026"
QUESTION = "Cos’è la depressione e come uscirne?"
SLUG = "cos-e-la-depressione-e-come-uscirne"
QURL = f"/domanda-del-giorno/{SLUG}/"
EXCERPT = "Non è una giornata storta né una prova di volontà: che cos’è un episodio depressivo, quali cure esistono e quando chiedere aiuto subito."
PARAGRAPHS = [
    "La depressione non è una giornata storta e non è un difetto di carattere. L’Organizzazione mondiale della sanità la distingue dalle oscillazioni ordinarie dell’umore: è un disturbo in cui l’umore depresso, oppure la perdita di interesse e di piacere, resta presente per gran parte della giornata, quasi ogni giorno, per almeno due settimane. Possono aggiungersi stanchezza, sonno e appetito alterati, difficoltà a concentrarsi, sensi di colpa sproporzionati. Non tutti i segnali compaiono insieme. Riconoscerli non è una diagnosi.",
    "Uscirne non è una prova di volontà. Chiedere a qualcuno di «reagire» confonde un disturbo con una scelta. Molte persone migliorano, ma i tempi non sono gli stessi per tutti. L’OMS indica trattamenti psicologici efficaci e, quando un clinico lo ritiene indicato, farmaci antidepressivi. Quale strada serva non si decide da una pagina: lo stabilisce un medico, dopo aver distinto forma e gravità. Interrompere un farmaco di propria iniziativa può peggiorare il quadro.",
    "Alcune cose possono stare accanto alla cura, senza sostituirla. Dirlo a una persona fidata, non restare del tutto isolati, rendere il sonno un po’ più regolare, limitare l’alcol, che può appesantire l’umore e non cura. Se il corpo lo consente, anche un movimento semplice può aiutare il percorso. Nessuno di questi gesti, da solo, è una via d’uscita garantita.",
    "Se compaiono pensieri di morte, o la sensazione di non farcela più, non è un dettaglio da rimandare a domani. In Italia il numero di emergenza è il 112. Telefono Amico Italia ascolta al 02 2327 2327, tutti i giorni, 24 ore su 24: è un dialogo con un volontario, non una terapia e non un pronto soccorso. Se il rischio è immediato, il posto giusto è un servizio di emergenza.",
    "Questa pagina non fa diagnosi e non indica una cura personale. Il primo passo utile non è trovare da soli la spiegazione perfetta, ma raccontare a un medico che cosa sta accadendo, anche con poche parole. Uscirne, quando accade, è di solito un percorso accompagnato. Non un gesto improvviso e non una colpa di chi non ce la fa in un giorno.",
]
SOURCES = (
    '<aside class="art-sources" aria-label="Fonti consultate"><p><strong>Fonti consultate</strong></p><p>'
    '<a href="https://www.who.int/news-room/fact-sheets/detail/depression" rel="noopener">OMS: scheda sul disturbo depressivo</a>'
    " · "
    '<a href="https://www.telefonoamico.it/" rel="noopener">Telefono Amico Italia: ascolto al 02 2327 2327</a>'
    "</p></aside>"
)
BOOK_URL = "/biblioteca/vita-relazioni/domande-per-conoscersi/quale-paura-chiameresti-prudenza-se-dovessi-raccontarla-senza-vergogna/"
BOOK_TITLE = "Il nome onesto della paura"
BOOK_KICKER = "Non è una cura: una lettura a parte, sul nome della paura"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump(path: Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def prepend_card(path: Path, cls: str, card: str) -> None:
    text = path.read_text(encoding="utf-8")
    if QURL in text:
        return
    needle = f'<section class="{cls}">'
    if needle not in text:
        raise SystemExit(f"griglia assente: {path}")
    path.write_text(text.replace(needle, needle + card, 1), encoding="utf-8")


def page(stamp: str) -> str:
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in PARAGRAPHS)
    book = (
        f'<a class="cm-daily-book-link" href="{BOOK_URL}">'
        f"<span><small>{escape(BOOK_KICKER)}</small><strong>{escape(BOOK_TITLE)}</strong></span>"
        '<span class="cm-daily-book-arrow" aria-hidden="true">→</span></a>'
    )
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": EXCERPT,
        "mainEntityOfPage": "https://curiomondo.it" + QURL,
        "datePublished": stamp, "dateModified": stamp,
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT",
    }
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(QUESTION)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="https://curiomondo.it{QURL}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=526"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><meta property="og:type" content="article"><meta property="og:title" content="{escape(QUESTION, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="https://curiomondo.it{QURL}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/ga4-v714.js"></script></head><body class="cm-daily-page"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{DATE}">{DATE_LABEL}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{escape(QUESTION)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno">{paragraphs}{book}</article>{SOURCES}</main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit("Data Europe/Rome diversa da quella del pacchetto")
    chars = len(" ".join(PARAGRAPHS))
    if not 1000 <= chars <= 3000:
        raise SystemExit(f"Risposta fuori standard: {chars}")
    stamp = now.isoformat(timespec="seconds")
    write(ROOT / QURL.strip("/") / "index.html", page(stamp))

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    section = (
        '<section class="cm-qday" aria-label="Domanda del giorno">'
        f'<a aria-label="Scopri la Domanda del giorno del {DATE_LABEL}" class="cm-qday-link" href="{QURL}">'
        f'<div class="cm-qday-card"><time class="cm-qday-date" datetime="{DATE}"><strong>7</strong><span>OTT · 2026</span></time>'
        '<span class="cm-qday-k">Domanda del giorno</span><span class="cm-qday-cta">Scopri <i aria-hidden="true">→</i></span></div></a></section>'
    )
    home, count = re.subn(r'<section class="cm-qday"[^>]*>.*?</section>', section, home, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("card della domanda assente in homepage")
    write(ROOT / "index.html", home)

    card = (
        f'<a class="cb-subcard" href="{QURL}"><span class="cb-kicker">{DATE_LABEL} · Domanda del giorno</span>'
        f"<h2>{escape(QUESTION)}</h2><p>{escape(EXCERPT)}</p><b>Leggi →</b></a>"
    )
    prepend_card(ROOT / "domanda-del-giorno/index.html", "cb-subgrid cb-qday-grid", card)
    prepend_card(ROOT / "biblioteca/index.html", "cb-subgrid cb-qday-grid", card)
    prepend_card(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid", card)

    book_page = ROOT / BOOK_URL.strip("/") / "index.html"
    book_html = book_page.read_text(encoding="utf-8")
    back = f'<a class="cm-book-back" href="{QURL}">Domanda del {DATE_LABEL}: {escape(QUESTION)}</a>'
    if QURL not in book_html:
        marker = "</article></main>"
        if book_html.count(marker) != 1:
            raise SystemExit("chiusura eBook non univoca")
        book_page.write_text(book_html.replace(marker, back + marker, 1), encoding="utf-8")

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    search["items"] = [item for item in search["items"] if item.get("url") != QURL]
    search["items"].insert(0, {"title": QUESTION, "excerpt": EXCERPT, "url": QURL, "section": "Domanda del giorno"})
    search["version"] = int(search.get("version", 0)) + 1
    dump(search_path, search)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    loc = "https://curiomondo.it" + QURL
    if loc not in sitemap:
        block = (
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{DATE}</lastmod>\n"
            "    <changefreq>daily</changefreq>\n"
            "    <priority>0.7</priority>\n"
            "  </url>\n"
        )
        sitemap = sitemap.replace("</urlset>", block + "</urlset>", 1)
        write(ROOT / "sitemap.xml", sitemap)

    feed_path = ROOT / "feed.xml"
    feed = feed_path.read_text(encoding="utf-8")
    full = "https://curiomondo.it" + QURL
    if full not in feed:
        item = (
            "    <item>\n"
            f"      <title>{escape(QUESTION)}</title>\n"
            f"      <link>{full}</link>\n"
            f"      <guid>{full}</guid>\n"
            f"      <pubDate>{format_datetime(now)}</pubDate>\n"
            f"      <description>{escape(EXCERPT)}</description>\n"
            "    </item>\n"
        )
        if "    <item>" not in feed:
            raise SystemExit("feed senza item")
        feed = feed.replace("    <item>", item + "    <item>", 1)
        write(feed_path, feed)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = max(
        int(manifest.get("site_version") or 0),
        int(manifest["site"]["current_site_version"]),
        int(search["version"]),
    )
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    manifest.update({"site_version": version, "version": f"v{version}", "release_version": f"v{version}"})
    daily = manifest["daily_state"]
    daily.update({
        "last_question_date": DATE,
        "last_question_slug": SLUG,
        "last_question_ebook_url": BOOK_URL,
        "last_daily_package_date": DATE,
        "owner_override_question": QUESTION,
        "owner_override_note": "Domanda del 7 ottobre indicata dal proprietario. Non è una guida clinica. Il PDF privato non era nel workspace: nessun numero di fonte è stato inventato. L’eBook collegato è una lettura già pubblicata sulla paura, non una cura.",
    })
    manifest["last_release"] = {
        "version": version,
        "date": DATE,
        "type": "daily-question-owner-override",
        "daily_question_added": SLUG,
        "ebook_linked": BOOK_URL,
        "ebook_created": False,
        "change": "Domanda del giorno del 7 ottobre: Cos’è la depressione e come uscirne?",
    }
    dump(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": version,
            "site_version": version,
            "version": str(version),
            "date": DATE,
            "release_date": DATE,
            "last_daily_question_date": DATE,
            "last_update": f"domanda-depressione-v{version}",
        })
        dump(path, state)
    print(json.dumps({"status": "prepared", "version": version, "chars": chars, "url": QURL}, ensure_ascii=False))


if __name__ == "__main__":
    main()
