#!/usr/bin/env python3
"""Prepara il lotto del primo mattino v845 senza manifest né operazioni remote."""
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
from tools.publish_notte_mattina_20261010_v827 import set_published
from tools.publish_finale_20261010_v836 import correct_visible_date

VERSION = 845


def set_times(rows):
    release = datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    for article, minutes in zip(rows, (0, 5, 11, 18, 26, 35, 45)):
        stamp = release - timedelta(minutes=minutes)
        set_published(article["slug"], stamp)
        correct_visible_date(article["slug"], stamp, article["luogo"])
    return release


def main():
    rows = json.loads((ROOT / "tools/news_batch_20261013_v845.json").read_text())
    source_map = json.loads((ROOT / "tools/news_images_20261013_v845.json").read_text())
    if sys.argv[1:] == ["--repair"]:
        target = next(a for a in rows if a["image_key"] == "papa")
        path = ROOT / "notizie" / (target["slug"] + ".html")
        doc = html.fromstring(path.read_text())
        doc.xpath('//figure[contains(@class,"article-image")]//img')[0].set("alt", target["image_alt"])
        doc.xpath('//meta[@property="og:image:alt"]')[0].set("content", target["image_alt"])
        path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n")
        path = ROOT / "assets/data/editorial-images-v210.json"
        registry = json.loads(path.read_text())
        for image in registry["items"]:
            if image.get("id") == target["slug"]:
                image.update({"alt": target["image_alt"], "prompt": source_map["papa_prompt"], "portraitOnly": True, "portraitFormat": "neutral-isolated"})
        path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
        target = next(a for a in rows if a["image_key"] == "arera")
        path = ROOT / "notizie" / (target["slug"] + ".html")
        doc = html.fromstring(path.read_text())
        for node, paragraph in zip(doc.xpath('//article[contains(@class,"art-body")]//p'), target["paragrafi"]):
            node.text = paragraph
        path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n")
        target = next(a for a in rows if a["image_key"] == "fmi")
        path = ROOT / "notizie" / (target["slug"] + ".html")
        doc = html.fromstring(path.read_text())
        anchors = doc.xpath('//div[contains(@class,"art-sources")]//li/a')
        anchors[1].set("href", target["fonti"][1]["url"])
        anchors[1].text = target["fonti"][1]["nome"]
        path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n")
        print("Riparati ritratto neutrale e paragrafi ARERA")
        return
    if sys.argv[1:] == ["--refresh-times"]:
        release = set_times(rows)
        site.sync_surfaces(rows, "/notizie/" + rows[0]["slug"] + ".html", VERSION, update_manifest=False)
        print(release.isoformat())
        return

    for article in rows:
        if (ROOT / "notizie" / (article["slug"] + ".html")).exists():
            raise SystemExit("Articolo già presente: " + article["slug"])

    images = []
    for article in rows:
        key = article["image_key"]
        source = ROOT.parent / "generated_images" / source_map[key]
        canvas = ImageOps.fit(Image.open(source).convert("RGB"), (1600, 900), method=Image.Resampling.LANCZOS)
        variants = []
        for width in (480, 800, 1200):
            height = round(width * 9 / 16)
            target = ROOT / "assets/images/editorial-auto" / f"{article['slug']}-v{VERSION}-{width}.webp"
            canvas.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=89, method=6)
            variants.append({"w": width, "h": height, "src": "/assets/images/editorial-auto/" + target.name, "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
        image = {"id": article["slug"], "article": "/notizie/" + article["slug"] + ".html", "alt": article["image_alt"], "prompt": source_map[key + "_prompt"], "variants": variants, "disclosure": site.CAPTION, "generator": "OpenAI image generation", "aiGenerated": True, "documentaryPhoto": False, "officialArtwork": False, "sensitiveContext": key == "papa", "weatherMap": False, "reenactedEvent": False, "logoApplied": False}
        if article.get("likeness"):
            image.update({"syntheticLikeness": "public-figure", "publicFigureName": article["likeness"]})
        if key == "papa":
            image.update({"portraitOnly": True, "portraitFormat": "neutral-isolated"})
        site.write_article(article, image, VERSION)
        images.append(image)

    release = set_times(rows)
    path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(path.read_text())
    registry["items"] = images + registry["items"]
    registry["version"] = VERSION
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    site.sync_surfaces(rows, images[0]["article"], VERSION, update_manifest=False)
    path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(path.read_text())
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION), "articleCount": int(state["articleCount"]) + len(rows), "generatedEditorialImages": int(state["generatedEditorialImages"]) + len(rows), "last_update": "ultime-notizie-v845", "date": release.date().isoformat(), "release_date": release.date().isoformat(), "updated_at": release.isoformat(), "status": "ready"})
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"version": VERSION, "new_articles": len(rows), "slugs": [a["slug"] for a in rows]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
