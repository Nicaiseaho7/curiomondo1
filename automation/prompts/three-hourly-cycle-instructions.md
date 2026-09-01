# Ciclo editoriale automatico ogni 3 ore — CurioMondo

Questo file è il manuale operativo che ogni sessione Claude Code Remote attivata
dalla Routine oraria deve leggere e seguire integralmente, dall'inizio alla fine,
prima di scrivere qualunque cosa. Non improvvisare varianti: dove questo file
riporta markup letterale, va riusato esattamente in quella forma.

## 0. Lettura obbligatoria, in ordine

1. Questo file.
2. `AGENTS.md`
3. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
4. `automation/prompts/image-generation-contract.txt`
5. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
6. `curiomondo-site-manifest.json`
7. `automation/config.json`
8. `automation/live-sources.json`

Se uno di questi file manca o è incoerente con questo manuale, interrompere il
ciclo senza pubblicare nulla e segnalarlo (nessuna pubblicazione forzata).

### Accesso al repository in questa sessione

Le sessioni generate da questa Routine **non hanno il connettore
GitHub/le API GitHub** (limite dell'organizzazione: le Routine non possono
portare connettori). Funzionano invece normalmente il git da riga di comando
(clone, fetch, pull, push con le credenziali già disponibili nella sessione)
e gli strumenti di ricerca web. Se il repository non risulta già disponibile
in locale, usare `add_repo` (owner `Nicaiseaho7`, repo `curiomondo1`,
`access: "push"`) e poi clonarlo con git normale su `main`. Tutto il
coordinamento con GitHub Actions in questo ciclo (§4) avviene quindi solo
via git (push di file, poi poll con `git fetch`), mai via chiamate dirette
alle API GitHub.

## 1. Ricerca notizie

- Fonti primarie: i feed RSS Google News già filtrati in `automation/live-sources.json`
  (`trusted_publishers`: Reuters, Associated Press/AP News, Bloomberg, ANSA, AGI,
  Adnkronos, United Nations). Le query dei feed usano `when:1h`; dato che il ciclo
  gira ogni 3 ore, ripetere la ricerca coprendo l'intera finestra dall'ultima
  pubblicazione (guardare `CURIOMONDO-RELEASE-STATE.json` → `release_date`/`last_update`
  e i timestamp degli articoli più recenti in `notizie/`), non solo l'ultima ora.
- Riscontro aggiuntivo con WebSearch/WebFetch per confermare che una notizia sia
  reale, recente e correttamente riportata (titolo, cifre, nomi).
- **Termini ad alto rischio** (`automation/live-sources.json` → `high_risk_terms`:
  guerra, missile, raid, ucciso, morto, morti, vittime, accusa, terror, ostaggi,
  nucleare, elezioni, epidemia, pandemia): servono almeno 2 fonti indipendenti e
  attendibili che concordino sui fatti essenziali. Una dichiarazione da una sola
  parte in un conflitto non è mai presentata come fatto accertato.
- Escludere sempre: gossip, indiscrezioni non confermate, aggiornamenti minori senza
  conseguenze concrete, duplicati di notizie già pubblicate, dichiarazioni senza
  sviluppo reale.
- **Deduplica**: prima di scrivere, controllare `notizie/*.html` (titoli e slug) e
  `assets/data/search-index-v210.json` per verificare che CurioMondo non abbia già
  la stessa storia. Se la storia base esiste già, valutare se serve un aggiornamento
  sostanziale (nuovo sviluppo reale) oppure se non c'è nulla da pubblicare.

**Se nel ciclo non emerge nessuna notizia genuinamente nuova, significativa e
verificata: il ciclo termina qui, senza modificare nulla.** Non esiste un obbligo
di pubblicare per riempire lo slot orario.

## 2. Quante notizie pubblicare

Se emergono più notizie valide nello stesso ciclo, pubblicarle tutte (fino al
tetto `automation/config.json` → `articles.max_articles_per_cycle`, attualmente 8),
ma con **un solo commit/deploy per l'intero ciclo** (`max_deploys_per_cycle: 1`).
La notizia editorialmente più pesante del ciclo (per impatto, novità, portata)
diventa il nuovo blocco "featured"/Ultima ora in homepage; l'attuale featured
scende in cima all'"auto-rail". Le altre notizie del ciclo entrano in cima
all'auto-rail e alle card, con la card più vecchia che scorre giù/esce.

