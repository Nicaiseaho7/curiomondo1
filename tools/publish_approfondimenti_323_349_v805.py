#!/usr/bin/env python3
"""Importa due guide su superfici correnti, senza leggere o aggiornare il manifest.

Non esegue commit o push. --finalize-dates fissa le date al momento del rilascio
per guide ancora in preparazione; non usarlo su pagine già pubblicate.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from lxml import etree, html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / 'tools/editorial-payloads/approfondimenti-323-349-v805'
CAPTION = 'Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
GUIDES = [
 dict(number=323, slug='domotica-cablata-o-wireless', title='Domotica cablata o wireless: costi, compatibilità e guasti',
      description='Cavi, radio e sistemi misti a confronto: lavori, controllo locale, Matter, manutenzione e voci da verificare nel preventivo.',
      category='Tecnologia e digitale', body='domotica-body.txt',
      alt='Tecnica con sensore radio e comando cablato accanto a un quadro domotico domestico; illustrazione IA non documentaria.',
      prompt='Impianto domotico domestico, tecnica in volto con sensore radio e comando cablato, quadro protetto e soggiorno, fotorealismo editoriale 3:2, nessun testo.',
      points=['Cavo, protocollo e piattaforma sono scelte distinte: controllare la funzione completa.',
              'La radio limita alcuni lavori, ma richiede alimentazione, copertura e manutenzione.',
              'Provare separatamente guasto Internet, rete locale e componenti centrali.',
              'Confrontare posa, configurazione, ricambi e servizi sullo stesso perimetro.'],
      disclaimer='Guida informativa: non è un progetto elettrico né un manuale per intervenire su circuiti. Modifiche e verifiche devono essere affidate ai professionisti abilitati quando richiesto.',
      related=[],
      sources=[('https://knx.org/knx-technology','KNX Association — mezzi TP, RF e IP, accoppiatori e architettura.'),
               ('https://csa-iot.org/all-solutions/matter/','Connectivity Standards Alliance — Matter e interoperabilità locale.'),
               ('https://threadgroup.org/What-is-Thread/Overview','Thread Group — architettura della rete Thread.'),
               ('https://www.home-assistant.io/integrations/matter/','Home Assistant — integrazione Matter, requisiti e limiti delle funzioni.'),
               ('https://www.home-assistant.io/integrations/knx/','Home Assistant — integrazione KNX e requisiti di configurazione.')]),
 dict(number=349, slug='master-online-o-in-presenza', title='Master online o in presenza: titolo, stage e costo totale',
      description='Come confrontare master universitari e corsi privati: modalità didattiche, frequenza, docenti, stage, networking e spese oltre la quota.',
      category='Economia e lavoro', body='master-body.txt',
      alt='Partecipanti adulti a un seminario con docente in aula e collegamento su laptop; illustrazione IA non documentaria.',
      prompt='Seminario universitario italiano con partecipanti adulti in volto, docente in aula e docente remota su laptop, ambiente realistico 3:2, nessun testo o logo.',
      points=['Verificare chi rilascia il titolo: la parola master non basta a identificarlo.',
              'Online può essere sincrono, asincrono o misto: controllare calendario e presenze.',
              'Aziende partner e orientamento non garantiscono uno stage o un posto di lavoro.',
              'Confrontare quota, strumenti, trasferte e tempo necessario per completare il corso.'],
      disclaimer='Guida informativa per confrontare percorsi formativi. Non garantisce riconoscimento in concorsi, occupazione o aumenti di reddito; requisiti e condizioni vanno verificati nel bando della singola edizione.',
      related=['/notizie/corporate-mba-cdp-1200-candidature-luiss-2-ottobre-2026.html'],
      sources=[('https://off270.mur.gov.it/leggi/dm270.html','MUR — decreto ministeriale 270/2004: master, crediti e impegno formativo.'),
               ('https://www.mur.gov.it/it/aree-tematiche/universita/le-universita','MUR — elenco e tipologie di università.'),
               ('https://master.unibo.it/media-educazione-didattica-innovazione-digitale/it/faq1','Università di Bologna, master MED — esempio di frequenza, didattica mista e stage; verificare il bando dell’edizione scelta.'),
               ('https://master.unibo.it/storia-cultura-alimentazione/it/il-master/struttura-del-master','Università di Bologna — esempio di organizzazione delle lezioni in aula e online.')]),
]

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def markup(node):
    return html.tostring(node, encoding='unicode', method='html', doctype='<!doctype html>')+'\n'

def fragment(text):
    return html.fragment_fromstring(text)

def build_page(g, date, version):
    doc=html.fromstring((ROOT/'approfondimenti/fibra-aziende-costi-sla.html').read_text(encoding='utf-8'))
    doc.xpath('//body')[0].set('data-article-id',g['slug'])
    canonical='https://curiomondo.it/approfondimenti/'+g['slug']+'.html'
    image='/assets/images/editorial-auto/'+g['slug']+'-v805-1200.webp'
    doc.xpath('//title')[0].text=g['title']+' | CurioMondo'
    fields={'description':g['description'],'og:title':g['title'],'og:description':g['description'],
            'og:url':canonical,'og:image':'https://curiomondo.it'+image,'og:image:alt':g['alt']}
    for m in doc.xpath('//meta'):
        key=m.get('name') or m.get('property')
        if key in fields: m.set('content',fields[key])
    doc.xpath('//link[@rel="canonical"]')[0].set('href',canonical)
    for s in doc.xpath('//script[@type="application/ld+json"]'):
        data=json.loads(s.text)
        if data.get('@type')!='Article':
            s.getparent().remove(s); continue
        data.update(headline=g['title'],description=g['description'],datePublished=date,dateModified=date,
                    mainEntityOfPage=canonical,image=['https://curiomondo.it'+image])
        s.text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    main=doc.xpath('//main')[0]
    main.xpath('./h1')[0].text=g['title']
    main.xpath('./p[@class="subtitle"]')[0].text=g['description']
    main.xpath('./div[@class="badge"]')[0].text='Approfondimento · '+g['category']
    body=main.xpath('./article[@class="art-body"]')[0]
    raw=(PAYLOAD/g['body']).read_text(encoding='utf-8').replace('cm-table-scroll','cm-table-wrap')
    newbody=fragment('<article class="art-body" data-editorial-protocol="4.0" data-article-format="feature">'+raw+'</article>')
    body.getparent().replace(body,newbody)
    count=len(newbody.text_content().split())
    if count<2000: raise ValueError('Guida sotto 2.000 parole')
    meta=main.xpath('./div[@class="meta"]')[0]
    meta.clear(); meta.set('class','meta')
    stamp=datetime.fromisoformat(date).strftime('%d/%m/%Y · %H:%M')
    meta.text=f'{stamp} · {math.ceil(count/200)} min di lettura'
    summary=fragment('<section class="cm-summary-box" aria-labelledby="in-sintesi"><h2 id="in-sintesi">In sintesi</h2><ul>'+''.join('<li>'+x+'</li>' for x in g['points'])+'</ul></section>')
    old=main.xpath('./section[@class="cm-insight"]')[0]; main.replace(old,summary)
    fig=main.xpath('./figure')[0]
    img=fig.xpath('.//img')[0]
    base='/assets/images/editorial-auto/'+g['slug']+'-v805-'
    img.set('src',base+'800.webp'); img.set('srcset',', '.join(base+str(w)+'.webp '+str(w)+'w' for w in (480,800,1200)))
    img.set('alt',g['alt'])
    related=main.xpath('./section[@class="curio-related"]')[0]
    main.remove(related)
    if g['related']:
        node=fragment('<section class="curio-related" data-curated-related="true"><h2>Notizia collegata</h2><div class="curio-related-grid"></div></section>')
        for url in g['related']:
            news=html.fromstring((ROOT/url.lstrip('/')).read_text(encoding='utf-8'))
            a=etree.SubElement(node.xpath('.//div')[0],'a',href=url)
            etree.SubElement(a,'small').text='Economia e formazione'
            etree.SubElement(a,'strong').text=news.xpath('//h1')[0].text_content()
        main.insert(main.index(newbody)+1,node)
    src=main.xpath('./div[@class="art-sources"]')[0]
    src.clear(); src.set('class','art-sources')
    etree.SubElement(src,'h2').text='Fonti consultate'
    ul=etree.SubElement(src,'ul')
    for url,label in g['sources']:
        etree.SubElement(etree.SubElement(ul,'li'),'a',href=url,rel='noopener noreferrer',target='_blank').text=label
    p=etree.SubElement(src,'p')
    p.text='Redazione CurioMondo · Testo originale. Ultimo aggiornamento editoriale: '+stamp+' (ora italiana). '
    etree.SubElement(p,'a',href='/pagine/metodo-editoriale.html').text='Come lavoriamo'
    etree.SubElement(src,'p').text=g['disclaimer']
    etree.SubElement(src,'p').text=CAPTION
    (ROOT/'approfondimenti'/ (g['slug']+'.html')).write_text(markup(doc),encoding='utf-8')

def sync_surfaces(version, dates):
    index_path=ROOT/'approfondimenti/index.html'
    doc=html.fromstring(index_path.read_text(encoding='utf-8'))
    for g in GUIDES:
        url='../approfondimenti/'+g['slug']+'.html'
        for old in doc.xpath('//a[@class="card"]'):
            if old.get('href')==url: old.getparent().remove(old)
        section=next(s for s in doc.xpath('//section[contains(@class,"cat-section")]')
                     if s.xpath('./h2')[0].text_content()==g['category'])
        grid=section.xpath('./div[@class="grid"]')[0]
        a=etree.Element('a',{'class':'card','data-cm-cat':g['category'],'data-cm-evergreen-slug':g['slug'],'href':url})
        etree.SubElement(a,'span',{'class':'tag'}).text=g['category']
        text=etree.SubElement(a,'div'); etree.SubElement(text,'h2').text=g['title']; etree.SubElement(text,'p').text=g['description']
        etree.SubElement(a,'b').text='Leggi l’approfondimento →'
        grid.insert(0,a)
    for s in doc.xpath('//section[contains(@class,"cat-section")]'):
        count=len(s.xpath('.//a[@class="card"]'))
        for small in doc.xpath('//a[@href="#'+s.get('id','')+'"]//small'): small.text=f'({count})'
    index_path.write_text(markup(doc),encoding='utf-8')
    search_path=ROOT/'assets/data/search-index-v210.json'
    data=json.loads(search_path.read_text(encoding='utf-8'))
    urls={'/approfondimenti/'+g['slug']+'.html' for g in GUIDES}
    data['items']=[dict(title=g['title'],excerpt=g['description'],url='/approfondimenti/'+g['slug']+'.html',section='Approfondimenti / '+g['category']) for g in GUIDES]+[x for x in data['items'] if x.get('url') not in urls]
    data['version']=version; dump(search_path,data)
    sitemap_path=ROOT/'sitemap.xml'; tree=etree.parse(str(sitemap_path)); ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    for url in list(tree.getroot()):
        if url.findtext('{'+ns+'}loc') in {'https://curiomondo.it'+x for x in urls}: tree.getroot().remove(url)
    for g in GUIDES:
        node=etree.SubElement(tree.getroot(),'{'+ns+'}url')
        for key,value in [('loc','https://curiomondo.it/approfondimenti/'+g['slug']+'.html'),('lastmod',dates[g['slug']]),('changefreq','monthly'),('priority','0.8')]: etree.SubElement(node,'{'+ns+'}'+key).text=value
    tree.write(str(sitemap_path),encoding='utf-8',xml_declaration=True)
    redirect_path=ROOT/'_redirects'; lines=redirect_path.read_text(encoding='utf-8').splitlines()
    for g in GUIDES:
        prefix='/approfondimenti/'+g['slug']
        for suffix in ['', '/']:
            route=prefix+suffix
            if not any(x.split() and x.split()[0]==route for x in lines): lines.insert(0,f'{route} {prefix}.html 301')
    redirect_path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    registry_path=ROOT/'assets/data/editorial-images-v210.json'; registry=json.loads(registry_path.read_text(encoding='utf-8'))
    for g in GUIDES:
        record=dict(key=g['slug']+'-v805',article='/approfondimenti/'+g['slug']+'.html',alt=g['alt'],prompt=g['prompt'],disclosure=CAPTION,generator='OpenAI image generation',aiGenerated=True,documentaryPhoto=False,officialArtwork=False,sensitiveContext=False,weatherMap=False,variants=[])
        for width in (480,800,1200):
            path=ROOT/'assets/images/editorial-auto'/f"{g['slug']}-v805-{width}.webp"
            with Image.open(path) as img: w,h=img.size
            record['variants'].append(dict(w=w,h=h,src='/'+str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size))
        registry['items']=[x for x in registry['items'] if x.get('article')!=record['article']]
        registry['items'].insert(0,record)
    registry['version']=version; dump(registry_path,registry)
    for g in GUIDES:
        for url in g['related']:
            path=ROOT/url.lstrip('/'); nd=html.fromstring(path.read_text(encoding='utf-8'))
            target='/approfondimenti/'+g['slug']+'.html'
            if nd.xpath('//aside[contains(@class,"cm-evergreen-reader")]//a[@href="'+target+'"]'): continue
            body=nd.xpath('//*[@class="art-body"]')[0]
            continuation=nd.xpath('//*[@class="art-flow-continuation"]')
            after=continuation[-1] if continuation else body
            block=etree.Element('aside',{'class':'cm-evergreen-reader'})
            etree.SubElement(block,'p',{'class':'cm-evergreen-reader__kicker'}).text='Approfondimento'
            etree.SubElement(block,'h2').text=g['title']; etree.SubElement(block,'p').text=g['description']
            etree.SubElement(block,'a',href=target).text='Leggi l’approfondimento →'
            after.addnext(block); path.write_text(markup(nd),encoding='utf-8')
    for name in ['CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json']:
        path=ROOT/name; state=json.loads(path.read_text(encoding='utf-8'))
        state.update(site_version=version,version=str(version),currentVersion=version,evergreen_added=[g['slug'] for g in GUIDES],last_update='approfondimenti-lista-323-349',updated_at=datetime.now(ZoneInfo('Europe/Rome')).isoformat(timespec='seconds'))
        dump(path,state)
    selection_path=ROOT/'automation/state/approfondimenti-lista-500.json'
    selection=json.loads(selection_path.read_text(encoding='utf-8')) if selection_path.exists() else {'source':'Lista approfondimenti.txt','items':[]}
    for g in GUIDES:
        selection['items']=[x for x in selection['items'] if x.get('number')!=g['number']]
        selection['items'].append(dict(number=g['number'],title=g['title'],url='/approfondimenti/'+g['slug']+'.html',status='prepared',selected_at=dates[g['slug']]))
    dump(selection_path,selection)
    subprocess.run(['node','tools/render_home_editorial.js'],cwd=ROOT,check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--finalize-dates',action='store_true'); args=ap.parse_args()
    current=json.loads((ROOT/'assets/data/editorial-images-v210.json').read_text(encoding='utf-8'))['version']
    version=805 if current<=805 else current+1
    now=datetime.now(ZoneInfo('Europe/Rome')).isoformat(timespec='seconds')
    dates={}
    for g in GUIDES:
        path=ROOT/'approfondimenti'/(g['slug']+'.html')
        date=now
        if path.exists() and not args.finalize_dates:
            found=re.search(r'"datePublished"\s*:\s*"([^"]+)"',path.read_text(encoding='utf-8'))
            if found: date=found[1]
        dates[g['slug']]=date
        build_page(g,date,version)
    sync_surfaces(version,dates)
    print(json.dumps({'prepared':[g['slug'] for g in GUIDES],'version':version,'datePublished':dates,'manifest':'excluded'},ensure_ascii=False))

if __name__=='__main__': main()
