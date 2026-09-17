#!/usr/bin/env python3
"""Pubblica l'allargamento del conflitto al fronte saudita-yemenita."""
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

VERSION = 401
PUBLISHED = "2026-09-17T07:11:14+02:00"
SLUG = "guerra-iran-yemen-houthi-arabia-saudita-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Guerra USA-Iran, il fronte si allarga: scontri tra Houthi e Arabia Saudita",
    "sommario": "Gli Houthi rivendicano nuovi attacchi contro obiettivi sauditi, mentre forze sostenute da Riad confermano raid su posizioni del gruppo in Yemen. Trump dice di sperare che la guerra sia vicina alla fine, ma non risulta annunciato alcun accordo.",
    "categoria": "Mondo",
    "luogo": "Medio Oriente",
    "formato": "standard",
    "parole_chiave_titolo": ["fronte si allarga", "Houthi e Arabia Saudita"],
    "dati_chiave": [
        {"icona": "◆", "valore": "2", "etichetta": "obiettivi sauditi indicati dagli Houthi"},
        {"icona": "●", "valore": "30 km", "etichetta": "fascia vietata ai dipendenti USA presso il confine"},
        {"icona": "↗", "valore": "1,2%", "etichetta": "calo del Brent nei primi scambi di giovedì"},
    ],
    "paragrafi": [
        "La guerra tra Stati Uniti, Israele e Iran si è estesa in modo più netto al fronte tra Yemen e Arabia Saudita. Gli Houthi, sostenuti da Teheran, hanno rivendicato nuovi lanci di droni e missili contro il porto petrolifero saudita di Yanbu e la base aerea di Khamis Mushait. Riad non ha confermato pubblicamente i singoli attacchi indicati dal gruppo.",
        "Sul versante opposto, funzionari del governo yemenita appoggiato dall'Arabia Saudita hanno riconosciuto che le proprie forze e quelle saudite stanno colpendo posizioni Houthi. La monarchia non ha però confermato direttamente le operazioni. Il portavoce militare Houthi Yahya Saree sostiene che in una settimana siano stati condotti 450 raid: il numero resta una dichiarazione di parte non verificata indipendentemente.",
        "Il presidente statunitense Donald Trump ha detto ai giornalisti di sperare che il conflitto sia vicino alla conclusione e ha affermato che l'Iran vorrebbe un'intesa. Non ha fornito dettagli sui contatti che dice di avere ricevuto da Teheran. Le sue parole documentano un auspicio politico, non l'esistenza di un cessate il fuoco o di un negoziato concluso.",
        "La cautela è necessaria anche perché gli obiettivi dichiarati da Washington sono cambiati più volte dall'inizio della guerra, il 28 febbraio. Al momento non risultano comunicati congiunti degli Stati Uniti e dell'Iran né un calendario negoziale ufficiale. La situazione sul terreno, intanto, mostra combattimenti e rischi che si stanno spostando verso la penisola arabica e il Mar Rosso.",
        "Il Dipartimento di Stato americano mantiene l'Arabia Saudita al livello 3, che invita a riconsiderare i viaggi, e vieta ai dipendenti governativi di avvicinarsi entro 20 miglia, circa 30 chilometri, dal confine yemenita. L'avviso cita il rischio di conflitto armato, attacchi con droni e missili e minacce provenienti dallo Yemen.",
        "Associated Press riferisce che l'escalation ha già prodotto un forte impatto umanitario nello Yemen. Più di 125.000 persone sarebbero state costrette a lasciare le proprie case, mentre strutture sanitarie e aiuti faticano a raggiungere le aree coinvolte. Queste cifre descrivono una crisi in rapido movimento e potrebbero essere aggiornate dalle organizzazioni internazionali.",
        "La dimensione energetica rende il nuovo fronte rilevante anche fuori dalla regione. La condotta saudita Est-Ovest, che permette di trasferire greggio dal Golfo al Mar Rosso evitando lo Stretto di Hormuz, è stata danneggiata e resta sotto pressione. Un'interruzione prolungata ridurrebbe una delle principali alternative logistiche in una fase di traffico già fortemente limitato nello stretto.",
        "Giovedì mattina il petrolio ha comunque registrato un arretramento: alle 02:49 italiane il Brent perdeva l'1,2% a 104,59 dollari al barile e il WTI l'1,1% a 101,29 dollari. Il calo è stato collegato alle offerte di carichi sauditi aggiuntivi attraverso l'Oman, che hanno attenuato temporaneamente i timori di carenze immediate.",
        "Il ribasso non elimina il rischio strutturale. Prima della guerra lo Stretto di Hormuz concentrava circa un quinto dei flussi mondiali di petrolio e gas naturale liquefatto. L'eventuale coinvolgimento duraturo del Mar Rosso e delle infrastrutture saudite restringerebbe contemporaneamente più corridoi, con effetti potenziali sui prezzi dell'energia, sui trasporti e sull'inflazione internazionale.",
        "Restano inoltre non verificati diversi elementi diffusi dai contendenti, compresa la rivendicazione Houthi di avere abbattuto un caccia saudita. Le immagini pubblicate dal gruppo non consentono da sole di attribuire con certezza luogo, data e dinamica. Per questo CurioMondo non tratta come accertati né il bilancio dei raid né tutte le rivendicazioni militari.",
        "I prossimi sviluppi verificabili saranno i comunicati sauditi, i riscontri indipendenti sui danni e le indicazioni sui contatti tra Washington e Teheran. È accertabile un fronte più intenso tra Houthi e forze sostenute da Riad; la fine imminente della guerra resta una dichiarazione di Trump.",
    ],
    "fonti": [
        {"url": "https://www.reuters.com/world/middle-east/trump-hopes-iran-war-nearing-end-houthi-saudi-fighting-escalates-2026-09-17/", "descrizione": "Reuters — dichiarazioni pubbliche di Trump, riscontri sui combattimenti, rivendicazioni Houthi e dati sul mercato petrolifero."},
        {"url": "https://apnews.com/article/5bb1f82555c147514fc2e8d2d61baf0c", "descrizione": "Associated Press — conferma indipendente dell'escalation, dell'avanzata Houthi e dell'impatto umanitario nello Yemen."},
        {"url": "https://travel.state.gov/en/international-travel/travel-advisories/saudi-arabia.html", "descrizione": "Dipartimento di Stato USA — avviso ufficiale sui rischi in Arabia Saudita e sulle restrizioni vicino al confine con lo Yemen."},
    ],
    "correlati": [
        {"url": "/notizie/guerra-usa-iran-cbo-costi-38-miliardi-inflazione-15-09-2026.html", "titolo": "Guerra USA-Iran, il CBO stima costi per 38 miliardi di dollari"},
        {"url": "/notizie/yemen-houthi-dhubab-bab-el-mandeb-11-settembre-2026.html", "titolo": "Yemen, gli Houthi conquistano Dhubab e minacciano Bab el-Mandeb"},
        {"url": "/notizie/guerra-usa-iran-rapporto-ufficiale-scorte-sotto-pressione-e-basi-danneggiate-15-09-2026.html", "titolo": "Guerra USA-Iran, rapporto ufficiale: scorte sotto pressione e basi danneggiate"},
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
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=84, method=6)
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(),
        "alt": "Terminale energetico e navi mercantili sul Mar Rosso all'alba, illustrazione editoriale fotorealistica generata con IA e non riferita a un luogo reale specifico.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "portraitFormat": "contextual-editorial-scene",
        "reenactedEvent": False,
        "prompt": "Contextual editorial Red Sea energy terminal and commercial shipping at sunrise; no attack, weapons, people, flags, text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('data-sensitive-context="true">', 'data-sensitive-context="true" data-portrait-format="contextual-editorial-scene">', 1)
    page_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Mondo",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-17T06:23:00+02:00",
        "status": "IN SVILUPPO",
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
        "change": "Pubblicato l'allargamento del conflitto al fronte saudita-yemenita",
        "image_policy_applied": "new-openai-contextual-sensitive-non-documentary",
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
            "last_update": "mondo-iran-yemen-saudi-v401",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "mondo-20260917T071114-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Mondo",
        "production_branch": "main",
        "base_commit": "baaf13740514c96af4f881212c93cddbf91f1724",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 11,
            "distinct_domains": 8,
            "target_reached": False,
            "note": "Conteggio prudenziale: titoli e snippet non sono stati contati. Sono state lette integralmente le fonti decisive; le rivendicazioni militari non indipendentemente verificabili sono attribuite e non trattate come fatti accertati.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.6,
            "status": "IN SVILUPPO",
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
