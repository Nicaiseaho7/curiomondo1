"""Contenuti del pacchetto quotidiano CurioMondo v679."""

import re


ANSWER = [
    "Una paura può chiamarsi prudenza quando indica un pericolo plausibile e ci aiuta a scegliere una protezione proporzionata. Diventa più difficile riconoscerla quando il nome serve soprattutto a salvare la nostra immagine: dire «sono prudente» suona ragionevole, mentre ammettere «ho paura di fallire, essere rifiutato o perdere controllo» ci espone. La vergogna non inventa necessariamente il rischio, ma può impedirci di misurarlo con onestà.",
    "La prudenza raccoglie informazioni, confronta conseguenze e decide un limite. La paura travestita, invece, tende a cercare soltanto conferme, rinvia senza stabilire condizioni e allarga progressivamente la zona da evitare. La differenza non sta nel fatto che una faccia sentire calmi e l’altra agitati: anche una decisione prudente può nascere con il cuore accelerato. Conta se, dopo aver valutato, sappiamo spiegare quale rischio stiamo riducendo e quale prezzo accettiamo di pagare.",
    "In alcune situazioni evitare è sensato: una relazione violenta, un investimento incomprensibile, una strada insicura, un compito per cui mancano competenze essenziali. Non ogni sfida merita coraggio e non ogni esitazione va superata. Ma se la minaccia principale è il giudizio, l’imperfezione o la possibilità di scoprire che non controlliamo tutto, la prudenza può diventare un nome rispettabile dato all’immobilità.",
    "Un test utile è rendere la scelta verificabile. Che cosa dovrebbe cambiare per permetterci di agire? Quale informazione manca davvero? Quale passo piccolo e reversibile possiamo provare senza ignorare la sicurezza? Se nessuna risposta sarebbe mai sufficiente, probabilmente non stiamo ancora valutando un rischio: stiamo proteggendo noi stessi dall’esperienza emotiva dell’incertezza.",
    "Raccontare la paura senza vergogna non significa obbedirle né disprezzarla. Significa darle un nome preciso, riconoscere che cosa tenta di difendere e poi decidere con tutti i dati disponibili. La prudenza migliore non cancella il timore: lo ascolta, gli assegna il posto che merita e impedisce che, nascosto dietro una parola ragionevole, scelga silenziosamente l’intera direzione della nostra vita.",
]


