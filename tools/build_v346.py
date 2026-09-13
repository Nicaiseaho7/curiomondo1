#!/usr/bin/env python3
from pathlib import Path
from html import escape
from PIL import Image
import json, runpy

ROOT=Path(__file__).resolve().parents[1]; VERSION=346
SLUG="zaporizhzhia-dieci-attacchi-droni-centro-addestramento-13-settembre-2026"
TITLE="Zaporizhzhia, la gestione russa denuncia oltre dieci attacchi con droni"
EXCERPT="La direzione dell’impianto accusa le forze ucraine di avere colpito ripetutamente l’area del centro di addestramento. L’attribuzione non è verificata in modo indipendente."
KEY="zaporizhzhia-centro-addestramento-droni-ai-openai-v346"
SRC=ROOT.parent/'generated_images'/'exec-fd7b5bc6-360a-4765-8162-ab5f9493926a.png'
CAP="Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
CAN=f"https://curiomondo.it/notizie/{SLUG}.html"; IMG=f"https://curiomondo.it/assets/images/editorial-auto/{KEY}-1200.webp"
body=[
"La direzione russa della centrale nucleare di Zaporizhzhia ha affermato che, dalla sera del 12 settembre, più di dieci attacchi con droni avrebbero interessato l’area del centro di addestramento del personale. La struttura si trova presso il complesso nucleare ucraino, occupato dalle forze russe e amministrato da operatori legati a Rosatom.",
"L’informazione proviene dalla gestione installata da Mosca. Al momento della pubblicazione non risultano una conferma indipendente dell’attribuzione a Kiev né una rivendicazione ucraina. Per questo non è corretto presentare come accertato che i velivoli appartenessero alle forze ucraine: si tratta di un’accusa russa in fase di verifica.",
"Secondo la comunicazione dell’impianto, non sarebbero emerse vittime nelle prime verifiche. L’entità degli eventuali danni non è stata ancora definita, perché la minaccia di nuovi attacchi avrebbe impedito ai tecnici di completare l’ispezione dell’area.",
"Il centro di addestramento non coincide con gli edifici dei reattori, ma gli episodi militari dentro o vicino al perimetro della centrale restano rilevanti per la sicurezza. L’Agenzia internazionale per l’energia atomica mantiene osservatori sul posto e ha ripetutamente chiesto di evitare attività militari attorno agli impianti nucleari.",
"La centrale di Zaporizhzhia, la più grande d’Europa, è in territorio ucraino ma sotto controllo russo dal 2022. I sei reattori non producono elettricità, tuttavia sistemi di raffreddamento, alimentazione esterna e generatori di emergenza devono continuare a funzionare per garantire la sicurezza del combustibile nucleare."
]
sources=[
("https://bloknot-zaporozhie.ru/news/vsu-bolee-desyati-raz-atakovali-uchebnyy-tsentr-za-2009118","Direzione della centrale di Zaporizhzhia — dichiarazione riportata il 13 settembre 2026"),
("https://www.reuters.com/business/energy/russian-nuclear-head-says-ukraine-attacked-fuel-trucks-endangered-zaporizhzhia-2026-09-13/","Reuters — 13 settembre 2026 — contesto sulla sicurezza della centrale e sulle accuse russe"),
("https://www.iaea.org/newscenter/focus/ukraine","AIEA — aggiornamenti ufficiali sulla sicurezza nucleare in Ucraina")]
schema={"@context":"https://schema.org","@type":"NewsArticle","headline":TITLE,"description":EXCERPT,"datePublished":"2026-09-13T15:30:00+02:00","dateModified":"2026-09-13T15:30:00+02:00","mainEntityOfPage":CAN,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo"},"publisher":{"@type":"Organization","name":"CurioMondo"},"image":[IMG]}
ps=''.join(f'<p>{escape(x)}</p>' for x in body); ss=''.join(f'<li><a href="{escape(u,quote=True)}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in sources)
stats='<div><strong>Oltre 10</strong><span>attacchi denunciati</span></div><div><strong>0</strong><span>vittime riferite finora</span></div><div><strong>6</strong><span>reattori nell’impianto</span></div>'
html=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT,quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{CAN}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE,quote=True)}"><meta property="og:description" content="{escape(EXCERPT,quote=True)}"><meta property="og:url" content="{CAN}"><meta property="og:image" content="{IMG}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=346"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{SLUG}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner"><a class="cm-global-header__back" href="/" aria-label="Torna alla home"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a></nav></header><main class="wrap"><div class="badge">Mondo / Ucraina / Sicurezza nucleare</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">13 settembre 2026 · Zaporizhzhia · <span id="readTime">3 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html">Redazione CurioMondo</a></p><figure class="article-image" data-ai-generated="true" data-sensitive-context="false"><picture><img src="../assets/images/editorial-auto/{KEY}-800.webp" srcset="../assets/images/editorial-auto/{KEY}-480.webp 480w, ../assets/images/editorial-auto/{KEY}-800.webp 800w, ../assets/images/editorial-auto/{KEY}-1200.webp 1200w" width="800" height="533" alt="Illustrazione editoriale della centrale di Zaporizhzhia e di droni nei pressi del centro di addestramento"></picture><figcaption>{CAP}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{stats}</div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="flash">{ps}</article><section class="curio-related"><h2>Potrebbe interessarti anche…</h2><div class="curio-related-grid"><a href="/notizie/russia-attacco-confine-polonia-yahodyn-dorohusk-13-settembre-2026.html"><strong>Attacco vicino al confine polacco</strong></a><a href="/notizie/odesa-attacco-russo-droni-cinque-feriti-13-settembre-2026.html"><strong>Nuovi raid russi su Odesa</strong></a><a href="/notizie/energia-attacchi-rotte-petrolio-pipeline-est-ovest-13-settembre-2026.html"><strong>Energia e rotte globali</strong></a></div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{ss}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 13 settembre 2026.<br>{CAP}</small></p></div></main><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=346" defer></script></body></html>'''

