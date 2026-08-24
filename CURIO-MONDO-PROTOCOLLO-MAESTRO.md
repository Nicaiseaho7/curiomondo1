# CURIO MONDO — PROTOCOLLO MAESTRO EDITORIALE E TECNICO

**Stato:** obbligatorio e permanente  
**Introdotto:** v139 — 22 agosto 2026  
**Scopo:** permettere a una persona o a un agente AI che non conosce CurioMondo di aprire lo ZIP e capire come mantenere correttamente il sito.

---

## 0. PRINCIPIO GENERALE

CurioMondo è un sito di notizie + Biblioteca di contenuti evergreen + funzioni editoriali ricorrenti.

Ogni modifica deve preservare contemporaneamente:

- affidabilità editoriale;
- struttura e identità visiva;
- SEO e Google News;
- prestazioni elevate;
- integrità dei collegamenti;
- aggiornamento degli elementi ricorrenti;
- versioning coerente.

Non limitarti alla singola modifica richiesta: esegui anche gli obblighi automatici dovuti per data o coerenza editoriale.

---

# 1. CHECK GIORNALIERO OBBLIGATORIO

Prima di creare una nuova versione, confronta la data corrente con `daily_state.last_question_date` nel manifest.

## 1.1 Domanda del giorno

Se la data corrente è successiva all'ultima Domanda del giorno pubblicata:

**DEVI crearne una nuova nello stesso ciclo**, anche se la richiesta dell'utente riguarda soltanto una notizia, una guida, una correzione o un'altra modifica.

La Domanda del giorno deve:

- essere una sola per giorno;
- essere originale;
- essere profonda, non banale;
- poter riguardare QUALSIASI tema utile: vita, relazioni, amore, amicizia, famiglia, sentimenti, odio, delusione, salute, identità, lavoro, denaro, scelte, tempo, società, tecnologia, paura, rimpianti, felicità, morte, futuro, morale, ecc.;
- evitare formule da “frase motivazionale” o domande da engagement vuoto;
- in homepage mostrare **SOLO una card mistero compatta** con la dicitura `Domanda del giorno` e la **data corrente**; NON mostrare la domanda, NON mostrare anteprime della risposta e NON mostrare il tema; l’intera card deve essere cliccabile e portare alla pagina dedicata, dove l’utente scopre la domanda e la risposta;
- la pagina non deve sembrare un manuale a capitoli: il mini e-book della Biblioteca può avere una struttura più articolata;
- le categorie tematiche tipo “Scienze & Natura”, “Mente & Corpo”, “Animali”, ecc. **non devono comparire come pillole orizzontali nella homepage**: restano disponibili nel menu hamburger.

## Approfondimenti collegati in homepage

La sezione `Approfondimenti collegati` deve mostrare **sempre e soltanto gli ultimi 3 approfondimenti inseriti**, ordinati dal più recente al meno recente. Non mostrarne 4, 5 o 6. Quando viene aggiunto un nuovo approfondimento, inserirlo in prima posizione e rimuovere automaticamente dalla sezione il quarto più vecchio. Le pagine degli approfondimenti più vecchi restano nel sito e negli archivi: vengono soltanto tolte da questo blocco homepage.


### Identità visiva della pagina “Domanda del giorno”

La pagina dedicata alla Domanda del giorno deve avere un design riconoscibile e distinto dagli articoli di notizie.

Regole:
- mantenere i colori identitari CurioMondo: **blu + bianco**;
- usare un hero editoriale dedicato alla rubrica, più scenografico della testata di un normale articolo;
- la domanda deve essere il protagonista visivo assoluto;
- usare dettagli grafici leggeri (gradienti, badge, linee, grandi segni tipografici) senza immagini pesanti;
- il corpo deve restare leggibile e fluido, non trasformarsi in una landing page piena di effetti;
- mantenere alte prestazioni: preferire CSS e forme vettoriali/gradienti a risorse pesanti;
- light e dark mode devono essere entrambi curati;
- la pagina deve apparire immediatamente come una rubrica premium e non come un articolo standard.


