#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime
from email.utils import format_datetime, parsedate_to_datetime
from html import escape
from pathlib import Path
import json, re, shutil, zipfile
from lxml import etree, html

ROOT=Path(__file__).resolve().parents[1]
VERSION=247
DATE='2026-08-30'
DISCLOSURE='Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
TEMPLATE=ROOT/'notizie/affitto-genitori-separati-fondo-60-milioni-30-agosto-2026.html'

AARAU={
 'slug':'svizzera-sparatoria-rave-aarau-morto-cinque-feriti-30-agosto-2026',
 'title':'Svizzera, sparatoria durante un rave ad Aarau: un morto e cinque feriti, killer in fuga',
 'excerpt':'Spari intorno alle 02:30 durante l’Aarau Rave VOL. 7: un morto e cinque feriti, alcuni gravi. La polizia cantonale cerca il responsabile e chiede foto e video ai testimoni.',
 'section':'Mondo · Svizzera / Cronaca','category_meta':'Mondo / Svizzera / Cronaca',
 'published':'2026-08-30T07:43:00+02:00','updated':'2026-08-30T07:43:00+02:00','display':'30 agosto 2026 · 07:43',
 'image_base':'/assets/images/editorial-v247/aarau-rave-sparatoria-30-agosto-2026-ai',
 'image_alt':'Scena editoriale IA fotorealistica di un’area per eventi notturni ad Aarau presidiata dalla polizia svizzera dopo una grave emergenza, senza rappresentare vittime o il momento della sparatoria',
 'insight':[('1','vittima confermata'),('5','feriti, alcuni in condizioni gravi'),('02:30','orario indicativo dell’allarme alla polizia')],
 'body':[
  'Una sparatoria avvenuta nella notte ad Aarau, nel nord della Svizzera, ha provocato un morto e cinque feriti, alcuni dei quali in condizioni gravi. La polizia cantonale dell’Argovia ha confermato il bilancio nelle prime ore di domenica 30 agosto e ha avviato una vasta operazione per rintracciare il responsabile, che al momento dell’ultimo aggiornamento risultava ancora ricercato. Reuters e Associated Press hanno rilanciato la conferma delle autorità, trasformando le prime notizie frammentarie su “diverse vittime” in un quadro molto più definito.',
  'L’allarme è arrivato alla polizia poco dopo le 02:30. In quel momento nell’area dell’ippodromo del quartiere Schachen si stava svolgendo l’Aarau Rave VOL. 7. Secondo le informazioni riferite dalla polizia a SRF, gli spari hanno fatto scattare un grande dispiegamento di forze: la zona attorno all’ippodromo è stata isolata, i residenti sono stati invitati a tenersi lontani e la presenza delle pattuglie è stata rafforzata anche oltre l’area immediatamente interessata. Le autorità non hanno ancora chiarito il movente né la dinamica completa.',
  'Il punto centrale dell’indagine resta l’identificazione dell’autore. La polizia cantonale ha dichiarato che la ricerca della persona responsabile è in corso e ha rivolto un appello diretto a chi si trovava alla festa o nelle vicinanze: fotografie e filmati registrati durante o subito dopo gli spari potrebbero aiutare gli investigatori a ricostruire movimenti, direzioni di fuga e sequenza degli eventi. È una richiesta particolarmente importante in un luogo affollato, dove molti presenti possono avere ripreso involontariamente dettagli utili senza rendersene conto.',
  'Associated Press riferisce che la polizia è stata avvertita intorno alle 02:30 e che il rave era in corso presso l’ippodromo di Schachen. Il bilancio ufficiale è di una persona uccisa e cinque ferite, alcune gravemente. La stessa agenzia sottolinea che l’autore non era stato ancora individuato e che le possibili motivazioni restavano sconosciute. CurioMondo evita quindi di attribuire numero, identità o caratteristiche agli aggressori sulla base di testimonianze non confermate circolate nelle prime ore: fino a un aggiornamento ufficiale, il dato verificato è che la polizia cerca un responsabile non identificato.',
  'SRF descrive un dispositivo di sicurezza molto ampio. Oltre alla polizia cantonale e ai vigili del fuoco sono stati mobilitati diversi servizi di soccorso e il Kantonales Katastrophen Einsatzelement, l’unità cantonale impiegata nelle situazioni straordinarie. Nell’area è stato osservato anche un elicottero Super Puma dell’esercito svizzero; le autorità non avevano però specificato pubblicamente quale compito operativo gli fosse stato assegnato. La piscina di Aarau è stata temporaneamente chiusa mentre proseguivano le ricerche e il controllo del territorio.',
  'Una cosa utile da sapere: in una caccia all’uomo dopo una sparatoria, il perimetro di sicurezza non serve soltanto a impedire l’accesso alla scena del crimine. Permette agli investigatori di conservare tracce, separare i testimoni, controllare le vie di uscita e ridurre il rischio che una persona armata possa confondersi con il normale movimento della città. Per questo le chiusure possono estendersi ben oltre il punto in cui sono stati esplosi i colpi e continuare anche quando i feriti sono già stati trasferiti in ospedale.',
  'Aarau è la capitale del cantone Argovia e conta poco più di ventimila abitanti; si trova circa 46 chilometri a ovest di Zurigo. L’episodio ha quindi avuto un impatto immediato su una città relativamente compatta, dove un’operazione di polizia di queste dimensioni modifica rapidamente viabilità e accesso agli spazi pubblici. Le immagini diffuse dalle agenzie mostrano pattuglie e blocchi stradali nel centro e nei pressi del luogo dell’evento, ma il lavoro investigativo resta concentrato sulla zona del rave e sulle possibili vie di allontanamento.',
  'Reuters ricorda che la Svizzera presenta un livello di possesso di armi relativamente elevato rispetto a molti altri Paesi europei, pur registrando sparatorie violente di questo tipo con frequenza limitata. Nel 2019 gli elettori svizzeri approvarono un irrigidimento delle regole sulle armi. Questo contesto non consente però di trarre conclusioni sull’arma utilizzata ad Aarau, sulla sua provenienza o sulla posizione amministrativa del responsabile: nessuno di questi elementi è stato reso noto dalle autorità nell’aggiornamento disponibile.',
  'Le prime testimonianze raccolte dai media svizzeri descrivono momenti di forte confusione, con alcune persone che inizialmente avrebbero scambiato i colpi per fuochi d’artificio. Questi racconti aiutano a comprendere il clima vissuto sul posto, ma non devono essere usati per fissare il numero degli aggressori o ricostruire la traiettoria dei colpi senza riscontro investigativo. Nelle ore immediatamente successive a un evento con centinaia di presenti, testimonianze sincere possono essere incomplete o contraddirsi perché ciascuno osserva soltanto una porzione della scena.',
  'La notizia è diventata pubblicabile con maggiore solidità quando il bilancio ufficiale è passato dalle formule generiche delle prime comunicazioni a un morto e cinque feriti, accompagnato dalla conferma di una ricerca attiva del responsabile. È questo il salto informativo decisivo: non soltanto una segnalazione di spari a un evento, ma un caso di omicidio con più feriti e un’operazione di sicurezza ancora aperta. Reuters, AP e SRF convergono sui punti essenziali del quadro.',
  'Le prossime informazioni davvero rilevanti saranno l’eventuale fermo del sospettato, l’identificazione della vittima, l’evoluzione delle condizioni dei feriti e soprattutto la ricostruzione del movente. Fino ad allora è corretto distinguere ciò che è confermato da ciò che resta oggetto d’indagine. Al momento dell’ultimo controllo: una persona è morta, cinque sono rimaste ferite, alcune gravemente, e la polizia cantonale dell’Argovia sta ancora cercando l’autore degli spari avvenuti durante la notte ad Aarau.'
 ],
 'sources':[
  ('https://www.reuters.com/world/europe/several-victims-reported-swiss-rave-shooting-blick-says-2026-08-30/','Reuters — bilancio confermato di un morto e almeno cinque feriti, caccia al responsabile e appello per foto e video'),
  ('https://apnews.com/article/switzerland-shooting-rave-aargau-843e1c1cc57e1a0cb379851007ea6ba8','Associated Press — orario dell’allarme, Aarau Rave VOL. 7, feriti e ricerca del sospettato'),
  ('https://www.srf.ch/news/schweiz/hintergruende-noch-unklar-schuesse-in-aarau-1-todesopfer-5-verletzte','SRF — dettagli sul grande dispiegamento di sicurezza e sulle operazioni nell’area di Schachen')
 ],
 'related':[
  ('/notizie/svizzera-riprende-trasferimenti-migranti-italia-18-agosto-2026.html','Europa · Svizzera','Svizzera e Italia, riprendono i trasferimenti dei richiedenti asilo'),
  ('/notizie/thailandia-sparatoria-scuola-insegnante-ucciso-7-agosto-2026.html','Mondo · Cronaca','Thailandia, sparatoria in una scuola: ucciso un insegnante'),
  ('/notizie/thailandia-strage-scuola-governo-stretta-armi-8-agosto-2026.html','Mondo · Sicurezza','Thailandia, dopo la strage il governo prepara una stretta sulle armi')
 ],
 'source_note':'Testo originale CurioMondo. Bilancio verificato su Reuters, Associated Press e SRF; ultimo controllo editoriale: 30 agosto 2026, ore 07:43 italiane.'
}

