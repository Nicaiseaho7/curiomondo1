# CurioMondo Automation — setup

## Configurazione corrente dalla v169
- Deploy Netlify esclusivamente statico: nessun comando di build, nessuna Function e nessuna dipendenza Node da compilare.
- Netlify pubblica direttamente la cartella già verificata.
- LIVE statico: il ticker contiene 10 elementi già inclusi nella homepage e viene aggiornato solo nelle versioni verificate del sito.
- Auto Editor: GitHub Actions ogni 2 ore (`:17` UTC).
- Biblioteca: GitHub Actions una volta al giorno (`05:37` UTC).
- Fail-closed: pubblicazione automatica disattivata finché non viene esplicitamente abilitata.

## Prima attivazione
1. Eseguire il deploy della cartella o dello ZIP già pronto, senza selezionare alcun comando di build.
2. Controllare la homepage: il ticker deve continuare a mostrare 10 elementi.
3. In GitHub > Actions verificare che esistano `CurioMondo Auto Editor` e `CurioMondo Biblioteca Daily`.

## Sicurezza
`CURIOMONDO_AUTO_PUBLISH` deve restare `false` finché il renderer degli articoli/guide non supera un test preview controllato.
Non inserire mai chiavi API nel codice o nei file del repository. Usare GitHub Secrets / Netlify environment variables.


## Contratto editoriale quotidiano v175
Ogni ciclo giornaliero completo deve produrre insieme: 1 Domanda del giorno, 1 eBook collegato da 15.000–30.000 caratteri e 2 guide Biblioteca da 3.000–15.000 caratteri ciascuna. La risposta breve alla domanda resta tra 1.000 e 3.000 caratteri. Le guide devono essere assegnate alla categoria corretta e la Biblioteca e gli eBook usano il tema premium bianco + blu CurioMondo; il verde non è una palette dominante.


## Contratto editoriale articoli — protocollo 4.0 (aggiornato 10 settembre 2026)
- Ogni ciclo articoli parte da fonti autorevoli e applica deduplicazione e verifica prima della pubblicazione.
- Pubblicare solo sviluppi realmente nuovi, significativi e con conseguenze concrete; aggiornamenti minori, rumor, gossip, duplicati e dichiarazioni senza sviluppo non bastano.
- Per guerre e geopolitica, una dichiarazione proveniente da una sola parte non va presentata come fatto accertato.
- **NON ESISTE PIÙ ALCUN LIMITE OBBLIGATORIO DI 3.000–7.000 CARATTERI.** La lunghezza dipende esclusivamente dal formato e dalla quantità di materia verificata, secondo `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md` v4.0. Riferimenti editoriali: flash 100–250 parole; notizia standard 300–600 parole; approfondimento 800–1.500+ parole quando la materia lo richiede. Non allungare né tagliare artificialmente un articolo per raggiungere un conteggio.
- **Zero ripetizioni:** lo stesso fatto o concetto non può comparire due volte, neppure parafrasato. Ogni paragrafo deve aggiungere informazione nuova; riepiloghi ridondanti e conclusioni che ripetono l’apertura sono vietati.
- Prima del rendering eseguire un passaggio anti-ridondanza frase-per-frase e paragrafo-per-paragrafo.
- Non spiegare parole difficili nel corpo della notizia. Quando un concetto merita utilità nel tempo, creare o collegare un approfondimento evergreen autonomo; prima verificare che non esista già. Notizia e approfondimento devono linkarsi in entrambe le direzioni.
- Ogni nuova notizia richiede una propria immagine editoriale fotorealistica, specifica e mai riutilizzata né derivata da un hero già pubblicato.
- **PROMPT IMMAGINI OBBLIGATORIO E MACHINE-READABLE:** prima di generare il visual di qualunque articolo, qualsiasi IA/renderer deve caricare e leggere integralmente `automation/prompts/image-generation-contract.txt`. Il percorso è dichiarato anche in `automation/config.json` (`articles.image_generation_prompt`) e viene caricato da `automation/run_cycle.py`. Se il file manca, il ciclo deve bloccarsi.
- **PERSONAGGI PUBBLICI E DEEPFAKE EDITORIALE:** qualsiasi IA deve inoltre leggere `AI-EDITORIAL-IMAGE-PROTOCOL.md`. Nelle notizie ordinarie sono ammessi personaggi riconoscibili in luoghi e ambientazioni pertinenti, anche con loghi coerenti. Per incidenti, morte, salute, violenza, tragedie, lutto, sofferenza o altri temi sensibili è obbligatorio il ritratto neutrale isolato e non si rappresenta il momento doloroso. Il ciclo si blocca se il protocollo manca o se il contratto del generatore non contiene entrambe le regole.
- Sotto ogni immagine IA articolo usare esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
- Ogni pubblicazione deve aggiornare SEO, canonical, NewsArticle JSON-LD, homepage/sezioni pertinenti, archivio, ricerca, collegamenti interni, feed, sitemap e Google News Sitemap quando applicabile.
- La posizione “Ultima ora” dipende dal peso editoriale, non dalla sola cronologia.
- Nessun deploy se non ci sono notizie valide; se ce ne sono più di una, possono essere pubblicate nello stesso ciclo con un solo deploy.

