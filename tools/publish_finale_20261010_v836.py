#!/usr/bin/env python3
"""Tre avvisi per la notte e domenica 11 ottobre, dopo il lotto v835."""
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

VERSION = 836
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "salento": ROOT.parent / "generated_images/exec-830fc6b7-e856-49e2-8918-26f3c129f588.png",
    "roma": ROOT.parent / "generated_images/exec-5778a0d7-1703-4a7c-b8e5-a40a9c5d280e.png",
    "como": ROOT.parent / "generated_images/exec-8ebe3af2-93ae-4bf8-811c-74b8d0446f22.png",
}

ARTICLES = [
    {
        "slug": "puglia-allerta-arancione-salento-domenica-11-ottobre-2026",
        "titolo": "Puglia, allerta arancione domenica nel Salento e nei bacini del Lato",
        "sommario": "Il bollettino nazionale del 10 ottobre conferma il livello arancione per temporali e rischio idrogeologico in due zone. Giallo sulle altre aree pugliesi indicate; la mappa distingue i territori.",
        "categoria": "Meteo", "luogo": "Puglia", "formato": "flash",
        "parole_chiave_titolo": ["allerta arancione", "Salento"],
        "dati_chiave": [{"valore": "11 ottobre", "etichetta": "giorno dell'allerta"}, {"valore": "2", "etichetta": "zone arancioni"}, {"valore": "14:17", "etichetta": "ora del bollettino nazionale"}],
        "paragrafi": [
            "Domenica 11 ottobre l'allerta arancione per temporali e rischio idrogeologico riguarda il Salento e i bacini del Lato e del Lenne in Puglia. Lo indica il bollettino nazionale della Protezione civile emesso sabato alle 14:17, che mantiene per le altre zone pugliesi elencate un livello giallo, non arancione.",
            "Il passaggio più utile per chi si sposta nella notte è la distinzione territoriale: il colore attribuito al Salento non si estende automaticamente a Bari o al Gargano. Il bollettino elenca fra le aree gialle il Tavoliere, il Gargano e Tremiti, il Basso Fortore e altri bacini della Puglia centrale e settentrionale.",
            "Il Comune di Bitonto riferisce che la Protezione civile regionale ha prorogato l'avviso in corso fino alle 6 di domenica, confermando arancione per Salento e Lato-Lenne e giallo nel resto della regione. Quell'orario riguarda la proroga descritta dal Comune: eventuali ulteriori avvisi regionali vanno controllati prima di partire.",
            "L'arancione nel bollettino nazionale è associato sia alla criticità per temporali sia a quella idrogeologica. Non è una previsione che garantisce un evento estremo in ogni singolo comune: i livelli rappresentano scenari di rischio per zone omogenee, non una misura di pioggia già caduta.",
            "Chi deve attraversare aree vulnerabili, sottopassi o strade soggette ad allagamento può verificare la zona di destinazione nella mappa ufficiale e seguire le indicazioni della Protezione civile locale. Le ordinanze dei comuni, se adottate, hanno contenuto e validità propri; il bollettino nazionale non dispone da solo chiusure di scuole o strade.",
        ],
        "fonti": [
            {"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/index.html", "nome": "Dipartimento della Protezione Civile — bollettino di criticità del 10 ottobre, previsione per l'11."},
            {"url": "https://www.comune.bitonto.ba.it/it/news/allerta-meteo-per-pioggia-e-temporali-prorogata-sino-alle-ore-6-di-domenica-11-ottobre?type=3", "nome": "Comune di Bitonto — proroga regionale dell'allerta fino alle 6 di domenica."},
        ],
        "image_source": "salento", "image_alt": "Illustrazione editoriale IA ultrarealistica di pioggia su una piazza del Salento; non documenta un evento specifico.",
        "image_prompt": "Piazza storica del Salento sotto nubi di pioggia, nessuna mappa; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "roma-bus-strade-domenica-11-ottobre-2026-processione-corse",
        "titolo": "Roma, domenica processione e corse: bus deviati e strade chiuse",
        "sommario": "La processione parte alle 8 verso San Pietro; gare a Ostiense, Cecchignola e Ostia cambiano percorsi e viabilità. Il Comune indica linee e fasce orarie da controllare.",
        "categoria": "Italia", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Roma", "bus deviati"],
        "dati_chiave": [{"valore": "8:00", "etichetta": "partenza processione"}, {"valore": "8:30–11:30", "etichetta": "deviazioni Ostiense"}, {"valore": "8:00–14:30", "etichetta": "chiusure a Ostia"}],
        "paragrafi": [
            "Domenica 11 ottobre a Roma sono previste modifiche a bus e viabilità per una processione nel centro e tre eventi sportivi. Roma Capitale ha pubblicato il programma del fine settimana con percorsi e fasce orarie: le conseguenze cambiano molto fra San Pietro, Ostiense, Cecchignola e il litorale di Ostia.",
            "La processione prende il via alle 8 da piazza dell'Oro e raggiunge piazza Papa Pio XII passando per Ponte Sant'Angelo, piazza Pia e via della Conciliazione. Il Comune segnala possibili rallentamenti o limitazioni per i bus 23, 34, 40, 46, 62, 64, 98, 115, 190F, 280, 870, 881 e 916F: non annuncia la cancellazione integrale di queste linee.",
            "La corsa podistica in zona Ostiense parte e arriva al Parco Schuster. Tra le 8:30 e le 11:30 circa sono indicate deviazioni per le linee 23, 128, 715, 766 e 792; la 128 avrà un capolinea provvisorio in largo San Leonardo Murialdo.",
            "Un'altra corsa alla Cecchignola parte alle 9:30 e coinvolge viale dell'Esercito e le strade circostanti, con una deviazione prevista per la linea 763.",
            "A Ostia, per il triathlon tra le 8 e le 14:30, sono annunciate chiusure delle corsie centrali della Cristoforo Colombo verso piazzale Colombo, del piazzale e del lungomare Amerigo Vespucci. Cambiano anche i percorsi dei bus 06, 07, 014 e 070.",
            "Resta chiuso al traffico fino alle 6 di lunedì 12 un tratto di viale Kennedy per l'evento street food, con modifiche alla linea 515. Prima di mettersi in viaggio è prudente controllare gli aggiornamenti di Atac e Roma Servizi per la Mobilità, indicati dallo stesso Comune: le deviazioni possono dipendere dall'andamento effettivo delle manifestazioni.",
        ],
        "fonti": [{"url": "https://www.comune.roma.it/web/it/notizia/mobilita-trasporti-10-11-ottobre-2026.page", "nome": "Roma Capitale — programma viabilità e trasporto pubblico del weekend 10–11 ottobre."}],
        "image_source": "roma", "image_alt": "Illustrazione editoriale IA ultrarealistica di un autobus rosso presso Castel Sant'Angelo; non è una fotografia delle deviazioni.",
        "image_prompt": "Bus urbano e Castel Sant'Angelo in scena editoriale non documentaria; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "como-chiasso-treni-sospesi-domenica-11-ottobre-2026",
        "titolo": "Como–Chiasso, treni sospesi domenica: riapertura lunedì alle 4:20",
        "sommario": "RFI ferma la circolazione fra Como San Giovanni e Chiasso per lavori in galleria. Coinvolti collegamenti regionali e lunga percorrenza; il cantiere torna anche il weekend successivo.",
        "categoria": "Italia", "luogo": "Como", "formato": "flash",
        "parole_chiave_titolo": ["Como–Chiasso", "4:20"],
        "dati_chiave": [{"valore": "4:20", "etichetta": "fine prevista lunedì 12"}, {"valore": "9–12", "etichetta": "primo weekend di lavori"}, {"valore": "16–19", "etichetta": "secondo weekend"}],
        "paragrafi": [
            "La circolazione ferroviaria fra Como San Giovanni e Chiasso resta sospesa domenica 11 ottobre, con riapertura prevista alle 4:20 di lunedì 12. Rete Ferroviaria Italiana ha programmato la chiusura dalle 20:35 di venerdì 9 per interventi di consolidamento e impermeabilizzazione di una galleria sulla linea Milano–Chiasso.",
            "Il provvedimento riguarda treni regionali e a lunga percorrenza che attraversano il confine. Non significa che l'intera linea Milano–Como sia chiusa: il tratto interessato dal cantiere è quello tra le stazioni di Como San Giovanni e Chiasso.",
            "Per alcune corse Eurocity l'avviso RFI specifica un percorso alternativo fra Chiasso e Como San Giovanni senza fermata nella stazione comasca. Altri servizi regionali transfrontalieri presentano variazioni; il viaggiatore deve verificare il numero del proprio treno, non dedurre dal solo nome della linea che sia soppresso.",
            "RFI segnala un secondo periodo con le stesse fasce orarie da venerdì 16 a lunedì 19 ottobre. La distinzione è importante per chi rientra domenica: il termine delle 4:20 di lunedì 12 non chiude definitivamente i lavori del mese.",
            "Prima della partenza conviene consultare l'avviso di infomobilità e il canale del proprio operatore per fermate, eventuale trasporto sostitutivo e orari aggiornati. RFI non pubblica nel comunicato una soluzione identica per ogni collegamento, e le modifiche possono differire per direzione e giorno.",
        ],
        "fonti": [
            {"url": "https://www.rfi.it/it/news-e-media/comunicati-stampa-e-news/2026/10/7/rfi---linea-milano-chiasso--modifiche-al-programma-circolazione-.html", "nome": "RFI — sospensione Como San Giovanni–Chiasso e finestre dei lavori."},
            {"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/9/linee-zurigo-chiasso-milano--zurigo-chiasso-venezia-s-l---zurigo.html", "nome": "RFI — modifiche ai treni Eurocity del 9–11 ottobre."},
        ],
        "image_source": "como", "image_alt": "Illustrazione editoriale IA ultrarealistica di un treno alla stazione di Como San Giovanni; non documenta i lavori reali.",
        "image_prompt": "Stazione Como San Giovanni e treno regionale in scena editoriale; logo CurioMondo circolare applicato in post-produzione.",
    },
]


