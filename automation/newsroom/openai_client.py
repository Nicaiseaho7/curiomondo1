"""Accesso al modello con timeout, ritentativi e un tetto di spesa vero.

Un'automazione che chiama un modello a pagamento senza limiti è un rischio
economico, non solo tecnico: un ciclo impazzito può bruciare un budget in
un'ora. Qui ogni chiamata viene contata e confrontata con un tetto persistente;
superata la soglia, il client si rifiuta di chiamare ancora.

La chiave viene letta solo dall'ambiente e non viene mai registrata.
"""
from __future__ import annotations

import json
import os
import time
import base64
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_BASE = "https://api.openai.com/v1"

# Prezzi indicativi per milione di token, usati solo per stimare la spesa e
# far scattare il tetto. Non devono essere esatti: servono a impedire fughe,
# non a fare contabilità. Vanno aggiornati se cambiano i listini.
PRICES_PER_MTOK = {
    "gpt-5":          {"in": 1.25, "out": 10.00},
    "gpt-4.1":        {"in": 2.00, "out": 8.00},
    "gpt-4o":         {"in": 2.50, "out": 10.00},
    "gpt-4.1-mini":   {"in": 0.40, "out": 1.60},
    "gpt-4o-mini":    {"in": 0.15, "out": 0.60},
}
FALLBACK_PRICE = {"in": 2.50, "out": 10.00}   # prudente: sovrastima, non sottostima
IMAGE_PRICE_EACH = 0.04                        # stima prudente per immagine generata

# Famiglie che ragionano prima di rispondere: i token di ragionamento vengono
# scalati dallo stesso tetto della risposta, quindi il tetto va dimensionato
# per entrambi e lo sforzo va dichiarato.
MODELLI_CHE_RAGIONANO = ("gpt-5", "o1", "o3", "o4")
TETTO_TOKEN_MASSIMO = 16000


def modello_ragiona(model: str) -> bool:
    return any(str(model).startswith(prefisso) for prefisso in MODELLI_CHE_RAGIONANO)


class BudgetExceeded(RuntimeError):
    """Il tetto di spesa configurato è stato raggiunto."""


class OpenAIError(RuntimeError):
    """Errore non recuperabile nel dialogo con l'API."""


@dataclass
class Usage:
    calls: int = 0
    seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    images: int = 0
    cost_usd: float = 0.0

    def add(self, other: "Usage") -> None:
        self.calls += other.calls
        self.seconds = round(self.seconds + other.seconds, 2)
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.images += other.images
        self.cost_usd = round(self.cost_usd + other.cost_usd, 6)

    def to_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "seconds": round(self.seconds, 2),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "images": self.images,
            "cost_usd": round(self.cost_usd, 4),
        }


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    price = PRICES_PER_MTOK.get(model, FALLBACK_PRICE)
    return (input_tokens * price["in"] + output_tokens * price["out"]) / 1_000_000