## Domanda del giorno — controllo data obbligatorio
- Ogni ciclo automatico deve calcolare la data corrente nel fuso `Europe/Rome` e confrontarla con `daily_state.last_question_date` in `curiomondo-site-manifest.json`.
- Se la data è cambiata, **prima di concludere il ciclo deve pubblicare automaticamente la nuova Domanda del giorno**, anche se il ciclo era stato avviato per cercare notizie.
- La domanda deve essere scelta **esclusivamente** dal PDF privato `Mille_e_piu_domande_per_pensare.pdf`, che contiene 1.125 domande numerate. Il PDF non deve essere pubblicato né copiato nel sito.
- Usare una domanda non ancora presente in `daily_state.used_question_source_numbers`; conservarne il testo invariato salvo apostrofi tipografici e registrare nel manifest il numero scelto, aggiornando `current_question_source_number`, `used_question_source_numbers`, `last_question_date` e `last_question_slug`.
- Se il PDF privato non è disponibile al ciclo, la pubblicazione della Domanda del giorno deve fermarsi in modalità fail-closed: non inventare né sostituire la domanda con una fonte diversa.
- Deve esistere una sola Domanda del giorno per ciascuna data italiana. Aggiornare nello stesso ciclo homepage/card mistero, pagina dedicata, archivio, ricerca, sitemap e gli altri output previsti dal Protocollo Maestro.

## Stato reale dell’automazione
- `automation/run_cycle.py` è ancora fail-closed: senza `CURIOMONDO_AUTO_PUBLISH=true` esegue soltanto dry-run; anche con la variabile attiva blocca la pubblicazione finché il renderer automatico non viene abilitato dopo un test preview controllato.
- Il predeploy locale resta obbligatorio e deve terminare con exit code 0 prima di qualsiasi commit/deploy.


### Coda guide Biblioteca
Leggere `automation/state/guide-topics.json`; scegliere solo da `remaining_topics`; dopo pubblicazione verificata rimuovere il titolo usato. Limiti: 3.000–15.000 caratteri.

### Regola disclosure immagini e approfondimenti
- Sotto ogni immagine IA articolo usare esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
- Gli approfondimenti evergreen si creano o collegano soltanto quando aggiungono valore durevole e non ridondante; non sono obbligatori per ogni notizia.
- Tutte le pagine editoriali pubbliche devono essere indicizzabili.
- Biblioteca/eBook: niente page-flip o swipe; navigazione soltanto con grandi controlli blu `Indietro` e `Avanti` sotto la pagina.
