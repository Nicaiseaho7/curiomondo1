#!/usr/bin/env python3
"""Update the existing Di Battista article for CurioMondo v235."""
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
SOURCE_IMAGE = ROOT.parent / "generated-v235" / "alessandro-di-battista-neutral-editorial-hero.png"
SLUG = "alessandro-di-battista-ricoverato-cuba-trasferimento-avana-29-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Di Battista riprende conoscenza a Cuba: verso L’Avana, pronto un aereo sanitario per l’Italia"
EXCERPT = ("Dopo alcune ore di incoscienza ha parlato con i medici. Prosegue il trasferimento da Santa Clara all’Avana; "
           "il governo ha predisposto un aereo sanitario, ma l’eventuale rimpatrio dipenderà dalla valutazione clinica.")
CATEGORY = "Ultima ora · Italia / Politica"
PUBLISHED = "2026-08-29T12:58:00+02:00"
UPDATED = "2026-08-29T18:54:00+02:00"
DATE_LABEL = "2026-08-29"
IMAGE_KEY = "alessandro-di-battista-ritratto-neutrale-29-agosto-2026-ai-v235"
IMAGE_DIR = "/assets/images/editorial-v235"
IMAGE_ALT = "Ritratto editoriale neutrale ultrarealistico di Alessandro Di Battista su uno sfondo blu da studio"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
PROMPT = ("Use case: photorealistic-natural. Article hero, 1536x1024 landscape. Create an ultra-realistic, highly "
          "recognizable, calm neutral editorial portrait of Italian public figure Alessandro Di Battista. Disclosed "
          "synthetic editorial likeness, not documentary evidence. Person alone, head-and-shoulders, calm neutral "
          "expression, sober unbranded dark jacket and light shirt, premium blue studio gradient, natural skin and "
          "credible soft studio light. No hospital, ambulance, stretcher, doctors, medical devices, oxygen, tubes, "
          "bandages, injury, pain, distress, unconsciousness, illness symptoms, reenactment, travel, airplane, airport, "
          "Cuba cues, logos, flags, text, watermark, props or sensationalism.")

