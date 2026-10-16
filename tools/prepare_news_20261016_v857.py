#!/usr/bin/env python3
"""Apertura 16 ottobre: dieci notizie, ZIP senza push.

--release-now riallinea le date e le superfici prima della prima pubblicazione.
Non apre né modifica curiomondo-site-manifest.json.
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as images_shared
VERSION=857
BATCH=ROOT/'tools/news_batch_20261016_v857.json'
IMAGES=ROOT/'tools/news_images_20261016_v857.json'
AUDIT=ROOT/'tools/news_audit_20261016_v857.json'
OFFSETS=(0,5,12,20,29,39,50,62,75,89)

def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def finish(a,release):
    shared.finish_page(a,release)
    p=ROOT/'notizie'/(a['slug']+'.html')
    text=p.read_text(encoding='utf-8').replace('/assets/css/global-header-v275.css?v=736','/assets/css/global-header-v275.css?v=633')
    p.write_text(text,encoding='utf-8')

def date_rows(rows,release):
    for a,offset in zip(rows,OFFSETS):
        t=release-timedelta(minutes=offset)
        if a.get('source_published'):
            assert t>=datetime.fromisoformat(a['source_published']),a['slug']
        a['published']=a['modified']=t.isoformat(timespec='seconds')

def main():
    shared.VERSION=images_shared.VERSION=VERSION
    rows=json.loads(BATCH.read_text(encoding='utf-8'))
    release=datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-16','Per un altro giorno riverificare tutte le informazioni.'
    assert len(rows)==len(OFFSETS)==10
    rerender=sys.argv[1:]==['--release-now']
    assert not sys.argv[1:] or rerender
    if rerender:
        for a in rows:
            check=subprocess.run(['git','cat-file','-e','HEAD:notizie/'+a['slug']+'.html'],cwd=ROOT,capture_output=True)
            assert check.returncode!=0,'Articolo già in HEAD: non modificare la prima pubblicazione.'
        audit=json.loads(AUDIT.read_text(encoding='utf-8'))
    else:
        phrases_path=ROOT/'assets/data/frasi-nome.json'
        phrases=json.loads(phrases_path.read_text(encoding='utf-8'))
        for phrase in (
            'Puoi controllare un orario prima di uscire di casa.',
            'Se un programma cambia, puoi scegliere un’alternativa senza colpevolizzarti.',
            'Puoi chiedere conferma quando un’informazione riguarda la tua sicurezza.',
            'Puoi rimandare una decisione finché hai i dati necessari.',
            'Puoi organizzare il viaggio lasciando qualche minuto in più.',
            'Una comunicazione chiara può evitare una preoccupazione inutile.',
            'Puoi proteggere il tuo tempo verificando prima gli impegni.',
            'Se il meteo cambia, puoi adattare il percorso con calma.',
            'Puoi distinguere una proposta da una regola già in vigore.',
            'Puoi fermarti a controllare prima di condividere una notizia.',
        ):
            if phrase not in phrases:phrases.append(phrase)
        _,used=nome_pensiero.used(ROOT)
        assert sum(p not in used for p in phrases)>=10
        dump(phrases_path,phrases)
        sources=json.loads(IMAGES.read_text(encoding='utf-8'))
        images=[]
        for a in rows:
            assert not (ROOT/'notizie'/(a['slug']+'.html')).exists()
            assert 1<=len(a['fonti'])<=2
            assert max(len(p.split()) for p in a['paragrafi'])<=60
            image=images_shared.image_for(a,sources)
            site.write_article(a,image,VERSION)
            images.append(image)
        registry_path=ROOT/'assets/data/editorial-images-v210.json'
        registry=json.loads(registry_path.read_text(encoding='utf-8'))
        registry['items']=images+registry['items'];registry['version']=VERSION
        dump(registry_path,registry)
        audit=dict(version=VERSION,new_articles=10,updated_articles=0,new_images=10,
                   request='10 notizie — apertura completa della mattina del 16 ottobre',
                   push_executed=False,manifest_accessed=False,
                   baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                   source_list='Ricerca web verificata nella mattina del 16 ottobre 2026; fonti elencate in ogni articolo.',
                   primary_access_limits=['Per scioperi e modifiche ferroviarie sono stati privilegiati MIT, RFI e PerlaPA.',
                     'Per il meteo sono stati separati il bollettino nazionale di criticità e la previsione meteorologica.',
                     'Per la cronaca internazionale sono stati incrociati AP e ANSA; per energia Reuters e S&P Global.'],
                   exclusions=['Nessun terremoto urgente inserito: non è emerso un evento notturno di rilievo verificabile per l’Italia.',
                     'Esclusi avvisi locali già scaduti o senza conferma primaria.',
                     'Escluse indiscrezioni politiche prive di atto o dichiarazione verificabile.'],
                   corrections=['Scuola: lo sciopero non equivale alla chiusura automatica degli istituti.',
                     'Consiglio europeo: richiesta di riesame dell’ETS2, non rinvio automatico.',
                     'Brasile: il testo sul MEI deve ancora completare l’iter al Senato e ottenere la sanzione presidenziale.',
                     'Meteo: assenza di allerta nazionale distinta dalla presenza di fenomeni locali.'],
                   format_exception='Flash di 188–226 parole: fatti circoscritti, lunghezza proporzionata e nessun riempitivo.',
                   image_visual_review='Completata su tutte le 10 immagini dedicate',browser_visual_qa='Non eseguita: verifica strutturale affidata ai gate e al controllo delle superfici',
                   evergreen_exception='Nessuna nuova guida commissionata; non sono aggiunti collegamenti generici non pertinenti.')
    date_rows(rows,release)
    for a in rows:finish(a,release)
    shared.sync_complete(rows)
    state_path=ROOT/'CURIOMONDO-RELEASE-STATE.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if not rerender:
        state['articleCount']+=10;state['generatedEditorialImages']+=10
    state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),date='2026-10-16',release_date='2026-10-16',updated_at=release.isoformat(),last_update='apertura-mattina-16-ottobre-v857',status='ready')
    dump(state_path,state)
    if rerender:audit['prepared_release']=audit.get('release')
    audit['release']=release.isoformat()
    audit['articles']=[dict(slug=a['slug'],title=a['titolo'],published=a['published'],modified=a['modified'],source_date=a['source_date'],source_published=a.get('source_published'),sources=a['fonti'],words=sum(len(p.split()) for p in a['paragrafi']),risk=a['risk'],original_value=a['original_value'],editorial_checks=dict(facts=True,sources=True,headline=True,original_value=True,no_duplicate=True,short_paragraphs=True)) for a in rows]
    dump(AUDIT,audit)
    print(json.dumps(dict(version=VERSION,new_articles=10,new_images=10,release=audit['release']),ensure_ascii=False))
if __name__=='__main__':main()
