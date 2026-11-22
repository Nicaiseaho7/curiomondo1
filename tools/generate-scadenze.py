#!/usr/bin/env python3
"""Genera le pagine statiche indicizzabili e la directory interna da scadenze.json."""
from __future__ import annotations
import html, json
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/data/scadenze.json'
INDEX=ROOT/'scadenze/index.html'

MONTHS=('gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre')
WEEKDAYS=('lunedì','martedì','mercoledì','giovedì','venerdì','sabato','domenica')
def e(value): return html.escape(str(value or ''),quote=True)
def date_label(value):
    d=datetime.fromisoformat(value); return f'{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month-1]} {d.year} alle {d:%H:%M}'
def item_date_label(item):
    d=datetime.fromisoformat(item['date'])
    return f'{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month-1]} {d.year}' if item.get('allDay') else date_label(item['date'])
def compact_date(value):
    d=datetime.fromisoformat(value); return f'{d.day} {MONTHS[d.month-1]} {d.year}'
def render(item,related):
    canonical=f"https://curiomondo.it/scadenze/{item['slug']}/"
    desc=item['summary'][:155]
    req=''.join(f'<li>{e(x)}</li>' for x in item['requirements'])
    rel=''.join(f'<a href="/scadenze/{e(x["slug"])}/">{e(x["shortTitle"])}</a>' for x in related)
    schema={"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":canonical,"url":canonical,"name":item['title'],"description":item['summary'],"dateModified":item['lastVerified'],"isPartOf":{"@type":"WebSite","name":"CurioMondo","url":"https://curiomondo.it/"},"about":{"@type":"Thing","name":item['shortTitle']}},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"CurioMondo","item":"https://curiomondo.it/"},{"@type":"ListItem","position":2,"name":"Scadenze Italia","item":"https://curiomondo.it/scadenze/"},{"@type":"ListItem","position":3,"name":item['shortTitle'],"item":canonical}]}
    ]}
    return f'''<!doctype html>
<html lang="it" data-page="scadenza-dettaglio"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{e(item['title'])} | Scadenze Italia</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="it_IT"><meta property="og:title" content="{e(item['title'])}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="/assets/css/editoriale-fonts-v1460.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=736"><link rel="stylesheet" href="/assets/css/scadenze-v1.css?v=1"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')}</script><script>try{{if(localStorage.getItem('cm_theme')==='dark')document.documentElement.classList.add('cm-dark')}}catch(e){{}}</script></head>
<body class="deadline-detail"><a class="skip-link" href="#main-content">Vai al contenuto</a><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/scadenze/" aria-label="Torna a Scadenze Italia"><span class="cm-global-header__back-icon" aria-hidden="true">←</span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>
<main id="main-content"><section class="detail-hero"><div class="shell"><nav class="breadcrumbs" aria-label="Percorso"><a href="/">Home</a><span>/</span><a href="/scadenze/">Scadenze</a><span>/</span><span aria-current="page">{e(item['shortTitle'])}</span></nav><span class="detail-badge">{e('Apertura' if item['dateType']=='apertura' else 'Scadenza')} · {e(item['category'])}</span><h1>{e(item['title'])}</h1><p class="detail-hero__summary">{e(item['summary'])}</p><div class="detail-date"><span><strong>Data:</strong> {e(item_date_label(item))}</span><span><strong>Destinatari:</strong> {e(item['audience'])}</span><span><strong>Territorio:</strong> {e(item['region'])}</span></div></div></section>
<div class="shell detail-layout"><article class="detail-content"><h2>Che cosa bisogna sapere</h2><p>{e(item['summary'])}</p>{f'<p><strong>Importo o beneficio:</strong> {e(item["amount"])}</p>' if item.get('amount') else ''}<h2>Come fare</h2><p>{e(item['how'])}</p><h2>Requisiti essenziali</h2><ul class="check-list">{req}</ul><h2>Controlla prima dell’invio</h2><p>Verifica sul portale ufficiale che requisiti, disponibilità delle risorse, documenti e modalità non siano cambiati. La pagina CurioMondo è uno strumento di orientamento e non sostituisce il bando o l’ente competente.</p><a class="official-button" href="{e(item['sourceUrl'])}" target="_blank" rel="noopener noreferrer">Apri la fonte ufficiale</a>{f'<div class="related-deadlines"><h2>Scadenze correlate</h2>{rel}</div>' if rel else ''}</article><aside class="detail-aside" aria-label="Riepilogo"><dl><div><dt>Data</dt><dd>{e(item_date_label(item))}</dd></div><div><dt>Categoria</dt><dd>{e(item['category'])}</dd></div><div><dt>Destinatari</dt><dd>{e(item['audience'])}</dd></div><div><dt>Stato</dt><dd>{e('Apertura programmata' if item['dateType']=='apertura' else 'Termine attivo')}</dd></div><div><dt>Fonte</dt><dd>{e(item['sourceName'])}</dd></div></dl><p class="verify-note">Ultima verifica effettiva: {e(date_label(item['lastVerified']))}, fuso Europe/Rome.</p></aside></div></main>
<footer class="site-footer"><div class="shell"><a class="footer-brand" href="/">Curio<span>Mondo</span></a><p>Notizie verificate, con le fonti in chiaro.</p><nav aria-label="Informazioni"><a href="/pagine/metodo-editoriale.html">Metodo editoriale</a><a href="/pagine/correzioni.html">Correzioni</a><a href="/pagine/privacy.html">Privacy</a></nav></div></footer><script defer src="/assets/js/global-header-v275.js"></script></body></html>'''

def main():
    payload=json.loads(DATA.read_text(encoding='utf-8')); items=payload['items']
    for item in items:
        related=[x for x in items if x['id']!=item['id'] and x['category']==item['category']][:3]
        folder=ROOT/'scadenze'/item['slug']; folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(render(item,related),encoding='utf-8')
    directory='<section class="static-directory" aria-labelledby="all-pages-title"><h2 id="all-pages-title">Tutte le schede</h2><div class="static-directory__links">'+''.join(f'<a href="/scadenze/{e(x["slug"])}/">{e(x["shortTitle"])} · {e(compact_date(x["date"]))}</a>' for x in sorted(items,key=lambda x:x['date']))+'</div></section>'
    text=INDEX.read_text(encoding='utf-8'); start='<!-- DEADLINE_STATIC_DIRECTORY_START -->'; end='<!-- DEADLINE_STATIC_DIRECTORY_END -->'; before,rest=text.split(start,1); _,after=rest.split(end,1); INDEX.write_text(before+start+'\n      '+directory+'\n      '+end+after,encoding='utf-8')
    urls=['https://curiomondo.it/scadenze/','https://curiomondo.it/scadenze/archivio/']+[f"https://curiomondo.it/scadenze/{x['slug']}/" for x in items]
    (ROOT/'SCADENZE_URLS.txt').write_text('\n'.join(urls)+'\n',encoding='utf-8')
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{e(url)}</loc><lastmod>2026-11-22</lastmod><changefreq>{"daily" if url.endswith("/scadenze/") else "weekly"}</changefreq><priority>{"0.90" if url.endswith("/scadenze/") else "0.70"}</priority></url>\n' for url in urls)+'</urlset>\n'
    (ROOT/'sitemap-scadenze.xml').write_text(sitemap,encoding='utf-8')
    print(f'Generate {len(items)} pagine statiche e {len(urls)} URL.')
if __name__=='__main__': main()
