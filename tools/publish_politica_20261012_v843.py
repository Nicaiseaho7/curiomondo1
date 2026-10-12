#!/usr/bin/env python3
"""Tre notizie istituzionali, verificate su fonti primarie il 12 ottobre."""
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageOps
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
from tools.publish_notte_mattina_20261010_v827 import set_published
from tools.publish_finale_20261010_v836 import correct_visible_date

VERSION = 843
ARTICLES = [
    {
        "slug": "dpfp-audizioni-giorgetti-12-ottobre-2026-orari",
        "titolo": "Conti pubblici, oggi sei audizioni: Giorgetti alla Camera alle 18",
        "sommario": "Le Commissioni Bilancio ascoltano gli organismi economici prima dell'esame del documento programmatico. Il calendario non annuncia nuovi bonus o modifiche alle imposte.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Conti pubblici", "alle 18"],
        "dati_chiave": [{"valore": "14:00", "etichetta": "inizio audizioni"}, {"valore": "18:00", "etichetta": "intervento Giorgetti"}, {"valore": "6", "etichetta": "audizioni programmate"}],
        "paragrafi": [
            "Il ministro dell'Economia Giancarlo Giorgetti è atteso lunedì 12 ottobre alle 18 alla Camera per un'audizione sul Documento programmatico di finanza pubblica 2026. Le Commissioni Bilancio di Camera e Senato si riuniscono nella Sala del Mappamondo: il programma comincia alle 14 e comprende sei audizioni.",
            "Aprono i rappresentanti della Corte dei conti. Seguono l'Istat alle 14:45, il CNEL alle 15:30 e Banca d'Italia alle 16:15. Alle 17 è previsto l'intervento della presidente dell'Ufficio parlamentare di bilancio, Lilia Cavallari, prima del ministro.",
            "Le audizioni precedono l'esame parlamentare del documento. Al termine, la Commissione Bilancio della Camera è convocata per l'esame in sede referente, con votazioni previste. Il fascicolo comprende il documento, l'annesso e gli allegati; la relatrice è Rebecca Frassini.",
            "Per famiglie, lavoratori e imprese il passaggio consente di seguire il confronto sui conti dello Stato. La convocazione, però, non introduce agevolazioni, nuovi requisiti o cambiamenti delle imposte: queste disposizioni richiedono provvedimenti specifici. Il calendario indica interventi ancora da svolgere, non valutazioni già espresse dagli organismi convocati.",
        ],
        "fonti": [{"url": "https://www.camera.it/leg19/1099?shadow_organo_parlamentare=3505", "nome": "Camera dei deputati — convocazione della Commissione Bilancio del 12 ottobre, orari e seguito dell'esame."}],
        "image_path": "exec-e5228b11-6e91-4b0a-80d8-dd3d2fb3da80.png",
        "image_alt": "Somiglianza sintetica editoriale IA di Giancarlo Giorgetti in ambiente parlamentare; non documenta l'audizione del 12 ottobre.",
        "image_prompt": "Giancarlo Giorgetti riconoscibile, in volto, in contesto parlamentare; scena sintetica non documentaria senza scritte.",
        "likeness": "Giancarlo Giorgetti",
    },
    {
        "slug": "protezione-civile-ddl-camera-personale-12-ottobre-2026",
        "titolo": "Protezione civile, il ddl sul personale arriva in Aula alla Camera",
        "sommario": "La discussione generale è nell'ordine del giorno delle 14:30. Il testo trasmesso dal Senato prevede sezioni contrattuali dedicate; le nuove disposizioni non sono ancora legge.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Protezione civile", "Camera"],
        "dati_chiave": [{"valore": "12 ottobre", "etichetta": "discussione in programma"}, {"valore": "C. 3076", "etichetta": "disegno di legge"}, {"valore": "14:30", "etichetta": "inizio della seduta"}],
        "paragrafi": [
            "Il disegno di legge sulla Protezione civile è nell'ordine del giorno della Camera di lunedì 12 ottobre, per la discussione generale nella seduta che comincia alle 14:30. Il provvedimento C. 3076 è già stato approvato dal Senato, ma deve completare l'iter parlamentare: le disposizioni proposte non sono ancora in vigore.",
            "Il testo trasmesso da Palazzo Madama prevede sezioni contrattuali specifiche per il personale, dirigenti compresi, delle strutture di Protezione civile di Regioni, Comuni, Province, città metropolitane e altri enti del comparto delle funzioni locali. La contrattazione dovrebbe disciplinare formazione, condizioni di lavoro, turnazioni e reperibilità entro le risorse disponibili.",
            "Per i dipendenti non dirigenti, la versione approvata dal Senato distingue un'indennità di base, una aggiuntiva per il pronto impiego e una per le missioni di coordinamento in emergenza. Gli importi sono affidati alla contrattazione: il documento non attribuisce già una cifra identica a tutti gli operatori.",
            "Sono previste anche tutela assicurativa e legale per ragioni di servizio e formazione continua obbligatoria. Un'altra parte del disegno di legge riguarda linee guida e responsabilità nelle attività di Protezione civile, con condizioni legate alle raccomandazioni e alle caratteristiche del caso concreto.",
            "La discussione iniziale in Assemblea non coincide con il voto definitivo. Per chi lavora nelle strutture territoriali, il passaggio da seguire è il testo che uscirà dall'esame della Camera, insieme all'eventuale approvazione conclusiva e alla successiva pubblicazione della legge.",
        ],
        "fonti": [{"url": "https://www.camera.it/leg19/187", "nome": "Camera dei deputati — ordine del giorno della seduta 725, discussione generale del C. 3076."}, {"url": "https://documenti.camera.it/apps/commonServices/getDocumento.ashx?codice=leg.19.pdl.camera.3076.19PDL0210890&idlegislatura=19&sezione=lavori&tipoDoc=testo_pdl_pdf", "nome": "Camera dei deputati — testo C. 3076 trasmesso dal Senato il 4 agosto 2026, sezioni contrattuali e tutele proposte."}],
        "image_path": "exec-ce391706-141d-47b7-bb98-32414d831915.png",
        "image_alt": "Illustrazione editoriale IA di una sala di coordinamento della Protezione civile; non documenta un'emergenza.",
        "image_prompt": "Sala operativa italiana di Protezione civile con radio e personale di sfondo rivolto verso la camera; scena concettuale non documentaria.",
    },
    {
        "slug": "consiglio-ambiente-ue-ets-cop31-12-ottobre-2026",
        "titolo": "Emissioni e clima, oggi il Consiglio UE prepara le posizioni per COP31",
        "sommario": "A Lussemburgo è in programma il confronto sul riesame dell'ETS e sui negoziati internazionali. Le conclusioni sul clima e sulla biodiversità sono attese, non ancora annunciate come approvate.",
        "categoria": "Politica", "luogo": "Lussemburgo", "formato": "flash",
        "parole_chiave_titolo": ["Emissioni e clima", "COP31"],
        "dati_chiave": [{"valore": "9:30", "etichetta": "inizio previsto"}, {"valore": "9–20 novembre", "etichetta": "COP31 ad Antalya"}, {"valore": "19–30 ottobre", "etichetta": "COP17 a Erevan"}],
        "paragrafi": [
            "I ministri europei dell'Ambiente hanno in programma lunedì 12 ottobre a Lussemburgo un confronto sul riesame del sistema UE di scambio delle quote di emissione e sulle posizioni negoziali per le prossime conferenze internazionali. La riunione del Consiglio Ambiente è prevista dalle 9:30; il calendario resta indicativo.",
            "Il dibattito sulle emissioni riguarda il pacchetto proposto dalla Commissione il 17 luglio, collegato al traguardo climatico per il 2040. I ministri possono presentare priorità e osservazioni su un testo ancora all'esame degli organi preparatori del Consiglio. Questa fase non equivale all'approvazione definitiva di nuove regole per le imprese italiane.",
            "Il programma colloca intorno alle 11:40 l'approvazione attesa delle conclusioni in vista della COP31. La conferenza sul clima si terrà dal 9 al 20 novembre ad Antalya, in Turchia, sotto la guida congiunta di Turchia e Australia. L'agenda europea mette l'accento sull'attuazione dell'accordo di Parigi e sugli impegni già assunti.",
            "Nel pomeriggio, intorno alle 14:45, sono previste conclusioni sulla biodiversità prima della COP17 di Erevan, dal 19 al 30 ottobre. Quell'appuntamento farà il primo riesame globale dei progressi verso gli obiettivi del quadro di Kunming-Montreal per il 2030.",
            "Tra gli altri temi figurano imballaggi e relativi rifiuti, materie prime plastiche riciclate e responsabilità dei produttori nelle acque reflue urbane. Sono dossier che interessano anche amministrazioni e filiere produttive italiane. Il programma non indica però un nuovo obbligo immediato per cittadini o aziende: gli esiti dovranno risultare dai documenti conclusivi.",
            "La conferenza stampa finale è indicata intorno alle 17:30. Gli orari del confronto e delle conclusioni possono cambiare durante i lavori.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/it/meetings/env/2026/10/12/", "nome": "Consiglio dell'Unione europea — agenda del Consiglio Ambiente del 12 ottobre, riesame ETS e conferenze COP."}, {"url": "https://www.consilium.europa.eu/it/press/press-releases/2026/10/09/media-advisory-environment-council-of-12-october-2026/", "nome": "Consiglio dell'Unione europea — programma indicativo e orari pubblicati il 9 ottobre."}],
        "image_path": "exec-dc17da31-ad32-4a20-98f8-deacc31f1465.png",
        "image_alt": "Illustrazione editoriale IA di un ambiente di riunione europeo a Lussemburgo; non documenta votazioni o decisioni.",
        "image_prompt": "Ambiente del centro conferenze ECCL a Lussemburgo con bandiere UE e dossier; personale di sfondo, nessuna decisione rappresentata.",
    },
]

