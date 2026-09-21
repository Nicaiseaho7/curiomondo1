"""Verifica editoriale e stesura dell'articolo.

Due passaggi distinti, e l'ordine conta.

Il primo decide **se** la notizia merita una pagina CurioMondo. Non è una
domanda sulla verità del fatto: è la domanda del protocollo editoriale, cioè se
esiste una fonte solida e se abbiamo qualcosa da aggiungere. Una riscrittura di
un lancio d'agenzia, per quanto corretta, non va pubblicata.

Il secondo scrive l'articolo, e lo fa soltanto sul materiale realmente letto
dalle fonti. Ogni vincolo del protocollo che il gate `predeploy.py` verifica in
automatico è ripetuto qui: è meglio che il modello lo sappia in partenza
piuttosto che vedersi rifiutare l'articolo alla fine.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from .extract import Extracted
from .normalize import dominio
from .openai_client import Client, Usage

# Categorie reali del sito: il modello non deve inventarne di nuove.
CATEGORIE = (
    "Italia", "Mondo", "Politica", "Cronaca", "Economia",
    "Sport", "Tecnologia", "Cultura", "Scienza", "Ambiente",
)

FORMATI = {"flash": (100, 250), "standard": (300, 600), "feature": (800, 1500)}

SISTEMA_VERIFICA = """Sei il caporedattore di CurioMondo, una testata italiana.

Decidi se una notizia merita una pagina originale. Non stai giudicando se il
fatto sia vero: stai applicando il protocollo editoriale di CurioMondo.

Il protocollo vieta di pubblicare articoli che siano soltanto riscritture,
riassunti, traduzioni o aggregazioni di fonti esterne. Citare fonti affidabili
è obbligatorio ma non è di per sé valore editoriale.

Apri un articolo solo se TUTTE queste condizioni sono vere:
1. La notizia poggia su una base solida, cioe almeno una fra queste:
   - una fonte primaria (ente, comunicato, dataset, atto ufficiale);
   - il resoconto diretto di un'agenzia o di una testata di prima fascia
     (ANSA, AFP, Reuters, AP, BBC, Guardian, Deutsche Welle e simili);
   - due fonti indipendenti e nominabili che riportano lo stesso fatto.
   Il resoconto di una sola testata affidabile e una base sufficiente per una
   notizia ordinaria: cio che conta e che i fatti siano attribuiti a chi li ha
   riferiti. Per i temi delicati questa base non basta (vedi sotto).
2. Sai dire in una frase quale valore aggiunto porta CurioMondo.
3. C'è abbastanza materia verificata per un pezzo autonomo. Se manca, non si
   allunga: si attende o non si pubblica.

Il valore aggiunto deve essere ALMENO DUE tra:
- spiegazione di un dato o metodo, compreso cio che non misura;
- limite o incertezza espliciti;
- confronto utile con un periodo, una media, un luogo o un precedente;
- scheda pratica con date, destinatari, procedura o conseguenze per il lettore;
- aggiornamento sostanziale rispetto a quanto gia noto.

Standard piu severi per notizie delicate (guerra, morti, incidenti, salute,
giustizia, geopolitica, elezioni):
- serve una fonte primaria oppure una conferma indipendente: il resoconto di
  una sola testata non basta per aprire il pezzo;
- la dichiarazione di una sola parte NON e un fatto accertato;
- se le fonti discordano, o se il fatto e rivendicato da una parte in conflitto,
  serve una conferma indipendente oppure l'articolo non si apre;
- numeri di vittime, responsabilita e cause richiedono attribuzione esplicita.

Rifiuta sempre: rumor, gossip, indiscrezioni non verificabili, contenuti
promozionali, aggiornamenti insignificanti, fatti gia raccontati senza sviluppi.

Rispondi solo in JSON."""

SISTEMA_STESURA = """Sei un redattore di CurioMondo. Scrivi in italiano standard,
adulto e preciso.

Scrivi ESCLUSIVAMENTE sulla base del materiale fornito. Non aggiungere fatti,
cifre, cause, scene, emozioni o citazioni che non siano nel materiale. Se un
elemento non e noto, dichiaralo invece di ipotizzarlo.

Struttura obbligatoria (piramide invertita):
1. Titolo chiaro e fattuale, senza clickbait, coerente con il fatto.
2. Sommario di una o due frasi che completano il titolo con un dettaglio chiave,
   senza ripeterlo.
