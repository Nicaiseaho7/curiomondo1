#!/usr/bin/env python3
"""Notizia meteo dell'8 ottobre 2026 e domanda del giorno.

I fatti dell'allerta restano quelli del comunicato del Dipartimento e del
bollettino di vigilanza. La domanda non inventa un numero del PDF privato.
"""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from hashlib import sha256
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re
import subprocess

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-08"
DATE_LABEL = "8 ottobre 2026"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
WORD_RE = re.compile(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b")

TITLE = "Allerta meteo 8 ottobre: arancione in Toscana, gialla in 11 regioni"
EXCERPT = "Per giovedì 8 ottobre la Protezione Civile valuta allerta arancione in Toscana e gialla in undici regioni, con temporali e vento forte sul Tirreno."
ALT = "Illustrazione editoriale di un temporale autunnale su un borgo collinare e un fiume in piena; non è una fotografia documentaria."
SLUG = "allerta-meteo-arancione-toscana-8-ottobre-2026"
NEWS_URL = f"/notizie/{SLUG}.html"
STEM = f"{SLUG}-v801"
PARAGRAPHS = [
    "Giovedì 8 ottobre il Dipartimento della Protezione Civile ha valutato un’allerta arancione in Toscana e un’allerta gialla in undici regioni. Una saccatura atlantica, già su parte del Nord-Ovest, si sposta verso sud-est: interessa il Centro-Nord e parte del Sud, con i fenomeni più intensi sul versante tirrenico.",
    "L’avviso, emesso il 7 ottobre d’intesa con le regioni, decorre dalle prime ore di giovedì. Prevede piogge da sparse a diffuse, in prevalenza rovesci o temporali, su Friuli-Venezia Giulia, Umbria, Lazio e Campania settentrionale, e sui settori interni e appenninici di Abruzzo e Molise.",
    "I fenomeni possono essere accompagnati da rovesci di forte intensità, forti raffiche di vento, grandinate locali e fulmini frequenti. Spetta alle regioni attivare i sistemi di protezione civile nei territori interessati.",
    "Il giallo copre settori di Friuli-Venezia Giulia, Lombardia, Liguria, Marche, Campania e Basilicata. Riguarda invece l’intero territorio di Umbria, Lazio, Abruzzo, Molise e Puglia. L’arancione, un livello più alto, è riservato alla Toscana.",
    "Anche la sala operativa della Regione ha diramato un’allerta arancione su tutta la Toscana per temporali forti, con rischio idrogeologico e idraulico sul reticolo minore. Ricorda di non sostare in sottopassi, seminterrati e lungo i corsi d’acqua.",
    "Il bollettino di vigilanza dell’8 ottobre indica piogge da sparse a diffuse, anche temporalesche, su Liguria di Levante, Toscana, Umbria, Lazio, Campania centro-settentrionale e zone interne di Abruzzo e Molise. I quantitativi sono in genere moderati.",
    "Possono diventare elevati sul Lazio meridionale, sull’Abruzzo meridionale, sul Molise occidentale e sulla Campania settentrionale. Altrove, sul resto del Centro-Nord, sulla Campania rimanente, sulla Sardegna centro-settentrionale, sulla Puglia e sulla Basilicata settentrionale, le piogge attese sono sparse e da deboli a moderate.",
    "I venti sono localmente forti da sud-ovest sulla Liguria, sui settori tirrenici di Toscana e Lazio e sull’Appennino centro-settentrionale. Forti da ovest sulla Sardegna settentrionale. In tendenza, forti da sud sulla Puglia meridionale e sulla Calabria ionica.",
    "Risultano molto mossi il Mar Ligure, il Tirreno centro-settentrionale e il Mare di Sardegna settentrionale. In serata Ligure e Mare di Sardegna possono tendere ad agitati. Anche lo Ionio settentrionale e l’Adriatico meridionale tendono a molto mossi.",
    "Le temperature massime calano in modo localmente sensibile su Sardegna, Toscana, Umbria e Lazio. L’allerta descrive un rischio, non la pioggia già misurata in ogni comune: l’effetto cambia dove il temporale nasce e quanto resta fermo.",
    "Il Dipartimento aggiorna il quadro ogni giorno. In caso di rovesci intensi conviene seguire i canali della propria regione, insieme alle norme di comportamento pubblicate con i bollettini.",
]
SOURCES = [
    ("https://www.protezionecivile.gov.it/it/comunicato-stampa/maltempo-allerta-arancione-toscana-7/", "Dipartimento della Protezione Civile: avviso e allerte dell’8 ottobre"),
    ("https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-vigilanza/", "Bollettino di vigilanza meteorologica nazionale"),
    ("https://www.intoscana.it/it/allerta-meteo-arancione-8-ottobre-2026/", "Regione Toscana: allerta arancione per temporali forti"),
]
RELATED = [
    ("/notizie/meteo-italia-7-14-ottobre-2026.html", "Meteo Italia 7-14 ottobre: più piogge, temperature ancora miti"),
    ("/notizie/meteo-italia-5-12-ottobre-sole-in-cedimento-piogge-e-temporali-in-arrivo-05-10-2026.html", "Meteo Italia 5-12 ottobre: sole in cedimento, piogge e temporali in arrivo"),
    ("/notizie/meteo-italia-4-11-ottobre-2026.html", "Meteo 4 ottobre: sole oggi, piogge possibili nella settimana"),
]

QUESTION = "IA vs umani: chi è più intelligente?"
QSLUG = "ia-vs-umani-chi-e-piu-intelligente"
QURL = f"/domanda-del-giorno/{QSLUG}/"
QEXCERPT = "Non c’è un podio unico: dipende dal compito, e da chi risponde se l’esito è sbagliato."
QPARAS = [
    "Non esiste un unico metro che metta una persona e una macchina sulla stessa linea del traguardo. «Più intelligente» dipende da quale compito si sta misurando. Un calcolo lungo, una ricerca in un archivio enorme, la ripetizione senza stanchezza: lì la macchina vince da decenni, e non serve un modello nuovo per accorgersene.",
    "Una persona arriva in una situazione con un corpo, una storia e delle conseguenze. Capisce quando una frase è una battuta, quando un silenzio pesa, quando un numero giusto risponde alla domanda sbagliata. Può anche sbagliare proprio perché tiene insieme cose che un punteggio separa.",
    "I sistemi di intelligenza artificiale di oggi completano schemi, soprattutto linguistici, a partire da enormi quantità di esempi. Non hanno una giornata da vivere e non rispondono di ciò che dicono. Possono essere utilissimi e, nello stesso momento, sicuri di una cosa che non sta in piedi. La fluidità non è una prova di comprensione.",
    "Chiamare intelligente solo chi è più veloce sposta il confronto su un terreno già scelto dalla macchina. Chiamare intelligente solo chi prova emozioni chiude il discorso prima di guardare i compiti in cui il calcolo è davvero meglio di noi. Le due scorciatoie si somigliano: evitano di dire per che cosa.",
    "Il punto pratico non è incoronare un vincitore. È decidere quali lavori si delegano e quali no. Una bozza, un riassunto, un controllo di coerenza possono passare da una macchina. Una scelta che tocca la vita di qualcuno, una diagnosi, una condanna, un licenziamento, resta una responsabilità umana anche quando uno strumento ha preparato il materiale.",
    "Allora la domanda si gira. Non chi è più intelligente, come se esistesse un podio unico. Piuttosto: in questo compito, che cosa conta davvero, e chi ne risponde se l’esito è sbagliato?",
]
BOOK_URL = "/biblioteca/vita-relazioni/domande-per-conoscersi/una-vita-piena-si-misura-dalle-esperienze-vissute-o-dallattenzione-con-cui-le-abbiamo-attraversate/"
BOOK_TITLE = "La misura invisibile di una vita piena"
BOOK_KICKER = "Non è una classifica tra cervelli: una lettura su come si misura una vita"
IMAGE_SRC = Path("/workspace/artifacts/imagine_images/99858cbf-7464-40b5-9af5-fac30024df47.jpg")


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def insert_first(text: str, key: str, obj: dict) -> str:
    needle = f'"{key}": ['
    index = text.find(needle)
    if index < 0:
        raise SystemExit(f"array assente: {key}")
    after = index + len(needle)
    nxt = text[after:]
    line = nxt.split("\n", 1)[1]
    indent = len(line) - len(line.lstrip(" "))
    pretty = json.dumps(obj, ensure_ascii=False, indent=2)
    extra = " " * (indent - 2)
    block = "\n".join(extra + line if line else line for line in pretty.split("\n"))
    return text[:after] + "\n" + block + "," + text[after:]


def prepend_card(path: Path, cls: str, card: str, marker: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    needle = f'<section class="{cls}">'
    if needle not in text:
        raise SystemExit(f"griglia assente: {path}")
    path.write_text(text.replace(needle, needle + card, 1), encoding="utf-8")


def news_page(stamp: str) -> str:
    body = "".join(f"<p>{escape(p)}</p>" for p in PARAGRAPHS)
    related = "".join(f'<a href="{href}"><strong>{escape(title)}</strong></a>' for href, title in RELATED)
    sources = "".join(
        f'<li><a href="{href}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>'
        for href, label in SOURCES
    )
    image = f"/assets/images/editorial-auto/{STEM}"
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": TITLE, "description": EXCERPT,
        "datePublished": stamp, "dateModified": stamp,
        "mainEntityOfPage": "https://curiomondo.it" + NEWS_URL,
        "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "image": ["https://curiomondo.it" + image + "-1200.webp"],
    }
    srcset = ", ".join(f"../assets/images/editorial-auto/{STEM}-{w}.webp {w}w" for w in (480, 800, 1200))
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://curiomondo.it{NEWS_URL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="https://curiomondo.it{NEWS_URL}"><meta property="og:image" content="https://curiomondo.it{image}-1200.webp"><meta property="og:image:alt" content="{escape(ALT, quote=True)}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=800"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=736"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{SLUG}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner"><a class="cm-global-header__back" href="/" aria-label="Torna alla home"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">Mondo / Meteo</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">{DATE_LABEL} · Italia · <span id="readTime">2 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html">Redazione CurioMondo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="false"><picture><img src="../assets/images/editorial-auto/{STEM}-800.webp" srcset="{srcset}" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><strong>Arancione</strong><span>Toscana</span></div><div><strong>Gialla</strong><span>11 regioni</span></div><div><strong>8 ottobre</strong><span>giornata dell’avviso</span></div></div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">{body}</article><section class="curio-related" data-curated-related="true"><h2>Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: {DATE_LABEL}.<br>{CAPTION}</small></p></div><aside class="cm-name-card" aria-label="Un pensiero per Egídio"><p class="cm-name-card__label">Un pensiero per <strong class="cm-name-note__name">Egídio</strong></p><p class="cm-name-card__text"><span class="cm-name-note__text">Rimanda a domani ciò che oggi non cambia nulla.</span></p></aside></main><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=800" defer></script></body></html>'''


def question_page(stamp: str) -> str:
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in QPARAS)
    book = (
        f'<a class="cm-daily-book-link" href="{BOOK_URL}">'
        f"<span><small>{escape(BOOK_KICKER)}</small><strong>{escape(BOOK_TITLE)}</strong></span>"
        '<span class="cm-daily-book-arrow" aria-hidden="true">→</span></a>'
    )
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": QEXCERPT,
        "mainEntityOfPage": "https://curiomondo.it" + QURL,
        "datePublished": stamp, "dateModified": stamp,
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT",
    }
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(QUESTION)} | CurioMondo</title><meta name="description" content="{escape(QEXCERPT, quote=True)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="https://curiomondo.it{QURL}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=526"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><meta property="og:type" content="article"><meta property="og:title" content="{escape(QUESTION, quote=True)}"><meta property="og:description" content="{escape(QEXCERPT, quote=True)}"><meta property="og:url" content="https://curiomondo.it{QURL}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script defer src="/assets/js/ga4-v714.js"></script></head><body class="cm-daily-page"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{DATE}">{DATE_LABEL}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{escape(QUESTION)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno">{paragraphs}{book}</article></main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''


