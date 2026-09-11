#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 323
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

ARTICLE = {
    "slug": "emma-bonino-morta-78-anni-11-settembre-2026",
    "title": "È morta Emma Bonino, storica leader radicale ed ex ministra degli Esteri",
    "excerpt": "La scomparsa, a 78 anni, è stata annunciata da +Europa. Nei giorni precedenti era stata ricoverata a Roma per una crisi respiratoria.",
    "published": "2026-09-11T09:43:00+02:00",
    "category": "Italia / Politica",
    "place": "Italia",
    "key": "emma-bonino-ritratto-neutrale-morte-ai-v323",
    "alt": "Ritratto editoriale neutrale e isolato di Emma Bonino su sfondo blu, somiglianza sintetica fotorealistica generata con IA per una notizia sensibile",
    "public_figure": "Emma Bonino",
    "sensitive": True,
    "points": [
        ("78 anni", "l'età di Emma Bonino"),
        ("11 settembre", "l'annuncio di +Europa"),
        ("2013–2014", "il mandato da ministra degli Esteri"),
    ],
    "body": [
        "Emma Bonino è morta a 78 anni. +Europa ha annunciato la scomparsa nella mattina dell'11 settembre 2026 e ANSA ha rilanciato la comunicazione. Nei giorni precedenti la storica leader radicale era stata ricoverata all'ospedale Santo Spirito di Roma per una crisi respiratoria, prima del trasferimento in una struttura privata.",
        "Al momento dell'annuncio non sono stati resi pubblici il luogo esatto, l'ora del decesso o una causa clinica definitiva. Il precedente ricovero offre la cronologia degli ultimi giorni, ma non consente di attribuire automaticamente la morte a una diagnosi specifica. Eventuali dettagli sanitari richiederanno una comunicazione autorizzata della famiglia, dello staff o dei medici.",
        "Nata a Bra, in provincia di Cuneo, il 9 marzo 1948, Bonino entrò alla Camera per la prima volta nel 1976. La scheda del Senato registra mandati parlamentari distribuiti tra Camera e Palazzo Madama, oltre all'incarico di vicepresidente del Senato dal 2008 al 2013.",
        "La sua attività istituzionale ebbe anche una dimensione europea e internazionale. Fu commissaria europea dal 1995 al 1999, con responsabilità che compresero aiuti umanitari, pesca, politica dei consumatori e sicurezza alimentare. Nel governo Letta ricoprì l'incarico di ministra degli Affari esteri dal 2013 al 2014.",
        "Bonino legò il proprio nome alle battaglie radicali sui diritti civili e alle campagne contro la pena di morte, le mutilazioni genitali femminili e i crimini internazionali. Il profilo storico della Farnesina ricorda il suo impegno per la Corte penale internazionale e la fondazione delle organizzazioni Nessuno Tocchi Caino e Non c'è Pace senza Giustizia.",
        "Il suo percorso attraversò quasi cinquant'anni di politica italiana senza limitarsi agli incarichi elettivi. Europa federale, giustizia internazionale e libertà individuali furono i temi più riconoscibili della sua iniziativa pubblica. La valutazione della sua eredità politica resta distinta dalla cronaca del decesso e si fonda su atti, campagne e incarichi documentati.",
        "La morte chiude una vicenda politica iniziata nella stagione dei referendum sui diritti civili e proseguita nelle istituzioni nazionali ed europee. I prossimi aggiornamenti riguarderanno le comunicazioni della famiglia, di +Europa e delle istituzioni, insieme alle informazioni ufficiali sulle esequie. CurioMondo non pubblicherà dettagli non confermati.",
    ],
    "sources": [
        ["https://www.ansa.it/", "ANSA — 11 settembre 2026 — annuncio della morte diffuso da +Europa"],
        ["https://www.esteri.it/it/ministero/storia/ministri_esteri/emma_bonino/", "Ministero degli Affari Esteri — profilo istituzionale, incarichi e campagne internazionali"],
        ["https://www.senato.it/legislature/16/composizione/senatori/elenco-alfabetico/scheda-attivita?did=321", "Senato della Repubblica — dati anagrafici, mandati e vicepresidenza"],
        ["https://www.europarl.europa.eu/meps/it/1566/EMMA_BONINO/history/1", "Parlamento europeo — archivio dei mandati europei"],
    ],
}

src = (ROOT / "tools/build_v310.py").read_text(encoding="utf-8")
ns = {"__file__": str(ROOT / "tools/build_v310.py")}
exec(src.split("def article(a):", 1)[0], ns)
exec("def article(a):" + src.split("def article(a):", 1)[1].split("registry_path=", 1)[0], ns)
out = ns["article"](ARTICLE)
out = out.replace("8 settembre 2026", "11 settembre 2026")
out = out.replace("?v=310", "?v=323")
out = out.replace(
    '<article class="art-body" data-length-policy="3000-7000">',
    '<article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">',
    1,
)
out = out.replace(
    '<figure class="article-image" data-ai-generated="true">',
    '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="true" data-portrait-format="neutral-isolated">',
    1,
)
schema_marker = '"creditText":' + json.dumps(CAPTION, ensure_ascii=False, separators=(",", ":"))
out = out.replace(
    schema_marker,
    schema_marker + ',"contentCredentials":"AI-generated neutral isolated synthetic likeness of a public figure in a sensitive obituary context"',
    1,
)
(ROOT / "notizie" / f"{ARTICLE['slug']}.html").write_text(out, encoding="utf-8")

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
variants = []
for width in (480, 800, 1200):
    image = ROOT / "assets/images/editorial-auto" / f"{ARTICLE['key']}-{width}.webp"
    variants.append({
        "w": width,
        "src": f"/assets/images/editorial-auto/{image.name}",
        "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
        "bytes": image.stat().st_size,
    })
registry["items"] = [i for i in registry["items"] if i.get("key") != ARTICLE["key"] and i.get("article") != f"/notizie/{ARTICLE['slug']}.html"]
registry["items"].insert(0, {
    "key": ARTICLE["key"],
    "article": f"/notizie/{ARTICLE['slug']}.html",
    "aiGenerated": True,
    "sensitiveContext": True,
    "documentaryPhoto": False,
    "variants": variants,
    "alt": ARTICLE["alt"],
    "disclosure": CAPTION,
    "portraitOnly": True,
    "portraitFormat": "neutral-isolated",
    "syntheticLikeness": "public-figure",
    "publicFigure": ARTICLE["public_figure"],
    "prompt": "Sensitive obituary context: neutral editorial portrait of Emma Bonino, isolated head-and-shoulders composition on a simple blue-gray studio background; no hospital, funeral, suffering, text or documentary reenactment.",
    "reenactedEvent": False,
})
registry["version"] = VERSION
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

runpy.run_path(str(ROOT / "tools/finalize_articles_20260906.py"), run_name="__main__")
runpy.run_path(str(ROOT / "tools/generate_category_pages.py"), run_name="__main__")

for rel in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_site_version"] = VERSION
manifest["site"]["site_version"] = VERSION
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for rel in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
    path = ROOT / rel
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if "site_version" in data:
            data["site_version"] = VERSION
        if "version" in data:
            data["version"] = str(VERSION)
        data["articleCount"] = 255
        data["generatedEditorialImages"] = 137
        data["last_daily_question_date"] = "2026-09-11"
        data["last_update"] = "emma-bonino-morta-78-anni-v323"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"status": "ok", "version": VERSION, "article": ARTICLE["slug"]}, ensure_ascii=False, indent=2))
