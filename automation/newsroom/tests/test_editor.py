"""Test della verifica editoriale, del tetto di spesa e dei controlli articolo.

Nessuna chiamata reale al modello: le risposte sono simulate. Quello che conta
qui è che le regole del protocollo siano applicate in codice, perché un modello
può sempre distrarsi e rispondere "pubblica" quando non deve.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from automation.newsroom import editor
from automation.newsroom.extract import Extracted
from automation.newsroom.openai_client import (
    BudgetExceeded, BudgetGuard, Client, Usage, estimate_cost,
)
from automation.newsroom.state import Candidate


class ClienteFinto(Client):
    """Client che restituisce risposte preconfezionate, senza rete."""

    def __init__(self, risposte):
        super().__init__(api_key="finta", budget=None)
        self.risposte = list(risposte)
        self.chiamate = []

    def complete_json(self, model, system, user, schema_hint="", max_tokens=2000, sforzo="low"):
        self.chiamate.append({"model": model, "user": user})
        if not self.risposte:
            raise AssertionError("chiamata inattesa al modello")
        return self.risposte.pop(0), Usage(calls=1, input_tokens=100, output_tokens=50)


def estratto_ok(url="https://fonte.it/a", parole=200):
    testo = " ".join(["parola"] * parole)
    return Extracted(url, "Titolo fonte", testo, [testo], True)


def estratto_ko(url="https://fonte.it/b"):
    return Extracted(url, "", "", [], False, "http_403")


VERDETTO_BUONO = {
    "pubblicare": True,
    "motivo": "fatto confermato da due agenzie con dati ufficiali",
    "formato": "standard",
    "categoria": "Economia",
    "fonte_primaria": True,
    "fonti_indipendenti": 2,
    "valore_aggiunto": ["spiegazione del dato", "confronto con il trimestre precedente"],
    "rischio_disinformazione": "basso",
    "sensibile": False,
    "dichiarazione_di_parte": False,
}


# ------------------------------------------------------------ tetto di spesa
def test_budget_accumula_e_persiste(tmp_path):
    guardia = BudgetGuard(tmp_path, daily_limit_usd=1.0)
    guardia.record(Usage(calls=1, input_tokens=1000, output_tokens=500, cost_usd=0.3))
    assert guardia.spent_today == pytest.approx(0.3)
    # Una nuova istanza deve ritrovare la spesa: serve ad accorgersi di una fuga lenta.
    assert BudgetGuard(tmp_path, daily_limit_usd=1.0).spent_today == pytest.approx(0.3)


def test_budget_blocca_oltre_il_tetto(tmp_path):
    guardia = BudgetGuard(tmp_path, daily_limit_usd=0.5)
    guardia.record(Usage(cost_usd=0.49))
    guardia.check(expected_cost=0.001)          # ancora dentro
    with pytest.raises(BudgetExceeded):
        guardia.check(expected_cost=0.05)


def test_budget_avvisa_prima_di_arrivare_al_limite(tmp_path):
    guardia = BudgetGuard(tmp_path, daily_limit_usd=1.0, alert_ratio=0.8)
    guardia.record(Usage(cost_usd=0.5))
    assert not guardia.near_limit()
    guardia.record(Usage(cost_usd=0.35))
    assert guardia.near_limit()


def test_client_rifiuta_di_chiamare_se_il_budget_e_finito(tmp_path):
    guardia = BudgetGuard(tmp_path, daily_limit_usd=0.1)
    guardia.record(Usage(cost_usd=0.2))
    client = Client(budget=guardia, api_key="finta")
    with pytest.raises(BudgetExceeded):
        client._post("/chat/completions", {})


def test_stima_costo_usa_prezzo_prudente_per_modelli_sconosciuti():
    noto = estimate_cost("gpt-4o-mini", 1_000_000, 0)
    ignoto = estimate_cost("modello-mai-visto", 1_000_000, 0)
    assert ignoto > noto, "un modello sconosciuto non deve essere stimato a poco"


# ----------------------------------------------------------------- verifica
def test_verifica_approva_notizia_solida():
    client = ClienteFinto([VERDETTO_BUONO])
    verdetto, _ = editor.verifica(
        client, "gpt-5", "Istat: il PIL cresce dello 0,3%", "ANSA",
        [estratto_ok()], conferme=[{"source": "Reuters"}], alto_rischio=False,
    )
    assert verdetto.pubblicare and verdetto.categoria == "Economia"


def test_verifica_rifiuta_se_manca_il_valore_aggiunto():
    """Il protocollo lo impone: una sola voce significa solo riscrittura."""
    risposta = dict(VERDETTO_BUONO, valore_aggiunto=["riassunto del lancio"])
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Titolo", "ANSA",
        [estratto_ok()], conferme=[], alto_rischio=False,
    )
    assert not verdetto.pubblicare and "riscrittura" in verdetto.motivo


def test_verifica_rifiuta_senza_fonti_leggibili():
    verdetto, _ = editor.verifica(
        ClienteFinto([VERDETTO_BUONO]), "gpt-5", "Titolo", "ANSA",
        [estratto_ko()], conferme=[], alto_rischio=False,
    )
    assert not verdetto.pubblicare and "materia verificata" in verdetto.motivo


def test_verifica_rifiuta_rischio_disinformazione_alto():
    risposta = dict(VERDETTO_BUONO, rischio_disinformazione="alto")
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Titolo", "ANSA",
        [estratto_ok()], conferme=[], alto_rischio=True,
    )
    assert not verdetto.pubblicare


def test_dichiarazione_di_una_sola_parte_non_diventa_fatto():
    """Il punto piu delicato: una rivendicazione non e una notizia accertata."""
    risposta = dict(VERDETTO_BUONO, dichiarazione_di_parte=True)
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Il ministero rivendica l'attacco", "TASS",
        [estratto_ok()], conferme=[], alto_rischio=True,
    )
    assert not verdetto.pubblicare and "conferme indipendenti" in verdetto.motivo


def test_dichiarazione_di_parte_passa_con_una_conferma():
    risposta = dict(VERDETTO_BUONO, dichiarazione_di_parte=True)
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Il ministero rivendica l'attacco", "TASS",
        [estratto_ok()], conferme=[{"source": "Reuters"}], alto_rischio=True,
    )
    assert verdetto.pubblicare


def test_verifica_corregge_categoria_inventata():
    risposta = dict(VERDETTO_BUONO, categoria="Gossip")
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Titolo", "ANSA",
        [estratto_ok()], conferme=[{"source": "AP"}], alto_rischio=False,
    )
    assert verdetto.categoria in editor.CATEGORIE


def test_il_materiale_delicato_avvisa_il_modello():
    client = ClienteFinto([VERDETTO_BUONO])
    editor.verifica(client, "gpt-5", "Missili sulla citta", "Reuters",
                    [estratto_ok()], conferme=[{"source": "AP"}], alto_rischio=True)
    assert "delicato" in client.chiamate[0]["user"]


# ------------------------------------------------------- controlli articolo
def articolo_valido(**extra):
    base = {
        "titolo": "Istat, il PIL italiano cresce dello 0,3% nel secondo trimestre",
        "sommario": "Il dato supera le attese degli analisti e conferma la ripresa dei servizi, mentre l'industria resta debole.",
        "luogo": "Roma",
        "formato": "standard",
        "categoria": "Economia",
        "paragrafi": [" ".join(["parola"] * 50) for _ in range(8)],
        "fonti": [
            {"url": "https://istat.it/x", "descrizione": "dati ufficiali"},
            {"url": "https://reuters.com/y", "descrizione": "conferma"},
        ],
        "parole_chiave_titolo": ["0,3%", "PIL"],
        "dati_chiave": [
            {"icona": "◆", "valore": "+0,3%", "etichetta": "crescita trimestrale"},
            {"icona": "▲", "valore": "2026", "etichetta": "anno di riferimento"},
            {"icona": "●", "valore": "Servizi", "etichetta": "settore trainante"},
        ],
    }
    base.update(extra)
    return base


def test_articolo_valido_non_ha_problemi():
    assert editor.controlla_articolo(articolo_valido()) == []


def test_scarta_paragrafo_troppo_lungo():
    lungo = articolo_valido(paragrafi=[" ".join(["parola"] * 80)] * 5)
    assert any("oltre 60 parole" in p for p in editor.controlla_articolo(lungo))


def test_scarta_lunghezza_fuori_fascia():
    corto = articolo_valido(paragrafi=["parola " * 10])
    assert any("fuori fascia" in p for p in editor.controlla_articolo(corto))


def test_pretende_almeno_due_fonti():
    una = articolo_valido(fonti=[{"url": "https://istat.it/x", "descrizione": "dati"}])
    assert any("due fonti" in p for p in editor.controlla_articolo(una))


def test_pretende_esattamente_tre_dati_chiave():
    """La card in evidenza ne mostra tre: due o quattro romperebbero il gate."""
    due = articolo_valido(dati_chiave=articolo_valido()["dati_chiave"][:2])
    assert any("3 dati chiave" in p for p in editor.controlla_articolo(due))


def test_scarta_parole_evidenziate_assenti_dal_titolo():
    fuori = articolo_valido(parole_chiave_titolo=["inflazione"])
    assert any("non presenti nel titolo" in p for p in editor.controlla_articolo(fuori))


def test_slug_pulito_da_accenti_e_punteggiatura():
    assert editor.slugify("Perché l'Istat rivede il PIL: +0,3%") == "perche-l-istat-rivede-il-pil-0-3"


# --------------------------------------------------------------- conferme
def test_candidato_raccoglie_conferme_senza_duplicare_la_fonte():
    c = Candidate(url_key="k", topic_key="t", url="u", title="t", source="ANSA", source_tier="agency")
    assert c.independent_sources == 1
    assert c.add_corroboration("Reuters", "https://r/1", "Titolo")
    assert not c.add_corroboration("Reuters", "https://r/2", "Altro titolo")
    assert c.independent_sources == 2


# ------------------------------------------------- taratura della severita
def test_notizia_ordinaria_da_agenzia_non_pretende_una_seconda_fonte():
    """Una sola agenzia affidabile basta per una notizia ordinaria.

    La prima prova sul campo rifiutava tutto perche il protocollo chiedeva due
    fonti indipendenti per qualunque fatto: una redazione cosi non pubblica mai.
    """
    risposta = dict(VERDETTO_BUONO, sensibile=False, fonte_primaria=False)
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Il Napoli batte il Bologna 1-0", "ANSA",
        [estratto_ok()], conferme=[], alto_rischio=False, tier="agency", trust="high",
    )
    assert verdetto.pubblicare


def test_tema_delicato_con_una_sola_fonte_non_si_apre():
    risposta = dict(VERDETTO_BUONO, sensibile=True, fonte_primaria=False)
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "Raid sulla citta, dieci vittime", "The Guardian",
        [estratto_ok()], conferme=[], alto_rischio=True, tier="agency", trust="high",
    )
    assert not verdetto.pubblicare and "delicato" in verdetto.motivo


def test_tema_delicato_con_atto_ufficiale_si_apre():
    risposta = dict(VERDETTO_BUONO, sensibile=True, fonte_primaria=True)
    verdetto, _ = editor.verifica(
        ClienteFinto([risposta]), "gpt-5", "La procura chiude l'inchiesta", "ANSA",
        [estratto_ok()], conferme=[], alto_rischio=True, tier="agency", trust="high",
    )
    assert verdetto.pubblicare


def test_la_natura_della_fonte_viene_detta_al_modello():
    client = ClienteFinto([VERDETTO_BUONO])
    editor.verifica(client, "gpt-5", "Titolo lungo abbastanza", "ANSA",
                    [estratto_ok()], conferme=[], alto_rischio=False,
                    tier="agency", trust="high")
    assert "agency" in client.chiamate[0]["user"]


def test_due_volte_la_stessa_pagina_non_fa_due_fonti():
    stessa = articolo_valido(fonti=[
        {"url": "https://theguardian.com/x", "descrizione": "il fatto"},
        {"url": "https://theguardian.com/x/", "descrizione": "le dichiarazioni"},
    ])
    assert any("fonti distinte" in p for p in editor.controlla_articolo(stessa))


def test_gli_indirizzi_citabili_includono_conferme_e_documenti_ufficiali():
    letto = Extracted("https://ansa.it/a", "t", "testo", ["testo"], True,
                      links=["https://www.istat.it/comunicato"])
    citabili = editor.url_citabili([letto], [{"url": "https://reuters.com/b", "source": "Reuters"}])
    assert citabili == ["https://ansa.it/a", "https://reuters.com/b", "https://www.istat.it/comunicato"]


def test_gli_indirizzi_citabili_non_si_ripetono():
    letto = Extracted("https://ansa.it/a", "t", "testo", ["testo"], True,
                      links=["https://ansa.it/a", "https://www.istat.it/c"])
    assert editor.url_citabili([letto], [{"url": "https://ansa.it/a"}]) == [
        "https://ansa.it/a", "https://www.istat.it/c"]
