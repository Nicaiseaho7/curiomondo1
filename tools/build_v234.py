#!/usr/bin/env python3
"""Build CurioMondo v234 from the verified v233 tree."""
from __future__ import annotations

from copy import deepcopy
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
SOURCE_IMAGE = ROOT.parent / "generated-v234" / "curiomondo-usa-venezuela-oil-trump-2026.png"
SLUG = "usa-venezuela-accordo-petrolio-65-miliardi-barili-29-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Il patto dei 65 miliardi di barili: Trump annuncia il controllo USA sul petrolio venezuelano"
EXCERPT = ("Washington punta al 55% operativo di una nuova società legata a 17 giacimenti venezuelani. "
           "L’annuncio parla di oltre 65 miliardi di barili, ma testo, struttura legale e tempi restano da chiarire.")
CATEGORY = "Ultima ora · Mondo / Energia / USA–Venezuela"
PUBLISHED = "2026-08-29T19:40:00+02:00"
UPDATED = "2026-08-29T19:40:00+02:00"
DATE_LABEL = "2026-08-29"
IMAGE_KEY = "trump-usa-venezuela-petrolio-29-agosto-2026-ai"
IMAGE_DIR = "/assets/images/editorial-v234"
IMAGE_ALT = ("Scena editoriale contestuale con Donald Trump davanti a infrastrutture petrolifere "
             "e alle bandiere di Stati Uniti e Venezuela")
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
PROMPT = ("Ultra-realistic recognizable editorial likeness of Donald Trump in a contextual oil-industry setting, "
          "waist-up and serious, with Venezuelan refinery infrastructure, pumpjacks, and clearly recognizable United States "
          "and Venezuela flags in the background; ordinary non-sensitive news context. No signing, handshake, meeting, "
          "document, podium, staged negotiation, fabricated specific act, text, caption, watermark, or news logo. "
          "One coherent landscape editorial scene, disclosed synthetic likeness, not documentary photography.")

