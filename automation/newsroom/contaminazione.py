"""Toglie dal testo pubblico le frasi operative, poi lascia passare la notizia.

Il controllo segnala la frase. Non ferma la pubblicazione: la frase si elimina
e si ricontrolla. Se non c'è più, lo stato è PASS.
"""
from __future__ import annotations

from html import escape, unescape
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
DESTINATARIO = (
    r"\b(?:il cms|il workflow|l['’]agente editoriale|chatgpt|il sistema editoriale)\b.{0,90}\b(?:deve|pubblica|aggiorna|non modificar)",
    r"\b(?:non modificare|lascia invariato|mantieni)\b.{0,40}\bslug\b",
    r"\bprompt\b.{0,40}\b(?:dell['’]agente|di sistema|interno)\b",
)
ORARI = re.compile(r"orari-tv|palinsesto|programmazione-tv", re.I)
ORARI_NEL_TESTO = re.compile(r"\borari[oi]?\b|palinsesto|diretta (?:tv|televisiva)|in tv\b", re.I)
TAG_VISIBILI = ("p", "h1", "h2", "h3", "li", "figcaption", "title")


def _trova(testo: str, regole: tuple[str, ...]) -> list[str]:
    trovati = []
    for regola in regole:
        match = re.search(regola, testo, re.I)
        if match:
            trovati.append(match.group(0)[:80])
    return trovati


def frase_vietata(testo: str) -> bool:
    piegato = str(testo).casefold()
    return bool(_trova(piegato, OPERATIVE) or _trova(piegato, DESTINATARIO))


def pulisci_testo(testo: str) -> str:
    """Tiene i fatti e butta solo la frase che farebbe scattare il BLOCK."""
    parti = re.split(r"(?<=[.!?])\s+", str(testo).strip())
    tenute = [parte.strip() for parte in parti if parte.strip() and not frase_vietata(parte)]
    return " ".join(tenute)


def controlla_testo(testo: str, *, slug: str = "") -> dict:
    """Dice se il testo, così com'è, contiene ancora una frase vietata."""
    if not str(testo).strip():
        return {"stato": BLOCK, "errori": ["testo pubblico assente"], "tipo": ["vuoto"]}
    if frase_vietata(testo):
        return {"stato": BLOCK, "errori": _trova(testo.casefold(), OPERATIVE + DESTINATARIO), "tipo": ["istruzione interna"]}
    if slug and ORARI.search(slug) and not ORARI_NEL_TESTO.search(testo):
        return {
            "stato": REVISE,
            "errori": ["lo slug promette orari o tv, il testo non ne parla"],
            "tipo": ["intento di ricerca cambiato"],
        }
    return {"stato": PASS, "errori": [], "tipo": []}


def testo_pubblico_html(pagina: str) -> str:
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


def pulisci_html(pagina: str) -> str:
    def fix(match):
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        plain = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
        if not frase_vietata(plain):
            return match.group(0)
        pulito = pulisci_testo(plain)
        if not pulito:
            return ""
        return f"<{tag}{attrs}>{escape(pulito)}</{tag}>"

    pagina = re.sub(
        r"<(p|h1|h2|h3|li|figcaption|title)(\b[^>]*)>(.*?)</\1>",
        fix,
        pagina,
        flags=re.S | re.I,
    )

    def fix_attr(match):
        content = unescape(match.group(2))
        if not frase_vietata(content):
            return match.group(0)
        return match.group(1) + escape(pulisci_testo(content), quote=True) + match.group(3)

    pagina = re.sub(r'(content=")(.*?)(")', fix_attr, pagina)
    return pagina


def controlla_html(pagina: str, *, slug: str = "") -> dict:
    if not isinstance(pagina, str):
        return {"stato": BLOCK, "errori": ["pagina non leggibile"], "tipo": ["verifica incompleta"]}
    return controlla_testo(testo_pubblico_html(pagina), slug=slug)


def campi_articolo(articolo: dict) -> list[str]:
    campi = [
        str(articolo.get("titolo", "")),
        str(articolo.get("sommario", "")),
        str((articolo.get("immagine") or {}).get("alt", "")),
    ]
    campi.extend(str(p) for p in articolo.get("paragrafi") or [])
    for dato in articolo.get("dati_chiave") or []:
        campi.append(str(dato.get("valore", "")))
        campi.append(str(dato.get("etichetta", "")))
    return campi


def controlla_articolo_dict(articolo: dict) -> dict:
    return controlla_testo("\n".join(campi_articolo(articolo)), slug=str(articolo.get("slug", "")))


def sistema_articolo(articolo: dict) -> dict:
    """Pulisce la bozza. Dopo, il controllo delle frasi vietate deve essere PASS."""
    for chiave in ("titolo", "sommario"):
        if chiave in articolo:
            articolo[chiave] = pulisci_testo(str(articolo.get(chiave, "")))
    immagine = articolo.get("immagine")
    if isinstance(immagine, dict) and immagine.get("alt"):
        immagine["alt"] = pulisci_testo(str(immagine.get("alt", "")))
    if articolo.get("paragrafi"):
        articolo["paragrafi"] = [pulisci_testo(str(p)) for p in articolo["paragrafi"] if pulisci_testo(str(p))]
    for dato in articolo.get("dati_chiave") or []:
        if isinstance(dato, dict):
            dato["valore"] = pulisci_testo(str(dato.get("valore", ""))) or dato.get("valore", "")
            dato["etichetta"] = pulisci_testo(str(dato.get("etichetta", ""))) or dato.get("etichetta", "")
    return articolo


def sistema(pagina: str, *, slug: str = "") -> tuple[str, dict]:
    """Toglie le frasi vietate e ricontrolla. Senza quelle frasi il testo passa."""
    pulita = pulisci_html(pagina)
    esito = controlla_html(pulita, slug=slug)
    if esito["stato"] == BLOCK:
        pulita = pulisci_html(pulita)
        esito = controlla_html(pulita, slug=slug)
    if esito["stato"] == REVISE:
        esito = {**esito, "stato": PASS, "tipo": esito.get("tipo", []) + ["nessuna frase vietata"]}
    return pulita, esito


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


def autorizza(pagina: str, *, slug: str = "", identificativo: str = "") -> tuple[str, dict]:
    """Pulisce, ricontrolla e restituisce la pagina che può uscire."""
    try:
        pulita, esito = sistema(pagina, slug=slug)
    except Exception as exc:
        esito = {"stato": BLOCK, "errori": [f"controllo non disponibile: {exc}"], "tipo": ["verifica incompleta"]}
        registra(identificativo or slug or "bozza", pagina if isinstance(pagina, str) else "", esito)
        raise ContaminazioneBloccata(esito) from exc
    registra(identificativo or slug or "bozza", pulita, esito, correzione="frasi vietate rimosse" if pulita != pagina else "")
    if esito["stato"] != PASS:
        raise ContaminazioneBloccata(esito)
    return pulita, esito


class ContaminazioneBloccata(RuntimeError):
    def __init__(self, esito: dict):
        self.esito = esito
        super().__init__(f"{esito.get('stato')}: {'; '.join(esito.get('errori') or [])}")
