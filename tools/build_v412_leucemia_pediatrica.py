#!/usr/bin/env python3
"""Pubblica i risultati dello studio AIEOP-BFM ALL 2017 sulla leucemia pediatrica."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 412
PUBLISHED = "2026-09-17T17:53:48+02:00"
DEVELOPMENT = "2026-09-17T14:35:00+02:00"
SLUG = "leucemia-pediatrica-immunoterapia-blinatumomab-studio-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "leucemia-pediatrica-immunoterapia-2026.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Leucemia pediatrica, immunoterapia riduce le recidive dal 21,4% all'11,8%",
    "sommario": "Nel trial AIEOP-BFM ALL 2017, due cicli di blinatumomab al posto di due blocchi di chemioterapia intensiva hanno migliorato la sopravvivenza libera da eventi nei bambini con leucemia linfoblastica acuta B ad alto rischio.",
    "categoria": "Italia",
    "luogo": "Monza / Italia",
    "formato": "standard",
    "parole_chiave_titolo": ["leucemia pediatrica", "immunoterapia", "recidive"],
    "dati_chiave": [
        {"icona": "◆", "valore": "709", "etichetta": "pazienti randomizzati"},
        {"icona": "↘", "valore": "11,8%", "etichetta": "recidive stimate a quattro anni"},
        {"icona": "●", "valore": "83%", "etichetta": "sopravvivenza libera da eventi a quattro anni"},
    ],
    "paragrafi": [
        "Due cicli di immunoterapia con blinatumomab, usati al posto di due blocchi di chemioterapia intensiva, hanno ridotto le recidive nei bambini e negli adolescenti con leucemia linfoblastica acuta a cellule B appena diagnosticata e classificata ad alto rischio.",
        "Il risultato arriva dallo studio internazionale di fase 3 AIEOP-BFM ALL 2017, pubblicato sul New England Journal of Medicine e coordinato in Italia dalla rete AIEOP con la Fondazione Tettamanti di Monza.",
        "Il trial ha assegnato in modo casuale 709 pazienti idonei: 358 hanno ricevuto due cicli di 28 giorni di blinatumomab, insieme al metotrexato intratecale previsto dal protocollo, mentre 351 hanno proseguito con due blocchi standard di chemioterapia intensiva. L'analisi riguarda quindi una popolazione selezionata ad alto rischio e non tutti i bambini con leucemia linfoblastica acuta.",
        "A quattro anni, la sopravvivenza libera da eventi è stata stimata all'83% nel gruppo blinatumomab e al 70,3% nel gruppo chemioterapia. L'incidenza cumulativa delle ricadute è risultata dell'11,8% contro il 21,4%: 31 recidive nel gruppo sperimentale e 57 nel gruppo di controllo.",
        "Il rapporto di rischio per l'esito principale è stato 0,51, dato compatibile con una riduzione sostanziale del rischio nel periodo osservato. La sopravvivenza complessiva a quattro anni è stata del 93,6% contro il 91%, una differenza numerica più contenuta.",
        "Il beneficio ha riguardato anche la tossicità durante la fase randomizzata. Le infezioni clinicamente rilevanti sono state osservate nel 23,9% dei pazienti trattati con blinatumomab e nel 69,4% di quelli sottoposti ai due blocchi chemioterapici.",
        "La mucosite grave è scesa dal 10% allo 0,3%. Nessuna infezione potenzialmente letale è stata registrata nel gruppo blinatumomab, contro undici nel controllo. Gli eventi neurologici sono però comparsi più spesso con l'immunoterapia, nel 12% dei pazienti contro il 3,2%, anche se le complicanze neurologiche gravi sono rimaste rare.",
        "Il blinatumomab è un anticorpo bispecifico: si lega alla proteina CD19 presente sulle cellule leucemiche B e contemporaneamente ai linfociti T, avvicinando le difese immunitarie al bersaglio tumorale. Nello studio non ha eliminato l'intero percorso chemioterapico, ma ha sostituito due dei blocchi più intensivi all'interno di una terapia articolata.",
        "Per l'Italia, la Fondazione Tettamanti ha svolto il ruolo di centro nazionale di coordinamento, occupandosi fra l'altro di gestione del protocollo, farmacovigilanza e analisi dei dati. Hanno contribuito anche l'Oncologia pediatrica dell'Università di Padova e la Fondazione Città della Speranza; nel complesso la sperimentazione ha coinvolto oltre cento centri in otto Paesi.",
        "La pubblicazione sottoposta a revisione scientifica consolida dati già presentati al congresso europeo di ematologia nel giugno 2026. I risultati sostengono l'integrazione anticipata dell'immunoterapia per questa specifica fascia ad alto rischio, ma non equivalgono a una raccomandazione valida per ogni paziente: applicazione clinica, indicazioni e monitoraggio devono dipendere dai protocolli oncologici e dalla valutazione specialistica.",
    ],
    "fonti": [
        {"url": "https://www.nejm.org/doi/full/10.1056/NEJMoa2604166", "descrizione": "New England Journal of Medicine — studio di fase 3 AIEOP-BFM ALL 2017, pubblicato il 16 settembre 2026."},
        {"url": "https://fondazionetettamanti.it/2026/09/17/leucemia-linfoblastica-acuta-pediatrica-ad-alto-rischio-limmunoterapia-dimezza-le-recidive-e-riduce-gli-effetti-collaterali-gravi/", "descrizione": "Fondazione Tettamanti — ruolo italiano, rete dei centri e contesto clinico della sperimentazione."},
        {"url": "https://www.ansa.it/canale_saluteebenessere/notizie/salute_bambini/news/2026/09/17/leucemia-acuta-pediatrica-limmunoterapia-dimezza-le-recidive_b3701232-43ac-4a80-86c9-a243c2af79e1.html", "descrizione": "ANSA — conferma indipendente della pubblicazione e del contributo della rete italiana."},
        {"url": "https://www.quotidianosanita.it/scienza-e-farmaci/leucemia-pediatrica-ad-alto-rischio-limmunoterapia-dimezza-le-recidive-lo-studio-che-ha-coinvolto-litalia/", "descrizione": "Quotidiano Sanità — verifica indipendente di disegno, risultati e limiti dello studio."},
        {"url": "https://oncodaily.com/hematology/blinatumomab-all-eha2026-520664", "descrizione": "OncoDaily — dati dettagliati della presentazione scientifica EHA 2026, usati come contesto per sicurezza e sottogruppi."},
    ],
    "correlati": [
        {"url": "/notizie/melanoma-vaccino-personalizzato-mrna-moderna-merck-fase-3-19-agosto-2026.html", "titolo": "Melanoma, vaccino personalizzato a mRNA entra in fase 3"},
        {"url": "/notizie/vaccini-oncologici-personalizzati-mrna-come-funzionano.html", "titolo": "Vaccini oncologici personalizzati: come funzionano"},
        {"url": "/notizie/sardegna-legge-minori-diabete-tipo-1-scuola-sport-17-settembre-2026.html", "titolo": "Diabete tipo 1, la Sardegna approva una legge per i minori"},
    ],
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_image_variants() -> list[dict]:
    image = Image.open(SOURCE_IMAGE).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets" / "images" / "editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(),
        "alt": "Illustrazione editoriale generata con IA di un laboratorio oncologico con provette, microscopio e pompa d'infusione; scena concettuale non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "prompt": "Ultrarealistic conceptual pediatric oncology research laboratory with sample tubes and infusion pump; no patient, text, logos or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page_path.write_text(page, encoding="utf-8")

    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Italia",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": DEVELOPMENT,
        "status": "CONFERMATA DA PIÙ FONTI",
        "public_url": PUBLIC_URL,
        "publication_state": "pending_deploy",
        "body": ARTICLE["paragrafi"],
        "sources": ARTICLE["fonti"],
        "image": image,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Pubblicati i risultati dello studio AIEOP-BFM ALL 2017 sulla leucemia pediatrica",
        "image_policy_applied": "new-openai-conceptual-editorial-image-no-text-no-logo-no-patient",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-17",
            "release_date": "2026-09-17",
            "articleCount": int(state.get("articleCount", 0)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
            "last_update": "salute-leucemia-pediatrica-immunoterapia-v412",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T175348-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Salute e scienza",
        "production_branch": "main",
        "base_commit": "08cc848053279c2498851085fa7e95adf2b8a706",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 12,
            "distinct_domains": 9,
            "target_reached": False,
            "note": "Conteggio prudenziale: il target di 500 contenuti non è stato raggiunto e non è stato inventato. Sono stati letti il lavoro NEJM, la documentazione della Fondazione Tettamanti e conferme sanitarie indipendenti; le altre candidate sono state escluse per rilevanza, territorialità o assenza di conferme.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.6,
            "status": "CONFERMATA DA PIÙ FONTI",
            "decision": "publish",
            "sources": [x["url"] for x in ARTICLE["fonti"]],
            "public_url": f"https://curiomondo.it/notizie/{SLUG}",
            "publication_state": "pending_deploy",
        }],
        "discarded": [
            {"title": "Bambino di cinque anni precipita da un balcone a Montelanico", "reason": "grave fatto locale, ma una sola fonte disponibile e rilevanza nazionale sotto soglia"},
            {"title": "Visita di Giorgia Meloni in Norvegia", "reason": "agenda diplomatica senza accordi o atti conclusivi documentati al momento del controllo"},
            {"title": "Piano nazionale per la sicurezza del paziente", "reason": "attività preparatoria annunciata, senza piano adottato né testo disponibile"},
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
