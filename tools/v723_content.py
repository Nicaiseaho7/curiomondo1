"""Contenuti eBook Domanda del giorno del 1 ottobre 2026."""

import re


CHAPTERS = [
    {
        "title": "La libertà non nasce fuori dalle relazioni",
        "lens": "riconoscere che ogni scelta personale avviene dentro legami, promesse e dipendenze reali",
        "risk": "confondere l’autonomia con l’assenza di conseguenze per chi ci vive accanto",
        "principle": "una scelta è più libera quando vede i legami senza fingere che non esistano e conserva una voce propria dentro di essi",
        "essay": [
            "La libertà viene spesso immaginata come una stanza vuota: nessuna pressione, nessuna aspettativa, nessuno da deludere. La vita reale comincia invece in mezzo a relazioni già presenti. Dipendiamo da cure ricevute, accordi economici, responsabilità e parole date. Scegliere non significa cancellare questa rete, ma capire quali fili esprimono reciprocità e quali trattengono una parte della nostra vita senza essere mai stati discussi.",
            "L’amore modifica legittimamente le decisioni. Rinunciare a una serata per assistere una persona malata o coordinare un trasferimento con il partner non è automaticamente mancanza di libertà. Possiamo desiderare di prenderci cura. Il problema nasce quando l’unica prova d’amore ammessa è la rinuncia silenziosa, oppure quando ogni preferenza diversa viene interpretata come abbandono.",
            "Una scelta relazionale contiene almeno tre domande: che cosa voglio, che cosa devo davvero e che cosa temo accada se dico la verità. Le risposte possono sovrapporsi. Separarle permette di non chiamare dovere una paura e di non chiamare autenticità un gesto che scarica sugli altri costi evitabili.",
            "La libertà adulta non promette innocenza. Anche una decisione giusta può dispiacere. Qualcuno può sentirsi escluso, preoccupato o contrariato senza che la nostra scelta diventi per questo sbagliata. Imparare a tollerare una quota di delusione è diverso dal diventare indifferenti: significa non affidare a ogni reazione altrui il potere di veto.",
            "Questo capitolo propone una mappa iniziale. Non cerca una percentuale astratta di libertà, ma osserva dove la nostra voce compare, dove negozia e dove scompare. La qualità di una scelta si vede dal modo in cui riconosce bisogni, informa chi subirà conseguenze e lascia spazio a una revisione senza trasformare l’amore in tribunale.",
        ],
        "actions": [
            "disegnare la rete delle persone che subiranno conseguenze da una decisione attuale",
            "separare in tre colonne desiderio, responsabilità verificabile e paura della reazione",
            "ricordare una rinuncia scelta con libertà e una compiuta soltanto per evitare tensione",
            "descrivere che cosa cambierebbe davvero per gli altri e che cosa riguarda soltanto le loro aspettative",
            "individuare una promessa esplicita che merita fedeltà e un’abitudine mai negoziata",
            "chiedere a una persona cara quale conseguenza concreta teme della nostra scelta",
            "formulare una preferenza senza presentarla come sentenza o richiesta di permesso",
            "stabilire quale costo siamo disposti ad assumerci in prima persona",
            "riconoscere una dipendenza materiale che limita realmente le opzioni disponibili",
            "scrivere una definizione provvisoria di libertà relazionale usando esempi quotidiani",
        ],
    },
    {
        "title": "Desiderio, colpa e bisogno di approvazione",
        "lens": "distinguere ciò che desideriamo dalla strategia usata per evitare colpa, critica o perdita di approvazione",
        "risk": "trattare il disagio emotivo come prova che una decisione personale sia ingiusta",
        "principle": "la colpa è un segnale da interpretare, non un verdetto automatico sul diritto di scegliere",
        "essay": [
            "Quando una scelta delude qualcuno che amiamo, il corpo può reagire prima del pensiero: tensione, urgenza di spiegarsi, desiderio di ritirare la decisione. Questa risposta non dimostra che stiamo facendo male. Può indicare empatia, memoria di vecchi conflitti o paura di perdere appartenenza. Per comprenderla occorre guardare il comportamento e le conseguenze, non soltanto l’intensità dell’emozione.",
            "Esiste una colpa responsabile: compare quando violiamo un impegno, mentiamo o ignoriamo un danno che potevamo evitare. Chiede riparazione. Esiste anche una colpa appresa: appare quando smettiamo di essere disponibili in ogni momento, scegliamo un percorso diverso o non confermiamo l’immagine che la famiglia aveva di noi. Questa seconda forma chiede spesso tolleranza e confini, non obbedienza.",
            "Il bisogno di approvazione è umano. Le persone importanti ci aiutano a capire chi siamo e un loro rifiuto può ferire. La libertà non elimina questo bisogno; impedisce che diventi l’unica fonte di orientamento. Possiamo desiderare un consenso, ascoltare le obiezioni e decidere comunque con criteri che saremmo disposti a spiegare anche se il consenso non arrivasse.",
            "A volte il desiderio personale viene idealizzato. Non ogni impulso merita di essere seguito: può essere transitorio, costoso o incompatibile con responsabilità accettate. La distinzione utile non è tra io e loro, ma tra ragioni. Quali bisogni sono in gioco? Quali accordi esistono? Chi paga? Che cosa può essere modificato? Una scelta libera sopporta domande precise.",
            "Riconoscere la colpa senza inginocchiarsi davanti ad essa apre uno spazio. Possiamo dire: sento che sto deludendo, ma devo ancora capire se sto danneggiando. In quello spazio entrano fatti, proporzioni e alternative. La decisione non diventa facile, ma smette di essere governata dall’urgenza di tornare subito la persona che nessuno rimprovera.",
        ],
        "actions": [
            "annotare le frasi interiori che compaiono quando immaginiamo di dire no",
            "distinguere una colpa che richiede riparazione da una che accompagna soltanto il cambiamento",
            "ricostruire da chi abbiamo imparato che essere amabili significa non creare problemi",
            "descrivere il danno concreto temuto senza usare parole generiche come egoismo",
            "confrontare l’intensità del disagio con la gravità reale delle conseguenze",
            "scrivere una risposta gentile che non cancelli la decisione per ottenere sollievo",
            "individuare un’approvazione desiderata ma non necessaria per procedere",
            "verificare se stiamo chiamando desiderio un impulso che trasferisce costi ingiusti",
            "scegliere una persona capace di offrire realtà invece di assoluzione",
            "definire quale riparazione offrire senza rinunciare automaticamente alla scelta",
        ],
    },
    {
        "title": "Le aspettative familiari che diventano una voce interna",
        "lens": "rendere visibili i copioni ereditati su lavoro, amore, successo, cura e appartenenza",
        "risk": "obbedire a una regola antica anche quando nessuno la sta più chiedendo apertamente",
        "principle": "onorare la propria storia non obbliga a ripeterne ogni soluzione",
        "essay": [
            "Le famiglie trasmettono molto più di regole esplicite. Insegnano che cosa si considera un lavoro serio, quando una relazione è rispettabile, chi deve occuparsi degli altri e quale rischio sia tollerabile. Questi messaggi possono offrire orientamento e protezione. Diventano vincoli opachi quando continuiamo a seguirli senza ricordare che sono interpretazioni nate in condizioni precise.",
            "Un genitore può aver privilegiato la stabilità perché ha conosciuto precarietà; un figlio può trasformare quella prudenza in divieto assoluto di cambiare. Un ideale di sacrificio può aver tenuto unita una casa e poi impedire a qualcuno di chiedere reciprocità. Capire l’origine di una regola permette di rispettarne la funzione senza considerarla eterna.",
            "Deludere un’aspettativa familiare può sembrare un tradimento identitario. Non stiamo soltanto scegliendo un corso di studi o una città: stiamo uscendo dal ruolo di figlio affidabile, persona forte o custode della pace. Per questo le spiegazioni razionali non bastano. Occorre elaborare la perdita del ruolo e costruire un modo nuovo di appartenere.",
            "Anche la ribellione può restare dipendente dal copione. Fare l’opposto di ciò che la famiglia desidera non è ancora libertà se ogni scelta continua a essere definita dal conflitto. L’autonomia cresce quando possiamo selezionare ciò che vogliamo conservare, correggere o lasciare, riconoscendo il debito senza trasformarlo in obbedienza permanente.",
            "Una storia familiare può essere riletta con gratitudine e limite. Possiamo dire: questa regola vi ha protetto, ma oggi produce un costo diverso. Oppure: questa cura mi appartiene ancora, ma non nella forma del sacrificio illimitato. La continuità non dipende dall’identità delle scelte; può vivere nei valori tradotti in condizioni nuove.",
        ],
        "actions": [
            "elencare cinque regole familiari mai pronunciate su successo, denaro e relazioni",
            "collegare ogni regola alla condizione storica che potrebbe averla resa utile",
            "distinguere il valore da conservare dalla soluzione concreta che possiamo cambiare",
            "individuare il ruolo familiare che rischiamo di perdere scegliendo diversamente",
            "osservare una scelta fatta per ribellione e una nata da un criterio personale",
            "chiedere a un familiare quale paura sta dietro una sua aspettativa",
            "scrivere una frase che riconosca la storia senza promettere obbedienza",
            "scegliere una tradizione da continuare in una forma più reciproca",
            "descrivere come vorremmo appartenere alla famiglia senza interpretare sempre lo stesso ruolo",
            "progettare una conversazione che separi gratitudine, decisione e conseguenze",
        ],
    },
    {
        "title": "Cura o controllo: il confine decisivo",
        "lens": "distinguere la preoccupazione che informa dalla pressione che pretende di decidere al posto nostro",
        "risk": "accettare il controllo perché si presenta con il linguaggio dell’amore",
        "principle": "la cura offre presenza, informazioni e aiuto; il controllo condiziona il legame all’obbedienza",
        "essay": [
            "Chi ci ama vede rischi che possiamo ignorare. Una domanda difficile o un consiglio contrario non sono automaticamente controllo. La cura adulta può disturbare, perché ricorda limiti, effetti economici e responsabilità. Il criterio non è quindi sentirsi sempre sostenuti, ma osservare se l’altra persona riconosce che la decisione finale appartiene a chi ne vivrà principalmente le conseguenze.",
            "Il controllo usa spesso strumenti indiretti: silenzio punitivo, minaccia di ritirare affetto, catastrofi ripetute, sorveglianza o ricatto economico. Non discute soltanto una scelta; trasforma la relazione nella posta in gioco. Di fronte a questa pressione, cedere può sembrare pace, ma insegna che il legame funziona soltanto quando una persona scompare.",
            "Esistono zone complesse quando risorse e conseguenze sono condivise. Se una scelta mette a rischio una casa comune o richiede lavoro di cura altrui, le altre persone hanno diritto di negoziare. Questo non significa possedere ogni aspetto della vita reciproca. Significa definire quali decisioni sono individuali, quali richiedono consenso e quali chiedono soltanto informazione.",
            "Anche noi possiamo controllare mentre crediamo di proteggere. Insistere finché l’altro cede, presentare una preferenza come emergenza o ricordare continuamente i sacrifici compiuti riduce la sua libertà. La reciprocità richiede di osservare entrambe le direzioni del potere, non soltanto quella in cui ci sentiamo limitati.",
            "Un confine utile descrive comportamento e conseguenza. Non chiede all’altro di approvare; chiarisce che cosa faremo se la conversazione diventa offensiva, se un aiuto è condizionato o se una decisione comune viene presa unilateralmente. Il confine non garantisce armonia. Rende visibile il prezzo del controllo e protegge uno spazio minimo di scelta.",
        ],
        "actions": [
            "riconoscere in una conversazione recente una domanda utile e una pressione indebita",
            "definire quali decisioni sono personali, condivise o semplicemente da comunicare",
            "elencare i segnali con cui l’affetto viene reso condizionato all’obbedienza",
            "verificare dove usiamo a nostra volta preoccupazione, denaro o silenzio per orientare l’altro",
            "tradurre un consiglio insistente in informazioni verificabili sul rischio",
            "preparare un confine espresso con comportamento, limite e conseguenza",
            "individuare una risorsa condivisa che dà diritto a negoziare ma non a possedere tutta la decisione",
            "chiedere aiuto senza cedere in cambio il controllo della propria vita",
            "stabilire quando interrompere una conversazione che non cerca più comprensione",
            "costruire una piccola alternativa materiale che riduca la dipendenza dal ricatto",
        ],
    },
    {
        "title": "Dire no senza trasformarlo in un addio",
        "lens": "imparare a porre limiti mantenendo rispetto, chiarezza e possibilità di relazione",
        "risk": "spiegarsi all’infinito finché il no diventa una trattativa sulla nostra legittimità",
        "principle": "un limite può proteggere la relazione quando impedisce al risentimento di sostituire la scelta",
        "essay": [
            "Molte persone dicono sì per evitare la scena del no. Il costo arriva più tardi sotto forma di stanchezza, ritardo, irritazione o promesse mantenute male. L’apparente armonia sposta il conflitto nel tempo e lo rende meno leggibile. Un no tempestivo può essere più rispettoso di un sì che chiederà agli altri di pagare il nostro risentimento.",
            "Dire no non richiede freddezza. Possiamo riconoscere il bisogno, esprimere dispiacere e offrire ciò che è realmente possibile. La gentilezza però non deve diventare ambiguità. Se ogni frase lascia intendere che abbastanza insistenza cambierà la risposta, la conversazione premia la pressione e rende i futuri limiti ancora più faticosi.",
            "Le spiegazioni hanno una funzione ma non sono un processo. Una persona cara può meritare contesto; non possiede per questo il diritto di approvare ogni ragione. Quando ci sentiamo obbligati a produrre una motivazione inattaccabile, stiamo spesso cercando di eliminare la delusione, obiettivo impossibile. Possiamo essere comprensibili senza diventare invulnerabili a ogni critica.",
            "Il no può avere forme diverse: non ora, non in questo modo, non a questo costo, non da solo. Specificare il limite evita che venga interpretato come rifiuto globale della persona. A volte esiste un’alternativa; altre volte offrirla trasformerebbe ancora il limite in lavoro supplementare. Anche la scelta di non proporre una soluzione può essere legittima.",
            "Dopo un no, la relazione ha bisogno di tempo. L’altro può essere triste o arrabbiato. Restare presenti senza ritirare subito la decisione permette di scoprire se il legame tollera due volontà. Se ogni differenza viene trattata come minaccia di abbandono, il problema non è soltanto la singola richiesta: riguarda la struttura della relazione.",
        ],
        "actions": [
            "individuare un sì recente seguito da risentimento e ricostruire il no non pronunciato",
            "scrivere un rifiuto in tre frasi: riconoscimento, limite e informazione utile",
            "distinguere una spiegazione rispettosa da una difesa senza fine",
            "scegliere tra non ora, non così, non a questo costo e non da solo",
            "valutare se un’alternativa è davvero disponibile o serve soltanto a placare il disagio",
            "praticare un no su una richiesta piccola prima di affrontare quella più carica",
            "restare nella conversazione senza rispondere a ogni ripetizione della stessa obiezione",
            "prevedere la delusione altrui senza trasformarla in una catastrofe relazionale",
            "riparare il tono se necessario senza cancellare il contenuto del limite",
            "osservare dopo una settimana se il no ha protetto energia e qualità della relazione",
        ],
    },
    {
        "title": "Le decisioni condivise non hanno un solo proprietario",
        "lens": "negoziare scelte di coppia e famiglia distinguendo voce, consenso, veto e responsabilità",
        "risk": "presentare come decisione individuale ciò che trasferisce stabilmente costi agli altri",
        "principle": "la libertà condivisa richiede che il potere decisionale segua le conseguenze e che nessuna voce venga data per scontata",
        "essay": [
            "Una scelta può riguardare principalmente una persona e tuttavia cambiare la vita di altre. Un nuovo lavoro, un trasferimento, un figlio, la cura di un genitore o un investimento modificano tempo e risorse comuni. In questi casi l’autonomia non basta come formula. Occorre capire chi decide che cosa e quali costi richiedono consenso anziché semplice comunicazione.",
            "Il consenso non è unanimità emotiva. Possiamo accettare una decisione senza desiderarla allo stesso modo, purché esistano informazione, possibilità reale di dissentire e accordi sostenibili. Se una persona dice sì perché non ha accesso al denaro, teme ritorsioni o sa che il lavoro ricadrà comunque su di lei, la forma del consenso nasconde uno squilibrio.",
            "Il veto è necessario in alcune aree: nessuno dovrebbe imporre un rischio grave al corpo, al debito o alla sicurezza altrui. In altre diventa strumento di controllo, soprattutto quando pretende di governare identità, amicizie e aspirazioni senza una conseguenza condivisa proporzionata. Definire in anticipo le zone di veto riduce trattative opportunistiche.",
            "Le coppie e le famiglie accumulano precedenti. Chi ha rinunciato una volta può aspettarsi reciprocità; chi guadagna di più può credere di avere più voce; chi cura può non riuscire nemmeno a partecipare alle riunioni in cui si decide. Una negoziazione equa deve considerare lavoro invisibile, dipendenze e possibilità future, non soltanto intenzioni dichiarate.",
            "Decidere insieme richiede spesso più di una conversazione. Servono scenari, numeri, periodi di prova e date di revisione. La libertà non viene diminuita da questa struttura: diventa più reale perché vede le condizioni. Un accordo chiaro permette a ciascuno di sapere che cosa sta scegliendo e quale responsabilità potrà chiedere all’altro.",
        ],
        "actions": [
            "mappare chi riceve benefici e chi sostiene costi in una decisione condivisa",
            "stabilire quali aspetti richiedono consenso e quali appartengono alla scelta individuale",
            "contare lavoro domestico, cura e disponibilità emotiva insieme al denaro",
            "verificare se ogni sì può essere ritirato senza punizioni sproporzionate",
            "costruire tre scenari realistici con tempi, costi e imprevisti",
            "riconoscere un precedente di rinuncia senza usarlo come credito infinito",
            "dare voce a chi subirà conseguenze ma partecipa meno alle conversazioni",
            "definire una prova reversibile prima di una trasformazione permanente",
            "assegnare responsabilità e risorse invece di affidarsi alla buona volontà",
            "fissare una data in cui l’accordo verrà valutato e potrà essere corretto",
        ],
    },
    {
        "title": "Lavoro, denaro e percorsi che gli altri chiamano sicuri",
        "lens": "valutare scelte di studio e lavoro senza confondere protezione economica, prestigio e aspettativa familiare",
        "risk": "seguire una traiettoria approvata e scoprire troppo tardi che non possiamo abitare la vita quotidiana che produce",
        "principle": "una scelta professionale libera considera bisogni materiali e desideri senza usare né la passione né la sicurezza come slogan assoluti",
        "essay": [
            "Le decisioni sul lavoro concentrano molte paure familiari. Un percorso stabile può rappresentare protezione dopo anni di precarietà; una professione prestigiosa può diventare riscatto collettivo. Chi sceglie diversamente non rifiuta soltanto un impiego: sembra rifiutare i sacrifici compiuti per offrirgli opportunità. Questa lettura rende difficile discutere dati e preferenze senza trasformare tutto in gratitudine.",
            "La sicurezza economica è un bisogno reale. Un desiderio non paga automaticamente affitto, salute o debiti. Ma la parola sicurezza può nascondere scenari diversi: reddito minimo, prevedibilità, riconoscimento sociale o paura di un fallimento visibile. Specificare cifra, tempo e rischio permette di progettare una transizione invece di opporre sogno e responsabilità.",
            "Anche la passione può diventare un comando. Pretendere che il lavoro realizzi tutta l’identità espone a sfruttamento e delusione. Una persona può scegliere un mestiere sufficientemente buono che sostiene una vita significativa altrove. La domanda non è quale opzione appaia più autentica, ma quale combinazione di reddito, capacità, tempo, salute e crescita sia sostenibile.",
            "Le persone care vedono talvolta informazioni che noi minimizziamo. Ascoltare non significa delegare. Possiamo chiedere quali fatti supportano una previsione, distinguere esperienza passata e condizione presente, e costruire esperimenti a rischio limitato. Un piano concreto riduce la necessità di vincere una battaglia simbolica contro il loro timore.",
            "La libertà professionale è distribuita in modo diseguale. Risparmi, passaporto, salute, rete e responsabilità di cura cambiano le opzioni. Non serve colpevolizzarsi né fingere che ogni persona possa scegliere tutto. Serve individuare il margine reale: una competenza serale, una soglia di risparmio, una candidatura o un limite al lavoro che prepara una possibilità futura.",
        ],
        "actions": [
            "tradurre la parola sicurezza in cifra minima, durata e protezioni necessarie",
            "descrivere un martedì ordinario dentro ciascuna opzione professionale",
            "separare il prestigio desiderato dalla vita concreta che il ruolo richiede",
            "riconoscere quali sacrifici familiari sentiamo di dover ripagare con la nostra carriera",
            "chiedere dati e scenari invece di discutere soltanto previsioni catastrofiche",
            "calcolare una transizione che limiti il rischio senza rinunciare subito alla direzione",
            "valutare energia, salute, relazioni e apprendimento insieme al reddito",
            "individuare il privilegio o il vincolo materiale che cambia davvero le possibilità",
            "scegliere un esperimento professionale piccolo e informativo",
            "definire la soglia oltre la quale la prudenza diventa rinvio permanente",
        ],
    },
    {
        "title": "Chi può deludere e chi deve sempre adattarsi",
        "lens": "riconoscere come genere, ruolo familiare e disuguaglianza distribuiscano in modo diverso il costo della delusione",
        "risk": "trattare come carattere personale un obbligo di cura sostenuto da aspettative sociali e dipendenze materiali",
        "principle": "la libertà richiede non solo coraggio individuale ma una distribuzione più equa di tempo, risorse e responsabilità",
        "essay": [
            "Non tutti pagano lo stesso prezzo quando deludono. In molte famiglie una persona è considerata naturalmente disponibile, capace di ricordare bisogni, accompagnare, mediare e rinunciare. Quando pone un limite, il sistema perde un lavoro invisibile e reagisce più intensamente. Definire questa reazione semplice dispiacere personale nasconde la struttura che beneficiava del suo adattamento.",
            "Genere, età, reddito e stato giuridico cambiano la possibilità di scegliere. Chi dipende economicamente o teme violenza non affronta soltanto il disagio di dire no. Un discorso sulla libertà che ignora queste condizioni rischia di attribuire mancanza di coraggio a chi sta valutando pericoli reali. La sicurezza viene prima dell’esercizio morale.",
            "Anche i ruoli privilegiati hanno copioni: dover sostenere tutti, non mostrare vulnerabilità, scegliere sempre la carriera o mantenere il controllo economico. Queste aspettative possono offrire potere e insieme restringere identità. Superarle non equivale però a negare le differenze di rischio. Occorre guardare sia il vincolo interiore sia le risorse disponibili.",
            "La soluzione non può essere soltanto imparare a dire no. Se nessuno assume il compito lasciato, il costo ricade su una persona più fragile o torna sulla stessa. La libertà richiede organizzazione: servizi, denaro, turni, competenze distribuite e accesso alle informazioni. Un confine personale diventa duraturo quando il sistema smette di dipendere dall’eroismo silenzioso.",
            "Rendere visibile la distribuzione del lavoro permette una conversazione più onesta. Non si tratta di misurare ogni gesto per vincere una contabilità affettiva, ma di verificare chi possiede tempo recuperabile, chi può sbagliare e chi resta responsabile quando gli altri scelgono. Senza questa domanda, la libertà di alcuni continua a essere finanziata dall’adattamento di altri.",
        ],
        "actions": [
            "registrare per una settimana lavoro di cura, organizzazione e memoria svolto da ciascuno",
            "individuare chi può dire no senza dover trovare un sostituto",
            "distinguere disagio relazionale, dipendenza economica e rischio per la sicurezza",
            "riconoscere un copione di genere o ruolo che limita anche chi sembra avere più potere",
            "trasformare un aiuto occasionale in responsabilità assegnata e verificabile",
            "calcolare risorse necessarie perché un confine non trasferisca il costo al più fragile",
            "condividere accessi, informazioni e competenze che oggi rendono una persona indispensabile",
            "scegliere un servizio esterno o una redistribuzione concreta del lavoro",
            "preparare un piano di sicurezza se la libertà espone a ricatto o violenza",
            "valutare se il tempo libero di qualcuno dipende sistematicamente dalla rinuncia di un altro",
        ],
    },
    {
        "title": "Il conflitto che informa invece di decidere",
        "lens": "usare il disaccordo per conoscere bisogni e conseguenze senza lasciare che il volume della reazione stabilisca l’esito",
        "risk": "cedere alla persona più insistente o interrompere ogni dialogo per proteggersi dal disagio",
        "principle": "un conflitto utile rende più precisa la decisione, ma non assegna automaticamente ragione a chi soffre o parla di più",
        "essay": [
            "Il conflitto viene spesso trattato come prova che una relazione stia fallendo. In realtà due persone possono amarsi e volere cose incompatibili in un momento preciso. Nascondere la differenza non la elimina: la sposta nei ritardi, nelle omissioni e nel risentimento. Una conversazione esplicita può essere dolorosa e insieme più rispettosa della pace apparente.",
            "Le emozioni contengono informazioni ma non istruzioni complete. La rabbia può segnalare paura, la tristezza una perdita, l’ansia incertezza. Nessuna di queste stabilisce da sola che l’altro debba cambiare scelta. Possiamo riconoscere l’emozione, chiedere quale bisogno esprime e poi valutare quali responsabilità sono davvero nostre.",
            "Un conflitto diventa improduttivo quando ripete accuse globali, introduce minacce o pretende una decisione immediata per terminare il disagio. Fermarsi non è fuga se la pausa ha durata e condizioni di ritorno. Continuare a discutere mentre nessuno può ascoltare produce spesso promesse fragili o parole che aggiungono ferite al problema iniziale.",
            "La negoziazione ha bisogno di opzioni. Se esistono soltanto obbedienza o rottura, ogni scelta appare estrema. Separare tempi, modalità e costi può creare combinazioni nuove. Non sempre un compromesso è possibile o giusto, ma esplorarlo chiarisce se l’incompatibilità riguarda il valore centrale o la prima soluzione immaginata.",
            "Dopo il conflitto serve una traccia. Quali fatti abbiamo capito? Quale accordo è stato preso? Che cosa resta irrisolto? Senza questa sintesi, ogni nuova tensione riapre tutto. Una decisione libera non deve vincere una discussione: deve poter essere abitata, verificata e corretta senza negare la dignità delle persone coinvolte.",
        ],
        "actions": [
            "descrivere il disaccordo senza attribuire intenzioni o difetti globali",
            "tradurre rabbia, tristezza e ansia in bisogni o perdite specifiche",
            "stabilire una pausa con orario e condizione di ritorno alla conversazione",
            "rifiutare minacce e urgenze create soltanto per ottenere una resa",
            "generare almeno tre opzioni oltre obbedienza e rottura",
            "separare il valore centrale dalla modalità inizialmente proposta",
            "verificare se il compromesso distribuisce il costo o lo nasconde",
            "riassumere ciò che abbiamo capito prima di ripetere la nostra posizione",
            "scrivere l’accordo, le responsabilità e ciò che resta aperto",
            "decidere quando serve una mediazione competente o un sostegno esterno",
        ],
    },
    {
        "title": "Una carta personale per scegliere restando in relazione",
        "lens": "trasformare la riflessione in criteri pratici, conversazioni e revisioni sostenibili",
        "risk": "cercare una regola perfetta che elimini per sempre la possibilità di deludere o sbagliare",
        "principle": "la libertà relazionale è una pratica: ascolta, decide, assume conseguenze e torna a verificare",
        "essay": [
            "Non esiste una formula capace di stabilire quanto siamo liberi in ogni scelta. Le relazioni cambiano, così come risorse e responsabilità. Possiamo però costruire una carta personale: pochi criteri abbastanza chiari da rallentare l’automatismo del compiacere e abbastanza flessibili da accogliere informazioni nuove.",
            "Una buona carta distingue valori e procedure. I valori possono essere autonomia, cura, reciprocità, sicurezza e verità. Le procedure dicono come usarli: chi consultare, quali numeri raccogliere, quale tempo prendersi e chi deve consentire. Senza procedure i valori restano parole nobili; senza valori le procedure diventano burocrazia del rapporto.",
            "Ogni decisione importante dovrebbe includere conseguenze che siamo disposti ad assumere. Se scegliamo un percorso, quali costi non scaricheremo sugli altri? Se chiediamo sostegno, quale voce riconosciamo a chi lo offre? Se diciamo no, quale presenza possiamo ancora garantire? Queste domande rendono la libertà responsabile senza ridurla a permesso.",
            "Serve anche una data di revisione. Alcune scelte sono irreversibili, ma molti accordi possono essere provati e corretti. Sapere che torneremo a valutare riduce sia la paura dell’altro sia la tentazione di promettere che tutto funzionerà. La revisione non è minaccia: è il momento in cui la realtà riceve il diritto di modificare il piano.",
            "Restare in relazione non significa evitare ogni delusione. Significa non usare la libertà per scomparire né l’amore per possedere. Una scelta sufficientemente libera può far soffrire e tuttavia essere onesta; una scelta apparentemente generosa può tradire una vita intera. Il compito è costruire decisioni che sappiano spiegare a chi appartengono, quali legami rispettano e quale verità non vogliono più nascondere.",
        ],
        "actions": [
            "scegliere cinque valori che devono orientare una decisione relazionale importante",
            "definire per ciascun valore un comportamento osservabile e un limite",
            "stabilire chi deve essere informato, consultato o chiamato a consentire",
            "scrivere quali conseguenze ci impegniamo ad assumere direttamente",
            "preparare una conversazione con fatti, preferenza, timori e richiesta concreta",
            "individuare una parte reversibile della scelta da sperimentare per trenta giorni",
            "scegliere due segnali di benessere e due di costo da monitorare",
            "fissare una data di revisione e le condizioni che autorizzano a correggere",
            "formulare una frase che riconosca la delusione senza consegnarle il veto",
            "scrivere il prossimo passo con data, durata, responsabilità e persona da coinvolgere",
        ],
    },
]