## 3. Regole editoriali del corpo articolo (invarianti, da `editorial-contract.txt`)

- Corpo `.art-body` tra **3.000 e 7.000 caratteri** di testo visibile (regola
  v257, in vigore dal 1° settembre 2026 ore 12:00 — sostituisce il precedente
  2.000-4.500), nessuna eccezione. **La lunghezza segue le informazioni
  disponibili, non un target fisso**: scrivi un articolo lungo quando la notizia
  ha davvero abbastanza sostanza verificata da riempire il corpo, e corto — ma
  sempre sopra i 3.000 caratteri — quando le informazioni verificate sono poche.
  Non allungare mai un articolo con riempitivo o ripetizioni solo per avvicinarti
  al tetto di 7.000. Se non si hanno almeno 3.000 caratteri di informazione
  verificata e non ripetitiva, non pubblicare quell'articolo come pezzo autonomo.
- **Zero ripetizioni**: nessun fatto, cifra, causa o conseguenza compare due volte,
  nemmeno parafrasata. Fare un passaggio anti-ridondanza frase per frase e
  paragrafo per paragrafo prima di contare i caratteri.
- Nessun sottotitolo H2/H3 dentro il corpo (i paragrafi bastano, come negli
  articoli esistenti).
- Ogni articolo contiene almeno un **gancio di conoscenza**: un paragrafo che
  spiega in modo semplice un elemento poco noto ma utile della notizia (istituzione,
  meccanismo, termine tecnico, procedura, luogo strategico, precedente storico).
  **Non esiste un box/markup dedicato per questo** — è un paragrafo normale dentro
  `art-body`, esattamente come negli articoli pubblicati (verificato leggendo il
  markup reale). Non inventare classi CSS nuove tipo `.cm-nugget`.
- Quando il tema lo giustifica, creare o collegare un **approfondimento evergreen**
  indicizzabile (vedi §6). L'eccezione è ammessa solo se davvero non esiste un
  contesto durevole utile.
- Almeno 2-3 fonti attendibili elencate in `art-sources`.

## 4. Regole immagini (vincolo specifico di questa automazione, più severo del
   protocollo generale del sito)

- **Se la notizia riguarda una persona pubblica reale e riconoscibile**: è
  ammesso generare il suo volto, ma **sempre e solo come ritratto/foto profilo
  neutrale isolato** (inquadratura testa-spalle o mezzobusto, sfondo neutro,
  espressione calma), **mai** inserito in una scena, situazione, luogo o momento
  ricostruito/scomodo. Questo vale sempre, non solo per i casi sensibili.
  - Nel workflow immagine: `is_portrait: true`.
  - Il testo `alt` deve contenere la frase esatta "ritratto editoriale neutrale"
    (in minuscolo), richiesta anche da `tools/predeploy.py`.
  - Nel markup `<figure>`: `data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="true|false" data-portrait-format="neutral-isolated"`.
- **Se la notizia non richiede il volto di una persona specifica**: immagine
  fotorealistica della scena/luogo/edificio/oggetto pertinente. Loghi e luoghi
  riconosciuti sono ammessi. `is_portrait: false`.
  - Nel markup `<figure>`: `data-ai-generated="true"` (+ `data-sensitive-context="true"`
    se il tema è sensibile, come negli esempi con `data-ai-generated="true"
    data-sensitive-context="true"`).
- Mai testo, watermark, didascalie o loghi editoriali dentro i pixel dell'immagine.
- Mai scene che raffigurino direttamente ferite, sangue, corpi, manette, funerali,
  pianto: per i temi sensibili senza volto specifico, restare su scene ambientali
  neutre (mezzi di soccorso, luoghi, strade transennate) senza vittime visibili.
- Sotto ogni immagine, `<figcaption>` con **esattamente**:
  `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`

### Come generare l'immagine (via richiesta file + GitHub Actions, non generazione diretta, NON bloccante)

Questa sessione non ha accesso a servizi di generazione immagini (rete
ristretta) e le sessioni orarie di questa Routine **non hanno il connettore
GitHub/le API GitHub Actions** (limite dell'organizzazione: le Routine non
possono portare connettori alle sessioni che generano). Il coordinamento con
il workflow immagine avviene quindi **solo con git semplice** (clone/pull/push),
che invece funziona regolarmente in ogni sessione con accesso al repository.