BODY = [
    "Donald Trump ha annunciato che gli Stati Uniti hanno raggiunto con il Venezuela un accordo petrolifero che, nelle sue parole, attribuirebbe a Washington il controllo maggioritario su oltre 65 miliardi di barili di riserve accertate. Reuters, Associated Press e ANSA hanno riportato l’annuncio tra il 28 e il 29 agosto. Il punto essenziale, però, è anche il principale limite informativo: il testo integrale dell’intesa non è stato reso pubblico e non sono ancora disponibili tutti i documenti societari, legali e finanziari necessari per valutarne l’attuazione.",
    "La formula «controllo su 65 miliardi di barili» non significa che quella quantità di greggio sia già passata fisicamente agli Stati Uniti o possa essere estratta subito. Indica, secondo quanto comunicato dall’amministrazione e ricostruito dalle agenzie, una partecipazione operativa in un nuovo veicolo privato collegato a una parte delle riserve venezuelane. È quindi più corretto parlare di controllo economico e operativo annunciato, non di trasferimento immediato della proprietà di tutto il petrolio contenuto nel sottosuolo.",
    "Associated Press riferisce che la struttura prospettata coinvolgerebbe il governo statunitense e un operatore ancora non identificato, con una quota effettiva del 55% della produzione dei giacimenti interessati. Washington avrebbe anche la possibilità di acquistare il greggio al costo di produzione. Sono dettagli di grande rilievo, ma al momento provengono dalla presentazione pubblica dell’accordo e dalle ricostruzioni giornalistiche: finché contratti, governance e obblighi delle parti non saranno pubblicati, non vanno trattati come un meccanismo già pienamente operativo.",
    "Il perimetro riguarderebbe 17 giacimenti. Una precedente ricostruzione di Reuters sui negoziati indicava asset distribuiti soprattutto nella Fascia dell’Orinoco e nell’area del Lago di Maracaibo, i due grandi poli dell’industria venezuelana. L’elenco definitivo, le concessioni coinvolte e la procedura con cui verrebbe scelto l’operatore non sono però stati illustrati in modo completo. Anche la relazione tra la nuova società, la compagnia statale PDVSA e gli investitori privati resta uno dei nodi da chiarire.",
    "Trump ha parlato di circa 100 miliardi di dollari di investimenti privati destinati a rilanciare pozzi, oleodotti, raffinerie, terminali e servizi tecnici. L’amministrazione ha inoltre indicato una possibile crescita molto consistente delle entrate fiscali venezuelane. Queste cifre descrivono l’obiettivo economico del piano, non denaro già impegnato o ricavi garantiti. Per trasformarsi in capitale reale serviranno operatori disposti ad assumere rischi elevati, condizioni contrattuali stabili e un quadro sanzionatorio e finanziario sufficientemente prevedibile.",
    "Qui è utile distinguere le riserve dalla produzione. Una riserva provata è una quantità di petrolio che, sulla base dei dati geologici e delle condizioni economiche e tecniche considerate, può essere recuperata con ragionevole certezza. Non equivale a un deposito pronto per la consegna. Portare quel greggio sul mercato richiede pozzi funzionanti, energia, diluenti, impianti di trattamento, oleodotti, porti, personale specializzato e manutenzione continua. È per questo che un accordo su decine di miliardi di barili può avere un peso strategico immediato ma effetti industriali molto più lenti.",
    "Secondo l’Energy Information Administration statunitense, il Venezuela possedeva circa 303 miliardi di barili di riserve provate di greggio, pari a circa il 17% del totale mondiale nei dati disponibili per il 2023. Una quota rilevante è petrolio extra-pesante della Fascia dell’Orinoco: può essere estratto e commercializzato, ma richiede processi, infrastrutture e competenze più impegnativi rispetto ai greggi leggeri. Il dato dei 65 miliardi rappresenterebbe dunque poco più di un quinto delle riserve provate nazionali, non l’intero patrimonio petrolifero venezuelano.",
    "Anni di sottoinvestimenti, guasti, sanzioni e perdita di capacità tecnica hanno ridotto l’efficienza del settore venezuelano. L’Associated Press sottolinea che, anche con nuovi capitali, non è realistico attendersi un aumento immediato dell’offerta capace di abbassare rapidamente i prezzi alla pompa. Riattivare campi maturi, riparare infrastrutture e assicurare continuità alle esportazioni richiede tempo. L’impatto sul mercato dipenderà inoltre dalla velocità degli investimenti, dalla qualità del greggio prodotto e dalla disponibilità delle raffinerie adatte a lavorarlo.",
    "L’opzione di acquistare petrolio al costo di produzione è stata collegata anche alla Strategic Petroleum Reserve, la riserva strategica federale degli Stati Uniti. La SPR non è una normale scorta commerciale: è uno strumento di sicurezza energetica pensato per rispondere a gravi interruzioni delle forniture. Un prezzo favorevole potrebbe rendere conveniente ricostituirla, ma l’annuncio non sostituisce le decisioni operative, di bilancio e logistiche necessarie per comprare, trasportare e immagazzinare effettivamente il greggio.",
    "Restano poi questioni di sovranità e diritto. Il petrolio venezuelano è soggetto alla Costituzione, alla legislazione nazionale sugli idrocarburi e al ruolo centrale dello Stato nel settore. La descrizione di un controllo statunitense maggioritario dovrà quindi essere tradotta in contratti compatibili con quelle regole o accompagnata da modifiche e autorizzazioni specifiche. Sarà decisivo capire chi deterrà le quote, chi nominerà i dirigenti, come saranno ripartiti costi e ricavi, quali controversie potranno essere arbitrate e quali garanzie saranno offerte agli investitori.",
    "La portata geopolitica dell’annuncio è amplificata dalla pressione che la guerra con l’Iran esercita sulle rotte energetiche e sul mercato del greggio. Washington avrebbe accesso privilegiato a una risorsa enorme nell’emisfero occidentale; Caracas potrebbe ottenere capitali e tecnologia per recuperare capacità produttiva. Ma questa prospettiva non elimina l’incertezza: dipende dai rapporti politici tra i due Paesi, dal regime delle sanzioni, dalla reazione degli altri partner del Venezuela e dalla capacità di mantenere gli impegni per molti anni.",
    "I prossimi segnali concreti da osservare sono la pubblicazione dell’accordo, l’identità dell’operatore, l’elenco definitivo dei 17 giacimenti, le licenze statunitensi, il calendario delle gare e i primi investimenti vincolanti. Solo allora sarà possibile misurare quanto del progetto annunciato diventerà produzione aggiuntiva e con quali tempi. Per ora la notizia è storica per l’ambizione e per il rapporto energetico che propone; i 65 miliardi di barili, il 55% operativo e i 100 miliardi di investimenti devono restare attribuiti all’annuncio e non trasformati in risultati già acquisiti."
]

