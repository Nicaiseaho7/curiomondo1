#!/usr/bin/env python3
"""Pubblica la legge sarda per l'inclusione dei minori con diabete tipo 1."""
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

VERSION = 402
PUBLISHED = "2026-09-17T07:36:05+02:00"
SLUG = "sardegna-legge-minori-diabete-tipo-1-scuola-sport-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Sardegna, una rete per i minori con diabete tra scuola e sport",
    "sommario": "Il Consiglio regionale ha approvato all'unanimità un sistema coordinato con formazione, registro informativo e centro pediatrico di riferimento. Per il 2026 sono previsti 1.210.850 euro.",
    "categoria": "Italia",
    "luogo": "Cagliari",
    "formato": "standard",
    "parole_chiave_titolo": ["rete per i minori", "scuola e sport"],
    "dati_chiave": [
        {"icona": "◆", "valore": "49", "etichetta": "voti favorevoli in Consiglio regionale"},
        {"icona": "●", "valore": "1,21 mln €", "etichetta": "oneri previsti per il 2026"},
        {"icona": "↗", "valore": "12 mesi", "etichetta": "termine per rete e centro pediatrico"},
    ],
    "paragrafi": [
        "Il Consiglio regionale della Sardegna ha approvato all'unanimità, con 49 voti favorevoli, il testo per l'inclusione scolastica, sportiva e sociale dei minori con diabete di tipo 1. Il provvedimento unifica due proposte presentate nel 2025 e costruisce un raccordo stabile tra sanità, scuole, associazioni sportive e famiglie.",
        "La legge prevede formazione continua per docenti, personale scolastico e operatori sportivi. Introduce inoltre una presa in carico coordinata, organismi multiprofessionali territoriali, un registro regionale collegato al Fascicolo sanitario elettronico e un centro diabetologico pediatrico di riferimento.",
        "L'obiettivo operativo è ridurre le situazioni in cui la gestione quotidiana ricade direttamente sui genitori. La rete dovrà sostenere la partecipazione alle lezioni, alle gite e all'attività fisica, comprese la continuità terapeutica e la risposta alle emergenze nei contesti educativi e sportivi.",
        "Gli oneri indicati nel testo ammontano a 1.210.850 euro per il 2026. La ripartizione comprende 30.500 euro per la formazione, 549.000 euro per piattaforma e registro e altri 549.000 euro per realizzare o adeguare il centro specialistico; 82.350 euro annui finanzieranno la manutenzione del sistema informativo.",
        "Due numeri presenti negli atti non descrivono la stessa platea. Durante il dibattito è stato richiamato il dato di circa 1.400 minori già in carico al servizio sanitario regionale. La relazione finanziaria usa invece 15–16 mila utenti come stima tecnica per dimensionare l'infrastruttura informatica: non va letta come conteggio dei minori sardi diagnosticati.",
        "Il testo fissa entro dodici mesi dall'entrata in vigore l'istituzione della rete diabetologica pediatrica e del centro regionale. La legge entrerà in vigore il giorno successivo alla pubblicazione nel Bollettino ufficiale della Regione; da quel momento decorreranno i termini attuativi.",
        "La Giunta dovrà riferire ogni anno al Consiglio sulle azioni svolte, sui risultati, sulle criticità organizzative e sulle eventuali correzioni. Questo controllo sarà decisivo per verificare se formazione, registro e presa in carico producono servizi uniformi nei diversi territori dell'isola.",
    ],
    "fonti": [
        {"url": "https://www.consregsardegna.it/nota-stampa-della-seduta-n-148/", "descrizione": "Consiglio regionale della Sardegna — nota ufficiale della seduta n. 148: voto, finalità, strumenti e dati richiamati in Aula."},
        {"url": "https://www.consregsardegna.it/wp-content/uploads/2026/09/TU126-138A.pdf", "descrizione": "Consiglio regionale della Sardegna — testo unificato 126-138/A: norme, copertura finanziaria, tempi di attuazione e clausola valutativa."},
        {"url": "https://www.ansa.it/canale_saluteebenessere/notizie/diabete/2026/09/15/in-sardegna-la-prima-legge-in-italia-sulla-tutela-dei-minori-col-diabete_5cb5f9af-10ae-4a58-87a1-92916a8a886f.html", "descrizione": "ANSA — conferma indipendente dell'approvazione e sintesi delle principali misure e risorse."},
    ],
    "correlati": [
        {"url": "/notizie/west-nile-italia-594-casi-41-decessi-10-settembre-2026.html", "titolo": "West Nile in Italia: 594 casi e 41 decessi nel nuovo bollettino"},
        {"url": "/notizie/vaccini-oncologici-personalizzati-mrna-come-funzionano.html", "titolo": "Vaccini oncologici personalizzati a mRNA: come funzionano"},
        {"url": "/notizie/vaccino-mrna-influenza-mflusiva-fda-adulti-50-anni.html", "titolo": "Vaccino mRNA contro l'influenza: cosa cambia per gli adulti"},
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
        "alt": "Scena editoriale fotorealistica generata con IA con zaino scolastico, borsa sportiva e kit per il monitoraggio del diabete in una scuola sarda; nessun minore identificabile.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "portraitFormat": "contextual-editorial-still-life",
        "reenactedEvent": False,
        "prompt": "Health-sensitive editorial still life in a Sardinian school gym with backpack, sports bag and glucose monitoring kit; no identifiable child, treatment, distress, text, logo or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('data-sensitive-context="true">', 'data-sensitive-context="true" data-portrait-format="contextual-editorial-still-life">', 1)
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
        "development_at": "2026-09-15T14:50:00+02:00",
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
        "change": "Pubblicata la legge sarda per l'inclusione dei minori con diabete di tipo 1",
        "image_policy_applied": "new-openai-sensitive-contextual-still-life-no-identifiable-minors",
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
            "last_update": "italia-sardegna-diabete-minori-v402",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "italia-20260917T073605-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Salute / Scuola",
        "production_branch": "main",
        "base_commit": "9cc66f1a657045f2a6b5cede10e5b80e7a86ac65",
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
