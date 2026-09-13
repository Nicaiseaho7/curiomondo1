"""Renderer e sincronizzatore del sito statico CurioMondo.

Riceve articoli già verificati, crea pagine coerenti con il template corrente e
rigenera in un solo passaggio tutte le superfici editoriali. Non effettua push:
il workflow pubblica soltanto dopo il gate ``tools/predeploy.py``.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from email.utils import format_datetime
from html import escape
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[2]
ROME = ZoneInfo("Europe/Rome")
CAPTION = (
    "Illustrazione editoriale CurioMondo generata con IA per rappresentare "
    "questa notizia; non è una fotografia documentaria."
)
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
NEWS_NS = "http://www.google.com/schemas/sitemap-news/0.9"


def _version() -> int:
    manifest = json.loads((ROOT / "curiomondo-site-manifest.json").read_text(encoding="utf-8"))
    site = manifest.get("site", {})
    return int(site.get("site_version") or site.get("current_site_version") or 0) + 1


def _italian_date(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ROME)
    months = ("gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
              "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre")
    return f"{dt.day} {months[dt.month - 1]} {dt.year}"


def _section(category: str) -> str:
    category = category.strip() or "Mondo"
    if category in {"Italia", "Mondo"}:
        return category
    if category in {"Politica", "Cronaca", "Economia", "Sport", "Cultura"}:
        return f"Italia / {category}"
    return f"Mondo / {category}"


def _related(article: dict[str, Any]) -> list[dict[str, str]]:
    path = ROOT / "assets/data/home-feed-v210.json"
    if not path.exists():
        return []
    items = json.loads(path.read_text(encoding="utf-8")).get("items", [])
    category = str(article.get("categoria", "")).lower()
    picked = [i for i in items if category and category in str(i.get("section", "")).lower()]
    picked.extend(i for i in items if i not in picked)
    return [{"url": i["url"], "title": i["title"]} for i in picked[:3]]


def render_article(article: dict[str, Any], image: dict[str, Any], version: int) -> tuple[str, str]:
    """Rende una pagina articolo e ritorna ``(slug, html)``."""
    now = datetime.now(ROME).replace(microsecond=0)
    slug = str(article["slug"]).strip("-")
    if not re.search(r"(?:19|20)\d{2}", slug):
        slug += "-" + now.strftime("%d-%m-%Y")
    target = ROOT / "notizie" / f"{slug}.html"
    if target.exists():
        raise ValueError(f"slug già esistente: {slug}")

    canonical = f"https://curiomondo.it/notizie/{slug}.html"
    title = str(article["titolo"]).strip()
    summary = str(article["sommario"]).strip()
    category = _section(str(article.get("categoria", "Mondo")))
    place = str(article.get("luogo", "")).strip() or "—"
    published = now.isoformat()
    img1200 = "https://curiomondo.it" + image["variants"][-1]["src"]
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": title, "description": summary,
        "datePublished": published, "dateModified": published,
        "mainEntityOfPage": canonical, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "image": [img1200],
    }
    paragraphs = "".join(f"<p>{escape(str(p))}</p>" for p in article["paragrafi"])
    sources = "".join(
        f'<li><a href="{escape(str(f["url"]), quote=True)}" rel="noopener noreferrer" '
        f'target="_blank">{escape(str(f.get("descrizione") or "Fonte consultata"))}</a></li>'
        for f in article["fonti"][:6]
    )
    stats = "".join(
        f'<div><strong>{escape(str(d.get("valore", "")))}</strong>'
        f'<span>{escape(str(d.get("etichetta", "")))}</span></div>'
        for d in article["dati_chiave"][:3]
    )
    related = "".join(
        f'<a href="{escape(i["url"], quote=True)}"><strong>{escape(i["title"])}</strong></a>'
        for i in _related(article)
    )
    attrs = ['class="article-image"', 'data-ai-generated="true"']
    sensitive = bool(image.get("sensitiveContext"))
    if image.get("syntheticLikeness") == "public-figure":
        attrs.extend(['data-synthetic-likeness="public-figure"',
                      f'data-sensitive-context="{str(sensitive).lower()}"'])
        if sensitive:
            attrs.append('data-portrait-format="neutral-isolated"')
    elif sensitive:
        attrs.append('data-sensitive-context="true"')
    variants = {v["w"]: v["src"] for v in image["variants"]}
    read_minutes = max(1, round(len(" ".join(article["paragrafi"]).split()) / 210))
    date_label = _italian_date(published)
    page = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | CurioMondo</title><meta name="description" content="{escape(summary, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(summary, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{img1200}"><meta property="og:image:alt" content="{escape(image['alt'], quote=True)}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v={version}"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{slug}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner"><a class="cm-global-header__back" href="/" aria-label="Torna alla home"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a></nav></header><main class="wrap"><div class="badge">{escape(category)}</div><h1>{escape(title)}</h1><p class="subtitle">{escape(summary)}</p><div class="meta">{date_label} · {escape(place)} · <span id="readTime">{read_minutes} min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html">Redazione CurioMondo</a></p><figure {' '.join(attrs)}><picture><img src="..{variants[800]}" srcset="..{variants[480]} 480w, ..{variants[800]} 800w, ..{variants[1200]} 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(image['alt'], quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{stats}</div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="{escape(str(article['formato']))}">{paragraphs}</article><section class="curio-related"><h2>Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: {date_label}.<br>{CAPTION}</small></p></div></main><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v={version}" defer></script></body></html>'''
    article["slug"] = slug
    article["published"] = published
    article["category_full"] = category
    return slug, page


def write_article(article: dict[str, Any], image: dict[str, Any], version: int) -> str:
    slug, page = render_article(article, image, version)
    (ROOT / "notizie" / f"{slug}.html").write_text(page, encoding="utf-8")
    return slug


def register_image(image: dict[str, Any], slug: str, version: int) -> None:
    path = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    image = dict(image)
    image["article"] = f"/notizie/{slug}.html"
    data.setdefault("items", []).insert(0, image)
    data["version"] = version
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _news_json(doc):
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            obj = json.loads(node.text or "")
        except Exception:
            continue
        if isinstance(obj, dict) and obj.get("@type") == "NewsArticle":
            return obj
    raise ValueError("NewsArticle assente")


def _text(nodes) -> str:
    return re.sub(r"\s+", " ", " ".join(nodes)).strip()


def _article_info(path: Path) -> dict[str, Any] | None:
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    if "noindex" in " ".join(doc.xpath('//meta[@name="robots"]/@content')).lower():
        return None
    hero = doc.xpath('//main//figure[contains(@class,"article-image")][1]//img[1]')
    if not hero:
        return None
    ld = _news_json(doc)
    iso = str(ld.get("datePublished", ""))
    if not iso:
        return None
    title = _text(doc.xpath('//main[contains(@class,"wrap")]//h1[1]//text()'))
    subtitle = _text(doc.xpath('//main[contains(@class,"wrap")]//p[contains(@class,"subtitle")][1]//text()'))
    badge = _text(doc.xpath('//main[contains(@class,"wrap")]//div[contains(@class,"badge")][1]//text()'))
    h = hero[0]
    src = h.get("src", "").removeprefix("..")
    srcset = re.sub(r'(?:(?<=^)|(?<=, ))\.\./', '/', h.get("srcset", ""))
    return {"title": title or str(ld.get("headline", "")), "excerpt": subtitle,
            "url": f"/notizie/{path.name}", "section": badge or "Notizie",
            "dateISO": iso, "dateLabel": iso[:10], "image": src,
            "imageAlt": h.get("alt", ""), "imageWidth": 800, "imageHeight": 533,
            "srcset": srcset}


def _picture(parent, item, eager=False):
    pic = etree.SubElement(parent, "picture")
    im = etree.SubElement(pic, "img", src=item["image"], srcset=item["srcset"],
                          sizes="(max-width:600px) 79vw,300px", width="800", height="533",
                          alt=item["imageAlt"], loading="eager" if eager else "lazy", decoding="async")
    if eager:
        im.set("fetchpriority", "high")


def _featured(item):
    node = etree.Element("article", {"class": "featured"}); _picture(node, item, True)
    txt = etree.SubElement(node, "div", {"class": "txt"})
    etree.SubElement(txt, "span", {"class": "tag"}).text = "In evidenza"
    h1 = etree.SubElement(txt, "h1"); title = item["title"]
    keys = [str(k) for k in item.get("featuredHighlights", []) if k]
    if keys:
        pattern = re.compile("(" + "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True)) + ")", re.I)
        parts = pattern.split(title); h1.text = parts[0]
        for part in parts[1:]:
            if pattern.fullmatch(part):
                etree.SubElement(h1, "span", {"class": "cm-featured-key"}).text = part
            elif len(h1):
                h1[-1].tail = (h1[-1].tail or "") + part
    else:
        h1.text = title
    etree.SubElement(txt, "p").text = item["excerpt"]
    stats = item.get("featuredStats", [])[:3]
    if len(stats) == 3:
        box = etree.SubElement(txt, "div", {"class": "cm-featured-stats", "aria-label": "Dati principali"})
        for stat in stats:
            row = etree.SubElement(box, "span", {"class": "cm-featured-stat"})
            etree.SubElement(row, "i", {"aria-hidden": "true"}).text = str(stat.get("icon", "•"))
            copy = etree.SubElement(row, "span")
            etree.SubElement(copy, "strong").text = str(stat.get("value", ""))
            etree.SubElement(copy, "small").text = str(stat.get("label", ""))
    foot = etree.SubElement(txt, "span", {"class": "cm-featured-foot"})
    etree.SubElement(foot, "a", {"class": "cta", "href": item["url"]}).text = "Leggi l’articolo →"
    etree.SubElement(foot, "time", {"class": "cm-featured-date", "datetime": item["dateISO"]}).text = _italian_date(item["dateISO"])
    return node


def _card(item, rail=False):
    node = etree.Element("a", {"class": "auto-card" if rail else "card", "href": item["url"]})
    _picture(node, item)
    body = etree.SubElement(node, "div", {"class": "abody" if rail else "body"})
    etree.SubElement(body, "div", {"class": "ameta" if rail else "meta"}).text = item["section"]
    etree.SubElement(body, "h3").text = item["title"]
    etree.SubElement(body, "p").text = item["excerpt"]
    etree.SubElement(body, "time", {"datetime": item["dateISO"]}).text = _italian_date(item["dateISO"]) if rail else item["dateLabel"]
    return node


def sync_surfaces(new_articles: list[dict[str, Any]], featured_url: str, version: int) -> list[dict[str, Any]]:
    """Rigenera home, archivio, ricerca, feed, sitemap e categorie."""
    infos = []
    for path in (ROOT / "notizie").glob("*.html"):
        if path.name == "index.html":
            continue
        try:
            info = _article_info(path)
        except Exception:
            info = None
        if info:
            infos.append(info)
    infos.sort(key=lambda i: i["dateISO"], reverse=True)
    new_by_url = {f"/notizie/{a['slug']}.html": a for a in new_articles}

    home_feed_path = ROOT / "assets/data/home-feed-v210.json"
    home_feed = json.loads(home_feed_path.read_text(encoding="utf-8"))
    old_by_url = {i.get("url"): i for i in home_feed.get("items", [])}
    feed_items = []
    for info in infos:
        old = old_by_url.get(info["url"], {})
        merged = dict(info)
        if old.get("excerpt"):
            merged["excerpt"] = old["excerpt"]
        for key in ("featuredHighlights", "featuredStats"):
            if old.get(key):
                merged[key] = old[key]
        if info["url"] in new_by_url:
            a = new_by_url[info["url"]]
            merged["featuredHighlights"] = a.get("parole_chiave_titolo", [])[:2]
            merged["featuredStats"] = [
                {"icon": d.get("icona", "•"), "value": d.get("valore", ""), "label": d.get("etichetta", "")}
                for d in a.get("dati_chiave", [])[:3]
            ]
        feed_items.append(merged)
    home_feed["version"] = version; home_feed["items"] = feed_items
    home_feed_path.write_text(json.dumps(home_feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    other = [i for i in search.get("items", []) if not str(i.get("url", "")).startswith("/notizie/")]
    search["version"] = version
    search["items"] = [{k: i[k] for k in ("title", "excerpt", "url", "section")} for i in feed_items] + other
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    home_path = ROOT / "index.html"; doc = html.fromstring(home_path.read_text(encoding="utf-8"))
    for track in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]'):
        for child in list(track): track.remove(child)
        for n, item in enumerate(feed_items[:10]):
            attrs = {"class": "ticker-news", "href": item["url"]}
            if track.tag == "div" and n >= 6: attrs["tabindex"] = "-1"
            etree.SubElement(track, "a", attrs).text = item["title"]
    featured = next((i for i in feed_items if i["url"] == featured_url), feed_items[0])
    ordered = [i for i in feed_items if i["url"] != featured["url"]]
    old_featured = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
    old_featured.getparent().replace(old_featured, _featured(featured))
    rail = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for child in list(rail): rail.remove(child)
    for item in ordered[:5]: rail.append(_card(item, True))
    cards = doc.xpath('//div[@id="cards"]')[0]
    for child in list(cards): cards.remove(child)
    for item in ordered[5:44]: cards.append(_card(item))
    cards.set("data-initial-count", str(min(39, max(0, len(ordered) - 5))))
    home_path.write_text('<!doctype html>\n' + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")

    archive_path = ROOT / "notizie/index.html"; archive = html.fromstring(archive_path.read_text(encoding="utf-8"))
    main = archive.xpath('//main')[0]; lead = main.xpath('./p[1]')
    if lead: lead[0].text = f"{len(feed_items)} articoli verificati e promossi, ordinati per data."
    ul = main.xpath('./ul')[0]
    for child in list(ul): ul.remove(child)
    for item in feed_items:
        li = etree.SubElement(ul, "li"); a = etree.SubElement(li, "a", href=item["url"])
        etree.SubElement(a, "strong").text = item["title"]; etree.SubElement(a, "span").text = item["dateLabel"]
    archive_path.write_text('<!doctype html>\n' + html.tostring(archive, encoding="unicode", method="html"), encoding="utf-8")

    rss_path = ROOT / "feed.xml"; tree = ET.parse(rss_path); channel = tree.getroot().find("channel")
    for node in list(channel):
        if node.tag == "item": channel.remove(node)
    for item in feed_items:
        node = ET.SubElement(channel, "item"); full = "https://curiomondo.it" + item["url"]
        ET.SubElement(node, "title").text = item["title"]; ET.SubElement(node, "link").text = full
        ET.SubElement(node, "guid").text = full
        ET.SubElement(node, "pubDate").text = format_datetime(datetime.fromisoformat(item["dateISO"].replace("Z", "+00:00")))
        ET.SubElement(node, "description").text = item["excerpt"]
    ET.indent(tree, space="  "); tree.write(rss_path, encoding="utf-8", xml_declaration=True)

    ET.register_namespace("", SM_NS); ET.register_namespace("news", NEWS_NS)
    news_root = ET.Element(f"{{{SM_NS}}}urlset"); cutoff = datetime.now(ROME) - timedelta(days=2)
    for item in feed_items:
        dt = datetime.fromisoformat(item["dateISO"].replace("Z", "+00:00")).astimezone(ROME)
        if dt < cutoff: continue
        u = ET.SubElement(news_root, f"{{{SM_NS}}}url"); ET.SubElement(u, f"{{{SM_NS}}}loc").text = "https://curiomondo.it" + item["url"]
        news = ET.SubElement(u, f"{{{NEWS_NS}}}news"); pub = ET.SubElement(news, f"{{{NEWS_NS}}}publication")
        ET.SubElement(pub, f"{{{NEWS_NS}}}name").text = "CurioMondo"; ET.SubElement(pub, f"{{{NEWS_NS}}}language").text = "it"
        ET.SubElement(news, f"{{{NEWS_NS}}}publication_date").text = item["dateISO"]
        ET.SubElement(news, f"{{{NEWS_NS}}}title").text = item["title"]
    news_tree = ET.ElementTree(news_root); ET.indent(news_tree, space="  ")
    news_tree.write(ROOT / "news-sitemap.xml", encoding="utf-8", xml_declaration=True)

    sitemap = ET.parse(ROOT / "sitemap.xml"); sm_root = sitemap.getroot()
    for node in list(sm_root):
        loc = node.find(f"{{{SM_NS}}}loc")
        if loc is not None and (loc.text or "").startswith("https://curiomondo.it/notizie/"):
            sm_root.remove(node)
    for item in reversed(feed_items):
        node = ET.Element(f"{{{SM_NS}}}url")
        ET.SubElement(node, f"{{{SM_NS}}}loc").text = "https://curiomondo.it" + item["url"]
        ET.SubElement(node, f"{{{SM_NS}}}lastmod").text = item["dateLabel"]
        sm_root.insert(0, node)
    ET.indent(sitemap, space="  "); sitemap.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)

    subprocess.run(["python3", "tools/generate_category_pages.py"], cwd=ROOT, check=True)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = version; manifest["site"]["site_version"] = version
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return feed_items