class BudgetGuard:
    """Tetto di spesa persistente, con soglia di allerta.

    Lo stato vive insieme a quello del watcher, quindi il conto non si azzera
    a ogni esecuzione: è quello che serve per accorgersi di una fuga lenta.
    """

    def __init__(self, state_dir: Path, daily_limit_usd: float = 5.0, alert_ratio: float = 0.8):
        self.path = Path(state_dir) / "budget.json"
        self.daily_limit = float(daily_limit_usd)
        self.alert_ratio = alert_ratio
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"days": {}}

    def _today(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    @property
    def spent_today(self) -> float:
        return float(self.data.get("days", {}).get(self._today(), {}).get("cost_usd", 0.0))

    def remaining(self) -> float:
        return max(0.0, self.daily_limit - self.spent_today)

    def check(self, expected_cost: float = 0.0) -> None:
        if self.spent_today + expected_cost > self.daily_limit:
            raise BudgetExceeded(
                f"tetto giornaliero raggiunto: spesi {self.spent_today:.3f} USD "
                f"su {self.daily_limit:.2f}"
            )

    def near_limit(self) -> bool:
        return self.spent_today >= self.daily_limit * self.alert_ratio

    def record(self, usage: Usage) -> None:
        day = self.data.setdefault("days", {}).setdefault(self._today(), {})
        day["cost_usd"] = round(float(day.get("cost_usd", 0.0)) + usage.cost_usd, 6)
        day["calls"] = int(day.get("calls", 0)) + usage.calls
        day["input_tokens"] = int(day.get("input_tokens", 0)) + usage.input_tokens
        day["output_tokens"] = int(day.get("output_tokens", 0)) + usage.output_tokens
        day["images"] = int(day.get("images", 0)) + usage.images
        # Conserva solo gli ultimi 30 giorni: serve la tendenza, non l'archivio.
        giorni = sorted(self.data["days"])
        for vecchio in giorni[:-30]:
            del self.data["days"][vecchio]
        self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


class Client:
    """Client minimale per le chiamate che servono alla redazione."""

    def __init__(
        self,
        budget: BudgetGuard | None = None,
        # Un modello che ragiona su 9000 token puo impiegare minuti: con un
        # timeout stretto si scartano risposte gia pagate e si ritenta a vuoto.
        timeout: int = 300,
        retries: int = 2,
        api_key: str | None = None,
    ):
        self.api_key = (api_key if api_key is not None else os.getenv("OPENAI_API_KEY", "")).strip()
        self.budget = budget
        self.timeout = timeout
        self.retries = retries
        self.usage = Usage()

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise OpenAIError("OPENAI_API_KEY non configurata")
        if self.budget is not None:
            self.budget.check()

        body = json.dumps(payload).encode()
        delay = 2.0
        ultimo = ""
        for tentativo in range(self.retries + 1):
            request = urllib.request.Request(f"{API_BASE}{path}", data=body, method="POST")
            request.add_header("Authorization", f"Bearer {self.api_key}")
            request.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as exc:
                testo = exc.read().decode(errors="replace")[:300]
                try:
                    ultimo = json.loads(testo).get("error", {}).get("message", testo)
                except Exception:
                    ultimo = testo
                # 4xx di configurazione: insistere non serve e costa tempo.
                if exc.code in (400, 401, 403, 404):
                    raise OpenAIError(f"http {exc.code}: {ultimo}") from None
                # 429 e 5xx sono transitori: vale la pena riprovare.
            except Exception as exc:
                ultimo = type(exc).__name__
            if tentativo < self.retries:
                time.sleep(delay)
                delay *= 2
        raise OpenAIError(f"chiamata non riuscita dopo {self.retries + 1} tentativi: {ultimo}")

    def complete_json(
        self,
        model: str,
        system: str,
        user: str,
        schema_hint: str = "",
        max_tokens: int = 2000,
        sforzo: str = "low",
    ) -> tuple[dict[str, Any], Usage]:
        """Chiede una risposta in JSON e la restituisce già interpretata.

        I modelli che ragionano consumano il tetto di token prima ancora di
        scrivere: se il tetto è stretto la risposta arriva vuota e troncata,
        pagata per intero. Per questo il ragionamento viene tenuto basso — qui
        serve un giudizio su materiale già fornito, non una dimostrazione — e
        un troncamento fa scattare un solo secondo tentativo più largo.
        """
        messaggio = user + (f"\n\n{schema_hint}" if schema_hint else "")
        tetto = max_tokens
        for tentativo in range(2):
            payload: dict[str, Any] = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": messaggio},
                ],
                "response_format": {"type": "json_object"},
                "max_completion_tokens": tetto,
            }
            if modello_ragiona(model):
                payload["reasoning_effort"] = sforzo
            avvio = time.monotonic()
            risposta = self._post("/chat/completions", payload)
            durata = round(time.monotonic() - avvio, 2)

            uso_api = risposta.get("usage", {})
            uso = Usage(
                calls=1,
                seconds=durata,
                input_tokens=int(uso_api.get("prompt_tokens", 0)),
                output_tokens=int(uso_api.get("completion_tokens", 0)),
            )
            uso.cost_usd = estimate_cost(model, uso.input_tokens, uso.output_tokens)
            self.usage.add(uso)
            if self.budget is not None:
                self.budget.record(uso)

            scelte = risposta.get("choices", [])
            if not scelte:
                raise OpenAIError("risposta senza contenuto")
            testo = scelte[0].get("message", {}).get("content", "") or ""

            if scelte[0].get("finish_reason") == "length" or not testo.strip():
                ragionamento = int(
                    uso_api.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
                )
                if tentativo == 0 and tetto < TETTO_TOKEN_MASSIMO:
                    tetto = min(tetto * 3, TETTO_TOKEN_MASSIMO)
                    continue
                raise OpenAIError(
                    f"risposta troncata a {tetto} token "
                    f"({ragionamento} spesi in ragionamento): accorciare il materiale"
                )

            try:
                return json.loads(testo), uso
            except json.JSONDecodeError as exc:
                raise OpenAIError(f"risposta non in JSON valido: {exc}") from None

        raise OpenAIError("risposta troncata due volte di seguito")

    def generate_image(
        self,
        model: str,
        prompt: str,
        size: str = "1536x1024",
        quality: str = "high",
    ) -> tuple[bytes, Usage]:
        """Genera un'immagine e restituisce i byte PNG senza scrivere segreti nei log."""
        if self.budget is not None:
            self.budget.check(IMAGE_PRICE_EACH)
        risposta = self._post("/images/generations", {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "output_format": "png",
            "n": 1,
        })
        immagini = risposta.get("data") or []
        encoded = immagini[0].get("b64_json", "") if immagini else ""
        if not encoded:
            raise OpenAIError("generazione immagine senza dati")
        try:
            payload = base64.b64decode(encoded, validate=True)
        except Exception as exc:
            raise OpenAIError("immagine restituita in formato non valido") from exc
        if len(payload) < 10_000:
            raise OpenAIError("immagine generata troppo piccola o corrotta")
        uso = Usage(calls=1, images=1, cost_usd=IMAGE_PRICE_EACH)
        self.usage.add(uso)
        if self.budget is not None:
            self.budget.record(uso)
        return payload, uso

    def inspect_image(
        self,
        model: str,
        image_bytes: bytes,
        brief: str,
    ) -> tuple[dict[str, Any], Usage]:
        """Applica un controllo visivo fail-closed prima della pubblicazione."""
        encoded = base64.b64encode(image_bytes).decode("ascii")
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Sei il controllo qualita visivo di una redazione. "
                            "Valuta soltanto l'immagine allegata rispetto al brief. "
                            "Rispondi in JSON con: approvata (boolean), fotorealistica "
                            "(boolean), coerente (boolean), testo_nei_pixel (boolean), "
                            "contenuto_sensibile_non_consentito (boolean), motivo (string). "
                            "Approva solo se e fotorealistica, coerente, senza testo, loghi "
                            "aggiunti o watermark e senza scene traumatiche inventate.\n\n"
                            f"Brief: {brief}"
                        ),
                    },
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{encoded}", "detail": "low"
                    }},
                ],
            }],
            "response_format": {"type": "json_object"},
            "max_completion_tokens": 500,
        }
        risposta = self._post("/chat/completions", payload)
        uso_api = risposta.get("usage", {})
        uso = Usage(
            calls=1,
            input_tokens=int(uso_api.get("prompt_tokens", 0)),
            output_tokens=int(uso_api.get("completion_tokens", 0)),
        )
        uso.cost_usd = estimate_cost(model, uso.input_tokens, uso.output_tokens)
        self.usage.add(uso)
        if self.budget is not None:
            self.budget.record(uso)
        choices = risposta.get("choices") or []
        if not choices:
            raise OpenAIError("verifica immagine senza contenuto")
        try:
            return json.loads(choices[0]["message"]["content"]), uso
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise OpenAIError("verifica immagine non in JSON valido") from exc
