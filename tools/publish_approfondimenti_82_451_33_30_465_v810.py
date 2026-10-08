#!/usr/bin/env python3
"""Prepara il lotto di cinque approfondimenti v810 senza leggere il manifest."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "tools/publish_approfondimenti_137_153_v808.py"
SPEC = importlib.util.spec_from_file_location("publish_base_v808", BASE_PATH)
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

base.VERSION = 810
base.PAYLOAD = ROOT / "tools/editorial-payloads/approfondimenti-82-451-33-30-465-v810"
base.GUIDES = [
    {
        "number": 82,
        "slug": "srl-o-ditta-individuale-quale-scegliere",
        "title": "SRL o ditta individuale: quale scegliere davvero",
        "description": "Responsabilità, imposte, contributi, costi amministrativi, soci e crescita: un metodo pratico per confrontare le due forme d'impresa.",
        "category": "Economia e lavoro",
        "body": "82-srl-o-ditta-individuale.txt",
        "alt": "Imprenditrice e consulente confrontano documenti societari in un ufficio; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, Italian woman entrepreneur and accountant facing camera in a bright contemporary office, comparing business structure using blank documents, calculator and laptop, natural daylight, believable details, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "La ditta individuale è più semplice, ma non separa in modo generale il patrimonio dell'attività da quello personale.",
            "La SRL crea un soggetto distinto, con capitale, organi, contabilità e adempimenti più articolati.",
            "Il confronto fiscale va fatto sul denaro che resta all'imprenditore, non sulla sola aliquota nominale.",
            "Rischio, soci, reinvestimenti e fabbisogno finanziario pesano spesso più del fatturato preso da solo.",
        ],
        "disclaimer": "Guida informativa generale: la scelta richiede una simulazione fiscale, previdenziale e patrimoniale sul caso concreto con professionisti abilitati.",
        "related": [
            "/approfondimenti/locazione-commerciale-durata-costi-clausole.html",
            "/approfondimenti/noleggio-operativo-aziende-costi-servizi-rischi.html",
            "/approfondimenti/fibra-aziende-costi-sla.html",
        ],
        "sources": [
            ("https://sni.unioncamere.it/sites/default/files/approfondimento/documenti/GUIDA%20TNO%20-%20La%20scelta%20della%20forma%20giuridica.pdf", "Unioncamere — guida alla scelta della forma giuridica d'impresa, responsabilità e principali differenze operative."),
            ("https://www.inps.it/it/it/inps-comunica/atti/circolari-messaggi-e-normativa/dettaglio.circolari-e-messaggi.2026.02.circolare-numero-14-del-09-02-2026_15162.html", "INPS — circolare 14/2026 sui contributi di artigiani e commercianti per l'anno 2026."),
        ],
    },
    {
        "number": 451,
        "slug": "revisore-legale-costi-quando-obbligatorio",
        "title": "Revisore legale: quando è obbligatorio e quanto costa",
        "description": "Soglie, incarico, indipendenza, revisione del bilancio, responsabilità e compenso: cosa deve valutare una società prima della nomina.",
        "category": "Economia e lavoro",
        "body": "451-revisore-legale.txt",
        "alt": "Revisore legale esamina registri e prospetti con un gruppo amministrativo; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, professional statutory auditor facing camera at an Italian company meeting table with two finance staff, blank ledgers, laptop with abstract unreadable charts and calculator, precise natural office lighting, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Per molte SRL l'obbligo nasce dalle condizioni dell'articolo 2477 del codice civile, non da una scelta discrezionale.",
            "Il compenso dipende soprattutto da dimensione, complessità, controlli interni, sedi e rischio dell'incarico.",
            "La revisione non coincide con la contabilità: mira a esprimere un giudizio professionale sul bilancio.",
            "Indipendenza, accesso ai documenti e calendario delle verifiche vanno chiariti prima dell'accettazione.",
        ],
        "disclaimer": "Guida informativa societaria: non sostituisce il parere di un commercialista, revisore legale o avvocato sul caso concreto.",
        "related": [
            "/approfondimenti/srl-o-ditta-individuale-quale-scegliere.html",
            "/approfondimenti/noleggio-operativo-aziende-costi-servizi-rischi.html",
            "/approfondimenti/locazione-commerciale-durata-costi-clausole.html",
        ],
        "sources": [
            ("https://www.normattiva.it/uri-res/N2Ls?urn%3Anir%3Astato%3Acodice.civile%3A1942-03-16%3B262~art2477=", "Normattiva — codice civile, articolo 2477: organo di controllo o revisore nelle società a responsabilità limitata."),
            ("https://revisionelegale.rgs.mef.gov.it/area-pubblica/export/mef/resources/PDF/Dlgs_39_2010_vigente_25092024.pdf", "MEF-Ragioneria generale dello Stato — decreto legislativo 39/2010 vigente sulla revisione legale."),
        ],
    },
    {
        "number": 33,
        "slug": "carta-di-credito-per-viaggiare-come-confrontarla",
        "title": "Carta di credito per viaggiare: come confrontarla",
        "description": "Cambio valuta, commissioni estero, assicurazioni, lounge, noleggio auto e assistenza: il confronto che evita costi e false sicurezze.",
        "category": "Economia e lavoro",
        "body": "33-carta-credito-viaggi.txt",
        "alt": "Viaggiatrice confronta una carta senza marchio e le spese di viaggio in aeroporto; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, adult woman traveler facing camera in a modern European airport, holding a generic blank payment card beside cabin luggage and phone with abstract unreadable payment screen, realistic terminal depth, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Il costo estero nasce dalla somma fra tasso di cambio applicato, maggiorazione dell'emittente e possibili commissioni del circuito o dell'ATM.",
            "Assicurazioni, lounge e assistenza valgono solo se condizioni, massimali ed esclusioni coincidono con il viaggio reale.",
            "Per il noleggio auto contano plafond disponibile, intestazione, circuito accettato e regole del deposito cauzionale.",
            "Una carta di riserva separata riduce il rischio operativo, ma richiede limiti, notifiche e contatti di emergenza ben preparati.",
        ],
        "disclaimer": "Guida informativa sui servizi di pagamento: costi, coperture e condizioni dipendono dal contratto aggiornato dell'emittente e dal singolo viaggio.",
        "related": [
            "/approfondimenti/differenza-tra-tan-e-taeg.html",
            "/approfondimenti/phishing-smishing-vishing-come-riconoscere-truffe.html",
            "/approfondimenti/prestito-online-confrontare-preventivi-condizioni.html",
        ],
        "sources": [
            ("https://economiapertutti.bancaditalia.it/aree-tematiche/pagamenti/carta-di-credito/index.html", "Banca d'Italia, Economia per tutti — funzionamento, costi e uso consapevole della carta di credito."),
            ("https://europa.eu/youreurope/citizens/consumers/shopping/pricing-payments/index_it.htm", "Unione europea, Your Europe — prezzi, pagamenti, autenticazione e regole sui supplementi nell'UE."),
        ],
    },
    {
        "number": 30,
        "slug": "conto-deposito-calcolare-rendimento-netto",
        "title": "Conto deposito: come calcolare il rendimento netto",
        "description": "Tasso lordo, imposta, bollo, durata, vincoli e capitalizzazione: la formula per confrontare offerte sullo stesso orizzonte temporale.",
        "category": "Economia e lavoro",
        "body": "30-conto-deposito.txt",
        "alt": "Risparmiatore calcola il rendimento di un deposito con consulente e fogli senza testo; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, adult saver and financial adviser facing camera at a calm bank office desk, calculator, generic coins, calendar blocks and blank rate sheets, laptop with abstract unreadable chart, warm realistic daylight, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Dal tasso lordo vanno sottratte l'imposta sugli interessi, l'imposta di bollo se dovuta e ogni costo contrattuale.",
            "La durata effettiva e la data di accredito contano: lo stesso tasso può produrre risultati diversi.",
            "Vincolo, svincolo anticipato e perdita degli interessi vanno trasformati in scenari numerici comparabili.",
            "La tutela dei depositi opera entro limiti e condizioni: va considerata anche la concentrazione per banca.",
        ],
        "disclaimer": "Guida informativa sul risparmio: non è una raccomandazione d'investimento né una valutazione di adeguatezza personale.",
        "related": [
            "/approfondimenti/titoli-di-stato-btp-bot-cct-come-funzionano.html",
            "/approfondimenti/che-cose-leuribor.html",
            "/approfondimenti/inflazione-come-si-misura-italia-nic-foi-ipca.html",
        ],
        "sources": [
            ("https://economiapertutti.bancaditalia.it/aree-tematiche/conto-corrente/il-conto-di-deposito/index.html", "Banca d'Italia, Economia per tutti — caratteristiche, interessi, tassazione e vincoli del conto deposito."),
            ("https://economiapertutti.bancaditalia.it/aree-tematiche/conto-corrente/il-fondo-interbancario-di-tutela-dei-depositi/index.html", "Banca d'Italia, Economia per tutti — tutela dei depositi e limite di copertura per depositante e banca."),
        ],
    },
    {
        "number": 465,
        "slug": "forensic-investigation-informatica-costi-utilizzi",
        "title": "Forensic investigation informatica: costi e utilizzi",
        "description": "Acquisizione delle prove, log, dispositivi, incidenti e relazione tecnica: come definire un incarico forense senza compromettere i dati.",
        "category": "Tecnologia e digitale",
        "body": "465-forensic-investigation.txt",
        "alt": "Analista forense esamina computer e telefono con strumenti di acquisizione; illustrazione editoriale IA non documentaria.",
        "prompt": "Photorealistic CurioMondo editorial 3:2 hero, digital forensic analyst facing camera in a secure evidence lab, examining laptop, smartphone, drive and hardware write blocker with blank evidence tags, realistic blue-neutral light, centered safe composition; no logos, no readable text, no watermark.",
        "points": [
            "Prima dell'analisi servono scopo, autorità, fonti da preservare e una catena di custodia documentata.",
            "L'acquisizione forense mira a lavorare su copie verificabili, evitando modifiche non controllate agli originali.",
            "Il costo cresce con volume, urgenza, cifratura, cloud, dispositivi e necessità di relazione o testimonianza.",
            "La relazione deve distinguere fatti osservati, metodo, limiti e interpretazioni: non promettere certezze assolute.",
        ],
        "disclaimer": "Guida informativa tecnica: indagini, trattamento di dati personali e utilizzo probatorio richiedono professionisti qualificati e consulenza legale sul caso concreto.",
        "related": [
            "/approfondimenti/firewall-aziendale-hardware-o-cloud.html",
            "/approfondimenti/phishing-smishing-vishing-come-riconoscere-truffe.html",
            "/approfondimenti/come-funzionano-analisi-dna-forense.html",
        ],
        "sources": [
            ("https://www.enisa.europa.eu/publications/electronic-evidence-a-basic-guide-for-first-responders", "ENISA — guida di base alla raccolta delle prove elettroniche per i primi intervenuti."),
            ("https://csrc.nist.gov/pubs/sp/800/86/final", "NIST — SP 800-86: integrazione delle tecniche forensi nella risposta agli incidenti."),
        ],
    },
]


def sync_states_prepared(published_at):
    slugs = [g["slug"] for g in base.GUIDES]
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(site_version=base.VERSION, version=str(base.VERSION), currentVersion=base.VERSION,
                    evergreen_added=slugs, last_update="approfondimenti-lista-82-451-33-30-465",
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
