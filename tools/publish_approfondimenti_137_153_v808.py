#!/usr/bin/env python3
"""Pubblica gli approfondimenti 137 e 153 sulle superfici CurioMondo correnti.

Il manifest storico è volutamente escluso: contiene istruzioni ritirate e viene
ignorato dai gate con --exclude-manifest. Lo script non esegue commit o push.
"""
import hashlib
import json
import math
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import etree, html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-137-153-v808"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
VERSION = 808

GUIDES = [
    {
        "number": 137,
        "slug": "firewall-aziendale-hardware-o-cloud",
        "title": "Firewall aziendale: hardware, cloud o soluzione ibrida",
        "description": "Come confrontare capacità reale, VPN, IDS/IPS, alta affidabilità, licenze, gestione e costo totale senza fermarsi al prezzo di listino.",
        "category": "Tecnologia e digitale",
        "body": "firewall-body.txt",
        "alt": "Tecnico di rete davanti a un firewall fisico in rack e a una console cloud; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero: network administrator facing camera beside a rack-mounted firewall and a cloud-managed security console in a real small-business server room; no logos, no readable text, no watermark, no split screen.",
        "points": [
            "La scelta parte dai flussi: sede, cloud, filiali e utenti remoti richiedono punti di controllo diversi.",
            "Il throughput va confrontato con IPS, VPN e ispezione realmente attivi, non sul solo dato di targa.",
            "Il costo totale comprende alta affidabilità, licenze, log, supporto, traffico e ore di gestione.",
            "Per molte PMI la soluzione più coerente è ibrida, purché policy e responsabilità restino unificate.",
        ],
        "disclaimer": "Guida informativa di sicurezza informatica: non sostituisce un'analisi tecnica, un test di rete o un progetto redatto da professionisti qualificati.",
        "related": [
            "/approfondimenti/fibra-aziende-costi-sla.html",
            "/approfondimenti/phishing-smishing-vishing-come-riconoscere-truffe.html",
            "/approfondimenti/software-sms-marketing-costi-funzionalita.html",
        ],
        "sources": [
            ("https://csrc.nist.gov/pubs/sp/800/41/r1/final", "NIST — SP 800-41 Rev. 1: tecnologie, policy, selezione, test e gestione dei firewall."),
            ("https://aws.amazon.com/network-firewall/pricing/", "AWS — struttura dei prezzi Network Firewall ed esempi con endpoint, zone e traffico elaborato."),
            ("https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html", "AWS — documentazione del servizio firewall gestito, ispezione stateful e protezione delle VPC."),
            ("https://azure.microsoft.com/it-it/pricing/details/azure-firewall/", "Microsoft Azure — componenti di prezzo del firewall cloud: distribuzione, dati e capacità opzionale."),
        ],
    },
    {
        "number": 153,
        "slug": "software-sms-marketing-costi-funzionalita",
        "title": "Software SMS marketing: costi, consenso e funzioni da valutare",
        "description": "Segmenti, codifica, mittente, automazioni, API, report e revoche: il metodo per stimare la spesa e confrontare piattaforme in Italia.",
        "category": "Tecnologia e digitale",
        "body": "sms-body.txt",
        "alt": "Professionista del marketing con laptop e telefoni che mostrano notifiche senza testo; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero: marketing professional facing camera at an Italian small-business desk with laptop, several phones showing blank notification cards, and clear scheduling-segmentation-delivery workflow cues; no logos, no readable text, no watermark, no split screen.",
        "points": [
            "Il costo dipende dai segmenti: codifica, simboli ed emoji possono moltiplicare le unità addebitate.",
            "Per gli SMS promozionali in Italia serve un consenso specifico e dimostrabile; il vecchio rapporto contrattuale non basta.",
            "Alias, numero mobile e gestione delle risposte cambiano fiducia, opt-out, funzionalità e prezzo.",
            "API, webhook, ruoli, limiti di spesa e portabilità contano quanto editor e report della campagna.",
        ],
        "disclaimer": "Guida informativa su software e processi di marketing: non sostituisce una valutazione legale o privacy sul singolo trattamento e sulla relativa campagna.",
        "related": [
            "/approfondimenti/phishing-smishing-vishing-come-riconoscere-truffe.html",
            "/approfondimenti/firewall-aziendale-hardware-o-cloud.html",
            "/approfondimenti/fibra-aziende-costi-sla.html",
        ],
        "sources": [
            ("https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10199166", "Garante privacy — provvedimento 23 ottobre 2025: consenso per SMS promozionali e limiti del legittimo interesse."),
            ("https://garanteprivacy.it/home/docweb/-/docweb-display/docweb/10262367", "Garante privacy — provvedimento 14 maggio 2026: controllo della filiera, consensi e dati acquisiti da terzi."),
            ("https://www.agcom.it/competenze/comunicazioni-elettroniche/reti/numerazione/piano-di-numerazione/alias", "AGCOM — disciplina e Registro degli Alias per la messaggistica aziendale."),
            ("https://www.agcom.it/provvedimenti/delibera-12-23-cir", "AGCOM — delibera 12/23/CIR sul quadro a regime degli Alias SMS."),
            ("https://www.twilio.com/en-us/sms/pricing/it", "Twilio — esempio pubblico di prezzi SMS per l'Italia e voci aggiuntive; condizioni variabili nel tempo."),
            ("https://www.twilio.com/docs/glossary/what-sms-character-limit", "Twilio Docs — limiti GSM-7 e UCS-2, segmentazione e impatto dei caratteri Unicode."),
        ],
    },
]


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def markup(node):
    return html.tostring(node, encoding="unicode", method="html", doctype="<!doctype html>") + "\n"


