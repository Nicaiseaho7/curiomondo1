"""Contenuti del pacchetto quotidiano CurioMondo v642."""

import re


ANSWER = [
    "Una vita piena non si lascia misurare con un solo contatore. Le esperienze allargano l’orizzonte: incontrare persone, attraversare luoghi, imparare, rischiare e cambiare ci espone a possibilità che altrimenti resterebbero invisibili. Ma la quantità, da sola, non garantisce profondità. Possiamo accumulare eventi come fotografie mai riguardate, passando rapidamente da un momento al successivo senza concedere a nessuno il tempo di trasformarci.",
    "L’attenzione compie il movimento opposto: non aggiunge necessariamente cose, ma rende abitabile ciò che già accade. Una conversazione ascoltata davvero, una passeggiata senza distrazioni o un lavoro svolto comprendendone il senso possono avere più peso di giornate eccezionali vissute con la mente altrove. Essere presenti non significa provare sempre intensità; significa accorgersi, distinguere e lasciare che l’esperienza produca una traccia.",
    "Anche l’attenzione, però, non basta se diventa una scusa per evitare il mondo. Si può osservare profondamente una vita sempre uguale e sentire comunque che una parte di sé non viene messa alla prova. Alcune conoscenze nascono soltanto facendo: partendo, iniziando, sbagliando, assumendo una responsabilità o entrando in relazione. Le esperienze forniscono materia; l’attenzione impedisce che quella materia scorra via senza essere compresa.",
    "La pienezza dipende inoltre dalla libertà reale. Non tutti possono moltiplicare viaggi, incontri o opportunità, e non sarebbe giusto trasformare il privilegio dell’accesso in una misura del valore personale. Una vita limitata da cura, salute o risorse può essere ricchissima di significato; allo stesso tempo, invitare qualcuno ad accontentarsi dell’interiorità non deve giustificare limiti sociali che potrebbero essere rimossi.",
    "Forse una vita piena nasce dalla relazione tra estensione e profondità. Le esperienze aprono porte; l’attenzione decide se le attraversiamo davvero. A volte serve cercare il nuovo, altre volte restare abbastanza a lungo da vedere ciò che la fretta nasconde. La misura più onesta non è quante cose abbiamo fatto, ma quante ci hanno resi più capaci di vedere, scegliere, amare e rispondere della vita che stiamo vivendo.",
]


