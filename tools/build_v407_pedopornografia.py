#!/usr/bin/env python3
"""Pubblica l'operazione Fly Trap contro una rete pedopornografica online."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 407
PUBLISHED = "2026-09-17T13:52:12+02:00"
SLUG = "pedopornografia-online-17-arresti-rete-mille-utenti-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Pedopornografia online, 17 arresti: rete da oltre mille utenti",
    "sommario": "L'operazione Fly Trap, coordinata dalla Dda di Roma, ha portato a 17 misure cautelari, dieci delle quali eseguite in flagranza. Un agente sotto copertura ha ricostruito per circa un anno la struttura del gruppo.",
    "categoria": "Cronaca",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["17 arresti", "oltre mille utenti"],
    "dati_chiave": [
        {"icona": "◆", "valore": "17", "etichetta": "misure cautelari eseguite"},
        {"icona": "●", "valore": "1.009+", "etichetta": "partecipanti nella rete privata"},
        {"icona": "↗", "valore": "282,9 GB", "etichetta": "contenuti digitali acquisiti"},
    ],
    "paragrafi": [
        "La Polizia di Stato ha eseguito il 17 settembre 17 misure cautelari nell'operazione Fly Trap, coordinata dalla Direzione distrettuale antimafia di Roma. L'indagine riguarda una rete transnazionale accusata di distribuire online materiale pedopornografico attraverso gruppi privati e pagamenti in criptovalute.",
        "Dieci persone sono state arrestate in flagranza; una misura è stata eseguita in Svizzera e le altre in Italia, tra Lombardia, Veneto, Puglia e Campania. Le contestazioni sono nella fase delle indagini: le misure cautelari non equivalgono a condanne definitive e le responsabilità individuali dovranno essere accertate nel processo.",
        "Gli investigatori hanno acquisito oltre 22 mila video, 34 mila immagini e 282,9 gigabyte di file. Queste cifre descrivono il materiale trovato, non il numero delle vittime né quello di episodi distinti: gli stessi contenuti possono essere duplicati o circolare in più archivi.",
        "L'inchiesta è iniziata nel 2024 dopo informazioni trasmesse dalla statunitense Homeland Security Investigations su un gruppo privato chiamato New Saga. Un agente italiano ha lavorato sotto copertura per circa un anno, ricostruendo ruoli e canali fino a ottenere funzioni di amministratore.",
        "Secondo la nota della Polizia riportata dalle fonti consultate, la comunità privata contava oltre 1.009 partecipanti. L'accesso e la permanenza erano legati a piccoli versamenti in criptovaluta, definiti donazioni, oppure alla condivisione di nuovo materiale; alcuni amministratori usavano canali separati per coordinarsi e ridurre il rischio di controlli.",
        "Il procuratore di Roma Francesco Lo Voi ha descritto l'organizzazione come una struttura paragonabile a una società multinazionale. Nella conferenza stampa ha indicato oltre venti utenti individuati in Italia e pagamenti mensili tra 3 e 9 dollari, mentre le figure chiave citate avevano tra 22 e 28 anni.",
        "La cooperazione con l'agenzia statunitense e l'esecuzione di una misura in Svizzera mostrano la dimensione internazionale dell'indagine. Restano da chiarire le posizioni dei singoli indagati, l'estensione completa della rete fuori dall'Italia e l'eventuale identificazione di altre persone coinvolte.",
    ],
    "fonti": [
        {"url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/17/pedopornografia-online-la-polizia-arresta-17-persone_ad32372f-9816-4668-b1f6-7451c66f16c7.html", "descrizione": "ANSA — resoconto della nota della Polizia di Stato e della conferenza stampa della Procura di Roma: misure, sequestri, struttura e dichiarazioni."},
        {"url": "https://tg24.sky.it/cronaca/2026/09/17/pedopornografia-operazione-arresti", "descrizione": "Sky TG24 — conferma indipendente di numeri, localizzazione delle misure, origine dell'indagine e attività sotto copertura."},
        {"url": "https://www.tgcom24.mediaset.it/cronaca/pedopornografia-arresti_116685688-202602k.shtml", "descrizione": "TGCOM24 — conferma dell'operazione coordinata dalla Dda di Roma e delle 17 persone arrestate."},
        {"url": "https://www.ilgiornale.it/news/nazionale/pedopornografia-online-blitz-della-polizia-17-misure-cautelari-nelloperazione-fly-trap/", "descrizione": "il Giornale — riscontro sull'emissione delle 17 misure cautelari da parte del giudice per le indagini preliminari."},
    ],
    "correlati": [
        {"url": "/notizie/revolut-pec-istituzionale-italiana-dati-clienti-16-settembre-2026.html", "titolo": "Revolut, inchiesta a Reggio Calabria: Dna attiva e riscatto da 3 milioni"},
        {"url": "/notizie/ue-social-media-divieto-sotto-13-anni-proposta-von-der-leyen-16-settembre-2026.html", "titolo": "EU Kids Act, adottata la proposta sul divieto social sotto i 13 anni"},
        {"url": "/notizie/come-funziona-coppa-privacy-minori-online.html", "titolo": "Privacy dei minori online: che cos'è la COPPA e quali obblighi impone alle piattaforme?"},
    ],
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_image_variants() -> list[dict]:
    image = Image.open(SOURCE_IMAGE).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets" / "images" / "editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(),
        "alt": "Scena editoriale fotorealistica generata con IA: mani guantate esaminano dispositivi di memoria in un laboratorio informatico; nessuna persona identificabile e nessun contenuto illecito visibile.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "portraitFormat": "contextual-editorial-still-life",
        "reenactedEvent": False,
        "prompt": "Sensitive cybercrime editorial still life with gloved investigators examining storage devices; no minors, faces, suspects, explicit material, logos, readable text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace(
        'data-sensitive-context="true">',
        'data-sensitive-context="true" data-portrait-format="contextual-editorial-still-life">',
        1,
    )
    page_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Cronaca",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-17T11:30:00+02:00",
        "status": "CONFERMATA DA PIÙ FONTI",
        "public_url": PUBLIC_URL,
        "publication_state": "pending_deploy",
        "body": ARTICLE["paragrafi"],
        "sources": ARTICLE["fonti"],
        "image": image,
    })
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Pubblicata l'operazione Fly Trap contro una rete pedopornografica transnazionale",
        "image_policy_applied": "new-openai-sensitive-contextual-still-life-no-minors-no-explicit-content",
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
            "articleCount": int(state.get("articleCount", 0)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
            "last_update": "cronaca-pedopornografia-fly-trap-v407",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "italia-20260917T135212-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Cronaca",
        "production_branch": "main",
        "base_commit": "b23d9dc22665d9da4e18c43ef4e74d34e676e74d",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "distinct_domains": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: l'obiettivo di 500 contenuti completi non è stato raggiunto. La candidata pubblicata è stata verificata sul resoconto della nota ufficiale e della conferenza stampa, con tre riscontri editoriali distinti.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.8,
            "status": "CONFERMATA DA PIÙ FONTI",
            "decision": "publish",
            "sources": [x["url"] for x in ARTICLE["fonti"]],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
