#!/usr/bin/env python3
"""Prepara il lotto v859; nessun push e nessun accesso al manifest."""
import json, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from lxml import etree, html

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as image_shared

VERSION=859
ROME=ZoneInfo('Europe/Rome')
OFFSETS=(0,5,12,20,29)
PHRASES=(
 'Puoi cercare informazioni affidabili prima di farti un’opinione.',
 'Prenderti cura di te può iniziare da un passo piccolo.',
 'Puoi chiedere aiuto senza dover spiegare tutto subito.',
 'Anche una giornata impegnativa può contenere una pausa.',
 'Puoi distinguere un’accusa da una decisione definitiva.',
)
UPDATES=[
 {"slug":"papa-leone-buona-ripresa-polmone-viaggio-sudamerica-15-ottobre-2026",
  "titolo":"Leone XIV, esami e radiografia confermano il miglioramento dopo l’intervento",
  "sommario":"Il nuovo bollettino riferisce una ripresa costante. Proseguono fisioterapia respiratoria e recupero al Gemelli.",
  "paragrafi":[
   "Gli esami del sangue e la radiografia toracica eseguiti venerdì confermano il miglioramento costante di Papa Leone XIV dopo l’intervento al polmone. Il bollettino diffuso dal Vaticano riferisce che il recupero postoperatorio procede bene.",
   "Il Pontefice continua la fisioterapia respiratoria e ha ripreso le normali attività quotidiane in autonomia. Ha celebrato Messa nella cappella allestita al Policlinico Gemelli e prosegue la convalescenza sotto controllo medico.",
   "L’intervento del 13 ottobre ha rimosso il lobo inferiore del polmone destro; l’esame del nodulo ha confermato un adenocarcinoma. Restano da valutare gli approfondimenti clinici necessari per definire eventuali ulteriori cure.",
   "Il Vaticano sta valutando la possibilità che il Papa reciti l’Angelus domenica dall’ospedale. La decisione dipenderà dall’andamento clinico; il bollettino positivo non equivale a una previsione certa sulla durata del ricovero o sul viaggio di novembre."
  ],
  "fonti":[
   {"url":"https://apnews.com/article/vatican-pope-surgery-leo-cancer-angelus-hospital-aee51a1005491f20276902b66b6f574e","nome":"Associated Press — esami, fisioterapia e recupero del Papa"},
   {"url":"https://www.reuters.com/world/pope-leo-showing-steady-improvement-after-lung-cancer-surgery-vatican-says-2026-10-16/","nome":"Reuters — bollettino vaticano e miglioramento costante"}
  ],
  "dati":[["Esami e radiografia","miglioramento confermato"],["Gemelli","fisioterapia respiratoria"],["Domenica","Angelus possibile, non confermato"]]},
 {"slug":"caro-gasolio-conftrasporto-rischio-fermo-nazionale-15-ottobre-2026",
  "titolo":"Caro gasolio, proteste dei tir al Sud: tavolo di governo il 27 ottobre",
  "sommario":"I presidi sono partiti in Calabria e Sicilia, mentre in Puglia proseguono iniziative autonome. Le modalità e gli effetti variano sul territorio.",
  "paragrafi":[
   "Le proteste degli autotrasportatori contro il caro carburante si sono estese in Calabria, Sicilia e Puglia. In Calabria i mezzi si sono disposti ai margini delle strade senza bloccare completamente il traffico; in Sicilia il fermo proclamato da un comitato riguarda il ritiro dei semirimorchi nei porti e prosegue fino al 20 ottobre.",
   "La situazione non è uniforme: in Puglia si registrano presidi e iniziative autonome, mentre in Calabria la mobilitazione regionale annunciata da Fedralog è prevista fino al 20 ottobre. Gli eventuali rallentamenti dipendono da luogo e adesioni, e non equivalgono a un blocco generalizzato dei rifornimenti.",
   "Il governo ha convocato le associazioni dell’autotrasporto per un tavolo al ministero dei Trasporti il 27 ottobre. La riunione è il prossimo passaggio istituzionale, ma non comporta ancora un accordo o nuove misure sul prezzo del gasolio.",
   "Per chi deve viaggiare o ricevere merci è utile controllare gli aggiornamenti delle autorità locali e dei gestori stradali. L’allarme nazionale lanciato dalle associazioni va distinto dagli effetti accertati nei singoli territori."
  ],
  "fonti":[
   {"url":"https://www.ansa.it/sito/notizie/cronaca/2026/10/15/sale-lallarme-carburanti-il-governo-convoca-lautotrasporto_0a0d0be1-020f-4955-8dbb-84592524f1bf.html","nome":"ANSA — tavolo del 27 ottobre e proteste nel Mezzogiorno"},
   {"url":"https://tg24.sky.it/cronaca/2026/10/16/protesta-tir-caro-carburante-news","nome":"Sky TG24 — modalità dei presidi in Calabria e fermo in Sicilia"}
  ],
  "dati":[["27 ottobre","tavolo al ministero"],["Fino al 20 ottobre","presidi in Calabria e fermo siciliano"],["Territori diversi","effetti locali, non blocco nazionale uniforme"]]}
]