SIRACUSA={
 'slug':'siracusa-rivolta-carcere-agenti-tetto-inchiesta-30-agosto-2026',
 'title':'Rivolta nel carcere di Siracusa, agenti costretti a lanciarsi dal tetto: dieci poliziotti in ospedale, chiesta un’inchiesta',
 'excerpt':'Nuovi dettagli sui disordini nel carcere di Siracusa: alcuni agenti sono saltati da circa quattro metri per sfuggire al lancio di pietre. I sindacati chiedono un’inchiesta sulla gestione dell’intervento.',
 'section':'Italia · Cronaca / Carceri / Sicurezza','category_meta':'Italia / Cronaca / Carceri / Sicurezza',
 'published':'2026-08-30T00:19:00+02:00','updated':'2026-08-30T00:19:00+02:00','display':'30 agosto 2026 · 00:19',
 'image_base':'/assets/images/editorial-v247/siracusa-carcere-rivolta-30-agosto-2026-ai',
 'image_alt':'Scena editoriale IA fotorealistica di un istituto penitenziario siciliano durante una situazione di emergenza, con agenti in sicurezza e senza mostrare ferite o il salto dal tetto',
 'insight':[('≈4 m','altezza indicata per il salto dal tetto'),('6–7','agenti saliti sul tetto con gli scudi'),('10','unità ospedalizzate citate nel nuovo resoconto ANSA')],
 'body':[
  'Emergono nuovi dettagli sulla rivolta avvenuta nel carcere di Siracusa e il quadro è più grave di quanto apparisse nelle prime ore. Alcuni agenti della polizia penitenziaria, saliti sul tetto dell’istituto durante i disordini, si sono lanciati da un’altezza di circa quattro metri per sottrarsi al lancio di pietre e altri oggetti. Hanno riportato traumi e contusioni e nessuno, secondo il resoconto diffuso da ANSA, risulta in pericolo di vita. La vicenda apre ora anche un confronto sulla gestione operativa dell’emergenza.',
  'I disordini risalgono a giovedì 27 agosto, ma il particolare del salto dal tetto è stato reso noto soltanto successivamente. Secondo la ricostruzione riportata dall’agenzia, un gruppo di detenuti ha forzato le recinzioni delle aree di passeggio ed è riuscito a raggiungere i tetti. Sono stati danneggiati pannelli fotovoltaici e dall’alto sono stati lanciati calcinacci, pietre, oggetti e sbarre di ferro contro il personale. Almeno sei o sette agenti sarebbero saliti sul tetto equipaggiati con scudi.',
  'È in quella fase che alcuni appartenenti al Corpo, temendo di essere colpiti, avrebbero scelto di scendere nel modo più rapido possibile saltando da circa quattro metri. Il dato aggiunge un elemento sostanziale alla notizia originaria perché sposta l’attenzione dalla sola protesta dei detenuti alle condizioni in cui il personale è stato impiegato. Il Sindacato di polizia penitenziaria chiede infatti di sapere chi abbia deciso, disposto o autorizzato la salita degli agenti sul tetto mentre i detenuti avevano a disposizione materiali da utilizzare come oggetti contundenti.',
  'Sul numero degli agenti coinvolti esiste una differenza tra i due resoconti ANSA pubblicati a distanza di due giorni e va segnalata con precisione. Il 28 agosto l’agenzia aveva riferito, citando l’Osapp, di undici agenti feriti e portati al pronto soccorso: sette a Siracusa e quattro ad Avola. Nel nuovo aggiornamento del 30 agosto, lo stesso sindacato parla di “ben dieci unità” della polizia penitenziaria mandate in ospedale mentre vengono descritti i salti dal tetto. CurioMondo mantiene entrambe le cifre attribuite alle rispettive comunicazioni, senza fingere che la discrepanza sia già stata chiarita.',
  'La protesta era iniziata nel pomeriggio e si è conclusa durante la notte. Nel primo resoconto, l’Osapp aveva spiegato che alcuni dei detenuti coinvolti erano in attesa di trasferimento e che per fronteggiare la situazione erano stati richiamati agenti fuori servizio e personale proveniente da altri istituti. All’esterno del carcere erano arrivati anche carabinieri, polizia e Guardia di finanza. Il provveditore dell’amministrazione penitenziaria Maurizio Veneziano aveva seguito direttamente la gestione della fase critica.',
  'Il nuovo passaggio è soprattutto istituzionale. Aldo Di Giacomo, segretario generale del Sindacato polizia penitenziaria, ha chiesto la rimozione del direttore e del comandante del carcere di Siracusa e l’apertura immediata di un’inchiesta amministrativa. Giuseppe Argentino, segretario provinciale dell’Osapp, ha chiesto invece di verificare se le procedure previste per affrontare una rivolta siano state applicate correttamente. Si tratta di richieste sindacali, non di conclusioni già raggiunte da un’autorità investigativa: eventuali responsabilità devono ancora essere accertate.',
  'Una cosa utile da sapere: la polizia penitenziaria non svolge soltanto funzioni di vigilanza statica nelle carceri. È un Corpo dello Stato con compiti di sicurezza degli istituti, gestione dell’ordine interno, traduzioni dei detenuti e partecipazione alle attività che rendono possibile l’esecuzione delle misure detentive. Nelle emergenze la catena di comando e le procedure operative sono cruciali perché ogni intervento deve bilanciare protezione del personale, tutela delle persone detenute, contenimento della violenza e ripristino dell’ordine.',
  'È proprio questo equilibrio a essere finito al centro delle domande dei sindacati. La questione non è soltanto se gli agenti siano riusciti a fermare la rivolta, ma se il modo in cui sono stati impiegati abbia esposto un numero limitato di persone a un rischio evitabile. Un’inchiesta amministrativa, se verrà effettivamente aperta, dovrebbe ricostruire ordini impartiti, tempi, disponibilità di equipaggiamento, numero di operatori presenti, richieste di rinforzi e decisioni prese durante le varie fasi dell’emergenza.',
  'Il caso di Siracusa arriva inoltre in un momento di forte pressione sul sistema penitenziario italiano. Negli stessi giorni, nella provincia, l’evasione di un detenuto dal carcere di Augusta aveva riacceso il dibattito su organici e sovraffollamento. Sono episodi distinti e non vanno collegati causalmente, ma mostrano perché la sicurezza degli istituti e le condizioni di lavoro della polizia penitenziaria siano tornate al centro dell’attenzione. Ogni struttura ha però numeri e criticità proprie, quindi il caso di Siracusa deve essere valutato sui fatti specifici della rivolta.',
  'Anche il linguaggio richiede cautela. Le informazioni disponibili derivano in larga parte dalle ricostruzioni dei sindacati della polizia penitenziaria riportate da ANSA. Non risultano, nell’aggiornamento utilizzato per questo articolo, una relazione amministrativa definitiva o un provvedimento che stabilisca responsabilità individuali. Per questo le accuse sulla gestione dell’intervento vengono presentate come richieste di chiarimento e non come fatti già accertati. La distinzione è essenziale soprattutto quando vengono chieste rimozioni di dirigenti.',
  'Resta invece acquisito il dato più impressionante del nuovo aggiornamento: alcuni agenti hanno lasciato il tetto saltando da circa quattro metri mentre erano esposti al lancio di oggetti. Il fatto che nessuno sia in pericolo di vita riduce fortunatamente la gravità sanitaria immediata, ma non quella organizzativa. Se personale dotato soltanto di scudi si è trovato in una posizione dalla quale il salto è apparso l’opzione più sicura, è ragionevole che la sequenza delle decisioni venga ricostruita in modo formale.',
  'I prossimi sviluppi da seguire sono quindi tre: l’eventuale apertura di un’inchiesta amministrativa, la risposta dell’amministrazione penitenziaria alle richieste dei sindacati e il chiarimento definitivo sul numero degli agenti feriti o ospedalizzati. Fino ad allora il quadro verificato resta quello di una rivolta con detenuti sui tetti, lancio di oggetti contro il personale, agenti costretti a saltare da circa quattro metri e una contestazione sindacale sulla gestione dell’operazione. È abbastanza per trasformare un episodio locale in un caso nazionale sulla sicurezza nelle carceri.'
 ],
 'sources':[
  ('https://www.ansa.it/sito/notizie/cronaca/2026/08/30/rivolta-in-carcere-a-siracusa-agenti-si-lanciano-dal-tetto-per-sfuggire-alle_59f33796-97f6-4121-a8ac-84d484f3b8f5.html','ANSA — nuovo dettaglio del salto dal tetto, richiesta di inchiesta e dieci unità indicate come ospedalizzate'),
  ('https://www.ansa.it/sicilia/notizie/2026/08/28/detenuti-sui-tetti-per-protesta-undici-agenti-feriti-nel-carcere_a22e6f0e-c778-4089-b494-594ede667459.html','ANSA Sicilia — primo resoconto della rivolta, undici agenti feriti e intervento di rinforzi')
 ],
 'related':[
  ('/notizie/perugia-esplosione-palazzina-crolla-tetto-due-feriti-gravi-22-agosto-2026.html','Italia · Cronaca','Perugia, esplosione in una palazzina: crolla il tetto e due persone restano ferite gravemente'),
  ('/notizie/difterite-palermo-cuginetto-positivo-paziente-zero-22-agosto-2026.html','Italia · Sicilia','Palermo, nuovo sviluppo sul caso di difterite'),
  ('/notizie/italia-spagna-scontro-controlli-frontiere-crisi-ceuta.html','Italia · Politica','Italia e Spagna, scontro sui controlli alle frontiere')
 ],
 'source_note':'Testo originale CurioMondo. ANSA ha riportato 11 agenti feriti il 28 agosto e, nel successivo resoconto del 30 agosto, 10 unità mandate in ospedale: la differenza viene mantenuta esplicitamente finché non sarà chiarita da una fonte ufficiale.'
}

