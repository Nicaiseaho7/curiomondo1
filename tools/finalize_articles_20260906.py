#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
import html as html_std
import json
import re
import xml.etree.ElementTree as ET

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

TARGETS = {
    "notizie/emma-bonino-morta-78-anni-11-settembre-2026.html": "emma-bonino-ritratto-neutrale-morte-ai-v323",
}

REG_PATH = ROOT / "assets/data/editorial-images-v210.json"
reg = json.loads(REG_PATH.read_text(encoding="utf-8"))
reg_by_key = {i.get("key"): i for i in reg.get("items", [])}

for rel, key in TARGETS.items():
    if key not in reg_by_key:
        raise SystemExit(f"Immagine mancante nel registro: {key}")
    for v in reg_by_key[key].get("variants", []):
        image_file = ROOT / v["src"].lstrip("/")
        if not image_file.exists() or image_file.stat().st_size == 0:
            raise SystemExit(f"Asset immagine mancante/vuoto: {image_file}")


def news_json(doc):
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        raw = node.text or ""
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if isinstance(obj, dict) and (obj.get("@type") == "NewsArticle" or "NewsArticle" in (obj.get("@type") or [])):
            return node, obj
    raise ValueError("NewsArticle JSON-LD assente")


def text_of(nodes):
    return re.sub(r"\s+", " ", " ".join(nodes)).strip()


def section_from_doc(doc):
    meta_text = text_of(doc.xpath('//main[contains(@class,"wrap")]//div[contains(concat(" ",normalize-space(@class)," ")," meta ")][1]//text()'))
    parts = [p.strip() for p in meta_text.split(" · ") if p.strip()]
    for p in parts:
        if "/" in p:
            return p
    badge = text_of(doc.xpath('//main[contains(@class,"wrap")]//div[contains(concat(" ",normalize-space(@class)," ")," badge ")][1]//text()'))
    return badge.replace(" · ", " / ") or "Notizie"


def italian_date(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    months = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    return f"{dt.day} {months[dt.month-1]} {dt.year}"


def image_data(item):
    variants = {int(v["w"]): v["src"] for v in item["variants"]}
    return {
        "image": variants[800],
        "srcset": f"{variants[480]} 480w, {variants[800]} 800w, {variants[1200]} 1200w",
        "image1200": variants[1200],
        "alt": item["alt"],
    }


def inject_image(rel, key):
    path = ROOT / rel
    source = path.read_text(encoding="utf-8")
    doc = html.fromstring(source)
    item = reg_by_key[key]
    img = image_data(item)
    public_figure = item.get("syntheticLikeness") == "public-figure"

    # Corregge il collegamento registro -> URL articolo reale.
    item["article"] = "/" + rel.replace("\\", "/")
    if public_figure:
        item["syntheticLikeness"] = "public-figure"
        item.setdefault("sensitiveContext", False)

    # OpenGraph: un solo og:image e alt, coerenti con hero e NewsArticle.image.
    head = doc.xpath("//head")[0]
    for n in doc.xpath('//meta[@property="og:image" or @property="og:image:alt"]'):
        n.getparent().remove(n)
    og_url = doc.xpath('//meta[@property="og:url"]')
    pos = head.index(og_url[0]) + 1 if og_url else len(head)
    ogi = etree.Element("meta", property="og:image", content="https://curiomondo.it" + img["image1200"])
    oga = etree.Element("meta", property="og:image:alt", content=img["alt"])
    head.insert(pos, ogi); head.insert(pos + 1, oga)

    ld_node, ld = news_json(doc)
    ld["image"] = ["https://curiomondo.it" + img["image1200"]]
    ld_node.text = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))

    # Rimuove eventuale vecchia hero e inserisce quella canonica subito dopo le azioni.
    main = doc.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," wrap ")]')[0]
    for old in main.xpath('./figure[contains(concat(" ",normalize-space(@class)," ")," article-image ")]'):
        main.remove(old)
    figure = etree.Element("figure", {"class": "article-image", "data-ai-generated": "true"})
    if public_figure:
        figure.set("data-synthetic-likeness", "public-figure")
        figure.set("data-sensitive-context", "true" if item.get("sensitiveContext") is True else "false")
        if item.get("sensitiveContext") is True:
            figure.set("data-portrait-format", "neutral-isolated")
    elif item.get("sensitiveContext") is True:
        figure.set("data-sensitive-context", "true")
    picture = etree.SubElement(figure, "picture")
    hero = etree.SubElement(picture, "img")
    hero.set("src", ".." + img["image"])
    hero.set("srcset", ", ".join(".." + chunk.strip() for chunk in img["srcset"].split(",")))
    hero.set("sizes", "(max-width:832px) calc(100vw - 32px),800px")
    hero.set("width", "800"); hero.set("height", "533")
    hero.set("alt", img["alt"]); hero.set("loading", "eager"); hero.set("decoding", "async"); hero.set("fetchpriority", "high")
    cap = etree.SubElement(figure, "figcaption"); cap.text = CAPTION
    actions = main.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," actions ")]')
    insert_at = main.index(actions[0]) + 1 if actions else 0
    main.insert(insert_at, figure)

    out = '<!doctype html>\n' + html.tostring(doc, encoding="unicode", method="html")
    path.write_text(out, encoding="utf-8")


