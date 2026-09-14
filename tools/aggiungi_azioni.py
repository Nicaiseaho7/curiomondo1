"""Rimette ascolto, condivisione e salvataggio negli articoli che ne sono privi.

I tre pulsanti sotto la firma — ascolta l'audio, condividi, salva — fanno parte
dell'articolo CurioMondo da sempre, ma il renderer della redazione automatica
non li scriveva: le pagine prodotte da li sono uscite senza. Questo strumento
li reinserisce dove mancano, subito dopo la firma, che e il posto che occupano
in tutte le altre pagine.

E ripetibile senza danni: un articolo che li ha gia viene saltato.

    python3 tools/aggiungi_azioni.py [--elenca]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AZIONI = (
    '<div class="actions">'
    '<button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button>'
    '<button type="button" data-share-article>↗ Condividi</button>'
    '<button id="cmSaveBtn" type="button">★ Salva</button>'
    '</div>'
)

# La firma chiude sempre con </p>: i pulsanti vanno subito dopo, prima della foto.
FIRMA = re.compile(r'(<p class="cm-article-byline">.*?</p>)', re.S)


def sistema(percorso: Path) -> str:
    testo = percorso.read_text(encoding="utf-8")
    if 'class="actions"' in testo:
        return "gia_presente"
    if "curiomondo-article-v210.js" not in testo:
        # Senza il controller i pulsanti sarebbero decorativi: meglio non metterli.
        return "senza_controller"
    nuovo, quante = FIRMA.subn(lambda m: m.group(1) + AZIONI, testo, count=1)
    if not quante:
        return "firma_non_trovata"
    percorso.write_text(nuovo, encoding="utf-8")
    return "aggiunto"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reinserisce i pulsanti negli articoli")
    parser.add_argument("--elenca", action="store_true", help="mostra solo cosa farebbe")
    args = parser.parse_args(argv)

    esiti: dict[str, list[str]] = {}
    for percorso in sorted((ROOT / "notizie").glob("*.html")):
        if percorso.name == "index.html":
            continue
        if args.elenca:
            stato = "gia_presente" if 'class="actions"' in percorso.read_text(encoding="utf-8") else "da_sistemare"
        else:
            stato = sistema(percorso)
        esiti.setdefault(stato, []).append(percorso.name)

    for stato, elenco in sorted(esiti.items()):
        print(f"{stato}: {len(elenco)}")
        if stato not in ("gia_presente", "aggiunto"):
            for nome in elenco:
                print(f"  - {nome}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