STORIES=[AARAU,SIRACUSA]
NEW=STORIES

def dump(path,obj,compact=False):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':') if compact else None,indent=None if compact else 2)+'\n',encoding='utf-8')

def write(path,text): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')
def url(story): return f"/notizie/{story['slug']}.html"
def canonical(story): return 'https://curiomondo.it'+url(story)
def image(story,w=800): return f"{story['image_base']}-{w}.webp"
def srcset(story): return f"{image(story,480)} 480w, {image(story,800)} 800w, {image(story,1200)} 1200w"
def date_label(story): return story['updated'][:10]
def entry(story):
 return {'title':story['title'],'excerpt':story['excerpt'],'url':url(story),'section':story['section'],'dateISO':story['updated'],'dateLabel':date_label(story),'image':image(story,800),'imageAlt':story['image_alt'],'imageWidth':800,'imageHeight':533,'srcset':srcset(story)}

def set_meta(doc, attr, key, value):
 n=doc.xpath(f'//meta[@{attr}="{key}"]')
 if n: n[0].set('content',value)

def set_article(story):
 path=ROOT/f"notizie/{story['slug']}.html"
 doc=html.fromstring(TEMPLATE.read_text(encoding='utf-8'))
 doc.xpath('//title')[0].text=story['title']+' | CurioMondo'
 set_meta(doc,'name','description',story['excerpt']); set_meta(doc,'property','og:title',story['title']); set_meta(doc,'property','og:description',story['excerpt']); set_meta(doc,'property','og:url',canonical(story)); set_meta(doc,'property','og:image','https://curiomondo.it'+image(story,1200)); set_meta(doc,'property','og:image:alt',story['image_alt'])
 doc.xpath('//link[@rel="canonical"]')[0].set('href',canonical(story))
 schema={'@context':'https://schema.org','@type':'NewsArticle','headline':story['title'],'description':story['excerpt'],'datePublished':story['published'],'dateModified':story['updated'],'mainEntityOfPage':canonical(story),'inLanguage':'it-IT','author':{'@type':'Organization','name':'Redazione CurioMondo'},'publisher':{'@type':'Organization','name':'CurioMondo','logo':{'@type':'ImageObject','url':'https://curiomondo.it/curiomondo-logo-512.png'}},'image':['https://curiomondo.it'+image(story,1200)]}
 doc.xpath('//script[@type="application/ld+json"]')[0].text=json.dumps(schema,ensure_ascii=False,separators=(',',':'))
 doc.xpath('//body')[0].set('data-article-id',story['slug'])
 doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," badge ")]')[0].text=story['section']
 doc.xpath('//h1')[0].text=story['title']
 doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')[0].text=story['excerpt']
 meta=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0]
 for c in list(meta): meta.remove(c)
 meta.text=f"{story['display']} · {story['category_meta']} · "; sp=etree.SubElement(meta,'span',id='readTime'); sp.text='5 min di lettura'
 fig=doc.xpath('//figure[contains(concat(" ",normalize-space(@class)," ")," article-image ")]')[0]
 fig.attrib.clear(); fig.set('class','article-image'); fig.set('data-ai-generated','true')
 pic=fig.xpath('./picture')[0]; img=pic.xpath('.//img')[0]
 img.set('src','..'+image(story,800)); img.set('srcset',f"..{image(story,480)} 480w, ..{image(story,800)} 800w, ..{image(story,1200)} 1200w"); img.set('alt',story['image_alt']); img.set('width','800'); img.set('height','533'); img.set('loading','eager'); img.set('fetchpriority','high'); img.set('decoding','async'); img.set('sizes','(max-width:832px) calc(100vw - 32px),800px')
 cap=fig.xpath('./figcaption')[0] if fig.xpath('./figcaption') else etree.SubElement(fig,'figcaption'); cap.text=DISCLOSURE
 ed=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," editorial-data ")]')[0]
 for c in list(ed): ed.remove(c)
 d1=etree.SubElement(ed,'div'); st=etree.SubElement(d1,'strong'); st.text='Keyword principale:'; st.tail=' '+story['title'].split(':')[0]
 d2=etree.SubElement(ed,'div'); st=etree.SubElement(d2,'strong'); st.text='URL SEO:'; st.tail=' '+url(story)
 ins=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-insight ")]')[0]
 newi=html.fragment_fromstring('<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"></div></section>'); grid=newi.xpath('.//div')[0]
 for b,small in story['insight']:
  d=etree.SubElement(grid,'div'); be=etree.SubElement(d,'b'); be.text=b; sm=etree.SubElement(d,'small'); sm.text=small
 ins.getparent().replace(ins,newi)
 art=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
 art.attrib.clear(); art.set('class','art-body'); art.set('data-length-policy','5000-7000')
 for c in list(art): art.remove(c)
 for ptxt in story['body']:
  p=etree.SubElement(art,'p'); p.text=ptxt
 sources=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]')[0]
 old=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," curio-related ")]')
 rh='<section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">'
 for u,cat,t in story['related']: rh+=f'<a href="{u}"><span>{escape(cat)}</span><strong>{escape(t)}</strong></a>'
 rh+='</div></section>'; rel=html.fragment_fromstring(rh)
 if old: old[0].getparent().replace(old[0],rel)
 else: sources.addprevious(rel)
 ul=sources.xpath('./ul')[0]
 for c in list(ul): ul.remove(c)
 for u,label in story['sources']:
  li=etree.SubElement(ul,'li'); a=etree.SubElement(li,'a',href=u,rel='noopener noreferrer',target='_blank'); a.text=label
 sm=sources.xpath('.//small')
 if sm: sm[0].text=story['source_note']
 for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'): link.set('href','../assets/css/curiomondo-article-v211.css?v=247')
 for sc in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'): sc.set('src','../assets/js/curiomondo-article-v210.js?v=247')
 write(path,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))
 dump(ROOT/f"contenuti/notizie/{story['slug']}.json",{'slug':story['slug'],'title':story['title'],'excerpt':story['excerpt'],'category':story['section'],'published_at':story['published'],'updated_at':story['updated'],'body':story['body'],'related':[u for u,_,_ in story['related']],'sources':[{'url':u,'label':l} for u,l in story['sources']],'image':{'key':Path(story['image_base']).name,'alt':story['image_alt'],'ai_generated':True,'documentary_photo':False,'disclosure':DISCLOSURE}})

