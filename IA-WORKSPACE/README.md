# IA-WORKSPACE — CurioMondo

Workspace ridotto e autosufficiente per **creare nuovi articoli di notizie
(`notizie/`)** e integrarli in tutti i punti del sito, senza avere bisogno
dell'intero repository.

**Ogni percorso in questa cartella corrisponde 1:1 al percorso reale nel
repository GitHub**, a partire dalla radice del sito. Esempio:
`IA-WORKSPACE/notizie/index.html` → nel repo è `notizie/index.html`.
Quando restituisci i file aggiornati, **mantieni esattamente questi stessi
percorsi/nomi file**: chi li reintegra deve solo sovrascrivere/aggiungere
file allo stesso posto, senza indovinare nulla.

Questa cartella riguarda **solo `notizie/` (le notizie)**. Biblioteca,
Domanda del giorno e Approfondimenti sono contenuti separati con regole
proprie e non sono nello scope di questo workspace (l'indice di
`approfondimenti/` è incluso solo perché una notizia può doverlo collegare).

---

## 0. Lettura obbligatoria, in quest'ordine, prima di scrivere qualunque cosa

1. Questo README.
2. `AGENTS.md`
3. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
4. `automation/prompts/image-generation-contract.txt`
5. `automation/prompts/editorial-contract.txt`
6. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
7. `curiomondo-site-manifest.json`
8. `automation/prompts/three-hourly-cycle-instructions.md` — è il manuale
   operativo più dettagliato: contiene il template HTML esatto da riusare
   (§5) e la checklist file-per-file (§6) su cui si basa questo README.
   In caso di dubbio o conflitto, **quel file vince** perché è il più
   aggiornato e il più specifico.

Se una di queste regole non può essere rispettata per un articolo, **non
pubblicare quell'articolo** (meglio niente che un pezzo non conforme).

---

## 1. Dove va salvato un nuovo articolo

- File: **`notizie/<slug-notizia>.html`** (un file HTML per articolo, slug
  minuscolo con trattini, spesso con la data in fondo, es.
  `notizie/istat-inflazione-agosto-2026-energia-3-3-per-cento.html`).
- **Usa come riferimento esatto** l'articolo completo già incluso qui:
  `notizie/siccita-po-lombardia-piemonte-record-autobotti-1-settembre-2026.html`.
  È un articolo reale, pubblicato, che rispetta tutte le regole correnti
  (v257): riusa la sua struttura `<head>`, il markup del corpo, della
  figure/immagine, del box fonti e del blocco "Potrebbe interessarti anche"
  copiandone la forma esatta e cambiando solo i contenuti.
- Asset CSS/JS richiamati in `<head>`/fondo pagina (**non modificarli, non
  servono file nuovi**, esistono già nel sito reale):
  `assets/css/site-base-v210.css`, `assets/css/curiomondo-article-v211.css?v=SITE_VERSION`,
  `assets/js/site-common-v210.js`, `assets/js/curiomondo-article-v210.js?v=SITE_VERSION`
  (il numero dopo `?v=` è l'attuale `site_version`, vedi §5 sotto).
- Se l'articolo merita anche un **approfondimento evergreen** (guida
  autonoma, senza data, tipo "come funziona…"/"perché…"): va anch'esso
  fisicamente in `notizie/<slug-guida>.html` (stessa struttura, senza
  `data-length-policy`), **non** in `approfondimenti/`, che contiene solo
  l'indice. Registralo anche in `approfondimenti/index.html`.
- **Prima di scrivere un nuovo articolo**, controlla che la stessa storia
  non sia già raccontata in `notizie/index.html` (l'elenco archivio incluso
  qui) o in `assets/data/search-index-v210.json`, per evitare duplicati.

### Regole editoriali invarianti del corpo (`editorial-contract.txt` + manifest)

- Corpo `<article class="art-body" data-length-policy="3000-7000">`: tra
  **3.000 e 7.000 caratteri** di testo visibile. Nessuna eccezione: se non
  ci sono abbastanza informazioni verificate per superare i 3.000 caratteri
  senza riempitivo, l'articolo non si pubblica come pezzo autonomo.
