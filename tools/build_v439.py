#!/usr/bin/env python3
"""Prova visiva 3D fuori quadro su quattro articoli ordinari."""
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

VERSION = 439

SOURCES = {
    "juric": Path("/workspace/artifacts/imagine_images/de2379bf-e3a2-492f-b5cc-47bcef5c0f8e.jpg"),
    "cirielli": Path("/workspace/artifacts/imagine_images/fcad647a-4ef1-4c5a-bdda-b7282d965711.jpg"),
    "mancini": Path("/workspace/artifacts/imagine_images/e73ac4b1-190f-48e0-88b5-f7d6f57cf598.jpg"),
    "trump": Path("/workspace/artifacts/imagine_images/24432cc0-5fd6-4163-b607-cf90712b6e00.jpg"),
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


def patch_article(slug: str, old_key: str, new_key: str, old_alt: str, new_alt: str, public_figure: bool) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    if old_key not in page:
        raise SystemExit(f"chiave immagine assente: {slug} {old_key}")
    page = page.replace(old_key, new_key)
    if old_alt:
        page = page.replace(old_alt, new_alt)
    if public_figure and 'data-synthetic-likeness="public-figure"' not in page.split("<figure", 1)[1][:400]:
        page = page.replace(
            '<figure class="article-image" data-ai-generated="true">',
            '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false">',
            1,
        )
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
    dest.mkdir(exist_ok=True)
    files = {
        "juric": dest / "juric-3d-v439.jpg",
        "cirielli": dest / "cirielli-3d-v439.jpg",
        "mancini": dest / "mancini-3d-v439.jpg",
        "trump": dest / "trump-3d-v439.jpg",
    }
    for key, src in SOURCES.items():
        shutil.copy2(src, files[key])

    jobs = [
        {
            "who": "juric",
            "slug": "monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026",
            "old_key": "monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026-v437",
            "old_alt": "Scena editoriale contestuale generata con IA: Ivan Juric riconoscibile, occhiali e capelli grigi, in panchina con tuta rosso-bianca; somiglianza sintetica, non è una fotografia documentaria della partita.",
            "alt": "Scena editoriale 3D fuori quadro generata con IA: Ivan Juric riconoscibile, occhiali e capelli grigi, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Out-of-bounds photoreal Ivan Juric glasses grey hair, head and hand in front of a black photo frame, Monza sideline inside the frame, no text.",
        },
        {
            "who": "cirielli",
            "slug": "cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026",
            "old_key": "cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026-v437",
            "old_alt": "Scena editoriale contestuale generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, a un tavolo della Farnesina; somiglianza sintetica, non è una fotografia documentaria della riunione.",
            "alt": "Scena editoriale 3D fuori quadro generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Out-of-bounds photoreal Edmondo Cirielli glasses, head and hand in front of a black photo frame, Farnesina table inside, no text.",
        },
        {
            "who": "mancini",
            "slug": "convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026",
            "old_key": "convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026-v436",
            "old_alt": "Scena editoriale contestuale generata con IA: Roberto Mancini riconoscibile in tuta azzurra su un campo di allenamento; somiglianza sintetica, non è una fotografia documentaria del raduno.",
            "alt": "Scena editoriale 3D fuori quadro generata con IA: Roberto Mancini riconoscibile in tuta azzurra, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Out-of-bounds photoreal Roberto Mancini azzurro kit, head and hand in front of a black photo frame, training field inside, no text.",
        },
        {
            "who": "trump",
            "slug": "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026",
            "old_key": "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026-ai-openai-v393",
            "old_alt": "Illustrazione editoriale IA del Campidoglio statunitense con un dossier, una petroliera e container in primo piano; non documentaria.",
            "alt": "Scena editoriale 3D fuori quadro generata con IA: Donald Trump riconoscibile, testa e mano che escono da una cornice; somiglianza sintetica, non è una fotografia documentaria.",
            "prompt": "Out-of-bounds photoreal Donald Trump, head and pointing hand in front of a black photo frame, White House interior inside, no text.",
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
        patch_article(job["slug"], job["old_key"], new_key, job["old_alt"], job["alt"], True)
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
        "change": "Prova immagini 3D fuori quadro su Juric, Cirielli, Mancini e Trump",
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
                "last_update": "3d-out-of-bounds-v439",
            }
        )
        write_json(path, state)


if __name__ == "__main__":
    main()
