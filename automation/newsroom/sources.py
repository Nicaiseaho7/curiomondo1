"""Lettura delle fonti: RSS e Atom, con richieste educate ed economiche.

Il watcher gira spesso, quindi ogni richiesta usa ``ETag``/``Last-Modified``:
se la fonte non ha novità risponde ``304`` e non scarichiamo nulla. Le fonti
lente o rotte non devono mai bloccare il ciclo, perciò ogni errore è isolato e
registrato senza interrompere le altre.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Iterable

from .normalize import canonical_url, clean_title, topic_key, url_key

USER_AGENT = "CurioMondoNewsroom/1.0 (+https://curiomondo.it; redazione automatica)"
DEFAULT_TIMEOUT = 12
DEFAULT_RETRIES = 2


@dataclass
class Feed:
    id: str
    name: str
    url: str
    tier: str = "agency"
    category: str = "mondo"
    cadence: str = "deep"
    trust: str = "medium"
    direct: bool = True
    enabled: bool = True
    # Falso per le testate che pubblicano il testo solo dietro registrazione o
    # pagamento: restano utili come conferma di un fatto, ma non possono
    # fornire il materiale per scriverlo.
    materiale: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Feed":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class Item:
    """Una voce grezza estratta da un feed."""

    title: str
    url: str
    published_at: str
    source: str
    source_tier: str
    category: str
    trust: str
    summary: str = ""
    materiale: bool = True

    @property
    def url_key(self) -> str:
        return url_key(self.url)

    @property
    def topic_key(self) -> str:
        return topic_key(self.title)


def load_feeds(path: Path, cadence: str | None = None) -> list[Feed]:
    """Carica il registro delle fonti, filtrando per velocità richiesta.

    ``cadence='fast'`` restituisce solo i feed del controllo rapido;
    ``cadence='deep'`` restituisce tutti i feed (la scansione ampia include
    anche quelli rapidi, così nulla resta scoperto).
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    feeds = [Feed.from_dict(item) for item in data.get("feeds", [])]
    feeds = [f for f in feeds if f.enabled]
    if cadence == "fast":
        feeds = [f for f in feeds if f.cadence == "fast"]
    return feeds


def _parse_date(value: str | None) -> str:
    if not value:
        return ""
    text = value.strip()
    for parser in (_parse_rfc2822, _parse_iso):
        try:
            moment = parser(text)
        except Exception:
            continue
        if moment is not None:
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=timezone.utc)
            return moment.astimezone(timezone.utc).isoformat(timespec="seconds")
    return ""


def _parse_rfc2822(text: str) -> datetime | None:
    return parsedate_to_datetime(text)


def _parse_iso(text: str) -> datetime | None:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _tag(element: ET.Element) -> str:
    return element.tag.split("}")[-1].lower()


def parse_feed(payload: bytes, feed: Feed) -> list[Item]:
    """Estrae le voci da RSS 2.0, RDF o Atom senza dipendenze esterne."""
    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        return []

    items: list[Item] = []
    for node in root.iter():
        name = _tag(node)
        if name not in ("item", "entry"):
            continue
        title = ""
        link = ""
        published = ""
        summary = ""
        for child in node:
            child_tag = _tag(child)
            text = (child.text or "").strip()
            if child_tag == "title" and not title:
                title = text
            elif child_tag == "link":
                # RSS mette l'URL nel testo, Atom nell'attributo href.
                href = child.get("href")
                if href and child.get("rel", "alternate") == "alternate" and not link:
                    link = href.strip()
                elif text and not link:
                    link = text
            elif child_tag in ("pubdate", "published", "updated", "date") and not published:
                published = _parse_date(text)
            elif child_tag in ("description", "summary", "content") and not summary:
                summary = text[:600]
        title = clean_title(title)
        if not title or not link:
            continue
        items.append(
            Item(
                title=title,
                url=canonical_url(link),
                published_at=published,
                source=feed.name,
                source_tier=feed.tier,
                category=feed.category,
                trust=feed.trust,
                summary=summary,
                materiale=feed.materiale,
            )
        )
    return items


def fetch_feed(
    feed: Feed,
    cache: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> tuple[list[Item], dict[str, Any]]:
    """Scarica un feed. Ritorna le voci e lo stato di salute della fonte.

    Usa la cache condizionale: se la fonte risponde 304 non c'è nulla di nuovo
    e il ciclo costa una manciata di byte.
    """
    cache = cache or {}
    headers = {"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml, */*"}
    entry = cache.get(feed.id, {})
    if entry.get("etag"):
        headers["If-None-Match"] = entry["etag"]
    if entry.get("last_modified"):
        headers["If-Modified-Since"] = entry["last_modified"]

    delay = 1.0
    last_error = ""
    for attempt in range(retries + 1):
        request = urllib.request.Request(feed.url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read()
                new_cache = {
                    "etag": response.headers.get("ETag", ""),
                    "last_modified": response.headers.get("Last-Modified", ""),
                    "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
                items = parse_feed(payload, feed)
                return items, {"feed": feed.id, "status": "ok", "items": len(items), "cache": new_cache}
        except urllib.error.HTTPError as exc:
            if exc.code == 304:
                entry["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                return [], {"feed": feed.id, "status": "not_modified", "items": 0, "cache": entry}
            last_error = f"http_{exc.code}"
            if exc.code in (400, 401, 403, 404, 410):
                break  # errori definitivi: inutile insistere
        except Exception as exc:  # rete, timeout, DNS, XML malformato
            last_error = type(exc).__name__
        if attempt < retries:
            time.sleep(delay)
            delay *= 2
    return [], {"feed": feed.id, "status": "error", "items": 0, "error": last_error, "cache": entry}


def fetch_all(
    feeds: Iterable[Feed],
    cache: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    workers: int = 8,
) -> tuple[list[Item], list[dict[str, Any]], dict[str, Any]]:
    """Interroga tutte le fonti in parallelo, isolando gli errori.

    In sequenza una manciata di fonti lente basterebbe a sforare la finestra di
    cinque minuti; in parallelo il ciclo dura quanto la fonte più lenta.
    """
    cache = dict(cache or {})
    feed_list = list(feeds)
    collected: list[Item] = []
    health: list[dict[str, Any]] = []
    if not feed_list:
        return collected, health, cache

    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(feed_list)))) as pool:
        futures = {
            pool.submit(fetch_feed, feed, dict(cache), timeout): feed
            for feed in feed_list
        }
        for future in as_completed(futures):
            feed = futures[future]
            try:
                items, report = future.result()
            except Exception as exc:  # nessuna fonte può far cadere il ciclo
                health.append({"feed": feed.id, "status": "error", "items": 0, "error": type(exc).__name__})
                continue
            collected.extend(items)
            if report.get("cache"):
                cache[feed.id] = report["cache"]
            health.append({k: v for k, v in report.items() if k != "cache"})
    return collected, health, cache
