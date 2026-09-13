#!/usr/bin/env python3
from pathlib import Path
from html import escape
from PIL import Image
import hashlib, json, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 344
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

ARTICLES = [
{
"slug":"stretto-hormuz-traffico-sette-navi-11-settembre-2026",
"title":"Stretto di Hormuz, colpita una nave commerciale iraniana: un morto",
"excerpt":"Il proiettile ha provocato un incendio al largo di Qeshm. Le autorità iraniane riferiscono quattro feriti; l’equipaggio è stato evacuato e la responsabilità resta sconosciuta.",
"published":"2026-09-13T08:57:00+02:00","modified":"2026-09-13T13:35:00+02:00","date_label":"13 settembre 2026","place":"Qeshm","category":"Mondo / Medio Oriente / Cronaca",
"key":"hormuz-nave-iraniana-qeshm-ai-openai-v344","src":"exec-b47ca0ae-c093-40f8-942b-32ac69b39e53.png",
"alt":"Scena editoriale sensibile generata con IA di una nave commerciale danneggiata vicino a Qeshm con mezzi di soccorso, senza vittime visibili","sensitive":True,"public_figure":False,
"stats":[("1 morto","bilancio riferito dalle autorità iraniane"),("4 feriti","tra i dieci membri dell’equipaggio"),("10 persone","evacuate dalla nave dopo l’incendio")],
"body":[
"Una nave commerciale iraniana è stata colpita da un proiettile domenica 13 settembre al largo dell’isola di Qeshm, nello Stretto di Hormuz. I media statali iraniani riferiscono un morto e quattro feriti tra i dieci membri dell’equipaggio. Le autorità locali hanno evacuato tutte le persone a bordo dopo l’incendio.",
"UK Maritime Trade Operations ha ricevuto da una fonte verificata la segnalazione dell’impatto e del successivo incendio. L’organismo britannico non ha attribuito l’attacco né identificato il tipo di proiettile. La coincidenza tra la segnalazione marittima e il caso descritto dai media iraniani è sostenuta da luogo e tempi, ma i dettagli tecnici restano incompleti.",
"Le autorità iraniane hanno definito l’episodio un atto terroristico, senza presentare pubblicamente prove sull’autore. Nessun soggetto aveva rivendicato l’attacco nelle prime ore. CurioMondo tratta quindi ogni ipotesi sulla responsabilità come non verificata.",
"Il primo bilancio diffuso da alcune testate indicava almeno tre feriti; Associated Press ha poi riportato quattro feriti citando le autorità iraniane. La differenza mostra quanto rapidamente possano cambiare i conteggi durante un’emergenza marittima. Il dato più recente disponibile viene indicato senza cancellare l’incertezza delle prime comunicazioni.",
"L’incendio e l’evacuazione riguardano direttamente la sicurezza dell’equipaggio, mentre l’impatto commerciale dipenderà da durata delle restrizioni e reazione degli armatori. Un singolo incidente non misura da solo il traffico complessivo. Tuttavia può aumentare costi assicurativi, cautela degli operatori e tempi di attraversamento se la minaccia viene considerata persistente.",
"Lo Stretto collega il Golfo Persico al Golfo di Oman ed è una rotta centrale per petrolio e gas. Secondo la U.S. Energy Information Administration, nella prima metà del 2025 vi transitavano in media 20,9 milioni di barili al giorno di petrolio e prodotti liquidi. Questo dato descrive l’esposizione strutturale della rotta, non l’effetto già prodotto dall’attacco odierno.",
"Gli aggiornamenti decisivi riguarderanno l’identità della nave, l’origine del colpo, le condizioni dei feriti e le eventuali misure sulla navigazione. La pagina sarà modificata soltanto in presenza di informazioni sostanziali attribuite ad autorità identificabili o confermate da più fonti indipendenti."
],
"sources":[
("https://apnews.com/article/aa034da0d8226f5a3b4794b10afb8b3b","Associated Press — 13 settembre 2026 — bilancio, evacuazione e comunicazioni iraniane"),
("https://www.reuters.com/business/energy/new-report-attack-strait-hormuz-shipping-fans-fears-threats-oil-supplies-2026-09-13/","Reuters — 13 settembre 2026 — incidente marittimo e contesto della navigazione"),
("https://www.ukmto.org/indian-ocean/recent-incidents","UKMTO — 13 settembre 2026 — segnalazione dell’impatto e dell’incendio"),
("https://www.eia.gov/international/analysis/special-topics/World_Oil_Transit_Chokepoints","U.S. EIA — dati sul ruolo energetico dello Stretto di Hormuz")]
},
{
"slug":"energia-attacchi-rotte-petrolio-pipeline-est-ovest-13-settembre-2026",
"title":"Energia, nuovo allarme globale dopo gli attacchi alle rotte del petrolio",
"excerpt":"La pipeline saudita Est-Ovest, capace di trasportare 4–5 milioni di barili al giorno, è stata fermata per precauzione. La durata dello stop determinerà la pressione effettiva sull’offerta.",
"published":"2026-09-13T13:20:00+02:00","modified":"2026-09-13T13:20:00+02:00","date_label":"13 settembre 2026","place":"Riyadh","category":"Mondo / Economia / Energia",
"key":"energia-pipeline-est-ovest-rotte-petrolio-ai-openai-v344","src":"exec-af0b0a06-8fe7-44d8-b74e-3eafa8744e56.png",
"alt":"Scena editoriale contestuale ordinaria generata con IA della pipeline saudita Est-Ovest verso il Mar Rosso con squadre di ispezione","sensitive":False,"public_figure":False,
"stats":[("4–5 mln","barili trasportati ogni giorno"),("4–5%","quota indicativa dell’offerta mondiale"),("1.200 km","lunghezza approssimativa della pipeline")],
"body":[
"La chiusura precauzionale della pipeline saudita Est-Ovest e il nuovo attacco a una nave nello Stretto di Hormuz aumentano la pressione sulle rotte petrolifere mondiali. Il ministero dell’Energia saudita ha fermato la condotta dopo attacchi nelle regioni di Riyadh e Medina. Le squadre tecniche stanno valutando sicurezza e danni, senza una data pubblica per la ripresa.",
"Negli ultimi mesi l’infrastruttura ha trasportato circa 4–5 milioni di barili al giorno verso il porto di Yanbu, sul Mar Rosso. Questa quantità equivale indicativamente al 4–5% dell’offerta mondiale. Il confronto rende visibile la scala del rischio, ma non significa che l’intero volume sia già scomparso dal mercato.",
"La condotta attraversa per circa 1.200 chilometri l’Arabia Saudita dai giacimenti orientali alla costa occidentale. Il suo valore strategico deriva dalla possibilità di evitare Hormuz. Uno stop prolungato ridurrebbe quindi proprio una delle principali alternative terrestri alla rotta marittima più esposta.",
"L’effetto sui prezzi dipenderà da quattro variabili: durata della chiusura, scorte disponibili, capacità di usare altri terminali e continuità dei passaggi marittimi. Un rincaro immediato incorpora anche il rischio percepito dagli operatori. Non coincide necessariamente con una perdita fisica della stessa quantità di greggio.",
"La Saudi Press Agency ha confermato che gli attacchi hanno provocato feriti e che la chiusura è stata adottata per precauzione. Reuters ha riferito che i droni sarebbero partiti dall’Iraq. L’origine geografica non stabilisce automaticamente mandante o responsabilità politica, che richiedono prove distinte.",
"Il sistema energetico può assorbire interruzioni brevi attraverso scorte, riprogrammazione delle consegne e capacità inutilizzata. Questi margini diventano meno efficaci quando più passaggi vengono messi sotto pressione nello stesso periodo. È l’accumulo degli incidenti, più del singolo episodio, a trasformare un problema locale in rischio globale.",
"I prossimi comunicati sauditi chiariranno condizioni dell’infrastruttura e tempi di riavvio. Serviranno inoltre dati sui flussi effettivi per distinguere l’allarme logistico da una riduzione persistente dell’offerta. Fino ad allora, l’impatto quantitativo resta in sviluppo."
],
"sources":[
("https://www.spa.gov.sa/en/N2674017","Saudi Press Agency — 11 settembre 2026 — chiusura precauzionale e valutazione della sicurezza"),
("https://www.reuters.com/business/energy/saudis-shut-down-oil-pipeline-houthis-tighten-grip-red-sea-shipping-2026-09-12/","Reuters — 12 settembre 2026 — flussi della pipeline e pressione sulle rotte"),
("https://apnews.com/article/025d052a14d9481258d51009a76d0bd6","Associated Press — 11 settembre 2026 — attacchi, chiusura e contesto regionale"),
("https://www.eia.gov/international/analysis/special-topics/World_Oil_Transit_Chokepoints","U.S. EIA — capacità delle rotte alternative e transiti energetici")]
},
{
"slug":"odesa-attacco-russo-droni-cinque-feriti-13-settembre-2026",
"title":"Ucraina, nuovo attacco russo con droni su Odesa: almeno cinque feriti",
"excerpt":"Colpite aree residenziali in più quartieri della città portuale. Il raid arriva un giorno dopo l’attacco che aveva causato due morti e 26 feriti.",
"published":"2026-09-13T12:55:00+02:00","modified":"2026-09-13T12:55:00+02:00","date_label":"13 settembre 2026","place":"Odesa","category":"Mondo / Ucraina / Guerra",
"key":"odesa-attacco-droni-residenze-ai-openai-v344","src":"exec-776de5e2-c910-49b8-80a4-038fc0bf999b.png",
"alt":"Scena editoriale sensibile generata con IA di edifici residenziali danneggiati a Odesa con soccorritori, senza vittime visibili","sensitive":True,"public_figure":False,
"stats":[("5 feriti","bilancio iniziale del nuovo raid"),("2 morti","nell’attacco del giorno precedente"),("26 feriti","nel precedente bilancio su Odesa")],
"body":[
"Almeno cinque persone sono rimaste ferite domenica 13 settembre in un nuovo attacco russo con droni contro Odesa, nel sud dell’Ucraina. Secondo l’amministrazione militare cittadina, sono state danneggiate aree residenziali in diversi quartieri. Le squadre di emergenza stanno completando verifiche e messa in sicurezza.",
"Il capo dell’amministrazione militare, Serhiy Lysak, ha comunicato il bilancio iniziale e la distribuzione dei danni. Le informazioni provengono dalle autorità ucraine presenti sul posto. Reuters ha riportato la comunicazione, ma non ha potuto verificare autonomamente ogni dettaglio nelle prime ore.",
"Il raid segue di circa un giorno un altro attacco sulla città che aveva colpito un edificio residenziale. Quel bilancio indicava due morti e 26 feriti. I due episodi devono restare separati per evitare di sommare vittime appartenenti a comunicazioni e finestre temporali differenti.",
"Odesa ospita il principale sistema portuale ucraino sul Mar Nero. Gli attacchi contro la città possono avere insieme conseguenze civili e logistiche, ma il danno alle abitazioni non dimostra da solo che fossero presenti obiettivi militari. Ogni affermazione sulla natura dei bersagli richiede prove specifiche.",
"I primi conteggi dopo un bombardamento possono cambiare quando i soccorritori raggiungono tutti gli edifici e gli ospedali consolidano gli accessi. Per questo il numero di cinque feriti viene presentato come minimo confermato dalle autorità locali. Non è una stima definitiva dell’impatto.",
"Nella stessa notte sono state segnalate incursioni con droni anche in altre regioni ucraine. L’estensione geografica impegna contemporaneamente difesa aerea e servizi di emergenza. Non consente però di attribuire automaticamente a ogni area la stessa intensità o lo stesso bilancio.",
"Gli sviluppi rilevanti saranno eventuali variazioni delle vittime, informazioni verificate sui danni e una valutazione consolidata delle autorità. Le rivendicazioni militari di Mosca o Kyiv saranno indicate come tali finché non emergeranno riscontri indipendenti."
,
"Per i residenti, la priorità indicata dalle autorità resta evitare le aree interdette e consentire agli artificieri di controllare frammenti e strutture instabili. Questa precauzione riguarda il rischio successivo all’impatto e non aggiunge nuove vittime al bilancio disponibile."
],
"sources":[
("https://www.reuters.com/world/europe/russian-drone-attack-injures-five-ukraines-odesa-officials-say-2026-09-13/","Reuters — 13 settembre 2026 — feriti e danni nei quartieri residenziali"),
("https://t.me/s/odesacityofficial","Amministrazione di Odesa — aggiornamenti ufficiali sui soccorsi e sui danni"),
("https://apnews.com/hub/russia-ukraine","Associated Press — copertura indipendente della guerra e dei raid sulle città ucraine"),
("https://www.president.gov.ua/en/news","Presidenza dell’Ucraina — quadro nazionale degli attacchi e della risposta d’emergenza")]
},
{
"slug":"brics-dichiarazione-new-delhi-medio-oriente-12-settembre-2026",
"title":"BRICS, Modi: tensioni e shock alle forniture minacciano la stabilità",
"excerpt":"Nel secondo giorno del vertice di New Delhi, il premier indiano chiede cooperazione sulle catene di approvvigionamento e sulle materie prime critiche. Intesa anche sull’allerta sanitaria integrata.",
"published":"2026-09-12T21:55:00+02:00","modified":"2026-09-13T12:35:00+02:00","date_label":"12 settembre 2026 · Aggiornato 13 settembre 2026","place":"New Delhi","category":"Mondo / Politica / Diplomazia",
"key":"brics-modi-new-delhi-secondo-giorno-ai-openai-v344","src":"exec-c8f94509-f059-42a0-8d65-4e3024c8a386.png",
"alt":"Scena editoriale contestuale ordinaria generata con IA di Narendra Modi durante il vertice BRICS a New Delhi","sensitive":False,"public_figure":True,
"stats":[("11 membri","Paesi riuniti nel formato BRICS"),("2 giorni","durata del vertice di New Delhi"),("1 sistema","allerta integrata per malattie infettive")],
"body":[
"Narendra Modi ha avvertito domenica 13 settembre che tensioni geopolitiche, guerre e shock nelle forniture minacciano la stabilità globale. Nel secondo giorno del vertice BRICS a New Delhi, il premier indiano ha chiesto una cooperazione più stretta sulle catene di approvvigionamento, sulle tecnologie e sulle materie prime critiche.",
"Modi ha criticato l’uso strategico di tecnologia e minerali essenziali come strumenti di pressione. Il passaggio amplia la dichiarazione comune approvata dal gruppo, che richiama resilienza economica e maggiore rappresentanza dei Paesi emergenti. Non introduce però obblighi vincolanti per i governi membri.",
"Il blocco ha raggiunto anche un’intesa per sviluppare un sistema integrato di allerta precoce sulle malattie infettive. L’obiettivo è condividere più rapidamente segnali epidemiologici e coordinare la preparazione. L’accordo politico dovrà essere seguito da regole tecniche, responsabilità operative e procedure comuni perché il sistema produca risultati misurabili.",
"Il vertice riunisce undici membri con interessi economici e alleanze differenti. Questa eterogeneità rende significativo il consenso su alcuni principi, ma limita l’idea di una posizione unica su ogni crisi. Le dichiarazioni comuni vanno quindi distinte dalle politiche nazionali che ciascun Paese applicherà.",
"Le interruzioni delle forniture incidono in modo diverso su energia, alimenti, componenti industriali e farmaci. Un sistema più resiliente non elimina lo shock: diversifica produttori, rotte e scorte per ridurne la propagazione. Questa è la conseguenza pratica più importante del richiamo di Modi, oltre alla formulazione diplomatica.",
"Sulle materie prime critiche, la cooperazione può riguardare investimenti, lavorazione, riciclo e accesso ai mercati. Restano però possibili conflitti tra sicurezza nazionale e apertura commerciale. Il vertice non ha annunciato un meccanismo unico capace di risolvere automaticamente tali divergenze.",
"La Cina assumerà la presidenza dei BRICS nel 2027. I passaggi da osservare saranno l’attuazione dell’allerta sanitaria, eventuali progetti sulle catene di approvvigionamento e il seguito diplomatico della Dichiarazione di New Delhi. Sono questi gli indicatori che separeranno gli impegni operativi dalle sole intenzioni politiche."
],
"sources":[
("https://www.mea.gov.in/bilateral-documents.htm?dtl/40668/BRICS_New_Delhi_Declaration_Building_for_Resilience_Innovation_Cooperation_and_Sustainability","Ministero degli Esteri dell’India — Dichiarazione ufficiale di New Delhi"),
("https://www.pmindia.gov.in/en/news_updates/","Ufficio del Primo ministro indiano — interventi ufficiali di Narendra Modi al vertice"),
("https://apnews.com/article/72e4329da3bc30ab7b231b2d11aae375","Associated Press — 13 settembre 2026 — secondo giorno, forniture e allerta sanitaria"),
("https://indianexpress.com/article/india/pm-modi-brics-speech-critical-minerals-weaponisation-supply-chain-startups-10876019/","Indian Express — 13 settembre 2026 — discorso su minerali critici e tecnologia")]
},
{
"slug":"meloni-alleanze-sostegno-ucraina-12-settembre-2026",
"title":"Meloni: «Non mi alleo con chi vota contro il sostegno all’Ucraina»",
"excerpt":"La presidente del Consiglio rivendica continuità sulla politica verso Kyiv e respinge cambi di linea per calcolo elettorale. La frase arriva in un’intervista al Foglio.",
"published":"2026-09-13T12:10:00+02:00","modified":"2026-09-13T12:10:00+02:00","date_label":"13 settembre 2026","place":"Roma","category":"Italia / Politica",
"key":"meloni-alleanze-ucraina-intervista-ai-openai-v344","src":"exec-48966cc2-dd78-4679-818f-c2d8b6072b2f.png",
"alt":"Scena editoriale contestuale ordinaria generata con IA di Giorgia Meloni durante un’intervista istituzionale a Roma","sensitive":False,"public_figure":True,
"stats":[("12 settembre","data originaria dell’intervista"),("1 linea","sostegno italiano alla difesa di Kyiv"),("Nessun nome","alleato citato direttamente nella risposta")],
"body":[
"Giorgia Meloni ha dichiarato di non essere disposta ad allearsi con forze che votano contro il sostegno alla difesa dell’Ucraina. La frase è stata pronunciata in un’intervista al Foglio e riportata da ANSA sabato 12 settembre alle 12:58. La presidente del Consiglio ha escluso cambi di posizione dettati dal calcolo politico o elettorale.",
"Meloni ha parlato di sé in terza persona, affermando che non farà il contrario di quanto sostenuto finora. Ha poi rivendicato coerenza e serietà, invitando chi cerca un premier disposto a cambiare linea secondo gli equilibri di partito a rivolgersi altrove.",
"La risposta fissa un criterio politico, ma non contiene il nome di Matteo Salvini o di un’altra forza della maggioranza. Interpretarla come un’esclusione formale di uno specifico alleato andrebbe oltre le parole pronunciate. Il dato verificabile è la condizione posta sul voto relativo al sostegno all’Ucraina.",
"La dichiarazione riguarda il perimetro delle alleanze future più che una decisione immediata del Governo. Non annuncia una crisi di maggioranza, un rimpasto o un nuovo provvedimento militare. Questi scenari richiederebbero atti politici separati.",
"Il passaggio rafforza la continuità della linea italiana a favore di Kyiv. Allo stesso tempo rende più visibile una possibile area di tensione tra partiti che distinguono sostegno politico, aiuti economici e forniture militari. Dire che una forza vota contro uno di questi strumenti non equivale automaticamente a negare ogni forma di sostegno.",
"La data corretta è il 12 settembre per la dichiarazione originaria. La pubblicazione CurioMondo del 13 settembre riflette il momento dell’inserimento e non trasforma la frase in un’affermazione pronunciata oggi. Questa distinzione evita di presentare come ultima ora un contenuto emerso il giorno precedente.",
"Il seguito concreto potrà essere valutato nei prossimi voti parlamentari e nella costruzione delle alleanze. Fino a quel momento la dichiarazione resta una posizione politica esplicita, non un accordo di coalizione già formalizzato."
],
"sources":[
("https://www.ansa.it/sito/notizie/politica/2026/09/12/meloni-non-mi-alleo-con-chi-vota-contro-il-sostegno-allucraina_b2b72aa5-3330-45f7-ba90-f4f0fff133a3.html","ANSA — 12 settembre 2026, ore 12:58 — dichiarazione e contesto dell’intervista"),
("https://www.ilfoglio.it/politica/","Il Foglio — intervista originaria alla presidente del Consiglio"),
("https://www.lanazione.it/ultimaora/meloni-non-mi-alleo-con-f870fe82","La Nazione — 12 settembre 2026 — testo della dichiarazione diffuso da ANSA"),
("https://www.alanews.it/2026/09/12/politica/meloni-a-tutto-campo-le-dichiarazioni-sullucraina-sulleconomia-sulleuropa-e-sullopposizione/","AlaNews — 12 settembre 2026 — quadro più ampio delle posizioni espresse")]
}
]