SOURCES = [
    ("https://www.reuters.com/business/energy/us-enters-into-oil-agreement-with-venezuela-trump-says-2026-08-28/", "Reuters — annuncio di Trump, oltre 65 miliardi di barili e interrogativi sul quadro legale e finanziario"),
    ("https://www.reuters.com/business/energy/us-nears-deal-secure-long-term-access-venezuelas-oil-reserves-sources-say-2026-08-27/", "Reuters — negoziati sui 17 giacimenti, Fascia dell’Orinoco e Lago di Maracaibo"),
    ("https://apnews.com/article/eb0ed5a1e99602c21a7f690c3368020e", "Associated Press — nuova società, quota operativa del 55%, acquisto al costo e investimenti prospettati"),
    ("https://apnews.com/article/c229bc39b6e1a3d5dd16f7f9e67fef3f", "Associated Press — cosa significa l’intesa e perché gli effetti su produzione e prezzi non sarebbero immediati"),
    ("https://www.ansa.it/sito/notizie/topnews/2026/08/29/trump-con-il-venezuela-il-piu-grande-accordo-sul-petrolio-della-storia_f81eb1df-4b3a-4a92-9074-f2dd9ce540e0.html", "ANSA — conferma dell’annuncio e della cifra indicata dal presidente statunitense"),
    ("https://www.eia.gov/international/analysis/country/VEN", "U.S. Energy Information Administration — riserve, caratteristiche del greggio e quadro energetico del Venezuela"),
]

RELATED = [
    ("/notizie/qatarenergy-stop-gas-edison-italia-novembre-29-agosto-2026.html", "Italia · Energia", "Gas, QatarEnergy ferma altre cinque consegne a Edison"),
    ("/notizie/iran-economia-guerra-sanzioni-commercio-29-agosto-2026.html", "Medio Oriente · Economia", "Iran, guerra e sanzioni soffocano l’economia"),
    ("/notizie/hormuz-traffico-navale-leggera-ripresa-27-agosto-2026.html", "Energia · Rotte marittime", "Hormuz, traffico in lieve ripresa ma lontano dalla normalità"),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump_json(path: Path, data: object, *, compact: bool = False) -> None:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":") if compact else None, indent=None if compact else 2)
    write(path, text + ("" if compact else "\n"))


