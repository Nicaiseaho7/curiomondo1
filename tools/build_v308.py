#!/usr/bin/env python3
from pathlib import Path
from html import escape
from lxml import html, etree
import json

ROOT=Path(__file__).resolve().parents[1]
VERSION=308
DATE='2026-09-08'
DATE_LABEL='8 settembre 2026'
OLD='cosa-faremmo-se-il-tempo-tornasse-indietro-di-dieci-anni-sapendo-cio-che-sappiamo-ora'
SLUG='quale-parte-della-tua-vita-stai-vivendo-in-attesa-di-sentirti-finalmente-pronto'
QUESTION='Quale parte della tua vita stai vivendo in attesa di sentirti finalmente pronto?'
DECK='Una riflessione sulla differenza tra prepararsi davvero e usare la preparazione per rimandare ciò che conta.'
BOOK_TITLE='La soglia che continuiamo a preparare'
BOOK_DECK='Un eBook su attesa, paura e piccoli inizi: come capire quando essere prudenti e quando la prudenza è diventata rinvio.'
QURL=f'/domanda-del-giorno/{SLUG}/'
BURL=f'/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/'
OLD_Q=f'/domanda-del-giorno/{OLD}/'

QUESTION_PARAGRAPHS=[
"Ci sono inizi che rimandiamo perché mancano davvero informazioni, denaro o sicurezza. E poi ci sono attese più sottili: aspettiamo di sentirci pronti, come se la prontezza dovesse arrivare prima del primo passo. Immaginiamo che un giorno la paura si ritirerà, la mente sarà ordinata e la scelta diventerà evidente. Intanto continuiamo a prepararci alla vita che vorremmo vivere, senza entrarci.",
"Prepararsi è utile quando riduce un rischio concreto. Studiare prima di un esame, fare un piano economico o chiedere un parere competente può cambiare davvero l’esito. Il rinvio comincia quando ogni risposta genera una nuova condizione: ancora un corso, ancora una conferma, ancora un momento migliore. La preparazione non avvicina più all’azione; protegge dall’esperienza di essere principianti.",
"La parte difficile è che spesso non possiamo sentirci pronti per qualcosa che non abbiamo mai fatto. La sicurezza arriva dopo aver attraversato piccole prove, non prima. È come aspettare di avere equilibrio perfetto prima di salire su una bicicletta: proprio il movimento che temiamo è ciò che permette al corpo di imparare a restare in piedi.",
"Questo non significa lanciarsi senza misura. Un primo passo può essere piccolo, reversibile e rispettoso dei nostri limiti. Possiamo inviare una richiesta, fissare un colloquio, dedicare trenta minuti al progetto, raccontare a una persona fidata ciò che desideriamo. L’obiettivo non è dimostrare coraggio, ma raccogliere informazioni che soltanto l’azione può fornire.",
"Forse la domanda di oggi non chiede di cambiare tutta la vita. Chiede di individuare il punto in cui l’attesa ha smesso di proteggerci e ha iniziato a trattenerci. Se nessuna nuova preparazione modifica la decisione, potremmo non avere bisogno di sentirci pronti. Potremmo avere bisogno di cominciare abbastanza piccoli da poter imparare mentre procediamo.",
"Qual è il gesto minimo che potresti compiere oggi, senza prometterti di non avere paura?"
]