def correct_visible_date(slug: str, published: datetime, place: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    label = site._italian_date(published.isoformat(timespec="seconds"))
    for node in doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]'):
        node.text = f"{label} · {place} · "
    for node in doc.xpath('//section[contains(@class,"art-sources")]//small/br[1]'):
        if node.tail and "Ultimo aggiornamento editoriale:" in node.tail:
            node.tail = f"Testo originale CurioMondo. Ultimo aggiornamento editoriale: {label}."
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def main() -> None:
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    for phrase in ("Un avviso letto in tempo può cambiare un viaggio.", "Ogni strada ha un momento giusto per essere percorsa.", "Prima di partire, dai un'occhiata al percorso."):
        if phrase not in phrases:
            phrases.append(phrase)
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    now = datetime.now(ZoneInfo("Europe/Rome"))
    # Il clock del contenitore è anticipato: ora reale sincronizzata tramite servizio web.
    release = datetime(2026, 10, 10, 23, 34, 0, tzinfo=ZoneInfo("Europe/Rome"))
    images = []
    for article, minutes in zip(ARTICLES, (0, 9, 21)):
        image = base.make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = release - timedelta(minutes=minutes)
        base.set_published(slug, published)
        correct_visible_date(slug, published, article["luogo"])
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
                  "last_update": f"finale-serale-v{VERSION}", "date": release.date().isoformat(),
                  "release_date": release.date().isoformat(), "updated_at": release.isoformat(timespec="seconds"),
                  "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in ARTICLES]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
