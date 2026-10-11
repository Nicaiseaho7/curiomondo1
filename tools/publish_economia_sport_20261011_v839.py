#!/usr/bin/env python3
"""Lotto economia e sport 11 ottobre, con un solo sync finale."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_finale_20261010_v836 as prior
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

VERSION = 839
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "startech": ROOT.parent / "generated_images/exec-929dc029-14a3-462a-9bf5-98939bfc2a61.png",
    "bot": ROOT.parent / "generated_images/exec-9d64c888-c436-4da5-b5a7-996d17fdea0e.png",
    "motogp": ROOT.parent / "generated_images/exec-e2d0c88d-8f92-4a83-81a3-65d701eb3f6e.png",
}

ARTICLES = [
    {
        "slug": "startech-trieste-urso-sindacati-rilancio-lavoro-10-ottobre-2026",
        "titolo": "StarTech Trieste, sostegno al reddito in scadenza il 31 ottobre",
        "sommario": "Urso e Fedriga chiedono una soluzione per lo stabilimento. La Regione avverte che l'ammortizzatore sociale scade a fine mese; non è stato annunciato un nuovo accordo.",
        "categoria": "Economia", "luogo": "Trieste", "formato": "flash",
        "parole_chiave_titolo": ["StarTech Trieste", "31 ottobre"],
        "dati_chiave": [
            {"valore": "10 ottobre", "etichetta": "incontro con i sindacati"},
            {"valore": "2025", "etichetta": "cessione annunciata"},
            {"valore": "in valutazione", "etichetta": "tutele per il sito"},
        ],
        "paragrafi": [
            "Il ministro delle Imprese Adolfo Urso ha incontrato sabato 10 ottobre a Trieste i sindacati di StarTech per discutere del futuro dello stabilimento e dei posti di lavoro. Il confronto si è svolto in Prefettura alla presenza del presidente del Friuli Venezia Giulia, Massimiliano Fedriga. Non è stato annunciato un nuovo accordo industriale.",
            "Secondo il Ministero delle Imprese e del Made in Italy, il progetto di cessione comunicato dall'azienda nel settembre 2025 non è stato attuato. Il piano avrebbe dovuto portare nuove attività nella fotonica, nello spazio e nella difesa nel sito che sviluppa e produce componenti e apparecchiature elettroniche per le telecomunicazioni.",
            "Urso ha chiesto all'azienda trasparenza e gli elementi che, a suo dire, non sono stati ancora forniti. Il ministro considera l'amministrazione straordinaria la strada per trovare un soggetto industriale capace di sostenere lo stabilimento: si tratta della sua posizione espressa durante l'incontro, non dell'annuncio che la procedura sia già stata avviata.",
            "La Regione avverte che l'ammortizzatore sociale attualmente in vigore scade il 31 ottobre: entro quella data, secondo Fedriga e l'assessore al Lavoro Alessia Rosolen, il quadro deve chiarirsi anche per garantire continuità al sostegno al reddito. È una scadenza per i lavoratori, non una data già fissata per l'apertura dell'amministrazione straordinaria o per una nuova cessione.",
        ],
        "fonti": [
            {"url": "https://www.mimit.gov.it/it/notizie-stampa/startech-urso-incontra-i-sindacati-lavoriamo-per-rilancio-sito-trieste-e-tutela-occupazione-ma-tempo-e-scaduto-azienda-sia-responsabile", "nome": "Ministero delle Imprese e del Made in Italy — incontro con i sindacati StarTech, 10 ottobre 2026."},
            {"url": "https://www.regione.fvg.it/rafvg/giunta/dettaglio.act?ass=C06&dir=/rafvg/cms/RAFVG/Giunta/Rosolen/comunicati/&id=151391", "nome": "Regione Friuli Venezia Giulia — comunicato Fedriga-Rosolen del 10 ottobre e scadenza del sostegno al reddito."},
        ],
        "image_source": "startech",
        "image_alt": "Illustrazione IA del ministro Adolfo Urso in un ritratto istituzionale ambientato a Trieste; non ritrae l'incontro con i sindacati.",
        "image_prompt": "Ritratto editoriale sintetico di Adolfo Urso presso edificio istituzionale a Trieste; logo CurioMondo circolare applicato in compositing.",
    },
    {
        "slug": "bot-12-mesi-asta-9-ottobre-2026-rendimento-3-175",
        "titolo": "BOT annuale, rendimento lordo al 3,175% nell'asta del 9 ottobre",
        "sommario": "Collocati 8 miliardi di euro di titoli con scadenza 14 ottobre 2027. Il dato è lordo, riferito all'asta e non coincide con il rendimento netto di ogni risparmiatore.",
        "categoria": "Economia", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["BOT annuale", "3,175%"],
        "dati_chiave": [
            {"valore": "3,175%", "etichetta": "rendimento lordo d'asta"},
            {"valore": "8 miliardi", "etichetta": "importo collocato"},
            {"valore": "14 ottobre 2027", "etichetta": "scadenza del titolo"},
        ],
        "paragrafi": [
            "Il BOT a dodici mesi collocato venerdì 9 ottobre ha registrato un rendimento medio ponderato semplice lordo del 3,175%. Il Tesoro ha assegnato 8 miliardi di euro di titoli, con scadenza il 14 ottobre 2027, secondo i risultati dell'asta pubblicati dalla Banca d'Italia.",
            "Il rendimento è salito di circa 21 punti base rispetto all'asta annuale del 9 settembre. Il confronto riguarda due collocamenti diversi, non una promessa che il tasso resti invariato per chi comprerà il titolo successivamente sul mercato.",
            "Per il risparmiatore, 3,175% non equivale al guadagno netto accreditato sul conto: il dato d'asta è lordo. Il risultato individuale dipende dal prezzo effettivo di acquisto, dalla tassazione, dalle commissioni dell'intermediario e dall'eventuale vendita prima della scadenza. Non va moltiplicato automaticamente per la somma investita come se fosse un interesse netto garantito.",
            "L'asta del 9 ottobre è già conclusa. Chi valuta ora l'acquisto deve quindi verificare il prezzo offerto dal proprio intermediario e i relativi costi, anziché usare il rendimento medio dell'asta come quotazione corrente. I BOT non pagano cedole periodiche: il rendimento deriva dalla differenza tra prezzo pagato e rimborso a scadenza, se il titolo viene mantenuto fino ad allora.",
        ],
        "fonti": [
            {"url": "https://www.bancaditalia.it/media/comunicati/documenti/2026-02/cs-aste-BOT-20261009.pdf", "nome": "Banca d'Italia — risultati ufficiali dell'asta BOT del 9 ottobre 2026."},
            {"url": "https://www.teleborsa.it/News/2026/10/09/asta-bot-12-mesi-collocati-8-miliardi-con-rendimento-che-balza-al-3-175percent-95.html", "nome": "Teleborsa — resoconto indipendente su importo, rendimento e confronto con settembre."},
        ],
        "image_source": "bot",
        "image_alt": "Illustrazione IA concettuale di titoli di Stato, monete e calcolatrice su una scrivania; non riproduce un documento reale.",
        "image_prompt": "Titoli di Stato concettuali e risparmio, foto editoriale sintetica; logo circolare compositato.",
    },
    {
        "slug": "bezzecchi-vince-motogp-indonesia-aprilia-prime-quattro-11-ottobre-2026",
        "titolo": "MotoGP Indonesia, vince Bezzecchi: Aprilia occupa i primi quattro posti",
        "sommario": "A Mandalika l'italiano precede Fernández, Martín e Ogura. Martín torna in testa al Mondiale con 355 punti, due più di Marc Márquez, sesto al traguardo.",
        "categoria": "Sport", "luogo": "Mandalika, Indonesia", "formato": "flash",
        "parole_chiave_titolo": ["vince Bezzecchi", "primi quattro posti"],
        "dati_chiave": [
            {"valore": "1°–4°", "etichetta": "quattro Aprilia"},
            {"valore": "355", "etichetta": "punti Martín"},
            {"valore": "+2", "etichetta": "vantaggio su Márquez"},
        ],
        "paragrafi": [
            "Marco Bezzecchi ha vinto domenica 11 ottobre il Gran Premio d'Indonesia di MotoGP sul circuito di Mandalika. Il pilota Aprilia ha superato Raúl Fernández a nove giri dalla fine; Jorge Martín ha chiuso terzo e Ai Ogura quarto. Tutte e quattro le prime posizioni sono occupate da moto Aprilia, comprese le due del team Trackhouse.",
            "Fernández, partito dalla pole position, era rimasto davanti nella prima parte della gara nonostante due dita fratturate dopo una caduta di sabato, condizione da lui raccontata al termine della corsa. Bezzecchi ha poi preso la testa e ottenuto la vittoria, che secondo il resoconto di Reuters è la numero 300 per un pilota italiano nella classe regina.",
            "La classifica piloti cambia ancora dopo la Sprint di sabato, vinta da Marc Márquez: Martín sale a 355 punti e torna al comando con due lunghezze di vantaggio sullo spagnolo, sesto nel Gran Premio. Il podio e la quarta posizione di Ogura segnano anche il primo arrivo dell'Aprilia nelle prime quattro posizioni di una gara MotoGP.",
            "La gara di oggi è conclusa: non va confusa con la Sprint disputata ieri. La distanza fra i primi due in campionato è di soli due punti secondo la classifica riportata dopo il traguardo, ma i punti delle prossime gare non sono ancora assegnati.",
        ],
        "fonti": [
            {"url": "https://stats.motogp.com/en/gp-results", "nome": "MotoGP Stats — risultati ufficiali del Gran Premio d'Indonesia dell'11 ottobre 2026."},
            {"url": "https://www.reuters.com/sports/bezzecchi-pips-fernandez-win-indonesian-gp-martin-retakes-championship-lead-2026-10-11/", "nome": "Reuters — cronaca della gara a Mandalika e classifica dopo il Gran Premio."},
        ],
        "image_source": "motogp",
        "image_alt": "Illustrazione IA di Marco Bezzecchi con la moto Aprilia numero 72 nell'ambientazione del circuito di Mandalika; non è una fotografia della gara.",
        "image_prompt": "Marco Bezzecchi e Aprilia numero 72 a Mandalika, illustrazione editoriale ultrarealistica; logo circolare compositato.",
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
            "Puoi chiedere informazioni aggiornate prima di scegliere.",
            "Confronta le condizioni prima di impegnare i tuoi risparmi.",
            "Trova oggi un momento per fare ciò che ti piace.",
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
        site.sync_surfaces(ARTICLES, f"/notizie/{slug}.html", VERSION, update_manifest=False)
        state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                      "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                      "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(ARTICLES),
                      "last_update": f"economia-sport-v{VERSION}", "date": published.date().isoformat(),
                      "release_date": published.date().isoformat(), "updated_at": published.isoformat(timespec="seconds"),
                      "status": "ready"})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": index, "slug": slug, "published": published.isoformat()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
