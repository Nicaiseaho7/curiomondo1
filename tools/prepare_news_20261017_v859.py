#!/usr/bin/env python3
"""Prepara dieci flash di attualità e servizi per il 17 ottobre 2026."""
import json, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as image_shared
VERSION=859
BATCH=ROOT/'tools/news_batch_20261017_v859.json'
IMAGES=ROOT/'tools/news_images_20261017_v859.json'
AUDIT=ROOT/'tools/news_audit_20261017_v859.json'
OFFSETS=(0,5,10,15,20,25,30,35,40,45)
PHRASES=(
 'Puoi verificare le informazioni prima di metterti in viaggio.',
 'Una fonte ufficiale aiuta a distinguere un avviso da una voce.',
 'La prudenza lascia spazio a decisioni più consapevoli.',
 'Controllare l’orario prima di partire può evitare attese inutili.',
 'Puoi seguire gli aggiornamenti locali per organizzare la giornata.',
 'Un dato chiaro rende più semplice capire che cosa cambia.',
 'Puoi informarti senza dare per certo ciò che non è confermato.',
 'Un programma può cambiare: controllare gli avvisi aiuta.',
 'La preparazione comincia dalle informazioni utili.',
 'Puoi condividere un avviso verificato con chi ne ha bisogno.'
)
def dump(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def assign_dates(rows,release):
    for article,minutes in zip(rows,OFFSETS):
        stamp=release-timedelta(minutes=minutes)
        if article.get('source_published'):
            assert stamp>=datetime.fromisoformat(article['source_published']),article['slug']
        article['published']=article['modified']=stamp.isoformat(timespec='seconds')
def finish(article,release):
    shared.finish_page(article,release)
    path=ROOT/'notizie'/(article['slug']+'.html')
    text=path.read_text(encoding='utf-8').replace('/assets/css/global-header-v275.css?v=736','/assets/css/global-header-v275.css?v=633')
    path.write_text(text,encoding='utf-8')
def main():
    shared.VERSION=image_shared.VERSION=VERSION
    rows=json.loads(BATCH.read_text(encoding='utf-8'))
    release=datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-17'
    assert len(rows)==len(OFFSETS)==10
    assert not sys.argv[1:]
    phrases_path=ROOT/'assets/data/frasi-nome.json'
    phrases=json.loads(phrases_path.read_text(encoding='utf-8'))
    _,used=nome_pensiero.used(ROOT)
    for phrase in PHRASES:
        if phrase not in phrases: phrases.append(phrase)
    assert sum(p not in used for p in phrases)>=10
    dump(phrases_path,phrases)
    sources=json.loads(IMAGES.read_text(encoding='utf-8'))
    images=[]
    for a in rows:
        assert not (ROOT/'notizie'/(a['slug']+'.html')).exists(),a['slug']
        assert 1<=len(a['fonti'])<=2
        assert max(len(p.split()) for p in a['paragrafi'])<=60
        image=image_shared.image_for(a,sources)
        site.write_article(a,image,VERSION)
        images.append(image)
    registry_path=ROOT/'assets/data/editorial-images-v210.json'
    registry=json.loads(registry_path.read_text(encoding='utf-8'))
    registry['items']=images+registry['items']; registry['version']=VERSION
    dump(registry_path,registry)
    assign_dates(rows,release)
    for a in rows: finish(a,release)
    shared.sync_complete(rows)
    state_path=ROOT/'CURIOMONDO-RELEASE-STATE.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    state['articleCount']+=10; state['generatedEditorialImages']+=10
    state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),date='2026-10-17',release_date='2026-10-17',updated_at=release.isoformat(),last_update='notizie-mattina-17-ottobre-v859',status='ready')
    dump(state_path,state)
    audit={'version':VERSION,'new_articles':10,'updated_articles':0,'new_images':10,
      'request':'Notizie, meteo, trasporti e servizi — 17 ottobre 2026','push_executed':False,'manifest_accessed':False,
      'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'source_list':'Fonti istituzionali e agenzie elencate nelle singole pagine.',
      'exclusions':['Notizie senza conferma primaria o con elementi non verificabili escluse.','Avviso ferroviario duplicato sul tratto Pisa–Pietrasanta escluso perché già pubblicato.'],
      'corrections':['Dichiarazioni KCNA attribuite all’agenzia e non presentate come verificate indipendentemente.','Ordine presidenziale distinto dall’abrogazione della legge.','Fermo merci distinto dallo sciopero del trasporto pubblico.'],
      'image_visual_review':'Completata su dieci copertine dedicate.','browser_visual_qa':'Da completare dopo i gate.',
      'format_exception':'Flash circoscritti ai fatti pratici e agli aggiornamenti verificati, senza riempitivo.',
      'evergreen_exception':'Nessun collegamento generico forzato.'}
    audit['release']=release.isoformat()
    audit['articles']=[{'slug':a['slug'],'title':a['titolo'],'published':a['published'],'modified':a['modified'],'source_date':a['source_date'],'sources':a['fonti'],'words':sum(len(p.split()) for p in a['paragrafi']),'risk':a['risk'],'original_value':a['original_value']} for a in rows]
    dump(AUDIT,audit)
    print(json.dumps({'version':VERSION,'new_articles':10,'new_images':10,'release':audit['release']},ensure_ascii=False))
if __name__=='__main__': main()
