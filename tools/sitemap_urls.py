#!/usr/bin/env python3
"""Controlla e corregge gli <url> annidati nelle sitemap di CurioMondo.

Lo standard Sitemap richiede che ogni <url> sia figlio diretto di <urlset>.
Questo modulo non legge il manifest e non modifica le date già presenti.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import argparse
import hashlib
import re
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


def _legacy_archive(repo: Path) -> dict[str, dict[str, Any]]:
    """Evidence for the frozen archive from the November 2026 migration."""
    path = repo / "tools/news_legacy_archive.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("registro archivio storico: oggetto atteso")
    for name, row in raw.items():
        if (not re.fullmatch(r"notizie/[a-z0-9][a-z0-9-]+\.html", name)
                or not isinstance(row, dict) or set(row) != {"sha256", "datePublished"}
                or not isinstance(row["sha256"], str)
                or not re.fullmatch(r"[a-f0-9]{64}", row["sha256"])):
            raise ValueError(f"registro archivio storico non valido: {name}")
        day = row["datePublished"]
        if day is not None:
            if not isinstance(day, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
                raise ValueError(f"registro archivio storico: data civile non valida per {name}")
            date.fromisoformat(day)
    return raw


def published_news(repo: Path) -> dict[str, dict[str, str]]:
    """Censisce ogni pagina /notizie/ pubblicata e indicizzabile.

    Il registro storico conserva soltanto pagine preesistenti con byte
    verificati e data civile, o nessuna data attestata. Non rende idonea
    alcuna nuova pagina priva di un timestamp completo.
    """
    news_dir = repo / "notizie"
    pages: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    legacy_rows = _legacy_archive(repo)
    seen_legacy: set[str] = set()
    for path in sorted(news_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        relative = path.relative_to(repo).as_posix()
        try:
            previous = legacy_rows.get(relative)
            content = path.read_bytes()
            parser = _NewsPageParser()
            parser.feed(content.decode("utf-8"))
            if previous is not None:
                seen_legacy.add(relative)
            if "noindex" in " ".join(parser.robots).casefold():
                if previous is not None:
                    raise ValueError("pagina storica deindicizzata")
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
            public_url = f"/notizie/{path.name}"
            if previous is not None and hashlib.sha256(content).hexdigest() == previous["sha256"]:
                verified = previous["datePublished"]
                observed = article.get("datePublished") if article else None
                if verified != observed or (verified is None and (article is not None or json_errors)):
                    raise ValueError("metadati storici diversi dal registro")
                pages[public_url] = {
                    "url": public_url, "loc": expected, "published": verified or "",
                    "lastmod": verified or "", "archive_only": "true",
                }
                continue
            if article is None:
                detail = f" ({'; '.join(json_errors)})" if json_errors else ""
                raise ValueError("NewsArticle assente o non valido" + detail)
            published = str(article.get("datePublished") or "")
            if not published:
                raise ValueError("datePublished assente")
            parsed = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if parsed.tzinfo is None or not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", published):
                raise ValueError("datePublished senza fuso orario")
            pages[public_url] = {
                "url": public_url,
                "loc": expected,
                "published": published,
                "lastmod": published[:10],
            }
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    errors.extend(f"{relative}: pagina storica mancante" for relative in sorted(set(legacy_rows) - seen_legacy))
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
    dated = {url for url, row in pages.items() if not row.get("archive_only")}
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
            missing(label, actual, dated if label == "home-feed-v210.json" else expected)
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
    recent = {loc for _, loc in news_window(pages, moment)}
    robots_path = repo / "robots.txt"
    try:
        robots = robots_path.read_text(encoding="utf-8") if robots_path.exists() else ""
        news_urls, news_errors = read_news_sitemaps(robots, lambda path: (repo / path[1:]).read_bytes())
        errors.extend(news_errors)
        missing("news-sitemap.xml", news_urls, recent)
    except (OSError, UnicodeError) as exc:
        errors.append(f"News Sitemap non verificabile: {exc}")
    return errors


NEWS_NS = "http://www.google.com/schemas/sitemap-news/0.9"
NEWS_LIMIT = 1000
NEWS_ROOT = "/news-sitemap.xml"
_PART = re.compile(r"/news-sitemap-(?:[2-9]|[1-9]\d+)\.xml")


def news_sitemap_paths(robots: str) -> tuple[str, ...]:
    """Only discover numbered News XML on CurioMondo; never follow other URLs."""
    paths = {NEWS_ROOT}
    for line in robots.splitlines():
        name, sep, value = line.partition(":")
        target = value.strip()
        if sep and name.strip().casefold() == "sitemap" and target.startswith(SITE):
            path = target[len(SITE):]
            if _PART.fullmatch(path):
                paths.add(path)
    return (NEWS_ROOT, *sorted(paths - {NEWS_ROOT}, key=lambda path: int(path.rsplit("-", 1)[1][:-4])))


def read_news_sitemaps(robots: str, read) -> tuple[set[str], list[str]]:
    urls: set[str] = set()
    errors: list[str] = []
    for path in news_sitemap_paths(robots):
        label = path.lstrip("/")
        try:
            root = ET.fromstring(read(path))
        except (OSError, ValueError, ET.ParseError) as exc:
            errors.append(f"{label}: non verificabile ({exc})")
            continue
        errors.extend(tree_errors(root, label))
        if len(root.findall(URL)) > NEWS_LIMIT:
            errors.append(f"{label}: superato il limite di {NEWS_LIMIT} voci News")
        rows = {(node.findtext(LOC) or "").strip() for node in root.findall(URL)}
        duplicated = sorted((urls & rows) - {""})
        if duplicated:
            errors.append(f"{label}: URL ripetuti tra file News: " + ", ".join(duplicated[:10]))
        urls.update(rows - {""})
    return urls, errors


def news_window(pages: dict[str, dict[str, str]], now: datetime) -> list[tuple[datetime, str]]:
    if now.tzinfo is None:
        raise ValueError("orario di verifica senza fuso")
    now = now.astimezone(timezone.utc)
    cutoff = now - timedelta(hours=48)
    rows = []
    for row in pages.values():
        if row.get("archive_only"):
            continue
        stamp = datetime.fromisoformat(row["published"].replace("Z", "+00:00"))
        if cutoff <= stamp <= now:
            rows.append((stamp, row["loc"]))
    return sorted(rows, reverse=True)


def write_news_sitemaps(repo: Path, pages: dict[str, dict[str, str]],
                        titles: dict[str, str], now: datetime) -> list[str]:
    rows = news_window(pages, now)
    # Validate before writing any file.
    absent = [url for _, url in rows if not titles.get(url)]
    if absent:
        raise ValueError(f"titolo assente per la News Sitemap: {absent[0]}")
    robots_path = repo / "robots.txt"
    prior = robots_path.read_text(encoding="utf-8")
    ET.register_namespace("", SM_NS)
    ET.register_namespace("news", NEWS_NS)
    ns = f"{{{NEWS_NS}}}"
    paths: list[str] = []
    for offset in range(0, max(1, len(rows)), NEWS_LIMIT):
        number = offset // NEWS_LIMIT + 1
        path = NEWS_ROOT if number == 1 else f"/news-sitemap-{number}.xml"
        root = ET.Element(f"{{{SM_NS}}}urlset")
        for stamp, url in rows[offset:offset + NEWS_LIMIT]:
            entry = ET.SubElement(root, URL)
            ET.SubElement(entry, LOC).text = url
            news = ET.SubElement(entry, ns + "news")
            pub = ET.SubElement(news, ns + "publication")
            ET.SubElement(pub, ns + "name").text = "CurioMondo"
            ET.SubElement(pub, ns + "language").text = "it"
            ET.SubElement(news, ns + "publication_date").text = stamp.isoformat()
            ET.SubElement(news, ns + "title").text = titles[url]
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(repo / path[1:], encoding="utf-8", xml_declaration=True)
        paths.append(path)
    # If an older extra part is still reachable, ensure it no longer advertises
    # out-of-window items. Never delete any sitemap or article.
    for old_path in set(news_sitemap_paths(prior)) - set(paths):
        empty = ET.Element(f"{{{SM_NS}}}urlset")
        ET.ElementTree(empty).write(repo / old_path[1:], encoding="utf-8", xml_declaration=True)
    def is_extra(line: str) -> bool:
        label, _, value = line.partition(":")
        return label.strip().casefold() == "sitemap" and value.strip().startswith(SITE) and bool(
            _PART.fullmatch(value.strip()[len(SITE):]))
    base = [line for line in prior.splitlines() if not is_extra(line)]
    for path in paths[1:]:
        base.append("Sitemap: " + SITE + path)
    robots = "\n".join(base) + "\n"
    if robots != prior:
        robots_path.write_text(robots, encoding="utf-8")
    return paths


def replace_news_urls(root: ET.Element, pages: dict[str, dict[str, str]], *, preserve_prior: bool = False) -> None:
    """Aggiorna le URL delle notizie; nel publisher conserva tutte le voci esistenti."""
    flatten(root)
    existing = set()
    for node in list(root):
        loc = (node.findtext(LOC) or "").strip()
        if not preserve_prior and loc.startswith(f"{SITE}/notizie/"):
            root.remove(node)
        else:
            existing.add(loc)
    for row in reversed(list(pages.values())):
        if row["loc"] in existing:
            continue
        node = ET.Element(URL)
        ET.SubElement(node, LOC).text = row["loc"]
        if row["lastmod"]:
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
    parser = argparse.ArgumentParser(description="Controlla le sitemap di CurioMondo")
    parser.add_argument("--refresh-news", action="store_true",
                        help="Ricrea solo le sitemap News dalle date di prima pubblicazione")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.refresh_news:
        pages = published_news(root)
        feed = json.loads((root / "assets/data/home-feed-v210.json").read_text(encoding="utf-8"))
        titles = {SITE + row["url"]: row["title"] for row in feed["items"]}
        paths = write_news_sitemaps(root, pages, titles, datetime.now(ROME))
        print("News Sitemap: " + ", ".join(paths))
    errors = structure_errors(root / "sitemap.xml")
    robots = (root / "robots.txt").read_text(encoding="utf-8")
    _, news_errors = read_news_sitemaps(robots, lambda path: (root / path[1:]).read_bytes())
    errors.extend(news_errors)
    if errors:
        print("\n".join(errors))
        return 1
    print("sitemap: struttura valida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
