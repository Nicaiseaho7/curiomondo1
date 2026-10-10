#!/usr/bin/env python3
"""Prepara due approfondimenti da lista su un checkout aggiornato di CurioMondo.

Non esegue commit, push o deploy. Non legge né modifica il manifest.
"""
import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-191-312"
BASE_PATH = ROOT / "tools/publish_approfondimenti_137_153_v808.py"
SPEC = importlib.util.spec_from_file_location("publish_base_v808", BASE_PATH)
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

base.PAYLOAD = PAYLOAD
base.GUIDES = [
    {
        "number": 191,
        "slug": "certificazione-iso-14001-costi-procedura",
        "title": "ISO 14001:2026, iter di certificazione e costi da confrontare",
        "description": "Campo di applicazione, aspetti ambientali, audit, organismi accreditati e costi del ciclo: guida alla certificazione ISO 14001.",
        "category": "Ambiente e clima",
        "body": "191-iso-14001.txt",
        "alt": "Addetto in uno stabilimento esamina una scheda davanti a impianti industriali; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic 3:2 Italian industrial workshop, worker with face visible reviewing blank clipboard near machinery and environmental monitoring, natural light, no logos or readable text, conceptual editorial illustration of ISO 14001 rather than a real audit.",
        "points": [
            "ISO 14001 certifica un sistema di gestione ambientale nel campo indicato, non un prodotto o l’assenza di impatti.",
            "Nel 2026 è disponibile una nuova edizione: chiedi quale versione e quali regole di transizione riguardano l’audit.",
            "Il costo totale include preparazione, lavoro interno, audit, sorveglianza e rinnovo: non esiste un prezzo unico.",
            "L’ISO non rilascia certificati; verifica organismo, accreditamento, campo e stato nelle banche dati pertinenti.",
        ],
        "disclaimer": "Guida informativa generale: obblighi ambientali, autorizzazioni, transizione alla nuova edizione e condizioni di certificazione vanno verificati per la singola organizzazione presso enti e professionisti competenti.",
        "related": [
            "/approfondimenti/agrivoltaico-come-funziona-colture-acqua-monitoraggio.html",
            "/approfondimenti/casa-legno-costi-durata-manutenzione.html",
        ],
        "sources": [
            ("https://www.iso.org/standard/14001", "ISO — ISO 14001:2026 e quadro del sistema di gestione ambientale."),
            ("https://www.iso.org/climate-change/iso-14001-2026", "ISO — novità e orientamento dell’edizione 2026."),
            ("https://www.iso.org/certification.html", "ISO — chiarimento: la certificazione è rilasciata da organismi esterni."),
            ("https://www.accredia.it/banche-dati/accreditamenti/", "Accredia — banca dati degli organismi accreditati e relativi scopi."),
            ("https://www.accredia.it/banche-dati/certificazioni/", "Accredia — ricerca dello stato dei certificati di sistema."),
        ],
    },
    {
        "number": 312,
        "slug": "sd-wan-come-funziona-quanto-costa",
        "title": "SD-WAN: come funziona e quali costi entrano nel contratto",
        "description": "Overlay, accessi, policy, sicurezza, SLA, gestione e migrazione: come confrontare le offerte SD-WAN per le imprese.",
        "category": "Tecnologia e digitale",
        "body": "312-sd-wan.txt",
        "alt": "Tecnico di rete osserva apparati e computer in una sala server; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic 3:2 editorial cover, Italian network engineer face visible beside realistic rack network hardware and unlabeled laptop, calm blue natural light, no fake logos or readable text, conceptual SD-WAN illustration.",
        "points": [
            "La SD-WAN è un servizio logico sopra collegamenti reali: non sostituisce le linee né garantisce banda aggiuntiva.",
            "Le policy possono scegliere percorsi secondo qualità e applicazione, ma il failover va provato in condizioni reali.",
            "Cifratura e instradamento non sostituiscono da soli firewall, identità, monitoraggio e piano di continuità.",
            "Il costo totale somma accessi, nodi, licenze, sicurezza, gestione, installazione e uscita dal contratto.",
        ],
        "disclaimer": "Guida tecnica informativa: architettura, sicurezza, protezione dei dati e contratti richiedono verifiche sulle applicazioni e sulla rete effettiva con professionisti competenti.",
        "related": [
            "/approfondimenti/fibra-aziende-costi-sla.html",
            "/approfondimenti/firewall-aziendale-hardware-o-cloud.html",
        ],
        "sources": [
            ("https://www.mplify.net/resources/mef-70-2-sd-wan-service-attributes-and-service-framework/", "Mplify Alliance — MEF 70.2, attributi e quadro del servizio SD-WAN."),
            ("https://www.mplify.net/service-standards/overlay-services/sd-wan/", "Mplify Alliance — servizio overlay SD-WAN e componenti del modello."),
            ("https://csrc.nist.gov/pubs/sp/800/215/final", "NIST — SP 800-215, guida alla sicurezza della rete aziendale moderna."),
        ],
    },
]


def sync_states_prepared(published_at):
    slugs = [guide["slug"] for guide in base.GUIDES]
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(
            site_version=base.VERSION,
            version=str(base.VERSION),
            currentVersion=base.VERSION,
            evergreen_added=slugs,
            last_update="approfondimenti-lista-191-312",
            updated_at=published_at,
            release_date=published_at[:10],
        )
        base.dump(path, data)
    path = ROOT / "automation/state/approfondimenti-lista-500.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"source": "Lista approfondimenti.txt", "items": []}
    for guide in base.GUIDES:
        data["items"].append({
            "number": guide["number"], "title": guide["title"],
            "url": f"/approfondimenti/{guide['slug']}.html",
            "status": "prepared", "selected_at": published_at,
        })
    base.dump(path, data)


def prepare():
    assert BASE_PATH.is_file(), "Manca lo script base v808 nel repository"
    assert (ROOT / "approfondimenti/fibra-aziende-costi-sla.html").is_file(), "Manca lo stampo aggiornato"
    state = json.loads((ROOT / "CURIOMONDO-RELEASE-STATE.json").read_text(encoding="utf-8"))
    selected = json.loads((ROOT / "automation/state/approfondimenti-lista-500.json").read_text(encoding="utf-8"))
    taken = {item.get("number") for item in selected["items"]}
    for guide in base.GUIDES:
        assert guide["number"] not in taken, f"Numero {guide['number']} già registrato: fermarsi e scegliere un altro tema"
        assert not (ROOT / "approfondimenti" / f"{guide['slug']}.html").exists(), f"Pagina già presente: {guide['slug']}"
        for url in guide["related"]:
            assert (ROOT / url.lstrip("/")).is_file(), f"Collegamento interno non trovato: {url}"
    base.VERSION = max(int(state.get("site_version", 0)), int(state.get("currentVersion", 0))) + 1
    base.sync_states = sync_states_prepared
    output = ROOT / "assets/images/editorial-auto"
    output.mkdir(parents=True, exist_ok=True)
    for guide in base.GUIDES:
        source = PAYLOAD / f"{guide['number']}-cover.png"
        assert source.is_file(), f"Copertina mancante: {source}"
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            for width in (480, 800, 1200):
                resized = ImageOps.fit(rgb, (width, width * 2 // 3), method=Image.Resampling.LANCZOS)
                resized.save(output / f"{guide['slug']}-v{base.VERSION}-{width}.webp", "WEBP", quality=84, method=6)


if __name__ == "__main__":
    prepare()
    base.main()
