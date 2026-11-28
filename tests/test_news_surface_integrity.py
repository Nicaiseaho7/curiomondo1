from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sitemap_urls", ROOT / "tools/sitemap_urls.py")
sitemap_urls = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sitemap_urls)


def article(slug: str, published: str, *, noindex: bool = False, broken_json: bool = False) -> str:
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    data = "{" if broken_json else json.dumps({"@context": "https://schema.org", "@type": "NewsArticle", "datePublished": published})
    return f'''<!doctype html><html><head>
<meta name="robots" content="{robots}">
<link rel="canonical" href="https://curiomondo.it/notizie/{slug}.html">
<script type="application/ld+json">{data}</script>
</head><body><h1>{slug}</h1></body></html>'''


def urlset(locs: list[str]) -> str:
    rows = "".join(f"<url><loc>{loc}</loc></url>" for loc in locs)
    return f'<urlset xmlns="{sitemap_urls.SM_NS}">{rows}</urlset>'


def build_repo(tmp_path: Path, visible: list[str], *, pages: dict[str, str]) -> Path:
    (tmp_path / "notizie").mkdir()
    (tmp_path / "assets/data").mkdir(parents=True)
    for slug, raw in pages.items():
        (tmp_path / f"notizie/{slug}.html").write_text(raw, encoding="utf-8")
    links = "".join(f'<li><a href="/notizie/{slug}.html">{slug}</a></li>' for slug in visible)
    (tmp_path / "notizie/index.html").write_text(f"<main><ul>{links}</ul></main>", encoding="utf-8")
    items = [{"url": f"/notizie/{slug}.html"} for slug in visible]
    for name in ("search-index-v210.json", "home-feed-v210.json"):
        (tmp_path / f"assets/data/{name}").write_text(json.dumps({"items": items}), encoding="utf-8")
    locs = [f"https://curiomondo.it/notizie/{slug}.html" for slug in visible]
    (tmp_path / "sitemap.xml").write_text(urlset(locs), encoding="utf-8")
    (tmp_path / "news-sitemap.xml").write_text(urlset(locs), encoding="utf-8")
    rss = "".join(
        f"<item><guid>https://curiomondo.it/notizie/{slug}.html</guid></item>" for slug in visible
    )
    (tmp_path / "feed.xml").write_text(f"<rss><channel>{rss}</channel></rss>", encoding="utf-8")
    return tmp_path


class NewsSurfaceIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._temporary.name)

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def test_due_lotti_dalla_stessa_base_non_possono_perdere_il_primo(self) -> None:
        tmp_path = self.tmp_path
        pages = {
            "lotto-a": article("lotto-a", "2026-11-25T08:00:00+01:00"),
            "lotto-b": article("lotto-b", "2026-11-25T09:00:00+01:00"),
        }
        repo = build_repo(tmp_path, ["lotto-b"], pages=pages)
        errors = sitemap_urls.news_completeness_errors(
            repo, now=datetime.fromisoformat("2026-11-25T10:00:00+01:00")
        )
        self.assertTrue(errors)
        self.assertTrue(all("lotto-a.html" in error for error in errors))
        self.assertEqual({error.split(":", 1)[0] for error in errors}, {
            "sitemap.xml", "notizie/index.html", "search-index-v210.json",
            "home-feed-v210.json", "feed.xml", "news-sitemap.xml",
        })


    def test_errore_di_parsing_blocca_il_censimento(self) -> None:
        tmp_path = self.tmp_path
        (tmp_path / "notizie").mkdir()
        (tmp_path / "notizie/rotta.html").write_text(
            article("rotta", "2026-11-25T08:00:00+01:00", broken_json=True), encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "NewsArticle assente o non valido"):
            sitemap_urls.published_news(tmp_path)


    def test_noindex_e_fuori_finestra_news_sitemap_sono_esclusioni_legittime(self) -> None:
        tmp_path = self.tmp_path
        pages = {
            "recente": article("recente", "2026-11-25T08:00:00+01:00"),
            "vecchia": article("vecchia", "2026-11-20T08:00:00+01:00"),
            "esclusa": article("esclusa", "2026-11-25T09:00:00+01:00", noindex=True),
        }
        repo = build_repo(tmp_path, ["recente", "vecchia"], pages=pages)
        (repo / "news-sitemap.xml").write_text(
            urlset(["https://curiomondo.it/notizie/recente.html"]), encoding="utf-8"
        )
        self.assertEqual(sitemap_urls.news_completeness_errors(
            repo, now=datetime.fromisoformat("2026-11-25T10:00:00+01:00")
        ), [])


    def test_sostituzione_notizie_conserva_le_pagine_non_news(self) -> None:
        root = ET.fromstring(urlset([
        "https://curiomondo.it/approfondimenti/guida.html",
        "https://curiomondo.it/notizie/vecchia.html",
        "https://curiomondo.it/scadenze/",
    ]))
        pages = {
        "/notizie/a.html": {
            "url": "/notizie/a.html",
            "loc": "https://curiomondo.it/notizie/a.html",
            "published": "2026-11-25T08:00:00+01:00",
            "lastmod": "2026-11-25",
        },
        "/notizie/b.html": {
            "url": "/notizie/b.html",
            "loc": "https://curiomondo.it/notizie/b.html",
            "published": "2026-11-25T09:00:00+01:00",
            "lastmod": "2026-11-25",
        },
    }
        sitemap_urls.replace_news_urls(root, pages)
        locs = {(node.text or "").strip() for node in root.iter(sitemap_urls.LOC)}
        self.assertEqual(locs, {
        "https://curiomondo.it/approfondimenti/guida.html",
        "https://curiomondo.it/scadenze/",
        "https://curiomondo.it/notizie/a.html",
        "https://curiomondo.it/notizie/b.html",
        })


    def test_sync_surfaces_fallisce_prima_di_rigenerare_su_articolo_non_parsabile(self) -> None:
        tmp_path = self.tmp_path
        sys.path.insert(0, str(ROOT))
        from automation.newsroom import site

        (tmp_path / "notizie").mkdir()
        (tmp_path / "tools").mkdir()
        (tmp_path / "notizie/rotta.html").write_text(
            article("rotta", "2026-11-25T08:00:00+01:00", broken_json=True), encoding="utf-8"
        )
        (tmp_path / "tools/sitemap_urls.py").write_text(
            (ROOT / "tools/sitemap_urls.py").read_text(encoding="utf-8"), encoding="utf-8"
        )
        previous = site.ROOT
        site.ROOT = tmp_path
        try:
            with self.assertRaisesRegex(ValueError, "pagine notizie non censibili"):
                site.sync_surfaces([], "", 1, update_manifest=False)
        finally:
            site.ROOT = previous


    def setup_historical_sample(self) -> Path:
        old = article("storica", "2026-08-13")
        nameless = article("senza", "2026-08-13").replace("NewsArticle", "WebPage")
        repo = build_repo(self.tmp_path, ["storica", "senza", "nuova"], pages={
            "storica": old, "senza": nameless,
            "nuova": article("nuova", "2026-11-28T05:00:00+01:00"),
        })
        (repo / "tools").mkdir()
        (repo / "tools/news_legacy_archive.json").write_text(json.dumps({
            "notizie/storica.html": {"sha256": hashlib.sha256(old.encode()).hexdigest(), "datePublished": "2026-08-13"},
            "notizie/senza.html": {"sha256": hashlib.sha256(nameless.encode()).hexdigest(), "datePublished": None},
        }), encoding="utf-8")
        (repo / "assets/data/home-feed-v210.json").write_text(
            json.dumps({"items": [{"url": "/notizie/nuova.html"}]}), encoding="utf-8"
        )
        (repo / "news-sitemap.xml").write_text(urlset(["https://curiomondo.it/notizie/nuova.html"]), encoding="utf-8")
        return repo

    def test_storiche_preservate_senza_orario_inventato(self) -> None:
        repo = self.setup_historical_sample()
        inventory = sitemap_urls.published_news(repo)
        self.assertEqual(inventory["/notizie/storica.html"]["published"], "2026-08-13")
        self.assertEqual(inventory["/notizie/senza.html"]["published"], "")
        now = datetime.fromisoformat("2026-11-28T05:30:00+01:00")
        self.assertEqual(sitemap_urls.news_completeness_errors(repo, now=now), [])
        self.assertEqual([u for _, u in sitemap_urls.news_window(inventory, now)],
                         ["https://curiomondo.it/notizie/nuova.html"])
        (repo / "feed.xml").write_text("<rss><channel></channel></rss>", encoding="utf-8")
        errors = "\n".join(sitemap_urls.news_completeness_errors(repo, now=now))
        self.assertIn("/notizie/storica.html", errors)
        self.assertIn("/notizie/senza.html", errors)

    def test_articolo_nuovo_o_storico_modificato_con_dati_incompleti_fallisce(self) -> None:
        repo = self.setup_historical_sample()
        (repo / "notizie/nuova.html").write_text(article("nuova", "2026-11-28"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nuova.html: datePublished senza fuso"):
            sitemap_urls.published_news(repo)
        (repo / "notizie/nuova.html").write_text(
            article("nuova", "2026-11-28T05:00:00+01:00"), encoding="utf-8")
        old = repo / "notizie/storica.html"
        old.write_text(old.read_text() + "<!-- file modificato -->", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "storica.html: datePublished senza fuso"):
            sitemap_urls.published_news(repo)

    def test_non_si_puo_togliere_una_storica_ne_deindicizzarla(self) -> None:
        repo = self.setup_historical_sample()
        historic = repo / "notizie/storica.html"
        historic.write_text(article("storica", "2026-08-13", noindex=True), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "storica.html: pagina storica deindicizzata"):
            sitemap_urls.published_news(repo)
        historic.unlink()
        with self.assertRaisesRegex(ValueError, "storica.html: pagina storica mancante"):
            sitemap_urls.published_news(repo)

    def test_news_sitemap_oltre_mille_partizioni_verificate(self) -> None:
        repo = self.tmp_path
        (repo / "robots.txt").write_text(
            "User-agent: *\nSitemap: https://curiomondo.it/sitemap.xml\n", encoding="utf-8")
        now = datetime.fromisoformat("2026-11-28T05:30:00+01:00")
        pages = {
            str(i): {"published": (now - timedelta(minutes=i)).isoformat(),
                     "loc": f"https://curiomondo.it/notizie/lotto-{i}.html"} for i in range(1001)
        }
        titles = {page["loc"]: "Titolo " + i for i, page in pages.items()}
        files = sitemap_urls.write_news_sitemaps(repo, pages, titles, now)
        self.assertEqual(files, ["/news-sitemap.xml", "/news-sitemap-2.xml"])
        reader = lambda loc: (repo / loc[1:]).read_bytes()
        robots = (repo / "robots.txt").read_text()
        urls, errors = sitemap_urls.read_news_sitemaps(robots, reader)
        self.assertFalse(errors)
        self.assertEqual(urls, set(titles))
        self.assertEqual([len(ET.fromstring(reader(loc))) for loc in files], [1000, 1])
        (repo / "news-sitemap-2.xml").write_text(urlset([pages["0"]["loc"]]), encoding="utf-8")
        self.assertTrue(any("URL ripetuti" in x for x in sitemap_urls.read_news_sitemaps(robots, reader)[1]))
        (repo / "news-sitemap-2.xml").unlink()
        self.assertTrue(any("non verificabile" in x for x in sitemap_urls.read_news_sitemaps(robots, reader)[1]))

    def test_sitemap_additiva_conserva_metadati_e_url_anteriore(self) -> None:
        root = ET.fromstring(urlset(["https://curiomondo.it/notizie/legacy.html"]))
        prior = list(root)[0]
        ET.SubElement(prior, f"{{{sitemap_urls.SM_NS}}}lastmod").text = "2026-08-13"
        sitemap_urls.replace_news_urls(root, {"news": {"loc": "https://curiomondo.it/notizie/fresh.html",
                                                       "lastmod": "2026-11-28"}}, preserve_prior=True)
        self.assertIn(prior, list(root))
        self.assertEqual(prior.findtext(f"{{{sitemap_urls.SM_NS}}}lastmod"), "2026-08-13")


if __name__ == "__main__":
    unittest.main()
