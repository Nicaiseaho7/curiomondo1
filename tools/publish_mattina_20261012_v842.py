#!/usr/bin/env python3
"""Quattro avvisi verificati per la mattina del 12 ottobre 2026."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_notte_mattina_20261010_v827 as base
from tools import publish_finale_20261010_v836 as prior
from automation.newsroom import site

VERSION = 842
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "bari": ROOT.parent / "generated_images/exec-901bfcf2-aed1-437a-bdb4-3cc91acbd8b3.png",
    "nettuno": ROOT.parent / "generated_images/exec-6dd278a8-7922-4809-ac23-24094c67481c.png",
    "asti": ROOT.parent / "generated_images/exec-ddc139a9-d2a3-40ed-a3cd-a690632c2d0d.png",
    "a14": ROOT.parent / "generated_images/exec-7a4ca769-d692-4704-a361-9deb9fcf7122.png",
}

ARTICLES = [
    {
        "slug": "sciopero-amtab-bari-12-ottobre-2026-orari-bus",
        "titolo": "Bari, sciopero AMTAB oggi 8:30–12:29: le fasce garantite",
        "sommario": "L'azienda distingue gli orari del personale viaggiante da quelli di uffici e impianti. Il MIT registra l'astensione locale di quattro ore.",
        "categoria": "Trasporti", "luogo": "Bari", "formato": "flash",
        "parole_chiave_titolo": ["AMTAB", "8:30–12:29"],
        "dati_chiave": [{"valore": "8:30–12:29", "etichetta": "personale bus"}, {"valore": "5:30–8:29", "etichetta": "prima fascia garantita"}, {"valore": "12:30–15:29", "etichetta": "seconda fascia"}],
        "paragrafi": [
            "A Bari i bus AMTAB possono subire disagi lunedì 12 ottobre per uno sciopero aziendale di quattro ore. Per conducenti, verificatori e altro personale di esercizio del trasporto pubblico, l'astensione annunciata va dalle 8:30 alle 12:29; le fasce di garanzia indicate dall'azienda sono 5:30–8:29 e 12:30–15:29.",
            "Gli addetti agli impianti fissi, compresi uffici, officine, depositi, autorimesse e sosta, si fermano invece nelle ultime due ore del rispettivo turno. La differenza evita di estendere automaticamente ai parcheggi o agli sportelli lo stesso orario dei conducenti.",
            "Il calendario del Ministero delle Infrastrutture e dei Trasporti registra per AMTAB di Bari un'azione locale dalle 8:30 alle 12:30. L'azienda precisa che alcune prestazioni minime, fra cui presidio del centro operativo e del numero verde, restano assicurate durante la protesta.",
            "L'adesione effettiva di oggi non è ancora nota. AMTAB indica per informazioni il numero verde 800 450 444; chi ha una coincidenza o un appuntamento può verificare la propria linea prima di partire. Il dato di adesione del 3,29% citato dall'azienda riguarda un precedente sciopero, non questa giornata.",
        ],
        "fonti": [{"url": "https://www.amtab.it/it/140-news-chatbot/3528-sciopero-aziendale-di-4-ore-del-personale-amtab-3", "nome": "AMTAB — avviso ufficiale sullo sciopero del 12 ottobre e fasce di garanzia."}, {"url": "https://scioperi.mit.gov.it/mit2/public/scioperi", "nome": "MIT — calendario degli scioperi, voce AMTAB Bari del 12 ottobre 2026."}],
        "image_source": "bari", "image_alt": "Illustrazione editoriale IA di un autobus AMTAB sul lungomare di Bari; non documenta lo sciopero.",
        "image_prompt": "Autobus AMTAB a Bari in scena editoriale fotorealistica non documentaria; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "roma-nettuno-frana-padiglione-marechiaro-bus-12-ottobre-2026",
        "titolo": "Roma–Nettuno, stop tra Padiglione e Marechiaro: bus attivi",
        "sommario": "Trenitalia segnala ancora il 12 ottobre la sospensione per una frana iniziata venerdì. Regionali limitati o cancellati, senza orario di riapertura indicato.",
        "categoria": "Trasporti", "luogo": "Lazio", "formato": "flash",
        "parole_chiave_titolo": ["Roma–Nettuno", "bus attivi"],
        "dati_chiave": [{"valore": "9 ottobre", "etichetta": "inizio interruzione"}, {"valore": "12 ottobre", "etichetta": "avviso ancora attivo"}, {"valore": "bus", "etichetta": "servizio sostitutivo"}],
        "paragrafi": [
            "La circolazione sulla linea Roma–Nettuno rimane sospesa tra Padiglione e Marechiaro nel bollettino di Trenitalia datato lunedì 12 ottobre. La causa indicata è un movimento franoso vicino alla linea; l'interruzione era iniziata alle 16:40 di venerdì 9 ottobre.",
            "I treni regionali possono essere cancellati o limitati nel percorso e registrare ritardi. Trenitalia segnala corse con autobus, ma non dà un orario di ripristino: il viaggiatore deve controllare il singolo treno e le fermate del bus attraverso i canali ufficiali prima di recarsi in stazione.",
            "Lo stop riguarda il tratto fra due stazioni, non una sospensione uniforme di tutti i servizi ferroviari del Lazio. La pagina Infomobilità distingue questo avviso dai lavori programmati nella stessa zona: non si deve presumere che la fine dei cantieri coincida con la riapertura dopo la frana.",
        ],
        "fonti": [{"url": "https://www.trenitalia.com/it/informazioni/Infomobilita/notizie-infomobilita.html?cid=primafascia1", "nome": "Trenitalia — Infomobilità, aggiornamento Roma–Nettuno del 12 ottobre 2026."}, {"url": "https://www.rfi.it/it/news-e-media/infomobilita/aggiornamenti/2026/10/9/linea-roma---nettuno--dalle-ore-16-40-circolazione-ferroviaria-s.html", "nome": "RFI — comunicazione iniziale dello stop del 9 ottobre."}],
        "image_source": "nettuno", "image_alt": "Illustrazione editoriale IA di un treno regionale in stazione nel Lazio; non documenta la frana o il tratto interrotto.",
        "image_prompt": "Treno regionale in stazione del Lazio, nessuna ricostruzione della frana; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "asti-alessandria-lavori-treni-orari-12-ottobre-2026",
        "titolo": "Asti–Alessandria, dal 12 ottobre cambiano i treni per Milano",
        "sommario": "RFI pubblica gli orari sostitutivi Trenord, il nuovo bus mattutino e le variazioni fino al 12 dicembre. Controllare numero e orario del proprio regionale.",
        "categoria": "Trasporti", "luogo": "Piemonte", "formato": "flash",
        "parole_chiave_titolo": ["Asti–Alessandria", "Milano"],
        "dati_chiave": [{"valore": "12 ottobre", "etichetta": "inizio lavori"}, {"valore": "12 dicembre", "etichetta": "fine prevista"}, {"valore": "4 minuti", "etichetta": "anticipo per alcuni treni"}],
        "paragrafi": [
            "Da lunedì 12 ottobre, lavori programmati fra Asti e Alessandria modificano diversi collegamenti regionali verso Milano e Torino. L'avviso di RFI vale fino al 12 dicembre e distingue le modifiche che iniziano oggi da quelle che scatteranno martedì 13.",
            "Per Trenord, sei regionali Asti–Milano Centrale sono cancellati e sostituiti da nuovi treni: fra questi il R 2361 delle 8:54 viene sostituito dal NT 7441 in partenza da Asti alle 8:50, con arrivo a Milano Centrale alle 10:35. Nella direzione opposta alcuni arrivi ad Asti slittano di quattro minuti.",
            "Il Trenitalia 2152 da Alessandria a Torino Porta Nuova, originariamente previsto alle 4:25, parte alle 5:15 e arriva alle 6:30 secondo la tabella RFI. È indicato anche il bus TO357, in partenza da Alessandria alle 4:00 e con fermate ad Asti e Torino Lingotto prima di Porta Nuova alle 5:40; il bus non trasporta biciclette.",
            "Da martedì 13 cambieranno anche collegamenti Trenitalia Asti–Milano, Asti–Alessandria e Asti–Voghera. I viaggiatori possono verificare il numero del treno nei canali di vendita aggiornati: l'avviso non significa che ogni corsa sulla linea sia cancellata.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/12/linee-torino-p--nuova---alessandria--asti---milano--asti---aless.html", "nome": "RFI — avviso e tabella delle variazioni 12 ottobre–12 dicembre 2026."}],
        "image_source": "asti", "image_alt": "Illustrazione editoriale IA di un treno regionale Trenord presso Asti; non è una fotografia dei lavori.",
        "image_prompt": "Treno regionale Trenord ad Asti, scena fotorealistica non documentaria; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "a14-bologna-chiusura-notturna-casalecchio-borgo-panigale-12-ottobre-2026",
        "titolo": "A14 Bologna, chiusure notturne dal 12 al 14 ottobre verso Milano",
        "sommario": "Il tratto dal Raccordo Casalecchio a Borgo Panigale sarà chiuso 21–5 per tre notti. Autostrade indica percorsi alternativi e l'uscita non raggiungibile.",
        "categoria": "Trasporti", "luogo": "Bologna", "formato": "flash",
        "parole_chiave_titolo": ["A14 Bologna", "21–5"],
        "dati_chiave": [{"valore": "21–5", "etichetta": "orario notturno"}, {"valore": "3 notti", "etichetta": "12, 13 e 14 ottobre"}, {"valore": "verso Milano", "etichetta": "direzione interessata"}],
        "paragrafi": [
            "Sulla A14 Bologna–Taranto è programmata la chiusura notturna del tratto fra l'allacciamento con il Raccordo di Casalecchio e Bologna Borgo Panigale, in direzione A1/Milano. Autostrade per l'Italia indica le notti di lunedì 12, martedì 13 e mercoledì 14 ottobre, ogni volta dalle 21 alle 5 del mattino successivo, per lavori di pavimentazione.",
            "Per chi arriva da Ancona, l'uscita di Bologna Borgo Panigale non sarà raggiungibile durante la chiusura. Il provvedimento non è annunciato per tutta la giornata del 12 ottobre né per entrambe le direzioni.",
            "Chi proviene da Pescara, Ancona o Padova ed è diretto verso Milano può percorrere il Raccordo di Casalecchio e immettersi sulla A1 verso Milano. Come alternativa per l'uscita di Borgo Panigale, Autostrade indica Bologna Casalecchio sul raccordo oppure Bologna Arcoveggio sulla A13.",
            "Le condizioni in tempo reale possono variare rispetto al programma dei cantieri. Prima di entrare in autostrada conviene consultare i canali viabilità del gestore; il call center dedicato è 803 111.",
        ],
        "fonti": [{"url": "https://www.autostrade.it/it/comunicazione-e-media/comunicati-stampa-viabilita/-/bulletin/view/dba729e0-f782-4896-b1a2-8a380b15673d", "nome": "Autostrade per l'Italia — avviso viabilità A14 del 9 ottobre per le notti 12–14 ottobre."}],
        "image_source": "a14", "image_alt": "Illustrazione editoriale IA di uno svincolo autostradale nell'area di Bologna al tramonto; non documenta la chiusura.",
        "image_prompt": "Svincolo autostradale nell'area di Bologna al tramonto, senza rappresentare il cantiere; logo CurioMondo circolare in post-produzione.",
    },
]


def main() -> None:
    if sys.argv[1:] == ["--repair-paragraph"]:
        path = ROOT / "notizie/asti-alessandria-lavori-treni-orari-12-ottobre-2026.html"
        current = path.read_text(encoding="utf-8")
        old = "Il regionale Trenitalia 2152 da Alessandria"
        if current.count(old) != 1:
            raise SystemExit("paragrafo da correggere non univoco")
        path.write_text(current.replace(old, "Il Trenitalia 2152 da Alessandria"), encoding="utf-8")
        return
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    for phrase in (
        "Controlla l'orario del tuo autobus prima di uscire.",
        "Un percorso alternativo può rendere più semplice la giornata.",
        "Verifica il numero del treno anche quando conosci già la tratta.",
        "Prima di metterti in viaggio, guarda gli aggiornamenti della strada.",
    ):
        if phrase not in phrases:
            phrases.append(phrase)
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    release = datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    for article, minutes in zip(ARTICLES, (0, 7, 17, 25)):
        image = base.make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = release - timedelta(minutes=minutes)
        base.set_published(slug, published)
        prior.correct_visible_date(slug, published, article["luogo"])
        image["article"] = f"/notizie/{slug}.html"
        registry_path = ROOT / "assets/data/editorial-images-v210.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["items"] = [image] + registry.get("items", [])
        registry["version"] = VERSION
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(ARTICLES, f"/notizie/{ARTICLES[0]['slug']}.html", VERSION, update_manifest=False)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                  "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                  "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(ARTICLES),
                  "last_update": f"mattina-v{VERSION}", "date": release.date().isoformat(),
                  "release_date": release.date().isoformat(), "updated_at": release.isoformat(timespec="seconds"),
                  "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": release.isoformat(), "slugs": [a["slug"] for a in ARTICLES]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
