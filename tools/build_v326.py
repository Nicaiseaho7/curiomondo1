#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 326
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

ARTICLE = {
    "slug": "usa-inflazione-agosto-34-percento-fed-tassi-11-settembre-2026",
    "title": "USA, inflazione al 3,4% in agosto: aumenta la pressione sulla Fed",
    "excerpt": "I prezzi crescono dello 0,4% nel mese, spinti soprattutto dalla benzina. Il dato di fondo sale più delle attese prima della riunione della Federal Reserve.",
    "published": "2026-09-11T19:52:00+02:00",
    "category": "Mondo / Economia / Stati Uniti",
    "place": "Washington",
    "key": "usa-inflazione-agosto-fed-tassi-ai-openai-v326",
    "alt": "Scena editoriale contestuale generata con IA di una consumatrice a un distributore statunitense, con spesa nell'auto e Campidoglio sullo sfondo",
    "points": [("+0,4%", "l'aumento mensile dei prezzi"), ("3,4%", "l'inflazione su dodici mesi"), ("15–16 settembre", "la prossima riunione della Fed")],
    "body": [
        "I prezzi al consumo negli Stati Uniti sono aumentati dello 0,4% in agosto e del 3,4% su base annua. Il Bureau of Labor Statistics ha pubblicato i dati l'11 settembre. L'accelerazione mensile, dopo il +0,1% di luglio, rafforza le attese di un aumento dei tassi nella riunione della Federal Reserve del 15 e 16 settembre.",
        "La benzina è cresciuta del 3,9% nel mese e ha spiegato più di un terzo dell'incremento complessivo. Gli altri carburanti per motori, compreso il diesel, sono saliti del 9,6%. Il rincaro dell'energia riflette anche le tensioni sulle forniture petrolifere, ma il dato non permette di attribuire ogni variazione a una sola causa.",
        "Al netto di alimentari ed energia, i prezzi sono aumentati dello 0,3%, contro il +0,2% previsto nel sondaggio Reuters. Su dodici mesi questa componente ha rallentato dal 2,5% al 2,4%. Il quadro è quindi misto: la misura annua migliora leggermente, mentre il passo mensile segnala pressioni più ampie di quanto atteso.",
        "Tra le voci in aumento compaiono abitazioni, servizi telefonici, voli, istruzione e veicoli usati. I prezzi alimentari sono cresciuti dello 0,1% per il secondo mese consecutivo, mentre la spesa nei supermercati è rimasta invariata. Questa differenza mostra perché l'indice generale non descrive allo stesso modo il bilancio di ogni famiglia.",
        "Il 3,4% annuo confronta il livello medio dei prezzi con agosto 2025 e non significa che ogni bene costi il 3,4% in più. Pesi di spesa, area geografica e consumi personali modificano l'esperienza concreta. Inoltre l'indice misura la variazione dei prezzi, non il livello raggiunto dopo gli aumenti accumulati negli anni precedenti.",
        "Reuters riferisce che i salari reali sono diminuiti per il quinto mese consecutivo. Il confronto tra retribuzioni e prezzi è rilevante perché misura quanto potere d'acquisto resta dopo l'inflazione. Un indice stabile su base annua può quindi continuare a pesare sui consumatori se le entrate crescono più lentamente.",
        "La Federal Reserve non usa il solo indice dei prezzi al consumo per fissare i tassi. Preferisce un'altra misura dell'inflazione e valuta anche lavoro, domanda e condizioni finanziarie. Il calendario ufficiale conferma la decisione per il 16 settembre; l'esito resta una scelta del comitato, non una conseguenza automatica del rapporto di agosto.",
        "Per mercati e famiglie, un eventuale rialzo renderebbe più costoso il credito a breve termine e potrebbe trasferirsi a prestiti, carte e nuovi mutui. L'effetto sui singoli contratti dipenderà però da durata, tasso e condizioni bancarie. I prossimi passaggi verificabili sono la decisione della Fed e la pubblicazione della misura dei prezzi preferita dalla banca centrale."
    ],
    "sources": [
        ["https://www.bls.gov/news.release/cpi.nr0.htm", "Bureau of Labor Statistics — 11 settembre 2026 — indice dei prezzi, componenti mensili e variazioni annuali"],
        ["https://www.reuters.com/world/us/us-consumer-inflation-picks-up-august-2026-09-11/", "Reuters — 11 settembre 2026 — attese degli economisti, salari reali e implicazioni per la Federal Reserve"],
        ["https://apnews.com/article/8c3272812f5e9b9238c6a3301921c17a", "Associated Press — 11 settembre 2026 — reazione dei mercati e prezzi dell'energia"],
        ["https://www.federalreserve.gov/newsevents/2026-september.htm", "Federal Reserve — calendario ufficiale della riunione del 15–16 settembre 2026"]
    ]
}

source = (ROOT / "tools/build_v310.py").read_text(encoding="utf-8")
namespace = {"__file__": str(ROOT / "tools/build_v310.py")}
exec(source.split("def article(a):", 1)[0], namespace)
exec("def article(a):" + source.split("def article(a):", 1)[1].split("registry_path=", 1)[0], namespace)
html = namespace["article"](ARTICLE)
html = html.replace("8 settembre 2026", "11 settembre 2026").replace("?v=310", "?v=326")
html = html.replace('<figure class="article-image" data-ai-generated="true">', '<figure class="article-image" data-ai-generated="true" data-sensitive-context="false">', 1)
html = html.replace('<article class="art-body" data-length-policy="3000-7000">', '<article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">', 1)
html = html.replace('<a href="/approfondimenti/"><small>Contesto</small><strong>Gli approfondimenti</strong></a>', '<a href="/approfondimenti/payroll-usa-come-influenzano-fed-e-tassi.html"><small>Approfondimento</small><strong>Come lavoro e inflazione influenzano le decisioni della Fed</strong></a>')
(ROOT / "notizie" / f"{ARTICLE['slug']}.html").write_text(html, encoding="utf-8")

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
variants = []
for width in (480, 800, 1200):
    image = ROOT / "assets/images/editorial-auto" / f"{ARTICLE['key']}-{width}.webp"
    variants.append({"w": width, "src": f"/assets/images/editorial-auto/{image.name}", "sha256": hashlib.sha256(image.read_bytes()).hexdigest(), "bytes": image.stat().st_size})
registry["items"] = [item for item in registry["items"] if item.get("article") != f"/notizie/{ARTICLE['slug']}.html"]
registry["items"].insert(0, {"key": ARTICLE["key"], "article": f"/notizie/{ARTICLE['slug']}.html", "aiGenerated": True, "sensitiveContext": False, "documentaryPhoto": False, "variants": variants, "alt": ARTICLE["alt"], "disclosure": CAPTION, "portraitOnly": False, "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False})
registry["version"] = VERSION
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

runpy.run_path(str(ROOT / "tools/finalize_articles_20260906.py"), run_name="__main__")
runpy.run_path(str(ROOT / "tools/generate_category_pages.py"), run_name="__main__")
for rel in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8")); data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_site_version"] = VERSION; manifest["site"]["site_version"] = VERSION
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
    path = ROOT / rel
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if "site_version" in data: data["site_version"] = VERSION
        if "version" in data: data["version"] = str(VERSION)
        data["articleCount"] = 257; data["generatedEditorialImages"] = 139
        data["last_update"] = "usa-inflazione-agosto-fed-tassi-v326"; data["last_daily_question_date"] = "2026-09-12"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "ok", "version": VERSION, "article": ARTICLE["slug"]}, ensure_ascii=False))
