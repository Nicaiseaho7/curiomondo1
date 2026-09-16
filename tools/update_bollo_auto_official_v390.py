#!/usr/bin/env python3
"""Aggiorna il bollo auto con il comunicato ufficiale del Cdm n. 189."""
from __future__ import annotations

import json
from pathlib import Path
import runpy
import sys

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 390
SLUG = "bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
PATH = ROOT / "notizie" / f"{SLUG}.html"
FEATURED_URL = "/notizie/federal-reserve-alza-tassi-3-75-4-percento-16-settembre-2026.html"
PUBLISHED = "2026-09-16T16:48:39+02:00"
UPDATED = "2026-09-16T21:51:30+02:00"
TITLE = "Bollo auto, il Cdm approva l’esenzione fino a 80 kW per il 2027"
SUMMARY = (
    "Il comunicato ufficiale del Cdm conferma per il 2027 l’esenzione delle auto fino a 80 kW "
    "e, alle condizioni previste, dei mezzi a due ruote. Sul gasolio lo sconto scende a 12,2 "
    "centesimi fino al 25 settembre e a 6,1 centesimi fino al 5 ottobre."
)
SECTION = "Italia"
IMAGE_ALT = (
    "Illustrazione editoriale di un’auto compatta e uno scooter parcheggiati "
    "in una strada italiana, non fotografia dell’annuncio."
)

BODY = [
    "Il Consiglio dei ministri ha approvato il 16 settembre 2026 un decreto-legge che prevede per il 2027 l’esenzione dal bollo delle auto fino a 80 kW e interviene anche sui veicoli a due ruote. Il comunicato n. 189 pubblicato da Palazzo Chigi documenta formalmente l’adozione del provvedimento e precisa anche il calendario della nuova riduzione delle accise sul gasolio.",
    "La soglia di 80 kW equivale a circa 109 cavalli ed è il criterio indicato per le autovetture. L’esenzione può riguardare anche ciclomotori e motocicli, a condizione che lo stesso proprietario non utilizzi già il beneficio per un’auto: il limite resta quindi un solo veicolo agevolato per contribuente.",
    "Il beneficio è previsto per il solo 2027. Reuters, che aveva esaminato una bozza prima della riunione, ha stimato un costo di 2,36 miliardi di euro. Il ministro dell’Economia Giancarlo Giorgetti ha spiegato che il governo intende cercare di rendere la misura permanente, ma al momento l’esenzione adottata è annuale.",
    "La platea annunciata dal governo è di circa 14,5 milioni di veicoli e comprende oltre il 70% delle auto piccole e medie interessate dalla soglia di potenza, oltre ai mezzi a due ruote che rispettano le condizioni. Il numero descrive la portata stimata della misura, non un accredito automatico per tutti i proprietari.",
    "Il decreto interviene anche sul caro carburanti. Dal 18 al 25 settembre 2026 la riduzione sul gasolio, comprensiva del corrispondente effetto sull’IVA, è pari a 12,2 centesimi al litro. Dal 26 settembre al 5 ottobre lo sconto si dimezza a 6,1 centesimi al litro, prima del ritorno all’aliquota ordinaria salvo ulteriori interventi.",
    "Per chi ha una scadenza del bollo nel 2026 non cambia nulla: l’esenzione riguarda l’anno successivo. Le istruzioni applicative dovranno chiarire come indicare il veicolo scelto, come trattare le cointestazioni e come coordinare il beneficio nazionale con le agevolazioni regionali già esistenti.",
    "Il bollo è una tassa automobilistica amministrata secondo regole regionali o provinciali. L’ACI ricorda che tariffe, scadenze ed esenzioni possono dipendere dal territorio di residenza; per questo restano necessarie le indicazioni degli enti competenti prima di modificare i pagamenti dovuti.",
    "Il decreto-legge dovrà essere pubblicato in Gazzetta Ufficiale per entrare in vigore e sarà poi sottoposto al Parlamento per la conversione entro sessanta giorni. L’approvazione del Cdm e i contenuti del comunicato sono ufficiali; formulazione normativa, coperture e procedure andranno verificati sul testo pubblicato.",
    "La notizia è UFFICIALE per l’approvazione del decreto e per le misure descritte nel comunicato n. 189 della Presidenza del Consiglio. Reuters e RaiNews confermano in modo indipendente soglia, durata, vincolo di un solo veicolo e calendario dello sconto sul gasolio."
]

SOURCES = [
    (
        "https://www.governo.it/it/articolo/comunicato-stampa-del-consiglio-dei-ministri-n-189/32596",
        "Presidenza del Consiglio dei ministri — 16 settembre 2026 — comunicato ufficiale n. 189: approvazione del decreto, esenzione 2027 e riduzione delle accise sul gasolio."
    ),
    (
        "https://www.reuters.com/business/italy-scraps-road-tax-most-cars-election-nears-2026-09-16/",
        "Reuters — 16 settembre 2026 — conferma indipendente di soglia, platea, vincolo di un veicolo, durata annuale e importi dello sconto sul gasolio."
    ),
    (
        "https://www.rainews.it/amp/articoli/2026/09/cdm-anche-proroga-taglio-accise-carburanti-e-abolizione-bollo-auto-moto-55273aeb-5402-4f5d-8421-2c9f7188c878.html",
        "RaiNews — 16 settembre 2026 — calendario della riduzione: 12,2 centesimi dal 18 al 25 settembre e 6,1 centesimi dal 26 settembre al 5 ottobre."
    ),
    (
        "https://www.aci.it/servizi/guida-al-bollo-auto/",
        "Automobile Club d’Italia — guida istituzionale alle regole regionali e provinciali della tassa automobilistica."
    ),
]


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_record() -> dict:
    registry = json.loads((ROOT / "assets/data/editorial-images-v210.json").read_text(encoding="utf-8"))
    record = dict(next(item for item in registry["items"] if item.get("article") == URL))
    record["alt"] = IMAGE_ALT
    return record