- **Zero ripetizioni**: nessun fatto/cifra/causa/conseguenza compare due
  volte, nemmeno parafrasato. Fai un passaggio anti-ridondanza prima di
  contare i caratteri.
- Niente H2/H3 dentro il corpo: solo paragrafi `<p>`.
- Almeno un paragrafo "gancio di conoscenza": spiega in modo semplice un
  elemento poco noto ma utile (istituzione, meccanismo, termine tecnico,
  precedente storico). È un paragrafo normale, non un box/classe dedicata.
- Almeno 2-3 fonti attendibili in `<div class="art-sources">`.
- Sezione `<section class="curio-related">` con 3 link ad altri articoli
  reali del sito (mai un link all'articolo stesso, né stesso H1).

---

## 2. Dove vanno salvate le immagini degli articoli

- Cartella corretta: **`assets/images/editorial-auto/`** (unica cartella
  "viva" per le nuove immagini editoriali; le altre sottocartelle
  `assets/images/editorial-vNNN/` che potresti vedere nel repo completo
  sono archivio storico e **non vanno usate**).
- Per ogni articolo servono **3 file WebP**, stesso nome base, tre larghezze:
  ```
  assets/images/editorial-auto/<filename_base>-480.webp
  assets/images/editorial-auto/<filename_base>-800.webp
  assets/images/editorial-auto/<filename_base>-1200.webp
  ```
  `<filename_base>` = slug descrittivo univoco, es.
  `siccita-po-lombardia-piemonte-1-settembre-2026-ai-v258` (i 6 file WebP
  inclusi in questo workspace sotto `assets/images/editorial-auto/` sono
  due esempi reali già pubblicati, da usare come riferimento di formato/peso).
- Specifiche immagine (da `image-generation-contract.txt` e
  `AI-EDITORIAL-IMAGE-PROTOCOL.md`, lettura obbligatoria integrale prima di
  generare qualunque immagine):
  - Ultra-realistica, fotografica, mai flat/vector/illustrazione/infografica.
  - Scena **completamente nuova** per ogni articolo: mai riuso, crop,
    resize, filtro o rinomina di un'immagine già pubblicata.
  - **Mai testo, watermark o didascalie dentro i pixel dell'immagine.**
  - Persone pubbliche: consentite in scena solo per notizie "ordinarie";
    per incidenti/morte/malattia/violenza/lutto e altri temi sensibili è
    **obbligatorio** un ritratto neutrale isolato (testa-spalle o mezzobusto,
    sfondo neutro, nessuna scena ricostruita).
- Nell'HTML dell'articolo, subito sotto l'immagine, la `<figcaption>` deve
  contenere **esattamente**:
  `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
- Se il volto di una persona pubblica è raffigurato, il tag `<figure>`
  richiede anche `data-synthetic-likeness="public-figure"
  data-sensitive-context="true|false"` (+ `data-portrait-format="neutral-isolated"`
  se sensibile) — vedi il file di esempio in `notizie/` per la sintassi
  esatta del markup `<figure>`/`<picture>`.
- **Se un'immagine non è ancora pronta**: pubblica comunque il testo
  dell'articolo omettendo del tutto il blocco `<figure>`, usa
  `https://curiomondo.it/curiomondo-logo-512.png` come `og:image`/JSON-LD
  `image`, e come immagine card in homepage/dati usa
  `curiomondo-logo-512.png?pending=<slug>`. Registra l'articolo in
  `automation/state/pending-images.json` (schema e dettagli completi in
  `automation/prompts/three-hourly-cycle-instructions.md` §4bis). Appena
  l'immagine reale è pronta, sostituiscila ovunque e rimuovi la voce da
  `pending-images.json`.

---

## 3. Tutti i file da modificare per far comparire il nuovo articolo nel sito

Per **ogni** articolo pubblicato, aggiorna in modo coerente tra loro tutti
questi file (tutti inclusi in questo workspace, pronti da modificare):

| # | File | Cosa fare |
|---|------|-----------|
| 1 | `notizie/<slug>.html` | Nuovo file, uno per articolo (vedi §1). |
| 2 | `notizie/index.html` | Aggiungi una nuova `<li>` in cima alla lista archivio e aggiorna il contatore "N articoli, ordinati per data.". |
| 3 | `index.html` → `class="ticker-track"` | **Due copie** identiche (nav accessibile + div `aria-hidden` duplicato): prepend del nuovo titolo, restano sempre **esattamente 10** link, il più vecchio esce. |
| 4 | `index.html` → `class="auto-rail"` | Prepend della card (titolo + estratto + immagine), restano **esattamente 5**. |
| 5 | `index.html` → `id="cards"` | Prepend della card in cima alla griglia "Tutte le notizie". |
| 6 | `index.html` → `class="featured"` (unico) | Se questo è l'articolo editorialmente più importante del momento, sostituiscilo con il nuovo (l'attuale "featured" scende in cima all'auto-rail). |
| 7 | `index.html` → `class="cm-home-deep-links"` | Solo se hai creato un nuovo approfondimento: prepend del link (restano 3), rimuovi il quarto più vecchio. |
| 8 | `assets/data/home-feed-v210.json` | Prepend di un oggetto in `items` (schema completo sotto) e bump di `version`. Deve restare sincronizzato con `#cards` in homepage. |
| 9 | `assets/data/search-index-v210.json` | Prepend di un oggetto in `items` (schema più semplice, sotto) e bump di `version`. |
| 10 | `feed.xml` | Prepend di un `<item>` (title/link/guid/pubDate RFC-822 con offset `+0200`/`+0100`/description). |
| 11 | `sitemap.xml` | Aggiungi `<url>` per l'articolo: `changefreq daily`, `priority 0.9`. |
| 12 | `news-sitemap.xml` | Aggiungi `<url>`/`<news:news>` (con `publication_date` ISO 8601 e offset) **e rimuovi le voci più vecchie di 48 ore** (finestra rolling richiesta dalla Google News Sitemap). |
| 13 | `_redirects` | Aggiungi una riga con lo stesso pattern delle altre: `/notizie/<slug>  /notizie/<slug>.html  301!` (alias extensionless → URL canonica). |
| 14 | `assets/data/editorial-images-v210.json` | Se generi le immagini, registra qui la nuova voce con lo stesso schema delle esistenti (coerenza controllata da `tools/predeploy.py`). |
| 15 | `curiomondo-site-manifest.json` + `CURIOMONDO-RELEASE-STATE.json` + `RELEASE-STATE.json` | Bump coerente di `site_version`/`currentVersion`/conteggio articoli, aggiorna data/ultimo rilascio e (nel manifest) il blocco `last_release` con gli slug pubblicati. |
| 16 | `automation/state/pending-images.json` | Aggiungi una voce se pubblichi senza immagine reale (§4bis del manuale ciclo); rimuovi la voce quando l'immagine viene completata. |
| 17 | `approfondimenti/index.html` | Solo se hai creato un nuovo approfondimento evergreen: aggiungilo all'indice. |

**Non serve toccare** `assets/css/*` o `assets/js/*`: un nuovo articolo
riusa sempre le classi e gli script già esistenti nel sito. Non sono
inclusi in questo workspace per questo motivo.

### Schema `assets/data/home-feed-v210.json` (oggetto in `items`, in cima)

```json
{
  "title": "Titolo esatto come nell'H1",
  "excerpt": "Estratto/sottotitolo breve",
  "url": "/notizie/<slug>.html",
  "section": "Macro-categoria / Categoria / Sottocategoria",
  "dateISO": "2026-09-01T17:30:00+02:00",
  "dateLabel": "2026-09-01",
  "image": "/assets/images/editorial-auto/<filename_base>-800.webp",
  "imageAlt": "Testo alternativo descrittivo dell'immagine",
  "imageWidth": 800,
  "imageHeight": 533,
  "srcset": "/assets/images/editorial-auto/<filename_base>-480.webp 480w, /assets/images/editorial-auto/<filename_base>-800.webp 800w, /assets/images/editorial-auto/<filename_base>-1200.webp 1200w"
}
```

### Schema `assets/data/search-index-v210.json` (oggetto in `items`, in cima)

```json
{
  "title": "Titolo esatto come nell'H1",
  "excerpt": "Estratto/sottotitolo breve",
  "url": "/notizie/<slug>.html",
  "section": "Macro-categoria / Categoria / Sottocategoria"
}
```

---

## 4. Validazione prima di restituire i file (`tools/predeploy.py`)

Il repository reale esegue `python3 tools/predeploy.py` prima di ogni
pubblicazione: controlla, tra l'altro, che non ci siano riferimenti/link
rotti, che ogni `<img>` abbia `alt`, che `.art-body` abbia
`data-length-policy="3000-7000"` e sia davvero in quel range di caratteri
senza frasi/paragrafi duplicati, che il blocco "Potrebbe interessarti" non
sia autoreferenziale, che la LIVE ticker abbia esattamente 10 link e
l'auto-rail esattamente 5, che non ci siano immagini duplicate tra
articoli, e altri controlli descritti nel file stesso (incluso qui come
riferimento leggibile — chi reintegra i file lo eseguirà davvero nel
repository completo). Scrivi/valida mentalmente contro queste stesse
regole prima di restituire i file, così il primo tentativo passa il gate.

---

## 5. Come restituire i file aggiornati

1. Mantieni **esattamente gli stessi percorsi relativi** presenti in questo
   workspace (es. `notizie/<slug>.html`, `assets/images/editorial-auto/...`,
   `index.html` alla radice) così chi reintegra può sovrascrivere/aggiungere
   file al posto giusto nel repository reale senza doverli rimappare.
2. Restituisci **solo i file effettivamente cambiati o nuovi** (nuovo
   articolo HTML, nuove immagini WebP, e le versioni aggiornate di tutti i
   file elencati nella tabella del punto 3 che hai effettivamente
   modificato) — non serve restituire file invariati.
3. Per il numero di versione (`site_version`/`?v=SITE_VERSION` negli script,
   `currentVersion`) usa il valore attuale + 1 rispetto a quanto trovi in
   `CURIOMONDO-RELEASE-STATE.json`/`curiomondo-site-manifest.json` inclusi
   qui, e riportalo in modo coerente in **tutti** i punti che lo richiedono
   (head dell'articolo, script `curiomondo-article-v210.js?v=`, manifest,
   release state).
4. Se non riesci a rispettare una regola obbligatoria (lunghezza, fonti,
   unicità immagine, ecc.) per un articolo specifico, **non includerlo**
   e segnalalo esplicitamente invece di pubblicare un pezzo non conforme.

---

## Cosa NON è incluso, e perché

Questo workspace **non** contiene: `.git`, `node_modules`, cache/build,
l'intero archivio storico di `notizie/*.html` (oltre 250 file — ne è
incluso solo uno come riferimento/template), l'intera cartella
`assets/images/` (centinaia di MB di immagini storiche — solo 2 set
d'esempio da 3 file WebP ciascuno), i fogli CSS/JS versionati (non vanno
mai toccati per pubblicare un articolo), `biblioteca/`, `domanda-del-giorno/`,
`contenuti/` (contenuti/pipeline separati, fuori scope), i vari
`RELEASE-NOTES-*.md`/`QA-REPORT-*.md` storici (changelog, non servono per
pubblicare) e gli script di build una-tantum in `tools/build_v*.py`
(superati, il gate valido è solo `tools/predeploy.py`). Se in futuro serve
anche gestire Biblioteca/Domanda del giorno, va creato un workspace
analogo dedicato con le sue regole (`automation/prompts/library-contract.txt`
e la sezione relativa del Protocollo Maestro).
