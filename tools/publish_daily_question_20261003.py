#!/usr/bin/env python3
"""Pubblica la domanda n. 1016, verificata sul PDF privato, il 3 ottobre.

Collega l'eBook esistente sui confini e sulle scelte di lavoro, senza
duplicarlo o presentarlo come un libro nuovo. Non include il PDF privato.
"""
from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re

from lxml import html

import build_v501_daily as shared
from daily_question_auto import (
    choose_question, render_question_page, update_feed, update_home,
    update_sitemap,
)

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-03"
DATE_LABEL = "3 ottobre 2026"
NUMBER = 1016
QUESTION = "Possiamo amare un lavoro e insieme proteggerci da esso?"
SLUG = "possiamo-amare-un-lavoro-e-insieme-proteggerci-da-esso"
QURL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = "/biblioteca/vita-relazioni/domande-per-conoscersi/quanto-siamo-liberi-nelle-scelte-che-facciamo-per-non-deludere-chi-amiamo/"
BOOK_TITLE = "Liberi senza smettere di appartenere"
PACKAGE = {
    "excerpt": "Amare il proprio mestiere non obbliga a essere sempre disponibili: una riflessione su passione, condizioni di lavoro e confini sostenibili.",
    "answer_paragraphs": [
        "Sì. Possiamo amare ciò che facciamo senza accettare ogni condizione in cui ci viene chiesto di farlo. Il piacere di risolvere un problema, costruire qualcosa o aiutare qualcuno non rende inesauribili il tempo e le energie. Quando un lavoro conta molto, fermarsi può sembrare un tradimento. Eppure un limite può essere proprio il modo di conservare quel legame senza lasciare che occupi tutta la vita.",
        "Conviene distinguere il mestiere dalla sua organizzazione. Una persona può amare insegnare e soffrire per i carichi assegnati; può essere orgogliosa di un lavoro artigiano e avere bisogno di orari più prevedibili. La passione descrive un rapporto con l’attività. Non dimostra che personale, tempi, retribuzione e richieste siano adeguati. Criticare quelle condizioni non significa negare il valore di ciò che si fa.",
        "Il confine diventa più difficile quando il lavoro è anche una parte dell’identità. Un incarico rifiutato può sembrare un’occasione persa per dimostrare quanto valiamo. Si comincia allora a rispondere sempre, a prendere un compito in più e a rinviare ciò che non produce risultati visibili. Una sera occupata può essere una scelta consapevole. La stessa rinuncia ripetuta senza più poterla discutere merita una domanda diversa: chi sta decidendo come viene usato il nostro tempo?",
        "Proteggersi richiede anche guardare le condizioni reali. Chi dipende da uno stipendio o ha poco potere contrattuale non può risolvere ogni squilibrio semplicemente dicendo no. L’organizzazione del lavoro, il sostegno dei colleghi e il confronto con chi rappresenta i lavoratori contano. Non tutto ciò che pesa è un problema di carattere, e non ogni difficoltà si corregge diventando più efficienti.",
        "Un primo passo può essere nominare una richiesta precisa: quale attività ha la priorità, che cosa può essere rimandato, chi copre un’assenza, quando serve davvero una risposta. Un confine sostenibile rende visibile il costo invece di nasconderlo nello sforzo di una sola persona. Se il carico non cambia, occorre osservare anche quella risposta: un accordo vale per ciò che permette di fare, non soltanto per le parole con cui viene accolto.",
        "Amare un lavoro non richiede di renderlo responsabile di tutto il nostro valore. Possono restare importanti una relazione, un interesse senza guadagno, una giornata in cui nessuno chiede una prestazione. Oggi, quale piccolo limite renderebbe più abitabile il lavoro che desideri continuare ad amare?",
    ],
}


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit("Data Europe/Rome diversa da quella del pacchetto")
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    daily = manifest["daily_state"]
    if daily.get("last_question_date", "") >= DATE:
        raise SystemExit("La domanda di oggi è già presente: nessuna modifica")
    chosen = choose_question(manifest)
    if chosen["number"] != NUMBER or chosen["question"] != QUESTION:
        raise SystemExit("La domanda selezionata non coincide con la voce PDF verificata")

    chars = len(" ".join(PACKAGE["answer_paragraphs"]))
    if not 1000 <= chars <= 3000:
        raise SystemExit(f"Risposta fuori standard: {chars}")
    book_path = ROOT / BOOK_URL.strip("/") / "index.html"
    book_text = book_path.read_text(encoding="utf-8")
    book = html.fromstring(book_text)
    stages = book.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " cm-book-stage ")]')
    words = len(re.findall(r"\S+", " ".join(stages[0].xpath('.//p//text()'))))
    chapters = len(book.xpath('//*[@data-book-page]'))
    if not 22000 <= words <= 32000 or not 8 <= chapters <= 12:
        raise SystemExit(f"eBook collegato fuori standard: {words} parole, {chapters} capitoli")
    if BOOK_TITLE != " ".join(book.xpath('//h1//text()')):
        raise SystemExit("Titolo dell’eBook non coerente")

    version = max(int(manifest.get("site_version", 0)), int(manifest["site"]["current_site_version"])) + 1
    page = render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL)
    page = page.replace("biblioteca-v1.css?v=346", "biblioteca-v1.css?v=526")
    page = page.replace("<small>Continua la riflessione</small>", "<small>eBook su autonomia, confini e scelte di lavoro</small>")
    page = page.replace("<strong>Leggi l'eBook collegato</strong>", f"<strong>{escape(BOOK_TITLE)}</strong>")
    stamp = now.isoformat(timespec="seconds")
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": QUESTION, "description": PACKAGE["excerpt"],
        "mainEntityOfPage": "https://curiomondo.it" + QURL,
        "datePublished": stamp, "dateModified": stamp,
        "author": {"@type": "Organization", "name": "CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo"},
        "inLanguage": "it-IT", "relatedLink": "https://curiomondo.it" + BOOK_URL,
    }
    page = page.replace("</head>", '<meta property="og:type" content="article"><meta property="og:title" content="' + escape(QUESTION, quote=True) + '"><meta property="og:description" content="' + escape(PACKAGE["excerpt"], quote=True) + '"><meta property="og:url" content="https://curiomondo.it' + QURL + '"><script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script><script defer src="/assets/js/ga4-v714.js"></script></head>')
    sources = '<aside class="art-sources" aria-label="Fonti consultate"><p><strong>Fonti consultate</strong></p><p><a href="https://osha.europa.eu/en/themes/psychosocial-risks-and-mental-health" rel="noopener">EU-OSHA: organizzazione del lavoro, carichi e rischi psicosociali</a> · <a href="https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work" rel="noopener">OMS: condizioni di lavoro e interventi sull’organizzazione</a></p></aside>'
    page = page.replace("</main>", sources + "</main>")
    shared.write(ROOT / QURL.strip("/") / "index.html", page)
    update_home(SLUG, now, DATE_LABEL)

    card = f'<a class="cb-subcard" href="{QURL}"><span class="cb-kicker">{DATE_LABEL} · Domanda del giorno</span><h2>{escape(QUESTION)}</h2><p>{escape(PACKAGE["excerpt"])}</p><b>Leggi →</b></a>'
    for path, cls in (
        ("domanda-del-giorno/index.html", "cb-qday-grid"),
        ("biblioteca/index.html", "cb-qday-grid"),
        ("biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid"),
    ):
        shared.prepend_card(ROOT / path, cls, card, QURL)

    # Il libro mantiene titolo, contenuto e data di prima pubblicazione.
    # Distinguiamo il suo legame originario dalla nuova riflessione collegata.
    book_text = book_text.replace("← Torna alla Domanda del giorno</a>", "← La domanda da cui nasce questo eBook</a>", 1)
    link = f'<a class="cm-book-back" href="{QURL}">Domanda del {DATE_LABEL}: {escape(QUESTION)}</a>'
    if QURL not in book_text:
        book_text = book_text.replace("</article></main>", link + "</article></main>", 1)
    if QURL not in book_text:
        raise SystemExit("Collegamento reciproco al nuovo quesito non inserito")
    shared.write(book_path, book_text)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    search["items"] = [item for item in search["items"] if item.get("url") != QURL]
    search["items"].insert(0, {"title": QUESTION, "excerpt": PACKAGE["excerpt"], "url": QURL, "section": "Domanda del giorno"})
    search["version"] = max(version, int(search.get("version", 0)))
    shared.dump(search_path, search)
    update_sitemap(DATE, QURL, BOOK_URL)
    update_feed(now, QUESTION, PACKAGE, QURL)

    manifest["site"].update({"current_site_version": version, "site_version": version})
    manifest.update({"site_version": version, "version": f"v{version}", "release_version": f"v{version}"})
    daily["used_question_source_numbers"].append(NUMBER)
    daily.update({
        "current_question_source_number": NUMBER, "last_question_date": DATE,
        "last_question_slug": SLUG, "last_question_ebook_url": BOOK_URL,
        "last_daily_package_date": DATE, "last_daily_guides": [],
        "current_question_source_verification": chosen["source_verification"],
        "question_queue_rule": "La coda è una cache: ogni voce deve essere verificata sul PDF privato originale prima della pubblicazione.",
    })
    daily.pop("current_question_owner_override", None)
    manifest["last_release"] = {
        "version": version, "date": DATE, "type": "daily-question",
        "daily_question_added": SLUG, "ebook_linked": BOOK_URL,
        "ebook_created": False, "guides_added": [], "news_added": [], "news_updated": [],
        "change": "Domanda n. 1016 verificata sul PDF originale; corretta la cache divergente e collegato l’eBook esistente su autonomia, confini e scelte di lavoro.",
    }
    shared.dump(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({"currentVersion": version, "site_version": version, "version": str(version), "date": DATE, "release_date": DATE, "last_daily_question_date": DATE, "last_update": f"daily-question-v{version}"})
        shared.dump(path, state)
    shared.write(ROOT / f"RELEASE-NOTES-v{version}.md", f'''# CurioMondo v{version} — {DATE_LABEL}

- Pubblicata la domanda n. {NUMBER}, verificata sul PDF privato originale: “{QUESTION}”.
- Corretta la voce divergente nella coda. Il selettore automatico richiede ora una verifica del PDF per ogni voce futura e rifiuta una voce modificata dopo la verifica.
- Risposta originale di {chars} caratteri; collegato l’eBook esistente “{BOOK_TITLE}” ({chapters} capitoli, {words} parole), con collegamento reciproco alla nuova domanda. Il libro non è presentato come nuova pubblicazione.
- Aggiornati card mistero, archivio, Biblioteca, ricerca, RSS, sitemap, manifest e stati di rilascio.
- Il PDF privato non è stato aggiunto al repository. Nessuna notizia modificata.
''')
    print(json.dumps({"status": "prepared", "version": version, "date": DATE, "question_number": NUMBER, "answer_characters": chars, "linked_book_words": words, "linked_book_chapters": chapters}, ensure_ascii=False))


if __name__ == "__main__":
    main()
