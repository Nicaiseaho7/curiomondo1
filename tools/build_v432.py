#!/usr/bin/env python3
"""Pubblica incontro Tajani-Bolat Farnesina (v432)."""
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

VERSION = 432
PUBLISHED = "2026-09-18T18:55:00+02:00"
SLUG = "tajani-bolat-turchia-farnesina-hormuz-commercio-18-settembre-2026"


def save_image_variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
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
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=86, method=6
        )
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return variants


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


ARTICLE = {
    "slug": SLUG,
    "titolo": "Tajani vede Bolat alla Farnesina: Hormuz e Mar Rosso sul tavolo commerciale",
    "sommario": "Il ministro degli Esteri ha ricevuto il ministro del Commercio turco. Interscambio 2025: 26,1 miliardi. Poi incontro con imprese italiane.",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Tajani", "Turchia"],
    "dati_chiave": [
        {"icona": "◆", "valore": "26,1 mld", "etichetta": "interscambio Italia-Turchia nel 2025"},
        {"icona": "●", "valore": "13,7 mld", "etichetta": "export italiano verso la Turchia"},
        {"icona": "↗", "valore": "2°", "etichetta": "partner europeo della Turchia, dopo la Germania"},
    ],
    "paragrafi": [
        "Antonio Tajani ha ricevuto oggi, venerdì 18 settembre, alla Farnesina il ministro del Commercio turco Ömer Bolat. Lo comunica il ministero degli Esteri. Sul tavolo i rapporti economici bilaterali e le conseguenze della crisi nel Mar Rosso e nello Stretto di Hormuz sul commercio internazionale.",
        "Al termine del colloquio i due ministri hanno incontrato imprese italiane con interessi in Turchia. I settori indicati dalla Farnesina sono infrastrutture e trasporti, difesa e aerospazio, energia, telecomunicazioni e siderurgia. Non è stato firmato un accordo nuovo.",
        "La Turchia è tra i Paesi prioritari del Piano d’azione per l’export. Nel 2025 l’interscambio è stato pari a 26,1 miliardi di euro: 13,7 miliardi di esportazioni italiane e 12,4 miliardi di importazioni. L’export, scrive la Farnesina, è cresciuto dell’11,3% a giugno e del 6,6% a luglio.",
        "Il Sole 24 Ore, sulla stessa nota, precisa il posizionamento: l’Italia è settimo fornitore e quarto cliente della Turchia. Con una quota export del 3,8% è il secondo partner europeo, dietro la Germania (7,2%) e davanti a Francia e Spagna.",
        "I due ministri hanno parlato anche di accesso ai mercati e delle relazioni economiche tra Turchia e Unione europea, in vista della prossima Commissione congiunta su economia e commercio, da tenersi in Turchia. La Farnesina non indica data né sede precisa.",
        "Il comunicato italiano non riporta citazioni dirette di Tajani. Fonti turche danno conto di un obiettivo di 40 miliardi di dollari di interscambio, fissato da Erdogan e Meloni: è un obiettivo politico, distinto dai 26,1 miliardi di euro del 2025.",
        "Il nesso con Hormuz e il Mar Rosso è dichiarato, non dettagliato: niente numeri su navi deviate, premi assicurativi o tempi di rotta. Resta il fatto che Roma ha messo le due crisi di navigazione al centro di un incontro commerciale, non solo militare.",
        "Conferma indipendente: Il Sole 24 Ore (nota Farnesina) e il resoconto turco della visita di Bolat a Roma. 18 settembre 2026, ore 18.55 Europe/Rome.",
    ],
    "fonti": [
        {
            "url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/09/tajani-incontra-il-ministro-del-commercio-turco-omer-bolat/",
            "descrizione": "MAECI — comunicato sull’incontro Tajani-Bolat del 18 settembre 2026.",
        },
        {
            "url": "https://www.ilsole24ore.com/art/tajani-vede-ministro-commercio-turco-bolat-italia-secondo-partner-europeo-dietro-germania-AJOdXKHB",
            "descrizione": "Il Sole 24 Ore — conferma della nota e ranking commerciale Italia-Turchia.",
        },
        {
            "url": "https://www.esteri.it/en/sala_stampa/archivionotizie/comunicati/",
            "descrizione": "MAECI in inglese — Tajani meets Turkish Trade Minister Ömer Bolat.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/hormuz-pasdaran-petroliera-trend-togo-17-settembre-2026.html",
            "titolo": "Hormuz, i Pasdaran colpiscono la petroliera Trend",
        },
        {
            "url": "/notizie/meloni-oslo-norvegia-gas-fen-saipem-17-settembre-2026.html",
            "titolo": "Meloni a Oslo: gas, FEN e Saipem",
        },
        {
            "url": "/notizie/tajani-missione-argentina-brasile-oltre-100-imprese-8-settembre-2026.html",
            "titolo": "Tajani in Argentina e Brasile con le imprese",
        },
    ],
}


def main() -> None:
    image = {
        "key": f"{SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(
            ROOT / "generated_images" / "tajani-bolat-v432.jpg", f"{SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Antonio Tajani riconoscibile, occhiali e capelli grigi, in un salone diplomatico con bandiere italiane; somiglianza sintetica, non è una fotografia documentaria dell’incontro.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Antonio Tajani with glasses, Farnesina diplomatic salon, Italian flags, no text.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    stamp_dates(slug, PUBLISHED)
    ARTICLE["published"] = PUBLISHED
    html = (ROOT / "notizie" / f"{slug}.html").read_text(encoding="utf-8")
    html = html.replace(
        '<figure class="article-image" data-ai-generated="true">',
        '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false">',
    )
    (ROOT / "notizie" / f"{slug}.html").write_text(html, encoding="utf-8")
    register_image(image, slug, VERSION)
    write_json(
        ROOT / "contenuti" / "notizie" / f"{slug}.json",
        {
            "slug": slug,
            "title": ARTICLE["titolo"],
            "excerpt": ARTICLE["sommario"],
            "category": ARTICLE["categoria"],
            "published_at": PUBLISHED,
            "updated_at": PUBLISHED,
            "development_at": "2026-09-18",
            "status": "UFFICIALE",
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
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Pubblicato l’incontro Tajani-Bolat alla Farnesina",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": "2026-09-18",
                "release_date": "2026-09-18",
                "articleCount": int(state.get("articleCount", 0)) + 1,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
                "last_update": "tajani-bolat-v432",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T185500-Europe-Rome.json",
        {
            "run_at": PUBLISHED,
            "skill": "ultime-notizie-scoop",
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "primary_source": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/09/tajani-incontra-il-ministro-del-commercio-turco-omer-bolat/",
                    "public_url": f"https://curiomondo.it/notizie/{SLUG}.html",
                }
            ],
            "discarded": [
                {"topic": "ESA ESTEC Open Day", "reason": "invito media per il 27 settembre, non notizia del giorno"},
                {"topic": "allerta gialla Protezione civile", "reason": "criticità ordinaria, già coperta il 17; niente escalation ad arancione"},
                {"topic": "FTSE MIB -1,6%", "reason": "chiusura di seduta ordinaria, impatto sotto soglia senza fatto nuovo istituzionale"},
                {"topic": "fentanyl d.m. Salute", "reason": "comunicato del 10 settembre, fuori finestra"},
                {"topic": "Pakistan attentato Kohat", "reason": "cronaca estera senza fonte primaria italiana letta per intero"},
                {"topic": "NBA partite", "reason": "nessuna gara questo weekend"},
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
