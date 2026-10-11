#!/usr/bin/env python3
"""Lotto politica 11 ottobre: pagine separate, superfici sincronizzate una volta."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_finale_20261010_v836 as prior
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

VERSION = 838
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "microcredito": ROOT.parent / "generated_images/exec-8d431081-7665-4ba5-9dd6-21e1f542025a.png",
    "iva": ROOT.parent / "generated_images/exec-d07a6c53-13c8-422a-9563-2634dfd9ed48.png",
}

ARTICLES = [
    {
        "slug": "emilia-romagna-legge-microcredito-sociale-fondo-ottobre-2026",
        "titolo": "Emilia-Romagna, legge sul microcredito sociale: domande non ancora aperte",
        "sommario": "Il fondo regionale può impegnare fino a un milione di euro l'anno nel 2026–2028. Requisiti, spese finanziabili e procedure attendono una delibera della Giunta.",
        "categoria": "Politica", "luogo": "Emilia-Romagna", "formato": "flash",
        "parole_chiave_titolo": ["microcredito sociale", "domande non ancora aperte"],
        "dati_chiave": [
            {"valore": "10 ottobre", "etichetta": "legge in vigore"},
            {"valore": "1 milione", "etichetta": "tetto annuo 2026–2028"},
            {"valore": "da definire", "etichetta": "requisiti e procedure"},
        ],
        "paragrafi": [
            "In Emilia-Romagna è entrata in vigore sabato 10 ottobre la legge regionale sul microcredito sociale, pubblicata il giorno prima nel bollettino ufficiale. La norma istituisce un fondo per sostenere persone e famiglie residenti in condizioni di vulnerabilità economica o sociale. Le domande non sono però ancora aperte: criteri e procedure devono essere stabiliti dalla Giunta.",
            "Il fondo potrà garantire i prestiti concessi, ridurre gli interessi e coprire costi di tutoraggio e accompagnamento. La legge prevede che la Regione ne concordi la gestione con l'Ente nazionale per il microcredito. È un sostegno sotto forma di finanziamento da restituire, non un contributo automatico a fondo perduto.",
            "La spesa autorizzata è limitata a un massimo di un milione di euro per ciascuno degli anni 2026, 2027 e 2028. La cifra è il tetto degli oneri per attuare la legge, non l'importo spettante a ogni famiglia: il testo non fissa ancora l'entità del singolo prestito.",
            "Una successiva delibera definirà requisiti, condizioni di ammissione e spese finanziabili. Dovrà considerare l'Isee e altri elementi di fragilità, comprese spese impreviste o non rinviabili e riduzioni temporanee delle risorse disponibili. Prima di concedere il credito, il soggetto erogatore dovrà valutare reddito, patrimonio e debiti complessivi del richiedente per evitare nuovo sovraindebitamento.",
            "Chi risiede in regione non può quindi presentare una richiesta sulla sola base della nuova legge. Il passaggio da seguire è la delibera attuativa, che stabilirà come accedere alla misura e come restituire le somme. Il testo lascia anche spazio a ulteriori risorse per emergenze o calamità, ma non le assegna già a beneficiari specifici.",
        ],
        "fonti": [
            {"url": "https://demetra.regione.emilia-romagna.it/al/articolo?urn=er%3Aassemblealegislativa%3Alegge%3A2026%3B11", "nome": "Regione Emilia-Romagna, legge regionale 9 ottobre 2026 n. 11 — articoli 1–7, beneficiari, fondi e decorrenza."},
            {"url": "https://bur.regione.emilia-romagna.it/dettaglio-inserzione?i=f9f57ac63cb84a5a85b076b994af520d", "nome": "Bollettino ufficiale Emilia-Romagna n. 261 del 9 ottobre — pubblicazione del provvedimento."},
        ],
        "image_source": "microcredito",
        "image_alt": "Illustrazione editoriale IA di un colloquio in un ufficio sociale emiliano-romagnolo; scena non documentaria.",
        "image_prompt": "Colloquio concettuale in un ufficio sociale emiliano-romagnolo, adulti in volto; logo circolare compositato dopo.",
    },
    {
        "slug": "ue-proposta-proroga-antifrode-iva-2030-ottobre-2026",
        "titolo": "IVA, Bruxelles propone di prorogare gli strumenti antifrode al 2030",
        "sommario": "La Commissione vuole mantenere disponibili inversione contabile facoltativa e intervento rapido fino al 30 giugno 2030. Serve ancora la decisione del Consiglio UE: nessun nuovo obbligo scatta ora per i contribuenti.",
        "categoria": "Politica", "luogo": "Bruxelles", "formato": "flash",
        "parole_chiave_titolo": ["IVA", "2030"],
        "dati_chiave": [
            {"valore": "2030", "etichetta": "nuova scadenza proposta"},
            {"valore": "2", "etichetta": "strumenti antifrode"},
            {"valore": "Consiglio", "etichetta": "deve ancora discuterne"},
        ],
        "paragrafi": [
            "La Commissione europea ha presentato una proposta per mantenere disponibili fino al 30 giugno 2030 due strumenti contro le frodi IVA: l'inversione contabile facoltativa in alcuni settori e un meccanismo di intervento rapido. La direzione generale Fiscalità ne ha dato notizia il 9 ottobre, precisando che la proposta era stata adottata il primo ottobre. Il Consiglio UE deve ancora discuterla.",
            "L'inversione contabile consente agli Stati membri, in settori individuati dalle norme europee e particolarmente esposti alle frodi, di spostare dal venditore all'acquirente la responsabilità del versamento dell'imposta. Il secondo strumento permette una risposta temporanea, soggetta a condizioni rigorose, se emerge una frode improvvisa e di grandi dimensioni in altri settori.",
            "Secondo la Commissione, il mantenimento dei due strumenti darebbe ai governi continuità mentre si preparano le nuove regole digitali dell'IVA. La proposta riguarda una facoltà degli Stati, non impone a tutte le imprese italiane un cambio immediato nel modo di emettere fatture o pagare l'imposta.",
            "Il documento propone il 30 giugno 2030 come nuovo termine. Non equivale a una proroga già approvata: la data e le condizioni potranno essere definitive solo dopo l'iter in Consiglio. Per imprese e professionisti, gli adempimenti restano quelli delle norme applicabili oggi, salvo successivi provvedimenti europei e nazionali.",
        ],
        "fonti": [
            {"url": "https://taxation-customs.ec.europa.eu/news/commission-proposes-extending-key-anti-vat-fraud-tools-until-june-2030-2026-10-09_en", "nome": "Commissione europea, DG Fiscalità — annuncio del 9 ottobre sulla proposta antifrode IVA e suo iter."},
        ],
        "image_source": "iva",
        "image_alt": "Illustrazione editoriale IA di un dossier IVA in un ufficio istituzionale a Bruxelles; scena non documentaria.",
        "image_prompt": "Dossier IVA in ambiente istituzionale a Bruxelles, funzionari in volto; logo circolare compositato dopo.",
    },
]


def main() -> None:
    if sys.argv[1:] == ["refresh-first-image"]:
        article = ARTICLES[0]
        variants = base.make_variants(base.IMAGE_SOURCES["microcredito"], article["slug"])
        registry_path = ROOT / "assets/data/editorial-images-v210.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["items"][0]["variants"] = variants
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Immagine del primo articolo aggiornata senza alterare data e nome")
        return
    if len(sys.argv) != 3:
        raise SystemExit("uso: script.py indice timestamp-ISO-Europe/Rome")
    index = int(sys.argv[1])
    published = datetime.fromisoformat(sys.argv[2])
    if published.utcoffset() != ZoneInfo("Europe/Rome").utcoffset(published):
        raise SystemExit("timestamp Europe/Rome richiesto")
    if index == 0:
        phrases_path = ROOT / "assets/data/frasi-nome.json"
        phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
        for phrase in ("Puoi informarti con calma prima di prendere una decisione.", "Oggi puoi chiedere una spiegazione prima di firmare."):
            if phrase not in phrases:
                phrases.append(phrase)
        phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    article = ARTICLES[index]
    image = base.make_image(article)
    slug = site.write_article(article, image, VERSION)
    base.set_published(slug, published)
    prior.correct_visible_date(slug, published, article["luogo"])
    image["article"] = f"/notizie/{slug}.html"

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["items"] = [image] + registry.get("items", [])
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if index == len(ARTICLES) - 1:
        site.sync_surfaces(ARTICLES, f"/notizie/{slug}.html", VERSION, update_manifest=False)
        state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                      "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                      "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(ARTICLES),
                      "last_update": f"politica-v{VERSION}", "date": published.date().isoformat(),
                      "release_date": published.date().isoformat(), "updated_at": published.isoformat(timespec="seconds"),
                      "status": "ready"})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": index, "slug": slug, "published": published.isoformat()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