def update_data():
 hp=ROOT/'assets/data/home-feed-v210.json'; h=json.loads(hp.read_text(encoding='utf-8')); h['version']=VERSION
 urls={url(s) for s in STORIES}; items=[x for x in h['items'] if x.get('url') not in urls]; items.extend(entry(s) for s in STORIES); items.sort(key=lambda x:str(x.get('dateISO','')),reverse=True); h['items']=items; dump(hp,h,True)
 sp=ROOT/'assets/data/search-index-v210.json'; s=json.loads(sp.read_text(encoding='utf-8')); s['version']=VERSION
 si=[x for x in s['items'] if x.get('url') not in urls]
 for st in reversed(STORIES): si.insert(0,{k:entry(st)[k] for k in ('title','excerpt','url','section')})
 s['items']=si; dump(sp,s,True)
 lp=ROOT/'automation/live-seed.json'; live=json.loads(lp.read_text(encoding='utf-8')); live['updated_at']='2026-08-30T06:53:00+00:00'; news=[x for x in items if x.get('url','').startswith('/notizie/')]; live['items']=[{'title':x['title'],'url':x['url'],'published_at':x['dateISO'],'source':'CurioMondo','article_exists':True} for x in news[:10]]; dump(lp,live)

def picture(item,eager=False):
 loading='eager' if eager else 'lazy'; fp=' fetchpriority="high"' if eager else ''; sizes='(max-width:600px) 79vw,300px'
 return f'<picture><img alt="{escape(item["imageAlt"],quote=True)}" decoding="async" loading="{loading}" height="533" sizes="{sizes}" src="{item["image"]}" srcset="{item["srcset"]}" width="800"{fp}></picture>'

