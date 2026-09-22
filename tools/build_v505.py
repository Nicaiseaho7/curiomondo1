#!/usr/bin/env python3
from pathlib import Path
from html import escape
from PIL import Image
from lxml import etree, html
import hashlib, json, email.utils
from datetime import datetime

ROOT=Path(__file__).resolve().parents[1]
VERSION=505
CAPTION="Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
IMG_SRC=ROOT.parent/'generated_images'

ARTICLES=[
{
 'slug':'carburanti-italia-benzina-diesel-aumenti-eurostat-agosto-2026',
 'title':'Carburanti, in Italia benzina +6,3% e diesel +5,2% in un mese',
 'excerpt':'Eurostat misura i rincari tra luglio e agosto 2026. Nell’UE i carburanti costano il 23,8% in più rispetto a un anno prima.',
 'published':'2026-09-22T12:20:00+02:00','date':'22 settembre 2026','place':'Lussemburgo','category':'Italia / Economia','primary':'italia','priority':100,
 'key':'carburanti-italia-aumenti-eurostat-agosto-2026-v505','src':'exec-ef4d1866-10d0-47f0-ada9-59a8a80166ec.png',
 'alt':'Illustrazione editoriale generata con IA di una stazione di servizio in Italia con automobili e pompe di carburante; non è una fotografia documentaria.',
 'stats':[('6,3%','aumento mensile della benzina in Italia'),('5,2%','aumento mensile del diesel in Italia'),('23,8%','rincaro annuo dei carburanti nell’UE')],
 'body':[
 'In Italia il prezzo della benzina è aumentato del 6,3% tra luglio e agosto 2026, mentre il diesel è salito del 5,2%. I dati pubblicati il 22 settembre da Eurostat collocano il rincaro italiano della benzina tra i più elevati dell’Unione europea nel mese considerato.',
 'Il dato misura la variazione dell’indice armonizzato dei prezzi al consumo per carburanti e lubrificanti destinati al trasporto personale. Non rappresenta quindi il prezzo assoluto mostrato da una singola stazione di servizio, ma il movimento medio rilevato con una metodologia comune nei Paesi dell’UE.',
 'Su base annua, nell’Unione i carburanti e i lubrificanti costavano ad agosto il 23,8% in più rispetto allo stesso mese del 2025. L’aumento aveva raggiunto il 13,7% a giugno e il 16,9% a luglio, segnalando un’accelerazione durante l’estate.',
 'Il diesel è aumentato su base mensile in 26 Paesi. I rialzi maggiori sono stati registrati in Cechia, con il 14,3%, Bulgaria, con il 13,5%, e Lussemburgo, con il 12,3%. L’Italia, con il 5,2%, compare invece tra i tre incrementi più contenuti insieme a Romania e Paesi Bassi.',
 'Per la benzina, 22 Paesi hanno registrato aumenti, tre diminuzioni e due prezzi sostanzialmente stabili. La Spagna guida la variazione mensile con l’8,2%, seguita da Romania al 6,6%, Italia al 6,3% e Cipro al 6,2%.',
 'Il confronto mostra che benzina e diesel non si sono mossi nello stesso modo nei diversi mercati nazionali. Fiscalità, contratti di fornitura, composizione della distribuzione e tempi di trasferimento delle quotazioni possono modificare la velocità con cui uno shock energetico arriva ai consumatori.',
 'I dati di settembre saranno necessari per capire se l’aumento di agosto sia proseguito oppure si sia attenuato. La rilevazione Eurostat fotografa il mese già concluso e non costituisce una previsione dei prezzi alla pompa nelle prossime settimane.'
 ],
 'sources':[('https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250922-1','Eurostat — 22 settembre 2026 — variazioni annuali e mensili dei carburanti nell’UE.'),('https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_minr/default/table','Eurostat Data Browser — indice armonizzato mensile dei prezzi al consumo.')]
},
{
 'slug':'importazioni-petrolio-ue-valore-56-percento-volume-stabile-q2-2026',
 'title':'Petrolio, l’UE paga il 55,8% in più con volumi quasi stabili',
 'excerpt':'Nel secondo trimestre le importazioni petrolifere sono cresciute soltanto dell’1,2% in quantità. Stati Uniti, Norvegia e Kazakistan restano i principali fornitori.',
 'published':'2026-09-22T12:18:00+02:00','date':'22 settembre 2026','place':'Lussemburgo','category':'Economia / Energia','primary':'economia','priority':95,
 'key':'importazioni-petrolio-ue-valore-volume-q2-2026-v505','src':'exec-6d123af6-eb4c-4f22-91d5-d178c388995d.png',
 'alt':'Illustrazione editoriale generata con IA di una petroliera in un porto energetico europeo con serbatoi e condotte; non è una fotografia documentaria.',
 'stats':[('55,8%','aumento del valore importato'),('1,2%','crescita del volume di petrolio'),('36,7 mln t','volume medio mensile nel trimestre')],
 'body':[
 'Il valore delle importazioni di petrolio dell’Unione europea è aumentato del 55,8% nel secondo trimestre del 2026, mentre i volumi sono rimasti quasi stabili. Eurostat calcola una media mensile di 36,7 milioni di tonnellate, superiore dell’1,2% alla media del 2025.',
 'La distanza tra valore e quantità indica che l’UE ha sostenuto un costo molto più elevato senza aumentare in misura comparabile il petrolio acquistato. Il dato non misura da solo la spesa di famiglie e imprese, ma descrive la pressione esercitata sui conti commerciali europei.',
 'Gli Stati Uniti hanno fornito il 18,8% delle importazioni petrolifere europee nel trimestre. Seguono Norvegia con il 14,3% e Kazakistan con il 13,4%. La graduatoria dei maggiori fornitori non è cambiata rispetto alle rilevazioni precedenti richiamate da Eurostat.',
 'Per il gas naturale liquefatto il valore importato è cresciuto del 4,1%, mentre il volume è diminuito del 5,6%. Il 63,2% del GNL è arrivato dagli Stati Uniti, il 17,3% dalla Russia e l’8,1% dall’Algeria.',
 'Il gas trasportato in forma gassosa ha registrato aumenti sia in valore, pari al 18,5%, sia in volume, pari al 3,4%. La Norvegia copre il 51,2% delle forniture, davanti ad Algeria, Regno Unito e Russia.',
 'Le percentuali sui fornitori descrivono la composizione degli acquisti e non implicano che ogni Paese europeo dipenda nello stesso modo dalle singole origini. Terminali, gasdotti, raffinerie e contratti nazionali distribuiscono l’esposizione in maniera diversa.',
 'Le prossime rilevazioni chiariranno se lo scarto tra costo e quantità sia temporaneo o persistente. Un ritorno dei valori verso i volumi ridurrebbe la pressione commerciale; un divario prolungato manterrebbe elevato il costo dell’approvvigionamento energetico.'
 ],
 'sources':[('https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260922-2','Eurostat — 22 settembre 2026 — importazioni europee di petrolio e gas nel secondo trimestre.'),('https://ec.europa.eu/eurostat/statistics-explained/index.php?title=EU_imports_of_energy_products_-_latest_developments','Eurostat Statistics Explained — metodologia e serie sulle importazioni energetiche.')]
},
{
 'slug':'lavoro-sport-europa-1-8-milioni-occupati-eurostat-2025',
 'title':'Sport, nell’UE lavorano 1,8 milioni di persone',
 'excerpt':'Eurostat pubblica i dati alla vigilia della Settimana europea dello sport: 5.380 produttori di articoli sportivi generano 8 miliardi di euro.',
 'published':'2026-09-22T12:16:00+02:00','date':'22 settembre 2026','place':'Lussemburgo','category':'Sport / Lavoro','primary':'sport','priority':85,
 'key':'lavoro-sport-europa-eurostat-2025-v505','src':'exec-98ea2102-37fb-44c3-8879-cad1a04f2d91.png',
 'alt':'Illustrazione editoriale generata con IA di due professionisti al lavoro in un moderno centro sportivo; non è una fotografia documentaria.',
 'stats':[('1,8 mln','occupati nello sport nell’UE'),('5.380','produttori di articoli sportivi'),('8 mld €','fatturato complessivo dei produttori')],
 'body':[
 'Nel 2025 il settore sportivo impiegava 1,8 milioni di persone nell’Unione europea. Eurostat ha diffuso il dato il 22 settembre, alla vigilia della Settimana europea dello sport in programma dal 23 al 30 settembre.',
 'La misura comprende le attività economiche e le occupazioni collegate allo sport secondo le classificazioni statistiche europee. Il totale non coincide soltanto con atleti e allenatori: il comparto comprende anche funzioni organizzative, tecniche, commerciali e di servizio.',
 'La filiera industriale contava nel 2024 5.380 produttori di articoli sportivi. Le imprese hanno generato complessivamente 8 miliardi di euro di fatturato, offrendo una misura separata dell’attività manifatturiera collegata al settore.',
 'I dati sull’istruzione mostrano un divario di genere nei percorsi universitari sportivi. Nel 2024, per ogni cinque studenti uomini iscritti a questi corsi, si contavano due studentesse. Il rapporto riguarda la composizione degli iscritti e non misura direttamente le opportunità lavorative successive.',
 'Il confronto tra occupazione, formazione e produzione consente di osservare lo sport come settore economico, oltre che come pratica e competizione. Le tre grandezze hanno anni di riferimento diversi e non devono essere sommate tra loro.',
 'L’infografica pubblicata da Eurostat raccoglie anche dati su partecipazione e impatto economico. Le serie dettagliate permettono di confrontare età e genere degli occupati e di distinguere le differenze tra i Paesi membri.',
 'La Settimana europea dello sport offrirà il contesto per nuove iniziative pubbliche dal 23 settembre. I dati odierni costituiscono la base statistica dell’edizione 2026, non una stima degli effetti che gli eventi produrranno sull’occupazione.'
 ],
 'sources':[('https://ec.europa.eu/eurostat/web/products-eurostat-news/w/wdn-20260922-1','Eurostat — 22 settembre 2026 — occupazione, formazione e industria dello sport nell’UE.'),('https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Sport_statistics','Eurostat Statistics Explained — definizioni e serie statistiche sullo sport.')]
},
{
 'slug':'oms-etica-intelligenza-artificiale-ricerca-sanitaria-21-settembre-2026',
 'title':'IA nella ricerca sanitaria, l’OMS chiede controlli etici più forti',
 'excerpt':'Il rapporto indica rischi per trasparenza, equità, privacy e responsabilità. I comitati etici potrebbero aver bisogno di nuove competenze.',
 'published':'2026-09-22T12:14:00+02:00','date':'22 settembre 2026','place':'Ginevra','category':'Salute / Tecnologia','primary':'tecnologia','priority':92,
 'key':'oms-etica-ia-ricerca-sanitaria-2026-v505','src':'exec-adac9ac8-5bfd-465e-9326-844a8625fe09.png',
 'alt':'Illustrazione editoriale generata con IA di un comitato multidisciplinare che valuta applicazioni dell’intelligenza artificiale nella ricerca sanitaria; non è una fotografia documentaria.',
 'stats':[('3 ambiti','categorie di ricerca considerate'),('intero ciclo','controlli dal progetto all’applicazione'),('più competenze','richiesta per i comitati etici')],
 'body':[
 'L’Organizzazione mondiale della sanità chiede di rafforzare la supervisione etica della ricerca sanitaria che utilizza l’intelligenza artificiale. Il nuovo rapporto, presentato il 21 settembre, propone indicazioni per ricercatori, comitati etici, regolatori, finanziatori e responsabili delle politiche pubbliche.',
 'L’OMS individua rischi legati a trasparenza, distorsioni dei modelli, equità, responsabilità, privacy e possibili danni prodotti dall’impiego rapido degli strumenti. Il documento non sostiene che ogni applicazione sia pericolosa: chiede che benefici e rischi siano valutati prima e durante lo studio.',
 'Il rapporto distingue tre categorie: ricerca sanitaria sui dati che utilizza l’IA, ricerca su strumenti e tecnologie di IA e studi sanitari dedicati a valutare questi strumenti. La distinzione serve ad adattare la revisione etica alla funzione effettiva del sistema.',
 'La supervisione dovrebbe accompagnare l’intero ciclo, dalla progettazione alla pubblicazione, fino a regolazione e applicazione. Individuare un problema soltanto alla fine può essere insufficiente quando dati, modelli o decisioni hanno già influenzato partecipanti e risultati.',
 'I comitati etici mantengono un ruolo centrale, ma potrebbero aver bisogno di formazione, competenze tecniche e risorse aggiuntive. L’OMS attribuisce responsabilità anche a riviste scientifiche, organismi di governo dei dati, associazioni professionali e autorità di regolazione.',
 'Un’attenzione specifica riguarda i Paesi a reddito basso e medio. Gran parte della ricerca e dello sviluppo tecnologico resta concentrata nei Paesi più ricchi; senza leadership e partecipazione locali, gli strumenti potrebbero non rappresentare popolazioni, sistemi sanitari e priorità differenti.',
 'Le raccomandazioni costituiscono un quadro di supervisione e non una nuova terapia o un’autorizzazione clinica. La loro applicazione dipenderà dalle regole nazionali, dalle istituzioni di ricerca e dalle procedure adottate per ciascun progetto.'
 ],
 'sources':[('https://www.who.int/papuanewguinea/news/detail-global/21-09-2026-new-who-report-calls-for-stronger-ethics-oversight-of-ai-related-health-research','OMS — 21 settembre 2026 — presentazione e raccomandazioni del rapporto.'),('https://www.who.int/publications/i/item/9789240119022','OMS — rapporto tecnico “Artificial intelligence-related health research: ethics review and oversight”.')]
},
{
 'slug':'brics-impegni-sanita-vaccini-pandemie-oms-21-settembre-2026',
 'title':'BRICS, impegni comuni su sanità, vaccini e nuove pandemie',
 'excerpt':'L’OMS richiama la Dichiarazione di New Delhi: priorità a cure primarie, finanziamenti sostenibili e produzione regionale di vaccini e test.',
 'published':'2026-09-22T12:12:00+02:00','date':'22 settembre 2026','place':'New Delhi','category':'Mondo / Salute','primary':'mondo','priority':88,
 'key':'brics-sanita-vaccini-pandemie-new-delhi-2026-v505','src':'exec-a654ef38-e771-4369-809b-a657b2a8149a.png',
 'alt':'Illustrazione editoriale generata con IA di una riunione diplomatica internazionale a New Delhi dedicata alla cooperazione sanitaria; non è una fotografia documentaria.',
 'stats':[('18° vertice','riunione BRICS a New Delhi'),('3 priorità','cure, preparazione e produzione'),('2027','presidenza successiva affidata alla Cina')],
 'body':[
 'I leader dei BRICS hanno riaffermato l’impegno a rafforzare i sistemi sanitari, l’accesso alle tecnologie mediche e i finanziamenti sostenibili. L’Organizzazione mondiale della sanità ha pubblicato il 21 settembre una valutazione degli accordi inseriti nella Dichiarazione di New Delhi, adottata al diciottesimo vertice del gruppo.',
 'Le priorità comprendono assistenza sanitaria di base, preparazione alle pandemie e produzione locale o regionale di vaccini, test diagnostici e trattamenti. L’obiettivo dichiarato è ridurre le disuguaglianze di accesso e rendere le catene di fornitura meno vulnerabili agli shock.',
 'La dichiarazione sostiene il ruolo centrale dell’OMS nella governance sanitaria mondiale. Il direttore generale Tedros Adhanom Ghebreyesus ha invitato i Paesi a trasformare gli impegni politici in investimenti misurabili e capacità operative.',
 'Il documento richiama anche la sorveglianza delle malattie infettive e la condivisione delle informazioni. Questi strumenti richiedono regole tecniche comuni, laboratori, personale formato e procedure rapide; l’annuncio politico non equivale da solo a un sistema già funzionante.',
 'La produzione regionale può riguardare vaccini, diagnostica e medicinali, ma dipende da impianti, autorizzazioni, trasferimento di competenze e domanda stabile. La Dichiarazione indica una direzione di cooperazione senza fissare in questa fase quantità o scadenze uguali per tutti i membri.',
 'Il vertice si è svolto il 13 settembre sotto la presidenza indiana. La pubblicazione successiva dell’OMS rappresenta il nuovo sviluppo del 21 settembre e concentra l’attenzione sulle conseguenze sanitarie dell’accordo.',
 'La Cina assumerà la presidenza dei BRICS nel 2027. I risultati potranno essere valutati attraverso finanziamenti approvati, progetti produttivi avviati e procedure condivise per l’allerta e la risposta alle emergenze.'
 ],
 'sources':[('https://www.who.int/news/item/21-09-2026-who-welcomes-strong-health-commitments-at-the-2026-brics-summit','OMS — 21 settembre 2026 — valutazione degli impegni sanitari del vertice BRICS.'),('https://www.mea.gov.in/bilateral-documents.htm?dtl/40668/BRICS_New_Delhi_Declaration_Building_for_Resilience_Innovation_Cooperation_and_Sustainability','Ministero degli Esteri dell’India — Dichiarazione ufficiale di New Delhi.')]
}
]

