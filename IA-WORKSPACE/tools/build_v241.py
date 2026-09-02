#!/usr/bin/env python3
"""Publish the verified Ranucci/Report story in CurioMondo v241."""
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
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-8fb4491c-f8af-4545-98a1-9bb13d5d2a8a.png"
SLUG = "rai-rimuove-sigfrido-ranucci-conduzione-report-29-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Rai rimuove Sigfrido Ranucci dalla conduzione di Report dopo nove anni: esplode lo scontro politico sulla libertà di stampa"
EXCERPT = ("La conduzione passa a Giulia Presutti e Daniele Piervincenzi. Ranucci annuncia una battaglia per la libertà di stampa, "
           "mentre opposizione e maggioranza si dividono sull’indipendenza del servizio pubblico.")
CATEGORY = "Ultima ora · Italia / Media / Politica"
PUBLISHED = "2026-08-29T15:12:00+02:00"
UPDATED = "2026-08-29T22:02:00+02:00"
DATE_LABEL = "2026-08-29"
IMAGE_KEY = "sigfrido-ranucci-report-studio-editoriale-29-agosto-2026-ai"
IMAGE_DIR = "/assets/images/editorial-v241"
IMAGE_ALT = "Ritratto editoriale sintetico di Sigfrido Ranucci in uno studio televisivo d’inchiesta"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
PROMPT = ("Use case: photorealistic-natural. CurioMondo breaking-news hero, landscape 3:2. Original ultra-realistic editorial "
          "illustration of Italian investigative journalist Sigfrido Ranucci in a refined public-television investigative newsroom, "
          "dark navy and cool-blue light, blurred cameras and empty anchor desk. Recognizable neutral and dignified synthetic likeness, "
          "dark suit and open-collar white shirt, serious resilient expression. No text, caption, logo, RAI or Report mark, party symbol, "
          "explosion, violence, watermark or fabricated specific act. Editorial illustration, not documentary photography.")

