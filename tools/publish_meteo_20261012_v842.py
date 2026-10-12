#!/usr/bin/env python3
"""Integra il quadro meteo del 12 ottobre nel lotto mattutino v842."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_notte_mattina_20261010_v827 as base
from tools import publish_finale_20261010_v836 as prior
from automation.newsroom import site

VERSION = 842
base.VERSION = VERSION
base.IMAGE_SOURCES = {"meteo": ROOT.parent / "generated_images/exec-36a43ab4-0fbb-4f43-93e8-7cfac3005b4e.png"}

ARTICLE = {
    "slug": "meteo-oggi-12-ottobre-2026-nord-stabile-cinque-regioni-allerta",
    "titolo": "Meteo 12 ottobre: Nord più stabile, cinque regioni in allerta gialla",
    "sommario": "La tendenza dell'Aeronautica Militare favorisce maggiore stabilità al Nord; il bollettino della Protezione Civile individua zone in giallo dal Centro al Sud. Nessuna allerta uniforme sulle intere regioni.",
    "categoria": "Meteo", "luogo": "Italia", "formato": "flash",
    "parole_chiave_titolo": ["Meteo 12 ottobre", "allerta gialla"],
    "dati_chiave": [{"valore": "5", "etichetta": "regioni con zone gialle"}, {"valore": "12 ottobre", "etichetta": "giornata considerata"}, {"valore": "14:17", "etichetta": "bollettino dell'11"}],
    "paragrafi": [
        "Lunedì 12 ottobre si profila maggiore stabilità al Nord e restano criticità in zone del Centro-Sud. Il bollettino nazionale emesso dalla Protezione Civile domenica alle 14:17 indica allerta gialla in settori di Toscana, Abruzzo, Campania, Calabria e Sicilia. Non è un'allerta estesa in modo uniforme a tutto il territorio delle cinque regioni.",
        "In Calabria il livello giallo riguarda i versanti tirrenici per rischio idraulico, temporali e rischio idrogeologico. In Abruzzo sono indicati i bacini Tordino-Vomano e Pescara; in Sicilia le aree nord-orientali e parte del settore tirrenico centro-settentrionale. Le zone della Toscana e della Campania elencate dal bollettino hanno criticità differenti, da verificare sulla mappa per il proprio comune.",
        "La previsione a scala settimanale dell'Aeronautica Militare, emessa venerdì 9 ottobre per il periodo 12–18, descrive alta pressione verso il Nord Italia e il settore centrale tirrenico, con condizioni tendenzialmente più stabili e asciutte. Segnala anche l'influenza marginale di una circolazione ciclonica sull'area ionica. La tendenza settimanale non esclude piogge locali oggi.",
        "Per gli spostamenti di oggi, la mappa della Protezione Civile distingue rischio idraulico, temporali e rischio idrogeologico per singola zona. L'allerta è una previsione di criticità, non la prova che un evento si sia già verificato. Prima di attraversare sottopassi o aree esposte conviene consultare gli aggiornamenti della Regione e del Comune interessati.",
    ],
    "fonti": [
        {"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/index.html", "nome": "Dipartimento della Protezione Civile — bollettino dell'11 ottobre 2026, ore 14:17, valido per il 12."},
        {"url": "https://www.meteoam.it/it/previsioni-mensili", "nome": "Aeronautica Militare — tendenza emessa il 9 ottobre per la settimana 12–18 ottobre 2026."},
    ],
    "image_source": "meteo",
    "image_alt": "Illustrazione editoriale IA della costa tirrenica calabrese sotto nubi sparse; non mostra un fenomeno osservato oggi.",
    "image_prompt": "Paesaggio costiero calabrese fotorealistico, nubi illustrative senza fenomeni estremi, nessuna mappa; logo CurioMondo circolare in post-produzione.",
}


def main() -> None:
    if sys.argv[1:] == ["--repair-paragraphs"]:
        path = ROOT / "notizie/meteo-oggi-12-ottobre-2026-nord-stabile-cinque-regioni-allerta.html"
        current = path.read_text(encoding="utf-8")
        replacements = {
            "Lunedì 12 ottobre il quadro meteorologico italiano presenta un contrasto fra la tendenza a condizioni più stabili al Nord e criticità segnalate in alcune zone del Centro-Sud.": "Lunedì 12 ottobre si profila maggiore stabilità al Nord e restano criticità in zone del Centro-Sud.",
            "È una tendenza della settimana, non una previsione oraria che esclude piogge oggi in ogni città settentrionale.": "La tendenza settimanale non esclude piogge locali oggi.",
        }
        for old, new in replacements.items():
            if current.count(old) != 1:
                raise SystemExit("paragrafo meteo da correggere non univoco")
            current = current.replace(old, new)
        path.write_text(current, encoding="utf-8")
        return
    phrase_path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(phrase_path.read_text(encoding="utf-8"))
    phrase = "Controlla la zona di allerta prima di scegliere il percorso."
    if phrase not in phrases:
        phrases.append(phrase)
        phrase_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    release = datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    image = base.make_image(ARTICLE)
    slug = site.write_article(ARTICLE, image, VERSION)
    base.set_published(slug, release)
    prior.correct_visible_date(slug, release, ARTICLE["luogo"])
    image["article"] = f"/notizie/{slug}.html"
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["items"] = [image] + registry.get("items", [])
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces([ARTICLE], f"/notizie/{slug}.html", VERSION, update_manifest=False)
    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({"articleCount": int(state.get("articleCount", 0)) + 1,
                  "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
                  "updated_at": release.isoformat(timespec="seconds")})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"slug": slug, "published": release.isoformat()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