for rel, key in TARGETS.items():
    inject_image(rel, key)

reg["version"] = 323
REG_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def article_info(path: Path):
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    robots = " ".join(doc.xpath('//meta[@name="robots"]/@content')).lower()
    hero = doc.xpath('//main//figure[1]//img[1]')
    if "noindex" in robots or not hero:
        return None
    _, ld = news_json(doc)
    iso = ld.get("datePublished")
    if not iso:
        return None
    title = text_of(doc.xpath('//main[contains(@class,"wrap")]//h1[1]//text()')) or ld.get("headline", "")
    subtitle = text_of(doc.xpath('//main[contains(@class,"wrap")]//p[contains(concat(" ",normalize-space(@class)," ")," subtitle ")][1]//text()'))
    desc = (doc.xpath('//meta[@name="description"]/@content') or [subtitle])[0]
    h = hero[0]
    src = h.get("src", "")
    if src.startswith("../"):
        src = "/" + src[3:]
    elif not src.startswith("/"):
        src = "/" + src
    srcset = h.get("srcset", "")
    srcset = re.sub(r'(?:(?<=^)|(?<=, ))\.\./', '/', srcset)
    url = "/notizie/" + path.name
    return {
        "title": title,
        "excerpt": subtitle or desc,
        "url": url,
        "section": section_from_doc(doc),
        "dateISO": iso,
        "dateLabel": iso[:10],
        "image": src,
        "imageAlt": h.get("alt", ""),
        "imageWidth": int(h.get("width") or 800),
        "imageHeight": int(h.get("height") or 533),
        "srcset": srcset,
        "_dt": datetime.fromisoformat(iso.replace("Z", "+00:00")),
    }

# Stesso criterio/ordine stabile usato dal predeploy: glob del filesystem + sort stabile per data.
infos = []
for p in (ROOT / "notizie").glob("*.html"):
    if p.name == "index.html":
        continue
    try:
        info = article_info(p)
    except Exception:
        info = None
    if info:
        infos.append(info)
infos.sort(key=lambda x: x["dateISO"], reverse=True)
by_url = {i["url"]: i for i in infos}

# Feed homepage: preserva i dati esistenti dove utili, ma riallinea ordine e immagini dai file reali.
home_feed_path = ROOT / "assets/data/home-feed-v210.json"
home_feed = json.loads(home_feed_path.read_text(encoding="utf-8"))
old_by_url = {i.get("url"): i for i in home_feed.get("items", [])}
feed_items = []
for info in infos:
    old = old_by_url.get(info["url"], {})
    merged = {k: v for k, v in info.items() if not k.startswith("_")}
    if old.get("excerpt") and info["url"] not in {"/" + x for x in TARGETS}:
        merged["excerpt"] = old["excerpt"]
    feed_items.append(merged)
