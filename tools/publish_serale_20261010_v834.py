#!/usr/bin/env python3
"""Lotto serale del 10 ottobre 2026: sviluppi verificati, non indiscrezioni."""
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

VERSION = 834
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "inter": ROOT.parent / "generated_images/exec-d6f9912f-d221-404a-a9c7-a20500ca5b34.png",
    "napoli": ROOT.parent / "generated_images/exec-c5f1e698-ad42-408f-8eb6-07a4c23fb42c.png",
    "meteo": ROOT.parent / "generated_images/exec-e8ecada1-fcb6-4eb5-bb8a-27b41b27a68b.png",
    "f1": ROOT.parent / "generated_images/exec-a5aa0199-274f-4d84-94a8-54f8024968df.png",
    "lombardia": ROOT.parent / "generated_images/exec-b9aa5018-d2e6-4305-8501-69b1881540d1.png",
}

ARTICLES = [
    {
        "slug": "inter-parma-3-0-sucic-calhanoglu-thuram-10-10-2026",
        "titolo": "Inter-Parma 3-0: Sucic, Calhanoglu e Thuram decidono a San Siro",
        "sommario": "Tre gol nel primo tempo e quinta vittoria in sei gare per i nerazzurri. La squadra di Chivu sale provvisoriamente a 16 punti, in attesa delle altre partite della giornata.",
        "categoria": "Sport", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Inter-Parma 3-0", "16 punti"],
        "dati_chiave": [{"valore": "3-0", "etichetta": "risultato finale"}, {"valore": "13′, 18′, 31′", "etichetta": "minuti dei gol"}, {"valore": "16", "etichetta": "punti dell’Inter dopo sei gare"}],
        "paragrafi": [
            "L'Inter ha battuto il Parma 3-0 a San Siro nella sesta giornata di Serie A, giocata sabato 10 ottobre con calcio d'inizio alle 18. Il match center ufficiale del club conferma il risultato finale: tutti e tre i gol sono arrivati nel primo tempo.",
            "Petar Sucic ha aperto le marcature al 13' dopo un recupero palla in area. Hakan Calhanoglu ha trasformato un rigore al 18', assegnato dopo un intervento di Diego Carlos su Pio Esposito. Marcus Thuram ha poi chiuso il conto al 31' con un diagonale al termine di un'azione in campo aperto.",
            "Nella ripresa il Parma ha cercato di reagire, ma il punteggio non è più cambiato. Cristian Chivu ha inserito anche Lautaro Martinez e Bonny nell'ultima mezz'ora; Djed Spence ha fatto il suo esordio ufficiale con la maglia dell'Inter, secondo la cronaca del club.",
            "La formazione iniziale nerazzurra comprendeva Martinez in porta, Pavard, Bisseck e Carlos Augusto in difesa, con Diouf, Sucic, Calhanoglu, Mkhitaryan e Dimarco a centrocampo, Esposito e Thuram in attacco. Per il Parma ha iniziato Corvi tra i pali.",
            "Con questa vittoria l'Inter raggiunge 16 punti e si porta al primo posto in via provvisoria. La posizione definitiva della sesta giornata dipenderà dagli altri incontri ancora da disputare: la classifica non va letta come già chiusa.",
            "Per chi aveva seguito gli avvisi di accesso e biglietteria di San Siro, questa è una notizia distinta: riguarda l'esito della gara e i marcatori ufficiali, non le indicazioni logistiche pubblicate prima del calcio d'inizio.",
        ],
        "fonti": [{"url": "https://www.inter.it/it/match_center/5374", "nome": "FC Internazionale — match center ufficiale Inter-Parma, risultato e cronaca del 10 ottobre."}],
        "image_source": "inter", "image_alt": "Illustrazione editoriale IA ultrarealistica di San Siro e di una celebrazione calcistica; non è una fotografia della partita.",
        "image_prompt": "San Siro serale dopo Inter-Parma, illustrazione editoriale fotorealistica; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "napoli-frosinone-convocati-allegri-20-45-10-10-2026",
        "titolo": "Napoli-Frosinone stasera alle 20:45: i convocati di Allegri",
        "sommario": "Il club pubblica la lista per la gara al Maradona. Presenti De Bruyne, Hojlund, McTominay e Politano; convocazione e formazione titolare non sono la stessa cosa.",
        "categoria": "Sport", "luogo": "Napoli", "formato": "flash",
        "parole_chiave_titolo": ["Napoli-Frosinone", "convocati"],
        "dati_chiave": [{"valore": "20:45", "etichetta": "inizio, ora italiana"}, {"valore": "21", "etichetta": "convocati dal Napoli"}, {"valore": "Maradona", "etichetta": "stadio della partita"}],
        "paragrafi": [
            "Il Napoli ha comunicato i convocati di Massimiliano Allegri per la partita di stasera, sabato 10 ottobre, contro il Frosinone. Il calcio d'inizio è fissato alle 20:45, ora italiana, allo stadio Diego Armando Maradona.",
            "Nella lista ufficiale compaiono i portieri Contini, Meret e Milinkovic-Savic; tra i difensori Badiashile, Beukema, Di Lorenzo, Marianucci, Rafa Marin, Rrahmani e Spinazzola. Sono convocati anche De Bruyne, Gilmour, Lobotka e McTominay.",
            "Completano l'elenco Giovane, Hojlund, Lang, Lucca, Milton Pereyra, Neres e Politano. La presenza tra i convocati indica la disponibilità per la gara, non l'impiego dal primo minuto: non è corretto presentare questa lista come formazione ufficiale.",
            "Il dato nuovo rispetto alle precedenti informazioni sul calendario è proprio la selezione resa nota dal club nel giorno della partita. Le scelte dell'undici iniziale e gli eventuali cambiamenti dell'ultimo momento vanno verificati sui canali della società o della Lega vicino al fischio d'inizio.",
            "Per chi si reca allo stadio, l'orario comunicato dal Napoli è quello italiano. Le indicazioni su biglietti, accessi e trasporti vanno controllate sui canali degli organizzatori: l'elenco dei convocati non annuncia variazioni ai servizi o alla viabilità.",
            "Il risultato non è disponibile al momento di questo aggiornamento prepartita. Non vengono quindi anticipati punteggi, formazioni non confermate o emittenti televisive senza una comunicazione verificata dei titolari dei diritti.",
        ],
        "fonti": [{"url": "https://sscnapoli.it/sscn-i-convocati-per-il-match-contro-il-frosinone/", "nome": "SSC Napoli — convocati e orario della partita contro il Frosinone, 10 ottobre."}],
        "image_source": "napoli", "image_alt": "Illustrazione editoriale IA ultrarealistica dell'esterno dello stadio Maradona di Napoli al tramonto; non documenta l'arrivo dei tifosi.",
        "image_prompt": "Stadio Diego Armando Maradona in serata prima di Napoli-Frosinone; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "campania-allerta-gialla-tutta-regione-11-ottobre-2026",
        "titolo": "Campania, allerta gialla in tutta la regione fino alle 15 di domenica",
        "sommario": "L'avviso regionale proroga il rischio idrogeologico all'11 ottobre. L'arancione è terminata alle 15 di sabato nelle zone 1 e 3, ma i terreni saturi richiedono attenzione.",
        "categoria": "Meteo", "luogo": "Campania", "formato": "flash",
        "parole_chiave_titolo": ["Campania", "allerta gialla"],
        "dati_chiave": [{"valore": "15:00", "etichetta": "scadenza di domenica 11"}, {"valore": "tutta", "etichetta": "la Campania in giallo"}, {"valore": "72 ore", "etichetta": "piogge pregresse considerate"}],
        "paragrafi": [
            "La Protezione civile della Campania ha prorogato l'allerta meteo fino alle 15 di domenica 11 ottobre. Dalle 15 di sabato 10 il livello è giallo su tutto il territorio regionale: l'arancione che interessava la zona di Napoli e quella sorrentino-amalfitana è cessata a quell'ora.",
            "È un aggiornamento sostanziale rispetto all'avviso precedente, non una nuova allerta arancione per la notte. Il passaggio al giallo segnala un'attenuazione prevista dei fenomeni dalla serata, ma non elimina il rischio di effetti delle piogge già cadute.",
            "La Regione richiama le precipitazioni consistenti delle ultime 72 ore e la saturazione dei terreni. Restano possibili allagamenti, ruscellamenti sulle strade, innalzamenti dei corsi d'acqua, caduta massi e frane nelle aree fragili, anche dove la pioggia si attenua.",
            "L'avviso riguarda in modo particolare il rischio idrogeologico. I Comuni sono invitati a mantenere attivi i centri operativi e ad adottare le misure previste dai rispettivi piani di protezione civile, con attenzione anche alle zone attraversate da incendi nei mesi precedenti.",
            "Chi deve spostarsi questa sera o domenica mattina dovrebbe verificare gli avvisi del proprio Comune e dei gestori della strada, evitare sottopassi allagati e non sostare vicino a corsi d'acqua durante i rovesci. Le eventuali chiusure locali vanno confermate dai singoli enti competenti.",
            "La scadenza indicata è domenica alle 15, salvo successivi aggiornamenti ufficiali. Non è una previsione uniforme di pioggia intensa in ogni comune: il livello di criticità descrive il rischio complessivo valutato per il territorio.",
        ],
        "fonti": [{"url": "https://www.regione.campania.it/comunicazione/area-stampa/comunicati/10102026-comunicato-n-638-protezione-civile-campania-prosegue-l-allerta-meteo", "nome": "Protezione civile della Regione Campania — comunicato 638 del 10 ottobre e orari dell'allerta."}],
        "image_source": "meteo", "image_alt": "Illustrazione editoriale IA ultrarealistica di pioggia su una strada di Napoli; non rappresenta un episodio specifico né una mappa di allerta.",
        "image_prompt": "Pioggia su Napoli come immagine editoriale illustrativa dell'allerta; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "f1-singapore-pole-verstappen-leclerc-antonelli-10-10-2026",
        "titolo": "F1 Singapore, pole di Verstappen: Leclerc secondo a 54 millesimi",
        "sommario": "Hamilton è terzo, Antonelli quarto nelle qualifiche del GP. La gara di domenica parte alle 14 italiane; Russell deve scontare una penalità in griglia.",
        "categoria": "Sport", "luogo": "Singapore", "formato": "flash",
        "parole_chiave_titolo": ["pole Verstappen", "Leclerc secondo"],
        "dati_chiave": [{"valore": "1:31.373", "etichetta": "tempo della pole"}, {"valore": "+0.054", "etichetta": "distacco di Leclerc"}, {"valore": "14:00", "etichetta": "gara domenica, ora italiana"}],
        "paragrafi": [
            "Max Verstappen ha conquistato la pole position del Gran Premio di Singapore 2026 in 1'31\"373. Charles Leclerc ha portato la Ferrari al secondo posto in qualifica, a soli 54 millesimi, mentre Lewis Hamilton ha chiuso terzo, secondo il resoconto ufficiale della Formula 1.",
            "Kimi Antonelli partirà dalla quarta casella maturata in qualifica, davanti a Lando Norris. George Russell ha ottenuto inizialmente il sesto tempo, ma la Formula 1 segnala una penalità in griglia da applicare: il suo piazzamento in classifica delle qualifiche non coincide necessariamente con quello finale di partenza.",
            "Verstappen aveva già fatto segnare il giro decisivo nel primo tentativo della Q3. Leclerc ha migliorato nell'ultimo passaggio senza riuscire a scavalcarlo; Hamilton, che era stato il più veloce nelle prime due fasi, non ha migliorato abbastanza nella fase conclusiva.",
            "La gara è in programma domenica 11 ottobre alle 20 locali a Marina Bay. Singapore è sei ore avanti rispetto all'Italia in questo periodo dell'anno: l'orario corrisponde alle 14:00 italiane, salvo eventuali variazioni comunicate dagli organizzatori.",
            "Questo risultato riguarda la griglia della gara lunga ed è distinto dalla Sprint disputata in precedenza nello stesso fine settimana. Le condizioni meteo e gli eventuali provvedimenti sportivi possono incidere sullo svolgimento del GP, non cancellano il tempo registrato nelle qualifiche.",
            "Per la diretta televisiva è prudente consultare il palinsesto aggiornato del proprio operatore: la fonte ufficiale delle qualifiche qui consultata non certifica canale e modalità di visione per l'Italia, quindi non ne attribuiamo uno senza riscontro.",
        ],
        "fonti": [{"url": "https://www.formula1.com/en/latest/article/verstappen-beats-leclerc-to-pole-position-for-the-singapore-gp.7yum1V3S9aSTyj3Zzzs0Y9", "nome": "Formula 1 — resoconto ufficiale delle qualifiche e orario locale della gara."}],
        "image_source": "f1", "image_alt": "Illustrazione editoriale IA ultrarealistica di monoposto sul circuito cittadino di Singapore; non è una fotografia delle qualifiche.",
        "image_prompt": "Circuito di Marina Bay e monoposto dopo le qualifiche, illustrazione editoriale; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "paul-seixas-vince-lombardia-ciccone-terzo-10-10-2026",
        "titolo": "Il Lombardia, vince Paul Seixas: Ciccone terzo a Como",
        "sommario": "Il francese ventenne conquista la classica dopo 239 chilometri, con 48 secondi su Enric Mas. Giulio Ciccone chiude a 1'05\"; è il più giovane vincitore della corsa.",
        "categoria": "Sport", "luogo": "Como", "formato": "flash",
        "parole_chiave_titolo": ["Paul Seixas", "Ciccone terzo"],
        "dati_chiave": [{"valore": "239 km", "etichetta": "percorso della corsa"}, {"valore": "+48″", "etichetta": "Enric Mas secondo"}, {"valore": "+1′05″", "etichetta": "Ciccone terzo"}],
        "paragrafi": [
            "Paul Seixas ha vinto il 120° Il Lombardia, disputato sabato 10 ottobre con arrivo a Como. Il francese della Decathlon CMA CGM ha percorso 239 chilometri in 5 ore, 49 minuti e 28 secondi, secondo l'ordine d'arrivo pubblicato dagli organizzatori.",
            "Enric Mas è arrivato secondo a 48 secondi. Giulio Ciccone ha chiuso al terzo posto a 1 minuto e 5 secondi, miglior italiano nella parte alta della classifica; Remco Evenepoel è quarto a 1 minuto e 20 secondi.",
            "La selezione decisiva è arrivata sulle salite finali. Seixas ha aumentato il ritmo sul Civiglio, staccando gli altri favoriti, e ha conservato il margine fino al traguardo. Mas ha superato Ciccone nella fase finale sul San Fermo della Battaglia.",
            "A vent'anni Seixas diventa il più giovane vincitore della storia della classica secondo l'organizzazione. La vittoria interrompe la serie di cinque successi consecutivi di Tadej Pogacar nella corsa, un risultato che dà ulteriore peso al cambio di protagonista.",
            "Per gli appassionati italiani il podio di Ciccone è il dato immediato, ma i distacchi aiutano a leggere la corsa: non si è trattato di uno sprint di gruppo, bensì di un successo in solitaria maturato prima dell'arrivo.",
            "Si tratta di un risultato definitivo, diverso dalle anticipazioni su percorso, orari e favoriti della mattinata. Le classifiche complete e gli eventuali provvedimenti di gara restano consultabili sul sito ufficiale della manifestazione.",
        ],
        "fonti": [{"url": "https://www.ilombardia.it/news/paul-seixas-vince-il-lombardia-2026/", "nome": "Il Lombardia — comunicato ufficiale e ordine d'arrivo del 10 ottobre."}],
        "image_source": "lombardia", "image_likeness": "public-figure",
        "image_alt": "Ritratto sintetico ultrarealistico e illustrativo del ciclista Paul Seixas al traguardo di Como; non è una fotografia della gara.",
        "image_prompt": "Paul Seixas in una scena editoriale illustrativa a Como dopo la vittoria; logo CurioMondo circolare applicato in post-produzione.",
    },
]


