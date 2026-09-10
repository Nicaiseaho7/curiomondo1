# Istruzioni obbligatorie per agenti IA

Prima di creare o aggiornare articoli o visual CurioMondo, leggere integralmente, nell'ordine:

1. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
2. `automation/prompts/image-generation-contract.txt`
3. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`
4. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
5. `curiomondo-site-manifest.json`

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Regola editoriale articoli v317 — prevalenza assoluta
Ogni articolo segue il protocollo 4.0 in `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`: piramide invertita; lead con le 5 W; paragrafi di 2–4 frasi e massimo 60 parole; frasi preferibilmente entro 20–25 parole; nessuna ripetizione, prima persona, enfasi o riempitivo. La lunghezza dipende dal formato: flash 100–250 parole, notizia standard 300–600, approfondimento autonomo 800–1.500+ parole. Gli aggiornamenti sostanziali possono superare la fascia. È vietato spiegare parole difficili nel corpo della notizia: usare un lessico chiaro oppure creare o collegare una pagina di approfondimento quando serve. Restano obbligatori il gate preventivo e almeno due elementi reali di valore aggiunto. Se manca materia verificata, l'esito è `NON PUBBLICARE — motivo`.

## Gate di pubblicazione completa — obbligatorio
Un articolo non deve mai essere considerato pubblicato soltanto perché il file HTML esiste nel repository. La pubblicazione è completa soltanto quando, nello stesso ciclo:

- è presente una nuova immagine editoriale IA dedicata, validata e collegata a hero, `og:image` e `NewsArticle.image`;
- sono aggiornati homepage o listing editoriale previsto, archivio, ricerca, feed, sitemap e News Sitemap quando pertinente;
- canonical e dati strutturati sono coerenti con l'URL pubblico;
- `python3 tools/predeploy.py` termina con exit code 0;
- dopo il deploy, l'URL pubblico dell'articolo e l'immagine hero rispondono correttamente e la notizia compare nelle superfici editoriali previste.

Se uno qualunque di questi punti manca, segnalare la pubblicazione come **incompleta** e non dichiararla conclusa.

## Regola approfondimenti coerente
Nessun glossario o gancio didascalico è obbligatorio dentro la notizia. Un approfondimento autonomo va creato o collegato **solo quando aggiunge valore durevole, non ridondante e realmente utile**. Se esiste già una guida equivalente, collegarla invece di crearne una nuova. Le spiegazioni tematiche necessarie vivono nella pagina dedicata; la notizia resta concentrata sui fatti.
