#!/usr/bin/env python3
"""Aggiorna l'articolo sul maltempo con le criticità accertate a Empoli."""
from __future__ import annotations

from datetime import datetime
from html import escape
import json
from pathlib import Path
import sys

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from automation.newsroom.site import CAPTION, sync_surfaces

VERSION = 410
SLUG = "maltempo-allerta-arancione-liguria-emilia-romagna-17-settembre-2026"
UPDATED = "2026-09-17T15:49:25+02:00"
DEVELOPMENT = "2026-09-17T15:41:00+02:00"
TITLE = "Maltempo, Empoli attiva il Coc dopo 43 mm di pioggia in mezz'ora"
SUMMARY = (
    "Il Comune ha attivato il Centro operativo comunale dopo temporali violenti, "
    "allagamenti e danni ancora in valutazione. Criticità anche in Toscana, Lombardia "
    "e Friuli-Venezia Giulia; non risultano vittime o feriti negli episodi verificati."
)

BODY = [
    "Il Comune di Empoli ha attivato il Centro operativo comunale di protezione civile dopo un temporale che ha scaricato 43 millimetri di pioggia in mezz'ora. Il provvedimento, annunciato nel pomeriggio del 17 settembre, serve a coordinare soccorsi, assistenza alla popolazione e interventi sulle criticità provocate da allagamenti e raffiche di vento.",
    "L'amministrazione comunale parla di danni ingenti ancora in corso di accertamento e conferma allagamenti localizzati di strade e sottopassi. Il Coc resterà attivo fino al ritorno alla normalità; l'allerta gialla per temporali forti e rischio idrogeologico sul territorio comunale è indicata fino alle 23:59 del 19 settembre.",
    "Durante la fase più intensa, il Comune ha invitato a evitare gli spostamenti non necessari, i sottopassi e le strade transennate. I vigili del fuoco hanno soccorso automobilisti rimasti bloccati nei sottopassi; la stazione ferroviaria risultava interessata da un allagamento dell'accesso carrabile. Non sono state segnalate vittime o persone ferite.",
    "Le piogge hanno causato disagi anche in altre zone della Toscana. A Torre del Lago, in Versilia, un fulmine caduto vicino alla scuola primaria Giacomo Puccini ha danneggiato l'impianto elettrico: l'edificio è stato evacuato e gli alunni sono rientrati a casa, senza feriti. Allagamenti sono stati segnalati inoltre tra Massa, Carrara e Viareggio.",
    "A Como, un temporale notturno ha provocato smottamenti e accumuli di fango sulla viabilità. Via Oltrecolle e via Monte Grappa sono state chiuse per gli interventi di messa in sicurezza; fango e detriti hanno interessato anche la zona della stazione di Como Camerlata, con cancellazioni e ritardi ferroviari riferiti durante la mattinata.",
    "In Friuli-Venezia Giulia la sala operativa regionale e il numero unico 112 avevano ricevuto 38 segnalazioni dalle 6 del mattino. Allagamenti e cadute di alberi o rami sono stati registrati in più comuni, compresi Trieste, Udine, Pordenone e Lignano Sabbiadoro.",
    "L'allerta arancione della mattina in Liguria e in parte dell'Emilia-Romagna era stata emessa sulla base delle previsioni di temporali intensi. Gli effetti osservati nel corso della giornata non sono uniformi: i dati di Empoli descrivono un evento locale particolarmente concentrato e non possono essere estesi automaticamente a tutte le aree in allerta.",
    "Per le decisioni operative restano validi i bollettini regionali e gli avvisi dei Comuni. Durante temporali intensi è necessario evitare sottopassi, argini, scantinati e strade già allagate e non attraversare accumuli d'acqua di profondità incerta."
]

SOURCES = [
    {
        "url": "https://www.comune.empoli.fi.it/Novita/Comunicati/Attivato-il-Centro-Operativo-Comunale-per-allerta-meteo-codice-giallo",
        "descrizione": "Comune di Empoli — attivazione ufficiale del Centro operativo comunale, 43 mm di pioggia in mezz'ora e danni in corso di accertamento."
    },
    {
        "url": "https://www.protezionecivile.gov.it/it/comunicato-stampa/maltempo-allerta-arancione-liguria-e-emilia-romagna-1/",
        "descrizione": "Dipartimento della Protezione Civile — comunicato ufficiale con fenomeni previsti e livelli di allerta del 17 settembre 2026."
    },
    {
        "url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/17/maltempo-scatta-lallerta-arancione-per-temporali-sul-centro-piogge-intense_3f7a2954-eac8-44fc-839a-b57362319686.html",
        "descrizione": "ANSA — riscontro indipendente sulle criticità in Toscana, Lombardia e Friuli-Venezia Giulia."
    }
]