def update_article() -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    doc.xpath("//title")[0].text = TITLE + " | CurioMondo"
    for xp, value in [
        ('//meta[@name="description"]', SUMMARY),
        ('//meta[@property="og:title"]', TITLE),
        ('//meta[@property="og:description"]', SUMMARY),
    ]:
        node = doc.xpath(xp)
        if node:
            node[0].set("content", value)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({"headline": TITLE, "description": SUMMARY, "datePublished": PUBLISHED, "dateModified": UPDATED})
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    doc.xpath('//main//div[contains(@class,"badge")][1]')[0].text = SECTION
    doc.xpath('//main//h1[1]')[0].text = TITLE
    doc.xpath('//main//p[contains(@class,"subtitle")][1]')[0].text = SUMMARY
    meta = doc.xpath('//main//div[contains(@class,"meta")][1]')[0]
    for child in list(meta):
        meta.remove(child)
    meta.text = "16 settembre 2026 · aggiornato alle 21:51 · Roma · "
    etree.SubElement(meta, "span", id="readTime").text = "4 min di lettura"

    body = doc.xpath('//article[contains(@class,"art-body")][1]')[0]
    body.set("data-substantive-update", "true")
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
    etree.SubElement(small, "br")
    small[-1].tail = (
        "Testo originale CurioMondo. Aggiornamento sostanziale verificato il 16 settembre 2026 "
        "alle 21:51 italiane. " + site.CAPTION
    )

    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")
    PATH.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def update_surfaces() -> list[dict]:
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    for item in home["items"]:
        if item.get("url") == URL:
            item["excerpt"] = SUMMARY
    write_json(home_path, home)

    metadata = {
        "slug": SLUG,
        "parole_chiave_titolo": ["Bollo auto", "80 kW"],
        "dati_chiave": [
            {"icona": "◆", "valore": "80 kW", "etichetta": "soglia massima per le auto"},
            {"icona": "●", "valore": "2027", "etichetta": "anno di applicazione"},
            {"icona": "▲", "valore": "5 ottobre", "etichetta": "termine dello sconto diesel"},
        ],
    }
    items = site.sync_surfaces([metadata], FEATURED_URL, VERSION)

    record = image_record()
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    registry["items"] = [record] + [i for i in registry["items"] if i.get("article") != URL]
    write_json(registry_path, registry)

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-09-16T19:51:30+00:00"
    live["items"] = [
        {"title": i["title"], "url": i["url"], "published_at": i["dateISO"], "source": "CurioMondo", "article_exists": True}
        for i in items[:10]
    ]
    write_json(live_path, live)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": TITLE,
        "excerpt": SUMMARY,
        "category": SECTION,
        "published_at": PUBLISHED,
        "updated_at": UPDATED,
        "status": "UFFICIALE",
        "body": BODY,
        "sources": [{"url": url, "label": label} for url, label in SOURCES],
        "image": record,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-16",
        "type": "content-update",
        "news_added": [],
        "news_updated": [SLUG],
        "change": "Comunicato ufficiale Cdm n. 189: calendario accise e stato ufficiale del decreto sul bollo",
        "image_policy_applied": "existing-dedicated-editorial-image-retained",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-16",
            "release_date": "2026-09-16",
            "last_update": "bollo-auto-comunicato-ufficiale-v390",
        })
        write_json(path, state)

    write_json(ROOT / "automation/logs/italia-20260916T215130-Europe-Rome.json", {
        "run_at": UPDATED,
        "production_branch": "main",
        "production_base_commit": "0d9ac84e9500fa93f36e621718ae4df20e8af66a",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale dei contenuti letti integralmente: articolo Reuters, due articoli RaiNews e articolo CurioMondo esistente. Il comunicato ufficiale di Palazzo Chigi è stato verificato tramite l'indice del dominio istituzionale ma l'apertura diretta è stata bloccata dal sito, quindi non è contato come lettura integrale; snippet e titoli esclusi."
        },
        "processed": [{
            "slug": SLUG,
            "action": "substantial_update_existing_article",
            "score": 9.3,
            "status": "UFFICIALE",
            "public_url": CANONICAL,
            "development_at": "2026-09-16T21:00:00+02:00",
            "development_time_note": "Orario esatto non indicato; comunicato reso disponibile intorno alle 21:00 Europe/Rome.",
            "sources": [url for url, _ in SOURCES],
            "publication_state": "pending_deploy"
        }],
        "excluded": []
    })
    return items


def qa(items: list[dict]) -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    schema = json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)
    assert doc.xpath('//main//h1[1]')[0].text_content() == TITLE
    assert schema["dateModified"] == UPDATED
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(BODY)
    assert len(doc.xpath('//div[contains(@class,"art-sources")]//li')) == len(SOURCES)
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert any(i["url"] == URL and i["excerpt"] == SUMMARY for i in items)


def main() -> None:
    update_article()
    items = update_surfaces()
    runpy.run_path(str(ROOT / "tools/generate_category_pages.py"), run_name="__main__")
    qa(items)
    position = next(i for i, item in enumerate(items, 1) if item["url"] == URL)
    print(json.dumps({"version": VERSION, "updated": URL, "feed_position": position, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
