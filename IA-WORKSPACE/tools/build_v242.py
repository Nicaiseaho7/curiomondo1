#!/usr/bin/env python3
"""Publish the verified Nancy Grace Roman launch story in CurioMondo v242."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path

from PIL import Image
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-89eeef5d-eaaa-42e6-86b1-3c50c58cdeab.png"
SLUG = "nancy-grace-roman-lancio-telescopio-nasa-30-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Nancy Grace Roman, domani il lancio: il telescopio NASA che mapperà miliardi di galassie"
EXCERPT = ("NASA e SpaceX puntano al decollo domenica 30 agosto alle 13:26 italiane con un Falcon Heavy. "
           "Roman studierà energia oscura, materia oscura, esopianeti e miliardi di galassie.")
CATEGORY = "Ultima ora · Scienza / Spazio / Astronomia"
PUBLISHED = "2026-08-29T22:24:00+02:00"
UPDATED = "2026-08-29T22:24:00+02:00"
DATE_LABEL = "2026-08-29"
IMAGE_KEY = "nancy-grace-roman-telescopio-spazio-galassie-29-agosto-2026-ai"
IMAGE_DIR = "/assets/images/editorial-v242"
IMAGE_ALT = "Visualizzazione editoriale del telescopio spaziale Nancy Grace Roman tra galassie lontane"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
PROMPT = ("CurioMondo science-news hero, landscape 3:2. Original ultra-premium photorealistic editorial visualization of the "
          "Nancy Grace Roman-inspired space observatory near the Sun-Earth L2 region, with Earth small in the distance, subtle "
          "gravitational-lensing arcs, distant galaxies and suggested exoplanetary systems. Deep navy, indigo, cyan and warm-gold "
          "palette. No launch, explosion, people, NASA or SpaceX logos, flags, text, numbers, watermark or documentary claim.")

BODY = [
    "Il Nancy Grace Roman Space Telescope è pronto al passaggio più delicato della sua storia: lasciare la Terra. NASA e SpaceX puntano al decollo non prima delle 7:26 del mattino EDT di domenica 30 agosto, le 13:26 in Italia, dal Launch Complex 39A del Kennedy Space Center in Florida. Il telescopio viaggerà a bordo di un Falcon Heavy. La formula «non prima di» è importante: indica un obiettivo ufficiale, non la garanzia che il lancio avvenga esattamente a quell’ora.",
    "La missione ha superato venerdì la Launch Readiness Review, il controllo finale con cui NASA e SpaceX hanno verificato lo stato del razzo, dell’osservatorio, delle squadre e delle condizioni operative. Dopo la revisione Roman è stato dichiarato «go» per il lancio. Il meteo resta però una variabile reale: gli specialisti della Space Force prevedono al momento una probabilità del 60% di condizioni favorevoli. Un rinvio, se necessario, sarebbe quindi una normale misura di sicurezza e non il segnale di un guasto.",
    "La diretta NASA inizierà alle 6:20 EDT, cioè alle 12:20 italiane, mentre il decollo è previsto poco più di un’ora dopo. Roman partirà dal pad 39A, lo stesso complesso legato a molte missioni storiche statunitensi e oggi utilizzato da SpaceX. Il telescopio è già stato racchiuso nella carenatura protettiva e integrato con il Falcon Heavy, che dovrà portarlo fuori dall’atmosfera e inserirlo sulla traiettoria iniziale verso la sua destinazione scientifica.",
    "Dopo la separazione dal razzo, Roman comincerà un viaggio verso il secondo punto di Lagrange del sistema Sole-Terra, chiamato L2, a circa 1,6 milioni di chilometri dal nostro pianeta. È la stessa regione dello spazio utilizzata dal James Webb Space Telescope, anche se i due osservatori seguiranno orbite ampie e resteranno ben distanti. In quel punto l’equilibrio tra gravità e moto consente di mantenere una posizione relativamente stabile consumando meno propellente.",
    "Roman non è stato progettato per sostituire Hubble o Webb, ma per osservare il cosmo in modo complementare. Unirà una visione nitida nell’infrarosso a un campo inquadrato almeno cento volte più grande di quello di Hubble. In pratica potrà fotografare porzioni enormi di cielo mantenendo un dettaglio elevato. Questa combinazione permetterà di costruire mappe statistiche su scale che richiederebbero tempi molto più lunghi a un telescopio con un campo ristretto.",
    "Uno degli obiettivi principali riguarda l’energia oscura, il nome dato alla componente ancora sconosciuta associata all’espansione accelerata dell’universo. Roman osserverà la distribuzione e l’evoluzione di un numero enorme di galassie e supernove, cercando segnali capaci di distinguere tra diversi modelli cosmologici. Non vedrà direttamente l’energia oscura: misurerà con grande precisione gli effetti che la sua presenza dovrebbe lasciare nella geometria e nella storia del cosmo.",
    "La materia oscura sarà studiata soprattutto attraverso la sua influenza gravitazionale. La luce proveniente da galassie lontane può essere deformata dalla massa incontrata lungo il percorso, producendo il fenomeno della lente gravitazionale. Analizzando queste deformazioni su vaste aree, gli astronomi potranno ricostruire mappe della materia invisibile e capire meglio come essa abbia guidato la formazione delle strutture cosmiche. Le sottili distorsioni diventano così uno strumento per misurare ciò che non emette luce.",
    "Un altro grande programma sarà dedicato agli esopianeti. Roman userà il microlensing gravitazionale, osservando temporanei aumenti di luminosità quando un sistema planetario passa davanti a una stella più lontana. Il metodo è particolarmente utile per censire pianeti che orbitano a distanze diverse dalla propria stella e popolazioni difficili da individuare con le tecniche più comuni. L’obiettivo non è soltanto trovare nuovi mondi, ma capire quanto siano frequenti i differenti tipi di sistema planetario nella Via Lattea.",
    "A bordo ci saranno il Wide Field Instrument, destinato alle grandi campagne di osservazione, e il Coronagraph Instrument, una dimostrazione tecnologica progettata per bloccare la luce abbagliante di una stella e rendere più visibili gli oggetti deboli nelle sue vicinanze. Il coronografo non è l’unico cuore scientifico della missione, ma potrà provare tecnologie utili ai futuri osservatori incaricati di analizzare direttamente pianeti simili alla Terra attorno ad altre stelle.",
    "La scala dei dati sarà una parte decisiva dell’esperimento. NASA prevede che Roman mapperà miliardi di galassie e renderà disponibili le osservazioni alla comunità scientifica dopo l’elaborazione. Questo modello consentirà a gruppi diversi di usare gli stessi archivi per ricerche non previste oggi: buchi neri, stelle esplosive, piccoli corpi del Sistema solare e fenomeni rari potranno emergere mentre il telescopio esegue le sue grandi survey. Il valore di Roman dipenderà anche dalle scoperte inattese nascoste in quelle immagini.",
    "La missione primaria è prevista per cinque anni, con l’obiettivo di arrivare a dieci. Prima della scienza regolare, però, serviranno il lancio, il viaggio verso L2, l’attivazione dei sistemi, il raffreddamento e una lunga fase di calibrazione. Domani non arriveranno quindi fotografie di galassie o nuovi pianeti: il decollo, se confermato, aprirà una sequenza di verifiche tecniche necessarie prima che l’osservatorio possa iniziare il proprio programma.",
    "L’orario da ricordare per l’Italia è dunque 13:26 di domenica 30 agosto, con copertura NASA dalle 12:20. Fino all’accensione dei motori, orario, meteo e condizioni operative possono cambiare. Se il Falcon Heavy partirà come previsto, inizierà una missione costruita per osservare l’universo non soltanto più in profondità, ma su una scala molto più ampia: dalla struttura invisibile del cosmo ai pianeti che orbitano intorno ad altre stelle."
]

SOURCES = [
    ("https://www.nasa.gov/news-release/nasa-sets-coverage-for-roman-space-telescope-launch-from-florida/", "NASA — orario, diretta, Falcon Heavy, destinazione L2 e obiettivi della missione"),
    ("https://science.nasa.gov/blogs/roman/2026/08/28/nasas-roman-space-telescope-go-for-launch/", "NASA Roman Blog — esito della Launch Readiness Review e probabilità meteo"),
    ("https://science.nasa.gov/missions/roman-space-telescope/9-things-to-know-about-nasas-nancy-grace-roman-space-telescope/", "NASA Science — campo visivo, materia oscura, energia oscura, esopianeti e dati pubblici"),
    ("https://www.spacex.com/launches/roman", "SpaceX — pagina ufficiale della missione Roman e obiettivo di lancio"),
]

RELATED = [
    ("/notizie/sole-immagini-dettaglio-inouye-telescope.html", "Scienza · Astronomia", "La superficie del Sole fotografata con un dettaglio senza precedenti"),
    ("/notizie/cina-rinvia-missione-lunare-change-7-ghiaccio-24-agosto-2026.html", "Spazio · Esplorazione", "Cina, rinviata Chang’e-7: slitta la missione verso il polo sud lunare"),
    ("/notizie/come-si-arriva-a-1000-lanci-spaziali-anno.html", "Spazio · Approfondimento", "Come si può arrivare a 1.000 lanci spaziali all’anno?"),
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


def feed_entry() -> dict:
    return {
        "title": TITLE, "excerpt": EXCERPT, "url": URL, "section": CATEGORY,
        "dateISO": UPDATED, "dateLabel": DATE_LABEL,
        "image": f"{IMAGE_DIR}/{IMAGE_KEY}-800.webp", "imageAlt": IMAGE_ALT,
        "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"{IMAGE_DIR}/{IMAGE_KEY}-{w}.webp {w}w" for w in (480, 800, 1200)),
    }


def article_html() -> str:
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": TITLE, "description": EXCERPT,
        "datePublished": PUBLISHED, "dateModified": UPDATED, "mainEntityOfPage": CANONICAL, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; somiglianza sintetica di personaggio pubblico, non fotografia documentaria.",
    }
    body = "".join(f"<p>{escape(p)}</p>" for p in BODY)
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in SOURCES)
    related = "".join(f'<a href="{u}"><small>{escape(section)}</small><strong>{escape(title)}</strong></a>' for u, section, title in RELATED)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CANONICAL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"><meta property="og:image:alt" content="{escape(IMAGE_ALT, quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=241"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{SLUG}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(CATEGORY)}</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">29 agosto 2026 · Italia / Media / Politica · aggiornato alle 22:02 · <span id="readTime">5 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’articolo</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false" data-portrait-format="contextual-editorial-scene"><picture><img src="../assets/images/editorial-v241/{IMAGE_KEY}-800.webp" srcset="../assets/images/editorial-v241/{IMAGE_KEY}-480.webp 480w, ../assets/images/editorial-v241/{IMAGE_KEY}-800.webp 800w, ../assets/images/editorial-v241/{IMAGE_KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> Rai rimuove Sigfrido Ranucci da Report</div><div><strong>URL SEO:</strong> {URL}</div><div>Immagine generata con intelligenza artificiale a scopo illustrativo.</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>9 anni</b><small>alla conduzione di Report</small></div><div><b>2</b><small>i nuovi conduttori annunciati</small></div><div><b>3</b><small>le alternative professionali offerte</small></div></div></section><article class="art-body" data-length-policy="5000-7000">{body}</article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Le accuse di influenza politica sono attribuite ai rispettivi esponenti; la Rai motiva la scelta con il rafforzamento dell’inchiesta e la valorizzazione di nuovi professionisti.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=241" defer></script></body></html>'''


def article_html() -> str:
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": TITLE, "description": EXCERPT,
        "datePublished": PUBLISHED, "dateModified": UPDATED, "mainEntityOfPage": CANONICAL, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; non fotografia documentaria.",
    }
    body = "".join(f"<p>{escape(p)}</p>" for p in BODY)
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in SOURCES)
    related = "".join(f'<a href="{u}"><small>{escape(section)}</small><strong>{escape(title)}</strong></a>' for u, section, title in RELATED)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CANONICAL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"><meta property="og:image:alt" content="{escape(IMAGE_ALT, quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=242"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{SLUG}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(CATEGORY)}</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">29 agosto 2026 · Scienza / Spazio / Astronomia · aggiornato alle 22:24 · <span id="readTime">5 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’articolo</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true"><picture><img src="..{IMAGE_DIR}/{IMAGE_KEY}-800.webp" srcset="..{IMAGE_DIR}/{IMAGE_KEY}-480.webp 480w, ..{IMAGE_DIR}/{IMAGE_KEY}-800.webp 800w, ..{IMAGE_DIR}/{IMAGE_KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> lancio telescopio Nancy Grace Roman</div><div><strong>URL SEO:</strong> {URL}</div><div>Immagine generata con intelligenza artificiale a scopo illustrativo.</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>13:26</b><small>l’orario previsto in Italia</small></div><div><b>60%</b><small>meteo favorevole stimato</small></div><div><b>100×</b><small>il campo visivo rispetto a Hubble</small></div></div></section><article class="art-body" data-length-policy="5000-7000">{body}</article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. L’orario è un obiettivo «non prima di» e può cambiare in base a meteo, condizioni tecniche e decisioni operative.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=242" defer></script></body></html>'''


def update_json_data(variants: list[dict]) -> None:
    entry = feed_entry()
    for filename in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = 242
        items = [x for x in data["items"] if x.get("url") != URL]
        value = entry if "home-feed" in filename else {k: entry[k] for k in ("title", "excerpt", "url", "section")}
        items.insert(0, value)
        data["items"] = items
        dump(path, data, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = 242
    current = {
        "key": IMAGE_KEY, "article": URL, "aiGenerated": True,
        "documentaryPhoto": False, "prompt": PROMPT,
        "variants": variants, "alt": IMAGE_ALT, "disclosure": CAPTION,
        "portraitOnly": False, "reenactedEvent": False,
    }
    registry["items"] = [current] + [x for x in registry["items"] if x.get("article") != URL]
    dump(registry_path, registry)

    dates_path = ROOT / "contenuti/notizie/_publication_dates.json"
    dates = json.loads(dates_path.read_text(encoding="utf-8"))
    dates[SLUG] = {"datePublished": PUBLISHED, "contentType": "news"}
    dump(dates_path, dict(sorted(dates.items())))

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-29T20:24:00+00:00"
    feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"],
                      "source": "CurioMondo", "article_exists": True} for x in feed if x["url"].startswith("/notizie/")][:10]
    dump(live_path, live)


def picture_markup(item: dict, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (f'<picture><img alt="{escape(item["imageAlt"], quote=True)}" decoding="async" loading="{loading}" '
            f'height="533" sizes="(max-width:600px) 79vw,300px" src="{item["image"]}" '
            f'srcset="{item["srcset"]}" width="800"{priority}/></picture>')


def auto_card(item: dict) -> etree._Element:
    return html.fragment_fromstring(
        f'<a class="auto-card" href="{item["url"]}">{picture_markup(item)}<div class="abody"><div class="ameta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3><p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'
    )


def regular_card(item: dict) -> etree._Element:
    return html.fragment_fromstring(
        f'<a class="card" href="{item["url"]}">{picture_markup(item)}<div class="body"><div class="meta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3><p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'
    )


def update_home() -> None:
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]
    entry = feed_entry()

    tracks = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')
    news_items = [x for x in feed if x["url"].startswith("/notizie/")][:10]
    for track_index, track in enumerate(tracks[:2]):
        for child in list(track):
            track.remove(child)
        for item in news_items:
            a = etree.Element("a", href=item["url"])
            a.set("class", "ticker-news")
            a.text = item["title"]
            if track_index == 1:
                a.set("tabindex", "-1")
            track.append(a)

    featured = doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
    new_featured = html.fragment_fromstring(
        f'<a class="featured" href="{URL}">{picture_markup(entry, eager=True)}<div class="txt"><span class="tag">Ultima ora</span><h1>{escape(TITLE)}</h1><p>{escape(EXCERPT)}</p><span class="cta">Leggi l’articolo →</span></div></a>'
    )
    featured.getparent().replace(featured, new_featured)

    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for node in rail.xpath(f'./a[@href="{URL}"]'):
        rail.remove(node)
    rail.insert(0, auto_card(entry))
    dropped = []
    while len(rail.xpath('./a')) > 5:
        node = rail.xpath('./a')[-1]
        dropped.append(node.get("href"))
        rail.remove(node)

    cards = doc.xpath('//div[@id="cards"]')[0]
    for dropped_url in dropped:
        if cards.xpath(f'./a[@href="{dropped_url}"]'):
            continue
        item = next((x for x in feed if x.get("url") == dropped_url and "image" in x), None)
        if item:
            cards.insert(0, regular_card(item))
    while len(cards.xpath('./a')) > 18:
        cards.remove(cards.xpath('./a')[-1])

    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", "/assets/js/home-v210.js?v=242")
    if len(doc.xpath('//*[@id="universo-curiomondo-title"]/*[contains(@class,"cm-universe-title-line")]')) != 2:
        raise RuntimeError("La centratura strutturale v240 di Universo CurioMondo è stata alterata")
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_archive_and_xml() -> None:
    archive_path = ROOT / "notizie/index.html"
    archive = html.fromstring(archive_path.read_text(encoding="utf-8"))
    ul = archive.xpath('//main//ul')[0]
    for li in ul.xpath(f'./li[a/@href="{URL}"]'):
        ul.remove(li)
    ul.insert(0, html.fragment_fromstring(f'<li><a href="{URL}"><strong>{escape(TITLE)}</strong><span>{DATE_LABEL}</span></a></li>'))
    lead = archive.xpath('//main/p')[0]
    lead.text = f"{len(ul.xpath('./li'))} articoli, ordinati per data."
    write(archive_path, "<!doctype html>" + html.tostring(archive, encoding="unicode", method="html"))

    parser = etree.XMLParser(remove_blank_text=False)
    feed_path = ROOT / "feed.xml"
    feed = etree.parse(str(feed_path), parser)
    channel = feed.getroot().find("channel")
    for item in list(channel.findall("item")):
        if item.findtext("link") == CANONICAL:
            channel.remove(item)
    item = etree.Element("item")
    for name, value in (("title", TITLE), ("link", CANONICAL), ("guid", CANONICAL),
                        ("pubDate", format_datetime(datetime.fromisoformat(UPDATED))), ("description", EXCERPT)):
        child = etree.SubElement(item, name)
        child.text = value
    first = channel.find("item")
    channel.insert(channel.index(first), item)
    feed_path.write_bytes(etree.tostring(feed, encoding="utf-8", xml_declaration=True, pretty_print=True))

    sitemap_path = ROOT / "sitemap.xml"
    sitemap = etree.parse(str(sitemap_path), parser)
    sns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    for node in sitemap.xpath('//s:url[s:loc=$loc]', namespaces={"s": sns}, loc=CANONICAL):
        node.getparent().remove(node)
    node = etree.Element(f"{{{sns}}}url")
    etree.SubElement(node, f"{{{sns}}}loc").text = CANONICAL
    etree.SubElement(node, f"{{{sns}}}lastmod").text = DATE_LABEL
    etree.SubElement(node, f"{{{sns}}}changefreq").text = "daily"
    etree.SubElement(node, f"{{{sns}}}priority").text = "0.9"
    sitemap.getroot().insert(0, node)
    sitemap_path.write_bytes(etree.tostring(sitemap, encoding="utf-8", xml_declaration=True, pretty_print=True))

    news_path = ROOT / "news-sitemap.xml"
    news = etree.parse(str(news_path), parser)
    nns = "http://www.google.com/schemas/sitemap-news/0.9"
    for old in news.xpath('//s:url[s:loc=$loc]', namespaces={"s": sns}, loc=CANONICAL):
        old.getparent().remove(old)
    url = etree.Element(f"{{{sns}}}url")
    etree.SubElement(url, f"{{{sns}}}loc").text = CANONICAL
    news_node = etree.SubElement(url, f"{{{nns}}}news")
    publication = etree.SubElement(news_node, f"{{{nns}}}publication")
    etree.SubElement(publication, f"{{{nns}}}name").text = "CurioMondo"
    etree.SubElement(publication, f"{{{nns}}}language").text = "it"
    etree.SubElement(news_node, f"{{{nns}}}publication_date").text = PUBLISHED
    etree.SubElement(news_node, f"{{{nns}}}title").text = TITLE
    news.getroot().insert(0, url)
    news_path.write_bytes(etree.tostring(news, encoding="utf-8", xml_declaration=True, pretty_print=True))


def update_release() -> None:
    release = json.loads((ROOT / "RELEASE-STATE.json").read_text(encoding="utf-8"))
    release.update({"currentVersion": 242, "baselineVersion": 241, "status": "ready", "date": DATE_LABEL,
                    "articleCount": 191, "generatedEditorialImages": 71, "site_version": 242,
                    "version": "242", "baseline_version": 241,
                    "baseline": "curiomondo-v241-ranucci-report-29-agosto-2026-netlify.zip",
                    "last_update": "nancy-grace-roman-launch-v242",
                    "designRestored": "Centratura Universo v240 preservata; aggiunto lancio Roman con immagine IA distinta e feed completi."})
    dump(ROOT / "RELEASE-STATE.json", release)

    state = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text(encoding="utf-8"))
    state.update({"site_version": 242, "baseline_version": 241, "version": "242", "date": DATE_LABEL,
                  "baseline": "curiomondo-v241-ranucci-report-29-agosto-2026-netlify.zip",
                  "last_update": "nancy-grace-roman-launch-v242",
                  "performance_pass": "WebP 480/800/1200; LIVE 10, Ultime notizie 5; Universo v240 invariato."})
    dump(ROOT / "CURIOMONDO-RELEASE-STATE.json", state)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = 242
    manifest["site_version"] = 242
    manifest["version"] = "v242"
    manifest["release_version"] = "v242"
    manifest["last_release"] = {"version": 242, "date": DATE_LABEL, "baseline_version": 241,
                                "news_added": [SLUG], "news_updated": [],
                                "image_policy_applied": "original-editorial-space-visualization",
                                "preserved": ["universo-curiomondo-centered-v240", "nicaise-signature-style"]}
    dump(manifest_path, manifest)

    notes = f'''# CurioMondo v242 — 29 agosto 2026

- Pubblicato “{TITLE}”.
- Verificati orario, stato «go», meteo, vettore Falcon Heavy e obiettivi scientifici con NASA e SpaceX.
- Creata una nuova illustrazione editoriale IA distinta in WebP 480/800/1200 con disclosure completa.
- Aggiornati Ultima ora, cinque Ultime notizie, LIVE a dieci elementi, archivio, ricerca, feed, sitemap e Google News Sitemap.
- Mantenuta integralmente la centratura strutturale di Universo CurioMondo introdotta nella v240.
'''
    write(ROOT / "RELEASE-NOTES-v242.md", notes)


def normalize_existing_public_figure_markup() -> None:
    """Complete the explicit sensitivity declaration on the existing Leão illustration."""
    path = ROOT / "notizie/leao-lascia-milan-galatasaray-istanbul-29-agosto-2026.html"
    text = path.read_text(encoding="utf-8")
    old = 'data-synthetic-likeness="public-figure"><picture>'
    new = 'data-synthetic-likeness="public-figure" data-sensitive-context="false"><picture>'
    if old in text:
        write(path, text.replace(old, new, 1))


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
                  "synthetic_likeness": None, "sensitive_context": False,
                  "documentary_photo": False, "disclosure": CAPTION},
    })
    update_json_data(variants)
    update_home()
    update_archive_and_xml()
    update_release()
    normalize_existing_public_figure_markup()
    print(json.dumps({"version": 242, "added": SLUG, "bodyCharacters": sum(map(len, BODY)),
                      "variants": variants}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
