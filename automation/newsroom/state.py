"""Stato persistente della redazione automatica.

Lo stato vive su un branch dedicato (``automation-state``) e **non** su ``main``:
Netlify pubblica la root di ``main``, quindi scrivere lo stato sul ramo di
produzione significherebbe un deploy ogni cinque minuti. Tenendolo separato il
watcher può girare quanto vuole senza consumare build.

Ogni elemento attraversa stati espliciti, così nessun candidato può generare
articoli doppi o rientrare in un ciclo infinito.
"""
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

# Ciclo di vita di un candidato.
SEEN = "seen"              # rilevato dal watcher
REJECTED = "rejected"      # scartato (filtro economico o verifica editoriale)
DRAFTED = "drafted"        # articolo + immagine pronti
QUEUED = "queued"          # in coda di pubblicazione
PUBLISHED = "published"    # deploy effettuato, non ancora verificato sul sito
VERIFIED = "verified"      # verificato sul dominio pubblico
FAILED = "failed"          # pubblicazione fallita in modo non recuperabile

ACTIVE_STATES = {SEEN, DRAFTED, QUEUED, PUBLISHED}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
    )
    try:
        json.dump(payload, handle, ensure_ascii=False, indent=1, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    finally:
        handle.close()
    os.replace(handle.name, path)


@dataclass
class Candidate:
    """Una notizia rilevata da una fonte."""

    url_key: str
    topic_key: str
    url: str
    title: str
    source: str
    source_tier: str
    published_at: str = ""
    first_seen: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)
    status: str = SEEN
    reason: str = ""
    priority: str = "normal"          # "breaking" oppure "normal"
    score: float = 0.0
    attempts: int = 0
    # Altre fonti che raccontano lo stesso fatto. Non sono rumore da scartare:
    # sono le conferme indipendenti che la verifica editoriale pretende prima
    # di trattare una notizia delicata come accertata.
    corroborations: list[dict[str, Any]] = field(default_factory=list)
    article: dict[str, Any] = field(default_factory=dict)

    def add_corroboration(self, source: str, url: str, title: str) -> bool:
        """Registra una conferma, evitando di contare due volte la stessa fonte."""
        if any(c.get("source") == source for c in self.corroborations):
            return False
        self.corroborations.append({"source": source, "url": url, "title": title})
        return True

    @property
    def independent_sources(self) -> int:
        """Quante fonti distinte riportano il fatto, compresa quella originale."""
        return 1 + len(self.corroborations)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Candidate":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


