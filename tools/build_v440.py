#!/usr/bin/env python3
"""Sostituisce le prove 3D gimmick con ritratti editoriali a profondità professionale."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces

VERSION = 440
SOURCES = {
    "juric": Path("/workspace/artifacts/imagine_images/f507063f-eca8-4e9a-9775-b7fceb7565a2.jpg"),
    "cirielli": Path("/workspace/artifacts/imagine_images/3e7608a4-cbf4-4e0e-9bcb-3445500c6cc7.jpg"),
    "mancini": Path("/workspace/artifacts/imagine_images/963e9c25-2062-4484-9c15-960d6bff6612.jpg"),
    "trump": Path("/workspace/artifacts/imagine_images/6f8fdd1e-cac2-4ab4-b2af-0236e47e4841.jpg"),
}


def save_image_variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
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
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=86, method=6
        )
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return variants


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_article(slug: str, old_key: str, new_key: str, old_alt: str, new_alt: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    if old_key not in page:
        raise SystemExit(f"chiave immagine assente: {slug}")
    page = page.replace(old_key, new_key).replace(old_alt, new_alt)
    path.write_text(page, encoding="utf-8")
    src = ROOT / "contenuti" / "notizie" / f"{slug}.json"
    if src.exists():
        data = json.loads(src.read_text(encoding="utf-8"))
        if isinstance(data.get("image"), dict):
            data["image"]["key"] = new_key
            data["image"]["alt"] = new_alt
        write_json(src, data)


def main() -> None:
    dest = ROOT / "generated_images"
    files = {
        "juric": dest / "juric-depth-v440.jpg",
        "cirielli": dest / "cirielli-depth-v440.jpg",
        "mancini": dest / "mancini-depth-v440.jpg",
        "trump": dest / "trump-depth-v440.jpg",
    }
    for key, src in SOURCES.items():
        shutil.copy2(src, files[key])

    jobs = [
        {
            "who": "juric",
            "slug": "monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026",
            "old_key": "monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026-v439",
            "old_alt": "Scena editoriale 3D fuori quadro generata con IA: Ivan Juric riconoscibile, occhiali e capelli grigi, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "alt": "Scena editoriale contestuale generata con IA: Ivan Juric riconoscibile, occhiali e capelli grigi, in panchina; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Photoreal news photo Ivan Juric glasses grey hair, subject closer than blurred sideline, no pointing, no frame, no text.",
        },
        {
            "who": "cirielli",
            "slug": "cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026",
            "old_key": "cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026-v439",
            "old_alt": "Scena editoriale 3D fuori quadro generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "alt": "Scena editoriale contestuale generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, in un interno istituzionale; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Photoreal news photo Edmondo Cirielli glasses, subject closer than blurred Farnesina interior, no pointing, no frame, no text.",
        },
        {
            "who": "mancini",
            "slug": "convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026",
            "old_key": "convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026-v439",
            "old_alt": "Scena editoriale 3D fuori quadro generata con IA: Roberto Mancini riconoscibile in tuta azzurra, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "alt": "Scena editoriale contestuale generata con IA: Roberto Mancini riconoscibile in tuta azzurra su un campo di allenamento; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Photoreal news photo Roberto Mancini azzurro kit, subject closer than blurred training field, no pointing, no frame, no text.",
        },
        {
            "who": "trump",
            "slug": "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026",
            "old_key": "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026-v439",
            "old_alt": "Scena editoriale 3D fuori quadro generata con IA: Donald Trump riconoscibile, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "alt": "Scena editoriale contestuale generata con IA: Donald Trump riconoscibile in abito scuro, interno istituzionale sfocato; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Photoreal news photo Donald Trump, subject closer than blurred White House interior, no pointing, no frame, no text.",
        },
    ]

    for job in jobs:
        new_key = f"{job['slug']}-v{VERSION}"
        variants = save_image_variants(files[job["who"]], new_key)
        image = {
            "key": new_key,
            "aiGenerated": True,
            "documentaryPhoto": False,
            "generator": "ChatGPT/OpenAI image generation",
            "syntheticLikeness": "public-figure",
            "variants": variants,
            "alt": job["alt"],
            "disclosure": CAPTION,
            "sensitiveContext": False,
            "reenactedEvent": False,
            "prompt": job["prompt"],
        }
        patch_article(job["slug"], job["old_key"], new_key, job["old_alt"], job["alt"])
        register_image(image, job["slug"], VERSION)

    sync_surfaces([], "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-19",
        "type": "image-release",
        "news_added": [],
        "news_updated": [j["slug"] for j in jobs],
        "change": "Ritratti editoriali a profondità 3D sobria, senza mani tese né cornici",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": "2026-09-19",
                "release_date": "2026-09-19",
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 4,
                "last_update": "editorial-depth-v440",
            }
        )
        write_json(path, state)


if __name__ == "__main__":
    main()
