#!/usr/bin/env python3
"""Corregge il visual del flash di Milano ripristinando i contrassegni reali pertinenti."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VERSION = 455
DATE = "2026-09-20"
STAMP = "2026-09-20T11:34:03+02:00"
SLUG = "milano-lite-strada-25enne-accoltellato-gola-20-settembre-2026"
ARTICLE_URL = f"/notizie/{SLUG}.html"
OLD_KEY = f"{SLUG}-v454"
NEW_KEY = f"{SLUG}-v455"
OLD_ALT = (
    "Scena editoriale neutrale generata con IA: pattuglia dei carabinieri e ambulanza "
    "in una strada di Milano di notte, senza persone ferite né ricostruzione "
    "dell’aggressione; non è una fotografia documentaria."
)
NEW_ALT = (
    "Scena editoriale neutrale generata con IA: auto dei carabinieri con scritte "
    "CARABINIERI e 112 e ambulanza con 118 e SOCCORSO SANITARIO in una strada di "
    "Milano di notte; non è una fotografia documentaria."
)
PROMPT = (
    "Ultra-realistic neutral editorial image of an emergency response on a Milan street "
    "at night. Show an Italian Carabinieri patrol car with its authentic CARABINIERI "
    "and 112 markings, and an Italian emergency ambulance with authentic 118, SOCCORSO "
    "SANITARIO, blue Star of Life and service striping. These real-world operational "
    "logos and markings naturally belong to the relevant vehicles. Keep any advertising "
    "billboard blank. No victim, injury, blood, weapon, attacker, headline, added label, "
    "watermark or AI disclosure in the pixels."
)
CAPTION = (
    "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa "
    "notizia; non è una fotografia documentaria."
)
SOURCE = Path(
    "/workspace/scratch/63d8c74bad9c/generated_images/"
    "exec-3ae4b9cb-6b83-4e5c-972a-a3e9a0adc764.png"
)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_variants() -> list[dict[str, object]]:
    image = Image.open(SOURCE).convert("RGB")
    ratio = 1.5
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))

    folder = ROOT / "assets/images/editorial-auto"
    variants: list[dict[str, object]] = []
    for width in (480, 800, 1200):
        target = folder / f"{NEW_KEY}-{width}.webp"
        resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
        resized.save(target, "WEBP", quality=86, method=6)
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{target.name}",
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "bytes": target.stat().st_size,
            }
        )
    return variants


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Immagine sorgente assente: {SOURCE}")

    variants = create_variants()
    image_record = {
        "key": NEW_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": variants,
        "alt": NEW_ALT,
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "syntheticLikeness": None,
        "prompt": PROMPT,
        "article": ARTICLE_URL,
    }

    replace_files = [
        ROOT / "index.html",
        ROOT / "notizie" / f"{SLUG}.html",
        ROOT / "assets/data/home-feed-v210.json",
        ROOT / "contenuti/notizie" / f"{SLUG}.json",
    ]
    for path in replace_files:
        text = path.read_text(encoding="utf-8")
        text = text.replace(OLD_KEY, NEW_KEY).replace(OLD_ALT, NEW_ALT)
        if path.name == f"{SLUG}.html":
            text = text.replace("?v=454", "?v=455")
        path.write_text(text, encoding="utf-8")

    content_path = ROOT / "contenuti/notizie" / f"{SLUG}.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    content["image"] = {key: value for key, value in image_record.items() if key != "article"}
    write_json(content_path, content)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    registry["items"] = [
        image_record,
        *[
            item
            for item in registry["items"]
            if not (item.get("article") == ARTICLE_URL and item.get("key") == OLD_KEY)
        ],
    ]
    write_json(registry_path, registry)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update(
        {
            "site_version": VERSION,
            "version": f"v{VERSION}",
            "release_version": f"v{VERSION}",
            "last_release": {
                "version": VERSION,
                "date": DATE,
                "type": "editorial-image-correction",
                "news_added": [],
                "news_updated": [SLUG],
                "change": (
                    "Corretto il visual di Milano ripristinando scritte e loghi operativi "
                    "pertinenti su Carabinieri e 118"
                ),
                "image_policy_applied": "real-relevant-vehicle-logos-and-markings-restored",
            },
        }
    )
    write_json(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        state_path = ROOT / name
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": DATE,
                "release_date": DATE,
                "last_update": "editorial-image-correction-v455",
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
            }
        )
        write_json(state_path, state)

    log = {
        "run_at": STAMP,
        "type": "editorial-image-correction",
        "article": ARTICLE_URL,
        "old_image_key": OLD_KEY,
        "new_image_key": NEW_KEY,
        "change": (
            "Ripristinati i contrassegni reali e pertinenti CARABINIERI, 112, 118, "
            "SOCCORSO SANITARIO e Stella della Vita; mantenuto vuoto il cartellone."
        ),
    }
    write_json(ROOT / "automation/logs/editoriale-20260920T113403-Europe-Rome.json", log)
    print(json.dumps({"updated": SLUG, "version": VERSION, "variants": variants}, ensure_ascii=False))


if __name__ == "__main__":
    main()
