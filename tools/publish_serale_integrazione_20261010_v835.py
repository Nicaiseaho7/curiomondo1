#!/usr/bin/env python3
"""Integrazione serale v835: cinque atti e risultati verificati."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

VERSION = 835
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "genoa": ROOT.parent / "generated_images/exec-f9d7766c-1a6a-4066-85db-74cb1dc6577c.png",
    "porto": ROOT.parent / "generated_images/exec-38336474-687e-4eda-baa1-18a6ea5f438a.png",
    "campania": ROOT.parent / "generated_images/exec-a5edb6fa-0316-480d-99ad-b3fcd9c47e41.png",
    "fisi": ROOT.parent / "generated_images/exec-508faf89-5193-446d-aacf-0ba5f92cef6d.png",
    "mclaren": ROOT.parent / "generated_images/exec-953c2ba2-5688-4d1f-bbf6-def29a4907be.png",
}

ARTICLES = [
    {
        "slug": "genoa-fiorentina-2-1-osmajic-messias-10-10-2026",
        "titolo": "Genoa-Fiorentina 2-1: prima vittoria rossoblù, viola battuti",
        "sommario": "Al Ferraris i padroni di casa sbloccano il campionato con Osmajic e Messias. Un'autorete di Vasquez riapre la gara, ma il Genoa conserva il vantaggio.",
        "categoria": "Sport", "luogo": "Genova", "formato": "flash",
        "parole_chiave_titolo": ["Genoa-Fiorentina 2-1", "prima vittoria"],
        "dati_chiave": [{"valore": "2-1", "etichetta": "risultato finale"}, {"valore": "3", "etichetta": "reti della partita"}, {"valore": "1ª", "etichetta": "vittoria del Genoa in campionato"}],
        "paragrafi": [
            "Il Genoa ha battuto la Fiorentina 2-1 al Luigi Ferraris sabato 10 ottobre, nella sesta giornata di Serie A. È la prima vittoria stagionale in campionato per la squadra di Daniele De Rossi, che arrivava alla partita con un solo punto nelle cinque gare precedenti.",
            "Milutin Osmajic ha sbloccato presto il risultato e Junior Messias ha firmato il raddoppio. I viola sono rientrati in partita grazie a un'autorete di Johan Vasquez, ma non hanno completato la rimonta prima del fischio finale.",
            "La cronaca ufficiale della Lega Serie A descrive il secondo gol del Genoa e lo svolgimento della gara. Il risultato e la sequenza dei marcatori trovano riscontro anche nel resoconto indipendente di Viola Nation.",
            "L'avvio è stato decisivo: i due gol rossoblù nei primi minuti hanno costretto la Fiorentina a inseguire. La squadra di Paolo Vanoli ha avuto più possesso nella ripresa, senza però ottenere il pareggio.",
            "Per il Genoa sono tre punti che cambiano la fotografia di una partenza difficile; per la Fiorentina è un'altra sconfitta in un avvio complicato. Le posizioni di classifica restano provvisorie finché non si completa il turno.",
            "La notizia riguarda il risultato definitivo, non il programma di Genoa-Fiorentina già pubblicato nei giorni scorsi. Eventuali sanzioni o rettifiche statistiche successive devono essere controllate attraverso la Lega.",
        ],
        "fonti": [{"url": "https://www.legaseriea.it/serie-a/match/c7dfbb8151954556bdb85503cc34d8d6/genoa-vs-fiorentina/commentary", "nome": "Lega Serie A — cronaca ufficiale Genoa-Fiorentina, 10 ottobre."}, {"url": "https://www.violanation.com/fiorentina-match-coverage/23027/genoa-2-1-fiorentina-match-report-serie-a-osmajic-messias-vasquez-goal", "nome": "Viola Nation — resoconto indipendente del risultato e dei marcatori."}],
        "image_source": "genoa", "image_alt": "Illustrazione editoriale IA ultrarealistica del Ferraris e di una celebrazione calcistica; non è una fotografia di Genoa-Fiorentina.",
        "image_prompt": "Stadio Luigi Ferraris e celebrazione calcistica simbolica, logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "santa-teresa-gallura-porto-acque-ordinanza-10-10-2026",
        "titolo": "Santa Teresa Gallura, precauzioni per le acque del porto turistico",
        "sommario": "L'ordinanza comunale invita a evitare il contatto diretto con l'acqua dopo analisi microbiologiche. Le normali attività senza immersioni possono proseguire; sono previsti nuovi controlli.",
        "categoria": "Cronaca", "luogo": "Santa Teresa Gallura", "formato": "flash",
        "parole_chiave_titolo": ["porto turistico", "ordinanza"],
        "dati_chiave": [{"valore": "55", "etichetta": "numero dell'ordinanza"}, {"valore": "6", "etichetta": "punti campionati"}, {"valore": "temporanee", "etichetta": "misure precauzionali"}],
        "paragrafi": [
            "Il Comune di Santa Teresa Gallura ha pubblicato il 10 ottobre l'ordinanza sindacale 55 sulle acque del porto turistico. Dopo sei campionamenti eseguiti il primo ottobre e risultati microbiologici elevati in diversi punti, invita cittadini, utenti e operatori a evitare il contatto diretto con l'acqua in attesa di ulteriori accertamenti.",
            "L'atto non dispone la chiusura del porto. Le attività ordinarie di ormeggio e assistenza che non richiedono immersioni o contatto con le acque possono proseguire; restano consentiti gli interventi urgenti indispensabili alla sicurezza delle persone e della navigazione.",
            "Agli operatori viene chiesto di rinviare temporaneamente, quando non urgenti o indifferibili, le operazioni che comportano immersioni, pulizia dei fondali o assistenza in acqua. I divieti di balneazione e pesca nell'area portuale erano già in vigore e restano distinti da queste nuove precauzioni.",
            "I risultati riportati dall'ordinanza variano tra i punti di prelievo. Alla banchina ITS, per esempio, sono indicati 5.700 UFC per 100 millilitri di Escherichia coli e 2.600 di enterococchi intestinali: il dato riguarda quel campione, non automaticamente tutte le spiagge o il mare circostante.",
            "Il Comune ha richiesto valutazioni all'ASL competente e ad ARPAS e ulteriori prelievi alla società che gestisce il porto. Le misure saranno rivalutate alla luce dei nuovi risultati; un'eventuale modifica o revoca richiederà un altro provvedimento espresso.",
            "Chi frequenta il porto dovrebbe seguire gli avvisi affissi agli accessi ed evitare contatti non necessari con l'acqua. Non sono riportate nell'atto diagnosi di malattie né una contaminazione estesa ad altri tratti di costa.",
        ],
        "fonti": [{"url": "https://www.comune.santateresagallura.ss.it/index.php/it/news/ordinanza-sindacale-n-55-del-10-ottobre-2026?type=3", "nome": "Comune di Santa Teresa Gallura — ordinanza sindacale 55 del 10 ottobre 2026."}],
        "image_source": "porto", "image_alt": "Illustrazione editoriale IA ultrarealistica del porto turistico sardo; non documenta le acque campionate né i risultati delle analisi.",
        "image_prompt": "Porto turistico di Santa Teresa Gallura, immagine editoriale neutrale, logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "campania-sostegno-psicologico-minori-gratuito-10-10-2026",
        "titolo": "Campania, rilanciato il sostegno psicologico gratuito per i minori",
        "sommario": "La Regione conferma il percorso per bambini e adolescenti in svantaggio sociale, su indicazione del pediatra o del medico. L'accesso non è automatico per tutte le famiglie.",
        "categoria": "Italia", "luogo": "Campania", "formato": "flash",
        "parole_chiave_titolo": ["sostegno psicologico", "minori"],
        "dati_chiave": [{"valore": "3–17", "etichetta": "anni dei destinatari"}, {"valore": "2.351", "etichetta": "minori assistiti nel primo anno"}, {"valore": "15.200", "etichetta": "sedute nel primo anno"}],
        "paragrafi": [
            "La Regione Campania ha annunciato il 10 ottobre il rafforzamento del percorso gratuito di sostegno psicologico per bambini e adolescenti dai tre anni fino ai 18 non compiuti che vivono situazioni di svantaggio sociale o rischiano l'esclusione.",
            "L'iniziativa esiste già nella legge regionale 5 del 2021 e viene rilanciata con la collaborazione dell'Ordine degli Psicologi della Campania. Non è un nuovo bonus nazionale e il comunicato non indica che qualsiasi famiglia possa attivare autonomamente sedute gratuite.",
            "Il percorso parte dall'indicazione del pediatra di libera scelta o del medico di medicina generale, che valuta la necessità del supporto. La famiglia può poi scegliere uno psicologo tra quelli presenti nell'elenco predisposto dall'Ordine; i costi degli incontri sono coperti dalle risorse regionali.",
            "Secondo i dati forniti dalla Regione, nel primo anno sono stati coinvolti 1.029 psicologi, assistiti 2.351 minori ed effettuate 15.200 sedute. Questi numeri descrivono l'attuazione precedente, non i posti o i fondi già stanziati per il nuovo ciclo.",
            "Per le famiglie potenzialmente interessate, il primo passo pratico è parlarne con il pediatra o il medico di riferimento e verificare le indicazioni operative della Regione e dell'Ordine. Il comunicato non specifica qui una data unica di apertura di domande online o una graduatoria da compilare.",
            "L'annuncio riguarda un servizio sociale e di prevenzione, non sostituisce una valutazione sanitaria individuale. In presenza di un'urgenza per un minore vanno contattati i servizi sanitari competenti senza attendere i passaggi amministrativi della misura.",
        ],
        "fonti": [{"url": "https://www.regione.campania.it/comunicazione/area-stampa/comunicati/10102026-comunicato-n-637-regione-campania-rilancia-rafforza-sostegno-psicologico-gratuito-bambini-adolescenti", "nome": "Regione Campania — comunicato 637 del 10 ottobre, requisiti e dati del primo anno."}],
        "image_source": "campania", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica e simbolica di un colloquio tra una famiglia e una professionista; non ritrae beneficiari del servizio.",
        "image_prompt": "Colloquio simbolico di sostegno familiare in ambiente professionale, senza attribuire condizioni cliniche a persone reali; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "fisi-elezione-presidente-quorum-non-raggiunto-10-10-2026",
        "titolo": "FISI, nessun presidente eletto nell'assemblea di Verona",
        "sommario": "Flavio Roda ottiene il 57,88% dei voti validi, ma non raggiunge il quorum richiesto. L'assemblea straordinaria approva invece le modifiche allo statuto federale.",
        "categoria": "Sport", "luogo": "Verona", "formato": "flash",
        "parole_chiave_titolo": ["FISI", "quorum non raggiunto"],
        "dati_chiave": [{"valore": "57,88%", "etichetta": "voti per Roda"}, {"valore": "nessuno", "etichetta": "presidente eletto"}, {"valore": "sì", "etichetta": "modifiche statutarie approvate"}],
        "paragrafi": [
            "L'assemblea elettiva della Federazione italiana sport invernali tenuta a Verona il 10 ottobre non ha eletto un presidente. Lo scrutinio pubblicato dalla FISI indica Flavio Roda al 57,88% dei voti validi, ma segnala espressamente che il quorum necessario non è stato raggiunto.",
            "Roda ha raccolto 48.015 voti; Antonio Rosario Maria Noris 29.838, pari al 35,97%; Roberto Bortoluzzi 2.087, pari al 2,52%. La percentuale più alta non basta dunque a dichiarare eletto il candidato in questa votazione.",
            "Alla chiusura degli accreditamenti risultavano presenti 971 delegati su 2.475 per l'assemblea ordinaria, con 83.160 voti accreditati. La FISI precisa che la prima convocazione non aveva raggiunto il quorum costitutivo, mentre la seconda convocazione è stata validamente costituita.",
            "Un altro esito è invece definitivo: alle 14 l'assemblea straordinaria ha approvato modifiche allo statuto federale. Il resoconto sintetico non riporta il testo integrale degli articoli modificati, quindi non è possibile attribuire a questa decisione nuove regole operative specifiche senza l'atto pubblicato.",
            "Il mancato quorum nell'elezione rinvia la scelta del vertice secondo le procedure federali, ma la comunicazione consultata non indica ancora una data per un nuovo voto. Non è una vittoria elettorale né un commissariamento annunciato in questo documento.",
            "Per atleti, società e appassionati degli sport invernali, il dato da seguire è la prossima comunicazione ufficiale della federazione sui passaggi successivi, mentre l'attività agonistica segue i calendari pubblicati separatamente.",
        ],
        "fonti": [{"url": "https://www.fisi.org/esito-assemblea-federale-ordinaria-elettiva-verona-10-ottobre-2026/", "nome": "FISI — scrutinio dell'assemblea di Verona e decisione statutaria, 10 ottobre."}],
        "image_source": "fisi", "image_alt": "Illustrazione editoriale IA ultrarealistica di una sala assembleare sportiva a Verona; non ritrae la votazione FISI reale.",
        "image_prompt": "Sala assembleare di una federazione degli sport invernali, scena simbolica senza atti leggibili; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "mclaren-norris-piastri-nessuna-sanzione-sprint-singapore-2026",
        "titolo": "F1, Norris e Piastri senza sanzioni dopo il contatto nella Sprint",
        "sommario": "I commissari non attribuiscono la responsabilità prevalente a nessuno dei due piloti McLaren. Il verdetto chiude l'indagine sul contatto dell'ultimo giro a Singapore.",
        "categoria": "Sport", "luogo": "Singapore", "formato": "flash",
        "parole_chiave_titolo": ["Norris e Piastri", "nessuna sanzione"],
        "dati_chiave": [{"valore": "0", "etichetta": "sanzioni per il contatto"}, {"valore": "curva 5", "etichetta": "punto dell'incidente"}, {"valore": "8°", "etichetta": "Norris al traguardo"}],
        "paragrafi": [
            "Lando Norris e Oscar Piastri non ricevono sanzioni per il contatto fra le due McLaren nell'ultimo giro della Sprint del Gran Premio di Singapore. Dopo aver ascoltato i piloti, i commissari hanno deciso di non prendere ulteriori provvedimenti, secondo il resoconto ufficiale della Formula 1.",
            "L'episodio è avvenuto alla curva 5 mentre i compagni di squadra inseguivano la Ferrari di Charles Leclerc per il terzo posto. Norris ha tentato il sorpasso all'interno, le monoposto si sono toccate e sono finite in testacoda.",
            "Piastri ha urtato le barriere e si è ritirato; Norris è riuscito a proseguire e a terminare ottavo. Il verdetto sportivo non modifica questi fatti della gara, ma chiarisce che non viene attribuita una penalità aggiuntiva a uno dei due.",
            "I commissari hanno valutato che entrambi abbiano contribuito al contatto e che nessuno fosse interamente o prevalentemente responsabile. Si tratta di un giudizio su questa manovra specifica, non di una regola generale per altri episodi di gara.",
            "La decisione è distinta dal risultato della Sprint e dalle qualifiche della gara lunga, trattati separatamente. Le vetture e i piloti sono poi tornati in pista per la sessione che ha assegnato la pole a Max Verstappen.",
            "La corsa principale è prevista domenica 11 ottobre alle 14 italiane. Questo provvedimento non introduce modifiche alla griglia di partenza; altre penalità, come quella già annunciata per George Russell, hanno una causa diversa.",
        ],
        "fonti": [{"url": "https://www.formula1.com/en/latest/article/stewards-reach-verdict-after-mclaren-intra-team-collision-in-singapore-gp-sprint.2LEoxWh3e7IEg674uCdLQ5", "nome": "Formula 1 — decisione dei commissari dopo il contatto McLaren nella Sprint, 10 ottobre."}],
        "image_source": "mclaren", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di due monoposto arancioni a Singapore; non ricostruisce il contatto tra Norris e Piastri.",
        "image_prompt": "Due monoposto arancioni separate sul circuito di Singapore, senza rappresentare l'incidente reale; logo CurioMondo circolare applicato in post-produzione.",
    },
]


def correct_visible_date(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    label = site._italian_date(published.isoformat(timespec="seconds"))
    place = next(a["luogo"] for a in ARTICLES if a["slug"] == slug)
    for node in doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]'):
        node.text = f"{label} · {place} · "
    for node in doc.xpath('//section[contains(@class,"art-sources")]//small/br[1]'):
        if node.tail and "Ultimo aggiornamento editoriale:" in node.tail:
            node.tail = f"Testo originale CurioMondo. Ultimo aggiornamento editoriale: {label}."
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def main() -> None:
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    for phrase in (
        "Una vittoria è ancora più preziosa dopo un inizio difficile.",
        "La sicurezza comincia dalle indicazioni più precise.",
        "Chiedere sostegno è un gesto di cura verso chi cresce.",
        "Una votazione si capisce solo conoscendone le regole.",
        "Un verdetto chiaro distingue la gara dalle interpretazioni.",
    ):
        if phrase not in phrases:
            phrases.append(phrase)
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    base_time = datetime(2026, 10, 10, 20, 55, 0, tzinfo=ZoneInfo("Europe/Rome"))
    images = []
    for article, minutes in zip(ARTICLES, (0, 8, 20, 35, 51)):
        image = base.make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base_time - timedelta(minutes=minutes)
        base.set_published(slug, published)
        correct_visible_date(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["items"] = images + registry.get("items", [])
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(ARTICLES, f"/notizie/{ARTICLES[0]['slug']}.html", VERSION, update_manifest=False)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                  "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                  "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
                  "last_update": f"serale-integrazione-v{VERSION}", "date": base_time.date().isoformat(),
                  "release_date": base_time.date().isoformat(), "updated_at": base_time.isoformat(timespec="seconds"),
                  "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in ARTICLES]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
