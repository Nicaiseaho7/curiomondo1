#!/usr/bin/env python3
"""Supermedia YouTrend/Agi: centrodestra al 40,7%."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 445
STAMP = "2026-09-19T14:38:00+02:00"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        w = round(image.height * ratio)
        left = (image.width - w) // 2
        image = image.crop((left, 0, left + w, image.height))
    else:
        h = round(image.width / ratio)
        top = (image.height - h) // 2
        image = image.crop((0, top, image.width, top + h))
    out = ROOT / "assets/images/editorial-auto"
    out.mkdir(parents=True, exist_ok=True)
    result = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=86, method=6
        )
        result.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return result


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


def persist(article: dict, image: dict, published: str) -> str:
    slug = write_article(article, image, VERSION)
    stamp_dates(slug, published)
    article["published"] = published
    register_image(image, slug, VERSION)
    write_json(
        ROOT / "contenuti/notizie" / f"{slug}.json",
        {
            "slug": slug,
            "title": article["titolo"],
            "excerpt": article["sommario"],
            "category": article["categoria"],
            "published_at": published,
            "updated_at": published,
            "development_at": "2026-09-19",
            "status": article["stato"],
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


def assert_body(article: dict) -> None:
    paras = article["paragrafi"]
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in paras)
    lo, hi = {"flash": (100, 250), "standard": (300, 600), "feature": (800, 1500)}[article["formato"]]
    if not lo <= words <= hi:
        raise SystemExit(f"{article['slug']} {article['formato']} {words} parole")
    for i, p in enumerate(paras, 1):
        n = len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p))
        if n > 60:
            raise SystemExit(f"{article['slug']} p{i} {n} parole")
    print(f"{article['slug']}: {words} parole")


ARTICLE = {
    "slug": "centrodestra-supermedia-40-7-sotto-41-percento-19-settembre-2026",
    "titolo": "Centrodestra al 40,7% nella Supermedia: prima volta sotto il 41%",
    "sommario": "La media ponderata YouTrend/Agi, aggiornata al 17 settembre, stima FdI, FI, Lega e Noi Moderati al 40,7%. Futuro Nazionale è quarto partito, davanti a Forza Italia.",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "stato": "CONFERMATA DA PIÙ FONTI",
    "parole_chiave_titolo": ["Centrodestra", "Supermedia"],
    "dati_chiave": [
        {"icona": "◆", "valore": "40,7%", "etichetta": "stima FdI, FI, Lega e Noi Moderati"},
        {"icona": "●", "valore": "26,6%", "etichetta": "Fratelli d’Italia, ancora primo partito"},
        {"icona": "↗", "valore": "7,7%", "etichetta": "Futuro Nazionale, quarto davanti a FI"},
    ],
    "paragrafi": [
        "Secondo la Supermedia YouTrend/Agi, i quattro partiti di governo sono stimati al 40,7 per cento. Fratelli d’Italia, Forza Italia, Lega e Noi Moderati scendono, per la prima volta in questa legislatura, sotto il 41 per cento. La media è ponderata il 17 settembre su sondaggi realizzati dal 2 al 16 settembre.",
        "Fratelli d’Italia resta primo, al 26,6 per cento, tre decimali in meno rispetto al 10 settembre. Il Partito Democratico è secondo, al 21,1. Il Movimento 5 Stelle sale al 12,5, con un progresso di quattro decimali, il più ampio tra le forze principali.",
        "Futuro Nazionale, la lista di Roberto Vannacci, è stimato al 7,7 e diventa il quarto partito, tre decimali sopra Forza Italia, ferma al 7,4. La Lega resta al 5,6. Noi Moderati è all’1,1. I decimali descrivono intenzioni di voto, non un risultato elettorale.",
        "Le somme di coalizione sono aggregazioni, non uno schema di liste già depositato. FdI, FI, Lega e Noi Moderati totalizzano il 40,7. Se a quella somma si aggiungesse Futuro Nazionale, il totale indicato nella rilevazione salirebbe al 48,4. Nessuna delle due ipotesi coincide con un voto già tenuto.",
        "Sul versante opposto, PD, Movimento 5 Stelle e Alleanza Verdi e Sinistra sommano il 40 per cento. Con Italia Viva e +Europa la somma sale al 43,8. Anche qui si tratta di una somma di intenzioni, non di una coalizione unica presentata agli elettori.",
        "Il testo elettorale approvato dal Senato prevede un premio di 70 deputati e 35 senatori alla coalizione che raggiunge almeno il 42 per cento in entrambe le Camere. Se la soglia manca, i seggi restano proporzionali. Il provvedimento non è ancora legge: deve tornare identico alla Camera.",
        "Azione è stimata al 3,3, in calo di quattro decimali. Italia Viva è al 2,3 e +Europa all’1,5. Il Partito Liberaldemocratico entra nella serie all’1,4. Queste forze restano fuori dalle due somme di coalizione usate sopra.",
        "I sondaggi della ponderazione provengono da Emg, Ixè, Noto, Only Numbers, Piepoli, Swg, Tecnè e YouTrend. Le schede metodologiche sono nel registro ufficiale. La differenza tra 40,7 e 42 resta, per ora, un confronto tra stime e una riforma ancora in esame.",
    ],
    "fonti": [
        {
            "url": "https://www.ilmessaggero.it/politica/sondaggi_politici_meloni_pd_conte_vannacci_numeri_proiezioni-9773136.html",
            "descrizione": "Il Messaggero, 19 settembre — Supermedia YouTrend/Agi, liste e somme di coalizione.",
        },
        {
            "url": "https://quifinanza.it/politica/sondaggi-politici-19-settembre-2026/1016072/",
            "descrizione": "QuiFinanza/ANSA — stessi percentuali, istituti della ponderazione e nota metodologica.",
        },
        {
            "url": "https://www.repubblica.it/politica/2026/09/19/news/sondaggi_centrodestra_legge_elettorale_melonellum_vittoria_centrosinistra-425594830/",
            "descrizione": "la Repubblica, 19 settembre — prima volta sotto il 41% in legislatura e premio al 42%.",
        },
        {
            "url": "https://www.quotidiano.net/politica/sondaggi-politici-oggi-centrodestra-f54xfdjo",
            "descrizione": "Quotidiano Nazionale, 17 settembre — liste complete e variazione rispetto al 10 settembre.",
        },
        {
            "url": "https://www.youtrend.it/2026/09/10/supermedia-youtrend-agi-fdi-al-269-cala-il-m5s/",
            "descrizione": "YouTrend — Supermedia precedente del 10 settembre, base di confronto.",
        },
        {
            "url": "https://www.sondaggipoliticoelettorali.it/",
            "descrizione": "Registro ufficiale dei sondaggi politico-elettorali.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/riforma-legge-elettorale-42-percento-camera-19-settembre-2026.html",
            "titolo": "Legge elettorale: premio al 42%, il testo torna alla Camera",
        },
        {
            "url": "/notizie/governo-meloni-record-longevita-repubblica-4-settembre-2026.html",
            "titolo": "Governo Meloni, record di longevità della Repubblica",
        },
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, il testo ufficiale dell’esenzione 2027",
        },
    ],
}

PROMPT = (
    "Photorealistic professional news photograph of Giorgia Meloni in a dark jacket, "
    "shallow depth of field, softly blurred Italian institutional interior, no text, no watermark."
)
ALT = (
    "Scena editoriale contestuale generata con IA: Giorgia Meloni in abito scuro "
    "in un interno istituzionale italiano; somiglianza sintetica, non una fotografia documentaria."
)


def main() -> None:
    assert_body(ARTICLE)
    source = ROOT / "generated_images/meloni-supermedia-v445.jpg"
    if not source.exists():
        raise SystemExit(f"immagine assente: {source}")
    key = f"{ARTICLE['slug']}-v{VERSION}"
    image = {
        "key": key,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": variants(source, key),
        "alt": ALT,
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": PROMPT,
    }
    slug = persist(ARTICLE, image, STAMP)
    sync_surfaces([ARTICLE], "", VERSION)
    mp = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-19",
        "type": "content-release",
        "news_added": [slug],
        "news_updated": [],
        "change": "Supermedia: centrodestra al 40,7%",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(mp, manifest)
    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        p = ROOT / name
        if p.exists():
            s = json.loads(p.read_text(encoding="utf-8"))
            s.update(
                {
                    "currentVersion": VERSION,
                    "site_version": VERSION,
                    "version": str(VERSION),
                    "date": "2026-09-19",
                    "release_date": "2026-09-19",
                    "articleCount": int(s.get("articleCount", 0)) + 1,
                    "generatedEditorialImages": int(s.get("generatedEditorialImages", 0)) + 1,
                    "last_update": "news-v445",
                }
            )
            write_json(p, s)
    write_json(
        ROOT / "automation/logs/editoriale-20260919T143800-Europe-Rome.json",
        {
            "run_at": STAMP,
            "skill": "editoriale-fonti-primarie",
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{slug}.html",
                }
            ],
        },
    )
    print("OK", slug)


if __name__ == "__main__":
    main()