def fragment(source):
    return html.fragment_fromstring(source)


def faq_payload(body):
    entries = []
    faq = body.xpath('.//h2[@id="faq"]')
    if not faq:
        return entries
    node = faq[0].getnext()
    while node is not None:
        if node.tag == "h3":
            answer = node.getnext()
            if answer is not None and answer.tag == "p":
                entries.append({
                    "@type": "Question",
                    "name": node.text_content().strip(),
                    "acceptedAnswer": {"@type": "Answer", "text": answer.text_content().strip()},
                })
        node = node.getnext()
    return entries


def build_page(guide, published_at):
    template = ROOT / "approfondimenti/fibra-aziende-costi-sla.html"
    doc = html.fromstring(template.read_text(encoding="utf-8"))
    canonical = f"https://curiomondo.it/approfondimenti/{guide['slug']}.html"
    image_url = f"https://curiomondo.it/assets/images/editorial-auto/{guide['slug']}-v{VERSION}-1200.webp"
    doc.xpath("//body")[0].set("data-article-id", guide["slug"])
    doc.xpath("//title")[0].text = guide["title"] + " | CurioMondo"
    doc.xpath('//link[@rel="canonical"]')[0].set("href", canonical)
    values = {
        "description": guide["description"],
        "og:title": guide["title"],
        "og:description": guide["description"],
        "og:url": canonical,
        "og:image": image_url,
        "og:image:alt": guide["alt"],
    }
    for meta in doc.xpath("//meta"):
        key = meta.get("name") or meta.get("property")
        if key in values:
            meta.set("content", values[key])
    article_schema = None
    for script in list(doc.xpath('//script[@type="application/ld+json"]')):
        data = json.loads(script.text)
        if data.get("@type") == "Article" and article_schema is None:
            article_schema = script
            data.update(
                headline=guide["title"],
                description=guide["description"],
                datePublished=published_at,
                dateModified=published_at,
                mainEntityOfPage=canonical,
                image=[image_url],
                articleSection=guide["category"],
            )
            data["author"] = {"@type": "Organization", "name": "Redazione CurioMondo", "url": "https://curiomondo.it/pagine/redazione.html"}
            data["publisher"] = {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}}
            data["creditText"] = CAPTION
            script.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        else:
            script.getparent().remove(script)
    main = doc.xpath("//main")[0]
    main.xpath('./div[@class="badge"]')[0].text = "Approfondimento · " + guide["category"]
    main.xpath("./h1")[0].text = guide["title"]
    main.xpath('./p[@class="subtitle"]')[0].text = guide["description"]
    raw = (PAYLOAD / guide["body"]).read_text(encoding="utf-8")
    body = fragment('<article class="art-body" data-editorial-protocol="4.0" data-article-format="feature">' + raw + "</article>")
    words = len(body.text_content().split())
    if words < 2000:
        raise ValueError(f"{guide['slug']}: {words} parole, minimo 2000")
    old_body = main.xpath('./article[@class="art-body"]')[0]
    old_body.getparent().replace(old_body, body)
    stamp = datetime.fromisoformat(published_at).strftime("%d/%m/%Y · %H:%M")
    meta = main.xpath('./div[@class="meta"]')[0]
    meta.clear()
    meta.set("class", "meta")
    meta.text = f"{stamp} · {math.ceil(words / 200)} min di lettura"
    summary = fragment('<section class="cm-summary-box" aria-labelledby="in-sintesi"><h2 id="in-sintesi">In sintesi</h2><ul>' + "".join(f"<li>{item}</li>" for item in guide["points"]) + "</ul></section>")
    old_summary = main.xpath('./section[@class="cm-insight"]')[0]
    main.replace(old_summary, summary)
    figure = main.xpath("./figure")[0]
    figure.set("data-ai-generated", "true")
    figure.set("data-sensitive-context", "false")
    img = figure.xpath(".//img")[0]
    base = f"/assets/images/editorial-auto/{guide['slug']}-v{VERSION}-"
    img.set("src", base + "800.webp")
    img.set("srcset", ", ".join(base + str(width) + ".webp " + str(width) + "w" for width in (480, 800, 1200)))
    img.set("alt", guide["alt"])
    figure.xpath("./figcaption")[0].text = CAPTION
    for related in main.xpath('./section[@class="curio-related"]'):
        main.remove(related)
    related = fragment('<section class="curio-related" data-curated-related="true"><h2>Per continuare</h2><div class="curio-related-grid"></div></section>')
    grid = related.xpath("./div")[0]
    for url in guide["related"]:
        page = ROOT / url.lstrip("/")
        if not page.exists() and url.endswith(".html") and url == f"/approfondimenti/{guide['slug']}.html":
            continue
        if page.exists():
            related_doc = html.fromstring(page.read_text(encoding="utf-8"))
            title = related_doc.xpath("//h1")[0].text_content().strip()
        else:
            other = next((g for g in GUIDES if url == f"/approfondimenti/{g['slug']}.html"), None)
            if not other:
                continue
            title = other["title"]
        link = etree.SubElement(grid, "a", href=url)
        etree.SubElement(link, "small").text = "Approfondimento collegato"
        etree.SubElement(link, "strong").text = title
    body.addnext(related)
    sources = main.xpath('./div[@class="art-sources"]')[0]
    sources.clear()
    sources.set("class", "art-sources")
    etree.SubElement(sources, "h2").text = "Fonti consultate"
    ul = etree.SubElement(sources, "ul")
    for url, label in guide["sources"]:
        etree.SubElement(etree.SubElement(ul, "li"), "a", href=url, rel="noopener noreferrer", target="_blank").text = label
    p = etree.SubElement(sources, "p")
    p.text = f"Redazione CurioMondo · Testo originale. Ultimo aggiornamento editoriale: {stamp} (ora italiana). "
    etree.SubElement(p, "a", href="/pagine/metodo-editoriale.html").text = "Come lavoriamo"
    etree.SubElement(sources, "p").text = guide["disclaimer"]
    etree.SubElement(sources, "p").text = CAPTION
    faq = etree.Element("script", type="application/ld+json")
    faq.text = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_payload(body)}, ensure_ascii=False, separators=(",", ":"))
    article_schema.addnext(faq)
    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css?v=")]'):
        link.set("href", re.sub(r"\?v=\d+", f"?v={VERSION}", link.get("href")))
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js?v=")]'):
        script.set("src", re.sub(r"\?v=\d+", f"?v={VERSION}", script.get("src")))
    (ROOT / "approfondimenti" / f"{guide['slug']}.html").write_text(markup(doc), encoding="utf-8")