home_feed["version"] = 323
home_feed["items"] = feed_items
home_feed_path.write_text(json.dumps(home_feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Indice di ricerca: notizie aggiornate davanti, contenuti non-news esistenti preservati.
search_path = ROOT / "assets/data/search-index-v210.json"
search = json.loads(search_path.read_text(encoding="utf-8"))
non_news = [i for i in search.get("items", []) if not str(i.get("url", "")).startswith("/notizie/")]
search_news = [{k: i[k] for k in ("title", "excerpt", "url", "section")} for i in feed_items]
search["version"] = 323
search["items"] = search_news + non_news
search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def picture(parent, item, eager=False):
    pic = etree.SubElement(parent, "picture")
    im = etree.SubElement(pic, "img")
    im.set("src", item["image"]); im.set("srcset", item["srcset"])
    im.set("sizes", "(max-width:600px) 79vw,300px")
    im.set("width", str(item.get("imageWidth", 800))); im.set("height", str(item.get("imageHeight", 533)))
    im.set("alt", item["imageAlt"]); im.set("loading", "eager" if eager else "lazy"); im.set("decoding", "async")
    if eager: im.set("fetchpriority", "high")


def make_featured(item):
    a = etree.Element("a", {"class": "featured", "href": item["url"]})
    picture(a, item, True)
    txt = etree.SubElement(a, "div", {"class": "txt"})
    tag = etree.SubElement(txt, "span", {"class": "tag"}); tag.text = "In evidenza"
    h1 = etree.SubElement(txt, "h1"); h1.text = item["title"]
    p = etree.SubElement(txt, "p"); p.text = item["excerpt"]
    cta = etree.SubElement(txt, "span", {"class": "cta"}); cta.text = "Leggi l’articolo →"
    return a


def make_rail(item):
    a = etree.Element("a", {"class": "auto-card", "href": item["url"]})
    picture(a, item)
    body = etree.SubElement(a, "div", {"class": "abody"})
    meta = etree.SubElement(body, "div", {"class": "ameta"}); meta.text = item["section"]
    h3 = etree.SubElement(body, "h3"); h3.text = item["title"]
    p = etree.SubElement(body, "p"); p.text = item["excerpt"]
    t = etree.SubElement(body, "time", {"datetime": item["dateISO"]}); t.text = italian_date(item["dateISO"])
    return a


def make_card(item):
    a = etree.Element("a", {"class": "card", "href": item["url"]})
    picture(a, item)
    body = etree.SubElement(a, "div", {"class": "body"})
    meta = etree.SubElement(body, "div", {"class": "meta"}); meta.text = item["section"]
    h3 = etree.SubElement(body, "h3"); h3.text = item["title"]
    p = etree.SubElement(body, "p"); p.text = item["excerpt"]
    t = etree.SubElement(body, "time", {"datetime": item["dateISO"]}); t.text = item["dateLabel"]
    return a

# Homepage: apertura + 5 ultime + 39 "Tutte" = top 45 articoli idonei, senza buchi cronologici.
home_path = ROOT / "index.html"
home_source = home_path.read_text(encoding="utf-8").replace("?v=322", "?v=323")
home = html.fromstring(home_source)
for track in home.xpath('//nav[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")][1] | //div[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]'):
    for child in list(track): track.remove(child)
    for n, item in enumerate(feed_items[:10]):
        attrs = {"class": "ticker-news", "href": item["url"]}
        if track.tag == "div" and n >= 6: attrs["tabindex"] = "-1"
        a = etree.SubElement(track, "a", attrs); a.text = item["title"]
featured = home.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
featured.getparent().replace(featured, make_featured(feed_items[0]))
rail = home.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
for child in list(rail): rail.remove(child)
for item in feed_items[1:6]: rail.append(make_rail(item))
cards = home.xpath('//div[@id="cards"]')[0]
for child in list(cards): cards.remove(child)
for item in feed_items[6:45]: cards.append(make_card(item))
cards.set("data-initial-count", str(min(39, max(0, len(feed_items)-6))))
home_path.write_text('<!doctype html>\n' + html.tostring(home, encoding="unicode", method="html"), encoding="utf-8")

# Archivio completo delle notizie idonee.
archive_path = ROOT / "notizie/index.html"
archive = html.fromstring(archive_path.read_text(encoding="utf-8"))
main = archive.xpath('//main')[0]
lead = main.xpath('./p[1]')
if lead:
    lead[0].text = f"{len(feed_items)} articoli verificati e promossi, ordinati per data."
ul = main.xpath('./ul')[0]
for child in list(ul): ul.remove(child)
for item in feed_items:
    li = etree.SubElement(ul, "li")
    a = etree.SubElement(li, "a", href=item["url"])
    strong = etree.SubElement(a, "strong"); strong.text = item["title"]
    span = etree.SubElement(a, "span"); span.text = item["dateLabel"]
archive_path.write_text('<!doctype html>\n' + html.tostring(archive, encoding="unicode", method="html"), encoding="utf-8")

# RSS: rigenera gli item news ordinati.
rss_path = ROOT / "feed.xml"
rss_tree = ET.parse(rss_path); rss_root = rss_tree.getroot(); channel = rss_root.find("channel")
for node in list(channel):
    if node.tag == "item": channel.remove(node)
for item in feed_items:
    node = ET.SubElement(channel, "item")
    ET.SubElement(node, "title").text = item["title"]
    full = "https://curiomondo.it" + item["url"]
    ET.SubElement(node, "link").text = full; ET.SubElement(node, "guid").text = full
    dt = datetime.fromisoformat(item["dateISO"].replace("Z", "+00:00"))
    ET.SubElement(node, "pubDate").text = format_datetime(dt)
    ET.SubElement(node, "description").text = item["excerpt"]
ET.indent(rss_tree, space="  "); rss_tree.write(rss_path, encoding="utf-8", xml_declaration=True)

# Google News sitemap: ultimi 2 giorni rispetto alla notizia più recente.
NEWS_NS = "http://www.google.com/schemas/sitemap-news/0.9"; SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", SM_NS); ET.register_namespace("news", NEWS_NS)
ns_tree = ET.ElementTree(ET.Element(f"{{{SM_NS}}}urlset")); ns_root = ns_tree.getroot()
latest_date = infos[0]["dateISO"][:10]
for info in infos:
    if info["dateISO"][:10] < "2026-09-09": continue
    u = ET.SubElement(ns_root, f"{{{SM_NS}}}url"); ET.SubElement(u, f"{{{SM_NS}}}loc").text = "https://curiomondo.it" + info["url"]
    news = ET.SubElement(u, f"{{{NEWS_NS}}}news"); pub = ET.SubElement(news, f"{{{NEWS_NS}}}publication")
    ET.SubElement(pub, f"{{{NEWS_NS}}}name").text = "CurioMondo"; ET.SubElement(pub, f"{{{NEWS_NS}}}language").text = "it"
    ET.SubElement(news, f"{{{NEWS_NS}}}publication_date").text = info["dateISO"]
    ET.SubElement(news, f"{{{NEWS_NS}}}title").text = info["title"]
ET.indent(ns_tree, space="  "); ns_tree.write(ROOT / "news-sitemap.xml", encoding="utf-8", xml_declaration=True)

# Sitemap generale: riallinea tutte le notizie pubbliche, senza eliminare pagine non-news.
sitemap_path = ROOT / "sitemap.xml"
sm_tree = ET.parse(sitemap_path); sm_root = sm_tree.getroot(); ns = {"sm": SM_NS}
new_urls = {"https://curiomondo.it" + i["url"] for i in feed_items}
for node in list(sm_root):
    loc = node.find(f"{{{SM_NS}}}loc")
    if loc is not None and loc.text in new_urls: sm_root.remove(node)
for item in reversed(feed_items):
    node = ET.Element(f"{{{SM_NS}}}url")
    ET.SubElement(node, f"{{{SM_NS}}}loc").text = "https://curiomondo.it" + item["url"]
    ET.SubElement(node, f"{{{SM_NS}}}lastmod").text = item["dateLabel"]
    sm_root.insert(0, node)
ET.indent(sm_tree, space="  "); sm_tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

# Cache busting dei JSON dinamici usati dalla homepage/articoli.
for rel in ("assets/js/home-v210.js", "assets/js/curiomondo-article-v210.js"):
    p = ROOT / rel
    if p.exists():
        p.write_text(p.read_text(encoding="utf-8").replace("?v=322", "?v=323"), encoding="utf-8")

print(json.dumps({"status":"ok","version":323,"new_articles":["/"+x for x in TARGETS],"homepage_top":[i["url"] for i in feed_items[:10]]}, ensure_ascii=False, indent=2))
