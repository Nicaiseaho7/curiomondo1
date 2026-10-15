#!/usr/bin/env python3
"""Prepare ten verified requested stories for a ZIP handoff, without push."""
import json,sys,subprocess
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as imgs
VERSION=855
BATCH=ROOT/'tools/news_batch_20261015_v855.json'
AUDIT=ROOT/'tools/news_audit_20261015_v855.json'
OFFSETS=(0,5,12,20,29,39,50,62,75,89)
PHRASES=['Puoi scegliere una cosa da fare oggi e rimandare il resto.','Se una stanza è rumorosa, puoi cercare un posto più tranquillo.','Puoi avvisare che arriverai in ritardo senza inventare una scusa.','Un appuntamento si può spostare quando hai bisogno di riposare.','Puoi chiedere di rileggere insieme un documento prima di firmarlo.','Se un oggetto ti serve, puoi prima verificare se lo hai già.','Puoi dedicare una pausa a mangiare con calma.','Puoi chiedere aiuto anche per una cosa che sai fare da solo.','Puoi uscire a prendere aria quando passi molte ore al chiuso.','Se una conversazione si scalda, puoi proporre una pausa.']
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def finish(a,release):
    shared.finish_page(a,release)
    path=ROOT/'notizie'/(a['slug']+'.html');doc=html.fromstring(path.read_text())
    figure=doc.xpath('//figure[contains(@class,"article-image")]')[0]
    figure.set('data-sensitive-context',str(bool(a.get('sensitive'))).lower())
    for n in doc.xpath('//script[@type="application/ld+json"]'):
        j=json.loads(n.text)
        if j.get('@type')=='NewsArticle':j['articleSection']=a['categoria'];n.text=json.dumps(j,ensure_ascii=False,separators=(',',':'))
    for n in doc.xpath('//meta[@property="article:section"]'):n.set('content',a['categoria'])
    for n in doc.xpath('//meta'):
        key=n.get('property') or n.get('name')
        value={'twitter:title':a['titolo'],'twitter:description':a['sommario'],'article:published_time':a['published'],'article:modified_time':a['modified']}.get(key)
        if value:n.set('content',value)
    for n in doc.xpath('//link[contains(@href,"global-header-v275.css")]'):n.set('href','/assets/css/global-header-v275.css?v=633')
    hero=figure.xpath('.//img')[0];hero.set('src','..'+a['hero1200']);hero.set('width','1200');hero.set('height','675')
    if a['image_key']=='cinturrino' and not doc.xpath('//aside[contains(@class,"cm-evergreen-reader")]'):
        block=html.fromstring('<aside class="cm-evergreen-reader"><p>Approfondimento</p><h2>Che cos’è l’avviso di conclusione delle indagini</h2><p>Il passaggio che precede la richiesta di processo e le possibilità della difesa.</p><a href="/approfondimenti/che-cose-415-bis-avviso-conclusione-indagini.html">Leggi l’approfondimento →</a></aside>')
        doc.xpath('//article[contains(@class,"art-body")]')[0].addnext(block)
    shared.save(path,doc)
def main():
    rows=json.loads(BATCH.read_text());release=datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-15','Riverificare le notizie prima di un rilascio in altra data'
    shared.VERSION=imgs.VERSION=VERSION
    if sys.argv[1:]==['--release-now']:
        audit=json.loads(AUDIT.read_text())
        for a,m in zip(rows,OFFSETS):
            assert subprocess.run(['git','cat-file','-e','HEAD:notizie/'+a['slug']+'.html'],cwd=ROOT,capture_output=True).returncode!=0,'Non alterare date di pagine già pubblicate'
            a['published']=a['modified']=(release-timedelta(minutes=m)).isoformat();a['hero1200']='/assets/images/editorial-auto/'+a['slug']+'-v855-1200.webp';finish(a,release)
        shared.sync_complete(rows)
        audit['prepared_release']=audit['release'];audit['release']=release.isoformat();audit['articles']=rows;dump(AUDIT,audit)
        p=ROOT/'CURIOMONDO-RELEASE-STATE.json';s=json.loads(p.read_text());s['updated_at']=release.isoformat();dump(p,s)
        print('Date riallineate per il primo rilascio. Eseguire di nuovo i gate.');return
    assert not sys.argv[1:]
    sources=json.loads((ROOT/'tools/news_images_20261015_v855.json').read_text())
    assert len(rows)==10
    for a in rows:
        assert not (ROOT/'notizie'/(a['slug']+'.html')).exists()
        assert 1<=len(a['fonti'])<=2 and max(len(p.split()) for p in a['paragrafi'])<=60
    p=ROOT/'assets/data/frasi-nome.json';phrases=json.loads(p.read_text());phrases.extend(x for x in PHRASES if x not in phrases);dump(p,phrases)
    images=[]
    for a,m in zip(rows,OFFSETS):
        im=imgs.image_for(a,sources);site.write_article(a,im,VERSION);images.append(im)
        a['published']=a['modified']=(release-timedelta(minutes=m)).isoformat();a['hero1200']=im['variants'][-1]['src'];finish(a,release)
    p=ROOT/'assets/data/editorial-images-v210.json';registry=json.loads(p.read_text());registry['items']=images+registry['items'];registry['version']=VERSION;dump(p,registry)
    shared.sync_complete(rows)
    p=ROOT/'CURIOMONDO-RELEASE-STATE.json';s=json.loads(p.read_text());s.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),articleCount=s['articleCount']+10,generatedEditorialImages=s['generatedEditorialImages']+10,last_update='segnalazioni-15-ottobre-v855',date='2026-10-15',release_date='2026-10-15',updated_at=release.isoformat(),status='ready');dump(p,s)
    dump(AUDIT,dict(version=VERSION,release=release.isoformat(),baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),new_articles=10,new_images=10,push_executed=False,manifest_accessed=False,selected_user_signals=[2,5,6,7,8,10,11,12,14,15],not_in_this_batch=[1,3,4,9,13],selection_reason='Limite di dieci articoli; preferenza a storie con riscontri dettagliati. Non è un giudizio di falsità sulle cinque escluse.',corrections=['Gudmundsson gioca nella Lazio e salta la gara contro la Juventus.','Peshawar: 35 morti, inclusi 34 bambini, nei bilanci AP e Reuters.','Pooh: centenario del libro del 1926, non del peluche acquistato nel 1921.','Giustizia: richiesta di rinvio, richieste di pena e sentenza di appello distinti.','PASSI: adulti 18–69 anni, biennio 2024–2025, dati autoriferiti.','Milesi: Los Angeles è un obiettivo, non una qualificazione acquisita.'],source_access_limits=['NYPL: pagina diretta 403, comunicato ufficiale indicizzato e testo ANSA consultati.','Anadolu: resoconto indicizzato, apertura diretta indisponibile; agenda ufficiale Royal Diary verificata.','Roma: ufficio stampa riportato da TuttoASRoma; ANSA fornisce resoconto indipendente.','Lazio: dichiarazioni dei canali ufficiali trascritte da Cittaceleste e verificate nel resoconto ANSA; rosa ufficiale consultata.'],image_visual_review='Controllate le dieci immagini e i ritagli; ritratto Milesi rigenerato da riferimento reale; Gudmundsson da riferimento reale.',technical_validation='In attesa',articles=rows))
    print('Preparati dieci articoli, trenta WebP e superfici editoriali v855.')
if __name__=='__main__':main()
