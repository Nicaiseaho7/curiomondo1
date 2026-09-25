#!/usr/bin/env python3
"""Verifica che una pubblicazione esista davvero online e nelle superfici."""
from __future__ import annotations
import argparse
import json
import sys
import time
import urllib.request

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

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--slug",required=True)
    parser.add_argument("--title",required=True)
    args=parser.parse_args()
    filename=args.slug+".html"
    status,article=fetch("/notizie/"+filename)
    errors=[]
    if status!=200: errors.append(f"articolo HTTP {status}")
    if args.title not in article: errors.append("titolo assente dalla pagina articolo")
    if 'content="noindex' in article.casefold(): errors.append("articolo marcato noindex")
    if 'data-editorial-status="revision-required"' in article: errors.append("articolo in revisione")
    for surface in ("/","/notizie/","/feed.xml","/sitemap.xml","/news-sitemap.xml"):
        try:
            code,body=fetch(surface)
        except UnicodeDecodeError as exc:
            errors.append(f"superficie {surface} non UTF-8: {exc}")
            continue
        # Netlify Pretty URLs può rimuovere ".html" dagli href nella risposta
        # pubblica, quindi la superficie si valida sullo slug canonico.
        if code!=200 or args.slug not in body:
            errors.append(f"articolo assente da {surface}")
    try:
        feed_status,feed_raw=fetch_bytes("/assets/data/home-feed-v210.json")
        feed=json.loads(feed_raw.decode("utf-8"))
        items=feed.get("items",[]) if isinstance(feed,dict) else []
        if feed_status!=200:
            errors.append(f"feed homepage HTTP {feed_status}")
        if not items:
            errors.append("feed homepage privo di articoli")
        elif not any(str(item.get("url","")).endswith("/"+filename) for item in items if isinstance(item,dict)):
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
    if errors:
        print({"live_publication":"fail","slug":args.slug,"errors":errors})
        return 1
    print({"live_publication":"pass","slug":args.slug})
    return 0

if __name__=="__main__":
    raise SystemExit(main())
