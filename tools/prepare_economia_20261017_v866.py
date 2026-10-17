#!/usr/bin/env python3
"""Pubblica dieci approfondimenti economici verificati del 17 ottobre 2026."""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools import prepare_news_20261014_v851 as shared
from tools import prepare_news_20261014_v852 as image_shared

VERSION = 866
BATCH = ROOT / "tools/news_batch_20261017_v866.json"
IMAGES = ROOT / "tools/news_images_20261017_v866.json"
AUDIT = ROOT / "tools/news_audit_20261017_v866.json"
OFFSETS = (0, 5, 10, 15, 20, 25, 30, 35, 40, 45)
PHRASES = (
    "Puoi controllare una scadenza prima di prendere una decisione economica.",
    "Un confronto tra più offerte aiuta a vedere i costi nascosti.",
    "Puoi chiedere una spiegazione scritta prima di firmare.",
    "Una promessa di rendimento merita sempre una verifica indipendente.",
    "Puoi conservare ricevute e documenti in un unico posto.",
    "Un dato mensile va confrontato con una serie più lunga.",
    "Puoi rimandare un investimento finché i rischi non sono chiari.",
    "La fretta non è un requisito per una buona scelta finanziaria.",
    "Puoi verificare un incentivo soltanto sui canali ufficiali.",
    "Un piccolo margine di sicurezza rende più solido un bilancio."
)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assign_dates(rows, release):
    for article, minutes in zip(rows, OFFSETS):
        stamp = release - timedelta(minutes=minutes)
        if article.get("source_published"):
            assert stamp >= datetime.fromisoformat(article["source_published"]), article["slug"]
        article["published"] = article["modified"] = stamp.isoformat(timespec="seconds")


def finish(article, release):
    shared.finish_page(article, release)
    path = ROOT / "notizie" / (article["slug"] + ".html")
    text = path.read_text(encoding="utf-8").replace(
        "/assets/css/global-header-v275.css?v=736",
        "/assets/css/global-header-v275.css?v=633",
    )
    path.write_text(text, encoding="utf-8")


