#!/usr/bin/env python3
"""Build CurioMondo v233: neutral-portrait-only policy for public figures."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/workspace/scratch/bb5bac13bd1d/generated-v233/tadej-pogacar-neutral-editorial-portrait.png")
OLD_DIR = "/assets/images/editorial-v232"
OLD_KEY = "pogacar-vuelta-caduta-29-agosto-2026-ai"
NEW_DIR = "/assets/images/editorial-v233"
NEW_KEY = "pogacar-ritratto-neutrale-29-agosto-2026-ai"
NEW_ALT = "Ritratto editoriale neutrale ultrarealistico di Tadej Pogačar su sfondo blu e rosso"
NEW_PROMPT = "Ultra-realistic recognizable neutral editorial portrait of Tadej Pogacar, head-and-shoulders framing, neutral pose and expression, sober generic unbranded cycling top, simple premium blue-and-red studio gradient background, natural skin texture and credible studio lighting; person only, no action, location, other people, vehicle, bicycle, prop, injury, bandage, medical care, celebration, text, logo or watermark; disclosed synthetic editorial likeness, not documentary photography."


def dump(path: Path, data: object, *, compact: bool = False) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":") if compact else None, indent=None if compact else 2) + ("" if compact else "\n"),
        encoding="utf-8",
    )


def replace_text(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    updated = text
    for old, new in replacements:
        updated = updated.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


if not SOURCE.exists():
    raise SystemExit(f"Missing generated portrait: {SOURCE}")

with Image.open(SOURCE) as source:
    if source.size != (1536, 1024):
        raise SystemExit(f"Unexpected source size: {source.size}")
    source = source.convert("RGB")
    out_dir = ROOT / NEW_DIR.lstrip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    for width, height, quality in ((480, 320, 84), (800, 533, 86), (1200, 800, 88)):
        frame = source.resize((width, height), Image.Resampling.LANCZOS)
        frame.save(out_dir / f"{NEW_KEY}-{width}.webp", "WEBP", quality=quality, method=6)

path_replacements = [
    (f"{OLD_DIR}/{OLD_KEY}-480.webp", f"{NEW_DIR}/{NEW_KEY}-480.webp"),
    (f"{OLD_DIR}/{OLD_KEY}-800.webp", f"{NEW_DIR}/{NEW_KEY}-800.webp"),
    (f"{OLD_DIR}/{OLD_KEY}-1200.webp", f"{NEW_DIR}/{NEW_KEY}-1200.webp"),
    (OLD_KEY, NEW_KEY),
]

for path in (
    ROOT / "index.html",
    ROOT / "notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.html",
    ROOT / "contenuti/notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.json",
    ROOT / "assets/data/home-feed-v210.json",
    ROOT / "assets/data/editorial-images-v210.json",
    ROOT / "tools/build_v232.py",
):
    replace_text(path, path_replacements)

article_path = ROOT / "notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.html"
replace_text(
    article_path,
    [
        ('data-ai-generated="true" data-synthetic-likeness="public-figure"', 'data-ai-generated="true" data-synthetic-likeness="public-figure" data-portrait-format="neutral-isolated"'),
        ('"dateModified":"2026-08-29T18:52:00+02:00"', '"dateModified":"2026-08-29T19:23:00+02:00"'),
    ],
)

# Cache-bust only the current shared data consumers and the two pages changed here.
for path in (
    ROOT / "index.html",
    ROOT / "notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.html",
    ROOT / "assets/js/home-v210.js",
    ROOT / "assets/js/curiomondo-article-v210.js",
):
    replace_text(path, [("?v=232", "?v=233")])

for rel, compact in (
    ("assets/data/home-feed-v210.json", True),
    ("assets/data/search-index-v210.json", True),
    ("assets/data/editorial-images-v210.json", False),
):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = 233
    dump(path, data, compact=compact)

content_path = ROOT / "contenuti/notizie/pogacar-caduta-ritiro-vuelta-mas-maglia-rossa-29-agosto-2026.json"
content = json.loads(content_path.read_text(encoding="utf-8"))
content["updated_at"] = "2026-08-29T19:23:00+02:00"
content["image"]["portrait_only"] = True
content["image"]["reenacted_event"] = False
content["image"]["figure_attributes"]["data-portrait-format"] = "neutral-isolated"
dump(content_path, content)

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
for item in registry.get("items", []):
    if item.get("publicFigure") == "Tadej Pogačar":
        item["portraitOnly"] = True
        item["portraitFormat"] = "neutral-isolated"
        item["reenactedEvent"] = False
dump(registry_path, registry)

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_protocol_version"] = "1.6"
manifest["site"]["protocol_date"] = "2026-08-29"
manifest["site"]["current_site_version"] = 233
manifest["site_version"] = 233
manifest["version"] = "v233"
manifest["release_version"] = "v233"
dump(manifest_path, manifest)

dump(
    ROOT / "RELEASE-STATE.json",
    {
        "currentVersion": 233,
        "baselineVersion": 232,
        "status": "ready",
        "date": "2026-08-29",
        "articleCount": 187,
        "generatedEditorialImages": 67,
        "designRestored": "Pogačar ora usa un ritratto neutrale isolato; protocollo personaggi pubblici aggiornato per vietare ogni ricostruzione narrativa.",
    },
)
dump(
    ROOT / "CURIOMONDO-RELEASE-STATE.json",
    {
        "site_version": 233,
        "baseline_version": 232,
        "release_date": "2026-08-29",
        "protocol_files": [
            "AGENTS.md",
            "AI-EDITORIAL-IMAGE-PROTOCOL.md",
            "automation/prompts/image-generation-contract.txt",
            "LEGGIMI-PRIMA-CURIOMONDO.md",
            "CURIO-MONDO-PROTOCOLLO-MAESTRO.md",
            "curiomondo-site-manifest.json",
        ],
        "last_daily_question_date": "2026-08-28",
        "version": "233",
        "date": "2026-08-29",
        "baseline": "curiomondo-v232-29-agosto-2026-netlify.zip",
        "last_update": "public-figures-neutral-portrait-only-v233",
        "performance_pass": "Nuovo ritratto WebP responsive 480/800/1200; rimossi i tre visual precedenti della ricostruzione.",
    },
)

(ROOT / "RELEASE-NOTES-v233.md").write_text(
    """# CurioMondo v233 — 29 agosto 2026

- Nuova regola permanente: i personaggi pubblici possono apparire soltanto come ritratti neutrali isolati.
- Vietate ricostruzioni della notizia, scene d'azione, luoghi, altre persone, mezzi, oggetti, ferite, cure, arresti o celebrazioni, anche quando l'evento è verificato.
- Sostituito il visual di Tadej Pogačar con un ritratto editoriale neutrale su sfondo da studio.
- Aggiornati protocollo canonico, istruzioni per agenti IA, contratto del generatore, configurazione machine-readable e gate fail-closed.
- Mantenute disclosure visibile, metadati di somiglianza sintetica, immagine responsive e coerenza tra hero, `og:image` e `NewsArticle.image`.
""",
    encoding="utf-8",
)

# The superseded reenactment remains recoverable in the v232 package, but is not shipped in v233.
for width in (480, 800, 1200):
    old = ROOT / OLD_DIR.lstrip("/") / f"pogacar-vuelta-caduta-29-agosto-2026-ai-{width}.webp"
    if old.exists():
        old.unlink()

print(json.dumps({"version": 233, "portrait": str(SOURCE), "status": "built"}, ensure_ascii=False))