CHAPTERS = [
    {
        "title": "La paura che vuole proteggerci",
        "focus": "riconoscere la funzione protettiva della paura senza concederle automaticamente il comando",
        "essay": [
            "La paura non è un difetto aggiunto alla persona: è un sistema di allarme. Accelera il corpo, restringe l’attenzione e prepara a fuggire, fermarsi o difendersi. Questa rapidità è preziosa davanti a un pericolo immediato, ma la vita quotidiana presenta minacce più ambigue: un colloquio, una conversazione difficile, una scelta economica, la possibilità di essere giudicati. L’allarme si attiva prima che abbiamo distinto un danno concreto da una ferita all’immagine di noi stessi.",
            "Chiamare la paura per nome può sembrare una resa. In realtà apre una distanza tra il segnale e la decisione. Dire «temo che questa persona mi umili» è diverso da «questa persona è sicuramente pericolosa»; dire «ho paura di non essere capace» è diverso da «non sono pronto». La prima formula descrive un’esperienza interna, la seconda trasforma l’esperienza in verdetto. Finché le confondiamo, la protezione appare come unica realtà possibile.",
            "La funzione della paura si comprende chiedendo che cosa tenta di preservare. Talvolta protegge il corpo, il denaro necessario, un legame, la reputazione professionale o la stabilità dei figli. Talvolta difende il diritto di non sentirsi inesperti, dipendenti o rifiutati. Questi beni non hanno lo stesso peso. Una valutazione adulta non ridicolizza nessuno di essi, ma evita di trattare ogni disagio come se fosse una minaccia alla sopravvivenza.",
            "Ascoltare la paura non significa eseguire il primo ordine che impartisce. Un allarme antincendio merita attenzione anche quando è stato attivato dal vapore: controlliamo, non incendiamo la casa per dimostrare coraggio e non ignoriamo il suono per orgoglio. Allo stesso modo possiamo raccogliere informazioni, abbassare l’attivazione e scegliere una risposta proporzionata. La paura offre dati grezzi; la decisione richiede contesto, valori e conseguenze.",
            "Il primo passo verso la prudenza autentica è quindi una frase semplice: ho paura di qualcosa, e voglio capire di che cosa. Questa ammissione conserva dignità perché non promette né fuga né eroismo. Permette di distinguere ciò che deve essere protetto da ciò che può essere attraversato. Il coraggio non comincia con l’assenza di paura, ma con la fine del bisogno di mascherarla per sentirci persone ragionevoli.",
        ],
        "tasks": [
            "scegli una decisione rimandata e completa per dieci volte la frase «ho paura che», senza usare la parola prudenza",
            "descrivi l’ultimo momento in cui il corpo ha dato un allarme e separa sensazioni, fatti e interpretazioni",
            "individua il bene che la tua paura tenta di proteggere e valuta quanto sarebbe davvero compromesso",
            "trasforma un giudizio assoluto sul futuro in tre scenari: probabile, possibile e remoto",
            "chiedi a una persona fidata che cosa vede nella situazione senza domandarle se sei coraggioso",
            "ricostruisci un’occasione in cui la paura ti ha protetto e una in cui ti ha ristretto inutilmente",
            "nomina una protezione concreta che ridurrebbe il rischio senza eliminare ogni incertezza",
            "osserva per una giornata quante volte usi parole razionali per evitare di dire che sei spaventato",
            "scrivi una decisione provvisoria che riconosca sia il segnale della paura sia il valore che vuoi difendere",
        ],
    },
    {
        "title": "Che cosa rende prudente una scelta",
        "focus": "costruire criteri di prudenza basati su probabilità, gravità, reversibilità e responsabilità",
        "essay": [
            "La prudenza non coincide con il comportamento meno rischioso. Restare sempre fermi riduce alcuni pericoli e ne crea altri: occasioni perdute, dipendenza, competenze mai sviluppate, relazioni lasciate deteriorare. Una scelta prudente considera l’intero campo delle conseguenze, comprese quelle del non agire. Per questo può condurre a dire no, a prepararsi meglio oppure a muoversi nonostante il timore.",
            "Quattro domande aiutano a darle struttura. Quanto è probabile il danno? Quanto sarebbe grave? La scelta è reversibile? Chi oltre a me ne sopporterà gli effetti? Un evento raro ma catastrofico merita cautele diverse da un esito frequente ma lieve. Un esperimento facilmente interrompibile non richiede la stessa certezza di una decisione irreversibile. E ciò che rischiamo per noi non può essere automaticamente imposto ad altri.",
            "La prudenza ha bisogno di informazioni sufficienti, non infinite. Cercare dati può essere cura; può anche diventare un modo elegante per rinviare. La soglia utile è raggiunta quando le nuove informazioni non cambiano più in modo significativo il piano, ma servono soltanto a calmare temporaneamente l’ansia. Stabilire prima che cosa dobbiamo sapere impedisce alla ricerca di trasformarsi in un corridoio senza uscita.",
            "Una cautela proporzionata lascia sempre intravedere il passo successivo. Se non siamo pronti oggi, possiamo dire quale competenza, risorsa, consenso o protezione renderebbe possibile decidere domani. La paura mascherata tende invece a spostare la condizione ogni volta che viene raggiunta. Il problema non è attendere: è attendere senza un criterio capace di dichiarare conclusa l’attesa.",
            "Essere prudenti significa infine rispondere delle conseguenze. Non possiamo controllarle tutte, ma possiamo spiegare il processo: quali dati abbiamo considerato, quali persone consultato, quale rischio accettato e quale limite rispettato. Questa tracciabilità non rende infallibili. Riduce però la tentazione di riscrivere dopo la scelta la storia, chiamando coraggio ciò che è stato impulso o prudenza ciò che è stato evitamento.",
        ],
        "tasks": [
            "costruisci una tabella con probabilità, gravità, reversibilità e persone coinvolte per una scelta reale",
            "elenca i rischi dell’agire e quelli del non agire usando lo stesso livello di precisione",
            "definisci le tre informazioni davvero necessarie prima di decidere e una data oltre la quale smetterai di cercare",
            "riduci una decisione grande a un esperimento reversibile che produca dati senza fingere che sia già la scelta finale",
            "chiedi a una persona competente quale cautela considera essenziale e quale invece ritiene eccessiva",
            "verifica se stai proteggendo soltanto te stesso oppure se conseguenze e costi ricadono anche su altri",
            "scrivi la condizione concreta che renderebbe possibile un sì e controlla se l’hai già spostata in passato",
            "immagina di dover spiegare il processo tra un anno, indipendentemente dall’esito, e nota che cosa manca",
            "formula una decisione proporzionata che includa limite, piano di uscita e momento di revisione",
        ],
    },
    {
        "title": "Il corpo non è un oracolo",
        "focus": "leggere le sensazioni fisiche come segnali importanti senza trasformarle in prove assolute",
        "essay": [
            "La paura parla spesso attraverso il corpo prima che compaiano le parole: stomaco contratto, respiro corto, calore, tremore, bisogno di allontanarsi. Questi segnali sono reali anche quando il pericolo interpretato non lo è. Dire che è tutto nella testa svaluta l’esperienza; dire che il corpo sa sempre la verità le attribuisce un’autorità che non possiede. Il corpo registra minaccia, non emette sentenze sul mondo.",
            "Una stessa sensazione può accompagnare situazioni diverse. L’accelerazione precede un incidente evitato, ma anche un discorso pubblico, una dichiarazione d’amore o il primo giorno in un ruolo desiderato. Il significato emerge dal contesto. Se interpretiamo ogni attivazione come ordine di fermarci, abbandoniamo anche possibilità importanti. Se la ignoriamo sistematicamente, perdiamo informazioni su stanchezza, confini e pericoli che il ragionamento sta minimizzando.",
            "Regolare il corpo prima di decidere non serve a cancellare la paura. Serve a recuperare un campo visivo più ampio. Respirare più lentamente, camminare, bere, dormire o allontanarsi per pochi minuti può cambiare l’intensità dell’allarme. Una decisione rimasta identica dopo la regolazione ha un peso diverso da quella presa nel picco. Se invece la calma fa apparire alternative nuove, abbiamo scoperto che l’urgenza stava restringendo la valutazione.",
            "Alcune reazioni sono legate a esperienze precedenti. Un tono, un luogo o una dinamica possono riattivare una protezione appresa quando era necessaria. Non è una debolezza e non va forzata con esercizi improvvisati. Quando l’allarme è intenso, ricorrente o collegato a trauma, un sostegno competente può aiutare a distinguere presente e passato senza esporre la persona a un rischio ulteriore.",
            "La prudenza corporea nasce dall’integrazione. Ascoltiamo il segnale, controlliamo i fatti, valutiamo le risorse e decidiamo il passo. A volte il risultato sarà un no netto; altre volte una preparazione o un avvicinamento graduale. L’obiettivo non è diventare impassibili, ma impedire che una sensazione venga umiliata oppure incoronata. Può sedere al tavolo della decisione senza occupare tutti i posti.",
        ],
        "tasks": [
            "mappa dove senti la paura nel corpo e descrivi intensità, durata e cambiamento senza interpretarla subito",
            "confronta la stessa scelta dopo sonno, movimento e una pausa per capire quanto l’attivazione modifichi il giudizio",
            "ricorda tre situazioni diverse che hanno prodotto una sensazione fisica simile e confrontane gli esiti",
            "crea una sequenza di regolazione breve da usare prima delle decisioni che non richiedono risposta immediata",
            "nota quale segnale corporeo tendi a ignorare e quale invece trasformi troppo rapidamente in certezza",
            "racconta a una persona sicura ciò che senti senza chiederle di convincerti che non esiste alcun pericolo",
            "distingui una situazione che richiede esposizione graduale da una che richiede distanza e protezione",
            "stabilisci quando una reazione intensa merita sostegno professionale invece di un esperimento solitario",
            "ripeti la valutazione quando il corpo è più regolato e annota ciò che resta vero in entrambe le condizioni",
        ],
    },
    {
        "title": "La vergogna costruisce alibi eleganti",
        "focus": "separare la dignità personale dal bisogno di apparire sempre lucidi, forti e coerenti",
        "essay": [
            "La vergogna non dice soltanto che proviamo paura; suggerisce che la paura riveli qualcosa di indegno su di noi. Temiamo di apparire fragili, inesperti, poco ambiziosi o dipendenti. Per evitare questo giudizio cerchiamo parole più rispettabili: realismo, standard, tempismo, razionalità. Queste parole possono descrivere ragioni vere, ma diventano alibi quando servono soprattutto a impedire che qualcuno veda la nostra vulnerabilità.",
            "L’alibi funziona anche davanti a noi stessi. Se ammettiamo di aver paura, dobbiamo decidere che cosa farne; se dichiariamo che la scelta è semplicemente insensata, la questione sembra chiusa. Così proteggiamo coerenza e autostima al prezzo di perdere informazioni. Non sappiamo più se stiamo difendendo un valore o evitando una sensazione. La lingua elegante rende l’immobilità difficile da discutere.",
            "La vergogna cresce nelle culture che premiano invulnerabilità e prestazione. Alcuni ambienti ridicolizzano l’esitazione, penalizzano l’errore e confondono velocità con competenza. In quei contesti nascondere la paura può essere una strategia di sopravvivenza sociale. La soluzione non è confessarsi indiscriminatamente, ma trovare luoghi e persone in cui l’incertezza possa essere nominata senza diventare un’arma.",
            "Parlare senza vergogna richiede precisione. Non serve dichiararsi codardi né raccontare tutto a tutti. Possiamo dire: temo questo esito, non so quanto sia probabile, ho bisogno di questa informazione e intanto scelgo questo limite. La precisione riduce il teatro dell’identità. Non siamo la nostra paura; siamo persone che stanno valutando una situazione con un sistema di allarme attivo.",
            "Quando la paura viene accolta senza umiliazione, spesso diventa più negoziabile. Non deve più gridare per essere riconosciuta né nascondersi dietro argomenti assoluti. Possiamo ringraziarla per la protezione tentata e contraddirla quando esagera. La dignità non dipende dall’essere sempre coraggiosi. Dipende anche dalla capacità di dire la verità su ciò che ci muove, senza usarla come scusa e senza trasformarla in colpa.",
        ],
        "tasks": [
            "raccogli le parole rispettabili con cui presenti una rinuncia e traduci ciascuna nella paura che potrebbe contenere",
            "scrivi che cosa temi che gli altri concludano su di te se ammettessi apertamente l’esitazione",
            "individua un ambiente in cui mostrare incertezza ha avuto un costo reale e uno in cui è stata accolta",
            "scegli una persona sicura e formula una frase precisa che nomini paura, dato mancante e limite attuale",
            "osserva quando giudichi la paura altrui e verifica quale immagine di forza stai difendendo",
            "sostituisci un’etichetta sul carattere con la descrizione di una situazione, una sensazione e una scelta",
            "ricorda un errore commesso per apparire sicuro e individua quale ammissione avrebbe ridotto il rischio",
            "decidi quali paure possono essere condivise, con chi e quali invece richiedono riservatezza o protezione",
            "scrivi una risposta rispettosa alla parte di te che teme di perdere valore se viene vista in difficoltà",
        ],
    },
    {
        "title": "L’evitamento che si allarga",
        "focus": "vedere quando una protezione temporanea restringe progressivamente autonomia, relazioni e possibilità",
        "essay": [
            "Evitare produce sollievo immediato. La riunione viene cancellata, la telefonata rimandata, il viaggio escluso: l’allarme scende e il cervello registra che la fuga ha funzionato. Questo apprendimento è potente. Alla prossima occasione la minaccia appare ancora più credibile, perché non abbiamo raccolto dati contrari. Una prudenza nata come pausa può trasformarsi lentamente in confine permanente.",
            "L’allargamento è spesso discreto. Non evitiamo soltanto il luogo difficile, ma anche quelli simili; non soltanto una conversazione, ma ogni tema che potrebbe condurvi; non soltanto un rischio economico, ma qualunque progetto richieda incertezza. La vita si organizza intorno alla prevenzione dell’allarme. Da fuori può sembrare ordine; dall’interno richiede energie crescenti per mantenere lontano ciò che potrebbe attivarlo.",
            "Non ogni evitamento va contrastato. Allontanarsi da violenza, manipolazione o condizioni insicure è protezione, non esercizio mancato. La distinzione riguarda l’effetto nel tempo: il confine aumenta sicurezza e libertà oppure chiede rinunce sempre più ampie senza ridurre davvero il pericolo? Una protezione efficace crea spazio per vivere; una gabbia protettiva consuma lo spazio che prometteva di difendere.",
            "Per interrompere l’allargamento non serve sempre un gesto enorme. Un passo piccolo, reversibile e sufficientemente sicuro può fornire nuove informazioni. L’obiettivo non è resistere finché l’ansia sparisce, né dimostrare forza. È verificare una previsione: che cosa accade davvero, quali risorse funzionano, dove il limite resta necessario. Se la situazione supera le capacità o coinvolge trauma, l’esperimento va progettato con sostegno competente.",
            "La domanda decisiva è quale vita la prudenza sta rendendo possibile. Se protegge salute, dignità e relazioni, merita rispetto. Se ogni mese richiede un’altra rinuncia e nessuna condizione sarebbe abbastanza sicura, la paura probabilmente ha iniziato a governare in segreto. Nominarlo non obbliga a correre. Permette di riaprire, con gradualità, una porta che il sollievo aveva trasformato in muro.",
        ],
        "tasks": [
            "disegna la mappa di una rinuncia iniziale e delle rinunce successive che sono nate per sostenerla",
            "misura il sollievo subito dopo un evitamento e il costo che compare un giorno e una settimana più tardi",
            "distingui un confine che aumenta libertà da uno che richiede controlli e restrizioni sempre maggiori",
            "scegli un passo minimo e reversibile che verifichi una previsione senza ignorare la sicurezza",
            "definisci in anticipo i segnali per continuare, fermarti o chiedere aiuto durante l’esperimento",
            "coinvolgi una persona capace di accompagnare senza spingere, giudicare o sostituirsi alla tua decisione",
            "ricostruisci un evitamento che sembrava definitivo e che in passato sei riuscito a ridimensionare",
            "calcola quanta energia spendi per impedire l’allarme e che cosa potresti fare con una parte di quella energia",
            "stabilisci un’area da proteggere e una da riaprire gradualmente nei prossimi trenta giorni",
        ],
    },
    {
        "title": "Rischio, controllo e incertezza",
        "focus": "accettare la parte di futuro che nessun piano può rendere certa senza rinunciare alla preparazione",
        "essay": [
            "Molte paure diventano prudenza apparente perché chiediamo alla decisione una garanzia impossibile. Vorremmo sapere che una relazione durerà prima di aprirci, che un lavoro riuscirà prima di candidarci, che una scelta non provocherà rimpianto prima di compierla. Le informazioni riducono l’incertezza, ma non la eliminano. Quando la soglia richiesta è la certezza, ogni rinvio può sembrare razionale.",
            "Il controllo offre benefici reali: pianificare, assicurarsi, preparare alternative e verificare contratti riduce danni evitabili. Diventa problematico quando non serve più alla realtà, ma a impedire qualunque esperienza di vulnerabilità. Allora moltiplichiamo liste, conferme e simulazioni senza sentirci più pronti. Il piano non è più una mappa per agire; è un rituale che deve tenerci lontani dalla possibilità di essere sorpresi.",
            "Accettare incertezza non significa affidarsi al caso. Significa stabilire quanto possiamo sapere, predisporre risorse e assumere che una parte dell’esito resterà aperta. Questa assunzione è diversa dall’ottimismo. Possiamo riconoscere che qualcosa potrebbe andare male e scegliere comunque perché il valore dell’azione, la reversibilità e le protezioni rendono il rischio sostenibile.",
            "Il bisogno di controllo aumenta quando le conseguenze passate ci hanno colti senza sostegno. Per questo non va deriso. Costruire una rete, un piano d’uscita e una riserva può essere il modo corretto di rendere l’incertezza abitabile. La prudenza non pretende di non dipendere da nessuno; riconosce invece quali dipendenze sono affidabili e quali risorse devono essere disponibili se il futuro prende una direzione diversa.",
            "Ogni scelta significativa contiene una quota di fiducia: nelle capacità, nelle persone, nelle istituzioni o nella possibilità di adattarsi. Non è fede cieca, ma disponibilità a procedere senza possedere l’intero percorso. La paura chiede spesso di vedere la fine prima del primo passo. La prudenza risponde mostrando il tratto visibile, le protezioni e il punto in cui sarà possibile fermarsi per guardare di nuovo.",
        ],
        "tasks": [
            "elenca ciò che puoi controllare, influenzare e soltanto osservare in una decisione che ti preoccupa",
            "individua quale certezza stai aspettando e verifica se potrebbe esistere davvero prima dell’azione",
            "riduci un rituale di controllo e misura se cambia il rischio concreto oppure soltanto l’ansia percepita",
            "prepara un piano d’uscita realistico senza usarlo per immaginare ogni possibile catastrofe",
            "nomina le persone e le risorse su cui potresti contare se l’esito fosse meno favorevole del previsto",
            "scegli una decisione reversibile e agisci con informazioni sufficienti invece di cercare conferma infinita",
            "ricorda un imprevisto che hai saputo affrontare e identifica le capacità reali che lo hanno reso possibile",
            "scrivi che cosa accetteresti di non sapere per proteggere un valore più importante del controllo",
            "definisci il prossimo tratto visibile del percorso e il punto esatto in cui rivaluterai la direzione",
        ],
    },
    {
        "title": "Paura nelle relazioni e nei conflitti",
        "focus": "proteggere confini e dignità senza usare la prudenza per evitare ogni confronto necessario",
        "essay": [
            "Nelle relazioni la prudenza è complessa perché il rischio non dipende soltanto da noi. Una conversazione può portare chiarezza, rifiuto, manipolazione o riparazione. Evitarla conserva una pace temporanea, ma può lasciare crescere risentimento e distanza. Affrontarla senza preparazione può invece esporre a un danno prevedibile. La domanda non è se parlare sempre, ma in quali condizioni la parola è sufficientemente sicura e utile.",
            "Un conflitto ordinario e una dinamica abusiva non sono la stessa cosa. Nel primo esiste spazio per dissentire, fermarsi e tornare; nella seconda l’altra persona usa paura, controllo, minacce o punizioni per restringere la libertà. Nessun esercizio di coraggio obbliga a confrontare da soli chi è violento. Cercare distanza, documentare, coinvolgere servizi e persone fidate può essere la forma più lucida di prudenza.",
            "Quando la sicurezza di base esiste, la paura può concentrarsi sul giudizio: essere considerati difficili, deludere, perdere approvazione. Chiamare prudenza il silenzio evita il disagio, ma assegna all’altra persona il compito di intuire bisogni e limiti. Nel tempo il rapporto si fonda su una versione incompleta di noi. Dire qualcosa di vero comporta un rischio; non dirlo comporta il rischio di restare presenti soltanto in apparenza.",
            "Preparare un confronto significa scegliere momento, obiettivo e linguaggio. Possiamo descrivere fatti, effetti e richieste senza diagnosticare il carattere dell’altro. Possiamo stabilire un limite e cosa faremo se non verrà rispettato. Non controlliamo la risposta, ma possiamo controllare quanto esporci, dove parlare e quale sostegno avere dopo. La prudenza costruisce condizioni; la paura travestita aspetta che la possibilità di ferita scompaia del tutto.",
            "Una relazione sana non richiede assenza di timore. Offre prove ripetute che la verità può essere ascoltata, anche quando non viene accolta subito. Se ogni parola autentica mette a rischio il legame, il problema potrebbe non essere il nostro coraggio. Distinguere questi casi evita due errori opposti: restare in silenzio quando un confronto sarebbe possibile e forzarsi a parlare dove la protezione richiede distanza.",
        ],
        "tasks": [
            "valuta una relazione distinguendo disaccordo, paura del giudizio e segnali concreti di controllo o violenza",
            "scrivi l’obiettivo di una conversazione difficile in una frase che non dipenda dal cambiare l’altra persona",
            "prepara fatti, effetti, bisogno e richiesta evitando accuse globali sul carattere",
            "scegli luogo, durata e possibilità di interrompere il confronto se la sicurezza o il rispetto vengono meno",
            "definisci un confine come comportamento che adotterai, non come minaccia destinata a controllare l’altro",
            "chiedi sostegno prima e dopo una conversazione senza affidare a terzi la decisione che ti appartiene",
            "riconosci un silenzio che protegge davvero e uno che mantiene soltanto una pace apparente",
            "osserva la risposta a un limite piccolo prima di aumentare vulnerabilità o dipendenza",
            "decidi se il passo prudente sia parlare, attendere con una condizione chiara oppure creare distanza",
        ],
    },
    {
        "title": "Quando la paura nasce dalla storia",
        "focus": "onorare le protezioni apprese nel passato e aggiornarle con gradualità alle condizioni presenti",
        "essay": [
            "Le paure non nascono tutte dalla situazione attuale. Alcune sono memorie operative: il corpo e la mente hanno imparato che un certo tono, un errore, una dipendenza o un cambiamento precedevano un danno. Quella lezione può aver salvato. In seguito, però, la stessa protezione può attivarsi in contesti diversi. Chiamarla semplice irrazionalità cancella la sua origine; chiamarla sempre prudenza impedisce di aggiornarla.",
            "Aggiornare non significa dimostrare che il passato non conta. Significa cercare differenze verificabili: oggi abbiamo più risorse? La persona davanti a noi rispetta i limiti? Possiamo uscire? Esistono testimoni, tutele o alternative che allora mancavano? Il presente non è sicuro soltanto perché è nuovo, ma può offrire condizioni diverse. La paura ha bisogno di vederle attraverso esperienze graduali, non soltanto di sentirsele spiegare.",
            "La gradualità è essenziale. Un passo troppo grande può confermare l’idea che ogni apertura sia pericolosa; uno troppo piccolo può non produrre alcuna informazione nuova. La misura giusta mantiene attivazione tollerabile e possibilità reale di scelta. Non esiste una scala universale. Ciò che per una persona è un gesto ordinario può essere per un’altra un passaggio che richiede preparazione, sostegno e recupero.",
            "Alcune storie chiedono competenza clinica, legale o sociale. Se ci sono trauma, violenza, attacchi di panico, autolesionismo o condizioni che compromettono la vita quotidiana, il libro non sostituisce un professionista né una rete di protezione. Chiedere aiuto non conferma fragilità; aggiunge risorse alla valutazione. La prudenza più matura riconosce quando non è corretto sperimentare da soli.",
            "Possiamo provare gratitudine per una protezione antica e insieme lasciarle un ruolo nuovo. Ha lavorato con le informazioni disponibili; oggi possiamo offrirle dati, confini e alleanze diversi. Il cambiamento non richiede di tradire la persona che siamo stati. Permette a quella persona di scoprire che non deve più affrontare ogni situazione con gli stessi strumenti di allora.",
        ],
        "tasks": [
            "riconosci una protezione appresa e descrivi la situazione in cui aveva una funzione reale",
            "confronta passato e presente attraverso risorse, possibilità di uscita, persone affidabili e tutele disponibili",
            "costruisci una scala di passi dal più sicuro al più impegnativo senza obbligarti a raggiungere l’ultimo",
            "scegli un esperimento con attivazione tollerabile e definisci prima come interromperlo",
            "individua il sostegno professionale, legale o sociale appropriato se il rischio supera l’autoaiuto",
            "nota che cosa succede dopo il passo e concedi tempo di recupero prima di interpretarne il significato",
            "evita di usare un’esperienza positiva per negare il passato o una negativa per dichiarare impossibile il futuro",
            "ringrazia simbolicamente la protezione antica e assegnale un compito più limitato nelle condizioni presenti",
            "formula un criterio di sicurezza aggiornato che possa essere verificato invece di una regola assoluta",
        ],
    },
    {
        "title": "Una prudenza capace di movimento",
        "focus": "trasformare la consapevolezza in un modo stabile di decidere, agire e rivedere le scelte",
        "essay": [
            "La prudenza migliore non promette immobilità né imprese spettacolari. Crea movimento sufficiente a mantenere viva la possibilità di scegliere. A volte quel movimento è un passo avanti; altre volte è una pausa dichiarata, una richiesta di aiuto o un no. Ciò che lo distingue dalla paura nascosta è la presenza di criteri: sappiamo che cosa proteggiamo, che cosa temiamo e quando torneremo a valutare.",
            "Un processo sostenibile può avere cinque passaggi: nominare il timore, verificare i fatti, regolare l’attivazione, scegliere una misura proporzionata e fissare una revisione. Nessun passaggio elimina l’incertezza. Insieme impediscono però che il primo impulso si trasformi in destino. Il processo deve restare leggero: se per ogni decisione costruiamo un tribunale infinito, la prudenza torna a essere una forma di paralisi.",
            "Anche il risultato va letto con cautela. Se una scelta rischiosa riesce, non significa che fosse prudente; se un piano accurato fallisce, non significa che fosse codardo o sbagliato. Valutiamo la qualità delle informazioni e delle protezioni disponibili al momento. Separare processo ed esito rende possibile imparare senza consegnare ogni giudizio alla fortuna.",
            "La revisione cerca segnali concreti. La zona di vita si sta ampliando o restringendo? I confini proteggono o isolano? Le informazioni nuove cambiano davvero il rischio? Le persone coinvolte stanno pagando costi che non avevamo considerato? Rispondere periodicamente evita sia la rigidità sia l’entusiasmo cieco. Una scelta prudente può essere corretta quando il mondo o le nostre risorse cambiano.",
            "Raccontare la paura senza vergogna diventa così una pratica di libertà. Non dobbiamo più dimostrare di non avere timore né obbedire a ogni allarme. Possiamo proteggere ciò che conta e, nello stesso tempo, lasciare che la vita ci raggiunga. La domanda finale non è se siamo stati abbastanza coraggiosi, ma se la nostra cautela ci ha resi più capaci di vedere, decidere e rispondere delle conseguenze.",
        ],
        "tasks": [
            "applica i cinque passaggi a una decisione piccola e osserva dove il processo tende a bloccarsi",
            "scrivi una frase di pausa che includa il motivo, la condizione mancante e la data di revisione",
            "scegli un no che protegge un valore e un sì che accetta un’incertezza proporzionata",
            "valuta una scelta passata separando qualità del processo e fortuna dell’esito",
            "definisci tre segnali che mostrerebbero se la tua vita si sta ampliando o restringendo",
            "condividi i criteri con una persona coinvolta e verifica se i costi sono distribuiti in modo equo",
            "riduci il processo alle domande essenziali per le decisioni quotidiane e conservalo completo per quelle importanti",
            "stabilisci un appuntamento mensile per rivedere confini, evitamenti e passi compiuti senza assegnarti un voto",
            "formula la tua definizione di prudenza come capacità di proteggere e muoversi, non come identità da difendere",
        ],
    },
]