STATS = [
    {"icona": "◆", "valore": "43 mm", "etichetta": "pioggia in mezz'ora a Empoli"},
    {"icona": "●", "valore": "1 Coc", "etichetta": "attivato fino al ritorno alla normalità"},
    {"icona": "↗", "valore": "0 feriti", "etichetta": "negli episodi verificati"},
]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_page(path: Path) -> None:
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    doc.xpath("//title")[0].text = f"{TITLE} | CurioMondo"
    for node in doc.xpath('//meta[@name="description"]'):
        node.set("content", SUMMARY)
    for prop, value in (("og:title", TITLE), ("og:description", SUMMARY)):
        for node in doc.xpath(f'//meta[@property="{prop}"]'):
            node.set("content", value)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({"headline": TITLE, "description": SUMMARY, "dateModified": UPDATED})
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    doc.xpath('//main[contains(@class,"wrap")]//h1[1]')[0].text = TITLE
    doc.xpath('//main[contains(@class,"wrap")]//p[contains(@class,"subtitle")][1]')[0].text = SUMMARY

    insight = doc.xpath('//section[contains(@class,"cm-insight")]//div[contains(@class,"cm-insight-grid")]')[0]
    for child in list(insight):
        insight.remove(child)
    for stat in STATS:
        block = html.Element("div")
        strong = html.Element("strong"); strong.text = stat["valore"]
        span = html.Element("span"); span.text = stat["etichetta"]
        block.extend([strong, span]); insight.append(block)

    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in BODY:
        node = html.Element("p"); node.text = paragraph; body.append(node)

    source_list = doc.xpath('//div[contains(@class,"art-sources")]//ul[1]')[0]
    for child in list(source_list):
        source_list.remove(child)
    for source in SOURCES:
        li = html.Element("li")
        a = html.Element("a", href=source["url"], rel="noopener noreferrer", target="_blank")
        a.text = source["descrizione"]; li.append(a); source_list.append(li)

    for node in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        node.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for node in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        node.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")

    path.write_text('<!doctype html>\n' + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def main() -> None:
    data_path = ROOT / "contenuti" / "notizie" / f"{SLUG}.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data.update({
        "title": TITLE,
        "excerpt": SUMMARY,
        "updated_at": UPDATED,
        "development_at": DEVELOPMENT,
        "development_time_note": "Il Comune di Empoli ha aggiornato il comunicato ufficiale alle 15:41 Europe/Rome.",
        "status": "UFFICIALE",
        "publication_state": "pending_deploy",
        "body": BODY,
        "sources": SOURCES,
    })
    write_json(data_path, data)

    page_path = ROOT / "notizie" / f"{SLUG}.html"
    update_page(page_path)

    feed_path = ROOT / "assets" / "data" / "home-feed-v210.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8"))
    for item in feed.get("items", []):
        if item.get("url") == f"/notizie/{SLUG}.html":
            item["excerpt"] = SUMMARY
            break
    write_json(feed_path, feed)

    article = {
        "slug": SLUG,
        "titolo": TITLE,
        "sommario": SUMMARY,
        "categoria": "Ambiente",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["Empoli attiva il Coc", "43 mm di pioggia in mezz'ora"],
        "dati_chiave": STATS,
        "paragrafi": BODY,
        "fonti": SOURCES,
    }
    sync_surfaces([article], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-update",
        "news_added": [],
        "news_updated": [SLUG],
        "change": "Aggiornato il maltempo con l'attivazione del Coc di Empoli e le criticità accertate",
        "image_policy_applied": "existing-editorial-image-retained",
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
            "last_update": "ambiente-maltempo-empoli-coc-v410",
        })
        write_json(path, state)

    log = {
        "run_at": UPDATED,
        "scope": "Italia / Ambiente",
        "production_branch": "main",
        "base_commit": "383f78d2cf51d66c29033ba2b14c98991e2c1d08",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 3,
            "distinct_domains": 3,
            "target_reached": False,
            "note": "Conteggio prudenziale: letti integralmente il comunicato del Comune di Empoli, l'aggiornamento ANSA sul maltempo e l'articolo CurioMondo esistente. Il target di 500 contenuti non è stato raggiunto e non è stato inventato."
        },
        "processed": [{
            "title": TITLE,
            "editorial_score": 8.3,
            "status": "UFFICIALE",
            "decision": "update_existing",
            "sources": [source["url"] for source in SOURCES],
            "public_url": f"https://curiomondo.it/notizie/{SLUG}",
            "publication_state": "pending_deploy",
        }],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    }
    write_json(ROOT / "automation" / "logs" / "italia-20260917T154925-Europe-Rome.json", log)
    print(json.dumps({"status": "ok", "version": VERSION, "updated": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
