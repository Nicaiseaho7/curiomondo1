#!/usr/bin/env python3
"""Sostituisce l'hero di un articolo gia' pubblicato con una nuova immagine
fornita dalla redazione, con didascalia veritiera in base al tipo dichiarato.

    python3 tools/update_article_image.py --slug <slug-senza-.html> \
        --immagine <file> --alt "..." --tipo foto|ufficiale [--personaggio-pubblico]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import sync_surfaces, _version  # noqa: E402

CAPTION_FOTO = (
    "Fotografia editoriale fornita alla redazione CurioMondo; "
    "non generata da intelligenza artificiale."
)
CAPTION_UFFICIALE = (
    "Immagine promozionale ufficiale fornita dagli aventi diritto; "
    "non generata da CurioMondo ne una fotografia di cronaca."
)


def variants(source: Path, slug: str, version: int) -> list[dict]:
    image = Image.open(source).convert("RGB")
    target = 1.5
    width, height = image.size
    if width / height > target:
        new_width = round(height * target)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    elif width / height < target:
        new_height = round(width / target)
        top = max(0, (height - new_height) // 2)
        image = image.crop((0, top, width, top + new_height))
    result = []
    for w in (480, 800, 1200):
        path = ROOT / "assets/images/editorial-auto" / f"{slug}-v{version}-{w}.webp"
        image.resize((w, round(w / target)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=90, method=6
        )
        result.append({"w": w, "src": f"/assets/images/editorial-auto/{path.name}",
                       "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                       "bytes": path.stat().st_size})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--immagine", required=True)
    parser.add_argument("--alt", required=True)
    parser.add_argument("--tipo", required=True, choices=["foto", "ufficiale"])
    parser.add_argument("--personaggio-pubblico", action="store_true")
    args = parser.parse_args()

    slug = args.slug
    version = _version()
    new_variants = variants(Path(args.immagine), slug, version)

    article_path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    og = doc.xpath('//meta[@property="og:image"]')[0]
    og.set("content", f"https://curiomondo.it{new_variants[-1]['src']}")
    og_alt = doc.xpath('//meta[@property="og:image:alt"]')[0]
    og_alt.set("content", args.alt)
    schema = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema_data = json.loads(schema.text)
    schema_data["image"] = [f"https://curiomondo.it{new_variants[-1]['src']}"]
    schema.text = json.dumps(schema_data, ensure_ascii=False, separators=(",", ":"))

    fig = doc.xpath('//figure[contains(@class,"article-image")]')[0]
    for attr in ("data-official-artwork", "data-documentary-photo",
                 "data-synthetic-likeness", "data-sensitive-context"):
        if fig.get(attr) is not None:
            del fig.attrib[attr]
    fig.set("data-ai-generated", "false")
    disclosure = CAPTION_UFFICIALE if args.tipo == "ufficiale" else CAPTION_FOTO
    if args.tipo == "ufficiale":
        fig.set("data-official-artwork", "true")
    else:
        fig.set("data-documentary-photo", "true")
        if args.personaggio_pubblico:
            fig.set("data-synthetic-likeness", "public-figure")
            fig.set("data-sensitive-context", "false")

    img = fig.xpath(".//img")[0]
    img.set("src", f"..{new_variants[1]['src']}")
    img.set("srcset", ", ".join(f"..{v['src']} {v['w']}w" for v in new_variants))
    img.set("alt", args.alt)
    figcaption = fig.xpath(".//figcaption")[0]
    figcaption.text = disclosure

    article_path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = version
    for item in registry["items"]:
        if item.get("article") == f"/notizie/{slug}.html":
            item.pop("prompt", None)
            item["alt"] = args.alt
            item["variants"] = new_variants
            item["disclosure"] = disclosure
            item["generator"] = ("materiale ufficiale fornito dagli aventi diritto"
                                 if args.tipo == "ufficiale" else "fornita dalla redazione")
            item["aiGenerated"] = False
            item["documentaryPhoto"] = args.tipo == "foto"
            item["officialArtwork"] = args.tipo == "ufficiale"
            if args.personaggio_pubblico:
                item["syntheticLikeness"] = "public-figure"
            else:
                item.pop("syntheticLikeness", None)
            break
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sync_surfaces([], f"/notizie/{slug}.html", version)

    for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(site_version=version, version=str(version), currentVersion=version,
                     last_update=f"immagine-aggiornata-{slug[:40]}-v{version}")
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    manifest["site_version"] = version
    manifest["version"] = f"v{version}"
    manifest["release_version"] = f"v{version}"
    manifest["last_release"] = {
        "version": version, "date": "2026-09-25", "type": "image-update",
        "news_added": [], "news_updated": [slug],
        "change": f"Immagine sostituita ({args.tipo})",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"slug": slug, "version": version}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
