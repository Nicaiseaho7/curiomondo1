#!/usr/bin/env python3
"""Domanda del giorno del 6 ottobre 2026, indicata dal proprietario.

Il PDF privato non è in questo workspace: nessun numero di fonte viene
inventato. Si collega l'eBook già pubblicato sul successo, senza ristamparlo.
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
DATE = "2026-10-06"
DATE_LABEL = "6 ottobre 2026"
QUESTION = "Che significa avere successo?"
SLUG = "che-significa-avere-successo"
QURL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = "/biblioteca/vita-relazioni/domande-per-conoscersi/se-il-successo-non-fosse-visibile-a-nessuno-quale-obiettivo-continueresti-a-inseguire/"
BOOK_TITLE = "Il successo quando nessuno guarda"
EXCERPT = "Una riflessione su traguardi, confronto e prezzo: il successo non è solo ciò che gli altri vedono, ma ciò che si riesce ancora a riconoscere come proprio."
PARAGRAPHS = [
    "Avere successo non significa soltanto arrivare in un punto che gli altri riconoscono. Un risultato può essere visibile — un incarico, un reddito, un riconoscimento — e restare estraneo a chi lo ha ottenuto. Il successo, in senso stretto, è il rapporto tra ciò che si voleva e ciò che si è disposti a sostenere per averlo. Senza questa verifica, il traguardo descrive una posizione, non una vita.",
    "Lo confondiamo spesso con il confronto. Sembra successo ciò che un ambiente sa misurare: lo stipendio, la visibilità, la velocità di una carriera. Queste misure non sono false, ma sono parziali. Dicono come un esito appare da fuori. Non dicono se è abitabile. Una promozione che toglie sonno e relazioni può essere un avanzamento e, insieme, un restringimento della giornata.",
    "Un criterio più sobrio è chiedere che cosa resta quando nessuno applaude. Se l’obiettivo continua a valere nel silenzio, tocca qualcosa di proprio: un mestiere fatto con cura, una persona accudita, una competenza che si voleva davvero. Se svanisce appena manca il pubblico, era soprattutto un modo per essere visti. Le due cose possono convivere. Il problema è non saperle più distinguere.",
    "Ogni successo ha un costo che i racconti pubblici tendono a omettere: tempo, salute, amicizie rinviate, tentativi falliti. Non ogni costo è un prezzo giusto. Avere successo può voler dire raggiungere ciò che si desiderava senza dover rinnegare, per ottenerlo, le condizioni minime di una vita che si riesce ancora a riconoscere come propria.",
    "C’è anche un successo che non si esibisce. Restare in un lavoro lento, dire no a qualcosa che avrebbe fatto bella figura, uscire da un’abitudine, tenere una relazione senza umiliarsi. Questi esiti non finiscono su un curriculum e proprio per questo rischiano di non essere contati. Contarli significa non lasciare che la definizione la scriva soltanto chi guarda da fuori.",
    "Forse avere successo significa poter dire, senza recitare, che quel risultato ci somiglia e che il prezzo pagato lo rifaremmo. Non è una formula. È una verifica. Quale traguardo stai inseguendo perché lo vuoi, e quale soltanto perché, se lo raggiungessi, qualcun altro dovrebbe ammetterlo?",
]


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
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": EXCERPT,
        "mainEntityOfPage": "https://curiomondo.it" + QURL,
        "datePublished": stamp, "dateModified": stamp,
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT", "relatedLink": "https://curiomondo.it" + BOOK_URL,
    }
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(QUESTION)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="https://curiomondo.it{QURL}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=526"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><meta property="og:type" content="article"><meta property="og:title" content="{escape(QUESTION, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="https://curiomondo.it{QURL}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/ga4-v714.js"></script></head><body class="cm-daily-page"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{DATE}">{DATE_LABEL}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{escape(QUESTION)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno">{paragraphs}<a class="cm-daily-book-link" href="{BOOK_URL}"><span><small>eBook su successo, applauso e obiettivi</small><strong>{escape(BOOK_TITLE)}</strong></span><span class="cm-daily-book-arrow" aria-hidden="true">→</span></a></article></main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit("Data Europe/Rome diversa da quella del pacchetto")
    chars = len(" ".join(PARAGRAPHS))
    if not 1000 <= chars <= 3000:
        raise SystemExit(f"Risposta fuori standard: {chars}")
    book_path = ROOT / BOOK_URL.strip("/") / "index.html"
    book = book_path.read_text(encoding="utf-8")
    if f"<h1>{BOOK_TITLE}</h1>" not in book and f">{BOOK_TITLE}<" not in book:
        raise SystemExit("eBook collegato non trovato")

    stamp = now.isoformat(timespec="seconds")
    write(ROOT / QURL.strip("/") / "index.html", page(stamp))

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    section = (
        '<section class="cm-qday" aria-label="Domanda del giorno">'
        f'<a aria-label="Scopri la Domanda del giorno del {DATE_LABEL}" class="cm-qday-link" href="{QURL}">'
        f'<div class="cm-qday-card"><time class="cm-qday-date" datetime="{DATE}"><strong>6</strong><span>OTT · 2026</span></time>'
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

    link = f'<a class="cm-book-back" href="{QURL}">Domanda del {DATE_LABEL}: {escape(QUESTION)}</a>'
    if QURL not in book:
        if "</article></main>" not in book:
            raise SystemExit("chiusura eBook non trovata")
        book = book.replace("</article></main>", link + "</article></main>", 1)
        write(book_path, book)

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
        feed = feed.replace("    <item>", item + "    <item>", 1)
        write(feed_path, feed)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = max(
        int(manifest.get("site_version", 0)),
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
        "owner_override_note": "Domanda del 6 ottobre indicata dal proprietario. Il PDF privato non era nel workspace: nessun numero di fonte è stato inventato.",
    })
    manifest["last_release"] = {
        "version": version,
        "date": DATE,
        "type": "daily-question-owner-override",
        "daily_question_added": SLUG,
        "ebook_linked": BOOK_URL,
        "ebook_created": False,
        "change": "Domanda del giorno del 6 ottobre: Che significa avere successo?",
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
            "last_update": f"domanda-che-significa-avere-successo-v{version}",
        })
        dump(path, state)
    print(json.dumps({"status": "prepared", "version": version, "chars": chars, "url": QURL}, ensure_ascii=False))


if __name__ == "__main__":
    main()
