"""Dalle bozze verificate a un unico rilascio statico pronto per il push."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

from .openai_client import BudgetGuard, Client, OpenAIError
from .site import CAPTION, ROOT, _version, register_image, sync_surfaces, write_article
from .state import DRAFTED, FAILED, PUBLISHED, QUEUED, Store


def _config() -> dict[str, Any]:
    return json.loads((ROOT / "automation/config.json").read_text(encoding="utf-8"))


def _image_prompt(article: dict[str, Any]) -> str:
    contract_path = ROOT / "automation/prompts/image-generation-contract.txt"
    policy_path = ROOT / "AI-EDITORIAL-IMAGE-PROTOCOL.md"
    if not contract_path.exists() or not policy_path.exists():
        raise RuntimeError("contratto o protocollo immagini mancante")
    contract = contract_path.read_text(encoding="utf-8")
    policy = policy_path.read_text(encoding="utf-8")
    image = article.get("immagine") or {}
    sensitive = bool(image.get("contesto_sensibile") or article.get("verifica", {}).get("sensibile"))
    public = bool(image.get("personaggio_pubblico"))
    safety = ""
    if sensitive and public:
        safety = "SENSITIVE public figure: neutral isolated portrait only; no traumatic scene."
    elif sensitive:
        safety = "Sensitive event: no injuries, bodies, blood, suffering or fabricated traumatic moment."
    return (
        contract + "\n\nCanonical policy loaded in full:\n" + policy +
        "\n\nCREATE ONE IMAGE NOW. Article title: " + str(article.get("titolo", "")) +
        "\nArticle summary: " + str(article.get("sommario", "")) +
        "\nSpecific visual brief: " + str(image.get("prompt", "")) +
        "\n" + safety +
        "\nREAL PEOPLE AND REAL LOGOS: if the article names a public figure, team or brand, depict that real recognizable subject with official kit, crest and sponsors. Invented faces, generic extras and fantasy uniforms are forbidden."
        "\nNo headline, caption, statistics, watermark, signature or added editorial text inside the pixels."
    )


def _validate_image(raw: bytes) -> Image.Image:
    try:
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        image.load()
    except Exception as exc:
        raise OpenAIError("immagine OpenAI non decodificabile") from exc
    if image.width < 1000 or image.height < 650:
        raise OpenAIError(f"immagine troppo piccola: {image.width}x{image.height}")
    stat = ImageStat.Stat(image.resize((96, 64)))
    if sum(stat.stddev) / len(stat.stddev) < 8:
        raise OpenAIError("immagine quasi uniforme: rigenerazione necessaria")
    return image


def _validate_visual_report(report: dict[str, Any]) -> None:
    required_true = ("approvata", "fotorealistica", "coerente", "soggetto_reale")
    forbidden_true = ("testo_nei_pixel", "contenuto_sensibile_non_consentito", "persone_inventate")
    if not all(report.get(key) is True for key in required_true):
        raise OpenAIError(f"immagine bocciata dal controllo visivo: {report.get('motivo', '')[:120]}")
    if any(report.get(key) is True for key in forbidden_true):
        raise OpenAIError(f"immagine non conforme: {report.get('motivo', '')[:120]}")


def _save_variants(image: Image.Image, key: str) -> list[dict[str, Any]]:
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio); left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio); top = max(0, (image.height - height) // 2)
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets/images/editorial-auto"; out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=88, method=6
        )
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}",
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def prepare_release(state_dir: Path, massimo: int = 3) -> dict[str, Any]:
    if os.getenv("CURIOMONDO_AUTO_PUBLISH", "").lower() != "true":
        return {"status": "blocked", "reason": "CURIOMONDO_AUTO_PUBLISH non attivo"}
    cfg = _config().get("newsroom", {})
    budget = BudgetGuard(state_dir, float(cfg.get("tetto_giornaliero_usd", 5.0)))
    client = Client(budget=budget)
    if not client.available:
        return {"status": "blocked", "reason": "OPENAI_API_KEY non configurata"}
    store = Store(state_dir)
    drafts = sorted(store.by_status(DRAFTED), key=lambda c: (c.priority == "breaking", c.score), reverse=True)[:massimo]
    if not drafts:
        return {"status": "ok", "articoli": 0, "reason": "nessuna bozza pronta"}

    version = _version(); built: list[dict[str, Any]] = []
    for candidate in drafts:
        article = candidate.article
        try:
            raw, _ = client.generate_image(
                str(cfg.get("modello_immagine", "gpt-image-1")), _image_prompt(article)
            )
            report, _ = client.inspect_image(
                str(cfg.get("modello_verifica_immagine", "gpt-4o")),
                raw,
                str(article.get("immagine", {}).get("prompt", "")),
            )
            _validate_visual_report(report)
            image = _validate_image(raw)
            key = f"{article['slug']}-ai-openai-v{version}"
            variants = _save_variants(image, key)
            meta = {
                "key": key, "aiGenerated": True, "documentaryPhoto": False,
                "variants": variants, "alt": article["immagine"]["alt"], "disclosure": CAPTION,
                "sensitiveContext": bool(article["immagine"].get("contesto_sensibile") or article.get("verifica", {}).get("sensibile")),
            }
            if article["immagine"].get("personaggio_pubblico"):
                meta["syntheticLikeness"] = "public-figure"
            slug = write_article(article, meta, version)
            register_image(meta, slug, version)
            store.update(candidate.url_key, status=QUEUED, article=article)
            built.append(article)
        except Exception as exc:
            attempts = candidate.attempts + 1
            store.update(candidate.url_key, attempts=attempts,
                         status=FAILED if attempts >= 3 else DRAFTED,
                         reason=f"immagine_o_render:{type(exc).__name__}:{str(exc)[:120]}")

    if not built:
        store.save()
        return {"status": "blocked", "reason": "nessun articolo ha superato immagine e rendering"}
    best = max(
        (c for c in drafts if c.article in built),
        key=lambda c: (c.priority == "breaking", c.score),
    )
    featured_url = f"/notizie/{best.article['slug']}.html"
    sync_surfaces(built, featured_url, version)
    store.note_cycle("publish_prepare", {"version": version, "articles": [a["slug"] for a in built]})
    store.save()
    return {"status": "ok", "articoli": len(built), "version": version,
            "slugs": [a["slug"] for a in built], "costo_usd": round(client.usage.cost_usd, 4)}


def confirm_release(state_dir: Path, commit_sha: str) -> dict[str, Any]:
    store = Store(state_dir); confirmed = []
    for candidate in store.by_status(QUEUED):
        slug = candidate.article.get("slug")
        if not slug:
            continue
        store.mark_published(candidate.url_key, slug, f"https://curiomondo.it/notizie/{slug}.html",
                             commit_sha=commit_sha)
        confirmed.append(slug)
    store.note_cycle("publish_confirm", {"commit": commit_sha, "articles": confirmed})
    store.save()
    return {"status": "ok", "confirmed": confirmed, "commit": commit_sha}


def rollback_release(state_dir: Path) -> dict[str, Any]:
    """Rimette in bozza il lotto se gate o push falliscono."""
    store = Store(state_dir); restored = []
    for candidate in store.by_status(QUEUED):
        store.update(candidate.url_key, status=DRAFTED, reason="pubblicazione_da_ritentare")
        restored.append(candidate.article.get("slug", candidate.url_key))
    store.note_cycle("publish_rollback", {"articles": restored})
    store.save()
    return {"status": "ok", "restored": restored}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pubblicatore automatico CurioMondo")
    parser.add_argument("--state", required=True)
    parser.add_argument("--max", type=int, default=3)
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--commit", default="")
    args = parser.parse_args(argv)
    if args.confirm and args.rollback:
        parser.error("--confirm e --rollback sono mutuamente esclusivi")
    if args.confirm:
        result = confirm_release(Path(args.state), args.commit)
    elif args.rollback:
        result = rollback_release(Path(args.state))
    else:
        result = prepare_release(Path(args.state), args.max)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
