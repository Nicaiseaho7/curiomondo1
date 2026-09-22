"""Filtri economici: decidono se vale la pena svegliare il worker editoriale.

Sono volutamente semplici e deterministici. Il loro compito non è giudicare la
notizia — quello spetta alla verifica editoriale — ma evitare di spendere una
chiamata al modello per contenuti palesemente inadatti: oroscopi, quote
scommesse, dirette perenni, gossip, o fatti che CurioMondo ha già raccontato.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .normalize import strip_accents

# Contenuti che CurioMondo non pubblica: scartati senza consultare il modello.
EXCLUDED_PATTERNS = (
    r"\boroscopo\b", r"\bhoroscope\b", r"\bgossip\b", r"\bpronostic", r"\bquote\b.*\bscommess",
    r"\bbetting\b", r"\bodds\b", r"\bmoviola\b", r"\bcalciomercato in diretta\b",
    r"\blive blog\b", r"\bliveblog\b", r"\bdiretta live\b", r"\bminuto per minuto\b",
    r"\bsegui la diretta\b", r"\bfoto gallery\b", r"\bphotos?:\b", r"\bin pictures\b",
    r"\bsponsored\b", r"\badvertorial\b", r"\bpubbliredazionale\b", r"\bcoupon\b",
    r"\bofferte\b.*\bamazon\b", r"\bblack friday\b", r"\bsaldi\b",
    r"\bopinione\b", r"\beditoriale:", r"\bcommento:", r"\bopinion\b", r"\banalysis:",
    r"\brecensione\b", r"\breview:", r"\bnecrologi\b", r"\bwhat to watch\b",
)

# Segnali che una notizia è davvero urgente.
BREAKING_PATTERNS = (
    r"\bbreaking\b", r"\bultim'ora\b", r"\bultima ora\b", r"\bflash\b",
    r"\bterremoto\b", r"\bscossa\b", r"\bmagnitudo\b", r"\besplosione\b",
    r"\battentato\b", r"\bsparatoria\b", r"\bevacuazione\b", r"\bstato di emergenza\b",
    r"\bdimission", r"\bsi dimette\b", r"\bmorto\b", r"\bmorta\b", r"\bucciso\b",
    r"\bcessate il fuoco\b", r"\baccordo raggiunto\b", r"\btregua\b",
    r"\bearthquake\b", r"\bexplosion\b", r"\bresigns\b", r"\bkilled\b", r"\bceasefire\b",
)

# Temi che richiedono verifica editoriale più severa (guerra, morte, salute, giustizia).
HIGH_RISK_PATTERNS = (
    r"\bguerra\b", r"\bmissil", r"\braid\b", r"\bbombard", r"\bucciso\b", r"\bmorti\b",
    r"\bvittime\b", r"\bstrage\b", r"\battacco\b", r"\bterror", r"\bostaggi\b",
    r"\bnucleare\b", r"\bepidemia\b", r"\bvirus\b", r"\bcontagi\b", r"\bfarmaco\b",
    r"\barrestato\b", r"\bindagato\b", r"\bcondannato\b", r"\bprocesso\b", r"\binchiesta\b",
    r"\bfrode\b", r"\bcorruzione\b", r"\bdimission", r"\belezioni\b", r"\breferendum\b",
    r"\bwar\b", r"\bkilled\b", r"\bcasualties\b", r"\bindicted\b", r"\barrested\b",
)

_EXCLUDED_RE = re.compile("|".join(EXCLUDED_PATTERNS), re.I)
_BREAKING_RE = re.compile("|".join(BREAKING_PATTERNS), re.I)
_HIGH_RISK_RE = re.compile("|".join(HIGH_RISK_PATTERNS), re.I)

TIER_WEIGHT = {"primary": 1.0, "agency": 0.9, "science": 0.85, "markets": 0.8, "sport": 0.75}
TRUST_WEIGHT = {"high": 1.0, "medium": 0.75, "low": 0.4}


@dataclass
class Decision:
    accepted: bool
    reason: str = ""
    priority: str = "normal"
    score: float = 0.0
    high_risk: bool = False


# Una scossa lieve non è una notizia: in Italia se ne registrano decine al
# giorno. Sotto questa magnitudo il sisma viene trattato come rumore di fondo.
MAGNITUDO_MINIMA = 3.0
_MAGNITUDO_RE = re.compile(
    r"(?:magnitudo|magnitude|\bml\b|\bmw\b|\bmb\b)[\s:]*([0-9]+(?:[.,][0-9]+)?)", re.I
)


def magnitudo_trascurabile(testo: str) -> bool:
    """Vero se il testo parla di un sisma e la magnitudo è sotto la soglia."""
    trovate = [float(m.replace(",", ".")) for m in _MAGNITUDO_RE.findall(testo or "")]
    if not trovate:
        return False
    return max(trovate) < MAGNITUDO_MINIMA


def is_breaking(title: str, summary: str = "") -> bool:
    testo = f"{title} {summary}"
    if not _BREAKING_RE.search(testo):
        return False
    # Le parole d'allarme non bastano: un terremoto di magnitudo 2.0 contiene
    # "terremoto" ma non è ultima ora.
    if magnitudo_trascurabile(testo):
        return False
    return True


def is_high_risk(title: str, summary: str = "") -> bool:
    return bool(_HIGH_RISK_RE.search(f"{title} {summary}"))


def _age_hours(published_at: str, now: datetime | None = None) -> float | None:
    if not published_at:
        return None
    try:
        moment = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    reference = now or datetime.now(timezone.utc)
    return (reference - moment).total_seconds() / 3600.0


def score_item(title: str, tier: str, trust: str, published_at: str, now: datetime | None = None) -> float:
    """Punteggio grezzo 0..1: quanto merita l'attenzione del worker editoriale."""
    base = TIER_WEIGHT.get(tier, 0.6) * TRUST_WEIGHT.get(trust, 0.7)
    age = _age_hours(published_at, now)
    if age is None:
        freshness = 0.6          # data assente: né premiata né penalizzata
    elif age <= 1:
        freshness = 1.0
    elif age <= 3:
        freshness = 0.9
    elif age <= 8:
        freshness = 0.7
    elif age <= 24:
        freshness = 0.5
    else:
        freshness = 0.4
    bonus = 0.1 if is_breaking(title) else 0.0
    # Un titolo troppo corto di solito è una scheda, non una notizia.
    words = len(re.findall(r"\w+", strip_accents(title)))
    length_penalty = 0.15 if words < 5 else 0.0
    return max(0.0, min(1.0, base * freshness + bonus - length_penalty))


