#!/usr/bin/env python3
"""Mazzola, allerta 19 settembre, aggiornamento sanzioni USA firmate."""
from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 438


def save_image_variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets" / "images" / "editorial-auto"
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=86, method=6
        )
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return variants


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


def persist(article: dict, image: dict, published: str) -> str:
    slug = write_article(article, image, VERSION)
    stamp_dates(slug, published)
    article["published"] = published
    register_image(image, slug, VERSION)
    write_json(
        ROOT / "contenuti" / "notizie" / f"{slug}.json",
        {
            "slug": slug,
            "title": article["titolo"],
            "excerpt": article["sommario"],
            "category": article["categoria"],
            "published_at": published,
            "updated_at": published,
            "development_at": "2026-09-19",
            "status": article.get("stato", "UFFICIALE"),
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


def assert_body(article: dict) -> None:
    paras = article["paragrafi"]
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in paras)
    lo, hi = {"flash": (100, 250), "standard": (300, 600), "feature": (800, 1500)}[article["formato"]]
    if not lo <= words <= hi:
        raise SystemExit(f"{article['slug']} {article['formato']} {words} parole")
    for i, p in enumerate(paras, 1):
        n = len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p))
        if n > 60:
            raise SystemExit(f"{article['slug']} p{i} {n} parole")


MAZZOLA = {
    "slug": "sandro-mazzola-morto-83-anni-inter-nazionale-19-settembre-2026",
    "titolo": "Sandro Mazzola è morto: aveva 83 anni, bandiera dell’Inter",
    "sommario": "Lo ha comunicato il club. Quattro scudetti, due Coppe dei Campioni, Europeo 1968. Figlio di Valentino, perso a Superga.",
    "categoria": "Sport",
    "luogo": "Milano",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Mazzola", "Inter"],
    "dati_chiave": [
        {"icona": "◆", "valore": "83", "etichetta": "anni, nato l’8 novembre 1942 a Torino"},
        {"icona": "●", "valore": "565", "etichetta": "partite con l’Inter, 161 gol secondo il club"},
        {"icona": "↗", "valore": "1968", "etichetta": "campione d’Europa con l’Italia"},
    ],
    "paragrafi": [
        "Sandro Mazzola è morto a 83 anni. Lo ha comunicato l’Inter nella notte tra venerdì e sabato 19 settembre. Il club lo definisce uno dei più grandi calciatori della storia, non soltanto di quella nerazzurra.",
        "«È stato la storia dell’Inter: ci è entrato da ragazzino e non ci è più uscito», scrive la società. Il presidente Giuseppe Marotta, Javier Zanetti, l’allenatore Cristian Chivu, i calciatori e il club si uniscono al cordoglio per la famiglia.",
        "Nato a Torino l’8 novembre 1942, era figlio di Valentino Mazzola, capitano del Grande Torino morto a Superga nel 1949. Sandro aveva sei anni. A otto vestì la maglia dell’Inter, dove rimase per tutta la carriera da calciatore.",
        "Con i nerazzurri ha disputato 565 partite e segnato 161 gol in 17 stagioni, secondo i dati del club. Ha vinto quattro scudetti, due Coppe dei Campioni e due Coppe Intercontinentali. Nel 1964 a Vienna segnò due reti al Real Madrid in finale.",
        "Fu capocannoniere della Serie A nel 1965, con 17 gol, e della Coppa dei Campioni nel 1964, con 7 reti. Nel 1971 arrivò secondo nel Pallone d’Oro, dietro Johan Cruijff. In Nazionale vinse l’Europeo 1968 e fu finalista al Mondiale 1970, dove Valcareggi lo alternò con Gianni Rivera.",
        "L’esordio in Serie A è del 10 giugno 1961, in Juventus-Inter 9-1, quando Angelo Moratti schierò la Primavera per protesta. Mazzola, 18 anni, segnò l’unico gol nerazzurro su rigore. Si ritirò da calciatore nel 1977.",
        "Dopo il campo fu dirigente e direttore sportivo dell’Inter, poi dello stesso Torino. Avrebbe compiuto 84 anni l’8 novembre. Il club ricorda il suo desiderio: essere ricordato come un bravo uomo, «che se la gioca sempre».",
        "Questa sera, sabato 19 settembre, l’Inter è di scena all’Olimpico contro la Roma per la quinta giornata di Serie A. Il club ha diramato il comunicato di cordoglio prima della gara.",
    ],
    "fonti": [
        {
            "url": "https://www.ansa.it/sito/notizie/sport/calcio/2026/09/19/addio-a-sandro-mazzola-la-bandiera-dellinter-aveva-83-anni_4e64feca-d64f-4fb1-92e1-065b2d74325f.html",
            "descrizione": "ANSA — comunicato Inter, 19 settembre 2026, palmarès e citazioni.",
        },
        {
            "url": "https://www.reuters.com/sports/soccer/famed-inter-milan-italy-forward-mazzola-dies-83-2026-09-19/",
            "descrizione": "Reuters — conferma indipendente della morte e del comunicato del club.",
        },
        {
            "url": "https://www.inter.it/en/club/hall-of-fame/sandro-mazzola",
            "descrizione": "Inter — Hall of Fame: 565 presenze, 161 gol, palmarès.",
        },
        {
            "url": "https://www.corriere.it/sport/calcio/26_settembre_19/sandro-mazzola-morto-l-ex-leggenda-di-inter-e-nazionale-aveva-83-anni-ee9199ad-92d9-4fe2-b493-d17a72ddcxlk.shtml",
            "descrizione": "Corriere — ulteriore conferma e citazione del comunicato nerazzurro.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html",
            "titolo": "Serie A, quinta giornata: stasera Roma-Inter",
        },
        {
            "url": "/notizie/monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026.html",
            "titolo": "Monza-Sassuolo 2-1, prima vittoria di Juric",
        },
        {
            "url": "/notizie/convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026.html",
            "titolo": "Mancini convoca 34 azzurri per la Nations League",
        },
    ],
}

