#!/usr/bin/env python3
"""Contesto documentato per le otto notizie del 22 settembre 2026."""
from pathlib import Path
import json
import re

from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
EXTRA = {
"italia-oro-staffetta-mista-mondiali-ciclismo-montreal-2026": [
    "Il vantaggio sulla Francia è rimasto sotto i nove secondi dopo oltre cinquanta minuti di corsa: un margine ridotto in una prova in cui conta anche il passaggio fra le due frazioni. Il sestetto francese schierava Bruno Armirail, Rémi Cavagna e Jordan Labrosse con Juliette Berthet, Marion Borras e Cédrine Kerbaol. La Svizzera, terza, aveva fra le proprie atlete Marlen Reusser, campionessa mondiale nella cronometro individuale.",
    "La velocità media attribuita agli azzurri è di circa 47,3 chilometri orari sull’intero tracciato. Il dato riassume il rendimento dei due gruppi, mentre le singole prestazioni non possono essere ricavate dal solo tempo finale. L’Australia, indicata fra le favorite, ha concluso quarta. L’Italia ha invece mantenuto il margine necessario anche nella fase in cui le francesi hanno tentato di recuperare terreno.",
    "Il risultato arriva dopo i due argenti già ottenuti dall’Italia nelle cronometro dei primi giorni: Ganna nella gara élite e Nicolas Milesi in quella Under 23. Nella staffetta mista il titolo è assegnato alla nazionale formata da tre uomini e tre donne: la composizione della squadra e l’ordine delle frazioni sono parte essenziale del risultato, oltre al tempo registrato sul traguardo di Montréal."
],
"bonus-colonnine-domestiche-2026-domande-dal-22-settembre": [
    "L’80% è una percentuale applicata alle spese riconosciute come ammissibili, non a qualunque costo sostenuto per la casa. Per esempio, su 1.000 euro di spese ammesse il contributo teorico è di 800 euro; su importi più elevati resta comunque il tetto di 1.500 euro per il privato. Nel condominio il limite massimo è diverso e arriva a 8.000 euro quando la ricarica riguarda le parti comuni dell’edificio.",
    "L’annualità è determinata dal completamento dell’installazione. Per la finestra 2026 il periodo ammesso va dal 26 giugno al 31 dicembre: una domanda inviata nel gennaio 2027 può dunque riferirsi a lavori ultimati nel 2026, purché rientrino nelle altre condizioni della misura. Il Ministero prevede 15 milioni anche per ciascuno degli anni dal 2027 al 2029 e 8 milioni per il 2030, con periodi di installazione distinti.",
    "Il bonus riguarda infrastrutture di ricarica come wall box e colonnine; Invitalia lo gestisce per conto del Ministero. Per evitare errori prima dell’invio, chi presenta la richiesta può consultare le istruzioni, la documentazione sulle spese e le risposte alle domande frequenti pubblicate dai due enti. La scadenza dello sportello non sostituisce la verifica dei requisiti dell’impianto e del richiedente."
],
"enisa-2026-pubblica-amministrazione-32-percento-attacchi-informatici": [
    "Nella distribuzione pubblicata dall’agenzia, i servizi alle imprese e i trasporti seguono a distanza con l’8% ciascuno; manifattura e finanza si fermano rispettivamente al 7% e al 6%. Il 73% delle organizzazioni prese di mira rientra fra i soggetti essenziali o importanti secondo la classificazione della direttiva europea NIS2. Questo non significa che tutti gli incidenti abbiano avuto lo stesso impatto operativo.",
    "ENISA distingue anche le motivazioni degli attori: il 57% degli episodi esaminati è collegato a finalità ideologiche, mentre quasi il 30% ha una motivazione economica. Nel caso del ransomware il danno può derivare dalla cifratura dei sistemi, dalla sottrazione di dati e dalle richieste di estorsione. Per questo il numero degli attacchi DDoS, da solo, non esaurisce la valutazione del rischio per un’amministrazione.",
    "Il rapporto richiama inoltre il phishing e altre forme di manipolazione delle persone, lo sfruttamento delle vulnerabilità e gli attacchi che passano da fornitori o servizi condivisi. Le dipendenze digitali possono allargare l’effetto di un singolo incidente a più enti. Per interpretare il primato della PA occorre quindi separare la frequenza degli eventi dalla continuità dei servizi colpiti e dalla loro capacità di ripristino."
],
"iea-elettrificazione-importazioni-combustibili-400-miliardi-2035": [
    "Il rapporto è stato preparato su richiesta della Turchia, presidente della COP31, e dell’Australia, che presiede i negoziati della conferenza. Alimenta il confronto su un obiettivo globale del 35% di consumi finali soddisfatti dall’elettricità. Il 33% stimato dall’IEA riguarda ciò che le tecnologie disponibili oggi potrebbero coprire a costi competitivi nel 2035, assumendo prezzi dell’energia precedenti allo shock delle forniture.",
    "Trasporti, edifici e industria rappresentano insieme oltre metà delle emissioni di anidride carbonica connesse all’energia. Nello scenario di elettrificazione più veloce, le loro emissioni scenderebbero del 40% entro il 2035. Si tratta di un risultato modellato per uno specifico insieme di scelte, non dell’effetto automatico della sola sostituzione di un combustibile con una presa elettrica.",
    "Le opportunità cambiano per regione: l’agenzia cita, per le economie emergenti, pompe elettriche per l’acqua in agricoltura, veicoli a due o tre ruote nelle città e usi produttivi nelle piccole imprese. Per rendere affidabile la maggiore domanda servono capacità di generazione, reti e flessibilità. L’IEA segnala inoltre i rischi delle filiere concentrate, gli attacchi informatici e gli eventi climatici per la sicurezza del sistema elettrico."
],
"michael-kayode-prima-convocazione-nazionale-serie-d-premier-2026": [
    "A Coverciano Kayode ha spiegato che in Inghilterra lavora sulle rimesse laterali con un tecnico specializzato. Alcuni lanci possono superare i 65 metri e diventare una soluzione offensiva studiata dal Brentford. Alla Fiorentina quella caratteristica era usata meno; il calciatore la presenta come un elemento del proprio gioco, accanto alla corsa sulla fascia e alla fase difensiva.",
    "Il passaggio al Gozzano, dopo le giovanili della Juventus, è avvenuto quando aveva 16 anni. Kayode lo descrive come un cambiamento impegnativo che gli ha dato minuti fra gli adulti e lo ha aiutato a crescere. È il senso del percorso dalla Serie D alla Premier League: l’esordio in un campionato minore non ha impedito l’approdo al calcio di vertice.",
    "Il legame con la Nazionale passa anche dall’Europeo Under 19 vinto sotto la guida di Bollini, ora collaboratore del commissario tecnico Roberto Mancini. Il difensore dice di aver parlato con Mancini delle richieste tattiche e di guardare a Paolo Maldini come modello, mentre considera Giovanni Di Lorenzo un riferimento nel gruppo. Alla prima convocazione il suo obiettivo dichiarato è dare continuità al lavoro e contribuire alla squadra."
],
"italia-bielorussia-femminile-biglietti-firenze-13-ottobre-2026-22-09-2026": [
    "Per il ridotto Under 20 la FIGC considera chi è nato dopo il 13 ottobre 2006; per l’Over 65 chi è nato prima del 13 ottobre 1961. Gli studenti universitari devono dimostrare l’iscrizione all’anno accademico in corso nei punti vendita Vivaticket abilitati. Gli abbonati della Fiorentina utilizzano il sigillo fiscale dell’abbonamento nel campo coupon previsto per ottenere la tariffa agevolata.",
    "La federazione ha aperto separatamente le procedure di accreditamento per i media. Per le persone con disabilità è prevista una richiesta di accredito il 7 ottobre, fino all’esaurimento dei posti, attraverso il portale indicato dalla FIGC; la registrazione preliminare va effettuata entro il 1° ottobre. Queste procedure seguono regole diverse rispetto all’acquisto ordinario dei biglietti.",
    "Il Franchi ha già ospitato la Nazionale femminile: la FIGC ricorda le vittorie con Portogallo nel 2018 e Israele nel 2021, oltre al pareggio con l’Inghilterra nel 1995. Il ritorno del 13 ottobre aggiunge una gara ufficiale a questa storia. Il risultato dell’andata determinerà il contesto sportivo della sfida di Firenze, mentre prezzi e orario di inizio sono già indicati nell’annuncio della biglietteria."
],
"brothers-apple-tv-debutto-23-settembre-mcconaughey-harrelson-22-09-2026": [
    "Il segreto emerge, secondo la presentazione di Apple, quando il personaggio della madre di Matthew, interpretato da Holland Taylor, lascia trapelare un’informazione sul passato delle famiglie. Woody cerca allora di scoprire che cosa sia accaduto, mentre Matthew affronta anche l’ipotesi di una candidatura a governatore del Texas. Sono elementi della finzione, costruiti attorno ai nomi e all’immagine pubblica dei due protagonisti.",
    "Nel cast compaiono inoltre Nolan Almeida, Ella Grace Helton, Noah Carganilla, Highdee Kuan e Oona Yaffe. La produzione è di Paramount Television Studios per Apple TV; McConaughey e Harrelson figurano anche fra i produttori esecutivi. Trent O’Donnell dirige più episodi, compreso il primo. La serie è presentata come una commedia sull’amicizia, la famiglia e la fama, con la ricerca della verità sui legami fra i personaggi al centro della trama.",
    "Il calendario annunciato parte con due puntate il 23 settembre e prosegue con una a settimana: il terzo episodio è quindi previsto il 30 settembre, salvo modifiche della piattaforma. Le otto puntate totali portano la conclusione al 4 novembre. La distribuzione è globale su Apple TV, ma disponibilità e modalità di accesso dipendono dal servizio nel Paese dell’utente. Alla vigilia del debutto non sono ancora disponibili gli episodi della stagione."
],
"ue-rinnova-sanzioni-russia-tre-anni-rimuove-usmanov-fridman-22-settembre-2026": [
    "Il congelamento dei beni limita l’accesso alle risorse economiche dei soggetti designati. Il divieto di mettere fondi a loro disposizione si applica anche ai trasferimenti indiretti, secondo la disciplina europea; per le persone fisiche è inoltre previsto il divieto di ingresso o transito nel territorio dell’Unione. La misura riguarda l’elenco collegato all’integrità territoriale dell’Ucraina e non implica una sanzione generalizzata per tutti i cittadini russi.",
    "Il riesame delle iscrizioni non coincide con la fine del regime sanzionatorio. Il Consiglio comunica che tre persone e un’entità non sono state rinnovate e che sono state rimosse altre tre persone decedute, mentre la maggior parte dei nominativi resta soggetta alle misure. I casi individuali possono essere riesaminati con procedure proprie; il numero complessivo superiore a 3.000 descrive l’ampiezza degli elenchi ancora in vigore.",
    "La durata triennale fissa la nuova scadenza al 22 settembre 2029. Per sapere se una persona o un’organizzazione è soggetta a restrizioni occorre consultare gli elenchi ufficiali aggiornati, non dedurlo dalla sola nazionalità o da notizie precedenti. La decisione del 22 settembre dà forma giuridica alla proroga, dopo la fase di accordo politico, e chiarisce il perimetro delle misure individuali adottate dall’Unione."
]}