### Regola tecnica Netlify — controlli predeploy
Prima di consegnare ogni ZIP eseguire `python3 tools/predeploy.py`: deve terminare con exit code 0.
Gli errori tecnici reali di sitemap, canonical, schema, redirect e robots restano bloccanti.
Una notizia recente non linkata direttamente dalla homepage è invece solo un avviso: la home mostra intenzionalmente una selezione compatta delle notizie.


## Regole editoriali di fluidità e marchio — v151
- Gli articoli devono essere costruiti come lettura narrativa continua, con pochissimi sottotitoli; di default il corpo dell’articolo non usa H2/H3 editoriali.
- Sono vietate in modo permanente intestazioni come “Perché conta davvero”, “Perché è rilevante”, “Perché conta” e formule equivalenti.
- Ogni articolo deve iniziare con una grande iniziale blu (drop cap) premium, elemento distintivo CurioMondo.
- Gli approfondimenti evergreen si aggiungono quando portano reale valore esplicativo e restano separati dal flusso dell’articolo.
- “Ultima ora” non è assegnata per semplice cronologia: ogni nuova notizia riceve un peso editoriale e la posizione va alla notizia più importante del lotto recente.
- Il menu hamburger deve mostrare il nome “Nicaise” con resa tipografica premium, elegante e riconoscibile.

## Regole immagini editoriali premium — v156
- Ogni nuova notizia deve avere un'immagine editoriale originale, specifica e coerente con il contenuto dell'articolo.
- Le immagini devono essere generate in **alta qualità, ultra realistiche e fotorealistiche**, con livello di dettaglio elevato, illuminazione credibile, profondità, texture naturali e composizione da grande testata internazionale.
- È vietato usare immagini banali, generiche, piatte, da stock evidente, mockup del sito, collage, schermate di interfaccia o visual che sembrino semplici illustrazioni decorative quando la notizia richiede una scena editoriale.
- La scena deve avere un **concept visivo forte**: inquadratura, atmosfera, soggetto e contesto devono raccontare la notizia e renderla immediatamente riconoscibile anche senza testo.
- Per tecnologia, scienza, spazio e innovazione sono preferiti visual cinematografici credibili e spettacolari, senza sacrificare accuratezza e realismo.
- Per cronaca, guerre, disastri e tragedie mantenere realismo editoriale ma senza gore, corpi espliciti o dettagli gratuiti.
- Non inserire scritte, titoli, watermark o loghi nell'immagine editoriale, salvo richiesta esplicita del proprietario.
- Se la prima generazione è mediocre, poco realistica, generica, incoerente o presenta artefatti, **scartarla e rigenerarla**. Non accettare la prima immagine soltanto perché tecnicamente valida.
- Prima del rilascio verificare che il soggetto principale sia nitido, le mani/volti/oggetti siano plausibili, lo sfondo sia coerente e l'immagine regga bene sia in hero desktop sia nei ritagli mobile/card.
- Obiettivo permanente: **nessuna immagine del sito deve sembrare banale**; ogni visual deve contribuire all'identità premium di CurioMondo.



