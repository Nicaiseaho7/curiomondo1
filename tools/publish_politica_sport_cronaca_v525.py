#!/usr/bin/env python3
"""Pubblica quattro notizie verificate e aggiorna quattro articoli esistenti."""
from __future__ import annotations

import hashlib, json, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import etree, html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 525
ROME = ZoneInfo("Europe/Rome")
NOW = datetime.now(ROME).replace(microsecond=0).isoformat()
IMAGES = {
    "milano-indossa-kippa-presidio-piazza-san-carlo-22-settembre-2026": ROOT.parent / "generated_images/exec-039cdcdd-df2c-45a1-afdc-c710e930cc92.png",
    "juventus-multa-10000-euro-minuto-silenzio-mazzola-22-settembre-2026": ROOT.parent / "generated_images/exec-49b007e3-1894-46cf-a7ec-6409235b9f1a.png",
    "fenerbahce-virtus-bologna-eurolega-25-settembre-2026": ROOT.parent / "generated_images/exec-3fc336ab-1990-4616-857e-a013cb2ec6ab.png",
    "davis-cup-italia-corea-sud-quarti-bologna-25-novembre-2026": ROOT.parent / "generated_images/exec-e5f6273c-9b44-4c1f-afb3-7b9e742dbdc3.png",
}

