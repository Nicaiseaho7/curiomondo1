#!/usr/bin/env python3
"""Avvisa i motori che il feed e le notizie nuove sono online.

Va eseguito solo dopo il deploy: il hub e IndexNow leggono gli URL dal sito
già pubblicato. Non garantisce l'indicizzazione. Google non accetta IndexNow
e la sua Indexing API non vale per le notizie.
"""
from __future__ import annotations

import json
import sys
import time
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


def _status(url: str, method: str = "GET", data: bytes | None = None, headers: dict[str, str] | None = None) -> int:
    request = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
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


def wait_until_live(urls: list[str]) -> bool:
    """Aspetta il deploy Netlify. IndexNow non va chiamato su pagine ancora assenti."""
    article = next((url for url in urls if "/notizie/" in url), "")
    targets = [f"https://{HOST}/{KEY}.txt"]
    if article:
        targets.append(article)
    for _ in range(24):
        if all(_status(url) == 200 for url in targets):
            return True
        time.sleep(10)
    return False


def main() -> int:
    key_path = ROOT / f"{KEY}.txt"
    if key_path.read_text(encoding="utf-8").strip() != KEY:
        print("chiave IndexNow assente o diversa dal file pubblico")
        return 1
    urls = news_urls()
    if "--wait" in sys.argv and not wait_until_live(urls):
        print(json.dumps({"wait": "timeout", "urls": len(urls)}, ensure_ascii=False))
        return 1
    hub_status = _status(
        HUB,
        method="POST",
        data=urllib.parse.urlencode({"hub.mode": "publish", "hub.url": FEED}).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    index_status = _status(
        INDEXNOW,
        method="POST",
        data=json.dumps({
            "host": HOST,
            "key": KEY,
            "keyLocation": f"https://{HOST}/{KEY}.txt",
            "urlList": urls,
        }).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    print(json.dumps({
        "websub": hub_status,
        "indexnow": index_status,
        "urls": len(urls),
    }, ensure_ascii=False))
    return 0 if hub_status in (200, 202, 204) or index_status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main())
