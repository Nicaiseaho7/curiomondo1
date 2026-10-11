#!/usr/bin/env python3
"""Segnalazioni dell'11 ottobre: sei notizie, un solo aggiornamento superfici."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_finale_20261010_v836 as prior
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

VERSION = 840
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "quiles": ROOT.parent / "generated_images/exec-75841676-465e-44e7-918c-7a2f2d2b77ef.png",
    "gea": ROOT.parent / "generated_images/exec-488b4fe5-fe15-481b-8734-b20083f3c2ad.png",
    "barcelona": ROOT.parent / "generated_images/exec-d446bb4d-6241-4a2f-93d9-7e09124ea172.png",
    "nepal": ROOT.parent / "generated_images/exec-bf1d64d4-3d14-4dc0-8f5a-6405ebb1d621.png",
    "fai": ROOT.parent / "generated_images/exec-0f5452e7-7be3-44a1-a891-bb3f27cb0af5.png",
    "unicef": ROOT.parent / "generated_images/exec-5a029e9d-f7f7-4120-a65f-df74a9145a16.png",
}

ARTICLES = [
    {
        "slug": "quiles-campione-moto3-mandalika-11-ottobre-2026",
        "titolo": "Moto3, Quiles campione del mondo dopo la vittoria a Mandalika",
        "sommario": "Lo spagnolo conquista il titolo con cinque Gran Premi ancora da disputare. In Indonesia precede Almansa e Uriarte nella gara decisiva.",
        "categoria": "Sport", "luogo": "Mandalika, Indonesia", "formato": "flash",
        "parole_chiave_titolo": ["Quiles", "Moto3"],
        "dati_chiave": [{"valore": "18 anni", "etichetta": "età di Quiles"}, {"valore": "5", "etichetta": "gare ancora da correre"}, {"valore": "1°", "etichetta": "a Mandalika"}],
        "paragrafi": [
            "Máximo Quiles è campione del mondo Moto3 2026. Il pilota spagnolo ha vinto domenica 11 ottobre il Gran Premio d'Indonesia a Mandalika e ha conquistato matematicamente il titolo quando mancano ancora cinque gare alla conclusione della stagione.",
            "Quiles ha preceduto al traguardo David Almansa e Álvaro Uriarte, secondo il risultato pubblicato dalla MotoGP. È il decimo successo dello spagnolo in questa stagione: la vittoria odierna chiude la lotta per il campionato senza dover attendere i prossimi appuntamenti.",
            "Il titolo arriva a 18 anni. Per chi segue la classe più piccola del Motomondiale, il dato decisivo non è soltanto l'ordine d'arrivo in Indonesia: il margine accumulato da Quiles non può più essere colmato dagli inseguitori nelle cinque corse rimanenti.",
            "La gara di Mandalika è già terminata. I successivi Gran Premi restano in calendario e potranno modificare il piazzamento degli altri piloti, ma non il nome del campione Moto3 2026.",
        ],
        "fonti": [{"url": "https://www.motogp.com/it/news/2026/10/10/il-successo-di-mandalika-vale-a-quiles-il-titolo-iridato-della-moto3/1174842", "nome": "MotoGP — vittoria a Mandalika e titolo mondiale Moto3, 11 ottobre 2026."}],
        "image_source": "quiles", "image_likeness": "Máximo Quiles",
        "image_alt": "Illustrazione editoriale IA del pilota Máximo Quiles in un paddock; la tuta è rappresentativa e non è un documento fotografico della gara.",
        "image_prompt": "Ritratto sintetico di Máximo Quiles nel paddock; non fotografia della premiazione. Logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "arthur-gea-elimina-ben-shelton-shanghai-11-ottobre-2026",
        "titolo": "Shanghai, Arthur Gea elimina Shelton: primo successo su un top 10",
        "sommario": "Il francese vince due tie-break, 7-6(5) 7-6(3), contro la terza testa di serie e raggiunge gli ottavi del Masters 1000.",
        "categoria": "Sport", "luogo": "Shanghai, Cina", "formato": "flash",
        "parole_chiave_titolo": ["Arthur Gea", "Shelton"],
        "dati_chiave": [{"valore": "7-6 7-6", "etichetta": "risultato"}, {"valore": "n. 3", "etichetta": "testa di serie Shelton"}, {"valore": "ottavi", "etichetta": "turno raggiunto"}],
        "paragrafi": [
            "Arthur Gea ha battuto Ben Shelton domenica 11 ottobre al Masters 1000 di Shanghai. Il francese ha chiuso 7-6(5), 7-6(3) contro la terza testa di serie, ottenendo la sua prima vittoria in carriera contro un giocatore fra i primi dieci del mondo.",
            "I due set sono stati decisi entrambi al tie-break. Gea, alla prima presenza nel tabellone principale di un torneo Masters 1000, accede così agli ottavi dopo avere superato uno dei favoriti del torneo.",
            "Il risultato è registrato nel resoconto ufficiale del torneo. La sconfitta ferma invece il percorso di Shelton a Shanghai: non è una notizia su un ritiro o un infortunio, ma sull'esito della partita giocata e conclusa oggi.",
            "Per gli appassionati italiani, il prossimo impegno di Gea dipenderà dal tabellone e dagli orari pubblicati dagli organizzatori. La vittoria in due tie-break non stabilisce da sola giorno e ora del match successivo.",
        ],
        "fonti": [{"url": "https://en.rolexshanghaimasters.com/en/media/news/gea-shelton-shanghai-2026-sunday", "nome": "Rolex Shanghai Masters — risultato e resoconto Gea-Shelton, 11 ottobre 2026."}],
        "image_source": "gea", "image_likeness": "Arthur Gea",
        "image_alt": "Illustrazione editoriale IA del tennista Arthur Gea su un campo a Shanghai; non è una fotografia del match contro Shelton.",
        "image_prompt": "Ritratto sintetico di Arthur Gea sul campo di Shanghai, non foto della partita; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "barcellona-getafe-3-0-otto-vittorie-11-ottobre-2026",
        "titolo": "Barcellona-Getafe 3-0: ottava vittoria di fila in Liga",
        "sommario": "Gordon segna dopo due minuti, poi vanno in rete Gabriel Jesus e Koundé. I catalani proseguono la striscia di successi nel campionato spagnolo.",
        "categoria": "Sport", "luogo": "Barcellona, Spagna", "formato": "flash",
        "parole_chiave_titolo": ["Barcellona", "Getafe"],
        "dati_chiave": [{"valore": "3-0", "etichetta": "risultato"}, {"valore": "2'", "etichetta": "gol di Gordon"}, {"valore": "8", "etichetta": "vittorie consecutive"}],
        "paragrafi": [
            "Il Barcellona ha battuto il Getafe 3-0 sabato 10 ottobre, ottenendo l'ottava vittoria consecutiva nella Liga. Anthony Gordon ha aperto il risultato al secondo minuto, Gabriel Jesus ha raddoppiato al 30' e Jules Koundé ha segnato il terzo gol al 73'.",
            "La cronologia ufficiale della Liga attribuisce a Lamine Yamal l'assist sul gol di Koundé. Il risultato non è un aggiornamento in diretta: la partita è terminata e le tre reti risultano nel tabellino della competizione.",
            "La serie di otto vittorie riguarda il campionato spagnolo, non tutte le competizioni. È questo il dato che rende rilevante il successo sul Getafe oltre al punteggio della singola gara.",
            "Per confrontare la posizione del Barcellona con le inseguitrici occorre considerare anche le altre partite della giornata: il 3-0 da solo non definisce la classifica finale del turno.",
        ],
        "fonti": [{"url": "https://www.laliga.com/en-US/match/temporada-2026-2027-laliga-ea-sports-fc-barcelona-getafe-cf-8", "nome": "LaLiga — tabellino ufficiale Barcellona-Getafe del 10 ottobre 2026."}, {"url": "https://www.fcbarcelona.com/en/football/first-team/news/4590436/fc-barcelona-equal-best-start-to-league-season", "nome": "FC Barcelona — otto successi nelle prime otto giornate e primato eguagliato."}],
        "image_source": "barcelona",
        "image_alt": "Illustrazione editoriale IA di uno stadio nella città di Barcellona; architettura evocativa, non fotografia dell'impianto o della partita.",
        "image_prompt": "Stadio evocativo a Barcellona, illustrazione non documentaria; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "nepal-piena-budhi-gandaki-gorkha-dispersi-soccorsi-11-ottobre-2026",
        "titolo": "Nepal, piena del Budhi Gandaki a Gorkha: dispersi e ponti distrutti",
        "sommario": "La radio pubblica segnala almeno dieci dispersi. La polizia locale riferisce danni a tre ponti nel distretto di Gorkha.",
        "categoria": "Mondo", "luogo": "Gorkha, Nepal", "formato": "flash",
        "parole_chiave_titolo": ["Nepal", "Budhi Gandaki"],
        "dati_chiave": [{"valore": "almeno 10", "etichetta": "dispersi segnalati"}, {"valore": "3", "etichetta": "ponti danneggiati"}, {"valore": "11 ottobre", "etichetta": "aggiornamento"}],
        "paragrafi": [
            "Una piena del fiume Budhi Gandaki ha colpito il distretto di Gorkha, in Nepal, domenica 11 ottobre. Radio Nepal, emittente pubblica, riferisce di almeno dieci persone disperse. Le ricerche e la valutazione dei danni sono in corso.",
            "Il Kathmandu Post riferisce, citando la polizia locale, che l'acqua ha portato via due ponti pedonali sospesi e un ponte in acciaio. Sono segnalati anche danni alle abitazioni nell'area interessata.",
            "Il numero dei dispersi è un bilancio provvisorio, non un conteggio confermato delle vittime. La notizia sui ponti descrive le infrastrutture danneggiate, non permette di dedurre quante persone siano state coinvolte direttamente.",
            "I ponti interrotti possono complicare gli spostamenti e i soccorsi nelle località servite dagli attraversamenti. Non sono disponibili, nelle comunicazioni consultate, tempi ufficiali per il ripristino o un bilancio definitivo dei danni.",
        ],
        "fonti": [{"url": "https://radionepalonline.com/en/2026/10/11/437636.html", "nome": "Radio Nepal — dispersi nella piena del Budhi Gandaki, 11 ottobre 2026."}, {"url": "https://kathmandupost.com/national/2026/10/11/budhi-gandaki-flood-washes-away-three-bridges-in-gorkha", "nome": "The Kathmandu Post — danni ai ponti secondo la polizia locale."}],
        "image_source": "nepal", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA di un ponte danneggiato da una piena in un paesaggio montano; non è una fotografia del disastro a Gorkha.",
        "image_prompt": "Scena sintetica di piena fluviale e ponte danneggiato, non documentaria; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "giornate-fai-autunno-11-ottobre-2026-luoghi-visite",
        "titolo": "Giornate FAI d'autunno, oggi ultimo giorno: oltre 700 luoghi aperti",
        "sommario": "Le visite interessano oltre 350 città. Per gli orari e le eventuali prenotazioni serve verificare la scheda del singolo luogo sul sito FAI.",
        "categoria": "Cultura", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Giornate FAI", "700 luoghi"],
        "dati_chiave": [{"valore": "11 ottobre", "etichetta": "ultimo giorno"}, {"valore": "oltre 700", "etichetta": "luoghi aperti"}, {"valore": "350", "etichetta": "città coinvolte"}],
        "paragrafi": [
            "Domenica 11 ottobre è l'ultimo giorno delle Giornate FAI d'autunno 2026. Il Fondo per l'Ambiente Italiano ha organizzato aperture in oltre 700 luoghi di più di 350 città, con visite a edifici storici, spazi culturali e siti normalmente meno accessibili.",
            "Per trovare una visita ancora possibile oggi, il passaggio utile è consultare l'elenco ufficiale dei luoghi aperti e poi la scheda della destinazione scelta. Orari, capienza, accessibilità e modalità d'ingresso non sono identici in tutte le località.",
            "L'iniziativa prevede generalmente un contributo libero a sostegno del FAI. Alcune aperture sono riservate agli iscritti e, dove indicato, può essere necessaria la prenotazione: per questo non è corretto considerare ogni ingresso libero e senza attesa.",
            "Tra gli itinerari annunciati figurano visite legate al patrimonio e al Made in Italy. Il programma resta consultabile sul sito FAI; prima di partire, soprattutto nelle ultime ore della giornata, è opportuno controllare disponibilità e orario di chiusura del luogo specifico.",
        ],
        "fonti": [{"url": "https://fondoambiente.it/news/giornate-fai-dautunno-2026-700-luoghi-aperti-in-350-citta-ditalia", "nome": "FAI — programma nazionale delle Giornate d'autunno 2026."}, {"url": "https://fondoambiente.it/il-fai/grandi-campagne/giornate-fai-autunno/i-luoghi-aperti", "nome": "FAI — elenco ufficiale dei luoghi, orari e modalità di visita."}],
        "image_source": "fai",
        "image_alt": "Illustrazione editoriale IA di visitatori in un cortile storico italiano; non documenta una specifica apertura FAI.",
        "image_prompt": "Visita sintetica in cortile storico italiano, non fotografia di evento FAI; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "giornata-bambine-2026-unicef-matrimoni-precoci-dati",
        "titolo": "Giornata delle bambine, UNICEF: 12 milioni di matrimoni precoci l'anno",
        "sommario": "La campagna 2026 richiama l'attenzione sul matrimonio infantile. Unicef stima che una donna su cinque sia stata sposata prima dei 18 anni.",
        "categoria": "Mondo", "luogo": "New York", "formato": "flash",
        "parole_chiave_titolo": ["UNICEF", "matrimoni precoci"],
        "dati_chiave": [{"valore": "12 milioni", "etichetta": "stima annua"}, {"valore": "1 su 5", "etichetta": "donne sposate da minori"}, {"valore": "11 ottobre", "etichetta": "giornata internazionale"}],
        "paragrafi": [
            "Per la Giornata internazionale delle bambine, domenica 11 ottobre, UNICEF mette al centro della campagna 2026 la prevenzione del matrimonio infantile. L'organizzazione stima che oltre 12 milioni di ragazze si sposino ogni anno prima dei 18 anni.",
            "Il dato di una su cinque si riferisce alle donne oggi in vita che sono state sposate da bambine, non alla quota di tutte le ragazze che si sposeranno quest'anno. UNICEF quantifica in circa 650 milioni le donne e ragazze viventi che hanno contratto un matrimonio prima della maggiore età.",
            "La prevalenza indicata dall'organizzazione è maggiore nell'Africa subsahariana, dove il valore riportato è del 31%. La stima globale non descrive quindi in modo uniforme i singoli Paesi o le comunità.",
            "La campagna chiede investimenti nei diritti e nelle opportunità delle ragazze. I numeri sono stime sulla dimensione del problema, non un nuovo conteggio di matrimoni avvenuti oggi; UNICEF segnala che nei 25 anni precedenti circa 68 milioni di matrimoni infantili sono stati evitati.",
        ],
        "fonti": [{"url": "https://www.unicef.org/gender-equality/international-day-girl", "nome": "UNICEF — Giornata internazionale delle bambine 2026 e dati sul matrimonio infantile."}],
        "image_source": "unicef", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA di quaderni e alunne viste di spalle in classe; non rappresenta bambine reali coinvolte nei dati UNICEF.",
        "image_prompt": "Scena sintetica rispettosa di scuola e bambine viste di spalle; logo CurioMondo circolare in post-produzione.",
    },
]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("uso: script.py indice timestamp-ISO-Europe/Rome")
    index = int(sys.argv[1])
    published = datetime.fromisoformat(sys.argv[2])
    if published.utcoffset() != ZoneInfo("Europe/Rome").utcoffset(published):
        raise SystemExit("timestamp Europe/Rome richiesto")
    if index == 0:
        phrases_path = ROOT / "assets/data/frasi-nome.json"
        phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
        for phrase in (
            "Oggi puoi dedicare tempo a un traguardo che conta per te.",
            "Un risultato inatteso può aprire possibilità nuove.",
            "Concediti una pausa dopo una giornata intensa.",
            "Se sei in difficoltà, chiedere aiuto è un passo concreto.",
            "Controlla gli orari prima di partire per una visita.",
            "Ogni ragazza merita opportunità di studiare e scegliere.",
        ):
            if phrase not in phrases:
                phrases.append(phrase)
        phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    article = ARTICLES[index]
    image = base.make_image(article)
    slug = site.write_article(article, image, VERSION)
    base.set_published(slug, published)
    prior.correct_visible_date(slug, published, article["luogo"])
    image["article"] = f"/notizie/{slug}.html"
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["items"] = [image] + registry.get("items", [])
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if index == len(ARTICLES) - 1:
        # Integra la seconda fonte primaria verificata dopo la stesura del terzo pezzo.
        match_path = ROOT / "notizie/barcellona-getafe-3-0-otto-vittorie-11-ottobre-2026.html"
        match_doc = html.fromstring(match_path.read_text(encoding="utf-8"))
        sources_list = match_doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]/ul')[0]
        club_source = ARTICLES[2]["fonti"][1]
        if not sources_list.xpath('./li/a[@href="' + club_source["url"] + '"]'):
            link = etree.SubElement(etree.SubElement(sources_list, "li"), "a", href=club_source["url"], rel="noopener noreferrer", target="_blank")
            link.text = club_source["nome"]
            match_path.write_text(html.tostring(match_doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")
        site.sync_surfaces(ARTICLES, f"/notizie/{slug}.html", VERSION, update_manifest=False)
        state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                      "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                      "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(ARTICLES),
                      "last_update": f"segnalazioni-v{VERSION}", "date": published.date().isoformat(),
                      "release_date": published.date().isoformat(), "updated_at": published.isoformat(timespec="seconds"),
                      "status": "ready"})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": index, "slug": slug, "published": published.isoformat()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
