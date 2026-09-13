"""Risoluzione dei link di Google News verso l'articolo vero.

Ventitré delle quarantaquattro fonti passano da Google News, perché molte
testate non espongono un feed raggiungibile da un runner. Il link che Google
mette nel feed però non è quello dell'articolo: è un rimando opaco
(``news.google.com/rss/articles/CBMi...``) che si apre solo con JavaScript.
Chi prova a leggerlo con una richiesta semplice riceve una pagina vuota — ed è
esattamente il motivo per cui la prima prova editoriale ha scartato quasi tutti
i candidati con "fonti_non_leggibili".

Qui il rimando viene sciolto, con tre tentativi in ordine di costo:

1. l'identificativo contiene l'URL in chiaro (vecchio formato): nessuna rete;
2. la richiesta viene reindirizzata dal server verso la testata;
3. la pagina espone firma e marca temporale, e si chiede a Google lo stesso
   scioglimento che farebbe il browser.

Nessuno dei tre aggira una protezione: sono le strade che Google stessa
percorre. Se falliscono tutti, il candidato resta senza materiale e non verrà
scritto — meglio un silenzio motivato di un articolo scritto a memoria.
"""
from __future__ import annotations

import base64
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass

USER_AGENT = "Mozilla/5.0 (compatible; CurioMondoNewsroom/1.0; +https://curiomondo.it)"
BATCH_URL = "https://news.google.com/_/DotsSplashUi/data/batchexecute"

E_UN_LINK_GOOGLE = re.compile(r"^https?://news\.google\.com/(?:rss/)?(?:articles|read)/", re.I)
_IDENTIFICATIVO = re.compile(r"/(?:articles|read)/([^?/#]+)")
_URL_IN_CHIARO = re.compile(rb"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]{12,}")
_FIRMA = re.compile(r'data-n-a-sg="([^"]+)"')
_MARCA = re.compile(r'data-n-a-ts="(\d+)"')
_RISPOSTA = re.compile(r'garturlres\\?",\\?"(http[^\\"]+)')

# Domini che compaiono nella pagina di Google ma non sono mai l'articolo.
_NON_ARTICOLI = ("google.com", "gstatic.com", "googleapis.com", "youtube.com", "policies.google")


@dataclass
class Risoluzione:
    url: str
    metodo: str = ""
    motivo: str = ""

    @property
    def risolto(self) -> bool:
        return bool(self.url) and not E_UN_LINK_GOOGLE.match(self.url)


def e_google_news(url: str) -> bool:
    return bool(E_UN_LINK_GOOGLE.match(url or ""))


def identificativo(url: str) -> str:
    trovato = _IDENTIFICATIVO.search(url or "")
    return trovato.group(1) if trovato else ""


def _pulisci(candidato: str) -> str:
    """Toglie la coda di byte che il protobuf lascia attaccata all'URL."""
    url = candidato.split("\\")[0].strip()
    # Il blob termina spesso con separatori che non appartengono all'indirizzo.
    while url and url[-1] in "?&=.,;:'\"":
        url = url[:-1]
    return url


def da_identificativo(url: str) -> str:
    """Vecchio formato: l'URL è dentro l'identificativo, in base64."""
    ident = identificativo(url)
    if not ident:
        return ""
    grezzo = ident + "=" * (-len(ident) % 4)
    try:
        blob = base64.urlsafe_b64decode(grezzo)
    except Exception:
        return ""
    trovato = _URL_IN_CHIARO.search(blob)
    if not trovato:
        return ""
    indirizzo = _pulisci(trovato.group(0).decode("utf-8", "ignore"))
    if E_UN_LINK_GOOGLE.match(indirizzo):
        return ""
    return indirizzo


def _scarica(url: str, timeout: int) -> tuple[str, str]:
    richiesta = urllib.request.Request(url)
    richiesta.add_header("User-Agent", USER_AGENT)
    richiesta.add_header("Accept", "text/html,application/xhtml+xml")
    with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
        return risposta.read(1_500_000).decode("utf-8", "replace"), risposta.geturl()


def _da_batchexecute(ident: str, firma: str, marca: str, timeout: int) -> str:
    """Chiede a Google lo stesso scioglimento che fa la pagina nel browser."""
    richiesta_interna = json.dumps([
        "garturlreq",
        [["X", "X", ["X", "X"], None, None, 1, 1, "IT:it", None, 1, None, None, None, None, None, 0, 1],
         "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0],
        ident, int(marca), firma,
    ])
    corpo = urllib.parse.urlencode({
        "f.req": json.dumps([[["Fbv4je", richiesta_interna, None, "generic"]]])
    }).encode()
    richiesta = urllib.request.Request(BATCH_URL, data=corpo, method="POST")
    richiesta.add_header("User-Agent", USER_AGENT)
    richiesta.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
        testo = risposta.read(400_000).decode("utf-8", "replace")
    trovato = _RISPOSTA.search(testo)
    return _pulisci(trovato.group(1)) if trovato else ""


def risolvi(url: str, timeout: int = 15) -> Risoluzione:
    """Restituisce l'indirizzo dell'articolo vero dietro un link di Google News."""
    if not e_google_news(url):
        return Risoluzione(url, "diretto")

    indirizzo = da_identificativo(url)
    if indirizzo:
        return Risoluzione(indirizzo, "identificativo")

    try:
        pagina, finale = _scarica(url, timeout)
    except Exception as errore:
        return Risoluzione("", "", f"pagina_non_letta:{type(errore).__name__}")

    if not E_UN_LINK_GOOGLE.match(finale):
        return Risoluzione(finale, "reindirizzamento")

    firma, marca = _FIRMA.search(pagina), _MARCA.search(pagina)
    if not (firma and marca):
        # Utile alla diagnosi: dice se Google ha cambiato ancora la pagina.
        esterni = [u for u in re.findall(r'href="(https?://[^"]+)"', pagina)
                   if not any(d in u for d in _NON_ARTICOLI)]
        if esterni:
            return Risoluzione(esterni[0], "collegamento_in_pagina")
        return Risoluzione("", "", "firma_assente")

    try:
        indirizzo = _da_batchexecute(identificativo(url), firma.group(1), marca.group(1), timeout)
    except Exception as errore:
        return Risoluzione("", "", f"batchexecute_fallito:{type(errore).__name__}")
    if indirizzo:
        return Risoluzione(indirizzo, "batchexecute")
    return Risoluzione("", "", "batchexecute_senza_url")
