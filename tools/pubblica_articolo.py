"""Pubblica un articolo scritto altrove — per esempio con ChatGPT.

La redazione automatica scrive da sola, ma a volte l'articolo lo scrivi tu: qui
il testo entra dalla porta principale, non da una scorciatoia. Passa dagli
stessi controlli della redazione (protocollo editoriale, due testate distinte,
tre dati per la card) e dallo stesso gate che decide se il sito puo cambiare.
Se un controllo fallisce, non viene pubblicato niente e il sito resta com'era.

    python3 tools/pubblica_articolo.py --file bozza.json --immagine foto.jpg

Il formato della bozza e descritto in automation/prompts/chatgpt-nuovo-articolo.md,
che e anche il testo da dare a ChatGPT perche produca un JSON valido.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from automation.newsroom import editor, site  # noqa: E402
from automation.newsroom.publisher import CAPTION, _save_variants, _validate_image  # noqa: E402

AGENTE = "CurioMondoNewsroom/1.0 (+https://curiomondo.it)"


def carica_bozza(percorso: str) -> dict[str, Any]:
    testo = sys.stdin.read() if percorso == "-" else Path(percorso).read_text(encoding="utf-8")
    try:
        dati = json.loads(testo)
    except json.JSONDecodeError as errore:
        raise SystemExit(f"La bozza non e JSON valido: {errore}")
    # ChatGPT a volte incarta la risposta in un oggetto: accettiamo entrambe le forme.
    return dati.get("articolo", dati) if isinstance(dati, dict) else dati


def prepara(articolo: dict[str, Any]) -> dict[str, Any]:
    articolo.setdefault("formato", "standard")
    articolo.setdefault("luogo", "")
    if not articolo.get("slug"):
        articolo["slug"] = editor.slugify(str(articolo.get("titolo", "")))
    categoria = str(articolo.get("categoria", "")).strip().capitalize()
    articolo["categoria"] = categoria if categoria in editor.CATEGORIE else "Mondo"
    return articolo


def scarica_immagine(origine: str) -> bytes:
    if origine.startswith("http"):
        richiesta = urllib.request.Request(origine, headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(richiesta, timeout=60) as risposta:
            return risposta.read(20_000_000)
    return Path(origine).read_bytes()


def errori_del_gate() -> list[str]:
    """Errori che il gate segnala sul sito cosi com'e adesso."""
    esito = subprocess.run([sys.executable, "tools/predeploy.py"], cwd=ROOT,
                           capture_output=True, text=True)
    try:
        return list(json.loads(esito.stdout).get("errors", []))
    except Exception:
        return ["gate non interpretabile: " + (esito.stderr or esito.stdout)[-300:]]


def in_evidenza_attuale() -> str:
    """Quale articolo occupa oggi la card principale della home."""
    from lxml import html
    pagina = html.parse(str(ROOT / "index.html"))
    trovati = pagina.xpath('//*[contains(@class,"featured")]//a/@href')
    return str(trovati[0]) if trovati else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pubblica un articolo scritto a mano")
    parser.add_argument("--file", required=True, help="bozza JSON, oppure - per leggerla da stdin")
    parser.add_argument("--immagine", default="",
                        help="file o indirizzo dell'immagine; se manca si usa immagine.url della bozza")
    parser.add_argument("--alt", default="", help="descrizione dell'immagine per chi non la vede")
    parser.add_argument("--non-in-evidenza", action="store_true",
                        help="non mettere l'articolo nella card principale della home")
    args = parser.parse_args(argv)

    # Fotografia del gate prima di toccare il sito: un rosso che c'era gia — per
    # esempio la Domanda del giorno non aggiornata — non e colpa di questo
    # articolo e non deve impedirti di pubblicarlo. Cio che conta e non
    # aggiungerne di nuovi.
    errori_preesistenti = set(errori_del_gate())

    articolo = prepara(carica_bozza(args.file))

    # Il controllo pretende anche il brief per il generatore di immagini, che
    # qui non serve: l'immagine la porti tu. Al suo posto resta l'obbligo vero,
    # cioe la descrizione per chi la pagina non la vede.
    immagine_bozza = articolo.get("immagine") or {}
    alt = (args.alt or immagine_bozza.get("alt") or "").strip()
    if not alt:
        print("Manca la descrizione dell'immagine: usa --alt oppure il campo immagine.alt.",
              file=sys.stderr)
        return 1
    articolo["immagine"] = {"alt": alt, "url": str(immagine_bozza.get("url", "")),
                            "prompt": "immagine fornita dalla redazione, non generata: "
                                      "il brief non serve per questo percorso manuale."}

    problemi = editor.controlla_articolo(articolo)
    if problemi:
        print("La bozza non rispetta il protocollo editoriale:", file=sys.stderr)
        for p in problemi:
            print(f"  - {p}", file=sys.stderr)
        return 1

    origine = args.immagine or str(articolo.get("immagine", {}).get("url", "")).strip()
    if not origine:
        print("Manca l'immagine: indicala con --immagine oppure nel campo immagine.url.",
              file=sys.stderr)
        return 1
    immagine_grezza = _validate_image(scarica_immagine(origine))

    versione = site._version()
    variants = _save_variants(immagine_grezza, f"{articolo['slug']}-v{versione}")
    immagine = {"alt": alt, "variants": variants, "disclosure": CAPTION,
                "generator": "fornita dalla redazione"}

    creati: list[Path] = [ROOT / v["src"].lstrip("/") for v in variants]
    try:
        slug = site.write_article(articolo, immagine, versione)
        creati.append(ROOT / "notizie" / f"{slug}.html")
        site.register_image(immagine, slug, versione)
        in_evidenza = f"/notizie/{slug}.html" if not args.non_in_evidenza else in_evidenza_attuale()
        site.sync_surfaces([articolo], in_evidenza, versione)

        nuovi = [e for e in errori_del_gate() if e not in errori_preesistenti]
        if nuovi:
            for errore in nuovi:
                print(f"  gate: {errore}", file=sys.stderr)
            raise RuntimeError("il gate ha rifiutato l'articolo")
    except Exception as errore:
        # Fail-closed: nessuna pubblicazione a meta. Si torna allo stato di prima.
        for percorso in creati:
            percorso.unlink(missing_ok=True)
        subprocess.run(["git", "checkout", "--", "assets/data", "index.html", "notizie/index.html",
                        "feed.xml", "sitemap.xml", "news-sitemap.xml", "categorie",
                        "curiomondo-site-manifest.json"], cwd=ROOT)
        print(f"NON PUBBLICATO: {errore}", file=sys.stderr)
        return 1

    if errori_preesistenti:
        print("Attenzione: il sito aveva gia questi problemi, non introdotti da questo "
              "articolo:", file=sys.stderr)
        for errore in sorted(errori_preesistenti):
            print(f"  - {errore}", file=sys.stderr)

    print(json.dumps({"status": "pronto", "slug": slug,
                      "url": f"https://curiomondo.it/notizie/{slug}.html",
                      "in_evidenza": not args.non_in_evidenza}, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
