#!/usr/bin/env python3
"""Ripara metadati cronologici storici e la card In evidenza per v522."""
from __future__ import annotations

from datetime import datetime, timedelta
import json
from pathlib import Path
import subprocess
import sys

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

TARGETS = {
    "italia-bielorussia-femminile-biglietti-firenze-13-ottobre-2026-22-09-2026.html",
    "ia-video-aws-e-tbc-lanciano-un-modello-ottimizzato-studiando-neuroni-reali-22-09-2026.html",
    "brothers-apple-tv-debutto-23-settembre-mcconaughey-harrelson-22-09-2026.html",
    "nasce-il-p4m-23-paesi-rilanciano-multilateralismo-e-diritto-internazionale-22-09-2026.html",
    "michael-kayode-prima-convocazione-nazionale-serie-d-premier-2026.html",
    "enisa-2026-pubblica-amministrazione-32-percento-attacchi-informatici.html",
    "italia-oro-staffetta-mista-mondiali-ciclismo-montreal-2026.html",
    "brad-pitt-torna-come-cliff-booth-nel-nuovo-film-di-david-fincher-22-09-2026.html",
    "iea-elettrificazione-importazioni-combustibili-400-miliardi-2035.html",
    "ue-e-australia-rafforzano-la-cooperazione-su-sicurezza-materie-prime-e-commercio-22-09-2026.html",
    "brics-impegni-sanita-vaccini-pandemie-oms-21-settembre-2026.html",
    "amazon-porta-in-italia-aggiungi-alla-consegna-come-funziona-per-i-clienti-prime-22-09-2026.html",
}


def repair_publication_dates() -> list[str]:
    repaired = []
    for path in (ROOT / "notizie").glob("*.html"):
        if path.name not in TARGETS:
            continue
        doc = html.fromstring(path.read_text(encoding="utf-8"))
        changed = False
        for node in doc.xpath('//script[@type="application/ld+json"]'):
            try:
                data = json.loads(node.text or "")
            except Exception:
                continue
            if not isinstance(data, dict) or data.get("@type") != "NewsArticle" or not data.get("datePublished"):
                continue
            proc = subprocess.run(
                ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", path.relative_to(ROOT).as_posix()],
                cwd=ROOT, capture_output=True, text=True, check=True,
            )
            stamps = [s.strip() for s in proc.stdout.splitlines() if s.strip()]
            if not stamps:
                break
            first_added = datetime.fromisoformat(stamps[-1].replace("Z", "+00:00"))
            declared = datetime.fromisoformat(str(data["datePublished"]).replace("Z", "+00:00"))
            if first_added.tzinfo is None:
                first_added = first_added.replace(tzinfo=site.ROME)
            if declared.tzinfo is None:
                declared = declared.replace(tzinfo=site.ROME)
            if first_added - declared > timedelta(minutes=15):
                data["datePublished"] = first_added.isoformat(timespec="seconds")
                modified = datetime.fromisoformat(str(data.get("dateModified", data["datePublished"])).replace("Z", "+00:00"))
                if modified.tzinfo is None:
                    modified = modified.replace(tzinfo=site.ROME)
                if modified < first_added:
                    data["dateModified"] = first_added.isoformat(timespec="seconds")
                node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                changed = True
            break
        if changed:
            path.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")
            repaired.append(path.name)
    return repaired


def main() -> None:
    repaired = repair_publication_dates()
    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8"))
    target = "/notizie/eurovolley-2026-francia-polonia-semifinali-3-0.html"
    for item in feed["items"]:
        if item.get("url") == target:
            item["featuredHighlights"] = ["Francia", "Polonia"]
            break
    feed_path.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces([], "", 522)
    print(json.dumps({"repaired_dates": repaired, "featured": target}, ensure_ascii=False))


if __name__ == "__main__":
    main()