def make_images() -> list[dict]:
    src = Image.open(IMAGE_SRC).convert("RGB")
    folder = ROOT / "assets/images/editorial-auto"
    variants = []
    for width, height in ((480, 320), (800, 533), (1200, 800)):
        dest = folder / f"{STEM}-{width}.webp"
        image = src.resize((width, height), Image.Resampling.LANCZOS)
        image.save(dest, "WEBP", quality=82, method=6)
        data = dest.read_bytes()
        variants.append({
            "w": width, "src": f"/assets/images/editorial-auto/{STEM}-{width}.webp",
            "sha256": sha256(data).hexdigest(), "bytes": len(data),
        })
    return variants


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit("Data Europe/Rome diversa da quella del pacchetto")
    if not 55 <= len(TITLE) <= 70:
        raise SystemExit(f"titolo fuori 55–70: {len(TITLE)}")
    counts = [words(p) for p in PARAGRAPHS]
    total = sum(counts)
    if any(n > 60 for n in counts) or not 300 <= total <= 700:
        raise SystemExit(f"formato notizia non valido: {total} {counts}")
    for forbidden in ("Fonte:", "Fonti:", "abbiamo verificato", "Europe/Rome"):
        if any(forbidden.casefold() in p.casefold() for p in PARAGRAPHS):
            raise SystemExit(f"frase vietata: {forbidden}")
    qchars = len(re.sub(r"\s+", " ", " ".join(QPARAS)).strip())
    if not 1000 <= qchars <= 3000:
        raise SystemExit(f"domanda fuori 1000–3000: {qchars}")
    for href, _title in RELATED:
        if not (ROOT / href.lstrip("/")).exists():
            raise SystemExit(f"correlato assente: {href}")
    book_path = ROOT / BOOK_URL.strip("/") / "index.html"
    book = html.parse(str(book_path))
    pages = book.xpath("//*[@data-book-page]")
    book_text = re.sub(r"\s+", " ", " ".join(book.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," cm-book-stage ")]//p//text()'))).strip()
    book_words = len(re.findall(r"\S+", book_text))
    heads = book.xpath("//h2")
    if not (8 <= len(pages) <= 12 and 22000 <= book_words <= 32000 and 8 <= len(heads) <= 12):
        raise SystemExit(f"eBook non conforme: pagine {len(pages)} parole {book_words} h2 {len(heads)}")

    stamp = now.isoformat(timespec="seconds")
    variants = make_images()
    write(ROOT / NEWS_URL.lstrip("/"), news_page(stamp))
    write(ROOT / QURL.strip("/") / "index.html", question_page(stamp))

    image_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = image_path.read_text(encoding="utf-8")
    registry = registry.replace('"version": 800', '"version": 801', 1)
    registry = insert_first(registry, "items", {
        "alt": ALT,
        "prompt": "Temporale autunnale su un borgo collinare e un fiume in piena, senza persone riconoscibili, scritte o loghi.",
        "variants": variants,
        "disclosure": CAPTION,
        "generator": "Imagine",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "article": NEWS_URL,
    })
    registry = insert_first(registry, "images", {
        "slug": SLUG,
        "version": 801,
        "path": f"/assets/images/editorial-auto/{STEM}-1200.webp",
        "variants": [480, 800, 1200],
        "aiGenerated": True,
        "sensitiveContext": False,
        "disclosure": CAPTION,
        "date": DATE,
        "alt": ALT,
    })
    write(image_path, registry)

    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = feed_path.read_text(encoding="utf-8").replace('"version": 800', '"version": 801', 1)
    feed = insert_first(feed, "items", {
        "title": TITLE, "excerpt": EXCERPT, "url": NEWS_URL, "section": "Mondo / Meteo",
        "dateISO": stamp, "dateLabel": DATE,
        "image": f"/assets/images/editorial-auto/{STEM}-800.webp",
        "imageAlt": ALT, "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"/assets/images/editorial-auto/{STEM}-{w}.webp {w}w" for w in (480, 800, 1200)),
        "featuredStats": [
            {"icon": "◆", "value": "Arancione", "label": "Toscana"},
            {"icon": "▲", "value": "Gialla", "label": "11 regioni"},
            {"icon": "●", "value": "8 ottobre", "label": "giornata dell’avviso"},
        ],
        "featuredHighlights": ["allerta arancione", "Toscana"],
    })
    write(feed_path, feed)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search_text = search_path.read_text(encoding="utf-8")
    search_version = int(json.loads(search_text).get("version", 0)) + 1
    search_text = search_text.replace(f'"version": {search_version - 1}', f'"version": {search_version}', 1)
    search_text = insert_first(search_text, "items", {"title": QUESTION, "excerpt": QEXCERPT, "url": QURL, "section": "Domanda del giorno"})
    search_text = insert_first(search_text, "items", {"title": TITLE, "excerpt": EXCERPT, "url": NEWS_URL, "section": "Mondo / Meteo"})
    write(search_path, search_text)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for loc in ("https://curiomondo.it" + NEWS_URL, "https://curiomondo.it" + QURL):
        if loc not in sitemap:
            block = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{DATE}</lastmod>\n  </url>\n"
            sitemap = sitemap.replace("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">", "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + block, 1)
    write(ROOT / "sitemap.xml", sitemap)

    news_sitemap = (ROOT / "news-sitemap.xml").read_text(encoding="utf-8")
    loc = "https://curiomondo.it" + NEWS_URL
    if loc not in news_sitemap:
        block = (
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            "    <news:news>\n"
            "      <news:publication>\n"
            "        <news:name>CurioMondo</news:name>\n"
            "        <news:language>it</news:language>\n"
            "      </news:publication>\n"
            f"      <news:publication_date>{stamp}</news:publication_date>\n"
            f"      <news:title>{escape(TITLE)}</news:title>\n"
            "    </news:news>\n"
            "  </url>\n"
        )
        news_sitemap = news_sitemap.replace("<url>", block + "  <url>", 1)
        write(ROOT / "news-sitemap.xml", news_sitemap)

    feed_xml = (ROOT / "feed.xml").read_text(encoding="utf-8")
    for link, item_title, description in (
        ("https://curiomondo.it" + NEWS_URL, TITLE, EXCERPT),
        ("https://curiomondo.it" + QURL, QUESTION, QEXCERPT),
    ):
        if link not in feed_xml:
            item = (
                "    <item>\n"
                f"      <title>{escape(item_title)}</title>\n"
                f"      <link>{link}</link>\n"
                f"      <guid>{link}</guid>\n"
                f"      <pubDate>{format_datetime(now)}</pubDate>\n"
                f"      <description>{escape(description)}</description>\n"
                "    </item>\n"
            )
            feed_xml = feed_xml.replace("    <item>", item + "    <item>", 1)
    write(ROOT / "feed.xml", feed_xml)

    index = (ROOT / "notizie/index.html").read_text(encoding="utf-8")
    card = f'<li><a href="{NEWS_URL}"><strong>{escape(TITLE)}</strong><span>{DATE}</span></a></li>'
    if NEWS_URL not in index:
        index = index.replace("<li><a href=\"/notizie/", card + "<li><a href=\"/notizie/", 1)
        write(ROOT / "notizie/index.html", index)

    category = ROOT / "categorie/meteo/index.html"
    cat = category.read_text(encoding="utf-8")
    if NEWS_URL not in cat:
        cat = cat.replace('numberOfItems":19', 'numberOfItems":20', 1)
        cat = cat.replace("<strong>19 articoli</strong>", "<strong>20 articoli</strong>", 1)
        old = '{"@type":"ListItem","position":1,"url":"https://curiomondo.it/notizie/meteo-italia-7-14-ottobre-2026.html"'
        cat = cat.replace(old, '{"@type":"ListItem","position":1,"url":"https://curiomondo.it' + NEWS_URL + '","name":"' + TITLE.replace('"', "") + '"},' + old.replace('"position":1', '"position":2', 1), 1)
        thumb = (
            f'<li><a href="{NEWS_URL}"><span class="category-card-thumb">'
            f'<img src="/assets/images/editorial-auto/{STEM}-480.webp" alt="" width="112" height="75" loading="lazy" decoding="async"></span>'
            f'<span class="category-card-copy"><small>Mondo / Meteo</small><strong>{escape(TITLE)}</strong><span>{escape(EXCERPT)}</span></span></a></li>'
        )
        marker = '<li><a href="/notizie/meteo-italia-7-14-ottobre-2026.html">'
        if marker not in cat:
            raise SystemExit("card meteo assente")
        cat = cat.replace(marker, thumb + marker, 1)
        write(category, cat)

    rendered = subprocess.run(["node", "tools/render_home_editorial.js"], cwd=ROOT, check=False, text=True, capture_output=True)
    if rendered.returncode:
        raise SystemExit(rendered.stderr or rendered.stdout)
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    section = (
        '<section class="cm-qday" aria-label="Domanda del giorno">'
        f'<a aria-label="Scopri la Domanda del giorno del {DATE_LABEL}" class="cm-qday-link" href="{QURL}">'
        f'<div class="cm-qday-card"><time class="cm-qday-date" datetime="{DATE}"><strong>8</strong><span>OTT · 2026</span></time>'
        '<span class="cm-qday-k">Domanda del giorno</span><span class="cm-qday-cta">Scopri <i aria-hidden="true">→</i></span></div></a></section>'
    )
    home, count = re.subn(r'<section class="cm-qday"[^>]*>.*?</section>', section, home, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("card della domanda assente in homepage")
    write(ROOT / "index.html", home)

    qcard = (
        f'<a class="cb-subcard" href="{QURL}"><span class="cb-kicker">{DATE_LABEL} · Domanda del giorno</span>'
        f"<h2>{escape(QUESTION)}</h2><p>{escape(QEXCERPT)}</p><b>Leggi →</b></a>"
    )
    prepend_card(ROOT / "domanda-del-giorno/index.html", "cb-subgrid cb-qday-grid", qcard, QURL)
    prepend_card(ROOT / "biblioteca/index.html", "cb-subgrid cb-qday-grid", qcard, QURL)
    prepend_card(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid", qcard, QURL)
    book_html = book_path.read_text(encoding="utf-8")
    if QURL not in book_html:
        back = f'<a class="cm-book-back" href="{QURL}">Domanda del {DATE_LABEL}: {escape(QUESTION)}</a>'
        if "</article></main>" not in book_html:
            raise SystemExit("chiusura eBook assente")
        book_path.write_text(book_html.replace("</article></main>", back + "</article></main>", 1), encoding="utf-8")

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = max(
        int(manifest.get("site_version") or 0),
        int(manifest["site"]["current_site_version"]),
        search_version,
        801,
    )
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    manifest.update({"site_version": version, "version": f"v{version}", "release_version": f"v{version}"})
    daily = manifest["daily_state"]
    daily.update({
        "last_question_date": DATE,
        "last_question_slug": QSLUG,
        "last_question_ebook_url": BOOK_URL,
        "last_daily_package_date": DATE,
        "owner_override_question": QUESTION,
        "owner_override_note": "Domanda dell’8 ottobre indicata dal proprietario. Il PDF privato non era nel workspace: nessun numero di fonte è stato inventato. L’eBook collegato è una lettura già pubblicata su come si misura una vita, non un verdetto sull’intelligenza artificiale.",
    })
    manifest["last_release"] = {
        "version": version, "date": DATE, "type": "daily-question-owner-override",
        "daily_question_added": QSLUG, "news_added": SLUG,
        "ebook_linked": BOOK_URL, "ebook_created": False,
        "change": "Meteo 8 ottobre e domanda: IA vs umani, chi è più intelligente?",
    }
    write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": version, "site_version": version, "version": str(version),
            "date": DATE, "release_date": DATE, "last_daily_question_date": DATE,
            "last_update": f"meteo-e-domanda-v{version}",
        })
        write(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": "prepared", "version": version, "news_words": total,
        "paragraphs": counts, "question_chars": qchars, "stamp": stamp,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