def make_images() -> list[dict]:
    out_dir = ROOT / IMAGE_DIR.lstrip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE_IMAGE) as source:
        source = source.convert("RGB")
        variants = []
        for width in (480, 800, 1200):
            height = round(width * 2 / 3)
            resized = source.resize((width, height), Image.Resampling.LANCZOS)
            target = out_dir / f"{IMAGE_KEY}-{width}.webp"
            resized.save(target, "WEBP", quality=86, method=6)
            variants.append({"w": width, "src": f"{IMAGE_DIR}/{IMAGE_KEY}-{width}.webp", "sha256": sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
    return variants


def entry() -> dict:
    return {
        "title": TITLE, "excerpt": EXCERPT, "url": URL, "section": CATEGORY,
        "dateISO": PUBLISHED, "dateLabel": DATE_LABEL,
        "image": f"{IMAGE_DIR}/{IMAGE_KEY}-800.webp", "imageAlt": IMAGE_ALT,
        "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"{IMAGE_DIR}/{IMAGE_KEY}-{w}.webp {w}w" for w in (480, 800, 1200)),
    }


def picture_html(*, featured: bool = False) -> str:
    return (f'<picture><img alt="{escape(IMAGE_ALT, quote=True)}" decoding="async" '
            f'{"fetchpriority=\"high\"" if featured else "loading=\"lazy\""} height="533" '
            f'sizes="(max-width:600px) 79vw,300px" src="{IMAGE_DIR}/{IMAGE_KEY}-800.webp" '
            f'srcset="{IMAGE_DIR}/{IMAGE_KEY}-480.webp 480w, {IMAGE_DIR}/{IMAGE_KEY}-800.webp 800w, '
            f'{IMAGE_DIR}/{IMAGE_KEY}-1200.webp 1200w" width="800"/></picture>')


def card_html(kind: str = "auto-card") -> str:
    body = "abody" if kind == "auto-card" else "body"
    meta = "ameta" if kind == "auto-card" else "meta"
    return (f'<a class="{kind}" href="{URL}">{picture_html()}<div class="{body}"><div class="{meta}">{escape(CATEGORY)}</div>'
            f'<h3>{escape(TITLE)}</h3><p>{escape(EXCERPT)}</p><time datetime="{PUBLISHED}">{DATE_LABEL}</time></div></a>')


def article_html() -> str:
    json_ld = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": TITLE, "description": EXCERPT,
        "datePublished": PUBLISHED, "dateModified": UPDATED, "mainEntityOfPage": CANONICAL, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; somiglianza sintetica di personaggio pubblico, non fotografia documentaria.",
    }
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in BODY)
    related = "".join(f'<a href="{u}"><small>{escape(s)}</small><strong>{escape(t)}</strong></a>' for u, s, t in RELATED)
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in SOURCES)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CANONICAL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"><meta property="og:image:alt" content="{escape(IMAGE_ALT, quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=234"><script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{SLUG}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(CATEGORY)}</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">29 agosto 2026 · {escape(CATEGORY)} · <span id="readTime">5 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’articolo</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false"><picture><img src="../assets/images/editorial-v234/{IMAGE_KEY}-800.webp" srcset="../assets/images/editorial-v234/{IMAGE_KEY}-480.webp 480w, ../assets/images/editorial-v234/{IMAGE_KEY}-800.webp 800w, ../assets/images/editorial-v234/{IMAGE_KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> accordo petrolio USA Venezuela 2026</div><div><strong>URL SEO:</strong> {URL}</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>65 mld</b><small>i barili indicati nell’annuncio</small></div><div><b>17</b><small>i giacimenti interessati</small></div><div><b>55%</b><small>la quota operativa effettiva prospettata</small></div></div></section><article class="art-body" data-length-policy="5000-7000">{paragraphs}<p>Per comprendere il ruolo delle restrizioni finanziarie e delle rotte marittime in questa vicenda, CurioMondo ha preparato anche l’approfondimento <a href="/notizie/come-funzionano-sanzioni-petrolio-iran-hormuz.html">come funzionano le sanzioni sul petrolio e perché Hormuz può cambiare tutto</a>.</p></article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. I termini economici sono attribuiti alle fonti e all’annuncio presidenziale; il testo completo dell’accordo non era pubblico al momento dell’aggiornamento.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=234" defer></script></body></html>'''


def update_home() -> None:
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    tracks = doc.xpath('//nav[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")] | //div[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')
    existing = []
    for a in tracks[0].xpath('./a')[:9]:
        existing.append((a.get("href"), "".join(a.itertext()).strip()))
    live = [(URL, TITLE)] + existing
    for i, track in enumerate(tracks[:2]):
        for child in list(track):
            track.remove(child)
        for href, title in live:
            a = etree.Element("a", href=href)
            a.set("class", "ticker-news")
            if i == 1:
                a.set("tabindex", "-1")
            a.text = title
            track.append(a)

    featured = doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
    replacement = html.fragment_fromstring(
        f'<a class="featured" href="{URL}">{picture_html(featured=True)}<div class="txt"><span class="tag">Ultima ora</span><h1>{escape(TITLE)}</h1><p>{escape(EXCERPT)}</p><span class="cta">Leggi l’articolo →</span></div></a>'
    )
    featured.getparent().replace(featured, replacement)

    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    rail.insert(0, html.fragment_fromstring(card_html("auto-card")))
    while len(rail.xpath('./a')) > 5:
        rail.remove(rail.xpath('./a')[-1])

    cards = doc.get_element_by_id("cards")
    cremona_url = "/notizie/cremona-tromba-aria-grandine-danni-29-agosto-2026.html"
    feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]
    cremona = next(item for item in feed if item["url"] == cremona_url)
    cremona_pic = (f'<picture><img alt="{escape(cremona["imageAlt"], quote=True)}" decoding="async" loading="lazy" height="533" '
                   f'sizes="(max-width:600px) 79vw,300px" src="{cremona["image"]}" srcset="{cremona["srcset"]}" width="800"/></picture>')
    cremona_card = (f'<a class="card" href="{cremona_url}">{cremona_pic}<div class="body"><div class="meta">{escape(cremona["section"])}</div>'
                    f'<h3>{escape(cremona["title"])}</h3><p>{escape(cremona["excerpt"])}</p><time datetime="{cremona["dateISO"]}">{cremona["dateLabel"]}</time></div></a>')
    cards.insert(0, html.fragment_fromstring(cremona_card))
    while len(cards.xpath('./a[contains(concat(" ",normalize-space(@class)," ")," card ")]')) > 17:
        cards.remove(cards.xpath('./a[contains(concat(" ",normalize-space(@class)," ")," card ")]')[-1])

    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", "/assets/js/home-v210.js?v=234")
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_data(variants: list[dict]) -> None:
    new_entry = entry()
    for filename in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = 234
        data["items"] = [new_entry] + [x for x in data["items"] if x.get("url") != URL]
        if "search-index" in filename:
            data["items"][0] = {k: new_entry[k] for k in ("title", "excerpt", "url", "section")}
        dump_json(path, data, compact=True)

    path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["version"] = 234
    for item in registry["items"]:
        if item.get("syntheticLikeness") == "public-figure" and item.get("publicFigure") == "Tadej Pogačar":
            item["sensitiveContext"] = True
    registry["items"] = [{
        "key": IMAGE_KEY, "article": URL, "aiGenerated": True,
        "syntheticLikeness": "public-figure", "publicFigure": "Donald Trump", "sensitiveContext": False,
        "documentaryPhoto": False, "prompt": PROMPT,
        "variants": variants, "alt": IMAGE_ALT, "disclosure": CAPTION,
        "portraitOnly": False, "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False,
    }] + [x for x in registry["items"] if x.get("article") != URL]
    dump_json(path, registry)

    live_path = ROOT / "automation/live-seed.json"
    live_data = json.loads(live_path.read_text(encoding="utf-8"))
    live_data["updated_at"] = "2026-08-29T17:40:00+00:00"
    home_feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]
    live_data["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"], "source": "CurioMondo", "article_exists": True} for x in home_feed[:10]]
    dump_json(live_path, live_data)


