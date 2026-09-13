"""Verifica sul dominio pubblico gli articoli pubblicati nei cicli precedenti."""
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin

from lxml import html

from .state import Store

SITE = "https://curiomondo.it"


def _get(url: str, timeout: int = 20) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "CurioMondo-Newsroom/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return int(response.status), response.read()


def verify_record(
    record: dict[str, Any],
    fetch: Callable[[str], tuple[int, bytes]] = _get,
) -> tuple[bool, dict[str, Any], str]:
    public_url = str(record.get("public_url", ""))
    checks: dict[str, Any] = {}
    try:
        status, body = fetch(public_url)
        checks["article_http_200"] = status == 200
        doc = html.fromstring(body)
        canonical = (doc.xpath('//link[@rel="canonical"]/@href') or [""])[0]
        checks["canonical_matches_public_url"] = canonical == public_url
        hero = (doc.xpath('//main//figure[contains(@class,"article-image")][1]//img[1]/@src') or [""])[0]
        hero_url = urljoin(public_url, hero)
        hero_status, _ = fetch(hero_url) if hero else (0, b"")
        checks["hero_image_http_200"] = hero_status == 200

        surfaces = {
            "article_visible_in_expected_listing": f"{SITE}/",
            "archive_contains_article": f"{SITE}/notizie/",
            "feed_contains_article_if_eligible": f"{SITE}/feed.xml",
            "sitemap_contains_article": f"{SITE}/sitemap.xml",
            "news_sitemap_contains_article_if_eligible": f"{SITE}/news-sitemap.xml",
        }
        needle = public_url.encode("utf-8")
        relative = public_url.removeprefix(SITE).encode("utf-8")
        for name, url in surfaces.items():
            surface_status, payload = fetch(url)
            checks[name] = surface_status == 200 and (needle in payload or relative in payload)
    except Exception as exc:
        return False, checks, f"{type(exc).__name__}:{str(exc)[:160]}"

    failed = [name for name, passed in checks.items() if passed is not True]
    return not failed, checks, ",".join(failed)


def verify_pending(state_dir: Path) -> dict[str, Any]:
    store = Store(state_dir); verified: list[str] = []; pending: list[str] = []
    for record in store.pending_verification():
        slug = str(record.get("slug", ""))
        ok, checks, reason = verify_record(record)
        if ok:
            store.mark_verified(slug, checks); verified.append(slug)
        else:
            store.mark_unverified(slug, checks, reason); pending.append(slug)
    store.note_cycle("post_deploy_verify", {"verified": verified, "pending": pending})
    store.save()
    return {"status": "ok", "verified": verified, "pending": pending}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verifica post-deploy CurioMondo")
    parser.add_argument("--state", required=True)
    args = parser.parse_args(argv)
    print(json.dumps(verify_pending(Path(args.state)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
