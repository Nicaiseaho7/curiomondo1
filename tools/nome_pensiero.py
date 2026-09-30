"""Assegna il pensiero con il nome sulle notizie.

Nomi: i 3.000 più usati, in assets/data/nomi-italiani.json.
Frasi: parlate, una per notizia, in assets/data/frasi-nome.json.
"""
from __future__ import annotations

from html import escape
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets/data/nomi-italiani.json"
PHRASES = ROOT / "assets/data/frasi-nome.json"
NAME_RE = re.compile(r'cm-name-note__name">([^<]+)')
TEXT_RE = re.compile(r'cm-name-note__text">([^<]+)')


def catalog() -> list[str]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def phrases() -> list[str]:
    return json.loads(PHRASES.read_text(encoding="utf-8"))


def used(root: Path | None = None) -> tuple[set[str], set[str]]:
    root = root or ROOT
    names: set[str] = set()
    texts: set[str] = set()
    for path in (root / "notizie").glob("*.html"):
        html = path.read_text(encoding="utf-8")
        for name in NAME_RE.findall(html):
            names.add(name.casefold())
        for text in TEXT_RE.findall(html):
            texts.add(text)
    return names, texts


def next_name(root: Path | None = None) -> str:
    root = root or ROOT
    taken, _ = used(root)
    names = catalog()
    for name in names:
        if name.casefold() not in taken:
            return name
    recent: list[str] = []
    for path in sorted((root / "notizie").glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True):
        html = path.read_text(encoding="utf-8")
        found = NAME_RE.search(html)
        if found:
            recent.append(found.group(1).casefold())
        if len(recent) >= 40:
            break
    blocked = set(recent)
    for name in names:
        if name.casefold() not in blocked:
            return name
    raise RuntimeError("nessun nome disponibile")


def next_message(root: Path | None = None) -> str:
    root = root or ROOT
    _, taken = used(root)
    for message in phrases():
        if message not in taken:
            return message
    raise RuntimeError("nessuna frase nuova disponibile")


def note_markup(root: Path | None = None) -> str:
    name = next_name(root)
    message = next_message(root)
    safe_name = escape(name)
    return (
        '<aside class="cm-name-card" aria-label="Un pensiero per '
        + escape(name, quote=True)
        + '"><p class="cm-name-card__label">Un pensiero per <strong class="cm-name-note__name">'
        + safe_name
        + '</strong></p><p class="cm-name-card__text"><span class="cm-name-note__text">'
        + escape(message)
        + "</span></p></aside>"
    )