ALLERTA = {
    "slug": "allerta-gialla-sei-regioni-temporali-19-settembre-2026",
    "titolo": "Allerta gialla oggi su sei regioni del Centro-Sud",
    "sommario": "Temporali su Abruzzo, Basilicata, Marche, Molise, Puglia e Sicilia. Niente codice arancione. Il Nord esce dalla mappa nazionale.",
    "categoria": "Cronaca",
    "luogo": "Italia",
    "formato": "flash",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["allerta gialla", "temporali"],
    "dati_chiave": [
        {"icona": "◆", "valore": "6", "etichetta": "regioni in allerta gialla sabato 19"},
        {"icona": "●", "valore": "gialla", "etichetta": "criticità ordinaria, non arancione"},
        {"icona": "↗", "valore": "Sud", "etichetta": "il fronte si è spostato dal Nord"},
    ],
    "paragrafi": [
        "Per sabato 19 settembre la Protezione civile conferma l’allerta gialla su sei regioni. Il bollettino di criticità delle 14.31 del 18 settembre indica criticità ordinaria per temporali su Abruzzo, Basilicata, Marche, Molise, Puglia e Sicilia.",
        "Rispetto a venerdì il quadro si restringe. Non restano in allerta nazionale Campania, Lazio, Lombardia, Sardegna, Toscana e Umbria. Non è prevista allerta arancione o rossa per la giornata in corso.",
        "In Abruzzo il codice giallo copre Marsica, bacini del Sangro, Tordino-Vomano, Pescara e Aterno. In Basilicata riguarda tutte le zone di allertamento. Nelle Marche l’avviso è su tutte le zone di allertamento.",
        "In Molise sono interessati Frentani-Sannio-Matese, la fascia litoranea e l’Alto Volturno. In Puglia il bollettino elenca Tavoliere, Gargano, Salento, Ofanto e i bacini adriatici. In Sicilia restano coperti entrambi i versanti, le Egadi, Ustica, Pantelleria e le Pelagie.",
        "Su Abruzzo, Puglia e Sicilia è confermata anche l’allerta gialla per rischio idrogeologico. Il livello descrive effetti possibili di piogge intense sul suolo, non danni già accertati.",
        "Il Dipartimento invita a seguire i messaggi regionali e comunali. L’allerta gialla è criticità ordinaria: non equivale a un’emergenza in corso e non sostituisce le ordinanze dei sindaci su scuole e spostamenti.",
        "Domenica i fenomeni tendono a concentrarsi sull’estremo Sud e sulle Isole, secondo la vigilanza meteorologica nazionale. Restano validi i bollettini aggiornati sul portale della Protezione civile.",
    ],
    "fonti": [
        {
            "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/",
            "descrizione": "Protezione civile — bollettino di criticità del 18 settembre 2026, ore 14.31, valido per il 19.",
        },
        {
            "url": "https://www.rainews.it/maratona/2026/09/maltempo-e-allerta-gialla-su-12-regioni-tempeste-e-violenti-temporali-il-meteo-162a8b8d-10c1-4079-ae9d-921bbcd650d5.html",
            "descrizione": "Rai News — sintesi dell’allerta gialla su sei regioni per sabato 19.",
        },
        {
            "url": "https://www.ilmeteo.it/notizie/protezione-civile-nazionale-allerta-meteo-per-rovesci-e-temporali-il-bollettino-per-sabato-19-settembre-173001",
            "descrizione": "IlMeteo — elenco regionale del bollettino per sabato 19 settembre.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/allerta-gialla-12-regioni-temporali-18-settembre-2026.html",
            "titolo": "Allerta gialla in 12 regioni, venerdì 18 settembre",
        },
        {
            "url": "/notizie/maltempo-allerta-arancione-liguria-emilia-romagna-17-settembre-2026.html",
            "titolo": "Maltempo, allerta arancione in Liguria ed Emilia-Romagna",
        },
        {
            "url": "/notizie/chiavari-rupinaro-maltempo-sirene-20-agosto-2026.html",
            "titolo": "Maltempo a Chiavari, sirene sul Rupinaro",
        },
    ],
}