def refresh_article(article):
    path = ROOT / "notizie" / (article["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for selector, value in (
        ("//title", article["titolo"] + " | CurioMondo"),
        ("//main//h1[1]", article["titolo"]),
        ('//main/p[contains(@class,"subtitle")]', article["sommario"]),
    ):
        doc.xpath(selector)[0].text = value
    for selector, value in (
        ('//meta[@name="description"]', article["sommario"]),
        ('//meta[@property="og:title"]', article["titolo"]),
        ('//meta[@property="og:description"]', article["sommario"]),
    ):
        doc.xpath(selector)[0].set("content", value)
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data.update(headline=article["titolo"], description=article["sommario"])
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in article["paragrafi"]:
        etree.SubElement(body, "p").text = paragraph
    stats = doc.xpath('//div[contains(@class,"cm-insight-grid")]/div')
    for node, row in zip(stats, article["dati_chiave"]):
        node.xpath("./strong")[0].text = row["valore"]
        node.xpath("./span")[0].text = row["etichetta"]
    sources = doc.xpath('//div[contains(@class,"art-sources")]/ul')[0]
    for child in list(sources):
        sources.remove(child)
    for source in article["fonti"]:
        li = etree.SubElement(sources, "li")
        etree.SubElement(li, "a", href=source["url"], rel="noopener noreferrer", target="_blank").text = source["nome"]
    doc.xpath('//*[@id="readTime"]')[0].text = f"{max(1, round(sum(len(p.split()) for p in article['paragrafi']) / 210))} min di lettura"
    shared.save(path, doc)


def main():
    shared.VERSION = image_shared.VERSION = VERSION
    rows = json.loads(BATCH.read_text(encoding="utf-8"))
    release = datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    assert release.date().isoformat() == "2026-10-17"
    assert len(rows) == len(OFFSETS) == 10
    if sys.argv[1:] == ["--refresh-sources"]:
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        stamps = {item["slug"]: item for item in audit["articles"]}
        refresh = {
            "bonus-mamme-2026-inps-60-euro-mese-requisiti-domanda",
            "consob-oscura-dieci-siti-truffe-finanziarie-cripto-ia-2026",
            "bonus-assunzioni-siisl-decreto-pubblicazione-offerte-lavoro-2026",
        }
        for article in rows:
            article["published"] = stamps[article["slug"]]["published"]
            article["modified"] = stamps[article["slug"]]["modified"]
            if article["slug"] in refresh:
                refresh_article(article)
                finish(article, datetime.fromisoformat(audit["release"]))
            stamps[article["slug"]].update(
                title=article["titolo"],
                sources=article["fonti"],
                words=sum(len(p.split()) for p in article["paragrafi"]),
                original_value=article["original_value"],
            )
        shared.sync_complete(rows)
        dump(AUDIT, audit)
        print("Fonti e contenuti aggiornati sulle tre pagine ad alto rischio.")
        return
    assert not sys.argv[1:]
    for article in rows:
        assert article["categoria"] == "Economia"
        assert article["formato"] == "standard"
        assert 500 <= sum(len(p.split()) for p in article["paragrafi"]) <= 800
        assert max(len(p.split()) for p in article["paragrafi"]) <= 60
        assert 1 <= len(article["fonti"]) <= 2
        assert len(article["dati_chiave"]) == 3
        assert not (ROOT / "notizie" / (article["slug"] + ".html")).exists(), article["slug"]

    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    _, used = nome_pensiero.used(ROOT)
    for phrase in PHRASES:
        if phrase not in phrases:
            phrases.append(phrase)
    assert sum(phrase not in used for phrase in phrases) >= 10
    dump(phrases_path, phrases)

    sources = json.loads(IMAGES.read_text(encoding="utf-8"))
    images = []
    for article in rows:
        image = image_shared.image_for(article, sources)
        site.write_article(article, image, VERSION)
        images.append(image)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert not {a["slug"] for a in rows}.intersection(i.get("id") for i in registry["items"])
    registry["items"] = images + registry["items"]
    registry["version"] = VERSION
    dump(registry_path, registry)

    assign_dates(rows, release)
    for article in rows:
        finish(article, release)
    shared.sync_complete(rows)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update(
        site_version=VERSION,
        currentVersion=VERSION,
        version=str(VERSION),
        date="2026-10-17",
        release_date="2026-10-17",
        updated_at=release.isoformat(),
        last_update="economia-17-ottobre-v866",
        status="ready",
    )
    state["articleCount"] += 10
    state["generatedEditorialImages"] += 10
    dump(state_path, state)

    audit = {
        "version": VERSION,
        "release": release.isoformat(),
        "new_articles": 10,
        "updated_articles": 0,
        "new_images": 10,
        "request": "Dieci ultime notizie economiche utili agli italiani — 17 ottobre 2026",
        "push_executed": False,
        "manifest_accessed": False,
        "baseline_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "selection_reason": "Massimo di dieci articoli per richiesta; priorità a misure operative, redditi, lavoro, credito, energia e tutela del risparmio.",
        "exclusions": [
            "Stablecoin non conformi MiCA esclusa perché già pubblicata sul sito.",
            "Segnalazioni senza fonte primaria o aggiornamento verificabile escluse."
        ],
        "image_visual_review": "Completata sulle dieci copertine originali.",
        "browser_visual_qa": "Controlli DOM, metadati, immagini e superfici completati; screenshot locale non disponibile perché il runtime non include un eseguibile browser.",
        "format_exception": "Nessuna: tutti i testi sono approfondimenti standard da almeno 500 parole.",
        "articles": [
            {
                "slug": a["slug"],
                "title": a["titolo"],
                "published": a["published"],
                "modified": a["modified"],
                "source_date": a["source_date"],
                "sources": a["fonti"],
                "words": sum(len(p.split()) for p in a["paragrafi"]),
                "risk": a["risk"],
                "original_value": a["original_value"],
            }
            for a in rows
        ],
    }
    dump(AUDIT, audit)
    print(json.dumps({"version": VERSION, "new_articles": 10, "new_images": 10, "release": audit["release"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
