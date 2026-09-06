#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from html import escape
import hashlib
import json
import runpy
import xml.etree.ElementTree as ET

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
VERSION = 286
DATE = "2026-09-06"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

STORIES = [
    {
        "slug": "leclerc-incidente-terzo-giro-gp-monza-ritiro-6-settembre-2026",
        "title": "F1, incidente per Leclerc al terzo giro a Monza: illeso, ma costretto al ritiro",
        "excerpt": "Il ferrarista è finito contro le barriere nelle prime fasi del Gran Premio d’Italia. È uscito da solo dall’abitacolo; la gara è stata fermata con la bandiera rossa.",
        "section": "Sport / Formula 1 / GP d’Italia",
        "published": "2026-09-06T15:08:00+02:00",
        "image_key": "charles-leclerc-ritratto-incidente-monza-6-settembre-2026-ai-v286",
        "image_alt": "Ritratto editoriale neutrale generato con IA di Charles Leclerc in tuta rossa, senza rappresentare l’incidente o conseguenze fisiche",
        "sensitive": True,
        "insights": [("3° giro", "il momento dell’incidente"), ("Illeso", "Leclerc è uscito dall’abitacolo"), ("Bandiera rossa", "gara sospesa per mettere in sicurezza la pista")],
        "evergreen": ("/approfondimenti/sicurezza-formula-1-halo-cellula-sopravvivenza.html", "Come proteggono il pilota halo e cellula di sopravvivenza"),
        "related": [
            ("/notizie/monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026.html", "Monza", "Vettel e la F2002, il tributo prima della gara"),
            ("/notizie/eurovolley-italia-polonia-3-1-finale-turchia-5-settembre-2026.html", "Sport", "EuroVolley, Italia in finale"),
            ("/notizie/sinner-us-open-ritiro-ginocchio-2026.html", "Tennis", "Sinner e il ritiro per il ginocchio")],
        "sources": [
            ("https://www.formula1.com/en/racing/2026/italy", "Formula 1 — pagina ufficiale del GP d’Italia 2026"),
            ("https://www.formula1.com/en/latest/article/the-starting-grid-for-the-2026-italian-grand-prix.6fzYcw5rNkuRXbj4pvH8ul", "Formula 1 — griglia ufficiale del Gran Premio"),
            ("https://www.theguardian.com/sport/live/2026/sep/06/italian-grand-prix-formula-one-f1-live", "The Guardian — diretta del Gran Premio d’Italia")],
        "body": [
            "Charles Leclerc si è ritirato dal Gran Premio d’Italia dopo un incidente avvenuto al terzo giro. Il pilota della Ferrari è andato dritto in curva e la monoposto ha colpito le barriere protettive. Leclerc è uscito da solo dall’abitacolo ed è apparso illeso: questo è il dato più importante nel primo aggiornamento disponibile.",
            "La direzione gara ha esposto la <strong>bandiera rossa</strong>, cioè ha sospeso la corsa e ordinato alle vetture di rientrare lentamente ai box. Non è una semplice neutralizzazione: viene usata quando la pista non può essere percorsa in sicurezza, per esempio perché devono intervenire i commissari, rimuovere una vettura o controllare e riparare le protezioni.",
            "L’episodio ha chiuso quasi subito la gara del ferrarista davanti al pubblico di Monza. Leclerc era partito dalla terza posizione, dopo la penalità assegnata a Oscar Piastri, e si trovava quindi nel gruppo di testa. Nelle prime tornate le monoposto sono vicine, i pneumatici non hanno ancora raggiunto un comportamento stabile e ogni traiettoria contesa lascia margini ridotti; questa è una spiegazione generale della fase di gara, non un’attribuzione automatica della causa dell’incidente.",
            "Le immagini televisive e la dinamica completa dovranno essere esaminate dalla direzione gara prima di stabilire se il fuori pista sia nato da un errore, da un contatto, da una perdita improvvisa di aderenza o da più fattori insieme. In Formula 1 la <strong>telemetria</strong> — i dati registrati dalla vettura su velocità, freno, acceleratore, sterzo e numerosi parametri tecnici — permette ai commissari e alla squadra di ricostruire con precisione ciò che è accaduto.",
            "Uscire autonomamente dall’abitacolo non rende l’urto trascurabile. Dopo un impatto, il pilota viene normalmente sottoposto ai controlli previsti e la monoposto è analizzata per verificare quali componenti abbiano assorbito l’energia. Le informazioni sanitarie oltre alla constatazione che Leclerc è uscito illeso non vanno anticipate senza una comunicazione ufficiale.",
            "Le moderne Formula 1 sono costruite intorno alla <strong>cellula di sopravvivenza</strong>, una struttura molto resistente in materiale composito che circonda il pilota. Le parti anteriori, posteriori e laterali sono progettate per deformarsi in modo controllato: invece di trasferire tutta l’energia al corpo, cercano di dissiparne una parte rompendosi secondo schemi verificati nei crash test. Anche l’halo, l’arco sopra l’abitacolo, protegge soprattutto testa e casco da ruote, detriti e intrusioni.",
            "Questi sistemi non eliminano il rischio e non consentono di attribuire a un singolo dispositivo l’esito di questo incidente senza dati tecnici. Spiegano però perché un impatto spettacolare può concludersi con il pilota capace di allontanarsi da solo. CurioMondo ha raccolto il funzionamento delle protezioni nella guida <a href=\"/approfondimenti/sicurezza-formula-1-halo-cellula-sopravvivenza.html\">come proteggono il pilota halo, cellula di sopravvivenza e zone deformabili</a>.",
            "Per la Ferrari il ritiro pesa sul risultato sportivo, ma la priorità immediata resta la sicurezza. La ripartenza può avvenire soltanto quando i commissari hanno liberato la pista, controllato le barriere e ricevuto l’autorizzazione della direzione gara. Il risultato finale, eventuali decisioni dei commissari e una diagnosi tecnica della causa saranno elementi separati da aggiornare solo dopo comunicazioni verificabili.",
            "La giornata era iniziata con il tributo alla storia Ferrari e con <a href=\"/notizie/monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026.html\">Sebastian Vettel al volante della F2002 di Michael Schumacher</a>. Il contrasto tra memoria sportiva e incidente ricorda che la Formula 1 contemporanea unisce velocità estreme e procedure di sicurezza sviluppate in decenni di ricerca, prove e lezioni apprese in pista."
        ]
    },
    {
        "slug": "monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026",
        "title": "Monza, da Sinner a Elkann e Chiellini: Vettel riporta in pista la F2002 di Schumacher",
        "excerpt": "Sportivi, imprenditori e artisti nel paddock del GP d’Italia. Prima della gara Sebastian Vettel ha guidato la Ferrari F2002, simbolo della stagione 2002 di Michael Schumacher.",
        "section": "Sport / Formula 1 / Monza",
        "published": "2026-09-06T15:03:00+02:00",
        "image_key": "monza-vettel-f2002-schumacher-6-settembre-2026-ai-v286",
        "image_alt": "Scena editoriale generata con IA di Sebastian Vettel accanto a una monoposto rossa dei primi anni Duemila nella corsia box di Monza",
        "sensitive": False,
        "insights": [("F2002", "la monoposto del tributo"), ("30 anni", "dall’arrivo di Schumacher in Ferrari"), ("Monza", "il paddock riunisce sport e spettacolo")],
        "evergreen": ("/approfondimenti/ferrari-f2002-perche-dominante.html", "Perché la Ferrari F2002 è ricordata come una monoposto dominante"),
        "related": [
            ("/notizie/leclerc-incidente-terzo-giro-gp-monza-ritiro-6-settembre-2026.html", "Formula 1", "Leclerc, incidente al terzo giro: è illeso"),
            ("/notizie/sinner-us-open-ritiro-ginocchio-2026.html", "Tennis", "Sinner e il ritiro per il ginocchio"),
            ("/notizie/eurovolley-italia-polonia-3-1-finale-turchia-5-settembre-2026.html", "Sport", "EuroVolley, Italia in finale")],
        "sources": [
            ("https://www.ansa.it/sito/notizie/sport/f1/2026/09/06/da-sinner-a-elkann-e-chiellini-e-parata-di-vip-a-monza_4a2f1aa5-926a-4b79-9cbb-b8b7246a7473.html", "ANSA — ospiti nel paddock e tributo di Vettel"),
            ("https://www.rainews.it/articoli/2026/09/da-sinner-a-elkann-e-chiellini-e-parata-di-vip-a-monza-vettel-gira-con-la-f2002-di-schumacher-43bd8f31-574f-486d-a13d-855918699541.html", "RaiNews — la parata di ospiti al GP d’Italia"),
            ("https://www.reuters.com/sports/formula1/ferrari-celebrate-schumacher-with-monza-livery-2026-09-03/", "Reuters — Ferrari celebra i trent’anni dell’era Schumacher"),
            ("https://www.formula1.com/en/latest/article/the-greatest-f1-car-ever-why-the-ferrari-f2002-is-a-contender.4BVI1mg5OSZVpLC0vQvM3h", "Formula 1 — storia e risultati della Ferrari F2002")],
        "body": [
            "Il paddock di Monza ha riunito campioni dello sport, rappresentanti dell’industria e volti dello spettacolo nelle ore che precedono il Gran Premio d’Italia. Tra gli ospiti segnalati ci sono Jannik Sinner, Federica Brignone, John Elkann, l’amministratore delegato Ferrari Benedetto Vigna e Giorgio Chiellini. Con loro anche il pilota Marco Bezzecchi, Matteo Berrettini, Ghali e Alessandro Borghese; Alberto Tomba e Valentino Rossi erano attesi nel corso della giornata.",
            "Il <strong>paddock</strong> è l’area riservata dietro i box, dove lavorano squadre, organizzatori, media e ospiti accreditati. Non è soltanto una passerella: è il centro logistico e relazionale del fine settimana, lo spazio in cui attività sportive, comunicazione e rapporti commerciali si incontrano senza confondersi con la pista.",
            "Sinner è arrivato accompagnato dal padre dopo avere rinunciato agli US Open per il problema al ginocchio. La presenza del numero uno del tennis italiano ha attirato grande attenzione, così come quella di Brignone e Chiellini. L’elenco degli ospiti racconta l’effetto Monza: il Gran Premio è una competizione, ma anche uno dei principali eventi pubblici dello sport italiano.",
            "Il momento più legato alla memoria della Formula 1 è stato affidato a Sebastian Vettel. Il quattro volte campione del mondo ha guidato la Ferrari F2002 associata ai successi di Michael Schumacher, riportando in movimento una monoposto che appartiene a un’epoca tecnica molto diversa da quella attuale. Il tributo celebra trent’anni dall’arrivo del pilota tedesco in Ferrari e dalla sua prima vittoria a Monza con la squadra, nel 1996.",
            "La F2002 non è importante soltanto perché vinse molto. Fu progettata come un insieme estremamente coerente: telaio leggero, aerodinamica efficiente, motore V10, cambio compatto e affidabilità permisero alla Ferrari di essere veloce su circuiti differenti. Formula 1 ricorda che la vettura vinse 14 dei 15 Gran Premi disputati nel 2002 e che Schumacher conquistò il titolo con larghissimo anticipo.",
            "Il termine <strong>V10</strong> indica un motore con dieci cilindri disposti su due bancate a forma di V. Quel suono acuto, legato ai regimi di rotazione molto elevati, è diventato una firma emotiva di quell’epoca. Le monoposto moderne usano invece unità ibride turbo più efficienti e recuperano energia: confrontare i tempi senza considerare regolamenti, pneumatici e sicurezza sarebbe quindi fuorviante.",
            "Guidare una monoposto storica durante un evento dimostrativo richiede comunque preparazione. Posizione di guida, comandi, frenata e procedure non sono quelli di un’automobile stradale; inoltre i componenti devono essere controllati e portati gradualmente alla temperatura corretta. Un <strong>demo run</strong>, letteralmente giro dimostrativo, non è una gara né una prova cronometrata: serve a mostrare il mezzo in movimento in condizioni pianificate.",
            "Il passaggio di Vettel aggiunge un legame personale. Il tedesco ha corso per la Ferrari dal 2015 al 2020 e ha indicato Schumacher come riferimento della propria formazione sportiva. Vederlo sulla F2002 collega tre generazioni: l’era vincente dei primi anni Duemila, l’esperienza di Vettel a Maranello e il pubblico di oggi.",
            "Per capire perché quella macchina sia diventata un simbolo, e perché dominare non significhi soltanto avere più potenza, è disponibile l’approfondimento <a href=\"/approfondimenti/ferrari-f2002-perche-dominante.html\">Ferrari F2002: progetto, motore V10 e ragioni del dominio</a>. La guida separa i risultati dal mito e spiega in modo semplice il rapporto tra aerodinamica, peso, affidabilità e strategia.",
            "La festa che ha preceduto il via non modifica il valore sportivo della gara, ma mostra perché Monza abbia un’identità particolare. Il circuito viene chiamato spesso “Tempio della velocità” per le sue medie elevate e la lunga storia; la sua forza culturale nasce anche dalla capacità di trasformare una giornata di Formula 1 in un incontro tra memoria, tecnologia e sport italiani."
        ]
    }
]

