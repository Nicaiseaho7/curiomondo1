#!/usr/bin/env python3
from pathlib import Path
from html import escape
import hashlib, json
import xml.etree.ElementTree as ET
from lxml import etree, html

ROOT=Path(__file__).resolve().parents[1]
VERSION=287
SLUG='sassonia-anhalt-voto-afd-favorita-urne-6-settembre-2026'
URL=f'/notizie/{SLUG}.html'
TITLE='Sassonia-Anhalt al voto, affluenza in forte aumento: l’AfD cerca una svolta storica'
EXCERPT='Alle 14 aveva votato il 54,4% degli aventi diritto, contro il 27,1% alla stessa ora nel 2021. I sondaggi favoriscono l’AfD, ma risultati e maggioranze arriveranno solo dopo la chiusura dei seggi.'
IMAGE_KEY='sassonia-anhalt-elettori-6-settembre-2026-ai-v287'
IMAGE_ALT='Scena editoriale generata con IA di elettori in fila davanti a un seggio della Sassonia-Anhalt, senza simboli di partito o risultati rappresentati'
CAPTION='Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
DEEP_SLUG='elezioni-land-germania-landtag-coalizioni-brandmauer'
DEEP_TITLE='Elezioni regionali in Germania: Landtag, coalizioni e Brandmauer spiegati'
DEEP_EXCERPT='Come si elegge un parlamento regionale tedesco, perché il partito più votato non governa automaticamente e che cosa indica il “muro tagliafuoco” politico.'

p=ROOT/'notizie'/f'{SLUG}.html'; doc=html.fromstring(p.read_text(encoding='utf-8'))
doc.xpath('//title')[0].text=TITLE+' | CurioMondo'
for xp,val in [('//meta[@name="description"]','content'),('//meta[@property="og:title"]','content'),('//meta[@property="og:description"]','content')]:
    n=doc.xpath(xp)[0]; n.set(val, TITLE if 'title' in xp else EXCERPT)
doc.xpath('//meta[@property="og:image"]')[0].set('content',f'https://curiomondo.it/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp')
doc.xpath('//meta[@property="og:image:alt"]')[0].set('content',IMAGE_ALT)
ld=doc.xpath('//script[@type="application/ld+json"]')[0]; data=json.loads(ld.text); data.update({'headline':TITLE,'description':EXCERPT,'dateModified':'2026-09-06T16:00:00+02:00','image':[f'https://curiomondo.it/assets/images/editorial-auto/{IMAGE_KEY}-1200.webp']}); ld.text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
main=doc.xpath('//main[contains(@class,"wrap")]')[0]; main.xpath('./h1')[0].text=TITLE; main.xpath('./p[contains(@class,"subtitle")]')[0].text=EXCERPT
meta=main.xpath('./div[contains(@class,"meta")]')[0]
for child in list(meta): meta.remove(child)
meta.text='6 settembre 2026 · aggiornato alle 16:00 · Europa / Germania / Elezioni · '; span=etree.SubElement(meta,'span',id='readTime'); span.text='5 min di lettura'
fig=main.xpath('./figure[contains(@class,"article-image")]')[0]; img=fig.xpath('.//img')[0]
img.set('src',f'../assets/images/editorial-auto/{IMAGE_KEY}-800.webp'); img.set('srcset',f'../assets/images/editorial-auto/{IMAGE_KEY}-480.webp 480w, ../assets/images/editorial-auto/{IMAGE_KEY}-800.webp 800w, ../assets/images/editorial-auto/{IMAGE_KEY}-1200.webp 1200w'); img.set('alt',IMAGE_ALT); fig.xpath('.//figcaption')[0].text=CAPTION
ins=main.xpath('.//section[contains(@class,"cm-insight")]/div')[0]; ins.clear()
for a,b in [('54,4%','affluenza alle 14, dato ufficiale'),('1,7 milioni','gli aventi diritto al voto'),('Ore 18','chiusura dei seggi, poi le proiezioni')]:
    box=etree.SubElement(ins,'div'); etree.SubElement(box,'b').text=a; etree.SubElement(box,'small').text=b
