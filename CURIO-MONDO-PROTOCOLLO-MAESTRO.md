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

### Gate di pubblicazione completa — prevalenza tecnica
Un articolo non è pubblicato soltanto perché il file HTML esiste. La pubblicazione è completa esclusivamente quando, nello stesso ciclo, risultano presenti e coerenti: articolo HTML, nuova immagine editoriale IA dedicata, hero, `og:image`, `NewsArticle.image`, canonical, homepage o listing previsto, archivio, ricerca, feed, sitemap e News Sitemap quando pertinente. `python3 tools/predeploy.py` deve terminare con exit code 0. Dopo il deploy devono inoltre essere verificati l'HTTP 200 dell'articolo e dell'immagine principale, il canonical pubblico e la presenza della notizia nelle superfici editoriali previste. Se uno solo di questi elementi manca, la pubblicazione deve essere dichiarata incompleta.

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
Prima di ogni rilascio eseguire `python3 tools/predeploy.py`: deve terminare con exit code 0. Gli errori tecnici reali di sitemap, canonical, schema, redirect e robots restano bloccanti.

### Regola homepage — Ultima ora editoriale + continuità cronologica
La card `featured` / **Ultima ora** è una scelta editoriale: non è necessariamente l'articolo più recente e va assegnata alla notizia più importante del lotto recente. Questa scelta non deve però nascondere articoli dalla sequenza cronologica generale.

Il blocco **Ultime notizie** (`auto-rail`) e **Tutte le notizie** (`#cards`) devono invece formare una sequenza cronologica continua tra tutti gli articoli idonei non già occupati dalla card `featured`, ordinati per `datePublished` decrescente, senza salti. Una notizia che esce da Ultime notizie per mancanza di spazio deve ricomparire come prima notizia in Tutte le notizie. Il ticker LIVE è indipendente e non esclude una notizia dagli altri blocchi. `tools/predeploy.py` deve verificare questo invariante senza obbligare `featured` a coincidere con il primo articolo cronologico.

## Regole editoriali di fluidità e marchio — v151
- Gli articoli devono essere costruiti come lettura narrativa continua, con pochissimi sottotitoli; di default il corpo dell’articolo non usa H2/H3 editoriali.
- Sono vietate in modo permanente intestazioni come “Perché conta davvero”, “Perché è rilevante”, “Perché conta” e formule equivalenti.
- Ogni articolo deve iniziare con una grande iniziale blu (drop cap) premium, elemento distintivo CurioMondo.
- Gli approfondimenti evergreen si aggiungono quando portano reale valore esplicativo e restano separati dal flusso dell’articolo.
- **GANCIO DI CONOSCENZA OBBLIGATORIO:** durante la scrittura di ogni articolo individuare almeno un elemento interno alla notizia che il lettore medio potrebbe non conoscere ma che vale la pena capire anche oltre l’evento del giorno: un’istituzione, un’organizzazione, un meccanismo, una procedura, un termine tecnico, una tecnologia, una regola, un ruolo pubblico, un luogo strategico o un precedente storico. Spiegarlo in modo semplice, concreto e accurato, chiarendo quando utile **che cos’è, a cosa serve, cosa fa, cosa non fa, chi lo controlla o perché è importante**. L’approfondimento deve nascere organicamente dalla notizia e aumentare davvero la cultura generale del lettore; non deve essere riempitivo né una ripetizione del fatto principale.
- Il gancio di conoscenza può essere integrato nel corpo con un riquadro editoriale discreto oppure trasformato/collegato a un approfondimento evergreen autonomo quando l’argomento merita una pagina riutilizzabile. Se esiste già una guida equivalente, collegarla invece di duplicarla.
- **REGOLA EVERGREEN UNIFICATA:** creare o collegare un approfondimento evergreen autonomo soltanto quando il concetto aggiunge valore durevole, non ridondante e realmente utile oltre la notizia del giorno. Se una spiegazione chiara e naturale nel corpo è sufficiente, non creare una pagina autonoma forzata. Prima di crearne uno nuovo verificare sempre che non esista già un approfondimento equivalente.
- Ogni nuovo approfondimento deve essere collegato in entrambe le direzioni: dalla notizia alla guida e dalla guida alla notizia di origine; deve entrare in ricerca, archivio degli approfondimenti, sitemap e feed. In homepage restano visibili soltanto gli ultimi 3 approfondimenti.
- “Ultima ora” non è assegnata per semplice cronologia: ogni nuova notizia riceve un peso editoriale e la posizione va alla notizia più importante del lotto recente.
- Il menu hamburger deve mostrare il nome “Nicaise” con resa tipografica premium, elegante e riconoscibile.

## Prompt macchina obbligatorio per la generazione immagini — v183
Il file canonico è `automation/prompts/image-generation-contract.txt`. Qualunque IA, agente o renderer che crea o aggiorna un articolo DEVE leggere integralmente questo file prima di generare o descrivere l’immagine. Il percorso è dichiarato in `automation/config.json` e caricato esplicitamente da `automation/run_cycle.py`; se il prompt manca, il ciclo editoriale deve fallire in modalità fail-closed.

## Regole immagini editoriali premium
- Ogni nuova notizia deve avere una nuova immagine editoriale IA originale, specifica e coerente con il contenuto dell'articolo.
- La generazione immagini è **bloccante**: l'articolo non può essere dichiarato completo né pubblicato prima che l'immagine sia stata generata, registrata e collegata correttamente.
- Per ogni articolo nuovo o corretto, `og:image`, hero visibile e `NewsArticle.image` devono riferirsi allo stesso asset.
- Resta in vigore integralmente `AI-EDITORIAL-IMAGE-PROTOCOL.md`, compresi trasparenza IA, divieto di riuso, gestione dei personaggi pubblici e regole per i contesti sensibili.

## Fonti, citazioni e attribuzioni
- Ogni articolo indicizzabile richiede almeno tre fonti attendibili e pertinenti, salvo impossibilità documentata che impedisca la pubblicazione autonoma.
- Quando possibile usare almeno una fonte primaria o ufficiale e almeno una fonte indipendente.
- Tre fonti che ripetono la stessa agenzia non valgono automaticamente come tre conferme indipendenti.
- Virgolette, dichiarazioni politiche, numeri sensibili, percentuali, accuse, stime o affermazioni controverse devono essere sostenuti da una fonte specifica e attribuiti con precisione.

## Deploy GitHub → Netlify
La produzione corrente usa il repository GitHub come sorgente e Netlify come deployment automatico. Un commit su `main` può avviare il deploy, ma **commit riuscito non equivale a pubblicazione verificata**. Dopo il deploy occorre controllare il sito pubblico secondo il Gate di pubblicazione completa.
