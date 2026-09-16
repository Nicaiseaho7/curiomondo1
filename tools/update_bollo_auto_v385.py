#!/usr/bin/env python3
"""Aggiorna l'articolo sul bollo dopo l'approvazione del decreto in Cdm."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 385
SLUG = "bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
PATH = ROOT / "notizie" / f"{SLUG}.html"
FEATURED_URL = "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html"
PUBLISHED = "2026-09-16T16:48:39+02:00"
UPDATED = "2026-09-16T17:48:56+02:00"
TITLE = "Bollo auto, il Cdm approva l’esenzione fino a 80 kW per il 2027"
SUMMARY = (
    "Il decreto-legge approvato dal Cdm esenta nel 2027 le auto fino a 80 kW e, "
    "a determinate condizioni, ciclomotori e motocicli. Prorogato al 5 ottobre "
    "il taglio delle accise sul gasolio; il testo pubblicato chiarirà le modalità operative."
)
SECTION = "Italia"
IMAGE_KEY = f"{SLUG}-ai-openai-v382"
IMAGE_ALT = (
    "Illustrazione editoriale di un’auto compatta e uno scooter parcheggiati "
    "in una strada italiana, non fotografia dell’annuncio."
)

BODY = [
    "Il Consiglio dei ministri ha approvato il 16 settembre 2026 un decreto-legge che abolisce per il 2027 il bollo sulle auto fino a 80 kW e interviene anche sui veicoli a due ruote. L’approvazione, riferita da ANSA alle 17:33, trasforma l’annuncio del pomeriggio in un provvedimento adottato dal governo, ma l’applicazione concreta richiede la pubblicazione del testo.",
    "La soglia di 80 kW equivale a circa 109 cavalli ed è il criterio indicato per le autovetture. Secondo le informazioni diffuse dopo la riunione, l’esenzione riguarda anche ciclomotori e motocicli, purché lo stesso proprietario non utilizzi già il beneficio per un’auto. Il limite resta quindi un solo veicolo agevolato per persona.",
    "Il beneficio vale per il solo 2027. Reuters, che ha esaminato una bozza prima della riunione, indica il periodo dal 1° gennaio al 31 dicembre e stima un costo di 2,36 miliardi di euro. Questi due dettagli provengono dalla bozza: andranno confrontati con la versione definitiva pubblicata in Gazzetta Ufficiale.",
    "La platea annunciata da Palazzo Chigi è di circa 14,5 milioni di veicoli: tutti i mezzi a due ruote interessati e oltre il 70% delle auto piccole e medie. Il dato descrive la portata stimata della misura, non il numero di contribuenti che riceveranno automaticamente l’esenzione.",
    "Per chi ha una scadenza nel 2026 non cambia nulla: il provvedimento riguarda l’anno successivo. Restano da definire le procedure con cui sarà associato il beneficio al veicolo scelto, il trattamento delle cointestazioni e l’eventuale coordinamento con esenzioni regionali già esistenti.",
    "Il decreto interviene anche sul caro carburanti. Il taglio delle accise sul gasolio viene prorogato fino al 5 ottobre con un meccanismo di riduzione graduale, definito «decalage». Le fonti consultate non riportano ancora il calendario completo e gli importi delle singole fasi, che non vanno quindi anticipati.",
    "Il bollo è una tassa automobilistica amministrata secondo regole regionali o provinciali. L’ACI ricorda che tariffe, scadenze ed esenzioni possono dipendere dal territorio di residenza; per questo le istruzioni degli enti competenti saranno necessarie per capire come la misura nazionale si innesterà sui sistemi esistenti.",
    "Il decreto-legge dovrà essere pubblicato in Gazzetta Ufficiale per entrare in vigore e sarà poi sottoposto al Parlamento per la conversione. Fino a quel momento, i proprietari non devono sospendere pagamenti già dovuti né basarsi soltanto sulla potenza dichiarata nei documenti del veicolo.",
    "La notizia è CONFERMATA DA PIÙ FONTI: ANSA documenta l’approvazione del Consiglio dei ministri, la soglia di 80 kW, l’anno 2027 e la proroga delle accise; Reuters conferma la platea, il vincolo di un veicolo e i dati contenuti nella bozza. Restano da verificare sul testo definitivo coperture, procedure e formulazione completa delle condizioni."
]

SOURCES = [
    (
        "https://www.ansa.it/canale_motori/notizie/istituzioni/2026/09/16/fonti-palazzo-chigi-oggi-via-il-bollo-per-auto-piccole-e-medie_cb12208d-db01-44ea-a5b5-7535dd0d2550.html",
        "ANSA — 16 settembre 2026, ore 17:33 — approvazione del decreto in Cdm, soglia di 80 kW, anno 2027 e proroga delle accise fino al 5 ottobre."
    ),
    (
        "https://www.reuters.com/business/italy-scraps-road-tax-most-cars-election-nears-2026-09-16/",
        "Reuters — 16 settembre 2026 — conferma indipendente della platea e del limite di un veicolo; durata e costo sono attribuiti alla bozza vista prima del Cdm."
    ),
    (
        "https://www.aci.it/servizi/guida-al-bollo-auto/",
        "Automobile Club d’Italia — guida istituzionale alle regole regionali e provinciali della tassa automobilistica."
    ),
]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_record() -> dict:
    registry = json.loads((ROOT / "assets/data/editorial-images-v210.json").read_text(encoding="utf-8"))
    record = next(item for item in registry["items"] if item.get("article") == URL)
    record = dict(record)
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
    schema.update({
        "headline": TITLE,
        "description": SUMMARY,
        "datePublished": PUBLISHED,
        "dateModified": UPDATED,
    })
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    doc.xpath('//main//div[contains(@class,"badge")][1]')[0].text = SECTION
    doc.xpath('//main//h1[1]')[0].text = TITLE
    doc.xpath('//main//p[contains(@class,"subtitle")][1]')[0].text = SUMMARY
    meta = doc.xpath('//main//div[contains(@class,"meta")][1]')[0]
    for child in list(meta):
        meta.remove(child)
    meta.text = "16 settembre 2026 · aggiornato alle 17:48 · Roma · "
    etree.SubElement(meta, "span", id="readTime").text = "3 min di lettura"

    hero = doc.xpath('//figure[contains(@class,"article-image")]//img[1]')[0]
    hero.set("alt", IMAGE_ALT)

    insight = doc.xpath('//section[contains(@class,"cm-insight")][1]')[0]
    replacement = html.fragment_fromstring(
        '<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span>'
        '<div class="cm-insight-grid"><div><strong>80 kW</strong><span>soglia massima per le auto</span></div>'
        '<div><strong>2027</strong><span>anno di applicazione</span></div>'
        '<div><strong>5 ottobre</strong><span>proroga del taglio delle accise</span></div></div></section>'
    )
    insight.getparent().replace(insight, replacement)

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
    etree.SubElement(small, "br")
    small[-1].tail = (
        "Testo originale CurioMondo. Aggiornamento sostanziale verificato il 16 settembre 2026 "
        "alle 17:48 italiane. " + site.CAPTION
    )

    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")
    PATH.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def update_records_and_surfaces() -> list[dict]:
    # sync_surfaces conserva l'estratto già presente: lo aggiorniamo prima del rebuild.
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    for item in home.get("items", []):
        if item.get("url") == URL:
            item["excerpt"] = SUMMARY
    write_json(home_path, home)

    metadata = {
        "slug": SLUG,
        "parole_chiave_titolo": ["Bollo auto", "80 kW"],
        "dati_chiave": [
            {"icona": "◆", "valore": "80 kW", "etichetta": "soglia massima per le auto"},
            {"icona": "●", "valore": "2027", "etichetta": "anno di applicazione"},
            {"icona": "▲", "valore": "5 ottobre", "etichetta": "proroga del taglio delle accise"},
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
    live["updated_at"] = "2026-09-16T15:48:56+00:00"
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
        "status": "CONFERMATA DA PIÙ FONTI",
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
        "change": "Aggiornamento bollo auto dopo l'approvazione del decreto in Cdm: soglia 80 kW, validità 2027 e proroga accise",
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
            "last_update": "bollo-auto-decreto-cdm-v385",
        })
        write_json(path, state)

    write_json(ROOT / "automation/logs/italia-20260916T174856-Europe-Rome.json", {
        "run_at": UPDATED,
        "production_branch": "main",
        "production_base_commit": "8d8a647275e77338284e070ac4628fed841e0869",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 3,
            "target_reached": False,
            "note": "Conteggio prudenziale: ANSA, Reuters e guida ACI letti integralmente; esclusi titoli, snippet, pagine duplicate e risultati di ricerca. Obiettivo non raggiunto; nessuna consultazione inventata."
        },
        "processed": [{
            "slug": SLUG,
            "action": "updated_existing_article",
            "score": 9.4,
            "status": "CONFERMATA DA PIÙ FONTI",
            "public_url": CANONICAL,
            "sources": [url for url, _ in SOURCES],
            "publication_state": "pending_deploy",
        }],
    })
    return items


def qa(items: list[dict]) -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    schema = json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)
    assert doc.xpath('//main//h1[1]')[0].text_content() == TITLE
    assert schema["datePublished"] == PUBLISHED and schema["dateModified"] == UPDATED
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(BODY)
    assert len(doc.xpath('//div[contains(@class,"art-sources")]//li')) == len(SOURCES)
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert any(i["url"] == URL and i["title"] == TITLE for i in items)
    assert len({i["url"] for i in items}) == len(items)


def main() -> None:
    update_article()
    items = update_records_and_surfaces()
    qa(items)
    position = next(i for i, item in enumerate(items, 1) if item["url"] == URL)
    print(json.dumps({"version": VERSION, "updated": URL, "feed_position": position, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