BODY = [
    "Alessandro Di Battista ha ripreso conoscenza dopo essere rimasto incosciente per alcune ore e ha parlato con i medici. È il nuovo elemento comunicato nella serata del 29 agosto da fonti parlamentari e riportato da ANSA. L’ex deputato del Movimento 5 Stelle è contemporaneamente in trasferimento dall’ospedale di Santa Clara verso una struttura sanitaria dell’Avana. Il recupero della coscienza rappresenta una prima evoluzione positiva rispetto alle informazioni precedenti, ma non equivale a una diagnosi né consente di formulare una prognosi.",
    "Di Battista era stato ricoverato nella serata di venerdì 28 agosto mentre si trovava a Cuba per un reportage. Secondo le ricostruzioni pubblicate dalle agenzie, avrebbe accusato un forte mal di testa seguito da un malore e sarebbe arrivato nell’ospedale di Santa Clara in condizioni descritte come gravi. Non è stato diffuso un bollettino medico e non è stata resa pubblica la causa del malore. CurioMondo mantiene quindi l’attribuzione alle fonti e non associa i sintomi a patologie specifiche.",
    "Dire che una persona ha ripreso conoscenza descrive un cambiamento osservabile nello stato di vigilanza, non una guarigione. Il fatto che Di Battista abbia potuto parlare con i medici aggiunge un dato concreto, ma non permette di conoscere la stabilità delle sue condizioni, gli esami svolti o le cure necessarie. È una distinzione importante nelle notizie sanitarie: un miglioramento momentaneo e l’evoluzione clinica complessiva sono informazioni diverse e soltanto i sanitari possono metterle in relazione.",
    "Il trasferimento in ambulanza da Santa Clara all’Avana era stato disposto nel pomeriggio ed è indicato come in corso nel nuovo aggiornamento. La capitale dispone di strutture sanitarie più grandi, ma le fonti non hanno specificato il nome dell’ospedale di destinazione né il motivo tecnico della scelta. Un trasferimento tra ospedali può servire ad accedere a specialisti, apparecchiature o livelli assistenziali differenti; nel caso concreto non è corretto dedurre quale necessità clinica lo abbia determinato.",
    "Parallelamente, Palazzo Chigi ha fatto sapere che il governo italiano ha un aereo sanitario disponibile per un eventuale rientro in Italia. La disponibilità del velivolo non significa che il rimpatrio sia stato deciso o programmato. Le fonti governative precisano che saranno i medici a valutare se le condizioni del paziente consentano il volo senza aggiungere rischi. Fino a quel via libera, l’aereo resta una possibilità organizzativa pronta a essere utilizzata, non la fase successiva già confermata.",
    "Un trasporto sanitario aereo è diverso da un normale viaggio di linea. Può richiedere personale medico, apparecchiature di monitoraggio, ossigeno, farmaci e una configurazione della cabina adatta alle necessità del paziente. Prima della partenza vengono considerate la stabilità clinica, la durata del tragitto, l’assistenza richiesta durante il volo e la continuità delle cure all’arrivo. Questa spiegazione descrive il funzionamento generale del servizio e non implica che Di Battista abbia bisogno di uno specifico dispositivo o trattamento.",
    "L’ambasciatrice italiana a Cuba, Simona De Martino, si è recata personalmente nell’ospedale di Santa Clara per acquisire informazioni e mantenere il raccordo con le autorità e la struttura sanitaria cubana. Il ministro degli Esteri Antonio Tajani aveva già dichiarato di essere in contatto con l’ambasciata dalla notte e di aver attivato l’assistenza della Farnesina per Di Battista e i familiari. Il coinvolgimento diretto della rappresentanza diplomatica conferma la dimensione istituzionale del caso.",
    "L’assistenza consolare, però, non sostituisce i medici e non decide la terapia. Un’ambasciata può facilitare i contatti con la famiglia e le autorità locali, aiutare a ottenere informazioni nei limiti della privacy, coordinare documenti e aspetti logistici e sostenere l’organizzazione di un rimpatrio. Le decisioni cliniche restano agli specialisti che hanno in cura il paziente; anche l’eventuale volo sanitario richiede il loro giudizio sulla trasportabilità.",
    "Nelle prime ore erano circolate indicazioni non coincidenti sul luogo del ricovero. Alcuni lanci parlavano genericamente dell’Avana, mentre le informazioni successive hanno collocato l’ospedale di partenza a Santa Clara, circa trecento chilometri a est della capitale, e hanno descritto il trasferimento verso L’Avana. La sequenza ora verificabile è quindi questa: malore e ricovero a Santa Clara, alcune ore di incoscienza, recupero della coscienza e trasferimento sanitario verso la capitale.",
    "Il Movimento 5 Stelle ha espresso grande apprensione e diversi esponenti politici hanno inviato messaggi di vicinanza. Queste reazioni spiegano l’attenzione pubblica, ma non aggiungono informazioni mediche. Di Battista, 48 anni, è stato deputato del M5S ed è rimasto una figura molto nota del dibattito politico italiano attraverso attività editoriali e reportage. Proprio la notorietà rende essenziale non trasformare indiscrezioni o formule generiche in dettagli clinici non autorizzati.",
    "Il quadro aggiornato alle 18:54 contiene dunque tre fatti nuovi e distinti: Di Battista ha ripreso conoscenza e parlato con i medici; il trasferimento da Santa Clara all’Avana è stato avviato; il governo italiano ha predisposto un aereo sanitario utilizzabile se i medici riterranno sicuro il viaggio. Nessuno di questi elementi chiarisce la diagnosi e nessuno consente di affermare che il rientro in Italia avverrà certamente o in tempi immediati.",
    "Le prossime informazioni decisive potranno arrivare dall’arrivo nella struttura dell’Avana, da una comunicazione autorizzata sulle condizioni o dalla decisione medica relativa al volo. L’articolo verrà aggiornato nello stesso indirizzo, evitando duplicati e mantenendo visibile la cronologia degli sviluppi. Fino ad allora la formulazione più prudente è anche la più precisa: c’è un primo segnale positivo, l’assistenza italiana è pienamente attivata, ma diagnosi, prognosi e rimpatrio restano non definiti."
]