CHAPTERS = [
    {
        "title": "Il problema di contare una vita",
        "focus": "distinguere la ricchezza reale dall’elenco di risultati, viaggi e momenti esibibili",
        "essay": [
            "Quando proviamo a capire se una vita sia piena, cerchiamo quasi subito qualcosa da contare: città visitate, traguardi, relazioni, libri, lavori, persone incontrate. I numeri danno una sensazione di chiarezza perché permettono confronti e progressi visibili. Eppure descrivono soltanto l’estensione. Non dicono se un viaggio ci abbia cambiati, se un successo ci appartenga davvero o se una relazione sia stata abitata con cura. Una biografia può essere affollata e lasciare comunque la sensazione di non essere mai arrivati in nessun luogo.",
            "L’errore non consiste nel desiderare molte esperienze. La curiosità ci porta fuori dalle abitudini e offre linguaggi nuovi per comprendere noi stessi. Il problema nasce quando l’elenco sostituisce il significato: facciamo qualcosa per poter dire di averla fatta, per non sentirci indietro o per costruire un’immagine convincente. In quel momento l’esperienza diventa una prova da esibire. Il suo valore viene deciso prima ancora che inizi e ciò che non produce una storia interessante sembra tempo perso.",
            "Anche l’idea di profondità può diventare una classifica. Possiamo giudicare superficiale chi cerca movimento e considerarci più autentici perché scegliamo lentezza e introspezione. Ma la presenza non si misura dalla gravità del tono né dalle ore passate a riflettere. Una persona può essere profondamente presente durante una festa o uno sport; un’altra può restare in silenzio senza entrare in contatto con ciò che sente. Non esiste uno stile esteriore che garantisca pienezza.",
            "Una misura più utile osserva le conseguenze. Dopo un’esperienza siamo più capaci di nominare ciò che conta? Vediamo meglio gli altri, oppure li usiamo come comparse della nostra storia? Abbiamo acquisito libertà di scelta o soltanto bisogno di un nuovo stimolo? Non ogni evento deve trasformarci radicalmente, ma nel tempo una vita piena dovrebbe lasciare segni di apprendimento, gratitudine, responsabilità e discernimento.",
            "Contare non va eliminato: calendari, fotografie e obiettivi aiutano la memoria e rendono visibili desideri trascurati. Occorre però ricordare che sono mappe, non territorio. Possiamo usarli per chiederci dove stiamo andando, non per assegnare un punteggio all’esistenza. La domanda sulla pienezza comincia quando smettiamo di cercare una cifra universale e osserviamo la qualità del rapporto tra ciò che accade e la persona che diventiamo mentre lo attraversiamo.",
        ],
        "tasks": [
            "scrivi dieci esperienze di cui parli più spesso e, accanto a ciascuna, annota che cosa ha cambiato nei tuoi gesti",
            "osserva il calendario dell’ultimo mese e separa gli impegni scelti da quelli accettati soltanto per non sentirti escluso",
            "riguarda cinque fotografie importanti senza pubblicarle e ricostruisci ciò che non compare nell’inquadratura",
            "scegli un traguardo di cui sei fiero e descrivi anche il costo, gli aiuti ricevuti e ciò che hai imparato dopo",
            "individua una cosa che fai per poterla raccontare e immagina come cambierebbe se nessuno venisse a saperlo",
            "confronta una giornata molto piena con una apparentemente vuota, usando energia, presenza e relazioni invece del numero di attività",
            "chiedi a una persona fidata quale cambiamento concreto ha notato in te negli ultimi due anni",
            "rinuncia per ventiquattro ore a misurare passi, produttività o reazioni e osserva quali criteri emergono al loro posto",
            "formula una definizione provvisoria di vita piena che non contenga numeri, prestigio o confronto con altre persone",
        ],
    },
    {
        "title": "Le esperienze ci danno materia",
        "focus": "usare il nuovo per incontrare realtà, corpi e persone invece di collezionare soltanto stimoli",
        "essay": [
            "Senza esperienze, l’attenzione rischia di rivolgersi sempre agli stessi oggetti. Entrare in un ambiente sconosciuto, assumere un compito difficile o ascoltare una storia diversa dalla nostra crea attrito. Le categorie abituali non bastano e siamo costretti a rivederle. Il nuovo non è prezioso perché eccitante in sé, ma perché interrompe l’illusione che il nostro modo di vivere sia l’unico possibile. Ogni incontro reale aggiunge dati che l’immaginazione, da sola, non avrebbe saputo produrre.",
            "Fare esperienza significa coinvolgere il corpo. Possiamo leggere tutto sulla fatica, sul mare, sulla cura o su un mestiere, ma alcune conoscenze arrivano soltanto attraverso ritmi, gesti e conseguenze. Il corpo registra distanze che una spiegazione rende astratte: la pazienza richiesta da un lavoro manuale, l’incertezza di una partenza, la vulnerabilità del chiedere aiuto. Questa conoscenza non sostituisce lo studio; gli offre consistenza e rende più difficile parlare del mondo senza esserne toccati.",
            "Le esperienze mettono alla prova le identità che raccontiamo. Possiamo considerarci coraggiosi finché non dobbiamo scegliere sotto pressione, generosi finché la condivisione non costa qualcosa, indipendenti finché non incontriamo un limite. La prova non serve a condannarci. Restituisce una versione meno immaginaria di noi stessi, con risorse e fragilità concrete. Da quella realtà possiamo imparare, mentre un’identità mai verificata resta una promessa che protegge l’autostima ma orienta male le decisioni.",
            "Non tutte le esperienze devono essere straordinarie. Imparare a cucinare un piatto, accompagnare qualcuno a una visita, abitare un quartiere, portare a termine un impegno ripetitivo sono esperienze in senso pieno quando ci espongono alla realtà. L’enfasi sull’eccezionale restringe il campo e rende invisibile la maggior parte della vita. Spesso ciò che forma non è il momento raccontabile, ma la continuità con cui torniamo a un compito e scopriamo dettagli che il primo entusiasmo non poteva vedere.",
            "Più contesti attraversiamo, più possibilità abbiamo di riconoscere preferenze e pregiudizi. Oltre una certa soglia, però, il nuovo diventa rumore. Se non c’è tempo per ricordare, confrontare e scegliere, le esperienze si neutralizzano a vicenda. La materia della vita ha bisogno di essere lavorata. L’obiettivo non è riempire ogni spazio del calendario, ma incontrare abbastanza realtà da non vivere soltanto dentro le nostre ipotesi.",
        ],
        "tasks": [
            "entra in un luogo ordinario che non frequenti e resta abbastanza da capire una regola non scritta di quel contesto",
            "impara un gesto pratico da una persona più competente senza fingere di sapere già",
            "prova un’attività che coinvolga il corpo e annota la differenza tra ciò che immaginavi e ciò che hai sentito",
            "parla con qualcuno la cui giornata è organizzata in modo diverso dalla tua e ascolta senza trasformare il confronto in gara",
            "ripeti un compito domestico lentamente, osservando competenze, fatica e dipendenze che di solito restano invisibili",
            "scegli una piccola responsabilità nuova che abbia una conseguenza reale per qualcun altro",
            "visita un quartiere vicino seguendo servizi, rumori e percorsi quotidiani invece delle attrazioni",
            "rivedi una convinzione personale alla luce di un’esperienza che l’ha contraddetta, senza difendere subito la versione precedente",
            "decidi una sola esperienza nuova per il prossimo mese e prepara il tempo necessario per integrarla dopo",
        ],
    },
    {
        "title": "L’attenzione trasforma il tempo",
        "focus": "recuperare la capacità di accorgersi senza pretendere concentrazione perfetta o colpevolizzare la distrazione",
        "essay": [
            "L’attenzione non allunga le ore, ma cambia la densità con cui le percepiamo. Quando siamo presenti distinguiamo voci, gesti, esitazioni e dettagli che altrimenti diventano sfondo. Questo non rende ogni istante memorabile; crea però le condizioni perché qualcosa possa raggiungerci. Una giornata vissuta in automatismo può sembrare scomparsa, mentre pochi minuti di ascolto autentico restano disponibili alla memoria perché hanno avuto contorni precisi. La pienezza comincia spesso dalla capacità di accorgersi.",
            "Essere attenti non significa controllare perfettamente la mente. La distrazione è parte della coscienza, e pretendere concentrazione continua aggiunge soltanto giudizio. L’attenzione è il gesto del ritorno: riconoscere che ci siamo allontanati e rientrare nella conversazione, nel corpo o nel compito. Ogni ritorno ricuce il rapporto con il presente. La qualità non dipende dall’assenza di dispersione, ma dalla disponibilità a non lasciarle tutta la giornata.",
            "La tecnologia può frammentare l’attenzione, ma non è l’unica responsabile. Anche ansia, precarietà, dolore e carico di cura occupano lo spazio mentale. Dire a chi è sotto pressione di vivere il momento rischia di trasformare un problema materiale in difetto personale. L’attenzione ha bisogno di condizioni: riposo sufficiente, sicurezza, limiti e tempi non interrotti. Proteggerla può richiedere scelte individuali, ma anche organizzazioni più umane e una distribuzione meno ingiusta delle urgenze.",
            "La presenza modifica anche l’etica. Se vediamo davvero chi abbiamo davanti, diventa più difficile ridurlo a funzione, ostacolo o pubblico. Notiamo il costo delle nostre decisioni e le richieste che non vengono pronunciate. L’attenzione non garantisce bontà, ma rende visibile ciò che l’indifferenza lascia fuori. Una vita piena non è soltanto quella che sente molto; è quella che permette alla realtà degli altri di influenzare i propri gesti senza perdere ogni confine.",
            "Possiamo allenare l’attenzione con pratiche piccole: terminare una cosa prima di aprirne un’altra, fare una domanda e aspettare la risposta, lasciare il telefono fuori portata durante un incontro, descrivere mentalmente ciò che vediamo. Nessuna pratica deve diventare un rituale rigido. Serve a recuperare scelta. L’attenzione è preziosa proprio perché limitata: decidere dove posarla significa dichiarare, per quel tratto di tempo, che cosa merita di esistere pienamente per noi.",
        ],
        "tasks": [
            "svolgi per venti minuti un solo compito e registra ogni impulso a cambiare finestra senza obbedirgli subito",
            "durante una conversazione formula una domanda reale e lascia che la risposta finisca prima di preparare la tua",
            "cammina per un percorso noto cercando cinque dettagli che non avevi mai nominato",
            "mangia una volta senza schermi e distingui fame, gusto, velocità e momento in cui ti senti sazio",
            "osserva quando prendi il telefono senza aver deciso che cosa cercare e annota quale emozione precede il gesto",
            "proteggi un intervallo breve da notifiche e richieste, spiegando agli altri quando tornerai disponibile",
            "riconosci una distrazione causata da preoccupazione reale e trasformala in una richiesta, un piano o un confine",
            "dedica attenzione completa a un’attività piacevole senza convertirla in contenuto o prova di produttività",
            "scegli una relazione a cui offrire presenza regolare invece di un gesto spettacolare e isolato",
        ],
    },
    {
        "title": "Memoria: ciò che resta di ciò che viviamo",
        "focus": "integrare gli eventi attraverso ricordo e racconto senza trasformare la vita in un archivio di prove",
        "essay": [
            "Non ricordiamo la vita come una registrazione continua. La memoria seleziona, ricompone e talvolta modifica. Periodi lunghi si riducono a poche immagini, mentre un episodio breve mantiene colori e parole. Per questo la quantità delle esperienze e la sensazione retrospettiva di pienezza non coincidono. Ciò che conta non è soltanto accaduto: è stato notato, raccontato, collegato a qualcosa che già sapevamo o a una persona con cui lo abbiamo condiviso.",
            "Le fotografie possono sostenere la memoria, ma anche sostituirsi all’osservazione. Scattare non è necessariamente distrarsi: scegliere un’inquadratura può far vedere meglio. Il rischio nasce quando l’intera esperienza viene organizzata per produrre una traccia pubblicabile. Invece di chiederci che cosa stiamo vivendo, chiediamo come apparirà. Una pratica equilibrata conserva qualche segno e poi restituisce spazio alla scena, accettando che una parte importante non sarà documentata.",
            "Raccontare integra l’esperienza. Quando proviamo a spiegare che cosa è successo, selezioniamo cause, emozioni e conseguenze. Possiamo scoprire un significato che durante l’evento non era visibile. Ma ogni racconto semplifica; ripetendolo, rischiamo di imprigionare il passato in una versione utile alla nostra identità. Tornare su un ricordo con domande nuove permette di riconoscere dettagli omessi e responsabilità che la prima narrazione aveva protetto.",
            "Anche dimenticare è necessario. Una vita in cui ogni dettaglio conservasse la stessa intensità sarebbe ingestibile. La memoria lascia sfumare molto per rendere possibile il presente. Pienezza non significa trattenere tutto, ma consentire ad alcune esperienze di diventare orientamento anche quando le immagini si attenuano. Una lezione può restare nei gesti senza che ricordiamo il giorno in cui l’abbiamo imparata; una relazione può averci cambiati anche se molte conversazioni sono perdute.",
            "Per dare forma a ciò che viviamo bastano pause di integrazione: una nota alla fine della giornata, una conversazione senza fretta, il ritorno in un luogo, una domanda su ciò che è cambiato. Queste pause non devono trasformare ogni evento in un progetto di miglioramento. Servono a riconoscere la traccia prima che venga coperta. La memoria rende la vita più piena quando non è un magazzino di prove, ma un tessuto che collega esperienze diverse e aiuta a scegliere il passo successivo.",
        ],
        "tasks": [
            "scegli un ricordo molto raccontato e scrivi tre dettagli che la tua versione abituale lascia sempre fuori",
            "guarda una fotografia senza leggere data o didascalia e ricostruisci ciò che sai davvero e ciò che stai immaginando",
            "annota la sera un’immagine, una frase e una domanda della giornata senza aggiungere giudizi",
            "racconta la stessa esperienza dal punto di vista di un’altra persona presente, dichiarando ciò che non puoi sapere",
            "individua una lezione che continui a usare anche se non ricordi più l’episodio preciso in cui l’hai appresa",
            "scegli un oggetto conservato per memoria e decidi se ti collega ancora a qualcosa o occupa soltanto spazio",
            "riprendi un vecchio diario o messaggio e nota in che modo il ricordo attuale ha semplificato quella fase",
            "condividi con qualcuno un ricordo comune e ascolta le differenze senza stabilire subito quale versione sia corretta",
            "crea un piccolo rito mensile per integrare le esperienze prima di cercarne altre",
        ],
    },
    {
        "title": "La noia e gli spazi non riempiti",
        "focus": "restituire respiro alla vita distinguendo il vuoto fertile dall’isolamento e dalla mancanza di possibilità",
        "essay": [
            "Una vita piena non è una vita satura. Se ogni intervallo viene occupato, non resta spazio per percepire desideri deboli, stanchezza o domande ancora senza forma. La noia può essere scomoda perché toglie gli stimoli con cui misuriamo il movimento. Non è sempre creativa: può pesare, soprattutto quando nasce da isolamento o mancanza di opportunità. Ma una piccola quota di vuoto scelto permette all’attenzione di allargarsi oltre ciò che reclama risposta immediata.",
            "La saturazione produce un paradosso. Cerchiamo molte esperienze per sentirci vivi, ma la velocità necessaria a contenerle riduce la capacità di sentirle. Il momento presente viene usato per preparare il successivo, documentare il precedente o controllare ciò che stiamo perdendo altrove. Alla fine restano molte attività e poca continuità. Rallentare non è una virtù universale; diventa utile quando consente di smettere di trattare ogni esperienza come un passaggio verso un’altra.",
            "Gli spazi vuoti rendono visibili anche le emozioni evitate. Senza rumore può emergere tristezza, paura o insoddisfazione. È uno dei motivi per cui riempiamo il tempo. Non tutte queste emozioni vanno affrontate soli, e talvolta serve un aiuto competente. La presenza non consiste nel restare immobili dentro una sofferenza ingestibile. Consiste nel riconoscere ciò che accade abbastanza presto da poter cercare sostegno, cambiare una condizione o scegliere consapevolmente una pausa.",
            "Il tempo non programmato permette di inventare, negoziare e scoprire interessi. Anche gli adulti hanno bisogno di territori simili: una camminata senza contenuti, un viaggio senza produttività, una sera non ottimizzata. Non producono necessariamente idee brillanti; restituiscono il diritto di non essere sempre consumatori o prestatori di attenzione. Il loro valore non dipende da ciò che generano dopo, ma dalla libertà che rendono percepibile mentre accadono.",
            "Proteggere il vuoto richiede confini concreti. Possiamo lasciare un margine tra appuntamenti, evitare di riempire automaticamente una coda, mantenere una parte del fine settimana senza obiettivi. Il risultato iniziale può essere irrequietezza, non pace. Con il tempo quel margine diventa un luogo in cui distinguere ciò che desideriamo da ciò che facciamo per abitudine. Una vita piena respira: contiene movimento e riposo, parole e silenzio, eventi e intervalli che permettono agli eventi di assumere forma.",
        ],
        "tasks": [
            "lascia dieci minuti di attesa senza contenuti e osserva quale impulso prova per primo a riempirli",
            "mantieni uno spazio tra due appuntamenti invece di usare il ritardo per aggiungere un altro compito",
            "trascorri una sera senza obiettivi di miglioramento e nota se il riposo viene subito giudicato",
            "distingui una noia dovuta a mancanza di stimolo da una dovuta a mancanza di significato o di relazioni",
            "spegni la riproduzione automatica e scegli consapevolmente se iniziare un contenuto successivo",
            "chiediti quale emozione diventerebbe più udibile se smettessi per un’ora di occuparti",
            "programma un tempo vuoto con lo stesso rispetto con cui proteggeresti un impegno preso con altri",
            "osserva un bambino o un adulto inventare qualcosa senza istruzioni e registra che cosa rende possibile il gioco",
            "elimina un’attività che non desideri più e lascia libero lo spazio prima di sostituirla",
        ],
    },
    {
        "title": "Privilegio, limiti e possibilità reali",
        "focus": "valutare la pienezza senza confondere accesso, denaro e libertà materiale con il valore personale",
        "essay": [
            "Il linguaggio delle esperienze può nascondere differenze materiali. Viaggiare, studiare, cambiare lavoro o dedicare tempo alla contemplazione richiede spesso denaro, salute, documenti, reti di sostegno e libertà da responsabilità urgenti. Presentare queste possibilità come semplice coraggio attribuisce merito a chi possiede accesso e colpa a chi non lo ha. Una misura onesta della pienezza distingue le scelte dai vincoli e non trasforma un certo stile di vita in modello universale.",
            "Anche l’invito a essere presenti può diventare ingiusto. Chi vive precarietà o dolore non è distratto per superficialità: una parte dell’attenzione è impegnata a prevedere rischi. La sicurezza amplia il presente perché rende meno necessario sorvegliare continuamente il futuro. Coltivare attenzione non è soltanto una pratica privata. Significa anche sostenere condizioni in cui più persone possano riposare, curarsi e disporre di tempo non interamente assorbito dalla sopravvivenza.",
            "I limiti, tuttavia, non cancellano ogni possibilità di pienezza. Una persona con mobilità ridotta, risorse modeste o obblighi di cura non vive automaticamente una vita meno ricca. Relazioni, competenza, immaginazione e presenza possono svilupparsi in territori ristretti. Affermarlo non serve a romanticizzare l’ostacolo. Serve a rifiutare l’idea che il valore umano dipenda dal consumo di opportunità visibili, mantenendo insieme la richiesta di rimuovere le barriere evitabili.",
            "La pienezza può essere condivisa. Non tutte le esperienze devono appartenerci individualmente. Ascoltare il racconto altrui, partecipare a un progetto comune, rendere possibile un’opportunità per qualcuno amplia il mondo senza trasformarlo in possesso. Questo sguardo corregge l’idea che la vita sia una raccolta privata. Molto di ciò che ci forma arriva da persone che hanno custodito conoscenze, luoghi e gesti prima di noi e che continueranno dopo di noi.",
            "Chiedersi quali possibilità siano reali non significa rinunciare al desiderio. Aiuta a scegliere un passo che non dipenda da un’immagine irraggiungibile e a identificare ciò che richiede un cambiamento collettivo. Possiamo cercare maggiore attenzione nel quotidiano e insieme pretendere accesso a istruzione, salute, cultura e tempo. La vita piena non è un premio per chi ottimizza meglio le proprie risorse: è un orizzonte personale e politico, fatto di libertà concreta e capacità di abitarla.",
        ],
        "tasks": [
            "elenca tre esperienze rese possibili da risorse, persone o servizi che tendi a considerare soltanto merito personale",
            "individua un limite attuale e separa ciò che puoi scegliere, ciò che richiede aiuto e ciò che dipende da condizioni collettive",
            "ascolta una storia di vita diversa evitando di trasformarla in ispirazione, colpa o confronto",
            "osserva come denaro, salute e tempo modificano concretamente una possibilità che desideri",
            "rendi accessibile a qualcuno una piccola esperienza attraverso informazione, accompagnamento o condivisione di risorse",
            "riconosci una forma di ricchezza non visibile che esiste nella tua vita senza negare ciò che manca",
            "sostituisci un consiglio generico con una domanda sulle condizioni reali della persona che hai davanti",
            "scegli un desiderio proporzionato alle risorse presenti e un’azione civica o collettiva legata al limite più grande",
            "riscrivi la tua idea di successo includendo dipendenza reciproca, cura ricevuta e possibilità restituite agli altri",
        ],
    },
    {
        "title": "Ampiezza e profondità nelle relazioni",
        "focus": "riconoscere il valore diverso degli incontri numerosi e dei legami che richiedono continuità, conflitto e cura",
        "essay": [
            "Le relazioni mostrano con chiarezza la tensione tra quantità e attenzione. Conoscere molte persone espone a linguaggi, opportunità e mondi diversi; investire in pochi legami rende possibili fiducia, vulnerabilità, conflitto e riparazione. Le reti ampie e i rapporti intimi svolgono funzioni differenti. Il problema nasce quando chiediamo a ogni contatto di diventare famiglia o trattiamo ogni rapporto come sostituibile appena richiede pazienza.",
            "La presenza relazionale non coincide con il tempo trascorso insieme. Si può condividere una casa restando inaccessibili, oppure incontrarsi raramente e offrire ascolto preciso. Contano la qualità dell’attenzione, la possibilità di dire la verità e la continuità tra parole e gesti. Nessuno riesce a mantenere intensità con tutti. Dare un nome realistico alla forma del legame evita promesse implicite che non possiamo sostenere e consente di offrire a ciascuna relazione una cura proporzionata.",
            "Anche le esperienze condivise possono essere usate per evitare l’intimità. Viaggi, feste e progetti producono ricordi, ma non garantiscono che le persone si conoscano. Talvolta il movimento impedisce domande difficili; quando l’attività finisce emerge il vuoto. Al contrario, la quotidianità può diventare un luogo di scoperta se continuiamo a chiedere come l’altro stia cambiando invece di trattarlo come una persona già conosciuta una volta per tutte.",
            "Una relazione profonda include il conflitto senza considerarlo prova automatica di incompatibilità. Essere attenti significa distinguere danno, divergenza e semplice delusione. Alcuni rapporti vanno interrotti per proteggersi; altri possono essere riparati riconoscendo effetti, responsabilità e bisogni. La pienezza relazionale non si misura dal numero di persone rimaste per sempre, ma dalla capacità di costruire legami in cui vicinanza e libertà non si annullano.",
            "Ci sono stagioni in cui una rete ampia sostiene più di un unico legame, e altre in cui poche presenze affidabili bastano. Nessuna formula vale per tutti. La domanda utile è se il nostro modo di stare con gli altri ci rende più disponibili alla realtà o più dipendenti dall’approvazione. Una vita piena non usa le persone per riempire il calendario: accetta che ogni incontro abbia una forma, un limite e una responsabilità diversa.",
        ],
        "tasks": [
            "disegna tre cerchi di relazioni e colloca le persone secondo fiducia reale invece che frequenza o prestigio",
            "dedica un incontro a conoscere che cosa sta cambiando nell’altra persona senza raccontare subito un’esperienza equivalente",
            "riconosci un rapporto che mantieni soltanto per paura del vuoto e chiediti quale confine sarebbe onesto",
            "scegli una relazione affidabile e compi un gesto di continuità che non abbia bisogno di essere spettacolare",
            "ripensa a un conflitto separando intenzione, effetto, responsabilità e possibilità concreta di riparazione",
            "contatta una persona con cui condividi valori ma non attività e proponi un tempo semplice senza programma",
            "osserva quali relazioni ricevono soltanto la parte stanca della tua giornata e quali ricevono tutta l’energia migliore",
            "smetti per una settimana di misurare un legame dalla rapidità delle risposte e guarda invece affidabilità e rispetto",
            "formula una promessa relazionale piccola che puoi mantenere e una promessa implicita che devi chiarire o ritirare",
        ],
    },
    {
        "title": "Lavoro, risultati e identità",
        "focus": "dare valore all’impegno senza permettere che produttività e riconoscimento occupino l’intera definizione di sé",
        "essay": [
            "Il lavoro offre molte esperienze: competenza, collaborazione, conflitto, autonomia, fatica, risultato. Può dare struttura e dignità, ma possiede anche misure aggressive: ore, obiettivi, fatturato, consegne, valutazioni. Quando queste metriche diventano l’unico linguaggio disponibile, una giornata piena di produzione sembra automaticamente una giornata piena di vita. Il corpo, le relazioni e la curiosità non misurabile finiscono ai margini, come se esistessero soltanto per sostenere la prestazione successiva.",
            "L’attenzione al lavoro non significa lavorare sempre. Significa comprendere il compito, vedere le persone coinvolte, riconoscere effetti e limiti. Si può essere molto occupati e poco presenti, passando da un’urgenza all’altra senza sapere quale problema stiamo risolvendo. Una competenza matura include la capacità di distinguere importanza e rumore, di chiedere chiarimenti e di interrompersi quando la qualità crolla. La presenza protegge il lavoro dal diventare soltanto movimento.",
            "Anche i risultati hanno bisogno di integrazione. Raggiunto un obiettivo, spesso corriamo al successivo perché il sollievo dura meno del previsto. Celebrare non è vanità: permette di riconoscere contributi, apprendimento e costo. Senza questa pausa, il successo non entra nell’identità; resta una soglia già superata che non può nutrire il presente. Allo stesso modo, un fallimento osservato con precisione può diventare informazione invece di verdetto sul valore personale.",
            "Non tutti possono ridurre il lavoro o sceglierlo liberamente. Parlare di equilibrio senza considerare reddito, contratti, cura e potere rischia di colpevolizzare chi ha meno margine. Anche dentro vincoli forti, però, è utile distinguere ciò che appartiene al ruolo da ciò che appartiene alla persona. Proteggere un gesto, una relazione o un interesse fuori dalla prestazione conserva un luogo in cui il giudizio professionale non decide tutto.",
            "Una vita piena può contenere ambizione. Il problema non è voler migliorare, ma affidare al risultato il compito impossibile di confermare definitivamente che meritiamo di esistere. Nessun traguardo chiude quella domanda per sempre. Lavorare con attenzione significa scegliere che cosa costruire, con quali costi e al servizio di quale realtà. Quando l’impegno risponde a questi criteri, la produttività torna a essere uno strumento invece di diventare identità totale.",
        ],
        "tasks": [
            "descrivi il tuo lavoro senza usare ruolo, titolo o quantità e indica quale problema concreto contribuisci a risolvere",
            "separa in una giornata le attività importanti dalle urgenze create da abitudini, notifiche o richieste non chiarite",
            "scegli un risultato recente e riconosci persone, competenze, rinunce e condizioni che lo hanno reso possibile",
            "individua un fallimento e trasformalo in tre informazioni operative senza usarlo come giudizio sulla persona",
            "proteggi una pausa vera e osserva quali paure compaiono quando non stai producendo",
            "dedica attenzione completa a un compito significativo e riduci deliberatamente il multitasking per il tempo necessario",
            "nomina un confine professionale che dipende da te e uno che richiede una negoziazione o tutela collettiva",
            "riprendi un interesse che non produce denaro, prestigio o vantaggio misurabile",
            "scrivi quale costo non sei disposto a pagare per il prossimo traguardo e quale contributo vuoi invece offrire",
        ],
    },
    {
        "title": "Scegliere un ritmo che possa durare",
        "focus": "alternare esplorazione, consolidamento e riposo secondo la stagione reale della vita",
        "essay": [
            "Ogni stagione richiede un equilibrio diverso. Ci sono periodi in cui esplorare è necessario: dobbiamo provare lavori, ambienti e relazioni per capire chi siamo. In altri momenti la crescita dipende dal restare, ripetere e prendersi cura. Nessuna direzione è superiore. L’esplorazione senza radici può diventare fuga; la profondità senza aperture può trasformarsi in paura. La scelta dipende da ciò che la vita contiene già e da ciò che continua a mancare.",
            "Un segnale di eccessiva ampiezza è la difficoltà a ricordare o mantenere. Iniziamo molto, terminiamo poco, raccontiamo gli eventi con formule simili e abbiamo bisogno di stimoli più forti. Un segnale di eccessiva chiusura è l’assenza di sorpresa: interpretiamo ogni novità con categorie già decise, rimandiamo qualsiasi rischio e confondiamo familiarità con sicurezza. Questi segnali non sono diagnosi; invitano a un gesto opposto e proporzionato.",
            "Il ritmo non è soltanto velocità. Comprende alternanza, recupero e possibilità di cambiare intensità. Due persone possono avere calendari ugualmente pieni ma vivere un rapporto diverso con il tempo: una dispone di margini e priorità, l’altra reagisce senza sosta. Un ritmo sostenibile contiene pause sufficienti a percepire il corpo, correggere la direzione e mantenere promesse. Non elimina le fasi eccezionali; impedisce che l’emergenza diventi la forma permanente della vita.",
            "Possiamo valutare un nuovo sì chiedendo quale qualità porterà: conoscenza, relazione, gioia, servizio o soltanto occupazione. E possiamo valutare un no chiedendo che cosa protegge: riposo, continuità, denaro, una promessa, oppure semplicemente timore. Le risposte non sono sempre limpide. Mettere in parole il criterio evita però che sia la pressione del momento a decidere. La pienezza cresce quando il calendario riflette almeno in parte valori riconosciuti.",
            "La decisione può essere temporanea. Possiamo dedicare una fase all’esplorazione e la successiva al consolidamento, oppure proteggere giorni diversi per funzioni diverse. Non occorre trovare una formula definitiva. Una vita piena è sensibile ai cambiamenti: rivede l’equilibrio quando arrivano età, responsabilità, perdite e opportunità. La coerenza non consiste nel mantenere sempre lo stesso ritmo, ma nel sapere perché adesso abbiamo bisogno di aprirci, restare o riposare.",
        ],
        "tasks": [
            "disegna la tua settimana come alternanza di espansione, concentrazione e recupero e individua ciò che manca",
            "scegli un’attività da consolidare per un mese invece di iniziarne un’altra",
            "introduci una novità piccola in un’area diventata troppo prevedibile e definisci che cosa vuoi scoprire",
            "calcola il tempo di recupero richiesto da un impegno prima di dire sì",
            "osserva in quale ora della giornata prendi decisioni peggiori e proteggila da scelte non necessarie",
            "trasforma un no automatico in un esperimento reversibile oppure un sì impulsivo in una verifica di ventiquattro ore",
            "riconosci una stagione conclusa che continui a mantenere per identità o aspettative altrui",
            "crea un margine realistico nel calendario per imprevisti invece di considerarlo tempo sprecato",
            "scegli il ritmo dei prossimi trenta giorni e scrivi quale segnale ti farà capire che va corretto",
        ],
    },
    {
        "title": "Una pratica per abitare la propria vita",
        "focus": "unire esperienza e attenzione in scelte concrete, verificabili e abbastanza flessibili da restare umane",
        "essay": [
            "La domanda iniziale non richiede di scegliere un vincitore tra esperienza e attenzione. Possiamo usarla come verifica periodica. Guardando l’ultima settimana, quali momenti erano davvero nostri e quali sono scivolati in automatismo? C’è qualcosa che desideriamo fare da tempo e continuiamo a sostituire con attività minori? C’è invece un’esperienza che ripetiamo senza più ascoltarla? Rispondere con esempi concreti evita che la riflessione resti un ideale elegante.",
            "Una pratica utile consiste nel selezionare un’esperienza da aggiungere e una da approfondire. La prima può essere piccola: visitare un luogo vicino, parlare con una persona fuori dal proprio ambiente, imparare un gesto. La seconda riguarda ciò che esiste già: una relazione, un compito, un quartiere, un’abitudine. Per entrambe scegliamo un tempo realistico e un segno di attenzione, come lasciare il telefono, annotare una domanda o condividere ciò che abbiamo scoperto.",
            "Serve anche sottrarre. Ogni nuova esperienza occupa un pezzo di vita, e l’attenzione non può moltiplicarsi senza limite. Prima di riempire uno spazio, possiamo chiederci che cosa non riceverà cura. La sottrazione non deve diventare minimalismo competitivo. È il riconoscimento che dire sì a tutto rende i sì indistinguibili. Rinunciare a un’attività, a una notifica o a un obbligo autoimposto può restituire presenza a qualcosa che avevamo già scelto.",
            "Alla fine di un’esperienza, una breve integrazione cambia il modo in cui resta. Possiamo nominare un dettaglio inatteso, una sensazione, una domanda e una conseguenza. Non occorre estrarre una lezione da ogni pranzo o passeggiata; basta permettere ad alcuni momenti di depositarsi. Se nulla emerge, anche questo è un dato: forse l’esperienza era soltanto piacevole, forse eravamo assenti, forse il suo significato arriverà più tardi. La pienezza non richiede interpretazione continua.",
            "Una vita piena si misura allora con una domanda mobile: ciò che viviamo sta ampliando la capacità di essere presenti, e la nostra attenzione ci rende disponibili a vivere ciò che conta? Le esperienze senza attenzione rischiano di diventare collezione; l’attenzione senza esperienza rischia di girare in uno spazio troppo stretto. Insieme creano un movimento fertile: il mondo ci cambia, noi lo riconosciamo e da quel riconoscimento nasce una scelta più libera per il passo successivo.",
        ],
        "tasks": [
            "rileggi l’ultima settimana e scegli un momento da aggiungere, uno da approfondire e uno da sottrarre",
            "definisci un’esperienza concreta per i prossimi sette giorni con tempo, luogo, costo e persona eventualmente coinvolta",
            "scegli un’attività abituale e stabilisci un segno semplice di attenzione che la renda nuovamente visibile",
            "crea una domanda di fine giornata che non misuri produttività ma presenza, relazione o apprendimento",
            "condividi il tuo esperimento con una persona che possa osservare senza controllare",
            "prepara una risposta gentile per quando il piano fallirà, distinguendo correzione da abbandono",
            "verifica se il nuovo gesto aumenta libertà o diventa un’altra prestazione da dimostrare",
            "raccogli una traccia privata dell’esperienza e lascia intenzionalmente una parte non documentata",
            "scegli il passo successivo soltanto dopo aver nominato ciò che il primo ha realmente cambiato",
        ],
    },
]


