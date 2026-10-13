#!/usr/bin/env python3
"""Lotto ANSA: 13 nuovi articoli e un aggiornamento; nessuna operazione remota.

Il manifest è deliberatamente escluso. Gli originali IA restano in scratch;
il repository contiene le tre varianti WebP e i prompt di ogni copertina.
"""
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import etree, html
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools.publish_notte_mattina_20261010_v827 import set_published

VERSION = 847
ROME = ZoneInfo("Europe/Rome")
OFFSETS = (0, 5, 11, 18, 26, 35, 45, 56, 68, 81, 95, 110, 126)
PHRASES = (
    "Puoi chiedere qualche minuto prima di rispondere a una domanda difficile.",
    "Non devi portare a termine tutto quello che inizi.",
    "Meriti di sapere quali sono le condizioni prima di accettare.",
    "Puoi proteggere il tuo tempo anche quando la richiesta viene da un amico.",
    "Se hai cambiato idea, puoi dirlo con parole semplici.",
    "Un errore non ti obbliga a rinunciare al prossimo tentativo.",
    "Puoi scegliere a chi raccontare quello che ti preoccupa.",
    "Non serve trovare subito la risposta per ascoltare qualcuno.",
    "Puoi fermarti quando una situazione non ti fa sentire al sicuro.",
    "Il tuo bisogno di riposo non deve aspettare che tutto sia finito.",
    "Chiedere spiegazioni è un modo per decidere con più serenità.",
    "Puoi fare una cosa alla volta anche in una giornata piena.",
    "Non devi dimostrare di stare bene per meritare attenzione.",
    "Puoi chiedere aiuto per una difficoltà anche se agli altri sembra piccola.",
    "Non sei obbligato a rispondere a una domanda che ti mette a disagio.",
)
EVERGREEN = {
    "prezzi": (
        "/approfondimenti/inflazione-come-si-misura-italia-nic-foi-ipca.html",
        "Inflazione: cos’è e come si misura in Italia",
        "Paniere, indici Istat e differenza fra il dato medio e le spese della propria famiglia.",
    ),
    "chieri": (
        "/approfondimenti/violenza-domestica-chiedere-aiuto-112-1522.html",
        "Violenza domestica: come chiedere aiuto",
        "112 nelle emergenze, 1522 e centri antiviolenza: contatti pubblici e precauzioni per cercare sostegno.",
    ),
}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_doc(path, doc):
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def available_phrases():
    path = ROOT / "assets/data/frasi-nome.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    _, used = nome_pensiero.used(ROOT)
    for phrase in PHRASES:
        if phrase not in catalog:
            catalog.append(phrase)
        if sum(p not in used for p in catalog) >= 13:
            break
    if sum(p not in used for p in catalog) < 13:
        raise RuntimeError("Servono tredici pensieri nuovi")
    dump(path, catalog)