**Importante: la richiesta immagine è "fire-and-forget". Non si attende mai
il completamento del workflow immagine prima di pubblicare il testo.** Il
testo dell'articolo si pubblica sempre subito (vedi §4bis per il
placeholder); l'immagine reale arriva in un passaggio di backfill separato,
eventualmente in un ciclo successivo. Questo evita che un'attesa di alcuni
minuti per articolo (moltiplicata per più articoli nello stesso ciclo)
rischi di far scadere/bloccare la sessione automatica.

1. Scrivere il prompt in inglese seguendo `automation/prompts/image-generation-contract.txt`.
2. Per ogni articolo, creare un file di richiesta
   `automation/state/image-requests/<filename_base>.json` con:
   ```json
   {"prompt": "...", "filename_base": "<slug-notizia>-ai-v<NNN>", "article_path": "/notizie/<slug>.html", "alt_text": "...", "is_portrait": false, "sensitive": false}
   ```
   `filename_base` deve essere uno slug deterministico e unico (NNN = prossimo `site_version`).
   Aggiungere e pushare **tutti** i file di richiesta del ciclo in un unico
   commit `git add automation/state/image-requests/ && git commit -m "..." && git push origin main`.
   Questo push, per via del filtro `paths` nel workflow, avvia
   automaticamente `.github/workflows/genera-immagine-editoriale.yml`, che
   gira su un runner con rete piena, genera le immagini per tutte le
   richieste trovate, aggiorna `assets/data/editorial-images-v210.json`,
   cancella i file di richiesta elaborati e fa commit+push da solo su `main`.
3. **Non attendere.** Subito dopo il push della richiesta, procedere a
   scrivere e pubblicare l'articolo senza immagine reale (vedi §4bis),
   registrando ogni articolo in `automation/state/pending-images.json`. Il
   workflow immagine gira in parallelo, in modo indipendente dal ciclo che
   sta pubblicando il testo.

## 4bis. Pubblicare senza immagine e completare dopo (backfill)

### Placeholder mentre l'immagine è pending

- **Nell'articolo (`notizie/<slug>.html`)**: omettere del tutto il blocco
  `<figure class="article-image">...</figure>` (nessun placeholder visibile
  nel corpo — niente immagine è meglio di un'immagine/didascalia fuorviante).
  `tools/predeploy.py` non richiede `<figure>`: i controlli su didascalia,
  classificazione volto sensibile e alt ritratto sono tutti condizionali
  alla sua presenza (verificato leggendo `tools/predeploy.py`).
- **`og:image`/JSON-LD `image`** nello stesso articolo: usare l'URL assoluto
  del logo del sito, `https://curiomondo.it/curiomondo-logo-512.png` (gli
  URL assoluti sono esclusi dal controllo di file rotto/duplicati di
  `predeploy.py`, quindi non servono trucchi di query string qui).
- **Card homepage** (`featured`/`auto-rail`/`cards`, ovunque compaia questo
  articolo): usare come `src` (e come unico valore di `srcset`)
  `curiomondo-logo-512.png?pending=<slug>` — path relativo al logo già
  presente in repo, con una query string univoca per articolo. La query
  string evita il falso positivo del controllo "immagini duplicate in
  Ultime notizie/Tutte le notizie" (confronta le stringhe `@src` esatte su
  `auto-rail` e `#cards`), mentre il controllo di file rotto verifica
  comunque il file reale, perché la query viene sempre rimossa prima del
  controllo di esistenza. Mantenere `width`/`height` standard delle card
  (es. `800`/`533`) anche se il logo è quadrato: è solo estetica temporanea.
- **`assets/data/home-feed-v210.json`**: stesso placeholder (`image`,
  `imageAlt` = testo neutro tipo "CurioMondo", `srcset` con lo stesso path
  con query).

### Tracciamento — `automation/state/pending-images.json`

Per ogni articolo pubblicato senza immagine reale, aggiungere una voce:
```json
{"slug": "...", "article_path": "/notizie/<slug>.html", "filename_base": "<slug>-ai-v<NNN>", "is_portrait": false, "alt_text": "...", "requested_at": "ISO8601", "homepage_refs": ["featured"]}
```
`homepage_refs` elenca le sezioni homepage dove l'articolo compare
(`featured`, `auto-rail`, `cards` — spesso più di una).

### Backfill (ad ogni ciclo, PRIMA della ricerca di nuove notizie)

