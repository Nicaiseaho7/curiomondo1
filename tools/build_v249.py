from pathlib import Path
from lxml import html, etree
from html import escape
import json, re, shutil, zipfile
from datetime import datetime
from email.utils import format_datetime

ROOT=Path(__file__).resolve().parents[1]
VERSION=249

stories=[
{
'slug':'italia-spagna-scontro-controlli-frontiere-crisi-ceuta',
'path':ROOT/'notizie/italia-spagna-scontro-controlli-frontiere-crisi-ceuta.html',
'title':'Migranti, l’Italia verso la proroga dei controlli alle frontiere con la Spagna: nuova tensione su Ceuta e Schengen',
'excerpt':'La misura introdotta il 1° agosto scade il 31 agosto. Roma sarebbe orientata a prorogarla di almeno un mese, ma la decisione non è ancora formalizzata.',
'section':'Italia · Politica / Migrazioni / Europa',
'category':'Politica / Migrazioni / Europa',
'published':'2026-08-30T07:07:00+02:00','updated':'2026-08-30T07:07:00+02:00','display':'30 agosto 2026 · 07:07',
'image':'/assets/images/optimized/unique-v182-come-funzionano-trasferimenti-richiedenti-asilo-europa-960.webp',
'body':[
'L’Italia sarebbe orientata a prorogare di almeno un altro mese i controlli temporanei sui passeggeri provenienti dalla Spagna, introdotti il 1° agosto dopo la grave crisi migratoria di Ceuta. La misura attualmente in vigore scade il 31 agosto e una decisione dovrà quindi arrivare in tempi molto rapidi. Adnkronos riferisce questa mattina l’orientamento del governo sulla base di informazioni rilanciate dai media spagnoli, ma al momento non risulta ancora una formalizzazione equivalente da parte del Viminale.',
'Tra le motivazioni considerate figurerebbero un ulteriore aggravamento della situazione nell’enclave di Ceuta e il rischio di possibili minacce terroristiche. Una proroga dei controlli interni allo spazio Schengen richiederebbe una comunicazione alla Commissione europea e dovrebbe mantenere il carattere di misura temporanea, proporzionata e motivata da esigenze di ordine pubblico o sicurezza interna. Proprio per questo la distinzione tra orientamento politico e decisione ufficiale è essenziale: finché non arriva l’atto formale, non è corretto presentare la proroga come già approvata.',
'La vicenda si inserisce in una fase di forte tensione diplomatica tra Roma e Madrid. Il ministro degli Esteri spagnolo José Manuel Albares ha accusato recentemente l’Italia di mancanza di solidarietà e di utilizzare politicamente la crisi migratoria. Per il governo spagnolo, la gestione di Ceuta non giustificherebbe una misura prolungata sui movimenti in arrivo dalla Spagna; Roma continua invece a considerare necessario mantenere strumenti di controllo finché il quadro non sarà ritenuto sufficientemente stabile.',
'Il nodo istituzionale riguarda Schengen. Il ripristino temporaneo dei controlli alle frontiere interne è previsto dalle regole europee soltanto in circostanze eccezionali e deve essere limitato nel tempo. Un’estensione di un altro mese trasformerebbe quindi la risposta inizialmente emergenziale alla crisi di Ceuta in un dispositivo più duraturo, con conseguenze anche sul piano politico europeo. La Commissione dovrà essere informata e potrà valutare proporzionalità, durata e motivazioni della misura.',
'Per i viaggiatori, l’eventuale proroga non equivarrebbe a una chiusura del confine tra Italia e Spagna. Significherebbe però il mantenimento di verifiche supplementari su alcune categorie di passeggeri e potrebbe comportare controlli più frequenti nei collegamenti aerei, marittimi o terrestri interessati. I dettagli operativi dipenderanno dal provvedimento finale, che non è ancora disponibile.',
'Il prossimo aggiornamento decisivo sarà quindi la conferma ufficiale del Viminale o la comunicazione italiana alla Commissione europea. Se arriverà, la notizia passerà da un orientamento governativo a una decisione effettiva e avrà un peso maggiore anche nei rapporti con Madrid. Fino ad allora il quadro corretto è questo: la proroga è considerata probabile, ma non ancora formalmente adottata.'
],
'sources':[('https://www.adnkronos.com/','Adnkronos — Italia verso la proroga dei controlli alle frontiere con la Spagna')]
},
{
'slug':'cia-direttore-john-ratcliffe-mosca-visita-25-agosto-2026',
'path':ROOT/'notizie/cia-direttore-john-ratcliffe-mosca-visita-25-agosto-2026.html',
'title':'Ucraina, missione segreta del capo della CIA a Mosca: proposta una riunione Trump-Putin-Zelensky',
'excerpt':'Durante la visita non annunciata del 25 agosto John Ratcliffe avrebbe proposto un vertice trilaterale per riaprire i negoziati. L’incontro non è stato concordato.',
'section':'Mondo · Ucraina / USA / Russia',
'category':'Mondo / Geopolitica',
'published':'2026-08-25T20:42:00+02:00','updated':'2026-08-30T08:10:00+02:00','display':'30 agosto 2026 · aggiornamento',
'image':'/assets/images/optimized/cia-ratcliffe-mosca-editoriale-v184-960.webp',
'body':[
'La visita non annunciata del direttore della CIA John Ratcliffe a Mosca del 25 agosto avrebbe avuto un obiettivo diplomatico molto più preciso di quanto emerso inizialmente. Secondo Axios, che cita due fonti informate e la cui ricostruzione è stata rilanciata da ANSA, Ratcliffe avrebbe proposto un vertice trilaterale tra Donald Trump, Vladimir Putin e Volodymyr Zelensky per tentare di riaprire il negoziato sulla guerra in Ucraina.',
'Ratcliffe avrebbe incontrato i vertici dell’intelligence russa, tra cui Sergei Naryshkin e Alexander Bortnikov. L’obiettivo sarebbe stato capire se i canali dei servizi potessero contribuire a convincere Putin a tornare a un percorso negoziale mediato dagli Stati Uniti. La missione assume così un significato più definito rispetto alle prime ore, quando era noto soltanto l’arrivo a Mosca del capo della CIA ma non l’agenda degli incontri.',
'Venerdì Washington avrebbe inoltre informato Zelensky sia dei colloqui avvenuti nella capitale russa sia della proposta del vertice a tre. Questo passaggio indica che il canale aperto con Mosca non sarebbe rimasto confinato a un semplice scambio tra apparati d’intelligence, ma sarebbe stato collegato a un tentativo politico più ampio di rimettere intorno allo stesso tavolo i tre leader coinvolti direttamente nel dossier.',
'La cautela resta però indispensabile. Il vertice Trump-Putin-Zelensky non è stato concordato e non esiste una data. Putin aveva già respinto in passato l’ipotesi di un incontro trilaterale, mentre Zelensky si era dichiarato disponibile a colloqui diretti se utili a produrre risultati concreti. La notizia corretta non è quindi che i tre presidenti si incontreranno, ma che Washington avrebbe presentato formalmente questa opzione attraverso un canale riservato.',
'Il ricorso al direttore della CIA mostra anche il valore dei canali di sicurezza nelle fasi di stallo diplomatico. I capi dei servizi possono trasmettere messaggi sensibili, chiarire condizioni preliminari e verificare la disponibilità dell’altra parte senza esporre immediatamente i governi a un fallimento pubblico. Questo non sostituisce il lavoro diplomatico tradizionale, ma può preparare il terreno a negoziati più visibili qualora emergano aperture reali.',
'Il prossimo passaggio da monitorare è la risposta di Mosca. Un’accettazione russa della proposta trasformerebbe il retroscena in un vero sviluppo negoziale; un rifiuto confermerebbe invece lo stallo. Per ora resta accertato soltanto che la missione di Ratcliffe è stata un contatto diretto e riservato di alto livello e che, secondo le fonti citate, al centro del confronto c’era anche la possibilità di una riunione fra Trump, Putin e Zelensky.'
],
'sources':[('https://www.ansa.it/','ANSA — aggiornamento del 30 agosto sulla missione di Ratcliffe'),('https://www.axios.com/','Axios — ricostruzione della missione e proposta del vertice trilaterale')]
},
{
'slug':'islanda-no-ue-referendum-negoziati-adesione-30-agosto-2026',
'path':ROOT/'notizie/islanda-no-ue-referendum-negoziati-adesione-30-agosto-2026.html',
'title':'Islanda, vince il “no” all’Unione europea: gli elettori bocciano la riapertura dei negoziati di adesione',
'excerpt':'Il referendum chiude il tentativo di riaprire il percorso verso Bruxelles. La premier aveva definito la consultazione decisiva per il futuro europeo del Paese.',
'section':'Mondo · Europa / Islanda / UE',
'category':'Mondo / Europa / Politica',
'published':'2026-08-30T08:35:00+02:00','updated':'2026-08-30T08:35:00+02:00','display':'30 agosto 2026 · 08:35',
'image':'/assets/images/optimized/unique-v182-spazio-difesa-europa-pmi-italiane-come-funziona-960.webp',
'body':[
'Gli elettori islandesi hanno respinto la riapertura dei negoziati per l’adesione all’Unione europea. Il risultato del referendum, riportato dall’emittente pubblica RÚV e da Reuters il 30 agosto, chiude almeno per questa fase il tentativo del governo di riportare l’Islanda su un percorso formale verso Bruxelles. La consultazione aveva un valore politico preciso: non chiedeva l’ingresso immediato nell’UE, ma se riavviare i negoziati interrotti anni fa.',
'La premier Kristrún Frostadóttir aveva indicato il voto come decisivo e aveva spiegato che una vittoria del “no” avrebbe chiuso la questione dell’adesione. Il governo aveva sostenuto il riavvicinamento alle istituzioni europee anche alla luce della crescente instabilità geopolitica, delle tensioni nell’Artico e della necessità di definire con maggiore chiarezza la posizione strategica dell’Islanda nel continente.',
'L’Islanda aveva presentato domanda di adesione nel 2009, nel pieno delle conseguenze della crisi finanziaria globale. I negoziati erano poi stati sospesi e successivamente abbandonati. Nel frattempo il Paese ha continuato a partecipare al mercato unico attraverso lo Spazio economico europeo e fa parte dell’area Schengen, mantenendo però fuori dal quadro comunitario settori considerati particolarmente sensibili, come pesca e gestione di alcune risorse naturali.',
'Il risultato non modifica quindi dall’oggi al domani la libera circolazione o i rapporti economici fondamentali con l’Europa. Cambia però la prospettiva politica: senza un nuovo mandato popolare, il governo non potrà riaprire il dossier di adesione nei termini prospettati. Il “no” rafforza inoltre le forze che considerano l’attuale rapporto con l’UE sufficiente e temono che una piena adesione possa ridurre l’autonomia islandese su pesca, energia e regolazione economica.',
'Il voto ha anche una dimensione strategica. L’Artico è diventato un’area sempre più rilevante per sicurezza, rotte marittime, energia e competizione fra grandi potenze. Chi sosteneva il riavvicinamento all’UE vedeva nell’adesione un possibile rafforzamento del peso internazionale dell’Islanda; gli oppositori ritengono invece che la NATO, lo Spazio economico europeo e gli accordi esistenti garantiscano già una rete sufficiente di cooperazione.',
'Con il risultato definitivo, la questione europea non scompare dal dibattito islandese, ma perde la sua prospettiva immediata. Un futuro governo potrebbe teoricamente riaprire il tema con un nuovo mandato politico o una nuova consultazione, ma il voto del 30 agosto blocca il percorso annunciato dall’esecutivo attuale e segna una scelta netta sulla direzione istituzionale del Paese.'
],
'sources':[('https://www.reuters.com/','Reuters — risultato del referendum islandese del 30 agosto'),('https://www.ruv.is/','RÚV — risultati e copertura del referendum')]
}
]

