#!/usr/bin/env python3
from pathlib import Path
from lxml import html, etree
import hashlib, json, runpy, re

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'notizie/alessandro-di-battista-ricoverato-cuba-trasferimento-avana-29-agosto-2026.html'
KEY='alessandro-di-battista-terapia-intensiva-avana-7-settembre-2026-ai-v306'
TITLE='Alessandro Di Battista resta in terapia intensiva a Cuba dopo l’intervento'
EXCERPT='L’intervento eseguito all’ospedale Hermanos Ameijeiras è riuscito secondo fonti vicine all’ex deputato. Di Battista rimane sedato e il rientro in Italia non ha ancora una data.'
CANONICAL='https://curiomondo.it/notizie/alessandro-di-battista-ricoverato-cuba-trasferimento-avana-29-agosto-2026.html'
CAPTION='Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
ALT='Ritratto editoriale neutrale di Alessandro Di Battista su sfondo scuro, somiglianza sintetica fotorealistica generata con IA per una notizia sanitaria sensibile'
BODY=[
"Alessandro Di Battista è ancora ricoverato in terapia intensiva all’ospedale Hermanos Ameijeiras dell’Avana dopo l’intervento chirurgico al quale è stato sottoposto il 5 settembre. Sky TG24 e il Corriere della Sera, citando fonti vicine all’ex deputato e fonti mediche, riferiscono che l’operazione è riuscita. Di Battista resta sedato e sotto osservazione; non è stata comunicata una data per il trasferimento in Italia.",
"La notizia aggiorna il quadro aperto il 28 agosto, quando Di Battista aveva accusato un forte mal di testa e un malore mentre si trovava a Cuba. Era stato ricoverato inizialmente a Santa Clara e poi trasferito nella capitale. Il 2 settembre aveva scritto di sentirsi meglio e aveva annunciato un rientro con aeroambulanza, ma il programma è stato successivamente annullato. L’associazione Schierarsi ha confermato il rinvio e ha chiesto discrezione e prudenza nella diffusione delle informazioni.",
"Le fonti disponibili non hanno reso pubblica una diagnosi. Non è quindi corretto collegare il malore o l’intervento a una patologia specifica, anche se alcuni siti hanno proposto ipotesi. Non sono stati diffusi un bollettino dell’ospedale cubano, il tipo di procedura eseguita, la durata prevista della degenza o una prognosi autorizzata dalla famiglia. CurioMondo limita l’aggiornamento ai fatti confermati da più testate e attribuisce chiaramente le informazioni.",
"La permanenza in terapia intensiva dopo un intervento indica che il paziente necessita di monitoraggio continuo e assistenza specialistica. Non permette, da sola, di stabilire se il quadro stia migliorando o peggiorando. Anche la sedazione può essere utilizzata nel decorso post-operatorio per ragioni differenti: senza una comunicazione dei medici non è possibile interpretarne durata, profondità o significato clinico nel caso di Di Battista.",
"Il Corriere riferisce che il decorso sarebbe al momento in linea con le aspettative e che la sedazione dovrebbe proseguire almeno per alcuni giorni. Queste indicazioni provengono da persone informate sulla situazione, non da un bollettino firmato e pubblicato dall’ospedale. La formulazione resta quindi prudente: l’intervento è indicato come riuscito, mentre l’evoluzione successiva deve ancora essere valutata dai sanitari.",
"Il trasferimento in Italia era stato organizzato con un’aeroambulanza privata coperta dall’assicurazione stipulata prima del viaggio. Un volo sanitario richiede che l’équipe valuti stabilità, necessità di monitoraggio, durata del tragitto e continuità dell’assistenza all’arrivo. La disponibilità di un velivolo non equivale all’autorizzazione clinica a partire. Dopo l’intervento, il rientro è stato rinviato e nessuna delle fonti consultate indica un nuovo calendario definitivo.",
"Due specialisti del Policlinico Gemelli di Roma — un neurochirurgo e un anestesista rianimatore — avevano raggiunto Cuba nei giorni precedenti per affiancare l’équipe locale. La loro presenza conferma il coordinamento sanitario, ma non consente di attribuire loro decisioni o valutazioni che non siano state rese pubbliche. Anche l’assistenza dell’ambasciata italiana riguarda i contatti istituzionali e gli aspetti logistici, non sostituisce le decisioni cliniche.",
"Nelle notizie sanitarie riguardanti una persona identificabile, l’assenza di dettagli non deve essere colmata con deduzioni. Espressioni come “intervento riuscito” descrivono l’esito tecnico iniziale riferito dalle fonti, ma non coincidono con guarigione, dimissione o prognosi favorevole. Allo stesso modo, il ricovero in terapia intensiva indica il livello di assistenza e non autorizza formule sensazionalistiche sul rischio per la vita.",
"Di Battista, 48 anni, è un ex deputato del Movimento 5 Stelle e il fondatore dell’associazione politica e culturale Schierarsi. Si trovava sull’isola per attività legate a reportage e documentari. Questi elementi spiegano l’interesse pubblico della notizia, ma le informazioni mediche rimangono dati personali particolarmente delicati. La richiesta di riservatezza avanzata dalle persone vicine va quindi rispettata anche quando il caso riceve ampia attenzione politica e mediatica.",
"Il prossimo aggiornamento sostanziale potrà riguardare la riduzione della sedazione, l’uscita dalla terapia intensiva, un bollettino autorizzato o una nuova decisione sul trasferimento. Fino ad allora restano confermati quattro punti: l’intervento è stato eseguito il 5 settembre all’Hermanos Ameijeras; le fonti lo descrivono come riuscito; Di Battista è ancora sedato in terapia intensiva; il rientro in Italia è rinviato senza una data pubblica."
]

