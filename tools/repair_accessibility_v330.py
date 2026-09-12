#!/usr/bin/env python3
"""Repair repeat ebook H1 headings and missing library index descriptions."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTIONS = {
    "biblioteca/vita-relazioni/attenzione-tempo/index.html": (
        "Guide CurioMondo per proteggere attenzione, concentrazione e tempo "
        "personale nelle giornate piene di impegni."
    ),
    "biblioteca/vita-relazioni/scelte-consapevoli/index.html": (
        "Guide CurioMondo per riconoscere automatismi, chiarire le priorità e "
        "compiere scelte più consapevoli."
    ),
}


def repair_ebook_headings(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "cm-book-page" not in text:
        return False
    seen = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal seen
        seen += 1
        if seen == 1:
            return match.group(0)
        return f'<h2 class="cm-book-title">{match.group(1)}</h2>'

    updated = re.sub(r"<h1>(.*?)</h1>", replace, text, flags=re.DOTALL)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def add_description(path: Path, description: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if re.search(r'<meta\s+name=["\']description["\']', text, re.I):
        return False
    updated, count = re.subn(
        r"(</title>)",
        rf'\1<meta name="description" content="{description}">',
        text,
        count=1,
        flags=re.I,
    )
    if count != 1:
        raise RuntimeError(f"Title element not found in {path}")
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    repaired = []
    for path in ROOT.glob("biblioteca/**/*.html"):
        if repair_ebook_headings(path):
            repaired.append(str(path.relative_to(ROOT)))
    for relative, description in DESCRIPTIONS.items():
        path = ROOT / relative
        if add_description(path, description):
            repaired.append(relative)
    print(f"Repaired {len(repaired)} files")
    for item in repaired:
        print(item)


if __name__ == "__main__":
    main()