BOOK_PAGES=[
("Quando l’attesa sembra responsabilità",[
"Essere prudenti è una capacità. Ci permette di distinguere un desiderio da un impulso, valutare conseguenze e non consegnare decisioni importanti all’entusiasmo di un momento. Il problema nasce quando la prudenza perde un criterio di conclusione: continuiamo a raccogliere informazioni, ma non sappiamo più quale informazione sarebbe sufficiente per scegliere.",
"In quel punto l’attesa può apparire molto seria. Facciamo liste, leggiamo, confrontiamo e immaginiamo scenari. Tutta questa attività produce la sensazione di occuparci del problema, anche se nessuna azione ci espone a un risultato reale. È un movimento senza attraversamento.",
"Una domanda utile è: che cosa deve essere vero perché io faccia il primo passo? Se la risposta è concreta e verificabile, probabilmente stiamo preparando. Se cambia ogni volta che ci avviciniamo alla soglia, probabilmente stiamo rimandando."]),
("La prontezza arriva spesso dopo",[
"Molte capacità non possono essere completate in anticipo. Possiamo studiare come parlare in pubblico, ma la voce impara davanti a persone reali. Possiamo leggere di relazioni, ma i confini diventano chiari quando proviamo a esprimerli. Possiamo progettare un lavoro, ma soltanto il contatto con clienti, colleghi e difficoltà rivela ciò che manca.",
"La prontezza non è sempre uno stato interiore. A volte è la memoria di avere affrontato una situazione simile. Se aspettiamo quella memoria prima della prima esperienza, chiediamo al tempo di funzionare al contrario.",
"Per questo un inizio intelligente non elimina l’incertezza: la rende abbastanza piccola da essere osservata. Un esperimento limitato può insegnare più di settimane di anticipazioni, senza obbligarci a una scelta irreversibile."]),
("Il costo nascosto del rinvio",[
"Rimandare sembra gratuito perché non produce una perdita visibile nel momento in cui avviene. Ma occupa attenzione. Ogni progetto sospeso rimane aperto nella mente, chiede nuove valutazioni e diventa una misura silenziosa della distanza tra ciò che diciamo di volere e ciò che facciamo.",
"Esiste anche un costo di identità. Dopo molti rinvii possiamo iniziare a descriverci come persone incapaci di cominciare. Non è necessariamente vero: forse abbiamo costruito condizioni troppo grandi per autorizzare il primo gesto.",
"Ridurre la soglia cambia la domanda. Non più: sono pronto a trasformare tutto? Ma: sono pronto a raccogliere un’informazione reale entro questa settimana? La seconda domanda non promette un futuro perfetto; restituisce una parte di movimento."]),
("Un primo passo ben progettato",[
"Un passo utile ha quattro caratteristiche. È specifico: sappiamo quando è compiuto. È piccolo: non richiede una nuova personalità. È informativo: produce un dato che prima non avevamo. Ed è proporzionato: non espone a conseguenze enormi soltanto per dimostrare determinazione.",
"Se vogliamo cambiare lavoro, il primo passo può essere parlare con chi svolge già quel ruolo. Se vogliamo creare qualcosa, può essere una bozza mostrata a tre persone. Se serve una conversazione difficile, può essere scrivere i punti essenziali e scegliere un momento adatto.",
"La misura del passo non è quanto appare coraggioso agli altri. È quanto ci avvicina alla realtà senza tradire sicurezza, responsabilità e limiti personali."]),
("Sette giorni invece di un giorno perfetto",[
"Scegli una parte della vita che senti ferma. Scrivi che cosa stai aspettando e separa ciò che è indispensabile da ciò che desideri soltanto per non sentirti vulnerabile. Poi stabilisci un gesto da compiere entro sette giorni.",
"Alla fine della settimana non chiederti se sei diventato sicuro. Chiediti che cosa hai imparato: il desiderio è ancora vivo? Il rischio era quello immaginato? Serve altra preparazione specifica oppure un secondo passo?",
"Il presente raramente offre una sensazione definitiva di via libera. Offre finestre piccole, informazioni incomplete e la possibilità di correggere la direzione. Essere pronti può significare proprio questo: non sapere tutto, ma sapere qual è il prossimo gesto abbastanza onesto da compiere."])
]