class Store:
    """Accesso allo stato su disco, con scritture atomiche."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.candidates_path = self.root / "candidates.json"
        self.published_path = self.root / "published.json"
        self.meta_path = self.root / "meta.json"
        self._candidates: dict[str, Candidate] = {}
        self._published: dict[str, dict[str, Any]] = {}
        self._meta: dict[str, Any] = {}
        self.load()

    # ------------------------------------------------------------------ I/O
    def load(self) -> None:
        if self.candidates_path.exists():
            raw = json.loads(self.candidates_path.read_text(encoding="utf-8"))
            self._candidates = {
                key: Candidate.from_dict(value) for key, value in raw.get("items", {}).items()
            }
        if self.published_path.exists():
            self._published = json.loads(self.published_path.read_text(encoding="utf-8")).get("items", {})
        if self.meta_path.exists():
            self._meta = json.loads(self.meta_path.read_text(encoding="utf-8"))

    def save(self) -> None:
        _write_atomic(
            self.candidates_path,
            {"updated_at": _now(), "items": {k: v.to_dict() for k, v in self._candidates.items()}},
        )
        _write_atomic(self.published_path, {"updated_at": _now(), "items": self._published})
        _write_atomic(self.meta_path, self._meta)

    # ------------------------------------------------------------ candidati
    def get(self, url_key: str) -> Candidate | None:
        return self._candidates.get(url_key)

    def all_candidates(self) -> list[Candidate]:
        return list(self._candidates.values())

    def by_status(self, *statuses: str) -> list[Candidate]:
        wanted = set(statuses)
        return [c for c in self._candidates.values() if c.status in wanted]

    def knows_url(self, url_key: str) -> bool:
        return url_key in self._candidates

    def knows_topic(self, topic_key: str) -> Candidate | None:
        """Ritorna un candidato con la stessa impronta esatta, se esiste."""
        if not topic_key:
            return None
        for candidate in self._candidates.values():
            if candidate.topic_key == topic_key:
                return candidate
        return None

    def find_similar(self, title: str, threshold: float = 0.6, limit: int = 1200) -> Candidate | None:
        """Cerca un candidato che racconti lo stesso fatto con parole diverse.

        L'impronta esatta non basta: "Terremoto di magnitudo 6.2 colpisce la
        costa del Giappone" e "Giappone, terremoto magnitudo 6.2 sulla costa"
        sono la stessa notizia ma hanno impronte diverse. Qui confrontiamo le
        parole significative, che è ciò che conta davvero.
        """
        from .normalize import title_similarity  # import locale: evita cicli

        if not title:
            return None
        recent = sorted(self._candidates.values(), key=lambda c: c.first_seen, reverse=True)[:limit]
        best: Candidate | None = None
        best_score = threshold
        for candidate in recent:
            score = title_similarity(title, candidate.title)
            if score >= best_score:
                best, best_score = candidate, score
        return best

    def add(self, candidate: Candidate) -> Candidate:
        self._candidates[candidate.url_key] = candidate
        return candidate

    def update(self, url_key: str, **changes: Any) -> Candidate | None:
        candidate = self._candidates.get(url_key)
        if candidate is None:
            return None
        for key, value in changes.items():
            setattr(candidate, key, value)
        candidate.updated_at = _now()
        return candidate

    # ----------------------------------------------------------- pubblicati
    def mark_published(self, url_key: str, slug: str, public_url: str, **extra: Any) -> None:
        self._published[slug] = {
            "url_key": url_key,
            "slug": slug,
            "public_url": public_url,
            "published_at": _now(),
            "verification": "pending",
            **extra,
        }
        self.update(url_key, status=PUBLISHED)

    def mark_verified(self, slug: str, checks: dict[str, Any]) -> None:
        record = self._published.get(slug)
        if record is None:
            return
        record["verification"] = "verified"
        record["verified_at"] = _now()
        record["checks"] = checks
        self.update(record.get("url_key", ""), status=VERIFIED)

    def mark_unverified(self, slug: str, checks: dict[str, Any], reason: str) -> None:
        record = self._published.get(slug)
        if record is None:
            return
        record["verification"] = "unverified"
        record["checked_at"] = _now()
        record["checks"] = checks
        record["reason"] = reason

    def published_slugs(self) -> set[str]:
        return set(self._published)

    def pending_verification(self) -> list[dict[str, Any]]:
        return [r for r in self._published.values() if r.get("verification") != "verified"]

    # ----------------------------------------------------------------- meta
    @property
    def meta(self) -> dict[str, Any]:
        return self._meta

    def note_cycle(self, name: str, payload: dict[str, Any]) -> None:
        cycles = self._meta.setdefault("cycles", {})
        cycles[name] = {"at": _now(), **payload}

    # ---------------------------------------------------------------- pulizia
    def prune(self, keep_days: int = 21) -> int:
        """Elimina i candidati chiusi più vecchi, per non far crescere lo stato."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
        removed = 0
        for key, candidate in list(self._candidates.items()):
            if candidate.status in ACTIVE_STATES:
                continue
            try:
                seen = datetime.fromisoformat(candidate.first_seen)
            except ValueError:
                continue
            if seen.tzinfo is None:
                seen = seen.replace(tzinfo=timezone.utc)
            if seen < cutoff:
                del self._candidates[key]
                removed += 1
        return removed


def existing_site_titles(articles_dir: Path, limit: int = 400) -> list[str]:
    """Titoli approssimativi degli articoli già online, ricavati dagli slug.

    Serve a non riscrivere un fatto che CurioMondo ha già raccontato, anche se
    lo stato del watcher venisse azzerato. Leggere lo slug è molto più veloce
    che aprire e parsare centinaia di file HTML a ogni ciclo.
    """
    if not articles_dir.exists():
        return []
    files = sorted(articles_dir.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    titles = []
    for path in files[:limit]:
        if path.name == "index.html":
            continue
        titles.append(path.stem.replace("-", " "))
    return titles