## Regole permanenti di leggibilità e lunghezza — v161
- La card `Domanda del giorno` in homepage conserva obbligatoriamente il design premium già approvato e il contratto DOM `cm-qday` → `cm-qday-link` → `cm-qday-card`, con `cm-qday-k` e `cm-qday-hint`. Non sostituire queste classi e non ridisegnare la card durante gli aggiornamenti: cambiare soltanto data, link e testo neutro previsto.
- In homepage la card continua a non rivelare domanda, risposta o tema.
- La risposta dedicata della Domanda del giorno non usa sottotitoli intermedi H2/H3: dopo la domanda parte direttamente una lettura continua.
- Il linguaggio della risposta deve essere semplice, chiaro e naturale. Le spiegazioni restano profonde ma facili da capire, senza periodi spezzati, gergo inutile o costruzioni difficili. La lettura deve risultare piacevole e fluida.
- Il corpo di un normale articolo di notizie deve contenere preferibilmente tra **5.000 e 7.000 caratteri**, corrispondenti a circa 5 minuti di lettura.
- Un articolo può essere più corto soltanto quando le informazioni verificate disponibili sono realmente insufficienti. L’eccezione deve essere motivata nel markup dell’articolo con `data-length-exception`; non può essere usata per evitare il lavoro editoriale.
- È vietato raggiungere la lunghezza aggiungendo ripetizioni, parole inutili, supposizioni, dettagli non verificati o paragrafi privi di valore. Ogni parte deve aumentare comprensione, contesto o utilità.
- Il predeploy deve bloccare card premium alterata, sottotitoli nella risposta quotidiana e articoli del ciclo fuori dal limite senza eccezione motivata.

## Regole permanenti Domanda del giorno e Biblioteca — v162
- La frase `Una domanda. Nessuna risposta automatica.` è vietata in modo permanente, anche con differenze di maiuscole, spaziatura o punteggiatura. Non deve comparire nelle pagine presenti né in quelle future.
- L'occhiello approvato per la pagina dedicata è `Uno spazio per fermarsi e pensare.` oppure un testo futuro esplicitamente approvato dal proprietario.
- Il mini e-book collegato a ogni Domanda del giorno deve essere presentato come un libro sfogliabile, non come una lunga pagina con una parete di capitoli.
- Il lettore usa copertina, pagine separate, pulsanti `Pagina precedente` e `Pagina successiva`, indicatore `Pagina X di Y`, tasti freccia e gesto di scorrimento sui dispositivi touch.
- Ogni mini e-book usa di norma 5 schermate totali: una copertina e quattro pagine di lettura. Sono ammesse da 4 a 6 schermate soltanto quando la quantità di contenuto lo richiede davvero.
- Mostrare al massimo un sottotitolo per pagina di lettura e non più di 4 sottotitoli H2 nell'intero mini e-book. Non trasformare ogni paragrafo in un capitolo.
- Restano obbligatori 7.000–15.000 caratteri di contenuto utile. La paginazione cambia la presentazione, non riduce la qualità o la profondità del testo.
- Usare gli asset condivisi `biblioteca-book-reader-v1.css` e `biblioteca-book-reader-v1.js`; il predeploy deve bloccare frase vietata, navigazione assente, troppe intestazioni o struttura non paginata.

## AUTOMAZIONE CURIOMONDO — CONTRATTO OPERATIVO

- LIVE: scansione ogni 5–10 minuti; implementazione corrente ogni 10 minuti; aggiornamento dati senza full deploy.
- Una voce LIVE è cliccabile solo se esiste un articolo CurioMondo corrispondente.
- Articoli: ciclo automatico ogni 2 ore. Più articoli validi possono essere pubblicati nello stesso ciclo; massimo un deploy per ciclo; zero notizie valide = zero deploy.
- Ogni pubblicazione automatica deve rispettare integralmente questo Protocollo e superare `tools/predeploy.py`; qualunque gate bloccante fallito impedisce il deploy.
- Biblioteca: una volta al giorno selezionare fino a 3 guide nuove, interessanti, utili, dettagliate, ben scritte e non duplicate. Qualità > quantità: 3 è un target, non un obbligo a pubblicare contenuti deboli.
- Sono escluse per ora le automazioni di autopubblicazione social, YouTube e newsletter.
- Il sistema deve mantenere audit, deduplicazione, verifica delle fonti, gestione degli aggiornamenti e fail-safe.
- L’autopublish resta disattivato finché il proprietario non approva il test controllato del renderer automatico.