ARTICLES = [
 {
  "slug":"milano-indossa-kippa-presidio-piazza-san-carlo-22-settembre-2026","titolo":"Milano indossa la kippà: in piazza contro l’antisemitismo","sommario":"Il presidio in piazza San Carlo riunisce la Comunità ebraica e rappresentanti delle istituzioni dopo l’aggressione a un rabbino in zona Bande Nere.","categoria":"Cronaca","luogo":"Milano","formato":"standard","parole_chiave_titolo":["Milano","kippà"],"dati_chiave":[{"valore":"22 settembre","etichetta":"data del presidio"},{"valore":"Piazza San Carlo","etichetta":"luogo della manifestazione"},{"valore":"16 settembre","etichetta":"aggressione al rabbino"}],
  "paragrafi":[
   "Centinaia di persone hanno partecipato martedì 22 settembre al presidio “Milano indossa la kippà” in piazza San Carlo. La Comunità ebraica milanese ha promosso l’iniziativa dopo l’aggressione subita il 16 settembre da un rabbino alla fermata dell’autobus di piazza Bande Nere.",
   "Molti partecipanti hanno indossato la kippà in segno di solidarietà. Il rabbino capo di Milano, Alfonso Arbib, ha chiesto che gli ebrei possano vivere con tranquillità e che gli episodi antisemiti non vengano minimizzati o giustificati con motivazioni politiche.",
   "Il presidente della Comunità ebraica di Milano, Walker Meghnagi, ha convocato il presidio come risposta pubblica all’aggressione. Alla manifestazione hanno preso parte rappresentanti politici locali e nazionali, esponenti della società civile e cittadini non appartenenti alla comunità.",
   "Secondo le ricostruzioni disponibili, l’episodio che ha preceduto la manifestazione è avvenuto in zona Bande Nere. La protesta non era rivolta contro una singola istituzione: l’obiettivo dichiarato era chiedere una presa di posizione condivisa contro l’odio antisemita.",
   "Arbib ha collegato la sicurezza quotidiana alla possibilità di esprimere apertamente la propria identità. Dal palco sono arrivati anche richiami alle istituzioni nazionali e al Presidente della Repubblica, nel quadro di un appello pubblico e non di una procedura formale.",
   "Il numero dei presenti varia nelle cronache, che parlano comunque di alcune centinaia di persone. CurioMondo evita una cifra puntuale non certificata dalle autorità e distingue il dato osservato dalle valutazioni politiche espresse durante il presidio.",
   "L’iniziativa si inserisce nel dibattito sulla crescita degli episodi antisemiti in Italia. La qualificazione giuridica dell’aggressione e le eventuali responsabilità individuali spettano agli investigatori e all’autorità giudiziaria, non agli organizzatori della manifestazione.",
  ],
  "fonti":[{"url":"https://www.mosaico-cem.it/comunita/news/martedi-22-settembre-in-piazza-san-carlo-manifestazione-di-solidarieta-dopo-lultimo-attacco-antisemita/","descrizione":"Mosaico – Comunità ebraica di Milano: convocazione, luogo e motivazioni del presidio."},{"url":"https://www.alanews.it/2026/09/22/cronaca/video/rabbino-aggredito-a-milano-la-comunita-ebraica-scende-in-piazza-mattarella-prenda-posizione/","descrizione":"Alanews – dichiarazioni di Alfonso Arbib e partecipanti alla manifestazione."},{"url":"https://tg24.sky.it/cronaca/2026/09/22/milano-presidio-kippa-rabbino-aggredito","descrizione":"Sky TG24 – ricostruzione del presidio e dell’aggressione precedente."}],
 },
 {
  "slug":"juventus-multa-10000-euro-minuto-silenzio-mazzola-22-settembre-2026","titolo":"Juventus multata di 10mila euro per il minuto di silenzio su Mazzola","sommario":"Il Giudice sportivo sanziona il club per il comportamento di una parte della Tribuna Sud prima della gara con l’Atalanta; ammenda attenuata dalla presa di posizione della società.","categoria":"Sport","luogo":"Torino","formato":"standard","parole_chiave_titolo":["10mila euro","Mazzola"],"dati_chiave":[{"valore":"10.000 €","etichetta":"ammenda alla Juventus"},{"valore":"Tribuna Sud","etichetta":"settore indicato"},{"valore":"1° anello","etichetta":"area dello Stadium"}],
  "paragrafi":[
   "Il Giudice sportivo della Serie A ha inflitto alla Juventus un’ammenda di 10mila euro per quanto accaduto durante il minuto di silenzio dedicato a Sandro Mazzola prima della partita casalinga contro l’Atalanta.",
   "Il provvedimento riguarda un gruppo definito numericamente esiguo di sostenitori della Tribuna Sud, primo anello. Secondo il dispositivo, i tifosi non hanno rispettato platealmente il minuto di raccoglimento disposto dalla FIGC.",
   "Le cronache della gara riferiscono che alcuni sostenitori si sono voltati di spalle al terreno di gioco e hanno intonato cori dedicati ad altre figure della storia juventina. La sanzione è rivolta alla società secondo le regole di responsabilità applicate alle condotte del pubblico.",
   "L’ammenda è stata attenuata per due elementi indicati dal Giudice sportivo: la tempestiva presa di posizione formale della Juventus contro il comportamento e la dissociazione del resto del pubblico presente allo Stadium.",
   "La decisione non comprende la chiusura del settore né altri provvedimenti disciplinari. I 10mila euro rappresentano quindi l’intera sanzione comunicata per questo episodio, distinta dalle valutazioni politiche e morali emerse dopo la partita.",
   "Sandro Mazzola è morto il 19 settembre a 83 anni. Ex capitano e simbolo dell’Inter e della Nazionale, era stato ricordato dalla Lega Serie A come una figura centrale della storia del calcio italiano.",
   "Il comunicato disciplinare stabilisce la conseguenza sportiva dell’episodio, ma non attribuisce la condotta all’intera tifoseria. La stessa motivazione evidenzia sia la dimensione limitata del gruppo sia la reazione contraria del resto dello stadio.",
  ],
  "fonti":[{"url":"https://www.legaseriea.it/lega-serie-a/documentazione","descrizione":"Lega Serie A – documentazione e comunicati ufficiali del Giudice sportivo."},{"url":"https://www.rainews.it/articoli/2026/09/oltraggio-al-minuto-di-silenzio-per-mazzola-multa-di-10-mila-euro-alla-juventus-345f6505-5a72-4a1c-959b-fb07bf0ffe33.html","descrizione":"RaiNews – importo della sanzione e ricostruzione dell’episodio."},{"url":"https://sport.sky.it/calcio/serie-a/2026/09/22/juve-multa-minuto-silenzio-mazzola","descrizione":"Sky Sport – motivazione e circostanze attenuanti indicate dal Giudice sportivo."}],
 },
 {
  "slug":"fenerbahce-virtus-bologna-eurolega-25-settembre-2026","titolo":"EuroLeague, la Virtus debutta a Istanbul contro il Fenerbahçe","sommario":"La prima gara europea dei bolognesi è in programma venerdì 25 settembre alle 19:45 sul campo del Fenerbahçe. Il calendario ufficiale corregge l’indicazione della gara in casa.","categoria":"Sport","luogo":"Istanbul","formato":"standard","parole_chiave_titolo":["Virtus","Fenerbahçe"],"dati_chiave":[{"valore":"25 settembre","etichetta":"data della partita"},{"valore":"19:45","etichetta":"orario italiano"},{"valore":"Istanbul","etichetta":"gara in trasferta"}],
  "paragrafi":[
   "La Virtus Bologna apre la propria EuroLeague 2026-2027 venerdì 25 settembre a Istanbul contro il Fenerbahçe. Il calendario ufficiale del club fissa la palla a due alle 19:45, ora italiana.",
   "La gara è indicata come Fenerbahçe–Virtus Bologna: si gioca quindi in Turchia e non a Bologna. La precisazione è importante perché alcune anticipazioni circolate online hanno invertito l’ordine delle squadre.",
   "Per la Virtus l’esordio propone subito una trasferta contro una delle formazioni di riferimento del basket europeo. Il dato certo alla vigilia riguarda programma, sede e orario; convocati e quintetti dipenderanno dalle decisioni tecniche comunicate più vicino alla partita.",
   "Il calendario della competizione impone alle squadre italiane una stagione lunga, con trasferte europee alternate agli impegni nazionali. La gestione dei recuperi diventa quindi rilevante già nelle prime settimane, ma non consente di anticipare rotazioni o minutaggi.",
   "La partita di Istanbul rappresenta il primo riferimento ufficiale della nuova campagna europea bolognese. Eventuali variazioni di orario, copertura televisiva o disponibilità dei giocatori dovranno essere verificate sui canali del club e dell’EuroLeague.",
   "L’Olimpia Milano affronta a sua volta la nuova stagione europea, ma CurioMondo non unisce alla gara della Virtus date non confermate dalla pagina ufficiale milanese consultata. Il calendario dei due club va letto separatamente per evitare sovrapposizioni.",
   "La prima giornata offre un test immediato sul livello della Virtus, senza però determinare da sola l’andamento della stagione. In EuroLeague la continuità lungo il calendario conta più del risultato isolato dell’esordio.",
  ],
  "fonti":[{"url":"https://www.virtus.it/evento/fenerbahce-istanbul-vs-virtus-bologna-2026-09-25-1945/","descrizione":"Virtus Bologna – scheda ufficiale della partita del 25 settembre alle 19:45."},{"url":"https://www.virtus.it/calendari/calendario-eurolega-virtus-bologna/","descrizione":"Virtus Bologna – calendario EuroLeague 2026-2027."},{"url":"https://www.euroleaguebasketball.net/euroleague/","descrizione":"EuroLeague Basketball – portale ufficiale della competizione."}],
 },
 {
  "slug":"davis-cup-italia-corea-sud-quarti-bologna-25-novembre-2026","titolo":"Davis Cup, Italia-Corea del Sud nei quarti a Bologna","sommario":"Il sorteggio della Final 8 assegna agli azzurri la Corea del Sud. Il quarto di finale si giocherà il 25 novembre alla BolognaFiere Arena.","categoria":"Sport","luogo":"Bologna","formato":"standard","parole_chiave_titolo":["Italia-Corea del Sud","Bologna"],"dati_chiave":[{"valore":"25 novembre","etichetta":"quarto di finale azzurro"},{"valore":"24–29 novembre","etichetta":"durata della Final 8"},{"valore":"3 titoli","etichetta":"ultime edizioni vinte dall’Italia"}],
  "paragrafi":[
   "L’Italia affronterà la Corea del Sud nei quarti di finale della Davis Cup 2026. Il sorteggio svolto a Bologna ha fissato il debutto degli azzurri a mercoledì 25 novembre alla BolognaFiere Arena.",
   "La Final 8 è in programma dal 24 al 29 novembre. L’orario della sfida italiana sarà confermato successivamente dagli organizzatori, quindi la data è ufficiale mentre l’inizio della sessione non va ancora considerato definitivo.",
   "Gli azzurri arrivano all’appuntamento da campioni delle ultime tre edizioni. Il dato aumenta le aspettative, ma non modifica la formula a eliminazione diretta: la vincente del quarto proseguirà verso la semifinale.",
   "La Corea del Sud partecipa per la prima volta alla Final 8 con il formato attuale. Italia e Corea del Sud si sono già affrontate tre volte in Davis Cup e gli azzurri hanno vinto tutti i precedenti, l’ultimo nei Qualifiers del 2020 a Cagliari.",
   "La composizione delle squadre sarà comunicata più avanti. Il sorteggio definisce l’accoppiamento, non garantisce la presenza dei singoli tennisti: convocazioni, condizioni fisiche e scelte dei capitani resteranno da verificare.",
   "La FITP indica SuperTennis e SuperTennis Plus come emittenti in chiaro della Final 8. Programmazione dettagliata e orari potranno essere aggiornati quando sarà completato lo schedule delle sessioni.",
   "Bologna ospita nuovamente la fase conclusiva del torneo. La concentrazione di tutti i quarti nella stessa arena riduce gli spostamenti e rende ogni giornata decisiva, con la finale prevista domenica 29 novembre.",
  ],
  "fonti":[{"url":"https://preprod-fitp.fitp.it/Federazione/News/Attivita-internazionale/davis-cup-2026-tabellone-final-8-bologna","descrizione":"FITP – tabellone della Final 8 e data di Italia-Corea del Sud."},{"url":"https://www.fitp.it/Federazione/News/Attivita-internazionale/davis-cup-finals-2026-apertura-biglietteria","descrizione":"FITP – sede e date della Davis Cup Final 8 a Bologna."},{"url":"https://tickets.italy.daviscup.com/","descrizione":"Davis Cup Italia – portale ufficiale di biglietteria e informazioni sull’evento."}],
 },
]

