"""Normalizzazione e impronte digitali per la deduplicazione.

La stessa notizia arriva da fonti diverse con URL sporchi di parametri di
tracciamento e titoli leggermente differenti. Qui produciamo due chiavi:

* ``url_key``   — l'URL ripulito, per riconoscere lo stesso identico link;
* ``topic_key`` — le parole significative del titolo, per riconoscere la stessa
  notizia raccontata da testate diverse.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import parse_qsl, urlsplit, urlunsplit

# Parametri di tracciamento che non identificano il contenuto.
_TRACKING_PREFIXES = ("utm_", "pk_", "mtm_", "hsa_", "fb_", "ga_")
_TRACKING_EXACT = {
    "gclid", "fbclid", "igshid", "mc_cid", "mc_eid", "ref", "ref_src", "cmpid",
    "icid", "ncid", "smid", "spm", "s_cid", "at_medium", "at_campaign", "oc",
    "__twitter_impression", "guccounter", "guce_referrer", "guce_referrer_sig",
}

# Parole troppo comuni per distinguere una notizia da un'altra.
_STOPWORDS = {
    "a", "ad", "agli", "ai", "al", "alla", "alle", "allo", "anche", "che", "chi",
    "coi", "col", "come", "con", "contro", "cui", "da", "dal", "dalla", "dalle",
    "dallo", "degli", "dei", "del", "della", "delle", "dello", "di", "dopo", "dove",
    "e", "ed", "fra", "gli", "ha", "hanno", "i", "il", "in", "la", "le", "lo", "ma",
    "nel", "nella", "nelle", "nello", "non", "o", "per", "piu", "più", "quando",
    "se", "si", "su", "sui", "sul", "sulla", "sulle", "sullo", "tra", "un", "una",
    "uno", "and", "for", "from", "of", "on", "the", "to", "with", "after", "says",
    "said", "new", "over", "as", "at", "by", "in", "is", "it", "its", "be",
}


def strip_accents(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def canonical_url(url: str) -> str:
    """Rimuove parametri di tracciamento, frammenti e differenze irrilevanti."""
    if not url:
        return ""
    parts = urlsplit(url.strip())
    # http e https indicano la stessa risorsa: per la deduplicazione contano uguale.
    scheme = "https"
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if parts.port and parts.port not in (80, 443):
        host = f"{host}:{parts.port}"
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=False)
        if key.lower() not in _TRACKING_EXACT
        and not any(key.lower().startswith(prefix) for prefix in _TRACKING_PREFIXES)
    ]
    query.sort()
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if len(path) > 1:
        path = path.rstrip("/")
    rebuilt = urlunsplit((scheme, host, path, "&".join(f"{k}={v}" for k, v in query), ""))
    return rebuilt


# Suffissi a due livelli: senza questi "bbc.co.uk" diventerebbe "co.uk" e tutte
# le testate britanniche sembrerebbero la stessa fonte.
_SUFFISSI_COMPOSTI = (
    "co.uk", "org.uk", "gov.uk", "ac.uk", "com.au", "net.au", "org.au",
    "co.jp", "com.br", "co.in", "com.tr", "europa.eu", "gov.it",
)


def dominio(url: str) -> str:
    """Testata a cui appartiene un indirizzo, ridotta al dominio registrabile.

    Serve a non contare due volte la stessa fonte: lo stesso lancio ANSA
    ripreso da un aggregatore arriva con un indirizzo diverso, ma non e una
    conferma indipendente — e la stessa testata.
    """
    host = urlsplit(url or "").netloc.lower().split("@")[-1].split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    parti = host.split(".")
    if len(parti) <= 2:
        return host
    ultimi_due = ".".join(parti[-2:])
    if ultimi_due in _SUFFISSI_COMPOSTI:
        return ".".join(parti[-3:])
    return ultimi_due


def url_key(url: str) -> str:
    canonical = canonical_url(url)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20] if canonical else ""


def title_tokens(title: str) -> list[str]:
    """Parole significative del titolo, normalizzate e ordinate.

    I numeri di almeno due cifre restano: in una notizia "6.2" o "2026" sono
    spesso l'elemento che distingue un fatto da un altro. Le cifre singole no,
    perché nascono quasi sempre dallo spezzarsi di un decimale.
    """
    flat = strip_accents(title or "").lower()
    words = re.findall(r"[a-z0-9]+", flat)
    keep = []
    for word in words:
        if word in _STOPWORDS:
            continue
        if word.isdigit():
            if len(word) >= 2:
                keep.append(word)
        elif len(word) >= 3:
            keep.append(word)
    return sorted(set(keep))


def topic_key(title: str) -> str:
    """Impronta grossolana della notizia, usata come raggruppamento rapido.

    Non basta da sola: due testate che raccontano lo stesso fatto usano quasi
    sempre una parola in più o in meno, e l'impronta cambierebbe. Serve perciò
    solo a raggruppare i casi facili; i quasi-duplicati li riconosce
    ``title_similarity``.
    """
    tokens = title_tokens(title)
    if len(tokens) < 3:
        return ""
    strongest = sorted(tokens, key=lambda w: (-len(w), w))[:5]
    return hashlib.sha256(" ".join(sorted(strongest)).encode("utf-8")).hexdigest()[:20]


def title_similarity(first: str, second: str) -> float:
    """Somiglianza 0..1 fra due titoli, basata sulle parole significative."""
    a, b = set(title_tokens(first)), set(title_tokens(second))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def clean_title(raw: str) -> str:
    """Toglie il suffisso della testata che molti feed aggiungono al titolo."""
    title = re.sub(r"\s+", " ", (raw or "")).strip()
    # Google News usa " - Testata" in coda.
    title = re.sub(r"\s+[-–—]\s+[^-–—]{2,40}$", "", title).strip()
    return title