d=html.fromstring(PATH.read_text(encoding='utf-8'))
d.xpath('//title')[0].text=TITLE+' | CurioMondo'
for xp,*val in [('//meta[@name="description"]','content',EXCERPT),('//meta[@property="og:title"]','content',TITLE),('//meta[@property="og:description"]','content',EXCERPT),('//meta[@property="og:image"]','content',f'https://curiomondo.it/assets/images/editorial-auto/{KEY}-1200.webp'),('//meta[@property="og:image:alt"]','content',ALT)]:
    nodes=d.xpath(xp)
    if nodes: nodes[0].set(val[0],val[1])
for node in d.xpath('//script[@type="application/ld+json"]'):
    try: obj=json.loads(node.text or '')
    except Exception: continue
    if isinstance(obj,dict) and obj.get('@type')=='NewsArticle':
        obj['headline']=TITLE; obj['description']=EXCERPT; obj['datePublished']='2026-09-07T21:35:00+02:00'; obj['dateModified']='2026-09-07T21:35:00+02:00'; obj['image']=[f'https://curiomondo.it/assets/images/editorial-auto/{KEY}-1200.webp']; node.text=json.dumps(obj,ensure_ascii=False,separators=(',',':')); break
main=d.xpath('//main[contains(@class,"wrap")]')[0]
main.xpath('./h1')[0].text=TITLE; main.xpath('./p[contains(@class,"subtitle")]')[0].text=EXCERPT
meta=main.xpath('./div[contains(@class,"meta")]')[0]; meta.clear(); meta.set('class','meta'); meta.text='7 settembre 2026 · aggiornato alle 21:35 · Italia / Salute / Politica · '; rt=etree.SubElement(meta,'span',id='readTime'); rt.text='5 min di lettura'
fig=main.xpath('./figure[contains(@class,"article-image")]')[0]; fig.clear(); fig.set('class','article-image'); fig.set('data-ai-generated','true'); fig.set('data-synthetic-likeness','public-figure'); fig.set('data-sensitive-context','true'); fig.set('data-portrait-format','neutral-isolated')
pic=etree.SubElement(fig,'picture'); img=etree.SubElement(pic,'img',src=f'../assets/images/editorial-auto/{KEY}-800.webp',srcset=f'../assets/images/editorial-auto/{KEY}-480.webp 480w, ../assets/images/editorial-auto/{KEY}-800.webp 800w, ../assets/images/editorial-auto/{KEY}-1200.webp 1200w',sizes='(max-width:832px) calc(100vw - 32px),800px',width='800',height='533',alt=ALT,loading='eager',decoding='async',fetchpriority='high'); cap=etree.SubElement(fig,'figcaption'); cap.text=CAPTION
ins=main.xpath('.//section[contains(@class,"cm-insight")]')[0]; ins.clear(); k=etree.SubElement(ins,'span',{'class':'cm-kicker'}); k.text='Il punto in tre dati'; grid=etree.SubElement(ins,'div',{'class':'cm-insight-grid'})
for a,b in [('5 settembre','la data dell’intervento'),('terapia intensiva','il reparto in cui resta ricoverato'),('nessuna data','il rientro in Italia resta rinviato')]:
    box=etree.SubElement(grid,'div'); strong=etree.SubElement(box,'strong'); strong.text=a; span=etree.SubElement(box,'span'); span.text=b
