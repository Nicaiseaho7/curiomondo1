"""Verifica che la chiave OpenAI sia configurata e funzionante.

Questo controllo non stampa mai la chiave, né per intero né in parte: dice solo
se c'è, se è valida e cosa permette di fare. Va eseguito dove la chiave esiste
davvero, cioè nei workflow GitHub Actions.

Fa tre cose, in ordine di costo crescente:

1. verifica che il segreto arrivi al processo (costo zero);
2. elenca i modelli disponibili per l'account (costo zero, ma conferma che la
   chiave è valida e dice cosa possiamo davvero usare);
3. su richiesta, una generazione minima per provare l'intera catena
   (costo trascurabile, qualche millesimo).
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

API = "https://api.openai.com/v1"
TIMEOUT = 30

# Modelli che la pipeline userà. Il controllo dice quali sono davvero
# disponibili, così la configurazione non si basa su un'ipotesi.
TEXT_CANDIDATES = ("gpt-5", "gpt-4.1", "gpt-4o", "gpt-4o-mini", "gpt-4.1-mini")
IMAGE_CANDIDATES = ("gpt-image-1", "dall-e-3")


def _request(path: str, key: str, payload: dict | None = None, retries: int = 2) -> tuple[int, Any]:
    """Chiamata all'API con ritentativi. Non registra mai la chiave."""
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    delay = 2.0
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
        req.add_header("Authorization", f"Bearer {key}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")[:400]
            try:
                detail = json.loads(body).get("error", {}).get("message", "")
            except Exception:
                detail = body
            # 401/403 sono definitivi: insistere non serve.
            if exc.code in (401, 403, 404) or attempt == retries:
                return exc.code, {"error": detail}
        except Exception as exc:
            if attempt == retries:
                return 0, {"error": type(exc).__name__}
        time.sleep(delay)
        delay *= 2
    return 0, {"error": "sconosciuto"}


def check(prova_generazione: bool = False) -> dict:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    esito: dict[str, Any] = {"chiave_presente": bool(key)}

    if not key:
        esito["stato"] = "non_configurata"
        esito["come_risolvere"] = (
            "Aggiungi il segreto OPENAI_API_KEY in GitHub: Settings > Secrets and "
            "variables > Actions > New repository secret."
        )
        return esito

    # Lunghezza e prefisso servono solo a distinguere un incollaggio troncato da
    # una chiave intera. Nessun carattere della chiave viene mai mostrato.
    esito["lunghezza_plausibile"] = len(key) >= 40
    esito["formato_atteso"] = key.startswith("sk-")

    stato, corpo = _request("/models", key)
    if stato != 200:
        esito["stato"] = "chiave_rifiutata" if stato in (401, 403) else "errore_api"
        esito["codice_http"] = stato
        esito["dettaglio"] = corpo.get("error", "")
        return esito

    disponibili = sorted({m.get("id", "") for m in corpo.get("data", [])})
    esito["stato"] = "valida"
    esito["modelli_totali"] = len(disponibili)
    esito["modelli_testo_disponibili"] = [m for m in TEXT_CANDIDATES if m in disponibili]
    esito["modelli_immagine_disponibili"] = [m for m in IMAGE_CANDIDATES if m in disponibili]

    if not prova_generazione:
        return esito

    modello = next((m for m in TEXT_CANDIDATES if m in disponibili), None)
    if not modello:
        esito["generazione"] = "nessun_modello_testo_disponibile"
        return esito

    stato, corpo = _request("/chat/completions", key, {
        "model": modello,
        "messages": [{"role": "user", "content": "Rispondi solo con: ok"}],
        "max_completion_tokens": 16,
    })
    if stato == 200:
        scelte = corpo.get("choices", [])
        testo = (scelte[0].get("message", {}).get("content", "") if scelte else "").strip()
        uso = corpo.get("usage", {})
        esito["generazione"] = "riuscita"
        esito["modello_provato"] = modello
        esito["risposta"] = testo[:40]
        esito["token_usati"] = uso.get("total_tokens")
    else:
        esito["generazione"] = "fallita"
        esito["codice_http_generazione"] = stato
        esito["dettaglio_generazione"] = corpo.get("error", "")
    return esito


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verifica la chiave OpenAI senza mai mostrarla")
    parser.add_argument("--genera", action="store_true",
                        help="prova anche una generazione minima (costo trascurabile)")
    args = parser.parse_args(argv)

    esito = check(prova_generazione=args.genera)
    print(json.dumps(esito, ensure_ascii=False, indent=2))
    return 0 if esito.get("stato") == "valida" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
