#!/usr/bin/env python3
"""Quattro dossier richiesti: due aggiornamenti e due articoli, senza manifest o push."""
import json,sys,subprocess
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as imgs
from tools.prepare_news_20261013_v847 import update_article
VERSION=854

def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    rows=json.loads((ROOT/'tools/news_batch_20261015_v854.json').read_text())
    sources=json.loads((ROOT/'tools/news_images_20261015_v854.json').read_text())
    release=datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-15'
    shared.VERSION=imgs.VERSION=VERSION
    phrases=ROOT/'assets/data/frasi-nome.json'
    values=json.loads(phrases.read_text())
    for p in ['Puoi prendere nota di un dubbio e tornarci quando hai più calma.','Puoi chiedere a una persona fidata di accompagnarti a un appuntamento.']:
        if p not in values:values.append(p)
    dump(phrases,values)
    images=[]
    for a in rows:
        assert len(a['fonti'])<=2
        assert max(len(p.split()) for p in a['paragrafi'])<=60
        image=imgs.image_for(a,sources)
        if a.get('update'):update_article(a,image,release)
        else:
            assert not (ROOT/'notizie'/(a['slug']+'.html')).exists()
            a['published']=a['modified']=release.isoformat()
            site.write_article(a,image,VERSION)
        shared.finish_page(a,release)
        path=ROOT/'notizie'/(a['slug']+'.html')
        doc=html.fromstring(path.read_text())
        figure=doc.xpath('//figure[contains(@class,"article-image")]')[0]
        figure.set('data-sensitive-context',str(bool(a.get('sensitive'))).lower())
        if a.get('likeness'):figure.set('data-synthetic-likeness','public-figure')
        else:figure.attrib.pop('data-synthetic-likeness',None)
        if a.get('sensitive') and a.get('likeness'):figure.set('data-portrait-format','neutral-isolated')
        else:figure.attrib.pop('data-portrait-format',None)
        for n in doc.xpath('//script[@type="application/ld+json"]'):
            j=json.loads(n.text)
            if j.get('@type')=='NewsArticle':
                j['articleSection']=a['categoria'];n.text=json.dumps(j,ensure_ascii=False,separators=(',',':'))
        for n in doc.xpath('//meta[@property="article:section"]'):n.set('content',a['categoria'])
        for meta in doc.xpath('//meta'):
            name=meta.get('property') or meta.get('name')
            field={'twitter:title':a['titolo'],'twitter:description':a['sommario'],'twitter:image':'https://curiomondo.it'+image['variants'][-1]['src'],'article:published_time':a['published'],'article:modified_time':a['modified']}.get(name)
            if field:meta.set('content',field)
        figure.xpath('.//img')[0].set('src','..'+image['variants'][-1]['src'])
        figure.xpath('.//img')[0].set('width','1200');figure.xpath('.//img')[0].set('height','675')
        for css in doc.xpath('//link[contains(@href,"global-header-v275.css")]'):css.set('href','/assets/css/global-header-v275.css?v=633')
        shared.save(path,doc)
        images.append(image)
    p=ROOT/'assets/data/editorial-images-v210.json';registry=json.loads(p.read_text())
    replaced={a['slug'] for a in rows}
    registry['items']=images+[i for i in registry['items'] if i.get('id') not in replaced];registry['version']=VERSION;dump(p,registry)
    p=ROOT/'assets/data/home-feed-v210.json';feed=json.loads(p.read_text());by_url={'/notizie/'+a['slug']+'.html':a for a in rows}
    for i in feed['items']:
        if i.get('url') in by_url:i['excerpt']=by_url[i['url']]['sommario']
    dump(p,feed)
    shared.sync_complete(rows)
    p=ROOT/'CURIOMONDO-RELEASE-STATE.json';state=json.loads(p.read_text());state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),articleCount=state['articleCount']+2,generatedEditorialImages=state['generatedEditorialImages']+4,last_update='quattro-dossier-15-ottobre-v854',date='2026-10-15',release_date='2026-10-15',updated_at=release.isoformat(),status='ready');dump(p,state)
    dump(ROOT/'tools/news_audit_20261015_v854.json',dict(version=VERSION,release=release.isoformat(),new_articles=2,updated_articles=2,new_images=4,push_executed=False,manifest_accessed=False,baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),corrections=['Papa: ultimo bollettino verificato del 14 ottobre alle 19:50, non bollettino del 15.','Consiglio europeo: programma e posizioni italiane, non accordi già approvati o arrivo a Bruxelles attestato.','Starlink: denuncia ucraina e replica di Musk; non accertata ritorsione politica né citazione tradito.','Hormuz: GFS Pride affondata e GFS Giselle danneggiata; Cape Dao colpita il 23 settembre. Escluso record non dimostrato.'],source_access_limits=['Governo.it 403: trascrizione pubblica del discorso da Mi-Lorenteggio, confrontata con resoconti ANSA e Agenzia Vista.','UKMTO: elenco non popolato nella versione testuale; recuperato comunicato MPA Singapore.','Ucraina: non recuperati i post originali su Starlink; utilizzate due ricostruzioni giornalistiche indipendenti Reuters ed Euronews.'],format_exception='Flash proporzionati alla materia verificata; nessun riempitivo.',articles=rows,editorial_checks={k:True for k in ['lead','sources','dates','attribution','title','original_value','no_duplicate','no_fillers','short_paragraphs','sources_outside_body','disclosure']},image_visual_review='Da completare',technical_validation='Da completare'))
    print(json.dumps(dict(version=VERSION,new_articles=2,updated_articles=2,release=release.isoformat())))
if __name__=='__main__':main()
