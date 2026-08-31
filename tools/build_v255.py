#!/usr/bin/env python3
"""Publish the 31 August wildfire story, daily question, ebook and two guides for CurioMondo v255."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re

from PIL import Image
from lxml import etree, html


ROOT = Path(__file__).resolve().parents[1]
VERSION = 255
DATE_LABEL = "2026-08-31"
DATE_HUMAN = "31 agosto 2026"
IMAGE_DIR = "/assets/images/editorial-v255"
GENERATED = ROOT.parent / "generated-v255/sicilia-incendi-31-agosto-2026-editorial.png"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

NEWS = {
    "slug": "sicilia-incendi-sciacca-ciminna-evacuati-intossicati-31-agosto-2026",
    "title": "Sicilia assediata dagli incendi: 500 evacuati a Sciacca, sei intossicati e un giovane gravemente ustionato",
    "excerpt": "Roghi in quasi tutte le province: residenti in fuga a Ciminna, evacuazioni a Makauda e fronti attivi anche in Puglia, Sardegna, Abruzzo e Campania.",
    "category": "Ultima ora · Italia / Ambiente / Incendi",
    "published": "2026-08-31T00:11:00+02:00",
    "updated": "2026-08-31T00:11:00+02:00",
    "image_key": "sicilia-incendi-emergenza-31-agosto-2026-ai-v255",
    "image_alt": "Illustrazione editoriale IA di un vasto incendio nelle campagne siciliane con mezzi antincendio su una strada sicura, senza persone in pericolo visibili",
    "sensitive": True,
    "prompt": "Use case: photorealistic-natural. Respectful ultra-realistic wide editorial illustration of a major rural wildfire in Sicily at night or dawn, broad fireline, smoke and distant fire engines on a safe road, tiny indistinct responders in safe positions, no victims, no injured people, no evacuees, no infant, no close-up distress, no text, no logos, no documentary claim.",
    "insights": [("500", "le persone evacuate a Makauda"), ("6", "gli intossicati, tra cui un neonato"), ("50+", "i lanci d’acqua sul fronte di Alberona")],
    "body": [
        "Una vasta emergenza incendi ha interessato la Sicilia tra il 30 e il 31 agosto, con roghi segnalati in quasi tutte le province. A Ciminna, nel Palermitano, alcuni residenti hanno lasciato le abitazioni minacciate dalle fiamme. Un uomo di 26 anni è rimasto gravemente ustionato mentre tentava di difendere la propria campagna: è ricoverato con prognosi riservata. Il sindaco ha chiesto alla Regione il riconoscimento dello stato di calamità dopo danni estesi a terreni, aziende e infrastrutture.",
        "La situazione più complessa per numero di persone coinvolte si è verificata a Makauda, nel territorio di Sciacca. Circa 500 ospiti di una struttura ricettiva sono stati allontanati e accompagnati sulla spiaggia mentre il fumo rendeva insicura l’area. Sei persone, compreso un neonato, sono state portate al pronto soccorso per intossicazione. Le autorità hanno chiuso temporaneamente un tratto della statale 115 e predisposto spazi di accoglienza per chi non poteva rientrare.",
        "Altri fronti hanno impegnato vigili del fuoco, Corpo forestale, Protezione civile e mezzi aerei tra Ciminna e Ventimiglia di Sicilia, dove risultano danneggiati impianti elettrici e telefonici, e nella zona di Castelmola sopra Taormina. Ad Acireale un incendio si è sviluppato vicino a un deposito di gas, imponendo particolare cautela. Il quadro resta mobile: un rogo dichiarato sotto controllo può riattivarsi se vento e vegetazione secca spingono le braci oltre le linee già bonificate.",
        "L’emergenza non è limitata all’isola. Incendi sono stati segnalati anche in Sardegna, Abruzzo e Campania. In Puglia è tornato a bruciare il bosco di Alberona, sui Monti Dauni: secondo il quadro riportato da ANSA e dalla stampa regionale, nella sola giornata di domenica sono stati effettuati almeno 50 lanci d’acqua con due Canadair e un elicottero. Il vento ha favorito la propagazione e il fumo ha reso più difficili le operazioni delle squadre a terra.",
        "Vento, caldo e siccità possono creare condizioni favorevoli alla rapida diffusione del fuoco, ma non dimostrano da soli quale sia stato l’innesco di ogni incendio. Le cause possono essere accidentali, dolose o legate a comportamenti negligenti e devono essere accertate dalle indagini. Anche quando si parla di emergenza climatica è quindi utile distinguere due piani: il clima può aumentare la frequenza delle giornate ad alto pericolo e la severità della vegetazione secca; l’origine concreta di un singolo rogo richiede prove specifiche.",
        "La richiesta comunale di stato di calamità non coincide automaticamente con la dichiarazione nazionale dello stato di emergenza. La prima serve a documentare danni e necessità del territorio e ad avviare le procedure regionali; la seconda è una decisione del Consiglio dei ministri che può attivare poteri e risorse straordinari di Protezione civile. In questa fase la priorità resta proteggere le persone, mettere in sicurezza le strutture esposte e completare la bonifica dei perimetri già attraversati dalle fiamme.",
        "I prossimi aggiornamenti utili riguarderanno le condizioni del giovane ustionato e delle persone intossicate, il rientro degli evacuati, la stima dei danni e l’esito degli accertamenti sugli inneschi. CurioMondo mantiene un’unica pagina nazionale per evitare una sequenza di articoli duplicati sui singoli focolai. I numeri operativi sono attribuiti alle fonti disponibili e potranno essere rivisti quando Protezione civile, comuni e vigili del fuoco pubblicheranno bilanci consolidati.",
    ],
    "related": [
        ("/notizie/europa-caldo-incendi-serbia-italia-27-citta-allerta-rossa.html", "Ambiente · Europa", "Caldo estremo e incendi in Europa: che cosa aumenta il rischio"),
        ("/notizie/canada-incendio-bald-range-columbia-britannica-20000-evacuati-8-agosto-2026.html", "Mondo · Ambiente", "Canada, un grande incendio costringe migliaia di persone a evacuare"),
        ("/notizie/perche-incendi-torbiere-difficili-spegnere.html", "Approfondimento · Incendi", "Perché alcuni incendi continuano a bruciare sotto terra"),
    ],
    "sources": [
        ("https://www.ansa.it/sito/notizie/cronaca/2026/08/30/ancora-incendi-nellarea-di-taormina-abitazioni-minacciate_a95c7dba-0368-4f41-89d6-73880b93193d.html", "ANSA — quadro nazionale dei roghi e interventi in Sicilia e Puglia"),
        ("https://www.ansa.it/sicilia/notizie/2026/08/30/sindaco-ciminna-scarso-aiuto-su-incendi-chiediamo-stato-demergenza_2787efcc-65e9-47b8-ba21-5c38eb26d4b1.html", "ANSA Sicilia — Ciminna, giovane ustionato e richiesta del Comune"),
        ("https://www.lasicilia.it/news/cronaca/3069258/sciacca-nella-morsa-delle-fiamme-fumo-tossico-a-makauda-sei-in-ospedale-pure-un-neonato.html", "La Sicilia — evacuazione a Makauda e persone intossicate"),
        ("https://qds.it/incendio-makauda-sciacca-persone-neonato-intossicati/", "Quotidiano di Sicilia — soccorsi, viabilità e accoglienza a Sciacca"),
        ("https://foggia.corriere.it/notizie/cronaca/26_agosto_30/brucia-ancora-il-bosco-di-alberona-in-puglia-almeno-50-i-lanci-di-acqua-fatti-nella-giornata-di-domenica-fc3ddeb2-ad56-48d4-a978-fb7e7a801xlk_amp.shtml", "Corriere del Mezzogiorno — mezzi e lanci d’acqua ad Alberona"),
    ],
}

QUESTION_SLUG = "quale-ferita-passata-sta-ancora-parlando-quando-diciamo-sono-fatto-cosi"
QUESTION_TITLE = "Quale ferita passata sta ancora parlando quando diciamo «sono fatto/a così»?"
QUESTION_EXCERPT = "Una riflessione sulle etichette con cui proteggiamo vecchie difese e sulla possibilità di cambiare senza negare la nostra storia."
BOOK_TITLE = "Le frasi con cui il passato continua a parlare"

QUESTION_PARAGRAPHS = [
    "La frase «sono fatto/a così» può essere una descrizione onesta: riconoscere il proprio temperamento, i limiti o un bisogno stabile evita di recitare una versione più comoda per gli altri. Ma a volte quella frase non racconta chi siamo. Custodisce il modo in cui abbiamo imparato a non essere feriti di nuovo. La distanza può essere nata dopo un abbandono, il controllo dopo un periodo di caos, l’ironia dopo essere stati derisi, l’autosufficienza dopo aver chiesto aiuto senza riceverlo.",
    "Una difesa non è una colpa. In un certo momento può averci permesso di restare in piedi. Il problema comincia quando la strategia continua a decidere anche in situazioni nuove: non mostriamo bisogno a persone affidabili, interpretiamo ogni silenzio come rifiuto, trasformiamo ogni critica in attacco, rinunciamo prima che qualcuno possa scegliere di non sceglierci. Ciò che un tempo proteggeva diventa allora una regola che restringe la vita.",
    "Capire l’origine di un comportamento non significa giustificarne ogni effetto. Una ferita può spiegare perché reagiamo con durezza, ma non rende innocuo ciò che facciamo agli altri. La responsabilità adulta tiene insieme due verità: quella risposta ha avuto una funzione; oggi posso osservare il prezzo che fa pagare a me e alle mie relazioni. Non devo disprezzare la parte che mi ha protetto, né lasciarle per sempre il volante.",
    "Per riconoscere la voce del passato, ascolta quando la frase compare. Arriva prima di chiedere scusa? Quando qualcuno desidera maggiore vicinanza? Quando una scelta ti esporrebbe al rischio di fallire? Prova a sostituirla con una formulazione più precisa: «Quando temo di essere rifiutato, tendo a chiudermi» oppure «Quando non controllo tutto, mi sento in pericolo». Una descrizione situata apre possibilità che un’etichetta definitiva cancella.",
    "Cambiare non obbliga a rinnegare la propria storia. Significa aggiornare una protezione con le informazioni del presente: distinguere chi è affidabile da chi non lo è, chiedere tempo senza sparire, mettere un limite senza punire, tollerare una piccola dose di incertezza. Il gesto nuovo può sembrare innaturale soltanto perché non è ancora familiare.",
]

BOOK_PAGES = [
    (None, [
        "«Sono fatto/a così» sembra una frase semplice, quasi una firma. Può nominare un tratto reale, ma può anche chiudere una porta proprio quando qualcosa dentro di noi chiede di essere compreso. Dietro l’impazienza può vivere la paura di non essere ascoltati; dietro l’indipendenza assoluta, il ricordo di una richiesta d’aiuto rimasta senza risposta; dietro l’ironia, la scelta antica di colpire prima di essere esposti.",
        "Questo eBook non invita a cercare una ferita nascosta dietro ogni caratteristica. Le persone hanno temperamenti, preferenze e confini che non devono essere corretti. Propone invece una distinzione: un tratto ci lascia libertà di adattarci, mentre una difesa rigida si attiva come se il pericolo fosse sempre lo stesso. La domanda non è «che cosa c’è di sbagliato in me?», ma «questa risposta appartiene ancora alla situazione presente?». ",
        "Guardare il passato con rispetto non significa consegnargli il futuro. Possiamo riconoscere che una strategia ci ha protetto, osservare il costo che produce oggi e scegliere una forma più precisa di sicurezza. Il cambiamento più profondo non umilia la parte che ha resistito: le mostra che ora esistono altre possibilità.",
        "La precisione è già una forma di cura. Dire «mi chiudo quando temo di non contare» è più vulnerabile e più utile di «sono fatto così», perché distingue una reazione dalla persona intera. La frase precisa non obbliga a cambiare subito, ma rende visibile il punto in cui il presente incontra una previsione antica. Da quel punto può nascere un esperimento, una richiesta o un confine diverso.",
    ]),
    ("Quando un’etichetta diventa una stanza chiusa", [
        "Le etichette personali riducono la complessità. Dire «sono timido», «sono diffidente» o «sono quello che risolve tutto» permette di prevedere il nostro comportamento e di farlo prevedere agli altri. Questa stabilità può essere rassicurante. Diventa però una stanza chiusa quando ogni eccezione viene vissuta come tradimento: il timido non può prendere parola, il forte non può chiedere aiuto, chi non si fida non può concedere una prova.",
        "Una descrizione flessibile include contesto e movimento. «In gruppi nuovi ho bisogno di tempo» è diversa da «non so stare con le persone». «Dopo una delusione controllo molto» contiene più verità di «sono geloso». La prima formulazione indica quando la risposta appare e lascia immaginare condizioni diverse; la seconda la trasforma in natura immutabile.",
        "Osserva il linguaggio assoluto: sempre, mai, tutti, nessuno. Non è una prova automatica di una ferita, ma segnala che l’esperienza viene organizzata come una legge. Chiedere «in quali situazioni questo è più vero?» restituisce sfumature. Spesso scopriamo che sappiamo già comportarci diversamente in contesti sicuri: quella eccezione è una capacità esistente, non una contraddizione da cancellare.",
    ]),
    (None, [
        "Una difesa nasce quando mente e corpo imparano ad anticipare un dolore. Se l’imprevedibilità è stata frequente, controllare tutto può offrire sollievo. Se l’affetto era condizionato alla prestazione, eccellere può diventare il prezzo immaginato dell’appartenenza. Se mostrare emozioni suscitava scherno, la neutralità può sembrare l’unico modo per conservare dignità.",
        "Queste risposte non sono decisioni prese una volta con parole chiare. Si costruiscono attraverso ripetizioni, segnali corporei e conclusioni implicite. «Non dipendere», «non sbagliare», «non disturbare», «non farti vedere» diventano regole senza essere mai state pronunciate. Per questo non basta ordinarsi di smettere: la protezione deve incontrare esperienze nuove, abbastanza sicure e ripetute da poter aggiornare la previsione.",
        "Riconoscere la funzione originaria evita due errori. Il primo è vergognarsi di una strategia che aveva un senso. Il secondo è idealizzarla perché una volta è stata utile. Possiamo ringraziare simbolicamente la parte che ci ha difeso e, nello stesso momento, dirle che oggi non tutte le stanze sono quella stanza, non tutte le persone sono quella persona, non ogni attesa annuncia un abbandono.",
    ]),
    ("Ferita, temperamento o abitudine?", [
        "Non ogni comportamento difficile nasce da un trauma e non ogni preferenza introversa è evitamento. Il temperamento indica tendenze relativamente stabili: intensità emotiva, bisogno di stimoli, velocità con cui ci apriamo, energia sociale. Un’abitudine è una risposta appresa e ripetuta perché comoda o automatica. Una difesa legata a una ferita tende invece ad avere un tono di urgenza: sembra che non esista alternativa senza perdere sicurezza, valore o appartenenza.",
        "Tre domande aiutano a distinguere. La risposta è proporzionata alla situazione? Posso scegliere diversamente quando mi sento al sicuro? Che cosa temo accadrebbe se non la mettessi in atto? Se il rifiuto di un invito produce semplice preferenza per la solitudine, può essere temperamento. Se produce panico all’idea di essere osservati e giudicati, merita un ascolto diverso. La distinzione non serve a diagnosticarsi, ma a scegliere con più precisione.",
        "Anche il costo conta. Un tratto può richiedere adattamenti senza distruggere relazioni o possibilità. Una difesa rigida tende a ripetere conseguenze indesiderate: vicinanze interrotte, conflitti identici, occasioni abbandonate, stanchezza da controllo. Quando il prezzo cresce ma la risposta sembra ancora obbligatoria, la frase «sono fatto/a così» sta forse proteggendo il meccanismo dall’esame.",
    ]),
    (None, [
        "Il corpo spesso parla prima dell’etichetta. Una richiesta innocua può irrigidire il petto; un messaggio senza risposta può accendere lo stomaco; un’osservazione critica può produrre calore, fretta o bisogno di fuggire. Questi segnali non dimostrano che il pericolo sia reale, ma mostrano che il sistema di allarme ha riconosciuto qualcosa di familiare.",
        "Prima di interpretare, prova a registrare la sequenza: evento, sensazione fisica, pensiero, impulso, azione. «Ha risposto dopo tre ore; ho sentito vuoto; ho pensato che non gli importasse; volevo cancellare la conversazione; ho inviato un messaggio duro». Separare i passaggi rallenta la fusione tra sensazione e fatto. Il vuoto è reale; l’interpretazione può essere verificata.",
        "La regolazione non consiste nel convincersi che va tutto bene. Può significare respirare più lentamente, camminare, rimandare una risposta di venti minuti, parlare con qualcuno affidabile o nominare ciò che accade: «Mi sto attivando e ho bisogno di capire». Quando il corpo scende di intensità, la mente recupera alternative. La sicurezza non viene imposta; viene costruita abbastanza da permettere una scelta.",
    ]),
    ("Le frasi protettive più comuni", [
        "«Non ho bisogno di nessuno» può proteggere dalla dipendenza vissuta come umiliazione. «Se non lo faccio io, nessuno lo farà bene» può difendere dalla paura del caos. «Io dico sempre quello che penso» può evitare la vulnerabilità necessaria per scegliere come dire una verità. «Le persone prima o poi deludono» può trasformare una perdita in una previsione universale, così da non essere più colti di sorpresa.",
        "La stessa frase può avere significati diversi. Un confine netto può essere cura di sé oppure punizione; l’autonomia può essere competenza oppure isolamento; l’umorismo può creare contatto oppure impedire ogni discorso serio. Non giudicare la forma soltanto dall’esterno. Chiedi che funzione svolge, quale emozione evita e quale conseguenza ripete.",
        "Un piccolo dizionario personale può aiutare. Scrivi la frase automatica, poi traducila in paura e bisogno: «Sono freddo» diventa «Temo che mostrarmi permetta agli altri di ferirmi; ho bisogno di gradualità e reciprocità». La traduzione non assolve comportamenti dannosi, ma rende possibile una richiesta concreta. Le etichette chiudono; paure e bisogni possono essere negoziati.",
    ]),
    (None, [
        "Capire non significa giustificare. Chi è stato ferito può ferire, ma la propria storia non annulla l’impatto sugli altri. Una persona può aver imparato a urlare per non essere ignorata e, allo stesso tempo, avere la responsabilità di non intimidire chi le sta accanto. Tenere insieme origine e conseguenza evita sia la condanna totale sia l’alibi permanente.",
        "La responsabilità comincia con una descrizione osservabile: che cosa ho fatto, che effetto ha avuto, che cosa posso riparare? «Mi sono chiuso per paura» aggiunge contesto; non sostituisce «ti ho lasciato senza risposta per giorni». Le scuse diventano credibili quando non chiedono all’altro di minimizzare il danno e quando sono accompagnate da un cambiamento verificabile.",
        "A volte l’altra persona non sarà pronta a fidarsi, anche se abbiamo compreso molto. La sua prudenza non rende inutile il lavoro. Le difese si sono formate nel tempo e il loro superamento diventa visibile nello stesso modo: attraverso ripetizioni diverse. Restare presenti, comunicare un limite senza sparire, chiedere una pausa senza minacciare la relazione sono prove piccole ma concrete.",
    ]),
    ("Il prezzo nascosto della protezione", [
        "Ogni protezione offre un vantaggio immediato e presenta un conto più tardi. Evitare un confronto riduce l’ansia oggi, ma lascia crescere risentimento e distanza. Controllare il partner attenua per poco l’incertezza, ma indebolisce fiducia e libertà. Lavorare senza fermarsi protegge dal senso di inutilità, ma consuma salute e relazioni. Vedere entrambi i lati rompe l’idea che la difesa sia semplicemente irrazionale.",
        "Disegna due colonne: «che cosa mi dà» e «che cosa mi costa». Sii specifico. Non scrivere soltanto «sicurezza»; indica «non rischio di sentirmi rifiutato questa sera». Non scrivere soltanto «solitudine»; indica «non racconto a nessuno quando sono in difficoltà». La precisione permette di cercare un’alternativa che conservi parte della protezione senza pagare tutto il prezzo.",
        "L’obiettivo non è diventare improvvisamente aperti, fiduciosi o spontanei. È ampliare la scelta. Se prima esistevano soltanto attacco o fuga, introdurre una pausa è già una terza via. Se chiedere aiuto a tutti sembra impossibile, scegliere una persona e una richiesta limitata è un esperimento. La libertà cresce per gradazioni, non attraverso una prova eroica.",
    ]),
    (None, [
        "Le relazioni sicure non cancellano automaticamente una ferita, ma possono offrire informazioni nuove. Coerenza, rispetto dei confini, capacità di riparare e curiosità reciproca permettono al sistema di allarme di imparare che non ogni vicinanza è invasione e non ogni disaccordo conduce all’abbandono. Questo apprendimento richiede tempo e non può essere estorto con la frase «devi fidarti». ",
        "Anche noi possiamo rendere più leggibile il processo. Invece di sparire, dire «mi sono chiuso e ho bisogno di una sera, domani torno sul tema». Invece di testare l’amore con richieste impossibili, formulare ciò che rassicura. Invece di aspettare che l’altro indovini, nominare il segnale che ha attivato una paura. La vulnerabilità non è esposizione senza limiti; è comunicazione proporzionata e responsabile.",
        "Una relazione non deve diventare terapia permanente. Chi ci vuole bene può accompagnare, ma non ha il compito di assorbire ogni reazione né di rinunciare ai propri confini. Se il dolore è intenso, ricorrente o legato a esperienze traumatiche, un professionista qualificato può offrire uno spazio strutturato. Chiedere aiuto non dichiara debolezza: riconosce la complessità del lavoro.",
        "La sicurezza relazionale si misura anche nella riparazione. Non richiede assenza di errori, ma possibilità di nominare ciò che è accaduto senza minacce, silenzi punitivi o rovesciamento della colpa. Quando un conflitto può essere attraversato e concluso con informazioni nuove, il passato perde una parte della sua pretesa di prevedere sempre lo stesso finale.",
    ]),
    ("Un esperimento di sette giorni", [
        "Per sette giorni annota un momento in cui hai pensato o detto «sono fatto/a così». Scrivi il contesto, la frase precisa, la sensazione fisica e ciò che temevi potesse accadere. Poi completa: «Questa risposta prova a proteggermi da…». Non cercare una grande origine ogni sera. Anche una paura semplice — sembrare incompetente, deludere, essere escluso — può rendere il comportamento più comprensibile.",
        "Aggiungi una domanda sul presente: «Quale prova ho che oggi il pericolo sia identico?». Potresti scoprire segnali che confermano prudenza oppure differenze importanti. Infine scegli un gesto più flessibile del cinque per cento: fare una domanda invece di accusare, aspettare prima di cancellare, dire no senza lunga giustificazione, chiedere una scadenza invece di promettere subito.",
        "Alla fine della settimana cerca le ripetizioni, non il voto. Quale situazione attiva più spesso la difesa? Quale bisogno rimane senza parole? In quali occasioni sei già riuscito a rispondere diversamente? Queste eccezioni indicano risorse. Il diario non serve a dimostrare che il passato comanda tutto; serve a riconoscere i punti in cui puoi aggiornare il copione.",
    ]),
    (None, [
        "Cambiare una difesa può provocare lutto. Quella risposta era parte dell’immagine con cui ci siamo riconosciuti e forse del ruolo che gli altri si aspettano: quello forte, disponibile, razionale, divertente, irraggiungibile. Quando smettiamo di interpretarlo, qualcuno può sentirsi disorientato o opporsi perché beneficiava della nostra vecchia posizione.",
        "Il disagio iniziale non prova che il cambiamento sia falso. Un limite nuovo può sembrare aggressivo a chi era abituato alla nostra disponibilità totale; chiedere aiuto può sembrare debole a chi ci ha sempre affidato tutto. Valuta il gesto attraverso i valori e le conseguenze, non soltanto attraverso la familiarità. Autentico non significa automatico: spesso ciò che è più nostro deve ancora essere allenato.",
        "Conserva una continuità gentile. Puoi essere affidabile senza essere sempre reperibile, indipendente senza isolarti, prudente senza interrogare ogni affetto, sensibile senza trasformare ogni disagio in colpa altrui. Il cambiamento non cancella i tratti; li libera dall’obbligo di proteggere continuamente una scena passata.",
    ]),
    ("Una frase nuova da portare con sé", [
        "La domanda iniziale non chiede di trovare una causa unica. La vita lascia molte tracce e nessuna spiegazione deve diventare una nuova etichetta. Chiede di ascoltare chi parla quando diciamo «sono fatto/a così»: una preferenza presente, un valore scelto, una paura antica, la voce di qualcuno che ci ha definiti o un’abitudine mai riesaminata.",
        "Possiamo sostituire la sentenza con una frase aperta: «Ho imparato a reagire così quando mi sento in pericolo; oggi voglio capire se mi serve ancora». Contiene storia e libertà. Non promette un cambiamento immediato, ma impedisce al passato di presentarsi come natura. Permette di cercare sicurezza senza ripetere automaticamente lo stesso prezzo.",
        "Porta con te tre criteri: proporzione, scelta, conseguenza. La risposta è proporzionata al presente? Posso scegliere almeno una piccola alternativa? Quale conseguenza produce per me e per gli altri? Se le risposte mostrano rigidità e costo, non sei davanti a una condanna. Sei davanti a un punto di lavoro.",
        "La ferita non è tutta la tua identità. È una parte della storia che può ancora parlare, talvolta a voce alta. Ascoltarla non significa obbedirle. Significa offrirle parole, confini e relazioni sufficientemente sicure perché non debba più usare ogni volta lo stesso allarme per essere presa sul serio.",
        "Non tutte le storie possono essere ricostruite con certezza e non serve ricordare ogni dettaglio per iniziare. Puoi lavorare sul circuito osservabile di oggi: che cosa lo attiva, che cosa temi, quale bisogno rimane nascosto e quale scelta riduce il danno. Anche senza una spiegazione perfetta, una risposta più libera può diventare esperienza. Ripetuta, quella esperienza offre al corpo e alla mente una nuova memoria del possibile.",
    ]),
]

GUIDES = [
    {
        "slug": "come-recuperare-password-gmail-facebook-instagram-wifi",
        "title": "Come recuperare password di Gmail, Facebook, Instagram e Wi‑Fi in sicurezza",
        "excerpt": "Procedure ufficiali, account compromessi, codici di verifica e password Wi‑Fi: che cosa fare senza affidarsi a siti o persone che promettono scorciatoie.",
        "topic": "Come recuperare password (Gmail, Facebook, Instagram, Wi-Fi)",
        "body": """