DEEP_DIVES = [
    {
        "slug":"ferrari-f2002-perche-dominante", "title":"Ferrari F2002: perché è ricordata come una Formula 1 dominante", "section":"Approfondimento · Formula 1 / Tecnica", "excerpt":"Motore V10, aerodinamica, cambio e affidabilità: come un progetto equilibrato trasformò velocità e costanza in una stagione storica.", "news":STORIES[1]["slug"],
        "body":[
            "La Ferrari F2002 è una delle monoposto più celebrate della Formula 1 moderna perché unì prestazione, affidabilità e capacità di adattarsi a circuiti molto diversi. Definirla “dominante” non significa soltanto osservare quante gare vinse: vuol dire capire quanto spesso permise ai piloti di sfruttare il potenziale senza essere fermati da guasti o da un comportamento imprevedibile.",
            "Il progetto nacque per la stagione 2002 ma debuttò soltanto quando Ferrari ritenne completati i controlli. Questa prudenza aiuta a capire un principio della Formula 1: una vettura leggermente più veloce ma fragile può raccogliere meno punti di una macchina che conclude quasi tutte le gare. La F2002 riuscì a essere entrambe le cose, rapida e affidabile.",
            "Il cuore era un <strong>motore V10</strong>, cioè dieci cilindri disposti su due file inclinate. Ferrari indica per quella vettura una potenza massima di circa 835 cavalli a 17.800 giri al minuto. Il dato impressiona, ma la qualità utile non era soltanto il picco: contavano erogazione, peso, raffreddamento e integrazione con il telaio.",
            "L’<strong>aerodinamica</strong> studia come l’aria scorre attorno alla vettura. Ali e fondo generano carico, una forza che spinge la monoposto verso l’asfalto e aumenta l’aderenza in curva senza aggiungere massa. Se il carico cresce troppo, però, aumenta anche la resistenza all’avanzamento e si perde velocità in rettilineo. La F2002 trovò un equilibrio efficace tra queste esigenze.",
            "Un cambio compatto e rapido contribuiva a ridurre gli intervalli tra una marcia e l’altra. La disposizione degli organi meccanici permetteva inoltre di curare la forma della parte posteriore e il flusso d’aria. In una Formula 1 ogni componente influenza gli altri: un motore potente ma difficile da raffreddare obbliga ad aprire la carrozzeria, mentre una trasmissione ingombrante limita le scelte aerodinamiche.",
            "La vettura vinse 14 dei 15 Gran Premi ai quali partecipò nel 2002; Michael Schumacher conquistò il titolo dopo 11 delle 17 gare del campionato. Questi numeri descrivono un margine sportivo eccezionale, ma furono anche il risultato del lavoro ai box, delle strategie e della capacità dei piloti di evitare errori.",
            "Il <strong>pacchetto</strong>, parola frequente nel motorsport, indica proprio l’insieme di macchina, pneumatici, piloti e organizzazione. Nessuna singola innovazione spiega da sola il dominio. La F2002 è ricordata perché quasi ogni elemento funzionava bene insieme e lasciava agli avversari pochi punti deboli da sfruttare.",
            "Rispetto alle Formula 1 contemporanee, la F2002 era più leggera, priva dell’attuale sistema ibrido e costruita secondo regole aerodinamiche differenti. Per questo un confronto diretto dei tempi sul giro dice poco. Più utile è confrontare quanto ciascuna vettura superasse le rivali della propria epoca.",
            "Il ritorno della monoposto a Monza con Sebastian Vettel non riscrive la storia né replica una gara originale: è un giro dimostrativo. Il suo valore sta nel rendere visibile una fase tecnica e sportiva che molti ricordano soprattutto attraverso risultati e filmati. La notizia collegata racconta <a href=\"/notizie/monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026.html\">il tributo di Vettel e gli ospiti presenti a Monza</a>."
        ]
    },
    {
        "slug":"sicurezza-formula-1-halo-cellula-sopravvivenza", "title":"Sicurezza in Formula 1: come funzionano halo e cellula di sopravvivenza", "section":"Approfondimento · Formula 1 / Sicurezza", "excerpt":"Dalla struttura in carbonio alle zone deformabili: che cosa protegge il pilota durante un impatto e perché nessun dispositivo lavora da solo.", "news":STORIES[0]["slug"],
        "body":[
            "Una Formula 1 protegge il pilota attraverso più sistemi progettati per lavorare insieme. Non esiste un singolo elemento capace di rendere innocuo ogni incidente: la sicurezza nasce dalla resistenza dell’abitacolo, dalla deformazione controllata di altre parti, dai dispositivi che trattengono corpo e testa, dalle barriere e dalla rapidità dei soccorsi.",
            "La <strong>cellula di sopravvivenza</strong>, chiamata anche monoscocca, è la struttura rigida che circonda il pilota. È realizzata soprattutto con materiali compositi in fibra di carbonio, leggeri ma molto resistenti. Prima di essere ammessa alle gare deve superare prove di urto e carico stabilite dalla federazione.",
            "Attorno alla cellula ci sono <strong>strutture deformabili</strong>. Il loro compito è assorbire energia schiacciandosi in modo previsto, così una parte minore della decelerazione raggiunge il corpo. È lo stesso principio generale delle zone a deformazione programmata nelle automobili, applicato a velocità, pesi e geometrie specifiche del motorsport.",
            "L’<strong>halo</strong> è l’arco protettivo in titanio montato sopra l’abitacolo. Serve soprattutto a deviare oggetti grandi, ruote o parti di vettura e a limitare l’intrusione nell’area della testa. La sua forma lascia al pilota una visuale centrale divisa da un montante; il cervello impara rapidamente a ignorarlo, come accade con il montante del parabrezza di un’auto.",
            "Casco e sistema HANS completano la protezione superiore. HANS significa Head and Neck Support: è un dispositivo appoggiato sulle spalle e collegato al casco, che limita il movimento violento della testa in avanti. Le cinture a più punti trattengono il busto e distribuiscono le forze su aree adatte a sopportarle.",
            "Anche il sedile viene costruito sulla forma del pilota e può essere estratto con lui in determinate procedure di soccorso. Indumenti ignifughi, guanti, scarpe e biancheria tecnica rallentano la trasmissione del calore. “Ignifugo” non significa che non possa bruciare per sempre: indica un materiale progettato per resistere alla fiamma per il tempo richiesto dai test.",
            "La telemetria e i sensori registrano l’intensità dell’impatto. Se viene superata una soglia, il controllo medico diventa obbligatorio anche quando il pilota appare cosciente e cammina. È una precauzione importante perché alcuni effetti di una forte decelerazione non sono visibili dall’esterno.",
            "Le barriere completano il sistema. Elementi metallici, pneumatici legati e moduli capaci di assorbire energia vengono scelti in base al punto del circuito e all’angolo probabile degli urti. Dopo un incidente la direzione gara può esporre la bandiera rossa per consentire ispezioni e riparazioni senza vetture in transito.",
            "Dire che un pilota è uscito illeso non permette di sapere quale componente sia stato decisivo. Gli ingegneri analizzano dati e danni, mentre le autorità sportive verificano eventuali miglioramenti. La sicurezza progredisce proprio trasformando ogni informazione in nuovi standard, senza presentare un singolo episodio come prova assoluta.",
            "Questi principi aiutano a leggere con cautela le prime notizie di un incidente. Nel caso collegato, <a href=\"/notizie/leclerc-incidente-terzo-giro-gp-monza-ritiro-6-settembre-2026.html\">Charles Leclerc è uscito dall’abitacolo dopo l’impatto a Monza</a>; cause tecniche e valutazioni dettagliate richiedono comunicazioni ufficiali, separate dall’osservazione immediata che il pilota era in piedi."
        ]
    }
]