SOURCES = [
    ("https://www.ansa.it/", "ANSA — recupero della coscienza, colloquio con i medici e trasferimento verso L’Avana"),
    ("https://www.ansa.it/sito/notizie/mondo/europa/2026/08/29/di-battista-sara-trasferito-in-ambulanza-allavana_3d7cd8d9-73a0-4891-bcf8-1dbb108699fd.html", "ANSA — trasferimento in ambulanza da Santa Clara all’Avana"),
    ("https://askanews.it/2026/08/29/di-battista-fonti-chigi-aereo-pronto-per-rientro-in-italia-si-valutano-condizioni/", "Askanews — aereo sanitario disponibile e rimpatrio subordinato alla valutazione medica"),
    ("https://www.agi.it/politica/news/2026-08-29/di-battista-ricoverato-a-cuba-38767124/", "AGI — ricovero, assistenza italiana e disponibilità del volo sanitario"),
    ("https://www.tgcom24.mediaset.it/politica/movimento-5-stelle-alessandro-di-battista-ricoverato-a-cuba_115967492-202602k.shtml", "Tgcom24 — dichiarazione di Palazzo Chigi e presenza dell’ambasciatrice a Santa Clara"),
]

RELATED = [
    ("/notizie/campi-flegrei-risoluzione-consiglio-campania-27-agosto-2026.html", "Italia · Politica", "Campi Flegrei, il Consiglio regionale approva una risoluzione per rafforzare il decreto"),
    ("/notizie/pd-primarie-centrosinistra-schlein-conte-26-agosto-2026.html", "Italia · Politica", "Centrosinistra, nel Pd si riapre il nodo primarie"),
    ("/notizie/usa-rientro-personale-ambasciate-medio-oriente-25-agosto-2026.html", "Diplomazia · Assistenza", "Gli USA iniziano a far rientrare personale dalle ambasciate in Medio Oriente"),
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
            source.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=86, method=6)
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
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CANONICAL}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE, quote=True)}"><meta property="og:description" content="{escape(EXCERPT, quote=True)}"><meta property="og:url" content="{CANONICAL}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{IMAGE_KEY}-1200.webp"><meta property="og:image:alt" content="{escape(IMAGE_ALT, quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=235"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{SLUG}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(CATEGORY)}</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">29 agosto 2026 · Italia / Politica · aggiornato alle 18:54 · <span id="readTime">5 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’articolo</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="true" data-portrait-format="neutral-isolated"><picture><img src="../assets/images/editorial-v235/{IMAGE_KEY}-800.webp" srcset="../assets/images/editorial-v235/{IMAGE_KEY}-480.webp 480w, ../assets/images/editorial-v235/{IMAGE_KEY}-800.webp 800w, ../assets/images/editorial-v235/{IMAGE_KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT, quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> Alessandro Di Battista riprende conoscenza Cuba</div><div><strong>URL SEO:</strong> {URL}</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>18:54</b><small>il quadro aggiornato della serata</small></div><div><b>2 città</b><small>da Santa Clara verso L’Avana</small></div><div><b>1 volo</b><small>disponibile, ma non ancora autorizzato</small></div></div></section><article class="art-body" data-length-policy="5000-7000">{body}</article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Il recupero della coscienza è un aggiornamento positivo, ma diagnosi, prognosi e idoneità al volo non sono state rese pubbliche.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=235" defer></script></body></html>'''


def update_json_data(variants: list[dict]) -> None:
    entry = feed_entry()
    for filename in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = 235
        items = [x for x in data["items"] if x.get("url") != URL]
        index = 1 if items and items[0].get("url", "").startswith("/notizie/usa-venezuela-") else 0
        value = entry if "home-feed" in filename else {k: entry[k] for k in ("title", "excerpt", "url", "section")}
        items.insert(index, value)
        data["items"] = items
        dump(path, data, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = 235
    old = []
    for item in registry["items"]:
        if item.get("article") == URL:
            item["superseded"] = True
            item["supersededBy"] = IMAGE_KEY
            old.append(item)
    current = {
        "key": IMAGE_KEY, "article": URL, "aiGenerated": True,
        "syntheticLikeness": "public-figure", "publicFigure": "Alessandro Di Battista",
        "sensitiveContext": True, "documentaryPhoto": False, "prompt": PROMPT,
        "variants": variants, "alt": IMAGE_ALT, "disclosure": CAPTION,
        "portraitOnly": True, "portraitFormat": "neutral-isolated", "reenactedEvent": False,
    }
    registry["items"] = [current] + [x for x in registry["items"] if x.get("article") != URL] + old
    dump(registry_path, registry)

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-29T16:54:00+00:00"
    feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"], "source": "CurioMondo", "article_exists": True} for x in feed[:10]]
    dump(live_path, live)


def update_home() -> None:
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    feed = json.loads((ROOT / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))["items"]

    tracks = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')
    for track_index, track in enumerate(tracks[:2]):
        for child in list(track): track.remove(child)
        for item in feed[:10]:
            a = etree.Element("a", href=item["url"]); a.set("class", "ticker-news"); a.text = item["title"]
            if track_index == 1: a.set("tabindex", "-1")
            track.append(a)

    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for node in rail.xpath(f'./a[@href="{URL}"]'): rail.remove(node)
    entry = feed_entry()
    card = html.fragment_fromstring(
        f'<a class="auto-card" href="{URL}"><picture><img alt="{escape(IMAGE_ALT, quote=True)}" decoding="async" loading="lazy" height="533" sizes="(max-width:600px) 79vw,300px" src="{entry["image"]}" srcset="{entry["srcset"]}" width="800"/></picture><div class="abody"><div class="ameta">{escape(CATEGORY)}</div><h3>{escape(TITLE)}</h3><p>{escape(EXCERPT)}</p><time datetime="{UPDATED}">{DATE_LABEL}</time></div></a>'
    )
    rail.insert(1, card)
    while len(rail.xpath('./a')) > 5: rail.remove(rail.xpath('./a')[-1])
    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'): script.set("src", "/assets/js/home-v210.js?v=235")
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_xml_and_archive() -> None:
    archive_path = ROOT / "notizie/index.html"
    archive = html.fromstring(archive_path.read_text(encoding="utf-8"))
    links = archive.xpath(f'//a[@href="{URL}"]')
    if links:
        strong = links[0].xpath('./strong')[0]; strong.text = TITLE
    write(archive_path, "<!doctype html>" + html.tostring(archive, encoding="unicode", method="html"))

    parser = etree.XMLParser(remove_blank_text=False)
    feed_path = ROOT / "feed.xml"
    feed = etree.parse(str(feed_path), parser); channel = feed.getroot().find("channel")
    target = next(x for x in channel.findall("item") if x.findtext("link") == CANONICAL)
    target.find("title").text = TITLE; target.find("description").text = EXCERPT
    target.find("pubDate").text = format_datetime(datetime.fromisoformat(UPDATED))
    channel.remove(target)
    first_item = channel.findall("item")[0]; channel.insert(channel.index(first_item) + 1, target)
    feed_path.write_bytes(etree.tostring(feed, encoding="utf-8", xml_declaration=True, pretty_print=True))

    news_path = ROOT / "news-sitemap.xml"
    news = etree.parse(str(news_path), parser)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "n": "http://www.google.com/schemas/sitemap-news/0.9"}
    for node in news.xpath('//s:url[s:loc=$loc]', namespaces=ns, loc=CANONICAL):
        title = node.find('.//{http://www.google.com/schemas/sitemap-news/0.9}title'); title.text = TITLE
    news_path.write_bytes(etree.tostring(news, encoding="utf-8", xml_declaration=True, pretty_print=True))


def update_release() -> None:
    for js in (ROOT / "assets/js/home-v210.js", ROOT / "assets/js/curiomondo-article-v210.js"):
        write(js, js.read_text(encoding="utf-8").replace("?v=234", "?v=235"))

    release = json.loads((ROOT / "RELEASE-STATE.json").read_text(encoding="utf-8"))
    release.update({"currentVersion": 235, "baselineVersion": 234, "status": "ready", "date": "2026-08-29",
                    "articleCount": 188, "generatedEditorialImages": 69,
                    "designRestored": "Di Battista aggiornato senza duplicato con ritratto neutrale sensibile, homepage e LIVE riallineate."})
    dump(ROOT / "RELEASE-STATE.json", release)
    state = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text(encoding="utf-8"))
    state.update({"site_version": 235, "baseline_version": 234, "version": "235",
                  "baseline": "curiomondo-v234-29-agosto-2026-netlify.zip",
                  "last_update": "di-battista-conscious-transfer-medical-flight-v235",
                  "performance_pass": "Nuovo ritratto neutrale WebP 480/800/1200; nessun nuovo articolo o duplicato; feed e cache aggiornati."})
    dump(ROOT / "CURIOMONDO-RELEASE-STATE.json", state)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = 235
    manifest["daily_state"]["last_question_date"] = "2026-08-29"
    manifest["daily_state"]["last_question_slug"] = "quale-parte-di-te-stai-cercando-di-correggere-quando-avrebbe-bisogno-prima-di-essere-ascoltata"
    manifest["site_version"] = 235; manifest["version"] = "v235"; manifest["release_version"] = "v235"
    manifest["last_release"] = {"version": 235, "date": "2026-08-29", "baseline_version": 234,
                                "news_added": [], "news_updated": [SLUG],
                                "image_policy_applied": "sensitive-public-figure-neutral-isolated-portrait"}
    dump(manifest_path, manifest)
    notes = f'''# CurioMondo v235 — 29 agosto 2026\n\n- Aggiornato senza duplicati l’articolo “{TITLE}”.\n- Integrati recupero della coscienza, trasferimento verso L’Avana e disponibilità condizionata di un aereo sanitario.\n- Sostituito il visual precedente con un nuovo ritratto editoriale neutrale isolato, conforme al protocollo per salute e ricoveri.\n- Aggiornati titolo, estratto, schema NewsArticle, homepage, LIVE, feed, ricerca, archivio e news sitemap.\n- La notizia USA–Venezuela resta in apertura per maggiore priorità editoriale; Di Battista sale al secondo posto delle notizie recenti e della LIVE.\n'''
    write(ROOT / "RELEASE-NOTES-v235.md", notes)


def main() -> None:
    if not SOURCE_IMAGE.exists(): raise SystemExit(f"Missing generated image: {SOURCE_IMAGE}")
    variants = create_images()
    write(ROOT / f"notizie/{SLUG}.html", article_html())
    dump(ROOT / f"contenuti/notizie/{SLUG}.json", {
        "slug": SLUG, "title": TITLE, "excerpt": EXCERPT, "category": CATEGORY,
        "published_at": PUBLISHED, "updated_at": UPDATED, "body": BODY,
        "related": [u for u, _, _ in RELATED], "sources": [{"url": u, "label": label} for u, label in SOURCES],
        "image": {"key": IMAGE_KEY, "alt": IMAGE_ALT, "ai_generated": True,
                  "synthetic_likeness": "public-figure", "public_figure": "Alessandro Di Battista",
                  "sensitive_context": True, "portrait_format": "neutral-isolated",
                  "documentary_photo": False, "disclosure": CAPTION},
    })
    update_json_data(variants)
    update_home()
    update_xml_and_archive()
    update_release()
    print(json.dumps({"version": 235, "updated": SLUG, "bodyCharacters": sum(map(len, BODY)), "variants": variants}, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