<p><strong>Recuperare una password non significa quasi mai vedere quella vecchia in chiaro. Per Gmail, Facebook e Instagram la procedura corretta è verificare la propria identità e impostarne una nuova. Per il Wi‑Fi, invece, la chiave può essere già salvata su un dispositivo autorizzato o stampata sul router.</strong></p>
<div class="box"><strong>Regola di sicurezza:</strong> usa soltanto l’app ufficiale o digita direttamente l’indirizzo del servizio. Nessuna assistenza seria chiede password, codici ricevuti via SMS, codici dell’autenticazione a due fattori o denaro per “sbloccare” un account.</div>
<h2>Prima di iniziare: identifica il vero problema</h2>
<p>Chiediti se hai dimenticato la password, se non possiedi più l’email o il numero associato, oppure se sospetti un furto dell’account. Nel primo caso basta spesso il normale reset. Nel secondo servono le opzioni di recupero già configurate o una verifica aggiuntiva. Nel terzo devi proteggere anche email, dispositivo e sessioni aperte, perché cambiare una sola password potrebbe non bastare.</p>
<p>Usa un dispositivo e una rete da cui accedevi abitualmente, se sono sicuri. I servizi possono riconoscere elementi come browser, località approssimativa e precedenti accessi. Inserisci le informazioni più recenti che ricordi e non fare decine di tentativi casuali: risposte incoerenti possono rallentare la verifica.</p>
<h2>Gmail e Account Google</h2>
<p>Apri la pagina ufficiale di recupero dell’Account Google, inserisci l’indirizzo Gmail e segui le domande. Google può inviare una conferma a un telefono già collegato, un codice all’email di recupero o chiedere una password precedente. Se riesci ancora ad accedere da un dispositivo, vai in Gestisci il tuo Account Google, Sicurezza, Password. Dopo il cambio controlla dispositivi, attività recente, metodi di recupero e verifica in due passaggi.</p>
<p>Se non hai più il numero o l’indirizzo secondario, scegli un’altra modalità quando viene proposta. Google raccomanda di rispondere al maggior numero possibile di domande e di usare un dispositivo familiare. Un account eliminato di recente può talvolta essere recuperato dalla procedura dedicata, ma non esiste una garanzia oltre la finestra prevista. Google non offre servizi telefonici a pagamento che “ricostruiscono” password dimenticate.</p>
<h2>Facebook e Instagram</h2>
<p>Su Facebook seleziona “Password dimenticata?” dalla schermata di accesso e cerca l’account con email, numero o nome. Se sospetti una compromissione, usa la procedura ufficiale per account violati: da un dispositivo già usato può aiutare a riconoscere il profilo. Dopo il recupero disconnetti le sessioni sconosciute, verifica email e telefono, cambia anche la password dell’email associata se potrebbe essere stata esposta.</p>
<p>Su Instagram tocca “Password dimenticata?” o “Ricevi assistenza per l’accesso”, inserisci nome utente, email o telefono e richiedi il link. Se non possiedi più quei recapiti, l’app può proporre una verifica dell’identità. Non pagare presunti hacker o profili di assistenza nei messaggi diretti: possono rubare altri dati o chiedere codici che permettono loro di completare l’accesso al posto tuo.</p>
<h2>Password Wi‑Fi: router e dispositivi autorizzati</h2>
<p>Controlla prima l’etichetta del router: la password predefinita può essere indicata come Wi‑Fi Key, WPA Key o Password. Se è stata cambiata, su Android e iPhone recenti puoi condividere la rete o mostrare un codice QR dopo lo sblocco del dispositivo; su Windows e macOS puoi consultare la chiave di una rete salvata tramite le impostazioni o il portachiavi, purché tu sia autorizzato.</p>
<p>In alternativa entra nel pannello del router digitando l’indirizzo indicato dal produttore e usando le credenziali amministrative. La password di amministrazione non è necessariamente la stessa del Wi‑Fi. Se non la ricordi, consulta il manuale dell’operatore. Il ripristino fisico del router cancella spesso configurazione, nome rete e impostazioni telefoniche: usalo solo come ultima risorsa e dopo aver verificato come riconfigurare la linea.</p>
<h2>Dopo il recupero: chiudi davvero l’incidente</h2>
<p>Crea una password lunga e unica, preferibilmente con un gestore di password. Attiva l’autenticazione a due fattori e conserva i codici di backup in un luogo separato dal telefono. Rimuovi metodi di recupero che non controlli più, revoca app sconosciute e verifica eventuali regole di inoltro dell’email. Se la stessa password era usata altrove, cambiala anche su quei servizi.</p>
<p>Diffida dei messaggi che creano urgenza. Prima di aprire un link, entra nel servizio dall’app o dal sito digitato a mano e controlla le notifiche interne. Un codice di verifica è come una chiave temporanea: non va comunicato nemmeno a chi dice di lavorare per Google, Meta, il gestore telefonico o il produttore del router.</p>
""",
        "sources": [
            ("https://support.google.com/accounts/answer/41078?hl=it", "Google — cambiare o reimpostare la password"),
            ("https://support.google.com/accounts/answer/183723?hl=it", "Google — configurare le opzioni di recupero"),
            ("https://www.facebook.com/help/213395615347144/", "Meta — recuperare o modificare la password di Facebook"),
            ("https://www.facebook.com/help/instagram/409847499070242?locale=it_IT", "Meta — recuperare la password di Instagram"),
        ],
    },
    {
        "slug": "come-installare-app-android-iphone",
        "title": "Come installare app su Android e iPhone senza rischi",
        "excerpt": "Play Store, App Store, permessi, aggiornamenti e installazioni alternative: una guida per riconoscere l’app giusta e risolvere gli errori più comuni.",
        "topic": "Come installare app (Android/iOS)",
        "body": """
