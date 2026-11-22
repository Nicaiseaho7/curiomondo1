#!/usr/bin/env python3
"""Integra Scadenze Italia nel menu e nei sistemi di indicizzazione CurioMondo."""
from __future__ import annotations
import argparse,re,sys
from pathlib import Path

MENU='\n<a class="mx-entry" href="/scadenze/"><em>05</em><strong>Scadenze Italia</strong><small>Bonus, fisco, concorsi e domande</small></a>'
REQUIRED=('scadenze/index.html','scadenze/archivio/index.html','assets/css/scadenze-v1.css','assets/js/scadenze-v1.js','assets/data/scadenze.json','sitemap-scadenze.xml','SCADENZE_URLS.txt')

def insert_menu(text):
    if 'href="/scadenze/"' in text:return text,False
    nav=re.search(r'(<nav\b[^>]*class="[^"]*\bmx-index\b[^"]*"[^>]*>)(.*?)(</nav>)',text,re.S)
    if not nav:return text,False
    concerts=list(re.finditer(r'<a\b[^>]*href="/concerti/"[^>]*>.*?</a>',nav.group(0),re.S))
    if concerts:
        pos=nav.start()+concerts[-1].end();return text[:pos]+MENU+text[pos:],True
    return text[:nav.start(3)]+MENU+'\n'+text[nav.start(3):],True

def sitemap_entries(urls):
    rows=[]
    for url in urls:
        priority='0.90' if url.endswith('/scadenze/') else '0.70'
        change='daily' if url.endswith('/scadenze/') else 'weekly'
        rows.append(f'  <url><loc>{url}</loc><lastmod>2026-11-22</lastmod><changefreq>{change}</changefreq><priority>{priority}</priority></url>')
    return '\n'.join(rows)+'\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='.');parser.add_argument('--dry-run',action='store_true');args=parser.parse_args();root=Path(args.root).resolve()
    missing=[p for p in REQUIRED if not(root/p).is_file()]
    if missing:print('ERRORE: mancano:\n  - '+'\n  - '.join(missing),file=sys.stderr);return 2
    changed=[]
    for path in root.rglob('*.html'):
        if any(part in {'.git','node_modules','scadenze'} for part in path.parts):continue
        text=path.read_text(encoding='utf-8');updated,did=insert_menu(text)
        if did:
            changed.append(path)
            if not args.dry_run:path.write_text(updated,encoding='utf-8')
    urls=(root/'SCADENZE_URLS.txt').read_text(encoding='utf-8').splitlines();sitemap=root/'sitemap.xml';sitemap_changed=False
    if sitemap.exists():
        text=sitemap.read_text(encoding='utf-8')
        if 'https://curiomondo.it/scadenze/' not in text:
            if '</urlset>' in text:updated=text.replace('</urlset>',sitemap_entries(urls)+'</urlset>',1)
            elif '</sitemapindex>' in text:updated=text.replace('</sitemapindex>','  <sitemap><loc>https://curiomondo.it/sitemap-scadenze.xml</loc><lastmod>2026-11-22</lastmod></sitemap>\n</sitemapindex>',1)
            else:raise RuntimeError('Formato sitemap.xml non riconosciuto')
            sitemap_changed=True
            if not args.dry_run:sitemap.write_text(updated,encoding='utf-8')
    robots=root/'robots.txt';robots_changed=False
    if robots.exists():
        text=robots.read_text(encoding='utf-8');line='Sitemap: https://curiomondo.it/sitemap-scadenze.xml'
        if line not in text:
            robots_changed=True
            if not args.dry_run:robots.write_text(text.rstrip()+'\n'+line+'\n',encoding='utf-8')
    mode='SIMULAZIONE' if args.dry_run else 'COMPLETATO'
    print(f'{mode}: menu aggiornati {len(changed)}; sitemap {"aggiornata" if sitemap_changed else "invariata o assente"}; robots {"aggiornato" if robots_changed else "invariato o assente"}.')
    print('Nessun URL esistente, manifest o redirect è stato modificato o rimosso.');return 0
if __name__=='__main__':raise SystemExit(main())