OPENERS = [
    "Comincia senza cercare una risposta brillante. Riserva quaranta minuti, togli le interruzioni prevedibili e svolgi questa consegna: {task}. Scrivi fatti osservabili prima delle interpretazioni: luoghi, orari, gesti, persone e conseguenze. Se compare un giudizio globale come sempre, mai, giusto o sbagliato, trasformalo in un episodio preciso. Lo scopo non è produrre una confessione né migliorare l’immagine di te, ma costruire materiale sufficientemente concreto da poter essere riletto. Concludi indicando ciò che sai, ciò che stai deducendo e ciò che resta ignoto.",
    "Porta la pratica nella giornata reale, non in una condizione ideale: {task}. Prima di iniziare, definisci un confine di tempo e una soglia minima che renda l’esperimento possibile anche con poca energia. Durante l’attività nota quando l’attenzione si sposta verso la prestazione, il confronto o il desiderio di finire. Non correggere tutto sul momento; registra il passaggio e torna al gesto. Alla fine descrivi una sorpresa, una resistenza e un elemento che vorresti verificare di nuovo in un contesto diverso.",
    "Usa questa consegna come osservazione, non come esame: {task}. Prepara due colonne, una per ciò che accade e una per il significato che gli attribuisci. Questa separazione riduce il rischio di scambiare la prima impressione per una verità definitiva. Se sono coinvolte altre persone, non presumere intenzioni: annota parole e comportamenti, poi formula domande. Termina scegliendo una sola ipotesi da conservare per ventiquattro ore senza agire, così da vedere se la distanza cambia il modo in cui interpreti la scena.",
    "Svolgi l’esercizio con una misura abbastanza piccola da poter essere ripetuta: {task}. Non aggiungere strumenti, applicazioni o regole se un foglio e un orario sono sufficienti. Prima registra l’aspettativa; dopo registra l’esperienza effettiva. Cerca soprattutto le differenze, perché mostrano dove il racconto anticipato non coincide con la vita. Se il compito risulta troppo facile o troppo difficile, non dichiararlo inutile: modifica durata, contesto o sostegno e descrivi la nuova versione che proveresti.",
    "Questa pratica richiede onestà ma non durezza: {task}. Osserva il modo in cui parli a te stesso mentre la svolgi. Un linguaggio accusatorio restringe l’attenzione e spinge a difendersi; un linguaggio troppo indulgente può nascondere le conseguenze. Usa frasi descrittive: è successo questo, ha prodotto questo effetto, avevo queste alternative. Aggiungi infine quale bisogno stavi proteggendo e quale costo ha avuto quella protezione. L’obiettivo è recuperare scelta, non distribuire colpe.",
    "Per questa tappa coinvolgi il corpo oltre al pensiero: {task}. Nota postura, respiro, velocità, fame, tensione e desiderio di interrompere. Le sensazioni non decidono da sole che cosa sia giusto, ma segnalano aspetti che il ragionamento può aver escluso. Confrontale con i fatti e con le esigenze delle persone coinvolte. Dopo l’esperimento concediti alcuni minuti senza contenuti, poi scrivi che cosa è diventato più chiaro e che cosa richiede invece informazioni, riposo o un confronto competente.",
    "Trasforma la consegna in una conversazione verificabile: {task}. Se puoi, racconta a una persona fidata che cosa stai osservando e chiedile un esempio, non una valutazione del tuo carattere. Ascolta senza discutere subito la sua versione. Poi confronta il suo sguardo con il tuo, cercando convergenze e differenze. Non consegnarle la decisione finale: usa il dialogo per ampliare i dati. Chiudi formulando una domanda più precisa di quella con cui avevi iniziato.",
    "Oggi lavora sulla continuità: {task}. Collega questa pratica a un gesto già presente nella giornata, così non dipenderà soltanto dalla motivazione. Riduci l’obiettivo finché può essere mantenuto per una settimana senza togliere cura a sonno, salute o relazioni importanti. Stabilisci anche una condizione di pausa: se compare un certo costo, interromperai e valuterai. La disciplina utile non ignora i limiti; li usa per costruire un ritmo che non richieda di ricominciare ogni volta da zero.",
    "Considera questa consegna una decisione provvisoria: {task}. Definisci in anticipo quando la rivedrai e quali segnali conteranno. Evita di affidarti soltanto all’entusiasmo immediato o al ricordo finale; raccogli una nota durante, una subito dopo e una il giorno seguente. Le tre prospettive possono divergere. Non cercare di renderle coerenti a forza. Usa la divergenza per capire se l’esperienza nutre, stanca, apre possibilità o serve soprattutto a confermare un’immagine.",
]


