#!/usr/bin/env python3
"""Pacchetto editoriale quotidiano CurioMondo del 23 settembre 2026."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json

from lxml import etree

import build_v501_daily as shared
from daily_question_auto import (
    render_book_page,
    render_question_page,
    update_archive,
    update_feed,
    update_home,
    update_search,
    update_sitemap,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = 521
DATE = "2026-09-23"
DATE_LABEL = "23 settembre 2026"
QUESTION_NUMBER = 1007
QUESTION = "Quale parte della tua identità esisterebbe ancora se nessuno ricordasse il tuo passato?"
SLUG = "quale-parte-della-tua-identita-esisterebbe-ancora-se-nessuno-ricordasse-il-tuo-passato"
QUESTION_URL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"

shared.VERSION = VERSION
shared.DATE = DATE
shared.DATE_LABEL = DATE_LABEL


PACKAGE = {
    "excerpt": "Una riflessione su ciò che resta di noi quando vengono meno ricordi condivisi, reputazione e racconti: valori, scelte presenti e capacità di ricominciare.",
    "answer_paragraphs": [
        "Una parte della nostra identità vive nella memoria degli altri. I racconti di famiglia, le amicizie, il lavoro svolto e perfino gli errori ricordati costruiscono un’immagine che ci precede. Sapere che qualcuno conosce il nostro passato ci dà continuità: non dobbiamo spiegare ogni volta da dove veniamo e perché certe cose hanno peso.",
        "Se nessuno ricordasse quel passato, però, non scompariremmo completamente. Resterebbero abitudini, sensibilità, competenze e paure depositate nel modo in cui reagiamo. Il passato non è soltanto una storia raccontata; è diventato postura, attenzione, desiderio e limite. Anche senza testimoni, molte tracce continuerebbero a orientare il presente.",
        "Resterebbe soprattutto la possibilità di scegliere. Non potremmo più affidarci alla reputazione per dimostrare chi siamo, né usare un vecchio errore come condanna definitiva. Ogni gesto avrebbe un peso nuovo, perché l’identità dovrebbe mostrarsi nel modo in cui trattiamo le persone adesso. Sarebbe una perdita, ma anche una forma radicale di libertà.",
        "Non tutto ciò che gli altri ricordano coincide con noi. A volte una famiglia conserva la versione più fragile di una persona, un gruppo quella più rumorosa, un ambiente professionale soltanto i risultati. Senza quegli sguardi potremmo scoprire parti rimaste invisibili. Ma perderemmo anche chi custodisce trasformazioni che da soli tendiamo a dimenticare.",
        "Forse l’identità non è né un archivio immutabile né una pagina bianca. È il dialogo tra ciò che ci ha formati e ciò che continuiamo a fare quando nessuno ci conferma. I ricordi danno profondità, ma le scelte presenti impediscono che il passato diventi l’unica definizione possibile.",
        "La domanda allora non chiede di cancellare la storia, ma di distinguere ciò che dipende dal pubblico che la ricorda. Se nessuno potesse confermare i tuoi successi, le tue ferite o il ruolo che hai avuto, quale valore continueresti a praticare oggi? Probabilmente quella scelta, ripetuta senza testimoni, è una delle parti più solide della tua identità.",
    ],
    "book_title": "Chi resta quando il passato non ha testimoni",
    "book_deck": "Un percorso tra memoria, reputazione, corpo, valori e trasformazione per capire quanto della nostra identità viene ricordato e quanto viene scelto ogni giorno.",
    "book_pages": [
        {
            "title": "L’identità come storia condivisa",
            "paragraphs": [
                "Impariamo molto presto chi siamo attraverso le parole degli altri. Un bambino sente raccontare di essere coraggioso, timido, ordinato o difficile prima di poter valutare quelle definizioni. Le storie familiari danno continuità e appartenenza, ma selezionano alcuni episodi e ne trascurano altri. Crescendo possiamo riconoscerci in quel racconto, opporci oppure continuare a interpretarlo senza accorgercene. La memoria condivisa non è un semplice archivio: è uno dei luoghi in cui l’identità prende forma.",
                "Anche le amicizie custodiscono versioni di noi che non sapremmo ricostruire da soli. Ricordano il tono di una promessa, un periodo di entusiasmo, una paura superata o una scelta che allora sembrava piccola. Quei testimoni collegano persone molto diverse che abbiamo abitato nel tempo. Quando li incontriamo, possiamo sentirci compresi oppure intrappolati, perché il loro ricordo non sempre coincide con ciò che siamo diventati.",
                "Il lavoro e la vita pubblica aggiungono un’altra memoria: risultati, errori, affidabilità, ruoli. La reputazione riduce l’incertezza e permette agli altri di decidere se fidarsi. Tuttavia tende a semplificare. Una promozione può diventare la prova che siamo ambiziosi; un fallimento la definizione di un limite. Se nessuno ricordasse il passato, perderemmo una parte del credito conquistato, ma anche alcune etichette che continuano a precederci.",
                "Immaginare l’assenza di testimoni fa emergere quanto dipendiamo dalla conferma. Molti gesti non cercano soltanto un risultato: cercano qualcuno che possa dire che siamo stati generosi, capaci, feriti o presenti. Non è necessariamente vanità. L’essere umano ha bisogno che la propria esperienza venga riconosciuta. Il rischio nasce quando ciò che non viene visto sembra privo di valore e smettiamo di sapere chi siamo senza uno sguardo esterno.",
                "La domanda non invita a svalutare la memoria degli altri. Mostra piuttosto che nessun testimone possiede l’intera storia. La nostra identità è distribuita tra ricordi differenti, spesso contraddittori. Sapere questo permette di ricevere un racconto senza consegnargli tutto il potere. Possiamo ringraziare chi conserva una parte del nostro passato e, nello stesso tempo, mantenere aperta la possibilità di diventare qualcuno che quel passato non aveva ancora previsto.",
            ],
        },
        {
            "title": "Ciò che il corpo continua a ricordare",
            "paragraphs": [
                "Anche se ogni persona dimenticasse il nostro passato, il corpo non tornerebbe neutro. Conserva abilità apprese, ritmi, allarmi e forme di sollievo. Una mano sa compiere un lavoro ripetuto; il respiro cambia davanti a un tono associato al pericolo; una musica riporta una calma che non sappiamo spiegare. Queste memorie non raccontano una biografia completa, ma mostrano che la storia continua a vivere anche quando non viene pronunciata.",
                "Le abitudini sono una forma quotidiana di memoria. Il modo in cui ordiniamo uno spazio, chiediamo aiuto o affrontiamo un imprevisto nasce da migliaia di esperienze ormai invisibili. Alcune abitudini sostengono la vita; altre ripetono una protezione che non serve più. Se nessuno conoscesse la loro origine, resterebbe comunque la possibilità di osservarne gli effetti e decidere se conservarle, modificarle o lasciarle andare.",
                "Anche le competenze sopravviverebbero alla perdita del racconto. Sapremmo leggere, guidare, cucinare, ascoltare o risolvere un problema pur senza poter esibire il percorso che ci ha portati fin lì. Questo distingue ciò che siamo capaci di fare dalla reputazione che lo certifica. I titoli e le testimonianze facilitano la fiducia sociale, ma la capacità reale torna visibile quando deve essere esercitata nel presente.",
                "Le ferite possono restare come attese automatiche. Una persona dimenticata dagli altri potrebbe continuare a temere l’abbandono, evitare un conflitto o prepararsi a una critica. Senza la storia condivisa, questi riflessi sembrerebbero più misteriosi. Non per questo sarebbero falsi. Comprenderli richiederebbe attenzione ai segnali attuali, senza inventare una spiegazione e senza trattare ogni reazione come un destino.",
                "Il corpo ricorda, ma non decide da solo chi dobbiamo essere. Una risposta appresa può essere riconosciuta e allenata diversamente. La memoria implicita offre informazioni, non ordini. L’identità più viva nasce quando ascoltiamo ciò che la storia ha lasciato dentro di noi e lo sottoponiamo alla realtà presente: questa protezione serve ancora, questa abilità merita spazio, questo automatismo può finalmente rallentare.",
            ],
        },
        {
            "title": "Reputazione, ruolo e sguardo degli altri",
            "paragraphs": [
                "Ogni ambiente ci assegna un ruolo. In una famiglia possiamo essere quello responsabile, in un gruppo quello ironico, al lavoro quello che risolve le emergenze. I ruoli semplificano la convivenza, ma diventano stretti quando gli altri accettano soltanto la parte di noi che conoscono. Se il passato non fosse ricordato, quei contratti impliciti perderebbero forza e dovremmo presentarci senza la protezione di una funzione già riconosciuta.",
                "La reputazione è utile perché nessuna relazione può ricominciare da zero ogni mattina. Permette di affidare un compito, confidare un segreto o prevedere una risposta. Tuttavia può confondere continuità e immobilità. Una persona considerata affidabile può attraversare una crisi; chi ha sbagliato può diventare più attento. Ricordare bene qualcuno significa conservare i fatti senza negargli il diritto di produrne di nuovi.",
                "Perdere ogni reputazione avrebbe un costo concreto. I meriti non aprirebbero più porte, le scuse già accettate non offrirebbero contesto, gli anni di cura non sarebbero conosciuti. Dovremmo dimostrare di nuovo qualità che oggi vengono date per acquisite. Questa immagine mostra perché essere ricordati è una forma di patrimonio relazionale e perché cancellare la storia di una persona può essere una forma di ingiustizia.",
                "Eppure l’assenza di reputazione toglierebbe anche alcuni alibi. Non potremmo usare il bene compiuto ieri per evitare una responsabilità attuale, né aspettarci fiducia soltanto perché un tempo l’abbiamo meritata. Le scelte avrebbero bisogno di coerenza presente. L’identità smetterebbe di essere un saldo accumulato e tornerebbe a mostrarsi nel modo in cui rispondiamo alla situazione davanti a noi.",
                "La libertà non consiste nel vivere come se lo sguardo degli altri non esistesse. Consiste nel non dipendere interamente da una versione pubblica. Possiamo curare la reputazione perché rende possibili relazioni e progetti, senza scambiarla per il nostro valore completo. Quando il ruolo cambia o il pubblico scompare, resta la domanda più semplice: quale comportamento considero giusto anche se nessuno lo collegherà al mio nome?",
            ],
        },
        {
            "title": "I valori che esistono senza pubblico",
            "paragraphs": [
                "Un valore diventa parte dell’identità quando orienta una scelta anche senza premio. Dire la verità soltanto quando protegge la reputazione è strategia; dirla con misura quando nessuno potrebbe scoprire la menzogna rivela un criterio più profondo. Questo non significa che dobbiamo agire senza considerare le conseguenze. Significa osservare quali principi continuano a contare quando viene meno la possibilità di essere riconosciuti.",
                "Molte qualità hanno bisogno di un contesto per diventare visibili. La generosità richiede qualcuno a cui offrire, il coraggio un rischio, la pazienza un’attesa. Se nessuno ricordasse il passato, queste qualità non sparirebbero, ma dovrebbero esprimersi di nuovo. Non sono oggetti conservati una volta per sempre. Sono disposizioni che diventano identità attraverso gesti ripetuti in circostanze diverse.",
                "Anche le contraddizioni fanno parte di questo processo. Possiamo considerare importante la lealtà e scoprire di averla sacrificata per paura. L’identità non coincide né con il valore dichiarato né con un singolo errore. Si costruisce nella distanza tra ciò che desideriamo praticare e ciò che riusciamo a fare, soprattutto nel modo in cui affrontiamo quella distanza senza nasconderla.",
                "Immaginare una vita senza testimoni aiuta a distinguere desiderio e immagine. Alcuni obiettivi perderebbero significato se nessuno potesse ammirarli; altri resterebbero vivi perché corrispondono a una curiosità, una cura o una forma di servizio. Non occorre disprezzare l’ambizione pubblica. È sufficiente capire quale parte dipende esclusivamente dall’applauso e quale continuerebbe a dare senso alle giornate in sua assenza.",
                "Un esercizio concreto consiste nello scegliere un gesto non destinato a essere raccontato: mantenere una promessa privata, riparare un errore senza annunciarlo, dedicare attenzione a un compito invisibile. Il valore di quel gesto non aumenta perché resta segreto, ma il segreto riduce il rumore della conferma. Permette di sentire se ciò che facciamo appartiene davvero al modo in cui vogliamo abitare il presente.",
            ],
        },
        {
            "title": "Quando il passato diventa una prigione",
            "paragraphs": [
                "La continuità è rassicurante, ma può trasformarsi in una sentenza. Una frase ripetuta per anni — «sono sempre stato così» — usa il passato come prova che il cambiamento sarebbe falso. In realtà ogni identità stabile contiene trasformazioni. Restiamo riconoscibili non perché ripetiamo tutto, ma perché integriamo esperienze nuove in una storia che continua ad avere un filo.",
                "Anche gli altri possono difendere la nostra vecchia versione. Un cambiamento modifica equilibri: chi era sempre disponibile comincia a porre limiti, chi evitava il conflitto prende parola, chi cercava approvazione sceglie un percorso meno comprensibile. La resistenza del gruppo non dimostra che la trasformazione sia sbagliata. Mostra soltanto che l’identità personale è legata a relazioni che devono riorganizzarsi.",
                "Alcuni errori diventano identità perché vengono ricordati più delle riparazioni. È giusto non cancellarne le conseguenze, ma è altrettanto importante distinguere responsabilità e condanna permanente. Una persona può dover rispondere di ciò che ha fatto e, nello stesso tempo, costruire comportamenti diversi. Se nessuno ricordasse il passato, sparirebbe il marchio; resterebbe però il compito di non ripetere il danno.",
                "Anche il successo può imprigionare. Essere stati brillanti, forti o indispensabili crea l’aspettativa di continuare a esserlo. Quando la vita cambia, si può difendere un’immagine ormai costosa pur di non deludere chi la ricorda. Lasciare un ruolo non significa negare ciò che abbiamo realizzato. Significa riconoscere che la fedeltà alla propria storia non richiede di ripeterne per sempre la stessa forma.",
                "Liberarsi dal passato non vuol dire dichiararlo irrilevante. Vuol dire sottrargli il monopolio sul futuro. Possiamo conservare gratitudine, rimorso e competenze senza trasformarli in istruzioni complete. La domanda utile diventa: se nessuno si aspettasse da me la vecchia risposta, quale risposta considererei oggi più onesta? Quello spazio tra attesa e scelta è spesso il luogo in cui l’identità torna a respirare.",
            ],
        },
        {
            "title": "La perdita dei testimoni e il bisogno di lutto",
            "paragraphs": [
                "Quando scompare una persona che ci conosceva da molto tempo, non perdiamo soltanto la sua presenza. Perdiamo anche un archivio vivente di parole, gesti e versioni di noi. Alcuni ricordi esistevano soltanto nella relazione. Il lutto può includere la sensazione che una parte della nostra storia non abbia più un luogo in cui essere confermata. Questo dolore mostra quanto l’identità sia anche un bene condiviso.",
                "Possiamo cercare di conservare tutto attraverso fotografie, messaggi e racconti. Questi oggetti aiutano, ma non sostituiscono lo sguardo capace di collegare un episodio al nostro modo di essere. La memoria digitale moltiplica le tracce e, nello stesso tempo, non garantisce comprensione. Un’immagine dice che eravamo presenti; raramente racconta che cosa quella giornata ha cambiato e perché continuava a essere ricordata.",
                "Accettare la perdita dei testimoni richiede di diventare, almeno in parte, custodi della propria storia. Scrivere, ordinare fotografie, registrare un racconto familiare o condividere un episodio con qualcuno più giovane può dare continuità. Non si tratta di costruire un monumento a se stessi, ma di scegliere quali esperienze meritano di essere trasmesse e quali possono restare private senza per questo perdere valore.",
                "Esiste anche il diritto di lasciare andare. Non ogni dettaglio deve essere salvato e non ogni fase della vita deve continuare a essere accessibile. Dimenticare è una funzione umana che alleggerisce, seleziona e permette di aggiornare l’immagine di sé. Una memoria completa sarebbe forse insopportabile. L’identità ha bisogno sia di radici sia di spazi vuoti in cui qualcosa di nuovo possa accadere.",
                "Quando nessuno può più ricordare con noi, restano gli effetti delle relazioni vissute. Una frase ricevuta continua a orientare una scelta, un esempio diventa criterio, un affetto modifica il modo in cui offriamo presenza. Il testimone non c’è, ma ciò che ha reso possibile passa attraverso di noi. In questo senso una parte del passato sopravvive non come racconto esatto, bensì come qualità della vita presente.",
            ],
        },
        {
            "title": "Ricominciare senza diventare una pagina bianca",
            "paragraphs": [
                "L’idea di ricominciare da zero è seducente perché promette libertà dalle aspettative. Cambiare città, lavoro o ambiente può davvero aprire possibilità. Tuttavia portiamo con noi abitudini, desideri e paure. Una pagina completamente bianca non esiste. Il nuovo inizio più onesto non cancella ciò che è stato: crea condizioni in cui possiamo rispondere diversamente quando vecchi schemi tornano a presentarsi.",
                "Un ambiente che non conosce il passato può offrire uno sguardo meno rigido. Nessuno presume che eviteremo una responsabilità o che saremo sempre disponibili. Questa neutralità permette esperimenti, ma richiede anche attenzione. Senza persone capaci di ricordarci i nostri schemi, possiamo ripeterli attribuendo ogni difficoltà alle circostanze. La libertà aumenta quando portiamo con noi una consapevolezza, non quando fingiamo di non avere storia.",
                "Raccontarsi a qualcuno di nuovo è una scelta graduale. Non dobbiamo consegnare subito l’intera biografia per essere autentici, né inventare una versione più conveniente. Possiamo condividere ciò che serve alla relazione presente e lasciare che la fiducia cresca. L’identità non viene dimostrata dalla quantità di confessioni, ma dalla coerenza tra ciò che diciamo, ciò che facciamo e i confini che sappiamo rispettare.",
                "Ricominciare può significare anche cambiare interpretazione senza cambiare luogo. Lo stesso passato può essere letto come prova di incapacità oppure come descrizione di strategie usate allora con le risorse disponibili. Una lettura più gentile non falsifica le responsabilità. Le colloca in un quadro che permette apprendimento. Quando la storia smette di essere un’accusa continua, diventa materiale con cui scegliere.",
                "La domanda più utile non è «chi sarei senza passato?», perché nessuno può separarsi completamente da ciò che lo ha formato. Possiamo chiederci invece quale parte della storia merita continuità e quale chiede una conclusione. Il nuovo inizio nasce da questa selezione: portare con sé valori, affetti e competenze, lasciando meno spazio alle etichette che impediscono di vedere ciò che sta già cambiando.",
            ],
        },
        {
            "title": "Un’identità verificata nel presente",
            "paragraphs": [
                "Se nessuno ricordasse il nostro passato, l’identità avrebbe bisogno di diventare visibile nel presente. Non potremmo indicare una vecchia azione per dimostrare di essere generosi, né un antico torto per spiegare ogni paura. Dovremmo osservare ciò che facciamo oggi. Questo criterio può sembrare severo, ma contiene una possibilità: nessuna reputazione positiva o negativa sarebbe sufficiente a sostituire la scelta attuale.",
                "Il presente non cancella la continuità. Una decisione assume significato anche perché incontra abitudini, promesse e conseguenze accumulate. Tuttavia è l’unico luogo in cui possiamo intervenire. Possiamo riconoscere un tratto ricevuto dalla famiglia e decidere come esprimerlo; custodire una memoria senza obbedirle; accettare che qualcuno ci ricordi diversamente senza dover vincere una disputa sulla versione definitiva di noi.",
                "L’identità più resistente non è quella che non cambia. È quella che sa attraversare i cambiamenti senza perdere ogni orientamento. Può abbandonare un ruolo e conservare un valore, cambiare opinione senza rinnegare la ricerca di verità, chiudere una relazione senza dichiarare inutile tutto ciò che ha insegnato. La coerenza profonda riguarda il modo in cui integriamo, non la ripetizione immobile.",
                "Possiamo allora usare i ricordi come testimonianze e non come verdetti. Ci aiutano a vedere schemi, capacità e debiti; non stabiliscono da soli che cosa saremo. Anche lo sguardo degli altri può essere accolto come informazione parziale. Chi ci ama può ricordarci una forza dimenticata, ma non deve impedire che la nostra forma cambi. Chi ci critica può indicare un effetto reale, ma non possiede l’intera definizione.",
                "Alla fine resterebbe la capacità di rispondere al presente con ciò che abbiamo imparato. Forse questa è la parte dell’identità che non dipende interamente dai testimoni: il modo in cui trasformiamo memoria, corpo e valori in una scelta concreta. Oggi, senza raccontare chi sei stato e senza promettere chi sarai, quale gesto farebbe riconoscere la persona che desideri essere adesso?",
            ],
        },
    ],
}


GUIDES = [
    {
        "topic": "Come creare PDF",
        "slug": "come-creare-pdf",
        "title": "Come creare un PDF da computer e smartphone",
        "deck": "Metodi integrati per trasformare documenti, foto e pagine web in PDF, ordinare le pagine e controllare il risultato prima di inviarlo.",
        "sections": [
            ("Scegliere il metodo corretto", [
                "Un PDF conserva impaginazione e contenuto in modo più stabile di un file modificabile, ma il risultato dipende dalla sorgente. Se parti da Word, Pages o Google Documenti usa Esporta o Scarica come PDF: testo, link e struttura restano più leggibili. La stampa virtuale è utile quando un’app non offre l’esportazione. Fotografare lo schermo o convertire tutto in immagini produce invece file pesanti e testo non selezionabile, quindi va evitato quando esiste un metodo diretto.",
                "Prima della conversione controlla formato pagina, margini, orientamento e interruzioni. Un documento che appare corretto sullo schermo può creare pagine vuote o tagliare una tabella in fase di esportazione. Usa l’anteprima di stampa e assegna un nome comprensibile, senza dati sensibili inutili. Se il file deve essere firmato, compilato o accessibile con lettori vocali, verifica che il programma mantenga campi e struttura anziché produrre una semplice fotografia.",
            ]),
            ("Windows e Mac", [
                "In Windows molte applicazioni includono Microsoft Print to PDF. Apri Stampa, scegli quella stampante virtuale, controlla pagine e orientamento, quindi salva. Nei programmi Office è preferibile File, Esporta, Crea PDF/XPS oppure Salva con nome PDF, perché offre opzioni per qualità e accessibilità. Per immagini multiple selezionale in Esplora file, usa Stampa e scegli PDF, ma verifica l’ordine alfabetico dei nomi prima di confermare.",
                "Su Mac usa File, Stampa e il menu PDF nella parte inferiore della finestra per salvare. Anteprima consente di unire documenti trascinando le miniature nella barra laterale, riordinare le pagine e ruotarle. Dopo ogni modifica scegli Esporta come PDF per creare una copia nuova, così l’originale resta disponibile. Quando riduci la dimensione con un filtro Quartz controlla fotografie e testi piccoli: la compressione automatica può essere troppo aggressiva.",
            ]),
            ("Android, iPhone e scansioni", [
                "Su Android apri il documento o la pagina nell’app compatibile, scegli Condividi o Stampa, poi Salva come PDF. Per fogli cartacei usa la funzione scansione di Google Drive o l’app del produttore: appoggia il documento su una superficie uniforme, usa luce diffusa e inquadra tutti i bordi. Correggi ritaglio e rotazione prima di aggiungere la pagina successiva. Non affidarti soltanto al riconoscimento automatico se numeri e nomi devono essere esatti.",
                "Su iPhone e iPad puoi creare PDF da Note tramite Scansiona documenti, oppure da una schermata di stampa aprendo l’anteprima con il gesto di ingrandimento e poi usando Condividi, Salva su File. Nell’app File alcune versioni permettono di creare un PDF da immagini selezionate. Ordina prima le foto e controlla l’orientamento. Per documenti d’identità o sanitari evita servizi di conversione casuali: usa strumenti integrati e conserva il file in una posizione protetta.",
            ]),
            ("Controlli prima dell’invio", [
                "Apri il PDF appena creato con un lettore diverso dal programma usato per esportarlo. Verifica tutte le pagine, cerca una parola per accertarti che il testo sia selezionabile, prova i link e ingrandisci firme o tabelle. Controlla le proprietà del documento: autore, titolo e altri metadati possono rivelare informazioni non destinate al destinatario. Se serve una versione finale non modificabile, ricorda che un PDF non garantisce da solo autenticità o protezione assoluta.",
                "Per ridurre il peso preferisci l’opzione Ottimizza o Dimensione minima del programma originale. Conserva una copia ad alta qualità prima della compressione. Se devi proteggere il file con password, usa un’app affidabile e comunica la password su un canale diverso; non perdere la chiave, perché il recupero può essere impossibile. Per firme con valore legale usa i servizi previsti, come firma digitale qualificata o piattaforme riconosciute, non una semplice immagine della firma.",
            ]),
        ],
    },
    {
        "topic": "Come comprimere file / foto",
        "slug": "come-comprimere-file-foto",
        "title": "Come comprimere file e foto senza perdere qualità inutilmente",
        "deck": "ZIP, immagini ridimensionate e formati moderni: come ridurre lo spazio, scegliere la qualità e inviare allegati in modo sicuro.",
        "sections": [
            ("Capire che cosa si può ridurre", [
                "Comprimere può significare due operazioni diverse. Creare un archivio ZIP raggruppa file e riduce soprattutto documenti testuali, fogli di calcolo e dati ripetitivi; fotografie JPEG, video MP4 e PDF già ottimizzati spesso cambiano poco. Ridimensionare o ricodificare una foto, invece, elimina informazioni e può ridurre molto il peso. Prima di procedere decidi se devi soltanto riunire più elementi o se puoi accettare una copia più leggera dell’originale.",
                "Conserva sempre gli originali quando le immagini hanno valore personale, professionale o documentale. Lavora su una copia in una cartella separata e assegna nomi che distinguano la versione compressa. La qualità visiva dipende da risoluzione, formato e livello di compressione. Per una condivisione sullo schermo spesso bastano dimensioni inferiori; per stampa, ritaglio futuro o archiviazione serve mantenere più dettaglio.",
            ]),
            ("Creare ZIP su computer e telefono", [
                "In Windows seleziona file o cartelle, usa il menu contestuale e scegli Comprimi in file ZIP. Su macOS seleziona gli elementi e scegli Comprimi. Il sistema crea un archivio che può essere inviato e aperto senza software speciale. Evita di includere cartelle di sistema o percorsi molto profondi. Dopo la creazione apri lo ZIP e controlla che contenga tutti gli elementi previsti prima di eliminare o spostare gli originali.",
                "Su Android l’app File del produttore o Files di Google permette normalmente di selezionare elementi e scegliere Comprimi. Su iPhone e iPad apri File, seleziona gli elementi e usa Comprimi dal menu. Se l’opzione non appare, verifica che i file siano stati scaricati dal cloud. Le app esterne che promettono compressioni eccezionali possono chiedere accesso completo ai documenti: usale soltanto se necessarie e provenienti dallo store ufficiale.",
            ]),
            ("Ridurre fotografie in modo controllato", [
                "Per inviare foto via email o pubblicarle sul web, riduci prima le dimensioni in pixel. Un’immagine da dodici megapixel è spesso eccessiva per la visualizzazione su telefono. Esporta una copia con lato lungo tra 1600 e 2400 pixel quando il destinatario non deve stampare in grande formato. Scegli una qualità JPEG intorno all’80–85 per fotografie comuni e osserva il risultato al cento per cento, soprattutto su volti, testo e zone con dettagli fini.",
                "PNG è adatto a grafica, schermate e immagini con trasparenza, ma può essere pesante per le fotografie. JPEG offre ampia compatibilità; WebP e AVIF possono ridurre di più, ma vanno scelti soltanto se il destinatario o la piattaforma li supporta. Convertire più volte un JPEG peggiora progressivamente la qualità. Parti sempre dall’originale e crea ogni versione finale con una sola esportazione.",
                "Le funzioni Foto di Windows, Anteprima su Mac e molte gallerie mobili permettono ridimensionamento o esportazione. Evita siti online quando le immagini contengono documenti, minori, dati sanitari o informazioni private: il caricamento trasferisce una copia a un servizio esterno. Per contenuti sensibili usa strumenti locali. Prima dell’invio controlla anche i metadati di posizione e rimuovili se non sono necessari.",
            ]),
            ("Scegliere il compromesso e verificare", [
                "Parti dal limite reale: dimensione massima dell’allegato, spazio disponibile o requisiti della piattaforma. Non comprimere più del necessario. Se un PDF contiene molte fotografie, usa la funzione di ottimizzazione del programma che lo ha creato; inserirlo in uno ZIP potrebbe non produrre alcun vantaggio. Per video e audio servono strumenti specifici e tempi maggiori, perché quei formati sono già compressi.",
                "Confronta la copia ridotta con l’originale a dimensione normale e con un ingrandimento moderato. Verifica che testi, bordi e colori importanti restino leggibili. Controlla anche il peso totale dell’archivio e prova ad aprirlo su un secondo dispositivo. Se devi inviare molti file, un collegamento cloud con permessi limitati può essere più pratico di una compressione estrema; imposta scadenza e accesso soltanto alle persone necessarie.",
                "Non usare la password di uno ZIP come unica misura di sicurezza senza conoscere il metodo di cifratura. Gli strumenti integrati possono offrire protezioni limitate o nessuna password. Per dati riservati scegli un archiviatore affidabile con cifratura AES e una password lunga, poi comunicala separatamente. Conserva una copia verificata prima di cancellare i file sciolti: un archivio corrotto o una password dimenticata può rendere irrecuperabile l’intero gruppo.",
            ]),
        ],
    },
]


def add_feed_entries(entries: list[tuple[str, str, str]]) -> None:
    path = ROOT / "feed.xml"
    tree = etree.parse(str(path))
    channel = tree.getroot().find("channel")
    if channel is None:
        raise SystemExit("channel RSS assente")
    urls = {f"https://curiomondo.it{url}" for _, url, _ in entries}
    for item in list(channel.findall("item")):
        if item.findtext("link") in urls:
            channel.remove(item)
    insertion = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    stamp = datetime(2026, 9, 23, 0, 1, tzinfo=ZoneInfo("Europe/Rome"))
    for title, url, description in entries:
        node = etree.Element("item")
        full = f"https://curiomondo.it{url}"
        for tag, value in (
            ("title", title),
            ("link", full),
            ("guid", full),
            ("pubDate", format_datetime(stamp)),
            ("description", description),
        ):
            child = etree.SubElement(node, tag)
            child.text = value
        channel.insert(insertion, node)
        insertion += 1
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def validate() -> dict:
    answer = len(" ".join(PACKAGE["answer_paragraphs"]))
    ebook = len(" ".join(p for page in PACKAGE["book_pages"] for p in page["paragraphs"]))
    guides = {
        guide["slug"]: len(" ".join(p for _, paragraphs in guide["sections"] for p in paragraphs))
        for guide in GUIDES
    }
    if not 1000 <= answer <= 3000:
        raise SystemExit(f"risposta fuori soglia: {answer}")
    if not 15000 <= ebook <= 30000:
        raise SystemExit(f"eBook fuori soglia: {ebook}")
    if not 8 <= len(PACKAGE["book_pages"]) <= 14:
        raise SystemExit("numero pagine eBook non conforme")
    for slug, chars in guides.items():
        if not 3000 <= chars <= 15000:
            raise SystemExit(f"guida fuori soglia {slug}: {chars}")
    return {"answer": answer, "ebook": ebook, "guides": guides}


def main() -> None:
    lengths = validate()
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    daily = manifest["daily_state"]
    if daily.get("last_question_date", "") >= DATE:
        print(json.dumps({"status": "noop", "date": DATE}, ensure_ascii=False))
        return
    used = set(daily.get("used_question_source_numbers", []))
    source = json.loads((ROOT / "automation/state/daily-questions.json").read_text(encoding="utf-8"))
    expected = next((item for item in source if item.get("number") not in used), None)
    if not expected or expected.get("number") != QUESTION_NUMBER or expected.get("question") != QUESTION:
        raise SystemExit("domanda diversa dalla prossima voce canonica non usata")

    dt = datetime(2026, 9, 23, 0, 1, tzinfo=ZoneInfo("Europe/Rome"))
    shared.write(ROOT / "domanda-del-giorno" / SLUG / "index.html", render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL))
    shared.write(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi" / SLUG / "index.html", render_book_page(QUESTION_URL, BOOK_URL, PACKAGE))
    update_home(SLUG, dt, DATE_LABEL)
    update_archive(QUESTION, PACKAGE, SLUG, DATE_LABEL)
    update_search(QUESTION, PACKAGE, QUESTION_URL, BOOK_URL)
    update_sitemap(DATE, QUESTION_URL, BOOK_URL)
    update_feed(dt, QUESTION, PACKAGE, QUESTION_URL)

    shared.prepend_card(
        ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html",
        "cb-subgrid",
        f'<a class="cb-subcard" href="{BOOK_URL}"><span class="cb-kicker">{DATE_LABEL} · eBook</span><h2>{escape(PACKAGE["book_title"])}</h2><p>{escape(PACKAGE["book_deck"])}</p><b>Sfoglia →</b></a>',
        BOOK_URL,
    )

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    category_path = ROOT / "biblioteca/tecnologia-ai/smartphone-computer/index.html"
    for guide in reversed(GUIDES):
        url = f'/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/'
        shared.write(ROOT / url.strip("/") / "index.html", shared.guide_html(guide))
        shared.prepend_card(
            category_path,
            "cb-manual-grid",
            f'<a class="cb-subcard" href="{url}"><span class="cb-kicker">Nuova guida · {DATE_LABEL}</span><h2>{escape(guide["title"])}</h2><p>{escape(guide["deck"])}</p><b>Leggi la guida →</b></a>',
            url,
        )
        search["items"] = [item for item in search.get("items", []) if item.get("url") != url]
        search["items"].insert(0, {
            "title": guide["title"],
            "excerpt": guide["deck"],
            "url": url,
            "section": "Biblioteca / Tecnologia e informatica",
        })
        shared.add_sitemap_url(url)
    search["version"] = VERSION
    shared.dump(search_path, search)

    entries = [
        (QUESTION, QUESTION_URL, PACKAGE["excerpt"]),
        (PACKAGE["book_title"], BOOK_URL, PACKAGE["book_deck"]),
    ] + [
        (guide["title"], f'/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/', guide["deck"])
        for guide in GUIDES
    ]
    add_feed_entries(entries)

    queue_path = ROOT / "automation/state/guide-topics.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    category = next(item for item in queue["categories"] if item["category"] == "Tecnologia e informatica")
    for guide in GUIDES:
        if guide["topic"] not in category["remaining_topics"]:
            raise SystemExit(f"tema guida canonico non disponibile: {guide['topic']}")
        category["remaining_topics"].remove(guide["topic"])
        if guide["topic"] not in category["published_from_queue"]:
            category["published_from_queue"].append(guide["topic"])
    queue["version"] = int(queue.get("version", 5)) + 1
    shared.dump(queue_path, queue)

    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    daily.update({
        "current_question_source_number": QUESTION_NUMBER,
        "last_question_date": DATE,
        "last_question_slug": SLUG,
        "last_daily_guides": [guide["slug"] for guide in GUIDES],
        "last_daily_package_date": DATE,
    })
    daily.setdefault("used_question_source_numbers", []).append(QUESTION_NUMBER)
    daily.pop("current_question_owner_override", None)
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "daily-editorial-package",
        "news_added": [],
        "news_updated": [],
        "daily_question_added": SLUG,
        "ebook_added": SLUG,
        "guides_added": [guide["slug"] for guide in GUIDES],
        "change": "Domanda del giorno n. 1007, eBook collegato e due guide Biblioteca",
    }
    shared.dump(manifest_path, manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": DATE,
            "release_date": DATE,
            "last_daily_question_date": DATE,
            "last_update": "daily-package-v521",
        })
        shared.dump(path, state)

    shared.write(ROOT / "RELEASE-NOTES-v521.md", f'''# CurioMondo v521 — {DATE_LABEL}

- Pubblicata la Domanda del giorno “{QUESTION}”.
- Pubblicato l’eBook collegato “{PACKAGE["book_title"]}”.
- Pubblicate due guide dalla coda canonica: creazione PDF e compressione di file/foto.
- Aggiornati homepage, archivi, ricerca, feed, sitemap, manifest e stati di rilascio.
- Nessuna notizia modificata.
''')
    print(json.dumps({
        "status": "ok",
        "version": VERSION,
        "question_number": QUESTION_NUMBER,
        "slug": SLUG,
        "lengths": lengths,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