OPENERS = [
    "Prendi un foglio e lavora su un episodio recente, non su come credi di essere in generale. La consegna è questa: {task}. Indica luogo, persone, parole pronunciate e decisione presa. Poi segna con colori diversi ciò che hai osservato, ciò che hai temuto e ciò che hai concluso. Se una frase contiene sempre, mai o sicuramente, riscrivila con una probabilità e un esempio. La precisione non serve a minimizzare l’allarme: serve a impedire che un’impressione diventi l’unica versione possibile dei fatti.",
    "Porta l’esercizio in una situazione abbastanza piccola da restare libera e sicura: {task}. Prima stabilisci durata, limite e modo per interrompere. Durante la prova non chiederti se stai vincendo la paura; osserva che cosa l’allarme prevede e che cosa accade davvero. Registra anche i costi che non avevi immaginato. Alla fine attendi almeno venti minuti prima di giudicare. Il sollievo o l’agitazione immediati sono dati importanti, ma non raccontano da soli se la scelta sia stata utile.",
    "Affronta questa consegna come un’indagine: {task}. Formula prima l’ipotesi che sostiene la paura e poi una spiegazione alternativa che rispetti gli stessi fatti. Cerca un elemento che confermi e uno che contraddica ciascuna versione. Non forzare una conclusione equilibrata se i segnali indicano pericolo reale. Lo scopo è sapere quali prove rendono una protezione necessaria e quali, invece, mostrano che stai reagendo a una possibilità trattata come certezza.",
    "Dedica all’attività trenta minuti e non usarla per prendere subito una decisione definitiva: {task}. Prepara una scala da zero a dieci per intensità, rischio concreto e costo del rinvio. Compilala prima, subito dopo e il giorno seguente. Le tre misure possono divergere. Se l’ansia scende ma il rischio resta alto, la calma non autorizza l’azione; se l’ansia resta alta mentre i fatti risultano sicuri, potresti aver bisogno di gradualità o sostegno, non di altre spiegazioni.",
    "Svolgi la pratica con un linguaggio rispettoso: {task}. Evita codardo, debole, paranoico e qualunque etichetta totale. Descrivi invece che cosa stai proteggendo, quale esito temi e quale risorsa manca. Aggiungi la frase che diresti a una persona amata nella stessa condizione e confrontala con quella che usi per te. La gentilezza non deve cancellare responsabilità o conseguenze; deve creare abbastanza sicurezza interna da poter guardare anche i fatti scomodi senza difenderti con un giudizio sul carattere.",
    "Coinvolgi il corpo senza consegnargli la decisione: {task}. Prima di iniziare nota respiro, tensione, temperatura e impulso principale. Fai una breve azione regolatrice adatta a te, poi ripeti l’osservazione. Se qualcosa cambia, registra quale interpretazione si è modificata; se non cambia, non concludere automaticamente che il pericolo sia certo. Confronta le sensazioni con informazioni, confini e possibilità di uscita. Il corpo segnala la necessità di attenzione, mentre la scelta richiede anche contesto e responsabilità.",
    "Se la situazione coinvolge altre persone, usa questa consegna per preparare un dialogo, non una confessione senza confini: {task}. Decidi che cosa vuoi condividere, con chi e per quale motivo. Chiedi esempi e osservazioni, non un verdetto su chi sei. Ascolta le differenze senza cedere la decisione. Se l’altra persona minimizza, spinge o usa la vulnerabilità contro di te, considera anche questo un dato sulla sicurezza del rapporto. Il confronto utile amplia le informazioni e lascia intatta la tua facoltà di fermarti.",
    "Trasforma l’esercizio in una prova ripetibile: {task}. Scegli un segnale di inizio, una versione minima e una condizione di stop. Esegui il passo in almeno due contesti prima di formulare una regola generale. Una sola esperienza positiva non cancella ogni rischio e una negativa non definisce il futuro intero. Cerca invece quali condizioni cambiano l’esito: tempo, stanchezza, presenza di sostegno, chiarezza dei confini o reversibilità. Sono queste condizioni a rendere la prudenza utilizzabile nella vita reale.",
    "Concludi il ciclo con una decisione temporanea: {task}. Scrivi fino a quando vale, quale segnale richiederà revisione e quale prezzo sei disposto a sostenere. Includi il costo del non agire, spesso invisibile perché distribuito nel tempo. Non promettere di non avere più paura. Definisci soltanto il prossimo comportamento osservabile e una protezione proporzionata. Una decisione limitata può essere più responsabile di una dichiarazione assoluta, perché resta aperta ai dati senza usare l’incertezza come scusa per non iniziare mai.",
]


