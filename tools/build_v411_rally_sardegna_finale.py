#!/usr/bin/env python3
"""Pubblica il Rally Italia Sardegna come finale del WRC 2026."""
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

VERSION = 411
PUBLISHED = "2026-09-17T16:51:08+02:00"
DEVELOPMENT = "2026-09-17T16:26:47+02:00"
SLUG = "rally-italia-sardegna-finale-mondiale-wrc-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "rally-italia-sardegna-finale-wrc-2026.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Rally Italia Sardegna diventa la finale del Mondiale WRC 2026",
    "sommario": "La FIA ha escluso la tappa saudita dal Mondiale a causa della situazione in Medio Oriente. Il titolo piloti sarà quindi assegnato sulle strade sterrate della Sardegna, dall'1 al 4 ottobre.",
    "categoria": "Sport",
    "luogo": "Sardegna / Alghero",
    "formato": "standard",
    "parole_chiave_titolo": ["finale del Mondiale", "Rally Italia Sardegna", "WRC 2026"],
    "dati_chiave": [
        {"icona": "◆", "valore": "1–4/10", "etichetta": "date della finale in Sardegna"},
        {"icona": "↗", "valore": "17", "etichetta": "punti tra Evans e Pajari"},
        {"icona": "●", "valore": "35", "etichetta": "punti disponibili nell'ultimo round"},
    ],
    "paragrafi": [
        "Il Rally Italia Sardegna sarà la finale del Mondiale WRC 2026. La FIA ha tolto dal campionato la tappa dell'Arabia Saudita, prevista dall'11 al 14 novembre, a causa degli sviluppi in Medio Oriente: la stagione terminerà quindi ad Alghero domenica 4 ottobre, al termine della gara italiana in programma dall'1 al 4 ottobre.",
        "Il Rally Saudi Arabia non viene cancellato integralmente. Secondo la decisione comunicata dalla FIA, l'evento di Gedda resterà in calendario a novembre come prova del FIA Middle East Rally Championship, ma non assegnerà punti per il Mondiale. La federazione e WRC Promoter dichiarano di voler riportare la gara saudita nel WRC nel 2027.",
        "La modifica trasforma una prova inizialmente indicata come tredicesima e penultima tappa nel confronto decisivo per il titolo piloti. Elfyn Evans arriva in Sardegna al comando con 230 punti, davanti al compagno Toyota Sami Pajari a 213 e a Oliver Solberg a 209. Restano 35 punti disponibili nella finale.",
        "Evans parte quindi con 17 punti di vantaggio su Pajari e 21 su Solberg. DirtFish calcola che 19 punti in Sardegna gli garantirebbero matematicamente il titolo indipendentemente dai risultati dei rivali. Pajari e Solberg restano però in corsa e la distribuzione dei punti dipenderà sia dalla classifica generale sia dai risultati della domenica.",
        "La gara avrà base ad Alghero e si svilupperà su 17 prove speciali per 309,36 chilometri cronometrati, tutti su sterrato. Il percorso attraversa soprattutto Monte Acuto, Anglona e Nurra; il programma prevede lo shakedown e l'avvio giovedì 1 ottobre, con il podio conclusivo domenica 4 alle 17.",
        "La tappa finale comprenderà due passaggi sulle prove di Osilo-Tergu e Sassari-Argentiera. Quest'ultima ospiterà la Power Stage, tratto che assegna punti supplementari e che può quindi avere un peso diretto nell'esito del campionato. Le strade sarde sono note per il fondo abrasivo e per l'elevata usura degli pneumatici.",
        "La decisione accorcia il campionato da quattordici a tredici appuntamenti e anticipa di oltre un mese la conclusione rispetto al calendario originario. Non è stato inserito un evento sostitutivo dopo la Sardegna. Per l'Italia sarà la terza finale WRC in sette stagioni, dopo le chiusure di Monza nel 2020 e nel 2021.",
        "È ufficiale la rimozione della componente WRC della gara saudita e la conseguente chiusura del Mondiale in Sardegna. Restano soggetti agli aggiornamenti organizzativi gli orari operativi, gli accessi per il pubblico e le eventuali modifiche alle prove: gli spettatori devono fare riferimento ai canali ufficiali del Rally Italia Sardegna.",
    ],
    "fonti": [
        {"url": "https://www.reuters.com/sports/italy-replaces-saudi-arabia-final-round-2026-world-rally-championship-2026-09-17/", "descrizione": "Reuters — decisione FIA, uscita della tappa saudita dal WRC e nuova finale in Sardegna."},
        {"url": "https://dirtfish.com/rally/wrc/wrc-drops-2026-season-finale-and-wont-replace-it/", "descrizione": "DirtFish — comunicato FIA, dichiarazioni dei responsabili e conseguenze sul calendario e sul titolo."},
        {"url": "https://www.wrc.com/en/events/wrc-rally-italia-sardegna-2026", "descrizione": "WRC — pagina ufficiale dell'evento italiano, date e caratteristiche sportive della gara."},
        {"url": "https://rallyitaliasardegna.com/2026/06/01/ecco-il-percorso-del-rally-italia-sardegna-2026/", "descrizione": "Rally Italia Sardegna — percorso ufficiale, prove speciali, chilometri e programma del podio finale."},
    ],
    "correlati": [
        {"url": "/notizie/formula-1-calendario-2027-dieci-sprint-monaco-monza.html", "titolo": "Formula 1, nel 2027 dieci Sprint: debutta Monaco e torna Monza"},
        {"url": "/notizie/kimi-antonelli-vince-gp-italia-monza-19esimo-6-settembre-2026.html", "titolo": "Antonelli, impresa a Monza: vince partendo 19°"},
        {"url": "/notizie/monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026.html", "titolo": "Monza, Vettel riporta in pista la Ferrari F2002"},
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
        "alt": "Illustrazione editoriale generata con IA di un'auto da rally su una strada sterrata della Sardegna, con costa mediterranea sullo sfondo; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultrarealistic editorial rally car on a Sardinian gravel stage with Mediterranean coast; no text, logos or watermark.",
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
        "category": "Sport",
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
        "change": "Pubblicata la finale WRC 2026 al Rally Italia Sardegna",
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
            "last_update": "sport-rally-sardegna-finale-wrc-v411",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T165108-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Sport",
        "production_branch": "main",
        "base_commit": "0932c434958980eb70de4ab0dc4df9750166367b",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 6,
            "distinct_domains": 5,
            "target_reached": False,
            "note": "Conteggio prudenziale: il target di 500 contenuti non è stato raggiunto e non è stato inventato. La candidata pubblicata è stata verificata su comunicato FIA riportato integralmente, Reuters, WRC e canali ufficiali della gara.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.4,
            "status": "UFFICIALE",
            "decision": "publish",
            "sources": [x["url"] for x in ARTICLE["fonti"]],
            "public_url": f"https://curiomondo.it/notizie/{SLUG}",
            "publication_state": "pending_deploy",
        }],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