art=main.xpath('./article[contains(@class,"art-body")]')[0]
paras=[
'Gli elettori della Sassonia-Anhalt, Stato della Germania orientale, sono chiamati a scegliere il nuovo parlamento regionale in un voto osservato in tutto il Paese. Circa 1,7 milioni di persone possono recarsi alle urne fino alle 18; soltanto dopo la chiusura arriveranno le prime proiezioni e poi i risultati dello scrutinio.',
'L’affluenza è in forte aumento. Secondo la responsabile elettorale del Land, alle 14 aveva votato il 54,4% degli aventi diritto, contro il 27,1% rilevato alla stessa ora nel 2021. Il dato misura la partecipazione nei distretti campione e non anticipa quale partito sia avanti: un’affluenza elevata può modificare le stime, ma non indica da sola chi ne tragga vantaggio.',
'L’appuntamento potrebbe produrre un passaggio senza precedenti nella Germania del dopoguerra: l’Alternative für Deutschland punta a diventare il primo partito di estrema destra capace di guidare un governo statale dalla Seconda guerra mondiale. “Guidare” significa riuscire a far eleggere il ministro-presidente e sostenere un esecutivo nel Land; arrivare primi nei voti, invece, non basta automaticamente.',
'I sondaggi pubblicati prima del voto collocano l’AfD poco sopra il 40% e la CDU intorno al 23%. Sono rilevazioni statistiche, non risultati elettorali. Il candidato dell’AfD alla presidenza è Ulrich Siegmund, mentre la CDU presenta il ministro-presidente uscente Sven Schulze. La sezione regionale dell’AfD è classificata dall’ufficio locale per la protezione della Costituzione come estremista di destra; il partito contesta la valutazione.',
'La Sassonia-Anhalt è un <strong>Land</strong>, uno dei sedici Stati federati tedeschi. Il suo parlamento si chiama <strong>Landtag</strong>: approva leggi nelle competenze regionali, controlla il governo locale ed elegge il ministro-presidente. Quest’ultimo può essere paragonato con cautela a un presidente di Regione italiano, perché opera in un sistema federale con poteri e rapporti istituzionali differenti.',
'Il passaggio decisivo sarà la maggioranza dei seggi. In Germania il governo nasce dal parlamento e le altre principali forze politiche escludono accordi con l’AfD. Questa scelta viene chiamata <strong>Brandmauer</strong>, letteralmente “muro tagliafuoco”: non è una regola scritta nella legge elettorale, ma un impegno politico a non formare coalizioni con l’estrema destra.',
'Se l’AfD arrivasse prima senza ottenere la maggioranza assoluta, CDU, SPD, Linke e altri partiti ammessi al Landtag dovrebbero valutare combinazioni alternative. Una coalizione è un accordo tra più forze per sostenere lo stesso governo; un governo di minoranza, invece, non dispone stabilmente di oltre metà dei seggi e deve cercare appoggi su singole decisioni.',
'La soglia del 5% rende il calcolo particolarmente delicato. Le liste che restano sotto questo limite, salvo le eccezioni previste, non partecipano alla distribuzione proporzionale dei seggi. Se molti voti vanno a partiti esclusi, una formazione può conquistare la maggioranza parlamentare pur restando sotto il 50% dei voti validi.',
'Ogni elettore dispone di due voti: il primo sceglie un candidato nel collegio, il secondo una lista regionale e determina soprattutto i rapporti di forza complessivi. Il sistema cerca di combinare rappresentanza territoriale e proporzionalità; per questo il numero finale dei seggi può dipendere anche dai mandati diretti ottenuti nei collegi.',
'Il voto è anche un test politico per il cancelliere Friedrich Merz. Un risultato debole della CDU aumenterebbe la pressione sulla leadership nazionale, ma non farebbe cadere automaticamente il governo federale. I Länder influenzano inoltre la politica nazionale attraverso il Bundesrat, la camera in cui sono rappresentati i governi regionali.',
'CurioMondo ha raccolto questi meccanismi nella guida <a href="/approfondimenti/elezioni-land-germania-landtag-coalizioni-brandmauer.html">come funzionano Landtag, coalizioni e Brandmauer nelle elezioni regionali tedesche</a>. L’approfondimento aiuta a distinguere tre momenti diversi: il partito più votato, la distribuzione dei seggi e la formazione effettiva del governo.',
'Fino alle 18 la notizia verificabile resta quindi il forte aumento della partecipazione e il vantaggio attribuito all’AfD dai sondaggi. Solo lo scrutinio dirà se quel vantaggio sarà confermato, quali partiti supereranno il 5% e se esisterà una maggioranza capace di eleggere il nuovo ministro-presidente.'
]
art.clear(); art.set('class','art-body'); art.set('data-length-policy','3000-7000')
for text in paras: art.append(html.fragment_fromstring(f'<p>{text}</p>'))
old=main.xpath('./section[contains(@class,"cm-evergreen-reader")]')
if not old:
    guide=html.fragment_fromstring(f'<section aria-labelledby="cm-evergreen-question" class="cm-evergreen-reader"><small>Una cosa utile da sapere</small><h2 id="cm-evergreen-question">Come funzionano Landtag, coalizioni e Brandmauer</h2><a href="/approfondimenti/{DEEP_SLUG}.html">Leggi l’approfondimento →</a></section>'); main.insert(main.index(art)+1,guide)
