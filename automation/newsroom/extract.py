"""Recupero del testo reale di una notizia.

Il watcher conosce solo titolo e sommario: troppo poco per scrivere un
articolo. Chiedere a un modello di sviluppare 400 parole partendo da un titolo
significa invitarlo a inventare i dettagli. Qui si legge la pagina della fonte,
una sola volta per candidato, come farebbe un lettore.

Non è uno scraper aggressivo: una richiesta, un limite di dimensione, un
timeout, e nessun tentativo di aggirare blocchi. Se la fonte non si lascia
leggere, il candidato resta senza materiale e non verrà scritto.
"""
from __future__ import annotations

import gzip
import io
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from lxml import html as LH

from . import googlenews

USER_AGENT = "CurioMondoNewsroom/1.0 (+https://curiomondo.it; redazione automatica)"
MAX_BYTES = 2_000_000
TIMEOUT = 20

# Contenitori dove di norma vive il testo dell'articolo, dal più specifico.
CANDIDATE_XPATHS = (
    '//article',
    '//*[@itemprop="articleBody"]',
    '//*[contains(@class,"article-body")]',
    '//*[contains(@class,"articleBody")]',
    '//*[contains(@class,"story-body")]',
    '//*[contains(@class,"entry-content")]',
    '//*[contains(@class,"post-content")]',
    '//main',
)

DROP_TAGS = ('script', 'style', 'noscript', 'nav', 'header', 'footer', 'aside', 'form', 'figure')


# Domini che compaiono in ogni pagina e non sono mai una fonte della notizia.
RUMORE = (
    "facebook.com", "twitter.com", "x.com", "instagram.com", "linkedin.com",
    "whatsapp.com", "youtube.com", "google.com", "apple.com", "telegram",
    "pinterest.com", "reddit.com", "tiktok.com", "amazon.", "/cdn-cgi/",
)
# Domini di chi pubblica atti, dati e comunicati: sono le fonti che vale la
# pena citare accanto alla testata che ha dato la notizia.
ISTITUZIONALI = (
    ".gov", ".gov.it", ".europa.eu", ".int", "istat.it", "ecb.europa.eu",
    "who.int", "un.org", "nasa.gov", "esa.int", "ingv.it", "protezionecivile.it",
    "governo.it", "camera.it", "senato.it", "bancaditalia.it", "consob.it",
    "doi.org", "nature.com", "science.org", "arxiv.org", "pubmed",
)


@dataclass
class Extracted:
    url: str
    title: str
    text: str
    paragraphs: list[str]
    ok: bool
    reason: str = ""
    # Collegamenti a documenti ufficiali citati dentro l'articolo: sono fonti
    # vere, e spesso sono la differenza fra un pezzo con due fonti e una
    # riscrittura che cita due volte la stessa pagina.
    links: list[str] = field(default_factory=list)

    @property
    def words(self) -> int:
        return len(re.findall(r"\w+", self.text))


def _fetch(url: str, timeout: int = TIMEOUT) -> tuple[bytes, str]:
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    request.add_header("Accept", "text/html,application/xhtml+xml")
    request.add_header("Accept-Language", "it-IT,it;q=0.9,en;q=0.8")
    request.add_header("Accept-Encoding", "gzip")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(MAX_BYTES)
        if response.headers.get("Content-Encoding") == "gzip":
            try:
                raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read(MAX_BYTES)
            except OSError:
                pass
        return raw, response.geturl()


def _collegamenti_utili(node, origine: str) -> list[str]:
    """Estrae dal corpo dell'articolo i link a documenti ufficiali."""
    dominio = origine.split("/")[2] if "//" in origine else ""
    trovati: list[str] = []
    for href in node.xpath('.//a/@href'):
        indirizzo = str(href).split("#")[0].strip()
        if not indirizzo.startswith("http"):
            continue
        if dominio and dominio in indirizzo:
            continue
        if any(r in indirizzo for r in RUMORE):
            continue
        if not any(i in indirizzo for i in ISTITUZIONALI):
            continue
        if indirizzo not in trovati:
            trovati.append(indirizzo)
    return trovati[:4]


def _clean_paragraphs(node) -> list[str]:
    for tag in DROP_TAGS:
        for bad in node.xpath(f'.//{tag}'):
            parent = bad.getparent()
            if parent is not None:
                parent.remove(bad)
    paragrafi = []
    for p in node.xpath('.//p'):
        testo = re.sub(r'\s+', ' ', ' '.join(p.itertext())).strip()
        # I paragrafi brevissimi sono didascalie, crediti o inviti al consenso.
        if len(testo) >= 60:
            paragrafi.append(testo)
    return paragrafi


def extract(url: str, timeout: int = TIMEOUT, min_words: int = 120) -> Extracted:
    """Scarica una notizia e ne estrae il testo principale.

    I feed di Google News non puntano all'articolo ma a un rimando opaco: va
    sciolto prima, altrimenti si legge una pagina vuota e la notizia viene
    scartata per un difetto nostro, non della fonte.
    """
    if googlenews.e_google_news(url):
        risoluzione = googlenews.risolvi(url, timeout=timeout)
        if not risoluzione.risolto:
            return Extracted(url, "", "", [], False,
                             f"google_news_non_risolto:{risoluzione.motivo or 'ignoto'}")
        url = risoluzione.url

    try:
        raw, final_url = _fetch(url, timeout=timeout)
    except urllib.error.HTTPError as exc:
        return Extracted(url, "", "", [], False, f"http_{exc.code}")
    except Exception as exc:
        return Extracted(url, "", "", [], False, type(exc).__name__)

    try:
        doc = LH.fromstring(raw)
    except Exception:
        return Extracted(url, "", "", [], False, "html_non_valido")

    titolo = ""
    for xp in ('//meta[@property="og:title"]/@content', '//h1//text()', '//title/text()'):
        valori = doc.xpath(xp)
        if valori:
            titolo = re.sub(r'\s+', ' ', str(valori[0])).strip()
            if titolo:
                break

    migliore: list[str] = []
    collegamenti: list[str] = []
    for xp in CANDIDATE_XPATHS:
        for nodo in doc.xpath(xp):
            trovati = _collegamenti_utili(nodo, url)
            paragrafi = _clean_paragraphs(nodo)
            if len(' '.join(paragrafi)) > len(' '.join(migliore)):
                migliore, collegamenti = paragrafi, trovati
        if len(re.findall(r"\w+", ' '.join(migliore))) >= min_words:
            break

    if not migliore:
        migliore = _clean_paragraphs(doc)

    testo = '\n\n'.join(migliore)
    parole = len(re.findall(r"\w+", testo))
    if parole < min_words:
        return Extracted(final_url, titolo, testo, migliore, False, f"testo_insufficiente_{parole}")
    return Extracted(final_url, titolo, testo, migliore, True, links=collegamenti)


def gather(urls: list[str], limit: int = 3, timeout: int = TIMEOUT) -> list[Extracted]:
    """Legge il materiale di più fonti sullo stesso fatto.

    Più fonti indipendenti significano sia più contesto per scrivere sia, e
    soprattutto, la possibilità di verificare che raccontino la stessa cosa.
    """
    risultati = []
    for url in urls[:limit]:
        esito = extract(url, timeout=timeout)
        risultati.append(esito)
    return risultati