CLOSERS = [
    "Rileggi il materiale una sola volta e sottolinea un fatto che contraddice la tua storia abituale. Non costruire subito una nuova identità intorno a quell’eccezione. Chiediti invece quale condizione l’ha resa possibile e se può essere ricreata. Scegli un’azione di dieci minuti da compiere entro due giorni. La verifica successiva non dovrà stabilire se sei cambiato, ma se hai aumentato di poco la capacità di vedere e scegliere.",
    "Prima di chiudere, assegna un nome preciso al costo dell’esperimento e al beneficio osservato. Evita parole totali come benessere o fallimento: indica sonno, energia, chiarezza, tempo, denaro, vicinanza o tensione. Questa precisione consente di confrontare esperienze diverse senza ridurle a un punteggio unico. Conserva soltanto la modifica che produce un vantaggio reale senza spostare silenziosamente il costo su un’altra persona o sulla tua salute.",
    "Se l’esercizio suscita un’emozione intensa, non usarla come prova conclusiva. Fermati, torna alle sensazioni fisiche e valuta se hai bisogno di sostegno. Alcune domande aprono ricordi o conflitti che non devono essere risolti in solitudine. Puoi sospendere la pratica senza tradirne il senso. La pienezza non richiede esposizione continua; include la capacità di riconoscere quando attenzione significa protezione, confine e richiesta di aiuto.",
    "Scrivi ora due frasi: nella prima, ciò che vuoi conservare; nella seconda, ciò che sei disposto a lasciare incompleto. Questa coppia impedisce alla pratica di diventare un’altra lista infinita. Se tutto sembra importante, scegli in base alle conseguenze nelle prossime settimane. La decisione può essere rivista, ma deve produrre un gesto riconoscibile. Senza un piccolo effetto nel calendario, anche la riflessione più elegante rischia di restare separata dalla vita.",
    "Confronta il risultato con il tema del capitolo e chiediti se hai aggiunto un’esperienza o aumentato l’attenzione. Se hai fatto soltanto una delle due cose, immagina il complemento: quale presenza renderebbe più profonda l’esperienza, oppure quale incontro renderebbe meno chiusa l’osservazione? Non serve realizzarlo subito. Nominarlo evita di trasformare una soluzione parziale in regola universale e mantiene aperta la possibilità di riequilibrare.",
    "Porta con te un dettaglio sensoriale dell’esperimento: un suono, una posizione del corpo, una luce, una frase ascoltata. Sarà un richiamo più efficace di una conclusione astratta. Quando quel dettaglio ricomparirà, usalo per fare una pausa e verificare la direzione. La memoria quotidiana lavora attraverso segnali concreti; scegliere un segnale permette alla pratica di continuare senza occupare continuamente il pensiero.",
    "Ringrazia l’eventuale persona coinvolta senza trasformarla nel supervisore del tuo cambiamento. Se il suo contributo ha rivelato un effetto delle tue azioni, riconoscilo e chiedi che cosa servirebbe per riparare o continuare. Non promettere trasformazioni assolute. Formula un comportamento osservabile e una data di verifica. La fiducia cresce più facilmente da impegni limitati mantenuti che da dichiarazioni intense destinate a svanire.",
    "Decidi dove conservare la nota e quando rileggerla. Se la accumuli insieme a decine di esercizi mai ripresi, diventerà un’altra esperienza consumata. Scegli un solo appuntamento di revisione e, fino ad allora, torna alla vita ordinaria. L’integrazione avviene anche senza analisi continua. Lascia che il gesto provato incontri imprevisti e resistenze; saranno informazioni per la revisione, non deviazioni da cancellare.",
    "Chiudi senza riassumere tutto. Completa soltanto questa frase: domani riconoscerò che sto vivendo con più attenzione quando… Inserisci un segnale concreto e modesto. Poi indica un’esperienza che sei disponibile a ricevere senza controllarne in anticipo il risultato. La prima scelta protegge la profondità; la seconda mantiene aperta l’ampiezza. Insieme formano una direzione, non una prestazione da dimostrare.",
]


