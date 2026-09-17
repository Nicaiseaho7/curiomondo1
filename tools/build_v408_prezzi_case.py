#!/usr/bin/env python3
"""Pubblica i prezzi Istat delle abitazioni nel secondo trimestre 2026."""
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

VERSION = 408
PUBLISHED = "2026-09-17T14:53:53+02:00"
SLUG = "prezzi-case-italia-secondo-trimestre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Prezzi delle case, +4% in un anno: Torino accelera all'8,5%",
    "sommario": "L'Istat stima nel secondo trimestre un aumento dell'1,7% rispetto ai primi tre mesi del 2026 e del 4% su base annua. Le compravendite restano quasi ferme, mentre Torino e Roma registrano i rincari più marcati tra le città osservate.",
    "categoria": "Italia",
    "luogo": "Italia",
    "formato": "standard",
    "parole_chiave_titolo": ["+4% in un anno", "Torino accelera all'8,5%"],
    "dati_chiave": [
        {"icona": "◆", "valore": "+4,0%", "etichetta": "prezzi in un anno"},
        {"icona": "●", "valore": "+1,7%", "etichetta": "rispetto al trimestre precedente"},
        {"icona": "↗", "valore": "+0,1%", "etichetta": "compravendite su base annua"},
    ],
    "paragrafi": [
        "I prezzi delle abitazioni acquistate dalle famiglie in Italia sono aumentati nel secondo trimestre 2026 dell'1,7% rispetto ai tre mesi precedenti e del 4% rispetto allo stesso periodo del 2025. Sono stime preliminari pubblicate dall'Istat il 17 settembre e riguardano acquisti per uso abitativo o investimento.",
        "La crescita annua rallenta rispetto al 5,1% rilevato nel primo trimestre, ma resta diffusa. Le abitazioni nuove segnano un aumento del 5%, quelle esistenti del 3,7%; su base trimestrale gli incrementi sono rispettivamente del 2,7% e dell'1,5%.",
        "I rincari si accompagnano a volumi di compravendita quasi invariati. L'Osservatorio del mercato immobiliare dell'Agenzia delle Entrate registra infatti un aumento annuo dello 0,1% nel settore residenziale, dopo il 4,4% del trimestre precedente.",
        "Il Centro mostra la crescita annua più elevata, pari al 5,1%. Seguono Nord-Est al 4,2%, Nord-Ovest al 3,9% e Sud e Isole al 2,6%. Tutte le ripartizioni restano in aumento, ma fuori dal Centro il ritmo rallenta sensibilmente rispetto ai primi tre mesi dell'anno.",
        "Rispetto al primo trimestre, la decelerazione è particolarmente evidente nel Nord-Est, dal 6,3% al 4,2%, e nel Nord-Ovest, dal 5% al 3,9%. Nel Sud e nelle Isole la crescita passa dal 3,7% al 2,6%, mentre il Centro resta quasi stabile, dal 5,2% al 5,1%.",
        "Tra le città per cui l'Istat pubblica l'indice, Torino accelera all'8,5% annuo dal precedente 3,8%. Roma sale del 6,4%, mentre Milano registra un aumento più contenuto, pari al 2,4%, dopo il 7,1% del primo trimestre.",
        "La variazione acquisita per il 2026 è del 3,8%: indica quale sarebbe l'aumento medio dell'anno se l'indice restasse invariato nei trimestri successivi. Non è quindi una previsione e può cambiare con le prossime rilevazioni.",
        "L'indice misura l'andamento dei prezzi delle abitazioni comprate dalle famiglie, non quello degli affitti e neppure il costo di una casa specifica. Le medie territoriali possono inoltre nascondere differenze rilevanti tra quartieri, caratteristiche dell'immobile e stato di conservazione.",
    ],
    "fonti": [
        {"url": "https://www.istat.it/comunicato-stampa/prezzi-delle-abitazioni-dati-provvisori-ii-trimestre-2026/", "descrizione": "Istat — comunicato ufficiale con indice nazionale, componenti, ripartizioni territoriali e città; dati provvisori del secondo trimestre 2026."},
        {"url": "https://www.agenziaentrate.gov.it/portale/documents/d/guest/statisticheomi_res_ii_2026", "descrizione": "Agenzia delle Entrate, Osservatorio del mercato immobiliare — statistiche ufficiali sulle compravendite residenziali nel secondo trimestre 2026."},
    ],
    "correlati": [
        {"url": "/notizie/istat-inflazione-agosto-2026-energia-3-3-per-cento.html", "titolo": "Istat, l'inflazione sale al 3,3% ad agosto: pesano i prezzi dell'energia"},
        {"url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html", "titolo": "Bollo auto, il Cdm approva l'esenzione fino a 80 kW per il 2027"},
        {"url": "/notizie/affitto-genitori-separati-fondo-60-milioni-30-agosto-2026.html", "titolo": "Affitto dimezzato per i genitori separati: pronta la norma da 60 milioni"},
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
        "alt": "Scena editoriale fotorealistica generata con IA: chiavi di casa in primo piano e un quartiere residenziale italiano con edifici nuovi ed esistenti.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "portraitFormat": "editorial-architectural-still-life",
        "reenactedEvent": False,
        "prompt": "Ultra-realistic editorial view of an Italian residential neighborhood with old and new buildings and house keys in the foreground; no people, text, logos, charts or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace(
        'data-sensitive-context="false">',
        'data-sensitive-context="false" data-portrait-format="editorial-architectural-still-life">',
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
        "category": "Italia",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-17T11:00:00+02:00",
        "status": "UFFICIALE",
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
        "change": "Pubblicati i dati Istat sui prezzi delle abitazioni nel secondo trimestre 2026",
        "image_policy_applied": "new-openai-editorial-architectural-still-life-no-text-no-logo",
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
            "last_update": "italia-prezzi-case-istat-v408",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "italia-20260917T145353-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Economia",
        "production_branch": "main",
        "base_commit": "aa0cbe38ad723cd90ac536f0567783403899b769",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 6,
            "distinct_domains": 5,
            "target_reached": False,
            "note": "Conteggio prudenziale: l'obiettivo di 500 contenuti completi non è stato raggiunto. La candidata è stata verificata sul comunicato e sulla nota metodologica Istat, sui dati OMI dell'Agenzia delle Entrate e su riscontri editoriali; sono state inoltre esaminate e scartate l'agenda della visita in Norvegia e altre notizie prive di sviluppi concreti.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.2,
            "status": "UFFICIALE",
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