BODY = [
    "La Rai ha annunciato che Sigfrido Ranucci non condurrà più Report, il programma d’inchiesta che guidava da nove anni. Dalla prossima stagione la conduzione sarà affidata a Giulia Presutti e Daniele Piervincenzi, entrambi giornalisti risultati vincitori della selezione Rai per professionisti. La decisione, comunicata nella tarda serata di venerdì 28 agosto, ha trasformato in un caso politico nazionale una scelta presentata dall’azienda come l’apertura di una nuova fase editoriale.",
    "Ranucci ha reagito affermando che non sarà più alla guida della trasmissione ma continuerà la sua «lotta per la libertà di stampa». Ha definito la scelta un arretramento per il programma e ha respinto l’idea che la vicenda possa essere ridotta a una normale rotazione televisiva. Il giornalista resta dipendente Rai e vicedirettore ad personam: l’azienda gli ha prospettato tre possibilità di ricollocazione, in RaiNews, al Tg3 oppure come corrispondente in una sede estera.",
    "La versione ufficiale della Rai non cita pressioni politiche né le controversie recenti. L’azienda sostiene di voler rafforzare il giornalismo investigativo e valorizzare giovani professionisti attraverso una conduzione a due. Presutti e Piervincenzi non sono presentati come figure esterne imposte al programma, ma come giornalisti selezionati con un concorso Rai e con esperienza sul campo. Questa è la motivazione dichiarata e deve essere distinta dalle interpretazioni politiche che si sono sovrapposte nelle ore successive.",
    "Le opposizioni leggono invece la rimozione come un attacco all’indipendenza del servizio pubblico. La segretaria del Partito democratico Elly Schlein e altri esponenti del centrosinistra sostengono che indebolire Report fosse da tempo un obiettivo della destra, anche in vista delle elezioni previste nel 2027. Dalla maggioranza è arrivata la valutazione opposta: Matteo Salvini ha definito corretta la decisione, mentre il presidente del Senato Ignazio La Russa ha espresso soddisfazione dopo avere criticato più volte la linea editoriale della trasmissione.",
    "La reazione più delicata per la Rai è arrivata dall’interno. I giornalisti di Report hanno definito la scelta inaccettabile e hanno avvertito che numerosi componenti della redazione potrebbero lasciare se l’azienda non tornerà sui propri passi. Non è ancora una dimissione collettiva né la chiusura del programma, ma è un segnale concreto sul futuro della squadra: una trasmissione investigativa dipende dalla continuità delle fonti, dalla memoria delle inchieste e dalla fiducia costruita tra autori, inviati e redazione.",
    "Il conflitto riapre un problema strutturale della Rai. Il consiglio di amministrazione e i vertici del servizio pubblico sono scelti attraverso meccanismi che coinvolgono governo e Parlamento. Questo non dimostra, da solo, che ogni decisione editoriale venga ordinata dall’esecutivo; spiega però perché ogni cambio ai vertici di una testata o di un programma politicamente sensibile venga letto anche attraverso i rapporti di forza della maggioranza del momento. La vulnerabilità percepita nasce dal sistema di governance, non soltanto dal nome del conduttore rimosso.",
    "Report occupa una posizione particolare nel panorama televisivo italiano perché unisce audience nazionale, tempi lunghi di lavorazione e inchieste su politica, imprese, criminalità organizzata e centri di potere. Il programma fu ideato e condotto da Milena Gabanelli fino al 2016. Ranucci, entrato nella squadra nel 2006, ne è diventato autore e conduttore nel dicembre 2016. Nei nove anni successivi il suo volto è diventato quasi inseparabile dall’identità pubblica della trasmissione, anche per le numerose controversie e azioni legali nate dalle inchieste.",
    "La vicenda arriva inoltre dopo l’attentato esplosivo dell’ottobre 2025 davanti alla casa di Ranucci a Campo Ascolano, vicino Roma. L’ordigno danneggiò l’auto del giornalista e quella della figlia senza provocare feriti. In quel momento esponenti di tutti gli schieramenti espressero solidarietà e il governo annunciò un rafforzamento della scorta. Il fatto resta importante nel profilo di rischio del giornalista, ma non prova quale sia la ragione della successiva decisione Rai.",
    "Il caso ha assunto una piega ulteriore nell’agosto 2026, quando l’imprenditore Valter Lavitola, conoscente di lunga data di Ranucci, è stato arrestato e, secondo il suo avvocato, ha dichiarato ai magistrati di avere organizzato l’attentato. Le autorità non hanno trovato elementi che dimostrino una conoscenza preventiva del piano da parte di Ranucci. Questa precisazione è essenziale: le ipotesi diffuse da alcuni media su un’operazione destinata ad accrescere la sua popolarità non equivalgono a una responsabilità accertata del giornalista.",
    "L’indipendenza editoriale non significa assenza di controllo o permanenza automatica di un conduttore. Significa che nomine, rimozioni e linee dei programmi devono poter essere spiegate con criteri professionali verificabili, senza premi o punizioni legati alla convenienza dei partiti. Nel servizio pubblico la trasparenza è ancora più importante perché il finanziamento, il mandato e la governance coinvolgono direttamente i cittadini e le istituzioni. Per questo la motivazione aziendale, la reazione della redazione e le pressioni politiche devono essere valutate separatamente.",
    "Sul piano pratico, Report non è stato cancellato. La Rai annuncia la prosecuzione con due nuovi conduttori e dichiara di volerne rafforzare la funzione investigativa. Resta però da capire se Presutti e Piervincenzi lavoreranno con l’attuale squadra, quali autonomie avranno, se le inchieste già avviate andranno in onda e quanti giornalisti manterranno il proprio incarico. La continuità del titolo non garantisce automaticamente la continuità del metodo, ma nemmeno autorizza a concludere in anticipo che il programma perderà ogni capacità d’inchiesta.",
    "I prossimi passaggi misurabili saranno l’eventuale risposta formale della Rai alla redazione, le decisioni professionali di Ranucci, la composizione della squadra per la nuova stagione e le iniziative della Commissione parlamentare di vigilanza. Fino a quel momento il fatto certo è uno: dopo nove anni cambia la conduzione del principale programma investigativo del servizio pubblico. Il significato politico della scelta resta oggetto di uno scontro aperto, che dovrà essere giudicato sui documenti, sulle procedure e soprattutto su ciò che Report riuscirà ancora a trasmettere."
]

SOURCES = [
    ("https://www.reuters.com/business/media-telecom/italian-state-broadcaster-rai-removes-veteran-journalist-sparking-political-2026-08-29/", "Reuters — rimozione di Ranucci, reazioni politiche, posizione della redazione e assenza di prove sul suo coinvolgimento nell’attentato"),
    ("https://tg24.sky.it/cronaca/2026/08/28/ranucci-lavitola-report-rai-ultime-notizie", "Sky TG24 / ANSA — nota Rai, nomi dei nuovi conduttori e tre opzioni professionali offerte a Ranucci"),
    ("https://www.rai.it/programmi/report/", "Rai — profilo ufficiale di Report, carriera di Ranucci e storia della trasmissione"),
    ("https://www.reuters.com/business/media-telecom/bomb-explodes-outside-home-top-italian-investigative-journalist-2025-10-17/", "Reuters — attentato dell’ottobre 2025, danni e quadro di protezione del giornalista"),
]

