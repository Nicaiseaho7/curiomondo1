from automation.newsroom.openai_client import Client
from automation.newsroom.publisher import _validate_visual_report, rollback_release
from automation.newsroom.state import Candidate, DRAFTED, QUEUED, Store
from automation.newsroom.verify import SITE, verify_record


def test_controllo_visivo_json(monkeypatch):
    client = Client(api_key="finta")
    monkeypatch.setattr(client, "_post", lambda *a, **k: {
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        "choices": [{"message": {"content": '{"approvata":true,"fotorealistica":true,"coerente":true,"soggetto_reale":true,"persone_inventate":false,"testo_nei_pixel":false,"contenuto_sensibile_non_consentito":false,"motivo":"ok"}'}}],
    })
    report, _ = client.inspect_image("gpt-4o", b"png", "una piazza")
    _validate_visual_report(report)


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
