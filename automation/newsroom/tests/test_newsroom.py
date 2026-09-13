"""Test della redazione automatica.

Girano senza rete: le risposte delle fonti sono fixture. Servono a garantire
che deduplicazione, filtri e stato si comportino sempre allo stesso modo, anche
quando il watcher viene eseguito centinaia di volte al giorno.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from automation.newsroom import filters, normalize, sources, watcher
from automation.newsroom.state import Candidate, Store

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


def iso(hours_ago: float) -> str:
    return (NOW - timedelta(hours=hours_ago)).isoformat(timespec="seconds")


# --------------------------------------------------------------- normalize
def test_canonical_url_rimuove_tracciamento_e_www():
    a = normalize.canonical_url("https://www.ansa.it/Articolo?utm_source=x&gclid=1&id=7")
    b = normalize.canonical_url("http://ansa.it/Articolo?id=7")
    assert a.endswith("/Articolo?id=7")
    assert normalize.url_key(a) == normalize.url_key(b)


def test_canonical_url_distingue_articoli_diversi():
    a = normalize.url_key("https://ansa.it/uno")
    b = normalize.url_key("https://ansa.it/due")
    assert a != b


def test_riconosce_la_stessa_notizia_da_fonti_diverse():
    """Due testate raccontano lo stesso fatto con parole leggermente diverse.

    L'impronta esatta non può bastare (una parola in più la cambia): il
    riconoscimento affidabile è quello per somiglianza fra le parole chiave.
    """
    reuters = "Terremoto di magnitudo 6.2 colpisce la costa del Giappone"
    ansa = normalize.clean_title("Giappone, terremoto magnitudo 6.2 sulla costa - ANSA")
    assert normalize.title_similarity(reuters, ansa) >= 0.62


def test_titoli_di_notizie_diverse_non_si_somigliano():
    assert normalize.title_similarity(
        "Terremoto di magnitudo 6.2 colpisce la costa del Giappone",
        "La Bce lascia invariati i tassi di interesse",
    ) < 0.3


def test_numeri_significativi_restano_nelle_parole_chiave():
    assert "2026" in normalize.title_tokens("Bilancio 2026 approvato dal governo")
    # Le cifre singole nascono dallo spezzarsi dei decimali: non distinguono nulla.
    assert "6" not in normalize.title_tokens("Scossa di magnitudo 6.2")


def test_topic_key_separa_notizie_diverse():
    assert normalize.topic_key("Terremoto in Giappone, magnitudo 6.2") != normalize.topic_key(
        "La Bce alza i tassi di interesse allo 2,5 per cento"
    )


def test_clean_title_toglie_il_suffisso_della_testata():
    assert normalize.clean_title("Crolla un ponte a Genova - Reuters") == "Crolla un ponte a Genova"


# ----------------------------------------------------------------- filters
def test_scarta_oroscopi_e_dirette_perenni():
    assert not filters.screen("Oroscopo di oggi segno per segno", "", "agency", "high", iso(1), now=NOW).accepted
    assert not filters.screen("Calciomercato in diretta live, tutte le trattative", "", "sport", "medium", iso(1), now=NOW).accepted


def test_scarta_notizie_troppo_vecchie():
    d = filters.screen("Il governo approva la nuova legge di bilancio", "", "primary", "high", iso(80), now=NOW)
    assert not d.accepted and d.reason == "troppo_vecchia"


def test_accetta_notizia_istituzionale_recente():
    d = filters.screen("La Commissione europea approva il piano da 90 miliardi", "", "primary", "high", iso(1), now=NOW)
    assert d.accepted and d.score > 0.8


def test_riconosce_le_breaking_news():
    d = filters.screen("Terremoto di magnitudo 6.4 al largo della Grecia", "", "agency", "high", iso(0.2), now=NOW)
    assert d.accepted and d.priority == "breaking"


def test_alto_rischio_da_fonte_debole_viene_scartato():
    d = filters.screen("Missili sulla capitale, decine di vittime", "", "agency", "low", iso(0.5), now=NOW)
    assert not d.accepted and d.reason == "alto_rischio_fonte_debole"


def test_alto_rischio_da_fonte_forte_passa_ma_resta_segnalato():
    d = filters.screen("Missili sulla capitale, decine di vittime", "", "agency", "high", iso(0.5), now=NOW)
    assert d.accepted and d.high_risk


def test_titolo_troppo_corto_scartato():
    assert not filters.screen("Breve", "", "primary", "high", iso(1), now=NOW).accepted


# ----------------------------------------------------------------- sources
RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>Prima notizia importante dal mondo</title><link>https://esempio.it/a?utm_source=rss</link><pubDate>Sun, 13 Sep 2026 11:30:00 GMT</pubDate><description>Sintesi</description></item>
<item><title>Seconda notizia rilevante di oggi</title><link>https://esempio.it/b</link><pubDate>Sun, 13 Sep 2026 10:00:00 GMT</pubDate></item>
</channel></rss>"""

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Notizia atom con titolo lungo</title><link rel="alternate" href="https://esempio.org/x"/><updated>2026-09-13T11:00:00Z</updated><summary>Testo</summary></entry>
</feed>"""


def _feed(**kwargs):
    base = dict(id="test", name="Test", url="https://esempio.it/rss", tier="agency",
                category="mondo", cadence="fast", trust="high", direct=True)
    base.update(kwargs)
    return sources.Feed(**base)


def test_parse_rss_estrae_voci_e_normalizza_url():
    items = sources.parse_feed(RSS.encode(), _feed())
    assert len(items) == 2
    assert items[0].title == "Prima notizia importante dal mondo"
    assert "utm_source" not in items[0].url
    assert items[0].published_at.startswith("2026-09-13T11:30")


def test_parse_atom():
    items = sources.parse_feed(ATOM.encode(), _feed())
    assert len(items) == 1 and items[0].url == "https://esempio.org/x"


def test_parse_feed_non_esplode_su_xml_rotto():
    assert sources.parse_feed(b"<rss><broken", _feed()) == []


def test_load_feeds_filtra_per_cadenza(tmp_path):
    path = tmp_path / "s.json"
    path.write_text(json.dumps({"feeds": [
        {"id": "a", "name": "A", "url": "https://a/rss", "cadence": "fast"},
        {"id": "b", "name": "B", "url": "https://b/rss", "cadence": "deep"},
        {"id": "c", "name": "C", "url": "https://c/rss", "cadence": "fast", "enabled": False},
    ]}), encoding="utf-8")
    assert [f.id for f in sources.load_feeds(path, cadence="fast")] == ["a"]
    assert [f.id for f in sources.load_feeds(path, cadence="deep")] == ["a", "b"]


def test_registro_fonti_reale_e_valido():
    feeds = sources.load_feeds(Path(__file__).resolve().parents[1] / "sources.json", cadence="deep")
    assert len(feeds) >= 30
    assert {f.id for f in feeds}.__len__() == len(feeds), "id duplicati nel registro"
    assert any(f.cadence == "fast" for f in feeds)
    assert all(f.url.startswith("https://") for f in feeds)


# ------------------------------------------------------------------- state
def test_store_salva_e_rilegge(tmp_path):
    store = Store(tmp_path)
    store.add(Candidate(url_key="k1", topic_key="t1", url="https://x/1", title="Uno",
                        source="ANSA", source_tier="agency"))
    store.save()
    assert Store(tmp_path).get("k1").title == "Uno"


def test_store_riconosce_stesso_argomento(tmp_path):
    store = Store(tmp_path)
    store.add(Candidate(url_key="k1", topic_key="t1", url="https://x/1", title="Uno",
                        source="ANSA", source_tier="agency"))
    assert store.knows_topic("t1") is not None
    assert store.knows_topic("t2") is None


def test_prune_rimuove_solo_i_chiusi_e_vecchi(tmp_path):
    store = Store(tmp_path)
    old = (datetime.now(timezone.utc) - timedelta(days=40)).isoformat(timespec="seconds")
    store.add(Candidate(url_key="vecchio", topic_key="a", url="u", title="t", source="s",
                        source_tier="agency", status="rejected", first_seen=old))
    store.add(Candidate(url_key="attivo", topic_key="b", url="u", title="t", source="s",
                        source_tier="agency", status="queued", first_seen=old))
    assert store.prune(keep_days=21) == 1
    assert store.get("attivo") is not None and store.get("vecchio") is None


def test_ciclo_di_vita_pubblicazione(tmp_path):
    store = Store(tmp_path)
    store.add(Candidate(url_key="k", topic_key="t", url="u", title="t", source="s", source_tier="agency"))
    store.mark_published("k", "mio-slug", "https://curiomondo.it/notizie/mio-slug.html")
    assert store.get("k").status == "published"
    assert store.pending_verification()
    store.mark_verified("mio-slug", {"http": 200})
    assert store.get("k").status == "verified"
    assert not store.pending_verification()


# ------------------------------------------------------------------ watcher
def test_watch_deduplica_e_filtra(tmp_path, monkeypatch):
    """Due fonti raccontano lo stesso fatto: deve restare un solo candidato."""
    feed_a = _feed(id="a", name="Reuters", tier="agency")
    feed_b = _feed(id="b", name="ANSA", tier="agency")

    def fake_fetch_all(feeds, cache=None, timeout=12):
        items = [
            sources.Item("Terremoto di magnitudo 6.2 colpisce la costa del Giappone",
                         "https://reuters.com/a", iso(0.3), "Reuters", "agency", "mondo", "high"),
            sources.Item("Giappone, terremoto magnitudo 6.2 sulla costa",
                         "https://ansa.it/b", iso(0.4), "ANSA", "agency", "mondo", "high"),
            sources.Item("Oroscopo di oggi, tutti i segni zodiacali",
                         "https://ansa.it/c", iso(0.2), "ANSA", "agency", "italia", "high"),
            sources.Item("La Bce lascia invariati i tassi di interesse",
                         "https://ansa.it/d", iso(1.0), "ANSA", "agency", "economia", "high"),
        ]
        health = [{"feed": "a", "status": "ok", "items": 2}, {"feed": "b", "status": "ok", "items": 2}]
        return items, health, cache or {}

    monkeypatch.setattr(watcher, "fetch_all", fake_fetch_all)
    monkeypatch.setattr(watcher, "load_feeds", lambda *a, **k: [feed_a, feed_b])

    empty_articles = tmp_path / "notizie"
    empty_articles.mkdir()
    summary = watcher.run_watch(tmp_path / "state", cadence="fast", articles_dir=empty_articles)

    assert summary["status"] == "ok"
    assert summary["nuovi_candidati"] == 2, "terremoto (una volta) + bce; oroscopo scartato"
    store = Store(tmp_path / "state")
    reasons = {c.reason for c in store.all_candidates() if c.status == "rejected"}
    assert "categoria_esclusa" in reasons
    assert any(r.startswith("duplicato_di:") for r in reasons)


def test_watch_non_ripropone_quello_che_gia_conosce(tmp_path, monkeypatch):
    feed = _feed()
    item = sources.Item("La Bce lascia invariati i tassi di interesse",
                        "https://ansa.it/d", iso(1.0), "ANSA", "agency", "economia", "high")
    monkeypatch.setattr(watcher, "fetch_all", lambda f, cache=None, timeout=12: ([item], [], cache or {}))
    monkeypatch.setattr(watcher, "load_feeds", lambda *a, **k: [feed])
    articles = tmp_path / "notizie"; articles.mkdir()

    first = watcher.run_watch(tmp_path / "state", articles_dir=articles)
    second = watcher.run_watch(tmp_path / "state", articles_dir=articles)
    assert first["nuovi_candidati"] == 1
    assert second["nuovi_candidati"] == 0, "un secondo giro non deve riproporre lo stesso link"


def test_watch_scarta_cio_che_e_gia_sul_sito(tmp_path, monkeypatch):
    articles = tmp_path / "notizie"; articles.mkdir()
    (articles / "bce-lascia-invariati-i-tassi-di-interesse.html").write_text("<html></html>", encoding="utf-8")
    item = sources.Item("Bce lascia invariati i tassi di interesse",
                        "https://ansa.it/d", iso(1.0), "ANSA", "agency", "economia", "high")
    monkeypatch.setattr(watcher, "fetch_all", lambda f, cache=None, timeout=12: ([item], [], cache or {}))
    monkeypatch.setattr(watcher, "load_feeds", lambda *a, **k: [_feed()])

    summary = watcher.run_watch(tmp_path / "state", articles_dir=articles)
    assert summary["nuovi_candidati"] == 0
    store = Store(tmp_path / "state")
    assert any(c.reason == "gia_pubblicato_sul_sito" for c in store.all_candidates())


def test_watch_rispetta_il_limite_per_ciclo(tmp_path, monkeypatch):
    # Titoli realmente diversi fra loro: altrimenti verrebbero (giustamente)
    # riconosciuti come la stessa notizia e il limite non verrebbe esercitato.
    titoli = [
        "La Commissione europea approva il piano industriale per i semiconduttori",
        "Il Parlamento italiano vota la riforma della giustizia civile",
        "La Banca centrale giapponese rivede le previsioni di crescita",
        "Il Canada annuncia nuovi finanziamenti per la transizione energetica",
        "L'agenzia spaziale indiana completa la missione lunare Chandrayaan",
        "Il ministero della Salute pubblica i dati sulle vaccinazioni stagionali",
        "L'Argentina raggiunge un accordo sul debito con i creditori privati",
        "La Corea del Sud presenta il bilancio pubblico per il prossimo anno",
        "Il Brasile amplia le aree protette nella foresta amazzonica",
        "La Norvegia inaugura il più grande parco eolico offshore del Paese",
    ]
    items = [
        sources.Item(titolo, f"https://ansa.it/{n}", iso(1.0), "ANSA", "primary", "mondo", "high")
        for n, titolo in enumerate(titoli)
    ]
    monkeypatch.setattr(watcher, "fetch_all", lambda f, cache=None, timeout=12: (items, [], cache or {}))
    monkeypatch.setattr(watcher, "load_feeds", lambda *a, **k: [_feed()])
    articles = tmp_path / "notizie"; articles.mkdir()

    summary = watcher.run_watch(tmp_path / "state", articles_dir=articles, max_new=3)
    assert summary["nuovi_candidati"] == 3


def test_log_non_contiene_segreti(tmp_path, monkeypatch):
    from automation.newsroom.observability import CycleLogger
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-1234567890abcdefghij")
    log = CycleLogger("t", log_dir=tmp_path, echo=False)
    log.event("prova", messaggio="chiave sk-test-1234567890abcdefghij dentro il testo")
    scritto = (tmp_path / f"{datetime.now(timezone.utc):%Y-%m-%d}.jsonl").read_text(encoding="utf-8")
    assert "sk-test-1234567890abcdefghij" not in scritto
    assert "[REDACTED]" in scritto
