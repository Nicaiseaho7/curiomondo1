#!/usr/bin/env python3
"""Pubblica il calendario F1 2027 e aggiorna Milan-Benfica con il risultato."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 399
PUBLISHED = "2026-09-17T06:29:14+02:00"
SLUG = "formula-1-calendario-2027-dieci-sprint-monaco-monza"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "exec-e7153a0e-ab9f-4524-9fa1-8589937a1a8a.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Formula 1, nel 2027 dieci Sprint: debutta Monaco e torna Monza",
    "sommario": "Formula 1 e FIA hanno approvato un calendario di 24 Gran Premi in 22 Paesi. Le Sprint salgono da sei a dieci; Monaco entra per la prima volta, mentre Monza torna al formato breve.",
    "categoria": "Sport",
    "luogo": "Monaco / Monza",
    "formato": "standard",
    "parole_chiave_titolo": ["dieci Sprint", "Monaco", "Monza"],
    "dati_chiave": [
        {"icona": "◆", "valore": "10", "etichetta": "weekend Sprint nel 2027"},
        {"icona": "↗", "valore": "24", "etichetta": "Gran Premi nel calendario"},
        {"icona": "●", "valore": "5/9", "etichetta": "gara di Monza"},
    ],
    "paragrafi": [
        "Formula 1 e FIA hanno ufficializzato il 16 settembre il calendario 2027: 24 Gran Premi in 22 Paesi e dieci weekend Sprint, quattro in più rispetto al 2026. Monaco ospiterà per la prima volta il formato breve, mentre Monza tornerà a proporlo nel fine settimana del 3-5 settembre.",
        "Le altre Sprint sono previste in Bahrain, Australia, Giappone, Canada, Gran Bretagna, Brasile, Qatar e Abu Dhabi. Bahrain, Melbourne, Suzuka, Monaco e Abu Dhabi debutteranno con questo programma; Montréal, Silverstone, Monza, Interlagos e Lusail lo hanno già ospitato.",
        "A Monaco la modifica incide soprattutto sulla struttura del weekend. Venerdì si terranno una sola sessione di prove libere e la Sprint Qualifying; sabato mattina si correrà la prova breve, seguita nel pomeriggio dalle qualifiche del Gran Premio. La gara principale resterà domenica sul tracciato cittadino.",
        "Il circuito monegasco è stretto e offre poche opportunità di sorpasso. Formula 1 punta quindi anche sul valore delle due sessioni di qualifica, nelle quali i piloti affrontano il tracciato con poco margine d'errore. L'introduzione della Sprint non cambia la distanza del Gran Premio e non garantisce automaticamente più sorpassi.",
        "La gara Sprint misura circa 100 chilometri e assegna punti ai primi otto classificati, da otto al vincitore a uno all'ottavo. Non prevede una sosta obbligatoria. Il formato riduce da tre a una le prove libere del weekend, aumentando il peso della preparazione al simulatore e delle decisioni prese dopo i primi giri in pista.",
        "Il calendario inizierà in Bahrain dal 12 al 14 marzo, dopo i test del 24-27 febbraio, e terminerà ad Abu Dhabi dal 10 al 12 dicembre. Portogallo e Turchia rientrano nel Mondiale; la prova di Istanbul resta soggetta all'omologazione FIA del circuito. Zandvoort e Barcellona non compaiono nel programma 2027.",
        "Per il pubblico italiano, Monza è fissata dal 3 al 5 settembre e avrà una Sprint per la seconda volta. Il Gran Premio d'Italia sarà seguito una settimana dopo dalla gara di Madrid. Le modalità di trasmissione in Italia per il 2027 non sono ancora indicate nelle fonti ufficiali consultate e non vanno dedotte dagli accordi delle stagioni precedenti.",
        "Formula 1 motiva l'espansione con i dati di pubblico: secondo l'organizzazione, i weekend Sprint ottengono in media il 12% di audience complessiva in più rispetto agli appuntamenti tradizionali. È un dato prodotto dal promotore e misura l'interesse televisivo dichiarato; non dimostra da solo un miglioramento della qualità sportiva o dei sorpassi.",
    ],
    "fonti": [
        {"url": "https://corp.formula1.com/2027-calendar-announced-with-10-sprint-events/", "descrizione": "Formula 1 — calendario ufficiale 2027 approvato dal World Motor Sport Council, date e sedi delle dieci Sprint."},
        {"url": "https://www.formula1.com/en/latest/article/whats-new-with-the-f1-sprint-in-2027.6UiqFIVYRoMSgPvAA8yiiZ", "descrizione": "Formula 1 — formato Sprint, circuiti al debutto e dati dichiarati sull'interesse del pubblico."},
        {"url": "https://www.reuters.com/sports/formula1/monaco-become-one-record-10-f1-sprint-weekends-2027-2026-09-16/", "descrizione": "Reuters — conferma indipendente del calendario, del debutto di Monaco e dell'espansione a dieci Sprint."},
        {"url": "https://www.theguardian.com/sport/2026/sep/16/number-of-sprint-races-increased-f1-2027-calendar", "descrizione": "The Guardian — riscontro indipendente su calendario, ritorni di Portogallo e Turchia e sedi Sprint."},
    ],
    "correlati": [
        {"url": "/notizie/kimi-antonelli-vince-gp-spagna-madrid-madring-13-settembre-2026.html", "titolo": "Antonelli vince il primo GP di Madrid e allunga nel Mondiale"},
        {"url": "/notizie/kimi-antonelli-vince-gp-italia-monza-19esimo-6-settembre-2026.html", "titolo": "Antonelli, impresa a Monza: vince partendo 19°"},
        {"url": "/notizie/monza-vip-sinner-elkann-chiellini-vettel-f2002-schumacher-6-settembre-2026.html", "titolo": "Monza, Vettel riporta in pista la Ferrari F2002"},
    ],
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_image_variants() -> list[dict]:
    image = Image.open(SOURCE_IMAGE).convert("RGB")
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
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=84, method=6)
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def update_milan_result() -> None:
    path = ROOT / "notizie" / "milan-benfica-oggi-16-settembre-2026-europa-league-orario-tv.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    title = "Milan-Benfica 0-2: Lukébakio e Kamiński decidono il debutto europeo"
    summary = "Il Benfica vince 2-0 a San Siro nella prima giornata di Europa League. Lukébakio segna al 16’, Kamiński raddoppia al 54’: il Milan parte senza punti nella classifica unica."
    for node in doc.xpath("//title"):
        node.text = title + " | CurioMondo"
    for node in doc.xpath('//meta[@name="description"] | //meta[@property="og:description"]'):
        node.set("content", summary)
    for node in doc.xpath('//meta[@property="og:title"]'):
        node.set("content", title)
    for node in doc.xpath('//main//h1[1]'):
        node.text = title
    for node in doc.xpath('//main//p[contains(@class,"subtitle")][1]'):
        node.text = summary
    schema = doc.xpath('//script[@type="application/ld+json"]')[0]
    data = json.loads(schema.text)
    data.update({"headline": title, "description": summary, "dateModified": PUBLISHED})
    schema.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    stats = doc.xpath('//section[contains(@class,"cm-insight")]//div[contains(@class,"cm-insight-grid")][1]')[0]
    stats.clear()
    for value, label in (("0-2", "risultato finale"), ("16’", "gol di Lukébakio"), ("54’", "raddoppio di Kamiński")):
        box = html.Element("div"); strong = html.Element("strong"); strong.text = value; span = html.Element("span"); span.text = label; box.extend([strong, span]); stats.append(box)
    body = doc.xpath('//article[contains(@class,"art-body")][1]')[0]
    body.clear(); body.set("class", "art-body"); body.set("data-editorial-protocol", "4.0"); body.set("data-article-format", "standard")
    paragraphs = [
        "Il Benfica ha battuto il Milan 2-0 mercoledì 16 settembre a San Siro, nella prima giornata della fase campionato di Europa League 2026/27. Dodi Lukébakio ha sbloccato la partita al 16’ e Jakub Kamiński ha raddoppiato al 54’, consegnando alla squadra portoghese i primi tre punti.",
        "Il primo gol è arrivato con un tiro basso di Lukébakio dal limite dell'area. Nella ripresa Kamiński ha chiuso al volo da circa quindici metri. Il Milan ha terminato con più possesso e più conclusioni complessive, ma entrambe le squadre hanno centrato quattro volte lo specchio della porta.",
        "Le statistiche aiutano a separare volume ed efficacia. ESPN registra 17 tiri del Milan contro 11 del Benfica e il 60% di possesso rossonero, ma assegna agli ospiti l'unica grande occasione della partita. Il dato sui tiri non equivale quindi a una superiorità nelle opportunità più pericolose.",
        "La sconfitta interrompe l'imbattibilità del Milan nei sei precedenti europei con il Benfica, chiusi con quattro vittorie e due pareggi. È anche la prima affermazione del club portoghese contro i rossoneri nelle competizioni UEFA, dopo le finali di Coppa dei Campioni vinte dal Milan nel 1963 e nel 1990.",
        "Il risultato lascia il Milan a zero punti dopo una delle otto partite previste. Nella classifica unica le prime otto squadre accederanno direttamente agli ottavi; quelle dal nono al ventiquattresimo posto passeranno dai playoff. Dopo una sola giornata, la posizione resta provvisoria e non determina ancora la qualificazione.",
        "Il prossimo impegno europeo del Milan è la trasferta con il Salisburgo, in programma giovedì 15 ottobre alle 18:45 italiane. Il calendario proseguirà poi con Bournemouth, Ferencváros, Olympiacos, Sunderland, Levski Sofia e Ararat-Armenia, per un totale di quattro gare in casa e quattro fuori.",
        "Reuters, UEFA, Sky Sport e Football Italia concordano su punteggio e marcatori. Per il dettaglio statistico CurioMondo mantiene separata la fonte ESPN: possesso, tiri e occasioni dipendono dal sistema di rilevazione utilizzato e possono presentare piccole differenze tra fornitori.",
    ]
    for text in paragraphs:
        p = html.Element("p"); p.text = text; body.append(p)
    sources = doc.xpath('//div[contains(@class,"art-sources")][1]')[0]
    ul = sources.xpath('.//ul[1]')[0]; ul.clear()
    refs = [
        ("https://www.uefa.com/uefaeuropaleague/video/02a9-219bb924c1a0-29aaa735c81c-1000--europa-league-highlights-milan-0-2-benfica/", "UEFA — risultato e highlights ufficiali di Milan-Benfica 0-2."),
        ("https://www.reuters.com/sports/soccer/benfica-earn-win-milan-sunderland-celebrate-historic-night-2026-09-16/", "Reuters — cronaca indipendente, marcatori e quadro della prima giornata."),
        ("https://sport.sky.it/calcio/europa-league/video/2026/09/16/milan-benfica-gol-highlights-europa-league-1125183", "Sky Sport — conferma indipendente del risultato e dei gol."),
        ("https://football-italia.net/uel-milan-0-2-benfica-nightmare-europa-league/", "Football Italia — tabellino e statistiche della partita."),
        ("https://www.espn.com/soccer/team-stats/_/gameId/401915586", "ESPN — statistiche di squadra, tiri, possesso e occasioni."),
    ]
    for url, desc in refs:
        li = html.Element("li"); a = html.Element("a", href=url, rel="noopener noreferrer", target="_blank"); a.text = desc; li.append(a); ul.append(li)
    small = sources.xpath('.//p/small[1]')[0]
    small.text = "Redazione CurioMondo · "; link = html.Element("a", href="/pagine/metodo-editoriale.html"); link.text = "Come lavoriamo"; small.append(link); link.tail = f"\nTesto originale CurioMondo. Ultimo aggiornamento editoriale: 17 settembre 2026, ore 06:29 italiane.\n{CAPTION}"
    path.write_text("<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def main() -> None:
    update_milan_result()
    image = {"key": IMAGE_KEY, "aiGenerated": True, "documentaryPhoto": False, "generator": "ChatGPT/OpenAI image generation", "variants": save_image_variants(), "alt": "Scena editoriale contestuale generata con IA: due monoposto di Formula 1 affrontano una curva del circuito cittadino di Monaco; non rappresenta una gara specifica.", "disclosure": CAPTION, "sensitiveContext": False, "reenactedEvent": False, "prompt": "Ultra-realistic editorial motorsport scene of two Formula 1 cars on Monaco street circuit; no text, infographic or watermark."}
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {"slug": SLUG, "title": ARTICLE["titolo"], "excerpt": ARTICLE["sommario"], "category": "Sport", "published_at": PUBLISHED, "updated_at": PUBLISHED, "development_at": "2026-09-16", "status": "UFFICIALE", "public_url": PUBLIC_URL, "publication_state": "pending_deploy", "body": ARTICLE["paragrafi"], "sources": ARTICLE["fonti"], "image": image})
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")); manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION}); manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"}); manifest["last_release"] = {"version": VERSION, "date": "2026-09-17", "type": "content-release", "news_added": [SLUG], "news_updated": ["milan-benfica-oggi-16-settembre-2026-europa-league-orario-tv"], "change": "Pubblicato il calendario F1 2027 e aggiornato Milan-Benfica con il risultato finale", "image_policy_applied": "new-openai-contextual-editorial-image; existing-relevant-image-preserved-on-update"}; write_json(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename; state = json.loads(path.read_text(encoding="utf-8")); state.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION), "date": "2026-09-17", "release_date": "2026-09-17", "articleCount": int(state.get("articleCount", 0)) + 1, "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1, "last_update": "sport-f1-milan-v399"}); write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "sport-20260917T062914-Europe-Rome.json", {"run_at": PUBLISHED, "scope": "Sport", "production_branch": "main", "base_commit": "59817b3", "coverage": {"target_distinct_full_contents": 500, "distinct_full_contents_actually_read": 18, "distinct_domains": 12, "target_reached": False, "note": "Conteggio prudenziale: l'obiettivo di 500 contenuti non è stato raggiunto nei limiti della sessione; ogni elemento pubblicato è stato verificato con fonte primaria e riscontri indipendenti."}, "processed": [{"title": ARTICLE["titolo"], "editorial_score": 8.4, "status": "UFFICIALE", "decision": "publish", "sources": [x["url"] for x in ARTICLE["fonti"]], "public_url": PUBLIC_URL, "publication_state": "pending_deploy"}, {"title": "Milan-Benfica 0-2: Lukébakio e Kamiński decidono il debutto europeo", "status": "CONFERMATA DA PIÙ FONTI", "decision": "substantive_update", "public_url": "https://curiomondo.it/notizie/milan-benfica-oggi-16-settembre-2026-europa-league-orario-tv.html", "publication_state": "pending_deploy"}], "publication": {"site_version": VERSION, "state": "pending_deploy"}})
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG, "updated": "milan-benfica"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
