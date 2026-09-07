# Istruzioni obbligatorie per agenti IA

Prima di creare o aggiornare articoli o visual CurioMondo, leggere integralmente, nell'ordine:

1. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
2. `automation/prompts/image-generation-contract.txt`
3. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`
4. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
5. `curiomondo-site-manifest.json`

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Regola editoriale articoli v303 — prevalenza assoluta
Non esiste un minimo fisso di caratteri. La lunghezza dipende dal tipo di contenuto e dai fatti verificati: notizie di servizio e bandi possono essere brevi e operativi; dati da decodificare e approfondimenti richiedono più spazio. Ogni articolo deve superare il gate preventivo e contenere almeno due elementi reali di valore aggiunto secondo `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`. È vietato ripetere, diluire o aggiungere definizioni ovvie per raggiungere una misura. Se il gate fallisce, l'esito è `NON PUBBLICARE — motivo`.

## Gate di pubblicazione completa — obbligatorio
Un articolo non deve mai essere considerato pubblicato soltanto perché il file HTML esiste nel repository. La pubblicazione è completa soltanto quando, nello stesso ciclo:

- è presente una nuova immagine editoriale IA dedicata, validata e collegata a hero, `og:image` e `NewsArticle.image`;
- sono aggiornati homepage o listing editoriale previsto, archivio, ricerca, feed, sitemap e News Sitemap quando pertinente;
- canonical e dati strutturati sono coerenti con l'URL pubblico;
- `python3 tools/predeploy.py` termina con exit code 0;
- dopo il deploy, l'URL pubblico dell'articolo e l'immagine hero rispondono correttamente e la notizia compare nelle superfici editoriali previste.

Se uno qualunque di questi punti manca, segnalare la pubblicazione come **incompleta** e non dichiararla conclusa.

## Regola evergreen coerente
Il gancio di conoscenza è obbligatorio in ogni articolo. Un approfondimento evergreen autonomo invece va creato o collegato **solo quando aggiunge valore durevole, non ridondante e realmente utile**. Se esiste già una guida equivalente, collegarla invece di crearne una nuova. Se il concetto è semplice e basta una spiegazione naturale nel corpo, non creare una pagina evergreen forzata.
