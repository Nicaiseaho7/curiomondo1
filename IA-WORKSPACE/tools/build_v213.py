#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = "/assets/images/editorial-v213"
DISCLOSURE = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

NEWS = [
    {
        "slug": "niger-attacco-aeroporto-presidenza-niamey-29-agosto-2026",
        "title": "Niger, attacco all’aeroporto e alla presidenza: esplosioni e spari scuotono Niamey",
        "excerpt": "Uomini armati hanno colpito l’aeroporto internazionale e tentato di superare il perimetro della presidenza. Le forze di sicurezza dichiarano di avere ripreso il controllo, ma restano verifiche in corso.",
        "section": "Ultima ora · Mondo / Africa / Sicurezza",
        "date_iso": "2026-08-29T09:32:00+02:00",
        "date_label": "29 agosto 2026",
        "image": "niger-niamey-attacco-29-agosto-2026-ai",
        "alt": "Scena editoriale notturna nei pressi dell’aeroporto di Niamey con forze di sicurezza e fumo in lontananza",
        "keyword": "attacco aeroporto Niamey presidenza Niger",
        "insights": [("3", "gravi episodi di unrest a Niamey nel 2026"), ("2023", "anno del colpo di Stato militare"), ("15%", "quota dell’uranio Orano un tempo fornita dal Niger")],
        "guide": None,
        "sources": [
            ("Reuters — attacco all’aeroporto, tentativo contro il perimetro presidenziale e operazioni di sicurezza", "https://www.reuters.com/world/gunfire-blasts-heard-several-areas-niger-capital-niamey-witness-says-2026-08-29/"),
            ("Associated Press — esplosioni, dispiegamento delle forze e quadro di sicurezza a Niamey", "https://apnews.com/article/77d0c701e5729f2779580ea557e0a2c3")
        ],
        "body": [
            "Niamey si è svegliata con esplosioni e raffiche di armi da fuoco in più punti della capitale. Secondo due testimoni sentiti da Reuters, gli spari sono proseguiti nelle ore precedenti l’alba, mentre fonti della sicurezza hanno riferito che uomini indicati come terroristi hanno attaccato l’aeroporto internazionale Diori Hamani e tentato di avvicinarsi al perimetro della presidenza. Le autorità non hanno ancora diffuso un bilancio pubblico completo e diversi passaggi della ricostruzione restano da verificare in modo indipendente.",
            "L’aeroporto non è soltanto uno scalo civile. Nello stesso complesso si trova la Base 101, infrastruttura militare già finita nel mirino durante altri episodi di violenza. Un esponente del Consiglio consultivo del Niger ha scritto che le forze di difesa avevano ripreso il controllo della base; una fonte di sicurezza ha aggiunto che alcuni assalitori erano stati neutralizzati e altri erano fuggiti. Reuters ha però segnalato nuove esplosioni e colpi d’arma da fuoco anche dopo le prime dichiarazioni rassicuranti, un dettaglio che impone prudenza.",
            "La notizia è rilevante perché l’azione ha interessato contemporaneamente un nodo aeroportuale, una base militare e l’area della presidenza. Colpire luoghi di questo tipo produce un effetto che supera il danno materiale: serve a dimostrare la capacità di raggiungere il cuore politico e logistico della capitale. Finché non arriveranno comunicazioni ufficiali più dettagliate, non è possibile stabilire con certezza il numero degli assalitori, la loro appartenenza, l’eventuale presenza di vittime o la reale durata degli scontri.",
            "Il Niger è governato dai militari dal colpo di Stato del luglio 2023 che rovesciò il presidente Mohamed Bazoum. La giunta guidata dal generale Abdourahamane Tiani aveva promesso di migliorare la sicurezza, ma il Paese continua a fronteggiare gruppi armati legati ad al Qaeda e allo Stato Islamico. Anche Mali e Burkina Faso, i due principali alleati regionali di Niamey, vivono una pressione simile lungo una vasta fascia del Sahel dove frontiere porose, territori difficili da controllare e istituzioni fragili favoriscono la mobilità delle organizzazioni jihadiste.",
            "Il Sahel non è uno Stato né un’organizzazione: è la grande fascia semi-arida che attraversa l’Africa sotto il Sahara. Nel suo settore occidentale si sovrappongono crisi politiche, rotte commerciali e militari, traffici illegali, competizione per le risorse e movimenti armati. Capire questa geografia aiuta a leggere perché un attacco a Niamey non sia soltanto un fatto locale. La capitale è un centro di comando per le operazioni nigerine e per la cooperazione con Mali e Burkina Faso nell’Alleanza degli Stati del Sahel, nota come AES.",
            "L’AES è nata dopo la rottura dei tre governi militari con la Comunità economica degli Stati dell’Africa occidentale. I suoi membri cercano maggiore autonomia diplomatica e militare, hanno ridotto la collaborazione con diversi partner occidentali e rafforzato i rapporti con la Russia. Questa scelta ha cambiato alleanze e strumenti di sicurezza, ma non ha finora eliminato le insurrezioni. Ogni episodio nella capitale diventa quindi anche una verifica politica delle promesse con cui i militari hanno giustificato il proprio potere.",
            "C’è inoltre una dimensione economica. Il Niger possiede uranio, petrolio e oro ed è stato per anni un fornitore importante per l’industria nucleare europea. Il governo ha sequestrato asset collegati alla francese Orano e riassegnato permessi minerari a società sostenute dallo Stato. Sicurezza, controllo delle miniere e rapporti con l’estero si intrecciano: una capitale percepita come vulnerabile può complicare investimenti, trasporti e gestione delle infrastrutture strategiche.",
            "Le prossime informazioni decisive riguarderanno il bilancio degli scontri, l’identità del gruppo responsabile, lo stato operativo dell’aeroporto e le eventuali misure d’emergenza. Sarà importante distinguere tra comunicazioni governative, rivendicazioni dei gruppi armati e fatti verificati sul terreno. In questa fase la formula più corretta è che esistono testimonianze convergenti su un attacco grave e fonti della sicurezza che dichiarano di averlo respinto, ma il quadro non è ancora definitivo.",
            "Per la popolazione di Niamey, intanto, l’impatto immediato è l’incertezza. Spari in prossimità della presidenza e del principale aeroporto significano restrizioni, controlli e possibili interruzioni della mobilità. La capacità delle autorità di fornire rapidamente dati verificabili sarà parte della risposta: in una crisi di sicurezza, il controllo del territorio e la credibilità delle informazioni sono due elementi inseparabili."
        ]
    },
    {
        "slug": "cremona-tromba-aria-grandine-danni-29-agosto-2026",
        "title": "Cremona dopo la tromba d’aria: 40 feriti, diecimila auto e dieci chiese danneggiate",
        "excerpt": "Una tromba d’aria accompagnata da grandine ha colpito Cremona in pochi minuti. Nessuno dei feriti è grave, ma case scoperchiate, alberi caduti e danni diffusi hanno lasciato otto famiglie senza abitazione.",
        "section": "Italia · Cronaca / Maltempo",
        "date_iso": "2026-08-29T10:42:00+02:00",
        "date_label": "29 agosto 2026",
        "image": "cremona-grandine-danni-29-agosto-2026-ai",
        "alt": "Centro storico italiano dopo una violenta grandinata con auto danneggiate, alberi caduti e soccorritori",
        "keyword": "Cremona tromba aria grandine danni",
        "insights": [("40+", "feriti lievi confermati"), ("10.000", "automobili danneggiate"), ("10", "chiese colpite, compresa la cattedrale")],
        "guide": None,
        "sources": [("ANSA — bilancio dei danni e interventi di soccorso a Cremona", "https://www.ansa.it/sito/notizie/topnews/2026/08/29/-cremona-in-ginocchio-danni-a-10-chiese-e-10mila-auto-_433fae67-1996-44d8-b2c2-149801777dd3.html"), ("RaiNews TGR Lombardia — danni alla torre civica, alla cattedrale e alle abitazioni", "https://www.rainews.it/tgr/lombardia/video/2026/08/tromba-daria-su-cremona-danneggiate-torre-civica-e-cattedrale-8bdc1a86-b3b1-4100-9e25-fd92e4cd0463.html")],
        "body": [
            "Cremona conta i danni dopo una tromba d’aria accompagnata da una grandinata eccezionale che ha attraversato la città in circa dieci minuti. Il passaggio è stato breve, ma abbastanza intenso da mobilitare vigili del fuoco e volontari della protezione civile in un centinaio di interventi. Il bilancio comunicato da ANSA parla di oltre quaranta feriti, nessuno in condizioni gravi, insieme a danni estesi ad abitazioni, edifici religiosi, alberi e automobili.",
            "Almeno otto famiglie sono state evacuate perché le loro case non erano più utilizzabili in sicurezza. Decine di tetti risultano scoperchiati e la stabilità di altri fabbricati dovrà essere controllata. Le verifiche strutturali sono una fase essenziale dopo eventi di vento estremo: tegole, cornicioni, impianti e coperture possono sembrare ancora al loro posto ma essere stati indeboliti, creando rischi anche quando la pioggia è finita.",
            "Il patrimonio storico della città è tra i settori più colpiti. ANSA riferisce danni ad almeno dieci chiese, compresa la cattedrale. Per edifici antichi, il problema non riguarda soltanto la riparazione immediata: occorre proteggere gli interni dalle infiltrazioni, mettere in sicurezza elementi instabili e valutare materiali e tecniche compatibili con la conservazione. Sono operazioni più lente e delicate rispetto alla sostituzione di una copertura moderna.",
            "La grandine ha danneggiato almeno diecimila automobili, una cifra che dà la misura della superficie interessata. Chicchi sospinti dal vento possono colpire carrozzerie, parabrezza, lucernari e pannelli solari con energia molto superiore a quella di una normale precipitazione. Alberi abbattuti e rami spezzati hanno inoltre ostruito strade e cortili, complicando gli spostamenti dei mezzi di emergenza e le prime ricognizioni.",
            "Nel linguaggio comune si usa spesso l’espressione tromba d’aria per descrivere una colonna d’aria rotante molto intensa. Stabilire con precisione se si sia trattato di un tornado richiede però osservazioni meteorologiche, immagini dei danni e analisi della traiettoria. La severità non dipende soltanto dalla velocità massima del vento: contano anche durata, larghezza del percorso, presenza di grandine e vulnerabilità degli edifici incontrati.",
            "Nelle ore successive la priorità passa dal soccorso alla messa in sicurezza. I vigili del fuoco rimuovono elementi pericolanti, liberano accessi e verificano le coperture; i tecnici comunali e i professionisti valutano l’agibilità; la protezione civile coordina assistenza e sistemazione temporanea delle famiglie evacuate. È un lavoro meno visibile dell’emergenza iniziale, ma decisivo per evitare incidenti secondari.",
            "Per chi ha subito danni è utile documentare tutto prima delle riparazioni definitive, quando le condizioni lo consentono e senza esporsi a pericoli: fotografie, video, elenco dei beni colpiti e comunicazioni delle autorità possono servire nelle pratiche assicurative. Non bisogna salire sui tetti o avvicinarsi a cavi, alberi inclinati e strutture lesionate. La verifica deve essere affidata a tecnici e squadre abilitate.",
            "Il quadro economico emergerà solo nei prossimi giorni. Il numero delle auto coinvolte, le coperture danneggiate e gli interventi sul patrimonio religioso indicano comunque costi potenzialmente elevati. A questi si aggiungono interruzioni di attività, rimozione degli alberi, ripristino della viabilità e assistenza alle famiglie. La stima iniziale può cambiare quando iniziano le ispezioni edificio per edificio.",
            "L’episodio richiama anche il tema della prevenzione urbana. Manutenzione degli alberi, sistemi di allerta tempestivi, punti di riparo accessibili e protocolli condivisi con scuole, imprese e strutture sanitarie possono ridurre l’esposizione durante fenomeni molto rapidi. Non eliminano il pericolo, ma accorciano i tempi di reazione e aiutano a concentrare i soccorsi dove servono di più. Dopo la fase acuta, una ricognizione trasparente dei danni permetterà di capire quali edifici e servizi abbiano mostrato le maggiori fragilità e quali interventi rendano la città più pronta al prossimo evento estremo.",
            "La buona notizia, dentro un bilancio pesante, è che non risultano feriti gravi. Resta però una città segnata in modo diffuso e chiamata a una ricostruzione fatta di migliaia di interventi piccoli e grandi. Le prossime comunicazioni dovranno chiarire l’agibilità degli edifici, la situazione delle scuole e dei servizi, i sostegni disponibili e l’evoluzione meteorologica."
        ]
    },
    {
        "slug": "nepal-alluvione-ricostruzione-5-miliardi-29-agosto-2026",
        "title": "Nepal, ricostruzione fino a 5 miliardi: l’alluvione vale quasi un decimo dell’economia",
        "excerpt": "Il governo nepalese stima tra 4 e 5 miliardi di dollari per ricostruire dopo la piena devastante al confine con il Tibet. Oltre 600 morti e più di 2.000 dispersi.",
        "section": "Mondo · Asia / Clima / Economia",
        "date_iso": "2026-08-29T08:38:00+02:00",
        "date_label": "29 agosto 2026",
        "image": "nepal-alluvione-ricostruzione-29-agosto-2026-ai",
        "alt": "Valle himalayana colpita da un’alluvione con ponte distrutto, impianto idroelettrico danneggiato e squadre di soccorso",
        "keyword": "Nepal alluvione ricostruzione 5 miliardi",
        "insights": [("$4–5 mld", "stima iniziale della ricostruzione"), ("600+", "morti in Nepal e Tibet"), ("12%", "capacità elettrica coinvolta dai danni")],
        "guide": ("Che cosa sono le piene dei laghi glaciali e perché possono travolgere intere valli?", "come-funzionano-piene-laghi-glaciali-glof-himalaya.html"),
        "sources": [
            ("Reuters — stima della ricostruzione e impatto economico", "https://www.reuters.com/world/china/nepal-needs-least-4-billion-rebuilding-finance-minister-says-2026-08-29/"),
            ("Associated Press — soccorsi, dispersi e situazione umanitaria", "https://apnews.com/article/fde34c839b648f93f6aa011f044deb00")
        ],
        "body": [
            "Ricostruire le aree del Nepal devastate dall’alluvione potrebbe costare tra 4 e 5 miliardi di dollari, una cifra vicina a un decimo dell’intera economia nazionale. La stima preliminare è stata fornita a Reuters dal ministro delle Finanze Swarnim Wagle mentre soccorritori e autorità continuano a cercare migliaia di persone lungo il confine con il Tibet. Il conto umano ha superato le seicento vittime complessive e oltre duemila persone risultano ancora disperse.",
            "La piena è stata innescata dal collasso di una massa glaciale che ha liberato roccia, ghiaccio, fango e detriti nei sistemi fluviali himalayani. Il materiale ha attraversato vallate strette con enorme energia, spazzando via ponti, strade, abitazioni e infrastrutture. Le squadre di soccorso lavorano in un territorio difficile, con collegamenti interrotti, instabilità dei versanti e condizioni meteorologiche che possono rallentare o sospendere le operazioni.",
            "La stima economica è ancora provvisoria. Wagle ha spiegato che la valutazione completa di perdite e danni non è terminata. Il confronto più immediato è con il terremoto del 2015, che richiese circa 9 miliardi di dollari per la ricostruzione e distrusse più di mezzo milione di case. Questa volta la cifra assoluta potrebbe essere inferiore, ma il peso resta enorme per un Paese con risorse fiscali limitate e fortemente dipendente da rimesse, turismo e produzione idroelettrica.",
            "Il danno agli impianti idroelettrici è particolarmente sensibile. Secondo Reuters, i progetti colpiti rappresentano oltre il 12% della capacità di generazione del Nepal. L’idroelettrico fornisce gran parte dell’elettricità nazionale e sostiene esportazioni verso i Paesi vicini. Riparare turbine, condotte, linee e strade di accesso non significa quindi soltanto riaccendere la luce nelle zone colpite: vuol dire proteggere entrate, attività produttive e stabilità della rete.",
            "Una ricostruzione pari al 10% del prodotto interno lordo non viene pagata in un solo anno, ma assorbe capacità amministrativa e finanziaria per molto tempo. Il governo dovrà decidere quali infrastrutture riaprire prima, come assistere le famiglie che hanno perso la casa e quali standard usare per ricostruire in aree esposte a nuovi eventi. Donatori internazionali e banche multilaterali possono fornire prestiti o aiuti, ma ogni finanziamento comporta tempi, condizioni e controlli.",
            "Il punto tecnico da capire è che una piena glaciale può essere diversa da una normale alluvione monsonica. Quando ghiaccio, roccia o una morena cedono improvvisamente, l’acqua può trascinare sedimenti e massi formando una colata molto densa. Nelle valli strette la massa accelera e cambia il letto dei fiumi, distruggendo strutture che si trovavano anche a distanza dal punto di origine. Le immagini satellitari aiutano a ricostruire dove è avvenuto il collasso e quali bacini restano instabili.",
            "Associated Press riferisce che molte famiglie attendono notizie dei dispersi mentre i sopravvissuti raggiungono centri di assistenza con pochissimi beni. Alcuni tunnel presso progetti idroelettrici risultano pieni di fango e potrebbero contenere lavoratori intrappolati. In situazioni simili, la ricerca richiede attrezzature specialistiche, analisi geologiche e un equilibrio continuo tra urgenza e sicurezza dei soccorritori.",
            "La ricostruzione dovrà tenere insieme rapidità e adattamento climatico. Ripristinare esattamente ponti e strade nello stesso punto può essere la soluzione più veloce, ma non sempre quella più sicura se il corso del fiume è cambiato o se nuovi laghi glaciali stanno crescendo. Servono mappe aggiornate, sistemi di allerta, vie di evacuazione e regole che impediscano di ricostruire nelle zone con rischio maggiore.",
            "L’impatto si estende anche oltre il Nepal. La zona di confine collega comunità, pellegrinaggi, commercio e turismo tra Nepal e Tibet. Oltre cinquecento cittadini stranieri risultano tra i dispersi segnalati in Tibet e la ricerca coinvolge autorità di più Paesi. La cooperazione internazionale sarà necessaria non soltanto per i fondi, ma per identificazione delle vittime, soccorso tecnico, ripristino delle comunicazioni e monitoraggio dei versanti.",
            "I numeri continueranno a cambiare. La stima tra 4 e 5 miliardi offre però già una misura della crisi: non è solo un’emergenza di pochi giorni, ma un evento capace di condizionare sviluppo, energia e bilanci pubblici per anni. La qualità della ricostruzione determinerà se il Nepal riuscirà a ridurre il rischio della prossima piena o se sarà costretto a riparare ancora le stesse vulnerabilità."
        ]
    },
    {
        "slug": "iran-economia-guerra-sanzioni-commercio-29-agosto-2026",
        "title": "Iran, guerra e sanzioni soffocano l’economia: commercio estero giù del 35%",
        "excerpt": "Teheran ammette il peso della guerra con gli Stati Uniti: inflazione al 66% e scambi internazionali ridotti di circa un terzo. Nessun arretramento sullo Stretto di Hormuz.",
        "section": "Mondo · Medio Oriente / Economia",
        "date_iso": "2026-08-29T07:24:00+02:00",
        "date_label": "29 agosto 2026",
        "image": "iran-economia-sanzioni-29-agosto-2026-ai",
        "alt": "Mercato di Teheran durante una fase di forte pressione economica con commercianti e attività ridotta",
        "keyword": "Iran economia guerra sanzioni commercio",
        "insights": [("−35%", "calo dichiarato di importazioni ed esportazioni"), ("66%", "inflazione annua indicata per luglio"), ("20%", "quota mondiale di petrolio e GNL che passava da Hormuz prima della guerra")],
        "guide": ("Come funzionano le sanzioni sul petrolio iraniano e perché Hormuz è decisivo?", "come-funzionano-sanzioni-petrolio-iran-hormuz.html"),
        "sources": [("Reuters — dati economici, nuove sanzioni e posizione iraniana su Hormuz", "https://www.reuters.com/world/asia-pacific/war-weighs-irans-economy-us-intensifies-sanctions-2026-08-29/"), ("Axios — analisi indipendente sull’intensificazione della pressione economica su Teheran", "https://www.axios.com/2026/08/24/trump-iran-sanctions-bessent-economy")],
        "body": [
            "La leadership iraniana ammette apertamente che la guerra con gli Stati Uniti e la nuova stretta delle sanzioni stanno comprimendo l’economia. Il presidente Masoud Pezeshkian ha dichiarato che importazioni ed esportazioni sono diminuite di circa il 35% a causa delle misure americane e del blocco navale dei porti. Reuters indica inoltre un’inflazione annua arrivata al 66% nell’ultimo mese disponibile, un livello che erode rapidamente salari, risparmi e capacità di acquisto.",
            "Il riconoscimento della crisi non coincide però con un arretramento politico. In una dichiarazione diffusa dai media statali, Teheran ha promesso di resistere alla pressione, continuare la diplomazia e mantenere il controllo che rivendica sullo Stretto di Hormuz. È una combinazione deliberata: il governo prova a mostrare disponibilità al negoziato senza rinunciare alla leva strategica più importante, il passaggio marittimo che collega il Golfo ai mercati mondiali dell’energia.",
            "Le autorità hanno elencato tra le priorità il contenimento dell’inflazione, la gestione dei prezzi, la creazione di posti di lavoro, il sostegno alla produzione interna e una riduzione graduale della dipendenza dal dollaro. Sono obiettivi difficili da raggiungere mentre le entrate in valuta calano e le imprese faticano a pagare fornitori, assicurazioni e trasporti. Anche quando un bene non è formalmente vietato, banche e compagnie possono rifiutare l’operazione per paura di sanzioni secondarie.",
            "Le sanzioni secondarie sono lo strumento con cui Washington cerca di condizionare non soltanto soggetti americani, ma anche aziende e istituzioni di altri Paesi. In pratica, una banca straniera che continua determinate operazioni con l’Iran può rischiare l’esclusione dal sistema finanziario in dollari. Questa minaccia amplia l’effetto delle misure: molte controparti interrompono i rapporti prima ancora di ricevere una sanzione diretta.",
            "La nuova campagna americana ha colpito anche Banque Misr per rapporti con Teheran attraverso una struttura negli Emirati Arabi Uniti, proponendo restrizioni sulle transazioni in dollari delle filiali emiratine. Sono state inoltre annunciate misure contro un’entità di Hong Kong e una persona collegata a Bank Melli. Cina e India, partner commerciali molto più grandi dell’Iran, non sono state colpite allo stesso modo, probabilmente perché una rottura brusca avrebbe conseguenze più ampie per mercati e catene di approvvigionamento.",
            "La pressione arriva dopo sei mesi di guerra e dopo il fallimento di una breve intesa raggiunta a giugno con la mediazione di Qatar e Pakistan. Durante quella fase Washington aveva consentito alcune vendite di petrolio e Pezeshkian afferma che l’Iran riuscì a esportare circa 90 milioni di barili. Il cessate il fuoco non ha retto alle divergenze sullo stretto e le trattative restano bloccate.",
            "Prima del conflitto, da Hormuz transitava circa un quinto del petrolio e del gas naturale liquefatto mondiali. Il passaggio è stretto, difficile da sostituire e circondato da grandi produttori. Anche una riduzione parziale dei transiti influenza noli, assicurazioni e prezzi. Dati preliminari citati da Reuters mostrano soltanto sette navi merci in transito giovedì, contro 17 il giorno precedente e una media recente di 15.",
            "Gli Stati Uniti sostengono di avere rimosso mine posate dalle forze iraniane e il presidente Donald Trump ripete che il passaggio è aperto. La marina dei Guardiani della Rivoluzione contesta questa versione e afferma che nessuna nave possa transitare senza autorizzazione iraniana. Le dichiarazioni opposte rendono essenziale osservare i dati reali del traffico, non soltanto i messaggi politici.",
            "Per le famiglie iraniane il dibattito strategico si traduce in problemi quotidiani: prezzi che cambiano rapidamente, difficoltà a trovare alcuni beni, incertezza sul lavoro e perdita di valore della moneta. Il richiamo della guida suprema Mojtaba Khamenei a occuparsi di inflazione, disoccupazione e mercato segnala che il costo sociale è diventato un problema politico interno, non solo una conseguenza esterna da attribuire al nemico.",
            "La via d’uscita dipenderà da due dossier collegati: un accordo sulla guerra e una disciplina condivisa per la navigazione nello stretto. Qatar e altri mediatori tentano di ricostruire un canale, ma nessun progresso concreto è stato annunciato. Fino ad allora, la strategia americana punta a rendere economicamente insostenibile la resistenza iraniana, mentre Teheran usa Hormuz per dimostrare che la pressione può avere un costo anche per il resto del mondo."
        ]
    },
    {
        "slug": "qatarenergy-stop-gas-edison-italia-novembre-29-agosto-2026",
        "title": "Gas, QatarEnergy ferma altre cinque consegne a Edison: stop fino a novembre",
        "excerpt": "La guerra con l’Iran prolunga la forza maggiore sulle forniture di GNL all’Italia. I carichi cancellati salgono a 29, ma Edison afferma di avere già trovato volumi alternativi.",
        "section": "Italia · Economia / Energia",
        "date_iso": "2026-08-29T06:48:00+02:00",
        "date_label": "29 agosto 2026",
        "image": "qatarenergy-edison-gas-italia-29-agosto-2026-ai",
        "alt": "Terminale italiano di gas naturale liquefatto con metaniera al largo nell’Adriatico al crepuscolo",
        "keyword": "QatarEnergy Edison gas Italia consegne",
        "insights": [("29", "carichi di GNL cancellati complessivamente"), ("3,8 mld m³", "gas interessato dalle cancellazioni"), ("10%", "quota dei consumi italiani coperta dal contratto annuo")],
        "guide": ("Come funzionano le sanzioni sul petrolio iraniano e perché Hormuz è decisivo?", "come-funzionano-sanzioni-petrolio-iran-hormuz.html"),
        "sources": [("Reuters — proroga della forza maggiore e sostituzione dei carichi", "https://www.reuters.com/business/energy/qatarenergy-cancels-gas-deliveries-italys-edison-until-early-november-2026-08-28/"), ("The National — conferma indipendente della sospensione e dei cinque carichi aggiuntivi", "https://www.thenationalnews.com/business/energy/2026/08/28/qatarenergy-extends-lng-supply-suspension-to-italy-until-november/")],
        "body": [
            "QatarEnergy ha comunicato a Edison che la sospensione per forza maggiore delle consegne di gas naturale liquefatto continuerà fino ai primi giorni di novembre. La decisione riguarda altri cinque carichi previsti tra la fine di settembre e l’inizio di novembre e porta il totale delle consegne cancellate a 29, equivalenti a circa 3,8 miliardi di metri cubi di gas. La causa indicata è la prosecuzione della guerra tra Stati Uniti e Iran e le conseguenti difficoltà nelle rotte del Golfo.",
            "Per l’Italia è una notizia significativa perché il contratto di lungo periodo tra Edison e QatarEnergy prevede 6,4 miliardi di metri cubi l’anno, circa il 10% del consumo nazionale. L’accordo è in vigore dal 2009 e ha una durata di 25 anni. Non significa tuttavia che un decimo del gas italiano venga improvvisamente a mancare: Edison dichiara di avere sostituito i volumi e di poter rispettare tutti gli impegni commerciali con i clienti.",
            "Alla data del 28 agosto, secondo la società, al terminale Adriatic LNG erano già stati sostituiti 21 carichi per circa 2 miliardi di metri cubi. Trovare forniture alternative richiede acquisti da altri produttori, nuove finestre di attracco e capacità disponibile nei terminali. Il sistema può quindi compensare una parte importante dello stop, ma il costo dipende dai prezzi spot, dai noli marittimi e dalla concorrenza con compratori asiatici ed europei.",
            "Il GNL è gas naturale raffreddato fino a circa meno 162 gradi, temperatura alla quale diventa liquido e occupa molto meno spazio. Può essere trasportato in metaniere senza un gasdotto continuo. Arrivato al terminale, viene riportato allo stato gassoso e immesso nella rete. Questa flessibilità permette di cambiare fornitore più facilmente rispetto a una condotta, ma introduce dipendenza da navi, porti, impianti e condizioni di navigazione.",
            "La formula forza maggiore indica un evento eccezionale che impedisce a una parte di rispettare il contratto per cause fuori dal suo controllo. Non cancella automaticamente ogni obbligo e può essere contestata; consente però di sospendere o modificare le consegne quando guerra, blocchi o altri eventi rendono materialmente impossibile il trasporto. In questo caso QatarEnergy aveva già interrotto le forniture ad aprile.",
            "Il collegamento con lo Stretto di Hormuz è diretto. Il Qatar è uno dei maggiori esportatori mondiali di GNL e le sue metaniere devono attraversare quella rotta per raggiungere molti mercati. Prima della guerra, Hormuz concentrava circa il 20% dei flussi mondiali di petrolio e gas liquefatto. Anche quando una nave può tecnicamente passare, rischio militare, mine, controlli e premi assicurativi possono rendere il viaggio impraticabile o troppo costoso.",
            "La sicurezza energetica italiana si basa proprio sulla diversificazione. Gasdotti dal Nord Africa e dall’Azerbaigian, stoccaggi, terminali di rigassificazione e acquisti di GNL da più aree riducono il rischio che un singolo stop blocchi il sistema. La sostituzione annunciata da Edison mostra che questa rete di alternative funziona, ma non elimina l’esposizione ai prezzi internazionali.",
            "Per famiglie e imprese, il punto da osservare non è il numero dei carichi in sé, ma l’effetto sul costo medio di approvvigionamento e sulle scorte in vista dell’inverno. Se il gas sostitutivo viene acquistato a prezzi più alti, una parte della differenza può emergere nei contratti e nelle bollette con tempi diversi. Regolatori e operatori dovranno monitorare stoccaggi, disponibilità dei terminali e andamento del mercato europeo TTF.",
            "L’annuncio non segnala al momento un rischio immediato di interruzione per i clienti Edison. La società afferma di avere coperto i volumi e mantenere tutti gli impegni. Resta però un indicatore concreto di quanto una crisi nel Golfo possa arrivare fino al sistema energetico italiano: non necessariamente spegnendo le forniture, ma modificando rotte, tempi e prezzi con mesi di anticipo.",
            "Le prossime variabili sono la durata dello stop, la possibilità di riaprire in modo stabile la navigazione e l’evoluzione dei negoziati con l’Iran. Se la forza maggiore terminasse a novembre, il mercato avrebbe più certezza per l’inverno. Un’ulteriore proroga obbligherebbe invece Edison e altri compratori europei a continuare la ricerca di carichi alternativi in una stagione di domanda elevata."
        ]
    }
]