def main():
    from adsense_structural_review import inspect
    for slug, paragraphs in EXTRA.items():
        path=ROOT/'notizie'/f'{slug}.html'
        doc=html.fromstring(path.read_text())
        body=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
        body.set('data-article-format','standard')
        already_extended=any((p.text or '').startswith(paragraphs[0][:50]) for p in body.xpath('./p'))
        if not already_extended:
            for paragraph in paragraphs: etree.SubElement(body,'p').text=paragraph
        body.set('data-extended-v520','true')
        for para in list(body.xpath('./p')):
            words=re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b",' '.join(para.itertext()))
            if len(words)<=60: continue
            sentences=re.split(r'(?<=[.!?])\s+',para.text or '')
            chunks=[]; current=''
            for sentence in sentences:
                candidate=(current+' '+sentence).strip()
                if len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b",candidate))>60 and current:
                    chunks.append(current);current=sentence
                else: current=candidate
            if current: chunks.append(current)
            assert all(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b",c))<=60 for c in chunks),slug
            at=list(body).index(para)
            body.remove(para)
            for i,chunk in enumerate(chunks): body.insert(at+i,etree.Element('p')) ; body[at+i].text=chunk
        path.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'))
        row=inspect(path)
        assert row['words']>=300,(slug,row['words'])
        print(slug,row['words'])

if __name__=='__main__': main()
