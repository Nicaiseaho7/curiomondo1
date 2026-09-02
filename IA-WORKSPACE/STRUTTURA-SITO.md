# STRUTTURA-SITO — CurioMondo

Riferimento tecnico sulla struttura reale del sito, allineato allo stato attuale di
`main` al momento di questo export. Ogni percorso qui sotto è identico al percorso
reale nel repository — nessuna reinterpretazione.

Nota sui file assenti dal repository reale (quindi non presenti neanche qui, come
richiesto): **non esistono** `netlify.toml`, `package.json`, `package-lock.json`,
`yarn.lock` né una cartella `scripts/` alla radice. Il sito è un output statico
puro, senza build step: nessun comando di installazione o compilazione è previsto
o necessario.

Questa versione del workspace è **completa**: include l'intero `notizie/`,
`biblioteca/`, `domanda-del-giorno/`, `assets/images/` (tutta la libreria
storica, non solo gli ultimi articoli), `assets/css/`, `assets/js/`,
`automation/`, `tools/`, `pagine/`, `ads.txt` e `_headers`. Restano esclusi
solo `.git`, `contenuti/` (JSON legacy non letti da nessuna pagina viva) e i
changelog storici alla radice (`RELEASE-NOTES-*.md`, `QA-REPORT-*.md`, ecc.).

---

## 1. Dove vengono salvati i nuovi articoli

- Notizie: **`notizie/<slug-notizia>.html`** — un file HTML per articolo. Non
  esiste un template a parte: si riusa la struttura di un articolo reale già
  pubblicato — l'intero archivio (oltre 200 file) è incluso in `notizie/`
  come riferimento.
- Approfondimenti evergreen (guide "come funziona…"/"perché…" collegate a una
  notizia): vivono anch'essi in **`notizie/<slug-approfondimento>.html`**, mai in
  `approfondimenti/`, che è solo l'indice curato che li elenca
  (`approfondimenti/index.html`).
- Domanda del giorno: **`domanda-del-giorno/<slug>/index.html`**, con
  `domanda-del-giorno/index.html` come archivio. eBook collegato (quando
  presente): `biblioteca/<categoria>/domande-per-conoscersi/<slug>/index.html`.
  Regole di lunghezza/formato nel Protocollo Maestro e in `library-contract.txt`.
- Non esiste una cartella `templates/`: il riferimento è sempre un articolo reale
  esistente più il markup esatto documentato in
  `automation/prompts/three-hourly-cycle-instructions.md` (§5).

## 2. Dove vengono salvate le immagini

- Cartella corrente per le nuove immagini: **`assets/images/editorial-auto/`**.
- Le sottocartelle `assets/images/editorial-vNNN/` sono archivio storico di
  build passate — incluse per intero in questo workspace solo per riferimento
  e controllo di unicità, **non vanno usate** per nuove immagini.
- Tre file WebP per immagine, stesso nome base, tre larghezze:
  `<filename_base>-480.webp`, `-800.webp`, `-1200.webp`.
- **Il nome file deve essere nuovo per ogni nuova immagine.** `/assets/images/*`
  ha `Cache-Control: public, max-age=31536000, immutable` (vedi `_headers`,
  incluso in questo workspace): se un'immagine viene rigenerata per un
  articolo già pubblicato riusando lo stesso nome file, browser e CDN continuano
  a servire indefinitamente i byte vecchi, anche dopo il deploy. Cambiare sempre
  il suffisso di versione nel nome (es. `-ai-v261` → `-ai-v262`) e aggiornare ogni
  riferimento (vedi punto 3).
- Prima di generare un'immagine per un articolo esistente, controllare in
  `assets/data/editorial-images-v210.json` se ha già una voce reale: se sì,
  non è "mancante", e va rigenerata solo su richiesta esplicita.

## 3. File da aggiornare quando si pubblica un articolo

Per ogni nuovo articolo (o sostituzione immagine di un articolo esistente),
aggiornare in modo coerente:

| File | Perché |
|---|---|
| `notizie/<slug>.html` | Il nuovo articolo. |
| `notizie/index.html` | Nuova `<li>` in cima all'archivio; aggiornare il contatore "N articoli...". |
| `index.html` | Ticker LIVE (`class="ticker-track"`, due copie identiche, sempre 10 link), `class="auto-rail"` (sempre 5), `id="cards"` (prepend), `class="featured"` (se è l'articolo più rilevante del ciclo), `class="cm-qday"` (solo se cambia la Domanda del giorno). |
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
| `domanda-del-giorno/index.html` | Solo se pubblicata una nuova Domanda del giorno. |

Non serve toccare `assets/css/*` o `assets/js/*` per pubblicare un articolo o
una Domanda del giorno normali: si riusano sempre gli stessi fogli
stile/script già esistenti (vedi punto 4). Sono inclusi per intero solo per
eventuali modifiche strutturali più ampie, esplicitamente richieste.

## 4. Come vengono aggiornati homepage, categorie, ricerca, sitemap e feed

- **Homepage** (`index.html`): il contenuto (ticker LIVE, blocco "featured",
  rail "Altre notizie", griglia `#cards`, mystery card "Domanda del giorno")
  è **HTML scritto direttamente nella pagina**, non generato da JSON a
  runtime. Si aggiorna con un prepend manuale (vedi tabella sopra).
  `assets/js/home-v210.js` interviene solo per il "carica altro" oltre le
  prime card e per i widget (quiz, curiosità), leggendo
  `assets/data/home-feed-v210.json`, `quiz-curiomondo.json`,
  `world-facts-v210.json`.
- **Categorie**: sulla homepage **non esistono pagine fisiche per categoria** —
  sono filtri lato client sulla query string (`/?categoria=nome`), letti da
  `assets/js/home-v210.js` (`params.get('categoria')`) che filtra le card già
  presenti in `home-feed-v210.json`. La Biblioteca invece **ha pagine categoria
  fisiche** (`biblioteca/<categoria>/index.html`, 6 cartelle), incluse per
  intero: sono contenuti diversi dalle notizie, con propria struttura e i
  propri capitoli (`biblioteca/<categoria>/<guida>/index.html`).
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
  in LIVE (10) e "Altre notizie" (5), immagini duplicate tra articoli, struttura
  della Domanda del giorno/eBook del giorno corrente, e altri controlli
  descritti nel file stesso. Gli altri script in `tools/build_v*.py` sono
  strumenti one-shot di release passate, non fanno parte del flusso corrente.
- **Nessun altro comando è necessario**: non c'è build (`npm run build` e simili
  non esistono in questo progetto), non c'è installazione di dipendenze Node
  (il sito non ha `package.json`). L'unica dipendenza Python richiesta da
  `predeploy.py` è `lxml`, installabile con
  `pip install -r automation/requirements.txt` (incluso in questo workspace).
- **Dopo il commit**: il deploy in produzione (Netlify) è collegato
  automaticamente al branch `main` del repository GitHub — un push su `main`
  avvia da solo la pubblicazione, senza upload manuale.
