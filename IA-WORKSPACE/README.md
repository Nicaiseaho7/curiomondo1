# IA-WORKSPACE — CurioMondo

Copia di lavoro quasi completa del sito, per **creare nuovi articoli** e per
**modifiche più profonde** (homepage, categorie, Biblioteca, Domanda del
giorno, Approfondimenti, pagine statiche, stile, script) senza avere bisogno
dell'intero repository Git (niente `.git`, niente cronologia commit, niente
strumenti di build una-tantum superati).

**Ogni percorso in questa cartella corrisponde 1:1 al percorso reale nel
repository GitHub**, a partire dalla radice del sito. Esempio:
`IA-WORKSPACE/notizie/index.html` → nel repo è `notizie/index.html`.
Quando restituisci i file aggiornati, **mantieni esattamente questi stessi
percorsi/nomi file**: chi li reintegra deve solo sovrascrivere/aggiungere
file allo stesso posto, senza indovinare nulla.

Contiene **tutto l'archivio notizie**, **tutta la Biblioteca**, **tutta la
Domanda del giorno**, **tutte le immagini editoriali già pubblicate**
(`assets/images/`) e **tutti** i CSS/JS del sito — non solo gli ultimi
articoli. Questo è intenzionale: avere l'intera libreria immagini/articoli
visibile evita di generare per errore un nome file già usato o un'immagine
doppione di una già pubblicata (vedi §2).

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
9. Per modifiche a Biblioteca/eBook: anche `automation/prompts/library-contract.txt`
   (ora incluso) e la sezione Biblioteca del Protocollo Maestro.

Se una di queste regole non può essere rispettata per un articolo, **non
pubblicare quell'articolo** (meglio niente che un pezzo non conforme).

---

## 1. Dove va salvato un nuovo articolo

- File: **`notizie/<slug-notizia>.html`** (un file HTML per articolo, slug
  minuscolo con trattini, spesso con la data in fondo). Ci sono oltre 200
  articoli reali già in `notizie/` da usare come riferimento diretto per
  qualunque taglio editoriale (geopolitica, economia, cronaca, sport…):
  riusa la struttura `<head>`, il markup del corpo, della figure/immagine,
  del box fonti e del blocco "Potrebbe interessarti anche" copiandone la
  forma esatta e cambiando solo i contenuti.
- Asset CSS/JS richiamati in `<head>`/fondo pagina di un articolo (**non
  modificarli per pubblicare un articolo normale**, esistono già):
  `assets/css/site-base-v210.css`, `assets/css/curiomondo-article-v211.css?v=SITE_VERSION`,
  `assets/css/editorial-trust-v263.css` (aggiunto in v263, obbligatorio su ogni
  articolo — vedi sotto), `assets/js/site-common-v210.js`,
  `assets/js/curiomondo-article-v210.js?v=SITE_VERSION`
  (il numero dopo `?v=` è l'attuale `site_version`, vedi §5 sotto).
- **Firma redazionale e link di trasparenza (introdotti in v263, obbligatori
  su ogni nuovo articolo)**: subito prima del blocco `.actions`, un paragrafo
  `<p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p>`.
  Nel `<footer class="site-footer">`, dopo il pulsante "Gestisci cookie",
  aggiungere: `<a href="/pagine/redazione.html">Redazione</a> · <a href="/pagine/metodo-editoriale.html">Metodo editoriale</a> · <a href="/pagine/correzioni.html">Correzioni</a> · <a href="/pagine/intelligenza-artificiale.html">Uso dell'IA</a> · <a href="/pagine/termini.html">Termini</a>`.
  Nel JSON-LD `NewsArticle`, `author` deve avere anche
  `"url":"https://curiomondo.it/pagine/redazione.html"`. Usa un articolo
  recente in `notizie/` come riferimento esatto per la sintassi.
- **Articoli storici sotto lo standard di qualità (regola v263)**: se rivedi
  o correggi un articolo esistente che risulta sotto i 2.000 caratteri o con
  meno di 2 fonti collegate, e non lo riporti sopra quella soglia, deve avere
  `<meta name="robots" content="noindex,follow">` e **non** caricare lo
  script AdSense (`pagead2.googlesyndication.com`); va inoltre rimosso da
  `sitemap.xml`, `news-sitemap.xml`, `feed.xml` e da
  `assets/data/home-feed-v210.json`/`search-index-v210.json`. Se invece lo
  porti sopra soglia, fai l'opposto: `index,follow`, pubblicità reintegrata,
  e rimesso in tutti quei file. Non creare nuovi articoli sotto queste soglie.
- Se l'articolo merita anche un **approfondimento evergreen** (guida
  autonoma, senza data, tipo "come funziona…"/"perché…"): va anch'esso
  fisicamente in `notizie/<slug-guida>.html` (stessa struttura, senza
  `data-length-policy`), **non** in `approfondimenti/`, che contiene solo
  l'indice. Registralo anche in `approfondimenti/index.html`.