<p><strong>Il modo più sicuro per installare un’app è partire dallo store ufficiale del telefono, controllare sviluppatore e permessi e mantenere sistema e applicazioni aggiornati. Il nome e l’icona da soli non bastano: copie e app ingannevoli possono assomigliare molto all’originale.</strong></p>
<div class="box"><strong>Controllo rapido:</strong> verifica nome dello sviluppatore, numero e qualità delle recensioni, data degli aggiornamenti, informativa privacy e permessi richiesti. Un’app torcia non dovrebbe aver bisogno di contatti e microfono.</div>
<h2>Installare un’app su Android</h2>
<p>Apri Google Play Store, cerca l’app e apri la scheda completa. Controlla che lo sviluppatore corrisponda al servizio ufficiale, poi tocca Installa. Il telefono scarica il pacchetto e aggiunge l’icona. Se possiedi più dispositivi collegati allo stesso Account Google, Play può permettere di scegliere su quale installare. Alcune app non sono compatibili con ogni versione di Android, Paese o modello.</p>
<p>Prima del primo utilizzo Android può chiedere permessi per fotocamera, posizione, contatti o notifiche. Concedi soltanto ciò che serve alla funzione che stai usando; molti permessi possono essere autorizzati solo durante l’uso. In Impostazioni, App, scegli l’app per rivedere autorizzazioni, consumo batteria, dati mobili e spazio occupato.</p>
<h2>Installare un’app su iPhone o iPad</h2>
<p>Apri App Store, cerca l’app, controlla sviluppatore e informazioni, quindi tocca Ottieni o il prezzo. Conferma con Face ID, Touch ID o password dell’Account Apple. Se compare l’icona della nuvola, l’app era già stata scaricata con quell’account. Gli acquisti e gli abbonamenti non sono la stessa cosa: prima della conferma controlla se il prezzo è una tantum o ricorrente.</p>
<p>Al primo avvio iOS chiede accesso a funzioni sensibili. Puoi scegliere opzioni limitate, come fotografie selezionate o posizione approssimativa. In Impostazioni, Privacy e sicurezza puoi rivedere i permessi; nella pagina dell’app trovi notifiche, dati mobili e altre preferenze. Negare un permesso può disattivare una funzione, ma puoi concederlo in seguito.</p>
<h2>Come riconoscere l’app ufficiale</h2>
<p>Arriva alla scheda dallo store, non da un banner che imita un avviso del telefono. Confronta lo sviluppatore con il sito ufficiale del servizio e usa il collegamento pubblicato lì quando hai dubbi. Leggi le recensioni recenti senza fermarti alla media: un improvviso cambio di funzione o sviluppatore può modificare il rischio. Controlla anche dimensione, età minima, acquisti in-app e modalità di trattamento dei dati.</p>
<p>Evita versioni “mod”, premium gratuite e store sconosciuti. Possono includere malware, pubblicità invasiva o furto di credenziali e spesso violano i termini del servizio. Nessuna promessa di funzioni sbloccate vale l’accesso a foto, messaggi, conti o codici di autenticazione.</p>
<h2>Se l’installazione non parte</h2>
<p>Controlla connessione, spazio libero, data e ora automatiche e aggiornamenti del sistema. Riavvia il dispositivo e riprova dallo store. Su Android verifica che Play Store e Google Play Services siano aggiornati; cancellare la cache dello store può risolvere un download bloccato senza rimuovere le app. Su iPhone Apple consiglia di controllare il metodo di pagamento anche per alcune app gratuite e di tenere premuta l’icona per dare priorità al download.</p>
<p>Se compare “non compatibile”, non forzare l’installazione da un sito casuale. L’app può richiedere una versione più recente del sistema, una funzione hardware o una distribuzione nel tuo Paese. Cerca una versione ufficiale web o contatta lo sviluppatore. Per le app già acquistate, usa la sezione degli acquisti dello stesso account per riscaricarle.</p>
<h2>Installazioni fuori dallo store: quando e con quali cautele</h2>
<p>Android permette file APK e store alternativi, ma l’opzione “installa app sconosciute” riduce una protezione importante. Usala soltanto se conosci la fonte, verifica firma e integrità quando disponibili e disattiva l’autorizzazione dopo l’uso. Un APK ricevuto in chat o trovato tramite pubblicità non è una fonte affidabile.</p>
<p>Nell’Unione europea Apple consente, in condizioni specifiche, distribuzione alternativa e marketplace autorizzati. Apple avverte che assistenza, acquisti, rimborsi e controlli possono differire dall’App Store. Leggi le informazioni mostrate da iOS, verifica lo sviluppatore e considera se la stessa app è disponibile nello store ufficiale. Non modificare Paese o impostazioni di sicurezza soltanto per seguire istruzioni di uno sconosciuto.</p>
<h2>Aggiornare, disinstallare e proteggere l’account</h2>
<p>Attiva gli aggiornamenti automatici oppure controllali regolarmente: spesso correggono vulnerabilità oltre ad aggiungere funzioni. Se un’app non serve più, disinstallala e verifica se esiste un abbonamento separato da annullare; rimuovere l’icona non interrompe necessariamente i pagamenti. Proteggi Account Google o Apple con una password unica e autenticazione a due fattori.</p>
<p>Per telefoni usati da bambini, configura i controlli famiglia e richiedi l’autorizzazione per installazioni e acquisti. Prima di cedere il dispositivo, esegui backup, esci dagli account e usa il ripristino previsto dal produttore. Una buona installazione non finisce quando appare l’icona: comprende permessi proporzionati, aggiornamenti, costi chiari e una fonte riconoscibile.</p>
""",
        "sources": [
            ("https://support.google.com/googleplay/answer/113409?hl=it", "Google Play — trovare e scaricare app"),
            ("https://support.google.com/googleplay/answer/14122894?hl=it", "Google Play — risolvere i problemi di download"),
            ("https://support.apple.com/it-it/102590", "Apple — scaricare app su iPhone e iPad"),
            ("https://support.apple.com/it-it/102632", "Apple — se non riesci a scaricare o aggiornare app"),
            ("https://support.apple.com/it-it/117767", "Apple — distribuzione alternativa delle app nell’Unione europea"),
        ],
    },
]


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def dump(path: Path, value: object, compact: bool = False) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=None if compact else 2,
                      separators=(",", ":") if compact else None)
    write(path, text + ("" if compact else "\n"))


def news_url() -> str:
    return f"/notizie/{NEWS['slug']}.html"


def canonical(path: str) -> str:
    return f"https://curiomondo.it{path}"


def make_image() -> list[dict]:
    if not GENERATED.exists():
        raise SystemExit(f"Missing generated image: {GENERATED}")
    target_dir = ROOT / IMAGE_DIR.lstrip("/")
    target_dir.mkdir(parents=True, exist_ok=True)
    variants = []
    with Image.open(GENERATED) as image:
        source = image.convert("RGB")
        for width in (480, 800, 1200):
            height = round(width * 2 / 3)
            target = target_dir / f"{NEWS['image_key']}-{width}.webp"
            source.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=88, method=6)
            variants.append({"w": width, "src": f"{IMAGE_DIR}/{NEWS['image_key']}-{width}.webp",
                             "sha256": sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
    return variants


def feed_entry() -> dict:
    return {
        "title": NEWS["title"], "excerpt": NEWS["excerpt"], "url": news_url(), "section": NEWS["category"],
        "dateISO": NEWS["updated"], "dateLabel": DATE_LABEL,
        "image": f"{IMAGE_DIR}/{NEWS['image_key']}-800.webp", "imageAlt": NEWS["image_alt"],
        "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"{IMAGE_DIR}/{NEWS['image_key']}-{w}.webp {w}w" for w in (480, 800, 1200)),
    }


def article_html() -> str:
    path = news_url()
    c = canonical(path)
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": NEWS["title"],
        "description": NEWS["excerpt"], "datePublished": NEWS["published"], "dateModified": NEWS["updated"],
        "mainEntityOfPage": c, "inLanguage": "it-IT", "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{NEWS['image_key']}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; non fotografia documentaria.",
    }
    body = "".join(f"<p>{p}</p>" for p in NEWS["body"])
    insights = "".join(f"<div><b>{escape(a)}</b><small>{escape(b)}</small></div>" for a, b in NEWS["insights"])
    related = "".join(f'<a href="{u}"><small>{escape(section)}</small><strong>{escape(title)}</strong></a>' for u, section, title in NEWS["related"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in NEWS["sources"])
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(NEWS['title'])} | CurioMondo</title><meta name="description" content="{escape(NEWS['excerpt'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{c}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(NEWS['title'], quote=True)}"><meta property="og:description" content="{escape(NEWS['excerpt'], quote=True)}"><meta property="og:url" content="{c}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{NEWS['image_key']}-1200.webp"><meta property="og:image:alt" content="{escape(NEWS['image_alt'], quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=255"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{NEWS['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(NEWS['category'])}</div><h1>{escape(NEWS['title'])}</h1><p class="subtitle">{escape(NEWS['excerpt'])}</p><div class="meta">31 agosto 2026 · aggiornato alle 00:11 · Italia / Ambiente / Incendi · <span id="readTime">4 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="true"><picture><img src="../assets/images/editorial-v255/{NEWS['image_key']}-800.webp" srcset="../assets/images/editorial-v255/{NEWS['image_key']}-480.webp 480w, ../assets/images/editorial-v255/{NEWS['image_key']}-800.webp 800w, ../assets/images/editorial-v255/{NEWS['image_key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(NEWS['image_alt'], quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> incendi Sicilia 31 agosto 2026</div><div><strong>URL SEO:</strong> {path}</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="2000-4500">{body}</article><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 31 agosto 2026, ore 00:11 italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=255" defer></script></body></html>'''


def question_html() -> str:
    body = "\n".join(f"    <p{' class=\"q-principle\"' if i == 2 else ''}>{p}</p>" for i, p in enumerate(QUESTION_PARAGRAPHS))
    carry = "Quale comportamento continui a chiamare carattere, anche se compare soprattutto quando temi di essere ferito di nuovo?"
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(QUESTION_TITLE)} | CurioMondo</title><meta name="description" content="{escape(QUESTION_EXCERPT, quote=True)}"><link rel="canonical" href="https://curiomondo.it/domanda-del-giorno/{QUESTION_SLUG}/"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=211"><style>:root{{--q:#1769df;--ink:#102b44}}*{{box-sizing:border-box}}body{{background:radial-gradient(900px 520px at 84% 4%,rgba(23,105,223,.13),transparent 63%),linear-gradient(180deg,#f9fcff,#edf5ff 48%,#f8fbff);color:var(--ink)}}.q-hero{{position:relative;overflow:hidden;margin:24px auto 30px;max-width:1040px;padding:clamp(28px,5vw,58px);border:1px solid rgba(23,105,223,.17);border-radius:36px;background:linear-gradient(145deg,#fff,#edf6ff);box-shadow:0 32px 90px rgba(10,55,105,.13)}}.q-hero:after{{content:"?";position:absolute;right:-.03em;bottom:-.34em;font:900 clamp(15rem,35vw,29rem)/1 Georgia,serif;color:rgba(23,105,223,.045)}}.q-top{{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}}.q-badge{{padding:9px 14px;border-radius:999px;background:linear-gradient(135deg,#0d5ed2,#2588ff);color:#fff;font:850 .72rem/1 system-ui;text-transform:uppercase;letter-spacing:.14em}}.q-date{{font:750 .8rem/1.2 system-ui;color:#57718a}}.q-eye{{margin-top:38px;font:850 .74rem/1.3 system-ui;letter-spacing:.17em;text-transform:uppercase;color:var(--q)}}.q-hero h1{{position:relative;max-width:950px;margin:12px 0 20px;font:900 clamp(2.15rem,6vw,4.7rem)/1 system-ui;letter-spacing:-.052em;color:#071f38;text-wrap:balance}}.q-deck{{position:relative;max-width:760px;margin:0;font:600 clamp(1rem,2.2vw,1.2rem)/1.62 system-ui;color:#48657f}}.q-meta{{margin-top:22px;font:800 .73rem/1 system-ui;text-transform:uppercase;letter-spacing:.1em;color:#56728b}}.q-flow{{max-width:840px;margin:0 auto 46px;padding:clamp(38px,6vw,72px) clamp(25px,7vw,76px);border:1px solid rgba(13,73,132,.11);border-radius:32px;background:#fff;box-shadow:0 28px 85px rgba(12,55,101,.10)}}.q-flow:before{{content:"Riflessione";display:block;margin-bottom:28px;font:850 .68rem/1 system-ui;letter-spacing:.23em;text-transform:uppercase;color:var(--q)}}.q-flow>p{{margin:0 0 1.42em;font:450 clamp(1.12rem,2.45vw,1.27rem)/1.82 Georgia,serif;color:#17334d}}.q-flow>p:first-of-type:first-letter{{float:left;margin:.08em .13em 0 0;font:900 4.6rem/.76 system-ui;color:var(--q)}}.q-principle{{margin:2.15em -18px!important;padding:24px 26px!important;border-left:4px solid var(--q);background:#eef6ff;font-size:clamp(1.22rem,2.8vw,1.45rem)!important;font-style:italic}}.q-carry{{margin:2.2em -24px!important;padding:clamp(26px,5vw,38px)!important;border-radius:25px;background:linear-gradient(145deg,#071a31,#0a2e57);color:#fff!important;font:600 clamp(1.2rem,2.8vw,1.43rem)/1.66 system-ui!important}}.q-carry:after{{content:"Domanda da portare con te";display:block;margin-top:20px;font:800 .67rem/1 system-ui;letter-spacing:.16em;text-transform:uppercase;color:#8fc3ff}}.q-deeper{{margin:2.8rem -14px 0;padding:28px;border:1px solid #cde2fa;border-radius:24px;background:linear-gradient(135deg,#eef7ff,#f8fbff)}}.q-deeper p{{margin:0 0 18px;font:600 1rem/1.65 system-ui;color:#3b5b77}}.q-deeper strong{{display:block;color:#0b345a;font-size:1.12rem}}.q-deeper a{{display:inline-flex;padding:15px 18px;border-radius:14px;background:#1769df;color:#fff!important;text-decoration:none;font:850 .86rem/1.2 system-ui}}.q-sign{{padding-top:1.45rem;border-top:1px solid #d9e8f7;font:650 .82rem/1.4 system-ui!important;color:#62798e!important}}@media(max-width:700px){{.q-hero{{margin:14px 0 22px;padding:25px 21px 30px;border-radius:25px}}.q-flow{{margin:0 0 28px;padding:35px 22px 31px;border-radius:25px}}.q-principle,.q-carry{{margin:2em -8px!important}}.q-deeper{{margin:2.4rem -5px 0;padding:23px 20px}}.q-deeper a{{width:100%;justify-content:center;text-align:center}}}}</style></head><body class="cm-daily-page"><header class="cb-header"><div class="cb-shell"><a class="cb-brand" href="/"><span>Curio</span>Mondo</a><nav class="cb-nav" aria-label="Navigazione principale"><a href="/">Home</a><a href="/domanda-del-giorno/">Domanda del giorno</a><a href="/biblioteca/">Biblioteca</a></nav></div></header><main class="cb-shell"><section class="q-hero" aria-labelledby="question-title"><div class="q-top"><span class="q-badge">Domanda del giorno</span><span class="q-date">31 agosto 2026</span></div><div class="q-eye">Uno spazio per fermarsi e pensare.</div><h1 id="question-title">{escape(QUESTION_TITLE)}</h1><p class="q-deck">{escape(QUESTION_EXCERPT)}</p><div class="q-meta">4 min di lettura · CurioMondo</div></section><article class="q-flow" aria-label="Risposta alla Domanda del giorno">{body}<p class="q-carry">{carry}</p><div class="q-deeper"><p><strong>Vuoi andare più a fondo?</strong> L’eBook di oggi esplora il confine tra temperamento, abitudine e vecchie protezioni, con esercizi per costruire risposte più libere.</p><a href="/biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/">Apri l’eBook nella Biblioteca →</a></div><p class="q-sign"><strong>CurioMondo</strong> · uno spazio per fermarsi e pensare.</p></article></main><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def ebook_html() -> str:
    pages = []
    total = len(BOOK_PAGES)
    for i, (heading, paragraphs) in enumerate(BOOK_PAGES, 1):
        attrs = ' class="cm-book-page is-active" data-book-page' if i == 1 else ' class="cm-book-page" data-book-page aria-hidden="true"'
        h = f"<h2>{escape(heading)}</h2>" if heading else ""
        ps = "".join(f"<p>{p}</p>" for p in paragraphs)
        pages.append(f'<section{attrs}><span class="cm-book-kicker">eBook CurioMondo · 31 agosto 2026</span><h1>{escape(BOOK_TITLE)}</h1>{h}{ps}<span class="cm-book-page-number">{i} / {total}</span></section>')
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(BOOK_TITLE)} | eBook CurioMondo</title><meta name="description" content="Un eBook per distinguere temperamento, abitudini e vecchie difese, comprendendo quando il passato parla attraverso le nostre definizioni."><link rel="canonical" href="https://curiomondo.it/biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=211"><link rel="stylesheet" href="/assets/css/biblioteca-book-reader-v1.css?v=245"><style>.cm-book-note{{padding:18px 20px;border-left:4px solid #1769e0;border-radius:0 16px 16px 0;background:#eef6ff;font:700 .95rem/1.55 system-ui;color:#244b73}}.cm-dark .cm-book-note{{background:#102f55;color:#dbeaff}}</style></head><body><header class="cb-header"><div class="cb-shell"><a class="cb-brand" href="/"><span>Curio</span>Mondo</a><nav class="cb-nav"><a href="/">Notizie</a><a href="/biblioteca/">Biblioteca</a></nav></div></header><main class="cb-shell"><article class="cm-book-shell"><div class="cm-book-stage">{''.join(pages)}</div><nav class="cm-book-controls" aria-label="Navigazione eBook"><button data-book-prev type="button">← Indietro</button><button data-book-next type="button">Avanti →</button></nav><a class="cm-book-back" href="/biblioteca/vita-relazioni/domande-per-conoscersi/">← Torna alle Domande per conoscersi</a></article></main><noscript><style>.cm-book-page{{display:block!important;min-height:0;margin-bottom:20px}}</style></noscript><script defer src="/assets/js/biblioteca-book-reader-v1.js?v=245"></script><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def guide_html(guide: dict) -> str:
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in guide["sources"])
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(guide['title'])} | Biblioteca CurioMondo</title><meta name="description" content="{escape(guide['excerpt'], quote=True)}"><link rel="canonical" href="https://curiomondo.it/biblioteca/tecnologia-ai/smartphone-computer/{guide['slug']}/"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=211"><style>body{{margin:0;background:#f7fbff;color:#16324a;font-family:system-ui,-apple-system,sans-serif}}article{{max-width:920px;background:#fff;margin:24px auto 60px;padding:38px 44px;border:1px solid #d6e7f7;border-radius:26px;box-shadow:0 18px 50px rgba(20,70,130,.08)}}h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;color:#0a2b49}}h2{{color:#0d5fcb;margin-top:34px}}p,li{{font:1.07rem/1.74 Georgia,serif}}.box{{background:#eef6ff;border:1px solid #d6e8fb;padding:18px 20px;border-radius:16px;margin:22px 0}}.sources a{{overflow-wrap:anywhere}}@media(max-width:650px){{article{{margin:12px;padding:24px 20px}}}}</style></head><body><header class="cb-header"><div class="cb-shell"><a class="cb-brand" href="/"><span>Curio</span>Mondo</a><nav class="cb-nav"><a href="/">Notizie</a><a href="/biblioteca/">Biblioteca</a></nav></div></header><main class="cb-shell"><article><div class="cb-breadcrumb"><a href="/biblioteca/">Biblioteca</a> / <a href="/biblioteca/tecnologia-ai/smartphone-computer/">Smartphone &amp; Computer</a></div><p class="cb-kicker">Guida pratica · 31 agosto 2026</p><h1>{escape(guide['title'])}</h1>{guide['body']}<div class="box sources"><strong>Fonti ufficiali consultate</strong><ul>{sources}</ul><p>Le interfacce possono cambiare con gli aggiornamenti. Usa sempre le pagine di assistenza del produttore e verifica ciò che compare sul tuo dispositivo.</p></div></article></main><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def picture(item: dict, eager: bool = False) -> str:
    priority = ' fetchpriority="high"' if eager else ""
    return (f'<picture><img alt="{escape(item.get("imageAlt", ""), quote=True)}" decoding="async" '
            f'loading="{"eager" if eager else "lazy"}" height="533" sizes="(max-width:600px) 79vw,300px" '
            f'src="{escape(item.get("image", ""), quote=True)}" srcset="{escape(item.get("srcset", ""), quote=True)}" width="800"{priority}></picture>')


def update_data(variants: list[dict]) -> list[dict]:
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    home["version"] = VERSION
    home["items"] = [x for x in home["items"] if x.get("url") != news_url()] + [feed_entry()]
    home["items"].sort(key=lambda x: x.get("dateISO", ""), reverse=True)
    dump(home_path, home, compact=True)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    additions = [
        {"title": NEWS["title"], "excerpt": NEWS["excerpt"], "url": news_url(), "section": NEWS["category"]},
        {"title": QUESTION_TITLE, "excerpt": QUESTION_EXCERPT, "url": f"/domanda-del-giorno/{QUESTION_SLUG}/", "section": "Domanda del giorno"},
        {"title": BOOK_TITLE, "excerpt": "Temperamento, difese e libertà: un percorso per ascoltare il passato senza lasciargli il comando.", "url": f"/biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/", "section": "Biblioteca · Vita e relazioni"},
    ] + [{"title": x["title"], "excerpt": x["excerpt"], "url": f"/biblioteca/tecnologia-ai/smartphone-computer/{x['slug']}/", "section": "Biblioteca · Tecnologia"} for x in GUIDES]
    urls = {x["url"] for x in additions}
    search["version"] = VERSION
    search["items"] = additions + [x for x in search["items"] if x.get("url") not in urls]
    dump(search_path, search, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    registry["items"] = [x for x in registry.get("items", []) if x.get("article") != news_url()]
    registry["items"].insert(0, {"key": NEWS["image_key"], "article": news_url(), "aiGenerated": True,
        "sensitiveContext": True, "documentaryPhoto": False, "prompt": NEWS["prompt"], "variants": variants,
        "alt": NEWS["image_alt"], "disclosure": CAPTION, "portraitOnly": False,
        "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False})
    dump(registry_path, registry)
    return home["items"]


def update_home(items: list[dict]) -> None:
    news = [x for x in items if x.get("url", "").startswith("/notizie/")]
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for index, track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
        for child in list(track): track.remove(child)
        for item in news[:10]:
            a = etree.SubElement(track, "a", href=item["url"], **{"class": "ticker-news"})
            if index == 1: a.set("tabindex", "-1")
            a.text = item["title"]

    fire = feed_entry()
    hero = news[0]
    if hero["url"] == fire["url"] and len(news) > 1:
        cyprus = next((x for x in news if "cipro-naufragio-traghetto-filojet" in x["url"]), news[1])
        hero = cyprus
    old = doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
    new = html.fragment_fromstring(f'<a class="featured" href="{hero["url"]}">{picture(hero, True)}<div class="txt"><span class="tag">Ultima ora</span><h1>{escape(hero["title"])}</h1><p>{escape(hero["excerpt"])}</p><span class="cta">Leggi l’articolo →</span></div></a>')
    old.getparent().replace(old, new)
    rail_items = [x for x in news if x["url"] != hero["url"]][:5]
    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for child in list(rail): rail.remove(child)
    for item in rail_items:
        rail.append(html.fragment_fromstring(f'<a class="auto-card" href="{item["url"]}">{picture(item)}<div class="abody"><div class="ameta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3><p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'))
    cards = doc.xpath('//div[@id="cards"]')[0]
    for child in list(cards): cards.remove(child)
    used = {hero["url"], *(x["url"] for x in rail_items)}
    for item in [x for x in news if x["url"] not in used][:18]:
        cards.append(html.fragment_fromstring(f'<a class="card" href="{item["url"]}">{picture(item)}<div class="body"><div class="meta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3><p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'))

    q = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-qday ")]')[0]
    qlink = q.xpath('.//a[contains(concat(" ",normalize-space(@class)," ")," cm-qday-link ")]')[0]
    qlink.set("href", f"/domanda-del-giorno/{QUESTION_SLUG}/")
    qlink.set("aria-label", "Scopri la Domanda del giorno del 31 agosto 2026")
    qk = q.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," cm-qday-k ")]')[0]
    qk.text = "Domanda del giorno · 31 agosto 2026"
    card = q.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," cm-qday-card ")]')[0]
    hints = card.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," cm-qday-hint ")]')
    if not hints:
        hint = etree.SubElement(card, "p", **{"class": "cm-qday-hint"})
        hint.text = "Tocca per scoprirla"
    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", re.sub(r"[?&]v=\d+", "?v=255", script.get("src") or ""))
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def prepend_card(path: Path, container_xpath: str, card_html: str) -> None:
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    container = doc.xpath(container_xpath)[0]
    href = html.fragment_fromstring(card_html).get("href")
    for old in container.xpath(f'./a[@href="{href}"]'): container.remove(old)
    container.insert(0, html.fragment_fromstring(card_html))
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_indexes(items: list[dict]) -> None:
    prepend_card(ROOT / "domanda-del-giorno/index.html", '//section[contains(concat(" ",normalize-space(@class)," ")," cb-subgrid ")]',
        f'<a class="cb-subcard" href="/domanda-del-giorno/{QUESTION_SLUG}/"><span class="cb-kicker">31 agosto 2026</span><h2>{escape(QUESTION_TITLE)}</h2><p>Ferite, vecchie difese e libertà di rispondere al presente.</p><b>Leggi →</b></a>')
    prepend_card(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html", '//section[contains(concat(" ",normalize-space(@class)," ")," cb-subgrid ")]',
        f'<a class="cb-subcard" href="/biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/"><span class="cb-kicker">31 agosto 2026 · eBook</span><h2>{escape(BOOK_TITLE)}</h2><p>Riconoscere vecchie difese e costruire risposte più libere.</p><b>Sfoglia →</b></a>')
    tech = ROOT / "biblioteca/tecnologia-ai/smartphone-computer/index.html"
    for guide in reversed(GUIDES):
        prepend_card(tech, '//section[contains(concat(" ",normalize-space(@class)," ")," cb-manual-grid ")]',
            f'<a class="cb-subcard" href="/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/"><span class="cb-kicker">Nuova guida · 31 agosto 2026</span><h2>{escape(guide["title"])}</h2><p>{escape(guide["excerpt"])}</p><b>Leggi la guida →</b></a>')

    archive_path = ROOT / "notizie/index.html"
    doc = html.fromstring(archive_path.read_text(encoding="utf-8"))
    ul = doc.xpath("//main//ul")[0]
    if not ul.xpath(f'.//a[@href="{news_url()}"]'):
        li = etree.Element("li"); a = etree.SubElement(li, "a", href=news_url())
        strong = etree.SubElement(a, "strong"); strong.text = NEWS["title"]
        span = etree.SubElement(a, "span"); span.text = DATE_LABEL
        ul.insert(0, li)
    paragraphs = doc.xpath("//main/p")
    if paragraphs: paragraphs[0].text = f"{len([p for p in (ROOT / 'notizie').glob('*.html') if p.name != 'index.html'])} articoli, ordinati per data."
    write(archive_path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    news_items = [x for x in items if x.get("url", "").startswith("/notizie/")][:10]
    live["updated_at"] = "2026-08-30T22:11:00+00:00"
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"], "source": "CurioMondo", "article_exists": True} for x in news_items]
    dump(live_path, live)


def update_xml() -> None:
    entries = [
        (NEWS["title"], news_url(), NEWS["excerpt"], NEWS["updated"]),
        (QUESTION_TITLE, f"/domanda-del-giorno/{QUESTION_SLUG}/", QUESTION_EXCERPT, "2026-08-31T06:00:00+02:00"),
        (BOOK_TITLE, f"/biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/", "Un percorso per riconoscere vecchie difese e rispondere al presente con più libertà.", "2026-08-31T06:00:00+02:00"),
    ] + [(g["title"], f"/biblioteca/tecnologia-ai/smartphone-computer/{g['slug']}/", g["excerpt"], "2026-08-31T06:00:00+02:00") for g in GUIDES]
    feed_path = ROOT / "feed.xml"
    tree = etree.parse(str(feed_path)); channel = tree.getroot().find("channel")
    targets = {canonical(path) for _, path, _, _ in entries}
    for old in list(channel.findall("item")):
        if old.findtext("link") in targets: channel.remove(old)
    insertion = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    for title, path, desc, stamp in entries:
        node = etree.Element("item")
        for tag, value in (("title", title), ("link", canonical(path)), ("guid", canonical(path)), ("pubDate", format_datetime(datetime.fromisoformat(stamp))), ("description", desc)):
            child = etree.SubElement(node, tag); child.text = value
        channel.insert(insertion, node); insertion += 1
    tree.write(str(feed_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    site_path = ROOT / "sitemap.xml"
    tree = etree.parse(str(site_path)); root = tree.getroot()
    existing = {x.text for x in root.xpath('//*[local-name()="loc"]')}
    for _, path, _, _ in entries:
        if canonical(path) in existing: continue
        u = etree.SubElement(root, f"{{{ns}}}url")
        loc = etree.SubElement(u, f"{{{ns}}}loc"); loc.text = canonical(path)
        lastmod = etree.SubElement(u, f"{{{ns}}}lastmod"); lastmod.text = DATE_LABEL
    tree.write(str(site_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    news_path = ROOT / "news-sitemap.xml"
    tree = etree.parse(str(news_path)); root = tree.getroot()
    target = canonical(news_url())
    for node in list(root):
        locs = node.xpath('./*[local-name()="loc"]/text()')
        if locs and locs[0] == target: root.remove(node)
    nns = "http://www.google.com/schemas/sitemap-news/0.9"
    u = etree.SubElement(root, f"{{{ns}}}url")
    loc = etree.SubElement(u, f"{{{ns}}}loc"); loc.text = target
    news = etree.SubElement(u, f"{{{nns}}}news")
    pub = etree.SubElement(news, f"{{{nns}}}publication")
    name = etree.SubElement(pub, f"{{{nns}}}name"); name.text = "CurioMondo"
    lang = etree.SubElement(pub, f"{{{nns}}}language"); lang.text = "it"
    date = etree.SubElement(news, f"{{{nns}}}publication_date"); date.text = NEWS["published"]
    title = etree.SubElement(news, f"{{{nns}}}title"); title.text = NEWS["title"]
    tree.write(str(news_path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def update_state() -> None:
    topics_path = ROOT / "automation/state/guide-topics.json"
    topics = json.loads(topics_path.read_text(encoding="utf-8"))
    category = next(x for x in topics["categories"] if x["category"] == "Tecnologia e informatica")
    for guide in GUIDES:
        if guide["topic"] in category["remaining_topics"]: category["remaining_topics"].remove(guide["topic"])
        if guide["topic"] not in category["published_from_queue"]: category["published_from_queue"].append(guide["topic"])
    topics["version"] = 3
    dump(topics_path, topics)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = "v255"
    manifest["release_version"] = "v255"
    manifest["last_release_date"] = DATE_LABEL
    manifest["daily_state"]["last_question_date"] = DATE_LABEL
    manifest["daily_state"]["last_question_slug"] = QUESTION_SLUG
    manifest["last_release"] = {"version": VERSION, "date": DATE_LABEL, "baseline_version": 254,
        "news_added": [NEWS["slug"]], "news_updated": [], "evergreen_added": [],
        "daily_question_added": QUESTION_SLUG, "ebook_added": QUESTION_SLUG,
        "guides_added": [g["slug"] for g in GUIDES], "ads_txt": "preserved-authorized-v254",
        "image_policy_applied": "sensitive-wildfire-context-no-visible-victims-v255"}
    dump(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
            "baselineVersion": 254, "baseline_version": 254,
            "baseline": "curiomondo-v254-30-agosto-2026-adsense-ads-txt-netlify.zip",
            "date": DATE_LABEL, "release_date": DATE_LABEL, "articleCount": 201,
            "generatedEditorialImages": 81, "last_daily_question_date": DATE_LABEL,
            "last_update": "sicilia-incendi-domanda-ferita-guide-v255",
            "designRestored": "Incendi Sicilia pubblicati; domanda, eBook e due guide del 31 agosto aggiunti; home, LIVE e indici riallineati."})
        dump(path, data)

    write(ROOT / "RELEASE-NOTES-v255.md", f'''# CurioMondo v255 — 31 agosto 2026

- Pubblicato “{NEWS['title']}” come unico quadro nazionale dell’emergenza incendi.
- Creata una nuova immagine editoriale IA rispettosa: nessuna vittima, persona ferita o evacuata è raffigurata.
- Pubblicata la Domanda del giorno “{QUESTION_TITLE}” e il relativo eBook “{BOOK_TITLE}”.
- Pubblicate due guide pratiche: recupero sicuro delle password e installazione sicura delle app.
- Aggiornati home, LIVE, archivio, ricerca, feed RSS, sitemap, news sitemap, Biblioteca e manifesti.
- Conservato `ads.txt` con il publisher AdSense autorizzato.
''')
    predeploy = ROOT / "tools/predeploy.py"
    text = predeploy.read_text(encoding="utf-8")
    text = re.sub(r'"""CurioMondo v\d+ static pre-deploy audit\."""', '"""CurioMondo v255 static pre-deploy audit."""', text)
    text = re.sub(r"report=\{'version':\d+", "report={'version':255", text)
    write(predeploy, text)


def validate_new_pages() -> dict:
    article_chars = len(" ".join(NEWS["body"]))
    answer_chars = len(" ".join(QUESTION_PARAGRAPHS))
    ebook_chars = len(" ".join(p for _, paragraphs in BOOK_PAGES for p in paragraphs))
    guide_chars = {g["slug"]: len(re.sub(r"<[^>]+>", " ", g["body"])) for g in GUIDES}
    if not 2000 <= article_chars <= 4500: raise SystemExit(f"Article body length invalid: {article_chars}")
    if not 1000 <= answer_chars <= 3000: raise SystemExit(f"Question answer length invalid: {answer_chars}")
    if not 15000 <= ebook_chars <= 30000: raise SystemExit(f"Ebook length invalid: {ebook_chars}")
    for slug, chars in guide_chars.items():
        if not 3000 <= chars <= 15000: raise SystemExit(f"Guide length invalid {slug}: {chars}")
    if sum(1 for heading, _ in BOOK_PAGES if heading) > 7: raise SystemExit("Too many ebook H2 headings")
    return {"article": article_chars, "question": answer_chars, "ebook": ebook_chars, "guides": guide_chars}


def main() -> None:
    lengths = validate_new_pages()
    variants = make_image()
    write(ROOT / f"notizie/{NEWS['slug']}.html", article_html())
    dump(ROOT / f"contenuti/notizie/{NEWS['slug']}.json", {
        "slug": NEWS["slug"], "title": NEWS["title"], "excerpt": NEWS["excerpt"], "category": NEWS["category"],
        "published_at": NEWS["published"], "updated_at": NEWS["updated"], "body": NEWS["body"],
        "related": [x[0] for x in NEWS["related"]], "sources": [{"url": u, "label": label} for u, label in NEWS["sources"]],
        "image": {"key": NEWS["image_key"], "alt": NEWS["image_alt"], "ai_generated": True,
                  "sensitive_context": True, "documentary_photo": False, "disclosure": CAPTION}})
    write(ROOT / f"domanda-del-giorno/{QUESTION_SLUG}/index.html", question_html())
    write(ROOT / f"biblioteca/vita-relazioni/domande-per-conoscersi/{QUESTION_SLUG}/index.html", ebook_html())
    for guide in GUIDES:
        write(ROOT / f"biblioteca/tecnologia-ai/smartphone-computer/{guide['slug']}/index.html", guide_html(guide))
    items = update_data(variants)
    update_home(items)
    update_indexes(items)
    update_xml()
    update_state()
    print(json.dumps({"version": VERSION, "added": [NEWS["slug"], QUESTION_SLUG, *(g["slug"] for g in GUIDES)], "lengths": lengths}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
