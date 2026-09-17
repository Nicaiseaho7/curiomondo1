#!/usr/bin/env python3
"""Pubblica i nuovi dati IOM sulla rotta del Mediterraneo centrale verso l'Italia."""
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

VERSION = 416
PUBLISHED = "2026-09-17T20:58:00+02:00"
DEVELOPMENT = "2026-09-17"
SLUG = "migranti-arrivi-italia-dimezzati-996-morti-dispersi-iom-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "migranti-iom-italia-v416.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Migranti, arrivi via mare verso l'Italia oltre dimezzati: 996 morti o dispersi",
    "sommario": "I dati IOM fino al 15 settembre indicano oltre 21.000 arrivi sulla rotta del Mediterraneo centrale verso l'Italia, contro oltre 48.000 nello stesso periodo del 2025. Le persone morte o disperse salgono però da 844 a 996; il bilancio reale potrebbe essere più alto.",
    "categoria": "Italia",
    "luogo": "Italia / Mediterraneo centrale",
    "formato": "standard",
    "parole_chiave_titolo": ["Migranti", "Italia", "996 morti o dispersi"],
    "dati_chiave": [
        {"icona": "◆", "valore": ">21.000", "etichetta": "arrivi verso l'Italia nel 2026"},
        {"icona": "●", "valore": ">48.000", "etichetta": "arrivi nello stesso periodo del 2025"},
        {"icona": "↗", "valore": "996", "etichetta": "morti o dispersi sulla rotta"},
    ],
    "paragrafi": [
        "Oltre 21.000 migranti e rifugiati sono arrivati via mare in Italia attraverso il Mediterraneo centrale dall'inizio del 2026 al 15 settembre, contro oltre 48.000 nello stesso periodo del 2025. Lo indicano i nuovi dati dell'Organizzazione internazionale per le migrazioni, pubblicati giovedì 17 settembre. Sulla stessa rotta risultano 996 morti o dispersi.",
        "Il calo degli arrivi supera la metà ed è il più marcato tra le principali rotte marittime verso l'Europa. Il numero delle vittime registrate, invece, cresce rispetto alle 844 dello stesso periodo dell'anno precedente. Arrivi più bassi non significano quindi viaggi più sicuri.",
        "Il dato di 996 comprende persone morte e persone disperse documentate nel Mediterraneo centrale. Non è un conteggio definitivo: l'IOM avverte che molti naufragi e sparizioni non vengono confermati e possono restare fuori dalle statistiche. Il bilancio reale potrebbe perciò essere più alto.",
        "Nel complesso, quasi 60.000 persone hanno raggiunto le coste europee via mare entro il 15 settembre, contro circa 98.000 un anno prima: una diminuzione del 39%. Nello stesso intervallo i morti o dispersi sulle rotte del Mediterraneo e dell'Atlantico sono saliti da 1.999 a 2.292.",
        "La fotografia italiana è particolarmente rilevante perché la rotta centrale collega soprattutto le partenze dal Nord Africa alle coste italiane. I flussi possono però cambiare rapidamente tra rotte, Paesi di partenza e destinazioni: i numeri non dimostrano da soli l'effetto di una singola politica nazionale o europea.",
        "L'IOM chiede maggiore cooperazione internazionale per le operazioni di soccorso, il contrasto ai trafficanti e l'apertura di canali legali di ingresso. La direttrice generale Amy Pope ha sottolineato che quasi ogni morte o scomparsa in mare è prevenibile. È una posizione dell'agenzia ONU, distinta dai dati numerici che documentano il fenomeno.",
        "Le cifre diffuse sono aggiornate al 15 settembre e possono essere riviste quando emergono nuovi sbarchi o informazioni sui naufragi. Anche il confronto con il 2025 usa lo stesso periodo dell'anno, evitando di accostare un dato parziale a un intero anno solare.",
        "I prossimi indicatori da seguire sono gli arrivi effettivi registrati dalle autorità italiane, gli eventi di ricerca e soccorso e gli aggiornamenti del Missing Migrants Project. Il punto centrale resta il divario tra la forte riduzione degli approdi e l'aumento delle persone morte o disperse sulla rotta verso l'Italia.",
    ],
    "fonti": [
        {
            "url": "https://www.iom.int/news/new-iom-data-migrant-arrivals-europe-fall-39-2026-while-deaths-continue-rise",
            "descrizione": "IOM — comunicato con i dati aggiornati al 15 settembre su arrivi, morti e dispersi lungo le rotte marittime europee.",
        },
        {
            "url": "https://apnews.com/article/migration-refugees-deaths-mediterranean-atlantic-shipwrecks-fa512b3ac2a31b8c4a79ae0e981ec94c",
            "descrizione": "Associated Press — dati specifici sulla rotta del Mediterraneo centrale verso l'Italia e confronto con il 2025.",
        },
        {
            "url": "https://www.reuters.com/world/europe-migrant-sea-crossings-fall-become-more-deadly-iom-says-2026-09-17/",
            "descrizione": "Reuters — conferma indipendente dei dati europei IOM e dell'avvertenza sul probabile sottoconteggio.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/tunisia-naufragio-migranti-italia-11-morti-24-agosto-2026.html",
            "titolo": "Tunisia, naufragio sulla rotta per l'Italia: 11 morti",
        },
        {
            "url": "/notizie/cinque-paesi-ue-return-hub-migranti-5-settembre-2026.html",
            "titolo": "Migranti, cinque Paesi Ue chiedono centri di rimpatrio fuori dall'Unione",
        },
        {
            "url": "/notizie/come-funzionano-trasferimenti-richiedenti-asilo-europa.html",
            "titolo": "Come funzionano i trasferimenti dei richiedenti asilo tra gli Stati europei",
        },
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
    out.mkdir(parents=True, exist_ok=True)
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
        "alt": "Illustrazione editoriale generata con IA: un'imbarcazione di soccorso e una piccola barca nel Mediterraneo al tramonto; scena simbolica, non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "prompt": "Ultrarealistic contextual editorial image of a generic rescue vessel and a small boat at distance on the Mediterranean at dawn; no real event, text, logos or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('<section class="curio-related">', '<section class="curio-related" data-curated-related="true">', 1)
    page = page.replace('curiomondo-article-v210.js?v=416', 'curiomondo-article-v210.js?v=416-related1', 1)
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
        "development_at": DEVELOPMENT,
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
        "change": "Pubblicati i dati IOM sulla rotta del Mediterraneo centrale verso l'Italia",
        "image_policy_applied": "new-openai-contextual-editorial-image-no-text-no-logo",
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
            "last_update": "italia-migranti-iom-v416",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T205800-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia",
        "production_branch": "main",
        "base_commit": "6ac2eb0e7044ccd276c299f7c1dd68fefb426eb1",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 2,
            "distinct_domains": 3,
            "target_reached": False,
            "note": "Conteggio prudenziale: il target di 500 contenuti non è stato raggiunto e non è stato inventato. Sono stati letti integralmente i riscontri Reuters e Associated Press; i dati centrali derivano dal comunicato ufficiale IOM identificato e sono stati confrontati nelle due fonti indipendenti.",
        },
        "processed": [
            {
                "title": ARTICLE["titolo"],
                "editorial_score": 8.4,
                "status": "UFFICIALE",
                "decision": "publish",
                "sources": [x["url"] for x in ARTICLE["fonti"]],
                "public_url": PUBLIC_URL,
                "publication_state": "pending_deploy",
            },
            {
                "title": "Visita della presidente Meloni in Norvegia",
                "editorial_score": 6.8,
                "decision": "exclude_agenda_only_no_substantive_signed_outcome",
                "source": "https://www.reuters.com/business/energy/italys-meloni-visits-norway-boost-energy-critical-minerals-ties-2026-09-17/",
            },
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
