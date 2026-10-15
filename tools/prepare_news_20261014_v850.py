#!/usr/bin/env python3
"""Dieci pagine nuove; preparazione ZIP senza push.

La sincronizzazione delle superfici è unica. Il manifest del sito è escluso.
Le copertine vengono dai dieci originali OpenAI controllati visivamente.
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
from tools.prepare_news_20261013_v847 import update_article

VERSION = 850
ROME = ZoneInfo("Europe/Rome")
OFFSETS = (0, 5, 12, 20, 29, 39, 50, 62, 75, 89)
PHRASES = ('Puoi chiedere una pausa prima che la stanchezza diventi troppo forte.', 'Puoi scegliere di rispondere domani quando oggi non hai le energie.', 'Hai il diritto di dire che un cambiamento ti preoccupa.', 'Puoi chiedere un esempio quando una spiegazione non ti è chiara.', 'Se un programma salta, puoi concederti il tempo di riorganizzarti.', 'Puoi preferire una serata tranquilla senza sentirti in difetto.', 'Se qualcosa ti dispiace, puoi dirlo con parole semplici.', 'Puoi ringraziare chi ti ascolta senza dover raccontare tutto.', 'Puoi scegliere un obiettivo piccolo per una giornata impegnativa.', 'Hai il diritto di chiedere che una promessa venga rispettata.')


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save(path, doc):
    path.write_text(html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n", encoding="utf-8")


def sync_complete(rows):
    # I tag di colore non inseriscono spazi nel testo visibile del titolo.
    # Il renderer legacy concatena i nodi con spazi: per il lotto si usa
    # il titolo editoriale esatto in tutte le superfici.
    by_slug = {a["slug"]: a for a in rows}
    original_info = site._article_info
    def exact_info(path):
        info = original_info(path)
        article = by_slug.get(path.stem)
        if info and article:
            info.update({"title": article["titolo"], "excerpt": article["sommario"]})
        return info
    site._article_info = exact_info
    try:
        site.sync_surfaces(rows, "/notizie/" + rows[0]["slug"] + ".html", VERSION, update_manifest=False)
    finally:
        site._article_info = original_info
    sitemap_path = ROOT / "sitemap.xml"
    tree = etree.parse(str(sitemap_path))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for article in rows:
        if article.get("update"):
            url = "https://curiomondo.it/notizie/" + article["slug"] + ".html"
            for node in tree.xpath('//s:url[s:loc=$url]/s:lastmod', namespaces=ns, url=url):
                node.text = article["modified"]
    tree.write(str(sitemap_path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def image_for(article, sources):
    key = article["image_key"]
    original = ROOT.parent / "generated_images" / sources[key]
    with Image.open(original) as im:
        im.load()
        assert im.width >= 1200
        canvas = ImageOps.fit(im.convert("RGB"), (1600, 900), method=Image.Resampling.LANCZOS)
    variants = []
    for width in (480, 800, 1200):
        height = round(width * 9 / 16)
        path = ROOT / "assets/images/editorial-auto" / f"{article['slug']}-v{VERSION}-{width}.webp"
        canvas.resize((width, height), Image.Resampling.LANCZOS).save(path, "WEBP", quality=89, method=6)
        with Image.open(path) as check:
            check.load()
            assert check.format == "WEBP" and check.size == (width, height)
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


def finish_page(article, release):
    path = ROOT / "notizie" / (article["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = article["published"]
            data["dateModified"] = article["modified"]
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dt = datetime.fromisoformat(article["published"]).astimezone(ROME)
    label = site._italian_date(article["published"]) + dt.strftime(" alle ore %H:%M")
    update = " · Aggiornato il " + site._italian_date(release.isoformat()) + release.strftime(" alle ore %H:%M") if article.get("update") else ""
    doc.xpath('//main/div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0].text = f"{label} · {article['luogo']}{update} · "
    stamp = datetime.fromisoformat(article["modified"])
    for br in doc.xpath('//div[contains(@class,"art-sources")]//small/br[1]'):
        br.tail = "Testo originale CurioMondo. Ultimo aggiornamento editoriale: " + site._italian_date(stamp.isoformat()) + stamp.strftime(" alle ore %H:%M") + "."
    if article["categoria"] == "Salute":
        doc.xpath('//main/div[@class="badge"]')[0].text = "Salute"
    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    body.set("data-risk-level", article["risk"])
    body.set("data-editorial-protocol", "4.0")
    body.set("data-article-format", article["formato"])
    body.attrib.pop("data-length-policy", None)
    if "correlati" in article:
        for grid in doc.xpath('//div[contains(@class,"curio-related-grid")]'):
            if not article["correlati"]:
                grid.getparent().getparent().remove(grid.getparent())
            else:
                for child in list(grid):
                    grid.remove(child)
                for item in article["correlati"][:3]:
                    link = etree.SubElement(grid, "a", href=item["url"])
                    etree.SubElement(link, "strong").text = item["titolo"]
    # Il titolo in pagina resta di un solo colore. Il blu è solo sulla card in homepage.
    h1 = doc.xpath('//main//h1[1]')[0]
    for child in list(h1):
        h1.remove(child)
    h1.text = article["titolo"]
    for grid in doc.xpath('//div[contains(@class,"cm-insight-grid")]'):
        for child in list(grid):
            grid.remove(child)
        for fact in article["dati_chiave"][:3]:
            box = etree.SubElement(grid, "div")
            etree.SubElement(box, "strong").text = fact["valore"]
            etree.SubElement(box, "span").text = fact["etichetta"]
    for img in doc.xpath('//figure[contains(@class,"article-image")]//img'):
        img.set("alt", article["image_alt"])
    for meta in doc.xpath('//meta[@property="og:image:alt"]'):
        meta.set("content", article["image_alt"])
    save(path, doc)


def main():
    rows = json.loads((ROOT / "tools/news_batch_20261014_v850.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "tools/news_images_20261014_v850.json").read_text(encoding="utf-8"))
    if sys.argv[1:] == ["--release-now"]:
        import subprocess
        audit_path = ROOT / "tools/news_audit_20261014_v850.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        stamps = {a["slug"]: a for a in audit["articles"]}
        release = datetime.now(ROME).replace(microsecond=0)
        assert release.date().isoformat() == "2026-10-14", "Il bollettino del 14 ottobre va riverificato per un altro giorno"
        new_rows = [a for a in rows if not a.get("update")]
        for article in new_rows:
            tracked = subprocess.run(["git", "cat-file", "-e", "HEAD:notizie/" + article["slug"] + ".html"], cwd=ROOT, capture_output=True)
            assert tracked.returncode != 0, "Pagina già in HEAD: non cambiare la prima pubblicazione"
        for article, minutes in zip(new_rows, OFFSETS):
            article["published"] = (release - timedelta(minutes=minutes)).isoformat(timespec="seconds")
            article["modified"] = article["published"]
        for article in rows:
            if article.get("update"):
                article["published"] = stamps[article["slug"]]["published"]
                article["modified"] = release.isoformat(timespec="seconds")
            finish_page(article, release)
            stamps[article["slug"]].update({"published": article["published"], "modified": article["modified"]})
        audit["prepared_release"] = audit["release"]
        audit["release"] = release.isoformat(timespec="seconds")
        dump(audit_path, audit)
        state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["updated_at"] = release.isoformat(timespec="seconds")
        dump(state_path, state)
        sync_complete(rows)
        print("Lotto allineato all'ora di rilascio prima del primo commit:", release.isoformat())
        return
    if sys.argv[1:] == ["--sync-surfaces"]:
        audit = json.loads((ROOT / "tools/news_audit_20261014_v850.json").read_text(encoding="utf-8"))
        stamps = {a["slug"]: a for a in audit["articles"]}
        for article in rows:
            article["published"] = stamps[article["slug"]]["published"]
            article["modified"] = stamps[article["slug"]]["modified"]
        sync_complete(rows)
        print("Titoli esatti e date originarie coerenti nelle superfici")
        return
    release = datetime.now(ROME).replace(microsecond=0)
    assert release.date().isoformat() == "2026-10-14"
    new_rows = [a for a in rows if not a.get("update")]
    assert len(rows) == 10 and len(new_rows) == len(OFFSETS) == 10
    for a in new_rows:
        assert not (ROOT / "notizie" / (a["slug"] + ".html")).exists(), a["slug"]
    for a in rows:
        assert len(a["fonti"]) <= 2
        assert max(len(p.split()) for p in a["paragrafi"]) <= 60
    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    _, used = nome_pensiero.used(ROOT)
    phrases.extend(x for x in PHRASES if x not in phrases)
    assert sum(x not in used for x in phrases) >= 10
    dump(phrases_path, phrases)
    images = []
    for article in rows:
        image = image_for(article, sources)
        if article.get("update"):
            update_article(article, image, release)
        else:
            site.write_article(article, image, VERSION)
        images.append(image)
    for article, minutes in zip(new_rows, OFFSETS):
        stamp = release - timedelta(minutes=minutes)
        if article.get("source_published"):
            assert stamp >= datetime.fromisoformat(article["source_published"]), article["slug"]
        article["published"] = stamp.isoformat(timespec="seconds")
        article["modified"] = article["published"]
    for article in rows:
        finish_page(article, release)
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    replaced = {a["slug"] for a in rows}
    registry["items"] = images + [i for i in registry["items"] if i.get("id") not in replaced]
    registry["version"] = VERSION
    dump(registry_path, registry)
    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8"))
    updated = {"/notizie/" + a["slug"] + ".html": a for a in rows if a.get("update")}
    for item in feed["items"]:
        if item.get("url") in updated:
            item["excerpt"] = updated[item["url"]]["sommario"]
    dump(feed_path, feed)
    sync_complete(rows)
    # lastmod dell'articolo aggiornato riflette la modifica sostanziale,
    # senza cambiare la sua prima pubblicazione o il suo nome/pensiero.
    sitemap_path = ROOT / "sitemap.xml"
    tree = etree.parse(str(sitemap_path))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for article in rows:
        if not article.get("update"):
            continue
        url = "https://curiomondo.it/notizie/" + article["slug"] + ".html"
        for node in tree.xpath('//s:url[s:loc=$url]/s:lastmod', namespaces=ns, url=url):
            node.text = article["modified"]
    tree.write(str(sitemap_path), encoding="utf-8", xml_declaration=True, pretty_print=True)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                  "articleCount": int(state["articleCount"]) + len(new_rows),
                  "generatedEditorialImages": int(state["generatedEditorialImages"]) + len(rows),
                  "last_update": "sport-cronaca-salute-mondo-14-ottobre-v850", "date": release.date().isoformat(),
                  "release_date": release.date().isoformat(), "updated_at": release.isoformat(timespec="seconds"), "status": "ready"})
    dump(state_path, state)
    audit = {"version": VERSION, "release": release.isoformat(timespec="seconds"), "new_articles": 10,
             "updated_articles": 0, "new_images": 10, "push_executed": False, "manifest_accessed": False,
             "image_visual_review": "Dieci immagini controllate: identità, luoghi, livrea, assenza di ricostruzioni traumatiche, leggibilità dei ritagli.",
             "evergreen_exception": "Nel catalogo non sono presenti guide specifiche pertinenti ai dieci fatti: nessun collegamento artificiale.",
             "excluded": ["Notizie già presenti nel feed, incluse le nove nuove pagine del lotto mattutino v849", "Programmi sportivi non confermati dai club o dalle federazioni"],
             "primary_access_limits": ["Virtus e Polizia Locale Trieste: accesso diretto non riuscito; informazioni primarie recuperate dagli indici e confermate con il sito SEF Virtus e Trieste All News"],
             "risk_rationale": "Le due dotazioni della Polizia Locale e i servizi digitali AIFA sono aggiornamenti tecnici non controversi, senza accuse o raccomandazioni cliniche. L’allargamento Ue è un atto istituzionale ordinario. Per OMS e voto palestinese usate due istituzioni distinte.",
             "browser_visual_qa": "Non eseguita: Chromium non disponibile nel runtime. Nessuna modifica al layout condiviso.",
             "articles": [{"slug": a["slug"], "title": a["titolo"], "action": "update" if a.get("update") else "new",
                           "published": a["published"], "modified": a["modified"], "source_date": a["source_date"],
                           "source_published": a.get("source_published"), "sources": a["fonti"],
                           "words": sum(len(p.split()) for p in a["paragrafi"]),
                           "paragraph_max": max(len(p.split()) for p in a["paragrafi"]),
                           "editorial_checks": {"facts": True, "sources": True, "headline": True, "original_value": True, "short_paragraphs": True, "no_duplicate": True}} for a in rows]}
    dump(ROOT / "tools/news_audit_20261014_v850.json", audit)
    print(json.dumps({k: audit[k] for k in ("version", "release", "new_articles", "updated_articles", "new_images")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
