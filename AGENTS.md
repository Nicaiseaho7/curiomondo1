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

## eBook Domanda del giorno — dal 28 settembre 2026
Ogni nuovo eBook della Domanda del giorno è un libro breve: **25.000 parole** (tolleranza 22.000–32.000), **8–12 capitoli**, una schermata per capitolo. Deve essere indicizzato (`index,follow`, canonical, sitemap, indice di ricerca). Gli eBook già pubblicati non si riscrivono per questa regola. Dettaglio in `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`.

## Categorie della home — mai mescolate
In ogni sezione della homepage (Sport, Politica, Cronaca e le altre) possono comparire solo notizie di quella categoria. Una card di un'altra categoria è un errore bloccante. Dopo ogni pubblicazione rieseguire `node tools/render_home_editorial.js`: aggiorna sezioni, Ultima ora e ticker «Ultime notizie». `tools/predeploy.py` rifiuta la home se una sezione è mista o se il ticker è vuoto.

## Primo piano
Le ultime notizie, in ordine di pubblicazione, occupano sempre il carosello in primo piano. La più recente è la prima slide. Non si lascia una notizia più vecchia davanti a una più nuova. Vale per ogni aggiornamento del feed, qualunque sia il nome del campo data.





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

**Curiosità e approfondimenti (obbligatorio, 28 settembre 2026):** prima di creare o rivedere una **curiosità** o un **approfondimento** (guide evergreen, pagine in `/approfondimenti/`, spiegazioni «che cos’è / come funziona / perché»), leggere integralmente anche `PROTOCOLLO-CURIOSITA-E-APPROFONDIMENTI.md`. Quel file **prevale** sulle guide brevi tipo scheda e sul testo superficiale: servono contenuti premium, documentati e di reale profondità. Se manca o non si può rispettare, non pubblicare la guida.

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. **I protagonisti devono essere persone, maglie e marchi veri: vietato inventare volti, extra generici o divise di fantasia.** Cercare foto di riferimento reali prima di generare; se il lettore non riconoscerebbe il soggetto, scartare e rigenerare. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Prevalenza ricerca notizie — 19 settembre 2026
Per richieste di ultime notizie e per la fase di scoperta dei cicli editoriali, `PROTOCOLLO-SCOPERTA-NOTIZIE.md` è obbligatorio e prevale sulle vecchie priorità che mettono le agenzie prima delle fonti ufficiali o dei documenti primari. La regola delle cinque storie riguarda l’output di scouting richiesto dall’utente e non obbliga a pubblicare contenuti che non superano i gate editoriali.



## Marchio intestazione CurioMondo — obbligatorio e identico su ogni articolo (27 settembre 2026)
Il **nome del sito** in intestazione di **ogni** articolo, presente e futuro, deve essere **sempre e solo** `CurioMondo` (testo concatenato esatto, mai «Curio Mondo», «CM», «curiomondo» o altre varianti).

Markup **canonico obbligatorio** (non semplificare):

```html
<link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633">
…
<a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a>
<button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button>
```

- `title` e `publisher` JSON-LD: suffisso/nome **`CurioMondo`**
- Predeploy blocca se il marchio non è esattamente `CurioMondo`
- Violazione = articolo non pubblicabile


## Divieto sottotitoli H2/H3 nelle notizie — 27 settembre 2026
Nelle pagine **notizie** (flash e standard) **non** usare H2/H3 nel corpo `.art-body`: solo paragrafi continui. H2/H3 ammessi solo negli **approfondimenti**. Vedi `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` e `PROTOCOLLO-REDAZIONE-CORPO.md`.

## Divieto fonti nel corpo — 27 settembre 2026 (fail-closed)
**Mai** inserire nel corpo dell'articolo (`.art-body`) righe o paragrafi `Fonte: …`, `Fonti: …`, elenchi di testate a fine pezzo o formule equivalenti. Le fonti con link stanno **solo** nella sezione **«Fonti consultate»** (`.art-sources`) sotto l'articolo. L'attribuzione nel testo, se indispensabile, è solo narrativa («secondo il comunicato FIGC…»), mai una riga `Fonte:`. Violazione = articolo non pubblicabile. Vedi `PROTOCOLLO-REDAZIONE-CORPO.md` e `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`.

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

## Integrità tecnica e verifica automatica — obbligatorio

- Prima di ogni commit editoriale eseguire `python3 tools/repository_integrity_gate.py`. Dopo la sincronizzazione di tutte le superfici eseguire anche `python3 tools/predeploy.py`; entrambi devono terminare con exit code 0 prima del push.
- Il gate di integrità deve validare UTF-8 e sintassi di tutti i JSON, le superfici pubbliche obbligatorie e le firme reali delle immagini editoriali. Un file troncato, binario al posto di testo o con estensione falsa blocca il deploy.
- Netlify ripete il gate prima e dopo ogni rigenerazione della build. Nessun errore di decodifica può essere ignorato o sostituito silenziosamente.
- Dopo il push, controllare l'URL pubblico dell'articolo, immagine hero, homepage, categoria, archivio, feed, sitemap e News Sitemap. Un commit presente su GitHub non equivale a una pubblicazione riuscita.
- Dopo ogni pubblicazione eseguire anche `python3 tools/verify_live_publication.py --slug SLUG --title "TITOLO"`. Il controllo deve decodificare come UTF-8 e JSON il file live `assets/data/home-feed-v210.json` e confermare la presenza degli asset `home-allocation-v504.js`, `home-sections-v504.js` e `home-sections-v504.css`. Un feed remoto troncato o binario è bloccante perché lascia visibile il vecchio fallback della homepage.
- Dichiarare `PUBBLICATO` soltanto quando tutti i controlli live rispondono correttamente e contengono il nuovo slug. In caso contrario diagnosticare, autoriparare e rieseguire l'intero ciclo senza chiedere una nuova autorizzazione editoriale.

