#!/usr/bin/env python3
"""Prepara le guide 409 e 67; non esegue commit, push o deploy.

Usa lo stampo vivo e le funzioni di sincronizzazione già presenti nel repo.
Non legge né modifica curiomondo-site-manifest.json.
"""
import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-409-67"
SPEC = importlib.util.spec_from_file_location("publish_base_v808", ROOT / "tools/publish_approfondimenti_137_153_v808.py")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)
base.PAYLOAD = PAYLOAD
SEED = 192231392131643
base.GUIDES = [
    {
        "number": 409,
        "slug": "chirurgia-plastica-confrontare-preventivi-cliniche",
        "title": "Chirurgia plastica: preventivi, qualifiche e assistenza da verificare",
        "description": "Le voci del preventivo, il ruolo del chirurgo, la sede dell’intervento e i controlli: un metodo pratico per confrontare percorsi e costo totale.",
        "category": "Scienza e salute",
        "body": "409-chirurgia-plastica.txt",
        "alt": "Medica e donna adulta confrontano documenti durante un colloquio, con un modello anatomico del naso; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic-natural, 3:2 Italian guide cover: adult woman doctor and client in calm surgery consultation office, both faces visible, comparing two blank quotation sheets beside neutral nose model. No procedure, distress, text, logos, watermark or collage. Conceptual editorial illustration, not a real doctor or clinic. Natural light, realistic anatomy, mobile-safe composition.",
        "points": [
            "Confronta prima il progetto clinico e l’identità dell’operatore: un prezzo iniziale non descrive tutto il percorso.",
            "Distingui compenso, struttura, anestesia, accertamenti e controlli, segnando le voci ancora da definire.",
            "Verifica sede effettiva, qualifiche e organizzazione dell’assistenza dopo la dimissione.",
            "Gli esempi economici sono simulazioni, non tariffe; la decisione richiede una valutazione specialistica personale.",
        ],
        "disclaimer": "Guida informativa per preparare il confronto con i sanitari: non fornisce diagnosi, indicazioni operatorie né tariffe di mercato e non sostituisce una visita specialistica, una valutazione anestesiologica o la lettura del contratto individuale.",
        "related": [
            "/approfondimenti/visita-ortopedica-privata-costi-cosa-aspettarsi.html",
            "/approfondimenti/differenza-tra-tan-e-taeg.html",
        ],
        "sources": [
            ("https://www.sicpre.it/bellezza-in-sicurezza-le-regole-da-seguire/", "SICPRE — competenza specialistica, informazione e sicurezza nella scelta del percorso chirurgico."),
            ("https://www.nhs.uk/tests-and-treatments/cosmetic-procedures/advice/choosing-who-will-do-your-procedure/", "NHS — domande su professionista, costi e assistenza; i riferimenti ai registri inglesi non valgono come autorizzazioni italiane."),
        ],
    },
    {
        "number": 67,
        "slug": "rc-professionale-ingegneri-architetti-massimali-copertura",
        "title": "RC ingegneri e architetti: massimali e copertura nel tempo",
        "description": "Attività assicurate, franchigie, scoperti, retroattività, postuma e rinnovo: come leggere e confrontare una polizza RC professionale.",
        "category": "Economia e lavoro",
        "body": "67-rc-professionale.txt",
        "alt": "Professionista in uno studio tecnico con progetti, modello di edificio, casco e due cartelle contrattuali; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic-natural, 3:2 Italian editorial cover: adult civil engineer face visible in realistic architecture studio, technical plans, small building model, yellow hard hat and two open blank contract folders. No floating symbols, money, text, logos, watermark or collage. Conceptual illustration, not a named individual or event; natural light, realistic hands and geometry.",
        "points": [
            "La polizza va confrontata con gli incarichi effettivi, le persone assicurate e le esclusioni.",
            "Massimale per sinistro, aggregato annuo e sottolimiti descrivono disponibilità diverse.",
            "Franchigia e scoperto determinano la quota personale: confrontali su scenari dichiarati come ipotetici.",
            "Nelle claims made verifica attività, richiesta e denuncia insieme a retroattività, postuma e circostanze note.",
        ],
        "disclaimer": "Guida informativa generale su contratti e rischi professionali: non sostituisce consulenza legale o assicurativa. Obblighi, adeguatezza e operatività delle garanzie vanno valutati per gli incarichi effettivi con Ordine competente e intermediario qualificato, leggendo le condizioni sottoscritte.",
        "related": [
            "/approfondimenti/srl-o-ditta-individuale-quale-scegliere.html",
            "/approfondimenti/firewall-aziendale-hardware-o-cloud.html",
        ],
        "sources": [
            ("https://www.gazzettaufficiale.it/eli/id/2012/08/14/012G0159/sg", "Gazzetta Ufficiale — DPR 7 agosto 2012 n. 137, articolo 5: assicurazione idonea e informazione al cliente."),
            ("https://www.ingegneri.aon.it/it/web/inarcassa/faq-domande-frequenti", "Aon — FAQ della convenzione ingegneri Fondazione Inarcassa: esempi di condizioni claims made, all risks e gestione delle richieste; non applicabili automaticamente a ogni prodotto."),
        ],
    },
]