def sync_index():
    path = ROOT / "approfondimenti/index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for guide in GUIDES:
        url = f"../approfondimenti/{guide['slug']}.html"
        for old in doc.xpath(f'//a[@class="card" and @href="{url}"]'):
            old.getparent().remove(old)
        section = next(section for section in doc.xpath('//section[contains(@class,"cat-section")]') if section.xpath("./h2")[0].text_content() == guide["category"])
        card = etree.Element("a", {"class": "card", "data-cm-cat": guide["category"], "data-cm-evergreen-slug": guide["slug"], "href": url})
        etree.SubElement(card, "span", {"class": "tag"}).text = guide["category"]
        text = etree.SubElement(card, "div")
        etree.SubElement(text, "h2").text = guide["title"]
        etree.SubElement(text, "p").text = guide["description"]
        etree.SubElement(card, "b").text = "Leggi l’approfondimento →"
        section.xpath('./div[@class="grid"]')[0].insert(0, card)
    for section in doc.xpath('//section[contains(@class,"cat-section")]'):
        count = len(section.xpath('.//a[@class="card"]'))
        for small in doc.xpath(f'//a[@href="#{section.get("id", "")}"]//small'):
            small.text = f"({count})"
    path.write_text(markup(doc), encoding="utf-8")


def sync_search():
    path = ROOT / "assets/data/search-index-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    urls = {f"/approfondimenti/{g['slug']}.html" for g in GUIDES}
    new = [{"title": g["title"], "excerpt": g["description"], "url": f"/approfondimenti/{g['slug']}.html", "section": "Approfondimenti / " + g["category"]} for g in GUIDES]
    data["items"] = new + [item for item in data["items"] if item.get("url") not in urls]
    data["version"] = VERSION
    dump(path, data)