def article_html(item: dict) -> str:
    title = html.escape(item["title"])
    excerpt = html.escape(item["excerpt"])
    slug = item["slug"]
    image_base = f"../assets/images/editorial-v213/{item['image']}"
    canonical = f"https://curiomondo.it/notizie/{slug}.html"
    body = "".join(f"<p>{html.escape(p)}</p>" for p in item["body"])
    insight = "".join(f"<div><b>{html.escape(v)}</b><small>{html.escape(l)}</small></div>" for v, l in item["insights"])
    sources = "".join(f'<li><a href="{html.escape(url)}" rel="noopener noreferrer" target="_blank">{html.escape(label)}</a></li>' for label, url in item["sources"])
    guide = ""
    if item["guide"]:
        label, url = item["guide"]
        guide = f'<section aria-labelledby="cm-evergreen-question" class="cm-evergreen-reader"><small>Approfondimento collegato</small><h2 id="cm-evergreen-question">{html.escape(label)}</h2><p>Una guida CurioMondo per capire il meccanismo che sta dietro la notizia.</p><a href="{html.escape(url)}">Leggi l’approfondimento →</a></section>'
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": item["title"],
        "description": item["excerpt"], "datePublished": item["date_iso"], "dateModified": item["date_iso"],
        "mainEntityOfPage": canonical, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it/assets/images/editorial-v213/{item['image']}-1200.webp"]
    }
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{title} | CurioMondo</title><meta name="description" content="{excerpt}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{excerpt}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://curiomondo.it/assets/images/editorial-v213/{item['image']}-1200.webp"><meta property="og:image:alt" content="{html.escape(item['alt'])}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{slug}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{html.escape(item['section'])}</div><h1>{title}</h1><p class="subtitle">{excerpt}</p><div class="meta">{html.escape(item['date_label'])} · {html.escape(item['section'].replace('Ultima ora · ', ''))} · <span id="readTime">5 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’articolo</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image"><picture><img src="{image_base}-800.webp" srcset="{image_base}-480.webp 480w, {image_base}-800.webp 800w, {image_base}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{html.escape(item['alt'])}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{DISCLOSURE}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> {html.escape(item['keyword'])}</div><div><strong>URL SEO:</strong> /notizie/{slug}.html</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insight}</div></section><article class="art-body" data-length-policy="5000-7000">{body}</article>{guide}<div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Dati e ricostruzioni sono attribuiti alle fonti indicate e aggiornati al momento della pubblicazione.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js" defer></script></body></html>'''


def picture(item: dict, eager: bool = False) -> str:
    base = f"/assets/images/editorial-v213/{item['image']}"
    loading = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<picture><img src="{base}-800.webp" srcset="{base}-480.webp 480w, {base}-800.webp 800w, {base}-1200.webp 1200w" sizes="(max-width:600px) 79vw,300px" width="800" height="533"{loading} decoding="async" alt="{html.escape(item["alt"])}"></picture>'


def card(item: dict, cls: str) -> str:
    body_cls = "abody" if cls == "auto-card" else "body"
    meta_cls = "ameta" if cls == "auto-card" else "meta"
    return f'<a class="{cls}" href="/notizie/{item["slug"]}.html">{picture(item)}<div class="{body_cls}"><div class="{meta_cls}">{html.escape(item["section"])}</div><h3>{html.escape(item["title"])}</h3><p>{html.escape(item["excerpt"])}</p><time datetime="{item["date_iso"]}">2026-08-29</time></div></a>'


def replace_block(text: str, start: str, end: str, replacement: str) -> str:
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + text[b:]


def update_home() -> None:
    path = ROOT / "index.html"
    s = path.read_text()
    ticker_links = "".join(f'<a class="ticker-news" href="/notizie/{n["slug"]}.html">{html.escape(n["title"])}</a>' for n in NEWS)
    first = '<nav class="ticker-track" aria-label="Ultime notizie in diretta">'
    a = s.index(first); b = s.index('</nav>', a) + len('</nav>')
    s = s[:a] + first + ticker_links + '</nav>' + s[b:]
    hidden_start = '<div class="ticker-track" aria-hidden="true" inert="">'
    hidden = ''.join(f'<a class="ticker-news" tabindex="-1" href="/notizie/{n["slug"]}.html">{html.escape(n["title"])}</a>' for n in NEWS)
    a = s.index(hidden_start); b = s.index('</div>', a) + len('</div>')
    s = s[:a] + hidden_start + hidden + '</div>' + s[b:]
    rail_start = '<h2 class="auto-rail-label">Ultime notizie</h2>'
    featured_start = '<a class="featured"'
    a = s.index(rail_start); b = s.index(featured_start, a)
    rail = rail_start + '<div class="auto-rail">' + ''.join(card(n, 'auto-card') for n in NEWS) + '</div>'
    s = s[:a] + rail + s[b:]
    a = s.index(featured_start); b = s.index('<section class="cm-home-deep-links">', a)
    hero = NEWS[0]
    hero_html = f'<a class="featured" href="/notizie/{hero["slug"]}.html">{picture(hero, True)}<div class="txt"><span class="tag">Ultima ora</span><h1>{html.escape(hero["title"])}</h1><p>{html.escape(hero["excerpt"])}</p><span class="cta">Leggi l’articolo →</span></div></a>'
    s = s[:a] + hero_html + s[b:]
    cards_marker = '<div id="cards" class="cards" data-initial-count="12">'
    s = s.replace(cards_marker, cards_marker + ''.join(card(n, 'card') for n in NEWS), 1)
    universe = '''<section class="cm-orbit-experience" aria-labelledby="universo-curiomondo-title"><div class="cm-orbit-shell"><div class="cm-orbit-copy"><small class="cm-orbit-kicker">Esplora · Scopri · Ricorda</small><h2 id="universo-curiomondo-title">Universo CurioMondo</h2><p>Ogni notizia è una porta. Entra nel nostro universo e scopri curiosità, quiz e storie che aiutano a capire meglio il mondo.</p><div class="cm-earth-stats">Curiosità scoperte: <strong id="worldLearnedCount">0</strong></div></div><div class="cm-orbit-stage"><button id="worldCore" class="cm-orbit-core" type="button" aria-label="Scopri una curiosità"><span class="cm-curiomondo-orb-copy"><small>TOCCA IL PIANETA</small><strong>Curio<b>Mondo</b></strong><em>Scopri qualcosa di nuovo</em></span></button><button class="cm-planet-btn" data-orbit-action="quiz" type="button"><b>?</b><span>Quiz CurioMondo</span></button><button class="cm-planet-btn" data-orbit-action="favs" type="button"><b>★</b><span>I tuoi preferiti</span></button><button class="cm-planet-btn" data-orbit-action="about" type="button"><b>CM</b><span>Chi siamo</span></button><button class="cm-planet-btn" data-orbit-action="contact" type="button"><b>↗</b><span>Contatti</span></button><div id="worldFact" class="cm-world-curiosity" hidden><button id="worldFactClose" class="cm-world-curiosity-close" type="button" aria-label="Chiudi">×</button><div class="cm-world-curiosity-top"><span id="worldFactCategory">Curiosità</span><span>Scoperta n. <b id="worldFactCount">1</b></span></div><p id="worldFactText"></p><small>Una nuova curiosità ti aspetta ogni volta che tocchi il pianeta.</small></div></div></div></section>'''
    if 'class="cm-orbit-experience"' not in s:
        marker = '</div>\n</main>\n<footer class="site-footer">'
        s = s.replace(marker, '</div>' + universe + '\n</main>\n<footer class="site-footer">', 1)
    path.write_text(s)


def update_archive() -> None:
    path = ROOT / "notizie/index.html"
    s = path.read_text()
    s = re.sub(r'<p>\d+ articoli, ordinati per data\.</p>', '<p>184 articoli, ordinati per data.</p>', s, count=1)
    links = ''.join(f'<li><a href="/notizie/{n["slug"]}.html"><strong>{html.escape(n["title"])}</strong><span>2026-08-29</span></a></li>' for n in NEWS)
    s = s.replace('<ul>', '<ul>' + links, 1)
    path.write_text(s)


def update_json_indexes() -> None:
    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = json.loads(feed_path.read_text())
    new_items = [{"title": n["title"], "excerpt": n["excerpt"], "url": f'/notizie/{n["slug"]}.html', "section": n["section"], "dateISO": n["date_iso"], "dateLabel": "2026-08-29", "image": f'{IMG_DIR}/{n["image"]}-800.webp', "imageAlt": n["alt"], "imageWidth": 800, "imageHeight": 533, "srcset": f'{IMG_DIR}/{n["image"]}-480.webp 480w, {IMG_DIR}/{n["image"]}-800.webp 800w, {IMG_DIR}/{n["image"]}-1200.webp 1200w'} for n in NEWS]
    old_urls = {x["url"] for x in new_items}
    feed["version"] = 213
    feed["items"] = new_items + [x for x in feed["items"] if x.get("url") not in old_urls]
    feed_path.write_text(json.dumps(feed, ensure_ascii=False, separators=(",", ":")))
    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text())
    sitems = [{"title": n["title"], "excerpt": n["excerpt"], "url": f'/notizie/{n["slug"]}.html', "section": n["section"]} for n in NEWS]
    existing = {x["url"] for x in sitems}
    search["items"] = sitems + [x for x in search["items"] if x.get("url") not in existing]
    search_path.write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")))
    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text())
    live["updated_at"] = "2026-08-29T08:42:00+00:00"
    litems = [{"title": n["title"], "url": f'/notizie/{n["slug"]}.html', "published_at": n["date_iso"], "source": "CurioMondo", "article_exists": True} for n in NEWS]
    existing = {x["url"] for x in litems}
    live["items"] = litems + [x for x in live["items"] if x.get("url") not in existing]
    live_path.write_text(json.dumps(live, ensure_ascii=False, indent=2))


def update_xml() -> None:
    news_path = ROOT / "news-sitemap.xml"
    s = news_path.read_text()
    entries = ''.join(f'''\n  <url><loc>https://curiomondo.it/notizie/{html.escape(n['slug'])}.html</loc><news:news><news:publication><news:name>CurioMondo</news:name><news:language>it</news:language></news:publication><news:publication_date>{n['date_iso']}</news:publication_date><news:title>{html.escape(n['title'])}</news:title></news:news></url>''' for n in NEWS)
    s = re.sub(r'(<urlset[^>]*>)', r'\1' + entries, s, count=1)
    news_path.write_text(s)
    site_path = ROOT / "sitemap.xml"
    s = site_path.read_text()
    entries = ''.join(f'\n  <url><loc>https://curiomondo.it/notizie/{html.escape(n["slug"])}.html</loc><lastmod>2026-08-29</lastmod></url>' for n in NEWS)
    s = re.sub(r'(<urlset[^>]*>)', r'\1' + entries, s, count=1)
    site_path.write_text(s)
    rss_path = ROOT / "feed.xml"
    s = rss_path.read_text()
    entries = ''.join(f'''\n    <item><title>{html.escape(n['title'])}</title><link>https://curiomondo.it/notizie/{n['slug']}.html</link><guid>https://curiomondo.it/notizie/{n['slug']}.html</guid><pubDate>Sat, 29 Aug 2026 {n['date_iso'][11:19]} +0200</pubDate><description>{html.escape(n['excerpt'])}</description></item>''' for n in NEWS)
    s = s.replace('<channel>', '<channel>' + entries, 1)
    rss_path.write_text(s)