def article_text_len(body): return sum(len(x) for x in body)
for s in stories:
    print(s['slug'], article_text_len(s['body']))

# create lightweight svg for Iceland homepage only
svg=ROOT/'assets/images/editorial-v249/islanda-ue-referendum-30-agosto-2026.svg'
svg.parent.mkdir(parents=True,exist_ok=True)
svg.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b2d5c"/><stop offset="1" stop-color="#133f8c"/></linearGradient></defs><rect width="1200" height="800" fill="url(#g)"/><rect x="60" y="100" width="500" height="330" rx="18" fill="#02529c"/><rect x="195" y="100" width="85" height="330" fill="#fff"/><rect x="60" y="222" width="500" height="85" fill="#fff"/><rect x="215" y="100" width="45" height="330" fill="#dc1e35"/><rect x="60" y="242" width="500" height="45" fill="#dc1e35"/><circle cx="850" cy="265" r="170" fill="#123a83" stroke="#fff" stroke-width="6"/><g fill="#ffcc00">''' + ''.join(f'<circle cx="{850+130*__import__("math").cos(i*__import__("math").pi/6):.1f}" cy="{265+130*__import__("math").sin(i*__import__("math").pi/6):.1f}" r="13"/>' for i in range(12)) + '''</g><path d="M640 590h420" stroke="#fff" stroke-width="8" opacity=".75"/><path d="M700 650h300" stroke="#fff" stroke-width="8" opacity=".4"/></svg>''',encoding='utf-8')
stories[2]['image']='/assets/images/editorial-v249/islanda-ue-referendum-30-agosto-2026.svg'

