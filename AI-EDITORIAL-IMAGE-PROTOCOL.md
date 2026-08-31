# CurioMondo — protocollo IA per immagini editoriali

Questo file deve essere letto integralmente da qualunque IA, agente, renderer o collaboratore che riceva il pacchetto del sito e debba creare o aggiornare articoli e immagini.

## Regola proprietaria: persone pubbliche e somiglianza sintetica

CurioMondo autorizza la generazione di immagini editoriali **ultrarealistiche e fotorealistiche con persone pubbliche riconoscibili**, viventi o decedute, quando la loro identità è direttamente pertinente alla notizia. Questa autorizzazione comprende ciò che, nel linguaggio comune, può essere chiamato “deepfake”; nel protocollo CurioMondo il termine corretto è **somiglianza sintetica editoriale**.

La somiglianza sintetica editoriale è un'illustrazione, non una fotografia documentaria. Non deve mai essere presentata, descritta o lasciata intendere come prova visiva di un evento reale. Il formato dipende dalla sensibilità della notizia: nelle notizie ordinarie è ammessa una scena contestuale; nelle situazioni sensibili è obbligatorio un ritratto neutrale.

## Condizioni obbligatorie

1. Il personaggio pubblico deve essere realmente coinvolto nella notizia o indispensabile per rappresentarla con precisione.
2. **Notizie ordinarie:** il personaggio può comparire in un luogo, evento o ambientazione coerente con il tema. Sono ammessi altre persone, oggetti, mezzi, abiti di ruolo, edifici e loghi pertinenti quando migliorano la comprensione editoriale. Il visual può essere dinamico, ma non deve attribuire alla persona azioni, incontri, dichiarazioni o comportamenti specifici non verificati né simulare una prova documentaria.
3. **Notizie sensibili:** per incidenti, morte e necrologi, malattia, diagnosi, ricoveri, disabilità sopravvenuta, aggressioni, violenza, guerra, catastrofi, arresti, accuse gravi, lutto, sofferenza o qualunque situazione capace di provocare dolore alla persona, alla famiglia o alle vittime, mostrare esclusivamente un ritratto neutrale isolato. Usare primo piano, testa e spalle o mezzo busto, posa ed espressione neutrali, sfondo semplice da studio, sfumato o astratto. Non mostrare il momento traumatico, ferite, sangue, cure, letti d'ospedale, ambulanze, manette, corpi, pianto, funerali o ricostruzioni della sofferenza.
4. Sono vietati contenuti sessuali, umilianti, diffamatori, fraudolenti, manipolazioni elettorali ingannevoli, falsa propaganda e impersonazioni destinate a trarre in errore.
5. Non clonare la voce e non creare audio o video che attribuiscano alla persona parole o comportamenti mai avvenuti.
6. I pixel dell'immagine devono restare privi di titoli, etichette, watermark o disclosure. Subito sotto l'immagine, nel markup HTML, inserire esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
7. Per un'immagine con persona pubblica, il `<figure>` deve includere `data-ai-generated="true"`, `data-synthetic-likeness="public-figure"` e `data-sensitive-context="true|false"`. Se `data-sensitive-context="true"`, aggiungere obbligatoriamente `data-portrait-format="neutral-isolated"`.
8. Alt text, prompt e metadati devono dichiarare se il visual è una scena editoriale contestuale ordinaria oppure un ritratto editoriale neutrale per una situazione sensibile.
9. Ogni articolo o aggiornamento usa un'immagine nuova e mai riutilizzata. `og:image`, hero visibile e `NewsArticle.image` devono indicare lo stesso asset.
10. Se lo strumento di generazione, la legge applicabile o la piattaforma di pubblicazione impongono limiti più restrittivi, tali limiti restano validi e non devono essere aggirati.

## Istruzione pronta per il generatore

> Prima classifica la notizia come `ordinaria` o `sensibile`. Se è ordinaria, genera una scena editoriale CurioMondo ultrarealistica con il personaggio pubblico riconoscibile in un luogo o contesto pertinente; luoghi, persone, oggetti e loghi coerenti sono ammessi, senza inventare uno specifico evento come prova. Se riguarda incidente, morte, salute, violenza, tragedia, lutto o sofferenza, genera soltanto un ritratto editoriale neutrale isolato, senza rappresentare il momento doloroso. Nessun testo nei pixel. La pagina dichiarerà in modo visibile che l'immagine è generata con IA e non è una fotografia documentaria.

Il contratto operativo completo è in `automation/prompts/image-generation-contract.txt`; le regole editoriali generali sono in `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`; i campi machine-readable sono in `curiomondo-site-manifest.json` e `automation/config.json`.