def patch_feed(url: str, title: str, excerpt: str) -> None:
    path = ROOT / "assets" / "data" / "home-feed-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data.get("items", []):
        if item.get("url") == url:
            item["title"] = title
            item["excerpt"] = excerpt
    write_json(path, data)


def replace_body(path: Path, paragraphs: list[str]) -> None:
    page = path.read_text(encoding="utf-8")
    inner = "".join(f"<p>{html_lib.escape(p)}</p>" for p in paragraphs)
    page, n = re.subn(
        r'(<article class="art-body"[^>]*>).*?(</article>)',
        lambda m: m.group(1) + inner + m.group(2),
        page,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"corpo non sostituito: {path.name}")
    path.write_text(page, encoding="utf-8")


def update_sanctions() -> None:
    path = ROOT / "notizie" / "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html"
    page = path.read_text(encoding="utf-8")
    old_title = "USA, la Camera approva le sanzioni alla Russia: possibili dazi fino al 100%"
    new_title = "Trump firma la legge sulle sanzioni a Russia e Iran"
    old_sum = "La Camera ha approvato con 262 voti contro 159 un pacchetto che colpisce funzionari, banche, settori strategici e petroliere russe. Il testo amplia anche i poteri tariffari del presidente, ma non è ancora legge e non applica automaticamente nuovi dazi."
    new_sum = "Il pacchetto Lindsey Graham è legge da venerdì 18 settembre. I dazi fino al 100% sui principali acquirenti di energia russa restano una facoltà, non un’aliquota già in vigore."
    page = page.replace(old_title, new_title)
    page = page.replace(old_sum, new_sum)
    page = page.replace('"dateModified":"2026-09-17T01:15:53+02:00"', '"dateModified":"2026-09-19T07:20:00+02:00"')
    page = page.replace(
        'data-article-format="standard"',
        'data-article-format="standard" data-substantive-update="true"',
    )
    page = page.replace(
        "Il testo, già approvato dal Senato, passa ora al presidente Donald Trump e non è ancora legge.",
        "Venerdì 18 settembre Donald Trump ha firmato il testo. La misura è legge. I dazi secondari non scattano in automatico.",
    )
    page = page.replace(
        "La decisione finale spetta ora a Trump, che può firmare o porre il veto secondo la procedura costituzionale.",
        "La firma chiude l’iter parlamentare. Restano da definire le prime misure attuative e le eventuali deroghe di interesse nazionale.",
    )
    page = page.replace(
        "Non sono però automatici: richiedono l’entrata in vigore della legge e decisioni attuative verificabili.",
        "Non sono automatici: richiedono decisioni attuative verificabili dopo la firma.",
    )
    page = page.replace(
        "Lo stato della notizia è UFFICIALE per l’approvazione della Camera e per il testo parlamentare. Non è invece ufficiale l’entrata in vigore delle nuove sanzioni, perché manca ancora la firma presidenziale. CurioMondo aggiornerà l’articolo se la Casa Bianca completerà l’iter o definirà le prime misure operative.",
        "La legge è in vigore dopo la firma del 18 settembre. Non risultano ancora i primi dazi del 100% già applicati sui cinque maggiori importatori di energia russa. L’attuazione resta discrezionale.",
    )
    page = page.replace(
        "Ultimo aggiornamento editoriale: 17 settembre 2026.",
        "Ultimo aggiornamento editoriale: 19 settembre 2026.",
    )
    ap = (
        '<li><a href="https://apnews.com/article/donald-trump-russia-sanctions-ukraine-lindsey-graham-d1715ad5e8feccba76bfae51c5f28c45" '
        'rel="noopener noreferrer" target="_blank">Associated Press — Trump ha firmato il pacchetto venerdì 18 settembre 2026.</a></li>'
    )
    if "d1715ad5e8feccba76bfae51c5f28c45" not in page:
        page = page.replace("</ul>", ap + "</ul>", 1)
    if "firma" not in page.split("art-body")[1][:900]:
        raise SystemExit("aggiornamento sanzioni non applicato")
    path.write_text(page, encoding="utf-8")
    src = ROOT / "contenuti" / "notizie" / "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.json"
    if src.exists():
        data = json.loads(src.read_text(encoding="utf-8"))
        data["title"] = new_title
        data["excerpt"] = new_sum
        data["updated_at"] = "2026-09-19T07:20:00+02:00"
        data["status"] = "UFFICIALE"
        write_json(src, data)
    patch_feed(
        "/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html",
        new_title,
        new_sum,
    )


