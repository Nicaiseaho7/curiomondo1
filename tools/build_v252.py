#!/usr/bin/env python3
"""Publish the Aragón MotoGP story and prepare CurioMondo v252."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re

from PIL import Image
from lxml import etree, html


ROOT = Path(__file__).resolve().parents[1]
VERSION = 252
SOURCE_IMAGE = ROOT.parent / "generated-v252" / "marc-marquez-aragon-motogp-editorial.png"
SLUG = "marc-marquez-vince-aragon-secondo-mondiale-30-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Márquez fa il pieno ad Aragón: secondo nel Mondiale, Martín ora è a 19 punti"
EXCERPT = ("Il pilota Ducati vince anche il GP dopo la Sprint, supera Bezzecchi nella classifica iridata "
           "e riduce a 19 punti il distacco dal leader Jorge Martín.")
CATEGORY = "Sport / MotoGP"
PUBLISHED = "2026-08-30T14:49:00+02:00"
UPDATED = PUBLISHED
DATE_LABEL = "2026-08-30"
IMAGE_KEY = "marc-marquez-aragon-motogp-30-agosto-2026-ai-v252"
IMAGE_DIR = "/assets/images/editorial-v252"
IMAGE_ALT = ("Scena editoriale contestuale ordinaria ultrarealistica di Marc Márquez nel paddock "
             "del MotorLand Aragón accanto a una Ducati MotoGP")
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
PROMPT = ("Use case: photorealistic-natural. CurioMondo sports-news hero, 1536x1024 landscape. "
          "Original ultra-realistic ordinary contextual editorial scene of recognizable public figure Marc Márquez "
          "standing calmly in the MotorLand Aragón paddock beside a technically plausible red Ducati MotoGP bike. "
          "Red racing suit, helmet under one arm, relevant Ducati and MotoGP visual cues and logos allowed, Spanish "
          "circuit grandstands softly blurred in the background, natural cinematic afternoon light, sharp face, natural "
          "skin and anatomy, credible professional sports-photo composition. No crash, overtaking, podium, trophy, "
          "celebration, fabricated race action, text, headline, watermark or documentary claim.")

BODY = [
    "Marc Márquez ha vinto il Gran Premio di Aragón e ha completato un fine settimana perfetto dopo il successo nella Sprint del sabato. Il pilota Ducati, partito dalla seconda casella, ha superato Marco Bezzecchi durante la gara e ha poi mantenuto il comando fino alla bandiera a scacchi. Pedro Acosta ha portato la KTM al secondo posto, mentre Bezzecchi ha chiuso terzo con l’Aprilia dopo essere scattato dalla pole position.",
    "Alle spalle del podio, Álex Márquez ha terminato quarto e Jorge Martín quinto. Fermín Aldeguer, Fabio Di Giannantonio e Diogo Moreira hanno occupato le posizioni successive; Enea Bastianini e Jack Miller hanno completato la top ten. Francesco Bagnaia è invece uscito dalla corsa dopo una caduta nelle prime fasi, senza incidere sulla lotta per la vittoria.",
    "L’effetto più importante riguarda il Mondiale piloti. Márquez sale a 237 punti e scavalca Bezzecchi, fermo a 232, conquistando la seconda posizione. Martín conserva la leadership con 256 punti, ma il suo margine sul rivale Ducati si riduce a 19 lunghezze. La classifica non assegna valore speciale al sorpasso fra i due durante la gara: è la somma dei punti ottenuti in Sprint e Gran Premi a determinare l’ordine generale.",
    "Il bottino pieno di un weekend MotoGP vale 37 punti: 12 al vincitore della Sprint e 25 a chi conquista la gara della domenica. La Sprint è una corsa più breve, assegna punti soltanto ai primi nove e non sostituisce il Gran Premio. Vincere entrambe le prove permette quindi di recuperare molto terreno in una sola tappa del calendario, come accaduto ad Aragón con Márquez rispetto a Martín e Bezzecchi.",
    "Per lo spagnolo è la terza vittoria consecutiva della stagione e l’ottava in carriera al MotorLand Aragón. Il circuito di Alcañiz gira in senso antiorario, una configurazione sulla quale Márquez ha storicamente costruito alcuni dei suoi risultati migliori. Il nuovo successo conferma quel rapporto favorevole con la pista, ma assume un peso ulteriore perché arriva nel momento in cui la corsa al titolo entra nella sua fase decisiva.",
    "Bezzecchi aveva aperto il fine settimana con un segnale fortissimo: in qualifica aveva fissato il nuovo record del tracciato in 1:44.962, diventando il primo pilota a scendere sotto il minuto e 45 secondi al MotorLand. La pole non garantisce però punti per il campionato e non protegge la posizione nella gara; indica soltanto il miglior tempo di qualifica e assegna la casella di partenza più avanzata.",
    "Il prossimo appuntamento è il Gran Premio di San Marino, previsto il 13 settembre. Martín arriverà ancora da leader, mentre Márquez avrà l’occasione di verificare se la rimonta di Aragón può proseguire su un circuito differente. Bezzecchi resta pienamente coinvolto con cinque punti di ritardo dal secondo posto: la lotta non è diventata un duello, ma ora comprende tre piloti separati da 24 punti.",
]

SOURCES = [
    ("https://www.reuters.com/sports/ducatis-marquez-completes-aragon-sweep-cut-martins-title-lead-2026-08-30/",
     "Reuters — vittoria, ordine d’arrivo, classifica iridata e statistiche di Márquez ad Aragón"),
    ("https://www.adnkronos.com/sport/",
     "Adnkronos Sport — risultato del GP di Aragón, top ten e prossimo appuntamento"),
    ("https://www.motogp.com/en/gp-results/2026/ara/motogp/rac/classification",
     "MotoGP — risultati e classifica ufficiale del Gran Premio di Aragón"),
]

RELATED = [
    ("/notizie/leao-lascia-milan-galatasaray-istanbul-29-agosto-2026.html", "Sport · Calcio", "Leão lascia il Milan e arriva a Istanbul per il Galatasaray"),
    ("/notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.html", "Sport · Ciclismo", "Pogačar fuori dalla Vuelta: la caduta che ribalta la corsa"),
    ("/notizie/perche-400-800-1500-stile-libero-strategie-diverse.html", "Sport · Come funziona", "Perché le gare di mezzofondo richiedono strategie così diverse"),
]


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def dump(path: Path, value: object, compact: bool = False) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=None if compact else 2,
                      separators=(",", ":") if compact else None)
    write(path, text + ("" if compact else "\n"))


def create_images() -> list[dict]:
    target_dir = ROOT / IMAGE_DIR.lstrip("/")
    target_dir.mkdir(parents=True, exist_ok=True)
    variants = []
    with Image.open(SOURCE_IMAGE) as image:
        source = image.convert("RGB")
        for width in (480, 800, 1200):
            height = round(width * 2 / 3)
            target = target_dir / f"{IMAGE_KEY}-{width}.webp"
            source.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=88, method=6)
            variants.append({"w": width, "src": f"{IMAGE_DIR}/{IMAGE_KEY}-{width}.webp",
                             "sha256": sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
    return variants


def entry() -> dict:
    return {
        "title": TITLE, "excerpt": EXCERPT, "url": URL, "section": CATEGORY,
        "dateISO": UPDATED, "dateLabel": DATE_LABEL,
        "image": f"{IMAGE_DIR}/{IMAGE_KEY}-800.webp", "imageAlt": IMAGE_ALT,
        "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"{IMAGE_DIR}/{IMAGE_KEY}-{w}.webp {w}w" for w in (480, 800, 1200)),
    }


def article_html() -> str:
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": TITLE,
        "description": EXCERPT, "datePublished": PUBLISHED, "dateModified": UPDATED,
        "mainEntityOfPage": CANONICAL, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; somiglianza sintetica di personaggio pubblico, non fotografia documentaria.",
    }
    body = "".join(f"<p>{escape(p)}</p>" for p in BODY)
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in SOURCES)
    related = "".join(f'<a href="{u}"><small>{escape(section)}</small><strong>{escape(title)}</strong></a>' for u, section, title in RELATED)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CANONICAL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"><meta property="og:image:alt" content="{escape(IMAGE_ALT, quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=252"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{SLUG}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{CATEGORY}</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">30 agosto 2026 · Sport / MotoGP · aggiornato alle 14:49 · <span id="readTime">3 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false"><picture><img src="../assets/images/editorial-v252/{IMAGE_KEY}-800.webp" srcset="../assets/images/editorial-v252/{IMAGE_KEY}-480.webp 480w, ../assets/images/editorial-v252/{IMAGE_KEY}-800.webp 800w, ../assets/images/editorial-v252/{IMAGE_KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> Marc Márquez vince Aragón MotoGP 2026</div><div><strong>URL SEO:</strong> {URL}</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>237</b><small>i punti di Márquez nel Mondiale</small></div><div><b>19</b><small>il distacco dal leader Martín</small></div><div><b>37</b><small>i punti conquistati nel weekend</small></div></div></section><article class="art-body" data-length-policy="2000-4500">{body}</article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Risultato e classifica sono aggiornati alla conclusione del Gran Premio di Aragón del 30 agosto 2026.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=252" defer></script></body></html>'''


def restore_preexisting_unique_image() -> None:
    """Undo the v250 accidental image reuse on the older Spain story."""
    p = ROOT / "notizie/spagna-controlli-viaggiatori-italia-disputa-migrazione-8-agosto-2026.html"
    text = p.read_text(encoding="utf-8")
    text = text.replace("/assets/images/editorial-v250/italia-spagna-controlli-photo-", "/assets/images/editorial-v210/spagna-controlli-v210-")
    text = text.replace("../assets/images/editorial-v250/italia-spagna-controlli-photo-", "../assets/images/editorial-v210/spagna-controlli-v210-")
    write(p, text)


def update_data(variants: list[dict]) -> list[dict]:
    item = entry()
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home_data = json.loads(home_path.read_text(encoding="utf-8"))
    home_data["version"] = VERSION
    home_data["items"] = [x for x in home_data["items"] if x.get("url") != URL]
    home_data["items"].append(item)
    home_data["items"].sort(key=lambda x: x.get("dateISO", ""), reverse=True)
    dump(home_path, home_data, compact=True)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    search["version"] = VERSION
    search["items"] = [x for x in search["items"] if x.get("url") != URL]
    search["items"].insert(0, {k: item[k] for k in ("title", "excerpt", "url", "section")})
    dump(search_path, search, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    current = {
        "key": IMAGE_KEY, "article": URL, "aiGenerated": True,
        "syntheticLikeness": "public-figure", "publicFigure": "Marc Márquez",
        "sensitiveContext": False, "documentaryPhoto": False, "prompt": PROMPT,
        "variants": variants, "alt": IMAGE_ALT, "disclosure": CAPTION,
        "portraitOnly": False, "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False,
    }
    registry["items"] = [current] + [x for x in registry.get("items", []) if x.get("article") != URL]
    dump(registry_path, registry)
    return home_data["items"]


def picture(item: dict, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (f'<picture><img alt="{escape(item.get("imageAlt", ""), quote=True)}" decoding="async" '
            f'loading="{loading}" height="533" sizes="(max-width:600px) 79vw,300px" '
            f'src="{escape(item.get("image", ""), quote=True)}" srcset="{escape(item.get("srcset", ""), quote=True)}" '
            f'width="800"{priority}></picture>')


def update_home(items: list[dict]) -> None:
    news = [x for x in items if x.get("url", "").startswith("/notizie/")]
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    tracks = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]
    for track_index, track in enumerate(tracks):
        for child in list(track): track.remove(child)
        for item in news[:10]:
            link = etree.SubElement(track, "a", href=item["url"])
            link.set("class", "ticker-news")
            if track_index == 1: link.set("tabindex", "-1")
            link.text = item["title"]

    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for child in list(rail): rail.remove(child)
    for item in news[:5]:
        fragment = (f'<a class="auto-card" href="{item["url"]}">{picture(item)}<div class="abody">'
                    f'<div class="ameta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3>'
                    f'<p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>')
        rail.append(html.fragment_fromstring(fragment))

    cards = doc.xpath('//div[@id="cards"]')[0]
    for child in list(cards): cards.remove(child)
    for item in news[5:23]:
        fragment = (f'<a class="card" href="{item["url"]}">{picture(item)}<div class="body">'
                    f'<div class="meta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3>'
                    f'<p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>')
        cards.append(html.fragment_fromstring(fragment))

    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", re.sub(r"[?&]v=\d+", "?v=252", script.get("src") or ""))
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_archive_and_live(items: list[dict]) -> None:
    news = [x for x in items if x.get("url", "").startswith("/notizie/")]
    archive_path = ROOT / "notizie/index.html"
    doc = html.fromstring(archive_path.read_text(encoding="utf-8"))
    ul = doc.xpath("//main//ul")[0]
    for child in list(ul): ul.remove(child)
    for item in news:
        li = etree.SubElement(ul, "li")
        link = etree.SubElement(li, "a", href=item["url"])
        strong = etree.SubElement(link, "strong"); strong.text = item["title"]
        span = etree.SubElement(link, "span"); span.text = item["dateLabel"]
    paragraphs = doc.xpath("//main/p")
    if paragraphs: paragraphs[0].text = f"{len(news)} articoli, ordinati per data."
    write(archive_path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-30T12:49:00+00:00"
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"],
                      "source": "CurioMondo", "article_exists": True} for x in news[:10]]
    dump(live_path, live)


def update_xml() -> None:
    # RSS
    feed_path = ROOT / "feed.xml"
    tree = etree.parse(str(feed_path))
    channel = tree.getroot().find("channel")
    assert channel is not None
    for old in list(channel.findall("item")):
        if old.findtext("link") == CANONICAL: channel.remove(old)
    node = etree.Element("item")
    for tag, value in (("title", TITLE), ("link", CANONICAL), ("guid", CANONICAL),
                       ("pubDate", format_datetime(datetime.fromisoformat(PUBLISHED))), ("description", EXCERPT)):
        child = etree.SubElement(node, tag); child.text = value
    first_item = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    channel.insert(first_item, node)
    tree.write(str(feed_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    def append_url(path: Path, news_mode: bool) -> None:
        ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        tree = etree.parse(str(path)); root = tree.getroot()
        if any((x.text or "") == CANONICAL for x in root.xpath('//*[local-name()="loc"]')): return
        url = etree.SubElement(root, f"{{{ns}}}url")
        loc = etree.SubElement(url, f"{{{ns}}}loc"); loc.text = CANONICAL
        if news_mode:
            nns = "http://www.google.com/schemas/sitemap-news/0.9"
            news = etree.SubElement(url, f"{{{nns}}}news")
            publication = etree.SubElement(news, f"{{{nns}}}publication")
            name = etree.SubElement(publication, f"{{{nns}}}name"); name.text = "CurioMondo"
            language = etree.SubElement(publication, f"{{{nns}}}language"); language.text = "it"
            date = etree.SubElement(news, f"{{{nns}}}publication_date"); date.text = PUBLISHED
            title = etree.SubElement(news, f"{{{nns}}}title"); title.text = TITLE
        else:
            lastmod = etree.SubElement(url, f"{{{ns}}}lastmod"); lastmod.text = "2026-08-30"
        tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    append_url(ROOT / "sitemap.xml", False)
    append_url(ROOT / "news-sitemap.xml", True)


def update_release(variants: list[dict]) -> None:
    release_path = ROOT / "RELEASE-STATE.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({"currentVersion": VERSION, "baselineVersion": 251, "site_version": VERSION,
                    "version": str(VERSION), "baseline_version": 251,
                    "baseline": "curiomondo-v251-30-agosto-2026-domanda-identita-netlify.zip",
                    "date": "2026-08-30", "release_date": "2026-08-30",
                    "articleCount": 197, "generatedEditorialImages": 77,
                    "last_update": "marquez-aragon-motogp-v252",
                    "designRestored": "Nuovo articolo MotoGP con hero IA originale; homepage, LIVE e indici riallineati."})
    dump(release_path, release)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"site_version": VERSION, "baseline_version": 251, "version": str(VERSION),
                  "date": "2026-08-30", "release_date": "2026-08-30",
                  "baseline": "curiomondo-v251-30-agosto-2026-domanda-identita-netlify.zip",
                  "last_update": "marquez-aragon-motogp-v252",
                  "performance_pass": "Nuova immagine WebP responsive 480/800/1200; homepage e feed aggiornati senza immagini duplicate."})
    dump(state_path, state)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = "v252"
    manifest["release_version"] = "v252"
    manifest["last_release_date"] = "2026-08-30"
    manifest["last_release"] = {"version": VERSION, "date": "2026-08-30", "baseline_version": 251,
                                "news_added": [SLUG], "news_updated": [],
                                "daily_question_preserved": manifest["daily_state"]["last_question_slug"],
                                "image_policy_applied": "ordinary-public-figure-contextual-editorial-scene-v252"}
    dump(manifest_path, manifest)

    notes = f'''# CurioMondo v252 — 30 agosto 2026\n\n- Pubblicato “{TITLE}”.\n- Integrati risultato del GP, classifica iridata aggiornata e spiegazione del sistema di punteggio Sprint + gara.\n- Creata una nuova immagine editoriale ultrarealistica e contestuale di Marc Márquez, dichiarata come illustrazione IA non documentaria.\n- Aggiornati LIVE, Ultime notizie, homepage, archivio, ricerca, feed RSS, sitemap e news sitemap.\n- “Ultima ora” resta sulla catastrofe Nepal–Tibet per maggiore priorità editoriale; Márquez entra al primo posto tra le notizie di oggi.\n- Ripristinata l’immagine originale dell’articolo Spagna del 7 agosto, eliminando un riuso accidentale preesistente.\n'''
    write(ROOT / "RELEASE-NOTES-v252.md", notes)

    predeploy_path = ROOT / "tools/predeploy.py"
    text = predeploy_path.read_text(encoding="utf-8")
    text = text.replace('"""CurioMondo v251 static pre-deploy audit."""', '"""CurioMondo v252 static pre-deploy audit."""')
    text = text.replace("report={'version':251", "report={'version':252")
    write(predeploy_path, text)


def main() -> None:
    if not SOURCE_IMAGE.exists():
        raise SystemExit(f"Missing generated image: {SOURCE_IMAGE}")
    variants = create_images()
    write(ROOT / f"notizie/{SLUG}.html", article_html())
    dump(ROOT / f"contenuti/notizie/{SLUG}.json", {
        "slug": SLUG, "title": TITLE, "excerpt": EXCERPT, "category": CATEGORY,
        "published_at": PUBLISHED, "updated_at": UPDATED, "body": BODY,
        "related": [u for u, _, _ in RELATED],
        "sources": [{"url": u, "label": label} for u, label in SOURCES],
        "image": {"key": IMAGE_KEY, "alt": IMAGE_ALT, "ai_generated": True,
                  "synthetic_likeness": "public-figure", "public_figure": "Marc Márquez",
                  "sensitive_context": False, "portrait_format": "contextual-editorial-scene",
                  "documentary_photo": False, "disclosure": CAPTION},
    })
    restore_preexisting_unique_image()
    items = update_data(variants)
    update_home(items)
    update_archive_and_live(items)
    update_xml()
    update_release(variants)
    print(json.dumps({"version": VERSION, "added": SLUG,
                      "bodyCharacters": len(" ".join(BODY)), "variants": variants},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