FOLLOWUPS = [
    "Prima di passare oltre, prova a raccontare l’osservazione in meno di cento parole, eliminando spiegazioni che non puoi verificare. Poi riscrivila aggiungendo il contesto che la rende comprensibile. La differenza tra le due versioni mostra quanta parte del significato dipenda dai dettagli e quanta dal racconto che tendi ad applicare automaticamente.",
    "Ripeti una parte dell’esperimento in un orario diverso. Energia, fretta e presenza degli altri possono cambiare il risultato più del contenuto della pratica. Se le due prove divergono, non scegliere subito quella che preferisci: considera entrambe e individua la condizione che ha inciso maggiormente. Questa informazione renderà più realistico il prossimo tentativo.",
    "Aggiungi una domanda che potrebbe smentire la tua interpretazione. Cercare soltanto conferme rende qualsiasi esercizio una dimostrazione già decisa. Un’ipotesi alternativa non deve essere più rassicurante: deve spiegare i fatti con meno presupposti. Conserva entrambe finché un nuovo gesto o una conversazione fornisce elementi sufficienti per distinguerle.",
    "Immagina ora di dover rendere la pratica accessibile a una persona con meno tempo, energia o libertà. Quale parte è essenziale e quale può essere rimossa? Questa riduzione fa emergere il meccanismo utile nascosto sotto il rituale. Applicala anche a te nei giorni difficili, così la continuità non dipenderà da condizioni perfette.",
    "Controlla se stai usando la consapevolezza per rimandare una decisione. Capire meglio è utile finché cambia la qualità del passo; oltre un certo punto può diventare protezione dall’incertezza. Stabilisci quale informazione manca davvero e quando deciderai anche se non arriverà. L’attenzione matura include il momento in cui smettiamo di osservare e assumiamo una conseguenza.",
    "Concedi al corpo un gesto di chiusura: bere, respirare vicino a una finestra, camminare o cambiare stanza. Non è una ricompensa, ma un modo per segnare che l’esperimento è finito. Le pratiche senza confine possono occupare mentalmente l’intera giornata. Chiuderle permette alle intuizioni di depositarsi senza diventare ruminazione.",
    "Se hai ricevuto uno sguardo esterno, annota anche ciò che l’altra persona non poteva vedere. Il confronto è prezioso ma parziale: nessuno conosce interamente intenzioni, limiti e storia. Integra la sua osservazione senza consegnarle l’autorità sulla tua identità. Cerca il punto in cui il suo esempio incontra un fatto che riconosci direttamente.",
    "Prepara un ostacolo probabile e una risposta minima. Se manca tempo, quale versione dura cinque minuti? Se dimentichi, quale segnale ti farà tornare? Se provi vergogna, con chi puoi parlarne? Anticipare non elimina l’imprevisto, ma evita che la prima difficoltà venga interpretata come prova che il cambiamento non è adatto a te.",
    "Lascia infine una riga bianca nel quaderno. È uno spazio intenzionale per ciò che non sai ancora nominare. Tornandoci, potresti non aggiungere nulla oppure trovare una parola diversa. Entrambi gli esiti sono accettabili. Una pratica di attenzione non deve chiudere ogni domanda; deve rendere possibile accorgersi quando la vita offre una risposta inattesa.",
]


