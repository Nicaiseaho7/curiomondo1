#!/usr/bin/env python3
"""Pacchetto editoriale verificato del 22 settembre 2026."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
import sys

from lxml import html, etree
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
GENERATED = ROOT.parent / "generated_images"
VERSION = 520
CAPTION = site.CAPTION

STORIES = [
    dict(slug="italia-oro-staffetta-mista-mondiali-ciclismo-montreal-2026", titolo="Mondiali di ciclismo, primo oro italiano nella staffetta mista", sommario="A Montréal Ganna, Cattaneo, Sobrero, Guazzini, Longo Borghini e Trinca Colonel precedono Francia e Svizzera.", categoria="Sport", luogo="Montréal", formato="flash", image="exec-74a63a90-8c5f-455f-97d5-a03e587d4097.png", alt="Illustrazione IA del terzetto femminile azzurro nella prova a Montréal; non è una fotografia della gara.", stats=[("51′32″28", "tempo dell’Italia"), ("8″63", "vantaggio sulla Francia"), ("19″90", "vantaggio sulla Svizzera")], body=[
        "L’Italia ha vinto il 22 settembre a Montréal la cronometro a squadre miste dei Mondiali di ciclismo su strada. Mattia Cattaneo, Filippo Ganna e Matteo Sobrero hanno affrontato la prima parte della prova; Vittoria Guazzini, Elisa Longo Borghini e Monica Trinca Colonel hanno completato il percorso. Il tempo finale è di 51 minuti, 32 secondi e 28 centesimi.",
        "La Francia ha chiuso a 8 secondi e 63 centesimi, la Svizzera a 19 secondi e 90 centesimi. La prova misurava 40,6 chilometri, ripartiti fra i tre uomini e le tre donne. La classifica premia il tempo complessivo della nazionale, non sei gare individuali separate.",
        "Per l’Italia è il primo titolo mondiale nella specialità. Nei precedenti appuntamenti iridati la nazionale aveva conquistato l’argento nel 2022 e il bronzo nel 2021 e nel 2024. Il successo aggiunge un oro al bilancio azzurro dei Mondiali canadesi, iniziati il 20 settembre.",
        "Ganna era già salito sul podio della cronometro individuale maschile di questa edizione, secondo alle spalle di Remco Evenepoel. Nella gara mista il risultato dipende invece dall’equilibrio delle due frazioni e dalla tenuta del terzetto finale fino al traguardo."
    ], sources=[("https://cyclingpro.net/spaziociclismo/montreal-2026/mondiali-montreal-2026-oro-italia-nella-cronostaffetta-mista-ganna-cattaneo-sobrero-guazzini-trinca-colonel-e-longo-borghini-fanno-limpresa/", "SpazioCiclismo — risultato, percorso e componenti della squadra, 22 settembre 2026."), ("https://www.cicloweb.it/news/292652748294/mondiali-2026-mixed-relay-l-italia-centra-l-oro-a-montreal", "Cicloweb — cronaca e precedenti azzurri, 22 settembre 2026."), ("https://www.uci.org/race-hub/2026-uci-road-world-championships/4VE2IVYHHB9zxSIC1CEhb9", "UCI — programma ufficiale dei Mondiali di Montréal 2026.")], primary="sport", priority=95),
    dict(slug="enisa-2026-pubblica-amministrazione-32-percento-attacchi-informatici", titolo="Attacchi informatici nell’UE, la PA è il settore più colpito", sommario="Nel rapporto ENISA sugli eventi del 2025 la pubblica amministrazione compare nel 32% dei casi. Il ransomware ha il maggiore impatto a breve termine.", categoria="Tecnologia", luogo="Unione europea", formato="flash", image="exec-f6ecbac5-7e8c-423a-87e6-0c07908f9477.png", alt="Illustrazione IA di personale in un ufficio pubblico davanti a un sistema di sicurezza informatica; scena non documentaria.", stats=[("32%", "eventi che riguardano la PA"), ("82%", "attacchi DDoS negli eventi della PA"), ("2025", "periodo osservato")], body=[
        "La pubblica amministrazione è il settore più colpito negli eventi informatici analizzati dall’ENISA per il 2025 nell’Unione europea. Nel rapporto pubblicato il 22 settembre 2026 compare nel 32% dei casi suddivisi per settore. La quota descrive la distribuzione degli eventi raccolti dall’agenzia, non la probabilità che ogni singolo ente venga attaccato.",
        "Fra gli episodi che hanno riguardato le amministrazioni, l’82% è costituito da attacchi DDoS motivati soprattutto da ragioni ideologiche. Il dato aiuta a leggere il primato del settore: nel campione sono numerose le azioni mirate a interrompere la disponibilità di servizi digitali, anche quando il danno del singolo evento è limitato.",
        "L’agenzia considera il ransomware la minaccia con il maggiore impatto nel breve periodo, perché può bloccare le attività e coinvolgere dati e sistemi. Gli attacchi DDoS, invece, sono la categoria più frequente nell’intero periodo osservato: rappresentano il 51% dei casi registrati. Frequenza e gravità sono dunque misure diverse.",
        "L’analisi copre gli eventi dal 1° gennaio al 31 dicembre 2025 e integra fonti aperte con informazioni condivise in forma anonima dagli Stati membri e dai partner dell’agenzia. Tra le altre categorie più esposte figurano servizi alle imprese e trasporti, entrambi all’8%."
    ], sources=[("https://www.enisa.europa.eu/news/exploring-the-evolution-of-the-cyber-threat-landscape-how-dependencies-weaken-our-digital-resilience", "ENISA — comunicato sul rapporto Threat Landscape 2026, 22 settembre 2026."), ("https://www.enisa.europa.eu/topics/cyber-threats/threat-landscape", "ENISA — rapporti e metodologia sul panorama delle minacce.")], primary="tecnologia", priority=92),
    dict(slug="iea-elettrificazione-importazioni-combustibili-400-miliardi-2035", titolo="IEA: più elettrificazione può ridurre la spesa per i combustibili importati", sommario="Nello scenario accelerato i Paesi importatori potrebbero spendere oltre 400 miliardi di dollari in meno nel 2035 rispetto al 2025.", categoria="Economia", luogo="Parigi", formato="flash", image="exec-a047eb5f-9569-48e7-abc4-79735836fa3f.png", alt="Illustrazione IA di reti elettriche e ricarica vicino a un porto commerciale; non è una fotografia del rapporto IEA.", stats=[(">400 mld $", "possibile risparmio sulle importazioni"), ("2035", "orizzonte dello scenario"), ("33%", "quota elettrica ottenibile a costi competitivi")], body=[
        "I Paesi che importano combustibili potrebbero ridurre di oltre 400 miliardi di dollari la spesa annua per le importazioni energetiche entro il 2035, rispetto ai livelli del 2025, se accelerassero sensibilmente l’elettrificazione. È uno scenario dell’Agenzia internazionale dell’energia presentato il 22 settembre, non un risparmio già conseguito né una previsione incondizionata.",
        "Con tecnologie oggi disponibili e prezzi dell’energia precedenti all’attuale shock delle forniture, l’elettricità potrebbe coprire in modo economicamente competitivo il 33% dei consumi finali mondiali nel 2035, contro il 23% odierno. La stima è vicina all’obiettivo del 35% discusso in sede internazionale.",
        "Nello stesso scenario accelerato, la domanda mondiale di petrolio potrebbe essere inferiore di 18 milioni di barili al giorno rispetto a quella che si avrebbe senza una diffusione più rapida delle tecnologie elettriche. La differenza dipenderebbe soprattutto dall’adozione dei veicoli elettrici.",
        "Il beneficio non arriva automaticamente con l’aumento della domanda di elettricità. L’IEA indica investimenti nella produzione e nelle reti, sistemi più flessibili e attenzione ai costi iniziali per famiglie e imprese. Confrontare spesa potenziale e investimenti necessari è essenziale per valutare le scelte di ciascun Paese."
    ], sources=[("https://www.iea.org/news/electrification-takes-centre-stage-as-hormuz-shock-spurs-countries-to-seek-to-enhance-energy-security", "IEA — analisi sull’elettrificazione, 22 settembre 2026."), ("https://www.iea.org/reports/electrification", "IEA — rapporto speciale sull’elettrificazione.")], primary="economia", priority=88),
    dict(slug="michael-kayode-prima-convocazione-nazionale-serie-d-premier-2026", titolo="Kayode alla prima convocazione azzurra: dalla Serie D alla Premier", sommario="Il difensore del Brentford ripercorre il passaggio da Gozzano a Fiorentina e Inghilterra nella conferenza di Coverciano.", categoria="Sport", luogo="Coverciano", formato="flash", image="exec-2af167b2-0bc2-4f6f-b326-e44e258d3484.png", alt="Ritratto editoriale IA di Michael Kayode in una conferenza stampa azzurra; non è una fotografia dell’incontro.", stats=[("22 anni", "età del difensore"), ("2023", "titolo europeo Under 19"), ("2025", "arrivo al Brentford")], body=[
        "Michael Kayode ha raccontato il 22 settembre a Coverciano il percorso che lo ha portato alla prima convocazione nella Nazionale maggiore. Il difensore del Brentford è passato dal Gozzano in Serie D alla Fiorentina, prima di approdare in Premier League. Ha indicato nella continuità di gioco una parte decisiva della propria crescita.",
        "Nato nel 2004 a Borgomanero, Kayode era cresciuto nel vivaio della Juventus. A 16 anni il passaggio al Gozzano gli ha consentito di giocare fra i senior. Con la Fiorentina ha poi esordito ai massimi livelli italiani e nelle competizioni europee; nel gennaio 2025 si è trasferito al Brentford.",
        "Con l’Italia Under 19 ha vinto l’Europeo del 2023, segnando in finale contro il Portogallo. A Coverciano ha ritrovato Alberto Bollini, oggi nello staff della Nazionale maggiore. Kayode ha spiegato di aver appreso la nuova convocazione dal telefono prima di una partita del suo club.",
        "Fra le caratteristiche citate in conferenza ci sono le rimesse laterali molto lunghe, sulle quali il Brentford lavora con schemi specifici. Il giocatore ha però messo al centro la possibilità di scendere in campo con regolarità e di adattarsi alle richieste tattiche del commissario tecnico."
    ], sources=[("https://www.figc.it/en/national-teams/news/kayode-from-serie-d-to-coverciano-via-the-premier-league-young-players-like-us-can-help-italy-nubq9w86", "FIGC — conferenza di Michael Kayode, 22 settembre 2026."), ("https://www.figc.it/en", "FIGC — notizie e convocazioni della Nazionale.")], primary="sport", priority=72, public=True),
    dict(slug="brothers-apple-tv-debutto-23-settembre-mcconaughey-harrelson-22-09-2026", titolo="“Brothers” arriva su Apple TV il 23 settembre con due episodi", sommario="Matthew McConaughey e Woody Harrelson interpretano versioni romanzate di sé. Otto episodi complessivi, finale previsto il 4 novembre.", categoria="Film e serie TV", luogo="Streaming", formato="flash", image="exec-3cb8cfad-ceba-424e-b54b-de4e179baa6f.png", alt="Ritratto editoriale IA di Matthew McConaughey e Woody Harrelson; non è un fotogramma della serie.", stats=[("23 settembre", "debutto annunciato"), ("2", "episodi alla partenza"), ("4 novembre", "ultimo episodio previsto")], body=[
        "“Brothers”, la commedia con Matthew McConaughey e Woody Harrelson, debutterà su Apple TV mercoledì 23 settembre 2026 con due episodi. La serie conta otto puntate: dopo la partenza, il calendario annunciato prevede una nuova uscita ogni mercoledì fino al 4 novembre.",
        "I due attori interpretano versioni romanzate di sé stessi. Nella trama, la loro amicizia viene sconvolta da un segreto familiare che li porta a chiedersi se siano fratelli. È la premessa narrativa della serie, non un’affermazione biografica sui due interpreti.",
        "La vicenda si sposta nel ranch texano del personaggio interpretato da McConaughey dopo che la famiglia di Harrelson vi arriva per una visita prolungata. Nel cast figurano anche Natalie Martinez, Brittany Ishibashi e Holland Taylor. Lee Eisenberg guida la produzione della commedia.",
        "Il 22 settembre la serie risulta dunque annunciata per il giorno successivo. La programmazione settimanale evita di confondere l’uscita dei primi due episodi con la disponibilità dell’intera stagione. La data è indicata da Apple come debutto globale sulla propria piattaforma."
    ], sources=[("https://www.apple.com/ca/tv-pr/news/2026/06/apple-tvs-new-comedy-series-brothers-starring-matthew-mcconaughey-and-woody-harrelson-to-make-global-debut-on-wednesday-september-23/", "Apple TV Press — calendario e cast della serie, 18 giugno 2026."), ("https://www.apple.com/tv-pr/originals/brothers/", "Apple TV Press — scheda ufficiale di Brothers.")], primary="film-serie-tv", priority=75, public=True),
]

UPDATES = [
    dict(slug="bonus-colonnine-domestiche-2026-domande-dal-22-settembre", image="exec-3c752a9b-0d25-4c0b-861d-6c7bcbbbee8b.png", alt="Illustrazione IA di una colonnina di ricarica domestica installata in un garage; scena non documentaria.", body=[
        "Si è aperto alle 12 del 22 settembre 2026 lo sportello per chiedere il Bonus colonnine domestiche destinato ai privati residenti in Italia e ai condomìni. Le domande si presentano sulla piattaforma Invitalia fino alle 12 del 31 gennaio 2027 per installazioni completate tra il 26 giugno e il 31 dicembre 2026.",
        "Il contributo copre l’80% delle spese ammissibili per acquisto e posa, con un massimo di 1.500 euro per una persona fisica e 8.000 euro per un intervento sulle parti comuni condominiali. Le risorse stanziate per l’annualità 2026 sono 15 milioni di euro.",
        "La domanda si compila online dopo l’installazione, accedendo con SPID, carta d’identità elettronica o carta nazionale dei servizi. Il Ministero delle Imprese e del Made in Italy rimanda alla piattaforma di Invitalia per l’invio e alle istruzioni ufficiali per documentare le spese.",
        "Chi ha in programma un impianto deve verificare il periodo di completamento dei lavori e conservare la documentazione richiesta. La finestra per inoltrare la domanda resta aperta fino alla scadenza indicata, mentre la disponibilità delle risorse va controllata sul portale che gestisce la misura."
    ], sources=[("https://www.mimit.gov.it/it/incentivi/bonus-colonnine-domestiche", "Ministero delle Imprese e del Made in Italy — requisiti, fondi e apertura sportello."), ("https://www.invitalia.it/incentivi-e-strumenti/bonus-colonnine-domestiche", "Invitalia — piattaforma, periodo ammissibile e scadenza.")]),
    dict(slug="ue-rinnova-sanzioni-russia-tre-anni-rimuove-usmanov-fridman-22-settembre-2026", image="exec-2c097726-7850-4b9b-ad0f-8bf1a76bb296.png", alt="Illustrazione IA di una sala di riunione istituzionale europea; non è una fotografia della decisione.", body=[
        "Il Consiglio dell’Unione europea ha approvato il 22 settembre la proroga per tre anni delle sanzioni individuali contro persone ed entità ritenute responsabili di minacciare l’integrità territoriale, la sovranità e l’indipendenza dell’Ucraina. Le misure resteranno in vigore fino al 22 settembre 2029.",
        "Le restrizioni in essere riguardano più di 3.000 persone ed entità. Per le persone fisiche comprendono limitazioni ai viaggi; sono inoltre previsti il congelamento dei beni e il divieto di mettere fondi o altre risorse economiche a disposizione dei soggetti inseriti negli elenchi.",
        "Nel riesame il Consiglio ha deciso di non rinnovare l’iscrizione di tre persone e un’entità e di cancellare tre persone decedute. Reuters riferisce che tra i nomi rimossi figurano Alisher Usmanov e Mikhail Fridman. La decisione istituzionale distingue le singole iscrizioni dall’impianto complessivo delle restrizioni prorogate.",
        "La proroga riguarda gli elenchi individuali legati alla sovranità ucraina. Non modifica automaticamente la durata di tutte le sanzioni economiche settoriali dell’Unione contro la Russia, disciplinate da provvedimenti separati. La novità rispetto alla notizia sull’intesa tra ambasciatori è l’adozione formale comunicata dal Consiglio."
    ], sources=[("https://www.consilium.europa.eu/en/press/press-releases/2026/09/22/ukraine-s-territorial-integrity-eu-extends-individual-listings-for-further-three-years/", "Consiglio UE — decisione formale e durata, 22 settembre 2026."), ("https://www.reuters.com/world/eu-renews-russia-sanctions-drops-russian-billionaires-usmanov-fridman-2026-09-22/", "Reuters — nomi rimossi dagli elenchi, 22 settembre 2026.")]),
]


def variants(slug: str, filename: str) -> list[dict]:
    image = Image.open(GENERATED / filename).convert("RGB")
    w, h = image.size
    target = 1.5
    if w / h > target:
        width = round(h * target)
        left = (w - width) // 2
        image = image.crop((left, 0, left + width, h))
    else:
        height = round(w / target)
        top = (h - height) // 2
        image = image.crop((0, top, w, top + height))
    directory = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        path = directory / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / 1.5)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=86, method=6)
        result.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return result


def update_existing(u: dict, image: dict) -> None:
    path = ROOT / "notizie" / (u["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body): body.remove(child)
    for paragraph in u["body"]: etree.SubElement(body, "p").text = paragraph
    body.set("data-article-format", "flash")
    figure = doc.xpath('//figure[contains(@class,"article-image")]')[0]
    figure.set("data-ai-generated", "true")
    figure.set("data-sensitive-context", "false")
    picture = figure.xpath('./picture')[0]
    old = picture.xpath('./img')[0]
    vv = {v["w"]: v["src"] for v in image["variants"]}
    old.set("src", ".." + vv[800]); old.set("srcset", ", ".join(f"..{vv[w]} {w}w" for w in (480,800,1200)))
    old.set("alt", u["alt"])
    caption = figure.xpath('./figcaption')[0]; caption.text = CAPTION
    canonical = doc.xpath('//link[@rel="canonical"]/@href')[0]
    doc.xpath('//meta[@property="og:image"]')[0].set("content", "https://curiomondo.it" + vv[1200])
    alt = doc.xpath('//meta[@property="og:image:alt"]')
    if alt: alt[0].set("content", u["alt"])
    ld = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(ld.text); schema["image"] = ["https://curiomondo.it" + vv[1200]]
    schema["dateModified"] = datetime.now(site.ROME).replace(microsecond=0).isoformat()
    ld.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    source_section = doc.xpath('//div[contains(@class,"art-sources")]')[0]
    ul = source_section.xpath('./ul')[0]
    for child in list(ul): ul.remove(child)
    for url, title in u["sources"]:
        li = etree.SubElement(ul, "li")
        etree.SubElement(li, "a", href=url, rel="noopener noreferrer", target="_blank").text = title
    p = source_section.xpath('./p/small')
    if p:
        br = p[0].xpath('./br')
        if br and br[0].tail is not None: br[0].tail = f"Testo originale CurioMondo. Ultimo aggiornamento editoriale: 22 settembre 2026."
    path.write_text("<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def main():
    registry = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(registry.read_text(encoding="utf-8"))
    articles = []
    for a in STORIES:
        image = {"alt": a["alt"], "variants": variants(a["slug"], a["image"]), "disclosure": CAPTION, "generator": "OpenAI image tool", "sensitiveContext": False, "key": f"{a['slug']}-v{VERSION}"}
        if a.get("public"): image["syntheticLikeness"] = "public-figure"
        article = {"slug": a["slug"], "titolo": a["titolo"], "sommario": a["sommario"], "categoria": a["categoria"], "luogo": a["luogo"], "formato": a["formato"], "paragrafi": a["body"], "fonti": [{"url": url, "descrizione": title} for url,title in a["sources"]], "dati_chiave": [{"valore": v, "etichetta": t, "icona": "◆"} for v,t in a["stats"]], "parole_chiave_titolo": []}
        if not (ROOT / "notizie" / f"{a['slug']}.html").exists():
            site.write_article(article, image, VERSION)
        articles.append(article)
        data["items"] = [i for i in data["items"] if i.get("article") != f"/notizie/{a['slug']}.html"]
        data["items"].insert(0, {**image, "article": f"/notizie/{a['slug']}.html"})
    for u in UPDATES:
        image = {"alt": u["alt"], "variants": variants(u["slug"], u["image"]), "disclosure": CAPTION, "generator": "OpenAI image tool", "sensitiveContext": False, "key": f"{u['slug']}-v{VERSION}", "article": f"/notizie/{u['slug']}.html"}
        update_existing(u, image)
        data["items"] = [i for i in data["items"] if i.get("article") != image["article"]]
        data["items"].insert(0, image)
    data["version"] = VERSION
    registry.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cfg_path = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    for a in STORIES:
        cfg["articles"][f"/notizie/{a['slug']}.html"] = {"firstPublishedAt": article_time(a["slug"]), "homepagePriority": a["priority"], "primaryCategory": a["primary"]}
    cfg["version"] = VERSION
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces(articles, "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site_version"] = VERSION; manifest["version"] = manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-22", "type": "editorial-news-cycle", "news_added": [a["slug"] for a in STORIES], "news_updated": [a["slug"] for a in UPDATES], "change": "Cinque notizie verificate; aggiornamento bonus colonnine e decisione formale sulle sanzioni UE"}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8"))
            state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION, release_date="2026-09-22", last_update="articoli-verificati-22-settembre-v520")
            if "articleCount" in state: state["articleCount"] += len(STORIES)
            if "generatedEditorialImages" in state: state["generatedEditorialImages"] += len(STORIES) + len(UPDATES)
            path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"added": [a["slug"] for a in STORIES], "updated": [a["slug"] for a in UPDATES]}, ensure_ascii=False))


def article_time(slug):
    doc = html.parse(str(ROOT / "notizie" / f"{slug}.html"))
    return json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)["datePublished"]


if __name__ == "__main__": main()
