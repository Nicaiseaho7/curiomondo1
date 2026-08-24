# CurioMondo Automation — setup

## Installato in v166
- LIVE dinamica: Netlify Scheduled Function ogni 10 minuti + Netlify Blobs. Nessun full deploy per i refresh LIVE.
- Endpoint pubblico LIVE: `/.netlify/functions/live-feed`.
- Homepage: aggiorna il ticker ogni 60 secondi leggendo l’endpoint.
- Auto Editor: GitHub Actions ogni 2 ore (`:17` UTC).
- Biblioteca: GitHub Actions una volta al giorno (`05:37` UTC).
- Fail-closed: pubblicazione automatica disattivata finché non viene esplicitamente abilitata.

## Prima attivazione
1. Pubblicare questa versione sul repository GitHub collegato a Netlify.
2. Verificare in Netlify > Functions che `live-refresh` mostri il badge Scheduled.
3. Premere Run now una volta su `live-refresh`; poi aprire `/.netlify/functions/live-feed`.
4. Controllare la homepage: il ticker deve continuare a mostrare 10 elementi e le voci senza articolo non devono essere cliccabili.
5. In GitHub > Actions verificare che esistano `CurioMondo Auto Editor` e `CurioMondo Biblioteca Daily`.

## Sicurezza
`CURIOMONDO_AUTO_PUBLISH` deve restare `false` finché il renderer degli articoli/guide non supera un test preview controllato.
Non inserire mai chiavi API nel codice o nei file del repository. Usare GitHub Secrets / Netlify environment variables.

## Variante iPhone / Working Copy

Questa patch non richiede la cartella nascosta `.github`.
Gli scheduler sono configurati direttamente in `netlify.toml`:
- `live-refresh`: ogni 10 minuti;
- `auto-editor`: ogni 2 ore;
- `library-daily`: una volta al giorno.

Le funzioni `auto-editor` e `library-daily` restano in SAFE MODE finché non vengono configurati i segreti/API e superato il test di pubblicazione controllato.