1. `git pull origin main`.
2. Per ogni voce in `automation/state/pending-images.json`, controllare se
   `assets/images/editorial-auto/<filename_base>-{480,800,1200}.webp`
   esistono ora nel repo (il workflow immagine li ha pubblicati in un
   momento imprecisato dopo la richiesta, in modo asincrono).
3. Se sì: inserire il `<figure>` reale nell'articolo con il markup standard
   di §5, aggiornare `og:image`/JSON-LD `image` con l'URL reale, sostituire
   il placeholder con i path reali in ogni sezione homepage elencata in
   `homepage_refs` e in `assets/data/home-feed-v210.json`, poi rimuovere la
   voce da `pending-images.json`.
4. Se ancora non pronta: lasciare la voce, nessun errore. Se una voce resta
   pending da più di ~48 ore, segnalarlo esplicitamente invece di ritentare
   in silenzio all'infinito.
5. Le modifiche di backfill possono andare in un commit dedicato (es.
   "Aggiorna immagini: <slug1>, <slug2>"), separato dalla pubblicazione di
   testo nuovo dello stesso ciclo — sempre passando da
   `python3 tools/predeploy.py` a 0 errori prima del push.

## 5. Template markup esatto da riusare

**Nota immagine pending**: il template sotto mostra il caso con immagine
reale già pronta (`FILENAME_BASE`). Se l'immagine per questo articolo è
ancora pending (§4bis): sostituire `og:image`/JSON-LD `image` con
`https://curiomondo.it/curiomondo-logo-512.png` e **omettere interamente**
il blocco `<figure class="article-image">...</figure>` dal corpo. Tutto il
resto del template resta identico.

### `<head>` (adattare titolo/descrizione/URL/JSON-LD)

```html
<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>TITOLO ARTICOLO | CurioMondo</title>
<meta name="description" content="SOTTOTITOLO/RIASSUNTO">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="https://curiomondo.it/notizie/SLUG.html">
<meta property="og:type" content="article">
<meta property="og:title" content="TITOLO ARTICOLO">
<meta property="og:description" content="SOTTOTITOLO/RIASSUNTO">
<meta property="og:url" content="https://curiomondo.it/notizie/SLUG.html">
<meta property="og:image" content="https://curiomondo.it/assets/images/editorial-auto/FILENAME_BASE-1200.webp">
<meta property="og:image:alt" content="ALT TESTO">
<meta name="theme-color" content="#071a33">
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="../assets/css/site-base-v210.css">
<link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=SITE_VERSION">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"NewsArticle",
"headline":"TITOLO ARTICOLO","description":"SOTTOTITOLO/RIASSUNTO","datePublished":"ISO8601",
"dateModified":"ISO8601","mainEntityOfPage":"https://curiomondo.it/notizie/SLUG.html",
"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo"},
"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},
"image":["https://curiomondo.it/assets/images/editorial-auto/FILENAME_BASE-1200.webp"]}</script>
<script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous"
 src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script>
</head>
```

### Corpo, immagine, insight box