im=Image.open(SRC).convert('RGB'); w,h=im.size
if w/h>1.5:
 nw=round(h*1.5); im=im.crop(((w-nw)//2,0,(w+nw)//2,h))
out=ROOT/'assets/images/editorial-auto'
for x in (480,800,1200): im.resize((x,round(x*2/3)),Image.Resampling.LANCZOS).save(out/f'{KEY}-{x}.webp','WEBP',quality=86,method=6)
(ROOT/'notizie'/f'{SLUG}.html').write_text(html,encoding='utf-8')
regp=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(regp.read_text())
reg['items']=[i for i in reg['items'] if i.get('article')!=f'/notizie/{SLUG}.html']
reg['items'].insert(0,{'key':KEY,'article':f'/notizie/{SLUG}.html','aiGenerated':True,'documentaryPhoto':False,'variants':[{'w':x,'src':f'/assets/images/editorial-auto/{KEY}-{x}.webp'} for x in (480,800,1200)],'alt':'Illustrazione editoriale della centrale di Zaporizhzhia e di droni nei pressi del centro di addestramento','disclosure':CAP}); reg['version']=VERSION; regp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
homep=ROOT/'assets/data/home-feed-v210.json'; home=json.loads(homep.read_text())
url=f'/notizie/{SLUG}.html'; home['items']=[i for i in home.get('items',[]) if i.get('url')!=url]
home['items'].insert(0,{'url':url,'featuredHighlights':['gestione russa','oltre dieci attacchi'],'featuredStats':[{'icon':'◆','value':'Oltre 10','label':'attacchi denunciati dalla gestione russa'},{'icon':'●','value':'0','label':'vittime riferite nelle prime verifiche'},{'icon':'⬡','value':'6','label':'reattori presenti nell’impianto'}]})
homep.write_text(json.dumps(home,ensure_ascii=False,indent=2)+'\n')
runpy.run_path(str(ROOT/'tools/finalize_articles_20260906.py'),run_name='__main__'); runpy.run_path(str(ROOT/'tools/generate_category_pages.py'),run_name='__main__')
for rel in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
 p=ROOT/rel; d=json.loads(p.read_text()); d['version']=VERSION; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'curiomondo-site-manifest.json'; d=json.loads(p.read_text()); d['site']['current_site_version']=VERSION; d['site']['site_version']=VERSION; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('v346',SLUG)
