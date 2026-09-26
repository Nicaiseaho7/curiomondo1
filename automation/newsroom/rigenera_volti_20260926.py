"""Rigenera, con gpt-image-1, le copertine del 26 settembre 2026 il cui
protagonista è una persona pubblica e l'immagine attuale non la mostra.

La chiave resta nella variabile d'ambiente. Non viene mai stampata.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from automation.newsroom.openai_client import BudgetGuard, Client, OpenAIError

OUT = ROOT / "assets" / "images" / "editorial-auto"
FEED = ROOT / "assets" / "data" / "home-feed-v210.json"
REGISTRY = ROOT / "assets" / "data" / "editorial-images-v210.json"

# Una scena ordinaria per articolo. Niente violenza, niente testo nei pixel.
JOBS = [
    (
        "leone-xiv-a-parigi-800-mila-alla-messa-poi-lourdes-26-09-2026",
        "leone-xiv-concorde-v690",
        "Ultra-realistic editorial photograph of Pope Leo XIV, recognizable, in white cassock, among a large crowd at Place de la Concorde in Paris, the obelisk behind him, daylight. No readable text, no watermark.",
        "Leone XIV tra la folla in Place de la Concorde, a Parigi. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "tajani-ai-magistrati-colpirne-uno-per-educarne-cento-26-09-2026",
        "tajani-farnesina-v691",
        "Ultra-realistic editorial photograph of Antonio Tajani, recognizable, speaking outdoors with the Italian flag and the Farnesina building in Rome behind him. No readable text, no watermark.",
        "Antonio Tajani davanti alla Farnesina, con la bandiera italiana. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "fiorello-annuncia-il-ritorno-su-rai1-con-un-video-muto-26-09-2026",
        "fiorello-rai-v692",
        "Ultra-realistic editorial photograph of Rosario Fiorello, recognizable, outside the Rai headquarters on viale Mazzini in Rome, the Rai logo correct on the building. No extra text, no watermark.",
        "Fiorello all'ingresso della sede Rai. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "pigozzi-rieletto-a-capo-della-medicina-dello-sport-mondiale-26-09-2026",
        "pigozzi-medicina-v693",
        "Ultra-realistic editorial portrait of Fabio Pigozzi, recognizable, a sports-medicine doctor beside an athletics track, neutral expression, daylight. No readable text, no watermark.",
        "Fabio Pigozzi a bordo pista. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "trump-le-fake-news-non-devono-entrare-alla-casa-bianca-26-09-2026",
        "trump-sala-stampa-v694",
        "Ultra-realistic editorial photograph of Donald Trump, recognizable, at the podium of the White House briefing room, journalists in front of him. No readable headlines, no watermark.",
        "Donald Trump al podio della sala stampa della Casa Bianca. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "leone-xiv-a-parigi-stupito-da-quanti-chiedono-il-battesimo-26-09-2026",
        "leone-xiv-notre-dame-v695",
        "Ultra-realistic editorial photograph of Pope Leo XIV, recognizable, in white cassock inside Notre-Dame in Paris, near the baptismal font, worshippers behind him. No readable text, no watermark.",
        "Leone XIV in Notre-Dame, vicino al fonte battesimale. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "leone-xiv-seconda-giornata-messa-alla-concorde-e-lourdes-26-09-2026",
        "leone-xiv-concorde-messa-v696",
        "Ultra-realistic editorial photograph of Pope Leo XIV, recognizable, celebrating outdoors at Place de la Concorde, rows of chairs and the obelisk, morning light. No readable text, no watermark.",
        "Leone XIV alla messa in Place de la Concorde. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "pezeshkian-si-agli-ispettori-nucleari-onu-dentro-un-negoziato-26-09-2026",
        "pezeshkian-ritratto-v697",
        "Ultra-realistic neutral editorial portrait of Masoud Pezeshkian, recognizable, indoors, the Iranian flag small and out of focus. No weapons, no raid, no readable text, no watermark.",
        "Ritratto di Masoud Pezeshkian. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "trump-respinge-la-tregua-di-sette-giorni-proposta-dall-iran-26-09-2026",
        "trump-tregua-v698",
        "Ultra-realistic editorial photograph of Donald Trump, recognizable, seated in a White House office, neutral, no military scene, no readable documents, no watermark.",
        "Donald Trump in un ufficio della Casa Bianca. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "mukiibi-a-terra-madre-il-diritto-al-cibo-riguarda-le-persone-26-09-2026",
        "mukiibi-terra-madre-v699",
        "Ultra-realistic editorial photograph of Edward Mukiibi, recognizable, at an outdoor food market in Turin among bread, grains and vegetables, autumn light. No readable labels, no watermark.",
        "Edward Mukiibi a un mercato alimentare di Torino. Illustrazione editoriale, non una foto documentaria.",
    ),
    (
        "worldsbk-cremona-superpole-gara1-bulega-titolo-26-settembre-2026",
        "bulega-ducati-v700",
        "Ultra-realistic editorial photograph of Nicolo Bulega, recognizable, face visible, in Ducati racing leathers in the Cremona pit lane, a red Ducati behind him. No readable numbers or sponsor text, no watermark.",
        "Nicolò Bulega ai box del circuito di Cremona, con una Ducati. Illustrazione editoriale, non una foto documentaria.",
    ),
]


def _crop(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    width, height = image.size
    target = 3 / 2
    if width / height > target:
        new_w = int(height * target)
        left = (width - new_w) // 2
        return image.crop((left, 0, left + new_w, height))
    new_h = int(width / target)
    top = (height - new_h) // 2
    return image.crop((0, top, width, top + new_h))


def _save(raw: bytes, key: str) -> None:
    image = _crop(Image.open(BytesIO(raw)))
    if image.width < 800:
        raise OpenAIError(f"immagine troppo piccola: {image.size}")
    OUT.mkdir(parents=True, exist_ok=True)
    for width in (480, 800, 1200):
        frame = image.resize((width, width * 2 // 3), Image.Resampling.LANCZOS)
        frame.save(OUT / f"{key}-{width}.webp", "WEBP", quality=86, method=6)


def _current_stem(html: str) -> str:
    match = re.search(r"/assets/images/editorial-auto/([a-z0-9-]+)-800\.webp", html)
    if not match:
        raise OpenAIError("copertina attuale non trovata")
    return match.group(1)


def _replace_everywhere(old: str, new: str, old_alt: str, new_alt: str) -> int:
    changed = 0
    skip = {".git", "node_modules", "bozze", "artifacts"}
    for path in ROOT.rglob("*"):
        if any(part in skip for part in path.parts):
            continue
        if path.suffix.lower() not in {".html", ".json", ".xml"}:
            continue
        if path.stat().st_size > 12_000_000:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated = text.replace(old, new)
        if old_alt:
            updated = updated.replace(old_alt, new_alt)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def _refresh_registry(keys: set[str]) -> None:
    if not REGISTRY.exists():
        return
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for item in registry.get("items") or []:
        hit = False
        for variant in item.get("variants") or []:
            src = variant.get("src") or ""
            if not any(key in src for key in keys):
                continue
            file_path = ROOT / src.lstrip("/")
            if not file_path.exists():
                continue
            raw = file_path.read_bytes()
            variant["bytes"] = len(raw)
            variant["sha256"] = hashlib.sha256(raw).hexdigest()
            hit = True
        if hit:
            item["prompt"] = item.get("alt") or item.get("prompt")
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    state = ROOT / "automation" / "state"
    state.mkdir(parents=True, exist_ok=True)
    client = Client(budget=BudgetGuard(state, 5.0))
    if not client.available:
        print("OPENAI_API_KEY non configurata. Nessuna copertina modificata.")
        return 1
    done: list[str] = []
    keys: set[str] = set()
    for slug, key, prompt, alt in JOBS:
        page = ROOT / "notizie" / f"{slug}.html"
        if not page.exists():
            print("manca", slug)
            continue
        html = page.read_text(encoding="utf-8")
        old = _current_stem(html)
        old_alt_match = re.search(r'property="og:image:alt" content="([^"]*)"', html)
        old_alt = old_alt_match.group(1) if old_alt_match else ""
        try:
            raw, _ = client.generate_image("gpt-image-1", prompt)
            _save(raw, key)
            _replace_everywhere(old, key, old_alt, alt)
            for width in (480, 800, 1200):
                previous = OUT / f"{old}-{width}.webp"
                if previous.exists():
                    previous.unlink()
            done.append(slug)
            keys.add(key)
            print("ok", slug)
        except Exception as exc:
            print("errore", slug, type(exc).__name__, str(exc)[:180])
    _refresh_registry(keys)
    print("fatte", len(done), "di", len(JOBS))
    return 0 if done else 1


if __name__ == "__main__":
    raise SystemExit(main())