EXTRA_EXISTING=[
[
"Un criterio di conclusione può essere una data, un importo, una competenza o il parere di una persona qualificata. Senza questo criterio, la preparazione si espande fino a occupare tutto lo spazio disponibile. Definirlo non obbliga ad agire: impedisce soltanto alla paura di spostare continuamente il traguardo.",
"Possiamo anche distinguere rischi reali e disagi emotivi. Perdere denaro necessario, compromettere la salute o assumere un impegno insostenibile sono rischi. Sentirsi inesperti, ricevere un rifiuto o mostrare una bozza imperfetta sono disagi. Entrambi meritano attenzione, ma non chiedono la stessa protezione.",
"Quando diciamo “non è il momento”, vale la pena completare la frase: quale evento renderebbe il momento adatto? Se non sappiamo rispondere, il calendario potrebbe essere soltanto un nome più elegante per la paura. Se invece la risposta è precisa, possiamo costruire un piano e verificare i progressi.",
"La responsabilità non consiste nell’attendere finché ogni esito è controllabile. Consiste nel raccogliere le informazioni proporzionate alla decisione, proteggere ciò che non possiamo permetterci di perdere e riconoscere il punto in cui altra analisi non cambia più la scelta."
],
[
"Anche chi appare sicuro spesso sta imparando in pubblico. Vediamo il risultato, non le prove intermedie, le correzioni e le richieste di aiuto. Confrontiamo così la nostra esitazione privata con la parte più composta del percorso altrui e concludiamo di essere gli unici non ancora pronti.",
"La competenza cresce attraverso cicli: tentativo, risposta, correzione. Saltare il tentativo interrompe il ciclo prima che possa produrre esperienza. Possiamo accumulare teoria, ma alcune domande restano invisibili finché non incontrano una situazione concreta.",
"Questo vale anche nelle relazioni. Nessuna preparazione garantisce che una conversazione delicata sarà accolta bene. Possiamo scegliere parole rispettose e un momento adatto, ma la risposta dell’altra persona resta fuori dal nostro controllo. Essere pronti significa tollerare questa parte di incertezza.",
"La prima esperienza non deve confermare un’identità. Una prova andata male non dimostra che non siamo portati; può mostrare che il formato, il momento o il livello di difficoltà erano sbagliati. Trattare l’inizio come un esperimento permette di imparare senza trasformare ogni esito in una sentenza."
],
[
"Il costo del rinvio cambia con il tempo. Una settimana può essere irrilevante; anni di attesa possono restringere possibilità, energia e fiducia. Non serve drammatizzare ogni scelta, ma è utile chiedersi se l’opzione che stiamo conservando resterà davvero disponibile alle stesse condizioni.",
"Alcune attese consumano anche le relazioni. Promesse indefinite come “prima o poi ne parleremo” o “quando sarò meno impegnato” chiedono agli altri di vivere dentro un calendario che non esiste. Dare una data o dire con onestà che non siamo disposti ad agire è spesso più rispettoso.",
"C’è poi il costo delle alternative escluse. Tenere aperto un progetto che non scegliamo può impedirci di investire in altro. Decidere di non procedere è diverso dal rimandare: chiude un ciclo, libera attenzione e ci permette di assumere la perdita senza continuarla ogni giorno.",
"Per misurare il rinvio possiamo osservare ciò che ripetiamo. Se da mesi formuliamo lo stesso desiderio con le stesse ragioni per non cominciare, non ci manca necessariamente una nuova soluzione. Potrebbe mancare l’accettazione che ogni strada comporta esposizione, rinuncia e una quota di imperfezione."
],
[
"La reversibilità è uno strumento potente. Prima di una scelta totale possiamo cercare una versione temporanea: un corso breve, una collaborazione limitata, una settimana di prova, un colloquio informativo. Non tutte le decisioni lo consentono, ma molte diventano meno astratte quando le riduciamo.",
"Un buon passo produce una risposta dal mondo. Scrivere ancora appunti può farci sentire ordinati; inviare una proposta ci dice se qualcuno la comprende. Pensare a un confine può chiarire le idee; esprimerlo ci mostra come cambia la relazione. L’informazione reale ha spesso un piccolo prezzo emotivo.",
"Serve anche un limite di tempo. Un’azione senza data rimane un’intenzione. La data deve essere abbastanza vicina da impedire nuove condizioni, ma abbastanza realistica da rispettare impegni e sicurezza. Se salta, non occorre punirsi: occorre capire quale ostacolo concreto non avevamo previsto.",
"Infine è utile decidere prima come valuteremo il risultato. Il successo del primo passo non è ottenere subito ciò che desideriamo. È aver raccolto dati, verificato un’ipotesi o scoperto il passaggio successivo. Questa misura protegge dalla pretesa che ogni inizio debba già sembrare una vittoria."
],
[
"Durante i sette giorni possiamo annotare il momento esatto in cui nasce l’impulso a rimandare. Quale frase compare? “Non so abbastanza”, “farò una brutta figura”, “ormai è tardi”. Scriverla rende visibile il meccanismo e permette di verificare se descrive un fatto oppure una previsione.",
"Poi possiamo cercare una prova contraria. Non una frase motivazionale, ma un dato: una volta in cui abbiamo imparato facendo, una persona disponibile ad aiutarci, una parte del compito che sappiamo già svolgere. Lo scopo non è eliminare il dubbio, ma impedirgli di presentarsi come certezza.",
"Alla fine della settimana possiamo scegliere fra tre esiti legittimi: continuare, modificare o fermare. Continuare significa che la prova ha confermato direzione e sostenibilità. Modificare significa che il desiderio resta, ma il formato va corretto. Fermare significa che abbiamo imparato abbastanza per dire un no consapevole.",
"Questa libertà rende l’esperimento più onesto. Se il primo passo è costruito come una promessa irrevocabile, la mente lo eviterà. Se può produrre anche una decisione di non proseguire, diventa uno strumento di conoscenza e non un esame sul nostro valore."
]
]
for (_,paras),extra in zip(BOOK_PAGES,EXTRA_EXISTING):
 paras.extend(extra)

