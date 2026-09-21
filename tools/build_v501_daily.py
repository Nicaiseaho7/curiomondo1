#!/usr/bin/env python3
"""Pacchetto Domanda del giorno del 22 settembre 2026, senza modificare le notizie."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json

from lxml import etree, html

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
VERSION = 501
DATE = "2026-09-22"
DATE_LABEL = "22 settembre 2026"
QUESTION_NUMBER = 1006
QUESTION = "Quando perdonare diventa libertà e quando rischia di diventare una scusa per non cambiare?"
SLUG = "quando-perdonare-diventa-liberta-e-quando-rischia-di-diventare-una-scusa-per-non-cambiare"
QUESTION_URL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"


PACKAGE = {
    "excerpt": "Una riflessione sul confine tra il perdono che scioglie il passato e quello usato per evitare responsabilità, limiti e cambiamenti necessari.",
    "answer_paragraphs": [
        "Perdonare può essere un gesto di libertà quando smette di consegnare al torto subito il potere di occupare ogni pensiero. Non cancella ciò che è accaduto e non obbliga a considerarlo accettabile. Significa decidere che la ferita non sarà l’unica voce autorizzata a descrivere il presente, anche se il dolore ha ancora bisogno di tempo.",
        "Il perdono diventa invece una scusa quando viene chiesto per chiudere in fretta una conversazione, evitare conseguenze o ripetere lo stesso comportamento. Dire «mi hai perdonato» non sostituisce una riparazione. Chi ha fatto male deve poter riconoscere il danno, ascoltarne gli effetti e mostrare un cambiamento verificabile, senza pretendere che l’altro torni subito come prima.",
        "Perdonare e riconciliarsi non sono la stessa cosa. Il perdono può avvenire anche a distanza; la riconciliazione richiede fiducia, reciprocità e sicurezza. Si può lasciare andare il desiderio di vendetta e, nello stesso tempo, scegliere di non riaprire una relazione che continua a ferire. Un confine non rende il perdono meno autentico: può impedirgli di trasformarsi in abbandono di sé.",
        "Anche chi perdona può usare il gesto per non cambiare. A volte assolvere subito l’altro evita di nominare la propria rabbia, di fare una richiesta scomoda o di accettare che un rapporto non sia più quello immaginato. La pace apparente protegge dalla paura del conflitto, ma lascia intatto il meccanismo che ha prodotto il dolore.",
        "Un perdono libero non nasce dall’obbligo morale di essere buoni. Arriva quando la persona può scegliere senza minacce, ricatti o fretta. Può includere parole, silenzio, distanza, una seconda possibilità oppure una chiusura definitiva. La sua misura non è quanto velocemente ristabilisce l’armonia, ma quanta verità e responsabilità riesce a contenere.",
        "Forse il criterio più semplice è osservare ciò che accade dopo. Il perdono apre spazio a una vita più ampia oppure rende più facile ripetere ciò che fa male? Restituisce dignità a entrambe le persone oppure chiede soltanto a una di sopportare? La risposta non è sempre immediata, ma indica se stiamo lasciando andare il passato o rinunciando al cambiamento che il presente richiede.",
    ],
    "book_title": "Perdonare senza cancellarsi",
    "book_deck": "Un percorso tra memoria, responsabilità, confini e riconciliazione per distinguere il perdono che libera dalla pace apparente che lascia tutto com’era.",
    "book_pages": [
        {
            "title": "Il perdono non riscrive i fatti",
            "paragraphs": [
                "Quando si parla di perdono, la prima confusione riguarda spesso la memoria. Sembra che perdonare significhi ridurre il peso di ciò che è accaduto, trovare una spiegazione rassicurante o smettere di chiamare il torto con il suo nome. In realtà la libertà comincia dalla precisione. Un fatto doloroso può essere compreso nel suo contesto senza essere negato, giustificato o trasformato in qualcosa di inevitabile.",
                "Ricordare non equivale a restare prigionieri. La memoria conserva informazioni necessarie per riconoscere un rischio, proteggere un confine e capire che cosa serve per sentirsi nuovamente al sicuro. Il problema nasce quando il ricordo non lascia più spazio ad altro e ogni gesto presente viene letto attraverso la stessa ferita. Il perdono non ordina di dimenticare; prova a restituire alla memoria una misura che non occupi l’intera identità.",
                "La persona ferita può avere bisogno di raccontare più volte l’accaduto. Non è necessariamente ostinazione: alcuni eventi diventano comprensibili soltanto quando trovano parole, ascolto e una sequenza. Chiedere di smettere subito perché «bisogna andare avanti» spesso protegge il disagio di chi ascolta. Un processo autentico consente al racconto di cambiare lentamente, finché il fatto resta vero ma non domina ogni nuova giornata.",
                "Anche chi ha causato il danno deve resistere alla tentazione di correggere la memoria dell’altro. Può offrire la propria versione, ma non decidere quali conseguenze emotive siano legittime. La responsabilità richiede di ascoltare senza trasformare ogni dettaglio in un processo alla propria intera persona. Riconoscere un comportamento non significa accettare di essere definiti per sempre da quel comportamento; significa smettere di nasconderlo.",
                "Il perdono che nasce dalla verità non ha bisogno di una storia perfetta. Può convivere con domande irrisolte, versioni parziali e sentimenti contraddittori. Ciò che conta è non usare l’incertezza per cancellare ciò che è sufficientemente chiaro. Prima di chiedersi se perdonare, può essere utile formulare una frase semplice: che cosa è successo, quale effetto ha avuto e che cosa non si vuole più rendere normale.",
            ],
        },
        {
            "title": "Lasciare andare non significa assolvere",
            "paragraphs": [
                "Lasciare andare è un’espressione attraente perché promette leggerezza, ma può nascondere significati opposti. A volte indica la scelta di non alimentare più vendetta e ruminazione. Altre volte diventa un invito a non fare domande, non pretendere riparazione e non disturbare l’equilibrio del gruppo. La differenza sta nel soggetto della scelta: la persona ferita sta recuperando spazio oppure qualcuno le sta chiedendo di diventare comoda?",
                "Assolvere significa dichiarare che una responsabilità non sussiste o non deve produrre conseguenze. Perdonare, invece, può riconoscere pienamente la responsabilità e rinunciare comunque a vivere soltanto in funzione della colpa. È possibile desiderare che l’altro affronti gli effetti delle proprie azioni senza organizzare l’esistenza intorno alla sua punizione. Questa distinzione evita di confondere la libertà interiore con l’assenza di giustizia.",
                "Nelle relazioni vicine, il desiderio di normalità rende facile anticipare il perdono. Si vuole tornare alla cena di famiglia, alla routine di coppia o alla collaborazione di lavoro. La fretta può produrre una tregua, ma non una trasformazione. Se il problema non viene nominato, la relazione impara che basta attendere il calo della tensione. Il comportamento resta disponibile e la persona ferita diventa responsabile anche della pace comune.",
                "Rinunciare alla vendetta non richiede di rinunciare alle conseguenze. Una distanza, una restituzione, un percorso di cura, una regola nuova o la fine di un rapporto possono essere parte della risposta. Le conseguenze non servono soltanto a punire: rendono visibile che il danno è stato compreso. Senza un cambiamento concreto, le parole di pentimento rischiano di chiedere fiducia a credito, senza offrire elementi per ricostruirla.",
                "Un esercizio utile consiste nel separare tre domande: voglio smettere di nutrire questo rancore? Voglio mantenere un rapporto con questa persona? Quali conseguenze considero necessarie? Le risposte possono essere diverse. Si può dire sì alla prima e no alla seconda; si può accettare un rapporto limitato e chiedere una riparazione precisa. Il perdono diventa più libero quando non deve risolvere tutto con una sola parola.",
            ],
        },
        {
            "title": "Responsabilità prima della riconciliazione",
            "paragraphs": [
                "La riconciliazione richiede almeno due persone disposte a lavorare sul presente. Il perdono può essere un processo individuale, ma la ricostruzione della fiducia non può essere compiuta da una parte sola. Chi ha ferito deve riconoscere l’azione, comprenderne l’impatto e accettare che la fiducia ritorni più lentamente del desiderio di essere perdonato. Chiedere una nuova possibilità non crea il diritto di ottenerla.",
                "Una scusa credibile contiene elementi concreti. Nomina il comportamento senza formule vaghe, non inserisce subito una giustificazione, riconosce l’effetto sull’altro e propone come evitare la ripetizione. «Mi dispiace che tu ci sia rimasto male» sposta l’attenzione sulla sensibilità della persona ferita. «Ho fatto questo, capisco che ha prodotto questo effetto e cambierò in questo modo» mantiene la responsabilità dove deve stare.",
                "Il cambiamento ha bisogno di tempo osservabile. Una promessa può aprire una porta, ma sono le scelte ripetute a renderla affidabile. Nelle situazioni quotidiane significa rispettare nuovi accordi, parlare prima che il problema esploda e accettare verifiche ragionevoli. Nei casi più seri può richiedere sostegno professionale, tutela legale o distanza. La profondità della riparazione deve essere proporzionata al danno, non alla fretta di tornare comodi.",
                "Chi ha chiesto perdono può sentirsi frustrato quando l’altro continua ad avere paura o rabbia. Questa frustrazione non dimostra che il percorso sia inutile. La ferita segue tempi diversi dall’intenzione di cambiare. Pretendere una reazione positiva immediata trasforma la scusa in un nuovo modo di controllare. La responsabilità include tollerare che l’esito non sia garantito, anche quando l’impegno è sincero.",
                "La persona ferita, d’altra parte, non deve promettere una riconciliazione che non sente possibile. Può riconoscere lo sforzo senza dichiarare concluso il processo. Può anche scoprire che la fiducia non torna, pur non desiderando più vendetta. Una relazione ricostruita è un possibile risultato, non la prova necessaria che il perdono sia avvenuto. La libertà comprende anche la possibilità di chiudere con rispetto.",
            ],
        },
        {
            "title": "Confini che proteggono il cambiamento",
            "paragraphs": [
                "Il confine viene spesso interpretato come il contrario del perdono, quasi fosse una pena aggiuntiva. In realtà può essere la struttura che rende possibile un cambiamento reale. Dire quali comportamenti non saranno più accettati, quali contatti sono sostenibili e che cosa accadrà se l’accordo viene violato sottrae la relazione all’ambiguità. Un limite chiaro non garantisce il futuro, ma rende il presente più leggibile.",
                "Un confine efficace descrive soprattutto ciò che farà chi lo pone. «Non devi più alzare la voce» dipende dalla volontà dell’altro; «se la conversazione diventa offensiva, la interromperò e la riprenderò in un momento sicuro» definisce un’azione possibile. Questa forma non elimina il dialogo. Evita però che la speranza sostituisca ogni protezione e che il perdono venga scambiato per disponibilità illimitata.",
                "I limiti possono essere temporanei o permanenti. Una pausa consente di capire che cosa si prova lontano dalla pressione immediata. Un contatto ridotto può verificare se il nuovo comportamento regge senza tornare subito all’intimità precedente. In alcune situazioni la chiusura è la scelta più responsabile. Non esiste una quantità di accesso che dobbiamo concedere per dimostrare di non portare rancore.",
                "Quando sono coinvolti violenza, minacce, controllo economico, stalking o paura concreta, la priorità non è il confronto diretto ma la sicurezza. Il perdono non sostituisce la protezione, le reti competenti o gli strumenti previsti dalla legge. Nessuna riflessione spirituale o affettiva deve spingere una persona a esporsi nuovamente al pericolo. La distanza, in questi casi, non è durezza: è riconoscimento della realtà.",
                "Anche nei conflitti meno gravi, il corpo offre informazioni importanti. Tensione costante, sonno disturbato e paura di parlare possono segnalare che la pace dichiarata non è ancora sicurezza. Ascoltare questi segnali non significa lasciare che l’ansia decida tutto. Significa includere nell’analisi ciò che le parole non hanno ancora risolto e procedere con passi abbastanza piccoli da poter essere osservati e corretti.",
            ],
        },
        {
            "title": "Quando perdonare diventa evitare",
            "paragraphs": [
                "Esiste un modo di perdonare che protegge dall’incontro con la propria rabbia. Chi teme il conflitto può dichiarare di aver superato tutto prima ancora di comprendere che cosa desidera. L’immagine di persona paziente e generosa diventa più importante della verità. La rabbia esclusa, però, non scompare: può trasformarsi in distanza, ironia, stanchezza o esplosioni apparentemente sproporzionate.",
                "Il perdono può anche evitare una decisione. Ammettere che un rapporto non funziona, che un collega ha oltrepassato un limite o che un familiare non intende cambiare obbliga a scegliere. Dichiarare tutto risolto conserva la possibilità di non modificare niente. In questo caso il problema non è la bontà, ma l’uso della bontà come riparo dalla responsabilità di agire.",
                "Un altro segnale è la ripetizione identica. Se dopo ogni episodio arrivano scuse, commozione e ritorno immediato alla normalità, il rito del perdono può essere diventato parte del meccanismo che mantiene il danno. Le emozioni sincere non bastano a interrompere uno schema. Serve introdurre una differenza concreta: un limite applicato, un aiuto esterno, una conseguenza o una nuova forma di relazione.",
                "Evitare può sembrare pace perché riduce la tensione nel breve periodo. Il costo emerge più tardi: diminuiscono spontaneità, fiducia e capacità di parlare. Si comincia a prevedere le reazioni dell’altro e ad adattare ogni parola. La relazione appare stabile ma richiede a una persona di restringersi. Un perdono che chiede questo prezzo non libera; rende il conflitto invisibile e quindi più difficile da trasformare.",
                "Per capire se stiamo evitando, può servire una domanda concreta: quale cambiamento diventerebbe necessario se ammettessi pienamente ciò che provo? La risposta può riguardare una conversazione, un confine, una richiesta di aiuto o una separazione. Non significa dover agire subito. Permette però di vedere che cosa la parola perdono sta tenendo lontano e di preparare un passo proporzionato e sicuro.",
            ],
        },
        {
            "title": "Perdonare se stessi senza sottrarsi",
            "paragraphs": [
                "Perdonare se stessi è spesso più difficile perché conosciamo intenzioni, occasioni mancate e giustificazioni. Possiamo oscillare tra condanna totale e minimizzazione. La condanna dice che un errore rivela per sempre chi siamo; la minimizzazione sostiene che non sia accaduto nulla di importante. Entrambe evitano il compito più esigente: riconoscere un’azione concreta e costruire una risposta diversa.",
                "L’autoperdono non precede automaticamente la riparazione. Può accompagnarla, impedendo che la vergogna renda impossibile agire. Una persona convinta di essere irrimediabilmente cattiva può cercare sollievo invece di responsabilità, chiedendo agli altri di rassicurarla. Riconoscere la propria dignità serve invece a sostenere il peso delle conseguenze senza fuggire e senza trasformare chi è stato ferito nel consolatore di chi ha ferito.",
                "Il primo passaggio consiste nel descrivere l’errore senza generalizzazioni. «Ho mentito in questa occasione» offre un punto su cui lavorare; «sono una persona falsa» sembra più severo, ma non indica alcuna azione. Poi occorre chiedersi che cosa può essere riparato, che cosa non può esserlo e quale regola personale deve cambiare. Il rimorso diventa utile quando produce apprendimento, non quando occupa tutta l’energia disponibile.",
                "Non sempre la persona ferita vuole contatto o scuse. Cercarla può servire più a ridurre il nostro disagio che al suo benessere. In questi casi la responsabilità può assumere una forma indiretta: rispettare la distanza, non ripetere il comportamento, restituire ciò che è possibile e accettare che una parte del dolore non venga cancellata. L’autoperdono non concede accesso alla vita altrui.",
                "Il cambiamento più credibile è spesso poco spettacolare. Consiste nel scegliere diversamente quando si ripresenta la situazione che aveva favorito l’errore. Preparare quella scelta, chiedere sostegno e osservare le ricadute rende il perdono verso se stessi una pratica responsabile. Non si tratta di dimenticare chi siamo stati, ma di impedire che la colpa diventi sia una condanna eterna sia un alibi per restare uguali.",
            ],
        },
        {
            "title": "Il tempo, la fiducia e le prove quotidiane",
            "paragraphs": [
                "La fiducia non ritorna perché è trascorso abbastanza tempo. Il tempo offre occasioni, ma sono i comportamenti a riempirle. Una settimana tranquilla può dare sollievo; mesi di coerenza mostrano se un nuovo modo di agire sta diventando stabile. Osservare non significa sottoporre l’altro a un esame infinito. Significa permettere alla realtà di confermare ciò che le promesse hanno soltanto annunciato.",
                "Nel frattempo possono convivere vicinanza e cautela. Si può apprezzare un gesto senza considerarlo una prova definitiva, accettare una conversazione senza ripristinare ogni confidenza e riconoscere un progresso senza negare le ricadute. Questa gradualità protegge entrambi: evita alla persona ferita di esporsi troppo presto e a chi cambia di dipendere da un’unica performance perfetta.",
                "Le ricadute devono essere valutate per qualità, frequenza e risposta. Un errore riconosciuto rapidamente, interrotto e riparato non equivale alla ripetizione accompagnata da negazione o colpevolizzazione. Cercare la perfezione può rendere impossibile qualunque ricostruzione; ignorare i segnali può ristabilire lo schema precedente. Il criterio è capire se la responsabilità aumenta oppure viene nuovamente spostata.",
                "Anche la persona che perdona cambia nel tempo. Ciò che sembrava accettabile può non esserlo più; un limite iniziale può diventare meno necessario oppure più netto. Non è incoerenza. Le decisioni affettive vengono prese con le informazioni disponibili e possono essere riviste. La libertà del perdono sta anche nel non trasformare una scelta passata in un contratto che impedisce di ascoltare il presente.",
                "Tenere un piccolo diario dei fatti può aiutare quando emozioni e promesse rendono difficile vedere lo schema. Non serve costruire un dossier contro qualcuno, ma distinguere impressioni e comportamenti: che cosa è accaduto, come è stato affrontato, quale accordo è stato rispettato. La chiarezza riduce sia il sospetto generalizzato sia la tendenza a dimenticare ogni problema appena torna la calma.",
            ],
        },
        {
            "title": "Una libertà che non chiede di tornare indietro",
            "paragraphs": [
                "Il perdono più maturo non promette di riportare la vita al punto precedente. Dopo una ferita, qualcosa è stato conosciuto e non può essere disconosciuto. La libertà consiste nel decidere che cosa costruire con quella conoscenza. A volte nasce una relazione diversa e più vera; altre volte nasce una distanza pacifica. In entrambi i casi il passato smette di imporre l’unica forma possibile al futuro.",
                "Non tutto deve avere un significato positivo. Alcune esperienze restano ingiuste anche quando producono consapevolezza. Cercare a ogni costo una lezione può aggiungere pressione alla persona ferita, come se il dolore dovesse dimostrare la propria utilità. È sufficiente riconoscere che è accaduto, proteggere ciò che conta e scegliere ciò che oggi rende la vita più abitabile.",
                "La libertà non coincide con l’indifferenza. Si può aver perdonato e provare ancora tristezza quando torna un ricordo. Si può essere sereni e non desiderare un incontro. Le emozioni residue non annullano il percorso; mostrano che la memoria umana non funziona come un interruttore. La domanda utile non è se il dolore sia scomparso, ma se continua a governare decisioni che non gli appartengono più.",
                "Anche l’idea di chiudere definitivamente può richiedere più passaggi. Ci sono conversazioni che non avverranno, risposte che non arriveranno e scuse che resteranno incomplete. Aspettare la frase perfetta dell’altro può mantenere un legame invisibile. Scegliere una propria conclusione non falsifica i fatti: riconosce che la vita deve poter proseguire anche quando la riparazione desiderata non è disponibile.",
                "Alla fine, perdonare diventa libertà quando amplia le possibilità senza diminuire la verità. Non obbliga alla vicinanza, non cancella le conseguenze e non premia l’assenza di cambiamento. Restituisce alla persona la facoltà di orientare il presente con criteri nuovi. La domanda da portare con sé è concreta: ciò che chiamo perdono mi rende più capace di scegliere oppure mi chiede ancora una volta di non scegliere nulla?",
            ],
        },
    ],
}


GUIDES = [
    {
        "topic": "Come attivare modalità scura",
        "slug": "come-attivare-modalita-scura",
        "title": "Come attivare la modalità scura su telefono, computer e app",
        "deck": "Passaggi per Android, iPhone, Windows, Mac e browser, con programmazione automatica, contrasto e soluzioni quando un’app resta chiara.",
        "sections": [
            ("Prima di attivarla", [
                "La modalità scura sostituisce gli sfondi chiari con tonalità scure e adatta testi, pulsanti e finestre. Può ridurre l’abbagliamento in ambienti poco illuminati e, sugli schermi OLED, limitare in alcune condizioni il consumo dei pixel neri. Non è però una cura universale per l’affaticamento visivo: luminosità eccessiva, caratteri piccoli, riflessi e uso prolungato continuano a contare. La configurazione migliore è quella leggibile nel luogo in cui stai usando il dispositivo.",
                "Prima di cambiare tema, regola la luminosità automatica e verifica che il testo non diventi troppo sottile. Le persone con astigmatismo o altre difficoltà visive possono percepire aloni sulle lettere chiare sopra il nero. In quel caso prova un tema scuro grigio, aumenta dimensione e spessore dei caratteri oppure torna al tema chiaro. Accessibilità significa poter scegliere, non usare obbligatoriamente l’impostazione più popolare.",
            ]),
            ("Android e iPhone", [
                "Su Android apri Impostazioni, cerca Schermo o Display e attiva Tema scuro. Il nome varia tra produttori, ma la ricerca interna delle impostazioni trova quasi sempre la voce corretta. Molti telefoni permettono di programmare il tema dal tramonto all’alba o in una fascia scelta. Se compare l’opzione per forzare il tema nelle app, usala con cautela: può rendere invisibili icone, campi di testo o immagini che non sono state progettate per lo sfondo scuro.",
                "Su iPhone e iPad vai in Impostazioni, Schermo e luminosità, quindi scegli Scuro. Attivando Automatico puoi selezionare Dal tramonto all’alba oppure creare una programmazione personalizzata. Dal Centro di Controllo tieni premuto il cursore della luminosità per trovare il comando rapido Aspetto. Se i colori risultano ancora troppo intensi, nelle impostazioni di Accessibilità puoi valutare Riduci punto di bianco senza alterare il tema delle singole app.",
                "Le app aggiornate normalmente seguono il tema del sistema, ma alcune mantengono una preferenza indipendente. Cerca Tema, Aspetto o Modalità scura nelle impostazioni dell’app. Scegli Sistema se vuoi che il cambio avvenga insieme al telefono; seleziona Scuro permanente se preferisci non alternare. Se l’opzione manca, controlla lo store e aggiorna l’app. Evita versioni modificate o pacchetti esterni che promettono soltanto un tema diverso.",
            ]),
            ("Windows, Mac e browser", [
                "In Windows 11 apri Impostazioni, Personalizzazione, Colori e scegli Scuro nella voce relativa alla modalità. Puoi anche impostare separatamente la modalità di Windows e quella delle applicazioni. Controlla poi Temi di contrasto: non sono la stessa cosa del tema scuro e cambiano più profondamente i colori per esigenze di accessibilità. Se una finestra resta chiara, potrebbe usare un’interfaccia propria o una versione non aggiornata.",
                "Su macOS apri Impostazioni di Sistema, Aspetto e scegli Scuro oppure Automatico. L’opzione automatica segue l’orario della giornata. Safari e le app compatibili adattano interfaccia e menu, mentre il contenuto dei siti dipende dalle scelte del sito stesso. In Accessibilità, Schermo, puoi aumentare contrasto o ridurre trasparenza quando i pannelli scuri risultano poco definiti. Verifica sempre il risultato nelle applicazioni che usi per lavorare.",
                "Chrome, Edge, Firefox e Safari seguono generalmente il sistema per menu e pagine interne. Alcuni siti offrono un proprio interruttore, spesso nel profilo o nel menu. Le estensioni che trasformano ogni pagina possono essere utili, ma leggono e modificano il contenuto dei siti: installale soltanto dallo store ufficiale, controlla permessi e sviluppatore e rimuovile se causano errori. Prima prova le funzioni native del browser e del sito.",
            ]),
            ("Problemi comuni e controllo finale", [
                "Se una sola app resta chiara, chiudila completamente, riaprila e cerca una preferenza interna. Se i colori diventano illeggibili, disattiva l’opzione che forza il tema sulle app non compatibili. Quando screenshot, documenti o presentazioni sembrano diversi agli altri, ricorda che il tema può cambiare soltanto la visualizzazione locale: verifica il file esportato in anteprima. Per siti e documenti importanti controlla sempre che grafici, link e avvisi mantengano contrasto sufficiente.",
                "Una configurazione pratica consiste nell’usare il tema automatico, una luminosità moderata e caratteri abbastanza grandi. Provalo per alcuni giorni in ambienti diversi e non valutare soltanto l’effetto estetico. Se leggi peggio o aumentano mal di testa e tensione, torna al tema chiaro o programma lo scuro soltanto la sera. Le guide ufficiali di Apple, Google, Microsoft e del produttore del dispositivo restano il riferimento quando nomi e percorsi cambiano con gli aggiornamenti.",
            ]),
        ],
    },
    {
        "topic": "Come sincronizzare Google Drive / OneDrive",
        "slug": "come-sincronizzare-google-drive-onedrive",
        "title": "Come sincronizzare Google Drive e OneDrive senza perdere file",
        "deck": "Installazione, cartelle offline, backup, conflitti e spazio cloud: un metodo sicuro per tenere allineati PC, Mac e smartphone.",
        "sections": [
            ("Sincronizzazione e backup non sono sinonimi", [
                "La sincronizzazione mantiene copie coordinate dello stesso file su più dispositivi e nel cloud. Se modifichi o elimini un elemento, il cambiamento può propagarsi ovunque. Un backup serve invece a recuperare una versione precedente dopo errore, guasto o attacco. Prima di iniziare conserva una copia separata dei documenti importanti su un disco non sempre collegato. In questo modo un’impostazione sbagliata non trasforma la comodità della sincronizzazione in una perdita simultanea.",
                "Scegli quale account userai e controlla lo spazio disponibile. Mescolare account personali, scolastici e aziendali rende facile salvare un file nel posto sbagliato o perdere l’accesso quando termina un rapporto. Attiva l’autenticazione a due fattori, aggiorna l’indirizzo di recupero e verifica le regole dell’organizzazione. I dati di lavoro devono restare nei servizi autorizzati; non spostarli nel cloud personale soltanto per avere più spazio.",
            ]),
            ("Configurare Google Drive", [
                "Su Windows o Mac scarica Google Drive per desktop dal sito ufficiale di Google, installalo e accedi all’account corretto. L’app propone due modalità principali. Lo streaming conserva la maggior parte dei contenuti online e scarica i file quando servono, riducendo lo spazio locale. Il mirroring mantiene una copia completa sul computer e richiede disco sufficiente. Scegli in base alla connessione, alla quantità di dati e alla necessità di lavorare senza Internet.",
                "Per rendere disponibile una cartella anche offline, apri Drive nel file manager, usa il menu contestuale e seleziona l’opzione di accesso offline prevista dalla versione installata. Attendi il completamento prima di spegnere il computer. Le icone accanto ai file mostrano se un elemento è online, in trasferimento o disponibile localmente. Non interpretare la semplice presenza del nome come prova che il contenuto sia già scaricato.",
                "Nelle preferenze puoi aggiungere cartelle del computer da sincronizzare o sottoporre a backup, incluse foto e documenti. Leggi con attenzione la destinazione proposta e non selezionare interi dischi senza un motivo. Una cartella molto grande può saturare spazio e rete. Inizia con un gruppo piccolo, verifica sul sito drive.google.com che i file siano arrivati e soltanto dopo estendi la configurazione.",
            ]),
            ("Configurare OneDrive", [
                "In Windows OneDrive è normalmente già presente. Aprilo dal menu Start o dall’icona a forma di nuvola, accedi e scegli la posizione della cartella. Su Mac installalo dal Mac App Store o dalla pagina Microsoft. Files On-Demand mostra i file senza scaricarli tutti: l’icona nuvola indica contenuto online, il segno di spunta segnala una copia locale. Usa Mantieni sempre su questo dispositivo soltanto per ciò che deve funzionare offline.",
                "OneDrive può proteggere le cartelle Desktop, Documenti e Immagini. Prima di attivare la funzione controlla se quelle cartelle contengono archivi molto grandi, macchine virtuali o file già sincronizzati da un altro servizio. Due programmi che gestiscono la stessa cartella possono creare duplicati e conflitti. Attiva il backup una cartella alla volta e verifica dal portale web che struttura e permessi siano corretti.",
                "Su Android e iPhone le app di Drive e OneDrive consentono accesso, caricamento e disponibilità offline di singoli elementi. Il caricamento automatico delle foto va configurato in una sola app principale, a meno che tu non voglia intenzionalmente due copie e disponga di spazio. Consenti l’uso della rete mobile solo se il piano dati lo permette. Mantieni attivo l’aggiornamento in background quando vuoi che i trasferimenti proseguano senza l’app aperta.",
            ]),
            ("Conflitti, eliminazioni e verifica", [
                "Un conflitto nasce quando lo stesso file viene modificato su due dispositivi prima che la sincronizzazione finisca. Il servizio può creare una copia con un nome diverso oppure chiedere quale versione conservare. Non cancellare subito una delle due: apri entrambe, confronta data e contenuto e crea manualmente una versione completa. Per documenti condivisi preferisci i formati collaborativi online oppure concorda chi modifica il file quando la connessione è instabile.",
                "Se un file scompare, sospendi le modifiche e controlla prima il cestino web, poi la cronologia versioni e l’attività recente. Drive e OneDrive conservano gli elementi eliminati per un periodo limitato, variabile secondo account e organizzazione. Ripristina dal portale ufficiale e non installare programmi di recupero sul disco prima di capire se il file era soltanto online. Nei casi aziendali contatta subito l’amministratore, perché possono esistere criteri di conservazione aggiuntivi.",
                "La prova finale deve includere un file nuovo, una modifica e un accesso offline. Crea un documento di test sul computer, verifica che appaia sul telefono e sul sito, poi modifica una riga da un secondo dispositivo. Infine rendilo disponibile offline e scollega temporaneamente la rete. Controlla anche che la copia di backup separata esista davvero. Una sincronizzazione affidabile non si riconosce dall’icona verde, ma dalla capacità verificata di ritrovare e aprire i contenuti quando servono.",
            ]),
        ],
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump(path: Path, data: object) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def guide_html(guide: dict) -> str:
    body = "".join(
        f"<h2>{escape(title)}</h2>" + "".join(f"<p>{escape(p)}</p>" for p in paragraphs)
        for title, paragraphs in guide["sections"]
    )
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(guide["title"])} | Biblioteca CurioMondo</title><meta name="description" content="{escape(guide["deck"], quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="https://curiomondo.it/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=501"><style>body{{margin:0;background:#f7fbff;color:#16324a;font-family:system-ui,-apple-system,sans-serif}}article{{max-width:920px;background:#fff;margin:24px auto 60px;padding:38px 44px;border:1px solid #d6e7f7;border-radius:26px;box-shadow:0 18px 50px rgba(20,70,130,.08)}}h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;color:#0a2b49}}h2{{color:#0d5fcb;margin-top:34px}}p{{font:1.07rem/1.74 Georgia,serif}}@media(max-width:650px){{article{{margin:12px;padding:24px 20px}}}}</style><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a></nav></header><main class="cb-shell"><article><div class="cb-breadcrumb"><a href="/biblioteca/">Biblioteca</a> / <a href="/biblioteca/tecnologia-ai/smartphone-computer/">Smartphone &amp; Computer</a></div><p class="cb-kicker">Guida pratica · {DATE_LABEL}</p><h1>{escape(guide["title"])}</h1><p><strong>{escape(guide["deck"])}</strong></p>{body}</article></main><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def prepend_card(path: Path, section_class: str, card: str, href: str) -> None:
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    container = doc.xpath(f'//section[contains(concat(" ",normalize-space(@class)," ")," {section_class} ")]')[0]
    for old in container.xpath(f'./a[@href="{href}"]'):
        container.remove(old)
    container.insert(0, html.fragment_fromstring(card))
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def add_feed_entries(entries: list[tuple[str, str, str]]) -> None:
    path = ROOT / "feed.xml"
    tree = etree.parse(str(path))
    channel = tree.getroot().find("channel")
    assert channel is not None
    urls = {f"https://curiomondo.it{url}" for _, url, _ in entries}
    for item in list(channel.findall("item")):
        if item.findtext("link") in urls:
            channel.remove(item)
    first_item = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    stamp = datetime(2026, 9, 22, 0, 0, tzinfo=ZoneInfo("Europe/Rome"))
    for title, url, description in entries:
        node = etree.Element("item")
        full = f"https://curiomondo.it{url}"
        for tag, value in (("title", title), ("link", full), ("guid", full), ("pubDate", format_datetime(stamp)), ("description", description)):
            child = etree.SubElement(node, tag)
            child.text = value
        channel.insert(first_item, node)
        first_item += 1
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def add_sitemap_url(url: str, priority: str = "0.6") -> None:
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    full = f"https://curiomondo.it{url}"
    if full not in xml:
        block = f"  <url><loc>{full}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n"
        write(path, xml.replace("</urlset>", block + "</urlset>"))


def validate() -> dict:
    answer = len(" ".join(PACKAGE["answer_paragraphs"]))
    book = len(" ".join(p for page in PACKAGE["book_pages"] for p in page["paragraphs"]))
    guides = {}
    if not 1000 <= answer <= 3000:
        raise SystemExit(f"risposta fuori soglia: {answer}")
    if not 15000 <= book <= 30000:
        raise SystemExit(f"ebook fuori soglia: {book}")
    if not 8 <= len(PACKAGE["book_pages"]) <= 14:
        raise SystemExit("numero pagine ebook non conforme")
    for guide in GUIDES:
        chars = len(" ".join(p for _, paragraphs in guide["sections"] for p in paragraphs))
        guides[guide["slug"]] = chars
        if not 3000 <= chars <= 15000:
            raise SystemExit(f"guida fuori soglia {guide['slug']}: {chars}")
    return {"answer": answer, "ebook": book, "guides": guides}


def main() -> None:
    lengths = validate()
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    daily = manifest["daily_state"]
    if daily.get("last_question_date", "") >= DATE:
        print(json.dumps({"status": "noop", "date": DATE}, ensure_ascii=False))
        return
    used = set(daily.get("used_question_source_numbers", []))
    if QUESTION_NUMBER in used:
        raise SystemExit("numero domanda già utilizzato")
    source = json.loads((ROOT / "automation/state/daily-questions.json").read_text(encoding="utf-8"))
    expected = next((item for item in source if item.get("number") not in used), None)
    if not expected or expected.get("number") != QUESTION_NUMBER or expected.get("question") != QUESTION:
        raise SystemExit("la domanda non coincide con la prossima voce canonica non usata")

    dt = datetime(2026, 9, 22, 0, 0, tzinfo=ZoneInfo("Europe/Rome"))
    write(ROOT / "domanda-del-giorno" / SLUG / "index.html", render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL))
    write(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi" / SLUG / "index.html", render_book_page(QUESTION_URL, BOOK_URL, PACKAGE))
    update_home(SLUG, dt, DATE_LABEL)
    update_archive(QUESTION, PACKAGE, SLUG, DATE_LABEL)
    update_search(QUESTION, PACKAGE, QUESTION_URL, BOOK_URL)
    update_sitemap(DATE, QUESTION_URL, BOOK_URL)
    update_feed(dt, QUESTION, PACKAGE, QUESTION_URL)

    prepend_card(
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
        write(ROOT / url.strip("/") / "index.html", guide_html(guide))
        prepend_card(
            category_path,
            "cb-manual-grid",
            f'<a class="cb-subcard" href="{url}"><span class="cb-kicker">Nuova guida · {DATE_LABEL}</span><h2>{escape(guide["title"])}</h2><p>{escape(guide["deck"])}</p><b>Leggi la guida →</b></a>',
            url,
        )
        search["items"] = [item for item in search.get("items", []) if item.get("url") != url]
        search["items"].insert(0, {"title": guide["title"], "excerpt": guide["deck"], "url": url, "section": "Biblioteca / Tecnologia e informatica"})
        add_sitemap_url(url)
    search["version"] = VERSION
    dump(search_path, search)

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
    queue["version"] = int(queue.get("version", 4)) + 1
    dump(queue_path, queue)

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
        "change": "Domanda del giorno n. 1006, eBook collegato e due guide Biblioteca",
    }
    dump(manifest_path, manifest)

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
            "last_update": "daily-package-v501",
        })
        dump(path, state)

    write(ROOT / "RELEASE-NOTES-v501.md", f'''# CurioMondo v501 — {DATE_LABEL}

- Pubblicata la Domanda del giorno “{QUESTION}”.
- Pubblicato l’eBook collegato “{PACKAGE["book_title"]}”.
- Pubblicate due guide dalla coda canonica: modalità scura e sincronizzazione Google Drive/OneDrive.
- Aggiornati homepage, archivi, ricerca, feed, sitemap, manifest e stati di rilascio.
- Nessuna notizia modificata.
''')
    print(json.dumps({"status": "ok", "version": VERSION, "question_number": QUESTION_NUMBER, "slug": SLUG, "lengths": lengths}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