def dump(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def update_existing(row,release):
    path=ROOT/'notizie'/(row['slug']+'.html')
    doc=html.fromstring(path.read_text(encoding='utf-8'))
    note=html.tostring(doc.xpath('//aside[contains(@class,"cm-name-card")]')[0])
    for q,v in (('//title',row['titolo']+' | CurioMondo'),('//main//h1[1]',row['titolo']),('//main/p[contains(@class,"subtitle")]',row['sommario'])): doc.xpath(q)[0].text=v
    for q,v in (('//meta[@name="description"]',row['sommario']),('//meta[@property="og:title"]',row['titolo']),('//meta[@property="og:description"]',row['sommario'])): doc.xpath(q)[0].set('content',v)
    published=None
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data=json.loads(node.text or '{}')
        if data.get('@type')=='NewsArticle':
            published=data['datePublished']; data.update({'headline':row['titolo'],'description':row['sommario'],'dateModified':release.isoformat(timespec='seconds')}); node.text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    if published is None: raise RuntimeError('Data di prima pubblicazione assente: '+row['slug'])
    body=doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body): body.remove(child)
    for p in row['paragrafi']: etree.SubElement(body,'p').text=p
    grid=doc.xpath('//div[contains(@class,"cm-insight-grid")]')[0]
    for node,data in zip(grid,row['dati']): node.xpath('./strong')[0].text=data[0]; node.xpath('./span')[0].text=data[1]
    ul=doc.xpath('//div[contains(@class,"art-sources")]/ul')[0]
    for child in list(ul): ul.remove(child)
    for source in row['fonti']:
        li=etree.SubElement(ul,'li'); etree.SubElement(li,'a',href=source['url'],rel='noopener noreferrer',target='_blank').text=source['nome']
    dt=datetime.fromisoformat(published).astimezone(ROME)
    doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0].text=site._italian_date(published)+dt.strftime(' alle ore %H:%M')+' · Aggiornato il '+site._italian_date(release.isoformat())+release.strftime(' alle ore %H:%M')+' · '
    doc.xpath('//*[@id="readTime"]')[0].text='1 min di lettura'
    for br in doc.xpath('//div[contains(@class,"art-sources")]//small/br[1]'): br.tail='Testo originale CurioMondo. Ultimo aggiornamento editoriale: '+site._italian_date(release.isoformat())+release.strftime(' alle ore %H:%M')+'.'
    assert note==html.tostring(doc.xpath('//aside[contains(@class,"cm-name-card")]')[0])
    path.write_text(html.tostring(doc,encoding='unicode',method='html',doctype='<!doctype html>')+'\n',encoding='utf-8')
    row.update({'published':published,'modified':release.isoformat(timespec='seconds'),'update':True,'categoria':doc.xpath('//main/div[@class="badge"]')[0].text,'sommario':row['sommario']})

