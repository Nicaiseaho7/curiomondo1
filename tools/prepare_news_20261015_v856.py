#!/usr/bin/env python3
"""Prepare all fifteen requested verified stories for ZIP handoff, without push."""
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
VERSION=856
BATCH=ROOT/'tools/news_batch_20261015_v856.json'
AUDIT=ROOT/'tools/news_audit_20261015_v856.json'
OFFSETS=tuple(range(15))
PHRASES=[
'Puoi annotare una cosa importante prima che ti sfugga.','Puoi controllare una cifra una seconda volta.','Puoi lasciare libero un momento della serata.','Una risposta chiara può essere anche breve.','Puoi scegliere un percorso diverso per tornare a casa.','Puoi mettere in ordine soltanto un cassetto.','Puoi rileggere un messaggio prima di inviarlo.','Puoi spegnere una notifica per un’ora.','Puoi chiedere una spiegazione con calma.','Puoi bere un bicchiere d’acqua prima di ripartire.','Puoi rimandare una decisione che non è urgente.','Puoi preparare domani ciò che oggi ti affatica.','Puoi ascoltare senza dover subito rispondere.','Puoi dedicare dieci minuti a una cosa che ti piace.','Puoi chiudere la giornata senza completare tutto.']
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
    shared.save(path,doc)
def main():
    rows=json.loads(BATCH.read_text());release=datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-15','Riverificare le notizie prima di un rilascio in altra data'
    shared.VERSION=imgs.VERSION=VERSION
    if sys.argv[1:]==['--release-now']:
        audit=json.loads(AUDIT.read_text())
        for a,m in zip(rows,OFFSETS):
            assert subprocess.run(['git','cat-file','-e','HEAD:notizie/'+a['slug']+'.html'],cwd=ROOT,capture_output=True).returncode!=0,'Non alterare date di pagine già pubblicate'
            a['published']=a['modified']=(release-timedelta(minutes=m)).isoformat();a['hero1200']='/assets/images/editorial-auto/'+a['slug']+'-v856-1200.webp';finish(a,release)
        shared.sync_complete(rows)
        audit['prepared_release']=audit['release'];audit['release']=release.isoformat();audit['articles']=rows;dump(AUDIT,audit)
        p=ROOT/'CURIOMONDO-RELEASE-STATE.json';s=json.loads(p.read_text());s['updated_at']=release.isoformat();dump(p,s)
        print('Date riallineate per il primo rilascio. Eseguire di nuovo i gate.');return
    assert not sys.argv[1:] and len(rows)==15
    for a in rows:
        assert not (ROOT/'notizie'/(a['slug']+'.html')).exists()
        assert 1<=len(a['fonti'])<=2 and max(len(p.split()) for p in a['paragrafi'])<=60
    p=ROOT/'assets/data/frasi-nome.json';phrases=json.loads(p.read_text());phrases.extend(x for x in PHRASES if x not in phrases);dump(p,phrases)
    sources=json.loads((ROOT/'tools/news_images_20261015_v856.json').read_text())
    images=[]
    for a,m in zip(rows,OFFSETS):
        im=imgs.image_for(a,sources);site.write_article(a,im,VERSION);images.append(im)
        a['published']=a['modified']=(release-timedelta(minutes=m)).isoformat();a['hero1200']=im['variants'][-1]['src'];finish(a,release)
    p=ROOT/'assets/data/editorial-images-v210.json';registry=json.loads(p.read_text());registry['items']=images+registry['items'];registry['version']=VERSION;dump(p,registry)
    shared.sync_complete(rows)
    p=ROOT/'CURIOMONDO-RELEASE-STATE.json';s=json.loads(p.read_text());s.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),articleCount=s['articleCount']+15,generatedEditorialImages=s['generatedEditorialImages']+15,last_update='segnalazioni-sera-15-ottobre-v856',date='2026-10-15',release_date='2026-10-15',updated_at=release.isoformat(),status='ready');dump(p,s)
    dump(AUDIT,dict(version=VERSION,release=release.isoformat(),baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),new_articles=15,new_images=15,push_executed=False,manifest_accessed=False,selected_user_signals=list(range(1,16)),not_in_this_batch=[],corrections=['Peshawar: bilancio consolidato di 35 vittime, 34 bambini e un’insegnante.','Papa Leone XIV: il viaggio sudamericano resta formalmente programmato; la partenza dipende dal decorso.','Diesel: replica della Casa Bianca e conseguenze diplomatiche trattate con angoli distinti.','Patriot: esaurimento attribuito a una fonte CNN, senza quantità ufficiali pubblicate.'],image_visual_review='Quindici copertine dedicate generate; contesti sensibili senza ricostruzioni di vittime, incidenti, arresti o esecuzioni.',technical_validation='In attesa',articles=rows))
    print('Preparati quindici articoli, quarantacinque WebP e superfici editoriali v856.')
if __name__=='__main__':main()
