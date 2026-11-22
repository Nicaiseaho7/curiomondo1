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
    kind='apertura' if item['dateType']=='apertura' else 'scadenza'
    kind_label='Data di apertura' if kind=='apertura' else 'Data di scadenza'
    amount=f'<p><strong>Importo o beneficio:</strong> {e(item["amount"])}</p>' if item.get('amount') else ''
    related_html=f'<div class="related-deadlines"><h2>Altre date</h2>{rel}</div>' if rel else ''
    linked=item.get('articles') or ([item['article']] if item.get('article') else [])
    news_html=''
    if linked:
        cards=[]
        for story in linked:
            image=story.get('image') or ''
            thumb=f'<img src="{e(image)}" alt="">' if image else ''
            cards.append(f'<a href="{e(story.get("url"))}"><span class="related-thumb">{thumb}</span><span class="related-copy"><strong>{e(story.get("title"))}</strong></span></a>')
        news_html='<h2>Notizie correlate</h2><div class="related-news">'+''.join(cards)+'</div>'
    schema={"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":canonical,"url":canonical,"name":item['title'],"description":item['summary'],"dateModified":item['lastVerified'],"isPartOf":{"@type":"WebSite","name":"CurioMondo","url":"https://curiomondo.it/"},"about":{"@type":"Thing","name":item['shortTitle']}},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"CurioMondo","item":"https://curiomondo.it/"},{"@type":"ListItem","position":2,"name":"Calendario del cittadino","item":"https://curiomondo.it/scadenze/"},{"@type":"ListItem","position":3,"name":item['shortTitle'],"item":canonical}]}
    ]}
    schema_json=json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="it" data-page="scadenza-dettaglio"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{e(item['title'])} | Calendario del cittadino</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="it_IT"><meta property="og:title" content="{e(item['title'])}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><link rel="stylesheet" href="/assets/css/editoriale-fonts-v1460.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=736"><link rel="stylesheet" href="/assets/css/scadenze-v1.css?v=10"><script type="application/ld+json">{schema_json}</script><script>try{{if(localStorage.getItem('cm_theme')==='dark')document.documentElement.classList.add('cm-dark')}}catch(e){{}}</script></head>
<body class="deadline-detail"><a class="skip-link" href="#main-content">Vai al contenuto</a><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/scadenze/" aria-label="Torna al calendario"><span class="cm-global-header__back-icon" aria-hidden="true">←</span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>
<main id="main-content"><section class="detail-hero"><div class="shell"><nav class="breadcrumbs" aria-label="Percorso"><a href="/">Home</a><span>/</span><a href="/scadenze/">Calendario</a><span>/</span><span aria-current="page">{e(item['shortTitle'])}</span></nav><span class="detail-badge kind-{kind}">{e(kind_label)}</span><h1>{e(item['title'])}</h1><p class="detail-hero__summary">{e(item['summary'])}</p><div class="detail-date"><span><strong>Data:</strong> {e(item_date_label(item))}</span><span><strong>Destinatari:</strong> {e(item['audience'])}</span><span><strong>Territorio:</strong> {e(item['region'])}</span></div></div></section>
<div class="shell detail-layout"><article class="detail-content">{amount}<h2>Come fare</h2><p>{e(item['how'])}</p><h2>Requisiti essenziali</h2><ul class="check-list">{req}</ul>{news_html}<a class="official-button" href="{e(item['sourceUrl'])}" target="_blank" rel="noopener noreferrer">Pagina ufficiale</a>{related_html}</article><aside class="detail-aside" aria-label="Riepilogo"><dl><div><dt>Tipo</dt><dd>{e(kind_label)}</dd></div><div><dt>Fonte</dt><dd>{e(item['sourceName'])}</dd></div></dl><p class="verify-note">Ultima verifica: {e(date_label(item['lastVerified']))}.</p></aside></div></main>
<footer class="site-footer"><div class="shell"><a class="footer-brand" href="/">Curio<span>Mondo</span></a><p>Notizie verificate, con le fonti in chiaro.</p><nav aria-label="Informazioni"><a href="/pagine/metodo-editoriale.html">Metodo editoriale</a><a href="/pagine/correzioni.html">Correzioni</a><a href="/pagine/privacy.html">Privacy</a></nav></div></footer><script defer src="/assets/js/global-header-v275.js"></script></body></html>'''

def main():
    payload=json.loads(DATA.read_text(encoding='utf-8')); items=payload['items']
    visible=[x for x in items if not (x.get('dateType')=='apertura' and x.get('status')=='in-arrivo')]
    for item in items:
        related=[x for x in visible if x['id']!=item['id'] and x['category']==item['category']][:3]
        folder=ROOT/'scadenze'/item['slug']; folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(render(item,related),encoding='utf-8')
    directory='<section class="static-directory" aria-labelledby="all-pages-title"><h2 id="all-pages-title">Tutte le schede</h2><div class="static-directory__links">'+''.join(f'<a href="/scadenze/{e(x["slug"])}/">{e(x["shortTitle"])} · {e(compact_date(x["date"]))}</a>' for x in sorted(visible,key=lambda x:x['date']))+'</div></section>'
    text=INDEX.read_text(encoding='utf-8'); start='<!-- DEADLINE_STATIC_DIRECTORY_START -->'; end='<!-- DEADLINE_STATIC_DIRECTORY_END -->'; before,rest=text.split(start,1); _,after=rest.split(end,1); INDEX.write_text(before+start+'\n      '+directory+'\n      '+end+after,encoding='utf-8')
    urls=['https://curiomondo.it/scadenze/','https://curiomondo.it/scadenze/archivio/']+[f"https://curiomondo.it/scadenze/{x['slug']}/" for x in items]
    (ROOT/'SCADENZE_URLS.txt').write_text('\n'.join(urls)+'\n',encoding='utf-8')
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{e(url)}</loc><lastmod>2026-11-22</lastmod><changefreq>{"daily" if url.endswith("/scadenze/") else "weekly"}</changefreq><priority>{"0.90" if url.endswith("/scadenze/") else "0.70"}</priority></url>\n' for url in urls)+'</urlset>\n'
    (ROOT/'sitemap-scadenze.xml').write_text(sitemap,encoding='utf-8')
    print(f'Generate {len(items)} pagine statiche e {len(urls)} URL.')
if __name__=='__main__': main()
