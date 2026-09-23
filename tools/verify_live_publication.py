#!/usr/bin/env python3
"""Verifica che una pubblicazione esista davvero online e nelle superfici."""
from __future__ import annotations
import argparse
import sys
import urllib.request

BASE="https://curiomondo.it"

def fetch(path):
    req=urllib.request.Request(BASE+path,headers={"User-Agent":"CurioMondo-Live-Validator/1.0"})
    with urllib.request.urlopen(req,timeout=30) as response:
        return response.status,response.read().decode("utf-8","replace")

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
        code,body=fetch(surface)
        if code!=200 or filename not in body:
            errors.append(f"articolo assente da {surface}")
    if errors:
        print({"live_publication":"fail","slug":args.slug,"errors":errors})
        return 1
    print({"live_publication":"pass","slug":args.slug})
    return 0

if __name__=="__main__":
    raise SystemExit(main())
