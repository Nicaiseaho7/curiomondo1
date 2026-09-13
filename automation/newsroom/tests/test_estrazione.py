"""Test dei due punti che hanno fatto fallire la prima prova editoriale.

La prova aveva esaminato 25 candidati e prodotto zero articoli: quasi tutti
scartati per "fonti_non_leggibili" (link di Google News mai sciolti) e i pochi
leggibili persi per una risposta troncata. Qui si fissano entrambi i
comportamenti, perché una regressione silenziosa su questi due punti
significherebbe una redazione che non pubblica mai e non dice perché.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from automation.newsroom import googlenews
from automation.newsroom.openai_client import Client, OpenAIError, modello_ragiona


def identificativo_vecchio_formato(url: str) -> str:
    """Ricostruisce il blob che Google usava prima degli identificativi opachi."""
    grezzo = b"\x08\x13\x22" + bytes([len(url)]) + url.encode() + b"\xd2\x01\x00"
    return base64.urlsafe_b64encode(grezzo).decode().rstrip("=")


# ------------------------------------------------------------- Google News
def test_riconosce_un_rimando_di_google_news():
    assert googlenews.e_google_news("https://news.google.com/rss/articles/CBMiK2h0dHA")
    assert not googlenews.e_google_news("https://www.ansa.it/sito/notizie/x.html")


def test_scioglie_il_vecchio_formato_senza_toccare_la_rete():
    vero = "https://www.reuters.com/world/europe/notizia-vera-2026-09-13/"
    link = f"https://news.google.com/rss/articles/{identificativo_vecchio_formato(vero)}?oc=5"
    assert googlenews.da_identificativo(link) == vero


def test_un_link_diretto_non_viene_toccato():
    diretto = "https://www.ansa.it/sito/notizie/mondo/x.html"
    esito = googlenews.risolvi(diretto)
    assert esito.url == diretto and esito.metodo == "diretto" and esito.risolto


def test_un_identificativo_illeggibile_non_finge_di_essere_risolto():
    esito = googlenews.Risoluzione("", "", "firma_assente")
    assert not esito.risolto


def test_ripulisce_la_coda_del_blob():
    assert googlenews._pulisci("https://sito.it/articolo\\xd2\\x01") == "https://sito.it/articolo"


# --------------------------------------------------------------- troncamento
class ClienteConRisposte(Client):
    """Client che non usa la rete: registra i payload e risponde a copione."""

    def __init__(self, risposte):
        super().__init__(api_key="finta", budget=None)
        self.risposte = list(risposte)
        self.payload = []

    def _post(self, path, payload):
        self.payload.append(payload)
        return self.risposte.pop(0)


def risposta(contenuto="", motivo="stop", ragionamento=0):
    return {
        "choices": [{"message": {"content": contenuto}, "finish_reason": motivo}],
        "usage": {"prompt_tokens": 800, "completion_tokens": 400,
                  "completion_tokens_details": {"reasoning_tokens": ragionamento}},
    }


def test_una_risposta_troncata_viene_ritentata_con_un_tetto_piu_largo():
    client = ClienteConRisposte([
        risposta("", "length", ragionamento=1200),
        risposta(json.dumps({"pubblicare": True})),
    ])
    dati, _ = client.complete_json("gpt-5", "sistema", "utente", max_tokens=1200)
    assert dati == {"pubblicare": True}
    assert client.payload[1]["max_completion_tokens"] > client.payload[0]["max_completion_tokens"]


def test_due_troncamenti_di_seguito_falliscono_dicendo_quanto_e_costato_il_ragionamento():
    client = ClienteConRisposte([
        risposta("", "length", ragionamento=1200),
        risposta("", "length", ragionamento=3600),
    ])
    with pytest.raises(OpenAIError) as errore:
        client.complete_json("gpt-5", "sistema", "utente", max_tokens=1200)
    assert "ragionamento" in str(errore.value)


def test_lo_sforzo_di_ragionamento_e_dichiarato_solo_ai_modelli_che_ragionano():
    assert modello_ragiona("gpt-5") and not modello_ragiona("gpt-4o")
    client = ClienteConRisposte([risposta(json.dumps({"ok": 1}))])
    client.complete_json("gpt-5", "s", "u", max_tokens=500, sforzo="low")
    assert client.payload[0]["reasoning_effort"] == "low"

    client = ClienteConRisposte([risposta(json.dumps({"ok": 1}))])
    client.complete_json("gpt-4o", "s", "u", max_tokens=500)
    assert "reasoning_effort" not in client.payload[0]


def test_una_risposta_vuota_ma_conclusa_non_passa_per_buona():
    """Un contenuto vuoto con finish_reason 'stop' è comunque niente da leggere."""
    client = ClienteConRisposte([risposta("   "), risposta(json.dumps({"ok": 1}))])
    dati, _ = client.complete_json("gpt-5", "s", "u", max_tokens=500)
    assert dati == {"ok": 1}