def article_html(s):
    canonical=f"https://curiomondo.it/notizie/{s['slug']}.html"; image=f"https://curiomondo.it/assets/images/editorial-auto/{s['image_key']}-1200.webp"
    schema={"@context":"https://schema.org","@type":"NewsArticle","headline":s["title"],"description":s["excerpt"],"datePublished":s["published"],"dateModified":s["published"],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},"image":[image]}
    attrs='data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="true" data-portrait-format="neutral-isolated"' if s['sensitive'] else 'data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false" data-portrait-format="contextual-editorial-scene"'
    insights=''.join(f'<div><b>{escape(a)}</b><small>{escape(b)}</small></div>' for a,b in s['insights'])
    related=''.join(f'<a href="{u}"><small>{escape(k)}</small><strong>{escape(t)}</strong></a>' for u,k,t in s['related'])
    sources=''.join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in s['sources'])
    body=''.join(f'<p>{p}</p>' for p in s['body'])
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(s['title'])} | CurioMondo</title><meta name="description" content="{escape(s['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(s['title'],quote=True)}"><meta property="og:description" content="{escape(s['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(s['image_alt'],quote=True)}"><meta name="theme-color" content="#eaf8ff"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=286"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{s['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(s['section'])}</div><h1>{escape(s['title'])}</h1><p class="subtitle">{escape(s['excerpt'])}</p><div class="meta">6 settembre 2026 · aggiornato alle {s['published'][11:16]} · {escape(s['section'])} · <span id="readTime">4 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" {attrs}><picture><img src="../assets/images/editorial-auto/{s['image_key']}-800.webp" srcset="../assets/images/editorial-auto/{s['image_key']}-480.webp 480w, ../assets/images/editorial-auto/{s['image_key']}-800.webp 800w, ../assets/images/editorial-auto/{s['image_key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(s['image_alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="3000-7000">{body}</article><section aria-labelledby="cm-evergreen-question" class="cm-evergreen-reader"><small>Una cosa utile da sapere</small><h2 id="cm-evergreen-question">{escape(s['evergreen'][1])}</h2><a href="{s['evergreen'][0]}">Leggi l’approfondimento →</a></section><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 6 settembre 2026, ore {s['published'][11:16]} italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=286" defer></script></body></html>'''

def deep_html(d):
    canonical=f"https://curiomondo.it/approfondimenti/{d['slug']}.html"; body=''.join(f'<p>{p}</p>' for p in d['body'])
    schema={"@context":"https://schema.org","@type":"Article","headline":d["title"],"description":d["excerpt"],"datePublished":"2026-09-06T15:10:00+02:00","dateModified":"2026-09-06T15:10:00+02:00","mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo"},"publisher":{"@type":"Organization","name":"CurioMondo"}}
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(d['title'])} | CurioMondo</title><meta name="description" content="{escape(d['excerpt'],quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=286"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/approfondimenti/" aria-label="Torna agli approfondimenti"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(d['section'])}</div><h1>{escape(d['title'])}</h1><p class="subtitle">{escape(d['excerpt'])}</p><div class="meta">Aggiornato il 6 settembre 2026 · 4 min di lettura</div><article class="art-body">{body}</article><section aria-labelledby="cm-news-link" class="cm-evergreen-reader"><small>Notizia collegata</small><h2 id="cm-news-link">Aggiornamento dal Gran Premio d’Italia</h2><a href="/notizie/{d['news']}.html">Leggi la notizia →</a></section><div class="art-sources"><h2>Fonti consultate</h2><ul><li><a href="https://www.formula1.com/" rel="noopener noreferrer" target="_blank">Formula 1 — archivio tecnico e sportivo ufficiale</a></li><li><a href="https://www.fia.com/" rel="noopener noreferrer" target="_blank">FIA — regolamenti tecnici e standard di sicurezza</a></li><li><a href="https://www.ferrari.com/en-EN/formula1/f2002" rel="noopener noreferrer" target="_blank">Ferrari — scheda storica F2002</a></li></ul></div></main><footer class="site-footer"><a href="/approfondimenti/">Altri approfondimenti</a></footer></body></html>'''