- **Prima di scrivere un nuovo articolo**, controlla che la stessa storia
  non sia già raccontata in `notizie/index.html` o in
  `assets/data/search-index-v210.json`, per evitare duplicati.

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

- Cartella corretta per le nuove immagini: **`assets/images/editorial-auto/`**.
- Le altre sottocartelle `assets/images/editorial-vNNN/` (v210, v213, v228…)
  sono **archivio storico** di build passate: sono incluse solo per
  completezza/verifica di unicità, ma **non vanno usate** per nuove immagini.
- Per ogni articolo servono **3 file WebP**, stesso nome base, tre larghezze:
  ```
  assets/images/editorial-auto/<filename_base>-480.webp
  assets/images/editorial-auto/<filename_base>-800.webp
  assets/images/editorial-auto/<filename_base>-1200.webp
  ```
- **Il nome file deve essere sempre nuovo, anche quando si sostituisce
  l'immagine di un articolo già pubblicato**: `/assets/images/*` ha
  `Cache-Control: public, max-age=31536000, immutable` (vedi `_headers`,
  incluso qui). Riusare un nome file esistente con un contenuto diverso
  significa che browser e CDN continueranno a servire i byte vecchi per
  un anno, deploy o non deploy. Se aggiorni un'immagine già pubblicata,
  cambia il suffisso di versione nel nome e aggiorna ogni riferimento.
- **Prima di generare un'immagine, controlla che il nome file scelto non
  esista già** in `assets/images/editorial-auto/` (ora incluso per intero)
  e che il registro `assets/data/editorial-images-v210.json` non contenga
  già un'immagine per quell'URL articolo: se l'articolo esiste già ed ha
  già un'immagine reale, non generarne una nuova senza che sia stato
  esplicitamente richiesto.
- Specifiche immagine (da `image-generation-contract.txt` e
  `AI-EDITORIAL-IMAGE-PROTOCOL.md`, lettura obbligatoria integrale prima di
  generare qualunque immagine):
  - Ultra-realistica, fotografica, mai flat/vector/illustrazione/infografica.
  - Scena **completamente nuova** per ogni articolo: mai riuso, crop,
    resize, filtro o rinomina di un'immagine già pubblicata.
  - **Mai testo, watermark o didascalie dentro i pixel dell'immagine.**
  - Persone pubbliche: consentite in scena solo per notizie "ordinarie";
    per incidenti/morte/malattia/violenza/lutto e altri temi sensibili è
    **obbligatorio** un ritratto neutrale isolato.
- Nell'HTML dell'articolo, subito sotto l'immagine, la `<figcaption>` deve
  contenere **esattamente**:
  `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
- **Se un'immagine non è ancora pronta**: pubblica comunque il testo
  omettendo del tutto il blocco `<figure>`, usa
  `https://curiomondo.it/curiomondo-logo-512.png` come `og:image`/JSON-LD
  `image`, e `curiomondo-logo-512.png?pending=<slug>` come immagine card.
  Registra l'articolo in `automation/state/pending-images.json` (schema in
  `automation/prompts/three-hourly-cycle-instructions.md` §4bis).

---

## 3. Tutti i file da modificare per far comparire il nuovo articolo nel sito

