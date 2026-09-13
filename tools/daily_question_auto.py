#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import json
import os
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
ROME = ZoneInfo("Europe/Rome")
BASE_URL = "https://curiomondo.it"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


MONTHS = {
    1: ("GEN", "gennaio"),
    2: ("FEB", "febbraio"),
    3: ("MAR", "marzo"),
    4: ("APR", "aprile"),
    5: ("MAG", "maggio"),
    6: ("GIU", "giugno"),
    7: ("LUG", "luglio"),
    8: ("AGO", "agosto"),
    9: ("SET", "settembre"),
    10: ("OTT", "ottobre"),
    11: ("NOV", "novembre"),
    12: ("DIC", "dicembre"),
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write_text(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


def write_json(path: str, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:110].strip("-") or "domanda-del-giorno"


def italian_date(dt: datetime) -> str:
    return f"{dt.day} {MONTHS[dt.month][1]} {dt.year}"


def require_secret(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        print(json.dumps({"status": "blocked", "reason": f"{name}_missing"}, ensure_ascii=False))
        sys.exit(2)
    return value


def load_question_queue() -> list[dict]:
    raw = os.getenv("CURIOMONDO_DAILY_QUESTIONS_JSON", "").strip()
    if not raw:
        private_path = ROOT / "automation/state/daily-questions.json"
        if private_path.exists():
            raw = private_path.read_text(encoding="utf-8")
    if not raw:
        print(json.dumps({
            "status": "blocked",
            "reason": "daily_question_source_missing",
            "message": "Add the private question queue as CURIOMONDO_DAILY_QUESTIONS_JSON."
        }, ensure_ascii=False))
        sys.exit(3)
    queue = json.loads(raw)
    if not isinstance(queue, list):
        raise SystemExit("CURIOMONDO_DAILY_QUESTIONS_JSON must be a JSON array")
    normalized = []
    for item in queue:
        if isinstance(item, str):
            normalized.append({"number": None, "question": item.strip()})
        elif isinstance(item, dict):
            normalized.append({
                "number": item.get("number") or item.get("id"),
                "question": str(item.get("question") or item.get("text") or "").strip(),
            })
    return [item for item in normalized if item["question"]]


def choose_question(manifest: dict) -> dict:
    used = set(manifest.get("daily_state", {}).get("used_question_source_numbers", []))
    used_questions = set()
    for page in (ROOT / "domanda-del-giorno").glob("*/index.html"):
        html = page.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
        if match:
            used_questions.add(re.sub(r"\s+", " ", re.sub(r"<.*?>", "", match.group(1))).strip())

    for item in load_question_queue():
        number = item.get("number")
        question = item["question"]
        if number is not None and number in used:
            continue
        if question in used_questions:
            continue
        return item
    print(json.dumps({"status": "blocked", "reason": "daily_question_queue_exhausted"}, ensure_ascii=False))
    sys.exit(4)


def openai_json(prompt: str) -> dict:
    key = require_secret("OPENAI_API_KEY")
    body = {
        "model": MODEL,
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "daily_question_package",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "excerpt": {"type": "string"},
                        "answer_paragraphs": {
                            "type": "array",
                            "minItems": 6,
                            "maxItems": 10,
                            "items": {"type": "string"}
                        },
                        "book_title": {"type": "string"},
                        "book_deck": {"type": "string"},
                        "book_pages": {
                            "type": "array",
                            "minItems": 6,
                            "maxItems": 10,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "title": {"type": "string"},
                                    "paragraphs": {
                                        "type": "array",
                                        "minItems": 3,
                                        "maxItems": 6,
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["title", "paragraphs"]
                            }
                        }
                    },
                    "required": ["excerpt", "answer_paragraphs", "book_title", "book_deck", "book_pages"]
                }
            }
        }
    }
    req = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return json.loads(content["text"])
    raise SystemExit("OpenAI response did not include output_text")


