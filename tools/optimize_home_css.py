#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT = ROOT / "assets/css/home-bundle-v291.css"

CSS_FILES = [
    "assets/css/site-base-v210.css",
    "assets/css/home-v211.css",
    "assets/css/design-restored-v212.css",
    "assets/css/home-premium-v213.css",
    "assets/css/home-premium-v214.css",
    "assets/css/home-premium-v215.css",
    "assets/css/home-premium-v216.css",
    "assets/css/home-premium-v217.css",
    "assets/css/home-premium-v218.css",
    "assets/css/home-premium-v221.css",
    "assets/css/home-premium-v222.css",
    "assets/css/home-premium-v223.css",
    "assets/css/home-premium-v224.css",
    "assets/css/home-premium-v225.css",
    "assets/css/home-premium-v226.css",
    "assets/css/home-drawer-v227.css",
    "assets/css/home-live-v229.css",
    "assets/css/home-brand-universe-v239.css",
    "assets/css/home-universe-centered-v240.css",
    "assets/css/home-adsense-v263.css",
    "assets/css/home-editorial-signature-v268.css",
    "assets/css/home-qday-luxury-v271.css",
    "assets/css/home-azure-v274.css",
]

missing = [p for p in CSS_FILES if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("CSS mancanti: " + ", ".join(missing))

parts = [
    "/* CurioMondo homepage CSS bundle v291.\n"
    "   Generato preservando rigorosamente l'ordine dei fogli originali. */\n"
]
for rel in CSS_FILES:
    text = (ROOT / rel).read_text(encoding="utf-8-sig")
    text = re.sub(r"^\s*@charset\s+[^;]+;\s*", "", text, flags=re.I)
    parts.append(f"\n/* source: {rel} */\n{text.rstrip()}\n")
OUT.write_text("".join(parts), encoding="utf-8")

html = INDEX.read_text(encoding="utf-8")
head_end = html.find("</head>")
if head_end < 0:
    raise SystemExit("index.html senza </head>")
head = html[:head_end]
tail = html[head_end:]

# Individua solo i fogli CSS locali della homepage, qualunque sia l'ordine degli attributi.
link_re = re.compile(r"<link\b(?=[^>]*\brel=[\"']stylesheet[\"'])(?=[^>]*\bhref=[\"']/assets/css/[^\"']+\.css(?:\?[^\"']*)?[\"'])[^>]*>\s*", re.I)
matches = list(link_re.finditer(head))
if len(matches) < 20:
    raise SystemExit(f"Attesi almeno 20 stylesheet locali in homepage, trovati {len(matches)}")

first = matches[0].start()
new_head = link_re.sub("", head)
bundle_tag = '<link rel="stylesheet" href="/assets/css/home-bundle-v291.css?v=291">\n'
new_head = new_head[:first] + bundle_tag + new_head[first:]
INDEX.write_text(new_head + tail, encoding="utf-8")

# Controlli minimi di sicurezza: deve restare un solo stylesheet locale, il bundle.
updated = INDEX.read_text(encoding="utf-8")
updated_head = updated[:updated.find("</head>")]
local_styles = link_re.findall(updated_head)
if len(local_styles) != 1 or "home-bundle-v291.css" not in local_styles[0]:
    raise SystemExit(f"Configurazione stylesheet homepage non valida: {local_styles}")
if updated.count("home-bundle-v291.css") != 1:
    raise SystemExit("Bundle CSS non collegato esattamente una volta")

print({
    "status": "ok",
    "css_sources": len(CSS_FILES),
    "bundle": str(OUT.relative_to(ROOT)),
    "bundle_bytes": OUT.stat().st_size,
    "homepage_stylesheet_requests": 1,
})
