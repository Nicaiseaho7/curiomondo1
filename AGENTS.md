# Istruzioni obbligatorie per agenti IA

## Regola editoriale flessibile v471 — prevalenza assoluta

Per selezione, verifica e pubblicazione delle notizie prevale la revisione v471 del 21 settembre 2026. Il protocollo deve favorire la pubblicazione di contenuti affidabili e utili, senza pretendere che ogni notizia sia eccezionale, esclusiva o assimilabile a un'inchiesta.

- **Rischio alto:** politica sensibile, accuse, reati, salute, minori, vittime, guerre, sicurezza e finanza richiedono fonte primaria più conferma indipendente, oppure almeno due fonti secondarie realmente indipendenti.
- **Rischio ordinario:** sport, cinema, serie TV, cultura, tecnologia, spettacolo, comunicati aziendali e fatti non controversi possono essere pubblicati sulla base di una fonte primaria autentica e competente. Una seconda fonte è consigliata, non obbligatoria.
- **Servizio:** calendari, orari, programmi, uscite, bandi, risultati, guide e informazioni pratiche possono basarsi sulla fonte ufficiale pertinente.
- Una notizia oltre le 24 ore non è automaticamente vecchia: è pubblicabile quando resta attuale, ricercata, utile, presenta uno sviluppo o consente un contributo CurioMondo concreto.
- Basta **almeno un elemento reale di valore aggiunto** per flash, notizie ordinarie e contenuti di servizio. Due elementi restano richiesti per analisi e approfondimenti autonomi.
- Stesso argomento non significa duplicato: aggiornare il pezzo esistente per sviluppi dello stesso dossier; creare un nuovo articolo per angolazioni autonome, guide o conseguenze sostanzialmente diverse.
- La lunghezza segue la materia verificata: flash 100–250 parole, standard 300–700, approfondimenti 800+ quando giustificati. Nessuna soglia minima rigida e nessun riempitivo.
- Un problema tecnico non annulla l'idoneità editoriale della storia: la notizia resta approvata ma la pubblicazione va completata e dichiarata conclusa solo dopo tutti i controlli tecnici e live.
- Restano sempre bloccanti falsità, attribuzioni ingannevoli, accuse non verificate, fonti contraffatte, dati inventati, immagini fuorvianti e pagine prive di sostanza.

Questa sezione sostituisce le precedenti regole incompatibili su doppia conferma universale, due valori aggiunti obbligatori per ogni formato, limite automatico di 24 ore, soglie quantitative di rilevanza e scarto editoriale causato da problemi tecnici riparabili.


## Trigger «notizie-trend-google» — non è un sito nuovo

Se il messaggio contiene `notizie-trend-google`, `trend google` o chiede di cercare i trend e pubblicare: **non creare alcun sito, app, dashboard o progetto App Builder**. CurioMondo è già online su https://curiomondo.it. Eseguire `skills/notizie-trend-google/SKILL.md`: cercare i Google Trends Italia di oggi e pubblicare gli articoli nel repository `Nicaiseaho7/curiomondo1` su `main`.

## Trigger «approfondimenti-evergreen» — non è un sito nuovo

Se il messaggio contiene `approfondimenti-evergreen`, `guide evergreen` o chiede di pubblicare approfondimenti: **non creare alcun sito, app, dashboard o progetto App Builder**. CurioMondo è già online su https://curiomondo.it. Eseguire `skills/approfondimenti-evergreen/SKILL.md`: creare fino a due guide evergreen collegate alle notizie del giorno e pubblicarle nel repository `Nicaiseaho7/curiomondo1` su `main`.

Prima di creare o aggiornare articoli o visual CurioMondo, leggere integralmente, nell'ordine:

1. `PROTOCOLLO-SCOPERTA-NOTIZIE.md`
2. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
3. `automation/prompts/image-generation-contract.txt`
4. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`
5. `PROTOCOLLO-REDAZIONE-CORPO.md`
6. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
7. `curiomondo-site-manifest.json`

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Prevalenza ricerca notizie — 19 settembre 2026
Per richieste di ultime notizie e per la fase di scoperta dei cicli editoriali, `PROTOCOLLO-SCOPERTA-NOTIZIE.md` è obbligatorio e prevale sulle vecchie priorità che mettono le agenzie prima delle fonti ufficiali o dei documenti primari. La regola delle cinque storie riguarda l’output di scouting richiesto dall’utente e non obbliga a pubblicare contenuti che non superano i gate editoriali.

## Regola editoriale articoli v317 — prevalenza assoluta
Ogni articolo segue il protocollo 4.0 in `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md` e il `PROTOCOLLO-REDAZIONE-CORPO.md`: piramide invertita; lead con le 5 W; paragrafi di 2–4 frasi e massimo 60 parole; frasi preferibilmente entro 20–25 parole; nessuna ripetizione, prima persona, enfasi, riempitivo, elenco di fonti nel corpo o nota interna. La lunghezza dipende dal formato: flash 100–250 parole, notizia standard 300–600, approfondimento autonomo 800–1.500+ parole. Gli aggiornamenti sostanziali possono superare la fascia. È vietato spiegare parole difficili nel corpo della notizia: usare un lessico chiaro oppure creare o collegare una pagina di approfondimento quando serve. Restano obbligatori il gate preventivo e almeno due elementi reali di valore aggiunto. Se manca materia verificata, l'esito è `NON PUBBLICARE — motivo`.

## Gate di pubblicazione completa — obbligatorio
Un articolo non deve mai essere considerato pubblicato soltanto perché il file HTML esiste nel repository. La pubblicazione è completa soltanto quando, nello stesso ciclo:

- è presente una nuova immagine editoriale IA dedicata, validata e collegata a hero, `og:image` e `NewsArticle.image`;
- sono aggiornati homepage o listing editoriale previsto, archivio, ricerca, feed, sitemap e News Sitemap quando pertinente;
- canonical e dati strutturati sono coerenti con l'URL pubblico;
- `python3 tools/predeploy.py` termina con exit code 0;
- dopo il deploy, l'URL pubblico dell'articolo e l'immagine hero rispondono correttamente e la notizia compare nelle superfici editoriali previste.

Se uno qualunque di questi punti manca, segnalare la pubblicazione come **incompleta** e non dichiararla conclusa.

## Regola approfondimenti coerente
Nessun glossario o gancio didascalico è obbligatorio dentro la notizia. Un approfondimento autonomo va creato o collegato **solo quando aggiunge valore durevole, non ridondante e realmente utile**. Se esiste già una guida equivalente, collegarla invece di crearne una nuova. Le spiegazioni tematiche necessarie vivono nella pagina dedicata; la notizia resta concentrata sui fatti.

## Regola permanente v470 — evergreen sotto l’articolo
Ogni approfondimento evergreen deve comparire **sotto ogni notizia che lo riguarda**, nel blocco visibile `.cm-evergreen-reader` (kicker, titolo, anteprima, `Leggi l’approfondimento →`). Non basta l’indice `/approfondimenti/` né una card in `curio-related`. Posizione: subito dopo `.art-body`. Massimo due blocchi per articolo. Un approfondimento senza almeno un blocco sotto un articolo correlato non è pubblicato.