article=main.xpath('.//article[contains(@class,"art-body")]')[0]; article.clear(); article.set('class','art-body'); article.set('data-length-policy','3000-7000')
for text in BODY: p=etree.SubElement(article,'p'); p.text=text
sources=main.xpath('.//div[contains(@class,"art-sources")]')[0]; sources.clear(); sources.set('class','art-sources'); h=etree.SubElement(sources,'h2'); h.text='Fonti consultate'; ul=etree.SubElement(sources,'ul')
for url,label in [('https://tg24.sky.it/cronaca/2026/09/07/alessandro-di-battista-come-sta','Sky TG24 — 7 settembre 2026 — terapia intensiva, sedazione, intervento e rientro rinviato'),('https://www.corriere.it/politica/26_settembre_07/alessandro-di-battista-sedato-come-sta-1d3be906-68c0-40de-8508-7e136fa73xlk_amp.shtml','Corriere della Sera — 7 settembre 2026 — decorso riferito da fonti mediche e permanenza in terapia intensiva'),('https://www.rainews.it/articoli/2026/09/alessandro-di-battista-rinviato-il-rientro-da-cuba-lo-comunica-lassociazione-schierarsi-lex-esponente-m5s-b45d8278-d6ab-496b-800c-3bba4ae7a2f4.html','RaiNews — 6 settembre 2026 — cronologia, intervento e richiesta di riservatezza'),('https://www.ansa.it/sito/notizie/politica/2026/09/05/rinviato-il-rientro-di-di-battista-in-italia_ca390614-eeae-4384-8a18-65ab0b40699d.html','ANSA — 5 settembre 2026 — comunicazione ufficiale di Schierarsi sul rinvio')]:
    li=etree.SubElement(ul,'li'); a=etree.SubElement(li,'a',href=url,rel='noopener noreferrer',target='_blank'); a.text=label
p=etree.SubElement(sources,'p'); small=etree.SubElement(p,'small'); small.text='Redazione CurioMondo · Come lavoriamo. Testo originale CurioMondo. Ultimo aggiornamento editoriale: 7 settembre 2026, ore 21:35 italiane. '+CAPTION
PATH.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

rp=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(rp.read_text(encoding='utf-8')); variants=[]
for w in (480,800,1200):
    f=ROOT/'assets/images/editorial-auto'/f'{KEY}-{w}.webp'; variants.append({'w':w,'src':f'/assets/images/editorial-auto/{f.name}','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
reg['items']=[x for x in reg['items'] if x.get('article')!='/notizie/'+PATH.name]
reg['items'].insert(0,{'key':KEY,'article':'/notizie/'+PATH.name,'aiGenerated':True,'syntheticLikeness':'public-figure','sensitiveContext':True,'documentaryPhoto':False,'prompt':'Sensitive-context neutral editorial portrait of Alessandro Di Battista, isolated studio background, no hospital or medical depiction, no text.','variants':variants,'alt':ALT,'disclosure':CAPTION,'portraitOnly':True,'portraitFormat':'neutral-isolated','reenactedEvent':False})
reg['version']=306; rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runpy.run_path(str(ROOT/'tools/finalize_articles_20260906.py'),run_name='__main__')
for rel in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
    p=ROOT/rel; data=json.loads(p.read_text(encoding='utf-8')); data['version']=306; p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runpy.run_path(str(ROOT/'tools/generate_category_pages.py'),run_name='__main__')
mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=306; m['site']['site_version']=306; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ok','updated':'/'+str(PATH.relative_to(ROOT))},ensure_ascii=False))