def sync_states_prepared(stamp):
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text())
        data.update(site_version=base.VERSION, version=str(base.VERSION), currentVersion=base.VERSION,
                    evergreen_added=[g["slug"] for g in base.GUIDES],
                    last_update="approfondimenti-lista-409-67", updated_at=stamp, release_date=stamp[:10])
        base.dump(path, data)
    path = ROOT / "automation/state/approfondimenti-lista-500.json"
    data = json.loads(path.read_text())
    for guide in base.GUIDES:
        data["items"].append({"number": guide["number"], "title": guide["title"],
                              "url": f"/approfondimenti/{guide['slug']}.html", "status": "prepared",
                              "selected_at": stamp, "selection_seed": SEED})
    base.dump(path, data)


def build_page(guide, stamp):
    original_build_page(guide, stamp)
    path = ROOT / "approfondimenti" / f"{guide['slug']}.html"
    doc = html.fromstring(path.read_text())
    main = doc.xpath('//main')[0]
    summary = main.xpath('./section[@class="cm-summary-box"]')[0]
    main.remove(summary)
    main.xpath('./div[@class="meta"]')[0].addnext(summary)
    path.write_text(base.markup(doc))


original_build_page = base.build_page
base.build_page = build_page
base.sync_states = sync_states_prepared


def prepare():
    state = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text())
    registry = json.loads((ROOT / "automation/state/approfondimenti-lista-500.json").read_text())
    used = {g["number"] for g in registry["items"]}
    base.VERSION = max(int(state.get("site_version", 0)), int(state.get("currentVersion", 0))) + 1
    for guide in base.GUIDES:
        assert guide["number"] not in used, f"Tema {guide['number']} già registrato"
        assert not (ROOT / "approfondimenti" / (guide["slug"] + ".html")).exists(), "Guida già presente"
        for url in guide["related"]:
            assert (ROOT / url.lstrip('/')).is_file(), f"Link interno assente: {url}"
        with Image.open(PAYLOAD / f"{guide['number']}-cover.webp") as image:
            for width in (480, 800, 1200):
                resized = ImageOps.fit(image.convert('RGB'), (width, width * 2 // 3), method=Image.Resampling.LANCZOS)
                resized.save(ROOT / f"assets/images/editorial-auto/{guide['slug']}-v{base.VERSION}-{width}.webp", 'WEBP', quality=84, method=6)
    base.main()


def refresh_timestamps():
    """Da usare dall'agente che applica il pacchetto subito prima del rilascio."""
    stamp = datetime.now(ZoneInfo('Europe/Rome')).isoformat(timespec='seconds')
    label = datetime.fromisoformat(stamp).strftime('%d/%m/%Y · %H:%M')
    for guide in base.GUIDES:
        path = ROOT / 'approfondimenti' / (guide['slug'] + '.html')
        doc = html.fromstring(path.read_text())
        for script in doc.xpath('//script[@type="application/ld+json"]'):
            data = json.loads(script.text)
            if data.get('@type') == 'Article':
                data.update(datePublished=stamp, dateModified=stamp)
                script.text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        meta = doc.xpath('//main/div[@class="meta"]')[0]
        meta.text = label + ' · ' + meta.text.split(' · ')[-1]
        sources = doc.xpath('//div[@class="art-sources"]')[0]
        for p in sources.xpath('./p'):
            if p.text and p.text.startswith('Redazione CurioMondo'):
                p.text = f'Redazione CurioMondo · Testo originale. Ultimo aggiornamento editoriale: {label} (ora italiana). '
        path.write_text(base.markup(doc))
    path = ROOT / 'automation/state/approfondimenti-lista-500.json'
    data = json.loads(path.read_text())
    for item in data['items']:
        if item['number'] in (409, 67):
            item['status'] = 'prepared'
            item['selected_at'] = stamp
    base.dump(path, data)
    base.sync_sitemap(stamp[:10])
    import subprocess
    subprocess.run(['node', 'tools/render_home_editorial.js'], cwd=ROOT, check=True)
    print(json.dumps({'refreshed': [409, 67], 'timestamp': stamp}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh-timestamps', action='store_true')
    args = parser.parse_args()
    if args.refresh_timestamps:
        refresh_timestamps()
    else:
        prepare()
