#!/usr/bin/env python3
"""Aggiorna senza duplicati l'articolo ex Ilva con gli sviluppi del 16 settembre."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
SLUG = "ex-ilva-taranto-stop-area-caldo-28-ottobre-11-settembre-2026"
PATH = ROOT / "notizie" / f"{SLUG}.html"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
FEATURED_URL = "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html"
VERSION = 381
PUBLISHED = "2026-09-11T23:11:19+02:00"
UPDATED = "2026-09-16T15:52:00+02:00"
TITLE = "Ex Ilva, udienza il 20 ottobre: decreto rinviato e licenziamenti sospesi"
SUMMARY = (
    "La Cassazione discuterà il ricorso sullo stop dell’area a caldo il 20 ottobre. "
    "Il governo rinvia il decreto sulle tutele e le imprese dell’indotto sospendono "
    "le procedure di licenziamento, con modalità ancora da definire."
)
SECTION = "Italia / Economia / Industria"
IMAGE_KEY = "ex-ilva-udienza-cassazione-ai-openai-v381"
IMAGE_ALT = (
    "Illustrazione editoriale generata con IA di due lavoratori anonimi davanti "
    "a un impianto siderurgico costiero, non fotografia dell’evento"
)
IMAGE = f"/assets/images/editorial-auto/{IMAGE_KEY}-800.webp"
SRCSET = (
    f"/assets/images/editorial-auto/{IMAGE_KEY}-480.webp 480w, "
    f"/assets/images/editorial-auto/{IMAGE_KEY}-800.webp 800w, "
    f"/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp 1200w"
)

BODY = [
    "La Corte di Cassazione ha fissato per il 20 ottobre 2026 l’udienza pubblica a sezioni unite sul ricorso straordinario presentato da Ilva, Acciaierie d’Italia e Adi Holding contro il provvedimento che impone lo stop dell’area a caldo di Taranto. La nuova scadenza, comunicata il 16 settembre durante il confronto a Palazzo Chigi, modifica i passaggi immediati della vertenza.",
    "Il decreto con le misure per i lavoratori, annunciato in mattinata e inizialmente atteso nel Consiglio dei ministri dello stesso giorno, non sarà esaminato oggi. Secondo quanto riferito da ANSA e confermato da Repubblica, il governo ha chiesto di aggiornare il tavolo quando il quadro giudiziario sarà più chiaro.",
    "Non esiste quindi ancora un testo approvato che stabilisca durata, platea e coperture delle tutele. Il rinvio cambia il calendario ma non trasforma gli impegni anticipati durante il confronto in diritti già applicabili ai dipendenti.",
    "Resta valida la strategia illustrata dal sottosegretario Alfredo Mantovano: una cassa integrazione diversa da quella per cessazione, tutela di lavoratori diretti e indotto, prosecuzione della gara di vendita, reindustrializzazione dell’area di Taranto e passaggio verso forni elettrici alimentati con preridotto di ferro. Sono però indirizzi politici, non misure già operative.",
    "Sul fronte dell’indotto, il presidente di Aigi Nicola Convertino ha annunciato l’intenzione delle imprese di sospendere le procedure di licenziamento almeno fino alla decisione della Cassazione. La dichiarazione riguarda oltre 2.500 addetti coinvolti nelle procedure avviate a settembre.",
    "ANSA precisa che tempi e modalità devono essere definiti nelle prossime ore: la sospensione annunciata non va quindi confusa con una revoca definitiva. Confederazione Aepi ha definito la scelta un atto di responsabilità nella fase di attesa.",
    "L’udienza del 20 ottobre riguarda il ricorso contro il decreto della Corte d’Appello di Milano del 27 luglio, che ha ordinato la chiusura dell’area a caldo entro novanta giorni per ragioni ambientali e sanitarie. La stessa Corte d’Appello ha poi respinto le richieste di sospensione.",
    "Reuters ha documentato la conferma dello stop e il rischio industriale per lo stabilimento, che occupa circa 8.000 persone direttamente. L’impianto resta strategico per diverse filiere manifatturiere italiane, ma la rilevanza economica non annulla gli obblighi di tutela ambientale e sanitaria posti dai giudici.",
    "Il provvedimento di fissazione dell’udienza, citato da ANSA, richiama la necessità di una trattazione rapida per la rilevanza dei diritti fondamentali coinvolti. Il pubblico ministero potrà depositare una memoria entro il 5 ottobre, le parti resistenti entro il 14 e i ricorrenti entro il 17. I ricorsi contengono complessivamente 25 motivi di impugnazione.",
    "La data ravvicinata non sospende automaticamente l’ordine di fermata. Il Fatto Quotidiano riferisce che i commissari intendono presentare una nuova istanza cautelare per chiedere di mantenere in funzione l’area a caldo fino alla pronuncia delle sezioni unite. Finché non arriverà una decisione su questa richiesta, resta efficace il calendario imposto dai giudici milanesi.",
    "Per i lavoratori, il prossimo passaggio concreto sarà un tavolo tecnico annunciato per venerdì, dedicato alla gestione sociale della crisi. Il rinvio del decreto evita per ora di fissare una misura costruita su uno scenario che potrebbe cambiare dopo il 20 ottobre, ma lascia senza definizione immediata gli ammortizzatori e le altre garanzie promesse.",
    "La notizia resta IN SVILUPPO: sono documentati la data dell’udienza, il mancato esame del decreto oggi e l’impegno dell’indotto a sospendere i licenziamenti. Restano invece provvisori l’esito del ricorso, l’eventuale sospensione dello stop, le modalità applicative per l’indotto e il contenuto definitivo delle tutele governative."
]

SOURCES = [
    ("https://www.ansa.it/sito/notizie/cronaca/2026/09/16/ex-ilva-tavolo-con-sindacati-riaggiornato-nessun-decreto-oggi-in-cdm_38ad21a4-7a0c-4aba-8529-c7025078aecf.html", "ANSA — 16 settembre 2026, ore 15:24 — udienza in Cassazione, rinvio del decreto e dichiarazione Aigi sulla sospensione dei licenziamenti"),
    ("https://www.repubblica.it/economia/2026/09/16/news/ex_ilva_la_cassazione_anticipa_udienza_commissari_decreto_cdm-425588679/", "Repubblica — 16 settembre 2026, ore 14:39 — conferma indipendente della data del 20 ottobre e del rinvio del decreto"),
    ("https://www.ilfattoquotidiano.it/2026/09/16/ilva-cassazione-anticipo-udienza-commissari-richiesta-sospensione-decreto-news/8508187/", "Il Fatto Quotidiano — 16 settembre 2026 — nuova istanza cautelare annunciata dai commissari e quadro giudiziario"),
    ("https://www.reuters.com/business/italian-court-confirms-shutdown-large-steelworks-blow-to-meloni-2026-09-11/", "Reuters — 11 settembre 2026 — conferma dello stop disposto dalla Corte d’Appello e dimensione occupazionale")
]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_article() -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    doc.xpath("//title")[0].text = TITLE + " | CurioMondo"
    for xp, value in [
        ('//meta[@name="description"]', SUMMARY),
        ('//meta[@property="og:title"]', TITLE),
        ('//meta[@property="og:description"]', SUMMARY),
        ('//meta[@property="og:image"]', f"https://curiomondo.it/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp"),
        ('//meta[@property="og:image:alt"]', IMAGE_ALT),
    ]:
        node = doc.xpath(xp)
        if node:
            node[0].set("content", value)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({
        "headline": TITLE,
        "description": SUMMARY,
        "datePublished": PUBLISHED,
        "dateModified": UPDATED,
        "image": [f"https://curiomondo.it/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp"],
        "creditText": site.CAPTION,
    })
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    doc.xpath('//main//h1[1]')[0].text = TITLE
    doc.xpath('//main//p[contains(@class,"subtitle")][1]')[0].text = SUMMARY
    meta = doc.xpath('//main//div[contains(@class,"meta")][1]')[0]
    for child in list(meta):
        meta.remove(child)
    meta.text = "11 settembre 2026 · aggiornato il 16 settembre 2026 alle 15:52 · Italia / Economia · "
    etree.SubElement(meta, "span", id="readTime").text = "4 min di lettura"

    figure = doc.xpath('//figure[contains(@class,"article-image")][1]')[0]
    replacement = html.fragment_fromstring(
        f'<figure class="article-image" data-ai-generated="true"><picture>'
        f'<img src="../assets/images/editorial-auto/{IMAGE_KEY}-800.webp" '
        f'srcset="../assets/images/editorial-auto/{IMAGE_KEY}-480.webp 480w, '
        f'../assets/images/editorial-auto/{IMAGE_KEY}-800.webp 800w, '
        f'../assets/images/editorial-auto/{IMAGE_KEY}-1200.webp 1200w" '
        f'sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" '
        f'alt="{IMAGE_ALT}" loading="eager" decoding="async" fetchpriority="high"></picture>'
        f'<figcaption>{site.CAPTION}</figcaption></figure>'
    )
    figure.getparent().replace(figure, replacement)

    insight = doc.xpath('//section[contains(@class,"cm-insight")][1]')[0]
    new_insight = html.fragment_fromstring(
        '<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span>'
        '<div class="cm-insight-grid"><div><strong>20 ottobre</strong><span>udienza in Cassazione</span></div>'
        '<div><strong>Rinviato</strong><span>il decreto sulle tutele</span></div>'
        '<div><strong>oltre 2.500</strong><span>licenziamenti sospesi nell’indotto</span></div></div></section>'
    )
    insight.getparent().replace(insight, new_insight)

    body = doc.xpath('//article[contains(@class,"art-body")][1]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in BODY:
        etree.SubElement(body, "p").text = paragraph

    sources = doc.xpath('//div[contains(@class,"art-sources")][1]')[0]
    ul = sources.xpath('./ul')[0]
    for child in list(ul):
        ul.remove(child)
    for href, label in SOURCES:
        li = etree.SubElement(ul, "li")
        etree.SubElement(li, "a", href=href, rel="noopener noreferrer", target="_blank").text = label
    note = sources.xpath('.//p[small]')[0]
    for child in list(note):
        note.remove(child)
    small = etree.SubElement(note, "small")
    strong = etree.SubElement(small, "strong")
    strong.text = "Redazione CurioMondo · "
    etree.SubElement(strong, "a", href="/pagine/metodo-editoriale.html").text = "Come lavoriamo"
    strong[-1].tail = (
        "\nTesto originale CurioMondo. Aggiornamento sostanziale verificato il 16 settembre 2026 "
        "alle 15:52 italiane. " + site.CAPTION
    )

    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")
    PATH.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def sync_surfaces() -> list[dict]:
    metadata = {
        "slug": SLUG,
        "parole_chiave_titolo": ["Ex Ilva", "20 ottobre"],
        "dati_chiave": [
            {"icona": "◆", "valore": "20 ottobre", "etichetta": "udienza in Cassazione"},
            {"icona": "↪", "valore": "Rinviato", "etichetta": "il decreto sulle tutele"},
            {"icona": "●", "valore": "oltre 2.500", "etichetta": "licenziamenti sospesi nell’indotto"},
        ],
    }
    items = site.sync_surfaces([metadata], FEATURED_URL, VERSION)

    # Un aggiornamento non rinnova la data di prima pubblicazione nella News Sitemap.
    news_path = ROOT / "news-sitemap.xml"
    tree = ET.parse(news_path)
    root = tree.getroot()
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and loc.text == CANONICAL:
            root.remove(node)
    ET.indent(tree, space="  ")
    tree.write(news_path, encoding="utf-8", xml_declaration=True)
    return items


def update_records(items: list[dict]) -> None:
    image_record = {
        "id": IMAGE_KEY,
        "article": URL,
        "alt": IMAGE_ALT,
        "aiGenerated": True,
        "generator": "OpenAI ImageGen",
        "documentaryPhoto": False,
        "disclosure": site.CAPTION,
        "variants": [
            {"src": f"/assets/images/editorial-auto/{IMAGE_KEY}-480.webp", "w": 480, "h": 320},
            {"src": f"/assets/images/editorial-auto/{IMAGE_KEY}-800.webp", "w": 800, "h": 533},
            {"src": f"/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp", "w": 1200, "h": 800},
        ],
    }
    path = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["items"] = [image_record] + [i for i in data.get("items", []) if i.get("article") != URL]
    write_json(path, data)

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-09-16T13:52:00+00:00"
    live["items"] = [
        {"title": i["title"], "url": i["url"], "published_at": i["dateISO"], "source": "CurioMondo", "article_exists": True}
        for i in items[:10]
    ]
    write_json(live_path, live)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG, "title": TITLE, "excerpt": SUMMARY, "category": SECTION,
        "published_at": PUBLISHED, "updated_at": UPDATED, "status": "IN SVILUPPO",
        "body": BODY, "sources": [{"url": u, "label": l} for u, l in SOURCES],
        "image": image_record,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site"]["site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {
        "version": VERSION, "date": "2026-09-16", "type": "content-update",
        "news_added": [], "news_updated": [SLUG],
        "change": "Aggiornamento ex Ilva: udienza in Cassazione il 20 ottobre, decreto rinviato e sospensione annunciata dei licenziamenti nell’indotto",
        "image_policy_applied": "new-openai-editorial-image-for-substantive-update",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state_data = json.loads(path.read_text(encoding="utf-8"))
        state_data.update({
            "currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
            "date": "2026-09-16", "release_date": "2026-09-16",
            "last_update": "ex-ilva-cassazione-20-ottobre-v381",
        })
        write_json(path, state_data)

    write_json(ROOT / "automation" / "logs" / "italia-20260916T155226-Europe-Rome.json", {
        "run_at": "2026-09-16T15:52:26+02:00",
        "production_branch": "main",
        "production_base_commit": "dc222bd2fc1af548e3d752745e391e81f463e2f4",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 3,
            "note": "Conteggio prudenziale: esclusi titoli, snippet e risultati duplicati. Obiettivo non raggiunto; nessuna consultazione inventata."
        },
        "processed": [{
            "slug": SLUG, "action": "updated_existing_article", "score": 9.0,
            "status": "IN SVILUPPO", "public_url": CANONICAL,
            "sources": [u for u, _ in SOURCES], "publication_state": "pending_deploy"
        }]
    })


def qa(items: list[dict]) -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    schema = json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)
    assert doc.xpath('//h1')[0].text == TITLE
    assert schema["datePublished"] == PUBLISHED and schema["dateModified"] == UPDATED
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(BODY)
    assert len(doc.xpath('//div[contains(@class,"art-sources")]//li')) == len(SOURCES)
    assert doc.xpath('//figure[contains(@class,"article-image")]//img')[0].get("alt") == IMAGE_ALT
    assert any(i["url"] == URL for i in items)
    assert len({i["url"] for i in items}) == len(items)


def main() -> None:
    update_article()
    items = sync_surfaces()
    update_records(items)
    qa(items)
    position = next(i for i, item in enumerate(items, 1) if item["url"] == URL)
    print(json.dumps({"version": VERSION, "updated": URL, "feed_position": position, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
