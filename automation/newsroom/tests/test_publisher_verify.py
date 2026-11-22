import pytest

from automation.newsroom.openai_client import Client, OpenAIError
from automation.newsroom.publisher import _image_prompt, _validate_visual_report, rollback_release
from automation.newsroom.state import Candidate, DRAFTED, QUEUED, Store
from automation.newsroom.verify import SITE, verify_record


def visual_report(**changes):
    result = dict(esito="conforme", certezza="alta", pertinenza="simbolica_pertinente",
                  soggetto_visibile="illustrazione anonima del laboratorio",
                  nesso_con_notizia="rappresenta l'esperimento descritto",
                  fotorealistica=True, volto_reale_riconoscibile=False,
                  logo_o_marchio=False, maglia_ufficiale=False,
                  persone_che_giocano=False, personaggio_protetto=False,
                  violenza_o_sofferenza=False, falso_documento=False,
                  testo_nei_pixel=False, motivo="pertinente")
    result.update(changes)
    return result


def test_controllo_visivo_json(monkeypatch):
    client = Client(api_key="finta")
    seen = {}

    def fake_post(path, payload):
        seen.update(payload)
        return {"usage": {"prompt_tokens": 10, "completion_tokens": 5},
                "choices": [{"finish_reason": "stop", "message": {"content": __import__("json").dumps(visual_report())}}]}

    monkeypatch.setattr(client, "_post", fake_post)
    report, _ = client.inspect_image("gpt-4o", b"png", title="Convegno di fisica",
                                     lead="Ricercatori illustrano l'esperimento.",
                                     brief="laboratorio e strumenti")
    _validate_visual_report(report)
    data = seen["messages"][0]["content"]
    assert all(term in data[0]["text"] for term in ("Convegno di fisica", "Ricercatori illustrano", "laboratorio e strumenti"))
    assert data[1]["image_url"]["detail"] == "high"


@pytest.mark.parametrize("reason,changes", [
    ("MotoGP con pista di atletica", {"esito": "non_conforme", "pertinenza": "fuori_tema",
                                    "soggetto_visibile": "pista di atletica"}),
    ("restauro chiesa con magazzino", {"esito": "non_conforme", "pertinenza": "fuori_tema",
                                       "soggetto_visibile": "magazzino"}),
    ("pertinenza incerta", {"esito": "incerto", "certezza": "bassa", "pertinenza": "incerta"}),
    ("volto reale", {"volto_reale_riconoscibile": True}),
    ("marchio", {"logo_o_marchio": True}),
    ("maglia", {"maglia_ufficiale": True}),
    ("sport praticato", {"persone_che_giocano": True}),
    ("personaggio protetto", {"personaggio_protetto": True}),
    ("documento falso", {"falso_documento": True}),
    ("violenza", {"violenza_o_sofferenza": True}),
    ("risposta incompleta", {"logo_o_marchio": None}),
    ("fiducia insufficiente", {"certezza": "bassa"}),
])
def test_rifiuta_immagine_non_conforme_anche_con_slug_corretto(reason, changes):
    # Il nome del file non entra nel verdetto visivo.
    with pytest.raises(OpenAIError, match="non approvata"):
        _validate_visual_report(visual_report(**changes))


def test_immagine_simbolica_pertinente_ammessa():
    _validate_visual_report(visual_report())
    _validate_visual_report(visual_report(pertinenza="diretta"))


def test_prompt_non_ripropone_ordini_storici(monkeypatch):
    import automation.newsroom.publisher as publisher
    article = {"titolo": "MotoGP: nuove prove", "sommario": "Prove sul circuito.",
               "paragrafi": ["La MotoGP corre domenica sul circuito."],
               "immagine": {"prompt": "pista moto vuota"}}
    prompt = _image_prompt(article)
    assert "pista moto vuota" in prompt
    assert "Article lead: La MotoGP" in prompt
    assert "depict the real person" not in prompt
    assert "PUBBLICHE E SOMIGLIANZA SINTETICA" not in prompt


def test_rollback_rimette_il_lotto_in_bozza(tmp_path):
    store = Store(tmp_path)
    store.add(Candidate(url_key="k", topic_key="t", url="u", title="t", source="s",
                        source_tier="agency", status=QUEUED, article={"slug": "slug"}))
    store.save()
    assert rollback_release(tmp_path)["restored"] == ["slug"]
    assert Store(tmp_path).get("k").status == DRAFTED


def test_verifica_post_deploy_completa():
    article_url = f"{SITE}/notizie/prova.html"
    page = f'<html><head><link rel="canonical" href="{article_url}"></head><body><main><figure class="article-image"><img src="/assets/prova.webp"></figure></main></body></html>'.encode()

    def fetch(url):
        if url == article_url:
            return 200, page
        if url.endswith(".webp"):
            return 200, b"image"
        return 200, article_url.encode()

    ok, checks, reason = verify_record({"public_url": article_url}, fetch)
    assert ok and not reason and all(checks.values())
