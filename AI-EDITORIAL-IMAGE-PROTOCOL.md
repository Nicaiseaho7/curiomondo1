# CurioMondo — protocollo IA per immagini editoriali

Questo file deve essere letto integralmente da qualunque IA, agente, renderer o collaboratore che riceva il pacchetto del sito e debba creare o aggiornare articoli e immagini.

## Prompt master — correzione dell'editore, 26 settembre 2026

Il testo operativo è `automation/prompts/image-generation-contract.txt`. In caso di conflitto con le regole del 21 settembre, vale questo:

- Un'immagine per notizia. Mai collage, riquadri o più notizie nella stessa foto.
- Fotorealismo editoriale. Niente estetica da «immagine AI», niente testo, watermark, loghi inventati o scritte deformate. Eccezione unica: le mappe meteo dell'Italia, con città e simboli leggibili.
- Ordine dell'editore, 26 settembre 2026, ore 20:14: le persone di spalle sono vietate. Vale per tutti, protagonisti e comparse. Se in copertina c'è una persona, il viso si vede. Niente nuche, niente figure girate, niente caschi chiusi al posto del volto, niente sagome. Se lo strumento rifiuta il volto, non si pubblica una persona girata.
- I sosia dei personaggi pubblici restano autorizzati, con la didascalia che è un'illustrazione editoriale e non una foto documentaria. Il viso è quello del protagonista, rivolto verso la camera.
- Cronaca, morte, violenza e arresti: niente corpi, sangue, ferite o ricostruzioni spettacolari. Se serve il volto, solo un ritratto neutro isolato.
- Non presentare la scena come fotografia documentaria dell'evento. La didascalia resta nel markup, non nei pixel.
- I limiti tecnici dello strumento di generazione restano: se quello strumento rifiuta il volto, non si aggira.
- Correzione della sera del 26 settembre 2026: il modello di qualità sono le copertine già online con la persona riconoscibile, il luogo e il marchio veri. Esempi scelti dall'editore: Haaland con la maglia della Norvegia all'Ullevaal; Trump e Xi al tavolo con i manager citati; Isaacman davanti al logo NASA. Senza un nome proprio, la scena ha comunque persone al lavoro e l'oggetto della notizia. Niente palazzi deserti e niente testo deformato.

## Persone vere, loghi veri — correzione dell'editore, 21 settembre 2026

Le immagini degli articoli devono essere **fotorealistiche** e devono raffigurare **soggetti realmente esistenti**. È vietato inventare protagonisti.

