#!/usr/bin/env python3
"""Apertura 15 ottobre: dieci notizie e meteo, ZIP senza push.

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
VERSION=853
BATCH=ROOT/'tools/news_batch_20261015_v853.json'
IMAGES=ROOT/'tools/news_images_20261015_v853.json'
AUDIT=ROOT/'tools/news_audit_20261015_v853.json'
OFFSETS=(0,5,12,20,29,39,50,62,75,89,105)

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
    assert release.date().isoformat()=='2026-10-15','Per un altro giorno riverificare tutte le informazioni.'
    assert len(rows)==len(OFFSETS)==11
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
            'Puoi rivedere un impegno se nel frattempo sono cambiate le tue esigenze.',
            'Prima di rispondere a una richiesta puoi controllare se hai tempo.',
            'Puoi lasciare libera una sera della settimana per riposarti.',
            'Se un lavoro ti sembra troppo puoi chiedere da dove cominciare.',
            'Puoi ritagliarti qualche minuto per chiamare una persona a cui tieni.',
            'Puoi avvisare che farai tardi senza inventare una scusa.',
            'Se hai cambiato idea puoi dirlo con gentilezza.',
            'Puoi lasciare una conversazione in sospeso finché trovi le parole.',
            'Puoi chiedere una pausa quando fai fatica a concentrarti.',
            'Puoi tenere del tempo per una passeggiata senza altre commissioni.',
            'Puoi riparare un piccolo errore senza giudicare tutta la tua giornata.',
        ):
            if phrase not in phrases:phrases.append(phrase)
        _,used=nome_pensiero.used(ROOT)
        assert sum(p not in used for p in phrases)>=11
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
        audit=dict(version=VERSION,new_articles=11,updated_articles=0,new_images=11,
                   request='10 articoli più meteo — apertura completa del 15 ottobre',
                   push_executed=False,manifest_accessed=False,
                   baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                   source_list='Fonti per la ricerca degli articoli.txt, 7 ottobre 2026',
                   primary_access_limits=['Fonti vigili del fuoco: documenti ufficiali integrali consultati in copie ospitate da TiConsiglio.',
                     'GRIM: avviso ufficiale indicizzato, apertura in timeout; nota integrale ripresa da Molise News 24.',
                     'Viminale e Prefettura Asti: aperture non disponibili; atto comunale e cronaca della presentazione consultati.',
                     'Venezuela: comunicazione diretta delle parti non recuperata. Conferme ANSA e RTVE/EFE; esclusi i numeri controversi sui detenuti.',
                     'INGV: nessun evento urgente della notte sufficientemente verificato per un articolo; nessuna deduzione dai sismogrammi.'],
                   exclusions=['Avvisi di sciopero toscani del 14 ottobre già scaduti.',
                     'Richiesta Usa sugli asset russi: conferme insufficienti per un fatto autonomo.',
                     'Giappone, sottomarini e mercati: non inseriti senza i riscontri necessari.'],
                   corrections=['Brasile: transizione di due mesi a 42 ore e ulteriori dodici mesi a 40 dopo promulgazione.',
                     'Venezuela: avvio il 14 locale; nessuna data elettorale dichiarata come già concordata.',
                     'Asti: il calendario operativo riportato dalla presentazione copre 19–23 ottobre; il Viminale indica un quadro 19–25. Titolo limitato all’avvio il 19.',
                     'Riccia: ore 6 come termine programmato, non attestazione di effettivo ripristino.',
                     'Meteo: bollettino di allerta distinto dalla previsione; dal 19 al 22 nessun dettaglio giornaliero inventato.'],
                   format_exception='Flash di 136–226 parole: fatti circoscritti, lunghezza proporzionata e nessun riempitivo.',
                   image_visual_review='Da completare',browser_visual_qa='Da completare',
                   evergreen_exception='Nessuna nuova guida commissionata; non sono aggiunti collegamenti generici non pertinenti.')
    date_rows(rows,release)
    for a in rows:finish(a,release)
    shared.sync_complete(rows)
    state_path=ROOT/'CURIOMONDO-RELEASE-STATE.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if not rerender:
        state['articleCount']+=11;state['generatedEditorialImages']+=11
    state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),date='2026-10-15',release_date='2026-10-15',updated_at=release.isoformat(),last_update='apertura-mattina-15-ottobre-v853',status='ready')
    dump(state_path,state)
    if rerender:audit['prepared_release']=audit.get('release')
    audit['release']=release.isoformat()
    audit['articles']=[dict(slug=a['slug'],title=a['titolo'],published=a['published'],modified=a['modified'],source_date=a['source_date'],source_published=a.get('source_published'),sources=a['fonti'],words=sum(len(p.split()) for p in a['paragrafi']),risk=a['risk'],original_value=a['original_value'],editorial_checks=dict(facts=True,sources=True,headline=True,original_value=True,no_duplicate=True,short_paragraphs=True)) for a in rows]
    dump(AUDIT,audit)
    print(json.dumps(dict(version=VERSION,new_articles=11,new_images=11,release=audit['release']),ensure_ascii=False))
if __name__=='__main__':main()