def render_article(a):
    canonical=f"https://curiomondo.it/notizie/{a['slug']}.html"
    image=f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema={"@context":"https://schema.org","@type":"NewsArticle","headline":a['title'],"description":a['excerpt'],"datePublished":a['published'],"dateModified":a['modified'],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},"image":[image],"creditText":CAPTION}
    paras=''.join(f'<p>{escape(p)}</p>' for p in a['body'])
    sources=''.join(f'<li><a href="{escape(u,quote=True)}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a['sources'])
    stats=''.join(f'<div><strong>{escape(v)}</strong><span>{escape(t)}</span></div>' for v,t in a['stats'])
    figure_attrs=' data-ai-generated="true" data-sensitive-context="'+str(a['sensitive']).lower()+'"'
    if a['public_figure']:
        figure_attrs += ' data-synthetic-likeness="public-figure"'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><meta name="theme-color" content="#071a33"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=344"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(a['category'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">{escape(a['date_label'])} · {escape(a['place'])} · <span id="readTime">4 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button data-share-article type="button">↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image"{figure_attrs}><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{stats}</div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">{paras}</article><section class="curio-related" aria-labelledby="related-title"><h2 id="related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid"><a href="/notizie/"><small>Archivio</small><strong>Altre notizie selezionate</strong></a><a href="/approfondimenti/"><small>Contesto</small><strong>Gli approfondimenti CurioMondo</strong></a></div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 13 settembre 2026, ore italiane.<br>{CAPTION}</small></p></div></main><footer class="site-footer"><nav class="site-footer-links"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=344" defer></script></body></html>'''

outdir=ROOT/'assets/images/editorial-auto'; outdir.mkdir(parents=True,exist_ok=True)
reg_path=ROOT/'assets/data/editorial-images-v210.json'; reg=json.loads(reg_path.read_text(encoding='utf-8'))
for a in ARTICLES:
    src=ROOT.parent/'generated_images'/a['src']
    im=Image.open(src).convert('RGB')
    target_ratio=3/2
    w0,h0=im.size
    if w0/h0 > target_ratio:
        nw=round(h0*target_ratio); left=(w0-nw)//2; im=im.crop((left,0,left+nw,h0))
    elif w0/h0 < target_ratio:
        nh=round(w0/target_ratio); top=(h0-nh)//2; im=im.crop((0,top,w0,top+nh))
    variants=[]
    for w in (480,800,1200):
        f=outdir/f"{a['key']}-{w}.webp"
        im.resize((w,round(w*2/3)),Image.Resampling.LANCZOS).save(f,'WEBP',quality=86,method=6)
        variants.append({'w':w,'src':f'/assets/images/editorial-auto/{f.name}','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
    (ROOT/'notizie'/f"{a['slug']}.html").write_text(render_article(a),encoding='utf-8')
    reg['items']=[i for i in reg['items'] if i.get('article')!=f"/notizie/{a['slug']}.html"]
    item={'key':a['key'],'article':f"/notizie/{a['slug']}.html",'aiGenerated':True,'sensitiveContext':a['sensitive'],'documentaryPhoto':False,'variants':variants,'alt':a['alt'],'disclosure':CAPTION,'portraitOnly':False,'portraitFormat':'contextual-editorial-scene','reenactedEvent':False}
    if a['public_figure']: item['syntheticLikeness']='public-figure'
    reg['items'].insert(0,item)
reg['version']=VERSION; reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Pre-semina i campi editoriali richiesti per la nuova card principale. Il
# finalizzatore conserva questi campi mentre ricostruisce dati e homepage.
home_seed=ROOT/'assets/data/home-feed-v210.json'
seed=json.loads(home_seed.read_text(encoding='utf-8'))
energy_url='/notizie/energia-attacchi-rotte-petrolio-pipeline-est-ovest-13-settembre-2026.html'
seed['items']=[i for i in seed.get('items',[]) if i.get('url')!=energy_url]
seed['items'].insert(0,{
    'url':energy_url,
    'featuredHighlights':['allarme globale','rotte del petrolio'],
    'featuredStats':[
        {'icon':'◆','value':'4–5 mln','label':'barili al giorno nella pipeline'},
        {'icon':'↗','value':'4–5%','label':'quota indicativa dell’offerta mondiale'},
        {'icon':'●','value':'1.200 km','label':'lunghezza della rotta Est-Ovest'}
    ]
})
home_seed.write_text(json.dumps(seed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

runpy.run_path(str(ROOT/'tools/finalize_articles_20260906.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/generate_category_pages.py'),run_name='__main__')
for rel in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
    p=ROOT/rel; d=json.loads(p.read_text(encoding='utf-8')); d['version']=VERSION; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json'):
    p=ROOT/rel
    if p.exists():
        d=json.loads(p.read_text(encoding='utf-8'))
        if 'site_version' in d: d['site_version']=VERSION
        if 'version' in d: d['version']=str(VERSION)
        if 'currentVersion' in d: d['currentVersion']=VERSION
        d['last_update']='notizie-13-settembre-v344'; d['last_daily_question_date']='2026-09-13'
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ok','version':VERSION,'articles':[a['slug'] for a in ARTICLES]},ensure_ascii=False))
