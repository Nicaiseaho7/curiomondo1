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
- **GANCIO DI CONOSCENZA OBBLIGATORIO:** durante la scrittura di ogni articolo individuare almeno un elemento interno alla notizia che il lettore medio potrebbe non conoscere ma che vale la pena capire anche oltre l’evento del giorno: un’istituzione, un’organizzazione, un meccanismo, una procedura, un termine tecnico, una tecnologia, una regola, un ruolo pubblico, un luogo strategico o un precedente storico. Spiegarlo in modo semplice, concreto e accurato, chiarendo quando utile **che cos’è, a cosa serve, cosa fa, cosa non fa, chi lo controlla o perché è importante**. L’approfondimento deve nascere organicamente dalla notizia e aumentare davvero la cultura generale del lettore; non deve essere riempitivo né una ripetizione del fatto principale. Esempio vincolante: se una notizia cita la CIA, spiegare almeno in forma sintetica che cos’è la Central Intelligence Agency, il suo ruolo nell’intelligence estera degli Stati Uniti, le sue funzioni principali, i suoi limiti rispetto alle forze di polizia e perché il suo direttore può essere un interlocutore rilevante in missioni riservate.
- Il gancio di conoscenza può essere integrato nel corpo con un riquadro editoriale discreto o trasformato/collegato a un approfondimento evergreen autonomo quando l’argomento merita una pagina riutilizzabile. Se esiste già una guida equivalente, collegarla invece di duplicarla. L’obiettivo è che ogni notizia lasci al lettore almeno una conoscenza utile che resti valida anche dopo che l’attualità è passata.
- Quando una notizia contiene un termine, meccanismo, organismo, procedura o concetto non immediatamente comprensibile al lettore medio, è obbligatorio creare o collegare un approfondimento evergreen autonomo. La guida deve spiegare con linguaggio semplice **che cos’è, come funziona, perché esiste o viene usato e perché conta nella notizia**. Non basta una definizione breve inserita nel corpo. Esempi vincolanti: una notizia sulle esercitazioni dei Volenterosi collega una guida sulla Coalizione, sulla forza multinazionale e sullo scopo delle esercitazioni; una notizia sul voto postale collega una guida su richiesta, verifica, restituzione e conteggio delle schede. Prima di crearne uno nuovo verificare che non esista già un approfondimento equivalente.
- Ogni nuovo approfondimento deve essere collegato in entrambe le direzioni: dalla notizia alla guida e dalla guida alla notizia di origine; deve entrare in ricerca, archivio degli approfondimenti, sitemap e feed. In homepage restano visibili soltanto gli ultimi 3 approfondimenti.
- “Ultima ora” non è assegnata per semplice cronologia: ogni nuova notizia riceve un peso editoriale e la posizione va alla notizia più importante del lotto recente.
- Il menu hamburger deve mostrare il nome “Nicaise” con resa tipografica premium, elegante e riconoscibile.

## Prompt macchina obbligatorio per la generazione immagini — v183
Il file canonico è `automation/prompts/image-generation-contract.txt`. **Qualunque IA, agente o renderer che crea o aggiorna un articolo DEVE leggere integralmente questo file prima di generare o descrivere l’immagine.** Il percorso è dichiarato in `automation/config.json` e caricato esplicitamente da `automation/run_cycle.py`; se il prompt manca, il ciclo editoriale deve fallire in modalità fail-closed.

Prompt canonico, da mantenere leggibile anche senza conoscere il resto del progetto:

