#!/usr/bin/env python3
"""Sostituisce l'hero AI del BJK Cup con la foto reale della squadra fornita
dalla redazione, con didascalia veritiera (fotografia, non illustrazione IA)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/tmp/claude-0/-home-user-curiomondo1/69b72a42-bff3-5a8e-91dd-03066c163099/scratchpad/collage25/bjk.png")
SLUG = "bjk-cup-italia-in-semifinale-cina-battuta-2-1-nel-doppio-24-09-2026"
VERSION = 565
ALT = (
    "Foto d'archivio di Jasmine Paolini e Sara Errani che esultano abbracciate "
    "in divisa azzurra, con il logo della Billie Jean King Cup sullo sfondo."
)
DISCLOSURE = (
    "Fotografia editoriale fornita alla redazione CurioMondo; "
    "non generata da intelligenza artificiale."
)

import sys
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import sync_surfaces


def variants() -> list[dict]:
    image = Image.open(SOURCE).convert("RGB")
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
    for width in (480, 800, 1200):
        path = ROOT / "assets/images/editorial-auto" / f"{SLUG}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / target)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=90, method=6
        )
        result.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return result


new_variants = variants()
article_path = ROOT / "notizie" / f"{SLUG}.html"
raw = article_path.read_text(encoding="utf-8")
doc = html.fromstring(raw)
og = doc.xpath('//meta[@property="og:image"]')[0]
og.set("content", f"https://curiomondo.it{new_variants[-1]['src']}")
og_alt = doc.xpath('//meta[@property="og:image:alt"]')[0]
og_alt.set("content", ALT)
schema = doc.xpath('//script[@type="application/ld+json"]')[0]
schema_data = json.loads(schema.text)
schema_data["image"] = [f"https://curiomondo.it{new_variants[-1]['src']}"]
schema.text = json.dumps(schema_data, ensure_ascii=False, separators=(",", ":"))
fig = doc.xpath('//figure[contains(@class,"article-image")]')[0]
fig.set("data-ai-generated", "false")
if fig.get("data-official-artwork") is not None:
    del fig.attrib["data-official-artwork"]
if fig.get("data-documentary-photo") is None:
    fig.set("data-documentary-photo", "true")
img = fig.xpath('.//img')[0]
img.set("src", f"..{new_variants[1]['src']}")
img.set("srcset", ", ".join(f"..{item['src']} {item['w']}w" for item in new_variants))
img.set("alt", ALT)
figcaption = fig.xpath('.//figcaption')[0]
figcaption.text = DISCLOSURE
serialized = html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n"
article_path.write_text(serialized, encoding="utf-8")

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
registry["version"] = VERSION
for item in registry["items"]:
    if item.get("article") == f"/notizie/{SLUG}.html":
        item.pop("prompt", None)
        item.update(key=f"{SLUG}-v{VERSION}", alt=ALT, variants=new_variants,
                    disclosure=DISCLOSURE, generator="fornita dalla redazione",
                    aiGenerated=False, documentaryPhoto=True)
        break
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

sync_surfaces([], f"/notizie/{SLUG}.html", VERSION)
for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
    path = ROOT / filename
    state = json.loads(path.read_text(encoding="utf-8"))
    state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION,
                 last_update="bjk-cup-foto-reale-v565")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_site_version"] = VERSION
manifest["site"]["site_version"] = VERSION
manifest["site_version"] = VERSION
manifest["version"] = f"v{VERSION}"
manifest["release_version"] = f"v{VERSION}"
manifest["last_release"] = {
    "version": VERSION,
    "date": "2026-09-25",
    "type": "image-update",
    "news_added": [],
    "news_updated": [SLUG],
    "change": "Foto reale della squadra al posto dell'illustrazione IA",
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"version": VERSION, "variants": new_variants}, ensure_ascii=False))
