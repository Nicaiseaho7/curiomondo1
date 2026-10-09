#!/usr/bin/env python3
"""Prepara il lotto di cinque approfondimenti v823 senza leggere il manifest."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "tools/publish_approfondimenti_137_153_v808.py"
SPEC = importlib.util.spec_from_file_location("publish_base_v808", BASE_PATH)
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

base.VERSION = 823
base.PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-400-270-56-55-401-v823"
base.GUIDES = [
    {
        "number": 400,
        "slug": "visita-ortopedica-privata-costi-cosa-aspettarsi",
        "title": "Visita ortopedica privata: costi e cosa aspettarsi",
        "description": "Preventivo, anamnesi, esame obiettivo, immagini, diagnosi e opzioni terapeutiche: come prepararsi e valutare il percorso.",
        "category": "Scienza e salute",
        "body": "400-visita-ortopedica.txt",
        "alt": "Ortopedica e paziente durante un colloquio clinico con modello anatomico; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, Italian female orthopedic physician and adult patient seated in a bright real clinic during a calm consultation, physician holds a simple accurate knee joint model, both faces natural, hands anatomically correct, blank paper folder, no examination procedure, no diagnostic screen, warm daylight, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Non esiste una tariffa privata nazionale unica: confronta preventivi con prestazioni e regime allineati.",
            "Porta immagini originali, referti, farmaci, allergie e una cronologia concreta dei sintomi.",
            "L'imaging integra anamnesi ed esame obiettivo: non coincide da solo con la diagnosi.",
            "La visita dovrebbe concludersi con ipotesi, opzioni, tempi, obiettivi e segnali per rivalutare.",
        ],
        "disclaimer": "Guida informativa generale: non sostituisce una valutazione medica. Sintomi importanti o improvvisi richiedono un contatto tempestivo con i servizi sanitari appropriati.",
        "related": [
            "/approfondimenti/procreazione-medicalmente-assistita-costi-percorso.html",
            "/approfondimenti/come-funziona-730-precompilato-italia.html",
            "/approfondimenti/cpap-prezzi-manutenzione-scelta.html",
        ],
        "sources": [
            ("https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/01-sanita/07-ticket-ed-esenzioni/ticket-esenzioni-prerstazioni-ssr/allegati/DGR%2Bn.%2BXII_4956%2Bdel%2B8.9.2025.pdf", "Regione Lombardia — nomenclatore e tariffe dell'assistenza specialistica ambulatoriale del servizio sanitario regionale."),
            ("https://www.ior.it/domande-frequenti-0", "Istituto Ortopedico Rizzoli — informazioni ufficiali su prenotazione, accesso e documentazione per le visite ortopediche."),
        ],
    },
    {
        "number": 270,
        "slug": "casa-legno-costi-durata-manutenzione",
        "title": "Casa in legno: costi, durata e manutenzione",
        "description": "Struttura, fondazioni, isolamento, incendio, umidità, tempi, capitolato e controlli: come valutare una casa in legno.",
        "category": "Ambiente e clima",
        "body": "270-casa-legno.txt",
        "alt": "Casa contemporanea in legno durante il montaggio con carpentieri e dettagli strutturali; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, modern Italian timber house under construction in a realistic residential site, clearly believable timber frame and cross-laminated wall panels on a concrete foundation, two professional carpenters wearing correct safety gear standing apart with natural anatomically correct hands, dry weather, precise joinery, no impossible beams, centered composition; no logos, no readable text, no watermark.",
        "points": [
            "Il costo reale comprende terreno, tecnici, fondazioni, struttura, impianti, finiture, logistica e imprevisti.",
            "Prefabbricazione rapida non significa progetto completo in pochi giorni: autorizzazioni e coordinamento restano decisivi.",
            "Durabilità significa soprattutto controllo dell'acqua, capacità di asciugare, dettagli corretti e ispezioni.",
            "Sisma, incendio, comfort e acustica si verificano sul sistema progettato, non sul materiale considerato da solo.",
        ],
        "disclaimer": "Guida informativa generale: progetto, autorizzazioni, sicurezza strutturale, antincendio e contratto richiedono tecnici abilitati e verifiche sul sito.",
        "related": [
            "/approfondimenti/che-cose-lape.html",
            "/approfondimenti/catasto-italiano-come-funziona-visura-rendita.html",
            "/approfondimenti/assicurazione-casa-coperture-costi.html",
        ],
        "sources": [
            ("https://www.gazzettaufficiale.it/eli/id/2018/02/20/18A00716/sg", "Gazzetta Ufficiale — decreto 17 gennaio 2018, aggiornamento delle Norme tecniche per le costruzioni."),
            ("https://www.vigilfuoco.it/sites/default/files/2022-10/COORD_DM_03_08_2015_Codice_Prevenzione_Incendi.pdf", "Corpo nazionale dei Vigili del fuoco — Codice di prevenzione incendi coordinato."),
        ],
    },
    {
        "number": 56,
        "slug": "assicurazione-casa-coperture-costi",
        "title": "Assicurazione casa: coperture e costi",
        "description": "Incendio, acqua, furto, responsabilità civile, eventi atmosferici e assistenza: come confrontare premio e rischio residuo.",
        "category": "Economia e lavoro",
        "body": "56-assicurazione-casa.txt",
        "alt": "Proprietaria e consulente osservano una lieve perdita d'acqua domestica; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, adult Italian homeowner and professional insurance adviser in a normal bright kitchen calmly inspecting a small realistic water stain below a sink cabinet, simple plumbing physically correct, natural faces and anatomically correct hands, blank clipboard, no disaster staging, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Fabbricato, contenuto, responsabilità e assistenza proteggono interessi diversi: definisci prima il rischio.",
            "Franchigia, scoperto, limite di indennizzo e regola proporzionale possono cambiare molto il rimborso.",
            "Acqua, furto ed eventi atmosferici operano secondo definizioni ed esclusioni, non secondo il solo nome commerciale.",
            "Confronta preventivi con dati, somme, massimali e quota a tuo carico perfettamente allineati.",
        ],
        "disclaimer": "Guida informativa assicurativa: fanno fede documenti informativi, condizioni e preventivo della singola impresa; esigenze e rischi vanno valutati sul caso concreto.",
        "related": [
            "/approfondimenti/casa-legno-costi-durata-manutenzione.html",
            "/approfondimenti/catasto-italiano-come-funziona-visura-rendita.html",
            "/approfondimenti/che-cose-lape.html",
        ],
        "sources": [
            ("https://www.ivass.it/consumatori/imparaconivass/guide/Guida_5_Le_assicurazioni_della_responsabilita_civile_versione_web.pdf", "IVASS — guida alle assicurazioni della responsabilità civile."),
            ("https://www.ivass.it/consumatori/imparaconivass/quaderni-didattici/Ivass_Guide_docenti_Superiori.pdf", "IVASS — guida didattica sui contratti assicurativi, franchigie, scoperti e gestione dei rischi."),
        ],
    },
    {
        "number": 55,
        "slug": "assicurazione-moto-costi-garanzie-confrontare",
        "title": "Assicurazione moto: costi e garanzie da confrontare",
        "description": "RC, massimali, sospensione, furto, conducente, assistenza, franchigie e rivalse: un confronto adatto all'uso reale.",
        "category": "Economia e lavoro",
        "body": "55-assicurazione-moto.txt",
        "alt": "Motociclista e consulente confrontano una polizza accanto a una moto parcheggiata; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, adult Italian motorcyclist and professional insurance adviser beside one realistic generic parked touring motorcycle, rider holds one correctly shaped helmet, adviser holds blank clipboard, motorcycle wheels and mechanical geometry accurate, natural faces and anatomically correct hands, daylight outside a simple office, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Confronta prima la RC con massimale, formula di guida, franchigia e rivalse allineati.",
            "La sospensione richiede procedura e calendario: non coincide con il semplice mancato uso della moto.",
            "Furto, conducente e assistenza hanno valori, scoperti, persone e servizi definiti dal contratto.",
            "Il preventivo più basso può lasciare a tuo carico un rischio molto più alto del risparmio annuale.",
        ],
        "disclaimer": "Guida informativa assicurativa: condizioni, prezzi e regole applicabili possono cambiare; verificare contratto, preventivo e canali ufficiali prima di circolare.",
        "related": [
            "/approfondimenti/che-cose-fermo-amministrativo-veicoli.html",
            "/approfondimenti/phishing-smishing-vishing-come-riconoscere-truffe.html",
            "/approfondimenti/prezzo-carburanti-accise-iva-come-si-forma.html",
        ],
        "sources": [
            ("https://www.ivass.it/consumatori/imparaconivass/guide/Guida_3_RC_Auto_versione_web.pdf", "IVASS — guida ufficiale alla responsabilità civile auto e moto, massimali, rivalsa, franchigia e sospensione."),
            ("https://www.consap.it/fondo-di-garanzia-per-le-vittime-della-strada/faq/", "Consap — domande frequenti sul Fondo di garanzia per le vittime della strada."),
        ],
    },
    {
        "number": 401,
        "slug": "procreazione-medicalmente-assistita-costi-percorso",
        "title": "Procreazione medicalmente assistita: costi e percorso",
        "description": "Valutazione, tecniche, esami, farmaci, laboratorio, cicli e scelta del centro: come leggere tempi, costi e probabilità.",
        "category": "Scienza e salute",
        "body": "401-pma.txt",
        "alt": "Medica parla con una coppia in un centro di fertilità, in un colloquio rispettoso; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, female Italian fertility specialist speaking respectfully with an adult couple seated in a calm modern consultation room, all fully clothed, supportive neutral expressions, natural anatomically correct hands resting visibly, blank folder and no medical procedure, no babies, no laboratory scene, soft daylight, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "La PMA è un percorso: valutazione, esami, tecnica, farmaci, laboratorio e seguito possono avere costi separati.",
            "Le percentuali vanno lette con esito, denominatore, fascia d'età e popolazione trattata.",
            "Un ciclo può interrompersi in fasi diverse: il preventivo deve spiegare quali costi restano dovuti.",
            "Centro autorizzato, consenso informato, reperibilità e chiarezza delle alternative contano quanto il prezzo.",
        ],
        "disclaimer": "Guida informativa generale: non sostituisce il consulto con un centro PMA autorizzato né indicazioni cliniche, farmacologiche o riproduttive personalizzate.",
        "related": [
            "/approfondimenti/visita-ortopedica-privata-costi-cosa-aspettarsi.html",
            "/approfondimenti/come-funziona-730-precompilato-italia.html",
        ],
        "sources": [
            ("https://www.iss.it/rpma-infertilita-e-tecniche", "Istituto Superiore di Sanità, Registro nazionale PMA — infertilità e tecniche di procreazione medicalmente assistita."),
            ("https://www.salute.gov.it/new/it/news-e-media/notizie/procreazione-medicalmente-assistita-relazione-al-parlamento-2025/", "Ministero della Salute — Relazione al Parlamento 2025 sull'attuazione della legge 40/2004 in materia di PMA."),
        ],
    },
]


def sync_states_prepared(published_at):
    slugs = [g["slug"] for g in base.GUIDES]
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(site_version=base.VERSION, version=str(base.VERSION), currentVersion=base.VERSION,
                    evergreen_added=slugs, last_update="approfondimenti-lista-400-270-56-55-401",
                    updated_at=published_at, release_date=published_at[:10])
        base.dump(path, data)
    path = ROOT / "automation/state/approfondimenti-lista-500.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for guide in base.GUIDES:
        data["items"] = [item for item in data["items"] if item.get("number") != guide["number"]]
        data["items"].append({"number": guide["number"], "title": guide["title"],
                              "url": f"/approfondimenti/{guide['slug']}.html",
                              "status": "prepared", "selected_at": published_at})
    base.dump(path, data)


base.sync_states = sync_states_prepared

if __name__ == "__main__":
    base.main()
