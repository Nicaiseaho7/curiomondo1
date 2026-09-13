"""Controllo del sito pubblico: risponde davvero, e risponde bene?

Il protocollo dice che una notizia non e pubblicata perche esiste un commit, ma
perche e raggiungibile sul dominio. Questo strumento applica la stessa idea al
sito intero: interroga curiomondo.it come farebbe un lettore e verifica le
pagine che contano — home, mappe del sito, ultime notizie — riportando codice
HTTP, peso e i requisiti che Google guarda.
"""
from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SITO = "https://curiomondo.it"
AGENTE = "CurioMondoNewsroom/1.0 (+https://curiomondo.it; controllo interno)"


def leggi(url: str, timeout: int = 25) -> tuple[int, bytes]:
    richiesta = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
            return int(risposta.status), risposta.read(3_000_000)
    except urllib.error.HTTPError as errore:
        return int(errore.code), b""
    except Exception:
        return 0, b""


def ultime_notizie(corpo: bytes, quante: int) -> list[str]:
    """Ricava dalla mappa delle notizie gli ultimi articoli pubblicati."""
    indirizzi = re.findall(rb"<loc>\s*([^<\s]+)\s*</loc>", corpo)
    puliti = [u.decode("utf-8", "ignore") for u in indirizzi]
    return [u for u in puliti if "/notizie/" in u][-quante:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Il sito pubblico risponde?")
    parser.add_argument("--articoli", type=int, default=5)
    args = parser.parse_args(argv)

    fisse = [
        f"{SITO}/", f"{SITO}/sitemap.xml", f"{SITO}/news-sitemap.xml",
        f"{SITO}/robots.txt", f"{SITO}/feed.xml",
    ]
    with ThreadPoolExecutor(max_workers=5) as pool:
        esiti = dict(zip(fisse, pool.map(leggi, fisse)))

    stato_news, corpo_news = esiti[f"{SITO}/news-sitemap.xml"]
    articoli = ultime_notizie(corpo_news, args.articoli) if stato_news == 200 else []
    with ThreadPoolExecutor(max_workers=5) as pool:
        esiti_articoli = list(pool.map(leggi, articoli))

    print("## Sito pubblico\n")
    print("| pagina | http | peso |")
    print("|---|---|---|")
    for url, (stato, corpo) in esiti.items():
        print(f"| {url.replace(SITO, '') or '/'} | {stato or 'irraggiungibile'} | {len(corpo)} |")
    for url, (stato, corpo) in zip(articoli, esiti_articoli):
        print(f"| {url.replace(SITO, '')} | {stato} | {len(corpo)} |")

    home_stato, home = esiti[f"{SITO}/"]
    if home_stato == 200:
        requisiti = {
            "titolo": b"<title",
            "canonical": b'rel="canonical"',
            "dati strutturati": b"application/ld+json",
            "adsense": b"pagead2.googlesyndication.com",
        }
        print("\n**Home:**")
        for nome, impronta in requisiti.items():
            print(f"- {nome}: " + ("sì" if impronta in home else "NO"))

    guasti = [u for u, (s, _) in esiti.items() if s != 200]
    guasti += [u for u, (s, _) in zip(articoli, esiti_articoli) if s != 200]
    print("\n**Pagine non a posto:** " + (", ".join(guasti) if guasti else "nessuna"))
    return 1 if guasti else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