BERG_PARAS = [
    "Venerdì 18 settembre la fregata Carlo Bergamini ha accompagnato il mercantile italiano Jolly Oro nello stretto di Bab el-Mandeb, in direzione nord. Lo ha comunicato la Marina Militare. L’unità è inquadrata nell’operazione europea Aspides.",
    "«L’attività rientra nei compiti affidati alle forze navali dell’operazione Aspides», scrive la Marina. La definisce «un segnale concreto, arrivato con ottimo tempismo», sulla sicurezza della navigazione commerciale nell’area.",
    "Il Jolly Oro appartiene alla compagnia Ignazio Messina & C. Il mercantile è partito il 4 settembre. La scorta è stata chiesta dall’armatore. Secondo la Marina l’operazione dovrebbe durare due giorni, tra andata e ritorno.",
    "Il giorno prima, al Forum Risorsa Mare di La Spezia, il ministro della Difesa Guido Crosetto aveva detto di voler garantire il transito delle navi italiane senza attendere i tempi del coordinamento europeo. Non ha annunciato l’uscita da Aspides.",
    "Crosetto ha detto di aver deciso, con il capo di Stato maggiore, di non aspettare che Aspides autorizzi ogni transito. Ha chiesto all’Unione europea di rafforzare la missione con più navi: in zona risultano una fregata italiana e una greca.",
    "L’attività di venerdì si è svolta dentro il mandato europeo, non come missione autonoma. I vertici di Aspides hanno autorizzato la Bergamini dopo la richiesta del mercantile.",
    "Bab el-Mandeb collega il Mar Rosso e il Golfo di Aden. Le forze Houthi controllano tratti della costa yemenita. Mercantili italiani risultavano in attesa di scorta al largo di Gibuti dopo l’avanzata sulla costa sudoccidentale.",
    "Deviare intorno al Capo di Buona Speranza allunga i viaggi e può aumentare noli, carburante e assicurazioni. La Marina ricorda che dallo stretto dipendono rotte e traffici rilevanti per l’economia italiana.",
    "La scorta non chiude il dibattito sul rafforzamento di Aspides. Resta da verificare se altre navi italiane riceveranno la stessa protezione. La Bergamini dovrebbe concludere l’accompagnamento nella serata di sabato, se non ci saranno altre scorte.",
]