def practice_paragraphs(spec: dict, action: str, index: int) -> list[str]:
    first = (
        f"Pratica {index + 1}. Il compito è {action}. Parti da un episodio avvenuto negli ultimi novanta giorni, "
        f"non da un’opinione generale. Ricostruisci parole, tempi, denaro, persone e conseguenze. L’obiettivo è {spec['lens']}. "
        "Scrivi prima la versione che racconteresti alla persona interessata e poi quella che conserveresti in privato. "
        "Confrontale senza scegliere automaticamente la seconda come più autentica: la riservatezza può proteggere una verità, "
        "ma può anche evitare responsabilità. Cerca un fatto che confermi la tua interpretazione e uno che potrebbe smentirla. "
        "Se mancano informazioni, trasformale in una domanda precisa invece di riempire il vuoto con intenzioni attribuite agli altri."
    )
    second = (
        f"Durante l’esercizio fai attenzione a questo rischio: {spec['risk']}. Non cercare una soluzione che impedisca a chiunque di "
        "provare dispiacere; cerca una decisione che possa spiegare benefici, costi e distribuzione del potere. Formula un passo piccolo, "
        "con data e limite, e indica chi deve esserne informato. Poi rileggi il principio del capitolo: "
        f"{spec['principle']}. Verifica se il passo lo traduce in comportamento oppure lo usa soltanto come frase rassicurante. "
        "Concludi annotando una responsabilità che accetti, un costo che non trasferirai e una reazione altrui che sei disposto a tollerare "
        "senza ritirare subito la scelta. Se emergono violenza, ricatto o dipendenza grave, sospendi il confronto diretto e cerca sostegno sicuro e competente."
    )
    return [first, second]


