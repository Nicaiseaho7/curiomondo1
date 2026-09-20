#!/usr/bin/env python3
"""Pubblica il flash sull'ex badante arrestata a Veroli il 20 settembre 2026."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article


VERSION = 456
DATE = "2026-09-20"
STAMP = "2026-09-20T11:48:00+02:00"
SOURCE_IMAGE = Path(
    "/workspace/scratch/63d8c74bad9c/generated_images/"
    "exec-72db4e9f-5bfa-410a-a435-4a91fd10e51c.png"
)


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
    result: list[dict[str, object]] = []
    for width in (480, 800, 1200):
        target = folder / f"{key}-{width}.webp"
        resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
        resized.save(target, "WEBP", quality=86, method=6)
        result.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{target.name}",
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "bytes": target.stat().st_size,
            }
        )
    return result


ARTICLE = {
    "slug": "veroli-badante-arrestata-maltrattamenti-donna-disabile-20-settembre-2026",
    "titolo": "Veroli, arrestata l’ex badante condannata per maltrattamenti a una donna disabile",
    "sommario": (
        "La pena definitiva è di tre anni, con cinque anni di interdizione dai pubblici "
        "uffici. Le telecamere contribuirono a documentare le condotte risalenti al 2021."
    ),
    "categoria": "Cronaca",
    "luogo": "Veroli",
    "formato": "flash",
    "stato": "CONFERMATA",
    "parole_chiave_titolo": ["arrestata l’ex badante", "donna disabile"],
    "dati_chiave": [
        {"icona": "◆", "valore": "3 anni", "etichetta": "pena detentiva definitiva"},
        {"icona": "●", "valore": "5 anni", "etichetta": "interdizione dai pubblici uffici"},
        {"icona": "▦", "valore": "2021", "etichetta": "anno a cui risalgono i fatti"},
    ],
    "paragrafi": [
        (
            "I carabinieri della Stazione di Veroli, in provincia di Frosinone, hanno "
            "arrestato una ex badante condannata in via definitiva per maltrattamenti "
            "contro una donna con sindrome di Down. La donna è stata trasferita nel "
            "carcere romano di Rebibbia per scontare tre anni di reclusione."
        ),
        (
            "L’ordine di carcerazione è stato emesso dalla Procura della Repubblica presso "
            "il Tribunale di Frosinone. Alla pena detentiva si aggiunge l’interdizione dai "
            "pubblici uffici per cinque anni: il provvedimento esegue una condanna definitiva "
            "e non costituisce una misura cautelare."
        ),
        (
            "I fatti risalgono al 2021, quando la donna lavorava come domestica e assistente "
            "nell’abitazione della famiglia della vittima. Le indagini partirono dalla "
            "denuncia, raccolsero testimonianze e utilizzarono riprese video per documentare "
            "percosse e condotte vessatorie."
        ),
        (
            "Le prove hanno retto nei successivi gradi di giudizio fino alla decisione "
            "divenuta definitiva. Le fonti consultate non rendono noti i nomi delle persone "
            "coinvolte, la data della sentenza né ulteriori dettagli sulle registrazioni, "
            "tutelando così l’identità della vittima."
        ),
    ],
    "fonti": [
        {
            "url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/20/percosse-a-una-donna-disabile-arrestata-la-badante-dopo-la-condanna_9fbd2024-b207-4267-a72a-309da69887f0.html",
            "descrizione": (
                "ANSA — ordine di carcerazione, durata della pena, interdizione e trasferimento "
                "a Rebibbia."
            ),
        },
        {
            "url": "https://laziotv.it/veroli/violenze-su-una-donna-disabile-ex-badante-arrestata-e-portata-in-carcere/",
            "descrizione": (
                "Lazio TV — esecuzione del provvedimento dei Carabinieri di Veroli e fatti "
                "risalenti al 2021."
            ),
        },
        {
            "url": "https://www.frosinonenews.eu/maltrattamenti-e-violenza-su-una-donna-con-sindrome-di-down-ex-badante-in-carcere/",
            "descrizione": (
                "Frosinone News — pena definitiva, ruolo assistenziale della condannata e "
                "trasferimento in carcere."
            ),
        },
    ],
    "correlati": [
        {
            "url": "/notizie/milano-lite-strada-25enne-accoltellato-gola-20-settembre-2026.html",
            "titolo": "Milano, 25enne accoltellato alla gola dopo una lite in strada",
        },
        {
            "url": "/notizie/violenza-prima-dei-16-anni-l-istat-stima-3-milioni-di-donne-italiane-coinvolte-16-09-2026.html",
            "titolo": "Violenza prima dei 16 anni: l’Istat stima 3 milioni di donne coinvolte",
        },
        {
            "url": "/notizie/pedopornografia-online-17-arresti-rete-mille-utenti-17-settembre-2026.html",
            "titolo": "Pedopornografia online, 17 arresti: rete da oltre mille utenti",
        },
    ],
}


def main() -> None:
    words = sum(
        len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", paragraph))
        for paragraph in ARTICLE["paragrafi"]
    )
    if not 100 <= words <= 250:
        raise SystemExit(f"word gate: {words}")
    if not SOURCE_IMAGE.exists():
        raise SystemExit(f"immagine sorgente assente: {SOURCE_IMAGE}")

    key = f"{ARTICLE['slug']}-v{VERSION}"
    image = {
        "key": key,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": variants(SOURCE_IMAGE, key),
        "alt": (
            "Scena editoriale neutrale generata con IA: auto dei Carabinieri con scritte "
            "CARABINIERI e 112 davanti all’ingresso di un istituto penitenziario, senza "
            "persone arrestate o vittime visibili; non è una fotografia documentaria."
        ),
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "syntheticLikeness": None,
        "prompt": (
            "Neutral sensitive-context editorial scene outside an Italian prison entrance "
            "with a Carabinieri patrol car and authentic CARABINIERI and 112 markings; no "
            "victim, detained person, violence, handcuffs, headline, added label or watermark."
        ),
    }

    slug = write_article(ARTICLE, image, VERSION)
    ARTICLE["published"] = STAMP
    register_image(image, slug, VERSION)
    write_json(
        Path("contenuti/notizie") / f"{slug}.json",
        {
            "slug": slug,
            "title": ARTICLE["titolo"],
            "excerpt": ARTICLE["sommario"],
            "category": ARTICLE["categoria"],
            "published_at": STAMP,
            "updated_at": STAMP,
            "development_at": DATE,
            "status": ARTICLE["stato"],
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": ARTICLE["paragrafi"],
            "sources": ARTICLE["fonti"],
            "image": image,
        },
    )
    sync_surfaces([ARTICLE], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update(
        {"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"}
    )
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "breaking-news",
        "news_added": [slug],
        "news_updated": [],
        "change": "Flash sull’ex badante arrestata a Veroli dopo la condanna definitiva",
        "image_policy_applied": "new-openai-sensitive-context-neutral-editorial-image",
    }
    write_json(Path("curiomondo-site-manifest.json"), manifest)

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": DATE,
                "release_date": DATE,
                "last_update": "breaking-news-v456",
                "articleCount": int(state.get("articleCount", 0)) + 1,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
            }
        )
        write_json(Path(name), state)

    write_json(
        Path("automation/logs/editoriale-20260920T114800-Europe-Rome.json"),
        {
            "run_at": STAMP,
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "decision": "publish",
                    "source_count": 3,
                    "independent_confirmations": 0,
                    "origin": "Carabinieri di Veroli, ordine della Procura di Frosinone",
                    "note": "Le fonti secondarie riportano lo stesso sviluppo di origine istituzionale.",
                }
            ],
        },
    )
    print(json.dumps({"added": [slug], "words": words}, ensure_ascii=False))


if __name__ == "__main__":
    main()
