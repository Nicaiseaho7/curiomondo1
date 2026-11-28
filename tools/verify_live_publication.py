#!/usr/bin/env python3
"""Verifica che una pubblicazione esista davvero online e nelle superfici."""
from __future__ import annotations
import argparse
import json
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urljoin
from lxml import html
from sitemap_urls import read_news_sitemaps

BASE="https://curiomondo.it"

def fetch_bytes(path):
    separator="&" if "?" in path else "?"
    url=BASE+path+separator+"cm_live_verify="+str(time.time_ns())
    req=urllib.request.Request(url,headers={"User-Agent":"CurioMondo-Live-Validator/1.0",
                                           "Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=30) as response:
        return response.status,response.read()

def fetch(path):
    status,raw=fetch_bytes(path)
    return status,raw.decode("utf-8")

def live_news_urls() -> tuple[set[str], list[str]]:
    def download(path):
        status, content = fetch_bytes(path)
        if status != 200:
            raise OSError(f"HTTP {status}")
        return content
    try:
        robots = download("/robots.txt").decode("utf-8")
    except (OSError, UnicodeError) as exc:
        return set(), [f"robots.txt non verificabile: {exc}"]
    return read_news_sitemaps(robots, download)


def canonical_path(url: str) -> str:
    return urlparse(url).path.rstrip("/").removesuffix(".html")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--slug",required=True)
    parser.add_argument("--title",required=True)
    parser.add_argument("--section",choices=("notizie","approfondimenti"),default="notizie")
    args=parser.parse_args()
    filename=args.slug+".html"
    article_path="/"+args.section+"/"+filename
    evergreen=args.section=="approfondimenti"
    status,article=fetch(article_path)
    errors=[]
    if status!=200: errors.append(f"articolo HTTP {status}")
    if args.title not in article: errors.append("titolo assente dalla pagina articolo")
    if 'content="noindex' in article.casefold(): errors.append("articolo marcato noindex")
    if 'data-editorial-status="revision-required"' in article: errors.append("articolo in revisione")
    # La News Sitemap contiene solo le prime pubblicazioni delle ultime 48 ore.
    # Un aggiornamento non rinnova datePublished e resta nella sitemap generale.
    article_doc=html.fromstring(article)
    published=None
    for raw in article_doc.xpath('//script[@type="application/ld+json"]/text()'):
        try:
            data=json.loads(raw)
            for item in data if isinstance(data,list) else [data]:
                if isinstance(item,dict) and item.get('@type')=='NewsArticle':
                    published=datetime.fromisoformat(item['datePublished'].replace('Z','+00:00'))
        except (ValueError,KeyError,TypeError):
            continue
    if not evergreen and (published is None or published.tzinfo is None):
        errors.append("data di prima pubblicazione assente o non valida")
    surfaces=("/","/approfondimenti/","/sitemap.xml","/assets/data/search-index-v210.json") if evergreen else ("/","/notizie/","/feed.xml","/sitemap.xml")
    for surface in surfaces:
        try:
            code,body=fetch(surface)
        except UnicodeDecodeError as exc:
            errors.append(f"superficie {surface} non UTF-8: {exc}")
            continue
        # Netlify Pretty URLs può rimuovere ".html" dagli href nella risposta
        # pubblica, quindi la superficie si valida sullo slug canonico.
        if code!=200 or args.slug not in body:
            errors.append(f"articolo assente da {surface}")
        if surface.endswith(".json"):
            try:
                json.loads(body)
            except json.JSONDecodeError as exc:
                errors.append(f"indice ricerca non decodificabile: {exc}")
    listed, news_errors = live_news_urls()
    errors.extend(news_errors)
    in_news = canonical_path(article_path) in {canonical_path(url) for url in listed}
    moment = datetime.now(timezone.utc)
    recent = published is not None and published.tzinfo is not None and moment - timedelta(hours=48) <= published <= moment
    if not evergreen and recent and not in_news:
        errors.append("notizia recente assente dalla News Sitemap")
    if evergreen and in_news:
        errors.append("approfondimento nella News Sitemap")
    try:
        feed_status,feed_raw=fetch_bytes("/assets/data/home-feed-v210.json")
        feed=json.loads(feed_raw.decode("utf-8"))
        items=feed.get("items",[]) if isinstance(feed,dict) else []
        if feed_status!=200:
            errors.append(f"feed homepage HTTP {feed_status}")
        if not items:
            errors.append("feed homepage privo di articoli")
        elif evergreen and any(str(item.get("url","")).endswith("/"+filename) for item in items if isinstance(item,dict)):
            errors.append("approfondimento inserito nel feed breaking")
        elif not evergreen and not any(str(item.get("url","")).endswith("/"+filename) for item in items if isinstance(item,dict)):
            errors.append("articolo assente dal feed homepage")
    except (UnicodeDecodeError,json.JSONDecodeError) as exc:
        errors.append(f"feed homepage non decodificabile: {exc}")
    try:
        _,homepage=fetch("/")
        for asset in ("home-allocation-v504.js","home-sections-v504.js","home-sections-v504.css"):
            if asset not in homepage:
                errors.append(f"asset layout homepage assente: {asset}")
    except UnicodeDecodeError as exc:
        errors.append(f"homepage non UTF-8: {exc}")
    if evergreen:
        doc=html.fromstring(article)
        if BASE+article_path not in doc.xpath('//link[@rel="canonical"]/@href'):
            errors.append("canonical approfondimento non coerente")
        hero=doc.xpath('//figure[contains(@class,"article-image")]//img[1]')
        if not hero:
            errors.append("immagine hero assente")
        else:
            paths={hero[0].get("src","")}
            paths.update(part.strip().split()[0] for part in hero[0].get("srcset","").split(",") if part.strip())
            for image in sorted(paths):
                path=urlparse(urljoin(BASE+article_path,image)).path
                code,data=fetch_bytes(path)
                if code!=200 or data[:4]!=b"RIFF" or data[8:12]!=b"WEBP":
                    errors.append(f"immagine WebP non valida: {path}")
        code, body = fetch("/feed.xml")
        if code != 200 or args.slug in body:
            errors.append("approfondimento nel feed RSS o feed non disponibile")
    if errors:
        print({"live_publication":"fail","slug":args.slug,"errors":errors})
        return 1
    print({"live_publication":"pass","slug":args.slug})
    return 0

if __name__=="__main__":
    raise SystemExit(main())
