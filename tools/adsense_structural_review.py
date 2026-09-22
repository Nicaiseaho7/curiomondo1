#!/usr/bin/env python3
"""Audit e quarantena editoriale per la candidatura AdSense di CurioMondo."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from lxml import etree, html

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
WORD_RE=re.compile(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b")
CAPTION="Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

def words(node):
    return len(WORD_RE.findall(" ".join(node.itertext())))

def inspect(path):
    doc=html.fromstring(path.read_text(encoding="utf-8",errors="replace"))
    robots=" ".join(doc.xpath('//meta[@name="robots"]/@content')).casefold()
    bodies=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')
    body=bodies[0] if bodies else None
    return {"path":path.relative_to(ROOT).as_posix(),"url":f"/notizie/{path.name}",
            "indexed":"noindex" not in robots,"words":words(body) if body is not None else 0,
            "format":body.get("data-article-format","") if body is not None else "",
            "sources":len(doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]//a[@href]')),
            "paragraphs":len(body.xpath(".//p")) if body is not None else 0}

def quarantine(path):
    doc=html.fromstring(path.read_text(encoding="utf-8",errors="replace"))
    metas=doc.xpath('//meta[@name="robots"]')
    if metas: metas[0].set("content","noindex,follow,noarchive")
    else: doc.xpath("//head")[0].insert(0,etree.Element("meta",name="robots",content="noindex,follow,noarchive"))
    for script in doc.xpath('//script[contains(@src,"pagead2.googlesyndication.com")]'):
        script.getparent().remove(script)
    for body in doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]'):
        body.set("data-editorial-status","revision-required")
    for caption in doc.xpath('//main/figure[1]/figcaption'): caption.text=CAPTION
    paths=doc.xpath('//header[@data-cm-global-header="v275"]//a[contains(@class,"cm-global-header__back")]//path')
    if len(paths)>=2:
        paths[0].set("d","M19 12H5"); paths[1].set("d","m11 18-6-6 6-6")
    else:
        backs=doc.xpath('//header[@data-cm-global-header="v275"]//a[contains(@class,"cm-global-header__back")]')
        if backs:
            back=backs[0]; back.text=None
            for child in list(back): back.remove(child)
            span=etree.SubElement(back,"span",{"class":"cm-global-header__back-icon","aria-hidden":"true"})
            svg=etree.SubElement(span,"svg",viewBox="0 0 24 24")
            etree.SubElement(svg,"path",d="M19 12H5"); etree.SubElement(svg,"path",d="m11 18-6-6 6-6")
    path.write_text("<!doctype html>\n"+html.tostring(doc,encoding="unicode",method="html"),encoding="utf-8")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--threshold",type=int,default=300)
    parser.add_argument("--version",type=int)
    args=parser.parse_args()
    version=args.version
    if version is None:
        manifest=json.loads((ROOT/"curiomondo-site-manifest.json").read_text(encoding="utf-8"))
        site=manifest.get("site",{})
        version=int(manifest.get("site_version") or manifest.get("version") or
                    site.get("site_version") or site.get("current_site_version") or 0)
    rows=[inspect(p) for p in sorted((ROOT/"notizie").glob("*.html")) if p.name!="index.html"]
    weak=[r for r in rows if r["indexed"] and r["words"]<args.threshold]
    report={"policy":"indexed news below 300 words require substantive revision",
            "total_news":len(rows),"indexed_before":sum(r["indexed"] for r in rows),
            "quarantine_candidates":len(weak),"threshold_words":args.threshold,"items":weak}
    if args.apply:
        for row in weak: quarantine(ROOT/row["path"])
        for row in rows:
            page=ROOT/row["path"]
            if 'data-editorial-status="revision-required"' in page.read_text(encoding="utf-8",errors="replace"):
                quarantine(page)
        from automation.newsroom.site import sync_surfaces
        sync_surfaces([],"",version)
        report["applied"]=True; report["indexed_after"]=report["indexed_before"]-len(weak)
    out=ROOT/"reports"/"adsense-structural-review.json"; out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