# helper update/create pages
def set_text(doc,xpath,text):
    nodes=doc.xpath(xpath)
    if nodes: nodes[0].text=text

def page_from_existing(s):
    path=s['path']
    if path.exists():
        doc=html.fromstring(path.read_text(encoding='utf-8'))
    else:
        # use Italy-Spain page as clean template
        doc=html.fromstring((ROOT/'notizie/italia-spagna-scontro-controlli-frontiere-crisi-ceuta.html').read_text(encoding='utf-8'))
    head=doc.xpath('//head')[0]
    title=head.xpath('./title')[0]; title.text=s['title']+' | CurioMondo'
    def meta(name=None,prop=None):
        xp=f'./meta[@name="{name}"]' if name else f'./meta[@property="{prop}"]'; n=head.xpath(xp)
        return n[0] if n else None
    for k,v in [('description',s['excerpt'])]:
        n=meta(name=k)
        if n is not None: n.set('content',v)
    for prop,val in [('og:title',s['title']),('og:description',s['excerpt']),('og:url','https://curiomondo.it/notizie/'+s['slug']+'.html')]:
        n=meta(prop=prop)
        if n is None: n=etree.SubElement(head,'meta'); n.set('property',prop)
        n.set('content',val)
    can=head.xpath('./link[@rel="canonical"]')
    if can: can[0].set('href','https://curiomondo.it/notizie/'+s['slug']+'.html')
    ld=head.xpath('./script[@type="application/ld+json"]')
    if ld:
        schema={"@context":"https://schema.org","@type":"NewsArticle","headline":s['title'],"description":s['excerpt'],"datePublished":s['published'],"dateModified":s['updated'],"mainEntityOfPage":'https://curiomondo.it/notizie/'+s['slug']+'.html',"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}}}
        ld[0].text=json.dumps(schema,ensure_ascii=False)
    body=doc.xpath('//body')[0]; body.set('data-article-id',s['slug'])
    set_text(doc,'//div[contains(concat(" ",normalize-space(@class)," ")," badge ")]',s['section'])
    set_text(doc,'//main//h1',s['title'])
    set_text(doc,'//p[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]',s['excerpt'])
    m=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')
    if m:
        for c in list(m[0]): m[0].remove(c)
        m[0].text=f"{s['display']} · {s['category']} · "; sp=etree.SubElement(m[0],'span',id='readTime'); sp.text='3 min di lettura'
    # remove figures for new Iceland to avoid false AI claims; preserve CIA existing image
    if s['slug'].startswith('islanda-'):
        for f in doc.xpath('//figure[contains(concat(" ",normalize-space(@class)," ")," article-image ")]'): f.getparent().remove(f)
    # insights: replace/create
    ins=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-insight ")]')
    if ins:
        grid=ins[0].xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," cm-insight-grid ")]')[0]
        for c in list(grid): grid.remove(c)
        vals = [('31 agosto','scadenza attuale dei controlli'),('1 mese','proroga ipotizzata'),('Schengen','quadro europeo coinvolto')] if s['slug'].startswith('italia-') else ([('25 agosto','visita non annunciata a Mosca'),('3 leader','ipotesi di vertice'),('Nessuna data','incontro non ancora concordato')] if s['slug'].startswith('cia-') else [('2009','domanda di adesione islandese'),('No','esito del referendum'),('Schengen','l’Islanda resta nell’area di libera circolazione')])
        for b,sm in vals:
            d=etree.SubElement(grid,'div'); be=etree.SubElement(d,'b'); be.text=b; se=etree.SubElement(d,'small'); se.text=sm
    art=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
    art.set('data-length-policy','2000-4500')
    for c in list(art): art.remove(c)
    art.text=None
    for ptxt in s['body']:
        p=etree.SubElement(art,'p'); p.text=ptxt
    # remove knowledge hooks/flow continuation
    for n in doc.xpath('//aside[contains(concat(" ",normalize-space(@class)," ")," cm-knowledge-hook ")] | //div[contains(concat(" ",normalize-space(@class)," ")," art-flow-continuation ")]'):
        if n.getparent() is not None: n.getparent().remove(n)
    src=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]')
    if src:
        ul=src[0].xpath('./ul')
        if not ul: ul=[etree.SubElement(src[0],'ul')]
        for c in list(ul[0]): ul[0].remove(c)
        for u,lbl in s['sources']:
            li=etree.SubElement(ul[0],'li'); a=etree.SubElement(li,'a',href=u,target='_blank',rel='noopener noreferrer'); a.text=lbl
        sm=src[0].xpath('.//small')
        if sm: sm[0].text='Testo originale CurioMondo. Le informazioni non ancora formalizzate o confermate ufficialmente sono indicate come tali.'
    # related remove old links if stale; keep section if exists
    path.write_text('<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')

