#!/usr/bin/env python3
"""Pacchetto editoriale quotidiano CurioMondo del 26 settembre 2026."""
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
    update_home,
    update_search,
    update_sitemap,
)


ROOT = Path(__file__).resolve().parents[1]
VERSION = 583
DATE = "2026-09-26"
DATE_LABEL = "26 settembre 2026"
QUESTION_NUMBER = 1010
QUESTION = "Che cosa perderemmo se ogni nostro desiderio venisse soddisfatto immediatamente?"
SLUG = "che-cosa-perderemmo-se-ogni-nostro-desiderio-venisse-soddisfatto-immediatamente"
QUESTION_URL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"

shared.VERSION = VERSION
shared.DATE = DATE
shared.DATE_LABEL = DATE_LABEL


PACKAGE = {
    "excerpt": "Una riflessione su attesa, limite e desiderio: ottenere tutto subito eliminerebbe frustrazione, ma anche scoperta, scelta e trasformazione.",
    "answer_paragraphs": [
        "Se ogni desiderio venisse soddisfatto immediatamente, perderemmo anzitutto la distanza che ci permette di capire che cosa vogliamo davvero. Molti desideri nascono da un’emozione, da un confronto o da una stanchezza momentanea. Il tempo non li rende automaticamente più nobili, ma li mette alla prova: alcuni resistono, altri cambiano forma, altri ancora scompaiono appena smettiamo di alimentarli.",
        "Perderemmo anche una parte della scelta. Desiderare non significa soltanto ricevere qualcosa; significa decidere a quale possibilità dedicare energie e a quali alternative rinunciare. Se tutto arrivasse nello stesso istante, nessun desiderio avrebbe bisogno di essere ordinato rispetto agli altri. Avremmo più possibilità, ma meno occasioni per scoprire quali valori guidano davvero le nostre priorità.",
        "L’attesa può essere dolorosa e non va idealizzata. Ci sono bisogni essenziali — sicurezza, salute, cibo, casa, affetto non violento — la cui soddisfazione non dovrebbe dipendere da una prova di pazienza. Ma tra un bisogno negato e un desiderio immediatamente esaudito esiste uno spazio in cui impariamo, prepariamo le condizioni, chiediamo aiuto e incontriamo la realtà invece di limitarci a consumare una risposta.",
        "Scomparirebbe una parte del piacere dell’avvicinamento. Immaginare, costruire, migliorare e condividere l’attesa danno profondità a ciò che otteniamo. Non perché la fatica renda ogni risultato meritato, ma perché il percorso crea competenze, ricordi e relazioni che l’oggetto finale non contiene. Una meta ricevuta senza cammino può essere gradevole; più difficilmente racconta chi siamo diventati per raggiungerla.",
        "Perderemmo perfino la possibilità di essere sorpresi dai nostri limiti. Un desiderio non realizzato può mostrarci che dipendeva dal riconoscimento altrui, che il suo costo era incompatibile con un altro bene o che la vita offriva una direzione inattesa. La frustrazione non è sempre una maestra: talvolta ferisce soltanto. Eppure, quando può essere attraversata in sicurezza, interrompe l’illusione che volere qualcosa equivalga a sapere già che cosa ci farà bene.",
        "Forse il valore del desiderio non è soltanto nel suo compimento. È anche nella domanda che apre: quanto siamo disposti a cambiare, che cosa non vogliamo sacrificare, con chi desideriamo condividere il risultato? Se tutto accadesse subito, saremmo liberati da molte attese inutili, ma rischieremmo di perdere il tempo necessario a diventare persone capaci di abitare ciò che hanno chiesto.",
    ],
    "book_title": "Il tempo tra desiderio e compimento",
    "book_deck": "Un percorso tra attesa, limite, piacere, scelta e responsabilità per capire che cosa rende un desiderio capace di trasformarci, oltre il momento in cui viene esaudito.",
    "book_pages": [
        {
            "title": "Il desiderio ha bisogno di distanza",
            "paragraphs": [
                "Un desiderio appare spesso come una certezza: voglio questo, quindi questo mi manca. La distanza tra l’impulso e il compimento introduce però una domanda che l’immediatezza cancella: che cosa sto cercando davvero? Dietro un acquisto può esserci bisogno di appartenenza, dietro una partenza il desiderio di interrompere una routine, dietro un successo la speranza di sentirsi finalmente riconosciuti. Il tempo non smaschera ogni intenzione, ma offre alla domanda la possibilità di emergere.",
                "Quando la risposta arriva prima della comprensione, il desiderio può rinnovarsi identico. Otteniamo l’oggetto, l’esperienza o l’approvazione, proviamo sollievo e poco dopo avvertiamo nuovamente la stessa mancanza. Non significa che ciò che abbiamo voluto fosse falso. Significa che conteneva più di una richiesta e che la soddisfazione visibile non poteva rispondere a tutte. La distanza aiuta a distinguere la cosa desiderata dal significato che le avevamo affidato.",
                "Attendere non vuol dire rendere sospetto ogni piacere. Un desiderio semplice può essere accolto senza processo: mangiare qualcosa di buono, riposare, chiamare una persona, scegliere un piccolo regalo. Il problema nasce quando l’accesso immediato diventa l’unico criterio e la presenza di un intervallo viene vissuta come un difetto. In quel momento non stiamo più scegliendo soltanto ciò che vogliamo; stiamo difendendo l’idea di non dover incontrare alcuna frustrazione.",
                "La distanza crea anche immaginazione. Possiamo anticipare un viaggio, discutere un progetto, cercare alternative, scoprire aspetti ignorati. A volte l’immaginazione eccede la realtà e prepara una delusione; altre volte rende il percorso parte dell’esperienza. Senza intervallo resterebbe il consumo del risultato, ma verrebbe meno la costruzione mentale e relazionale che gli dà un posto nella nostra storia.",
                "Per capire se una distanza è utile, possiamo osservare che cosa produce. Ci rende più lucidi, capaci e presenti oppure ci tiene in un’attesa imposta e sterile? Non ogni ritardo educa e non ogni immediatezza impoverisce. La domanda importante è se il tempo tra desiderio e compimento ci permette di conoscere meglio ciò che chiediamo o serve soltanto a giustificare un ostacolo che potrebbe essere rimosso.",
            ],
        },
        {
            "title": "Bisogni essenziali e desideri non sono la stessa cosa",
            "paragraphs": [
                "Una riflessione sull’attesa diventa ingiusta se tratta allo stesso modo una persona che desidera un nuovo oggetto e una persona che aspetta cure, sicurezza, documenti, reddito o una casa dignitosa. I bisogni essenziali non acquistano valore perché vengono rimandati. L’incertezza prolungata può consumare salute e capacità di scelta. In questi casi ridurre l’attesa è un dovere organizzativo e sociale, non una perdita di profondità personale.",
                "Anche l’affetto ha una dimensione necessaria. Nessuno può pretendere amore immediato da una persona specifica, ma ogni essere umano ha bisogno di relazioni non violente, ascolto e appartenenza. Idealizzare la mancanza rischia di trasformare solitudine e trascuratezza in esercizi di carattere. Un limite può formare; l’abbandono ripetuto più spesso restringe, rende diffidenti e obbliga a investire energie nella semplice protezione.",
                "Distinguere bisogno e desiderio non significa creare una gerarchia morale rigida. Un desiderio non essenziale può dare gioia, identità e creatività. Un bisogno può manifestarsi attraverso forme diverse. La distinzione serve a capire quale attesa sia negoziabile. Possiamo rimandare un acquisto per verificarne il valore; non dovremmo chiedere a qualcuno di sopportare fame o pericolo affinché impari ad apprezzare ciò che riceverà.",
                "Molti servizi digitali confondono deliberatamente questi livelli. Una notifica rende urgente un contenuto, un conto alla rovescia trasforma un’offerta in occasione irripetibile, un sistema di ricompense presenta la continuità d’uso come appartenenza. Fermarsi permette di chiedere se stiamo rispondendo a una necessità concreta o a un’urgenza progettata da altri. La risposta non deve essere sempre rinuncia; può essere una scelta più consapevole del momento e del costo.",
                "Una società capace di soddisfare rapidamente i bisogni fondamentali non eliminerebbe il desiderio. Al contrario, potrebbe liberarlo dalla lotta per la sopravvivenza e renderlo più creativo. La questione non è conservare ogni mancanza, ma costruire condizioni in cui l’attesa non sia una punizione e il desiderio possa diventare esplorazione, relazione e progetto invece di compensazione continua di un’insicurezza primaria.",
            ],
        },
        {
            "title": "Scegliere significa anche rinunciare",
            "paragraphs": [
                "Ogni desiderio soddisfatto occupa spazio, tempo e attenzione. Perfino quando il denaro non è un limite, restano limiti fisici e relazionali: non possiamo abitare contemporaneamente tutte le vite immaginate. Se ogni desiderio si realizzasse subito, le alternative non sparirebbero; si accumulerebbero. Potremmo avere tutto in teoria e non riuscire a dare presenza a nulla. La scelta serve a trasformare possibilità astratte in una vita concreta.",
                "La rinuncia viene spesso raccontata come perdita pura. In realtà può proteggere ciò che abbiamo scelto. Dire no a un impegno conserva tempo per una relazione; non inseguire ogni opportunità permette a una competenza di maturare; lasciare un oggetto nel negozio difende un obiettivo economico più importante. La rinuncia non rende automaticamente saggia una decisione, ma mostra quali beni non vogliamo sacrificare per soddisfare l’impulso più recente.",
                "Un mondo senza rinunce indebolirebbe anche la promessa. Promettere significa restringere volontariamente le possibilità future: esserci, rispettare un accordo, mantenere una cura. Se ogni nuovo desiderio fosse immediatamente disponibile, la fedeltà sembrerebbe un ostacolo anziché una forma di libertà scelta. Potremmo cambiare direzione senza costo, ma sarebbe più difficile costruire quella continuità da cui dipendono fiducia e progetti comuni.",
                "Non tutte le rinunce sono libere. Povertà, discriminazione, malattia e responsabilità distribuite in modo ingiusto impongono scelte che altri non devono affrontare. Chiamarle maturità può nascondere il problema. Per questo occorre distinguere la rinuncia che esprime un valore da quella subita per mancanza di alternative. Solo la prima racconta davvero una priorità; la seconda chiede tutele e possibilità più eque.",
                "Un criterio pratico è domandarsi non soltanto che cosa otterremmo dicendo sì, ma quale realtà riceverebbe meno cura. Ogni sì crea un’ombra: denaro non disponibile altrove, tempo sottratto, energie divise. Guardare quell’ombra non serve a colpevolizzarsi. Rende visibile il prezzo e permette di scegliere un desiderio insieme alle sue conseguenze, invece di immaginarlo come un’aggiunta senza peso.",
            ],
        },
        {
            "title": "Il piacere dell’avvicinamento",
            "paragraphs": [
                "Parte del piacere nasce prima del risultato. Preparare una cena, imparare una canzone, risparmiare per un viaggio o attendere un incontro crea una sequenza di piccoli segnali che orientano l’attenzione. Il futuro desiderato illumina gesti presenti. Se il compimento fosse istantaneo, rimarrebbe la sensazione finale, ma scomparirebbe quella trama di anticipazioni che spesso rende l’esperienza più lunga e più condivisa.",
                "L’anticipazione può anche diventare eccessiva. Un evento immaginato per mesi rischia di non sostenere il peso delle aspettative. Per questo il valore dell’attesa non sta nel fantasticare senza limite, ma nel prepararsi restando disponibili alla realtà. Il viaggio reale avrà imprevisti, la persona incontrata non coinciderà con l’immagine, il progetto richiederà correzioni. Un desiderio maturo sa avvicinarsi senza pretendere che il mondo reciti esattamente la scena immaginata.",
                "La preparazione produce capacità che restano anche quando la meta cambia. Allenarsi per una gara costruisce conoscenza del corpo; studiare per un lavoro sviluppa competenze trasferibili; organizzare un progetto insegna collaborazione. Il risultato può fallire e il percorso non diventa per questo inutile. L’immediatezza, al contrario, consegnerebbe il premio senza offrirci necessariamente gli strumenti per mantenerlo, comprenderlo o condividerlo.",
                "Molte relazioni nascono proprio nello spazio dell’avvicinamento. Chiediamo consigli, condividiamo dubbi, riceviamo aiuto, scopriamo che qualcun altro desidera qualcosa di simile. Se la meta arrivasse senza passaggi, alcune di queste connessioni non avrebbero occasione di formarsi. Non bisogna creare difficoltà artificiali per incontrarsi, ma riconoscere che il percorso può contenere beni diversi dal traguardo.",
                "Possiamo recuperare questo piacere senza trasformare ogni attesa in un rituale. Basta rendere visibile un passaggio: annotare un progresso, coinvolgere una persona, imparare una competenza collegata, preparare lo spazio che accoglierà il risultato. Così il desiderio non resta una promessa sospesa né viene bruciato nell’istante. Diventa una direzione capace di dare forma al presente mentre il futuro si avvicina.",
            ],
        },
        {
            "title": "Frustrazione: segnale, non maestra infallibile",
            "paragraphs": [
                "La frustrazione indica che esiste una distanza tra ciò che vogliamo e ciò che accade. Non dice, da sola, chi abbia ragione. Può segnalare un ostacolo ingiusto, un limite reale, un piano insufficiente o un desiderio incompatibile con la libertà altrui. Trattarla sempre come una prova da superare romanticizza sofferenze evitabili; eliminarla in ogni caso impedisce di ascoltare le informazioni che contiene.",
                "Una risposta utile comincia dal corpo. Quanto è intensa l’emozione? Possiamo decidere in sicurezza o abbiamo bisogno di una pausa? Ridurre l’attivazione non significa rinunciare al desiderio. Permette di separare l’urgenza dalla direzione. Quando l’impulso si abbassa, possiamo capire se serve insistere, cambiare strategia, chiedere aiuto, accettare un limite oppure lasciare andare una meta che non corrisponde più a ciò che conta.",
                "La tolleranza alla frustrazione non è sopportazione infinita. È la capacità di restare presenti abbastanza a lungo da scegliere una risposta proporzionata. Comprende anche interrompere un percorso dannoso. Chi sa tollerare un no non deve accettare ogni porta chiusa; può contestarla senza distruggersi, cercare un’alternativa o riconoscere che il costo dell’insistenza supera il valore della meta.",
                "Nei bambini e negli adulti, una gratificazione sempre immediata può rendere ogni attesa simile a una minaccia. Ma l’opposto — rimandare arbitrariamente per insegnare una lezione — crea sfiducia. L’apprendimento migliore avviene con limiti comprensibili, tempi prevedibili e possibilità di partecipare. Sapere perché bisogna aspettare e che cosa si può fare nel frattempo trasforma l’intervallo da impotenza a esperienza gestibile.",
                "Quando la frustrazione si ripete nello stesso punto, merita un’analisi più ampia. Forse il desiderio dipende da una persona che non può offrirci ciò che chiediamo; forse la strategia non cambia; forse stiamo cercando attraverso quella meta una conferma impossibile da ottenere una volta per tutte. La ripetizione non ordina di rinunciare, ma invita a spostare l’attenzione dal singolo ostacolo al bisogno che continua a presentarsi.",
            ],
        },
        {
            "title": "Desideri progettati dagli altri",
            "paragraphs": [
                "Non tutti i desideri nascono in solitudine. Pubblicità, algoritmi, gruppi e modelli familiari mostrano continuamente che cosa dovrebbe renderci felici. Questo non rende falsi i desideri influenzati: impariamo sempre osservando. Diventa però importante riconoscere chi guadagna dalla nostra urgenza e quali immagini vengono ripetute finché sembrano spontanee. Il tempo è uno degli strumenti più semplici per sottrarre la scelta alla pressione del momento.",
                "Le piattaforme riducono ogni intervallo: riproduzione automatica, acquisto con un tocco, consegna rapida, notifiche personalizzate. La comodità è reale e spesso preziosa. Ma quando ogni attrito scompare, perdiamo punti in cui avremmo potuto fermarci. Inserire un limite volontario — una lista, una notte prima dell’acquisto, notifiche ridotte — non serve a demonizzare la tecnologia; ricrea uno spazio decisionale che il design ha eliminato.",
                "Anche il confronto sociale accelera il desiderio. Vediamo il risultato altrui senza il percorso, i costi o le rinunce, e interpretiamo la distanza come ritardo personale. L’immediatezza promessa diventa allora una forma di recupero: devo ottenere presto ciò che gli altri sembrano avere già. Ricordare che l’immagine pubblica è selettiva non cancella l’invidia, ma impedisce che diventi l’unica misura del tempo giusto per la nostra vita.",
                "Un desiderio più autonomo non è necessariamente originale. Possiamo volere una casa, un viaggio, un lavoro prestigioso o un oggetto comune e volerlo davvero. L’autonomia si vede nella capacità di spiegare quale esperienza cerchiamo, quali costi accettiamo e quali no. Se la risposta dipende soltanto dal fatto che il desiderio sia visibile e approvato, l’attesa può aiutarci a ritrovare una ragione personale oppure a lasciarlo andare.",
                "Una verifica concreta consiste nell’immaginare che nessuno venga a sapere del risultato. Continueremmo a desiderarlo? Se sì, quale parte rimarrebbe importante? Se no, non significa che il desiderio sia vergognoso: il riconoscimento è un bisogno umano. Sapere che stiamo cercando soprattutto uno sguardo, però, permette di domandarsi se esista un modo più diretto e meno costoso per costruire appartenenza e valore.",
            ],
        },
        {
            "title": "Ottenere non significa saper abitare",
            "paragraphs": [
                "Alcuni desideri modificano la vita quando si realizzano. Un ruolo più grande, una somma di denaro, una relazione, una casa o una nuova libertà portano possibilità e responsabilità. Riceverli subito non garantisce di saperli abitare. Possiamo sentirci impreparati, continuare a vivere secondo la vecchia mancanza o temere di perdere ciò che abbiamo ottenuto. Il compimento apre spesso un nuovo lavoro interiore invece di chiudere il precedente.",
                "La preparazione non deve diventare una scusa per rimandare all’infinito. Nessuno è completamente pronto. Serve però una base proporzionata: competenze, informazioni, sostegno, confini e una comprensione realistica del cambiamento. Chiedersi che cosa richiederà il giorno dopo il risultato è un modo efficace per distinguere la fantasia dalla vita concreta. Il desiderio riguarda l’arrivo; l’abitare riguarda la continuità.",
                "La gratitudine non basta a rendere semplice il possesso. Si può essere riconoscenti e insieme sopraffatti. Chi ottiene ciò che ha desiderato può aver bisogno di tempo per integrare la nuova realtà senza sentirsi colpevole. L’idea che dovremmo essere soltanto felici impedisce di nominare paura, fatica e perdita delle vecchie abitudini. Ogni passaggio contiene anche un lutto per la persona e la vita che non esistono più nello stesso modo.",
                "Condividere il risultato aiuta a renderlo reale. Celebrare, raccontare il percorso, ringraziare chi ha contribuito o usare ciò che abbiamo ottenuto a beneficio di altri crea legami tra il desiderio e il mondo. Non ogni meta deve diventare servizio, ma restare soli davanti al compimento può renderlo sorprendentemente vuoto. La relazione offre un contesto che l’oggetto o il successo non possono produrre da soli.",
                "Abitare un desiderio realizzato significa anche permettere che perda centralità. Dopo un tempo, la novità diventa quotidianità. Pretendere che continui a fornire la stessa intensità prepara una nuova insoddisfazione. Possiamo riconoscere il valore di ciò che c’è senza chiedergli di emozionarci sempre. La stabilità non è il fallimento del desiderio: è una delle forme con cui il compimento entra davvero nella vita.",
            ],
        },
        {
            "title": "Un ritmo scelto, non una virtù dell’attesa",
            "paragraphs": [
                "La conclusione non è che aspettare renda migliori. Alcune attese vanno accorciate, alcuni desideri possono essere accolti subito e alcune occasioni richiedono rapidità. La libertà consiste nel non usare sempre lo stesso ritmo. Possiamo rispondere immediatamente a un bisogno chiaro, concederci un piacere semplice, proteggere un tempo di verifica per una decisione costosa e rifiutare un rinvio imposto senza ragione.",
                "Un ritmo scelto considera reversibilità e conseguenze. Se una decisione costa poco e può essere corretta, l’esperimento rapido è spesso sensato. Se coinvolge salute, debiti, lavoro, casa o fiducia altrui, rallentare permette di raccogliere informazioni e ascoltare chi subirà gli effetti. Non è indecisione: è proporzionare il tempo alla profondità della scelta. L’obiettivo non è evitare errori impossibili da eliminare, ma renderli meno ciechi.",
                "Possiamo creare tre domande prima di agire: che cosa sto cercando oltre l’oggetto visibile? Che cosa dovrò trascurare o mantenere se dico sì? Che cosa cambierebbe se aspettassi un giorno, una settimana o un mese? La durata dipende dal caso. Ciò che conta è interrompere abbastanza l’automatismo da permettere al desiderio di incontrare valori, risorse e realtà.",
                "Quando decidiamo di attendere, serve una data o un criterio. Un rinvio indefinito non è riflessione: spesso è paura. Possiamo stabilire quando riesamineremo la scelta, quale informazione manca o quale condizione renderà possibile procedere. Così l’attesa diventa attiva e verificabile. Se la condizione arriva, scegliamo; se non arriva, decidiamo comunque che significato dare alla sua assenza.",
                "Se ogni desiderio fosse soddisfatto subito, perderemmo alcuni ostacoli inutili e questo sarebbe un bene. Perderemmo però anche occasioni di conoscerci, scegliere, prepararci e incontrare altri lungo il percorso. Il compito non è difendere la mancanza, ma evitare che la velocità decida per noi. Un desiderio diventa umano quando può essere accolto, discusso, trasformato e infine abitato con responsabilità.",
            ],
        },
    ],
}


