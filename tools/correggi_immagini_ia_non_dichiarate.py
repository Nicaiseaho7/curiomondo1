#!/usr/bin/env python3
"""Corregge la didascalia di tutte le immagini di questa sessione dichiarate
per errore come fotografie vere o materiale ufficiale, quando erano in realta
immagini generate con IA (ChatGPT) fornite dalla redazione insieme alla bozza.

Non tocca il file immagine: cambia soltanto disclosure, attributi e registro,
cosi la pagina dichiara correttamente cio che l'immagine e davvero.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION  # noqa: E402

SLUGS = [
    "vannacci-e-alemanno-chiudono-insieme-il-forum-di-orvieto-con-una-delegazione-afd-25-09-2026",
    "robert-downey-jr-torna-nel-marvel-cinematic-universe-sara-victor-von-doom-in-avengers-doom-25-09-2026",
    "gta-vi-the-album-la-colonna-sonora-ufficiale-con-34-brani-arriva-il-19-novembre-25-09-2026",
    "diesel-a-2-23-euro-al-litro-nell-ue-record-dal-2005",
    "nadia-rinaldi-da-150-a-67-chili-con-dieta-proteica-ma-il-calo-parte-dal-bypass-del-2001",
    "belluno-bancarotta-nel-turismo-la-finanza-accerta-distrazioni-per-4-milioni-25-09-2026",
    "olanda-germania-1-1-gakpo-klopp-nations-league-24-settembre-2026",
    "bjk-cup-italia-in-semifinale-cina-battuta-2-1-nel-doppio-24-09-2026",
    "senato-si-definitivo-alla-delega-sul-nucleare-sostenibile-24-09-2026",
    "scuola-il-decreto-sul-tetto-degli-studenti-stranieri-arriva-in-cdm-24-09-2026",
    "lamezia-terme-14enne-progettava-un-aggressione-a-scuola-piano-scoperto-dai-carabinieri-24-09-2026",
    "champions-league-femminile-roma-0-0-a-leuven-24-09-2026",
    "volley-italia-eliminata-dalla-finlandia-agli-europei-24-09-2026",
    "eni-tetto-ai-prezzi-di-gasolio-e-benzina-dal-28-settembre-25-09-2026",
    "scontro-con-una-bici-rider-in-scooter-muore-a-palermo-25-09-2026",
    "roncola-contro-la-moglie-condannato-a-16-anni-la-vittima-resta-tetraplegica-25-09-2026",
]

GENERATOR = "immagine IA (ChatGPT) fornita alla redazione insieme alla bozza"


def fix_html(slug: str) -> bool:
    path = ROOT / "notizie" / f"{slug}.html"
    raw = path.read_text(encoding="utf-8")
    changed = False

    for old, new in (
        (
            'Fotografia editoriale fornita alla redazione CurioMondo; '
            'non generata da intelligenza artificiale.',
            CAPTION,
        ),
        (
            'Immagine promozionale ufficiale fornita dagli aventi diritto; '
            'non generata da CurioMondo ne una fotografia di cronaca.',
            CAPTION,
        ),
    ):
        if old in raw:
            raw = raw.replace(old, new)
            changed = True

    for old, new in (
        ('data-ai-generated="false" data-documentary-photo="true"', 'data-ai-generated="true"'),
        ('data-ai-generated="false" data-official-artwork="true"', 'data-ai-generated="true"'),
        ('data-documentary-photo="true" data-ai-generated="false"', 'data-ai-generated="true"'),
    ):
        if old in raw:
            raw = raw.replace(old, new)
            changed = True

    if changed:
        path.write_text(raw, encoding="utf-8")
    return changed


def fix_registry() -> int:
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    fixed = 0
    wanted = {f"/notizie/{s}.html" for s in SLUGS}
    for item in registry["items"]:
        if item.get("article") in wanted:
            item["disclosure"] = CAPTION
            item["generator"] = GENERATOR
            item["aiGenerated"] = True
            item["documentaryPhoto"] = False
            item["officialArtwork"] = False
            item.pop("prompt", None)
            fixed += 1
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return fixed


def main() -> int:
    html_fixed = sum(1 for s in SLUGS if fix_html(s))
    registry_fixed = fix_registry()
    print(json.dumps({"html_fixed": html_fixed, "registry_fixed": registry_fixed,
                      "total_slugs": len(SLUGS)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