```text
You are an elite content and visual production system for the website CurioMondo.

Every time you create or add new articles to the site, you must also generate the accompanying images according to these strict rules:

1. All images must be ultra-realistic, high-definition, and photorealistic.
2. Every image must be 100% coherent with the specific content, location, people, events and atmosphere of the article it belongs to.
3. Images must look like real professional news photography.
4. NEVER place the AI disclosure, captions, labels, headlines or editorial text inside the image itself. The image pixels must remain clean. Immediately below the image, in the article HTML, include a visible figcaption that says “Immagine illustrativa generata con IA” (or “Creato da IA”).
5. Do not use generic, stock-looking or mismatched images. Each image must feel specifically created for that exact article.
6. Prefer cinematic lighting, natural colors and journalistic composition.

When generating or updating articles:
- First write the original article in the site’s established journalistic style.
- Then create or describe the matching ultra-realistic AI-generated image that perfectly fits the article.
- Ensure the image is inserted cleanly with no editorial text inside it, followed immediately by the required AI disclosure in a visible figcaption under the image.

All final responses must be written in Italian.
```

## Regole immagini editoriali premium — v156
- **PERSONAGGI PUBBLICI E SOMIGLIANZA SINTETICA — REGOLA PROPRIETARIA v231:** sono consentite immagini ultrarealistiche e fotorealistiche con qualunque personaggio pubblico riconoscibile, vivente o deceduto, quando la sua identità è direttamente pertinente alla notizia. La tecnica può essere comunemente chiamata “deepfake”, ma CurioMondo la usa esclusivamente come **somiglianza sintetica editoriale dichiarata**, mai come fotografia documentaria o prova di un evento. Prima di generare leggere integralmente `AI-EDITORIAL-IMAGE-PROTOCOL.md` e `automation/prompts/image-generation-contract.txt`.
- **REGOLA CONTESTUALE PERSONAGGI PUBBLICI — v234:** nelle notizie ordinarie il personaggio può apparire in posti, luoghi, eventi e ambientazioni coerenti con l'articolo. Sono ammessi persone, oggetti, mezzi, abiti di ruolo, edifici e loghi pertinenti, purché non si inventi uno specifico fatto come falsa prova documentaria. Il ritratto neutrale isolato diventa obbligatorio soltanto per incidenti, morte o necrologi, malattia, diagnosi, ricoveri, violenza, guerra, catastrofi, arresti, accuse gravi, lutto, sofferenza e altre situazioni sensibili che possono provocare dolore. In questi casi non raffigurare il momento traumatico, ferite, cure, ospedali, ambulanze, manette, corpi, funerali o pianto.
- Sono vietati contenuti sessuali, umilianti, diffamatori, fraudolenti, ingannevoli per gli elettori o propagandistici, così come clonazioni vocali e audio/video che attribuiscano dichiarazioni o comportamenti mai avvenuti. Non aggirare limiti dello strumento, della piattaforma o della legge applicabile.
- Ogni `<figure>` generata con IA usa `data-ai-generated="true"`; quando raffigura un personaggio pubblico usa anche `data-synthetic-likeness="public-figure"` e `data-sensitive-context="true|false"`. Se il contesto è sensibile usa inoltre `data-portrait-format="neutral-isolated"`. Resta obbligatoria la didascalia esatta non documentaria sotto l'immagine.
- Ogni nuova notizia deve avere un'immagine editoriale originale, specifica e coerente con il contenuto dell'articolo.
- **DIVIETO ASSOLUTO DI RIUSO:** non usare mai la stessa fotografia, illustrazione, asset, crop o derivazione visiva già presente in qualunque altro articolo del sito. La regola vale anche per aggiornamenti della stessa notizia, follow-up, sviluppi e articoli sullo stesso soggetto: ogni nuova pubblicazione richiede un visual nuovo e distinto.
- Rinominare o ricomprimere un'immagine già usata NON la rende nuova. Sono vietati anche ritagli, resize, filtri, specchiature o piccole modifiche di un asset già pubblicato.
- Prima del deploy il controllo automatico deve eseguire un **audit globale di tutti gli hero degli articoli**, non soltanto delle immagini del ciclo corrente: unicità del percorso, SHA-256 e controllo percettivo per intercettare anche crop, resize e ricompressioni dello stesso visual. Qualunque duplicato tra articoli differenti blocca il rilascio.
- Per ogni articolo nuovo o corretto, `og:image`, hero visibile e `NewsArticle.image` devono riferirsi allo stesso asset.
- Le immagini devono essere generate in **alta qualità, ultra realistiche e fotorealistiche**, con livello di dettaglio elevato, illuminazione credibile, profondità, texture naturali e composizione da grande testata internazionale.
- **GATE FOTOREALISMO OBBLIGATORIO:** per le notizie non sono accettabili flat design, vector art, silhouette, pittogrammi, poster, infographic-style, render minimalisti, collage, mockup, icone o scene che sembrino disegnate. Se l'immagine non potrebbe essere scambiata a prima vista per una fotografia editoriale reale e professionale, deve essere scartata e rigenerata.
- Le scene devono avere fotografia credibile: ottica/camera plausibile, luce naturale o giornalistica, materiali e pelle realistici, profondità di campo coerente, prospettiva corretta, dettagli ambientali veri e nessun elemento grafico sospeso o simbolico.
- Per politica, sport, cultura, spettacolo, tecnologia e attualità ordinaria con personaggi pubblici sono ammesse scene fotogiornalistiche contestuali, luoghi e loghi pertinenti. Per incidenti, morte, salute, violenza, tragedie, lutto o sofferenza prevale sempre il ritratto neutrale isolato.
- È vietato usare immagini banali, generiche, piatte, da stock evidente, mockup del sito, collage, schermate di interfaccia o visual che sembrino semplici illustrazioni decorative quando la notizia richiede una scena editoriale.
- La scena deve avere un **concept visivo forte**: inquadratura, atmosfera, soggetto e contesto devono raccontare la notizia e renderla immediatamente riconoscibile anche senza testo.
- Per tecnologia, scienza, spazio e innovazione sono preferiti visual cinematografici credibili e spettacolari, senza sacrificare accuratezza e realismo.
- Per cronaca, guerre, disastri e tragedie mantenere realismo editoriale ma senza gore, corpi espliciti o dettagli gratuiti.
- Non inserire titoli editoriali, watermark commerciali, loghi o disclosure dentro l’immagine. **Regola obbligatoria:** sotto ogni immagine IA deve comparire come `<figcaption>` visibile ESATTAMENTE la frase: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.` La disclosure non deve mai essere sovrapposta ai pixel del visual.
- Se la prima generazione è mediocre, poco realistica, generica, incoerente o presenta artefatti, **scartarla e rigenerarla**. Non accettare la prima immagine soltanto perché tecnicamente valida.
- Prima del rilascio verificare che il soggetto principale sia nitido, le mani/volti/oggetti siano plausibili, lo sfondo sia coerente e l'immagine regga bene sia in hero desktop sia nei ritagli mobile/card.
- Obiettivo permanente: **nessuna immagine del sito deve sembrare banale**; ogni visual deve contribuire all'identità premium di CurioMondo.



## Regole permanenti di leggibilità, lunghezza e anti-ripetizione — v248
- La card `Domanda del giorno` in homepage conserva obbligatoriamente il design premium già approvato e il contratto DOM `cm-qday` → `cm-qday-link` → `cm-qday-card`, con `cm-qday-k` e `cm-qday-hint`. Non sostituire queste classi e non ridisegnare la card durante gli aggiornamenti: cambiare soltanto data, link e testo neutro previsto.
- In homepage la card continua a non rivelare domanda, risposta o tema.
- La risposta dedicata della Domanda del giorno non usa sottotitoli intermedi H2/H3: dopo la domanda parte direttamente una lettura continua.
- Il linguaggio della risposta deve essere semplice, chiaro e naturale. Le spiegazioni restano profonde ma facili da capire, senza periodi spezzati, gergo inutile o costruzioni difficili. La lettura deve risultare piacevole e fluida.
- **REGOLA OBBLIGATORIA DAL v257 (1° settembre 2026, ore 12:00):** il corpo di ogni nuovo articolo di notizie e di ogni aggiornamento editoriale sostanziale deve contenere **minimo 3.000 e massimo 7.000 caratteri** di testo visibile. Il conteggio riguarda esclusivamente il corpo `.art-body`: titolo, sottotitolo, metadati, didascalie, fonti e correlati non concorrono al limite.
- **Non esistono eccezioni di lunghezza, ma la lunghezza segue le informazioni disponibili, non un target fisso.** All'interno del range 3.000–7.000, l'articolo deve essere lungo quando la notizia lo giustifica e ci sono abbastanza informazioni verificate per riempirlo senza ripetere o diluire i fatti, e corto (ma comunque sopra i 3.000) quando le informazioni verificate sono poche. Se le informazioni non bastano nemmeno per arrivare a 3.000 caratteri senza ripetere o diluire, non creare un articolo autonomo: attendere nuovi elementi oppure integrare lo sviluppo in una storia esistente quando editorialmente corretto. Se il testo supera 7.000 caratteri, tagliare ridondanze, dettagli secondari e contesto non indispensabile — non allungare un articolo solo per avvicinarsi al tetto.
- **DIVIETO ASSOLUTO DI RIPETIZIONE:** ogni fatto, cifra, causa, conseguenza, spiegazione o contesto deve essere espresso una sola volta nel corpo. È vietato ripetere lo stesso concetto con sinonimi, parafrasi, formule di riepilogo o frasi costruite in modo diverso.
- Ogni paragrafo deve introdurre almeno un elemento informativo nuovo e verificato. Se un paragrafo non aggiunge un fatto, una conseguenza, un contesto o una spiegazione realmente nuova, va eliminato o fuso con quello precedente.
- Vietati i paragrafi conclusivi che si limitano a ricapitolare ciò che è già stato detto, le aperture ripetute più avanti nel testo, le frasi `in altre parole`, `in sostanza`, `in pratica` o equivalenti quando servono soltanto a riscrivere un concetto già espresso.
- Prima della pubblicazione è obbligatorio un **passaggio anti-ridondanza**: confrontare paragrafi e frasi, eliminare duplicazioni esatte e semantiche, poi ricontare i caratteri. La priorità è densità informativa, non la lunghezza.
- Il predeploy deve bloccare card premium alterata, sottotitoli nella risposta quotidiana e, per i contenuti soggetti alla regola v257, articoli fuori dal limite 3.000–7.000 o con duplicazioni testuali rilevabili automaticamente.

## Regole permanenti Domanda del giorno e Biblioteca — v162
- La frase `Una domanda. Nessuna risposta automatica.` è vietata in modo permanente, anche con differenze di maiuscole, spaziatura o punteggiatura. Non deve comparire nelle pagine presenti né in quelle future.
- L'occhiello approvato per la pagina dedicata è `Uno spazio per fermarsi e pensare.` oppure un testo futuro esplicitamente approvato dal proprietario.
- L’eBook collegato alla Domanda del giorno è diviso in pagine di lettura, ma **NON deve avere alcun effetto sfoglia-pagina**. Il cambio pagina avviene esclusivamente tramite due controlli grandi, blu e accessibili sotto il contenuto: `Indietro` e `Avanti`.
- Il lettore usa copertina, pagine separate, pulsanti visibili `← Indietro` e `Avanti →` e indicatore `Pagina X di Y`; non usa tasti freccia, swipe o gesture nascoste.
- Ogni eBook usa una paginazione semplice, normalmente 8–14 schermate complessive compresa la copertina, calibrata sulla quantità reale di contenuto. Vietati swipe, gesture di sfoglio, animazioni 3D, page-turn e navigazione nascosta: si usano soltanto i due pulsanti blu `Indietro` e `Avanti` sotto la pagina.
- Mostrare al massimo un sottotitolo per pagina di lettura e non più di 4 sottotitoli H2 nell'intero mini e-book. Non trasformare ogni paragrafo in un capitolo.
- Restano obbligatori 15.000–30.000 caratteri di contenuto utile. La paginazione cambia la presentazione, non riduce la qualità o la profondità del testo.
- Usare gli asset condivisi `biblioteca-book-reader-v1.css` e `biblioteca-book-reader-v1.js`; il predeploy deve bloccare frase vietata, navigazione assente, troppe intestazioni o struttura non paginata.

## AUTOMAZIONE CURIOMONDO — CONTRATTO OPERATIVO

- LIVE: scansione ogni 5–10 minuti; implementazione corrente ogni 10 minuti; aggiornamento dati senza full deploy.
- Una voce LIVE è cliccabile solo se esiste un articolo CurioMondo corrispondente.
- Articoli: ciclo automatico ogni 2 ore. Più articoli validi possono essere pubblicati nello stesso ciclo; massimo un deploy per ciclo; zero notizie valide = zero deploy.
- Ogni pubblicazione automatica deve rispettare integralmente questo Protocollo e superare `tools/predeploy.py`; qualunque gate bloccante fallito impedisce il deploy.
- Biblioteca: insieme alla Domanda del giorno pubblicare esattamente 2 guide nuove premium, interessanti, utili, dettagliate, ben scritte, non duplicate e da 3.000–15.000 caratteri ciascuna; entrambe devono superare i gate di qualità prima del ciclo giornaliero completo.
- Sono escluse per ora le automazioni di autopubblicazione social, YouTube e newsletter.
- Il sistema deve mantenere audit, deduplicazione, verifica delle fonti, gestione degli aggiornamenti e fail-safe.
- L’autopublish resta disattivato finché il proprietario non approva il test controllato del renderer automatico.



### Regola Netlify deploy-only (v173)
Il pacchetto finale destinato al drag-and-drop Netlify deve essere un output statico già pronto e NON deve contenere `netlify.toml`, `package.json`, Netlify Functions o configurazioni di framework/build. Il controllo editoriale locale `python3 tools/predeploy.py` non è un build Netlify: serve solo a validare lo ZIP prima della consegna.


## Regole permanenti premium Domanda del giorno, eBook e Biblioteca — v176

Queste regole sostituiscono qualunque limite precedente incompatibile relativo a Domanda del giorno, mini e-book e guide della Biblioteca.

### Risposta alla Domanda del giorno
- La risposta principale deve contenere **1.000–3.000 caratteri** di testo utile.
- Deve essere scritta in italiano naturale, caldo, chiaro e profondo: niente tono da manuale, niente frasi motivazionali vuote, niente gergo psicologico inutile.
- Deve poter toccare emotivamente il lettore senza manipolarlo: partire da un'esperienza riconoscibile, spiegare il meccanismo umano con semplicità e chiudere lasciando una domanda o un pensiero che rimane.
- Non usare H2/H3 nel corpo della risposta. La lettura deve essere continua e bellissima da leggere.
- La risposta deve creare curiosità autentica verso l'eBook collegato senza riassumerlo tutto né usare call-to-action aggressive.
- Il design della scrittura deve essere premium e riconoscibile: veri paragrafi HTML, colonna di lettura controllata, carattere editoriale da rivista, interlinea generosa, contrasto elevato e ritmo verticale coerente.
- È vietato pubblicare la risposta come un unico blocco continuo di testo.
- Il principio centrale e la domanda riflessiva possono ricevere un trattamento grafico distinto, senza cambiare il significato né interrompere la continuità della lettura.
- La resa premium è obbligatoria anche su mobile e in modalità scura.

### eBook collegato alla Domanda del giorno
- Ogni Domanda del giorno deve avere un **vero eBook da 15.000–30.000 caratteri**, non un mini-articolo allungato.
- L'eBook deve avere una voce narrativa naturale e coerente, spiegazioni profonde ma accessibili, esempi concreti, passaggi di riflessione e strumenti realmente utili.
- La quantità di pagine è dinamica: di norma **8–14 schermate complessive**, compresa la copertina, in funzione della lunghezza. Non comprimere 20.000 caratteri in quattro pareti di testo.
- Usare pochi sottotitoli: normalmente **4–7 H2 in tutto l'eBook**, mai un sottotitolo per ogni paragrafo.
- Durante la lettura possono e, quando aumentano davvero la comprensione, devono comparire **immagini, fotografie, mappe concettuali, schemi, calendari, diagrammi o altre visualizzazioni utili**. Ogni visual deve aiutare a capire, immaginare, orientarsi o ricordare; sono vietate immagini generiche inserite soltanto per bellezza.
- Ogni visual deve avere alt text descrittivo e, quando serve, una breve didascalia che spieghi cosa osservare.
- Il lettore deve sembrare un vero prodotto editoriale premium grazie a copertina, gerarchia tipografica, carta luminosa, volume e ombre controllate, senza imitazioni di sfoglio fisico.
- Restano obbligatori i due grandi pulsanti `← Indietro` e `Avanti →`, l'indicatore pagina, focus visibile, stato disabled chiaro e supporto `prefers-reduced-motion`.
- Sono vietati animazioni 3D, page-turn, swipe, gesture e navigazione nascosta.

### Biblioteca e guide quotidiane
- La Biblioteca e gli eBook adottano come identità visiva principale uno stile **premium bianco + blu CurioMondo**, luminoso, elegante e pulito, con molto spazio bianco, blu profondi/azzurri controllati e dettagli discreti. Il verde non deve essere usato come palette dominante; può comparire soltanto con significato funzionale (es. stato positivo, conferma, dato ambientale) e mai sostituire l'identità blu CurioMondo.
- Ogni giorno in cui viene pubblicata la nuova Domanda del giorno devono essere pubblicate nello stesso ciclo anche **esattamente 2 nuove guide di altissima qualità** nella Biblioteca. Non pubblicare guide deboli solo per riempire il numero: se una delle due non supera i gate editoriali, il ciclo quotidiano non è completo e va segnalato come tale prima del deploy automatico.
- Ogni guida deve contenere **3.000–15.000 caratteri** di contenuto utile, salvo un'eccezione editoriale esplicita e motivata solo quando il tema non consente quella profondità senza ripetizioni.
- Le guide devono avere **pochissimi sottotitoli**: struttura ampia e fluida, non una sequenza di micro-capitoli.
- Le immagini sono ammesse e incoraggiate solo quando chiariscono davvero la guida: esempi corretti sono mappe, itinerari, calendari, timeline, diagrammi, checklist visive, illustrazioni tecniche, confronti o fotografie esplicative. Vietate immagini decorative generiche.
- Prima della pubblicazione verificare sempre la categoria. Se nessuna categoria esistente descrive bene il contenuto, è consentito creare una **nuova categoria utile e stabile**, evitando categorie usa-e-getta.
- Ogni nuova guida deve entrare nella categoria corretta, ricerca, sitemap e feed e deve essere verificata su desktop e mobile.
- La qualità prevale sulla velocità, ma la regola quotidiana resta: **Domanda del giorno + eBook + 2 guide premium** formano un unico pacchetto editoriale giornaliero.


## CODA CANONICA GUIDE BIBLIOTECA
- Le guide sono scelte esclusivamente da `automation/state/guide-topics.json` finché la coda contiene temi.
- Dopo una pubblicazione verificata il tema viene eliminato da `remaining_topics` e registrato in `published_from_queue`.
- Vietato riutilizzare un tema consumato.
- Esattamente 2 guide al giorno quando disponibili.
- Lunghezza obbligatoria: 3.000–15.000 caratteri.
- Qualsiasi IA che crea guide deve leggere questa coda prima di scegliere l'argomento.

### Indicizzazione universale delle pagine editoriali
- Ogni pagina editoriale pubblica deve poter essere indicizzata: notizie, approfondimenti, guide, categorie Biblioteca, Domanda del giorno, archivi ed eBook.
- Ogni pagina pubblica deve avere canonical coerente e non deve contenere `noindex`; eccezioni solo per pagine tecniche realmente non editoriali.
- Testi, titoli, URL, metadati e collegamenti interni devono essere scritti in modo comprensibile ai motori di ricerca senza keyword stuffing.

### Approfondimenti evergreen come pilastro editoriale
- Sulla maggior parte delle notizie, oltre al box `Una cosa utile da sapere`, creare o collegare un approfondimento autonomo che resti utile nel tempo.
- L'approfondimento deve spiegare il contesto che trasforma la cronaca in cultura generale: origini di un conflitto, storia e funzionamento di un'istituzione, meccanismo di un'elezione, nascita di una tecnologia, logica di una procedura, cause e tappe di un fenomeno.
- Esempi vincolanti: per Russia-Ucraina spiegare origini, passaggi storici e sviluppo del conflitto; per le elezioni presidenziali USA spiegare come funzionano, come sono nate, primarie, Electoral College e passaggi costituzionali.
- Non creare un approfondimento artificiale per notizie casuali prive di un contesto durevole sensato. In quel caso il box interno può essere sufficiente.
- Gli approfondimenti devono essere autonomi, SEO-friendly, indicizzabili, collegati dalla notizia e, quando utile, rimandare alla notizia o al cluster tematico di origine.

### Navigazione paginata Biblioteca/eBook — accessibilità
- È vietato l'effetto di sfoglio e qualsiasi imitazione di un libro fisico che ruota o gira pagina.
- È vietata la navigazione tramite swipe/gesture.
- Sotto ogni pagina devono comparire soltanto due comandi grandi e ad alto contrasto blu: `← Indietro` e `Avanti →`.
- I controlli devono essere facili da vedere e premere anche per utenti anziani: font grande, area cliccabile generosa, focus visibile e stato disabled chiaramente distinguibile.

### Sistema condiviso Biblioteca e Domanda del giorno — v192
- Biblioteca, categorie, guide, manuali, eBook e risposte della Domanda del giorno devono usare gli stessi asset condivisi e la stessa identità premium bianco + blu CurioMondo + navy.
- Tutte le risposte della Domanda del giorno devono avere lo stesso layout editoriale: hero, colonna di lettura, paragrafi, principio centrale, domanda riflessiva, invito all'eBook, mobile e modalità scura.
- Le singole pagine non devono introdurre varianti locali che rendano una guida o una risposta visivamente standard o incoerente rispetto alle altre.
- Ogni rilascio deve verificare collegamenti interni, pulsanti, tema, indice, ripresa lettura e controlli `← Indietro` / `Avanti →`; nessun controllo visibile può restare senza comportamento.

### Lettura audio degli articoli — voce naturale premium
- La lettura vocale deve privilegiare una voce italiana profonda, calda e naturale, con ritmo editoriale umano e pause legate alla punteggiatura.
- Il sito deve preferire eventuali file audio neurali premium associati all’articolo (`data-audio-src` o meta `cm:article-audio`). Se non sono presenti, usa la migliore voce italiana premium/enhanced disponibile sul dispositivo, con impostazioni conservative di ritmo e tono.
- Evitare deliberatamente voci acute, troppo veloci o chiaramente robotiche quando è disponibile un’alternativa migliore.
- Non dichiarare mai che la voce browser è indistinguibile da una voce umana: la qualità dipende dal dispositivo. Per qualità realmente studio/neural, pubblicare un file audio pre-generato con TTS neurale e servirlo come asset statico.