def article_html(a):
    url=f"https://curiomondo.it/notizie/{a['slug']}.html"; img=f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema={'@context':'https://schema.org','@type':'NewsArticle','headline':a['title'],'description':a['excerpt'],'datePublished':a['published'],'dateModified':a['published'],'mainEntityOfPage':url,'inLanguage':'it-IT','author':{'@type':'Organization','name':'Redazione CurioMondo','url':'https://curiomondo.it/pagine/redazione.html'},'publisher':{'@type':'Organization','name':'CurioMondo'},'image':[img]}
    paras=''.join(f'<p>{escape(p)}</p>' for p in a['body']); stats=''.join(f'<div><strong>{escape(v)}</strong><span>{escape(l)}</span></div>' for v,l in a['stats']); sources=''.join(f'<li><a href="{escape(u,quote=True)}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a['sources'])
    related=[x for x in ARTICLES if x is not a][:3]; rel=''.join(f'<a href="/notizie/{x["slug"]}.html"><strong>{escape(x["title"])}</strong></a>' for x in related)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v={VERSION}"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner"><a class="cm-global-header__back" href="/" aria-label="Torna alla home"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a></nav></header><main class="wrap"><div class="badge">{escape(a['category'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">{a['date']} · {a['place']} · <span id="readTime">3 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html">Redazione CurioMondo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="false"><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{stats}</div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">{paras}</article><section class="curio-related" data-curated-related="true"><h2>Potrebbe interessarti anche…</h2><div class="curio-related-grid">{rel}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 22 settembre 2026.<br>{CAPTION}</small></p></div></main><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v={VERSION}" defer></script></body></html>'''

out=ROOT/'assets/images/editorial-auto'; out.mkdir(parents=True,exist_ok=True)
regp=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(regp.read_text())
for a in ARTICLES:
    im=Image.open(IMG_SRC/a['src']).convert('RGB'); w,h=im.size; ratio=1.5
    if w/h>ratio: nw=round(h*ratio); left=(w-nw)//2; im=im.crop((left,0,left+nw,h))
    elif w/h<ratio: nh=round(w/ratio); top=(h-nh)//2; im=im.crop((0,top,w,top+nh))
    variants=[]
    for width in (480,800,1200):
        p=out/f"{a['key']}-{width}.webp"; im.resize((width,round(width/1.5)),Image.Resampling.LANCZOS).save(p,'WEBP',quality=86,method=6)
        variants.append({'w':width,'src':f'/assets/images/editorial-auto/{p.name}','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    (ROOT/'notizie'/f"{a['slug']}.html").write_text(article_html(a),encoding='utf-8')
    reg['items']=[x for x in reg['items'] if x.get('article')!=f"/notizie/{a['slug']}.html"]
    reg['items'].insert(0,{'alt':a['alt'],'variants':variants,'disclosure':CAPTION,'generator':'OpenAI image tool','sensitiveContext':False,'article':f"/notizie/{a['slug']}.html",'key':a['key']})
reg['version']=VERSION; regp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')

# JSON indexes
hp=ROOT/'assets/data/home-feed-v210.json'; home=json.loads(hp.read_text()); sp=ROOT/'assets/data/search-index-v210.json'; search=json.loads(sp.read_text())
for a in reversed(ARTICLES):
    url=f"/notizie/{a['slug']}.html"; home['items']=[x for x in home['items'] if x.get('url')!=url]; search['items']=[x for x in search['items'] if x.get('url')!=url]
    entry={'title':a['title'],'excerpt':a['excerpt'],'url':url,'section':a['category'],'dateISO':a['published'],'dateLabel':'2026-09-22','image':f"/assets/images/editorial-auto/{a['key']}-800.webp",'imageAlt':a['alt'],'imageWidth':800,'imageHeight':533,'srcset':', '.join(f"/assets/images/editorial-auto/{a['key']}-{w}.webp {w}w" for w in (480,800,1200))}
    entry['featuredHighlights']=[a['stats'][0][0],a['stats'][1][0]]; entry['featuredStats']=[{'icon':i,'value':v,'label':l} for i,(v,l) in zip(('◆','▲','●'),a['stats'])]
    home['items'].insert(0,entry); search['items'].insert(0,{'title':a['title'],'excerpt':a['excerpt'],'url':url,'section':a['category']})
home['version']=search['version']=VERSION; hp.write_text(json.dumps(home,ensure_ascii=False,indent=2)+'\n'); sp.write_text(json.dumps(search,ensure_ascii=False,indent=2)+'\n')

# Homepage category mapping v504
cp=ROOT/'assets/data/homepage-config-v504.json'; cfg=json.loads(cp.read_text()); cfg['version']=VERSION
for a in ARTICLES: cfg['articles'][f"/notizie/{a['slug']}.html"]={'firstPublishedAt':a['published'],'homepagePriority':a['priority'],'primaryCategory':a['primary']}
cp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')

# Archive list
ap=ROOT/'notizie/index.html'; doc=html.fromstring(ap.read_text()); ul=doc.xpath('//ul')[0]
for a in reversed(ARTICLES):
    li=html.Element('li'); link=html.Element('a',href=f"/notizie/{a['slug']}.html"); link.text=a['title']; li.append(link); ul.insert(0,li)
ap.write_text('<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')

# RSS
fp=ROOT/'feed.xml'; tree=etree.parse(str(fp)); channel=tree.getroot().find('channel')
for a in reversed(ARTICLES):
    item=etree.Element('item')
    for tag,val in [('title',a['title']),('link',f"https://curiomondo.it/notizie/{a['slug']}.html"),('guid',f"https://curiomondo.it/notizie/{a['slug']}.html"),('pubDate',email.utils.format_datetime(datetime.fromisoformat(a['published']))),('description',a['excerpt'])]: etree.SubElement(item,tag).text=val
    channel.insert(4,item)
tree.write(str(fp),encoding='UTF-8',xml_declaration=True,pretty_print=True)

# Sitemaps
NS='http://www.sitemaps.org/schemas/sitemap/0.9'; NEWS='http://www.google.com/schemas/sitemap-news/0.9'
sm=ROOT/'sitemap.xml'; st=etree.parse(str(sm)); sr=st.getroot()
for a in ARTICLES:
    u=etree.Element(f'{{{NS}}}url'); etree.SubElement(u,f'{{{NS}}}loc').text=f"https://curiomondo.it/notizie/{a['slug']}.html"; etree.SubElement(u,f'{{{NS}}}lastmod').text='2026-09-22'; etree.SubElement(u,f'{{{NS}}}changefreq').text='daily'; etree.SubElement(u,f'{{{NS}}}priority').text='0.9'; sr.insert(0,u)
st.write(str(sm),encoding='utf-8',xml_declaration=True,pretty_print=True)
np=ROOT/'news-sitemap.xml'; nt=etree.parse(str(np)); nr=nt.getroot()
for a in ARTICLES:
    u=etree.Element(f'{{{NS}}}url'); etree.SubElement(u,f'{{{NS}}}loc').text=f"https://curiomondo.it/notizie/{a['slug']}.html"; n=etree.SubElement(u,f'{{{NEWS}}}news'); pub=etree.SubElement(n,f'{{{NEWS}}}publication'); etree.SubElement(pub,f'{{{NEWS}}}name').text='CurioMondo'; etree.SubElement(pub,f'{{{NEWS}}}language').text='it'; etree.SubElement(n,f'{{{NEWS}}}publication_date').text=a['published']; etree.SubElement(n,f'{{{NEWS}}}title').text=a['title']; nr.insert(0,u)
nt.write(str(np),encoding='utf-8',xml_declaration=True,pretty_print=True)

# Release state
mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text()); m['site']['current_site_version']=m['site']['site_version']=VERSION; m['site_version']=VERSION; m['version']=m['release_version']=f'v{VERSION}'; m['last_release']={'version':VERSION,'date':'2026-09-22','type':'editorial-news-cycle','news_added':[a['slug'] for a in ARTICLES],'news_updated':[],'change':'Cinque articoli da fonti primarie su energia, sport, tecnologia sanitaria e BRICS'}; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
for rel in ('CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json'):
    p=ROOT/rel
    if p.exists():
        d=json.loads(p.read_text()); d['site_version']=VERSION; d['version']=str(VERSION); d['currentVersion']=VERSION; d['last_update']='ciclo-editoriale-22-settembre-v505'; d['release_date']='2026-09-22'; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'version':VERSION,'articles':[a['slug'] for a in ARTICLES]},ensure_ascii=False))