- Se la notizia nomina una persona pubblica (politico, atleta, allenatore, pilota, attore, conduttore, scienziato, dirigente), l'immagine mostra quella persona in volto, anche come sosia sintetico autorizzato dall'editore il 26 settembre 2026. Non sostituirla con un palazzo vuoto, una silhouette o un extra anonimo.
- Se la notizia riguarda una squadra, una nazionale o una partita, mostra i **giocatori veri** di quel roster e la **maglia ufficiale vera**: stemma, sponsor, fornitore tecnico, numeri e nomi. Non usare maglie lisce, loghi inventati o atleti anonimi in divisa di fantasia.
- Marchi, loghi, prodotti, mezzi, edifici e luoghi devono essere quelli **reali e pertinenti** (DHL/Erreà sulla maglia azzurra, stemma FIGC/FIPAV, logo CEV, livrea aziendale, facciata dell'istituzione). Non sostituirli con versioni generiche «per evitare marchi».
- Prima di generare: cerca foto di riferimento recenti della persona, della maglia e dei loghi; usa quelle foto come riferimento visivo. Dopo la generazione, controlla se un lettore italiano riconoscerebbe il protagonista. Se il volto, la maglia o il logo sono inventati o illeggibili, **scarta e rigenera**.
- Gli astanti di sfondo (folla, pubblico, commessi) possono restare non identificabili. Il **soggetto principale no**.
- Se la notizia non ha un volto specifico (sciopero mezzi, bando, sonda, edificio, documento), mostra l'oggetto o il luogo **reale**: la livrea vera, il veicolo vero, la sonda vera, la sede vera. Non inventare un protagonista umano.
- Un'immagine tecnicamente bella ma con personaggi inventati è un errore bloccante, come un'immagine non fotorealistica.

Questa regola non autorizza a presentare l'illustrazione come fotografia documentaria dell'evento. Resta una scena editoriale IA dichiarata, ma i volti, le maglie e i loghi devono appartenere al mondo reale.

## Soggetto principale obbligatorio — correzione dell'editore, 15 settembre 2026

La coerenza con il soggetto della notizia viene prima della bellezza dello sfondo. Un'immagine non è adeguata soltanto perché mostra un bel paesaggio, una città o un impianto della stessa disciplina sportiva.

- Se titolo e apertura riguardano un giocatore, allenatore, pilota, tennista o altro personaggio pubblico, genera **quella persona specifica, riconoscibile e protagonista dell'immagine**. Non sostituirla con un atleta anonimo, una silhouette, un pallone, uno stadio vuoto, uno skyline o un paesaggio.
- Per una notizia ordinaria è ammessa una scena editoriale contestuale fotorealistica con il protagonista: il ritratto neutrale non è il formato obbligatorio per tutte le immagini. Abbigliamento, squadra, stagione, attrezzatura e ambientazione devono essere coerenti con i fatti verificati. Non rappresentare firme, premiazioni, incontri o azioni specifiche non documentate come se fossero fotografie dell'evento.
- Per una partita o una notizia di squadra, rappresenta i protagonisti o gli elementi identificativi realmente pertinenti a quella sfida o squadra; non un campo generico intercambiabile con qualunque articolo.
- Paesaggi, panorami, edifici e impianti possono essere il soggetto principale **soltanto quando il luogo o l'infrastruttura è davvero il centro della notizia**. Non sono la soluzione predefinita né un ripiego per evitare persone pubbliche.
- Nelle notizie sensibili continua a rappresentare la persona pertinente, quando è il soggetto della notizia, ma mediante il ritratto neutrale isolato previsto sotto: non ricostruire sofferenza, traumi o accuse.
- Prima di generare, identifica il soggetto principale dal titolo e dal lead. Controlla visivamente che il risultato mostri il soggetto corretto e riconoscibile, senza personaggi estranei, scritte editoriali o watermark. Scarta e rigenera un'immagine non pertinente; non accettarla soltanto perché esteticamente riuscita e non ripiegare su un paesaggio generico.

Restano obbligatorie le regole di trasparenza, sensibilità, originalità e assenza di testo sovrapposto. La disclosure IA resta nel markup sotto l'immagine, non nei pixel.

## Regola assoluta per ogni nuovo articolo

Ogni nuovo articolo pubblicato su CurioMondo deve avere una **nuova immagine editoriale IA dedicata**, generata appositamente per quel singolo contenuto e coerente con il tema, il luogo, i soggetti e il tono della notizia. Un articolo non deve essere considerato completo o pronto per la pubblicazione finché l'immagine non è stata generata, registrata e collegata correttamente nel markup.

La generazione dell'immagine fa parte dello stesso flusso editoriale della creazione dell'articolo: non è un passaggio opzionale da rimandare. Per ogni nuovo articolo devono essere aggiornati almeno l'immagine hero visibile, `og:image`, `NewsArticle.image`, l'alt text, la disclosure IA e il registro immagini previsto dal sito. Se la pipeline automatica di generazione immagini non è temporaneamente disponibile, la pubblicazione deve essere considerata incompleta e il problema va segnalato esplicitamente; non si deve sostituire l'asset con immagini generiche, riutilizzate o non pertinenti.

Le immagini devono essere ultrarealistiche/fotorealistiche e mantenere uno stile da fotografia editoriale professionale, nel rispetto delle regole di sensibilità e trasparenza descritte sotto.

## Divieto permanente Pollinations

È vietato usare Pollinations, `pollinations.ai`, `image.pollinations.ai` o qualunque suo endpoint, modello o asset per generare, scaricare o pubblicare immagini su CurioMondo. Le immagini editoriali devono essere generate direttamente con gli strumenti immagini di ChatGPT/OpenAI autorizzati dal proprietario e devono essere controllate visivamente prima della pubblicazione. Qualunque asset con watermark, firma o marchio del generatore è bloccante e non può essere pubblicato.

## Regola proprietaria: persone pubbliche e somiglianza sintetica

CurioMondo autorizza la generazione di immagini editoriali **ultrarealistiche e fotorealistiche con persone pubbliche riconoscibili**, viventi o decedute, quando la loro identità è direttamente pertinente alla notizia. Questa autorizzazione comprende ciò che, nel linguaggio comune, può essere chiamato “deepfake”; nel protocollo CurioMondo il termine corretto è **somiglianza sintetica editoriale**.

La somiglianza sintetica editoriale è un'illustrazione, non una fotografia documentaria. Non deve mai essere presentata, descritta o lasciata intendere come prova visiva di un evento reale. Il formato dipende dalla sensibilità della notizia: nelle notizie ordinarie è ammessa una scena contestuale; nelle situazioni sensibili è obbligatorio un ritratto neutrale.

CurioMondo autorizza inoltre la rappresentazione di **marchi, loghi, prodotti, edifici, impianti, circuiti, stazioni, città e altri luoghi realmente esistenti** quando sono pertinenti e migliorano la precisione editoriale. Non è necessario sostituirli sempre con versioni generiche. Il loro uso non deve suggerire sponsorizzazioni inesistenti, alterare un logo per attribuirgli messaggi falsi o trasformare la scena generata in una presunta prova documentaria.

## Condizioni obbligatorie

1. Il personaggio pubblico deve essere realmente coinvolto nella notizia o indispensabile per rappresentarla con precisione. Deve essere **quella persona**, non un volto inventato.
2. **Notizie ordinarie:** il personaggio può comparire in un luogo, evento o ambientazione coerente con il tema. Sono ammessi altre persone, oggetti, mezzi, abiti di ruolo, edifici e loghi pertinenti quando migliorano la comprensione editoriale. Il visual può essere dinamico, ma non deve attribuire alla persona azioni, incontri, dichiarazioni o comportamenti specifici non verificati né simulare una prova documentaria.
3. **Notizie sensibili:** per incidenti, morte e necrologi, malattia, diagnosi, ricoveri, disabilità sopravvenuta, aggressioni, violenza, guerra, catastrofi, arresti, accuse gravi, lutto, sofferenza o qualunque situazione capace di provocare dolore alla persona, alla famiglia o alle vittime, mostrare esclusivamente un ritratto neutrale isolato. Usare primo piano, testa e spalle o mezzo busto, posa ed espressione neutrali, sfondo semplice da studio, sfumato o astratto. Non mostrare il momento traumatico, ferite, sangue, cure, letti d'ospedale, ambulanze, manette, corpi, pianto, funerali o ricostruzioni della sofferenza.
4. Sono vietati contenuti sessuali, umilianti, diffamatori, fraudolenti, manipolazioni elettorali ingannevoli, falsa propaganda e impersonazioni destinate a trarre in errore.
5. Non clonare la voce e non creare audio o video che attribuiscano alla persona parole o comportamenti mai avvenuti.
6. I pixel dell'immagine devono restare privi di titoli editoriali, etichette aggiunte, watermark o disclosure. Marchi e loghi realmente presenti nel soggetto o nel luogo sono ammessi quando pertinenti; non devono essere inseriti come decorazione o falsa sponsorizzazione. Subito sotto l'immagine, nel markup HTML, inserire esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
7. Per un'immagine con persona pubblica, il `<figure>` deve includere `data-ai-generated="true"`, `data-synthetic-likeness="public-figure"` e `data-sensitive-context="true|false"`. Se `data-sensitive-context="true"`, aggiungere obbligatoriamente `data-portrait-format="neutral-isolated"`.
8. Alt text, prompt e metadati devono dichiarare se il visual è una scena editoriale contestuale ordinaria oppure un ritratto editoriale neutrale per una situazione sensibile.
9. Ogni articolo o aggiornamento usa un'immagine nuova e mai riutilizzata. `og:image`, hero visibile e `NewsArticle.image` devono indicare lo stesso asset.
10. Se lo strumento di generazione, la legge applicabile o la piattaforma di pubblicazione impongono limiti più restrittivi, tali limiti restano validi e non devono essere aggirati.
11. **Divieto di personaggi inventati:** se titolo o lead nominano persone, squadre o marchi reali, l'immagine che li sostituisce con extra generici, maglie di fantasia o loghi illeggibili è rifiutata. Cercare riferimenti visivi reali prima di generare.

## Istruzione pronta per il generatore

> Prima identifica il soggetto principale dal titolo e dal lead. Se è un personaggio pubblico, raffigura proprio quella persona riconoscibile, non un volto inventato, un atleta anonimo o un paesaggio. Se è una squadra, usa i giocatori e la maglia ufficiali veri, con stemma e sponsor reali. Classifica poi la notizia come `ordinaria` o `sensibile`. Se è ordinaria, genera una scena editoriale CurioMondo ultrarealistica con il personaggio pubblico riconoscibile in un luogo o contesto pertinente; luoghi, persone, oggetti e loghi coerenti sono ammessi, senza inventare uno specifico evento come prova. Se riguarda incidente, morte, salute, violenza, tragedia, lutto o sofferenza, genera soltanto un ritratto editoriale neutrale isolato della persona reale, senza rappresentare il momento doloroso. Un luogo può essere il soggetto principale soltanto quando è realmente al centro della notizia. Nessun testo editoriale nei pixel. La pagina dichiarerà in modo visibile che l'immagine è generata con IA e non è una fotografia documentaria.

Il contratto operativo completo è in `automation/prompts/image-generation-contract.txt`; le regole editoriali generali sono in `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`; i campi machine-readable sono in `curiomondo-site-manifest.json` e `automation/config.json`.