```html
<body data-article-id="SLUG">
<div class="cm-reading-progress" aria-hidden="true"></div>
<header class="topbar">... (riusare header esistente da un articolo recente) ...</header>
<main class="wrap">
<div class="badge">CATEGORIA · Sottocategoria</div>
<h1>TITOLO ARTICOLO</h1>
<p class="subtitle">SOTTOTITOLO/RIASSUNTO</p>
<div class="meta">DATA · aggiornato alle ORA · CATEGORIA · <span id="readTime">N min di lettura</span></div>
<div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l'audio</button>
<button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div>

<figure class="article-image" data-ai-generated="true" data-sensitive-context="true|false"
 data-synthetic-likeness="public-figure" data-portrait-format="neutral-isolated">
<picture>
<img src="../assets/images/editorial-auto/FILENAME_BASE-800.webp"
 srcset="../assets/images/editorial-auto/FILENAME_BASE-480.webp 480w, ../assets/images/editorial-auto/FILENAME_BASE-800.webp 800w, ../assets/images/editorial-auto/FILENAME_BASE-1200.webp 1200w"
 sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533"
 alt="ALT TESTO DESCRITTIVO" loading="eager" decoding="async" fetchpriority="high"></picture>
<figcaption>Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.</figcaption>
</figure>

<div class="editorial-data"><div><strong>Keyword principale:</strong> KEYWORD</div>
<div><strong>URL SEO:</strong> /notizie/SLUG.html</div></div>

<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span>
<div class="cm-insight-grid"><div><b>N</b><small>ETICHETTA</small></div>
<div><b>N</b><small>ETICHETTA</small></div><div><b>N</b><small>ETICHETTA</small></div></div></section>

<article class="art-body" data-length-policy="3000-7000">
<p>Paragrafo 1...</p>
<!-- 5-8 paragrafi, incluso il gancio di conoscenza come paragrafo normale -->
<p>Ultimo paragrafo (prossimi sviluppi, senza ripetere quanto già detto)...</p>
</article>

<section class="curio-related" aria-labelledby="curio-related-title">
<h2 id="curio-related-title">Potrebbe interessarti anche…</h2>
<div class="curio-related-grid">
<a href="/notizie/ALTRO-SLUG-1.html"><small>Categoria</small><strong>Titolo correlato 1</strong></a>
<a href="/notizie/ALTRO-SLUG-2.html"><small>Categoria</small><strong>Titolo correlato 2</strong></a>
<a href="/notizie/APPROFONDIMENTO-SLUG.html"><small>Approfondimento · Tema</small><strong>Titolo approfondimento</strong></a>
</div></section>

<div class="art-sources"><h2>Fonti consultate</h2><ul>
<li><a href="URL_FONTE_1" rel="noopener noreferrer" target="_blank">Fonte 1 — descrizione</a></li>
<li><a href="URL_FONTE_2" rel="noopener noreferrer" target="_blank">Fonte 2 — descrizione</a></li>
</ul>
<p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: DATA, ore ORA italiane.</small></p>
</div>
</main><footer class="site-footer">... (riusare footer esistente, MAI la firma "cm-nicaise-signature") ...</footer>
<script src="../assets/js/site-common-v210.js" defer></script>
<script src="../assets/js/curiomondo-article-v210.js?v=SITE_VERSION" defer></script>
</body></html>
```

**Regole non negoziabili verificate da `tools/predeploy.py`** (leggerlo prima di
pubblicare, gira comunque nel passo 8 sotto, ma è utile saperlo prima):
- `data-length-policy="3000-7000"` deve essere presente e il testo visibile in
  `.art-body` deve essere davvero 3000-7000 caratteri.
- Nessuna frase duplicata, nessun paragrafo quasi-duplicato.
- `curio-related` non può linkare l'articolo stesso (stesso URL canonico o stesso
  titolo H1).
- `curiomondo-article-v210.js` deve avere `?v=NNN` con un numero, mai senza versione.
- Ogni `<img>` deve avere `alt`. Nessun link interno rotto.
- Nessuna immagine duplicata tra articoli (il registro/hash lo previene se si usa
  sempre `filename_base` univoco).
- **Nessuna di queste regole obbliga `<figure>` a esistere.** Se l'immagine è
  ancora pending, l'articolo si pubblica senza `<figure>` seguendo §4bis: è
  una pubblicazione pienamente valida per il gate automatico, non un'eccezione
  da giustificare.

### Template approfondimento evergreen (quando serve)

Vive fisicamente in `notizie/` (non in `approfondimenti/`, che è solo l'indice),
con slug tipo `come-funziona-...`/`perche-...`/`cosa-sono-...` senza data. Stessa
struttura dell'articolo ma: `<div class="badge">Approfondimento · Tema</div>`,
riga meta "Guida aggiornata il ...", **nessun `data-length-policy`** su `art-body`
(esente dal cancello 3000-7000), chiusura con
`<div class="art-flow-continuation"><p>...</p></div>` prima di `art-sources`.
Aggiungere link **in entrambe le direzioni**: dall'articolo di notizia verso
l'approfondimento (link inline nel testo o card in `curio-related` con
`<small>Approfondimento · Tema</small>`), e dall'approfondimento verso la notizia
in `curio-related`. Registrare il nuovo approfondimento anche in `approfondimenti/index.html`.

## 6. File da aggiornare per OGNI pubblicazione (in un unico batch/commit per ciclo)