def practice_paragraphs(task: str, index: int) -> list[str]:
    return [OPENERS[index].format(task=task), CLOSERS[index], FOLLOWUPS[index]]


def make_chapter(spec: dict) -> dict:
    paragraphs = list(spec["essay"])
    paragraphs.append(
        "Il laboratorio che segue serve a " + spec["focus"] + ". Non è una sfida da completare tutta in fretta. Le nove pratiche possono occupare nove giorni oppure essere distribuite in un mese. Prima di iniziare scegli una misura sostenibile, proteggi la riservatezza delle persone coinvolte e interrompi se l’esercizio apre una sofferenza che richiede un sostegno diverso. Il criterio non è la perfezione: è la qualità delle informazioni che raccogli sulla tua vita reale."
    )
    for index, task in enumerate(spec["tasks"]):
        paragraphs.extend(practice_paragraphs(task, index))
    paragraphs.append(
        "Dopo l’ultima pratica non assegnarti un voto. Cerca invece una differenza tra ciò che pensavi e ciò che hai osservato, poi lascia che produca una scelta limitata. Se non emerge nulla, conserva la domanda e torna a vivere: alcune comprensioni hanno bisogno di incontrare altre esperienze prima di diventare chiare. Il capitolo ha svolto il suo lavoro se ti ha reso meno automatico, non se ti ha fornito una definizione definitiva."
    )
    return {"title": spec["title"], "paragraphs": paragraphs}


