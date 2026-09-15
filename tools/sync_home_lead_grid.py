#!/usr/bin/env python3
"""Sincronizza le tre card di categoria e rimuove i duplicati da Ultime notizie."""
from copy import deepcopy
from pathlib import Path
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def classes(node):
    return set((node.get("class") or "").split())


def text(node, xpath):
    value = node.xpath(xpath)
    if not value:
        return ""
    item = value[0]
    return " ".join(item.text_content().split()) if hasattr(item, "text_content") else str(item)


def is_film(item):
    haystack = " ".join((item["href"], item["title"], item["meta"])).lower()
    terms = ("cinema", "film", "serie", "streaming", "televis", "slow-horses", "netflix", "prime-video", "disney", "apple-tv", "hbo")
    return any(term in haystack for term in terms)


def to_item(node):
    time_nodes = node.xpath(".//time")
    image_nodes = node.xpath(".//img")
    return {
        "node": node,
        "href": node.get("href", ""),
        "title": text(node, ".//h3"),
        "meta": text(node, './/*[contains(concat(" ",normalize-space(@class)," ")," ameta ") or contains(concat(" ",normalize-space(@class)," ")," meta ")]'),
        "excerpt": text(node, ".//p"),
        "datetime": time_nodes[0].get("datetime", "") if time_nodes else "",
        "date_label": " ".join(time_nodes[0].text_content().split()) if time_nodes else "",
        "image": deepcopy(image_nodes[0]) if image_nodes else None,
    }


def set_card_mode(node, mode):
    node.set("class", "auto-card" if mode == "rail" else "card")
    bodies = node.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," abody ") or contains(concat(" ",normalize-space(@class)," ")," body ")]')
    if bodies:
        bodies[0].set("class", "abody" if mode == "rail" else "body")
        metas = bodies[0].xpath('./*[contains(concat(" ",normalize-space(@class)," ")," ameta ") or contains(concat(" ",normalize-space(@class)," ")," meta ")]')
        if metas:
            metas[0].set("class", "ameta" if mode == "rail" else "meta")


def side_card(item, label):
    link = html.Element("a", {"class": "cm-section-card", "href": item["href"], "aria-label": f"{label}: {item['title']}"})
    if item["image"] is not None:
        image = item["image"]
        image.set("loading", "lazy")
        image.set("decoding", "async")
        link.append(image)
    copy = html.Element("span", {"class": "cm-section-card-copy"})
    kicker = html.Element("span", {"class": "cm-section-card-kicker"})
    kicker.text = label
    title = html.Element("strong")
    title.text = item["title"]
    copy.extend((kicker, title))
    if item["date_label"]:
        stamp = html.Element("time", {"datetime": item["datetime"]})
        stamp.text = item["date_label"]
        copy.append(stamp)
    link.append(copy)
    return link


doc = html.parse(str(INDEX))
root = doc.getroot()
featured = root.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
featured_href = featured.xpath('.//a[contains(@class,"cta")]/@href')
if featured.tag != "a":
    href = featured_href[0]
    featured.tag = "a"
    featured.set("href", href)
    for cta in featured.xpath('.//a[contains(@class,"cta")]'):
        cta.tag = "span"
        cta.attrib.pop("href", None)
featured_href = featured.get("href", "")

rail = root.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
all_news = root.xpath('//div[@id="cards"]')[0]
items = [to_item(n) for n in rail.xpath('./a[@href]') + all_news.xpath('./a[@href]')]
items.sort(key=lambda item: (item["datetime"], item["href"]), reverse=True)

used = {featured_href}
chosen = []
rules = (
    ("Sport", lambda item: "sport" in item["meta"].lower()),
    ("Film e serie TV", is_film),
    ("Italia", lambda item: item["meta"].lower().startswith("italia") and "sport" not in item["meta"].lower() and not is_film(item)),
)
for label, predicate in rules:
    match = next((item for item in items if item["href"] not in used and predicate(item)), None)
    if match is None:
        raise SystemExit(f"Nessun articolo idoneo per la card {label}")
    chosen.append((label, match))
    used.add(match["href"])

side = root.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," cm-featured-side ")]')[0]
side[:] = [side_card(item, label) for label, item in chosen]

remaining = [item for item in items if item["href"] not in used]
rail_items = remaining[:5]
rail_urls = {item["href"] for item in rail_items}
archive_items = [item for item in items if item["href"] != featured_href and item["href"] not in rail_urls]
rail[:] = []
all_news[:] = []
for item in rail_items:
    node = item["node"]
    set_card_mode(node, "rail")
    rail.append(node)
for item in archive_items:
    node = item["node"]
    set_card_mode(node, "all")
    all_news.append(node)

INDEX.write_text('<!doctype html>\n' + html.tostring(root, encoding="unicode", method="html"), encoding="utf-8")
print({"side_cards": {label: item["href"] for label, item in chosen}, "latest_news": len(rail), "duplicates": 0})
