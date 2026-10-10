#!/usr/bin/env python3
"""Release v826: meteo di oggi e nove notizie recenti da fonti primarie."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 826
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"
LOGO = ROOT / "curiomondo-logo-512.png"

IMAGE_SOURCES = {
    "meteo": GENERATED / "exec-bb6c9568-ca62-4c82-8e44-da3ab010ebea.png",
    "panama": GENERATED / "exec-832fddf9-6867-4094-91e4-ef17d0b965b8.png",
    "stazioni": GENERATED / "exec-8786ffa8-dce7-4efc-a590-a982ed9cfe66.png",
    "gravidanza": GENERATED / "exec-ee2cfd25-0825-428b-9ef8-f3de314e127c.png",
    "youth": GENERATED / "exec-4df1ccfa-383e-4c2d-aebf-9c9455cf37aa.png",
    "nucleare": GENERATED / "exec-b4ab0814-b313-4db7-9220-5cb8ea2a8042.png",
    "nicaragua": GENERATED / "exec-502bb83a-1996-4519-aaae-f97d8cbddfd6.png",
    "difesa": GENERATED / "exec-d0d366af-e846-4c43-b3cd-2c72d043d1a3.png",
    "lisa": GENERATED / "exec-f33f2499-bd6a-4543-90d8-4f5335bf732d.png",
    "curiosity": GENERATED / "exec-eb0e1a04-f1aa-46b3-afd0-5190f63fa33c.png",
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
    logo = Image.open(LOGO).convert("RGBA")
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        height = round(width / ratio)
        canvas = image.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        logo_size = max(48, round(width * 0.105))
        mark = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        mark.putalpha(mark.getchannel("A").point(lambda value: round(value * 0.92)))
        margin = max(10, round(width * 0.018))
        canvas.alpha_composite(mark, (width - logo_size - margin, height - logo_size - margin))
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        canvas.convert("RGB").save(path, "WEBP", quality=89, method=6)
        variants.append({"w": width, "h": height, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def make_image(article: dict) -> dict:
    image = {
        "key": f"{article['slug']}-v{VERSION}", "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION, "generator": "OpenAI image generation",
        "aiGenerated": True, "documentaryPhoto": False, "officialArtwork": False,
        "sensitiveContext": article.pop("image_sensitive", False), "weatherMap": False,
        "reenactedEvent": article.pop("image_reenacted", False), "logoApplied": True,
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
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "La prudenza è un modo concreto di prendersi cura degli altri.",
        "Dopo una scossa, anche la calma ha bisogno di punti fermi.",
        "Ogni nuova rotta comincia da una domanda ben formulata.",
        "La cura parte spesso da una misura semplice fatta al momento giusto.",
        "Le idee giovani crescono quando trovano spazio nelle decisioni.",
        "Esplorare lontano richiede responsabilità ancora prima che energia.",
        "La diplomazia misura la forza anche nella precisione delle regole.",
        "Semplificare funziona quando non significa smettere di proteggere.",
        "Per ascoltare l'universo servono strumenti capaci di restare immobili.",
        "Un'alba lontana può raccontare una storia antica miliardi di anni.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "allerta-meteo-10-ottobre-campania-calabria-puglia-sicilia",
        "titolo": "Meteo oggi, allerta arancione in quattro regioni del Sud",
        "sommario": "Temporali intensi, raffiche e possibili grandinate interessano Campania, Calabria, Puglia e Sicilia. Allerta gialla anche in altre quattro regioni e in alcuni settori del Centro-Sud.",
        "categoria": "Meteo", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Meteo oggi", "allerta arancione"],
        "dati_chiave": [{"valore": "4 regioni", "etichetta": "con settori in arancione"}, {"valore": "10 ottobre", "etichetta": "giornata dell'allerta"}, {"valore": "8 regioni", "etichetta": "coinvolte dal giallo"}],
        "paragrafi": [
            "Oggi, sabato 10 ottobre, l'allerta arancione riguarda la Sicilia e alcuni settori di Campania, Calabria e Puglia. Il quadro nazionale della Protezione Civile segnala inoltre allerta gialla in Abruzzo, Molise, Basilicata e in parti di Umbria, Lazio, Campania, Calabria e Puglia.",
            "Un'area depressionaria vicina alla Sardegna continua a richiamare correnti umide e instabili da sud-ovest. L'aria risale dallo Stretto di Sicilia verso la Puglia e può alimentare temporali molto intensi sulle regioni meridionali.",
            "Le precipitazioni persistono tra Campania e Calabria e dalla mattina si estendono sulla Puglia. I fenomeni possono essere accompagnati da rovesci forti, raffiche di vento, grandinate locali e frequente attività elettrica.",
            "L'allerta descrive un rischio su aree definite nei bollettini regionali e non significa che ogni comune subirà gli stessi fenomeni. Le criticità idrogeologiche e idrauliche dipendono dall'intensità e dalla durata dei rovesci, oltre che dalle condizioni locali.",
            "Il Dipartimento aggiorna ogni giorno il quadro. Prima di spostarsi conviene consultare gli avvisi della propria Regione e del Comune, evitando sottopassi, corsi d'acqua e zone esposte durante i temporali più intensi.",
        ],
        "fonti": [{"url": "https://www.protezionecivile.gov.it/it/comunicato-stampa/maltempo-allerta-arancione-su-campania-calabria-puglia-e-sicilia/", "nome": "Dipartimento della Protezione Civile — avviso meteo e livelli di allerta del 10 ottobre."}, {"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/", "nome": "Dipartimento della Protezione Civile — bollettino nazionale di criticità e allerta."}],
        "image_source": "meteo", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un forte temporale su una città costiera pugliese; scena non documentaria.",
        "image_prompt": "Temporale autunnale su una città costiera della Puglia, pioggia intensa e raffiche, copertina ultrarealistica con logo CurioMondo applicato in post-produzione.",
    },
    {
        "slug": "terremoto-panama-magnitudo-7-6-pitaloza-arriba-9-ottobre-2026",
        "titolo": "Terremoto di magnitudo 7,6 colpisce il centro di Panama",
        "sommario": "L'USGS localizza l'epicentro a circa dieci chilometri da Pitaloza Arriba e stima una profondità di dieci chilometri. Le misure restano soggette a revisione.",
        "categoria": "Mondo", "luogo": "Panama", "formato": "flash",
        "parole_chiave_titolo": ["Terremoto Panama", "magnitudo 7,6"],
        "dati_chiave": [{"valore": "7,6", "etichetta": "magnitudo USGS"}, {"valore": "10 km", "etichetta": "profondità stimata"}, {"valore": "9 ottobre", "etichetta": "data della scossa"}],
        "paragrafi": [
            "Un forte terremoto è stato registrato nel centro di Panama il 9 ottobre. L'evento rivisto dall'US Geological Survey ha magnitudo 7,6 e un epicentro stimato circa dieci chilometri a ovest-sud-ovest di Pitaloza Arriba.",
            "La profondità indicata dall'USGS è di dieci chilometri. La scossa è avvenuta alle 17:56 UTC, quando in Italia erano le 19:56, e rientra tra gli eventi superficiali capaci di essere avvertiti su un'area ampia.",
            "EarthScope propone una stima lievemente diversa, pari a 7,7 e 12,6 chilometri di profondità. Differenze di pochi decimi sono normali nelle prime analisi perché reti e metodi elaborano segnali differenti e vengono aggiornati con nuovi dati.",
            "Le pagine strumentali confermano quindi la forza dell'evento, ma non sostituiscono i bilanci delle autorità locali. In assenza di dati ufficiali consolidati non è corretto attribuire vittime o danni specifici alla scossa.",
            "Chi si trova nell'area deve seguire le indicazioni della protezione civile panamense e verificare eventuali comunicazioni locali. Dopo un terremoto forte possono verificarsi repliche, anche se non è possibile prevederne con precisione numero e intensità.",
        ],
        "fonti": [{"url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000u18k", "nome": "US Geological Survey — scheda strumentale rivista dell'evento."}, {"url": "https://www.earthscope.org/geophysical-event/m-7-7-earthquake-near-pitaloza-arriba-panama/", "nome": "EarthScope — analisi geofisica indipendente della scossa."}],
        "image_source": "panama", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di controlli dopo un terremoto in una località rurale di Panama; non è una foto dell'evento.",
        "image_prompt": "Operatori controllano lievi danni in una cittadina rurale di Panama dopo un terremoto, ricostruzione ultrarealistica con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "nasa-bando-stazioni-spaziali-commerciali-proposte-dicembre-2026",
        "titolo": "NASA apre il bando per le future stazioni spaziali private",
        "sommario": "Le aziende hanno tempo fino all'8 dicembre per presentare progetti completi di destinazione e trasporto in orbita bassa. I primi contratti sono attesi nella primavera 2027.",
        "categoria": "Scienza", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["NASA", "stazioni spaziali commerciali"],
        "dati_chiave": [{"valore": "8 dicembre", "etichetta": "scadenza delle proposte"}, {"valore": "2+", "etichetta": "contraenti nella fase iniziale"}, {"valore": "primavera 2027", "etichetta": "assegnazioni previste"}],
        "paragrafi": [
            "La NASA ha pubblicato la richiesta finale di proposte per le stazioni spaziali commerciali destinate a operare in orbita terrestre bassa. L'obiettivo è mantenere una presenza statunitense dopo il ritiro della Stazione spaziale internazionale.",
            "Le aziende dovranno presentare entro l'8 dicembre piani credibili per progettare, costruire, collaudare, certificare e gestire destinazioni orbitali. La richiesta comprende anche i servizi di trasporto necessari per l'uso umano.",
            "L'agenzia intende assegnare contratti a prezzo fisso e a più vincitori. Nella fase iniziale saranno selezionati almeno due operatori; in seguito una gara definirà progettazione finale, prove, certificazione e servizi.",
            "Le assegnazioni sono previste nella primavera del 2027. La NASA vuole continuare a svolgere ricerca, sviluppo tecnologico e addestramento degli equipaggi, lasciando però più spazio agli investimenti e ai clienti del settore privato.",
            "Il bando non sceglie ancora una stazione e non garantisce che ogni progetto proposto arriverà in orbita. Apre invece la fase competitiva che dovrà trasformare concetti industriali in strutture certificate per astronauti e attività scientifiche.",
        ],
        "fonti": [{"url": "https://www.nasa.gov/news-release/nasa-seeks-us-industry-plans-for-commercial-space-stations/", "nome": "NASA — richiesta finale di proposte per destinazioni commerciali in orbita bassa."}],
        "image_source": "stazioni", "image_alt": "Illustrazione editoriale IA ultrarealistica di una futura stazione spaziale commerciale in orbita terrestre; scena non documentaria.",
        "image_prompt": "Futura stazione spaziale commerciale in orbita bassa con astronauti e Terra visibile, copertina ultrarealistica con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "oms-roadmap-ipertensione-gravidanza-2035-pre-eclampsia",
        "titolo": "Gravidanza, nuova roadmap OMS contro l'ipertensione",
        "sommario": "I disturbi ipertensivi complicano il 10-15% delle gravidanze e sono associati a circa 42.000 morti materne l'anno. Il piano coordina ricerca, diagnosi e accesso alle cure.",
        "categoria": "Salute", "luogo": "Ginevra", "formato": "flash",
        "parole_chiave_titolo": ["ipertensione in gravidanza", "roadmap OMS"],
        "dati_chiave": [{"valore": "10-15%", "etichetta": "gravidanze interessate"}, {"valore": "42.000", "etichetta": "morti materne stimate l'anno"}, {"valore": "2035", "etichetta": "orizzonte della roadmap"}],
        "paragrafi": [
            "L'Organizzazione mondiale della sanità e i suoi partner hanno lanciato una roadmap globale contro i disturbi ipertensivi della gravidanza, inclusa la pre-eclampsia. Il piano copre il periodo 2026-2035 e indica azioni coordinate per ricerca, diagnosi e cure.",
            "Secondo l'OMS, questi disturbi complicano tra il 10 e il 15% delle gravidanze. Sono associati a circa il 16% delle morti materne nel mondo, pari a una stima di 42.000 decessi ogni anno.",
            "L'impatto riguarda anche i bambini: l'agenzia stima oltre mezzo milione di nati morti e decessi neonatali. In molti Paesi mancano misurazioni affidabili della pressione, test delle proteine nelle urine, farmaci essenziali e sistemi rapidi di invio alle cure.",
            "La roadmap mette insieme linee cliniche, accesso a medicinali e diagnostica, attuazione nei sistemi sanitari, responsabilità pubblica e ricerca. Più di 140 partner hanno individuato venti domande scientifiche prioritarie per orientare i finanziamenti futuri.",
            "Il documento non sostituisce la valutazione del medico. In gravidanza pressione elevata, forte mal di testa, disturbi visivi o dolore addominale richiedono un contatto tempestivo con i servizi sanitari, secondo le indicazioni locali.",
        ],
        "fonti": [{"url": "https://www.who.int/news/item/08-10-2026-new-global-roadmap-launched-to-tackle-hypertension-in-pregnancy-a-leading-cause-of-maternal-and-newborn-deaths", "nome": "OMS — lancio e dati della roadmap globale sull'ipertensione in gravidanza."}, {"url": "https://www.who.int/publications/i/item/9789240128415", "nome": "OMS — roadmap globale 2026-2035 sui disturbi ipertensivi della gravidanza."}],
        "image_source": "gravidanza", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una misurazione della pressione durante una visita in gravidanza; scena non documentaria.",
        "image_prompt": "Medico misura la pressione a una paziente incinta in una clinica moderna, scena rispettosa con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "oms-youth-council-2026-2028-venticinque-organizzazioni-berlino",
        "titolo": "OMS, 25 organizzazioni nel nuovo Consiglio dei giovani",
        "sommario": "Il gruppo 2026-2028 si riunisce per la prima volta a Berlino. Undici organizzazioni entrano nel Consiglio e quattordici confermano la partecipazione.",
        "categoria": "Salute", "luogo": "Berlino", "formato": "flash",
        "parole_chiave_titolo": ["OMS", "Consiglio dei giovani"],
        "dati_chiave": [{"valore": "25", "etichetta": "organizzazioni rappresentate"}, {"valore": "11", "etichetta": "nuovi ingressi"}, {"valore": "2026-2028", "etichetta": "durata del mandato"}],
        "paragrafi": [
            "Il Consiglio dei giovani dell'OMS ha riunito per la prima volta a Berlino i componenti del mandato 2026-2028. Il gruppo comprende referenti di 25 organizzazioni guidate da giovani o impegnate nei servizi per le nuove generazioni.",
            "Undici organizzazioni partecipano per la prima volta, mentre quattordici tornano dal mandato precedente. Le competenze rappresentate spaziano da medicina e infermieristica a salute mentale, HIV, nutrizione, clima e diplomazia sanitaria.",
            "L'incontro del 9 e 10 ottobre serve a definire il metodo di lavoro, il comitato direttivo e i progetti. Tre gruppi si concentrano su educazione sanitaria, accessibilità ed equità, e salute planetaria.",
            "Il comitato direttivo aveva già individuato fino a cinque azioni per rafforzare la governance e tre obiettivi generali. Dopo la riunione, i membri parteciperanno al World Health Summit di Berlino dall'11 al 13 ottobre.",
            "Il Consiglio consiglia il direttore generale e i vertici dell'OMS. Non è un organo decisionale autonomo, ma una piattaforma per portare esperienze giovanili nei programmi e sviluppare nuove iniziative di partecipazione sanitaria.",
        ],
        "fonti": [{"url": "https://www.who.int/news/item/09-10-2026-who-youth-council-welcomes-2026-2028-members-in-berlin", "nome": "OMS — composizione e prima riunione del Youth Council 2026-2028."}],
        "image_source": "youth", "image_alt": "Illustrazione editoriale IA ultrarealistica di giovani leader sanitari riuniti a Berlino; scena non documentaria.",
        "image_prompt": "Giovani leader sanitari internazionali a un tavolo di lavoro a Berlino, copertina ultrarealistica con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "nasa-energia-accordo-nucleare-spazio-reattori-luna-2030",
        "titolo": "NASA e Dipartimento dell'Energia accelerano sul nucleare spaziale",
        "sommario": "Il nuovo accordo copre ricerca, combustibile, test e operazioni. Gli Stati Uniti indicano il 2028 per Space Reactor-1 e il 2030 per un reattore sulla superficie lunare.",
        "categoria": "Scienza", "luogo": "Washington", "formato": "flash",
        "parole_chiave_titolo": ["nucleare spaziale", "NASA"],
        "dati_chiave": [{"valore": "1 novembre", "etichetta": "entrata in vigore"}, {"valore": "2028", "etichetta": "obiettivo Space Reactor-1"}, {"valore": "2030", "etichetta": "obiettivo reattore lunare"}],
        "paragrafi": [
            "La NASA e il Dipartimento dell'Energia degli Stati Uniti hanno firmato un memorandum per accelerare le tecnologie nucleari destinate allo spazio. L'accordo entrerà in vigore il 1° novembre e organizza una collaborazione dall'inizio alla fine dei programmi.",
            "Il quadro comprende ricerca avanzata, produzione del combustibile, test, integrazione con i lanci e operazioni. Le due agenzie indicano la sicurezza come requisito centrale per sistemi a fissione e generatori a radioisotopi.",
            "La NASA prevede il lancio di Space Reactor-1 Freedom nel 2028 e punta a rendere pronto un reattore per la superficie lunare entro il 2030. Questi sistemi dovrebbero fornire energia durante periodi di buio prolungato e a infrastrutture lontane dalla Terra.",
            "Anche la missione Dragonfly verso Titano, prevista al lancio nel 2028, userà un generatore termoelettrico a radioisotopi e 24 unità riscaldanti. La sonda volerà in più località per studiare l'abitabilità della luna di Saturno.",
            "Le date indicate sono obiettivi di programma, non l'annuncio di un reattore già operativo. Sviluppo, collaudi e autorizzazioni dovranno ancora dimostrare prestazioni e sicurezza prima del volo e dell'impiego extraterrestre.",
        ],
        "fonti": [{"url": "https://www.nasa.gov/news-release/nasa-energy-department-advance-new-era-of-nuclear-powered-exploration/", "nome": "NASA — memorandum con il Dipartimento dell'Energia e programmi nucleari spaziali."}],
        "image_source": "nucleare", "image_likeness": "public-figure", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica della firma di un accordo statunitense sul nucleare spaziale; non è una foto dell'evento.",
        "image_prompt": "Funzionari NASA ed energia firmano un accordo con un modello di reattore lunare, ricostruzione ultrarealistica con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "ue-proroga-sanzioni-nicaragua-15-ottobre-2027",
        "titolo": "Nicaragua, l'UE proroga le sanzioni fino a ottobre 2027",
        "sommario": "Le misure riguardano 21 persone e tre entità. Restano il congelamento dei beni, il divieto di mettere fondi a disposizione e, per le persone, il blocco dei viaggi nell'UE.",
        "categoria": "Mondo", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Nicaragua", "sanzioni UE"],
        "dati_chiave": [{"valore": "15 ottobre 2027", "etichetta": "nuova scadenza"}, {"valore": "21 persone", "etichetta": "soggetti elencati"}, {"valore": "3 entità", "etichetta": "organizzazioni interessate"}],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha prorogato di un anno le misure restrittive legate alla situazione in Nicaragua. La nuova scadenza è fissata al 15 ottobre 2027.",
            "L'elenco comprende in totale 21 persone e tre entità. Per tutti vale il congelamento dei beni e cittadini e imprese europee non possono mettere fondi o risorse economiche a loro disposizione.",
            "Le persone elencate sono inoltre soggette a un divieto di viaggio, che impedisce ingresso e transito nei territori dell'Unione. Le misure sono mirate e non equivalgono a un embargo generale contro il Paese.",
            "Il Consiglio collega la decisione alla repressione sistemica attribuita alle autorità nicaraguensi e rinnova la richiesta di liberare i prigionieri politici, ripristinare lo stato di diritto e consentire il ritorno delle organizzazioni internazionali per i diritti umani.",
            "Il quadro sanzionatorio esiste dall'ottobre 2019 ed è riesaminato ogni anno dagli Stati membri. La proroga mantiene quindi in vigore strumenti già applicati, senza aggiungere nuovi nominativi nel comunicato del 9 ottobre.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/nicaragua-council-extends-restrictive-measures-until-october-2027/", "nome": "Consiglio dell'UE — proroga e portata delle misure restrittive sul Nicaragua."}],
        "image_source": "nicaragua", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un corridoio diplomatico europeo con richiami visivi al Nicaragua; scena non documentaria.",
        "image_prompt": "Corridoio diplomatico a Bruxelles con funzionari europei e bandiera del Nicaragua, scena sobria con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "ue-via-libera-regole-industria-difesa-permessi-102-giorni",
        "titolo": "Difesa UE, via libera alle nuove regole su appalti e permessi",
        "sommario": "Il pacchetto Omnibus V semplifica investimenti, trasferimenti e acquisti comuni. Per i progetti di prontezza militare il termine ordinario dei permessi sarà di 102 giorni lavorativi.",
        "categoria": "Mondo", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Difesa UE", "permessi 102 giorni"],
        "dati_chiave": [{"valore": "102 giorni", "etichetta": "termine massimo ordinario"}, {"valore": "3 atti", "etichetta": "componenti del pacchetto"}, {"valore": "2030", "etichetta": "orizzonte della prontezza"}],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha dato il via libera finale a tre atti per semplificare investimenti, appalti e trasferimenti nel settore della difesa. Il pacchetto è chiamato Omnibus V e rientra nell'agenda europea di riduzione degli oneri.",
            "Un regolamento interviene sul Fondo europeo per la difesa e aumenta il sostegno ai progetti che coinvolgono piccole e medie imprese. Un secondo testo crea un quadro comune per accelerare i permessi dei progetti considerati rilevanti per la prontezza militare.",
            "Il termine massimo ordinario per la procedura autorizzativa viene fissato a 102 giorni lavorativi. Se l'autorità competente non decide entro la scadenza, può scattare l'approvazione tacita, salvo eccezioni nazionali per gravi rischi alla salute o alla sicurezza.",
            "Una direttiva facilita i trasferimenti di prodotti per la difesa tra Paesi UE, alza alcune soglie degli appalti e introduce più flessibilità negli accordi quadro e negli acquisti congiunti occasionali.",
            "Il via libera del Consiglio chiude la fase politica europea descritta nel comunicato, ma l'applicazione concreta dipenderà dall'entrata in vigore dei testi e, per la direttiva, dal recepimento nazionale. Le tutele sanitarie e ambientali restano richiamate nel pacchetto.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/simplification-council-gives-final-green-light-to-new-laws-boosting-defence-industry-and-readiness/", "nome": "Consiglio dell'UE — via libera finale al pacchetto Omnibus V sulla difesa."}],
        "image_source": "difesa", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di ministri e tecnici europei riuniti su appalti e industria della difesa; scena non documentaria.",
        "image_prompt": "Ministri e tecnici europei a un tavolo di lavoro a Bruxelles sull'industria della difesa, scena sobria con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "nasa-telescopio-test-lisa-onde-gravitazionali-spazio",
        "titolo": "LISA, NASA ordina il telescopio di prova prima del volo",
        "sommario": "L'unità in vetroceramica sarà l'ultimo passaggio prima dell'hardware destinato alla missione ESA. Tre sonde misureranno onde gravitazionali su lati lunghi 2,5 milioni di chilometri.",
        "categoria": "Scienza", "luogo": "Spazio", "formato": "flash",
        "parole_chiave_titolo": ["LISA", "onde gravitazionali"],
        "dati_chiave": [{"valore": "3 sonde", "etichetta": "costellazione prevista"}, {"valore": "2,5 milioni km", "etichetta": "lunghezza di ogni lato"}, {"valore": "metà anni 2030", "etichetta": "lancio previsto"}],
        "paragrafi": [
            "La NASA ha avviato la realizzazione di una nuova unità di prova per i telescopi della missione LISA, l'osservatorio spaziale guidato dall'Agenzia spaziale europea che cercherà onde gravitazionali a frequenze non accessibili da Terra.",
            "L3Harris progetterà, assemblerà e integrerà l'Engineering Test Unit. Sarà l'ultimo telescopio prima della produzione dell'hardware di volo e incorporerà ciò che i tecnici hanno imparato dai test sul prototipo consegnato nel 2024.",
            "LISA userà tre sonde disposte in un triangolo, con lati lunghi 2,5 milioni di chilometri. I telescopi invieranno e riceveranno laser infrarossi per misurare variazioni di distanza più piccole della larghezza di un atomo di elio.",
            "Ogni telescopio sarà costruito in Zerodur, una vetroceramica stabile a grandi variazioni di temperatura. La missione dovrebbe osservare fusioni di buchi neri massicci e sistemi compatti nella Via Lattea.",
            "Il lancio è previsto a metà degli anni Trenta. La nuova unità non volerà nello spazio: serve a verificare progettazione, montaggio e prestazioni prima della consegna dei telescopi definitivi all'ESA.",
        ],
        "fonti": [{"url": "https://science.nasa.gov/missions/lisa/nasa-advances-lisa-mission-contributions-with-new-test-telescope/", "nome": "NASA Science — nuova unità di prova del telescopio LISA e architettura della missione."}],
        "image_source": "lisa", "image_alt": "Illustrazione editoriale IA ultrarealistica di un tecnico che ispeziona un telescopio in vetroceramica per LISA; scena non documentaria.",
        "image_prompt": "Tecnico in camera pulita ispeziona un telescopio ambrato per LISA, copertina ultrarealistica con logo CurioMondo in post-produzione.",
    },
    {
        "slug": "curiosity-alba-marte-yardang-monte-sharp-panorama-2026",
        "titolo": "Curiosity fotografa l'alba marziana e le scogliere di yardang",
        "sommario": "Il panorama conserva i toni blu del mattino e mostra strutture scolpite dal vento sul Monte Sharp. Il rover ha superato un chilometro di dislivello nel cratere Gale.",
        "categoria": "Scienza", "luogo": "Marte", "formato": "flash",
        "parole_chiave_titolo": ["Curiosity", "alba marziana"],
        "dati_chiave": [{"valore": "6 immagini", "etichetta": "scatti uniti nel panorama"}, {"valore": "16 km", "etichetta": "estensione degli yardang"}, {"valore": "1 km", "etichetta": "dislivello superato dal rover"}],
        "paragrafi": [
            "La NASA ha pubblicato un nuovo panorama di Marte ripreso dal rover Curiosity all'alba. Sei immagini della Mastcam, scattate l'11 agosto alle 8:30 locali, sono state unite mantenendo i colori del primo mattino senza il consueto bilanciamento del bianco.",
            "In primo piano compaiono tonalità bluastre, mentre la luce illumina all'orizzonte gli yardang: scogliere e creste modellate dal vento che gli scienziati attendono di studiare da vicino.",
            "La formazione si estende per circa sedici chilometri sul fianco nord-occidentale del Monte Sharp. Curiosity, che sale la montagna dal 2014, ha appena superato un chilometro di dislivello rispetto al fondo del cratere Gale.",
            "Gli strati del monte registrano fasi diverse della storia marziana. Una delle ipotesi è che gli yardang derivino da ceneri di antiche eruzioni, poi erose dal vento, ma la loro origine non è ancora stabilita.",
            "Il rover dovrebbe raggiungere la base della formazione nel 2027. Lì potrà usare il braccio robotico per misure ravvicinate, mentre nel prossimo anno attraverserà strati ricchi di solfati e carbonati legati all'antico prosciugamento della superficie.",
        ],
        "fonti": [{"url": "https://www.nasa.gov/missions/mars-science-laboratory/curiosity-rover/nasas-curiosity-rover-catches-stunning-martian-dawn/", "nome": "NASA/JPL — panorama dell'alba marziana e avanzamento di Curiosity sul Monte Sharp."}],
        "image_source": "curiosity", "image_alt": "Illustrazione editoriale IA ultrarealistica di Curiosity davanti agli yardang del Monte Sharp all'alba marziana; scena non documentaria.",
        "image_prompt": "Curiosity osserva gli yardang del Monte Sharp all'alba marziana, toni blu del mattino e logo CurioMondo in post-produzione.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 6, 14, 25, 37, 50, 65, 81, 98, 116)
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
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                  "articleCount": int(state.get("articleCount", 0)) + len(written),
                  "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
                  "last_update": f"meteo-ultime-v{VERSION}", "date": base.date().isoformat(),
                  "release_date": base.date().isoformat(), "updated_at": base.isoformat(timespec="seconds"), "status": "ready"})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
