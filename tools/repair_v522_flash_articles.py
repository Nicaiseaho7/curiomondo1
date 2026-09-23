#!/usr/bin/env python3
"""Allinea gli articoli flash v522 al protocollo editoriale v4."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "giornate-europee-patrimonio-26-27-settembre-2026.html",
    "roma-barcellona-femminile-biglietti-30-settembre-2026.html",
    "btp-green-2038-collocati-otto-miliardi-rendimento.html",
    "meta-petal-cavo-transatlantico-petabit-francia-usa-2029.html",
    "nasa-spacex-crew-13-lancio-1-ottobre-2026.html",
    "eurovolley-2026-francia-polonia-semifinali-3-0.html",
    "pio-sebastiano-esposito-insieme-nazionale-fratelli-italia-23-09-2026.html",
    "docufilm-80-anni-fipav-rai-2-23-settembre-2026.html",
    "incendiamoeba-cascadensis-record-eucarioti-63-gradi-23-09-2026.html",
    "inail-2025-1189-morti-lavoratori-malattie-professionali.html",
]


def first_commit(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", rel],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return [line for line in result.stdout.splitlines() if line][-1]


for filename in FILES:
    path = ROOT / "notizie" / filename
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    body = doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
    for paragraph in body.xpath("./p[position() > 4]"):
        paragraph.getparent().remove(paragraph)
    published = first_commit(path)
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            data = json.loads(node.text)
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("@type") == "NewsArticle":
            data["datePublished"] = published
            if data.get("dateModified", "") < published:
                data["dateModified"] = published
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    rendered = html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>")
    path.write_text(rendered + "\n", encoding="utf-8")

print(json.dumps({"repaired": len(FILES)}, ensure_ascii=False))