note=main.xpath('.//div[contains(@class,"art-sources")]//p/small')[0]; note.text='Testo originale CurioMondo. Ultimo aggiornamento editoriale: 6 settembre 2026, ore 16:00 italiane. I dati dei sondaggi non sono risultati elettorali.'
p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')

# Approfondimento evergreen autonomo e bidirezionale.
deep_body=[
'La Germania è una federazione composta da sedici Länder. Ogni Land possiede un parlamento regionale, chiamato Landtag nella maggior parte degli Stati, e un governo con competenze importanti in settori come istruzione, polizia, cultura e amministrazione locale. Per questo un’elezione regionale non è soltanto un sondaggio sul governo nazionale.',
'Gli elettori scelgono rappresentanti con un sistema che combina collegi e liste. Il voto di lista determina soprattutto la proporzione dei seggi, mentre il voto al candidato assegna i mandati diretti. Il numero complessivo dei parlamentari può cambiare quando servono seggi aggiuntivi per ristabilire la proporzionalità.',
'La soglia del 5% limita l’accesso dei partiti più piccoli. I voti delle liste escluse non vengono utilizzati nella distribuzione proporzionale ordinaria: di conseguenza la maggioranza dei seggi può richiedere meno del 50% dei voti espressi. La percentuale necessaria dipende quindi da quanti partiti superano la soglia.',
'Il partito più votato non riceve automaticamente il governo. Il Landtag elegge il ministro-presidente e quest’ultimo deve poter contare su una maggioranza, stabile o costruita voto per voto. Quando nessun partito possiede abbastanza seggi, iniziano negoziati per una coalizione.',
'Una <strong>coalizione</strong> è un accordo fra partiti che definisce programma, incarichi e regole di collaborazione. Un <strong>governo di minoranza</strong> nasce invece senza una maggioranza permanente e deve ottenere l’appoggio esterno di altre forze per approvare bilanci e leggi.',
'La parola <strong>Brandmauer</strong> significa “muro tagliafuoco”. Nel dibattito tedesco indica la scelta dei partiti tradizionali di non governare con l’AfD. Non è un divieto costituzionale: è una linea politica, quindi incide sulle coalizioni possibili anche quando l’AfD ottiene molti voti.',
'I governi dei Länder partecipano anche al Bundesrat, la camera federale che esamina numerose leggi nazionali. Una nuova coalizione regionale può dunque modificare gli equilibri di voto a Berlino, specialmente sulle norme che richiedono il consenso della camera dei Länder.',
'Per leggere correttamente una serata elettorale servono tre dati distinti. La percentuale dei voti indica il consenso; i seggi mostrano la forza parlamentare effettiva; l’accordo di governo stabilisce chi amministrerà. Le prime proiezioni sono stime basate su sondaggi all’uscita e risultati parziali, mentre il risultato provvisorio nasce dallo scrutinio molto più avanzato.',
f'Questa distinzione è centrale nella <a href="{URL}">elezione della Sassonia-Anhalt del 6 settembre 2026</a>: anche un primo posto netto dell’AfD non equivale da solo alla conquista del governo. Servono abbastanza seggi oppure alleati disposti a eleggere il suo candidato alla presidenza del Land.'
]
canonical=f'https://curiomondo.it/approfondimenti/{DEEP_SLUG}.html'; schema={'@context':'https://schema.org','@type':'Article','headline':DEEP_TITLE,'description':DEEP_EXCERPT,'datePublished':'2026-09-06T16:00:00+02:00','dateModified':'2026-09-06T16:00:00+02:00','mainEntityOfPage':canonical,'inLanguage':'it-IT','author':{'@type':'Organization','name':'Redazione CurioMondo'},'publisher':{'@type':'Organization','name':'CurioMondo'}}
deep=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(DEEP_TITLE)} | CurioMondo</title><meta name="description" content="{escape(DEEP_EXCERPT,quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=287"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">Approfondimento · Germania / Elezioni</div><h1>{escape(DEEP_TITLE)}</h1><p class="subtitle">{escape(DEEP_EXCERPT)}</p><div class="meta">Aggiornato il 6 settembre 2026 · 4 min di lettura</div><article class="art-body">{''.join(f'<p>{x}</p>' for x in deep_body)}</article><section class="cm-evergreen-reader"><small>Notizia collegata</small><h2>Sassonia-Anhalt al voto</h2><a href="{URL}">Leggi l’aggiornamento →</a></section><div class="art-sources"><h2>Fonti consultate</h2><ul><li><a href="https://wahlen.sachsen-anhalt.de/zu-den-wahlen/landtagswahl" rel="noopener noreferrer" target="_blank">Landeswahlleiterin Sachsen-Anhalt — informazioni ufficiali sul voto</a></li><li><a href="https://www.landtag.sachsen-anhalt.de/alle-dossiers/landtagswahl-am-6-september-2026" rel="noopener noreferrer" target="_blank">Landtag Sachsen-Anhalt — elezione del 6 settembre 2026</a></li><li><a href="https://www.bundesrat.de/EN/funktionen-en/funktionen-en-node.html" rel="noopener noreferrer" target="_blank">Bundesrat — ruolo dei Länder nel sistema federale</a></li></ul></div></main><footer class="site-footer"><a href="/approfondimenti/">Altri approfondimenti</a></footer></body></html>'''
(ROOT/'approfondimenti'/f'{DEEP_SLUG}.html').write_text(deep,encoding='utf-8')