for s in stories: page_from_existing(s)

# update feeds/search/home
hp=ROOT/'assets/data/home-feed-v210.json'; h=json.load(open(hp,encoding='utf-8')); h['version']=VERSION
urls={'/notizie/'+s['slug']+'.html' for s in stories}
items=[x for x in h['items'] if x.get('url') not in urls]
for s in stories:
    items.append({'title':s['title'],'excerpt':s['excerpt'],'url':'/notizie/'+s['slug']+'.html','section':s['section'],'dateISO':s['updated'],'dateLabel':'2026-08-30','image':s['image'],'imageAlt':'Illustrazione editoriale coerente con la notizia','imageWidth':960,'imageHeight':640,'srcset':s['image']+' 960w'})
items.sort(key=lambda x:x.get('dateISO',''),reverse=True); h['items']=items
hp.write_text(json.dumps(h,ensure_ascii=False,indent=2),encoding='utf-8')
sp=ROOT/'assets/data/search-index-v210.json'; sd=json.load(open(sp,encoding='utf-8')); sd['version']=VERSION
sd['items']=[x for x in sd['items'] if x.get('url') not in urls]
for s in reversed(stories): sd['items'].insert(0,{'title':s['title'],'excerpt':s['excerpt'],'url':'/notizie/'+s['slug']+'.html','section':s['section']})
sp.write_text(json.dumps(sd,ensure_ascii=False,indent=2),encoding='utf-8')

