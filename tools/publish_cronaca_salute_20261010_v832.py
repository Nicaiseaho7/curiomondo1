#!/usr/bin/env python3
"""Release v832: cronaca, sicurezza, salute e ambiente del 10 ottobre 2026."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

ROME = ZoneInfo("Europe/Rome")
VERSION = 832

base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "cologno": ROOT.parent / "generated_images/exec-4c19efdd-8b5d-4148-bfcf-4f8d4150f197.png",
    "pontecorvo": ROOT.parent / "generated_images/exec-55cb73b1-3d26-4371-ae08-82a0d2900ab4.png",
    "pellaro": ROOT.parent / "generated_images/exec-11382fd2-3c96-44f6-949e-7ee160ca16f6.png",
    "campoli": ROOT.parent / "generated_images/exec-3a936342-fd19-4d85-93bc-1267ec304b94.png",
    "tuscolano": ROOT.parent / "generated_images/exec-d1d303c3-f47c-4a05-a44b-bb18383818fe.png",
    "obesita": ROOT.parent / "generated_images/exec-fa562119-6b2f-4be5-89ed-558c3527ea3b.png",
    "ecdc": ROOT.parent / "generated_images/exec-252202d3-0280-491f-8807-180c3b4a342b.png",
    "uccelli": ROOT.parent / "generated_images/exec-8773d8ec-c362-4029-b797-4ce66361f672.png",
    "waveguard": ROOT.parent / "generated_images/exec-5daa13d2-b2a9-482b-8c98-ebe9325a1788.png",
    "natura": ROOT.parent / "generated_images/exec-1933483b-e4f5-4afb-ae4f-b6af84ca36e1.png",
}

ARTICLES = [
    {
        "slug": "cologno-monzese-quattro-arresti-arma-clandestina-indagini-10-10-2026",
        "titolo": "Cologno Monzese, quattro arresti dopo l'aggressione: sequestrata un'arma",
        "sommario": "I Carabinieri hanno arrestato quattro uomini per l'ipotesi di detenzione in concorso di un'arma clandestina. Le altre contestazioni restano al vaglio degli inquirenti.",
        "categoria": "Cronaca", "luogo": "Cologno Monzese", "formato": "flash",
        "parole_chiave_titolo": ["Cologno Monzese", "quattro arresti"],
        "dati_chiave": [{"valore": "4", "etichetta": "persone arrestate"}, {"valore": "7 ottobre", "etichetta": "data dell'intervento"}, {"valore": "2", "etichetta": "giovani rimasti feriti"}],
        "paragrafi": [
            "Quattro uomini tra i 18 e i 41 anni sono stati arrestati dai Carabinieri della Tenenza di Cologno Monzese per l'ipotesi di detenzione illegale, in concorso, di un'arma clandestina. Il provvedimento è stato adottato in flagranza e dovrà essere valutato dall'autorità giudiziaria.",
            "L'intervento è collegato a una violenta aggressione avvenuta nella notte tra il 6 e il 7 ottobre, nella quale due giovani sono rimasti feriti. Le loro condizioni e la dinamica completa dell'episodio sono state oggetto degli accertamenti investigativi.",
            "Secondo il comunicato dell'Arma, durante le perquisizioni sono stati recuperati una pistola con matricola abrasa, un machete, un coltello e indumenti che potrebbero essere utili alle verifiche. Tutti gli elementi sequestrati dovranno essere analizzati.",
            "I quattro sono stati anche segnalati all'autorità giudiziaria per le ipotesi di tentato omicidio, lesioni gravi e rapina. Si tratta di contestazioni provvisorie: la responsabilità individuale potrà essere accertata soltanto nel procedimento e con una decisione definitiva.",
            "Gli investigatori stanno ricostruendo ruoli, movimenti e motivi dell'aggressione anche attraverso testimonianze e immagini disponibili. La presenza degli oggetti sequestrati non consente, da sola, di attribuire ogni condotta a ciascun indagato.",
            "Per la sicurezza della zona sono proseguiti controlli mirati. Chi possiede informazioni utili può rivolgersi alle forze dell'ordine evitando di diffondere online nomi, immagini o ricostruzioni non verificate.",
        ],
        "fonti": [{"url": "https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa/tentato-omicidio-arrestate-4-persone-nell%27hinterland-milanese", "nome": "Carabinieri — comunicato sull'arresto di quattro persone nell'hinterland milanese."}, {"url": "https://www.rainews.it/tgr/lombardia/articoli/2026/10/rissa-tra-latin-kings-con-pistole-e-machete-quattro-arresti-a-cologno-monzese-edbcd970-e37e-41a7-b9d6-8eb5e4b33558.html", "nome": "RaiNews TGR Lombardia — riscontro sull'operazione e sui sequestri."}],
        "image_source": "cologno", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di una strada di Cologno Monzese presidiata nella notte; non è una fotografia dell'operazione.",
        "image_prompt": "Strada di Cologno Monzese presidiata nella notte, nessuna persona o violenza visibile; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "ecdc-minacce-sanitarie-europa-settimana-41-ottobre-2026",
        "titolo": "ECDC, il nuovo bollettino aggiorna le minacce sanitarie in Europa",
        "sommario": "Il rapporto della settimana 41 segue virus respiratori, West Nile, dengue, chikungunya, morbillo e altri eventi. In Italia resta segnalato un caso locale di chikungunya.",
        "categoria": "Salute", "luogo": "Europa", "formato": "flash",
        "parole_chiave_titolo": ["ECDC", "minacce sanitarie"],
        "dati_chiave": [{"valore": "3-9 ottobre", "etichetta": "periodo coperto"}, {"valore": "1", "etichetta": "caso locale di chikungunya in Italia"}, {"valore": "18", "etichetta": "Paesi con casi umani locali di West Nile"}],
        "paragrafi": [
            "L'ECDC ha pubblicato il rapporto settimanale sulle minacce da malattie trasmissibili relativo al periodo dal 3 al 9 ottobre 2026. Il documento è destinato agli operatori sanitari, ma offre anche una fotografia aggiornata degli eventi seguiti nell'Unione europea e nello Spazio economico europeo.",
            "Tra i temi compaiono la circolazione dei virus respiratori, il morbillo, il virus West Nile, dengue e chikungunya. Il bollettino include inoltre aggiornamenti su Ebola, febbre emorragica Crimea-Congo e altri eventi internazionali sottoposti a sorveglianza.",
            "Per la chikungunya, alla data del 7 ottobre risultavano casi acquisiti localmente in Francia e un caso in Italia. Un caso locale indica una trasmissione avvenuta sul territorio, ma non equivale automaticamente a una diffusione estesa nel Paese.",
            "Il rapporto conta 1.855 casi umani locali di infezione da West Nile segnalati in 18 Paesi europei dall'inizio della stagione. I dati sono aggregati da sistemi nazionali con tempi di notifica differenti e possono essere aggiornati retrospettivamente.",
            "L'ECDC non presenta il bollettino come un'allerta generalizzata per i viaggiatori. Le misure utili dipendono dal luogo e comprendono protezione dalle punture di zanzara, rispetto degli avvisi sanitari locali e valutazione medica in caso di febbre o sintomi persistenti.",
            "Per l'Italia restano centrali i bollettini dell'Istituto superiore di sanità e delle autorità regionali. Il rapporto europeo aiuta a confrontare il quadro, ma non sostituisce diagnosi, indicazioni cliniche o comunicazioni territoriali.",
        ],
        "fonti": [{"url": "https://www.ecdc.europa.eu/en/publications-data/communicable-disease-threats-report-3-9-october-week-41", "nome": "ECDC — Communicable Disease Threats Report, settimana 41 del 2026."}],
        "image_source": "ecdc",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un centro europeo di sorveglianza epidemiologica; scena non documentaria.",
        "image_prompt": "Centro europeo di sorveglianza epidemiologica con ricercatori e mappa dell'Europa; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "reggio-calabria-rapina-gioielleria-pellaro-tre-misure-10-10-2026",
        "titolo": "Rapina in gioielleria a Reggio Calabria, eseguite tre misure cautelari",
        "sommario": "Il gip ha disposto il carcere per un indagato e i domiciliari per altri due. L'inchiesta riguarda il colpo del 26 febbraio in un negozio di Pellaro.",
        "categoria": "Cronaca", "luogo": "Reggio Calabria", "formato": "flash",
        "parole_chiave_titolo": ["Reggio Calabria", "gioielleria"],
        "dati_chiave": [{"valore": "3", "etichetta": "misure cautelari"}, {"valore": "oltre 23.000 €", "etichetta": "valore stimato dei monili"}, {"valore": "26 febbraio", "etichetta": "data della rapina contestata"}],
        "paragrafi": [
            "I Carabinieri della Compagnia di Reggio Calabria hanno eseguito tre misure cautelari nell'inchiesta sulla rapina a una gioielleria di Pellaro del 26 febbraio. Il gip ha disposto la custodia in carcere per un indagato e gli arresti domiciliari per altri due.",
            "Secondo l'ipotesi accusatoria, una dipendente sarebbe stata minacciata durante il colpo e i responsabili si sarebbero impossessati di monili in oro per un valore stimato superiore a 23 mila euro.",
            "Le indagini sono state condotte dai Carabinieri della Stazione di Pellaro e coordinate dalla Procura di Reggio Calabria. Il provvedimento cautelare si basa sul quadro raccolto finora e non costituisce una sentenza.",
            "Le misure hanno intensità differenti perché il giudice valuta posizione, esigenze cautelari e circostanze attribuite a ciascuna persona. I dettagli completi potranno essere discussi dalla difesa nelle sedi previste.",
            "Le persone coinvolte devono essere considerate non colpevoli fino a una eventuale condanna definitiva. Anche il valore del bottino e la ricostruzione dei ruoli restano elementi dell'accusa da verificare nel processo.",
            "Per commercianti e cittadini, le autorità raccomandano di segnalare tempestivamente movimenti sospetti e conservare le registrazioni degli impianti di videosorveglianza senza diffonderle sui social.",
        ],
        "fonti": [{"url": "https://www.carabinieri.it/in-vostro-aiuto/informazioni/news/2026/10/10/new0-20261010085700-1906891", "nome": "Carabinieri — notizia sulle tre misure cautelari per la rapina di Pellaro."}, {"url": "https://www.rainews.it/tgr/calabria/articoli/2026/10/reggio-rapina-ina-gioielleria-di-pellaro-3-arresti-8ef50d5a-5228-4318-b962-873df6913072.html", "nome": "RaiNews TGR Calabria — conferma dell'esecuzione delle misure e del valore contestato."}],
        "image_source": "pellaro", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica dell'esterno di una gioielleria a Pellaro messa in sicurezza; non è una fotografia dell'operazione.",
        "image_prompt": "Gioielleria a Pellaro messa in sicurezza, nessuna persona o violenza visibile; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "oms-obesita-bambini-adolescenti-linee-guida-7-ottobre-2026",
        "titolo": "Obesità nei minori, le prime linee guida globali dell'OMS",
        "sommario": "Priorità a dieta, attività fisica e sostegno comportamentale con il coinvolgimento delle famiglie. Sotto i 10 anni non sono raccomandati farmaci o chirurgia.",
        "categoria": "Salute", "luogo": "Ginevra", "formato": "flash",
        "parole_chiave_titolo": ["obesità nei minori", "linee guida OMS"],
        "dati_chiave": [{"valore": "0-9 anni", "etichetta": "fascia senza farmaci o chirurgia"}, {"valore": "170 milioni", "etichetta": "minori con obesità nel 2024"}, {"valore": "4 volte", "etichetta": "aumento dal 1990"}],
        "paragrafi": [
            "L'Organizzazione mondiale della sanità ha pubblicato le prime linee guida globali per la gestione integrata dell'obesità nei bambini e negli adolescenti. Il documento punta su percorsi personalizzati, continuativi e senza stigma, costruiti con famiglie e professionisti.",
            "L'OMS raccomanda programmi strutturati che combinino alimentazione, attività fisica e sostegno al cambiamento dei comportamenti. Il supporto digitale può essere utilizzato in alcuni casi, con la supervisione di un genitore o di chi si prende cura del minore.",
            "Per i bambini da zero a nove anni l'OMS non raccomanda farmaci, chirurgia bariatrica o dispositivi per la perdita di peso, perché le prove su benefici e sicurezza a lungo termine non sono considerate sufficienti.",
            "Dai 10 ai 19 anni, farmaci o chirurgia possono essere presi in considerazione soltanto in situazioni selezionate, dopo una valutazione specialistica e quando gli interventi assistiti sullo stile di vita non hanno ottenuto risultati adeguati. Non sono scorciatoie né indicazioni per l'autogestione.",
            "Nel 2024 circa 170 milioni di persone tra 5 e 19 anni vivevano con obesità, secondo i dati richiamati dall'OMS. La prevalenza nel gruppo è quadruplicata rispetto al 1990, ma peso e indice di massa corporea non bastano da soli a definire la salute del singolo bambino.",
            "Le famiglie non dovrebbero modificare terapie o acquistare prodotti dimagranti senza una valutazione pediatrica. Il documento insiste anche su accesso a cibi sani, spazi per muoversi, salute mentale e contrasto alla discriminazione.",
        ],
        "fonti": [{"url": "https://www.who.int/news/item/07-10-2026-who-issues-first-global-guidelines-on-child-and-adolescent-obesity", "nome": "OMS — prime linee guida globali sull'obesità in bambini e adolescenti."}, {"url": "https://www.reuters.com/business/healthcare-pharmaceuticals/who-endorses-lifestyle-changes-over-glp-1-drugs-child-obesity-fight-2026-10-07/", "nome": "Reuters — riscontro indipendente sulle raccomandazioni e sui limiti delle prove."}],
        "image_source": "obesita",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un colloquio pediatrico rispettoso su alimentazione e attività fisica; scena non documentaria.",
        "image_prompt": "Pediatra, genitore e bambino parlano di alimentazione e movimento senza stigma; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "pontecorvo-auto-autolavaggio-carabiniere-arresto-10-10-2026",
        "titolo": "Pontecorvo, arrestato un 19enne dopo il furto in un autolavaggio",
        "sommario": "I Carabinieri contestano furto, resistenza e lesioni dopo un intervento ad Aquino. L'arresto è avvenuto in flagranza e resta soggetto al vaglio giudiziario.",
        "categoria": "Cronaca", "luogo": "Pontecorvo", "formato": "flash",
        "parole_chiave_titolo": ["Pontecorvo", "autolavaggio"],
        "dati_chiave": [{"valore": "19 anni", "etichetta": "età dell'arrestato"}, {"valore": "4", "etichetta": "ipotesi contestate"}, {"valore": "Aquino", "etichetta": "luogo dell'intervento iniziale"}],
        "paragrafi": [
            "Un diciannovenne residente a Pontecorvo è stato arrestato in flagranza dai Carabinieri dopo il furto dell'incasso dalla gettoniera di un autolavaggio ad Aquino. Le contestazioni indicate sono furto, resistenza a pubblico ufficiale, lesioni e guida senza patente.",
            "Secondo la ricostruzione diffusa dall'Arma, il giovane sarebbe stato individuato alla guida di un'auto sottratta poco prima a un familiare. Non avrebbe mai conseguito la patente.",
            "Condotto in caserma per gli atti, avrebbe tentato di allontanarsi e durante il blocco un militare avrebbe riportato lesioni. La prognosi e gli esiti sanitari non sono stati dettagliati nella comunicazione disponibile.",
            "L'arresto in flagranza fotografa una fase iniziale del procedimento. Spetterà all'autorità giudiziaria valutarne la convalida e le eventuali misure; la responsabilità penale non è definitiva.",
            "Le fonti locali riferiscono che l'intervento è avvenuto dopo la segnalazione del danneggiamento all'autolavaggio. Ulteriori elementi sulla successione dei fatti potranno emergere dagli accertamenti e dalle dichiarazioni delle parti.",
            "Diffondere identità, immagini o giudizi personali non aiuta l'indagine e può danneggiare le persone coinvolte. Per informazioni utili resta corretto rivolgersi direttamente alle forze dell'ordine.",
        ],
        "fonti": [{"url": "https://www.carabinieri.it/in-vostro-aiuto/informazioni/news/2026/10/10/new0-20261010092700-1906900", "nome": "Carabinieri — notizia sull'arresto eseguito tra Aquino e Pontecorvo."}, {"url": "https://www.tunews24.it/2026/10/10/ruba-lauto-del-nonno-assalta-un-autolavaggio-e-aggredisce-un-carabiniere-arrestato-19enne/", "nome": "TuNews24 — riscontro locale sulla dinamica comunicata dagli investigatori."}],
        "image_source": "pontecorvo", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di un autolavaggio ad Aquino messo in sicurezza; non è una fotografia dell'intervento.",
        "image_prompt": "Autolavaggio ad Aquino messo in sicurezza con auto dei Carabinieri vuota; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "giornata-uccelli-migratori-italia-citizen-science-10-10-2026",
        "titolo": "Uccelli migratori, ISPRA invita i cittadini a segnalare gli avvistamenti",
        "sommario": "La giornata mondiale del 10 ottobre mette al centro la scienza partecipata. L'Italia è un ponte decisivo lungo le rotte tra Europa e Africa.",
        "categoria": "Ambiente", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["uccelli migratori", "avvistamenti"],
        "dati_chiave": [{"valore": "10 ottobre", "etichetta": "giornata mondiale"}, {"valore": "110+", "etichetta": "Paesi coinvolti nell'area AEWA"}, {"valore": "circa 300", "etichetta": "specie mappate dall'Atlante europeo"}],
        "paragrafi": [
            "ISPRA e Ministero dell'Ambiente invitano i cittadini a registrare gli avvistamenti di uccelli migratori in occasione della giornata mondiale del 10 ottobre. Il tema del 2026 sottolinea che ogni osservazione può contribuire alla ricerca.",
            "L'Italia si trova lungo una delle principali rotte che collegano Eurasia e Africa. Mari, montagne e zone umide offrono aree di sosta essenziali a milioni di uccelli durante gli spostamenti stagionali.",
            "I dati raccolti tramite piattaforme come eBird, iNaturalist e Ornitho possono aiutare a individuare cali delle popolazioni, cambiamenti nelle rotte e habitat da proteggere. Le osservazioni devono essere precise e non devono disturbare gli animali.",
            "Per gli uccelli con anelli leggibili a distanza, ISPRA raccoglie in Italia le segnalazioni attraverso il proprio canale dedicato. Fotografie e coordinate sono utili soltanto quando vengono ottenute rispettando distanze e divieti di accesso.",
            "Tra le minacce indicate figurano perdita di habitat, cambiamento climatico, bracconaggio, plastica, collisioni con infrastrutture e inquinamento luminoso. Un singolo avvistamento non dimostra però da solo un cambiamento nella popolazione.",
            "Il 2026 segna anche i sessant'anni dell'International Waterbird Census. In Italia il monitoraggio degli uccelli acquatici è coordinato scientificamente da ISPRA da oltre trent'anni.",
        ],
        "fonti": [{"url": "https://www.isprambiente.gov.it/it/news/giornata-mondiale-degli-uccelli-migratori", "nome": "ISPRA — giornata mondiale, rotte italiane e indicazioni per la citizen science."}, {"url": "https://www.worldmigratorybirdday.org/", "nome": "World Migratory Bird Day — campagna internazionale e tema del 2026."}],
        "image_source": "uccelli",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di uccelli migratori osservati in una zona umida italiana; scena non documentaria.",
        "image_prompt": "Uccelli migratori sopra una zona umida italiana con osservatori di profilo; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "roma-tuscolano-controlli-quattro-arresti-locale-sospeso-9-10-2026",
        "titolo": "Roma, controlli al Tuscolano: quattro arresti e un locale sospeso",
        "sommario": "I Carabinieri hanno controllato 377 persone e 125 veicoli tra Don Bosco, Cinecittà e Quadraro. Le singole posizioni restano al vaglio giudiziario.",
        "categoria": "Cronaca", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Roma", "controlli Tuscolano"],
        "dati_chiave": [{"valore": "377", "etichetta": "persone controllate"}, {"valore": "125", "etichetta": "veicoli verificati"}, {"valore": "4", "etichetta": "arresti comunicati"}],
        "paragrafi": [
            "Quattro persone sono state arrestate e una denunciata durante controlli straordinari dei Carabinieri nei quartieri Don Bosco, Cinecittà, Quadraro e Tuscolano, a Roma. L'operazione ha coinvolto reparti territoriali, unità mobili e il NAS.",
            "Nel complesso sono state controllate 377 persone e 125 veicoli. Due arresti riguardano ipotesi legate alla detenzione di sostanze stupefacenti, mentre un altro deriva dall'aggravamento di una precedente misura cautelare.",
            "Tra le persone coinvolte figurano anche minorenni. Per tutelarne la riservatezza, omettiamo elementi che possano renderli identificabili e ricordiamo che ogni posizione deve essere valutata separatamente dall'autorità giudiziaria.",
            "Il NAS ha riscontrato carenze igienico-sanitarie in un'attività commerciale di via Tuscolana, che è stata sospesa. Sono state inoltre comunicate sanzioni amministrative superiori a 3 mila euro.",
            "I posti di controllo hanno prodotto contravvenzioni al codice della strada per oltre 16 mila euro. Cinque giovani sono stati segnalati alla Prefettura per il possesso di sostanze destinate, secondo gli accertamenti, a uso personale.",
            "Arresti, denunce e segnalazioni non sono equivalenti a condanne. Gli esiti definitivi dipenderanno dalle convalide, dagli accertamenti sanitari e dai procedimenti previsti per ciascun caso.",
        ],
        "fonti": [{"url": "https://www.carabinieri.it/in-vostro-aiuto/informazioni/news/2026/10/09/new0-20261009020700-1906761", "nome": "Carabinieri — bilancio dei controlli nei quartieri del quadrante sud-est di Roma."}, {"url": "https://www.grnet.it/roma-quattro-arresti-nei-quartieri-periferici-contro-le-bande-giovanili/", "nome": "GrNet — riscontro indipendente sui controlli e sulla sospensione dell'attività commerciale."}],
        "image_source": "tuscolano", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di controlli in una strada del Tuscolano senza persone visibili; non è una fotografia dell'operazione.",
        "image_prompt": "Strada del Tuscolano con pattuglie e locale chiuso, nessuna persona visibile; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "waveguard-allerta-medicane-meteotsunami-sicilia-malta-2026",
        "titolo": "Medicane e meteo-tsunami, nuove reti di allerta tra Sicilia e Malta",
        "sommario": "Il progetto WAVEGUARD potenzierà osservazioni e modelli nel Canale di Sicilia. Previste anche esercitazioni e prototipi per la gestione delle emergenze.",
        "categoria": "Ambiente", "luogo": "Canale di Sicilia", "formato": "flash",
        "parole_chiave_titolo": ["WAVEGUARD", "Canale di Sicilia"],
        "dati_chiave": [{"valore": "2", "etichetta": "Paesi coinvolti"}, {"valore": "2021-2027", "etichetta": "programma Interreg"}, {"valore": "8 ottobre", "etichetta": "presentazione pubblica"}],
        "paragrafi": [
            "Italia e Malta rafforzeranno il monitoraggio degli eventi meteo-marini estremi nel Canale di Sicilia con il progetto WAVEGUARD. ISPRA partecipa all'iniziativa finanziata dal programma europeo Interreg Italia-Malta 2021-2027.",
            "Il progetto si concentra sui Medicane, cicloni con caratteristiche simili a quelle tropicali che possono formarsi nel Mediterraneo, e sui meteo-tsunami, oscillazioni rapide del livello del mare generate da particolari condizioni atmosferiche.",
            "Saranno installate o potenziate reti osservative, sviluppati modelli idrodinamici e realizzati prototipi di allerta. L'obiettivo è fornire informazioni più tempestive a chi gestisce porti, coste ed emergenze.",
            "Il piano comprende anche esercitazioni operative in Italia e a Malta. Simulare gli scenari serve a verificare comunicazioni e tempi di risposta, ma non elimina l'incertezza delle previsioni né sostituisce gli avvisi ufficiali.",
            "ISPRA ha presentato il progetto l'8 ottobre nell'edizione siciliana di Buongiorno Regione insieme a Università di Catania e CNR. La fase pubblica accompagna attività tecniche che richiedono coordinamento transfrontaliero.",
            "Per cittadini e naviganti resta essenziale seguire Capitanerie, Protezione civile e servizi meteorologici. Le nuove reti potranno migliorare la conoscenza del rischio, ma non autorizzano a ignorare divieti o ordinanze locali.",
        ],
        "fonti": [{"url": "https://www.isprambiente.gov.it/it/news/progetto-waveguard", "nome": "ISPRA — obiettivi, reti osservative ed esercitazioni del progetto WAVEGUARD."}, {"url": "https://italiamalta.eu/waveguard/", "nome": "Programma Interreg Italia-Malta — scheda del progetto WAVEGUARD."}],
        "image_source": "waveguard",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una boa e una stazione di monitoraggio nel Canale di Sicilia; scena non documentaria.",
        "image_prompt": "Boa oceanografica e stazione costiera davanti all'Etna per monitorare il mare; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "campoli-appennino-ordigni-bellici-domiciliari-10-10-2026",
        "titolo": "Campoli Appennino, ordigni in un garage: disposti i domiciliari",
        "sommario": "La scoperta risale al principio d'incendio del 27 settembre, quando furono evacuati circa 80 residenti. Le accuse e la provenienza del materiale devono essere accertate.",
        "categoria": "Cronaca", "luogo": "Campoli Appennino", "formato": "flash",
        "parole_chiave_titolo": ["Campoli Appennino", "ordigni bellici"],
        "dati_chiave": [{"valore": "80", "etichetta": "residenti evacuati in via precauzionale"}, {"valore": "150 m", "etichetta": "raggio iniziale di sicurezza"}, {"valore": "27 settembre", "etichetta": "data del ritrovamento"}],
        "paragrafi": [
            "Il giudice ha convalidato l'arresto e disposto i domiciliari per un uomo di 55 anni nell'inchiesta sugli ordigni rinvenuti in un garage a Campoli Appennino, nel Frusinate. La misura cautelare non equivale a una condanna.",
            "La vicenda era iniziata il 27 settembre, quando un principio d'incendio aveva richiesto l'intervento dei Vigili del fuoco. Nel locale furono individuati materiali bellici e scattò una vasta operazione di messa in sicurezza.",
            "Il Comune ordinò l'evacuazione precauzionale di circa 80 residenti entro un raggio di 150 metri. Gli artificieri lavorarono alla rimozione e alla catalogazione, mentre le persone poterono rientrare dopo il cessato pericolo.",
            "Le cronache locali indicano un numero molto elevato di pezzi tra granate, bombe da mortaio, mine e altro materiale. Quantità, stato di conservazione e capacità offensiva devono essere confermati dagli accertamenti tecnici e dagli atti ufficiali.",
            "Gli investigatori dovranno chiarire provenienza, disponibilità e finalità del materiale. L'indagato ha diritto alla presunzione di innocenza e potrà contestare gli elementi raccolti nelle sedi giudiziarie.",
            "In presenza di un possibile residuato bellico non bisogna toccarlo o spostarlo. È necessario allontanarsi, impedire l'accesso all'area e chiamare immediatamente il 112 o le forze dell'ordine.",
        ],
        "fonti": [{"url": "https://www.rainews.it/tgr/lazio/articoli/2026/09/frosinone-campoli-appennino-granate-nello-scantinato-evacuate-80-persone--3015857b-b4e1-4bd0-ba83-98de406d3f62.html", "nome": "RaiNews TGR Lazio — ritrovamento, evacuazione e intervento degli artificieri."}, {"url": "https://www.ciociariaoggi.it/news/cronaca/318950/arsenale-di-ordigni-bellici-ai-domiciliari.html", "nome": "Ciociaria Oggi — aggiornamento del 10 ottobre sulla convalida e sulla misura cautelare."}],
        "image_source": "campoli", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di una strada di Campoli Appennino durante la bonifica, senza ordigni o persone visibili; non è una fotografia dell'intervento.",
        "image_prompt": "Strada di Campoli Appennino delimitata con mezzi tecnici vuoti, nessun ordigno visibile; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "piano-nazionale-ripristino-natura-bozza-commissione-ue-2026",
        "titolo": "Ripristino della natura, online la bozza del piano italiano",
        "sommario": "Il documento è stato trasmesso alla Commissione europea, che potrà formulare osservazioni nei prossimi sei mesi. La versione pubblicata non è ancora definitiva.",
        "categoria": "Ambiente", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["ripristino della natura", "piano italiano"],
        "dati_chiave": [{"valore": "6 mesi", "etichetta": "tempo per la valutazione europea"}, {"valore": "2024/1991", "etichetta": "regolamento UE di riferimento"}, {"valore": "bozza", "etichetta": "stato attuale del documento"}],
        "paragrafi": [
            "È disponibile online la bozza del Piano nazionale di ripristino della natura trasmessa dall'Italia alla Commissione europea. Il documento attua il regolamento UE 2024/1991 e descrive misure per ecosistemi degradati, biodiversità e resilienza climatica.",
            "La pubblicazione comprende il testo della bozza e una tabella di sintesi degli interventi. Rendere accessibili entrambi i documenti permette a Regioni, Comuni, imprese, agricoltori, associazioni e cittadini di conoscere il quadro proposto.",
            "La Commissione europea avrà sei mesi per esaminare il piano e potrà formulare osservazioni. Il testo oggi online non è quindi la versione finale e singole misure possono ancora essere precisate o modificate.",
            "Il ripristino non coincide soltanto con la creazione di nuove aree protette. Può comprendere recupero di zone umide, fiumi, habitat agricoli e marini, maggiore connettività ecologica e contrasto alle specie invasive.",
            "ISPRA sottolinea che l'attuazione richiederà collaborazione tra istituzioni, ricerca, territori e categorie economiche. Obiettivi e risultati dovranno essere misurabili, evitando di confondere annunci, finanziamenti e interventi effettivamente completati.",
            "Per cittadini e proprietari non scattano automaticamente nuovi obblighi dalla sola pubblicazione della bozza. Eventuali effetti concreti dipenderanno dal piano definitivo e dai successivi atti nazionali o territoriali.",
        ],
        "fonti": [{"url": "https://www.isprambiente.gov.it/it/news/online-la-bozza-del-piano-nazionale-di-ripristino-della-natura-trasmessa-alla-commissione-europea", "nome": "ISPRA — pubblicazione della bozza e iter di valutazione europea."}, {"url": "https://www.mase.gov.it/portale/piano-nazionale-di-ripristino-della-natura", "nome": "Ministero dell'Ambiente — documentazione del Piano nazionale di ripristino della natura."}],
        "image_source": "natura",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una zona umida italiana rinaturalizzata; scena non documentaria.",
        "image_prompt": "Zona umida italiana ripristinata con passerella e fauna selvatica; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
]


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "La prudenza protegge i fatti prima ancora delle persone coinvolte.",
        "Una sorveglianza efficace distingue i segnali dai falsi allarmi.",
        "La giustizia richiede tempo, prove e rispetto per ogni posizione.",
        "La salute dei più giovani cresce con ascolto, sostegno e niente stigma.",
        "Raccontare un'indagine significa separare sempre accuse e responsabilità accertate.",
        "Ogni osservazione accurata può diventare una tessera della conoscenza scientifica.",
        "La sicurezza pubblica funziona quando controlli e diritti avanzano insieme.",
        "Conoscere il mare aiuta a prepararsi prima che il rischio diventi emergenza.",
        "Davanti a un residuato bellico, la distanza è la prima forma di protezione.",
        "Ripristinare un ecosistema significa restituire spazio anche al futuro.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    append_name_phrases()
    base_time = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 8, 20, 35, 51, 68, 86, 105, 123, 142)
    images, written = [], []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = base.make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base_time - timedelta(minutes=minutes)
        base.set_published(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"cronaca-salute-ambiente-v{VERSION}", "date": base_time.date().isoformat(),
        "release_date": base_time.date().isoformat(), "updated_at": base_time.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base_time.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
