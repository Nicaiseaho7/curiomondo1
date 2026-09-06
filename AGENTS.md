# Istruzioni obbligatorie per agenti IA

Prima di creare o aggiornare articoli o visual CurioMondo, leggere integralmente, nell'ordine:

1. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
2. `automation/prompts/image-generation-contract.txt`
3. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`
4. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
5. `curiomondo-site-manifest.json`

È consentito raffigurare persone pubbliche riconoscibili con immagini ultrarealistiche quando editorialmente pertinenti. Nelle notizie ordinarie il personaggio può comparire in luoghi e ambientazioni coerenti con l'articolo; sono ammessi anche loghi pertinenti. Il **ritratto neutrale isolato** è obbligatorio soltanto per incidenti, morte, malattia, ricoveri, violenza, tragedie, lutto e altre situazioni sensibili che possono provocare dolore. Ogni somiglianza sintetica deve essere dichiarata come illustrazione IA non documentaria e non deve trasformare una scena inventata in una falsa prova. Se uno dei file obbligatori manca o le regole non possono essere rispettate, interrompere la pubblicazione.

## Regola editoriale articoli v257 — prevalenza assoluta
Per ogni nuovo articolo o aggiornamento sostanziale: corpo `.art-body` tra **3.000 e 7.000 caratteri**, senza eccezioni. La lunghezza segue le informazioni realmente disponibili, non un target fisso: lungo quando la notizia ha abbastanza sostanza verificata per riempirlo, corto (ma sempre sopra i 3.000) quando ne ha meno. È vietato ripetere un fatto o un concetto, anche riscrivendolo con parole diverse, per allungare artificialmente il testo. Ogni paragrafo deve aggiungere informazione nuova; prima del deploy è obbligatoria una revisione anti-ridondanza. Se non si raggiungono 3.000 caratteri senza ripetizioni o riempitivo, non pubblicare un articolo autonomo.

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