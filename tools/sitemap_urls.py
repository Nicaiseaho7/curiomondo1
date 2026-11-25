#!/usr/bin/env python3
"""Controlla e corregge gli <url> annidati nelle sitemap di CurioMondo.

Lo standard Sitemap richiede che ogni <url> sia figlio diretto di <urlset>.
Questo modulo non legge il manifest e non modifica le date già presenti.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from html.parser import HTMLParser
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
URL = f"{{{SM_NS}}}url"
LOC = f"{{{SM_NS}}}loc"
ROME = ZoneInfo("Europe/Rome")
SITE = "https://curiomondo.it"


class _NewsPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.robots: list[str] = []
        self.canonicals: list[str] = []
        self._json_script = False
        self._json_buffer: list[str] = []
        self.json_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = {str(key).casefold(): value or "" for key, value in attrs}
        if tag.casefold() == "meta" and values.get("name", "").casefold() == "robots":
            self.robots.append(values.get("content", ""))
        elif tag.casefold() == "link" and "canonical" in values.get("rel", "").casefold().split():
            self.canonicals.append(values.get("href", ""))
        elif tag.casefold() == "script" and values.get("type", "").casefold() == "application/ld+json":
            self._json_script = True
            self._json_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "script" and self._json_script:
            self.json_blocks.append("".join(self._json_buffer))
            self._json_script = False
            self._json_buffer = []

    def handle_data(self, data: str) -> None:
        if self._json_script:
            self._json_buffer.append(data)


def _news_object(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        if value.get("@type") == "NewsArticle":
            return value
        graph = value.get("@graph")
        if isinstance(graph, list):
            return next((item for item in graph if isinstance(item, dict) and item.get("@type") == "NewsArticle"), None)
    if isinstance(value, list):
        return next((item for item in value if isinstance(item, dict) and item.get("@type") == "NewsArticle"), None)
    return None


def published_news(repo: Path) -> dict[str, dict[str, str]]:
    """Censisce ogni pagina /notizie/ pubblicata e indicizzabile.

    Le pagine ``noindex`` sono esclusioni editoriali legittime. Qualsiasi altra
    pagina deve avere canonical coerente e metadati NewsArticle leggibili: un
    errore blocca la rigenerazione, invece di far sparire la pagina dagli indici.
    """
    news_dir = repo / "notizie"
    pages: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    for path in sorted(news_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        relative = path.relative_to(repo).as_posix()
        try:
            raw = path.read_text(encoding="utf-8")
            parser = _NewsPageParser()
            parser.feed(raw)
            if "noindex" in " ".join(parser.robots).casefold():
                continue
            expected = f"{SITE}/notizie/{path.name}"
            if parser.canonicals != [expected]:
                raise ValueError(f"canonical atteso {expected}, trovati {parser.canonicals or 'nessuno'}")
            article = None
            json_errors: list[str] = []
            for block in parser.json_blocks:
                try:
                    article = _news_object(json.loads(block)) or article
                except json.JSONDecodeError as exc:
                    json_errors.append(str(exc))
            if article is None:
                detail = f" ({'; '.join(json_errors)})" if json_errors else ""
                raise ValueError("NewsArticle assente o non valido" + detail)
            published = str(article.get("datePublished") or "")
            if not published:
                raise ValueError("datePublished assente")
            parsed = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                raise ValueError("datePublished senza fuso orario")
            public_url = f"/notizie/{path.name}"
            pages[public_url] = {
                "url": public_url,
                "loc": expected,
                "published": published,
                "lastmod": published[:10],
            }
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    if errors:
        raise ValueError("pagine notizie non censibili:\n- " + "\n- ".join(errors))
    return pages


def _xml_locs(path: Path) -> set[str]:
    return {
        (node.text or "").strip()
        for node in ET.parse(path).getroot().iter(LOC)
        if (node.text or "").strip()
    }


def _hrefs(path: Path) -> set[str]:
    class Links(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.values: set[str] = set()

        def handle_starttag(self, tag: str, attrs) -> None:
            if tag.casefold() != "a":
                return
            values = {str(key).casefold(): value or "" for key, value in attrs}
            if values.get("href"):
                self.values.add(values["href"])

    parser = Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.values


def news_completeness_errors(repo: Path, now: datetime | None = None) -> list[str]:
    """Confronta le pagine reali con tutte le superfici editoriali complete."""
    try:
        pages = published_news(repo)
    except ValueError as exc:
        return [str(exc)]
    expected = set(pages)
    expected_locs = {row["loc"] for row in pages.values()}
    errors: list[str] = []

    def missing(label: str, actual: set[str], wanted: set[str]) -> None:
        absent = sorted(wanted - actual)
        if absent:
            errors.append(f"{label}: mancano {len(absent)} notizie: " + ", ".join(absent[:10]))

    try:
        missing("sitemap.xml", _xml_locs(repo / "sitemap.xml"), expected_locs)
    except (OSError, ET.ParseError) as exc:
        errors.append(f"sitemap.xml non verificabile: {exc}")
    try:
        missing("notizie/index.html", _hrefs(repo / "notizie/index.html"), expected)
    except OSError as exc:
        errors.append(f"notizie/index.html non verificabile: {exc}")
    for relative, label in (
        ("assets/data/search-index-v210.json", "search-index-v210.json"),
        ("assets/data/home-feed-v210.json", "home-feed-v210.json"),
    ):
        try:
            data = json.loads((repo / relative).read_text(encoding="utf-8"))
            actual = {str(item.get("url")) for item in data.get("items", []) if isinstance(item, dict)}
            missing(label, actual, expected)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{label} non verificabile: {exc}")
    try:
        feed_root = ET.parse(repo / "feed.xml").getroot()
        actual = set()
        for item in feed_root.findall("./channel/item"):
            target = (item.findtext("guid") or item.findtext("link") or "").strip()
            if target.startswith(SITE):
                target = target[len(SITE):]
            if target.startswith("/notizie/"):
                actual.add(target)
        missing("feed.xml", actual, expected)
    except (OSError, ET.ParseError) as exc:
        errors.append(f"feed.xml non verificabile: {exc}")
    moment = (now or datetime.now(ROME)).astimezone(ROME)
    cutoff = moment - timedelta(days=2)
    recent = {
        row["loc"] for row in pages.values()
        if datetime.fromisoformat(row["published"].replace("Z", "+00:00")).astimezone(ROME) >= cutoff
    }
    try:
        missing("news-sitemap.xml", _xml_locs(repo / "news-sitemap.xml"), recent)
    except (OSError, ET.ParseError) as exc:
        errors.append(f"news-sitemap.xml non verificabile: {exc}")
    return errors


def replace_news_urls(root: ET.Element, pages: dict[str, dict[str, str]]) -> None:
    """Sostituisce solo le URL delle notizie, conservando ogni altra pagina."""
    flatten(root)
    for node in list(root):
        loc = (node.findtext(LOC) or "").strip()
        if loc.startswith(f"{SITE}/notizie/"):
            root.remove(node)
    for row in reversed(list(pages.values())):
        node = ET.Element(URL)
        ET.SubElement(node, LOC).text = row["loc"]
        ET.SubElement(node, f"{{{SM_NS}}}lastmod").text = row["lastmod"]
        root.insert(0, node)


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