def main():
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text())
    for phrase in ("Puoi rimandare una risposta finché hai le idee più chiare.", "Se una scarpa ti fa male, fermati e sistemala.", "Puoi chiedere a qualcuno di parlare più lentamente."):
        if phrase not in phrases:
            phrases.append(phrase)
    phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2)+"\n")
    release = datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    rows = deepcopy(ARTICLES)
    images = []
    for a, minutes in zip(rows, (0, 5, 11)):
        source = ROOT.parent / "generated_images" / a.pop("image_path")
        im = ImageOps.fit(Image.open(source).convert("RGB"), (1600, 900), method=Image.Resampling.LANCZOS)
        variants = []
        for w in (480, 800, 1200):
            path = ROOT / "assets/images/editorial-auto" / f"{a['slug']}-v{VERSION}-{w}.webp"
            im.resize((w, round(w*9/16)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=89, method=6)
            variants.append({"w": w, "h": round(w*9/16), "src": "/assets/images/editorial-auto/"+path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
        image = {"id": a["slug"], "article": "/notizie/"+a["slug"]+".html", "alt": a.pop("image_alt"), "prompt": a.pop("image_prompt"), "variants": variants, "disclosure": site.CAPTION, "generator": "OpenAI image generation", "aiGenerated": True, "documentaryPhoto": False, "officialArtwork": False, "sensitiveContext": False, "weatherMap": False, "reenactedEvent": False, "logoApplied": False}
        if a.get("likeness"):
            image["syntheticLikeness"] = "public-figure"
            image["publicFigureName"] = a.pop("likeness")
        slug = site.write_article(a, image, VERSION)
        published = release - timedelta(minutes=minutes)
        set_published(slug, published)
        correct_visible_date(slug, published, a["luogo"])
        a["published"] = published.isoformat()
        if "protezione-civile-ddl" in slug:
            path = ROOT / "notizie" / (slug+".html")
            doc = html.fromstring(path.read_text())
            body = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
            block = html.fragment_fromstring('<aside class="cm-evergreen-reader"><p>Approfondimento</p><h2>Come diventa legge un disegno di legge in Italia</h2><p>I passaggi tra commissioni, Assemblee e pubblicazione.</p><a href="/approfondimenti/come-diventa-legge-disegno-di-legge-italia.html">Leggi l’approfondimento →</a></aside>')
            body.addnext(block)
            path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>")+"\n")
        images.append(image)
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text())
    registry["items"] = images + registry["items"]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2)+"\n")
    site.sync_surfaces(rows, images[0]["article"], VERSION, update_manifest=False)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text())
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION), "articleCount": int(state["articleCount"])+3, "generatedEditorialImages": int(state["generatedEditorialImages"])+3, "last_update": "politica-v843", "date": release.date().isoformat(), "release_date": release.date().isoformat(), "updated_at": release.isoformat(), "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in rows]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