| # | File | Cosa fare |
|---|------|-----------|
| 1 | `notizie/<slug>.html` | Nuovo file, uno per articolo (vedi §1). |
| 2 | `notizie/index.html` | Nuova `<li>` in cima all'archivio; aggiorna il contatore "N articoli, ordinati per data.". |
| 3 | `index.html` → `class="ticker-track"` | Due copie identiche (nav accessibile + div `aria-hidden`): prepend, restano sempre **esattamente 10** link. |
| 4 | `index.html` → `class="auto-rail"` | Prepend, restano **esattamente 5**. |
| 5 | `index.html` → `id="cards"` | Prepend in cima alla griglia "Tutte le notizie". |
| 6 | `index.html` → `class="featured"` (unico) | Se è l'articolo più rilevante del ciclo, sostituiscilo (l'ex featured scende in cima all'auto-rail). |
| 7 | `index.html` → `class="cm-home-deep-links"` | Solo se creato un nuovo approfondimento: prepend (restano 3). |
| 8 | `index.html` → `class="cm-qday"` | Solo se cambia la Domanda del giorno: aggiorna data/href/titolo, mantenendo il markup esatto (incluso `cm-qday-hint`). |
| 9 | `assets/data/home-feed-v210.json` | Prepend voce in `items`, bump `version`. |
| 10 | `assets/data/search-index-v210.json` | Prepend voce in `items`, bump `version`. |
| 11 | `feed.xml` | Prepend `<item>` RSS. |
| 12 | `sitemap.xml` | Nuovo `<url>` (`changefreq daily`, `priority 0.9`). |
| 13 | `news-sitemap.xml` | Nuovo `<url>`/`<news:news>`; **potare le voci più vecchie di 48 ore**. |
| 14 | `_redirects` | Nuova riga, stesso pattern delle esistenti. |
| 15 | `assets/data/editorial-images-v210.json` | Nuova voce con lo stesso schema delle esistenti. |
| 16 | `curiomondo-site-manifest.json` + `CURIOMONDO-RELEASE-STATE.json` + `RELEASE-STATE.json` | Bump coerente di versione/conteggio articoli/data. |
| 17 | `automation/state/pending-images.json` | Solo se pubblichi senza immagine reale. |
| 18 | `approfondimenti/index.html` | Solo se creato un nuovo approfondimento evergreen. |
| 19 | `domanda-del-giorno/<slug>/index.html` + `domanda-del-giorno/index.html` | Solo se pubblichi una nuova Domanda del giorno (vedi Protocollo Maestro per le regole di lunghezza/formato). |
| 20 | `biblioteca/<categoria>/domande-per-conoscersi/<slug>/index.html` | Solo se la Domanda del giorno ha un eBook collegato (8-14 pagine, 15.000-30.000 caratteri nello stage del libro). |

**Non serve toccare** `assets/css/*` o `assets/js/*` per un articolo o una
Domanda del giorno normali: si riusano sempre gli stessi file. Sono inclusi
per intero solo perché una modifica strutturale più ampia potrebbe
richiederlo esplicitamente — in quel caso, cambia il file CSS/JS reale
riferito da più pagine, non crearne uno nuovo senza necessità.

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
pubblicazione (incluso qui, insieme ai vecchi `tools/build_v*.py` — questi
ultimi sono script one-shot di release passate, **non fanno parte del
flusso corrente**, solo `predeploy.py` è il gate valido). Controlla, tra
l'altro: link interni rotti, `alt` mancanti, lunghezza/non-ripetizione del
corpo articolo, didascalia IA esatta, classificazione immagini con persone
pubbliche, numero esatto di voci in LIVE (10) e "Altre notizie" (5),
immagini duplicate tra articoli, struttura della Domanda del giorno e
dell'eBook del giorno corrente. Scrivi/valida mentalmente contro queste
stesse regole prima di restituire i file.

---

## 5. Come restituire i file aggiornati

1. Mantieni **esattamente gli stessi percorsi relativi** presenti in questo
   workspace.
2. Restituisci **solo i file effettivamente cambiati o nuovi** — non serve
   restituire l'intero workspace invariato.
3. Per il numero di versione (`site_version`/`?v=SITE_VERSION`,
   `currentVersion`) usa il valore attuale + 1 rispetto a quanto trovi in
   `CURIOMONDO-RELEASE-STATE.json`/`curiomondo-site-manifest.json`, e
   riportalo in modo coerente ovunque richiesto.
4. Se non riesci a rispettare una regola obbligatoria per un articolo
   specifico, **non includerlo** e segnalalo esplicitamente.
5. **Non rigenerare né rinominare immagini di articoli già pubblicati** a
   meno che non sia stato esplicitamente richiesto: questo workspace
   include l'intera libreria immagini proprio per evitare doppioni
   involontari.

---

## Cosa NON è incluso, e perché

Questo workspace **non** contiene: `.git` (nessuna cronologia commit),
`contenuti/` (JSON grezzi legacy, `Disallow`'d in `robots.txt`, non letti
da nessuna pagina viva), i vari `RELEASE-NOTES-*.md`/`QA-REPORT-*.md`/
`AGGIORNAMENTO-*.txt` storici alla radice (changelog, non servono per
pubblicare), `netlify.toml` e `package.json` (**non esistono nel
repository reale**: il sito è un output statico puro, senza build step —
non vanno creati). Tutto il resto — articoli, immagini, Biblioteca,
Domanda del giorno, CSS, JS, automazione, strumenti — è incluso per
intero.
