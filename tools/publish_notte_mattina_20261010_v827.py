#!/usr/bin/env python3
"""Release v827: dieci notizie principali emerse nella notte e al mattino."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 827
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"
LOGO = ROOT / "assets/images/curiomondo-logo-circle-v715.png"

IMAGE_SOURCES = {
    "mattarella": GENERATED / "exec-ef4fc4e8-c22c-4815-be08-bc8a2445293b.png",
    "marsala": GENERATED / "exec-acf98ee5-d0e8-4cf3-a432-f8e6ca4bec7d.png",
    "tramvia": GENERATED / "exec-4258ae17-2cd2-4ba5-94bc-928aef844f89.png",
    "treni": GENERATED / "exec-67242cd0-f2ce-403f-865f-aff747cebc21.png",
    "richiami": GENERATED / "exec-63a0b8d7-361f-4caf-9039-1ba6415f2904.png",
    "isaias": GENERATED / "exec-d1cb6a5f-548b-4e0e-ba4f-30701138ea6e.png",
    "simon": GENERATED / "exec-afe82e4f-bdcf-41cb-bb78-2a04a228de17.png",
    "diesel": GENERATED / "exec-f4f70613-f72f-4724-882b-762fec086cbc.png",
    "riyadh": GENERATED / "exec-0bb4359d-2516-406b-b3fc-5c2d0f1508a5.png",
    "cpi": GENERATED / "exec-da7aeabe-25ea-42fe-9ac6-422a2ad15832.png",
}


def make_variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        crop_width = round(image.height * ratio)
        left = (image.width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, image.height))
    else:
        crop_height = round(image.width / ratio)
        top = (image.height - crop_height) // 2
        image = image.crop((0, top, image.width, top + crop_height))

    source_logo = Image.open(LOGO).convert("RGBA")
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        height = round(width / ratio)
        canvas = image.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        logo_size = max(48, round(width * 0.105))
        mark = source_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        circle = Image.new("L", (logo_size, logo_size), 0)
        ImageDraw.Draw(circle).ellipse((0, 0, logo_size - 1, logo_size - 1), fill=235)
        mark.putalpha(ImageChops.multiply(mark.getchannel("A"), circle))
        margin = max(10, round(width * 0.018))
        canvas.alpha_composite(mark, (width - logo_size - margin, height - logo_size - margin))
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        canvas.convert("RGB").save(path, "WEBP", quality=89, method=6)
        variants.append({
            "w": width, "h": height,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def make_image(article: dict) -> dict:
    image = {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": article.pop("image_sensitive", False),
        "weatherMap": False,
        "reenactedEvent": article.pop("image_reenacted", False),
        "logoApplied": True,
        "logoShape": "circle",
    }
    likeness = article.pop("image_likeness", None)
    if likeness:
        image["syntheticLikeness"] = likeness
    return image


def set_published(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Le regole diventano concrete quando ogni passaggio è comprensibile.",
        "Dopo il vento più forte, la priorità è rimettere in sicurezza ciò che resta.",
        "Un viaggio informato comincia prima di arrivare alla fermata.",
        "Negli imprevisti, un aggiornamento affidabile vale quanto una coincidenza.",
        "Controllare il lotto è un gesto piccolo che protegge tutta la famiglia.",
        "Davanti a una tempesta, la prudenza non è mai tempo perso.",
        "Seguire gli avvisi ufficiali è il modo più semplice per ridurre il rischio.",
        "Le decisioni sull'energia cambiano mercati, alleanze e vite quotidiane.",
        "Anche in una crisi improvvisa, distinguere fatti e rivendicazioni è essenziale.",
        "La giustizia internazionale vive della fiducia che gli Stati scelgono di darle.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "mattarella-promulga-legge-elettorale-vigore-24-ottobre-2026",
        "titolo": "Mattarella promulga la legge elettorale: in vigore dal 24 ottobre",
        "sommario": "Il testo è diventato la legge 180 del 2026 ed è stato pubblicato in Gazzetta Ufficiale. Le nuove regole sostituiranno il Rosatellum tra due settimane.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Mattarella", "legge elettorale"],
        "dati_chiave": [{"valore": "24 ottobre", "etichetta": "entrata in vigore"}, {"valore": "42%", "etichetta": "soglia del premio"}, {"valore": "n. 180", "etichetta": "numero della legge"}],
        "paragrafi": [
            "Il presidente della Repubblica Sergio Mattarella ha promulgato nella serata del 9 ottobre la nuova legge elettorale per Camera e Senato. La pubblicazione in Gazzetta Ufficiale ha completato il passaggio successivo al voto definitivo della Camera.",
            "Il provvedimento è la legge 9 ottobre 2026, numero 180. La scheda ufficiale della Gazzetta fissa l'entrata in vigore al 24 ottobre: fino a quel giorno il nuovo sistema non produce effetti giuridici.",
            "La riforma abbandona i collegi uninominali e torna a un impianto proporzionale. Se una lista o una coalizione raggiunge almeno il 42% dei voti validi in entrambe le Camere, scatta un premio di governabilità con limiti massimi ai seggi assegnabili.",
            "Restano le soglie del 3% per le liste e del 10% per le coalizioni. Sono previste preferenze con capilista bloccati e l'indicazione preventiva del candidato alla presidenza del Consiglio da parte delle coalizioni.",
            "La firma del Quirinale non anticipa automaticamente le elezioni. La scadenza ordinaria della legislatura resta nel 2027 e l'eventuale scioglimento delle Camere segue le procedure costituzionali distinte dall'entrata in vigore della legge.",
            "La novità di questa mattina è quindi formale e concreta: il testo già approvato dal Parlamento è ora una legge pubblicata, con una data precisa per l'efficacia. Il confronto politico si sposta sui ricorsi annunciati e sull'applicazione delle nuove regole.",
        ],
        "fonti": [{"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.codiceRedazionale=26G00201&atto.dataPubblicazioneGazzetta=2026-10-09&elenco30giorni=false", "nome": "Gazzetta Ufficiale — legge 9 ottobre 2026 n. 180 ed entrata in vigore."}, {"url": "https://www.rainews.it/articoli/2026/10/presidente-della-repubblica-sergio-mattarella-ha-promulgato-la-legge-elettorale-d052119d-485b-4ebc-bee6-941fc71e5008.html", "nome": "RaiNews — promulgazione e principali regole del nuovo sistema."}],
        "image_source": "mattarella", "image_likeness": "Sergio Mattarella", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di Sergio Mattarella al Quirinale mentre esamina un atto; non è una foto della promulgazione.",
        "image_prompt": "Sergio Mattarella al Quirinale esamina un atto istituzionale, ritratto ultrarealistico e ricostruzione non documentaria; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "trombe-marine-marsala-mazara-petrosino-feriti-scuola-danni",
        "titolo": "Trombe marine nel Trapanese: circa 20 feriti e scuola danneggiata",
        "sommario": "Le raffiche hanno colpito Marsala, Mazara del Vallo e Petrosino. Tra i feriti ci sono una decina di bambini; la Prefettura non segnala morti né dispersi.",
        "categoria": "Cronaca", "luogo": "Trapani", "formato": "flash",
        "parole_chiave_titolo": ["trombe marine", "Trapanese"],
        "dati_chiave": [{"valore": "circa 20", "etichetta": "persone ferite"}, {"valore": "273", "etichetta": "alunni nel plesso colpito"}, {"valore": "0", "etichetta": "morti o dispersi segnalati"}],
        "paragrafi": [
            "Due trombe marine hanno investito il Trapanese nel pomeriggio di venerdì, lasciando danni estesi tra Marsala, Mazara del Vallo e Petrosino. Il bilancio disponibile questa mattina indica circa venti feriti, tra cui una decina di bambini medicati negli ospedali della zona.",
            "La Prefettura di Trapani ha riferito che i passeggeri di un'auto travolta dal vento a Petrosino sono stati trasferiti in codice rosso a Palermo. Non risultano persone disperse né decessi nei comuni danneggiati.",
            "A Marsala è stata colpita la sede di contrada Terrenuove dell'istituto Alcide De Gasperi. Nel plesso, che comprende elementari e medie, erano presenti 273 alunni; insegnanti e personale li hanno spostati nelle zone interne considerate più sicure.",
            "Le raffiche hanno danneggiato abitazioni, rovesciato automobili e abbattuto alberi e pali. La sindaca Andreana Patti ha parlato di almeno cinque case distrutte, precisando che la ricognizione era ancora in corso.",
            "Tra i feriti più seri figura una coppia che si trovava in un'auto sollevata e ribaltata. Le condizioni descritte non indicavano pericolo di vita, ma entrambi sono stati trasferiti in strutture palermitane per le cure necessarie.",
            "La conta dei danni resta provvisoria e può cambiare con i sopralluoghi. Con l'allerta arancione ancora attiva in Sicilia, è prudente evitare aree costiere esposte, alberi, pali e strade allagate e seguire gli avvisi dei Comuni.",
        ],
        "fonti": [{"url": "https://www.ansa.it/sito/notizie/cronaca/2026/10/09/maltempo-doppia-tromba-marina-nel-trapanese-danni-e-nove-feriti_8a1fb1c3-e77d-44de-ad4a-f0d636c72330.html", "nome": "ANSA — aggiornamenti della Prefettura, bilancio sanitario e danni nel Trapanese."}, {"url": "https://www.protezionecivile.gov.it/it/comunicato-stampa/maltempo-allerta-arancione-su-campania-calabria-puglia-e-sicilia/", "nome": "Protezione Civile — allerta arancione in Sicilia per il 10 ottobre."}],
        "image_source": "marsala", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica dei danni del maltempo sulla costa del Trapanese; non è una foto dell'evento.",
        "image_prompt": "Danni dopo trombe marine sulla costa del Trapanese, scuola e strada messe in sicurezza, nessuna vittima visibile; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "sciopero-tramvia-firenze-10-ottobre-2026-fasce-garantite",
        "titolo": "Sciopero tramvia a Firenze oggi: orari e fasce garantite",
        "sommario": "Lo stop aziendale proclamato da Cobas dura 24 ore e può causare ritardi o cancellazioni sulle linee T1 e T2. Servizio garantito in due finestre.",
        "categoria": "Trasporti", "luogo": "Firenze", "formato": "flash",
        "parole_chiave_titolo": ["sciopero tramvia Firenze", "fasce garantite"],
        "dati_chiave": [{"valore": "24 ore", "etichetta": "durata dello sciopero"}, {"valore": "6:30-9:30", "etichetta": "prima fascia garantita"}, {"valore": "17:00-20:00", "etichetta": "seconda fascia garantita"}],
        "paragrafi": [
            "Oggi, sabato 10 ottobre, la tramvia di Firenze è interessata da uno sciopero aziendale di 24 ore proclamato da Cobas. GEST avverte che sulle linee T1 e T2 possono verificarsi ritardi e cancellazioni.",
            "Le fasce di garanzia sono dalle 6:30 alle 9:30 e dalle 17:00 alle 20:00. Al di fuori di queste finestre la regolarità del servizio dipende dal numero di lavoratori che aderisce allo sciopero.",
            "L'azienda ricorda che nell'ultima agitazione proclamata dalla stessa organizzazione l'adesione era stata del 3,25%. Il dato è solo un precedente: non permette di prevedere l'impatto effettivo della protesta odierna.",
            "Tra le motivazioni elencate figurano turni, relazioni industriali, ricollocamento del personale non più idoneo alla guida, manutenzione e pulizia dei mezzi, sicurezza dell'esercizio e voci retributive.",
            "Chi deve raggiungere stazione, aeroporto, Careggi o Villa Costanza dovrebbe controllare il servizio poco prima di partire e considerare un margine aggiuntivo, soprattutto nelle ore non protette.",
            "GEST invita a consultare i pannelli elettronici alle fermate, il proprio sito e i canali social ufficiali. Le informazioni possono cambiare nel corso della giornata in base all'adesione e alla disponibilità dei tram.",
        ],
        "fonti": [{"url": "https://www.gestramvia.it/10-ottobre-sciopero-aziendale-di-24-ore-indetto-da-cobas/", "nome": "GEST — durata, linee coinvolte e fasce garantite dello sciopero."}],
        "image_source": "tramvia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un tram fermo a Firenze durante lo sciopero; scena non documentaria.",
        "image_prompt": "Tram moderno fermo a Firenze durante lo sciopero, Santa Maria Novella riconoscibile, luce del mattino; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "treni-10-ottobre-stop-pisciotta-sapri-ritardi-bitetto-sicilia",
        "titolo": "Treni oggi, stop Pisciotta-Sapri e ritardi fino a 90 minuti a Bitetto",
        "sommario": "RFI segnala la sospensione sulla Salerno-Paola, forti rallentamenti sulla Bari-Taranto e variazioni per maltempo su tre linee siciliane.",
        "categoria": "Trasporti", "luogo": "Sud Italia", "formato": "flash",
        "parole_chiave_titolo": ["treni oggi", "Pisciotta Sapri"],
        "dati_chiave": [{"valore": "dalle 5:00", "etichetta": "stop Pisciotta-Sapri"}, {"valore": "fino a 90 min", "etichetta": "ritardi a Bitetto"}, {"valore": "3 linee", "etichetta": "riprogrammate in Sicilia"}],
        "paragrafi": [
            "Mattinata difficile per chi viaggia in treno nel Sud. RFI segnala che sulla Salerno-Paola la circolazione resta sospesa tra Pisciotta e Sapri dalle 5 per un inconveniente alla linea elettrica di alimentazione.",
            "I tecnici sono al lavoro e l'offerta ferroviaria è in corso di riprogrammazione. L'ultimo aggiornamento ufficiale delle 7:40 non indicava ancora un orario di ripresa: i viaggiatori devono verificare il proprio treno prima di raggiungere la stazione.",
            "Sulla Bari-Taranto la circolazione è fortemente rallentata in prossimità di Bitetto. Alle 8 RFI indicava ritardi fino a 90 minuti, oltre a variazioni e cancellazioni, con l'intervento tecnico ancora in corso.",
            "In Sicilia l'allerta meteo comporta variazioni, limitazioni e cancellazioni sulle linee Catania-Caltanissetta, Siracusa-Caltanissetta e Palermo-Trapani. La riprogrammazione riguarda l'intera giornata del 10 ottobre.",
            "I tre disagi hanno cause diverse: guasto alla linea elettrica nel Cilento, inconveniente tecnico nel Barese e misure preventive legate al maltempo in Sicilia. Non vanno quindi letti come un unico blocco della rete meridionale.",
            "La situazione è evolutiva. Prima della partenza è consigliabile controllare i monitor di stazione e i canali Infomobilità di RFI e Trenitalia, evitando di fare affidamento sugli orari ordinari se il viaggio attraversa i tratti coinvolti.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/aggiornamenti/2026/10/10/linea-salerno--paola--dalle-ore-05-00-circolazione-ferroviaria-s.html", "nome": "RFI — sospensione tra Pisciotta e Sapri e aggiornamenti tecnici."}, {"url": "https://www.rfi.it/", "nome": "RFI Infomobilità — aggiornamenti del 10 ottobre per Puglia e Sicilia."}],
        "image_source": "treni", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di tecnici su una linea ferroviaria costiera sotto la pioggia; non è una foto dell'evento.",
        "image_prompt": "Treno fermo e tecnici sulla linea elettrica lungo la costa cilentana sotto la pioggia; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "richiamo-casera-dop-pezzente-lucano-ecoli-salmonella-lotti",
        "titolo": "Richiamo alimentare: Casera DOP e salume lucano, i lotti da controllare",
        "sommario": "Il Ministero della Salute segnala un rischio microbiologico per E. coli STEC e Salmonella. I prodotti interessati non devono essere consumati.",
        "categoria": "Salute", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["richiamo alimentare", "Casera DOP"],
        "dati_chiave": [{"valore": "220726", "etichetta": "lotto del formaggio"}, {"valore": "63/26", "etichetta": "lotto del salume"}, {"valore": "2 prodotti", "etichetta": "richiami microbiologici"}],
        "paragrafi": [
            "Il Ministero della Salute ha pubblicato due richiami per rischio microbiologico. Riguardano Valtellina Casera DOP per presenza di Escherichia coli STEC e pezzente della montagna materana per Salmonella spp.",
            "Il formaggio appartiene al lotto 220726. Le confezioni porzionate a marchio Zanetti sono pezzi da due chilogrammi con termini minimi di conservazione 27 ottobre, 4 e 30 novembre, 7 e 21 dicembre 2026.",
            "Lo stesso lotto è stato venduto anche in forme intere senza marchio, con termini minimi di conservazione 12 ottobre 2026 e 24 luglio 2027. Il produttore indicato è l'Azienda Agricola Negrini di Caspoggio, in provincia di Sondrio.",
            "Il salume interessato è il pezzente della montagna materana a marchio Salumi Tipici Lucani. È venduto sottovuoto in confezioni da circa 300 grammi, lotto 63/26, con termine minimo di conservazione 8 marzo 2027.",
            "Chi possiede uno dei prodotti con i dati indicati non deve consumarlo. La raccomandazione diffusa con gli avvisi è di restituirlo al punto vendita, conservando confezione o informazioni del lotto per il controllo.",
            "Il richiamo è circoscritto ai lotti elencati e non riguarda automaticamente tutti i prodotti dello stesso tipo o marchio. In caso di dubbi è opportuno confrontare attentamente lotto, formato e data presenti sull'etichetta.",
        ],
        "fonti": [{"url": "https://www.salute.gov.it/new/it/avvisi/avvisi-e-richiami-di-prodotti-alimentari/", "nome": "Ministero della Salute — portale ufficiale degli avvisi e richiami alimentari."}, {"url": "https://ilfattoalimentare.it/richiamo-pezzente-casera.html", "nome": "Il Fatto Alimentare — dettaglio di lotti, formati e termini di conservazione."}],
        "image_source": "richiami", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di formaggio e salume sottoposti a controllo alimentare; scena non documentaria.",
        "image_prompt": "Formaggio stagionato e salume sottovuoto durante un controllo di sicurezza alimentare, nessun marchio leggibile; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "uragano-isaias-florida-landfall-blackout-alluvioni-10-ottobre",
        "titolo": "Uragano Isaias sulla Florida: oltre mezzo milione senza corrente",
        "sommario": "La tempesta è arrivata vicino a Destin come categoria 2 e si è indebolita a categoria 1. Restano rischi di mareggiata e alluvioni verso Alabama e Tennessee.",
        "categoria": "Mondo", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["uragano Isaias", "Florida"],
        "dati_chiave": [{"valore": "105 mph", "etichetta": "vento al landfall"}, {"valore": "590.000+", "etichetta": "utenze senza corrente stimate"}, {"valore": "categoria 1", "etichetta": "forza dopo il landfall"}],
        "paragrafi": [
            "L'uragano Isaias ha toccato terra vicino a Destin, nel Panhandle della Florida, come tempesta di categoria 2. Il National Hurricane Center ha indicato venti massimi sostenuti di 105 miglia orarie al momento dell'arrivo sulla costa.",
            "Nelle ore successive Isaias si è indebolito a categoria 1, con venti intorno a 90 miglia orarie. Il calo di intensità non elimina il pericolo: mareggiata, piogge torrenziali e alluvioni improvvise restano possibili lungo la traiettoria interna.",
            "Le rilevazioni citate da Reuters indicavano quasi 380 mila utenze senza elettricità in Florida e oltre 210 mila in Alabama. Il numero può variare rapidamente con i guasti e i ripristini delle squadre tecniche.",
            "Le autorità hanno chiesto ai residenti di restare al riparo e di non mettersi in strada. Alberi caduti, linee elettriche danneggiate e ponti o strade temporaneamente chiusi rendono rischiosi gli spostamenti anche lontano dalla costa.",
            "Il sistema è atteso attraverso l'Alabama e poi verso la Tennessee Valley. Le previsioni indicano che dovrebbe perdere ulteriore forza sulla terraferma, continuando però a trasportare molta pioggia nel Sud-Est degli Stati Uniti.",
            "I dati descrivono la situazione della notte e possono essere aggiornati dal centro uragani. Per le aree coinvolte contano gli ordini locali di evacuazione o riparo, non la sola categoria numerica della tempesta.",
        ],
        "fonti": [{"url": "https://www.reuters.com/business/environment/category-3-hurricane-isaias-makes-landfall-near-destin-florida-nhc-says-2026-10-10/", "nome": "Reuters — aggiornamenti NHC, traiettoria e interruzioni elettriche."}, {"url": "https://apnews.com/article/hurricane-isaias-landfall-gulf-alabama-mississippi-919a46d4bd705726b4e57f18ce677ac5", "nome": "Associated Press — landfall, venti e misure di emergenza."}],
        "image_source": "isaias", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica dell'uragano Isaias sulla costa della Florida; non è una foto dell'evento.",
        "image_prompt": "Uragano sul Panhandle della Florida con mareggiata e palme piegate, nessuna vittima visibile; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "uragano-simon-categoria-2-messico-jalisco-piogge-evacuazioni",
        "titolo": "Uragano Simon verso il Messico: evacuazioni e scuole chiuse in Jalisco",
        "sommario": "La tempesta ha raggiunto la categoria 2 e può rafforzarsi ancora. Allarme per inondazioni e frane lungo la costa pacifica del Paese.",
        "categoria": "Mondo", "luogo": "Messico", "formato": "flash",
        "parole_chiave_titolo": ["uragano Simon", "Messico"],
        "dati_chiave": [{"valore": "categoria 2", "etichetta": "intensità raggiunta"}, {"valore": "100 mph", "etichetta": "venti massimi stimati"}, {"valore": "22 comuni", "etichetta": "scuole sospese in Jalisco"}],
        "paragrafi": [
            "L'uragano Simon si è rafforzato fino alla categoria 2 mentre si avvicina alla costa pacifica del Messico. Il National Hurricane Center ha stimato venti massimi prossimi a 100 miglia orarie e un'ulteriore intensificazione possibile.",
            "Sono in vigore avvisi di uragano per tratti della costa centrale e sud-occidentale. Le piogge più intense possono interessare Jalisco e parti di Michoacán, Colima e Nayarit, con rischio di inondazioni improvvise e frane.",
            "Il governo del Jalisco ha sospeso le lezioni venerdì e lunedì in 22 comuni costieri. Sono inoltre iniziate evacuazioni dalle aree più esposte e il settore turistico di Puerto Vallarta è stato invitato a predisporre rifugi o zone sicure.",
            "Al momento dell'aggiornamento Simon si trovava circa 335 chilometri a sud di Manzanillo e 500 chilometri a sud-sud-est di Cabo Corrientes. La traiettoria è stata descritta come irregolare dalle autorità locali.",
            "Anche Guerrero ha sospeso lezioni e attività non essenziali in alcune aree. Ad Acapulco diverse strade sono state allagate, ma la governatrice Evelyn Salgado non aveva segnalato vittime nel primo bilancio.",
            "La categoria misura soprattutto il vento e non riassume tutti i rischi. Chi si trova lungo la costa deve evitare spiagge e corsi d'acqua, seguire gli ordini locali e considerare che piogge e mareggiate possono precedere l'arrivo del centro della tempesta.",
        ],
        "fonti": [{"url": "https://apnews.com/article/hurricane-simon-mexico-pacific-733c6a028547ee832c885274cf11589e", "nome": "Associated Press — dati NHC, evacuazioni e sospensioni in Messico."}],
        "image_source": "simon", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica dell'uragano Simon vicino alla costa pacifica messicana; non è una foto dell'evento.",
        "image_prompt": "Grande uragano sul Pacifico davanti alla costa del Jalisco, pioggia sulla città e nessuna vittima visibile; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "trump-putin-accordo-diesel-russo-usa-sanzioni-licenza-135",
        "titolo": "Trump annuncia diesel russo negli USA: sanzioni allentate fino ad aprile",
        "sommario": "La licenza 135 del Tesoro autorizza temporaneamente vendita e importazione del carburante. Mosca promette oltre 300 mila tonnellate subito, ma l'effetto sui prezzi è incerto.",
        "categoria": "Mondo", "luogo": "Washington", "formato": "flash",
        "parole_chiave_titolo": ["diesel russo", "sanzioni USA"],
        "dati_chiave": [{"valore": "300.000+ t", "etichetta": "prima fornitura annunciata"}, {"valore": "2,25 mln barili", "etichetta": "equivalente stimato"}, {"valore": "7 aprile", "etichetta": "scadenza della licenza"}],
        "paragrafi": [
            "Donald Trump ha annunciato un accordo con Vladimir Putin per immettere diesel russo nei mercati statunitensi e internazionali. Nelle stesse ore il Tesoro americano ha emesso la licenza generale 135, che autorizza temporaneamente operazioni sul carburante di origine russa.",
            "Secondo Trump, la prima fornitura supera le 300 mila tonnellate, equivalenti a circa 2,25 milioni di barili. Il presidente ha inoltre indicato 500 mila tonnellate a novembre e un ulteriore milione in una fase successiva.",
            "La licenza dell'Office of Foreign Assets Control copre vendita, consegna, scarico e importazione di diesel russo. Reuters riferisce che la finestra autorizzata resta aperta fino al 7 aprile.",
            "La decisione attenua una parte delle restrizioni adottate contro il settore energetico russo per ridurre le entrate di Mosca durante la guerra in Ucraina. Il presidente ucraino Volodymyr Zelensky e alcuni parlamentari statunitensi hanno criticato l'accordo.",
            "L'impatto sui prezzi non è automatico. Gli Stati Uniti esportano normalmente circa 1,5 milioni di barili di diesel al giorno e analisti citati da Reuters considerano i volumi iniziali insufficienti per una riduzione duratura delle quotazioni.",
            "La notizia riguarda una deroga delimitata, non la cancellazione generale delle sanzioni alla Russia. Per valutarne gli effetti serviranno consegne effettive, capacità delle raffinerie russe e andamento del mercato globale dei carburanti.",
        ],
        "fonti": [{"url": "https://ofac.treasury.gov/recent-actions/20261009_33", "nome": "OFAC — emissione ufficiale della licenza generale 135 sul diesel russo."}, {"url": "https://www.reuters.com/business/energy/trump-big-announcement-coming-up-diesel-2026-10-09/", "nome": "Reuters — volumi annunciati, durata della deroga e valutazioni di mercato."}],
        "image_source": "diesel", "image_sensitive": True, "image_reenacted": True, "image_likeness": "Donald Trump e Vladimir Putin",
        "image_alt": "Scena concettuale IA ultrarealistica con Donald Trump e Vladimir Putin in un incontro sull'energia; non raffigura un incontro realmente avvenuto.",
        "image_prompt": "Donald Trump e Vladimir Putin a un tavolo istituzionale in una scena concettuale sul diesel, nessuna firma o stretta di mano; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "attacco-aeroporto-riyadh-tre-morti-voli-cancellati-houthi",
        "titolo": "Attacco all'aeroporto di Riyadh: tre morti e voli sospesi",
        "sommario": "L'autorità saudita conferma due attacchi contro lo scalo King Khalid e un aereo Saudia. Gli Houthi rivendicano, ma Riad non attribuisce ufficialmente la responsabilità.",
        "categoria": "Mondo", "luogo": "Arabia Saudita", "formato": "flash",
        "parole_chiave_titolo": ["aeroporto Riyadh", "tre morti"],
        "dati_chiave": [{"valore": "3", "etichetta": "cittadini sauditi morti"}, {"valore": "2 obiettivi", "etichetta": "aeroporto e aereo"}, {"valore": "9 ottobre", "etichetta": "conferma dell'autorità"}],
        "paragrafi": [
            "Tre cittadini sauditi sono morti e altre persone sono rimaste ferite nell'attacco contro l'aeroporto internazionale King Khalid di Riyadh e un aereo della compagnia Saudia. Il bilancio è stato confermato dall'Autorità generale dell'aviazione civile saudita.",
            "L'autorità ha parlato di due attacchi distinti, uno diretto allo scalo e uno al velivolo, senza indicare il tipo di arma impiegata né attribuire ufficialmente la responsabilità.",
            "I ribelli Houthi dello Yemen hanno rivendicato un lancio con missile balistico contro l'aeroporto. La rivendicazione resta separata dalla conferma saudita: al momento non è stata accompagnata da una verifica indipendente pubblica.",
            "L'episodio ha avuto effetti immediati sui collegamenti. FlyDubai ha cancellato temporaneamente i voli per Riyadh e Yanbu fino a sabato e per Abha fino a domenica; Pakistan International Airlines ha sospeso i voli verso Riyadh.",
            "Chi deve transitare dallo scalo o volare verso l'Arabia Saudita dovrebbe verificare direttamente con la compagnia e con l'aeroporto prima di partire. Le riprotezioni dipendono dal singolo vettore e dall'evoluzione delle misure di sicurezza.",
            "La situazione si inserisce nella nuova fase di scontri tra gli Houthi sostenuti dall'Iran e le forze appoggiate dall'Arabia Saudita. Eventuali aggiornamenti su responsabili, numero dei feriti e ripresa dei voli richiedono conferme ufficiali ulteriori.",
        ],
        "fonti": [{"url": "https://apnews.com/article/saudi-houthis-airport-attack-mideast-october-9-2026-4aba968d517041a89ae2284f0e00bd87", "nome": "Associated Press — conferma dell'autorità saudita, rivendicazione e voli sospesi."}],
        "image_source": "riyadh", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica dell'aeroporto King Khalid di Riyadh dopo un allarme di sicurezza; non è una foto dell'attacco.",
        "image_prompt": "Aeroporto King Khalid di Riyadh di notte con mezzi di emergenza dopo un incidente di sicurezza, nessuna esplosione o vittima; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "stati-uniti-sanzioni-corte-penale-internazionale-sei-mesi",
        "titolo": "Gli USA sanzionano la Corte penale internazionale: sei mesi di tregua operativa",
        "sommario": "Washington vieta le transazioni con la Corte, ma introduce un periodo iniziale per adeguarsi e alcune esenzioni. CPI e Unione europea contestano la misura.",
        "categoria": "Mondo", "luogo": "L'Aia", "formato": "flash",
        "parole_chiave_titolo": ["sanzioni USA", "Corte penale internazionale"],
        "dati_chiave": [{"valore": "6 mesi", "etichetta": "periodo iniziale di adeguamento"}, {"valore": "2002", "etichetta": "anno di nascita della Corte"}, {"valore": "70+", "etichetta": "mandati emessi nella sua storia"}],
        "paragrafi": [
            "Gli Stati Uniti hanno imposto sanzioni alla Corte penale internazionale come istituzione, estendendo la pressione già esercitata in passato contro singoli magistrati e funzionari. La misura vieta le transazioni con la Corte e può colpire imprese che le forniscono servizi.",
            "Il Tesoro ha previsto un periodo iniziale di sei mesi per l'adeguamento. Restano inoltre alcune eccezioni per telecomunicazioni, software, pensioni e operazioni legate alle persone detenute.",
            "Il segretario di Stato Marco Rubio ha motivato la decisione con la volontà di impedire che la CPI persegua cittadini e personale statunitense. Washington non ha ratificato lo Statuto di Roma che ha istituito la Corte.",
            "La CPI ha respinto le sanzioni e ha dichiarato che il proprio lavoro continuerà. L'Alto rappresentante dell'Unione europea Kaja Kallas ha definito i sei mesi una finestra per il dialogo, ricordando che l'UE dispone di strumenti per sostenere la Corte.",
            "Le restrizioni possono incidere su banche, assicurazioni, fornitori tecnologici e altri servizi essenziali. Proprio per ridurre questa vulnerabilità, la Corte aveva già preparato soluzioni alternative per software, pagamenti e coperture sanitarie.",
            "Il provvedimento è più ampio delle precedenti designazioni individuali, ma il periodo transitorio evita un blocco immediato completo. Gli effetti concreti dipenderanno dalle regole applicative, dalle eventuali modifiche statunitensi e dalle contromisure dei Paesi membri.",
        ],
        "fonti": [{"url": "https://www.icc-cpi.int/", "nome": "Corte penale internazionale — risposta ufficiale alle sanzioni statunitensi del 9 ottobre."}, {"url": "https://www.reuters.com/world/us-imposes-sanctions-international-criminal-court-hours-after-former-judge-wins-2026-10-09/", "nome": "Reuters — portata delle sanzioni, esenzioni e periodo di sei mesi."}],
        "image_source": "cpi", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica della sede della Corte penale internazionale all'Aia con bandiere statunitense ed europee; scena non documentaria.",
        "image_prompt": "Sede della Corte penale internazionale all'Aia con bandiera USA in primo piano e bandiere europee, atmosfera istituzionale; logo CurioMondo circolare in post-produzione.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 18, 31, 45, 60, 76, 93, 111, 130)
    images, written = [], []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base - timedelta(minutes=minutes)
        set_published(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"notte-mattina-v{VERSION}", "date": base.date().isoformat(),
        "release_date": base.date().isoformat(), "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