CLOSERS = [
    "Rileggi ciò che hai scritto e cerchia la frase che contiene più certezza di quanta i fatti permettano. Riscrivila indicando probabilità, fonte e parte ignota. Poi scegli un’informazione che puoi ottenere senza aumentare inutilmente il rischio. Se nessuna informazione cambierebbe la decisione, riconoscilo: potresti avere già un confine valido oppure stare cercando conferme per una conclusione presa dalla paura. Distinguerli richiede guardare gli effetti nel tempo.",
    "Dopo la prova, separa il beneficio della protezione dal sollievo dell’evitamento. Il primo aumenta sicurezza o libertà anche domani; il secondo può svanire e chiedere una rinuncia ulteriore. Scrivi quale dei due hai osservato e con quali segnali. Non correggere subito il piano. Lascia passare una notte, poi verifica se il passo ha ampliato capacità di scelta oppure ha soltanto reso più urgente impedire che la situazione si ripresenti.",
    "Aggiungi una colonna intitolata conseguenze per gli altri. Una cautela personale può spostare lavoro, incertezza o responsabilità su chi ci sta vicino. Questo non rende illegittimo il limite, ma chiede chiarezza e negoziazione. Indica quale costo ti appartiene, quale può essere condiviso e quale non hai diritto di imporre. La prudenza diventa più affidabile quando considera l’intero sistema invece di misurare soltanto la diminuzione della propria ansia.",
    "Formula adesso una condizione sufficiente, non perfetta, per procedere o fermarti. Deve essere osservabile: una somma, una competenza, un consenso, una via d’uscita, un comportamento rispettato. Evita condizioni come sentirmi completamente pronto, perché possono spostarsi all’infinito. Fissa anche il giorno della verifica. Se la condizione sarà raggiunta e nascerà subito un nuovo requisito, trattalo come informazione sul ruolo della paura, non automaticamente come nuovo pericolo.",
    "Conserva una frase che riconosca la funzione protettiva senza obbedienza automatica: capisco che vuoi evitarmi questo dolore, ora controllerò di che cosa abbiamo davvero bisogno. Ripetila soltanto se ti aiuta a rallentare, non come formula magica. Poi compi un gesto concreto di cura: riposo, informazione, confine o richiesta. La paura diventa più ascoltabile quando riceve una risposta specifica invece di essere combattuta o lasciata dirigere l’intera giornata.",
    "Se l’attivazione rimane molto alta, non aumentare la difficoltà per orgoglio. Riduci il passo, torna a una situazione sicura e valuta sostegno. Se invece scende, non interpretare la calma come prova che devi procedere: rivedi comunque i fatti. La regolazione restituisce capacità di scelta; non sostituisce il giudizio. Annota quale intensità ti permette di pensare, comunicare e mantenere i limiti. Quella fascia sarà il riferimento per esperimenti futuri.",
    "Ringrazia chi ha partecipato e chiarisci che cosa farai delle informazioni ricevute. Non promettere un cambiamento totale per ricompensare l’ascolto. Scegli un comportamento verificabile e un momento in cui ne parlerete di nuovo. Se sono emerse pressioni o svalutazioni, proteggi la riservatezza e considera con attenzione quanto affidamento fare sul rapporto. La vulnerabilità è utile soltanto dove non viene trasformata in debito, controllo o spettacolo.",
    "Prepara l’ostacolo più probabile. Se mancherà tempo, quale versione minima resta significativa? Se salirà la paura, quale pausa userai? Se comparirà un rischio reale, come uscirai? Un piano non elimina l’imprevisto, ma impedisce che la prima difficoltà venga usata come prova universale. Dopo ogni ripetizione aggiorna una sola condizione. Cambiarne troppe insieme rende impossibile capire che cosa abbia davvero aumentato sicurezza o libertà.",
    "Scrivi la decisione in una frase che possa essere riletta senza vergogna anche se l’esito sarà diverso da quello sperato. Deve mostrare dati, limite e valore, non prevedere il futuro. Poi smetti di analizzare fino alla data fissata, salvo nuovi fatti importanti. La revisione continua può diventare un’altra forma di controllo. Lascia che la scelta incontri la realtà: soltanto lì produrrà le informazioni che il pensiero, da solo, non può anticipare.",
]