def update_bergamini() -> None:
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in BERG_PARAS)
    if not 300 <= words <= 600:
        raise SystemExit(f"bergamini update {words} parole")
    for i, p in enumerate(BERG_PARAS, 1):
        n = len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p))
        if n > 60:
            raise SystemExit(f"bergamini p{i} {n} parole")
    slug = "bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026"
    path = ROOT / "notizie" / f"{slug}.html"
    old_title = "Bab el-Mandeb, Crosetto prepara una missione navale per i mercantili italiani"
    new_title = "Bab el-Mandeb, la fregata Bergamini scorta il mercantile Jolly Oro"
    old_sum = "Il ministro della Difesa ha attivato la Marina per predisporre misure a tutela del transito delle navi italiane. Numero di unità, tempi e configurazione dell'eventuale missione devono ancora essere decisi con governo e Parlamento."
    new_sum = "La Marina comunica la scorta in direzione nord, nell’ambito di Aspides. L’operazione dovrebbe durare due giorni."
    page = path.read_text(encoding="utf-8")
    page = page.replace(old_title, new_title)
    page = page.replace(old_sum, new_sum)
    # meta description uses &#x27; for apostrophes
    page = page.replace(
        "Il ministro della Difesa ha attivato la Marina per predisporre misure a tutela del transito delle navi italiane. Numero di unità, tempi e configurazione dell&#x27;eventuale missione devono ancora essere decisi con governo e Parlamento.",
        html_lib.escape(new_sum, quote=True),
    )
    page = page.replace('"dateModified":"2026-09-17T19:57:00+02:00"', '"dateModified":"2026-09-19T07:22:00+02:00"')
    page = page.replace(
        'data-article-format="standard"',
        'data-article-format="standard" data-substantive-update="true"',
    )
    page = page.replace(
        "<div><strong>17/9</strong><span>data dell&#x27;attivazione preparatoria</span></div>"
        "<div><strong>0</strong><span>unità navali finora indicate</span></div>"
        "<div><strong>2</strong><span>passaggi citati: governo e Parlamento</span></div>",
        "<div><strong>18/9</strong><span>scorta comunicata dalla Marina</span></div>"
        "<div><strong>Jolly Oro</strong><span>mercantile Ignazio Messina & C.</span></div>"
        "<div><strong>2 giorni</strong><span>durata indicata della scorta</span></div>",
    )
    page = page.replace(
        "Ultimo aggiornamento editoriale: 17 settembre 2026.",
        "Ultimo aggiornamento editoriale: 19 settembre 2026.",
    )
    ansa = (
        '<li><a href="https://www.ansa.it/sito/notizie/mondo/africa/2026/09/18/la-fregata-bergamini-scorta-un-mercantile-italiano-a-bab-el-mandeb_2708dbf7-ef46-4ae2-9841-2489604162d0.html" '
        'rel="noopener noreferrer" target="_blank">ANSA — comunicato della Marina sulla scorta del Jolly Oro, 18 settembre 2026.</a></li>'
    )
    if "la-fregata-bergamini-scorta-un-mercantile" not in page:
        page = page.replace("</ul>", ansa + "</ul>", 1)
    path.write_text(page, encoding="utf-8")
    replace_body(path, BERG_PARAS)
    page = path.read_text(encoding="utf-8")
    if "Jolly Oro" not in page.split("art-body")[1][:500]:
        raise SystemExit("aggiornamento Bergamini non applicato")
    if "fonti consultate" in page.split("art-body")[1].split("</article>")[0].casefold():
        raise SystemExit("nota interna rimasta nel corpo Bergamini")
    src = ROOT / "contenuti" / "notizie" / f"{slug}.json"
    if src.exists():
        data = json.loads(src.read_text(encoding="utf-8"))
        data["title"] = new_title
        data["excerpt"] = new_sum
        data["updated_at"] = "2026-09-19T07:22:00+02:00"
        data["status"] = "UFFICIALE"
        data["body"] = BERG_PARAS
        write_json(src, data)
    patch_feed(f"/notizie/{slug}.html", new_title, new_sum)


