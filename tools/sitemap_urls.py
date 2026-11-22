#!/usr/bin/env python3
"""Controlla e corregge gli <url> annidati nelle sitemap di CurioMondo.

Lo standard Sitemap richiede che ogni <url> sia figlio diretto di <urlset>.
Questo modulo non legge il manifest e non modifica le date già presenti.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
URL = f"{{{SM_NS}}}url"
LOC = f"{{{SM_NS}}}loc"


def flatten(root: ET.Element) -> int:
    """Porta ogni <url> annidato al livello di <urlset>, senza toccare <loc> e <lastmod>."""
    hoisted = 0
    moved = True
    while moved:
        moved = False
        for parent in root.iter():
            if parent is root:
                continue
            for child in list(parent):
                if child.tag != URL:
                    continue
                parent.remove(child)
                root.append(child)
                hoisted += 1
                moved = True
                break
            if moved:
                break
    return hoisted


def tree_errors(root: ET.Element, label: str = "sitemap") -> list[str]:
    errors: list[str] = []
    if root.tag != f"{{{SM_NS}}}urlset":
        return [f"{label}: la radice non è urlset"]
    parent_of: dict[ET.Element, ET.Element] = {}
    for parent in root.iter():
        for child in list(parent):
            parent_of[child] = parent
    seen: dict[str, int] = {}
    for node in root.iter(URL):
        parent = parent_of.get(node)
        loc = (node.findtext(LOC) or "").strip()
        if parent is not root:
            errors.append(f"{label}: <url> annidato, non figlio diretto di <urlset>: {loc or '(senza loc)'}")
        if not loc:
            errors.append(f"{label}: <url> senza <loc>")
            continue
        if not loc.startswith("https://curiomondo.it/"):
            errors.append(f"{label}: <loc> fuori dal sito: {loc}")
        seen[loc] = seen.get(loc, 0) + 1
    for loc, count in seen.items():
        if count > 1:
            errors.append(f"{label}: <loc> ripetuto {count} volte: {loc}")
    return errors


def structure_errors(path: Path) -> list[str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{path.name}: XML non valido ({exc})"]
    return tree_errors(root, path.name)


def ensure_approfondimenti(repo: Path) -> list[str]:
    """Inserisce in sitemap.xml ogni guida di /approfondimenti/ ancora assente.

    Non toglie URL e non riscrive le voci già presenti. Le curiosità e gli
    approfondimenti non vanno nella news-sitemap.
    """
    import re

    sitemap_path = repo / "sitemap.xml"
    guide_dir = repo / "approfondimenti"
    if not sitemap_path.exists() or not guide_dir.exists():
        return []
    text = sitemap_path.read_text(encoding="utf-8")
    if "</urlset>" not in text:
        raise RuntimeError("sitemap.xml senza </urlset>")
    added: list[str] = []
    blocks: list[str] = []
    for guide in sorted(guide_dir.glob("*.html")):
        if guide.name == "index.html":
            continue
        loc = f"https://curiomondo.it/approfondimenti/{guide.name}"
        if loc in text:
            continue
        raw = guide.read_text(encoding="utf-8", errors="replace")[:8000]
        found = re.search(r'dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', raw)
        if not found:
            found = re.search(r'datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', raw)
        day = found.group(1) if found else "2026-11-22"
        blocks.append(
            "  <url>"
            f"<loc>{loc}</loc>"
            f"<lastmod>{day}</lastmod>"
            "<changefreq>monthly</changefreq><priority>0.8</priority>"
            "</url>\n"
        )
        added.append(guide.name)
    if blocks:
        sitemap_path.write_text(text.replace("</urlset>", "".join(blocks) + "</urlset>"), encoding="utf-8")
    return added


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    for name in ("sitemap.xml", "news-sitemap.xml"):
        path = root / name
        if not path.exists():
            errors.append(f"assente: {name}")
            continue
        errors.extend(structure_errors(path))
    if errors:
        print("\n".join(errors))
        return 1
    print("sitemap: struttura valida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