def make_package(question: str, date_label: str) -> dict:
    prompt = f"""
Sei l'editor premium di CurioMondo.it.

Crea il pacchetto editoriale per la Domanda del giorno del {date_label}.

Domanda canonica, da non modificare:
{question}

Regole:
- italiano naturale, profondo, chiaro, non motivazionale generico;
- la risposta breve deve essere tra 1000 e 3000 caratteri complessivi;
- nessun sottotitolo H2/H3 nella risposta della pagina Domanda del giorno;
- l'eBook deve essere sostanzioso, diviso in pagine con titoli, senza effetto sfoglia;
- niente riferimenti a IA, prompt, automazioni o fonti private.
"""
    package = openai_json(prompt)
    answer_len = len(" ".join(package["answer_paragraphs"]))
    if not 1000 <= answer_len <= 3000:
        raise SystemExit(f"Answer length outside gate: {answer_len}")
    return package


def site_header() -> str:
    return '''<header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>'''


def render_question_page(question: str, package: dict, slug: str, date: str, date_label: str, book_url: str) -> str:
    paragraphs = "".join(f"<p>{escape(p)}</p>" for p in package["answer_paragraphs"])
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(question)} | CurioMondo</title><meta name="description" content="{escape(package["excerpt"], quote=True)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="{BASE_URL}/domanda-del-giorno/{slug}/"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=346"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body class="cm-daily-page">{site_header()}<main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{date}">{date_label}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{escape(question)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno">{paragraphs}<a class="cm-daily-book-link" href="{book_url}"><span><small>Continua la riflessione</small><strong>Leggi l'eBook collegato</strong></span><span class="cm-daily-book-arrow" aria-hidden="true">→</span></a></article></main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''


