# CurioMondo — checklist qualità e idoneità AdSense

Questa checklist non garantisce l'approvazione AdSense: la decisione finale spetta a Google. Serve a evitare i problemi tecnici/editoriali più comuni che possono rendere il sito non idoneo o percepito come di scarso valore.

## Contenuti indicizzabili

- Ogni nuovo articolo di notizie indicizzabile deve avere 3.000–7.000 caratteri di testo visibile nel corpo editoriale.
- Ogni paragrafo deve aggiungere informazione, contesto, spiegazione o conseguenza nuova; niente riempitivo o ripetizioni.
- Almeno 2 fonti attendibili e collegate per ogni articolo indicizzabile; preferire fonti primarie quando disponibili.
- Vietato copiare o parafrasare meccanicamente articoli di altre testate. CurioMondo deve aggiungere contesto, spiegazione e valore autonomo.
- Le pagine storiche troppo sottili o con fonti insufficienti vanno migliorate; se restano sotto standard, usare `noindex,follow`, rimuoverle da sitemap/feed/home/search e non caricare AdSense.
- Evitare pagine generate in massa con schemi quasi identici e scarso valore informativo.

## Trasparenza e fiducia

Devono restare pubbliche, raggiungibili e coerenti:

- `/pagine/chi-siamo.html`
- `/pagine/redazione.html`
- `/pagine/metodo-editoriale.html`
- `/pagine/intelligenza-artificiale.html`
- `/pagine/correzioni.html`
- `/pagine/contatti.html`
- `/pagine/privacy.html`
- `/pagine/cookie.html`
- `/pagine/termini.html`

Ogni articolo recente deve mostrare una firma/redazione riconoscibile, fonti, data e link al metodo editoriale.

## AdSense

- `ads.txt` deve contenere esattamente il record autorizzato del publisher CurioMondo.
- Non caricare o mostrare annunci su pagine `noindex` sotto standard.
- Non creare pagine vuote o quasi vuote solo per ospitare annunci.
- La quantità di pubblicità non deve sovrastare il contenuto editoriale.

## Consenso e privacy

Per traffico SEE, Regno Unito e Svizzera, la configurazione finale deve utilizzare una CMP certificata da Google e integrata con IAB TCF quando richiesta per gli annunci personalizzati. Il semplice banner cookie personalizzato del sito non va considerato automaticamente equivalente a una CMP certificata.

## Prima di una nuova richiesta AdSense

1. Eseguire `python3 tools/predeploy.py` e risolvere ogni errore.
2. Controllare manualmente un campione di articoli vecchi e recenti.
3. Verificare che le pagine di trasparenza siano raggiungibili e coerenti.
4. Verificare `ads.txt`, privacy/cookie e configurazione CMP.
5. Evitare di ripresentare la richiesta immediatamente dopo modifiche superficiali: il sito deve mostrare un miglioramento sostanziale e stabile della qualità editoriale.
