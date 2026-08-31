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

- Corpo `.art-body` tra **2.000 e 4.500 caratteri** di testo visibile, nessuna
  eccezione. Se non si hanno almeno 2.000 caratteri di informazione verificata e
  non ripetitiva, non pubblicare quell'articolo come pezzo autonomo.
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

### Come generare l'immagine (workflow, non generazione diretta)

Questa sessione non ha accesso a servizi di generazione immagini (rete
ristretta). Per ogni articolo:
1. Scrivere il prompt in inglese seguendo `automation/prompts/image-generation-contract.txt`.
2. Triggerare `.github/workflows/genera-immagine-editoriale.yml` con
   `mcp__github__actions_run_trigger` (`method: run_workflow`, `workflow_id: genera-immagine-editoriale.yml`,
   `ref: main`, `inputs: {prompt, filename_base, article_path, alt_text, is_portrait, sensitive}`).
   `filename_base` deve essere uno slug deterministico e unico, es.
   `<slug-notizia>-ai-v<NNN>` (NNN = prossimo `site_version`).
3. Individuare la run con `mcp__github__actions_list` (`method: list_workflow_runs`,
   `workflow_runs_filter: {event: "workflow_dispatch"}`), poi attenderla con
   `mcp__github__actions_get` (`method: get_workflow_run`) finché `status == "completed"`.
   Se `conclusion != "success"`, leggere i log con `mcp__github__get_job_logs`
   (`run_id`, `failed_only: true`, `return_content: true`) e NON pubblicare quel
   singolo articolo (gli altri del ciclo possono proseguire se non dipendono da esso).
4. Dopo il successo, `git pull origin main` per prendere i file appena pubblicati
   dal workflow: `assets/images/editorial-auto/<filename_base>-480.webp`,
   `-800.webp`, `-1200.webp`, e la voce aggiornata in
   `assets/data/editorial-images-v210.json`.

## 5. Template markup esatto da riusare

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

<article class="art-body" data-length-policy="2000-4500">
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
- `data-length-policy="2000-4500"` deve essere presente e il testo visibile in
  `.art-body` deve essere davvero 2000–4500 caratteri.
- Nessuna frase duplicata, nessun paragrafo quasi-duplicato.
- `curio-related` non può linkare l'articolo stesso (stesso URL canonico o stesso
  titolo H1).
- `curiomondo-article-v210.js` deve avere `?v=NNN` con un numero, mai senza versione.
- Ogni `<img>` deve avere `alt`. Nessun link interno rotto.
- Nessuna immagine duplicata tra articoli (il registro/hash lo previene se si usa
  sempre `filename_base` univoco).

### Template approfondimento evergreen (quando serve)

Vive fisicamente in `notizie/` (non in `approfondimenti/`, che è solo l'indice),
con slug tipo `come-funziona-...`/`perche-...`/`cosa-sono-...` senza data. Stessa
struttura dell'articolo ma: `<div class="badge">Approfondimento · Tema</div>`,
riga meta "Guida aggiornata il ...", **nessun `data-length-policy`** su `art-body`
(esente dal cancello 2000-4500), chiusura con
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

## 7. Sequenza operativa completa del ciclo

1. `git pull origin main` (partire sempre dallo stato pubblicato più recente).
2. Ricerca e verifica di tutte le notizie idonee nella finestra del ciclo (§1).
3. Se nessuna notizia valida → **fine ciclo, nessuna modifica, nessun commit**.
4. Per ciascun articolo: decidere `is_portrait`/scena, scrivere il prompt immagine,
   triggerare il workflow `genera-immagine-editoriale.yml` (§4).
5. Attendere il completamento di tutte le run immagine di questo ciclo.
6. `git pull origin main` per prendere le immagini appena pubblicate.
7. Scrivere l'HTML di ogni articolo (§5), decidere il nuovo "featured", e
   aggiornare **tutti** i file di §6 in modo coerente tra loro.
8. `pip install -r automation/requirements.txt` (garantisce `lxml`), poi
   `python3 tools/predeploy.py`. Se l'exit code non è 0, **non pubblicare**:
   correggere gli errori riportati o, se non risolvibili in questo ciclo,
   abortire senza fare commit.
9. Un solo `git add -A && git commit && git push` verso `main` per l'intero ciclo,
   con messaggio che elenca gli articoli pubblicati.

Se un passaggio fallisce (immagine non generata, predeploy che non passa,
notizia che non regge la verifica), quell'articolo (o l'intero ciclo, se serve)
salta senza pubblicare nulla di non conforme. Meglio un ciclo senza pubblicazioni
che un articolo che viola il protocollo.