BOOK_PAGES.extend([
("Le voci che chiedono perfezione",[
"A volte l’attesa non nasce soltanto da noi. Famiglia, scuola o lavoro possono averci insegnato che mostrare un tentativo incompleto espone al giudizio. Se l’errore è stato trattato come una colpa, prepararci all’infinito diventa un modo comprensibile per proteggerci dalla vergogna.",
"Riconoscere l’origine di questa voce non basta a spegnerla, ma permette di non confonderla con un’analisi oggettiva. Possiamo chiederci di chi è lo standard che stiamo cercando di soddisfare e se quella persona comprenderebbe davvero il contesto presente.",
"La perfezione promette immunità: se facciamo tutto bene, nessuno potrà rifiutarci. Ma molti rifiuti dipendono da preferenze, tempi e bisogni altrui. Prepararci meglio può migliorare una proposta; non può eliminare la libertà del mondo di rispondere diversamente.",
"Per cominciare può servire un pubblico più sicuro. Mostrare una bozza a qualcuno capace di essere preciso senza umiliare, provare in un ambiente limitato o dichiarare apertamente che siamo in fase di apprendimento riduce la pressione senza nascondere il lavoro.",
"Con il tempo impariamo che essere visibili prima della perfezione non distrugge la credibilità. Spesso la rafforza: permette correzioni anticipate, crea relazioni di fiducia e mostra la capacità più importante, quella di apprendere senza difendere ogni errore."
]),
("Quando aspettare è la scelta giusta",[
"Non ogni rinvio è evitamento. Se mancano condizioni di sicurezza, consenso, stabilità economica o informazioni sanitarie, attendere può essere la decisione più adulta. Il punto non è glorificare l’azione, ma rendere l’attesa intenzionale e verificabile.",
"Un’attesa sana ha un motivo dichiarato. Sappiamo che cosa stiamo proteggendo, quali dati mancano e quando rivaluteremo la situazione. Non ci raccontiamo che la scelta si risolverà da sola: manteniamo un appuntamento con la decisione.",
"Può anche contenere azioni preparatorie reali. Mettere da parte una somma, acquisire una certificazione, costruire una rete di sostegno o consultare un professionista modifica le condizioni future. La differenza si vede nei risultati accumulati, non nella quantità di pensieri dedicati.",
"Esistono poi decisioni che coinvolgono altre persone e non possono essere accelerate unilateralmente. Rispettare tempi, confini e responsabilità condivise non è debolezza. È riconoscere che il nostro desiderio non è l’unico elemento legittimo della situazione.",
"L’attesa giusta non ci lascia immobili: ci rende più capaci di scegliere quando la soglia arriva. E se le condizioni non maturano, ci permette di decidere consapevolmente se cambiare strada invece di restare sospesi senza fine."
]),
(None,[
"Le promesse enormi hanno fascino perché trasformano il cambiamento in una scena netta. Da domani farò tutto, non avrò più paura, non perderò tempo. Ma una promessa che richiede energia eccezionale si rompe facilmente e ogni rottura alimenta l’idea di non essere affidabili.",
"Una promessa piccola non cerca di impressionarci. Definisce un comportamento osservabile: venti minuti, una telefonata, un documento, una domanda. Può sembrare insufficiente rispetto alla distanza da percorrere, ma costruisce la prova più utile: siamo capaci di tornare.",
"La continuità non significa ripetere senza interruzioni. Significa progettare il ritorno dopo un’interruzione. Possiamo stabilire in anticipo che cosa faremo quando salteremo un giorno, riceveremo un no o perderemo slancio. Il piano di rientro vale più della fantasia di non inciampare.",
"Anche la celebrazione deve essere proporzionata. Non serve dichiarare che la vita è cambiata dopo il primo gesto. Basta riconoscere che abbiamo attraversato una soglia e possediamo un’informazione nuova. La sobrietà protegge il percorso dal bisogno di dimostrare subito risultati.",
"La prontezza può allora diventare una pratica, non un sentimento. Ogni volta che scegliamo un passo sostenibile, osserviamo la risposta e correggiamo, costruiamo fiducia basata su esperienza. Non ci promettiamo assenza di paura; ci promettiamo un modo per procedere anche quando la paura resta."
])
])