def update_home():
 p=ROOT/'index.html'; doc=html.fromstring(p.read_text(encoding='utf-8')); items=json.loads((ROOT/'assets/data/home-feed-v210.json').read_text(encoding='utf-8'))['items']; news=[x for x in items if x.get('url','').startswith('/notizie/')]
 for ti,track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
  for c in list(track): track.remove(c)
  for it in news[:10]:
   a=etree.SubElement(track,'a',href=it['url']); a.set('class','ticker-news'); a.text=it['title'];
   if ti==1: a.set('tabindex','-1')
 # Keep Nepal as Ultima Ora: editorial priority 10/10 outranks Aarau 9/10.
 nepal_url='/notizie/nepal-tibet-alluvioni-oltre-350-morti-1300-dispersi-27-agosto-2026.html'; nepal=next(x for x in news if x['url']==nepal_url)
 hero=doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]; hero.set('href',nepal['url'])
 for c in list(hero): hero.remove(c)
 hero.append(html.fragment_fromstring(picture(nepal,True))); txt=etree.SubElement(hero,'div'); txt.set('class','txt'); tag=etree.SubElement(txt,'span'); tag.set('class','tag'); tag.text='Ultima ora'; h1=etree.SubElement(txt,'h1'); h1.text=nepal['title']; pp=etree.SubElement(txt,'p'); pp.text=nepal['excerpt']; cta=etree.SubElement(txt,'span'); cta.set('class','cta'); cta.text='Leggi l’articolo →'
 rail=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
 for c in list(rail): rail.remove(c)
 for it in news[:5]: rail.append(html.fragment_fromstring(f'<a class="auto-card" href="{it["url"]}">{picture(it)}<div class="abody"><div class="ameta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
 cards=doc.xpath('//div[@id="cards"]')[0]
 for c in list(cards): cards.remove(c)
 for it in news[5:23]: cards.append(html.fragment_fromstring(f'<a class="card" href="{it["url"]}">{picture(it)}<div class="body"><div class="meta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
 for sc in doc.xpath('//script[contains(@src,"home-v210.js")]'): sc.set('src','/assets/js/home-v210.js?v=247')
 write(p,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))

def update_archive():
 p=ROOT/'notizie/index.html'; doc=html.fromstring(p.read_text(encoding='utf-8')); ul=doc.xpath('//main//ul')[0]; urls={url(s) for s in STORIES}
 existing=[]
 for li in list(ul):
  a=li.xpath('./a')
  if not a: continue
  href=a[0].get('href'); strong=a[0].xpath('./strong'); span=a[0].xpath('./span'); existing.append((href,strong[0].text_content() if strong else a[0].text_content(),span[0].text_content() if span else ''))
 byhref={h:(t,d) for h,t,d in existing if h not in urls}
 for st in STORIES: byhref[url(st)]=(st['title'],date_label(st))
 for c in list(ul): ul.remove(c)
 feed=json.loads((ROOT/'assets/data/home-feed-v210.json').read_text(encoding='utf-8'))['items']; order=[x for x in feed if x.get('url','').startswith('/notizie/')]; seen=set()
 for it in order:
  href=it['url']
  if href in byhref and href not in seen:
   t,d=byhref[href]; ul.append(html.fragment_fromstring(f'<li><a href="{href}"><strong>{escape(t)}</strong><span>{escape(d)}</span></a></li>')); seen.add(href)
 for href,t,d in existing:
  if href not in seen and href not in urls:
   ul.append(html.fragment_fromstring(f'<li><a href="{href}"><strong>{escape(t)}</strong><span>{escape(d)}</span></a></li>')); seen.add(href)
 doc.xpath('//main/p')[0].text=f"{len(ul.xpath('./li'))} articoli, ordinati per data."
 write(p,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))

def update_feed():
 p=ROOT/'feed.xml'; parser=etree.XMLParser(remove_blank_text=False); tree=etree.parse(str(p),parser); ch=tree.getroot().find('channel'); urls={canonical(s) for s in STORIES}
 for it in list(ch.findall('item')):
  if it.findtext('link') in urls: ch.remove(it)
 for st in STORIES:
  it=etree.Element('item')
  for n,v in [('title',st['title']),('link',canonical(st)),('guid',canonical(st)),('pubDate',format_datetime(datetime.fromisoformat(st['updated']))),('description',st['excerpt'])]: etree.SubElement(it,n).text=v
  ch.append(it)
 items=list(ch.findall('item'))
 def dtkey(x):
  try: return parsedate_to_datetime(x.findtext('pubDate'))
  except Exception: return datetime(1970,1,1).astimezone()
 items.sort(key=dtkey,reverse=True)
 for it in list(ch.findall('item')): ch.remove(it)
 for it in items: ch.append(it)
 p.write_bytes(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def update_sitemaps():
 sns='http://www.sitemaps.org/schemas/sitemap/0.9'; nns='http://www.google.com/schemas/sitemap-news/0.9'; parser=etree.XMLParser(remove_blank_text=False)
 sp=ROOT/'sitemap.xml'; stree=etree.parse(str(sp),parser); root=stree.getroot()
 for story in STORIES:
  can=canonical(story); nodes=stree.xpath('//s:url[s:loc=$loc]',namespaces={'s':sns},loc=can)
  node=nodes[0] if nodes else etree.SubElement(root,f'{{{sns}}}url')
  loc=node.find(f'{{{sns}}}loc')
  if loc is None: loc=etree.SubElement(node,f'{{{sns}}}loc')
  loc.text=can; lm=node.find(f'{{{sns}}}lastmod')
  if lm is None: lm=etree.SubElement(node,f'{{{sns}}}lastmod')
  lm.text=DATE
 sp.write_bytes(etree.tostring(stree,encoding='utf-8',xml_declaration=True,pretty_print=True))
 np=ROOT/'news-sitemap.xml'; ntree=etree.parse(str(np),parser); nroot=ntree.getroot()
 for story in STORIES:
  can=canonical(story); nodes=ntree.xpath('//s:url[s:loc=$loc]',namespaces={'s':sns},loc=can)
  if nodes: node=nodes[0]
  else:
   node=etree.Element(f'{{{sns}}}url'); etree.SubElement(node,f'{{{sns}}}loc').text=can; news=etree.SubElement(node,f'{{{nns}}}news'); pub=etree.SubElement(news,f'{{{nns}}}publication'); etree.SubElement(pub,f'{{{nns}}}name').text='CurioMondo'; etree.SubElement(pub,f'{{{nns}}}language').text='it'; etree.SubElement(news,f'{{{nns}}}publication_date').text=story['published']; etree.SubElement(news,f'{{{nns}}}title').text=story['title']; nroot.insert(0,node)
 np.write_bytes(etree.tostring(ntree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def update_release():
 for fn in ['RELEASE-STATE.json','CURIOMONDO-RELEASE-STATE.json']:
  p=ROOT/fn
  if not p.exists(): continue
  d=json.loads(p.read_text(encoding='utf-8'))
  if fn=='RELEASE-STATE.json': d.update({'currentVersion':VERSION,'baselineVersion':246,'status':'ready','date':DATE,'site_version':VERSION,'version':str(VERSION),'baseline_version':246,'baseline':'curiomondo-v246-nepal-750-affitti-bollette-30-agosto-2026-netlify.zip','last_update':'aarau-shooting-siracusa-prison-v247','release_date':DATE,'articleCount':d.get('articleCount',193)+2,'generatedEditorialImages':d.get('generatedEditorialImages',74)+2})
  else: d.update({'site_version':VERSION,'baseline_version':246,'version':str(VERSION),'date':DATE,'baseline':'curiomondo-v246-nepal-750-affitti-bollette-30-agosto-2026-netlify.zip','last_update':'aarau-shooting-siracusa-prison-v247','performance_pass':'Due nuovi visual WebP responsive; LIVE 10, Notizie di oggi 5, nessun build Netlify.'})
  dump(p,d)
 mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site_version']=VERSION; m['version']='v247'; m['release_version']='v247'; m['last_release_date']=DATE; m['last_release']={'version':VERSION,'date':DATE,'baseline_version':246,'news_added':[AARAU['slug'],SIRACUSA['slug']],'news_updated':[],'daily_question_preserved':'quanto-di-te-stai-rendendo-piu-piccolo-per-non-mettere-a-disagio-gli-altri','library_guides_preserved':['come-scaricare-video-youtube','come-fare-backup-whatsapp-foto-pc'],'image_policy_applied':'two-new-ai-editorial-visuals-v247'}; dump(mp,m)
 notes='''# CurioMondo v247 — 30 agosto 2026\n\n- Aggiunto il nuovo articolo sulla sparatoria durante l’Aarau Rave VOL. 7: un morto, cinque feriti e responsabile ancora ricercato; fonti incrociate Reuters, Associated Press e SRF.\n- Aggiunto il nuovo articolo sulla rivolta nel carcere di Siracusa con il dettaglio degli agenti costretti a saltare dal tetto e le richieste sindacali di un’inchiesta.\n- Nel caso Siracusa è esplicitata la differenza tra il primo resoconto ANSA (11 agenti feriti) e il successivo riferimento a 10 unità ospedalizzate, senza appiattire dati non perfettamente coincidenti.\n- Creati due nuovi visual editoriali IA dedicati, senza testo editoriale nei pixel pubblicati e con disclosure obbligatoria nelle pagine articolo.\n- Nepal–Tibet resta in Ultima Ora per priorità editoriale 10/10; Aarau entra in testa alla LIVE per recenza. Aggiornati Notizie di oggi, Altre notizie, archivio, ricerca, feed RSS, sitemap e News Sitemap.\n- Preservati Domanda del giorno ed eBook/guide della v245-v246.\n'''; write(ROOT/'RELEASE-NOTES-v247.md',notes)

def qa():
 errors=[]; report={}
 for st in STORIES:
  p=ROOT/f"notizie/{st['slug']}.html"; txt=p.read_text(encoding='utf-8'); doc=html.fromstring(txt); body_chars=sum(len(x) for x in st['body'])
  checks={'body_chars':body_chars,'body_ok':5000<=body_chars<=7000,'h1_ok':doc.xpath('//h1')[0].text_content()==st['title'],'sources':len(doc.xpath('//div[contains(@class,"art-sources")]//li')),'related':len(doc.xpath('//section[contains(@class,"curio-related")]//a')),'image_480':(ROOT/image(st,480).lstrip('/')).exists(),'image_800':(ROOT/image(st,800).lstrip('/')).exists(),'image_1200':(ROOT/image(st,1200).lstrip('/')).exists(),'disclosure':DISCLOSURE in txt,'canonical':canonical(st) in txt,'jsonld':st['title'] in txt}
  report[st['slug']]=checks
  if not all([checks['body_ok'],checks['h1_ok'],checks['related']==3,checks['image_480'],checks['image_800'],checks['image_1200'],checks['disclosure'],checks['canonical'],checks['jsonld']]): errors.append((st['slug'],checks))
 home=html.fromstring((ROOT/'index.html').read_text(encoding='utf-8')); tracks=home.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]'); rail=home.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0].xpath('./a'); cards=home.xpath('//div[@id="cards"]')[0].xpath('./a'); hero=home.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
 h={'live':len(tracks[0].xpath('./a')),'today':len(rail),'other':len(cards),'hero_nepal':hero.get('href')=='/notizie/nepal-tibet-alluvioni-oltre-350-morti-1300-dispersi-27-agosto-2026.html','live_first_aarau':tracks[0].xpath('./a')[0].get('href')==url(AARAU),'unique_today_other':len({a.get('href') for a in rail+cards})==len(rail+cards)}; report['home']=h
 if h!={'live':10,'today':5,'other':18,'hero_nepal':True,'live_first_aarau':True,'unique_today_other':True}: errors.append(('home',h))
 # Daily question must remain current.
 m=json.loads((ROOT/'curiomondo-site-manifest.json').read_text(encoding='utf-8')); report['daily_question_current']=m.get('daily_state',{}).get('last_question_date')==DATE
 if not report['daily_question_current']: errors.append(('daily_question',m.get('daily_state')))
 # No deploy/build config regression.
 forbidden=[x for x in ('netlify.toml','package.json') if (ROOT/x).exists()]; report['forbidden_deploy_files']=forbidden
 if forbidden: errors.append(('forbidden',forbidden))
 if errors: raise RuntimeError(errors)
 return report

def main():
 for st in STORIES: set_article(st)
 update_data(); update_home(); update_archive(); update_feed(); update_sitemaps(); update_release()
 q=qa(); write(ROOT/'QA-REPORT-v247.md', '# QA CurioMondo v247 — 30 agosto 2026\n\n- Pre-deploy static audit: 0 errori.\n- Nuovi articoli: Aarau rave; rivolta carcere Siracusa.\n- Homepage: Ultima Ora = Nepal–Tibet; Notizie di oggi = 5; LIVE = 10; Altre notizie = 18.\n- Aarau è prima nella LIVE per recenza; Nepal–Tibet resta hero per priorità 10/10.\n- Due nuovi visual editoriali IA responsive (480/800/1200 WebP) con disclosure presente.\n- NewsArticle JSON-LD, canonical, feed, ricerca, archivio, sitemap e News Sitemap aggiornati.\n- Domanda del giorno del 30 agosto e Biblioteca preservate.\n- Pacchetto deploy-only: nessun netlify.toml o package.json.\n')
 print(json.dumps({'version':VERSION,'checks':q},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
