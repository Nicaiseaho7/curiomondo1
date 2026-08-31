#!/usr/bin/env python3
"""Update the existing Cremona severe-weather story with the verified 29 Aug 20:27 developments."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime, parsedate_to_datetime
from html import escape
import json
from pathlib import Path

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
SLUG = "cremona-tromba-aria-grandine-danni-29-agosto-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
TITLE = "Cremona in ginocchio dopo la tromba d’aria: 43 feriti, 10mila auto danneggiate e famiglie evacuate"
EXCERPT = ("Il bilancio sale a 43 feriti, quattro ricoverati e 12 famiglie evacuate. Circa 10mila auto e almeno dieci chiese sono state danneggiate; la Lombardia ha chiesto di estendere lo stato di emergenza.")
CATEGORY = "Ultima ora · Italia / Cronaca / Ambiente"
PUBLISHED = "2026-08-29T10:42:00+02:00"
UPDATED = "2026-08-29T20:27:00+02:00"
DATE_LABEL = "2026-08-29"
DISPLAY_DATE = "29 agosto 2026"
IMAGE = "/assets/images/editorial-v213/cremona-grandine-danni-29-agosto-2026-ai-800.webp"
SRCSET = "/assets/images/editorial-v213/cremona-grandine-danni-29-agosto-2026-ai-480.webp 480w, /assets/images/editorial-v213/cremona-grandine-danni-29-agosto-2026-ai-800.webp 800w, /assets/images/editorial-v213/cremona-grandine-danni-29-agosto-2026-ai-1200.webp 1200w"
IMAGE_ALT = "Centro storico italiano dopo una violenta grandinata con auto danneggiate, alberi caduti e soccorritori"

BODY = [
    "Cremona entra nella fase più difficile dell’emergenza dopo la violenta tromba d’aria accompagnata da grandine che ha colpito la città nel pomeriggio del 28 agosto. Il bilancio sanitario aggiornato è di 43 persone assistite al pronto soccorso: la maggior parte è stata dimessa, una è rimasta in osservazione e quattro pazienti traumatizzati hanno avuto bisogno del ricovero. Nessuno dei feriti risulta in condizioni gravi e non sono stati registrati codici rossi. In quattro casi i medici hanno riscontrato fratture del femore, mentre molti degli altri traumi sono stati provocati da cadute o dai tentativi di trovare riparo durante la grandinata.",
    "Anche il numero delle persone costrette a lasciare casa è stato aggiornato. Dodici famiglie sono state evacuate da una palazzina dichiarata inagibile per i danni provocati dal maltempo. Nove hanno trovato una sistemazione presso parenti o amici, mentre tre sono state accolte in strutture alberghiere. I controlli sugli edifici proseguono perché il problema non riguarda soltanto ciò che è crollato immediatamente: coperture, cornicioni, alberi e altri elementi possono essere rimasti instabili e richiedere verifiche prima che le aree vengano riaperte.",
    "La dimensione materiale dei danni è enorme. Le prime stime parlano di circa 10.000 automobili colpite dalla grandine, migliaia di alberi caduti e numerosi tetti divelti. Almeno dieci chiese hanno riportato danni. Tra i luoghi simbolo interessati ci sono la Cattedrale e il complesso del municipio, dove la torre civica necessita di interventi di messa in sicurezza. Il Palazzo Comunale è stato dichiarato temporaneamente inagibile e alcuni uffici e servizi dovranno essere trasferiti. Anche la fiera cittadina ha riportato danni a tre dei quattro padiglioni, mentre imprese e aziende agricole stanno ancora quantificando le perdite.",
    "I dati meteorologici comunicati dal sindaco Andrea Virgilio rendono l’idea della violenza del fenomeno. In poco meno di venti minuti sarebbe caduta una quantità di pioggia pari a circa l’80% di quella normalmente registrata nell’intero mese di agosto. La grandine ha raggiunto in alcuni casi dimensioni fino a dieci centimetri e il vento è stato indicato attorno ai 90 chilometri orari. Una combinazione così concentrata di acqua, ghiaccio e raffiche può produrre danni molto diversi nello stesso momento: vetri e carrozzerie colpiti, alberi sradicati, coperture sollevate e allagamenti improvvisi.",
    "L’emergenza non riguarda soltanto Cremona. I vigili del fuoco hanno effettuato oltre 500 interventi in Lombardia, con la maggior parte delle criticità concentrate nel Cremonese. Le squadre sono state impegnate nella rimozione di alberi e rami, nei dissesti statici, nella messa in sicurezza di tetti ed elementi strutturali, negli allagamenti e nella liberazione delle strade. Tra gli interventi più delicati c’è stato anche il salvataggio di quattro persone ferite rimaste bloccate in un’automobile in panne. Il maltempo ha interessato inoltre il Mantovano, il Bergamasco e il Pavese, mentre in Veneto sono proseguite operazioni analoghe dopo temporali e forti raffiche di vento.",
    "La priorità indicata dal Comune è ora liberare e mettere in sicurezza la città. Parchi e giardini sono stati chiusi in attesa delle verifiche, così come il cimitero, dove sono caduti numerosi alberi. Sono in corso controlli su scuole, palestre e altre strutture pubbliche. Diverse strade e piste ciclabili restano interessate da ostacoli o transennamenti e l’amministrazione ha invitato i cittadini a evitare le aree interdette. È una fase meno spettacolare del passaggio della tempesta, ma decisiva: gran parte del rischio residuo arriva infatti da strutture indebolite, rami sospesi e coperture che possono cedere anche ore dopo la fine del temporale.",
    "L’emergenza ha assunto anche una dimensione istituzionale nazionale. Il presidente della Repubblica Sergio Mattarella ha telefonato al sindaco di Cremona per esprimere vicinanza alla comunità, mentre la presidente del Consiglio Giorgia Meloni ha fatto sapere di seguire la situazione in contatto con il ministro per la Protezione civile Nello Musumeci, il sottosegretario Alfredo Mantovano, il capo del Dipartimento della Protezione Civile Fabio Ciciliano e le autorità locali. Musumeci ha assicurato che l’intervento del governo potrà essere tempestivo una volta completata l’istruttoria tecnica prevista dalla legge.",
    "La Regione Lombardia ha avviato l’estensione della richiesta di stato di emergenza alle province di Cremona, Mantova, Bergamo e Pavia, aggiungendole alla documentazione già predisposta per gli eventi di maltempo iniziati il 20 agosto. Il passaggio è importante perché una dichiarazione di emergenza nazionale può consentire di attivare procedure straordinarie e risorse per gli interventi urgenti, ma non equivale ancora a una quantificazione definitiva dei danni o a un rimborso automatico. Prima serviranno ricognizioni tecniche, stime economiche e la definizione degli interventi prioritari.",
    "Per le famiglie e le imprese colpite comincia quindi una seconda conta, quella economica. Il solo numero delle automobili danneggiate lascia prevedere costi molto elevati. A questi si aggiungono tetti, serramenti, impianti, attività produttive, coltivazioni, strutture pubbliche e beni storico-artistici. Federcarrozzieri ha stimato che le riparazioni di un veicolo colpito dalla grandine possono variare molto a seconda della gravità, mentre la copertura assicurativa contro gli eventi atmosferici non è presente su tutte le auto. Le valutazioni reali richiederanno comunque perizie caso per caso.",
    "Particolarmente delicato sarà il lavoro sugli edifici storici. Quando grandine e vento colpiscono chiese, torri e coperture antiche non basta sostituire gli elementi danneggiati: occorre verificare la stabilità, proteggere gli interni dalle infiltrazioni e coordinare gli interventi con gli enti responsabili della tutela. Per la torre civica è stata coinvolta la Soprintendenza. La Cattedrale e altri luoghi monumentali rappresentano inoltre una parte centrale della vita cittadina e del turismo, perciò tempi e modalità della messa in sicurezza avranno conseguenze che vanno oltre il semplice costo della riparazione.",
    "Il quadro aggiornato cambia quindi la scala della notizia rispetto alle prime ore. Non si parla più soltanto di un temporale molto violento: ci sono 43 feriti, dodici famiglie evacuate, migliaia di veicoli e alberi coinvolti, danni al patrimonio storico e una richiesta di estensione dello stato di emergenza. La buona notizia resta l’assenza di feriti in condizioni gravi. La parte più lunga, però, comincia adesso: verificare l’agibilità degli edifici, riaprire gli spazi pubblici, quantificare i danni e capire quali risorse saranno necessarie per riportare Cremona e gli altri territori colpiti alla normalità."
]

SOURCES = [
    ("https://www.ansa.it/sito/notizie/cronaca/2026/08/29/cremona-in-ginocchio-per-il-maltempo-matterella-telefona-al-sindaco_3555cb29-4091-4045-be28-97246b751cc4.html", "ANSA — bilancio aggiornato: 43 feriti, 12 famiglie evacuate, 10mila auto e richiesta di estensione dello stato di emergenza"),
    ("https://www.adnkronos.com/cronaca/maltempo-cremona-interventi-urgenti-danni-cosa-e-successo-aggiornamenti_5q1vsQKOdDzOLSRSmgCIkd", "Adnkronos — 500 interventi, pioggia pari all’80% del mese e grandine fino a 10 centimetri"),
    ("https://askanews.it/2026/08/29/nubifragio-a-cremona-la-regione-lombardia-chiede-lo-stato-demergenza/", "Askanews — stato di emergenza, chiusure, verifiche sugli edifici e reazioni istituzionali"),
    ("https://www.vigilfuoco.tv/lombardia/cremona/cremona/maltempo-lombardia-500-interventi-dei-vigili-del-fuoco-il-maggior-numero", "Vigili del Fuoco — oltre 500 interventi in Lombardia, salvataggi ed evacuazione di 12 famiglie"),
    ("https://fr.lapresse.it/actualite/2026/08/29/intemperies-500-interventions-des-pompiers-en-lombardie-evacuations-et-sauvetages-a-cremone/", "LaPresse — riscontro su interventi, evacuazioni e soccorsi nel Cremonese"),
]

RELATED = [
    ("/notizie/chiavari-rupinaro-maltempo-sirene-20-agosto-2026.html", "Italia · Ambiente", "Chiavari e il Rupinaro: maltempo, sirene e gestione dell’allerta"),
    ("/notizie/torrenti-liguri-rupinaro-sirene-allarme-come-funziona.html", "Approfondimento · Protezione civile", "Come funzionano sirene e sistemi di allerta nei territori a rischio"),
    ("/notizie/campi-flegrei-risoluzione-consiglio-campania-27-agosto-2026.html", "Italia · Emergenze", "Campi Flegrei, nuove richieste di tutela per famiglie e territori"),
]


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def dump(path: Path, value: object, compact: bool = False) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=None if compact else 2,
                      separators=(",", ":") if compact else None)
    write(path, text + ("" if compact else "\n"))


def entry() -> dict:
    return {
        "title": TITLE, "excerpt": EXCERPT, "url": URL, "section": CATEGORY,
        "dateISO": UPDATED, "dateLabel": DATE_LABEL,
        "image": IMAGE, "imageAlt": IMAGE_ALT, "imageWidth": 800, "imageHeight": 533,
        "srcset": SRCSET,
    }


def replace_text_content(el, text: str) -> None:
    for child in list(el):
        el.remove(child)
    el.text = text


def update_article() -> None:
    path = ROOT / f"notizie/{SLUG}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))

    # Head / SEO
    doc.xpath("//title")[0].text = TITLE + " | CurioMondo"
    for xp, value in [
        ('//meta[@name="description"]', EXCERPT),
        ('//meta[@property="og:title"]', TITLE),
        ('//meta[@property="og:description"]', EXCERPT),
    ]:
        nodes = doc.xpath(xp)
        if nodes:
            nodes[0].set("content", value)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({"headline": TITLE, "description": EXCERPT, "datePublished": PUBLISHED,
                   "dateModified": UPDATED, "mainEntityOfPage": CANONICAL})
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    # Article header
    doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," badge ")]')[0].text = CATEGORY
    doc.xpath('//h1')[0].text = TITLE
    doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')[0].text = EXCERPT
    meta = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0]
    for child in list(meta):
        meta.remove(child)
    meta.text = f"{DISPLAY_DATE} · Italia · Cronaca / Ambiente · aggiornato alle 20:27 · "
    span = etree.SubElement(meta, "span", id="readTime")
    span.text = "5 min di lettura"

    # Three data points
    insight = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-insight ")]')[0]
    new_insight = html.fragment_fromstring(
        '<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span>'
        '<div class="cm-insight-grid"><div><b>43</b><small>persone assistite al pronto soccorso</small></div>'
        '<div><b>12</b><small>famiglie evacuate da una palazzina inagibile</small></div>'
        '<div><b>10.000</b><small>automobili stimate danneggiate</small></div></div></section>'
    )
    insight.getparent().replace(insight, new_insight)

    # Body
    article = doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
    for child in list(article):
        article.remove(child)
    for paragraph in BODY:
        p = etree.SubElement(article, "p")
        p.text = paragraph

    # Related links: add or replace directly before sources.
    sources = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]')[0]
    old_related = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," curio-related ")]')
    related_html = '<section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">'
    for u, cat, title in RELATED:
        related_html += f'<a href="{u}"><span>{escape(cat)}</span><strong>{escape(title)}</strong></a>'
    related_html += '</div></section>'
    related = html.fragment_fromstring(related_html)
    if old_related:
        old_related[0].getparent().replace(old_related[0], related)
    else:
        sources.addprevious(related)

    # Sources
    ul = sources.xpath('./ul')[0]
    for child in list(ul):
        ul.remove(child)
    for u, label in SOURCES:
        li = etree.SubElement(ul, "li")
        a = etree.SubElement(li, "a", href=u, rel="noopener noreferrer", target="_blank")
        a.text = label
    small = sources.xpath('.//small')
    if small:
        small[0].text = "Testo originale CurioMondo. Dati verificati e incrociati sulle fonti indicate; ultimo aggiornamento editoriale verificato: 29 agosto 2026, ore 20:27 italiane."

    # Cache bust only on this updated article.
    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", "../assets/css/curiomondo-article-v211.css?v=243")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", "../assets/js/curiomondo-article-v210.js?v=243")

    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))

    # Canonical content JSON (the original older story did not have one).
    dump(ROOT / f"contenuti/notizie/{SLUG}.json", {
        "slug": SLUG, "title": TITLE, "excerpt": EXCERPT, "category": CATEGORY,
        "published_at": PUBLISHED, "updated_at": UPDATED, "body": BODY,
        "related": [u for u, _, _ in RELATED],
        "sources": [{"url": u, "label": label} for u, label in SOURCES],
        "image": {"key": "cremona-grandine-danni-29-agosto-2026-ai", "alt": IMAGE_ALT,
                  "ai_generated": True, "documentary_photo": False,
                  "disclosure": "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."},
    })


def update_data() -> None:
    current = entry()
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    home["version"] = 243
    items = [x for x in home["items"] if x.get("url") != URL]
    items.append(current)
    items.sort(key=lambda x: str(x.get("dateISO", "")), reverse=True)
    home["items"] = items
    dump(home_path, home, compact=True)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    search["version"] = 243
    search_items = [x for x in search["items"] if x.get("url") != URL]
    search_items.insert(0, {k: current[k] for k in ("title", "excerpt", "url", "section")})
    search["items"] = search_items
    dump(search_path, search, compact=True)

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-29T18:27:00+00:00"
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"],
                      "source": "CurioMondo", "article_exists": True}
                     for x in home["items"] if x.get("url", "").startswith("/notizie/")][:10]
    dump(live_path, live)


def picture_markup(item: dict, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (f'<picture><img alt="{escape(item["imageAlt"], quote=True)}" decoding="async" loading="{loading}" '
            f'height="533" sizes="(max-width:600px) 79vw,300px" src="{item["image"]}" '
            f'srcset="{item["srcset"]}" width="800"{priority}></picture>')


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
    news_items = [x for x in feed if x.get("url", "").startswith("/notizie/")]

    # LIVE: latest ten by current feed order.
    tracks = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')
    for track_index, track in enumerate(tracks[:2]):
        for child in list(track):
            track.remove(child)
        for item in news_items[:10]:
            a = etree.Element("a", href=item["url"])
            a.set("class", "ticker-news")
            a.text = item["title"]
            if track_index == 1:
                a.set("tabindex", "-1")
            track.append(a)

    # Preserve the current hero (Roman), rebuild exactly five 'Notizie di oggi'.
    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for child in list(rail):
        rail.remove(child)
    for item in news_items[:5]:
        rail.append(auto_card(item))

    # Rebuild 'Altre notizie' from positions 6..23 to avoid duplicates after the update moves Cremona upward.
    cards = doc.xpath('//div[@id="cards"]')[0]
    for child in list(cards):
        cards.remove(child)
    for item in news_items[5:23]:
        cards.append(regular_card(item))

    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", "/assets/js/home-v210.js?v=243")
    if len(doc.xpath('//*[@id="universo-curiomondo-title"]/*[contains(@class,"cm-universe-title-line")]')) != 2:
        raise RuntimeError("La centratura strutturale di Universo CurioMondo è stata alterata")
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_archive_feed_sitemaps() -> None:
    # Archive: place updated Cremona after Roman and Ranucci, reflecting the 20:27 update.
    archive_path = ROOT / "notizie/index.html"
    archive = html.fromstring(archive_path.read_text(encoding="utf-8"))
    ul = archive.xpath('//main//ul')[0]
    for li in ul.xpath(f'./li[a/@href="{URL}"]'):
        ul.remove(li)
    li = html.fragment_fromstring(f'<li><a href="{URL}"><strong>{escape(TITLE)}</strong><span>{DATE_LABEL}</span></a></li>')
    ul.insert(min(2, len(ul)), li)
    archive.xpath('//main/p')[0].text = f"{len(ul.xpath('./li'))} articoli, ordinati per data."
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
        child = etree.SubElement(item, name); child.text = value
    existing = list(channel.findall("item"))
    insert_at = channel.index(existing[2]) if len(existing) >= 3 else len(channel)
    channel.insert(insert_at, item)
    feed_path.write_bytes(etree.tostring(feed, encoding="utf-8", xml_declaration=True, pretty_print=True))

    # Standard sitemap: update lastmod and keep URL unique.
    sitemap_path = ROOT / "sitemap.xml"
    sitemap = etree.parse(str(sitemap_path), parser)
    sns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    nodes = sitemap.xpath('//s:url[s:loc=$loc]', namespaces={"s": sns}, loc=CANONICAL)
    if nodes:
        node = nodes[0]
        lm = node.find(f"{{{sns}}}lastmod")
        if lm is None: lm = etree.SubElement(node, f"{{{sns}}}lastmod")
        lm.text = DATE_LABEL
    sitemap_path.write_bytes(etree.tostring(sitemap, encoding="utf-8", xml_declaration=True, pretty_print=True))

    # Google News sitemap: preserve original publication time, update headline.
    news_path = ROOT / "news-sitemap.xml"
    news = etree.parse(str(news_path), parser)
    nns = "http://www.google.com/schemas/sitemap-news/0.9"
    nodes = news.xpath('//s:url[s:loc=$loc]', namespaces={"s": sns}, loc=CANONICAL)
    if nodes:
        title = nodes[0].find(f".//{{{nns}}}title")
        if title is not None: title.text = TITLE
        pub = nodes[0].find(f".//{{{nns}}}publication_date")
        if pub is not None: pub.text = PUBLISHED
    news_path.write_bytes(etree.tostring(news, encoding="utf-8", xml_declaration=True, pretty_print=True))


def update_release() -> None:
    release = json.loads((ROOT / "RELEASE-STATE.json").read_text(encoding="utf-8"))
    release.update({"currentVersion": 243, "baselineVersion": 242, "status": "ready", "date": "2026-08-30",
                    "articleCount": release.get("articleCount", 191), "generatedEditorialImages": release.get("generatedEditorialImages", 71),
                    "site_version": 243, "version": "243", "baseline_version": 242,
                    "baseline": "curiomondo-v242-nancy-grace-roman-29-agosto-2026-netlify.zip",
                    "last_update": "cremona-43-feriti-12-famiglie-v243",
                    "release_date": "2026-08-30",
                    "designRestored": "Design v242 preservato; aggiornato l’articolo Cremona, feed, LIVE e home senza duplicati."})
    dump(ROOT / "RELEASE-STATE.json", release)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({"site_version": 243, "baseline_version": 242, "version": "243", "date": "2026-08-30",
                      "baseline": "curiomondo-v242-nancy-grace-roman-29-agosto-2026-netlify.zip",
                      "last_update": "cremona-43-feriti-12-famiglie-v243",
                      "performance_pass": "Nessun nuovo asset pesante; feed e markup aggiornati; LIVE 10, Notizie di oggi 5."})
        dump(state_path, state)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if isinstance(manifest.get("site"), dict):
        manifest["site"]["current_site_version"] = 243
    manifest["site_version"] = 243
    manifest["version"] = "v243"
    manifest["release_version"] = "v243"
    manifest["last_release"] = {"version": 243, "date": "2026-08-30", "baseline_version": 242,
                                "news_added": [], "news_updated": [SLUG],
                                "image_policy_applied": "existing-ai-editorial-image-retained-for-story-update",
                                "preserved": ["universo-curiomondo-centered-v240", "nicaise-signature-style", "v242-home-design"]}
    dump(manifest_path, manifest)

    notes = f'''# CurioMondo v243 — 30 agosto 2026\n\n- Aggiornato l’articolo “{TITLE}”.\n- Nuovo bilancio verificato: 43 feriti, quattro ricoverati, 12 famiglie evacuate, circa 10.000 auto e almeno dieci chiese danneggiate.\n- Inseriti i dati sul temporale: circa l’80% della pioggia mensile in meno di 20 minuti, grandine fino a 10 cm e oltre 500 interventi dei Vigili del Fuoco in Lombardia.\n- Aggiornata la dimensione istituzionale: Mattarella, Palazzo Chigi e richiesta lombarda di estensione dello stato di emergenza a Cremona, Mantova, Bergamo e Pavia.\n- Fonti incrociate nell’articolo: ANSA, Adnkronos, Askanews, Vigili del Fuoco e LaPresse.\n- Aggiornati LIVE, Notizie di oggi, Altre notizie, ricerca, feed RSS, archivio, sitemap e News Sitemap senza creare un articolo duplicato.\n- Design e struttura della v242 preservati.\n'''
    write(ROOT / "RELEASE-NOTES-v243.md", notes)


def qa() -> dict:
    article_path = ROOT / f"notizie/{SLUG}.html"
    text = article_path.read_text(encoding="utf-8")
    doc = html.fromstring(text)
    body_chars = sum(len(p) for p in BODY)
    home = html.fromstring((ROOT / "index.html").read_text(encoding="utf-8"))
    live1 = home.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[0].xpath('./a')
    rail = home.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0].xpath('./a')
    cards = home.xpath('//div[@id="cards"]')[0].xpath('./a')
    all_urls = [a.get('href') for a in rail + cards]
    checks = {
        "title_updated": doc.xpath('//h1')[0].text == TITLE,
        "date_modified": json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text).get('dateModified') == UPDATED,
        "body_characters": body_chars,
        "body_policy_ok": 5000 <= body_chars <= 7000,
        "live_count": len(live1),
        "today_count": len(rail),
        "other_count": len(cards),
        "home_no_duplicates": len(all_urls) == len(set(all_urls)),
        "cremona_in_today": URL in [a.get('href') for a in rail],
        "cremona_not_in_other": URL not in [a.get('href') for a in cards],
        "related_count": len(doc.xpath('//section[contains(@class,"curio-related")]//a')),
        "source_count": len(doc.xpath('//div[contains(@class,"art-sources")]//li')),
    }
    if not all(v is True or isinstance(v, int) for v in checks.values()):
        raise RuntimeError(checks)
    if checks["live_count"] != 10 or checks["today_count"] != 5 or checks["other_count"] != 18:
        raise RuntimeError(checks)
    if not checks["body_policy_ok"] or not checks["home_no_duplicates"] or not checks["cremona_in_today"] or not checks["cremona_not_in_other"]:
        raise RuntimeError(checks)
    return checks


def main() -> None:
    update_article()
    update_data()
    update_home()
    update_archive_feed_sitemaps()
    update_release()
    checks = qa()
    print(json.dumps({"version": 243, "updated": SLUG, "checks": checks}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
