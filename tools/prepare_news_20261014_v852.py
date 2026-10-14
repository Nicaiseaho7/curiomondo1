#!/usr/bin/env python3
"""Prepara dieci articoli verificati e sincronizza le superfici una sola volta.

Il comando --release-now riallinea il lotto prima del primo commit.
Il manifest è escluso. Non effettua push né modifica il layout condiviso.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site
from tools import nome_pensiero
from tools import prepare_news_20261014_v851 as shared

VERSION = 852
ROME = ZoneInfo("Europe/Rome")
BATCH = ROOT / "tools/news_batch_20261014_v852.json"
IMAGES = ROOT / "tools/news_images_20261014_v852.json"
AUDIT = ROOT / "tools/news_audit_20261014_v852.json"
OFFSETS = (0, 5, 12, 20, 29, 39, 50, 62, 75, 89)
PHRASES = (
    "Puoi chiedere di parlarne domani se oggi ti manca la calma.",
    "Un messaggio può aspettare mentre stai cenando.",
    "Puoi scegliere un orario comodo per una visita che rimandi da tempo.",
    "Se una promessa ti pesa, puoi parlarne con chi l'ha ricevuta.",
    "Puoi mettere via il telefono quando vuoi ascoltare qualcuno.",
    "Puoi prenderti un giorno per capire se una proposta ti interessa.",
    "Hai il diritto di chiedere che una spiegazione sia più chiara.",
    "Puoi tenere per te una notizia finché ti senti pronto a condividerla.",
    "Se ti senti stanco, puoi scegliere un impegno in meno questa sera.",
    "Puoi ringraziare qualcuno anche dopo che è passato un po' di tempo.",
)

VALUES = {
    "irpef": "Distinzione tra aliquota vigente e proposta; simulazione originale di 500 euro lordi su 55 mila euro, con ipotesi e limiti.",
    "gas": "Costo alla produzione e prezzo di mercato distinti; previsione attribuita alla premier, senza promessa sulle bollette.",
    "provenzano": "Ricostruzione del confronto con entrambe le posizioni; accusa politica distinta da un fatto accertato.",
    "sixkings": "Calendario precedente e nuovo; motivazione ufficiale logistica distinta dal contesto di sicurezza.",
    "leone": "Interpretazione dello storico distinta da prognosi medica; 90 minuti di intervento distinti dalle tre ore in sala.",
    "burnham": "I 10 milioni accelerati fanno parte dei 45 milioni; impegno pluriennale distinto dall'aiuto immediato.",
    "centralpark": "Accordo politico distinto da legge approvata; data del voto e decorrenza futura, con tutele dei lavoratori.",
    "paolini": "Due segnalazioni riunite; punteggi e prossime avversarie distinti fra singolare e doppio, copertura italiana.",
    "padel": "40 milioni, non 40 mila; spesa, produzione e Pil distinti; calendario programmato distinto dal consuntivo 2025.",
    "arbitri": "Calendario pratico e ruoli degli ufficiali delle tre partite, con orari italiani.",
}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
        temporary = path.with_name(path.name + ".tmp")
        canvas.resize((width, height), Image.Resampling.LANCZOS).save(temporary, "WEBP", quality=89, method=6)
        with temporary.open("rb") as stream:
            os.fsync(stream.fileno())
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
    if sources.get(key + "_generation_prompt"):
        image["generationPrompt"] = sources[key + "_generation_prompt"]
    if article.get("likeness"):
        image.update({"syntheticLikeness": "public-figure", "publicFigureName": article["likeness"]})
        if article.get("sensitive"):
            image.update({"portraitOnly": True, "portraitFormat": "neutral-isolated"})
    return image

def finish(article, release):
    shared.finish_page(article, release)
    path = ROOT / "notizie" / (article["slug"] + ".html")
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for link in doc.xpath('//link[@rel="stylesheet"]'):
        if "global-header-v275.css" in link.get("href", ""):
            link.set("href", "/assets/css/global-header-v275.css?v=633")
    shared.save(path, doc)


def assign_dates(rows, release):
    for article, minutes in zip(rows, OFFSETS):
        stamp = release - timedelta(minutes=minutes)
        if article.get("source_published"):
            assert stamp >= datetime.fromisoformat(article["source_published"])
        article["published"] = stamp.isoformat(timespec="seconds")
        article["modified"] = article["published"]


def release_only(rows, release):
    for article in rows:
        check = subprocess.run(
            ["git", "cat-file", "-e", "HEAD:notizie/" + article["slug"] + ".html"],
            cwd=ROOT, capture_output=True)
        if check.returncode == 0:
            raise RuntimeError("Pagina già in HEAD: conservare la prima pubblicazione, " + article["slug"])
    assign_dates(rows, release)
    for article in rows:
        finish(article, release)
    shared.sync_complete(rows)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    audit["prepared_release"] = audit["release"]
    audit["release"] = release.isoformat(timespec="seconds")
    for entry, article in zip(audit["articles"], rows):
        entry.update(published=article["published"], modified=article["modified"])
    dump(AUDIT, audit)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["updated_at"] = release.isoformat(timespec="seconds")
    dump(state_path, state)
    print("Lotto riallineato prima del primo commit:", release.isoformat())


def main():
    shared.VERSION = VERSION
    rows = json.loads(BATCH.read_text(encoding="utf-8"))
    release = datetime.now(ROME).replace(microsecond=0)
    if release.date().isoformat() != "2026-10-14":
        raise RuntimeError("Riverificare le notizie per una data di rilascio diversa dal 14 ottobre.")
    if sys.argv[1:] == ["--release-now"]:
        release_only(rows, release)
        return
    if sys.argv[1:]:
        raise RuntimeError("Usare nessun argomento oppure --release-now.")
    assert len(rows) == len(OFFSETS) == 10
    for article in rows:
        assert not (ROOT / "notizie" / (article["slug"] + ".html")).exists(), article["slug"]
        assert 1 <= len(article["fonti"]) <= 2
        assert max(len(p.split()) for p in article["paragrafi"]) <= 60
        assert article["formato"] == "flash"

    phrases_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
    _, used = nome_pensiero.used(ROOT)
    for phrase in PHRASES:
        if phrase not in phrases:
            phrases.append(phrase)
    assert sum(p not in used for p in phrases) >= 10
    dump(phrases_path, phrases)

    sources = json.loads(IMAGES.read_text(encoding="utf-8"))
    images = []
    for article in rows:
        image = image_for(article, sources)
        site.write_article(article, image, VERSION)
        images.append(image)

    assign_dates(rows, release)
    for article in rows:
        finish(article, release)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert not {a["slug"] for a in rows}.intersection(i.get("id") for i in registry["items"])
    registry["items"] = images + registry["items"]
    registry["version"] = VERSION
    dump(registry_path, registry)

    shared.sync_complete(rows)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
        "articleCount": int(state["articleCount"]) + 10,
        "generatedEditorialImages": int(state["generatedEditorialImages"]) + 10,
        "last_update": "segnalazioni-sera-14-ottobre-v852",
        "date": release.date().isoformat(), "release_date": release.date().isoformat(),
        "updated_at": release.isoformat(timespec="seconds"), "status": "ready",
    })
    dump(state_path, state)
    audit = {
        "version": VERSION, "release": release.isoformat(timespec="seconds"),
        "new_articles": 10, "updated_articles": 0, "new_images": 10,
        "push_executed": False, "manifest_accessed": False,
        "source_list": "Fonti per la ricerca degli articoli.txt, versione 7 ottobre 2026",
        "selected_user_signals": [1, 3, 4, 5, 6, 10, 11, 15, 16, 17, 20],
        "combined_signals": {"paolini": [15, 20]},
        "not_in_this_batch": [2, 7, 8, 9, 12, 13, 14, 18, 19],
        "selection_reason": "Limite di dieci articoli per richiesta; nove segnalazioni restano fuori dal lotto, senza giudizio di falsità.",
        "corrections": [
            "Padel: oltre 40 milioni di praticanti, non 40 mila.",
            "Irpef: 33% già vigente fino a 50 mila euro; proposta di estensione oltre il limite, fino a 60 mila.",
            "Central Park: accordo e voto atteso, non divieto già entrato in vigore.",
            "Six Kings Slam: annuncio di Riyadh Season sulle nuove date e sulla logistica distinto dal contesto degli attacchi.",
        ],
        "image_visual_review": "Dieci copertine viste singolarmente, identità confrontate con riferimenti reali, contesti sensibili in ritratto neutrale; sfondi di Central Park e Dall'Ara rifiniti.",
        "evergreen_exception": "Le guide esistenti su SBU e regolamento metano non riguardano il meccanismo centrale di questi fatti; nessun collegamento forzato.",
        "format_exception": "Flash da 153–216 parole: fatti circoscritti, massimo due fonti, contenuto proporzionato senza riempitivo.",
        "primary_access_limits": [
            "Governo italiano: pagine ufficiali trovate, apertura 403; resoconto Camera disponibile solo per la seduta già verbalizzata. Dichiarazioni Meloni controllate nei resoconti giornalistici e normativa Irpef ufficiale.",
            "Agenzia Entrate: testo ufficiale indicizzato con nota sull'aliquota 2026; apertura diretta non disponibile.",
            "Saudi Press Agency: annuncio ufficiale indicizzato; apertura in timeout. Nuove date e motivazione confermate anche da Reuters e Sky Sports.",
            "GOV.UK e Reuters: metadati datati 13 ottobre; il resoconto Reuters identifica il colloquio svolto mercoledì 14 ottobre.",
        ],
        "browser_visual_qa": "Da completare",
        "articles": [{
            "slug": a["slug"], "title": a["titolo"], "action": "new",
            "published": a["published"], "modified": a["modified"],
            "source_date": a["source_date"], "sources": a["fonti"],
            "words": sum(len(p.split()) for p in a["paragrafi"]),
            "paragraph_max": max(len(p.split()) for p in a["paragrafi"]),
            "risk": a["risk"], "original_value": VALUES[a["image_key"]],
            "editorial_checks": {
                "facts": True, "sources": True, "headline": True,
                "original_value": True, "short_paragraphs": True, "no_duplicate": True,
            },
        } for a in rows],
    }
    dump(AUDIT, audit)
    print(json.dumps({k: audit[k] for k in ("version", "release", "new_articles", "new_images")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

