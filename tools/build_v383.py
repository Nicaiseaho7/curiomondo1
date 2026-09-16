#!/usr/bin/env python3
"""Aggiorna il decreto bollo/accise e pubblica l'inchiesta William Solo."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 383
PUBLISHED_BOLLO = "2026-09-16T16:48:39+02:00"
UPDATED_BOLLO = "2026-09-16T17:49:45+02:00"
PUBLISHED_WILLIAM = "2026-09-16T17:49:45+02:00"
FEATURED_URL = "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html"

BOLLO_SLUG = "bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026"
WILLIAM_SLUG = "william-solo-procura-chiede-arresto-finti-incidenti-16-settembre-2026"

BOLLO_IMAGE = ROOT.parent / "generated_images" / "exec-d50e7ecf-c0cf-4cbb-b57f-c9e1ed5d0935.png"
WILLIAM_IMAGE = ROOT.parent / "generated_images" / "exec-8ac75023-5e5f-49ce-9dd1-48e36def22d7.png"

BOLLO = {
    "slug": BOLLO_SLUG,
    "titolo": "Bollo auto, il Cdm approva l’esenzione fino a 80 kW dal 2027",
    "sommario": "Il decreto elimina il bollo per auto fino a 80 kW, motocicli e ciclomotori dal 2027, con un solo veicolo agevolabile per proprietario. Lo sconto sulle accise del gasolio prosegue fino al 5 ottobre con riduzione graduale.",
    "categoria": "Italia", "luogo": "Roma", "formato": "standard",
    "parole_chiave_titolo": ["Cdm approva", "80 kW"],
    "dati_chiave": [
        {"icona": "◆", "valore": "80 kW", "etichetta": "potenza massima delle auto esenti"},
        {"icona": "●", "valore": "2027", "etichetta": "anno di avvio dell’esenzione"},
        {"icona": "↓", "valore": "5 ottobre", "etichetta": "termine del decalage sul gasolio"},
    ],
    "paragrafi": [
        "Il Consiglio dei ministri ha approvato mercoledì 16 settembre 2026 il decreto legge che abolisce dal 2027 il bollo per le auto con potenza fino a 80 kW, oltre che per motocicli e ciclomotori. Lo stesso provvedimento proroga fino al 5 ottobre il taglio delle accise sul gasolio, riducendo progressivamente lo sconto.",
        "L’approvazione trasforma in un provvedimento governativo l’annuncio diffuso poche ore prima da Palazzo Chigi. La soglia di 80 kW equivale a circa 109 cavalli, ma il dato decisivo per l’agevolazione sarà quello riportato nei documenti del veicolo e nelle regole applicative definitive.",
        "L’esenzione potrà essere usata per un solo veicolo dello stesso proprietario. Chi possiede sia un’auto sia un ciclomotore non potrà quindi cumulare il beneficio su entrambi; il ciclomotore sarà esente soltanto se l’agevolazione non viene già impiegata per l’auto.",
        "Per i contribuenti non cambia nulla sulle scadenze del 2026. La nuova disciplina è prevista dal 2027 e richiederà la pubblicazione del decreto e delle istruzioni operative, necessarie per chiarire registrazione del mezzo prescelto, cointestazioni ed eventuali controlli automatici.",
        "La platea annunciata in precedenza dal governo era di circa 14,5 milioni di veicoli, comprendendo tutti i motocicli e oltre il 70% delle auto piccole e medie. La soglia ora indicata consente una verifica più concreta, ma il costo complessivo e il meccanismo di compensazione per Regioni e Province autonome restano da precisare nel testo ufficiale.",
        "Il capitolo carburanti riguarda il gasolio e non cancella le accise. Lo sconto viene prorogato fino al 5 ottobre attraverso un decalage: il vantaggio fiscale si ridurrà per fasi, invece di terminare in un’unica data con lo stesso importo applicato fino al giorno precedente.",
        "Il valore effettivo alla pompa dipenderà non soltanto dall’accisa, ma anche dai prezzi internazionali dei prodotti raffinati, dai margini distributivi e dai tempi con cui le variazioni fiscali vengono trasferite. Per questo la proroga non garantisce da sola un prezzo finale stabile.",
        "La misura sul bollo incide su una tassa automobilistica gestita a livello regionale o provinciale. Fino all’entrata in vigore delle nuove regole, i proprietari devono continuare a rispettare importi e scadenze vigenti nel proprio territorio, senza sospendere pagamenti sulla base dell’annuncio.",
    ],
    "fonti": [
        {"url": "https://www.ansa.it/canale_motori/notizie/istituzioni/2026/09/16/fonti-palazzo-chigi-oggi-via-il-bollo-per-auto-piccole-e-medie_cb12208d-db01-44ea-a5b5-7535dd0d2550.html", "descrizione": "ANSA — approvazione del decreto, soglia di 80 kW, decorrenza 2027 e proroga delle accise fino al 5 ottobre."},
        {"url": "https://www.reuters.com/business/italy-scraps-road-tax-most-cars-election-nears-2026-09-16/", "descrizione": "Reuters — platea annunciata, limite di un veicolo per persona e aspetti finanziari ancora da definire."},
        {"url": "https://www.aci.it/servizi/guida-al-bollo-auto/", "descrizione": "Automobile Club d’Italia — disciplina vigente e guida istituzionale al bollo auto."},
    ],
    "correlati": [
        {"url": "/notizie/diesel-sconto-accise-proroga-17-settembre-2026.html", "titolo": "Diesel, prorogato fino al 17 settembre lo sconto di 17 centesimi"},
        {"url": "/notizie/bonus-colonnine-domestiche-2026-domande-dal-22-settembre.html", "titolo": "Bonus colonnine domestiche 2026: domande dal 22 settembre"},
        {"url": "/notizie/codice-strada-patente-17-anni-superamento-destra-proposte-mit-2026.html", "titolo": "Codice della Strada, le nuove proposte del MIT"},
    ],
}

WILLIAM = {
    "slug": WILLIAM_SLUG,
    "titolo": "William Solo, la procura chiede l’arresto per presunte frodi assicurative",
    "sommario": "I pm di Genova contestano un’associazione per delinquere legata a falsi incidenti stradali. Il gip ha fissato gli interrogatori preventivi per l’inizio di ottobre: le richieste cautelari non sono ancora una decisione del giudice.",
    "categoria": "Cronaca", "luogo": "Genova", "formato": "standard",
    "parole_chiave_titolo": ["William Solo", "chiede l’arresto"],
    "dati_chiave": [
        {"icona": "◆", "valore": "9", "etichetta": "misure cautelari richieste dai pm"},
        {"icona": "●", "valore": "dal 2020", "etichetta": "periodo minimo contestato"},
        {"icona": "→", "valore": "ottobre", "etichetta": "interrogatori preventivi fissati dal gip"},
    ],
    "paragrafi": [
        "La procura di Genova ha chiesto misure cautelari per lo youtuber e biker William Solo, all’anagrafe Ilija Kosanke, nell’inchiesta su presunti falsi incidenti organizzati per ottenere risarcimenti assicurativi. Il gip ha fissato gli interrogatori preventivi per l’inizio di ottobre e non ha ancora deciso sulle richieste dei pm.",
        "Kosanke, genovese di 54 anni, è noto online per il video e il tormentone «può accompagnare solo». Secondo l’accusa avrebbe partecipato, con il supporto di altre persone e di alcune officine, a un sistema attivo almeno dal 2020 e basato sulla simulazione di sinistri stradali.",
        "Le contestazioni sono formulate dagli inquirenti e dovranno essere vagliate dal giudice. La richiesta di arresto non equivale a un arresto eseguito né a una condanna: in questa fase vale la presunzione di innocenza e gli indagati potranno esporre le proprie difese negli interrogatori.",
        "Il pubblico ministero Luca Scorza Azzarà ha chiesto complessivamente due misure in carcere e sette agli arresti domiciliari. Il Secolo XIX riferisce che l’indagine coinvolge 36 persone e comprende anche sequestri, delineando un’inchiesta più ampia rispetto alle sole posizioni raggiunte dalle richieste cautelari.",
        "Tra gli indagati figurano, secondo le ricostruzioni pubblicate, un assistente della polizia locale e due avvocati. Per il dipendente pubblico è stata chiesta la sospensione dall’ufficio; per i legali, invece, la sospensione temporanea dall’albo.",
        "Gli inquirenti sostengono che il gruppo avrebbe inscenato per anni un numero elevato di incidenti. Restano però da accertare in sede giudiziaria il ruolo attribuito a ciascun indagato, il numero dei singoli episodi, l’ammontare complessivo dei risarcimenti e la tenuta delle prove raccolte.",
        "L’interrogatorio preventivo consente alla persona sottoposta a indagine di essere sentita prima che il giudice decida su una misura cautelare richiesta dalla procura. L’esito può essere l’accoglimento, il rigetto o l’applicazione di una misura diversa, in base alle esigenze cautelari e agli elementi disponibili.",
        "La vicenda ha rilievo pubblico per la notorietà online di Kosanke e per la presenza di professionisti e di un dipendente pubblico tra gli indagati. La responsabilità penale, tuttavia, potrà essere stabilita soltanto al termine del procedimento e non può essere desunta dalla richiesta avanzata dall’accusa.",
    ],
    "fonti": [
        {"url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/16/finti-incidenti-per-truffare-assicurazioni-la-procura-chiede-larresto-per-lo-youtuber_eb5a504d-c1ba-4142-8e0e-4c23a0673ab8.html", "descrizione": "ANSA — richieste cautelari, contestazioni, persone coinvolte e data degli interrogatori preventivi."},
        {"url": "https://www.ilsecoloxix.it/", "descrizione": "Il Secolo XIX — riscontro locale sull’inchiesta, le 36 persone coinvolte e i sequestri."},
        {"url": "https://www.genova24.it/", "descrizione": "Genova24 — conferma locale dell’indagine e della posizione attribuita a William Solo."},
    ],
    "correlati": [
        {"url": "/notizie/truffa-specchietto-inseguimento-200-kmh-torino-settimo-5-settembre-2026.html", "titolo": "Truffa dello specchietto a Torino: fuga dopo 30 euro sottratti"},
        {"url": "/notizie/revolut-pec-istituzionale-italiana-dati-clienti-16-settembre-2026.html", "titolo": "Revolut, PEC istituzionale usata per ottenere dati di 680 clienti"},
        {"url": "/notizie/piantedosi-casapound-roma-sara-sgomberata-settembre-2026.html", "titolo": "Piantedosi: «CasaPound a Roma sarà sgomberata»"},
    ],
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_variants(source: Path, folder: str, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio); left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio); top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets" / "images" / folder
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=84, method=6)
        variants.append({"w": width, "src": f"/assets/images/{folder}/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def stamp(path: Path, published: str, modified: str) -> None:
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{modified}"', page)
    path.write_text(page, encoding="utf-8")


def main() -> None:
    bollo_image = {"key": f"{BOLLO_SLUG}-ai-openai-v{VERSION}", "aiGenerated": True, "documentaryPhoto": False,
        "variants": image_variants(BOLLO_IMAGE, "editorial-auto", f"{BOLLO_SLUG}-ai-openai-v{VERSION}"),
        "alt": "Scena editoriale contestuale con auto compatta, motocicletta e ciclomotore presso un distributore italiano, non fotografia del Consiglio dei ministri.",
        "disclosure": CAPTION, "sensitiveContext": False}
    william_image = {"key": f"{WILLIAM_SLUG}-ai-openai-v{VERSION}", "aiGenerated": True, "documentaryPhoto": False,
        "variants": image_variants(WILLIAM_IMAGE, "editorial-cronaca", f"{WILLIAM_SLUG}-ai-openai-v{VERSION}"),
        "alt": "Ritratto editoriale neutrale e isolato dello youtuber William Solo in un contesto giudiziario sensibile; somiglianza sintetica non documentaria.",
        "disclosure": CAPTION, "sensitiveContext": True, "syntheticLikeness": "public-figure",
        "portraitOnly": True, "portraitFormat": "neutral-isolated", "reenactedEvent": False,
        "prompt": "Sensitive-context neutral editorial portrait of public figure William Solo, neutral isolated studio portrait, no arrest, accident or alleged conduct depicted."}

    (ROOT / "notizie" / f"{BOLLO_SLUG}.html").unlink()
    write_article(BOLLO, bollo_image, VERSION)
    write_article(WILLIAM, william_image, VERSION)
    stamp(ROOT / "notizie" / f"{BOLLO_SLUG}.html", PUBLISHED_BOLLO, UPDATED_BOLLO)
    stamp(ROOT / "notizie" / f"{WILLIAM_SLUG}.html", PUBLISHED_WILLIAM, PUBLISHED_WILLIAM)
    BOLLO["published"] = UPDATED_BOLLO
    WILLIAM["published"] = PUBLISHED_WILLIAM
    register_image(bollo_image, BOLLO_SLUG, VERSION)
    register_image(william_image, WILLIAM_SLUG, VERSION)
    items = sync_surfaces([BOLLO, WILLIAM], FEATURED_URL, VERSION)

    for article, image, published, status in ((BOLLO, bollo_image, UPDATED_BOLLO, "UFFICIALE"), (WILLIAM, william_image, PUBLISHED_WILLIAM, "IN SVILUPPO")):
        write_json(ROOT / "contenuti" / "notizie" / f"{article['slug']}.json", {
            "slug": article["slug"], "title": article["titolo"], "excerpt": article["sommario"],
            "category": article["categoria"], "published_at": published, "updated_at": published,
            "status": status, "body": article["paragrafi"], "sources": article["fonti"], "image": image,
        })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-16", "type": "content-release",
        "news_added": [WILLIAM_SLUG], "news_updated": [BOLLO_SLUG],
        "change": "Aggiornato il decreto bollo/accise e pubblicata l’inchiesta William Solo",
        "image_policy_applied": "two-new-openai-editorial-images"}
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8"))
            state.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
                "date": "2026-09-16", "release_date": "2026-09-16", "last_update": "bollo-decreto-william-solo-v383"})
            state["articleCount"] = 262
            state["generatedEditorialImages"] = 145
            write_json(path, state)

    assert any(i["url"] == f"/notizie/{WILLIAM_SLUG}.html" for i in items)
    print(json.dumps({"status": "ok", "version": VERSION, "added": WILLIAM_SLUG, "updated": BOLLO_SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