def screen(
    title: str,
    summary: str,
    tier: str,
    trust: str,
    published_at: str,
    *,
    max_age_hours: float = 168.0,
    min_score: float = 0.28,
    now: datetime | None = None,
) -> Decision:
    """Filtro preliminare economico applicato prima di qualunque chiamata IA."""
    text = f"{title} {summary}"
    if len(title.strip()) < 15:
        return Decision(False, "titolo_troppo_corto")
    if _EXCLUDED_RE.search(text):
        return Decision(False, "categoria_esclusa")

    if magnitudo_trascurabile(text):
        # Le reti sismiche pubblicano ogni scossa: senza questo filtro il
        # worker spenderebbe una verifica per ogni micro-sisma della giornata.
        return Decision(False, "sisma_sotto_soglia")

    age = _age_hours(published_at, now)
    if age is not None and age > max_age_hours:
        return Decision(False, "troppo_vecchia")
    if age is not None and age < -2:
        # Date nel futuro indicano feed mal formati: meglio non fidarsi.
        return Decision(False, "data_incoerente")

    score = score_item(title, tier, trust, published_at, now)
    high_risk = is_high_risk(title, summary)
    breaking = is_breaking(title, summary)

    # Un tema ad alto rischio da fonte non affidabile non merita una chiamata IA:
    # servirebbe comunque una fonte primaria per poterlo raccontare.
    if high_risk and TRUST_WEIGHT.get(trust, 0.7) < 0.75:
        return Decision(False, "alto_rischio_fonte_debole", high_risk=True)

    if score < min_score:
        return Decision(False, "punteggio_basso", score=score, high_risk=high_risk)

    return Decision(
        True,
        "",
        priority="breaking" if breaking else "normal",
        score=score,
        high_risk=high_risk,
    )
