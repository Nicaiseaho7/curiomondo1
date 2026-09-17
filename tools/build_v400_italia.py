#!/usr/bin/env python3
"""Pubblica la notizia sull'aggressione al rabbino a Milano."""
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

VERSION = 400
PUBLISHED = "2026-09-17T06:51:07+02:00"
SLUG = "rabbino-aggredito-milano-bande-nere-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "rabbino-aggredito-milano-bande-nere-17-settembre-2026.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Milano, rabbino aggredito alla fermata del bus: tre persone individuate",
    "sommario": "Un rabbino di circa 60 anni è stato insultato, spinto e picchiato nel quartiere Bande Nere. La Polizia ha individuato tre persone; la loro posizione resta al vaglio e il movente non è stato formalmente accertato.",
    "categoria": "Cronaca",
    "luogo": "Milano",
    "formato": "standard",
    "parole_chiave_titolo": ["rabbino aggredito", "tre persone individuate"],
    "dati_chiave": [
        {"icona": "◆", "valore": "3", "etichetta": "persone individuate dalla Polizia"},
        {"icona": "●", "valore": "17:30", "etichetta": "orario indicativo dell'aggressione"},
        {"icona": "↗", "valore": "1", "etichetta": "denuncia presentata dalla vittima"},
    ],
    "paragrafi": [
        "Un rabbino di circa 60 anni è stato insultato, spinto e picchiato mercoledì 16 settembre, intorno alle 17:30, mentre aspettava un autobus in piazzale Bande Nere a Milano. Tre persone sono state rintracciate poco dopo dalla Polizia. Le ragioni dell'aggressione e le eventuali responsabilità individuali devono ancora essere accertate.",
        "La vittima ha raccontato di essere stata accerchiata, colpita con calci e pugni e raggiunta da sputi. Secondo le ricostruzioni concordanti di ANSA, RaiNews e Corriere della Sera, è riuscita a fotografare e filmare il gruppo mentre si allontanava verso la metropolitana, quindi ha chiamato gli agenti e presentato denuncia.",
        "Le fonti usano formule diverse sulle condizioni dell'uomo e sull'assistenza sanitaria ricevuta. ANSA riferisce che si è recato in ospedale, mentre il Corriere scrive che non sarebbe stato trasportato. Non è stato diffuso un referto medico pubblico: entità e prognosi delle lesioni non possono quindi essere definite con precisione.",
        "L'individuazione dei tre sospettati non equivale a un arresto, a un'imputazione o a una condanna. Il Corriere riferisce che sono stati accompagnati negli uffici di polizia per l'identificazione e che la loro posizione è al vaglio degli investigatori. Alle 06:51 del 17 settembre non risultava pubblicato un provvedimento giudiziario ufficiale.",
        "Walker Meghnagi, presidente della Comunità ebraica di Milano, ha sostenuto che il rabbino sia stato riconosciuto come ebreo dall'abbigliamento. Questa dichiarazione documenta la ricostruzione della comunità, ma la matrice antisemita dovrà essere verificata dagli inquirenti. Anche l'origine attribuita agli aggressori non risulta confermata da una fonte ufficiale.",
        "La presidente del Consiglio Giorgia Meloni ha definito l'episodio «vile e inaccettabile» e lo ha condannato come espressione di odio antisemita. Il presidente del Senato Ignazio La Russa ha chiesto l'accertamento dei fatti e delle responsabilità. Le prese di posizione istituzionali non sostituiscono la qualificazione penale dell'accaduto.",
        "Il caso assume rilievo pubblico perché l'aggressione è avvenuta in pieno giorno, vicino al quartiere ebraico, e avrebbe preso di mira un segno visibile dell'identità religiosa. La rapidità dell'identificazione mostra inoltre il peso delle immagini raccolte dalla vittima, che restano però materiale investigativo e non una prova pubblicamente valutabile.",
        "I prossimi passaggi verificabili sono le decisioni della Polizia e della Procura sulla posizione dei tre uomini e l'eventuale contestazione di un movente discriminatorio. Fino ad allora, lo stato corretto della notizia è quello di un'aggressione denunciata, confermata da più testate e con tre persone identificate, ma senza responsabilità definitive.",
    ],
    "fonti": [
        {"url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/16/a-milano-rabbino-aggredito-preso-a-calci-e-pugni-a-fermata-del-bus_75d9797f-e106-492f-97fc-6d4e2f8d8e5b.html", "descrizione": "ANSA — denuncia dell'aggressione, individuazione dei tre sospettati e dichiarazioni della Comunità e delle istituzioni."},
        {"url": "https://www.rainews.it/tgr/lombardia/articoli/2026/09/a-milano-rabbino-aggredito-preso-a-calci-e-pugni-alla-fermata-del-bus-61e3d111-d134-4f03-8fad-f7c642a0fa2b.html", "descrizione": "RaiNews TGR Lombardia — conferma indipendente di luogo, dinamica riferita e intervento della Polizia."},
        {"url": "https://milano.corriere.it/notizie/cronaca/26_settembre_16/milano-rabbino-aggredito-da-tre-sconosciuti-alla-fermata-dell-autobus-preso-a-calci-e-pugni-lui-li-filma-e-li-denuncia-8a0f5bc5-1944-4dd2-8052-114cfa5f8xlk_amp.shtml", "descrizione": "Corriere della Sera Milano — riscontro su orario, denuncia, identificazione e posizione ancora al vaglio degli investigatori."},
    ],
    "correlati": [
        {"url": "/notizie/carol-maltesi-ergastolo-davide-fontana-appello-ter-16-settembre-2026.html", "titolo": "Carol Maltesi, ergastolo a Davide Fontana nell'appello ter"},
        {"url": "/notizie/milano-greco-pirelli-deragliamento-carro-merci-treni-17-settembre-2026.html", "titolo": "Milano Greco Pirelli, treni interrotti dopo il deragliamento di un carro merci"},
        {"url": "/notizie/csm-test-psicoattitudinali-magistrati-criteri-16-settembre-2026.html", "titolo": "Test psicoattitudinali per i magistrati: il CSM approva i criteri"},
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
        "alt": "Ritratto editoriale neutrale e non identificativo generato con IA di un rabbino adulto; non raffigura la vittima reale né l'aggressione.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "portraitFormat": "neutral-isolated",
        "reenactedEvent": False,
        "prompt": "Sensitive-context neutral isolated non-identifying editorial portrait of an anonymous rabbi; no violence, injuries, text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('data-sensitive-context="true">', 'data-sensitive-context="true" data-portrait-format="neutral-isolated">', 1)
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
        "development_at": "2026-09-16T17:30:00+02:00",
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
        "change": "Pubblicata la notizia sull'aggressione a un rabbino nel quartiere Bande Nere a Milano",
        "image_policy_applied": "new-openai-sensitive-neutral-non-identifying-portrait",
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
            "last_update": "italia-rabbino-milano-v400",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "italia-20260917T065107-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia",
        "production_branch": "main",
        "base_commit": "667d795f87aff4bcaf02532e3d7ceb3751066694",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 7,
            "distinct_domains": 6,
            "target_reached": False,
            "note": "Conteggio prudenziale: titoli e snippet non sono stati conteggiati. La candidata pubblicata è stata letta integralmente su tre fonti e verificata distinguendo fatti, dichiarazioni e punti non ancora accertati.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.3,
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