## Regola approfondimenti coerente
Nessun glossario o gancio didascalico è obbligatorio dentro la notizia. Un approfondimento autonomo va creato o collegato **solo quando aggiunge valore durevole, non ridondante e realmente utile**. Se esiste già una guida equivalente, collegarla invece di crearne una nuova. Le spiegazioni tematiche necessarie vivono nella pagina dedicata; la notizia resta concentrata sui fatti.

## Protocollo curiosità e approfondimenti — v1.0 (28 settembre 2026)
**Obbligatorio e fail-closed.** File: `PROTOCOLLO-CURIOSITA-E-APPROFONDIMENTI.md`.

- Vietati contenuti brevi, superficiali, generici o da «scheda informativa».
- Obiettivo: articolo editoriale premium (spiegazione, origine, contesto, cause, funzionamento, dati, falsi miti, limiti di ciò che non si sa).
- Curiosità: risposta rapida + viaggio nell’argomento (orientativo 800–2.000+ parole secondo complessità).
- Approfondimento: sistematico e completo (orientativo 1.500–3.000+, grandi temi anche 5.000+ se la materia verificata lo merita).
- Nessuna lunghezza fissa da riempire: niente ripetizioni, niente filler; se manca materia, non pubblicare.
- Ricerca reale su fonti primarie/istituzionali/scientifiche prima di scrivere; ipotesi distinte dai fatti.
- H2/H3 ammessi e utili; box «In breve / Il dato / Attenzione» solo se migliorano la lettura.
- Prevale sulle guide corte e sulle abitudini da chatbot. Non sostituisce AdSense, immagini, marchio e gate tecnici.

## Regola permanente v470 — evergreen sotto l’articolo
Ogni approfondimento evergreen deve comparire **sotto ogni notizia che lo riguarda**, nel blocco visibile `.cm-evergreen-reader` (kicker, titolo, anteprima, `Leggi l’approfondimento →`). Non basta l’indice `/approfondimenti/` né una card in `curio-related`. Posizione: subito dopo `.art-body`. Massimo due blocchi per articolo. Un approfondimento senza almeno un blocco sotto un articolo correlato non è pubblicato.

## Deploy Netlify — nessun build command, nessun netlify.toml

**Data:** 23 settembre 2026 — obbligatorio.

CurioMondo e un sito statico: Netlify deve limitarsi a pubblicare la cartella.
`netlify.toml` e `requirements-netlify.txt` non devono esistere nel repository,
coerentemente con il divieto gia previsto dal protocollo maestro.

Il 22 settembre un build command in `netlify.toml` installava Python e lxml e
poi eseguiva quattro gate dentro la build. Ha bloccato i deploy per un giorno —
quattordici commit fra riparazioni e deploy forzati — e con essi dodici articoli
gia conformi: i gate passavano, la build no. Una pipeline dentro il deploy e una
macchina in piu che puo guastarsi, e quando si guasta non pubblica niente.

I controlli restano obbligatori ma **prima del push**, dove un errore ferma
l'articolo sbagliato invece dell'intero sito:

    python3 tools/repository_integrity_gate.py
    python3 tools/adsense_deploy_gate.py
    python3 tools/predeploy.py

`tools/pubblica_articolo.py` li esegue gia tutti e tre a ogni pubblicazione.

## Immagini forze dell’ordine — niente targhe (27 settembre 2026)
Nelle illustrazioni di auto di **Carabinieri, Polizia, Guardia di Finanza, ambulanza, vigili del fuoco** **non** inserire mai targhe (neppure inventate o sfocate leggibili). Paraurti pulito, senza riquadro targa. Vale anche per veicoli esteri di polizia.


## Vietati i commenti personali / meta della redazione nel corpo — 27 settembre 2026

Nelle **notizie** (`notizie/*.html`) è **vietato** inserire nel corpo `.art-body` frasi meta, di metodo o di «voce CurioMondo», ad esempio:
- «CurioMondo segue il caso con sobrietà…»
- «CurioMondo aggiorna solo su fatti di agenzia…»
- «CurioMondo non pubblica dettagli…»
- «Non anticipiamo sentenze…» / «Aggiorneremo solo con fonti…»
- qualsiasi chiusura in prima persona redazionale o auto-elogio del metodo

Il pezzo racconta **fatti, contesto e fonti**. Metodo, disclosure IA e firma stanno **solo** in `art-sources` / footer / pagine istituzionali (`Come lavoriamo`), non nei paragrafi della notizia.
Violazione = correggere prima del go-live.


## Immagini incidenti / morti sul lavoro — vietati rottami e scene macabre (27 settembre 2026)

Nelle hero e illustrazioni di **notizie su incidenti stradali, morti sul lavoro, cantieri, investimenti, incidenti autostradali**:
- **MAI** auto rovesciate, carcasse, lamiere contorte, vetri infranti in primo piano, sangue, corpi, barelle, scene di soccorso gore o “re-enactment” spettacolari dell’incidente.
- **Sì** a immagini sobrie di contesto: cantiere segnalato, coni e luci, tratto di strada vuoto, barriere, autostrada di notte **senza** veicolo incidentato.
- Niente targhe (anche inventate) su qualsiasi veicolo.
- Tone: documentario, rispettoso della vittima, non tabloid.

Violazione = rigenerare l’immagine e aggiornare hero/og prima del go-live. **Non deve più succedere.**

