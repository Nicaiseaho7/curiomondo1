#!/usr/bin/env python3
"""Integra la voce Scioperi nel menu CurioMondo e registra i nuovi URL.

Il pacchetto va prima estratto nella radice della repository. Lo script non
rinomina, elimina o sposta URL esistenti ed è idempotente.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MENU_LINK = (
    '\n<a class="mx-entry" href="/scioperi/">'
    '<em>03</em><strong>Scioperi</strong>'
    '<small>Calendario verificato per regione</small></a>'
)

SITEMAP_BLOCK = """\
  <url>
    <loc>https://curiomondo.it/scioperi/</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.90</priority>
  </url>
  <url>
    <loc>https://curiomondo.it/scioperi/archivio/</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.65</priority>
  </url>
"""

REQUIRED = (
    "scioperi/index.html",
    "scioperi/archivio/index.html",
    "assets/css/scioperi-v1.css",
    "assets/js/scioperi-v1.js",
    "assets/data/scioperi.json",
)


def insert_menu_link(text: str) -> tuple[str, bool]:
    if 'href="/scioperi/"' in text:
        return text, False
    pattern = re.compile(r'(<nav\b[^>]*class="[^"]*\bmx-index\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S)
    match = pattern.search(text)
    if not match:
        return text, False
    updated = text[: match.start(3)] + MENU_LINK + "\n" + text[match.start(3) :]
    return updated, True


def patch_sitemap(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        print("AVVISO: sitemap.xml non presente; nessuna modifica allo sitemap.")
        return False
    text = path.read_text(encoding="utf-8")
    if "https://curiomondo.it/scioperi/" in text:
        return False
    marker = "</urlset>"
    if marker not in text:
        raise RuntimeError("sitemap.xml non contiene </urlset>; modifica interrotta")
    updated = text.replace(marker, SITEMAP_BLOCK + marker, 1)
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Radice della repository CurioMondo")
    parser.add_argument("--dry-run", action="store_true", help="Mostra le modifiche senza scriverle")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    missing = [relative for relative in REQUIRED if not (root / relative).is_file()]
    if missing:
        print("ERRORE: pacchetto incompleto; mancano:", file=sys.stderr)
        for relative in missing:
            print(f"  - {relative}", file=sys.stderr)
        return 2

    changed_html: list[Path] = []
    for path in root.rglob("*.html"):
        if any(part in {".git", "node_modules"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        updated, changed = insert_menu_link(text)
        if changed:
            changed_html.append(path)
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")

    sitemap_changed = patch_sitemap(root / "sitemap.xml", args.dry_run)
    mode = "SIMULAZIONE" if args.dry_run else "COMPLETATO"
    print(f"{mode}: voce Scioperi aggiunta a {len(changed_html)} menu.")
    print(f"{mode}: sitemap {'aggiornato' if sitemap_changed else 'già aggiornato o assente'}.")
    print("Nessun URL esistente è stato rinominato o rimosso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