def update_release() -> None:
    state_path = ROOT / "RELEASE-STATE.json"
    state = json.loads(state_path.read_text())
    state.update({"currentVersion": 213, "baselineVersion": 212, "status": "ready", "date": "2026-08-29", "articleCount": 184, "generatedEditorialImages": 63, "designRestored": "Homepage premium ricostruita sulle misure del riferimento: rail orizzontali, Ultima ora rossa lampeggiante e Universo CurioMondo"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    pre = ROOT / "tools/predeploy.py"
    s = pre.read_text().replace("report={'version':212", "report={'version':213")
    pre.write_text(s)


def main() -> None:
    for n in NEWS:
        body_chars = sum(len(p) for p in n["body"])
        if body_chars < 4200:
            raise SystemExit(f"Articolo troppo corto: {n['slug']} ({body_chars})")
        (ROOT / f"notizie/{n['slug']}.html").write_text(article_html(n))
    update_home()
    update_archive()
    update_json_indexes()
    update_xml()
    update_release()
    (ROOT / "RELEASE-NOTES-v213.md").write_text("""# CurioMondo v213 — homepage premium e notizie del 29 agosto 2026\n\n- Design mobile ricostruito sulle dimensioni del riferimento.\n- Cinque nuove notizie complete in Ultime notizie, LIVE, archivio, ricerca, feed e sitemap.\n- Niamey scelta come Ultima ora, con badge rosso lampeggiante.\n- Tutte le raccolte della homepage scorrono orizzontalmente.\n- Universo CurioMondo ripristinato in fondo alla pagina.\n- Cinque immagini editoriali IA nuove e non riutilizzate.\n""")


if __name__ == "__main__":
    main()