ALTS = {
 ARTICLES[0]["slug"]:"Presidio editoriale IA in una piazza di Milano, con cittadini riuniti e alcune persone che indossano la kippà; scena non documentaria.",
 ARTICLES[1]["slug"]:"Stadio editoriale IA di Torino durante un minuto di silenzio prima di una partita di calcio; scena non documentaria.",
 ARTICLES[2]["slug"]:"Arena editoriale IA di Istanbul durante il riscaldamento prima di una partita europea di basket; scena non documentaria.",
 ARTICLES[3]["slug"]:"Arena editoriale IA di tennis a Bologna illuminata con i colori di Italia e Corea del Sud; scena non documentaria.",
}

def make_image(slug):
 im=Image.open(IMAGES[slug]).convert("RGB"); w,h=im.size; target=1.5
 if w/h>target:
  nw=round(h*target); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
 else:
  nh=round(w/target); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
 out=[]
 for width in (480,800,1200):
  p=ROOT/'assets/images/editorial-auto'/f'{slug}-v{VERSION}-{width}.webp'; im.resize((width,round(width/target)),Image.Resampling.LANCZOS).save(p,'WEBP',quality=87,method=6)
  out.append({'w':width,'src':f'/assets/images/editorial-auto/{p.name}','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 return {'key':f'{slug}-v{VERSION}','alt':ALTS[slug],'variants':out,'disclosure':site.CAPTION,'generator':'OpenAI image tool','sensitiveContext':False}

for a in ARTICLES:
 img=make_image(a['slug']); site.write_article(a,img,VERSION); site.register_image(img,a['slug'],VERSION)

def update_article(filename, paragraphs, sources):
 p=ROOT/'notizie'/filename; d=html.fromstring(p.read_text(encoding='utf-8'))
 body=d.xpath('//article[contains(@class,"art-body")]')[0]
 for text in paragraphs: etree.SubElement(body,'p').text=text
 ul=d.xpath('//div[contains(@class,"art-sources")]//ul')[0]
 for url,label in sources:
  li=etree.SubElement(ul,'li'); a=etree.SubElement(li,'a',href=url,rel='noopener noreferrer',target='_blank'); a.text=label
 for node in d.xpath('//script[@type="application/ld+json"]'):
  try: data=json.loads(node.text)
  except Exception: continue
  if isinstance(data,dict) and data.get('@type')=='NewsArticle': data['dateModified']=NOW; node.text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
 p.write_text(html.tostring(d,encoding='unicode',method='html',doctype='<!doctype html>')+'\n',encoding='utf-8')

update_article('convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026.html',[
 'Bryan Cristante ha lasciato il raduno per indisponibilità. Mancini ha chiamato Samuele Ricci, mentre l’uscita di Federico Dimarco ha portato alla convocazione di Matteo Ruggeri. Italia-Belgio resta in programma venerdì 25 settembre alle 20:45 allo Stadio Olimpico di Roma.'
],[('https://www.figc.it/it/nazionali/news/altro-forfait-tra-gli-azzurri-dimarco-lascia-il-raduno-a-coverciano-arriva-matteo-ruggeri-meln9cj8','FIGC – aggiornamenti sui forfait e sui sostituti nel raduno azzurro.')])
update_article('istat-deficit-2025-31-pil-italia-resta-procedura-ue-22-settembre-2026.html',[
 'Il ministro dell’Economia Giancarlo Giorgetti ha espresso rammarico per la mancata uscita anticipata e ha indicato il 2027 come nuovo obiettivo. Giorgia Meloni ha contestato l’interpretazione politica del dato, sostenendo che successive revisioni potrebbero modificare il quadro.',
 'Le dichiarazioni del governo non cambiano il valore certificato dall’Istat né la procedura europea in corso. L’eventuale uscita dipenderà dai conti successivi e dalla decisione delle istituzioni dell’Unione.'
],[('https://www.rainews.it/video/2026/09/litalia-resta-sotto-procedura-ue-giorgetti-prendiamo-atto-non-senza-rammarico-53275d9d-7b89-4d31-836f-26af83c04ed5.html','RaiNews – reazione di Giorgetti e obiettivo di uscita nel 2027.')])
update_article('meloni-in-arrivo-tetto-agli-stranieri-in-classe-e-divieto-di-burqa-a-scuola-20-09-2026.html',[
 'Il 22 settembre Meloni ha precisato che il tetto del 30% riguarderebbe gli studenti stranieri che non parlano italiano. Ha collegato la proposta all’obiettivo di evitare concentrazioni e creare classi più equilibrate.',
 'La premier ha richiamato due circolari firmate da Sergio Mattarella quando era ministro dell’Istruzione, nel 1989 e nel 1990. Quei documenti invitavano a distribuire gli studenti stranieri e prevedevano valutazioni affidate alle scuole: non coincidono automaticamente con il nuovo provvedimento, il cui testo resta da esaminare.'
],[('https://www.quirinale.it/it/discorso/intervento-presidente-repubblica-sergio-mattarella-cerimonia-inaugurazione-anno-scolastico-2026-2027-presso-istituto-omnicomprensivo-sergio-marchionne-occasione-deci','Quirinale – intervento di Mattarella sull’integrazione scolastica.'),('https://tg24.sky.it/politica/2026/09/22/scuola-tetto-stranieri-circolari-mattarella','Sky TG24 – contenuto delle circolari del 1989 e 1990 citate da Meloni.')])

cfg_path=ROOT/'assets/data/homepage-config-v504.json'; cfg=json.loads(cfg_path.read_text()) ; cfg['version']=VERSION
for i,a in enumerate(ARTICLES): cfg['articles'][f"/notizie/{a['slug']}.html"]={'firstPublishedAt':a['published'],'homepagePriority':88-i,'primaryCategory':a['categoria'].lower()}
cfg_path.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
site.sync_surfaces(ARTICLES,f"/notizie/{ARTICLES[0]['slug']}.html",VERSION)
manifest_path=ROOT/'curiomondo-site-manifest.json'; m=json.loads(manifest_path.read_text()); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; m['site_version']=VERSION; m['version']=f'v{VERSION}'; m['release_version']=f'v{VERSION}'; m['last_release']={'version':VERSION,'date':'2026-09-23','type':'politics-sport-crime','news_added':[a['slug'] for a in ARTICLES],'news_updated':['carta-dedicata-a-te-500-euro-4-novembre-2026','convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026','istat-deficit-2025-31-pil-italia-resta-procedura-ue-22-settembre-2026','meloni-in-arrivo-tetto-agli-stranieri-in-classe-e-divieto-di-burqa-a-scuola-20-09-2026'],'change':'Quattro nuove notizie verificate e aggiornamenti a quattro articoli esistenti'}; manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for name in ('CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json'):
 p=ROOT/name; s=json.loads(p.read_text()); s.update(site_version=VERSION,version=str(VERSION),currentVersion=VERSION,last_update='politica-sport-cronaca-v525'); p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'added':[a['slug'] for a in ARTICLES],'updated':4},ensure_ascii=False))