def make_chapter(spec: dict) -> dict:
    paragraphs = list(spec["essay"])
    paragraphs.append(
        "Il laboratorio che segue non misura quanto ami le persone coinvolte. Serve a osservare come una decisione viene costruita. "
        "Puoi distribuire le dieci pratiche in dieci giorni, interrompere quelle non adatte e proteggere dati sensibili. Non usare gli esercizi "
        "per diagnosticare gli altri né per ottenere una sentenza a tuo favore. Cerca fatti, proporzioni, alternative e responsabilità. "
        "La libertà non richiede purezza dalle influenze: richiede la possibilità concreta di riconoscerle, discuterle e scegliere quale peso assegnare loro."
    )
    for index, action in enumerate(spec["actions"]):
        paragraphs.extend(practice_paragraphs(spec, action, index))
    paragraphs.append(
        "Chiudi il capitolo senza assegnarti un voto. Confronta la decisione iniziale con ciò che hai scoperto e scegli una modifica limitata. "
        "Potresti confermare un impegno, chiedere una negoziazione, porre un confine o riconoscere che una responsabilità reale riduce il margine disponibile. "
        "Nessuno di questi esiti dimostra da solo libertà o dipendenza. La prova è nel processo: più verità, più voce, costi visibili e la possibilità di tornare a verificare."
    )
    return {"title": spec["title"], "paragraphs": paragraphs}


PACKAGE = {
    "excerpt": "Una riflessione su libertà, amore e appartenenza: quanto scegliamo davvero quando temiamo di deludere le persone importanti?",
    "book_title": "Liberi senza smettere di appartenere",
    "book_deck": "Un libro-laboratorio su desiderio, colpa, aspettative familiari, cura, confini e decisioni condivise per scegliere con una voce propria senza rendere invisibili i legami.",
    "book_pages": [make_chapter(spec) for spec in CHAPTERS],
}


def metrics() -> dict:
    text = " ".join(paragraph for page in PACKAGE["book_pages"] for paragraph in page["paragraphs"])
    return {"book_words": len(re.findall(r"\S+", text)), "chapters": len(PACKAGE["book_pages"])}
