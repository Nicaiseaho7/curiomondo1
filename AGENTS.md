# Istruzioni obbligatorie per agenti IA

## REVISIONE v503 — GATE PROPORZIONATO E AUTORIPARAZIONE

**Data:** 22 settembre 2026  
**Stato:** obbligatorio, permanente e prevalente sulle regole incompatibili precedenti.

L'obiettivo operativo è pubblicare un numero maggiore di articoli interessanti senza ridurre accuratezza, trasparenza o sicurezza.

- Per notizie ordinarie e contenuti di servizio è sufficiente una fonte primaria o ufficiale autentica e competente. La seconda conferma è consigliata, non obbligatoria.
- Per flash, notizie ordinarie e servizio basta un solo elemento concreto di utilità o valore aggiunto. Due elementi sono richiesti soltanto per analisi e approfondimenti autonomi.
- La rilevanza nazionale, l'esclusività e la pubblicazione entro 24 ore non sono requisiti. Sono ammesse notizie locali, di nicchia, culturali, sportive, di spettacolo e sviluppi fino a sette giorni o oltre quando ancora attuali, ricercati, utili o nuovi per CurioMondo.
- Una storia già trattata può produrre un nuovo articolo se cambia l'angolazione, il pubblico, la conseguenza o l'utilità. È duplicato soltanto il contenuto sostanzialmente identico.
- Un difetto tecnico riparabile non comporta lo scarto dell'articolo. L'agente è autorizzato a correggere autonomamente file, indici, feed, sitemap, canonical, dati strutturati, immagini, collegamenti, categorie, cache-busting e pipeline necessari alla pubblicazione, limitandosi al repository CurioMondo e preservando i contenuti già validi.
- Dopo una riparazione, rieseguire il gate tecnico. Dichiarare conclusa la pubblicazione solo dopo il superamento dei controlli predeploy e live.
- Restano bloccanti: fatti inventati, fonti false, accuse o dati sensibili non verificati, citazioni inesistenti, immagini fuorvianti, violazioni legali, contenuti privi di sostanza e problemi tecnici non risolti dopo i tentativi sicuri di riparazione.

Il principio è: **riparare e pubblicare quando la storia è valida; bloccare soltanto quando il difetto editoriale non è sanabile o il rilascio tecnico resta non valido.**


## Standard scrittura professionale v502 — prevalenza assoluta sul testo pubblico

Dal 22 settembre 2026, ore 06:00 (Europe/Rome), ogni nuovo articolo CurioMondo e ogni revisione richiesta di un articolo già pubblicato seguono `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`.

Questo file prevale su qualunque istruzione precedente incompatibile relativa a titolo, lead, piramide invertita, paragrafi, attribuzione, citazioni, numeri, stile, meta-commenti, contesto, SEO, lunghezza, sottotitoli e chiusura.

Sostituisce in particolare:

- le soglie fisse di caratteri (v248, v257 e successive, compreso l’obbligo 3.000–7.000);
- l’obbligo di allungare un pezzo per raggiungere una fascia;
- il divieto meccanico di H2/H3 nel corpo quando un sottotitolo informativo aiuta davvero la lettura.

Non sostituisce:

- il gate di rischio e la verifica delle fonti (`PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`, revisione v471);
- `PROTOCOLLO-SCOPERTA-NOTIZIE.md`;
- il protocollo immagini;
- il gate tecnico di pubblicazione completa.

Le fasce flash / standard / approfondimento restano un orientamento di formato, non un obiettivo di riempimento. Se la materia verificata sta sotto le 300 parole, il pezzo è un flash. Se manca materia, non si pubblica.

I nuovi articoli non devono dichiarare `data-length-policy="3000-7000"`.


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

1. `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`
2. `PROTOCOLLO-SCOPERTA-NOTIZIE.md`
3. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
4. `automation/prompts/image-generation-contract.txt`
5. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`
6. `PROTOCOLLO-REDAZIONE-CORPO.md`
7. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
8. `curiomondo-site-manifest.json`

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. **I protagonisti devono essere persone, maglie e marchi veri: vietato inventare volti, extra generici o divise di fantasia.** Cercare foto di riferimento reali prima di generare; se il lettore non riconoscerebbe il soggetto, scartare e rigenerare. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Prevalenza ricerca notizie — 19 settembre 2026
Per richieste di ultime notizie e per la fase di scoperta dei cicli editoriali, `PROTOCOLLO-SCOPERTA-NOTIZIE.md` è obbligatorio e prevale sulle vecchie priorità che mettono le agenzie prima delle fonti ufficiali o dei documenti primari. La regola delle cinque storie riguarda l’output di scouting richiesto dall’utente e non obbliga a pubblicare contenuti che non superano i gate editoriali.

## Regola editoriale articoli v317 — superata per la scrittura da v502
Ogni articolo segue `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` per il testo pubblico e il protocollo 4.0 in `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md` per gate di rischio, originalità e AdSense. Piramide invertita; lead con le 5 W quando note; nessuna ripetizione, prima persona, enfasi, riempitivo, elenco di fonti nel corpo o nota interna. La lunghezza dipende dalla materia verificata, non da una quota. È vietato spiegare parole difficili nel corpo della notizia: usare un lessico chiaro oppure creare o collegare una pagina di approfondimento quando serve. Se manca materia verificata, l'esito è `NON PUBBLICARE — motivo`.

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
