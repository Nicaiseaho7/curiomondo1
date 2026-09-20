#!/usr/bin/env python3
"""Pubblica il pacchetto di ultime notizie del 20 settembre 2026."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article


VERSION = 457
DATE = "2026-09-20"
SOURCES = {
    "acosta": Path("/workspace/scratch/63d8c74bad9c/generated_images/exec-1cf51be4-e3ed-4195-9605-2d1503572a2c.png"),
    "meloni": Path("/workspace/scratch/63d8c74bad9c/generated_images/exec-ab83d606-2c17-4440-a35e-296c342fc891.png"),
    "mosca": Path("/workspace/scratch/63d8c74bad9c/generated_images/exec-7d15324f-1aad-44e1-9ade-555fe3b9d771.png"),
}


def write_json(path: Path, data: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variants(source: Path, key: str) -> list[dict[str, object]]:
    image = Image.open(source).convert("RGB")
    ratio = 1.5
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    folder = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        target = folder / f"{key}-{width}.webp"
        resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
        resized.save(target, "WEBP", quality=86, method=6)
        result.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{target.name}",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "bytes": target.stat().st_size,
        })
    return result


ARTICLES = [
    {
        "source_key": "acosta",
        "slug": "pedro-acosta-prima-vittoria-motogp-gp-austria-20-settembre-2026",
        "titolo": "MotoGP, Pedro Acosta vince in Austria: è il primo successo nella classe regina",
        "sommario": "Il pilota KTM supera Jorge Martin al nono giro e trionfa al Red Bull Ring. Marco Bezzecchi completa il podio, Marc Marquez chiude quinto.",
        "categoria": "Sport",
        "luogo": "Spielberg",
        "formato": "flash",
        "stato": "CONFERMATA",
        "parole_chiave_titolo": ["Pedro Acosta", "primo successo"],
        "dati_chiave": [
            {"icona": "●", "valore": "1ª", "etichetta": "vittoria di Acosta in MotoGP"},
            {"icona": "↗", "valore": "9° giro", "etichetta": "sorpasso decisivo su Martin"},
            {"icona": "◆", "valore": "37", "etichetta": "numero della KTM vincitrice"},
        ],
        "paragrafi": [
            "Pedro Acosta ha vinto il Gran Premio d’Austria di MotoGP al Red Bull Ring di Spielberg, conquistando il primo successo nella classe regina. Il ventiduenne spagnolo della KTM ha preceduto Jorge Martin e Marco Bezzecchi, entrambi su Aprilia.",
            "Partito dalla terza posizione, Acosta ha superato Martin al nono dei 28 giri e ha poi costruito il margine decisivo. La vittoria arriva il giorno dopo la caduta nella Sprint, quando era al comando con un vantaggio consistente.",
            "Alle spalle dei primi tre, Ai Ogura ha chiuso quarto e Marc Marquez quinto. Martin conserva la testa del Mondiale con 306 punti, dodici in più di Marquez; Bezzecchi resta terzo a quota 264.",
            "Il risultato ha un peso particolare per KTM, ottenuto sulla pista di casa del costruttore austriaco. Acosta, campione Moto3 nel 2021 e Moto2 nel 2023, lascerà la squadra a fine stagione per passare alla Ducati.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/sports/acosta-recovers-sprint-exit-beat-martin-maiden-motogp-win-austria-2026-09-20/", "descrizione": "Reuters — cronaca della gara, sorpasso decisivo, podio e classifica mondiale."},
            {"url": "https://www.ansa.it/sito/notizie/sport/moto/2026/09/20/motogp-acosta-sulla-ktm-vince-il-gp-daustria_27ce93da-f760-4556-aeb4-8d072cf34f8a.html", "descrizione": "ANSA — ordine d’arrivo del Gran Premio d’Austria."},
            {"url": "https://www.motogp.com/en/news/2026/09/19/electric-martin-beats-marquez-and-acosta-to-pole-as-title-fight-heats-up-in-austria/1090417", "descrizione": "MotoGP — griglia di partenza e contesto sportivo del fine settimana al Red Bull Ring."},
        ],
        "correlati": [
            {"url": "/notizie/marc-marquez-vince-aragon-secondo-mondiale-30-agosto-2026.html", "titolo": "Marc Marquez vince ad Aragon e conquista il secondo successo stagionale"},
            {"url": "/notizie/roma-inter-2-2-lautaro-doppietta-rimonta-19-settembre-2026.html", "titolo": "Roma-Inter 2-2: Lautaro firma una doppietta nella rimonta"},
            {"url": "/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html", "titolo": "Serie A, quinta giornata: calendario e orari TV"},
        ],
        "image": {
            "alt": "Illustrazione editoriale generata con IA: Pedro Acosta accanto alla KTM numero 37 nel paddock del Red Bull Ring, con le scritte e i loghi sportivi pertinenti visibili; non è una fotografia documentaria.",
            "sensitiveContext": False,
            "syntheticLikeness": "public-figure",
            "prompt": "Pedro Acosta celebrates beside the number 37 Red Bull KTM MotoGP bike at the Red Bull Ring; accurate naturally placed team logos and circuit signs; no added headline or watermark.",
        },
    },
    {
        "source_key": "meloni",
        "slug": "meloni-tetto-alunni-stranieri-divieto-veli-scuola-20-settembre-2026",
        "titolo": "Meloni annuncia un tetto agli alunni stranieri e lo stop ai veli a scuola",
        "sommario": "La premier anticipa una misura destinata al Consiglio dei ministri. Non sono ancora noti il limite per classe, il testo giuridico né i tempi di entrata in vigore.",
        "categoria": "Politica",
        "luogo": "Roma",
        "formato": "flash",
        "stato": "ANNUNCIO — TESTO NON ANCORA PUBBLICATO",
        "parole_chiave_titolo": ["tetto agli alunni stranieri", "stop ai veli"],
        "dati_chiave": [
            {"icona": "◆", "valore": "11,6%", "etichetta": "alunni senza cittadinanza italiana"},
            {"icona": "▦", "valore": "CdM", "etichetta": "prossimo passaggio annunciato"},
            {"icona": "?", "valore": "N.D.", "etichetta": "limite numerico non comunicato"},
        ],
        "paragrafi": [
            "Giorgia Meloni ha annunciato una misura per fissare un numero massimo di alunni stranieri per classe e vietare a scuola indumenti che coprano il volto. La premier ne ha parlato a Fenix, evento giovanile di Fratelli d’Italia, indicando come prossimo passaggio il Consiglio dei ministri.",
            "Meloni ha collegato il tetto alla presenza di studenti che non parlano italiano e ha aggiunto che, nei casi di maggiori difficoltà d’integrazione, sarebbe richiesto ai genitori di imparare la lingua. Ha inoltre richiamato la parità tra uomo e donna.",
            "Al momento non è stato pubblicato un testo normativo: non sono noti il limite previsto per classe, le eventuali deroghe né la formulazione esatta del divieto sui veli. L’annuncio non equivale quindi a una regola già approvata o in vigore.",
            "Secondo i dati citati da Reuters, nell’anno scolastico 2023-2024 gli alunni senza cittadinanza italiana erano circa 930 mila, l’11,6% del totale. Sarà il testo del provvedimento a chiarire destinatari, criteri applicativi e compatibilità con le norme esistenti.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/world/italy-ban-veils-schools-limit-foreign-students-per-class-meloni-says-2026-09-20/", "descrizione": "Reuters — annuncio della premier, contesto e quota degli alunni senza cittadinanza italiana."},
            {"url": "https://www.ansa.it/sito/notizie/topnews/2026/09/20/meloni-in-classe-numero-massimo-di-stranieri-e-divieto-di-burqa-norma-in-arrivo_0d622362-ec85-4807-a30b-27c63fa3aabd.html", "descrizione": "ANSA — dichiarazioni di Meloni all’evento Fenix e contenuti anticipati della misura."},
            {"url": "https://www.ansa.it/canale_legalita_scuola/", "descrizione": "ANSA Scuola — cronologia dell’annuncio e reazioni politiche nella giornata del 20 settembre."},
        ],
        "correlati": [
            {"url": "/notizie/centrodestra-supermedia-40-7-sotto-41-percento-19-settembre-2026.html", "titolo": "Centrodestra al 40,7% nella Supermedia: coalizione sotto il 41%"},
            {"url": "/notizie/schlein-lettera-meloni-14-miliardi-energia-conte-17-settembre-2026.html", "titolo": "Schlein scrive a Meloni sul caro energia"},
            {"url": "/notizie/meloni-beretta-500-anni-gardone-val-trompia-18-settembre-2026.html", "titolo": "Meloni celebra i 500 anni della Beretta"},
        ],
        "image": {
            "alt": "Illustrazione editoriale generata con IA: Giorgia Meloni parla a un podio con le scritte FENIX e Fratelli d’Italia, davanti alle bandiere italiana ed europea; non è una fotografia documentaria.",
            "sensitiveContext": False,
            "syntheticLikeness": "public-figure",
            "prompt": "Giorgia Meloni speaking at a FENIX lectern with Italian and EU flags; naturally visible FENIX and Fratelli d’Italia logos; no added headline or watermark.",
        },
    },
    {
        "source_key": "mosca",
        "slug": "mosca-attacco-record-droni-ultimo-giorno-voto-russia-20-settembre-2026",
        "titolo": "Mosca, attacco record di droni nell’ultimo giorno del voto russo",
        "sommario": "Le autorità russe attribuiscono all’Ucraina oltre mille lanci, almeno 450 diretti sulla capitale. Segnalati due morti, venti feriti e danni a una raffineria.",
        "categoria": "Mondo",
        "luogo": "Mosca",
        "formato": "flash",
        "stato": "IN SVILUPPO — DATI ATTRIBUITI ALLE AUTORITÀ RUSSE",
        "parole_chiave_titolo": ["attacco record", "droni"],
        "dati_chiave": [
            {"icona": "◆", "valore": "1.110", "etichetta": "droni intercettati secondo Mosca"},
            {"icona": "●", "valore": "450", "etichetta": "diretti sulla capitale"},
            {"icona": "!", "valore": "2", "etichetta": "morti riferiti nella regione"},
        ],
        "paragrafi": [
            "Le autorità russe hanno attribuito all’Ucraina il più grande attacco di droni mai diretto contro Mosca, avvenuto nell’ultimo giorno delle elezioni parlamentari. Il ministero della Difesa russo sostiene di aver intercettato 1.110 velivoli tra Russia, Crimea occupata e Mar Nero, almeno 450 dei quali verso la capitale.",
            "Secondo le autorità regionali, due persone sono morte e venti sono rimaste ferite nell’area di Mosca. Sono stati inoltre segnalati danni a un impianto petrolifero e a edifici residenziali; centinaia di abitanti sarebbero stati evacuati nel distretto di Ramenskoye.",
            "I numeri provengono in larga parte da fonti ufficiali russe e non sono verificabili in modo indipendente nell’immediato. Reuters e Associated Press hanno comunque descritto l’operazione come senza precedenti per scala; Kiev non aveva diffuso una ricostruzione completa nelle prime ore.",
            "L’attacco coincide con la chiusura del voto per la Duma, il primo dall’invasione su vasta scala del 2022. Il Cremlino lo ha definito un tentativo di interrompere le elezioni, mentre l’esito resta atteso tra la serata di domenica e lunedì.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/world/europe/two-dead-moscow-region-drones-hit-oil-refinery-russian-capital-2026-09-20/", "descrizione": "Reuters — vittime, danni e conteggio comunicato dalle autorità russe."},
            {"url": "https://apnews.com/article/5f7889d027c0247ca2c2c64425b9ffa9", "descrizione": "Associated Press — scala dell’attacco, feriti e contesto della guerra dei droni."},
            {"url": "https://www.reuters.com/world/europe/russian-election-cast-test-support-ukraine-war-enters-final-day-2026-09-20/", "descrizione": "Reuters — collegamento temporale con l’ultimo giorno delle elezioni parlamentari russe."},
        ],
        "correlati": [
            {"url": "/notizie/russia-elezioni-duma-voto-kamchatka-18-settembre-2026.html", "titolo": "Russia al voto per la Duma: urne aperte dalla Kamchatka"},
            {"url": "/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html", "titolo": "Usa, la Camera approva nuove sanzioni contro la Russia"},
            {"url": "/notizie/ucraina-stop-attacchi-petroliere-novorossiysk-richiesta-usa-12-agosto-2026.html", "titolo": "Ucraina, richiesta Usa di fermare gli attacchi alle petroliere"},
        ],
        "image": {
            "alt": "Illustrazione editoriale generata con IA: skyline notturno di Mosca con droni e scie della difesa aerea in lontananza, senza persone o danni visibili; non è una fotografia documentaria.",
            "sensitiveContext": True,
            "syntheticLikeness": None,
            "prompt": "Distant Moscow night skyline with small drone silhouettes and restrained air-defence trails; neutral non-graphic sensitive-context illustration; no casualties, headline or watermark.",
        },
    },
]


def main() -> None:
    for path in SOURCES.values():
        if not path.exists():
            raise SystemExit(f"immagine sorgente assente: {path}")

    published = []
    for index, article in enumerate(ARTICLES):
        words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
        if not 100 <= words <= 250:
            raise SystemExit(f"word gate {article['slug']}: {words}")
        if index:
            time.sleep(1.1)
        key = f"{article['slug']}-v{VERSION}"
        image_meta = article.pop("image")
        image = {
            "key": key,
            "aiGenerated": True,
            "documentaryPhoto": False,
            "generator": "ChatGPT/OpenAI image generation",
            "variants": variants(SOURCES[article.pop("source_key")], key),
            "alt": image_meta["alt"],
            "disclosure": CAPTION,
            "sensitiveContext": image_meta["sensitiveContext"],
            "reenactedEvent": False,
            "syntheticLikeness": image_meta["syntheticLikeness"],
            "prompt": image_meta["prompt"],
        }
        slug = write_article(article, image, VERSION)
        register_image(image, slug, VERSION)
        stamp = article["published"]
        write_json(Path("contenuti/notizie") / f"{slug}.json", {
            "slug": slug,
            "title": article["titolo"],
            "excerpt": article["sommario"],
            "category": article["categoria"],
            "published_at": stamp,
            "updated_at": stamp,
            "development_at": DATE,
            "status": article["stato"],
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        })
        published.append({"slug": slug, "words": words, "stamp": stamp})

    sync_surfaces(ARTICLES, "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "news-batch",
        "news_added": [item["slug"] for item in published],
        "news_updated": [],
        "change": "Ultime notizie: droni su Mosca, annuncio scuola di Meloni e vittoria MotoGP di Acosta",
        "image_policy_applied": "three-new-openai-contextual-editorial-images-with-relevant-logos-preserved",
    }
    write_json(Path("curiomondo-site-manifest.json"), manifest)

    state_names = ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json")
    previous_states = [json.loads((ROOT / name).read_text(encoding="utf-8")) for name in state_names]
    article_count = max(int(state.get("articleCount", 0)) for state in previous_states) + len(published)
    image_count = max(int(state.get("generatedEditorialImages", 0)) for state in previous_states) + len(published)
    for name in state_names:
        state = json.loads((ROOT / name).read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": DATE,
            "release_date": DATE,
            "last_update": "news-batch-v457",
            "articleCount": article_count,
            "generatedEditorialImages": image_count,
        })
        write_json(Path(name), state)

    write_json(Path("automation/logs/editoriale-20260920T160000-Europe-Rome.json"), {
        "run_at": published[-1]["stamp"],
        "processed": [
            {"title": a["titolo"], "decision": "publish", "source_count": len(a["fonti"]), "status": a["stato"]}
            for a in ARTICLES
        ],
    })
    print(json.dumps({"added": published}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