1. `notizie/<slug>.html` — nuovo file per ogni articolo.
2. `approfondimenti/<slug>.html` + `approfondimenti/index.html` — solo se creato un evergreen.
3. `index.html`:
   - `class="ticker-track"` — **due copie** (nav focusabile + div `aria-hidden` duplicato
     con `tabindex="-1"` su ogni link): prepend dei nuovi titoli, restano sempre
     esattamente 10 link, i più vecchi escono.
   - `class="auto-rail"` (`auto-card`/`abody`/`ameta`): prepend, restano esattamente 5.
   - `id="cards"` (`class="card"`/`body`/`meta`): prepend in cima.
   - `class="featured"` (unico, con `<h1>`, `loading="eager" fetchpriority="high"`):
     sostituire con la notizia più pesante del ciclo; l'ex featured scende in cima
     all'auto-rail.
   - `class="cm-home-deep-links"` (esattamente 3 link): prepend se è stato creato un
     nuovo approfondimento, rimuovere il quarto più vecchio.
4. `notizie/index.html` — aggiungere `<li>` in cima alla lista archivio e aggiornare
   il contatore "N articoli, ordinati per data.".
5. `assets/data/search-index-v210.json` — prepend `{title, excerpt, url, section}`
   per ogni nuovo articolo; bump `version`.
6. `assets/data/home-feed-v210.json` — stessa cosa, schema più ricco (aggiunge
   `dateISO`, `dateLabel`, `image`, `imageAlt`, `imageWidth`, `imageHeight`, `srcset`),
   deve restare sincronizzato con `#cards` in homepage.
7. `feed.xml` — prepend un `<item>` per articolo (title/link/guid/pubDate RFC-822
   con offset `+0200`/`+0100`/description).
8. `sitemap.xml` — aggiungere `<url>` per articolo: `changefreq daily`, `priority 0.9`.
9. `news-sitemap.xml` — aggiungere `<url>`/`<news:news>` per articolo (`publication_date`
   ISO 8601 con offset) **e potare le voci più vecchie di 48 ore** (finestra rolling,
   richiesta dalla spec Google News Sitemap).
10. `assets/data/editorial-images-v210.json` — già aggiornato dal workflow immagine
    per ogni immagine generata; verificare solo che sia coerente.
11. `CURIOMONDO-RELEASE-STATE.json` + `RELEASE-STATE.json` + `curiomondo-site-manifest.json`
    — bump coerente di `site_version`/`currentVersion`/`articleCount`, aggiornare
    `last_update`, `release_date`, e in `curiomondo-site-manifest.json` il blocco
    `last_release` (news_added con gli slug, evergreen_added se applicabile).
12. `automation/state/pending-images.json` — aggiungere una voce per ogni
    articolo pubblicato senza immagine reale (§4bis); rimuovere le voci
    completate durante un backfill.

## 7. Sequenza operativa completa del ciclo

1. `git pull origin main` (partire sempre dallo stato pubblicato più recente).
2. **Backfill prima di tutto**: controllare `automation/state/pending-images.json`
   e completare con l'immagine reale ogni voce per cui le webp sono già
   comparse in repo (§4bis). Questo può già generare un commit a sé, prima
   di cercare notizie nuove.
3. Ricerca e verifica di tutte le notizie idonee nella finestra del ciclo (§1).
4. Se nessuna notizia valida → **fine ciclo qui** (il backfill del passo 2,
   se ha prodotto modifiche, resta comunque valido e va pubblicato).
5. Per ciascun articolo: decidere `is_portrait`/scena, scrivere il prompt
   immagine, pushare la richiesta (§4) **senza attendere il completamento**.
6. Scrivere subito l'HTML di ogni articolo (§4bis: nessun `<figure>`,
   placeholder logo su homepage/`og:image`), decidere il nuovo "featured", e
   aggiornare **tutti** i file di §6 in modo coerente tra loro, incluso
   `automation/state/pending-images.json`.
7. `pip install -r automation/requirements.txt` (garantisce `lxml`), poi
   `python3 tools/predeploy.py`. Se l'exit code non è 0, **non pubblicare**:
   correggere gli errori riportati o, se non risolvibili in questo ciclo,
   abortire senza fare commit.
8. Un solo `git add -A && git commit && git push` verso `main` per l'intero
   ciclo, con messaggio che elenca gli articoli pubblicati (e se pending
   immagine, dirlo nel messaggio).

Se un passaggio fallisce (predeploy che non passa, notizia che non regge la
verifica), quell'articolo (o l'intero ciclo, se serve) salta senza pubblicare
nulla di non conforme. La sola immagine non ancora pronta **non è più un
motivo per non pubblicare**: si pubblica il testo e si completa dopo (§4bis).
Meglio un ciclo senza pubblicazioni valide che un articolo che viola il
protocollo.
