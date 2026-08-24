# CurioMondo v167 — Autopilota dinamico articoli

## Cosa cambia
- LIVE: resta ogni 10 minuti.
- Auto Editor: ogni 30 minuti.
- Gli articoli automatici sono salvati in Netlify Blobs: nessun deploy per ogni articolo.
- URL: /notizie/<slug>.html tramite fallback dinamico; i vecchi file HTML statici continuano a vincere.
- Homepage: legge /api/curiomondo/articles e integra gli articoli dinamici.
- Sitemap dinamiche: /dynamic-sitemap.xml e /dynamic-news-sitemap.xml.
- Immagini: solo Wikimedia Commons con CC0/Public Domain/CC BY/CC BY-SA; se non trova una licenza adatta, niente immagine.

## Variabili Netlify obbligatorie
OPENAI_API_KEY = chiave API OpenAI
CURIOMONDO_AUTO_PUBLISH = true
CURIOMONDO_OPENAI_MODEL = gpt-5.6-sol (opzionale)

NON mettere mai OPENAI_API_KEY in GitHub.

## Prima attivazione
1. Caricare questa patch nel repository mantenendo i percorsi.
2. Lasciare CURIOMONDO_AUTO_PUBLISH non impostata finché il deploy non è verde.
3. Testare:
   /api/curiomondo/articles
   /dynamic-sitemap.xml
4. Inserire OPENAI_API_KEY nelle Environment variables Netlify.
5. Impostare CURIOMONDO_AUTO_PUBLISH=true.
6. Attendere il ciclo successivo (massimo 30 minuti) e controllare Function logs -> auto-editor.

## Fail-closed
Se manca API key, JSON non valido, fonti senza URL, corpo troppo corto/lungo o duplicato evidente, l'articolo non viene pubblicato.
