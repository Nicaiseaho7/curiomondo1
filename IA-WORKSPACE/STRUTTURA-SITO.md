# STRUTTURA-SITO — CurioMondo

Riferimento tecnico sulla struttura reale del sito, allineato allo stato attuale di
`main` al momento di questo export. Ogni percorso qui sotto è identico al percorso
reale nel repository — nessuna reinterpretazione.

Nota sui file assenti dal repository reale (quindi non presenti neanche qui, come
richiesto): **non esistono** `netlify.toml`, `package.json`, `package-lock.json`,
`yarn.lock` né una cartella `scripts/` alla radice. Il sito è un output statico
puro, senza build step: nessun comando di installazione o compilazione è previsto
o necessario.

---

## 1. Dove vengono salvati i nuovi articoli

- Notizie: **`notizie/<slug-notizia>.html`** — un file HTML per articolo. Non
  esiste un template a parte: si riusa la struttura di un articolo reale già
  pubblicato (nel workspace: i 10 più recenti, in `notizie/`).
- Approfondimenti evergreen (guide "come funziona…"/"perché…" collegate a una
  notizia): vivono anch'essi in **`notizie/<slug-approfondimento>.html`**, mai in
  `approfondimenti/`, che è solo l'indice curato che li elenca
  (`approfondimenti/index.html`).
- Non esiste una cartella `templates/`: il riferimento è sempre un articolo reale
  esistente più il markup esatto documentato in
  `automation/prompts/three-hourly-cycle-instructions.md` (§5).

## 2. Dove vengono salvate le immagini

- Cartella unica e corrente: **`assets/images/editorial-auto/`**.
- Tre file WebP per immagine, stesso nome base, tre larghezze:
  `<filename_base>-480.webp`, `-800.webp`, `-1200.webp`.
- **Il nome file deve essere nuovo per ogni nuova immagine.** `/assets/images/*`
  ha `Cache-Control: public, max-age=31536000, immutable` (vedi `_headers` nel
  repository completo, non incluso qui): se un'immagine viene rigenerata per un
  articolo già pubblicato riusando lo stesso nome file, browser e CDN continuano
  a servire indefinitamente i byte vecchi, anche dopo il deploy. Cambiare sempre
  il suffisso di versione nel nome (es. `-ai-v260` → `-ai-v261`) e aggiornare ogni
  riferimento (vedi punto 3).

## 3. File da aggiornare quando si pubblica un articolo

Per ogni nuovo articolo (o sostituzione immagine di un articolo esistente),
aggiornare in modo coerente:

