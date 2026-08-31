# QA CurioMondo v248

Data: 30 agosto 2026

## Scopo
Aggiornamento esclusivamente editoriale/protocollare. Nessun articolo esistente è stato riscritto e nessun elemento grafico del sito è stato modificato.

## Nuovo contratto articoli
- Corpo `.art-body`: minimo 2.000, massimo 4.500 caratteri.
- Nessuna eccezione di lunghezza per nuovi articoli o aggiornamenti sostanziali soggetti alla policy v248.
- Divieto assoluto di ripetizioni esatte, parafrasi ridondanti e riepiloghi che ripetano concetti già espressi.
- Ogni paragrafo deve aggiungere informazione nuova.
- Se le informazioni verificate non consentono 2.000 caratteri senza riempitivo, non si pubblica un articolo autonomo.

## File canonici aggiornati
- `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
- `AUTOMAZIONE-CURIOMONDO-SETUP.md`
- `automation/prompts/editorial-contract.txt`
- `automation/config.json`
- `curiomondo-site-manifest.json`
- `AGENTS.md`
- `LEGGIMI-PRIMA-CURIOMONDO.md`
- `tools/predeploy.py`

## Gate automatici
Il predeploy v248:
- verifica che config e manifest dichiarino 2.000–4.500 caratteri;
- applica il limite ai contenuti pubblicati/modificati dopo l'entrata in vigore della policy v248;
- richiede `data-length-policy="2000-4500"` nel markup dei contenuti soggetti alla nuova regola;
- intercetta frasi duplicate e somiglianze testuali forti come segnale di ridondanza;
- conserva tutti i gate storici di integrità, immagini, LIVE, homepage e link.

## Esito
`python tools/predeploy.py` → 0 errori.
