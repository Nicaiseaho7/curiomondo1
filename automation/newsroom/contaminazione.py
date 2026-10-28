"""Controllo anti-contaminazione. Blocca le istruzioni interne prima della pubblicazione.

Due passaggi, entrambi deterministici. Il secondo non è un secondo modello:
guarda il destinatario della frase, non soltanto le parole vietate.
Se questo modulo non si carica, la pubblicazione resta bloccata.
"""
from __future__ import annotations

from html import unescape
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PASS, REVISE, BLOCK = "PASS", "REVISE", "BLOCK"
REGISTRO = Path("/tmp/curiomondo-controlli-editoriali.jsonl")

# Frasi rivolte al sistema, non al lettore. Non è un elenco di parole singole:
# «istruzioni» da solo può essere la notizia.
OPERATIVE = (
    r"non creare un secondo articolo",
    r"aggiornare la pagina esistente",
    r"questa informazione deve essere inserita",
    r"l['’]agente deve",
    r"mantenere invariato lo slug",
    r"non modificare il titolo seo",
    r"il workflow deve",
    r"inserire qui un collegamento",
    r"controllare successivamente la correttezza",
    r"(?:questa sezione|questo testo) è stat[oa] generat[oa] automaticamente",
    r"nota per il sistema editoriale",
    r"istruzioni per chatgpt",
    r"da verificare prima della pubblicazione",
    r"\bTODO\b",
    r"\bDEBUG\b",
    r"\bPLACEHOLDER\b",
    r"\bFIXME\b",
    r"url originale",
    r"senza creare una nuova url",
    r"curiomondo aggiorner",
    r"questa pagina sar[àa] corretta",
    r"questo articolo integra gli sviluppi",
    r"mantenendo la url",
    r"ignora le istruzioni precedenti",
    r"modifica il workflow",
    r"pubblica questo testo",
)
# Secondo passaggio: a chi è rivolta la frase.
DESTINATARIO = (
    r"\b(?:il cms|il workflow|l['’]agente editoriale|chatgpt|il sistema editoriale)\b.{0,90}\b(?:deve|pubblica|aggiorna|non modificar)",
    r"\b(?:non modificare|lascia invariato|mantieni)\b.{0,40}\bslug\b",
    r"\bprompt\b.{0,40}\b(?:dell['’]agente|di sistema|interno)\b",
)
ORARI = re.compile(r"orari-tv|palinsesto|programmazione-tv", re.I)
ORARI_NEL_TESTO = re.compile(r"\borari[oi]?\b|palinsesto|diretta (?:tv|televisiva)|in tv\b", re.I)


def _trova(testo: str, regole: tuple[str, ...]) -> list[str]:
    trovati = []
    for regola in regole:
        match = re.search(regola, testo, re.I)
        if match:
            trovati.append(match.group(0)[:80])
    return trovati


def controlla_testo(testo: str, *, slug: str = "") -> dict:
    """Ritorna PASS, REVISE o BLOCK. Un testo vuoto non è pubblicabile."""
    if not str(testo).strip():
        return {"stato": BLOCK, "errori": ["testo pubblico assente"], "tipo": ["vuoto"]}
    piegato = str(testo).casefold()
    errori = _trova(piegato, OPERATIVE)
    if errori:
        return {"stato": BLOCK, "errori": errori, "tipo": ["istruzione interna"]}
    indirette = _trova(piegato, DESTINATARIO)
    if indirette:
        return {"stato": BLOCK, "errori": indirette, "tipo": ["destinatario operativo"]}
    if slug and ORARI.search(slug) and not ORARI_NEL_TESTO.search(testo):
        return {
            "stato": REVISE,
            "errori": ["lo slug promette orari o tv, il testo non ne parla"],
            "tipo": ["intento di ricerca cambiato"],
        }
    return {"stato": PASS, "errori": [], "tipo": []}


def testo_pubblico_html(pagina: str) -> str:
    """Campi che il lettore o un motore di ricerca può vedere. Non lo script di pagina."""
    pezzi = []
    for attr in ("title", "description"):
        for match in re.finditer(
            rf'<meta[^>]+(?:name|property)="(?:og:)?{attr}"[^>]+content="([^"]*)"',
            pagina,
            re.I,
        ):
            pezzi.append(unescape(match.group(1)))
    for tag in ("title", "h1", "h2", "h3", "figcaption", "li", "p", "span", "strong"):
        pezzi.extend(unescape(re.sub(r"<[^>]+>", " ", m)) for m in re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", pagina, re.S | re.I))
    for alt in re.findall(r'\balt="([^"]*)"', pagina, re.I):
        pezzi.append(unescape(alt))
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', pagina, re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            pezzi.append(raw)
            continue
        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if isinstance(node, dict):
                pezzi.append(str(node.get("headline", "")))
                pezzi.append(str(node.get("description", "")))
    return "\n".join(pezzi)


def controlla_html(pagina: str, *, slug: str = "") -> dict:
    if not isinstance(pagina, str):
        return {"stato": BLOCK, "errori": ["pagina non leggibile"], "tipo": ["verifica incompleta"]}
    return controlla_testo(testo_pubblico_html(pagina), slug=slug)


def controlla_articolo_dict(articolo: dict) -> dict:
    campi = [
        str(articolo.get("titolo", "")),
        str(articolo.get("sommario", "")),
        str((articolo.get("immagine") or {}).get("alt", "")),
    ]
    campi.extend(str(p) for p in articolo.get("paragrafi") or [])
    for dato in articolo.get("dati_chiave") or []:
        campi.append(str(dato.get("valore", "")))
        campi.append(str(dato.get("etichetta", "")))
    return controlla_testo("\n".join(campi), slug=str(articolo.get("slug", "")))


def registra(identificativo: str, contenuto: str, esito: dict, *, correzione: str = "") -> None:
    """Registro privato, fuori dal sito e fuori dal repository."""
    riga = {
        "id": identificativo,
        "quando": datetime.now(ZoneInfo("Europe/Rome")).isoformat(timespec="seconds"),
        "hash": hashlib.sha256(contenuto.encode("utf-8")).hexdigest()[:16],
        "stato": esito.get("stato", BLOCK),
        "tipo": esito.get("tipo", []),
        "errori": esito.get("errori", []),
        "correzione": correzione,
    }
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(riga, ensure_ascii=False) + "\n")


def autorizza(pagina: str, *, slug: str = "", identificativo: str = "") -> dict:
    """Unico via libera. Manca il PASS, la pubblicazione non parte."""
    try:
        esito = controlla_html(pagina, slug=slug)
    except Exception as exc:
        esito = {"stato": BLOCK, "errori": [f"controllo non disponibile: {exc}"], "tipo": ["verifica incompleta"]}
    if esito.get("stato") not in {PASS, REVISE, BLOCK}:
        esito = {"stato": BLOCK, "errori": ["stato sconosciuto"], "tipo": ["verifica incompleta"]}
    registra(identificativo or slug or "bozza", pagina, esito)
    if esito["stato"] != PASS:
        raise ContaminazioneBloccata(esito)
    return esito


class ContaminazioneBloccata(RuntimeError):
    def __init__(self, esito: dict):
        self.esito = esito
        super().__init__(f"{esito.get('stato')}: {'; '.join(esito.get('errori') or [])}")
