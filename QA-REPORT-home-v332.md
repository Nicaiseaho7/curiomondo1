# Homepage editoriale v332

Il redesign rende più riconoscibile la testata, espone le categorie e separa fotografia e titolo principale. La presentazione editoriale precede il lungo archivio orizzontale. Restano gli articoli e il loro ordinamento esistente.

## Verifiche

- `python3 tools/predeploy.py`: exit 0, 490 pagine HTML, zero errori.
- Axe WCAG 2 A/AA e 2.1 AA: zero violazioni rilevate a 320, 390, 768 e 1440 px, in modalità chiara e scura dopo la chiusura del consenso.
- Nessun overflow della pagina alle quattro larghezze; menu e ricerca aprono i rispettivi dialog.
- Screenshot desktop/mobile e scuro esaminati.
- Un solo stylesheet; nessun JavaScript, font esterno o dipendenza runtime aggiunti.
- Corrette dimensioni responsive dell'immagine principale, contrasti delle date, etichette e footer; aggiunti skip link e nome accessibile alla ricerca.
- Il generatore CSS può rigenerare il bundle anche dopo il consolidamento e conserva le correzioni del drawer precedentemente presenti solo nel bundle.

Lighthouse 12.3 / Chromium 133, emulazione mobile su server HTTP locale, due confronti: performance 97→96 e 87→91; accessibilità finale 93→100; best practice finale 96→100; SEO 100→100. I punteggi di performance del runtime condiviso variano e non dimostrano equivalenza con PageSpeed pubblico: non si certifica il mantenimento del 100 dello screenshot. CLS 0 in entrambi i primi campioni. È necessario verificare PageSpeed sulla pubblicazione Netlify.

Problema preesistente rilevato: i tre WebP `roma-monti-carabinieri-ai-openai-v326-*` non sono decodificabili. Nessuna immagine sostitutiva estranea alla notizia è stata introdotta in questo redesign.
