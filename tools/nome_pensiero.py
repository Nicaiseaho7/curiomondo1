"""Assegna il pensiero con il nome sulle notizie.

Il catalogo è i 3.000 nomi propri più usati in Italia, in assets/data/nomi-italiani.json.
Ogni notizia nuova prende il primo nome non ancora usato. Si ricomincia solo
quando l'elenco è esaurito, mai prima di 40 notizie.
"""
from __future__ import annotations

from html import escape
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets/data/nomi-italiani.json"
NAME_RE = re.compile(r'cm-name-note__name">([^<]+)')
TEXT_RE = re.compile(r'cm-name-note__text">([^<]+)')

S1 = [
    "Continua a credere in quello che stai costruendo.",
    "Non mollare proprio adesso.",
    "Quello che fai ha un valore, anche quando non si vede.",
    "Abbi fiducia nel passo che stai per fare.",
    "Sei più forte di quanto ti sembri oggi.",
    "C’è spazio anche per te e per ciò che desideri.",
    "Il tuo impegno di oggi non va perso.",
    "Tieniti vicino a chi ti fa stare bene.",
    "Va bene andare piano, se continui a camminare.",
    "Ciò che sogni merita ancora la tua cura.",
    "Non giudicarti solo dai giorni stanchi.",
    "Dentro di te c’è già una forza tranquilla.",
    "Il futuro può essere più gentile di quanto temi.",
    "Resta fedele a ciò che senti vero.",
    "Anche una giornata ordinaria può spostare qualcosa.",
    "Non sei in ritardo sulla tua vita.",
    "Chiedere aiuto non ti rende meno capace.",
    "Una speranza piccola resta comunque dalla tua parte.",
    "Il cuore sa quando una cosa vale la pena.",
    "Continua a scegliere te, con calma.",
    "Ciò che costruisci in silenzio un giorno si vedrà.",
    "Un momento difficile non è tutta la tua storia.",
    "Ti è permesso ricominciare senza spiegazioni.",
    "La costanza che hai già avuto conta davvero.",
    "C’è amore anche nelle cose che fai con cura.",
    "Il tuo domani non è già scritto.",
    "Respira: stai facendo abbastanza.",
    "I sogni non scadono solo perché il tempo passa.",
    "Qualcuno crede in te più di quanto immagini.",
    "La felicità può arrivare anche in un dettaglio.",
    "Non spegnere la luce che porti agli altri.",
    "Ogni volta che insisti, qualcosa si sta già muovendo.",
    "Meriti una vita che ti somigli.",
    "La pazienza che hai avuto fin qui è coraggio.",
    "Oggi puoi essere gentile con te.",
    "Quello che impari adesso ti servirà più avanti.",
    "Non lasciare a metà una cosa che ti accende.",
    "Sei qui per un motivo buono.",
    "Tieni vivo ciò che ti fa sentire vivo.",
    "Anche oggi hai il diritto di sperare.",
]
S2 = [
    "Anche i passi piccoli possono portarti lontano.",
    "Un giorno ti ringrazierai per avere continuato.",
    "Resta: il meglio ha ancora bisogno di te.",
    "Continua, con la tua misura.",
    "Non tutto deve riuscire subito per essere giusto.",
    "La strada si fa mentre la percorri.",
    "Tieniti questo pensiero vicino.",
    "Sei sulla via, anche se oggi non la vedi.",
    "Datti il tempo che daresti a chi ami.",
    "Ciò che semini con cura torna, a modo suo.",
    "In quello che stai attraversando non cammini in solitudine.",
    "La prossima pagina può essere più luminosa.",
    "Fidati ancora un poco di te.",
    "Il tuo passo, anche lento, è comunque avanti.",
    "Conserva la speranza: è già una direzione.",
    "C’è ancora bellezza da incontrare.",
    "Lascia che il domani ti sorprenda.",
    "La tua storia non si ferma qui.",
    "Porta con te solo ciò che ti fa crescere.",
    "Un gesto buono verso di te cambia la giornata.",
    "Il futuro si avvicina anche quando sembra fermo.",
    "Resta aperto a quello che puoi diventare.",
    "La luce che cerchi può partire da te.",
    "Non rinunciare a ciò che ti accende.",
    "Oggi basta un passo onesto.",
    "Puoi sperare ancora.",
    "Ciò che resisti a lasciare andare ti sta formando.",
    "Tieni il cuore aperto: può arrivare qualcosa di buono.",
]


def catalog() -> list[str]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


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
    # Elenco esaurito: il primo che non compare nelle ultime 40 notizie.
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
    raise RuntimeError("nessun nome disponibile nel catalogo italiano")


def next_message(root: Path | None = None) -> str:
    root = root or ROOT
    _, taken = used(root)
    pairs = [f"{a} {b}" for a in S1 for b in S2]
    random.Random(len(taken) + 30).shuffle(pairs)
    for message in pairs:
        if message not in taken:
            return message
    raise RuntimeError("nessuna frase nuova disponibile")


def note_markup(root: Path | None = None) -> str:
    name = next_name(root)
    message = next_message(root)
    return (
        '<p class="cm-name-note"><strong class="cm-name-note__name">'
        + escape(name)
        + '</strong><span class="cm-name-note__text">'
        + escape(message)
        + "</span></p>"
    )
