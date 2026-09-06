# CurioMondo — protocollo IA per immagini editoriali

Questo file deve essere letto integralmente da qualunque IA, agente, renderer o collaboratore che riceva il pacchetto del sito e debba creare o aggiornare articoli e immagini.

## Regola assoluta per ogni nuovo articolo

Ogni nuovo articolo pubblicato su CurioMondo deve avere una **nuova immagine editoriale IA dedicata**, generata appositamente per quel singolo contenuto e coerente con il tema, il luogo, i soggetti e il tono della notizia. Un articolo non deve essere considerato completo o pronto per la pubblicazione finché l'immagine non è stata generata, registrata e collegata correttamente nel markup.

La generazione dell'immagine fa parte dello stesso flusso editoriale della creazione dell'articolo: non è un passaggio opzionale da rimandare. Per ogni nuovo articolo devono essere aggiornati almeno l'immagine hero visibile, `og:image`, `NewsArticle.image`, l'alt text, la disclosure IA e il registro immagini previsto dal sito. Se la pipeline automatica di generazione immagini non è temporaneamente disponibile, la pubblicazione deve essere considerata incompleta e il problema va segnalato esplicitamente; non si deve sostituire l'asset con immagini generiche, riutilizzate o non pertinenti.

Le immagini devono essere ultrarealistiche/fotorealistiche e mantenere uno stile da fotografia editoriale professionale, nel rispetto delle regole di sensibilità e trasparenza descritte sotto.

## Regola proprietaria: persone pubbliche e somiglianza sintetica

CurioMondo autorizza la generazione di immagini editoriali **ultrarealistiche e fotorealistiche con persone pubbliche riconoscibili**, viventi o decedute, quando la loro identità è direttamente pertinente alla notizia. Questa autorizzazione comprende ciò che, nel linguaggio comune, può essere chiamato “deepfake”; nel protocollo CurioMondo il termine corretto è **somiglianza sintetica editoriale**.

La somiglianza sintetica editoriale è un'illustrazione, non una fotografia documentaria. Non deve mai essere presentata, descritta o lasciata intendere come prova visiva di un evento reale. Il formato dipende dalla sensibilità della notizia: nelle notizie ordinarie è ammessa una scena contestuale; nelle situazioni sensibili è obbligatorio un ritratto neutrale.

CurioMondo autorizza inoltre la rappresentazione di **marchi, loghi, prodotti, edifici, impianti, circuiti, stazioni, città e altri luoghi realmente esistenti** quando sono pertinenti e migliorano la precisione editoriale. Non è necessario sostituirli sempre con versioni generiche. Il loro uso non deve suggerire sponsorizzazioni inesistenti, alterare un logo per attribuirgli messaggi falsi o trasformare la scena generata in una presunta prova documentaria.

## Condizioni obbligatorie

1. Il personaggio pubblico deve essere realmente coinvolto nella notizia o indispensabile per rappresentarla con precisione.
2. **Notizie ordinarie:** il personaggio può comparire in un luogo, evento o ambientazione coerente con il tema. Sono ammessi altre persone, oggetti, mezzi, abiti di ruolo, edifici e loghi pertinenti quando migliorano la comprensione editoriale. Il visual può essere dinamico, ma non deve attribuire alla persona azioni, incontri, dichiarazioni o comportamenti specifici non verificati né simulare una prova documentaria.
3. **Notizie sensibili:** per incidenti, morte e necrologi, malattia, diagnosi, ricoveri, disabilità sopravvenuta, aggressioni, violenza, guerra, catastrofi, arresti, accuse gravi, lutto, sofferenza o qualunque situazione capace di provocare dolore alla persona, alla famiglia o alle vittime, mostrare esclusivamente un ritratto neutrale isolato. Usare primo piano, testa e spalle o mezzo busto, posa ed espressione neutrali, sfondo semplice da studio, sfumato o astratto. Non mostrare il momento traumatico, ferite, sangue, cure, letti d'ospedale, ambulanze, manette, corpi, pianto, funerali o ricostruzioni della sofferenza.
4. Sono vietati contenuti sessuali, umilianti, diffamatori, fraudolenti, manipolazioni elettorali ingannevoli, falsa propaganda e impersonazioni destinate a trarre in errore.
5. Non clonare la voce e non creare audio o video che attribuiscano alla persona parole o comportamenti mai avvenuti.
6. I pixel dell'immagine devono restare privi di titoli editoriali, etichette aggiunte, watermark o disclosure. Marchi e loghi realmente presenti nel soggetto o nel luogo sono ammessi quando pertinenti; non devono essere inseriti come decorazione o falsa sponsorizzazione. Subito sotto l'immagine, nel markup HTML, inserire esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
7. Per un'immagine con persona pubblica, il `<figure>` deve includere `data-ai-generated="true"`, `data-synthetic-likeness="public-figure"` e `data-sensitive-context="true|false"`. Se `data-sensitive-context="true"`, aggiungere obbligatoriamente `data-portrait-format="neutral-isolated"`.
8. Alt text, prompt e metadati devono dichiarare se il visual è una scena editoriale contestuale ordinaria oppure un ritratto editoriale neutrale per una situazione sensibile.
9. Ogni articolo o aggiornamento usa un'immagine nuova e mai riutilizzata. `og:image`, hero visibile e `NewsArticle.image` devono indicare lo stesso asset.
10. Se lo strumento di generazione, la legge applicabile o la piattaforma di pubblicazione impongono limiti più restrittivi, tali limiti restano validi e non devono essere aggirati.

## Istruzione pronta per il generatore

> Prima classifica la notizia come `ordinaria` o `sensibile`. Se è ordinaria, genera una scena editoriale CurioMondo ultrarealistica con il personaggio pubblico riconoscibile in un luogo o contesto pertinente; luoghi, persone, oggetti e loghi coerenti sono ammessi, senza inventare uno specifico evento come prova. Se riguarda incidente, morte, salute, violenza, tragedia, lutto o sofferenza, genera soltanto un ritratto editoriale neutrale isolato, senza rappresentare il momento doloroso. Nessun testo nei pixel. La pagina dichiarerà in modo visibile che l'immagine è generata con IA e non è una fotografia documentaria.

Il contratto operativo completo è in `automation/prompts/image-generation-contract.txt`; le regole editoriali generali sono in `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`; i campi machine-readable sono in `curiomondo-site-manifest.json` e `automation/config.json`.