GUIDES = [
    {
        "topic": "Come fare screen sul PC",
        "slug": "come-fare-screen-sul-pc",
        "title": "Come fare uno screenshot sul PC: Windows, tastiera e ritagli",
        "deck": "Tasti rapidi, Strumento di cattura, salvataggio e privacy: tutti i metodi per acquisire lo schermo su Windows senza perdere l’immagine.",
        "sections": [
            ("Scegliere che cosa catturare", [
                "Prima di premere un tasto, decidi se ti serve l’intero schermo, una sola finestra o un’area precisa. Chiudi notifiche, chat e schede con dati personali; controlla nomi, indirizzi, codici e fotografie visibili. Uno screenshot registra esattamente ciò che appare, comprese informazioni che l’occhio può ignorare perché abituato all’interfaccia. Se l’immagine verrà pubblicata, prepara una schermata pulita oppure oscura i dati con un editor prima di condividerla.",
                "Verifica anche la scala e la leggibilità. Se il testo è troppo piccolo, ingrandisci la pagina o la finestra prima della cattura invece di ritagliare e ingrandire molto dopo, perché il risultato può diventare sfocato. Per mostrare un errore, includi il messaggio completo e un minimo di contesto, ma evita password, codici di accesso e numeri di documento. Un’immagine utile deve spiegare il problema senza esporre più informazioni del necessario.",
            ]),
            ("I tasti rapidi di Windows", [
                "Premendo Windows+Maiusc+S si apre la barra dello Strumento di cattura. Puoi scegliere rettangolo, forma libera, finestra o schermo intero. Dopo la selezione l’immagine viene copiata negli appunti e compare una notifica: aprila per annotare e salvare. Se incolli subito con Ctrl+V in un messaggio o in un documento, la cattura non viene necessariamente conservata come file; salvala se pensi di averne bisogno in seguito.",
                "Il tasto Stamp o PrtScn copia normalmente l’intero schermo negli appunti. Alt+Stamp cattura soltanto la finestra attiva. Windows+Stamp acquisisce lo schermo intero e salva automaticamente un file nella cartella Immagini, Screenshot, anche se il percorso può cambiare quando OneDrive protegge la cartella Immagini. Su alcuni portatili occorre premere anche Fn. Se il tasto Stamp apre lo Strumento di cattura, è attiva l’impostazione moderna di accessibilità prevista da Windows 11.",
            ]),
            ("Usare lo Strumento di cattura", [
                "Apri Start e cerca Strumento di cattura quando vuoi un controllo maggiore. Il programma permette di scegliere il tipo di acquisizione, impostare un ritardo e, nelle versioni recenti di Windows 11, registrare anche lo schermo. Il ritardo è utile per aprire menu che scomparirebbero appena fai clic altrove. Dopo la cattura usa penna, evidenziatore e ritaglio con moderazione: le annotazioni devono indicare il punto importante senza coprire il testo necessario.",
                "Quando salvi, PNG è adatto a interfacce e testo perché mantiene bordi netti; JPEG può ridurre il peso delle fotografie, ma introduce compressione. Dai al file un nome comprensibile invece di lasciare una sequenza generica e controlla la cartella scelta. Se la cattura non compare, verifica gli appunti con Windows+V, la cartella Screenshot e le impostazioni di OneDrive. Evita programmi casuali scaricati dal web: per la maggior parte degli usi gli strumenti integrati sono sufficienti.",
            ]),
            ("Pagine lunghe, giochi e contenuti protetti", [
                "Per una pagina web più lunga dello schermo, alcuni browser offrono la cattura dell’intera pagina nei propri strumenti. In Edge cerca Acquisizione Web; in Firefox usa Acquisisci schermata dal menu contestuale o dalle azioni della pagina, secondo la versione. Chrome include funzioni negli strumenti per sviluppatori, meno immediate per chi non li usa. In alternativa crea più immagini ordinate, mantenendo una piccola sovrapposizione tra una cattura e la successiva.",
                "Nei giochi puoi usare Xbox Game Bar con Windows+G o il comando di acquisizione previsto dal gioco. Alcune piattaforme di streaming, applicazioni bancarie e contenuti protetti mostrano una schermata nera o impediscono la cattura: è una misura tecnica e non va aggirata con software sconosciuto. Per assistenza, cerca una funzione di condivisione o esportazione ufficiale. Ricorda inoltre che poter catturare un contenuto non concede automaticamente il diritto di ripubblicarlo.",
            ]),
            ("Controllo finale e condivisione", [
                "Prima di inviare l’immagine, aprila al 100% e verifica che il punto importante sia leggibile, che il ritaglio non abbia escluso informazioni indispensabili e che non compaiano dati privati. Se devi oscurare qualcosa, usa una forma opaca: una sfocatura leggera può essere reversibile visivamente o lasciare intuire il testo. Salva una copia pulita se ti serve per archivio e una copia censurata per la condivisione, così non rischi di pubblicare quella sbagliata.",
                "Per problemi tecnici accompagna lo screenshot con sistema operativo, applicazione, azione eseguita e orario dell’errore. L’immagine da sola raramente spiega la sequenza. Se il file è troppo pesante, ridimensiona mantenendo il testo leggibile oppure usa PNG ottimizzato; non trasformare ripetutamente tra formati. Quando condividi tramite servizi pubblici, controlla i permessi del link e rimuovi la cattura quando non deve più restare accessibile.",
            ]),
        ],
    },
    {
        "topic": "Come aggiornare Windows / Android",
        "slug": "come-aggiornare-windows-android",
        "title": "Come aggiornare Windows e Android in sicurezza",
        "deck": "Backup, spazio libero, controlli ufficiali e soluzioni agli errori: una procedura prudente per installare aggiornamenti senza perdere dati.",
        "sections": [
            ("Prepararsi prima dell’aggiornamento", [
                "Gli aggiornamenti correggono vulnerabilità, migliorano stabilità e introducono funzioni, ma modificano componenti importanti del sistema. Prima di iniziare salva i documenti aperti e crea una copia dei dati essenziali su cloud o disco esterno. Un backup è utile soltanto se sai dove si trova e riesci ad aprirlo. Collega il portatile o il telefono all’alimentazione, usa una rete affidabile e lascia abbastanza tempo: interrompere forzatamente il dispositivo durante l’installazione può causare errori.",
                "Controlla lo spazio disponibile. Windows può richiedere diversi gigabyte per scaricare e decomprimere i file; Android varia secondo produttore e versione. Elimina temporaneamente download inutili e sposta video pesanti, senza usare applicazioni che promettono pulizie aggressive del registro o del sistema. Verifica inoltre che l’account principale e i metodi di recupero siano accessibili: dopo un aggiornamento importante potrebbe essere richiesto nuovamente il PIN, la password Microsoft o l’account Google.",
            ]),
            ("Aggiornare Windows 11 e Windows 10", [
                "In Windows 11 apri Impostazioni, Windows Update e seleziona Verifica disponibilità aggiornamenti. In Windows 10 il percorso è Impostazioni, Aggiornamento e sicurezza, Windows Update. Installa prima gli aggiornamenti di sicurezza proposti normalmente. Gli aggiornamenti facoltativi, compresi alcuni driver, non devono essere scelti tutti per abitudine: usali quando risolvono un problema specifico o sono raccomandati dal produttore del computer.",
                "Dopo il download Windows può chiedere un riavvio. Salva il lavoro e programma un orario in cui il computer può restare indisponibile. Non spegnerlo anche se la percentuale sembra ferma; alcune fasi richiedono tempo e possono riavviare più volte. Al termine torna in Windows Update, verifica che non restino aggiornamenti importanti e apri le applicazioni principali. Per un aggiornamento di versione, controlla prima sul sito del produttore che modello, BIOS e software critici siano compatibili.",
            ]),
            ("Aggiornare Android", [
                "Su Android il percorso cambia leggermente. In genere apri Impostazioni, Sistema, Aggiornamento software o Aggiornamento di sistema; sui dispositivi Samsung trovi Aggiornamento software direttamente nelle Impostazioni. Usa soltanto il menu integrato o gli strumenti ufficiali del produttore. La disponibilità dipende da modello, operatore e area geografica: se un’altra persona riceve l’aggiornamento prima, non significa necessariamente che il tuo telefono abbia un problema.",
                "Mantieni almeno metà batteria, preferibilmente collega il caricatore e usa il Wi-Fi. Il telefono può diventare caldo e riavviarsi; non tentare di usarlo durante l’installazione. Dopo l’avvio, attendi alcuni minuti perché le app vengano ottimizzate. Apri Play Store, tocca il profilo, Gestisci app e dispositivo e aggiorna le applicazioni. Controlla anche Aggiornamento di sistema Google Play nelle impostazioni di sicurezza, se presente: è distinto dall’aggiornamento completo fornito dal produttore.",
            ]),
            ("Se l’aggiornamento non riesce", [
                "Se Windows segnala un errore, riavvia, controlla connessione, data, ora e spazio, quindi esegui di nuovo Windows Update. Scollega periferiche non necessarie durante un grande aggiornamento. La risoluzione dei problemi integrata e le pagine di supporto Microsoft possono indicare il significato del codice. Non cancellare cartelle di sistema seguendo comandi casuali. Se il PC è aziendale, contatta l’amministratore: criteri e cifratura possono richiedere una procedura specifica.",
                "Su Android, se il download si interrompe, passa a una rete stabile, libera spazio e riavvia il telefono. Non installare pacchetti firmware trovati su siti non ufficiali: un file sbagliato può bloccare il dispositivo o compromettere i dati. Se l’aggiornamento è disponibile ma fallisce ripetutamente, usa l’assistenza del produttore indicando modello esatto, versione corrente e messaggio. Un ripristino di fabbrica è l’ultima soluzione e cancella i dati: eseguilo solo dopo un backup verificato e una guida ufficiale.",
            ]),
            ("Dopo l’installazione", [
                "Nelle prime ore il dispositivo può consumare più batteria o sembrare più lento perché ricostruisce indici, aggiorna app e sincronizza dati. Lascialo collegato per un po’ prima di concludere che esista un guasto. Verifica Wi-Fi, Bluetooth, fotocamera, audio, stampanti e programmi necessari al lavoro. Controlla le impostazioni di privacy: un aggiornamento importante può introdurre nuove opzioni o riproporre scelte relative a diagnostica, posizione e personalizzazione.",
                "Conserva il backup finché sei certo che tutto funzioni. In Windows crea o verifica un punto di ripristino e consulta la cronologia degli aggiornamenti; se un aggiornamento causa un problema serio, usa le opzioni ufficiali di disinstallazione entro il periodo disponibile. Su Android il ritorno alla versione precedente raramente è supportato senza cancellazione e assistenza tecnica. Per questo la procedura più sicura resta aggiornare da canali ufficiali, con dati salvati e senza forzare tempi o strumenti.",
            ]),
        ],
    },
]


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
    stamp = datetime(2026, 9, 26, 0, 2, tzinfo=ZoneInfo("Europe/Rome"))
    for title, url, description in entries:
        node = etree.Element("item")
        full = f"https://curiomondo.it{url}"
        for tag, value in (("title", title), ("link", full), ("guid", full), ("pubDate", format_datetime(stamp)), ("description", description)):
            child = etree.SubElement(node, tag)
            child.text = value
        channel.insert(first_item, node)
        first_item += 1
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
    if len(PACKAGE["book_pages"]) != 8:
        raise SystemExit("l’eBook deve avere esattamente 8 pagine")
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

    dt = datetime(2026, 9, 26, 0, 2, tzinfo=ZoneInfo("Europe/Rome"))
    shared.write(ROOT / "domanda-del-giorno" / SLUG / "index.html", render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL))
    shared.write(ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi" / SLUG / "index.html", render_book_page(QUESTION_URL, BOOK_URL, PACKAGE))
    update_home(SLUG, dt, DATE_LABEL)
    update_archive(QUESTION, PACKAGE, SLUG, DATE_LABEL)
    update_search(QUESTION, PACKAGE, QUESTION_URL, BOOK_URL)
    update_sitemap(DATE, QUESTION_URL, BOOK_URL)

    ebook_archive = ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi/index.html"
    # Ripara la card eBook del 25 settembre, omessa dal rilascio precedente.
    previous_url = "/biblioteca/vita-relazioni/domande-per-conoscersi/siamo-stanchi-del-lavoro-o-stanchi-di-una-vita-che-il-lavoro-sta-sostituendo/"
    shared.prepend_card(
        ebook_archive,
        "cb-subgrid",
        f'<a class="cb-subcard" href="{previous_url}"><span class="cb-kicker">25 settembre 2026 · eBook</span><h2>Quando il lavoro prende il posto della vita</h2><p>Un percorso tra fatica, identità, tempo, denaro, relazioni e confini per capire che cosa ci sta esaurendo e quale spazio concreto possiamo restituire alla vita.</p><b>Sfoglia →</b></a>',
        previous_url,
    )
    shared.prepend_card(
        ebook_archive,
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
        search["items"].insert(0, {"title": guide["title"], "excerpt": guide["deck"], "url": url, "section": "Biblioteca / Tecnologia e informatica"})
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
    queue["version"] = int(queue.get("version", 7)) + 1
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
        "change": "Domanda del giorno n. 1010, eBook collegato, riparazione archivio e due guide Biblioteca",
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
            "last_update": "daily-package-v583",
        })
        shared.dump(path, state)

    shared.write(ROOT / "RELEASE-NOTES-v583.md", f'''# CurioMondo v583 — {DATE_LABEL}

- Pubblicata la Domanda del giorno “{QUESTION}”.
- Pubblicato l’eBook collegato “{PACKAGE["book_title"]}”.
- Pubblicate due guide dalla coda canonica: screenshot su PC e aggiornamenti Windows/Android.
- Ripristinata nell’archivio Biblioteca la card dell’eBook del 25 settembre.
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
