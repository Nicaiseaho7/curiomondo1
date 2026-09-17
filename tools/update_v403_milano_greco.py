#!/usr/bin/env python3
"""Aggiorna l'articolo su Milano Greco Pirelli con il ripristino ufficiale RFI."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, sync_surfaces

VERSION = 403
RUN_AT = "2026-09-17T07:49:24+02:00"
SLUG = "milano-greco-pirelli-deragliamento-carro-merci-treni-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
RFI_URL = "https://www.rfi.it/it/news-e-media/infomobilita/aggiornamenti/2026/9/16/linea-milano---chiasso--milano---lecco-dalle-ore-20-45-circolazi.html"
TITLE = "Milano Greco Pirelli, circolazione regolare dopo il deragliamento"
SUMMARY = (
    "RFI comunica che dalle 05:40 del 17 settembre la circolazione sulle linee "
    "Milano-Chiasso e Milano-Lecco è tornata regolare. Il deragliamento di un carro merci "
    "aveva provocato rallentamenti, cancellazioni e limitazioni; non risultano feriti né fuoriuscite."
)

BODY = [
    "La circolazione ferroviaria sulle linee Milano-Chiasso e Milano-Lecco è tornata regolare dalle 05:40 di giovedì 17 settembre. Rete Ferroviaria Italiana ha comunicato alle 06:00 che i tecnici hanno ripristinato la piena funzionalità della linea in prossimità della stazione di Milano Greco Pirelli. L'aggiornamento è pubblicato nel bollettino ufficiale di infomobilità.",
    "L'interruzione era iniziata alle 20:45 di mercoledì 16 settembre, dopo l'uscita dai binari di un carro merci. Il blocco aveva coinvolto i collegamenti da Milano verso Como, Lecco, Sondrio e Ponte San Pietro, con rallentamenti, cancellazioni e limitazioni dei percorsi per treni Intercity e regionali.",
    "Una prima riapertura parziale era stata riferita alle 23:07 sulla direttrice Milano-Lecco-Sondrio. L'aggiornamento pubblicato da RFI nella mattina del 17 settembre chiude la fase di emergenza operativa: sulle due linee indicate non risultano più sospensioni legate a questo episodio.",
    "Secondo il Corriere della Sera, il convoglio era composto da carri cisterna destinati al trasporto di acrilonitrile stabilizzato, ma le cisterne erano vuote. Non sono state segnalate fuoriuscite di sostanze pericolose e non risultano persone ferite.",
    "Il ritorno alla regolarità riguarda la funzionalità dell'infrastruttura e non chiarisce ancora la causa del deragliamento. RFI aveva indicato inizialmente motivi tecnici in corso di accertamento; eventuali verifiche sul materiale rotabile e sulle responsabilità seguono un percorso distinto dalla riapertura della linea.",
    "Per i pendolari, il ripristino elimina la limitazione generale che minacciava gli spostamenti del mattino sulle direttrici interessate. Restano possibili effetti residui sui singoli convogli dopo una notte di cancellazioni e variazioni: orari e composizione del servizio vanno controllati sui canali dell'operatore ferroviario.",
    "La notizia è ora classificata UFFICIALE per il ripristino della circolazione, documentato dall'autorità che gestisce l'infrastruttura. La dinamica del deragliamento, l'assenza di feriti e la natura dei carri sono sostenute dalle ricostruzioni convergenti delle testate consultate; la causa tecnica non è ancora stata resa nota.",
]

SOURCES = [
    {"url": RFI_URL, "descrizione": "Rete Ferroviaria Italiana — aggiornamento ufficiale delle 06:00: circolazione regolare dalle 05:40 dopo il ripristino della piena funzionalità."},
    {"url": "https://milano.repubblica.it/cronaca/2026/09/16/news/deraglia_un_carro_merci_nella_stazione_di_greco_pirelli_a_milano-425589630/", "descrizione": "la Repubblica Milano — dinamica del deragliamento e direttrici ferroviarie coinvolte."},
    {"url": "https://milano.corriere.it/notizie/cronaca/26_settembre_16/milano-deraglia-treno-merci-a-greco-pirelli-circolazione-sospesa-su-linee-per-como-sondrio-e-tirano-esclusa-fuoriuscita-di-d25f7dba-316c-4282-9497-8246b071exlk.shtml", "descrizione": "Corriere della Sera Milano — carri cisterna vuoti, assenza di fuoriuscite e quadro delle interruzioni."},
    {"url": "https://it.marketscreener.com/notizie/riattivata-la-circolazione-solo-sulla-milano-lecco-sondrio-ce785bd2d088f221", "descrizione": "AWP/ANSA — riapertura parziale della direttrice Milano-Lecco-Sondrio alle 23:07."},
]

ARTICLE = {
    "slug": SLUG,
    "titolo": TITLE,
    "sommario": SUMMARY,
    "categoria": "Italia",
    "luogo": "Milano",
    "formato": "standard",
    "parole_chiave_titolo": ["Greco Pirelli", "circolazione regolare"],
    "dati_chiave": [
        {"icona": "◷", "valore": "20:45", "etichetta": "inizio della sospensione"},
        {"icona": "✓", "valore": "05:40", "etichetta": "circolazione tornata regolare"},
        {"icona": "●", "valore": "0", "etichetta": "feriti segnalati"},
    ],
    "paragrafi": BODY,
    "fonti": SOURCES,
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_text(node, value: str) -> None:
    for child in list(node):
        node.remove(child)
    node.text = value


def update_article_html() -> None:
    path = ROOT / "notizie" / f"{SLUG}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    doc.xpath("//title")[0].text = f"{TITLE} | CurioMondo"
    doc.xpath('//meta[@name="description"]')[0].set("content", SUMMARY)
    doc.xpath('//meta[@property="og:title"]')[0].set("content", TITLE)
    doc.xpath('//meta[@property="og:description"]')[0].set("content", SUMMARY)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({"headline": TITLE, "description": SUMMARY, "dateModified": RUN_AT})
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    replace_text(doc.xpath('//main[contains(@class,"wrap")]//h1[1]')[0], TITLE)
    replace_text(doc.xpath('//main[contains(@class,"wrap")]//p[contains(@class,"subtitle")][1]')[0], SUMMARY)

    grid = doc.xpath('//section[contains(@class,"cm-insight")]//div[contains(@class,"cm-insight-grid")]')[0]
    for child in list(grid):
        grid.remove(child)
    for datum in ARTICLE["dati_chiave"]:
        cell = etree.SubElement(grid, "div")
        etree.SubElement(cell, "strong").text = datum["valore"]
        etree.SubElement(cell, "span").text = datum["etichetta"]

    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in BODY:
        etree.SubElement(body, "p").text = paragraph

    sources = doc.xpath('//div[contains(@class,"art-sources")]//ul[1]')[0]
    for child in list(sources):
        sources.remove(child)
    for source in SOURCES:
        item = etree.SubElement(sources, "li")
        link = etree.SubElement(item, "a", href=source["url"], rel="noopener noreferrer", target="_blank")
        link.text = source["descrizione"]

    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")

    path.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def main() -> None:
    content_path = ROOT / "contenuti" / "notizie" / f"{SLUG}.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    content.update({
        "title": TITLE,
        "excerpt": SUMMARY,
        "updated_at": RUN_AT,
        "development_at": "2026-09-17T05:40:00+02:00",
        "development_time_note": "RFI ha comunicato alle 06:00 che la circolazione è tornata regolare dalle 05:40 del 17 settembre.",
        "status": "UFFICIALE",
        "publication_state": "pending_deploy",
        "body": BODY,
        "sources": SOURCES,
    })
    content.pop("verified_online_at", None)
    content.pop("verification", None)
    write_json(content_path, content)

    update_article_html()

    home_path = ROOT / "assets" / "data" / "home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    for item in home.get("items", []):
        if item.get("url") == f"/notizie/{SLUG}.html":
            item.update({"title": TITLE, "excerpt": SUMMARY})
            break
    write_json(home_path, home)
    sync_surfaces([ARTICLE], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-update",
        "news_added": [],
        "news_updated": [SLUG],
        "change": "Aggiornato il deragliamento di Milano Greco Pirelli con il ripristino ufficiale della circolazione",
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
            "date": "2026-09-17",
            "release_date": "2026-09-17",
            "last_update": "italia-milano-greco-ripristino-v403",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T074924-Europe-Rome.json", {
        "run_at": RUN_AT,
        "scope": "Italia / Trasporti",
        "production_branch": "main",
        "base_commit": "be1b34f02d5c148d69ce6269f9a2b1e4478df500",
        "coverage": {
            "distinct_full_contents_consulted": 5,
            "target": 500,
            "target_reached": False,
            "note": "Conteggio limitato ai contenuti aperti integralmente in questa esecuzione; titoli e snippet esclusi.",
        },
        "processed": [{
            "title": TITLE,
            "editorial_score": 8.1,
            "status": "UFFICIALE",
            "decision": "update_existing_article",
            "sources": [item["url"] for item in SOURCES],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "updated": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