BOOK_PAGES[-1][1].extend([
"Per rendere la promessa concreta possiamo scriverla con un verbo e una misura. “Occuparmi del progetto” è troppo ampio; “aprire il documento martedì alle 18 e lavorare per venticinque minuti” crea un appuntamento riconoscibile. La precisione riduce la trattativa che facciamo con noi stessi nel momento di iniziare.",
"È utile preparare anche l’ambiente. Lasciare disponibili materiali, contatto, indirizzo o documento elimina piccoli ostacoli che la paura può usare come alibi. Non è un trucco per costringerci: è un modo per non chiedere alla forza di volontà di risolvere ogni dettaglio proprio quando l’energia è più bassa.",
"Possiamo poi raccontare la promessa a una persona affidabile, senza trasformarla in un giudice. Il suo ruolo non è controllare il risultato, ma ricordarci la domanda iniziale quando torniamo a inventare nuove condizioni. Una presenza gentile rende più difficile confondere una difficoltà reale con il riflesso automatico di ritirarsi.",
"Se il gesto continua a non avvenire, serve curiosità. Forse è ancora troppo grande, forse il desiderio non è nostro, forse esiste un rischio che non abbiamo nominato. Ridurre ancora, cambiare strada o chiedere sostegno sono risposte più intelligenti dell’insulto verso noi stessi.",
"Alla fine, sentirsi pronti non è il premio che riceviamo per aver pensato abbastanza. È spesso un effetto temporaneo dell’aver mantenuto alcune piccole promesse. La fiducia cresce quando vede prove ripetute che possiamo iniziare, fermarci, correggere e tornare senza trasformare ogni passaggio in un giudizio definitivo."
])

HEADER='''<header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>'''

def question_page():
 paras=''.join(f'<p>{escape(x)}</p>' for x in QUESTION_PARAGRAPHS[:-1])+f'<p class="q-pull cm-daily-question">{escape(QUESTION_PARAGRAPHS[-1])}</p>'
 return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(QUESTION)} | CurioMondo</title><meta name="description" content="Domanda del giorno dell’8 settembre 2026: {escape(DECK)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="https://curiomondo.it{QURL}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=308"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body class="cm-daily-page">{HEADER}<main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{DATE}">{DATE_LABEL}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{escape(QUESTION)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno">{paras}<a class="cm-daily-book-link" href="{BURL}"><span><small>Continua la riflessione</small><strong>Leggi l’eBook collegato</strong></span><span class="cm-daily-book-arrow" aria-hidden="true">→</span></a></article></main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''

def book_page():
 pages=[]
 for i,(heading,paras) in enumerate(BOOK_PAGES,1):
  attrs=' class="cm-book-page'+(' is-active' if i==1 else '')+'" data-book-page'+('' if i==1 else ' aria-hidden="true"')
  body=''.join(f'<p>{escape(x)}</p>' for x in paras)
  sub=f'<h2>{escape(heading)}</h2>' if heading else ''
  title_tag = f'<h1>{escape(BOOK_TITLE)}</h1>' if i == 1 else f'<h2 class="cm-book-title">{escape(BOOK_TITLE)}</h2>'
  pages.append(f'<section{attrs}><span class="cm-book-kicker">eBook CurioMondo · {DATE_LABEL}</span>{title_tag}{sub}{body}<span class="cm-book-page-number">{i} / {len(BOOK_PAGES)}</span></section>')
 return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(BOOK_TITLE)} | eBook CurioMondo</title><meta name="description" content="{escape(BOOK_DECK,quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="https://curiomondo.it{BURL}"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=308"><link rel="stylesheet" href="/assets/css/biblioteca-book-reader-v1.css?v=273"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body>{HEADER}<main class="cb-shell"><article class="cm-book-shell"><div class="cm-book-stage">{''.join(pages)}</div><nav class="cm-book-controls" aria-label="Navigazione eBook"><button data-book-prev type="button">← Indietro</button><button data-book-next type="button">Avanti →</button></nav><a class="cm-book-back" href="{QURL}">← Torna alla Domanda del giorno</a></article></main><noscript><style>.cm-book-page{{display:block!important;min-height:0;margin-bottom:20px}}</style></noscript><script defer src="/assets/js/biblioteca-book-reader-v1.js?v=273"></script><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''