RELATED = [
    ("/notizie/pd-primarie-centrosinistra-schlein-conte-26-agosto-2026.html", "Italia · Politica", "Centrosinistra, nel Pd si riapre il nodo primarie"),
    ("/notizie/meloni-consensi-giovani-under-35-13-agosto-2026.html", "Italia · Politica", "Meloni e il consenso tra i giovani: cosa mostrano davvero i dati"),
    ("/notizie/decreto-giustizia-governo-fiducia-camera.html", "Italia · Istituzioni", "Decreto giustizia, il governo pone la fiducia alla Camera"),
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


def update_json_data(variants: list[dict]) -> None:
    entry = feed_entry()
    for filename in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = 241
        items = [x for x in data["items"] if x.get("url") != URL]
        value = entry if "home-feed" in filename else {k: entry[k] for k in ("title", "excerpt", "url", "section")}
        items.insert(0, value)
        data["items"] = items
        dump(path, data, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = 241
    current = {
        "key": IMAGE_KEY, "article": URL, "aiGenerated": True,
        "syntheticLikeness": "public-figure", "publicFigure": "Sigfrido Ranucci",
        "sensitiveContext": False, "documentaryPhoto": False, "prompt": PROMPT,
        "variants": variants, "alt": IMAGE_ALT, "disclosure": CAPTION,
        "portraitOnly": False, "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False,
    }
    registry["items"] = [current] + [x for x in registry["items"] if x.get("article") != URL]
    dump(registry_path, registry)

    dates_path = ROOT / "contenuti/notizie/_publication_dates.json"
    dates = json.loads(dates_path.read_text(encoding="utf-8"))
    dates[SLUG] = {"datePublished": PUBLISHED, "contentType": "news"}
    dump(dates_path, dict(sorted(dates.items())))

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-29T20:02:00+00:00"
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
        script.set("src", "/assets/js/home-v210.js?v=241")
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
    release.update({"currentVersion": 241, "baselineVersion": 240, "status": "ready", "date": DATE_LABEL,
                    "articleCount": 190, "generatedEditorialImages": 70, "site_version": 241,
                    "version": "241", "baseline_version": 240,
                    "baseline": "curiomondo-v240-universo-centrato-CORRETTO-29-agosto-2026-netlify.zip",
                    "last_update": "ranucci-report-press-freedom-v241",
                    "designRestored": "Centratura Universo v240 preservata; aggiunto Ranucci/Report con immagine IA distinta e feed completi."})
    dump(ROOT / "RELEASE-STATE.json", release)

    state = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text(encoding="utf-8"))
    state.update({"site_version": 241, "baseline_version": 240, "version": "241", "date": DATE_LABEL,
                  "baseline": "curiomondo-v240-universo-centrato-CORRETTO-29-agosto-2026-netlify.zip",
                  "last_update": "ranucci-report-press-freedom-v241",
                  "performance_pass": "WebP 480/800/1200; LIVE 10, Ultime notizie 5; Universo v240 invariato."})
    dump(ROOT / "CURIOMONDO-RELEASE-STATE.json", state)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = 241
    manifest["site_version"] = 241
    manifest["version"] = "v241"
    manifest["release_version"] = "v241"
    manifest["last_release"] = {"version": 241, "date": DATE_LABEL, "baseline_version": 240,
                                "news_added": [SLUG], "news_updated": [],
                                "image_policy_applied": "ordinary-public-figure-contextual-editorial-scene",
                                "preserved": ["universo-curiomondo-centered-v240", "nicaise-signature-style"]}
    dump(manifest_path, manifest)

    notes = f'''# CurioMondo v241 — 29 agosto 2026

- Pubblicato “{TITLE}”.
- Verificati decisione Rai, nuovi conduttori, reazioni politiche, posizione della redazione e contesto dell’attentato del 2025.
- Creata una nuova illustrazione editoriale IA distinta in WebP 480/800/1200 con disclosure completa.
- Aggiornati Ultima ora, cinque Ultime notizie, LIVE a dieci elementi, archivio, ricerca, feed, sitemap e Google News Sitemap.
- Mantenuta integralmente la centratura strutturale di Universo CurioMondo introdotta nella v240.
'''
    write(ROOT / "RELEASE-NOTES-v241.md", notes)


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
                  "synthetic_likeness": "public-figure", "public_figure": "Sigfrido Ranucci",
                  "sensitive_context": False, "portrait_format": "contextual-editorial-scene",
                  "documentary_photo": False, "disclosure": CAPTION},
    })
    update_json_data(variants)
    update_home()
    update_archive_and_xml()
    update_release()
    normalize_existing_public_figure_markup()
    print(json.dumps({"version": 241, "added": SLUG, "bodyCharacters": sum(map(len, BODY)),
                      "variants": variants}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