def render_book_page(question_url: str, book_url: str, package: dict) -> str:
    pages = []
    for page in package["book_pages"]:
        body = "".join(f"<p>{escape(p)}</p>" for p in page["paragraphs"])
        pages.append(f'<section class="cm-book-page"><h2>{escape(page["title"])}</h2>{body}</section>')
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(package["book_title"])} | eBook CurioMondo</title><meta name="description" content="{escape(package["book_deck"], quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{BASE_URL}{book_url}"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=346"><link rel="stylesheet" href="/assets/css/biblioteca-book-reader-v1.css?v=273"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body>{site_header()}<main class="cb-shell"><article class="cm-book-shell"><div class="cm-book-stage">{''.join(pages)}</div><nav class="cm-book-controls" aria-label="Navigazione eBook"><button data-book-prev type="button">← Indietro</button><button data-book-next type="button">Avanti →</button></nav><a class="cm-book-back" href="{question_url}">← Torna alla Domanda del giorno</a></article></main><noscript><style>.cm-book-page{{display:block!important;min-height:0;margin-bottom:20px}}</style></noscript><script defer src="/assets/js/biblioteca-book-reader-v1.js?v=273"></script><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def update_home(slug: str, dt: datetime, date_label: str) -> None:
    html = read_text("index.html")
    short_month = MONTHS[dt.month][0]
    section = (
        f'<section class="cm-qday" aria-label="Domanda del giorno">'
        f'<a aria-label="Scopri la Domanda del giorno del {date_label}" class="cm-qday-link" href="/domanda-del-giorno/{slug}/">'
        f'<div class="cm-qday-card"><time class="cm-qday-date" datetime="{dt.date().isoformat()}"><strong>{dt.day}</strong><span>{short_month} · {dt.year}</span></time>'
        f'<span class="cm-qday-k">Domanda del giorno</span><span class="cm-qday-cta">Scopri <i aria-hidden="true">→</i></span></div></a></section>'
    )
    html, count = re.subn(r'<section class="cm-qday"[^>]*>.*?</section>', section, html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("cm-qday card not found")
    write_text("index.html", html)


def update_archive(question: str, package: dict, slug: str, date_label: str) -> None:
    html = read_text("domanda-del-giorno/index.html")
    href = f"/domanda-del-giorno/{slug}/"
    if href in html:
        return
    card = f'<a class="cb-subcard" href="{href}"><span class="cb-kicker">{escape(date_label)}</span><h2>{escape(question)}</h2><p>{escape(package["excerpt"])}</p><b>Leggi →</b></a>'
    html = html.replace('<section class="cb-subgrid">', '<section class="cb-subgrid">' + card, 1)
    write_text("domanda-del-giorno/index.html", html)


def update_search(question: str, package: dict, qurl: str, book_url: str) -> None:
    path = "assets/data/search-index-v210.json"
    data = read_json(path)
    data["items"] = [item for item in data.get("items", []) if item.get("url") not in {qurl, book_url}]
    data["items"].insert(0, {"title": question, "excerpt": package["excerpt"], "url": qurl, "section": "Domanda del giorno"})
    data["items"].insert(1, {"title": package["book_title"], "excerpt": package["book_deck"], "url": book_url, "section": "Biblioteca / Vita e relazioni"})
    data["version"] = int(data.get("version", 346)) + 1
    write_json(path, data)


def update_sitemap(date: str, qurl: str, book_url: str) -> None:
    xml = read_text("sitemap.xml")
    for url, priority in ((BASE_URL + qurl, "0.7"), (BASE_URL + book_url, "0.6")):
        if url not in xml:
            block = f"  <url><loc>{url}</loc><lastmod>{date}</lastmod><changefreq>daily</changefreq><priority>{priority}</priority></url>\n"
            xml = xml.replace("</urlset>", block + "</urlset>")
    write_text("sitemap.xml", xml)


def update_feed(dt: datetime, question: str, package: dict, qurl: str) -> None:
    path = ROOT / "feed.xml"
    if not path.exists():
        return
    xml = path.read_text(encoding="utf-8")
    full = BASE_URL + qurl
    if full in xml:
        return
    item = (
        f"<item><title>{escape(question)}</title><link>{full}</link><guid>{full}</guid>"
        f"<pubDate>{format_datetime(dt)}</pubDate><description>{escape(package['excerpt'])}</description></item>"
    )
    xml = xml.replace("<channel>", "<channel>" + item, 1)
    path.write_text(xml, encoding="utf-8")


def update_state(dt: datetime, slug: str, question: dict) -> None:
    date = dt.date().isoformat()
    manifest = read_json("curiomondo-site-manifest.json")
    version = int(manifest.get("site", {}).get("site_version", 346)) + 1
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    daily = manifest.setdefault("daily_state", {})
    daily["last_question_date"] = date
    daily["last_question_slug"] = slug
    if question.get("number") is not None:
        daily["current_question_source_number"] = question["number"]
        used = daily.setdefault("used_question_source_numbers", [])
        if question["number"] not in used:
            used.append(question["number"])
    write_json("curiomondo-site-manifest.json", manifest)

    for rel in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / rel
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data["currentVersion"] = version
        data["site_version"] = version
        data["version"] = str(version)
        data["date"] = date
        data["release_date"] = date
        data["last_daily_question_date"] = date
        data["last_update"] = f"domanda-del-giorno-{date}"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(ROME)
    date = now.date().isoformat()
    date_label = italian_date(now)
    manifest = read_json("curiomondo-site-manifest.json")
    last_date = manifest.get("daily_state", {}).get("last_question_date")
    if last_date >= date:
        print(json.dumps({"status": "noop", "reason": "daily_question_already_current", "date": date}, ensure_ascii=False))
        return

    question_item = choose_question(manifest)
    question = question_item["question"]
    slug = slugify(question)
    qurl = f"/domanda-del-giorno/{slug}/"
    book_url = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{slug}/"
    package = make_package(question, date_label)

    write_text(f"domanda-del-giorno/{slug}/index.html", render_question_page(question, package, slug, date, date_label, book_url))
    write_text(f"biblioteca/vita-relazioni/domande-per-conoscersi/{slug}/index.html", render_book_page(qurl, book_url, package))
    update_home(slug, now, date_label)
    update_archive(question, package, slug, date_label)
    update_search(question, package, qurl, book_url)
    update_sitemap(date, qurl, book_url)
    update_feed(now, question, package, qurl)
    update_state(now, slug, question_item)

    print(json.dumps({"status": "ok", "date": date, "slug": slug, "question_number": question_item.get("number")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