FOLLOWUPS = [
    "Il giorno seguente racconta l’episodio in cento parole senza aggettivi sul carattere. Se la storia diventa meno drammatica, non significa che la paura fosse falsa: significa che hai separato l’esperienza dalla tua identità. Aggiungi poi i dettagli necessari a capire il rischio. Questa doppia versione mostra quali parti appartengono ai fatti e quali al bisogno di spiegare immediatamente che tipo di persona sei.",
    "Ripeti mentalmente la scelta dal punto di vista di chi ne subirà l’effetto più a lungo. Non presumere emozioni o intenzioni: usa soltanto conseguenze osservabili e domande da verificare. Se emerge un costo non considerato, aggiungilo al piano. Se emerge soltanto il timore di essere giudicato, chiamalo per nome. Il giudizio altrui può avere conseguenze reali, ma non deve essere confuso con ogni altro tipo di pericolo.",
    "Cerca un precedente simile ma non identico. Quale differenza di contesto potrebbe cambiare il risultato? Il passato offre dati, non profezie. Scrivi una condizione che allora mancava e che oggi esiste, oppure una vulnerabilità che è ancora presente. Questo confronto aiuta ad aggiornare le protezioni senza negare ciò che hai imparato né costringerti a vivere come se nessuna risorsa fosse mai cambiata.",
    "Riduci l’esercizio alla sua parte essenziale e immagina di proporlo a qualcuno con meno tempo, denaro o sostegno. Se richiede condizioni irrealistiche, riscrivilo. La prudenza non deve diventare privilegio mascherato: un piano valido considera risorse effettive e non colpevolizza chi ne possiede meno. Indica ciò che dipende da te e ciò che richiede una tutela, una persona o un cambiamento collettivo.",
    "Controlla se la comprensione sta rimandando l’azione. Quale dato manca davvero e quale emozione vorresti invece non provare? Stabilire questa differenza evita di usare l’introspezione come rifugio. Se il dato può essere ottenuto, pianifica come. Se resta soprattutto un’emozione, decidi quale quantità sei disposto a attraversare con protezioni adeguate. Non tutto ciò che fa paura necessita di un’altra spiegazione.",
    "Chiudi con un gesto fisico semplice e torna a un’attività ordinaria. Non trascorrere il resto della giornata a sorvegliare come ti senti. La paura può diminuire lentamente e non deve sparire perché l’esperimento abbia valore. Alla verifica successiva domanda se hai mantenuto scelta, confini e capacità di recupero. Questi criteri descrivono meglio la sostenibilità di quanto faccia un singolo picco emotivo.",
    "Se hai chiesto un parere, annota anche ciò che l’altra persona non poteva conoscere: storia, sensazioni, risorse e responsabilità. Integra il suo esempio senza trasformarlo in autorizzazione. Una consulenza competente pesa più di un’opinione casuale sul rischio tecnico; nessuno, però, può decidere interamente il valore che vuoi proteggere. La prudenza usa le competenze altrui e conserva la titolarità della scelta.",
    "Prepara una risposta alla ricaduta. Potresti tornare a evitare, spostare la condizione o cercare conferme. Invece di dichiarare fallito il percorso, identifica il punto esatto in cui hai perso scelta e torna alla versione precedente. La gradualità non procede in linea retta. Diventa affidabile quando include un modo dignitoso di rientrare, senza punizione e senza fingere che il costo non esista.",
    "Lascia una domanda aperta nella nota: quale prova futura potrebbe farmi cambiare idea? Una decisione che non ammette alcun dato contrario rischia di essere identità, non prudenza. Non devi cercare subito quella prova. Sapere che esiste mantiene il confine permeabile alla realtà. Se invece il limite riguarda dignità o sicurezza non negoziabili, scrivi perché non dipende dall’umore né dalla pressione del momento.",
]