def make_image(article, sources):
    key = article["image_key"]
    original = ROOT.parent / "generated_images" / sources[key]
    canvas = ImageOps.fit(Image.open(original).convert("RGB"), (1600, 900), method=Image.Resampling.LANCZOS)
    variants = []
    for width in (480, 800, 1200):
        height = round(width * 9 / 16)
        path = ROOT / "assets/images/editorial-auto" / f"{article['slug']}-v{VERSION}-{width}.webp"
        temporary = path.with_suffix(".webp.tmp")
        canvas.resize((width, height), Image.Resampling.LANCZOS).save(temporary, "WEBP", quality=89, method=6)
        with Image.open(temporary) as check:
            check.load()
            assert check.format == "WEBP" and check.size == (width, height)
        temporary.replace(path)
        variants.append({"w": width, "h": height, "src": "/assets/images/editorial-auto/" + path.name,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    image = {"id": article["slug"], "article": "/notizie/" + article["slug"] + ".html",
             "alt": article["image_alt"], "prompt": sources[key + "_prompt"], "variants": variants,
             "disclosure": site.CAPTION, "generator": "OpenAI image generation", "aiGenerated": True,
             "documentaryPhoto": False, "officialArtwork": False, "sensitiveContext": bool(article.get("sensitive")),
             "weatherMap": False, "reenactedEvent": False, "logoApplied": False}
    if article.get("likeness"):
        image.update({"syntheticLikeness": "public-figure", "publicFigureName": article["likeness"]})
        if article.get("sensitive"):
            image.update({"portraitOnly": True, "portraitFormat": "neutral-isolated"})
    return image


def update_article(article, image, release):
    path = ROOT / "notizie" / (article["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    note = html.tostring(doc.xpath('//aside[contains(@class,"cm-name-card")]')[0])
    for selector, value in (
        ('//title', article["titolo"] + " | CurioMondo"),
        ('//main//h1[1]', article["titolo"]),
        ('//main/p[contains(@class,"subtitle")]', article["sommario"]),
    ):
        doc.xpath(selector)[0].text = value
    for selector, value in (
        ('//meta[@name="description"]', article["sommario"]),
        ('//meta[@property="og:title"]', article["titolo"]),
        ('//meta[@property="og:description"]', article["sommario"]),
        ('//meta[@property="og:image"]', "https://curiomondo.it" + image["variants"][-1]["src"]),
        ('//meta[@property="og:image:alt"]', image["alt"]),
    ):
        doc.xpath(selector)[0].set("content", value)
    published = None
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            published = data["datePublished"]
            data.update({"headline": article["titolo"], "description": article["sommario"],
                         "dateModified": release.isoformat(timespec="seconds"),
                         "image": ["https://curiomondo.it" + image["variants"][-1]["src"]]})
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if published is None:
        raise RuntimeError("Data originale assente")
    figure = doc.xpath('//figure[contains(@class,"article-image")]')[0]
    figure.set("data-ai-generated", "true")
    figure.set("data-sensitive-context", "true")
    figure.set("data-synthetic-likeness", "public-figure")
    figure.set("data-portrait-format", "neutral-isolated")
    hero = figure.xpath('.//img')[0]
    hero.set("src", ".." + image["variants"][1]["src"])
    hero.set("srcset", ", ".join(".." + v["src"] + " " + str(v["w"]) + "w" for v in image["variants"]))
    hero.set("alt", image["alt"])
    hero.set("width", "800")
    hero.set("height", "450")
    figure.xpath('./figcaption')[0].text = site.CAPTION
    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in article["paragrafi"]:
        etree.SubElement(body, "p").text = paragraph
    stats = doc.xpath('//div[contains(@class,"cm-insight-grid")]/div')
    for node, row in zip(stats, article["dati_chiave"]):
        node.xpath('./strong')[0].text = row["valore"]
        node.xpath('./span')[0].text = row["etichetta"]
    sources = doc.xpath('//div[contains(@class,"art-sources")]/ul')[0]
    for child in list(sources):
        sources.remove(child)
    for source in article["fonti"]:
        li = etree.SubElement(sources, "li")
        etree.SubElement(li, "a", href=source["url"], rel="noopener noreferrer", target="_blank").text = source["nome"]
    doc.xpath('//*[@id="readTime"]')[0].text = "1 min di lettura"
    assert note == html.tostring(doc.xpath('//aside[contains(@class,"cm-name-card")]')[0])
    save_doc(path, doc)
    article["published"] = published
    article["modified"] = release.isoformat(timespec="seconds")


def visible_date(article, release):
    path = ROOT / "notizie" / (article["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = article["published"]
            data["dateModified"] = article.get("modified", article["published"])
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dt = datetime.fromisoformat(article["published"]).astimezone(ROME)
    label = site._italian_date(article["published"]) + dt.strftime(" alle ore %H:%M")
    update = " · Aggiornato alle " + release.strftime("%H:%M") if article.get("update") else ""
    doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0].text = f"{label} · {article['luogo']}{update} · "
    stamp = release if article.get("update") else dt
    for br in doc.xpath('//div[contains(@class,"art-sources")]//small/br[1]'):
        br.tail = "Testo originale CurioMondo. Ultimo aggiornamento editoriale: " + site._italian_date(stamp.isoformat()) + stamp.strftime(" alle ore %H:%M") + "."
    if article["image_key"] in EVERGREEN:
        url, title, preview = EVERGREEN[article["image_key"]]
        if not (ROOT / url.lstrip("/")).is_file():
            raise RuntimeError("Approfondimento assente: " + url)
        for old in doc.xpath('//section[contains(@class,"cm-evergreen-reader")]'):
            old.getparent().remove(old)
        block = etree.Element("section", {"class": "cm-evergreen-reader", "aria-label": "Approfondimento collegato"})
        etree.SubElement(block, "small").text = "Per approfondire"
        etree.SubElement(block, "h2").text = title
        etree.SubElement(block, "p").text = preview
        etree.SubElement(block, "a", href=url).text = "Leggi l’approfondimento →"
        doc.xpath('//article[contains(@class,"art-body")]')[0].addnext(block)
    save_doc(path, doc)


def main():
    rows = json.loads((ROOT / "tools/news_batch_20261013_v847.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "tools/news_images_20261013_v847.json").read_text(encoding="utf-8"))
    if sys.argv[1:] == ["--sync-times"]:
        audit = json.loads((ROOT / "tools/news_audit_20261013_v847.json").read_text(encoding="utf-8"))
        stamps = {a["slug"]: a for a in audit["articles"]}
        release = datetime.fromisoformat(audit["release"])
        for article in rows:
            article["published"] = stamps[article["slug"]]["published"]
            article["modified"] = stamps[article["slug"]]["modified"]
            visible_date(article, release)
        site.sync_surfaces(rows, "/notizie/" + max(audit["articles"], key=lambda a: a["published"])["slug"] + ".html", VERSION, update_manifest=False)
        print("Metadati e superfici riallineati agli orari del lotto")
        return
    if len(sys.argv) == 3 and sys.argv[1] == "--repair-image":
        article = next(a for a in rows if a["image_key"] == sys.argv[2])
        image = make_image(article, sources)
        path = ROOT / "assets/data/editorial-images-v210.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["items"] = [image if i.get("id") == article["slug"] else i for i in registry["items"]]
        dump(path, registry)
        print("Varianti rigenerate e verificate:", article["image_key"])
        return
    release = datetime.now(ROME).replace(microsecond=0)
    new_rows = sorted((a for a in rows if not a.get("update")), key=lambda a: a["source_published"], reverse=True)
    assert len(new_rows) == len(OFFSETS) == 13
    assert release.date().isoformat() == "2026-10-13"
    for article in new_rows:
        if (ROOT / "notizie" / (article["slug"] + ".html")).exists():
            raise RuntimeError("Articolo già presente: " + article["slug"])
    available_phrases()
    images = []
    for article in rows:
        image = make_image(article, sources)
        if article.get("update"):
            update_article(article, image, release)
        else:
            site.write_article(article, image, VERSION)
        images.append(image)
    for article, minutes in zip(new_rows, OFFSETS):
        stamp = release - timedelta(minutes=minutes)
        if stamp < datetime.fromisoformat(article["source_published"]):
            raise RuntimeError("Data di pubblicazione precedente al riscontro: " + article["slug"])
        set_published(article["slug"], stamp)
        article["published"] = stamp.isoformat(timespec="seconds")
        article["modified"] = article["published"]
    for article in rows:
        visible_date(article, release)
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    replaced = {a["slug"] for a in rows}
    registry["items"] = images + [i for i in registry["items"] if i.get("id") not in replaced]
    registry["version"] = VERSION
    dump(registry_path, registry)
    # sync_surfaces conserva normalmente il sommario storico: questo aggiornamento
    # sostanziale richiede invece il nuovo sommario anche nelle card e nel feed.
    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8"))
    updated = {"/notizie/" + a["slug"] + ".html": a for a in rows if a.get("update")}
    for item in feed["items"]:
        if item.get("url") in updated:
            item["excerpt"] = updated[item["url"]]["sommario"]
    dump(feed_path, feed)
    site.sync_surfaces(rows, "/notizie/" + new_rows[0]["slug"] + ".html", VERSION, update_manifest=False)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                  "articleCount": int(state["articleCount"]) + len(new_rows),
                  "generatedEditorialImages": int(state["generatedEditorialImages"]) + len(rows),
                  "last_update": "ultime-notizie-ansa-v847", "date": release.date().isoformat(),
                  "release_date": release.date().isoformat(), "updated_at": release.isoformat(timespec="seconds"), "status": "ready"})
    dump(state_path, state)
    audit = {"version": VERSION, "release": release.isoformat(timespec="seconds"), "new_articles": 13,
             "updated_articles": 1, "new_images": 14, "push_executed": False, "manifest_accessed": False,
             "image_visual_review": "14 copertine controllate; Riccia rigenerata dal riferimento reale",
             "excluded": ["promozioni dello speciale Midterm, ripetute negli screenshot", "streaming ANSA Incontra sul fegato, non una nuova scoperta clinica"],
             "evergreen_linked": list(EVERGREEN),
             "evergreen_exception": "Per gli altri temi il catalogo non offre una guida pertinente: nessun collegamento forzato e nessuna nuova guida breve.",
             "articles": [{"slug": a["slug"], "title": a["titolo"], "action": "update" if a.get("update") else "new",
                           "published": a["published"], "modified": a.get("modified", a["published"]),
                           "source_published": a["source_published"], "sources": a["fonti"],
                           "words": sum(len(p.split()) for p in a["paragrafi"]), "paragraph_max": max(len(p.split()) for p in a["paragrafi"])} for a in rows]}
    dump(ROOT / "tools/news_audit_20261013_v847.json", audit)
    print(json.dumps({k: audit[k] for k in ("version", "release", "new_articles", "updated_articles", "new_images")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
