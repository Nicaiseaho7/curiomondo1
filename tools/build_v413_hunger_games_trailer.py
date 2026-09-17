#!/usr/bin/env python3
"""Pubblica il nuovo trailer italiano di Hunger Games: L'alba sulla mietitura."""
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

VERSION = 413
PUBLISHED = "2026-09-17T19:46:28+02:00"
SLUG = "hunger-games-alba-mietitura-trailer-italiano-19-novembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Hunger Games, nuovo trailer italiano: al cinema il 19 novembre",
    "sommario": "Il secondo trailer mette al centro il giovane Haymitch Abernathy, interpretato da Joseph Zada. Notorious Pictures conferma l'uscita italiana nelle sale il 19 novembre 2026.",
    "categoria": "Film e serie TV",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Hunger Games", "trailer italiano", "19 novembre"],
    "dati_chiave": [
        {"icona": "◆", "valore": "19 novembre", "etichetta": "uscita nelle sale italiane"},
        {"icona": "●", "valore": "24 anni prima", "etichetta": "rispetto alla storia di Katniss"},
        {"icona": "↗", "valore": "50ª edizione", "etichetta": "gli Hunger Games raccontati"},
    ],
    "paragrafi": [
        "Il nuovo trailer italiano di Hunger Games: L'alba sulla mietitura è online. Il film diretto da Francis Lawrence arriverà nelle sale italiane il 19 novembre 2026, un giorno prima della data nordamericana indicata da Lionsgate. La distribuzione nazionale è affidata a Notorious Pictures.",
        "Il secondo trailer sposta l'attenzione sul giovane Haymitch Abernathy, interpretato da Joseph Zada. Il personaggio è noto al pubblico dei film precedenti nella versione adulta interpretata da Woody Harrelson, ma questo capitolo ne racconta la giovinezza senza proseguire la storia di Katniss Everdeen.",
        "La vicenda è ambientata 24 anni prima del primo Hunger Games, durante la cinquantesima edizione dei Giochi, chiamata Seconda Edizione della Memoria. La regola speciale prevede il doppio dei tributi rispetto alla competizione ordinaria, come conferma la sinossi pubblicata dal distributore italiano.",
        "Nel trailer compaiono anche Ralph Fiennes nel ruolo del presidente Snow, Jesse Plemons come Plutarch Heavensbee, Mckenna Grace nei panni di Maysilee Donner, Elle Fanning come Effie Trinket e Kieran Culkin come Caesar Flickerman. Il cast ufficiale comprende inoltre Glenn Close, Maya Hawke, Whitney Peak e Kelvin Harrison Jr.",
        "Francis Lawrence torna alla regia dopo aver firmato quattro capitoli cinematografici della saga, da La ragazza di fuoco a La ballata dell'usignolo e del serpente. Il nuovo film adatta il romanzo di Suzanne Collins pubblicato nel 2025 e si concentra sulla partecipazione di Haymitch ai Giochi.",
        "Per il pubblico italiano il dato pratico è già definito: uscita al cinema il 19 novembre. Le fonti ufficiali consultate non indicano ancora una data italiana per noleggio, acquisto digitale o streaming; la finestra annunciata riguarda esclusivamente le sale e non va estesa ad altre modalità di visione.",
        "Il film non è ancora disponibile e il trailer non equivale a una recensione. Le immagini confermano personaggi, ambientazione e tono del progetto, ma non permettono di valutare l'opera completa. CurioMondo eviterà dettagli ulteriori della trama per non anticipare gli sviluppi raccontati nel romanzo.",
    ],
    "fonti": [
        {"url": "https://notoriouspictures.it/movie/hunger-games-lalba-sulla-mietitura/", "descrizione": "Notorious Pictures — scheda ufficiale italiana con data di uscita, regia, cast, sinossi e trailer."},
        {"url": "https://www.youtube.com/watch?v=lYXtL5TreOE", "descrizione": "Lionsgate Movies — secondo trailer ufficiale internazionale pubblicato il 16 settembre 2026."},
        {"url": "https://tg24.sky.it/spettacolo/cinema/video/2026/09/17/hunger-games-l-alba-sulla-mietitura-trailer-1125229", "descrizione": "Sky TG24 — riscontro italiano del nuovo trailer e dell'uscita nazionale del 19 novembre, pubblicato il 17 settembre 2026."},
        {"url": "https://gizmodo.com/the-new-sunrise-on-the-reaping-trailer-asks-whats-haymitchs-story-2000812588", "descrizione": "Gizmodo — conferma indipendente del secondo trailer, del cast e della data nordamericana del 20 novembre."},
    ],
    "correlati": [
        {"url": "/notizie/cinema-uscite-italia-14-20-settembre-2026.html", "titolo": "Cinema, sette uscite tra 16 e 17 settembre: film e streaming in Italia"},
        {"url": "/notizie/spider-man-brand-new-day-record-box-office-nord-america-17-settembre-2026.html", "titolo": "Spider-Man supera Star Wars: record da 936,8 milioni in Nord America"},
        {"url": "/notizie/stranger-things-tales-from-85-2-arriva-il-17-settembre-su-netflix-16-09-2026.html", "titolo": "Stranger Things: Tales From ’85 2 arriva il 17 settembre su Netflix"},
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
        "alt": "Illustrazione editoriale fotorealistica generata con IA di Joseph Zada, con giacca verde scuro davanti a strutture circolari color bronzo e un bosco sfocato.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "syntheticLikeness": "public-figure",
        "portraitFormat": "editorial-contextual-portrait",
        "reenactedEvent": False,
        "prompt": "Ultrarealistic editorial illustration of adult actor Joseph Zada alone in a restrained cinema-studio setting, dark olive field jacket, abstract bronze circular structures and softly blurred woodland backdrop; no text, logos, posters, statistics, weapons, violence or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('<div class="badge">Mondo / Film e serie TV</div>', '<div class="badge">Film e serie TV</div>', 1)
    page = page.replace(
        'data-sensitive-context="false">',
        'data-sensitive-context="false" data-portrait-format="editorial-contextual-portrait">',
        1,
    )
    page_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    ARTICLE["category_full"] = "Film e serie TV"
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Film e serie TV",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-17T10:17:00+02:00",
        "development_time_note": "Il distributore non espone l'orario del caricamento italiano; alle 10:17 il nuovo trailer era già disponibile e documentato da Sky TG24.",
        "status": "UFFICIALE",
        "status_note": "Trailer, uscita italiana, regia e cast sono verificati sulla scheda del distributore italiano; Sky TG24 e Gizmodo forniscono riscontri editoriali indipendenti.",
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
        "change": "Pubblicato il nuovo trailer italiano di Hunger Games: L'alba sulla mietitura",
        "image_policy_applied": "new-openai-public-figure-contextual-portrait-no-text-no-logo",
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
            "last_update": "cinema-hunger-games-trailer-v413",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "cinema-20260917T194628-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Cinema e serie / trailer e uscite italiane",
        "production_branch": "main",
        "base_commit": "6ea1b8b1a10e887fbbe122f3ee5086d3917d8557",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 9,
            "distinct_domains": 8,
            "target_reached": False,
            "note": "Conteggio prudenziale: esclusi snippet, duplicati, pagine bloccate e risultati non aperti. Sono state lette pagine ufficiali e redazionali su uscite, cataloghi e trailer; le candidature vecchie, già coperte o prive di disponibilità italiana verificata sono state scartate.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.6,
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