def update_archive_and_xml() -> None:
    archive = ROOT / "notizie/index.html"
    text = archive.read_text(encoding="utf-8")
    text = text.replace("187 articoli, ordinati per data.", "188 articoli, ordinati per data.")
    item = f'<li><a href="{URL}"><strong>{escape(TITLE)}</strong><span>{DATE_LABEL}</span></a></li>\n'
    text = text.replace("<ul>\n", "<ul>\n" + item, 1)
    write(archive, text)

    feed_path = ROOT / "feed.xml"
    parser = etree.XMLParser(remove_blank_text=False)
    feed = etree.parse(str(feed_path), parser)
    channel = feed.getroot().find("channel")
    node = etree.Element("item")
    for tag, value in (("title", TITLE), ("link", CANONICAL), ("guid", CANONICAL),
                       ("pubDate", format_datetime(datetime.fromisoformat(PUBLISHED))), ("description", EXCERPT)):
        child = etree.SubElement(node, tag); child.text = value
    channel.insert(0, node)
    feed_path.write_bytes(etree.tostring(feed, encoding="utf-8", xml_declaration=True, pretty_print=True))

    sitemap_path = ROOT / "sitemap.xml"
    site = etree.parse(str(sitemap_path), parser)
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    url_node = etree.Element(f"{{{ns}}}url")
    for tag, value in (("loc", CANONICAL), ("lastmod", DATE_LABEL), ("changefreq", "daily"), ("priority", "0.9")):
        child = etree.SubElement(url_node, f"{{{ns}}}{tag}"); child.text = value
    site.getroot().insert(0, url_node)
    sitemap_path.write_bytes(etree.tostring(site, encoding="utf-8", xml_declaration=True, pretty_print=True))

    news_path = ROOT / "news-sitemap.xml"
    news = etree.parse(str(news_path), parser)
    nns = "http://www.google.com/schemas/sitemap-news/0.9"
    node = etree.Element(f"{{{ns}}}url")
    loc = etree.SubElement(node, f"{{{ns}}}loc"); loc.text = CANONICAL
    news_node = etree.SubElement(node, f"{{{nns}}}news")
    publication = etree.SubElement(news_node, f"{{{nns}}}publication")
    name = etree.SubElement(publication, f"{{{nns}}}name"); name.text = "CurioMondo"
    language = etree.SubElement(publication, f"{{{nns}}}language"); language.text = "it"
    date = etree.SubElement(news_node, f"{{{nns}}}publication_date"); date.text = PUBLISHED
    title = etree.SubElement(news_node, f"{{{nns}}}title"); title.text = TITLE
    news.getroot().insert(0, node)
    news_path.write_bytes(etree.tostring(news, encoding="utf-8", xml_declaration=True, pretty_print=True))