for s in STORIES:
    (ROOT/'notizie'/f"{s['slug']}.html").write_text(article_html(s),encoding='utf-8')
for d in DEEP_DIVES:
    page=deep_html(d).replace('href="/approfondimenti/" aria-label="Torna agli approfondimenti"','href="/" aria-label="Torna alla home di CurioMondo"',1)
    (ROOT/'approfondimenti'/f"{d['slug']}.html").write_text(page,encoding='utf-8')

# Registro immagini, con hash dei file realmente distribuiti.
rp=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(rp.read_text(encoding='utf-8')); reg['version']=VERSION
new_keys={s['image_key'] for s in STORIES}; reg['items']=[i for i in reg['items'] if i.get('key') not in new_keys]
prompts={STORIES[0]['image_key']:"Neutral editorial portrait of Charles Leclerc, isolated against a simple studio background; no crash, injury or reenactment.", STORIES[1]['image_key']:"Ultra-realistic editorial scene of Sebastian Vettel beside an F2002-inspired historic red Formula 1 car in the Monza pit lane."}
for s in STORIES:
    variants=[]
    for w in (480,800,1200):
        p=ROOT/'assets/images/editorial-auto'/f"{s['image_key']}-{w}.webp"; variants.append({'w':w,'src':f"/assets/images/editorial-auto/{p.name}",'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    reg['items'].insert(0,{'key':s['image_key'],'article':f"/notizie/{s['slug']}.html",'aiGenerated':True,'syntheticLikeness':'public-figure','sensitiveContext':s['sensitive'],'documentaryPhoto':False,'prompt':prompts[s['image_key']],'variants':variants,'alt':s['image_alt'],'disclosure':CAPTION,'portraitOnly':s['sensitive'],'portraitFormat':'neutral-isolated' if s['sensitive'] else 'contextual-editorial-scene','reenactedEvent':False})
rp.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Riutilizza il finalizzatore canonico: ricostruisce ordine, home, archivio, feed e sitemap dalle pagine reali.
runpy.run_path(str(ROOT/'tools/finalize_articles_20260906.py'),run_name='__main__')

# Versione e contenuti evergreen dopo la ricostruzione news.
for rel in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
    p=ROOT/rel; data=json.loads(p.read_text(encoding='utf-8')); data['version']=VERSION
    if rel.endswith('search-index-v210.json'):
        entries=[{'title':d['title'],'excerpt':d['excerpt'],'url':f"/approfondimenti/{d['slug']}.html",'section':d['section'].replace('Approfondimento · ','')} for d in DEEP_DIVES]
        urls={e['url'] for e in entries}; data['items']=entries+[x for x in data['items'] if x.get('url') not in urls]
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Prepend delle nuove guide nell'archivio approfondimenti.
ap=ROOT/'approfondimenti/index.html'; doc=html.fromstring(ap.read_text(encoding='utf-8')); grid=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," grid ")]')[0]
for old in grid.xpath('./a[@data-cm-evergreen-slug="ferrari-f2002-perche-dominante" or @data-cm-evergreen-slug="sicurezza-formula-1-halo-cellula-sopravvivenza"]'): grid.remove(old)
for d in reversed(DEEP_DIVES):
    a=html.fragment_fromstring(f'<a class="card" href="../approfondimenti/{d["slug"]}.html" data-cm-evergreen-slug="{d["slug"]}"><span class="tag">{escape(d["section"])}</span><div><h2>{escape(d["title"])}</h2><p>{escape(d["excerpt"])}</p></div><b>Leggi l’approfondimento →</b></a>')
    grid.insert(0,a)
