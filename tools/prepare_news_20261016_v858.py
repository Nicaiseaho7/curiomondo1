#!/usr/bin/env python3
"""Prepara quindici notizie politica/economia/sport in uno ZIP senza push."""
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

VERSION=858
BATCH=ROOT/'tools/news_batch_20261016_v858.json'
IMAGES=ROOT/'tools/news_images_20261016_v858.json'
AUDIT=ROOT/'tools/news_audit_20261016_v858.json'
OFFSETS=(0,5,12,20,29,39,50,62,75,89,104,120,137,155,174)
PHRASES=(
 'Puoi leggere una regola fino in fondo prima di decidere.',
 'Puoi conservare i documenti che serviranno più avanti.',
 'Chiedere aiuto per assistere qualcuno non riduce il tuo affetto.',
 'Puoi semplificare un compito senza trascurare ciò che conta.',
 'La sicurezza cresce quando ogni controllo viene fatto con cura.',
 'Un progetto può iniziare da un passo piccolo e ben preparato.',
 'Tenere i conti in ordine protegge il lavoro di molte persone.',
 'Puoi distinguere una stima da un fatto accertato.',
 'Un numero racconta di più quando conosci il periodo a cui si riferisce.',
 'Puoi controllare due volte i dati prima di inviare una richiesta.',
 'Concludere bene un progetto è importante quanto iniziarlo.',
 'Un risultato speciale nasce anche dal lavoro quotidiano.',
 'Rialzarsi dopo uno svantaggio richiede lucidità.',
 'Puoi arrivare in anticipo e vivere l’attesa con calma.',
 'Ogni turno superato merita concentrazione per quello successivo.'
)

def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

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
    assert release.date().isoformat()=='2026-10-16'
    assert len(rows)==len(OFFSETS)==15
    rerender=sys.argv[1:]==['--release-now']
    assert not sys.argv[1:] or rerender
    if rerender:
        for a in rows:
            assert subprocess.run(['git','cat-file','-e','HEAD:notizie/'+a['slug']+'.html'],cwd=ROOT,capture_output=True).returncode!=0
        audit=json.loads(AUDIT.read_text(encoding='utf-8'))
    else:
        phrases_path=ROOT/'assets/data/frasi-nome.json'
        phrases=json.loads(phrases_path.read_text(encoding='utf-8'))
        _,used=nome_pensiero.used(ROOT)
        for phrase in PHRASES:
            if phrase not in phrases: phrases.append(phrase)
        assert sum(p not in used for p in phrases)>=15
        dump(phrases_path,phrases)
        sources=json.loads(IMAGES.read_text(encoding='utf-8'))
        images=[]
        for a in rows:
            assert not (ROOT/'notizie'/(a['slug']+'.html')).exists()
            assert 1<=len(a['fonti'])<=2
            assert max(len(p.split()) for p in a['paragrafi'])<=60
            image=image_shared.image_for(a,sources)
            site.write_article(a,image,VERSION)
            images.append(image)
        registry_path=ROOT/'assets/data/editorial-images-v210.json'
        registry=json.loads(registry_path.read_text(encoding='utf-8'))
        registry['items']=images+registry['items']; registry['version']=VERSION
        dump(registry_path,registry)
        audit={'version':VERSION,'new_articles':15,'updated_articles':0,'new_images':15,
          'request':'Politica italiana ed europea, economia, lavoro, denaro e sport — 16 ottobre 2026',
          'push_executed':False,'manifest_accessed':False,
          'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'source_list':'Fonti per la ricerca degli articoli.txt; fonti elencate in ogni articolo.',
          'exclusions':['Inflazione definitiva esclusa come nuovo articolo perché il tema era già presente nel sito.','Risultati o indiscrezioni senza fonte verificabile esclusi.'],
          'corrections':['Atti in calendario distinti da leggi approvate.','Conclusioni UE distinte da norme immediatamente applicabili.','Procedure INPS e GSE distinte da rimborsi o incentivi automatici.'],
          'image_visual_review':'Completata su quindici copertine dedicate.','browser_visual_qa':'Da completare dopo i gate.',
          'format_exception':'Flash proporzionati a fatti circoscritti, senza riempitivo.','evergreen_exception':'Nessuna nuova guida richiesta; nessun collegamento generico forzato.'}
    assign_dates(rows,release)
    for a in rows: finish(a,release)
    shared.sync_complete(rows)
    state_path=ROOT/'CURIOMONDO-RELEASE-STATE.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if not rerender:
        state['articleCount']+=15; state['generatedEditorialImages']+=15
    state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),date='2026-10-16',release_date='2026-10-16',updated_at=release.isoformat(),last_update='politica-economia-sport-16-ottobre-v858',status='ready')
    dump(state_path,state)
    if rerender: audit['prepared_release']=audit.get('release')
    audit['release']=release.isoformat()
    audit['articles']=[{'slug':a['slug'],'title':a['titolo'],'published':a['published'],'modified':a['modified'],'source_date':a['source_date'],'sources':a['fonti'],'words':sum(len(p.split()) for p in a['paragrafi']),'risk':a['risk'],'original_value':a['original_value']} for a in rows]
    dump(AUDIT,audit)
    print(json.dumps({'version':VERSION,'new_articles':15,'new_images':15,'release':audit['release']},ensure_ascii=False))

if __name__=='__main__': main()