# Registro del nuovo visual.
rp=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(rp.read_text(encoding='utf-8')); reg['version']=VERSION; reg['items']=[x for x in reg['items'] if x.get('key')!=IMAGE_KEY]
variants=[]
for w in (480,800,1200):
    f=ROOT/'assets/images/editorial-auto'/f'{IMAGE_KEY}-{w}.webp'; variants.append({'w':w,'src':f'/assets/images/editorial-auto/{f.name}','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
reg['items'].insert(0,{'key':IMAGE_KEY,'article':URL,'aiGenerated':True,'sensitiveContext':False,'documentaryPhoto':False,'prompt':'Ultra-realistic neutral editorial photo of voters entering a polling station in Saxony-Anhalt; no politicians, party symbols, readable text or implied result.','variants':variants,'alt':IMAGE_ALT,'disclosure':CAPTION,'portraitOnly':False,'portraitFormat':'contextual-editorial-scene','reenactedEvent':False})
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Feed dati e ricerca.
hp=ROOT/'assets/data/home-feed-v210.json'; h=json.loads(hp.read_text(encoding='utf-8')); h['version']=VERSION
item=next(x for x in h['items'] if x['url']==URL); item.update({'title':TITLE,'excerpt':EXCERPT,'image':f'/assets/images/editorial-auto/{IMAGE_KEY}-800.webp','imageAlt':IMAGE_ALT,'srcset':f'/assets/images/editorial-auto/{IMAGE_KEY}-480.webp 480w, /assets/images/editorial-auto/{IMAGE_KEY}-800.webp 800w, /assets/images/editorial-auto/{IMAGE_KEY}-1200.webp 1200w'})
hp.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sp=ROOT/'assets/data/search-index-v210.json'; s=json.loads(sp.read_text(encoding='utf-8')); s['version']=VERSION
next(x for x in s['items'] if x.get('url')==URL).update({'title':TITLE,'excerpt':EXCERPT})
du=f'/approfondimenti/{DEEP_SLUG}.html'; s['items']=[x for x in s['items'] if x.get('url')!=du]; s['items'].insert(0,{'title':DEEP_TITLE,'excerpt':DEEP_EXCERPT,'url':du,'section':'Germania / Elezioni'})
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Aggiorna le rappresentazioni statiche della notizia.
for rel in ('index.html','notizie/index.html'):
    q=ROOT/rel; d=html.fromstring(q.read_text(encoding='utf-8'))
    for a in d.xpath(f'//a[@href="{URL}"]'):
        title_nodes=a.xpath('.//h1|.//h3|.//strong');
        if title_nodes: title_nodes[0].text=TITLE
        ps=a.xpath('.//p');
        if ps: ps[0].text=EXCERPT
        im=a.xpath('.//img');
        if im: im[0].set('src',f'/assets/images/editorial-auto/{IMAGE_KEY}-800.webp'); im[0].set('srcset',f'/assets/images/editorial-auto/{IMAGE_KEY}-480.webp 480w, /assets/images/editorial-auto/{IMAGE_KEY}-800.webp 800w, /assets/images/editorial-auto/{IMAGE_KEY}-1200.webp 1200w'); im[0].set('alt',IMAGE_ALT)
        if a.getparent() is not None and a.getparent().tag in ('nav','div') and 'ticker-news' in (a.get('class') or ''): a.text=TITLE
    q.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

# Archivio approfondimenti.
ap=ROOT/'approfondimenti/index.html'; d=html.fromstring(ap.read_text(encoding='utf-8')); grid=d.xpath('//section[contains(@class,"grid")]')[0]
for old in grid.xpath(f'./a[@data-cm-evergreen-slug="{DEEP_SLUG}"]'): grid.remove(old)
grid.insert(0,html.fragment_fromstring(f'<a class="card" href="../approfondimenti/{DEEP_SLUG}.html" data-cm-evergreen-slug="{DEEP_SLUG}"><span class="tag">Approfondimento · Germania / Elezioni</span><div><h2>{escape(DEEP_TITLE)}</h2><p>{escape(DEEP_EXCERPT)}</p></div><b>Leggi l’approfondimento →</b></a>'))
ap.write_text('<!doctype html>'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

# RSS, news sitemap, sitemap generale.
rss=ROOT/'feed.xml'; t=ET.parse(rss); ch=t.getroot().find('channel')
for n in ch.findall('item'):
    if n.findtext('guid')=='https://curiomondo.it'+URL: n.find('title').text=TITLE; n.find('description').text=EXCERPT
ET.indent(t,space='  '); t.write(rss,encoding='utf-8',xml_declaration=True)
NS='http://www.sitemaps.org/schemas/sitemap/0.9'; NN='http://www.google.com/schemas/sitemap-news/0.9'; ns=ROOT/'news-sitemap.xml'; t=ET.parse(ns)
for n in t.getroot().findall(f'{{{NS}}}url'):
    if n.findtext(f'{{{NS}}}loc')=='https://curiomondo.it'+URL: n.find(f'.//{{{NN}}}title').text=TITLE
ET.indent(t,space='  '); t.write(ns,encoding='utf-8',xml_declaration=True)
sm=ROOT/'sitemap.xml'; t=ET.parse(sm); root=t.getroot(); full='https://curiomondo.it'+du
if full not in {x.text for x in root.findall(f'{{{NS}}}url/{{{NS}}}loc')}:
    n=ET.Element(f'{{{NS}}}url'); ET.SubElement(n,f'{{{NS}}}loc').text=full; ET.SubElement(n,f'{{{NS}}}lastmod').text='2026-09-06'; root.insert(0,n)
ET.indent(t,space='  '); t.write(sm,encoding='utf-8',xml_declaration=True)

mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; m['site_version']=VERSION; m['version']=m['release_version']=f'v{VERSION}'; m['last_release']={'version':VERSION,'date':'2026-09-06','type':'content-update','change':'Aggiornamento elezioni Sassonia-Anhalt con affluenza delle 14, nuovo visual IA e approfondimento evergreen su Landtag, coalizioni e Brandmauer','article_body_policy':'3000-7000'}; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ok','version':VERSION,'article':URL,'evergreen':du},ensure_ascii=False))
