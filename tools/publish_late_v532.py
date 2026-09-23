#!/usr/bin/env python3
"""Publish the verified late September 23 batch."""
import hashlib
import json
import sys
from pathlib import Path
from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 532
IMAGES = {
    "trump_xi": ("2b993741-76cc-4c7d-a740-16054e40c0ae", "Scena editoriale contestuale con Donald Trump e Xi Jinping riconoscibili davanti alla Casa Bianca; somiglianze sintetiche non documentarie."),
    "usa_iran": ("96288807-1f24-4ff3-a3de-a7ee3d241361", "Ritratto editoriale neutrale e isolato di Steve Witkoff e Abbas Araghchi; somiglianze sintetiche non documentarie."),
    "baldissero": ("16d348fb-0642-4242-860b-643f40557e53", "Composizione editoriale neutrale con telefono sulla chiamata al 112 e paesaggio rurale piemontese, senza persone."),
    "rottamazione": ("98e5bf6e-4ed2-414d-8dfb-ff5b506c0ac2", "Avviso di pagamento e calendario sul 30 settembre in un ufficio italiano, illustrazione editoriale IA."),
    "polonia": ("f869668f-16da-41ce-9488-a5270fa9db85", "Elicottero militare russo Mi-8 in volo in una scena editoriale neutrale vicino al confine polacco."),
}


def main():
    articles = json.loads((ROOT / "tools/news_batch_20260923_late.json").read_text(encoding="utf-8"))
    previous_release = json.loads((ROOT / "curiomondo-site-manifest.json").read_text(encoding="utf-8")).get("site_version", 0)
    cfg_path = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    urls = {f"/notizie/{a['slug']}.html" for a in articles}
    registry["items"] = [i for i in registry["items"] if i.get("article") not in urls]
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for a in articles:
        a["fonti"] = [{"url": u, "descrizione": d} for u, d in a["fonti"]]
        a["dati_chiave"] = [{"valore": v, "etichetta": l} for v, l in a.pop("stats")]
        ident, alt = IMAGES[a["id"]]
        source = ROOT.parent / f"generated_images/exec-{ident}.png"
        img = Image.open(source).convert("RGB")
        variants = []
        for width in (480, 800, 1200):
            path = ROOT / f"assets/images/editorial-auto/{a['slug']}-v{VERSION}-{width}.webp"
            img.resize((width, round(width / 1.5)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=87, method=6)
            variants.append({"w": width, "src": "/" + str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
        image = {"key": f"{a['slug']}-v{VERSION}", "alt": alt, "variants": variants, "disclosure": site.CAPTION, "generator": "OpenAI image tool", "sensitiveContext": bool(a.get("sensitive"))}
        if a.get("public"):
            image["syntheticLikeness"] = "public-figure"
        if a.get("public") and a.get("sensitive"):
            image.update(portraitOnly=True, portraitFormat="neutral-isolated", reenactedEvent=False, prompt="Neutral editorial portrait, isolated public figures, plain studio background; no reenactment of conflict or negotiations.")

        target = ROOT / f"notizie/{a['slug']}.html"
        existing = target.read_text(encoding="utf-8") if target.exists() else None
        previous = existing if a.get("update") else None
        if existing and not a.get("update") and f"-v{VERSION}-800.webp" not in existing:
            raise ValueError(f"slug già esistente e non creato da questa release: {a['slug']}")
        if previous:
            previous_ld = site._news_json(html.fromstring(previous))
            target.unlink()
        elif existing:
            target.unlink()
        try:
            slug, page = site.render_article(a, image, VERSION)
        finally:
            if previous:
                target.write_text(previous, encoding="utf-8")
        doc = html.fromstring(page)
        if previous:
            script = doc.xpath('//script[@type="application/ld+json"]')[0]
            ld = json.loads(script.text)
            ld["datePublished"] = previous_ld["datePublished"]
            script.text = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))
            meta = doc.xpath('//div[@class="meta"]')[0]
            meta.text = f"Pubblicato il {site._italian_date(ld['datePublished'])} · Aggiornato il {site._italian_date(ld['dateModified'])} · {a['luogo']} · "
            a["published"] = ld["datePublished"]
        target.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode"), encoding="utf-8")
        site.register_image(image, slug, VERSION)
        url = f"/notizie/{slug}.html"
        cfg["articles"][url] = {"firstPublishedAt": a["published"], "homepagePriority": 96 if a["id"] in ("trump_xi", "usa_iran") else 82, "primaryCategory": a["categoria"].lower()}

    cfg["version"] = VERSION
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces(articles, f"/notizie/{articles[0]['slug']}.html", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = manifest["site"]["site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-23", "type": "late-news-batch", "news_added": [a["slug"] for a in articles if not a.get("update")], "news_updated": [a["slug"] for a in articles if a.get("update")], "change": "Tre notizie nuove e due aggiornamenti verificati"}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION, release_date="2026-09-23", last_update="late-news-v532")
        if "articleCount" in state and previous_release < VERSION:
            state["articleCount"] += 3
        if "generatedEditorialImages" in state and previous_release < VERSION:
            state["generatedEditorialImages"] += 5
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Published 3 new articles and 2 updates locally; live validation pending.")


if __name__ == "__main__":
    main()
