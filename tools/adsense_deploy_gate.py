#!/usr/bin/env python3
"""Gate fail-closed eseguito da Netlify dopo la revisione strutturale."""
from pathlib import Path
from lxml import html
import re, sys
from editorial_rules import format_errors, source_errors

ROOT=Path(__file__).resolve().parents[1]
WORD_RE=re.compile(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b")
errors=[]
quarantined=[]

for path in sorted((ROOT/"notizie").glob("*.html")):
    if path.name=="index.html":
        continue
    try:
        doc=html.fromstring(path.read_text(encoding="utf-8",errors="replace"))
    except Exception as exc:
        errors.append(f"HTML non valido {path.name}: {exc}")
        continue
    robots=" ".join(doc.xpath('//meta[@name="robots"]/@content')).casefold()
    bodies=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')
    count=len(WORD_RE.findall(" ".join(bodies[0].itertext()))) if bodies else 0
    article_format=(bodies[0].get("data-article-format","") if bodies else "").strip().casefold()
    if "noindex" in robots:
        quarantined.append(path.name)
        if doc.xpath('//script[contains(@src,"pagead2.googlesyndication.com")]'):
            errors.append(f"pubblicita presente sulla pagina in revisione: {path.name}")
    else:
        errors.extend(f"{message}: {path.name}" for message in format_errors(bodies[0] if bodies else None))
        errors.extend(f"{message}: {path.name}" for message in source_errors(doc, bodies[0] if bodies else None))
        if not doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," cm-article-byline ")] | //a[@href="/pagine/redazione.html"]'):
            errors.append(f"responsabilita editoriale assente: {path.name}")

surfaces="\n".join((ROOT/p).read_text(encoding="utf-8",errors="replace") for p in
                   ("index.html","feed.xml","sitemap.xml","news-sitemap.xml"))
for name in quarantined:
    if name in surfaces:
        errors.append(f"pagina in revisione ancora promossa: {name}")

print({"indexed_quality_gate":"pass" if not errors else "fail",
       "quarantined":len(quarantined),"errors":errors})
raise SystemExit(1 if errors else 0)