ap.write_text('<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')

# Sitemap generale: aggiunge le due guide e assicura la versione release.
SM='http://www.sitemaps.org/schemas/sitemap/0.9'; sp=ROOT/'sitemap.xml'; tree=ET.parse(sp); root=tree.getroot(); existing={n.text for n in root.findall(f'{{{SM}}}url/{{{SM}}}loc')}
for d in reversed(DEEP_DIVES):
    url=f"https://curiomondo.it/approfondimenti/{d['slug']}.html"
    if url not in existing:
        n=ET.Element(f'{{{SM}}}url'); ET.SubElement(n,f'{{{SM}}}loc').text=url; ET.SubElement(n,f'{{{SM}}}lastmod').text=DATE; root.insert(0,n)
ET.indent(tree,space='  '); tree.write(sp,encoding='utf-8',xml_declaration=True)

# Regola permanente richiesta dal proprietario.
contract=ROOT/'automation/prompts/editorial-contract.txt'; c=contract.read_text(encoding='utf-8')
rule="\n- **EVERGREEN E PAROLE DIFFICILI — REGOLA PERMANENTE DEL PROPRIETARIO:** ogni articolo deve offrire un aggancio evergreen utile e autonomo quando il tema lo consente. Termini tecnici, sigle e parole non comuni devono essere spiegati alla prima occorrenza con linguaggio naturale, piacevole e comprensibile, senza trasformare il testo in un glossario e senza ripetizioni.\n"
if 'EVERGREEN E PAROLE DIFFICILI — REGOLA PERMANENTE DEL PROPRIETARIO' not in c: c+=rule
contract.write_text(c,encoding='utf-8')

mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; m['site_version']=VERSION; m['version']=f'v{VERSION}'; m['release_version']=f'v{VERSION}'; m['last_release_date']=DATE
m['permanent_rules']['evergreen_and_plain_language']='Every article must include a useful evergreen knowledge hook when applicable. Explain technical, uncommon or difficult words naturally at first occurrence, in pleasant accessible Italian, without glossary-like interruptions or repetition.'
m['last_release']={'version':VERSION,'date':DATE,'type':'content-update','change':'2 nuovi articoli Formula 1 su Monza: tributo Vettel-F2002 e incidente di Charles Leclerc, con 2 approfondimenti evergreen su F2002 e sicurezza, nuove immagini editoriali IA e regola permanente per spiegare i termini difficili','article_body_policy':'3000-7000'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({'status':'ok','version':VERSION,'articles':[s['slug'] for s in STORIES],'deep_dives':[d['slug'] for d in DEEP_DIVES]},ensure_ascii=False,indent=2))
