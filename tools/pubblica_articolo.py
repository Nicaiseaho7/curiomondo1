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
import ast
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from automation.newsroom import editor, site  # noqa: E402
from automation.newsroom.openai_client import Client, OpenAIError  # noqa: E402
from automation.newsroom.publisher import (  # noqa: E402
    CAPTION,
    _save_variants,
    _validate_image,
    _validate_visual_report,
)

AGENTE = "CurioMondoNewsroom/1.0 (+https://curiomondo.it)"


def carica_bozza(percorso: str) -> dict[str, Any]:
    testo = sys.stdin.read() if percorso == "-" else Path(percorso).read_text(encoding="utf-8")
    try:
        dati = json.loads(testo)
    except json.JSONDecodeError as errore:
        raise SystemExit(f"La bozza non e JSON valido: {errore}")
    return dati.get("articolo", dati) if isinstance(dati, dict) else dati


def prepara(articolo: dict[str, Any]) -> dict[str, Any]:
    articolo.setdefault("formato", "standard")
    articolo.setdefault("luogo", "")
    if not articolo.get("slug"):
        articolo["slug"] = editor.slugify(str(articolo.get("titolo", "")))
    categoria = str(articolo.get("categoria", "")).strip()
    if categoria.lower() == "film e serie tv":
        articolo["categoria"] = "Film e serie TV"
    else:
        categoria = categoria.capitalize()
        articolo["categoria"] = categoria if categoria in editor.CATEGORIE else "Mondo"
    return articolo


def scarica_immagine(origine: str) -> bytes:
    if origine.startswith("http"):
        richiesta = urllib.request.Request(origine, headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(richiesta, timeout=60) as risposta:
            return risposta.read(20_000_000)
    return Path(origine).read_bytes()


def genera_immagine(prompt: str) -> tuple[bytes, str]:
    client = Client(timeout=300, retries=2)
    if not client.available:
        raise OpenAIError("OPENAI_API_KEY non configurata per la generazione dell'immagine")
    raw, _ = client.generate_image("gpt-image-1", prompt, size="1536x1024", quality="high")
    report, _ = client.inspect_image("gpt-4o", raw, prompt)
    _validate_visual_report(report)
    return raw, "OpenAI gpt-image-1"


# I tre controlli che devono passare prima che il sito cambi. Sono gli stessi
# che per un giorno hanno vissuto dentro il build di Netlify, bloccando ogni
# deploy quando la loro macchina si rompeva: qui fermano l'articolo sbagliato
# invece dell'intero sito, ed e il posto giusto per loro.
GATE = (
    ("integrita del repository", "tools/repository_integrity_gate.py"),
    ("qualita AdSense", "tools/adsense_deploy_gate.py"),
    ("gate del sito", "tools/predeploy.py"),
)


def errori_del_gate() -> list[str]:
    """Errori che i controlli segnalano sul sito cosi com'e adesso."""
    trovati: list[str] = []
    for nome, strumento in GATE:
        esito = subprocess.run([sys.executable, strumento], cwd=ROOT,
                               capture_output=True, text=True)
        # Non tutti gli strumenti stampano JSON: adsense_deploy_gate.py stampa un
        # dizionario Python. Si accettano entrambe le forme.
        try:
            dati = json.loads(esito.stdout)
        except Exception:
            try:
                dati = ast.literal_eval(esito.stdout.strip())
                if not isinstance(dati, dict):
                    raise ValueError
            except Exception:
                trovati.append(f"{nome}: esito non interpretabile "
                               + (esito.stderr or esito.stdout)[-200:])
                continue
        trovati.extend(f"{nome}: {e}" for e in dati.get("errors", []))
        if esito.returncode != 0 and not dati.get("errors"):
            trovati.append(f"{nome}: fallito senza spiegazione (codice {esito.returncode})")
    return trovati


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
                        help="file o indirizzo dell'immagine; se manca si usa immagine.url o si genera da immagine.prompt")
    parser.add_argument("--alt", default="", help="descrizione dell'immagine per chi non la vede")
    parser.add_argument("--non-in-evidenza", action="store_true",
                        help="non mettere l'articolo nella card principale della home")
    args = parser.parse_args(argv)

    errori_preesistenti = set(errori_del_gate())
    articolo = prepara(carica_bozza(args.file))

    immagine_bozza = articolo.get("immagine") or {}
    alt = (args.alt or immagine_bozza.get("alt") or "").strip()
    prompt = str(immagine_bozza.get("prompt") or "").strip()
    origine = args.immagine or str(immagine_bozza.get("url") or "").strip()
    public = bool(immagine_bozza.get("personaggio_pubblico"))
    sensitive = bool(immagine_bozza.get("contesto_sensibile"))

    if not alt:
        print("Manca la descrizione dell'immagine: usa --alt oppure il campo immagine.alt.",
              file=sys.stderr)
        return 1
    if not origine and not prompt:
        print("Manca l'immagine: indica immagine.url con l'indirizzo di una figura gia pronta. "
              "La generazione automatica non e piu disponibile: il sito non usa piu chiavi a pagamento.",
              file=sys.stderr)
        return 1

    articolo["immagine"] = {
        "alt": alt,
        "url": origine,
        # Il controllo pretende un brief lungo perche serve al generatore
        # automatico. Quando l'immagine arriva gia pronta quel brief non esiste:
        # al suo posto resta scritto, per esteso, da dove viene la figura.
        "prompt": prompt or ("immagine fornita dalla redazione insieme alla bozza e non "
                             "generata automaticamente: il brief per il generatore non "
                             "serve in questo percorso manuale."),
        "personaggio_pubblico": public,
        "contesto_sensibile": sensitive,
    }

    problemi = editor.controlla_articolo(articolo)
    if problemi:
        print("La bozza non rispetta il protocollo editoriale:", file=sys.stderr)
        for p in problemi:
            print(f"  - {p}", file=sys.stderr)
        return 1

    try:
        if origine:
            raw = scarica_immagine(origine)
            generator = "fornita dalla redazione"
        else:
            raw, generator = genera_immagine(prompt)
        immagine_grezza = _validate_image(raw)
    except Exception as errore:
        print(f"NON PUBBLICATO: immagine non disponibile o non conforme: {errore}", file=sys.stderr)
        return 1

    versione = site._version()
    variants = _save_variants(immagine_grezza, f"{articolo['slug']}-v{versione}")
    immagine: dict[str, Any] = {
        "alt": alt,
        "variants": variants,
        "disclosure": CAPTION,
        "generator": generator,
        "sensitiveContext": sensitive,
    }
    if public:
        immagine["syntheticLikeness"] = "public-figure"

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
        for percorso in creati:
            percorso.unlink(missing_ok=True)
        subprocess.run(["git", "checkout", "--", "assets/data", "index.html", "notizie/index.html",
                        "feed.xml", "sitemap.xml", "news-sitemap.xml", "categorie",
                        "curiomondo-site-manifest.json"], cwd=ROOT)
        print(f"NON PUBBLICATO: {errore}", file=sys.stderr)
        return 1

    if errori_preesistenti:
        print("Attenzione: il sito aveva gia questi problemi, non introdotti da questo articolo:",
              file=sys.stderr)
        for errore in sorted(errori_preesistenti):
            print(f"  - {errore}", file=sys.stderr)

    print(json.dumps({"status": "pronto", "slug": slug,
                      "url": f"https://curiomondo.it/notizie/{slug}.html",
                      "in_evidenza": not args.non_in_evidenza}, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
