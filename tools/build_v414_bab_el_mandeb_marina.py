#!/usr/bin/env python3
"""Pubblica la preparazione di una possibile missione navale italiana a Bab el-Mandeb."""
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

VERSION = 414
PUBLISHED = "2026-09-17T19:57:00+02:00"
DEVELOPMENT = "2026-09-17T18:50:54+02:00"
SLUG = "bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Bab el-Mandeb, Crosetto prepara una missione navale per i mercantili italiani",
    "sommario": "Il ministro della Difesa ha attivato la Marina per predisporre misure a tutela del transito delle navi italiane. Numero di unità, tempi e configurazione dell'eventuale missione devono ancora essere decisi con governo e Parlamento.",
    "categoria": "Politica",
    "luogo": "La Spezia / Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Bab el-Mandeb", "Crosetto", "missione navale", "mercantili italiani"],
    "dati_chiave": [
        {"icona": "◆", "valore": "17/9", "etichetta": "data dell'attivazione preparatoria"},
        {"icona": "●", "valore": "0", "etichetta": "unità navali finora indicate"},
        {"icona": "↗", "valore": "2", "etichetta": "passaggi citati: governo e Parlamento"},
    ],
    "paragrafi": [
        "Il ministro della Difesa Guido Crosetto ha attivato giovedì 17 settembre la Marina Militare affinché prepari le misure necessarie a proteggere il transito delle navi italiane nello stretto di Bab el-Mandeb. L'annuncio è arrivato al Forum Risorsa Mare di La Spezia, mentre le tensioni nell'area minacciano una rotta strategica tra Mar Rosso e Golfo di Aden.",
        "La decisione riguarda per ora la fase preparatoria. Crosetto non ha indicato quante unità potrebbero essere impiegate, quali navi verrebbero scelte, quando partirebbero né con quali regole operative. Ha precisato che la configurazione di un eventuale intervento dovrà essere valutata dal governo e dal Parlamento. Le fonti consultate non documentano quindi l'avvio di una scorta navale già operativa.",
        "Il ministro ha collegato l'iniziativa alla necessità di non lasciare esposti i mercantili italiani e ha detto di voler accelerare rispetto ai tempi del coordinamento europeo. Questo passaggio non equivale però all'uscita dell'Italia da EUNAVFOR Aspides, la missione difensiva dell'Unione europea nel Mar Rosso: non è stato annunciato alcun ritiro né un nuovo mandato che la sostituisca.",
        "Bab el-Mandeb collega il Mar Rosso e l'Oceano Indiano. Reuters riferisce che le forze Houthi controllano parti della costa yemenita affacciata sullo stretto. Minacce e attacchi hanno reso più rischiosa la navigazione, ma le responsabilità per i singoli episodi devono essere accertate caso per caso: le rivendicazioni delle parti non costituiscono da sole una prova.",
        "Per l'Italia il problema è anche economico. Deviare le navi intorno al Capo di Buona Speranza allunga i viaggi e può aumentare carburante, noli, assicurazioni e tempi di consegna. Crosetto ha richiamato il possibile effetto sui prezzi pagati da imprese e consumatori; non esiste però una stima ufficiale del costo attribuibile a questa specifica fase di tensione.",
        "La sicurezza riguarda anche cavi sottomarini, collegamenti energetici e infrastrutture marittime che attraversano o servono l'area. Una missione italiana dovrebbe quindi definire con precisione obiettivi, coordinamento con gli alleati, copertura giuridica e limiti d'impiego. Sono elementi essenziali per distinguere la protezione della navigazione commerciale da operazioni offensive, che non risultano annunciate.",
        "È ufficiale l'ordine politico di predisporre quanto serve per il transito sicuro delle navi italiane. Non sono invece ancora ufficiali l'invio di una forza, il numero delle unità, la data di partenza o le modalità di scorta. Nelle fonti consultate non è inoltre segnalato, in relazione a questo annuncio, un attacco già avvenuto contro un mercantile italiano.",
        "I prossimi riscontri decisivi saranno un atto del governo, gli eventuali passaggi parlamentari, l'identificazione delle navi, il calendario della missione e le comunicazioni operative alla navigazione. Fino a quel momento la formulazione corretta resta quella indicata dal ministro: la Marina è stata attivata per preparare le opzioni, mentre l'impiego concreto deve ancora essere definito.",
    ],
    "fonti": [
        {"url": "https://www.instagram.com/p/DdZKz-6AlS2/", "descrizione": "Ministero della Difesa — dichiarazione ufficiale di Crosetto sull'attivazione preparatoria della Marina."},
        {"url": "https://www.reuters.com/world/italy-readies-navy-protect-its-shipping-amid-bab-el-mandeb-tensions-2026-09-17/", "descrizione": "Reuters — annuncio, carattere preparatorio della decisione e contesto di sicurezza nello stretto."},
        {"url": "https://www.ansa.it/sito/notizie/politica/2026/09/17/crosetto-navi-militari-italiane-a-bab-el-mandeb-per-ripristino-dei-traffici_5b0db8d7-6df3-4d2b-838c-9d5eca2fce0e.html", "descrizione": "ANSA — dichiarazioni al Forum Risorsa Mare e passaggi ancora richiesti a governo e Parlamento."},
        {"url": "https://www.eeas.europa.eu/eunavfor-aspides/eunavfor-aspides-mandate-video_en", "descrizione": "Servizio europeo per l'azione esterna — mandato e natura difensiva dell'operazione EUNAVFOR Aspides."},
    ],
    "correlati": [
        {"url": "/notizie/guerra-iran-yemen-houthi-arabia-saudita-17-settembre-2026.html", "titolo": "Guerra USA-Iran, il fronte si allarga: scontri tra Houthi e Arabia Saudita"},
        {"url": "/notizie/hormuz-sette-navi-traffico-minimi-21-agosto-2026.html", "titolo": "Stretto di Hormuz, il traffico scende a sette navi in un giorno"},
        {"url": "/notizie/italia-non-partecipa-esercitazioni-volenterosi-ucraina-ottobre-25-agosto-2026.html", "titolo": "Ucraina, l'Italia non parteciperà alle esercitazioni dei Volenterosi"},
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
        "alt": "Illustrazione editoriale generata con IA di una fregata italiana che accompagna un mercantile verso Bab el-Mandeb; scena non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultrarealistic editorial illustration of a generic Italian Navy frigate guarding a civilian container ship near Bab el-Mandeb; no combat, text, logos or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page_path.write_text(page, encoding="utf-8")

    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Politica",
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
        "change": "Pubblicata l'attivazione preparatoria della Marina per Bab el-Mandeb",
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
            "articleCount": 386,
            "generatedEditorialImages": 204,
            "last_update": "politica-bab-el-mandeb-marina-v414",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T195700-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Politica",
        "production_branch": "main",
        "base_commit": "e7dd2d89c25a4c3953d3a452bf28d10b60aaf5ef",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 11,
            "distinct_domains": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: il target di 500 contenuti non è stato raggiunto e non è stato inventato. Sono state aperte le principali sezioni ANSA e lette integralmente le fonti pertinenti; la candidata pubblicata è stata verificata sulla dichiarazione ufficiale del Ministero, Reuters, ANSA e documentazione UE.",
        },
        "processed": [
            {
                "title": ARTICLE["titolo"],
                "editorial_score": 8.6,
                "status": "UFFICIALE",
                "decision": "publish",
                "sources": [x["url"] for x in ARTICLE["fonti"]],
                "public_url": PUBLIC_URL,
                "publication_state": "pending_deploy",
            },
            {
                "title": "Pioggia agli Uffizi, acqua sulla teca del Bacco di Caravaggio",
                "editorial_score": 6.6,
                "decision": "exclude_below_threshold_no_damage_to_work",
                "source": "https://www.ansa.it/sito/notizie/cronaca/2026/09/17/maltempo-pioggia-si-infiltra-agli-uffizi-e-bagna-teca-di-un-caravaggio_7a36b18b-72a9-4de1-8024-abdebc7faf34.html",
            },
            {
                "title": "Visita della presidente Meloni in Norvegia",
                "editorial_score": 6.8,
                "decision": "exclude_agenda_only_no_substantive_signed_outcome",
            },
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