fixed=[]
for p in (ROOT/'notizie').glob('*.html'):
 d=html.fromstring(p.read_text(errors='replace')); changed=False
 for grid in d.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," cm-insight-grid ")]'):
  for strong in grid.xpath('./div/strong'): strong.tag='b'; changed=True
  for span in grid.xpath('./div/span'): span.tag='small'; changed=True
 if changed:
  for link in d.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'): link.set('href','../assets/css/curiomondo-article-v211.css?v=308')
  p.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8'); fixed.append(p.name)

qp=ROOT/QURL.strip('/')/'index.html'; qp.parent.mkdir(parents=True,exist_ok=True); qp.write_text(question_page(),encoding='utf-8')
bp=ROOT/BURL.strip('/')/'index.html'; bp.parent.mkdir(parents=True,exist_ok=True); bp.write_text(book_page(),encoding='utf-8')

p=ROOT/'index.html'; d=html.fromstring(p.read_text(encoding='utf-8'))
for a in d.xpath(f'//a[@href="{OLD_Q}"]'): a.set('href',QURL)
for node in d.xpath('//time[contains(concat(" ",normalize-space(@class)," ")," cm-qday-date ")]'):
 node.set('datetime',DATE); strong=node.xpath('./strong'); span=node.xpath('./span')
 if strong: strong[0].text='08'
 if span: span[0].text='SET · 2026'
p.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

def add_card(path,url,title,deck,suffix=''):
 p=ROOT/path; d=html.fromstring(p.read_text(encoding='utf-8')); grid=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cb-subgrid ")]')[0]
 for a in grid.xpath(f'./a[@href="{url}"]'): grid.remove(a)
 action='Sfoglia' if suffix else 'Leggi'
 card=html.fragment_fromstring(f'<a class="cb-subcard" href="{url}"><span class="cb-kicker">{DATE_LABEL}{suffix}</span><h2>{escape(title)}</h2><p>{escape(deck)}</p><b>{action} →</b></a>')
 grid.insert(0,card); p.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')
add_card('domanda-del-giorno/index.html',QURL,QUESTION,DECK)
add_card('biblioteca/vita-relazioni/domande-per-conoscersi/index.html',BURL,BOOK_TITLE,BOOK_DECK,' · eBook')

sp=ROOT/'assets/data/search-index-v210.json'; data=json.loads(sp.read_text(encoding='utf-8')); data['items']=[x for x in data['items'] if x.get('url') not in {QURL,BURL}]
data['items'].insert(0,{'title':BOOK_TITLE,'excerpt':BOOK_DECK,'url':BURL,'section':'Biblioteca · Vita e relazioni'})
data['items'].insert(0,{'title':QUESTION,'excerpt':DECK,'url':QURL,'section':'Domanda del giorno'}); data['version']=VERSION; sp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('assets/data/home-feed-v210.json','assets/data/editorial-images-v210.json'):
 p=ROOT/rel; data=json.loads(p.read_text(encoding='utf-8')); data['version']=VERSION; p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

sm=ROOT/'sitemap.xml'; tree=etree.parse(str(sm)); ns='http://www.sitemaps.org/schemas/sitemap/0.9'; root=tree.getroot(); existing={x.text for x in root.findall(f'{{{ns}}}url/{{{ns}}}loc')}
for url in (f'https://curiomondo.it{QURL}',f'https://curiomondo.it{BURL}'):
 if url not in existing:
  node=etree.Element(f'{{{ns}}}url'); etree.SubElement(node,f'{{{ns}}}loc').text=url; etree.SubElement(node,f'{{{ns}}}lastmod').text=DATE; root.insert(1,node)
tree.write(str(sm),encoding='utf-8',xml_declaration=True,pretty_print=True)

mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; m['daily_state']['last_question_date']=DATE; m['daily_state']['last_question_slug']=SLUG; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ok','version':VERSION,'fixed_articles':fixed,'question':QURL,'ebook':BURL},ensure_ascii=False,indent=2))