| File | Perché |
|---|---|
| `notizie/<slug>.html` | Il nuovo articolo. |
| `notizie/index.html` | Nuova `<li>` in cima all'archivio; aggiornare il contatore "N articoli...". |
| `index.html` | Ticker LIVE (`class="ticker-track"`, due copie identiche, sempre 10 link), `class="auto-rail"` (sempre 5), `id="cards"` (prepend), `class="featured"` (se è l'articolo più rilevante del ciclo). |
| `assets/data/home-feed-v210.json` | Prepend voce in `items` (schema con `image`/`srcset`), bump `version`. |
| `assets/data/search-index-v210.json` | Prepend voce in `items` (schema più semplice), bump `version`. |
| `assets/data/editorial-images-v210.json` | Registro immagini: nuova voce con `article`, `key`, `variants` (`src`/`sha256`/`bytes` per ogni larghezza). |
| `feed.xml` | Prepend `<item>` RSS. |
| `sitemap.xml` | Nuovo `<url>` (`changefreq daily`, `priority 0.9`). |
| `news-sitemap.xml` | Nuovo `<url>`/`<news:news>`; **potare le voci più vecchie di 48 ore** (finestra rolling richiesta da Google News Sitemap). |
| `_redirects` | Nuova riga alias extensionless → `.html` (stesso pattern delle righe esistenti). |
| `curiomondo-site-manifest.json`, `RELEASE-STATE.json`, `CURIOMONDO-RELEASE-STATE.json` | Bump coerente di versione/conteggio articoli/data ultimo rilascio. |
| `automation/state/pending-images.json` | Solo se l'articolo viene pubblicato senza immagine reale pronta (vedi §4bis del manuale ciclo). |
| `approfondimenti/index.html` | Solo se creato un nuovo approfondimento evergreen. |

Non serve mai toccare `assets/css/*` o `assets/js/*` per pubblicare un articolo:
si riusano sempre gli stessi fogli stile/script già esistenti (vedi punto 4).

## 4. Come vengono aggiornati homepage, categorie, ricerca, sitemap e feed

- **Homepage** (`index.html`): il contenuto (ticker LIVE, blocco "featured",
  rail "Altre notizie", griglia `#cards`) è **HTML scritto direttamente nella
  pagina**, non generato da JSON a runtime. Si aggiorna con un prepend manuale
  (vedi tabella sopra). `assets/js/home-v210.js` interviene solo per il
  "carica altro" oltre le prime card e per i widget (quiz, curiosità), leggendo
  `assets/data/home-feed-v210.json`.
- **Categorie**: sulla homepage **non esistono pagine fisiche per categoria** —
  sono filtri lato client sulla query string (`/?categoria=nome`), letti da
  `assets/js/home-v210.js` (`params.get('categoria')`) che filtra le card già
  presenti in `home-feed-v210.json`. La Biblioteca invece **ha pagine categoria
  fisiche** (`biblioteca/<categoria>/index.html`, 6 cartelle), incluse in questo
  workspace: sono contenuti diversi dalle notizie, con propria struttura.
- **Ricerca**: interamente client-side. `assets/js/home-v210.js` scarica
  `assets/data/search-index-v210.json` (schema minimo: `title`, `excerpt`, `url`,
  `section`) e filtra in JavaScript nel browser; nessun backend di ricerca.
- **Sitemap**: `sitemap.xml` e `news-sitemap.xml` **non sono generati
  automaticamente da uno script** nel repository — vengono editati a mano (o da
  chi pubblica) aggiungendo/rimuovendo i blocchi `<url>`. `news-sitemap.xml`
  richiede la potatura delle voci oltre le 48 ore ad ogni pubblicazione, perché
  Google News Sitemap accetta solo contenuti recenti.
- **Feed**: `feed.xml` (RSS) riceve un `<item>` in testa per ogni nuovo articolo,
  con `pubDate` in formato RFC-822 e offset orario italiano (`+0200`/`+0100`).
  Non esiste un `rss.xml` separato: `feed.xml` è l'unico feed del sito.

## 5. Comandi/script eseguiti prima del commit

- **`python3 tools/predeploy.py`** — l'unico gate di validazione del sito.
  Deve terminare con **exit code 0** prima di qualunque pubblicazione: controlla
  link interni rotti, `alt` mancanti sulle immagini, lunghezza e non-ripetizione
  del corpo articolo (`data-length-policy="3000-7000"`), didascalia IA esatta,
  classificazione delle immagini con persone pubbliche, numero esatto di voci
  in LIVE (10) e "Altre notizie" (5), immagini duplicate tra articoli, e altri
  controlli descritti nel file stesso.
- **Nessun altro comando è necessario**: non c'è build (`npm run build` e simili
  non esistono in questo progetto), non c'è installazione di dipendenze Node
  (il sito non ha `package.json`). L'unica dipendenza Python richiesta da
  `predeploy.py` è `lxml`, installabile con `pip install -r automation/requirements.txt`
  (file presente nel repository completo, non necessario per la sola lettura
  dei file di questo workspace).
- **Dopo il commit**: il deploy in produzione (Netlify) è collegato
  automaticamente al branch `main` del repository GitHub — un push su `main`
  avvia da solo la pubblicazione, senza upload manuale.