def main() -> None:
    for art in (MAZZOLA, ALLERTA):
        assert_body(art)

    img_m = {
        "key": f"{MAZZOLA['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "mazzola-v438.jpg", f"{MAZZOLA['slug']}-v{VERSION}"),
        "alt": "Ritratto editoriale neutrale isolato generato con IA di Sandro Mazzola anziano, baffi e capelli grigi, su fondo scuro; somiglianza sintetica, non è una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "portraitOnly": True,
        "portraitFormat": "neutral-isolated",
        "prompt": "Sensitive-context neutral editorial portrait of Sandro Mazzola, elderly mustache grey hair, isolated dark studio background, no stadium, no reenacted event, no text.",
    }
    img_a = {
        "key": f"{ALLERTA['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(ROOT / "generated_images" / "allerta-v438.jpg", f"{ALLERTA['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: strada costiera bagnata nel Sud Italia sotto nubi; non è una fotografia documentaria di un evento specifico.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic rainy southern Italy coastal road, no people in distress, no text.",
    }

    slug_m = persist(MAZZOLA, img_m, "2026-09-19T07:18:00+02:00")
    slug_a = persist(ALLERTA, img_a, "2026-09-19T07:16:00+02:00")
    update_sanctions()
    update_bergamini()
    sync_surfaces([MAZZOLA, ALLERTA], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-19",
        "type": "content-release",
        "news_added": [slug_m, slug_a],
        "news_updated": [
            "usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026",
            "bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026",
        ],
        "change": "Mazzola, allerta 19 settembre, firma Trump, scorta Bergamini a Bab el-Mandeb",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": "2026-09-19",
                "release_date": "2026-09-19",
                "articleCount": int(state.get("articleCount", 0)) + 2,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
                "last_update": "scoop-v438",
            }
        )
        write_json(path, state)
    write_json(
        ROOT / "automation" / "logs" / "scoop-20260919T071800-Europe-Rome.json",
        {
            "run_at": "2026-09-19T07:18:00+02:00",
            "skill": "ultime-notizie-scoop",
            "desks": ["cronaca", "politica", "italia", "mondo", "sport", "cinema"],
            "processed": [
                {"title": MAZZOLA["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_m}.html"},
                {"title": ALLERTA["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_a}.html"},
                {"title": "Trump firma la legge sulle sanzioni a Russia e Iran", "decision": "update", "public_url": "https://curiomondo.it/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html"},
                {"title": "Bab el-Mandeb, la fregata Bergamini scorta il mercantile Jolly Oro", "decision": "update", "public_url": "https://curiomondo.it/notizie/bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026.html"},
            ],
            "discarded": [
                {"topic": "Hashim Thaçi", "reason": "già pubblicato il 16 settembre"},
                {"topic": "Roma-Inter", "reason": "gara alle 18, niente risultato; coperta nel calendario quinta giornata"},
                {"topic": "Music Awards serata 2", "reason": "stesso evento già in pagina; niente albo ufficiale Rai"},
                {"topic": "Resident Evil Cinetel", "reason": "incasso venerdì utile ma sotto la soglia rispetto a Mazzola e allerta odierna"},
                {"topic": "Kohat", "reason": "bilancio vittime ancora discordante"},
                {"topic": "Riad esplosioni", "reason": "allarme e all-clear, senza conferma ufficiale su obiettivo e danni"},
                {"topic": "Eurofighter Ta'if", "reason": "notizia di venerdì, fuori dal ciclo notturno; da riprendere se arrivano nuovi fatti"},
            ],
        },
    )


if __name__ == "__main__":
    main()
