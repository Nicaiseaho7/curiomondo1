#!/usr/bin/env python3
"""Pubblica gli approfondimenti 96 e 183 senza aprire il manifest storico."""
import json
from pathlib import Path

import publish_approfondimenti_137_153_v808 as base

ROOT = Path(__file__).resolve().parents[1]
VERSION = 809
PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-96-183-v809"

GUIDES = [
    {
        "number": 96,
        "slug": "locazione-commerciale-durata-costi-clausole",
        "title": "Locazione commerciale: durata, costi e clausole da controllare",
        "description": "Destinazione d’uso, durata, canone, garanzie, lavori, recesso e registrazione: il metodo per leggere il contratto prima della firma.",
        "category": "Società e diritto",
        "body": "locazione-commerciale-body.txt",
        "alt": "Imprenditore e professionista esaminano la planimetria davanti a un locale commerciale; illustrazione IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero: a small-business owner and a property professional, both facing camera, inspect a floor plan outside a real Italian street-level commercial property; natural daylight, no readable text, no logos, no watermark, no legal clichés.",
        "points": [
            "L’uso scritto nel contratto non sostituisce compatibilità urbanistica, edilizia e autorizzazioni dell’attività.",
            "Il costo totale comprende canone, spese, imposte, garanzie, lavori, manutenzioni e ripristino finale.",
            "Durata, rinnovo, recesso e comunicazioni devono essere trasformati in un calendario di scadenze.",
            "Promesse su lavori e idoneità del locale vanno inserite nel contratto o in allegati richiamati.",
        ],
        "disclaimer": "Guida informativa generale: non sostituisce la revisione legale del contratto, la verifica tecnica dell’immobile o la consulenza fiscale sul caso concreto.",
        "related": [
            "/approfondimenti/catasto-italiano-come-funziona-visura-rendita.html",
            "/approfondimenti/che-cose-lape.html",
        ],
        "sources": [
            ("https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1978-07-27;392", "Normattiva — legge 392/1978: durata, rinnovo, recesso, cessione e avviamento nelle locazioni a uso diverso."),
            ("https://www.normattiva.it/eli/id/1942/04/04/042U0262/CONSOLIDATED", "Normattiva — Codice civile: disciplina generale della locazione e obblighi delle parti."),
            ("https://www.agenziaentrate.gov.it/portale/schede/pagamenti/imposta-di-registro/registrazione-contratti-di-locazione-fabbricati-e-affitto-terreni", "Agenzia delle Entrate — registrazione dei contratti di locazione e termine ordinario."),
            ("https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/registrazione-di-un-nuovo-contratto/quanto-si-paga-regime-ordinario", "Agenzia delle Entrate — imposta di registro e regole per i fabbricati strumentali."),
        ],
    },
    {
        "number": 183,
        "slug": "noleggio-operativo-aziende-costi-servizi-rischi",
        "title": "Noleggio operativo per aziende: costi, servizi e rischi",
        "description": "Canone, durata, manutenzione, SLA, assicurazione, restituzione e contabilità: come confrontare il noleggio con acquisto e leasing.",
        "category": "Economia e lavoro",
        "body": "noleggio-operativo-body.txt",
        "alt": "Imprenditore e tecnica controllano attrezzature aziendali noleggiate in un magazzino; illustrazione IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero: an SME owner and a service technician, both faces visible, review leased business equipment in a modern Italian warehouse-office with a pallet mover and professional printer; realistic daylight, no readable text, no logos, no watermark, no charts.",
        "points": [
            "Il canone va sommato a installazione, consumi, assicurazione, servizi esclusi e costi di restituzione.",
            "Noleggio operativo, acquisto, leasing finanziario e servizio gestito trasferiscono rischi diversi.",
            "Assistenza inclusa ha valore solo con tempi di ripristino, ricambi, sostituzione e rimedi misurabili.",
            "Deducibilità, IVA e classificazione contabile dipendono da contratto, bene, uso e principi applicati.",
        ],
        "disclaimer": "Guida informativa per decisioni aziendali: non sostituisce analisi finanziaria, consulenza contabile o fiscale e revisione legale del singolo contratto.",
        "related": [
            "/approfondimenti/fibra-aziende-costi-sla.html",
            "/approfondimenti/firewall-aziendale-hardware-o-cloud.html",
        ],
        "sources": [
            ("https://www.normattiva.it/eli/id/1942/04/04/042U0262/CONSOLIDATED", "Normattiva — Codice civile: nozione e disciplina generale della locazione di cose."),
            ("https://www.fondazioneoic.eu/wp-content/uploads/2024/11/2024-03-OIC-12-Composizione-e-schemi-del-bilancio.pdf", "OIC — OIC 12: composizione del conto economico e costi per godimento di beni di terzi."),
            ("https://def.finanze.it/DocTribFrontend/getAttoNormativoDetail.do?ACTION=getSommario&id=%7B31D694E8-4398-4030-873B-FEAF5A6647F9D%7D", "Dipartimento delle Finanze — Testo unico delle imposte sui redditi e regole fiscali sui beni d’impresa."),
            ("https://www.mimit.gov.it/it/incentivi/agevolazioni-per-gli-investimenti-delle-pmi-in-beni-strumentali-nuova-sabatini", "MIMIT — Nuova Sabatini: modalità ammesse per gli investimenti in beni strumentali."),
        ],
    },
]


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_states(published_at):
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(
            site_version=VERSION,
            version=str(VERSION),
            currentVersion=VERSION,
            evergreen_added=[guide["slug"] for guide in GUIDES],
            last_update="approfondimenti-lista-96-183",
            updated_at=published_at,
            release_date=published_at[:10],
        )
        dump(path, data)

    path = ROOT / "automation/state/approfondimenti-lista-500.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"source": "Lista approfondimenti.txt", "items": []}
    for guide in GUIDES:
        data["items"] = [item for item in data["items"] if item.get("number") != guide["number"]]
        data["items"].append(
            {
                "number": guide["number"],
                "title": guide["title"],
                "url": f"/approfondimenti/{guide['slug']}.html",
                "status": "published",
                "selected_at": published_at,
            }
        )
    dump(path, data)


base.ROOT = ROOT
base.PAYLOAD = PAYLOAD
base.VERSION = VERSION
base.GUIDES = GUIDES
base.sync_states = sync_states


if __name__ == "__main__":
    base.main()
