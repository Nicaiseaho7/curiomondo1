#!/usr/bin/env python3
"""Correzioni minime al legacy cinema richieste dal gate v4."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notizie" / "cinema-uscite-italia-14-20-settembre-2026.html"
page = path.read_text(encoding="utf-8")

replacements = {
    "Horror, memoria della dittatura argentina e commedia sentimentale: tre percorsi diversi arrivano nei cinema italiani giovedì 17 settembre 2026. Resident Evil, Ritorno a Buenos Aires e Dov’è la Fiesta? compongono questa selezione per la settimana dal 14 al 20 settembre. La guida è stata aggiornata il 16 settembre con una novità utile anche per chi guarda le serie in streaming: Neagley è ora disponibile su Prime Video.":
    "Horror, memoria della dittatura argentina e commedia sentimentale arrivano nei cinema italiani giovedì 17 settembre 2026. Resident Evil, Ritorno a Buenos Aires e Dov’è la Fiesta? compongono la selezione della settimana. Dal 16 settembre Neagley è inoltre disponibile su Prime Video.",
    "Dal 16 settembre è disponibile anche Neagley, spin-off di Reacher con Maria Sten nel ruolo di Frances Neagley. Amazon conferma che tutti gli otto episodi della prima stagione sono già online su Prime Video in oltre 240 Paesi e territori. La scheda italiana della piattaforma mostra gli otto episodi datati 16 settembre 2026 e indica audio e sottotitoli in italiano.":
    "Dal 16 settembre è disponibile anche Neagley, spin-off di Reacher con Maria Sten. Amazon conferma che gli otto episodi della prima stagione sono online su Prime Video in oltre 240 Paesi e territori. La scheda italiana indica audio e sottotitoli in italiano.",
    "La serie segue Neagley, ora investigatrice privata a Chicago, quando la morte sospetta di una persona del suo passato la spinge ad avviare un’indagine. È la premessa ufficiale e non anticipa gli sviluppi degli episodi. Nel cast figurano anche Greyston Holt, Adeline Rudolph, Jasper Jones, Matthew Del Negro e Damon Herriman; Alan Ritchson compare come guest star nei panni di Jack Reacher. Nick Santora e Nicholas Wootton sono creatori e co-showrunner.":
    "Neagley, investigatrice privata a Chicago, avvia un’indagine dopo la morte sospetta di una persona del suo passato. È la premessa ufficiale e non anticipa gli sviluppi degli episodi. Nel cast figurano Greyston Holt, Adeline Rudolph, Jasper Jones, Matthew Del Negro e Damon Herriman; Alan Ritchson compare come Jack Reacher.",
    "Per il pubblico italiano la distinzione pratica è importante: Neagley è proposta come serie in streaming su Prime Video, non come noleggio o acquisto digitale singolo. La pagina italiana mostra l’accesso attraverso iscrizione o periodo di prova; prezzi e condizioni dipendono dall’account e dal territorio. TheWrap aveva anticipato la distribuzione in blocco degli otto episodi il 16 settembre, mentre TVLine include oggi il debutto tra le principali uscite streaming della giornata.":
    "Neagley è proposta in Italia come serie in streaming su Prime Video, non come noleggio o acquisto digitale singolo. La pagina italiana mostra l’accesso tramite iscrizione o prova; prezzi e condizioni dipendono dall’account e dal territorio. TheWrap e TVLine confermano l’uscita degli otto episodi il 16 settembre.",
    "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa guida; non è una fotografia documentaria.":
    "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.",
}

for old, new in replacements.items():
    if old not in page:
        raise RuntimeError(f"testo legacy non trovato: {old[:50]}")
    page = page.replace(old, new, 1)

path.write_text(page, encoding="utf-8")
print(path)
