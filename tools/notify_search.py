#!/usr/bin/env python3
"""Avvisa i motori che il feed e le notizie nuove sono online.

Va eseguito solo dopo il deploy: il hub e IndexNow leggono gli URL dal sito
già pubblicato. Non garantisce l'indicizzazione. Google non accetta IndexNow
e la sua Indexing API non vale per le notizie.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "curiomondo.it"
KEY = "b273bc86ad8ad90ba1e5e563b54a7813"
FEED = f"https://{HOST}/feed.xml"
HUB = "https://pubsubhubbub.appspot.com/"
INDEXNOW = "https://api.indexnow.org/indexnow"
NEWS_NS = "http://www.google.com/schemas/sitemap-news/0.9"
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def _post(url: str, data: bytes, headers: dict[str, str]) -> int:
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code


def news_urls() -> list[str]:
    root = ET.parse(ROOT / "news-sitemap.xml").getroot()
    urls = [node.text.strip() for node in root.findall(f".//{{{SM_NS}}}loc") if node.text]
    home = f"https://{HOST}/"
    if home not in urls:
        urls.insert(0, home)
    return urls[:10000]


def main() -> int:
    key_path = ROOT / f"{KEY}.txt"
    if key_path.read_text(encoding="utf-8").strip() != KEY:
        print("chiave IndexNow assente o diversa dal file pubblico")
        return 1
    hub_body = urllib.parse.urlencode({"hub.mode": "publish", "hub.url": FEED}).encode()
    hub_status = _post(HUB, hub_body, {"Content-Type": "application/x-www-form-urlencoded"})
    urls = news_urls()
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }).encode()
    index_status = _post(INDEXNOW, payload, {"Content-Type": "application/json; charset=utf-8"})
    print(json.dumps({
        "websub": hub_status,
        "indexnow": index_status,
        "urls": len(urls),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