def practice_paragraphs(task: str, index: int) -> list[str]:
    return [OPENERS[index].format(task=task), CLOSERS[index], FOLLOWUPS[index]]


def make_chapter(spec: dict) -> dict:
    paragraphs = list(spec["essay"])
    paragraphs.append(
        "Il laboratorio che segue serve a " + spec["focus"] + ". Le nove pratiche non sono una prova di coraggio e non vanno completate tutte insieme. Distribuiscile in nove giorni o in un mese, scegliendo situazioni che non compromettano la sicurezza. Interrompi se emergono violenza, trauma o un livello di attivazione che richiede sostegno competente. Il criterio non è sentirsi impavidi: è raccogliere dati più precisi e aumentare, anche di poco, la possibilità di scegliere."
    )
    paragraphs.append(
        "Prima di ogni pratica annota anche il contesto materiale: tempo disponibile, denaro, salute, obblighi e persone che dipendono dalla decisione. La stessa paura può richiedere risposte diverse quando cambiano le risorse. Questo controllo impedisce di trasformare un esercizio personale in una misura morale universale e ricorda che la prudenza autentica considera la realtà, non soltanto l’intensità con cui desideriamo superare un limite."
    )
    for index, task in enumerate(spec["tasks"]):
        paragraphs.extend(practice_paragraphs(task, index))
    paragraphs.append(
        "Dopo l’ultima pratica non cercare un verdetto sul tuo carattere. Confronta piuttosto la previsione iniziale, i fatti osservati e il costo delle protezioni adottate. Conserva una cautela che aumenta libertà, modifica quella che produce soltanto sollievo immediato e chiedi aiuto quando il rischio supera le risorse disponibili. Il capitolo ha svolto il suo lavoro se paura e prudenza sono diventate più distinguibili, non se ogni incertezza è scomparsa."
    )
    return {"title": spec["title"], "paragraphs": paragraphs}


PACKAGE = {
    "excerpt": "Una riflessione sul confine tra paura e prudenza: come proteggersi con lucidità senza usare la cautela per nascondere vergogna, evitamento e bisogno di controllo.",
    "answer_paragraphs": ANSWER,
    "book_title": "Il nome onesto della paura",
    "book_deck": "Un libro-laboratorio per distinguere allarme, rischio e prudenza, costruire protezioni proporzionate e scegliere senza dover fingere di non avere paura.",
    "book_pages": [make_chapter(spec) for spec in CHAPTERS],
}


def metrics() -> dict:
    book = " ".join(p for page in PACKAGE["book_pages"] for p in page["paragraphs"])
    return {
        "answer_chars": len(" ".join(ANSWER)),
        "book_words": len(re.findall(r"\S+", book)),
        "book_chars": len(book),
        "chapters": len(PACKAGE["book_pages"]),
    }