PACKAGE = {
    "excerpt": "Una riflessione sulla misura di una vita piena: non soltanto quante esperienze raccogliamo, ma quanta presenza, memoria e libertà portiamo dentro ciò che viviamo.",
    "answer_paragraphs": ANSWER,
    "book_title": "La misura invisibile di una vita piena",
    "book_deck": "Un libro-laboratorio tra esperienza, attenzione, memoria, noia, relazioni e scelta per capire quando la vita si allarga davvero e quando stiamo soltanto accumulando momenti.",
    "book_pages": [make_chapter(spec) for spec in CHAPTERS],
}


GUIDES = [
    {
        "topic": "Come resettare telefono",
        "slug": "come-resettare-telefono-android-iphone",
        "title": "Come resettare un telefono Android o iPhone senza perdere i dati",
        "deck": "Backup, account, ripristino e controlli finali: la procedura sicura per cancellare Android o iPhone prima di ricominciare o cederlo.",
        "sections": [
            ("Prima del reset", [
                "Il ripristino alle impostazioni di fabbrica elimina dal telefono account, applicazioni, fotografie, messaggi e impostazioni locali. Non cancella automaticamente ciò che è già sincronizzato nel cloud, ma può rendere irrecuperabili i file presenti soltanto sul dispositivo. Prima di procedere verifica perché vuoi resettare: per un rallentamento possono bastare riavvio, aggiornamento e spazio libero; per vendere o regalare il telefono, invece, la cancellazione completa è la scelta corretta.",
                "Tieni a portata di mano PIN, password dell’account Google o Apple e, se usi l’autenticazione a due fattori, un secondo dispositivo o i codici di recupero. Dopo il reset Android e iPhone possono chiedere le credenziali del proprietario precedente come protezione antifurto. Assicurati che la batteria sia almeno al 50%, collega il caricatore e non interrompere la procedura. Se il dispositivo appartiene a un’azienda, contatta prima l’amministratore perché potrebbero essere attivi criteri di gestione.",
            ]),
            ("Creare e verificare il backup", [
                "Su Android apri Impostazioni e cerca Backup; il percorso può trovarsi in Google, Sistema oppure Account e backup secondo il produttore. Controlla la data dell’ultimo salvataggio e avviane uno nuovo. Fotografie e video possono essere gestiti separatamente da Google Foto o dal servizio del produttore: apri l’app e verifica che la sincronizzazione sia terminata. Copia su computer i file importanti nelle cartelle Download e Documenti e i dati delle app che non usano il cloud.",
                "Su iPhone apri Impostazioni, tocca il tuo nome, iCloud e Backup iCloud, quindi esegui il backup. In alternativa collega l’iPhone a un Mac o a un PC e crea una copia con Finder, Dispositivi Apple o iTunes secondo il sistema. Se vuoi conservare dati Salute e password in un backup locale, seleziona la cifratura e custodisci la password: senza di essa il backup non può essere ripristinato. Non limitarti a vedere che una copia esiste; controlla data, dimensione e contenuti sincronizzati.",
            ]),
            ("Resettare Android", [
                "I nomi dei menu cambiano, ma di solito il percorso è Impostazioni, Sistema o Gestione generale, Opzioni di ripristino, Cancella tutti i dati oppure Ripristina dati di fabbrica. Leggi l’elenco degli account e dei dati che saranno rimossi. Se stai cedendo il telefono, rimuovi prima l’account Google e gli account del produttore, disattiva le funzioni di localizzazione e togli SIM e scheda microSD. Poi avvia il ripristino, inserisci il PIN e attendi tutti i riavvii.",
                "Se il telefono non si avvia, molti modelli offrono una modalità di recupero tramite una combinazione di tasti, ma la sequenza dipende esattamente da marca e modello. Usa soltanto la pagina di assistenza ufficiale del produttore: una procedura sbagliata può selezionare funzioni diverse o non risolvere il problema. Anche un reset dalla modalità di recupero può attivare la protezione dell’account Google. Se non ricordi le credenziali, recuperale prima; non affidarti a programmi che promettono di aggirare il blocco.",
            ]),
            ("Resettare iPhone", [
                "Su iPhone apri Impostazioni, Generali, Trasferisci o inizializza iPhone, quindi Inizializza contenuto e impostazioni. Il sistema mostra che cosa verrà rimosso e può chiedere il codice del dispositivo e la password dell’account Apple per disattivare Dov’è e il Blocco attivazione. Se usi una eSIM, scegli se conservarla soltanto quando continuerai a usare lo stesso telefono; se lo cedi, segui le indicazioni dell’operatore per trasferire o eliminare il piano.",
                "Se non puoi aprire le Impostazioni, puoi ripristinare l’iPhone da un computer mettendolo in modalità di recupero e usando Finder o l’app Dispositivi Apple. Questa operazione installa nuovamente il sistema e cancella il dispositivo. La combinazione di tasti varia in base al modello, quindi consulta il supporto Apple. Il ripristino non rimuove il Blocco attivazione senza l’account associato: è una protezione intenzionale, non un errore da aggirare.",
            ]),
            ("Controlli finali", [
                "Se il telefono resterà tuo, durante la configurazione collegati a una rete affidabile, accedi con il tuo account e scegli il backup corretto in base a data e modello. Lascialo in carica e connesso al Wi-Fi: applicazioni, fotografie e messaggi possono continuare a scaricarsi per ore. Verifica chiamate, codici di autenticazione, chat, note e file prima di eliminare copie esterne. Reimposta con attenzione impronta, volto, wallet e applicazioni bancarie.",
                "Se devi venderlo o regalarlo, fermati alla schermata iniziale di benvenuto: non configurarlo con un account provvisorio. Controlla dal portale Google o Apple che il dispositivo non risulti più legato al tuo account e rimuovilo, se necessario, seguendo la procedura ufficiale. Togli SIM, microSD, cover e accessori personali. Un reset riuscito protegge i dati, ma il passaggio decisivo è verificare backup e disassociazione prima di consegnare fisicamente il telefono.",
            ]),
        ],
    },
    {
        "topic": "Come trasferire dati da Android a iPhone (e viceversa)",
        "slug": "come-trasferire-dati-android-iphone",
        "title": "Come trasferire dati da Android a iPhone e viceversa",
        "deck": "Contatti, foto, chat e account: come preparare il passaggio tra Android e iPhone, scegliere il metodo giusto e verificare che nulla manchi.",
        "sections": [
            ("Preparare entrambi i telefoni", [
                "Prima del trasferimento aggiorna i due dispositivi, collegali all’alimentazione e usa una rete Wi-Fi stabile. Controlla che il nuovo telefono abbia spazio sufficiente per i dati che vuoi copiare. Crea comunque un backup separato del vecchio dispositivo: la migrazione non deve essere l’unica copia. Tieni disponibili password Google e Apple, PIN, SIM o dati eSIM e codici di recupero dell’autenticazione a due fattori. Non cancellare il vecchio telefono finché non hai verificato ogni categoria importante.",
                "Decidi quali dati devono davvero passare. Contatti, calendari e posta possono essere già sincronizzati con un account e ricomparire appena lo aggiungi. Fotografie, messaggi, chat, note, registrazioni e file delle app richiedono controlli specifici. Fai un inventario e annota le applicazioni essenziali, soprattutto banca, identità digitale, autenticazione, lavoro e messaggistica. Alcune app non trasferiscono i dati tra sistemi diversi e richiedono esportazione o nuova configurazione.",
            ]),
            ("Da Android a iPhone", [
                "Per un iPhone nuovo o appena inizializzato, durante la configurazione scegli Trasferisci dati da Android. Sul telefono Android installa l’app ufficiale Passa a iOS dal Play Store, accetta le autorizzazioni e inserisci il codice mostrato dall’iPhone. I dispositivi creano una connessione temporanea; seleziona i contenuti disponibili e lasciali vicini, alimentati e inutilizzati fino al completamento. Anche se Android sembra aver terminato, attendi che la barra sull’iPhone sia conclusa.",
                "La procedura può trasferire contatti, cronologia dei messaggi, fotografie, video, calendari, account di posta e altri dati compatibili; la disponibilità può variare. Le app gratuite presenti su entrambi gli store vengono proposte per il nuovo download, ma accessi e dati interni non sono sempre inclusi. Se l’iPhone è già configurato, Passa a iOS richiede normalmente di inizializzarlo: valuta se conviene ricominciare oppure trasferire manualmente le singole categorie.",
            ]),
            ("Da iPhone ad Android", [
                "Durante la configurazione di molti telefoni Android puoi collegare l’iPhone con un cavo compatibile e seguire la procedura Copia app e dati. Sblocca l’iPhone, autorizza la connessione e scegli ciò che vuoi copiare. Alcuni produttori offrono applicazioni ufficiali che possono trasferire categorie aggiuntive. Usa sempre l’app preinstallata o indicata nel supporto del produttore, evitando programmi di terzi che chiedono accesso completo senza una politica chiara.",
                "Prima di spostare la SIM, disattiva iMessage e FaceTime nelle Impostazioni dell’iPhone, così i nuovi SMS non continueranno a essere indirizzati al servizio Apple. Se non possiedi più l’iPhone, Apple mette a disposizione una procedura online per annullare la registrazione del numero. Dopo il passaggio verifica che i messaggi normali arrivino su Android. Per fotografie e file puoi anche usare un servizio cloud comune o una copia su computer, soprattutto quando la migrazione via cavo si interrompe.",
            ]),
            ("Chat e autenticazione", [
                "WhatsApp offre procedure ufficiali per migrare le chat tra Android e iPhone, ma in genere devono essere eseguite durante la configurazione del nuovo dispositivo e con requisiti precisi di versione, numero e collegamento. Segui le istruzioni nell’app e nel centro assistenza aggiornato; un normale backup Google Drive non si ripristina direttamente su iCloud e viceversa. Non cancellare WhatsApp dal vecchio telefono finché non vedi chat e allegati sul nuovo.",
                "Le applicazioni di autenticazione meritano priorità. Alcune sincronizzano i codici con un account, altre richiedono esportazione, QR di trasferimento o nuova registrazione servizio per servizio. Prima di cambiare telefono genera e conserva i codici di recupero degli account importanti. Wallet, carte, SPID, app bancarie e profili aziendali quasi sempre richiedono una nuova verifica per ragioni di sicurezza. Completa queste attivazioni mentre puoi ancora ricevere conferme sul vecchio dispositivo.",
            ]),
            ("Verificare il passaggio", [
                "Confronta i telefoni categoria per categoria: numero di contatti, eventi futuri del calendario, album fotografici, video, messaggi, note, file scaricati e chat principali. Apri alcuni elementi anziché controllare soltanto che le icone esistano. Verifica chiamate, SMS, posta e notifiche. Se usi fotografie ottimizzate nel cloud, assicurati che gli originali siano accessibili e non soltanto anteprime. Lascia il vecchio telefono intatto per qualche giorno, spento e custodito, se la sicurezza lo consente.",
                "Quando sei certo che tutto funzioni, scollega account e dispositivi fidati che non userai più, trasferisci o rimuovi SIM ed eSIM e ripristina il vecchio telefono alle impostazioni di fabbrica se lo cedi. Conserva il backup finché non hai superato almeno un ciclo normale di utilizzo del nuovo dispositivo. Una migrazione riuscita non è quella che termina più velocemente, ma quella in cui dati, accessi e comunicazioni sono stati verificati prima di cancellare l’unica copia rimasta.",
            ]),
        ],
    },
]


def metrics() -> dict:
    book = " ".join(p for page in PACKAGE["book_pages"] for p in page["paragraphs"])
    return {
        "answer_chars": len(" ".join(ANSWER)),
        "book_words": len(re.findall(r"\S+", book)),
        "book_chars": len(book),
        "guide_chars": {
            guide["slug"]: len(" ".join(p for _, paragraphs in guide["sections"] for p in paragraphs))
            for guide in GUIDES
        },
    }
