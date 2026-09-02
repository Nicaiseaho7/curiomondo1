#!/usr/bin/env python3
"""Genera l'immagine editoriale IA per un articolo CurioMondo e aggiorna il registro.

Pensato per girare dentro il workflow GitHub Actions
`.github/workflows/genera-immagine-editoriale.yml`, dove la rete non è
ristretta (a differenza della sessione Claude Code che lo triggera).
Non richiede alcuna chiave API: usa un servizio di generazione immagini
gratuito e senza autenticazione (image.pollinations.ai).
"""
from __future__ import annotations
import hashlib
import io
import json
import os
import random
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = ROOT / "assets/images/editorial-auto"
REGISTRY_PATH = ROOT / "assets/data/editorial-images-v210.json"
REQUESTS_DIR = ROOT / "automation/state/image-requests"
DISCLOSURE = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
MASTER_W, MASTER_H = 1600, 1067  # 3:2, coerente con il layout esistente del sito
VARIANT_WIDTHS = (480, 800, 1200)


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def build_prompt(base_prompt: str, is_portrait: bool) -> str:
    if is_portrait:
        framing = (
            "Neutral editorial portrait, head-and-shoulders to waist-up framing, "
            "centered in a plain softly lit studio-style setting, calm neutral "
            "expression, no re-enacted event, no props referencing any incident."
        )
        return f"{base_prompt.strip()} {framing} Ultra-realistic photojournalistic quality, natural lighting, sharp focus, no text, no watermark, no logo overlay."
    return f"{base_prompt.strip()} Ultra-realistic photojournalistic editorial photography, natural cinematic lighting, sharp focus, no text, no watermark, no logo overlay."


def fetch_master_image(prompt: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(4):
        seed = random.randint(1, 10_000_000)
        url = (
            f"https://image.pollinations.ai/prompt/{quote(prompt)}"
            f"?width={MASTER_W}&height={MASTER_H}&seed={seed}&nologo=true&model=flux"
        )
        try:
            resp = requests.get(url, timeout=90)
            resp.raise_for_status()
            data = resp.content
            if len(data) < 5000:
                raise ValueError(f"immagine troppo piccola/sospetta ({len(data)} byte)")
            Image.open(io.BytesIO(data)).verify()
            return data
        except Exception as exc:  # noqa: BLE001 - vogliamo ritentare su qualunque errore di rete/decodifica
            last_error = exc
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"generazione immagine fallita dopo 4 tentativi: {last_error}")


def save_variants(master_bytes: bytes, filename_base: str) -> list[dict]:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    master = Image.open(io.BytesIO(master_bytes)).convert("RGB")
    if master.size != (MASTER_W, MASTER_H):
        master = master.resize((MASTER_W, MASTER_H), Image.LANCZOS)
    variants = []
    for w in VARIANT_WIDTHS:
        h = round(w * MASTER_H / MASTER_W)
        resized = master.resize((w, h), Image.LANCZOS)
        rel_path = f"assets/images/editorial-auto/{filename_base}-{w}.webp"
        out_path = ROOT / rel_path
        resized.save(out_path, "WEBP", quality=82, method=6)
        file_bytes = out_path.read_bytes()
        variants.append(
            {
                "w": w,
                "src": f"/{rel_path}",
                "sha256": hashlib.sha256(file_bytes).hexdigest(),
                "bytes": len(file_bytes),
            }
        )
    return variants


def update_registry(items: list[dict]) -> None:
    if not items:
        return
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry.setdefault("items", [])
    keys = {i["key"] for i in items}
    registry["items"] = [i for i in registry["items"] if i.get("key") not in keys]
    registry["items"] = items + registry["items"]
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_item(base_prompt: str, filename_base: str, article_path: str, alt_text: str, is_portrait: bool, sensitive: bool) -> dict:
    full_prompt = build_prompt(base_prompt, is_portrait)
    master_bytes = fetch_master_image(full_prompt)
    variants = save_variants(master_bytes, filename_base)
    item = {
        "key": filename_base,
        "article": article_path,
        "aiGenerated": True,
        "sensitiveContext": sensitive,
        "documentaryPhoto": False,
        "prompt": full_prompt,
        "variants": variants,
        "alt": alt_text,
        "disclosure": DISCLOSURE,
        "portraitOnly": is_portrait,
        "portraitFormat": "neutral-isolated" if is_portrait else "contextual-editorial-scene",
        "reenactedEvent": False,
    }
    if is_portrait:
        item["syntheticLikeness"] = "public-figure"
    return item


def process_single_request(req: dict) -> dict | None:
    base_prompt = (req.get("prompt") or "").strip()
    filename_base = (req.get("filename_base") or "").strip()
    article_path = (req.get("article_path") or "").strip()
    alt_text = (req.get("alt_text") or "").strip()
    is_portrait = bool(req.get("is_portrait", False))
    sensitive = bool(req.get("sensitive", False))
    if not base_prompt or not filename_base or not article_path or not alt_text:
        print(json.dumps({"status": "error", "reason": "missing_required_field", "request": req}, ensure_ascii=False))
        return None
    if is_portrait and "ritratto editoriale neutrale" not in alt_text.lower():
        print(json.dumps({"status": "error", "reason": "portrait_alt_text_missing_required_phrase", "key": filename_base}, ensure_ascii=False))
        return None
    return build_item(base_prompt, filename_base, article_path, alt_text, is_portrait, sensitive)


def main_single_from_env() -> int:
    """Modalità singola per workflow_dispatch manuale/di test (input diretti)."""
    req = {
        "prompt": env("IMAGE_PROMPT"),
        "filename_base": env("FILENAME_BASE"),
        "article_path": env("ARTICLE_PATH"),
        "alt_text": env("ALT_TEXT"),
        "is_portrait": env("IS_PORTRAIT", "false").lower() == "true",
        "sensitive": env("SENSITIVE", "false").lower() == "true",
    }
    item = process_single_request(req)
    if item is None:
        return 2
    update_registry([item])
    print(json.dumps({"status": "ok", "key": item["key"], "variants": item["variants"]}, ensure_ascii=False))
    return 0


def main_batch_from_requests_dir() -> int:
    """Modalità principale della pipeline: elabora tutte le richieste immagine
    accodate in automation/state/image-requests/*.json da un ciclo editoriale
    (scritte via git push semplice, senza bisogno dell'API GitHub/connettore)."""
    if not REQUESTS_DIR.exists():
        print(json.dumps({"status": "no_requests", "reason": "requests_dir_missing"}, ensure_ascii=False))
        return 0
    request_files = sorted(REQUESTS_DIR.glob("*.json"))
    if not request_files:
        print(json.dumps({"status": "no_requests"}, ensure_ascii=False))
        return 0

    items: list[dict] = []
    errors: list[str] = []
    for path in request_files:
        try:
            req = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.name}: json non valido ({exc})")
            continue
        item = process_single_request(req)
        if item is None:
            errors.append(f"{path.name}: richiesta non valida")
            continue
        items.append(item)
        path.unlink()

    update_registry(items)
    print(json.dumps({"status": "ok", "processed": [i["key"] for i in items], "errors": errors}, ensure_ascii=False))
    return 0 if items else 1


def main() -> int:
    if env("IMAGE_PROMPT"):
        return main_single_from_env()
    return main_batch_from_requests_dir()


if __name__ == "__main__":
    sys.exit(main())