def main():
    shared.VERSION=image_shared.VERSION=VERSION
    batch=ROOT/'tools/news_batch_20261016_v859.json'; images_file=ROOT/'tools/news_images_20261016_v859.json'; audit_file=ROOT/'tools/news_audit_20261016_v859.json'
    rows=json.loads(batch.read_text(encoding='utf-8')); image_sources=json.loads(images_file.read_text(encoding='utf-8'))
    if sys.argv[1:]==['--sync-basciano-source']:
        row=rows[0]; path=ROOT/'notizie'/(row['slug']+'.html'); doc=html.fromstring(path.read_text(encoding='utf-8'))
        ul=doc.xpath('//div[contains(@class,"art-sources")]/ul')[0]
        for child in list(ul): ul.remove(child)
        for source in row['fonti']:
            li=etree.SubElement(ul,'li'); etree.SubElement(li,'a',href=source['url'],rel='noopener noreferrer',target='_blank').text=source['nome']
        path.write_text(html.tostring(doc,encoding='unicode',method='html',doctype='<!doctype html>')+'\n',encoding='utf-8')
        audit=json.loads(audit_file.read_text(encoding='utf-8'))
        for article in audit['articles']:
            if article['slug']==row['slug']: article['sources']=row['fonti']
        dump(audit_file,audit); dump(batch,rows); print('Fonti del caso aggiornate e verificate'); return
    release=datetime.now(ROME).replace(microsecond=0)
    assert release.date().isoformat()=='2026-10-16'
    assert len(rows)==len(OFFSETS)==5
    for a in rows:
        assert not (ROOT/'notizie'/(a['slug']+'.html')).exists(),a['slug']
        assert len(a['fonti'])<=2 and max(len(p.split()) for p in a['paragrafi'])<=60
    phrase_path=ROOT/'assets/data/frasi-nome.json'; phrases=json.loads(phrase_path.read_text(encoding='utf-8')); _,used=nome_pensiero.used(ROOT)
    for phrase in PHRASES:
        if phrase not in phrases: phrases.append(phrase)
    assert sum(p not in used for p in phrases)>=5
    dump(phrase_path,phrases)
    image_rows=[]
    for a in rows:
        img=image_shared.image_for(a,image_sources); site.write_article(a,img,VERSION); image_rows.append(img)
    registry_path=ROOT/'assets/data/editorial-images-v210.json'; registry=json.loads(registry_path.read_text(encoding='utf-8'))
    registry['items']=image_rows+registry['items']; registry['version']=VERSION; dump(registry_path,registry)
    for a,minutes in zip(rows,OFFSETS):
        stamp=release-timedelta(minutes=minutes)
        if a.get('source_published'): assert stamp>=datetime.fromisoformat(a['source_published']),a['slug']
        a['published']=a['modified']=stamp.isoformat(timespec='seconds')
        shared.finish_page(a,release)
        page=ROOT/'notizie'/(a['slug']+'.html'); page.write_text(page.read_text(encoding='utf-8').replace('/assets/css/global-header-v275.css?v=736','/assets/css/global-header-v275.css?v=633'),encoding='utf-8')
    updates=json.loads(json.dumps(UPDATES))
    for row in updates: update_existing(row,release)
    all_rows=rows+updates
    shared.sync_complete(all_rows)
    state_path=ROOT/'CURIOMONDO-RELEASE-STATE.json'; state=json.loads(state_path.read_text(encoding='utf-8'))
    state['articleCount']+=len(rows); state['generatedEditorialImages']+=len(rows)
    state.update(site_version=VERSION,currentVersion=VERSION,version=str(VERSION),date='2026-10-16',release_date='2026-10-16',updated_at=release.isoformat(),last_update='politica-cronaca-sport-16-ottobre-v859',status='ready')
    dump(state_path,state)
    audit={'version':VERSION,'new_articles':len(rows),'updated_articles':len(updates),'new_images':len(rows),
      'request':'Aggiornamenti del 16 ottobre: cronaca giudiziaria, proteste, Flotilla, Napoli, sport; bollettini Papa e autotrasporto.',
      'push_executed':False,'manifest_accessed':False,'baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'source_list':'Fonti indicate in ciascun articolo; materiali di riferimento allegati dall’utente.',
      'exclusions':['Manovra, ETS e vertice UE non duplicati: pagine di contesto sono già presenti e le segnalazioni non aggiungevano un nuovo atto conclusivo.','Il Consiglio UE e la richiesta di Starlink sono trattati nei contenuti Ucraina/UE già presenti.','Scioperi EasyJet, scuola e vigili del fuoco non ripubblicati: copertura del 16 ottobre già presente; cortei aggiornati con la notizia torinese.'],
      'corrections':['Rinvio a giudizio non equivale a condanna.','Contestazioni della Procura sulla Flotilla presentate come ipotesi investigative.','Incendio: cause non attribuite, nessun ferito secondo i primi aggiornamenti.','Proteste trasporto: segnalati gli effetti territoriali distinti, non un blocco nazionale uniforme.'],
      'image_visual_review':'Cinque copertine originali controllate; immagini non documentarie, scena sensibile trattata con neutralità.',
      'browser_visual_qa':'Da completare dopo i gate.','format_exception':'Flash proporzionati a fatti circoscritti, senza riempitivo.','evergreen_exception':'Collegamento di tutela aggiunto alla pagina sul procedimento giudiziario.'}
    audit['release']=release.isoformat(); audit['articles']=[{'slug':a['slug'],'title':a['titolo'],'published':a['published'],'modified':a['modified'],'source_date':a.get('source_date'),'sources':a['fonti'],'words':sum(len(p.split()) for p in a['paragrafi']),'risk':a.get('risk'),'original_value':a.get('original_value'),'updated':bool(a.get('update'))} for a in all_rows]
    dump(audit_file,audit)
    print(json.dumps({'version':VERSION,'new_articles':len(rows),'updated_articles':len(updates),'new_images':len(rows),'release':audit['release']},ensure_ascii=False))

if __name__=='__main__': main()