def correct_visible_date(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    label = site._italian_date(published.isoformat(timespec="seconds"))
    for node in doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]'):
        node.text = f"{label} · {next(a['luogo'] for a in ARTICLES if a['slug'] == slug)} · "
    for node in doc.xpath('//section[contains(@class,"art-sources")]//small/br[1]'):
        if node.tail and "Ultimo aggiornamento editoriale:" in node.tail:
            node.tail = f"Testo originale CurioMondo. Ultimo aggiornamento editoriale: {label}."
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def main() -> None:
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    for phrase in (
        "Ogni risultato diventa più chiaro quando ne conosciamo la fonte.",
        "Una sera informata comincia dai fatti già confermati.",
        "La prudenza aiuta a leggere anche un cielo che si apre.",
        "Un dettaglio verificato può cambiare la storia di una gara.",
        "Arrivare al traguardo è anche saper raccontare il percorso.",
    ):
        if phrase not in phrases:
            phrases.append(phrase)
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    base_time = datetime(2026, 10, 10, 20, 20, 0, tzinfo=ZoneInfo("Europe/Rome"))
    offsets = (0, 8, 20, 35, 51)
    images = []
    for article, minutes in zip(ARTICLES, offsets):
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
                  "last_update": f"serale-v{VERSION}", "date": base_time.date().isoformat(),
                  "release_date": base_time.date().isoformat(), "updated_at": base_time.isoformat(timespec="seconds"),
                  "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base_time.isoformat(),
                      "articles": [a["slug"] for a in ARTICLES]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