def sync_sitemap(day):
    path = ROOT / "sitemap.xml"
    tree = etree.parse(str(path))
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    wanted = {f"https://curiomondo.it/approfondimenti/{g['slug']}.html" for g in GUIDES}
    for node in list(tree.getroot()):
        if node.findtext(f"{{{namespace}}}loc") in wanted:
            tree.getroot().remove(node)
    for guide in GUIDES:
        node = etree.SubElement(tree.getroot(), f"{{{namespace}}}url")
        for key, value in (("loc", f"https://curiomondo.it/approfondimenti/{guide['slug']}.html"), ("lastmod", day), ("changefreq", "monthly"), ("priority", "0.8")):
            etree.SubElement(node, f"{{{namespace}}}{key}").text = value
    tree.write(str(path), encoding="utf-8", xml_declaration=True)


def sync_redirects():
    path = ROOT / "_redirects"
    lines = path.read_text(encoding="utf-8").splitlines()
    for guide in GUIDES:
        canonical = f"/approfondimenti/{guide['slug']}.html"
        for source in (f"/approfondimenti/{guide['slug']}", f"/approfondimenti/{guide['slug']}/"):
            if not any(line.split() and line.split()[0] == source for line in lines):
                lines.insert(0, f"{source} {canonical} 301")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sync_images():
    path = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for guide in GUIDES:
        record = {
            "key": f"{guide['slug']}-v{VERSION}",
            "article": f"/approfondimenti/{guide['slug']}.html",
            "alt": guide["alt"],
            "prompt": guide["prompt"],
            "disclosure": CAPTION,
            "generator": "OpenAI image generation",
            "aiGenerated": True,
            "documentaryPhoto": False,
            "officialArtwork": False,
            "sensitiveContext": False,
            "weatherMap": False,
            "variants": [],
        }
        for width in (480, 800, 1200):
            image = ROOT / "assets/images/editorial-auto" / f"{guide['slug']}-v{VERSION}-{width}.webp"
            with Image.open(image) as opened:
                w, h = opened.size
            record["variants"].append({"w": w, "h": h, "src": "/" + str(image.relative_to(ROOT)), "sha256": hashlib.sha256(image.read_bytes()).hexdigest(), "bytes": image.stat().st_size})
        data["items"] = [item for item in data["items"] if item.get("article") != record["article"]]
        data["items"].insert(0, record)
    data["version"] = VERSION
    dump(path, data)


def sync_states(published_at):
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION, evergreen_added=[g["slug"] for g in GUIDES], last_update="approfondimenti-lista-137-153", updated_at=published_at, release_date=published_at[:10])
        dump(path, data)
    path = ROOT / "automation/state/approfondimenti-lista-500.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"source": "Lista approfondimenti.txt", "items": []}
    for guide in GUIDES:
        data["items"] = [item for item in data["items"] if item.get("number") != guide["number"]]
        data["items"].append({"number": guide["number"], "title": guide["title"], "url": f"/approfondimenti/{guide['slug']}.html", "status": "published", "selected_at": published_at})
    dump(path, data)


def main():
    published_at = datetime.now(ZoneInfo("Europe/Rome")).isoformat(timespec="seconds")
    for guide in GUIDES:
        build_page(guide, published_at)
    sync_index()
    sync_search()
    sync_sitemap(published_at[:10])
    sync_redirects()
    sync_images()
    sync_states(published_at)
    subprocess.run(["node", "tools/render_home_editorial.js"], cwd=ROOT, check=True)
    print(json.dumps({"published": [g["slug"] for g in GUIDES], "version": VERSION, "datePublished": published_at, "manifest": "excluded"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