# update home by mimicking current structure
p=ROOT/'index.html'; doc=html.fromstring(p.read_text(encoding='utf-8')); news=[x for x in items if x.get('url','').startswith('/notizie/')]
for ti,track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
    for c in list(track): track.remove(c)
    for it in news[:10]:
        a=etree.SubElement(track,'a',href=it['url']); a.set('class','ticker-news'); a.text=it['title'];
        if ti==1: a.set('tabindex','-1')
# don't change hero, just rails/cards
rail=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
for c in list(rail): rail.remove(c)
def pic(it):
    return f'<picture><img alt="{escape(it.get("imageAlt",""),quote=True)}" decoding="async" loading="lazy" height="533" sizes="(max-width:600px) 79vw,300px" src="{it.get("image","")}" srcset="{it.get("srcset",it.get("image","")+" 960w")}" width="800"></picture>'
for it in news[:5]:
    rail.append(html.fragment_fromstring(f'<a class="auto-card" href="{it["url"]}">{pic(it)}<div class="abody"><div class="ameta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
cards=doc.xpath('//div[@id="cards"]')[0]
for c in list(cards): cards.remove(c)
for it in news[5:23]: cards.append(html.fragment_fromstring(f'<a class="card" href="{it["url"]}">{pic(it)}<div class="body"><div class="meta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
p.write_text('<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')

# archive rebuild from feed, preserve any existing labels
a=ROOT/'notizie/index.html'; adoc=html.fromstring(a.read_text(encoding='utf-8')); ul=adoc.xpath('//main//ul')[0]
for c in list(ul): ul.remove(c)
for it in news:
    li=etree.SubElement(ul,'li'); aa=etree.SubElement(li,'a',href=it['url']); st=etree.SubElement(aa,'strong'); st.text=it['title']; spn=etree.SubElement(aa,'span'); spn.text=it['dateLabel']
pars=adoc.xpath('//main/p')
if pars: pars[0].text=f'{len(news)} articoli, ordinati per data.'
a.write_text('<!doctype html>'+html.tostring(adoc,encoding='unicode',method='html'),encoding='utf-8')

# sitemap append/update
sm=ROOT/'news-sitemap.xml'; txt=sm.read_text(encoding='utf-8')
for s in stories:
    loc='https://curiomondo.it/notizie/'+s['slug']+'.html'
    if loc not in txt:
        block=f'\n<url><loc>{loc}</loc><news:news><news:publication><news:name>CurioMondo</news:name><news:language>it</news:language></news:publication><news:publication_date>{s["updated"]}</news:publication_date><news:title>{escape(s["title"])}</news:title></news:news></url>\n'
        txt=txt.replace('</urlset>',block+'</urlset>')
sm.write_text(txt,encoding='utf-8')

# release notes
(ROOT/'RELEASE-NOTES-v249.md').write_text('''# CurioMondo v249 — aggiornamento notizie 30 agosto 2026\n\n- Aggiornato l’articolo Italia-Spagna con l’orientamento verso una proroga dei controlli legati alla crisi di Ceuta, mantenendo esplicito che la decisione non è ancora ufficiale.\n- Aggiornato l’articolo sulla missione del direttore CIA John Ratcliffe a Mosca con la proposta di un possibile vertice Trump-Putin-Zelensky, non ancora concordato.\n- Pubblicato il nuovo articolo sul referendum islandese che boccia la riapertura dei negoziati di adesione all’UE.\n- Aggiornati homepage, LIVE, Ultime notizie, archivio, ricerca e news sitemap.\n- Applicata la policy v248: corpi articolo tra 2.000 e 4.500 caratteri e niente ripetizioni artificiali.\n''',encoding='utf-8')

# zip
out=ROOT.parent/'curiomondo-v249-30-agosto-2026-notizie-netlify.zip'
if out.exists(): out.unlink()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for f in ROOT.rglob('*'):
        if f.is_file(): z.write(f,f.relative_to(ROOT))
print(out)
