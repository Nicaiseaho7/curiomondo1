# CurioMondo v210 — rapporto di verifica

Data: 29 agosto 2026

## Esito statico

- 283 pagine HTML analizzate.
- 179 articoli conservati e normalizzati.
- 179 corpi editoriali presenti; il testo degli articoli è rimasto invariato durante la migrazione.
- 145 articoli con immagine editoriale IA e didascalia di trasparenza; 34 articoli restano intenzionalmente testuali, senza fallback generici.
- 58 nuove scene IA ultrarealistiche e pertinenti, esportate in 174 WebP responsive (480, 800 e 1200 px).
- Nessun riferimento immagine duplicato fra gli articoli.
- Nessun riferimento immagine duplicato nella homepage.
- Nessun file immagine vuoto.
- Nessun collegamento o asset interno mancante.
- Nessun ID HTML duplicato.
- JavaScript v210 sintatticamente valido.
- Script pubblicitari inattivi prima del consenso marketing.

## Prestazioni

La homepage usa 2 fogli di stile v210 e 2 script differiti v210, per circa 64 KB complessivi di HTML, CSS e JavaScript non compressi. Le immagini hanno varianti responsive, dimensioni intrinseche e caricamento differito; il visual principale usa priorità alta. I vecchi runtime home sovrapposti non sono più caricati.

Il punteggio PageSpeed definitivo deve essere misurato sul dominio dopo il deploy, perché dipende anche da CDN, cache, latenza, consenso e configurazione Netlify. Il pacchetto è stato ottimizzato per l'obiettivo 90–100, ma il rapporto non inventa un punteggio non misurato.

## Navigazione agentica

Sono presenti link reali, ricerca semantica, dialog nativi, controlli con etichette, dati strutturati `NewsArticle`, archivio completo, indice JSON e `llms.txt`. La verifica finale 2/2 va eseguita sulla versione pubblicata.

## Verifica ripetibile

Eseguire dalla radice del sito:

```bash
python3 tools/predeploy.py --root .
```

Esito atteso: `errors: []`.
