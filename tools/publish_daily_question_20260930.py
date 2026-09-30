#!/usr/bin/env python3
"""Domanda scelta esplicitamente dal proprietario per il 30 settembre 2026.

Non attribuire questa domanda al PDF privato: l'istruzione del proprietario
prevale per questa pubblicazione e viene registrata come tale nel manifest.
"""
from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re
from lxml import etree, html
from daily_question_auto import render_question_page, update_home

ROOT = Path(__file__).resolve().parents[1]
NUMBER = 1013
QUESTION = "Se il successo non fosse visibile a nessuno, quale obiettivo continueresti a inseguire?"
SLUG = "se-il-successo-non-fosse-visibile-a-nessuno-quale-obiettivo-continueresti-a-inseguire"
QURL = f"/domanda-del-giorno/{SLUG}/"
BOOK_SLUG = "una-vita-piena-si-misura-dalle-esperienze-vissute-o-dallattenzione-con-cui-le-abbiamo-attraversate"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{BOOK_SLUG}/"
PACKAGE = {
    "excerpt": "Una riflessione su ambizione e riconoscimento: distinguere ciò che desideriamo vivere da ciò che vorremmo dimostrare agli altri.",
    "answer_paragraphs": [
        "Un obiettivo che continueresti a inseguire anche senza testimoni rivela qualcosa di ciò che desideri vivere, oltre a ciò che vorresti dimostrare. Potrebbe essere imparare un mestiere, costruire una casa serena, scrivere, capire meglio il mondo o diventare affidabile per qualcuno. Non deve essere piccolo né rinunciatario. La domanda cambia il criterio del successo: che cosa resterebbe prezioso se non potesse migliorare la tua immagine?",
        "Il riconoscimento degli altri non rende falso un desiderio. Essere apprezzati, ricevere fiducia e vedere riconosciuto il proprio lavoro sono bisogni comprensibili. Molti obiettivi nascono dentro relazioni e acquistano senso proprio perché qualcuno ne beneficia. Un risultato invisibile non è automaticamente più autentico: aiutare una persona può richiedere che quella persona veda e riceva ciò che fai.",
        "La distinzione utile riguarda il rapporto tra il contenuto della meta e l’effetto che produce sul pubblico. Desideri imparare davvero oppure desideri essere considerato competente? Vuoi maggiore sicurezza economica oppure soprattutto il confronto favorevole con chi conosci? Le due spinte possono convivere. Riconoscerle permette di scegliere quali costi accettare, invece di lasciare che sia lo sguardo altrui a fissare sempre la misura.",
        "Immagina di raggiungere un obiettivo senza poterlo raccontare per un anno. Resterebbero il lavoro necessario, le giornate che cambierebbero, le responsabilità e le rinunce. Quali parti vorresti ancora? Se ti interessa soltanto l’annuncio finale, può valere la pena rivedere la meta. Se il percorso conserva un significato, anche quando è faticoso o poco visibile, hai un indizio concreto su ciò che desideri coltivare.",
        "Questo esperimento non impone di fare tutto in silenzio. Serve a distinguere il valore che incontri nell’esperienza da quello che cerchi nella conferma. Puoi condividere un traguardo senza consegnare agli applausi il potere di deciderne il senso. E puoi cambiare direzione quando scopri che stai pagando con tempo, salute o relazioni un’immagine di successo che non corrisponde alla vita che vuoi abitare.",
        "Scegli allora una meta e completa questa frase: anche se nessuno lo sapesse, continuerei perché nella mia vita cambierebbe questo. Cerca una conseguenza precisa, non un’etichetta prestigiosa. Poi individua un passo piccolo che abbia valore prima di essere mostrato. La risposta non deve convincere nessuno: deve aiutarti a capire quale parte della tua ambizione merita davvero il tuo tempo."
    ],
}


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def dump(rel, data):
    write(rel, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def prepend(rel, section_class, card):
    text = (ROOT / rel).read_text(encoding="utf-8")
    pattern = rf'(<section\b[^>]*class="[^"]*\b{section_class}\b[^"]*"[^>]*>)'
    text, count = re.subn(pattern, lambda m: m.group(1) + card, text, count=1)
    if count != 1:
        raise SystemExit(f"Archivio non trovato: {rel}")
    write(rel, text)


def main():
    now = datetime.now(ZoneInfo("Europe/Rome"))
    day = now.date().isoformat()
    if day != "2026-09-30":
        raise SystemExit(f"Data diversa da quella autorizzata: {day}")
    label = "30 settembre 2026"
    manifest = json.loads((ROOT / "curiomondo-site-manifest.json").read_text())
    daily = manifest["daily_state"]
    if daily["last_question_date"] >= day:
        raise SystemExit("Domanda o data già utilizzata")
    for p in (ROOT / "domanda-del-giorno").glob("*/index.html"):
        doc = html.fromstring(p.read_text())
        if doc.xpath(f'//time[@datetime="{day}"]') or QUESTION in doc.xpath('//h1/text()'):
            raise SystemExit(f"Domanda già presente: {p}")
    book_path = ROOT / BOOK_URL.strip("/") / "index.html"
    book_text = book_path.read_text()
    book = html.fromstring(book_text)
    pages = book.xpath('//*[@data-book-page]')
    words = len(re.findall(r'\S+', ' '.join(book.xpath('//*[@data-book-page]//p//text()'))))
    if not 8 <= len(pages) <= 12 or not 22000 <= words <= 32000:
        raise SystemExit("L'eBook collegato non supera il gate")
    answer_chars = len(" ".join(PACKAGE["answer_paragraphs"]))
    if not 1000 <= answer_chars <= 3000:
        raise SystemExit(f"Risposta fuori soglia: {answer_chars}")

    page = render_question_page(QUESTION, PACKAGE, SLUG, day, label, BOOK_URL)
    page = page.replace('biblioteca-v1.css?v=346', 'biblioteca-v1.css?v=526')
    page = page.replace('<small>Continua la riflessione</small>', '<small>Ambizione, risultati e senso della propria vita</small>')
    page = page.replace('<strong>Leggi l\'eBook collegato</strong>', '<strong>La misura invisibile di una vita piena</strong>')
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": PACKAGE["excerpt"],
        "mainEntityOfPage": "https://curiomondo.it" + QURL,
        "datePublished": now.isoformat(timespec="seconds"),
        "dateModified": now.isoformat(timespec="seconds"),
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT", "isPartOf": {"@type": "WebSite", "name": "CurioMondo", "url": "https://curiomondo.it/"},
        "relatedLink": "https://curiomondo.it" + BOOK_URL,
    }
    page = page.replace('</head>', '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script><script defer src="/assets/js/ga4-v714.js"></script></head>')
    write(QURL.strip("/") + "/index.html", page)
    update_home(SLUG, now, label)

    card = f'<a class="cb-subcard" href="{QURL}"><span class="cb-kicker">{label}</span><h2>{escape(QUESTION)}</h2><p>{escape(PACKAGE["excerpt"])}</p><b>Leggi →</b></a>'
    prepend("domanda-del-giorno/index.html", "cb-qday-grid", card)
    library_card = card.replace('<b>Leggi →</b>', '<b>Leggi la risposta e scopri l’eBook →</b>')
    prepend("biblioteca/index.html", "cb-qday-grid", library_card)
    prepend("biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid", library_card)

    backlink = f'<a class="cm-book-back" href="{QURL}">Domanda del giorno del {label}: {escape(QUESTION)} →</a>'
    marker = '</article></main>'
    if marker not in book_text:
        raise SystemExit("Tela eBook inattesa")
    write(str(book_path.relative_to(ROOT)), book_text.replace(marker, backlink + marker, 1))

    search = json.loads((ROOT / "assets/data/search-index-v210.json").read_text())
    search["items"].insert(0, {"title": QUESTION, "excerpt": PACKAGE["excerpt"], "url": QURL, "section": "Domanda del giorno"})
    if BOOK_URL not in {x.get("url") for x in search["items"]}:
        raise SystemExit("eBook assente dalla ricerca")
    search["version"] = 715
    dump("assets/data/search-index-v210.json", search)

    xml = (ROOT / "sitemap.xml").read_text()
    if "https://curiomondo.it" + BOOK_URL not in xml:
        raise SystemExit("eBook assente dalla sitemap")
    block = f'<url><loc>https://curiomondo.it{QURL}</loc><lastmod>{day}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    write("sitemap.xml", xml.replace('</urlset>', block + '</urlset>'))

    feed = etree.parse(str(ROOT / "feed.xml"))
    channel = feed.getroot().find("channel")
    item = etree.Element("item")
    for tag, value in (("title", QUESTION), ("link", "https://curiomondo.it" + QURL), ("guid", "https://curiomondo.it" + QURL), ("pubDate", format_datetime(now)), ("description", PACKAGE["excerpt"])):
        etree.SubElement(item, tag).text = value
    index = next((i for i, x in enumerate(channel) if x.tag == "item"), len(channel))
    channel.insert(index, item)
    feed.write(str(ROOT / "feed.xml"), encoding="utf-8", xml_declaration=True, pretty_print=True)

    manifest["site"].update({"current_site_version": 715, "site_version": 715})
    manifest.update({"site_version": 715, "version": "v715", "release_version": "v715"})
    daily.update({"current_question_source_number": None, "last_question_date": day,
        "last_question_slug": SLUG, "last_daily_package_date": day, "last_daily_guides": [],
        "last_question_ebook_url": BOOK_URL,
        "current_question_owner_override": {"date": day, "question": QUESTION,
            "reason": "Scelta esplicita del proprietario dopo il confronto tra coda e PDF privato; non attribuita a un numero del PDF."}})
    daily.setdefault("used_owner_questions", []).append({"date": day, "question": QUESTION, "slug": SLUG})
    manifest["last_release"] = {"version": 715, "date": day, "type": "daily-editorial-package",
        "news_added": [], "news_updated": [], "daily_question_added": SLUG,
        "ebook_linked": BOOK_SLUG, "ebook_created": False, "guides_added": [],
        "change": "Domanda scelta esplicitamente dal proprietario; risposta originale ed eBook esistente pertinente collegato. Nessuna notizia modificata."}
    dump("curiomondo-site-manifest.json", manifest)
    for rel in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        state = json.loads((ROOT / rel).read_text())
        state.update({"currentVersion": 715, "site_version": 715, "version": "715", "date": day,
            "release_date": day, "last_daily_question_date": day, "last_update": "daily-question-1013-v715"})
        dump(rel, state)
    print(json.dumps({"date": day, "question": QUESTION, "source": "explicit_owner_instruction",
        "answer_characters": answer_chars, "linked_ebook_words": words, "linked_ebook_chapters": len(pages)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
