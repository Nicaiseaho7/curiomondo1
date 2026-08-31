# CurioMondo v238 — 29 agosto 2026

## Lettura audio articoli
- Nuovo profilo “voce naturale” per tutti gli articoli che usano il controller comune.
- Selezione automatica della migliore voce italiana disponibile, con priorità a voci premium, neural, natural o enhanced e preferenza per timbri maschili/profondi quando riconoscibili dal browser.
- Ritmo più umano: segmentazione per frase e punteggiatura, velocità 0,92, pitch 0,78.
- Pulsante aggiornato in “Ascolta con voce naturale”.
- Supporto già predisposto per file audio neurali premium per singolo articolo tramite `data-audio-src` o meta `cm:article-audio`; in quel caso il file audio viene usato al posto della sintesi vocale del browser.
- Nessuna chiave API viene esposta nel frontend e non sono state introdotte funzioni Netlify o build server-side.

## Baseline
- Basata su v237 del 29 agosto 2026.