def update_versions() -> None:
    for js in (ROOT / "assets/js/home-v210.js", ROOT / "assets/js/curiomondo-article-v210.js"):
        write(js, js.read_text(encoding="utf-8").replace("?v=233", "?v=234"))
    poga = ROOT / "notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.html"
    text = poga.read_text(encoding="utf-8")
    text = text.replace('data-synthetic-likeness="public-figure" data-portrait-format=', 'data-synthetic-likeness="public-figure" data-sensitive-context="true" data-portrait-format=')
    write(poga, text)

    release = {"currentVersion": 234, "baselineVersion": 233, "status": "ready", "date": "2026-08-29", "articleCount": 188,
               "generatedEditorialImages": 68,
               "designRestored": "Nuovo articolo USA–Venezuela; immagini contestuali per notizie ordinarie e ritratto neutrale obbligatorio solo nei contesti sensibili."}
    dump_json(ROOT / "RELEASE-STATE.json", release)
    curio = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text(encoding="utf-8"))
    curio.update({"site_version": 234, "baseline_version": 233, "version": "234", "baseline": "curiomondo-v233-29-agosto-2026-netlify.zip",
                  "last_update": "usa-venezuela-oil-agreement-and-context-sensitive-public-figure-policy-v234",
                  "performance_pass": "Nuova immagine WebP responsive 480/800/1200; homepage, LIVE, feed e indici aggiornati senza duplicare la seconda sezione."})
    dump_json(ROOT / "CURIOMONDO-RELEASE-STATE.json", curio)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site_version"] = 234; manifest["version"] = "v234"; manifest["release_version"] = "v234"
    manifest["last_release"] = {"version": 234, "date": "2026-08-29", "baseline_version": 233,
                                "news_added": [SLUG], "news_updated": [],
                                "image_policy_applied": "public-figure-contextual-ordinary-neutral-sensitive"}
    dump_json(manifest_path, manifest)

    notes = f'''# CurioMondo v234 — 29 agosto 2026\n\n- Pubblicato “{TITLE}” con attribuzione prudente dei termini non ancora accompagnati dal testo integrale dell’accordo.\n- Nuova immagine originale IA di Donald Trump in un contesto petrolifero, dichiarata come illustrazione editoriale e non come fotografia documentaria.\n- Protocollo permanente aggiornato: scene e loghi pertinenti sono ammessi per notizie ordinarie; incidente, morte, salute, violenza, tragedie e altri contesti dolorosi richiedono un ritratto neutrale isolato.\n- Homepage aggiornata: articolo in apertura, primo nelle cinque notizie recenti e primo nella LIVE; Cremona spostata in “Altre notizie” senza duplicati.\n- Feed, ricerca, archivio, sitemap e registro immagini aggiornati alla versione 234.\n'''
    write(ROOT / "RELEASE-NOTES-v234.md", notes)


def main() -> None:
    if not SOURCE_IMAGE.exists():
        raise SystemExit(f"Missing generated image: {SOURCE_IMAGE}")
    variants = make_images()
    write(ROOT / f"notizie/{SLUG}.html", article_html())
    dump_json(ROOT / f"contenuti/notizie/{SLUG}.json", {
        "slug": SLUG, "title": TITLE, "excerpt": EXCERPT, "category": CATEGORY,
        "published_at": PUBLISHED, "updated_at": UPDATED, "body": BODY,
        "evergreen": "/notizie/come-funzionano-sanzioni-petrolio-iran-hormuz.html",
        "related": [u for u, _, _ in RELATED], "sources": [{"url": u, "label": label} for u, label in SOURCES],
        "image": {"key": IMAGE_KEY, "alt": IMAGE_ALT, "ai_generated": True, "synthetic_likeness": "public-figure", "public_figure": "Donald Trump", "sensitive_context": False, "documentary_photo": False, "disclosure": CAPTION},
    })
    update_home()
    update_data(variants)
    update_archive_and_xml()
    update_versions()
    print(json.dumps({"version": 234, "slug": SLUG, "bodyCharacters": sum(len(p) for p in BODY), "images": variants}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