3. Primo paragrafo: il nocciolo della notizia, con chi, cosa, quando, dove e
   perche. Se una di queste manca, dillo.
4. Corpo: dettagli, cifre, citazioni attribuite e contesto in ordine decrescente
   di importanza.
5. Chiusura: solo background o precedente pertinente. Vietati morale, commento
   e riepilogo del lead.

Regole di scrittura, tutte obbligatorie:
- Un'idea per paragrafo: da 2 a 4 frasi, MAI piu di 60 parole per paragrafo.
- Frasi brevi, soggetto-verbo-complemento, circa 20-25 parole.
- Vietata ogni ripetizione: nessuna frase e nessun paragrafo puo ripetere un
  altro, nemmeno riformulato con parole diverse. Un controllo automatico
  rifiuta l'articolo se due frasi si somigliano troppo.
- Niente riempitivi, avverbi inutili, aggettivi enfatici, prima persona,
  giudizi di valore o formule emotive.
- Non spiegare parole difficili, sigle o termini tecnici nel corpo: usa un
  lessico comune.
- Le dichiarazioni vanno attribuite ("secondo il ministero", "ha riferito
  l'agenzia"). Una rivendicazione di parte non diventa mai un fatto accertato.
- Vietato aggiungere contesto generico solo per allungare il testo.
- Attribuisci a chi ha parlato o deciso (l'ente, l'azienda, la persona), non
  alla testata che ha dato la notizia: il nome della testata puo comparire al
  massimo una volta, e solo se serve davvero.
- Se un dato non e noto, dillo nel punto in cui servirebbe. Vietato chiudere
  con un elenco di cio che il materiale non dice: non e un articolo, e un
  verbale.

Rispondi solo in JSON."""


def slugify(testo: str) -> str:
    piatto = unicodedata.normalize("NFD", testo or "")
    piatto = "".join(c for c in piatto if unicodedata.category(c) != "Mn").lower()
    piatto = re.sub(r"[^a-z0-9]+", "-", piatto).strip("-")
    return re.sub(r"-{2,}", "-", piatto)[:90].strip("-")


@dataclass
class Verdetto:
    pubblicare: bool
    motivo: str
    formato: str = "standard"
    categoria: str = ""
    fonte_primaria: bool = False
    fonti_indipendenti: int = 0
    valore_aggiunto: list[str] = None  # type: ignore[assignment]
    rischio_disinformazione: str = "basso"
    sensibile: bool = False
    grezzo: dict[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self):
        self.valore_aggiunto = self.valore_aggiunto or []
        self.grezzo = self.grezzo or {}


def _materiale(titolo: str, fonte: str, estratti: list[Extracted], limite_caratteri: int = 9000) -> str:
    """Prepara il materiale letto dalle fonti, con un tetto di lunghezza."""
    pezzi = [f"TITOLO SEGNALATO: {titolo}", f"FONTE SEGNALANTE: {fonte}", ""]
    quota = max(1200, limite_caratteri // max(1, len([e for e in estratti if e.ok])))
    for indice, estratto in enumerate(estratti, 1):
        if not estratto.ok:
            pezzi.append(f"[FONTE {indice}] non leggibile ({estratto.reason}) — {estratto.url}")
            continue
        pezzi.append(f"[FONTE {indice}] {estratto.title or '(senza titolo)'}\nURL: {estratto.url}\n{estratto.text[:quota]}")
        pezzi.append("")
    return "\n".join(pezzi)


def url_citabili(estratti: list[Extracted], conferme: list[dict[str, Any]]) -> list[str]:
    """Indirizzi che l'articolo puo citare come fonte, senza ripetizioni.

    Sono le pagine lette, le testate che riportano lo stesso fatto e i documenti
    ufficiali richiamati dentro gli articoli. Servono due indirizzi distinti:
    citare due volte la stessa pagina non fa due fonti.
    """
    indirizzi: list[str] = []
    for estratto in estratti:
        if estratto.ok:
            indirizzi.append(estratto.url)
    for conferma in conferme:
        if conferma.get("url"):
            indirizzi.append(str(conferma["url"]))
    for estratto in estratti:
        indirizzi.extend(estratto.links)
    return list(dict.fromkeys(i for i in indirizzi if i))


def verifica(
    client: Client,
    modello: str,
    titolo: str,
    fonte: str,
    estratti: list[Extracted],
    conferme: list[dict[str, Any]],
    alto_rischio: bool,
    gia_pubblicati: list[str] | None = None,
    tier: str = "",
    trust: str = "",
) -> tuple[Verdetto, Usage]:
    """Decide se la notizia merita una pagina CurioMondo."""
    leggibili = [e for e in estratti if e.ok]
    contesto = [
        _materiale(titolo, fonte, estratti),
        f"FONTI INDIPENDENTI CHE RIPORTANO IL FATTO: {1 + len(conferme)}",
    ]
    if tier or trust:
        # Il modello non puo indovinare se chi segnala e un'agenzia o un blog:
        # senza questo dato tende a rifiutare tutto per prudenza.
        contesto.append(
            f"NATURA DELLA FONTE SEGNALANTE: {tier or 'ignota'}, affidabilita {trust or 'ignota'}"
        )
    if conferme:
        contesto.append("Altre testate: " + ", ".join(c.get("source", "") for c in conferme))
    if alto_rischio:
        contesto.append(
            "ATTENZIONE: il filtro ha classificato questo tema come delicato. "
            "Applica gli standard di verifica piu severi."
        )
    if gia_pubblicati:
        contesto.append(
            "Titoli gia pubblicati da CurioMondo di recente (non ripetere lo stesso fatto):\n- "
            + "\n- ".join(gia_pubblicati[:25])
        )

    schema = """Rispondi con questo JSON:
{
  "pubblicare": true oppure false,
  "motivo": "una frase che spiega la decisione",
  "formato": "flash" | "standard" | "feature",
  "categoria": una tra Italia, Mondo, Politica, Cronaca, Economia, Sport, Tecnologia, Cultura, Scienza, Ambiente,
  "fonte_primaria": true se esiste un ente/comunicato/dataset/atto ufficiale,
  "fonti_indipendenti": numero di fonti distinte che riportano il fatto,
  "valore_aggiunto": ["elemento 1", "elemento 2"],
  "rischio_disinformazione": "basso" | "medio" | "alto",
  "sensibile": true se riguarda guerra, morti, incidenti, salute, giustizia o elezioni,
  "dichiarazione_di_parte": true se il fatto e rivendicato da una sola parte interessata
}"""

    dati, uso = client.complete_json(
        model=modello,
        system=SISTEMA_VERIFICA,
        user="\n\n".join(contesto),
        schema_hint=schema,
        # Il giudizio è breve, ma il modello ragiona prima di darlo: il tetto
        # deve coprire il ragionamento, altrimenti si paga una risposta vuota.
        max_tokens=4000,
        sforzo="low",
    )

    pubblicare = bool(dati.get("pubblicare"))
    motivo = str(dati.get("motivo", "")).strip()
    valori = [str(v) for v in (dati.get("valore_aggiunto") or []) if str(v).strip()]
    categoria = str(dati.get("categoria", "")).strip()

    # Regole non negoziabili, applicate in codice e non lasciate al modello:
    # il protocollo le impone e un modello puo sempre distrarsi.
    if pubblicare and len(valori) < 2:
        pubblicare, motivo = False, "meno di due elementi di valore aggiunto: solo riscrittura"
    if pubblicare and not leggibili:
        pubblicare, motivo = False, "nessuna fonte leggibile: non c'e materia verificata"
    if pubblicare and str(dati.get("rischio_disinformazione", "")).lower() == "alto":
        pubblicare, motivo = False, "rischio di disinformazione alto"
    if pubblicare and dati.get("dichiarazione_di_parte") and (1 + len(conferme)) < 2:
        pubblicare, motivo = False, "rivendicazione di una sola parte senza conferme indipendenti"
    # Sui temi delicati il resoconto di una sola testata non basta: o c'e un
    # atto ufficiale, o c'e qualcun altro che riporta lo stesso fatto.
    if (pubblicare and bool(dati.get("sensibile"))
            and not dati.get("fonte_primaria") and (1 + len(conferme)) < 2):
        pubblicare, motivo = False, "tema delicato senza fonte primaria ne conferma indipendente"
    if pubblicare and categoria not in CATEGORIE:
        categoria = "Mondo"

    verdetto = Verdetto(
        pubblicare=pubblicare,
        motivo=motivo,
        formato=str(dati.get("formato", "standard")).lower() if str(dati.get("formato", "")).lower() in FORMATI else "standard",
        categoria=categoria,
        fonte_primaria=bool(dati.get("fonte_primaria")),
        fonti_indipendenti=int(dati.get("fonti_indipendenti") or (1 + len(conferme))),
        valore_aggiunto=valori,
        rischio_disinformazione=str(dati.get("rischio_disinformazione", "basso")).lower(),
        sensibile=bool(dati.get("sensibile")),
        grezzo=dati,
    )
    return verdetto, uso


def scrivi(
    client: Client,
    modello: str,
    titolo: str,
    fonte: str,
    estratti: list[Extracted],
    verdetto: Verdetto,
    conferme: list[dict[str, Any]],
) -> tuple[dict[str, Any], Usage]:
    """Genera l'articolo rispettando il contratto che il gate verifica."""
    minimo, massimo = FORMATI.get(verdetto.formato, FORMATI["standard"])
    obiettivo = int((minimo + massimo) / 2)

    istruzioni = f"""Scrivi l'articolo CurioMondo su questo fatto.

FORMATO: {verdetto.formato} — il corpo deve stare fra {minimo} e {massimo} parole
(punta a circa {obiettivo}). La misura e una conseguenza dell'informazione
disponibile, mai un obiettivo da riempire.

CATEGORIA: {verdetto.categoria}

VALORE AGGIUNTO da rendere esplicito nel testo:
- """ + "\n- ".join(verdetto.valore_aggiunto)

    citabili = url_citabili(estratti, conferme)
    istruzioni += "\n\nINDIRIZZI CITABILI (usane almeno due DIVERSI, copiati esattamente):\n- " + "\n- ".join(citabili)

    if verdetto.sensibile:
        istruzioni += (
            "\n\nTEMA DELICATO: attribuisci ogni numero e ogni responsabilita. "
            "Dichiara cosa non e ancora confermato. Nessuna scena ricostruita."
        )

    schema = """Rispondi con questo JSON:
{
  "titolo": "titolo fattuale, max 100 caratteri, senza clickbait",
  "sommario": "una o due frasi che completano il titolo senza ripeterlo, 150-250 caratteri",
  "luogo": "citta o paese del fatto, una o due parole",
  "paragrafi": ["primo paragrafo con le 5 W", "secondo", "..."],
  "fonti": [{"url": "url reale preso dal materiale", "descrizione": "cosa conferma questa fonte"}],
  "parole_chiave_titolo": ["fino a 2 parole o cifre PRESENTI NEL TITOLO da evidenziare"],
  "dati_chiave": [
    {"icona": "un solo carattere tipo ◆ ▲ ●", "valore": "cifra o parola breve", "etichetta": "cosa rappresenta, max 6 parole"}
  ],
  "immagine": {
    "prompt": "descrizione in inglese di una fotografia editoriale ultrarealistica specifica per questa notizia, con le persone reali nominate, maglie e loghi ufficiali veri, senza volti inventati, testo, titoli, watermark o infografiche",
    "alt": "alt text italiano che dichiara scena editoriale contestuale ordinaria oppure ritratto editoriale neutrale per situazione sensibile",
    "personaggio_pubblico": true oppure false,
    "contesto_sensibile": true oppure false
  }
}

Vincoli tassativi:
- ogni paragrafo: massimo 60 parole, da 2 a 4 frasi;
- nessuna frase puo somigliare a un'altra: un controllo automatico rifiuta l'articolo;
- da 3 a 6 fonti, con URL presi dal materiale fornito e mai inventati;
- esattamente 3 elementi in "dati_chiave", tutti ricavati da cifre o fatti presenti nel materiale;
- "parole_chiave_titolo" deve contenere parole che compaiono ESATTAMENTE nel titolo che hai scritto;
- il prompt immagine deve descrivere una fotografia editoriale professionale nuova e specifica, con le persone reali nominate e i loghi/maglie ufficiali, senza volti inventati e senza testo nei pixel;
- se la notizia riguarda morte, incidente, malattia, violenza, guerra, catastrofe, arresto, accuse gravi, lutto o sofferenza, il visual non deve ricostruire il trauma. Se raffigura un personaggio pubblico deve essere soltanto un ritratto neutrale isolato."""

    dati, uso = client.complete_json(
        model=modello,
        system=SISTEMA_STESURA,
        user=_materiale(titolo, fonte, estratti) + "\n\n" + istruzioni,
        schema_hint=schema,
        max_tokens=9000,
        sforzo="medium",
    )
    dati["formato"] = verdetto.formato
    dati["categoria"] = verdetto.categoria
    dati["slug"] = slugify(str(dati.get("titolo", titolo)))
    return dati, uso


def controlla_articolo(
    articolo: dict[str, Any],
    allowed_source_urls: set[str] | None = None,
) -> list[str]:
    """Verifica in codice i vincoli che il gate applicherà comunque.

    Serve a scartare subito un articolo difettoso, invece di scoprirlo alla
    fine della pipeline quando è già costato un'immagine e un deploy.
    """
    problemi: list[str] = []
    paragrafi = [str(p).strip() for p in (articolo.get("paragrafi") or []) if str(p).strip()]
    if not paragrafi:
        return ["nessun paragrafo"]

    formato = articolo.get("formato", "standard")
    minimo, massimo = FORMATI.get(formato, FORMATI["standard"])
    parole = len(re.findall(r"\b[\w'’]+\b", " ".join(paragrafi)))
    if parole < minimo or parole > massimo:
        problemi.append(f"lunghezza {formato} fuori fascia: {parole} parole (attese {minimo}-{massimo})")

    for indice, paragrafo in enumerate(paragrafi, 1):
        conteggio = len(re.findall(r"\b[\w'’]+\b", paragrafo))
        if conteggio > 60:
            problemi.append(f"paragrafo {indice} oltre 60 parole ({conteggio})")

    titolo = str(articolo.get("titolo", "")).strip()
    if not titolo:
        problemi.append("titolo assente")
    elif len(titolo) > 120:
        problemi.append("titolo troppo lungo")

    if not str(articolo.get("sommario", "")).strip():
        problemi.append("sommario assente")

    fonti = articolo.get("fonti") or []
    valide = [f for f in fonti if str(f.get("url", "")).startswith("http")]
    urls = [str(f.get("url", "")).strip() for f in valide]
    if len(valide) < 2:
        problemi.append(f"meno di due fonti con URL ({len(valide)})")
    if len(set(urls)) != len(urls):
        problemi.append("fonti duplicate")
    if len(urls) > 6:
        problemi.append(f"piu di sei fonti ({len(urls)})")
    # Due testate, non due indirizzi: lo stesso lancio ANSA ripreso da un
    # aggregatore cambia URL ma resta una fonte sola, e il gate del sito conta
    # i link senza accorgersene.
    testate = {dominio(u) for u in urls} - {""}
    if len(testate) < 2:
        problemi.append(f"meno di due testate distinte fra le fonti ({len(testate)})")
    if allowed_source_urls is not None:
        inventate = [url for url in urls if url not in allowed_source_urls]
        if inventate:
            problemi.append("URL fonte non presente nel materiale")

    dati_chiave = articolo.get("dati_chiave") or []
    if len(dati_chiave) != 3:
        problemi.append(f"servono esattamente 3 dati chiave ({len(dati_chiave)})")

    # Le parole evidenziate devono esistere nel titolo, altrimenti la card in
    # evidenza mostrerebbe un'evidenziazione che non corrisponde a nulla.
    chiavi = [str(k) for k in (articolo.get("parole_chiave_titolo") or []) if str(k).strip()]
    assenti = [k for k in chiavi if k.lower() not in titolo.lower()]
    if assenti:
        problemi.append(f"parole chiave non presenti nel titolo: {', '.join(assenti)}")
    if not chiavi:
        problemi.append("nessuna parola chiave da evidenziare nel titolo")

    immagine = articolo.get("immagine") or {}
    prompt = str(immagine.get("prompt", "")).strip()
    alt = str(immagine.get("alt", "")).strip()
    if len(prompt) < 80:
        problemi.append("prompt immagine assente o troppo generico")
    if not alt:
        problemi.append("alt text immagine assente")
    if articolo.get("verifica", {}).get("sensibile") and immagine.get("personaggio_pubblico"):
        if not immagine.get("contesto_sensibile"):
            problemi.append("personaggio pubblico sensibile senza contesto_sensibile")

    return problemi
