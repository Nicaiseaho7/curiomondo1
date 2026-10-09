#!/usr/bin/env python3
"""Quattro notizie Italia del 9 ottobre 2026, non presenti nel sito."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 821
OUT = ROOT / "assets" / "images" / "editorial-auto"
SOURCES = {
    "firenze": Path("/workspace/artifacts/imagine_images/b8bdc7ba-8b82-4d23-82f3-8ec360a41c56.jpg"),
    "santanche": Path("/workspace/artifacts/imagine_images/a7dc3974-02ac-4f87-9c5d-1ee5434ccc6b.jpg"),
    "antinori": Path("/workspace/artifacts/imagine_images/cc77d9f3-954d-43d0-8768-6951e598d2fa.jpg"),
    "salvini": Path("/workspace/artifacts/imagine_images/fe3a6e77-fa83-4c77-821d-c9834e149ff0.jpg"),
}


def variants(src: Path, slug: str) -> list[dict]:
    image = Image.open(src).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    rows = []
    for width in (480, 800, 1200):
        path = OUT / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / ratio)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=89, method=6
        )
        rows.append({
            "w": width,
            "h": round(width / ratio),
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return rows


ARTICLES = [
    {
        "slug": "salvini-voto-fine-legislatura-autunno-2027-09-10-2026",
        "titolo": "Salvini: per la Lega si vota nell’autunno del 2027",
        "sommario": "A margine di una conferenza al ministero delle Infrastrutture il vicepremier indica la scadenza naturale della legislatura. Non è un calendario fissato dal governo.",
        "categoria": "Politica",
        "luogo": "Roma",
        "formato": "standard",
        "image_key": "salvini",
        "image_alt": "Sala stampa vuota di un ministero italiano, senza persone; illustrazione editoriale, non la conferenza di Salvini.",
        "paragrafi": [
            "Matteo Salvini ha detto che, per la Lega, il voto resta fissato alla fine naturale della legislatura, nell’autunno del 2027. Lo ha dichiarato venerdì 9 ottobre a Roma, a margine di una conferenza stampa al Ministero delle infrastrutture e dei trasporti.",
            "Secondo l’ANSA, il vicepremier ha legato quella data al lavoro ancora aperto: «così tante cose da fare, così tanti cantieri da completare, così tante case da riassegnare». È una posizione politica, non un atto che sposti da solo la scadenza delle Camere.",
            "Nella stessa occasione ha rivendicato l’approvazione della legge elettorale. Ha detto che per mesi era stato spiegato che la maggioranza non avrebbe avuto i numeri e che invece «i numeri c’erano». Sulla riforma, ha aggiunto, ci sono state «troppe chiacchiere inutili».",
            "La legge è già stata approvata in via definitiva alla Camera l’8 ottobre, con 227 sì a scrutinio segreto. Le parole di oggi non aggiungono un nuovo voto in Aula: indicano che Salvini non spinge, almeno in questa dichiarazione, per un’elezione anticipata.",
        ],
        "dati_chiave": [
            {"valore": "2027", "etichetta": "autunno indicato da Salvini"},
            {"valore": "MIT", "etichetta": "sede della conferenza stampa"},
            {"valore": "227", "etichetta": "sì della Camera sulla legge elettorale"},
        ],
        "fonti": [
            {"nome": "ANSA", "url": "https://www.gazzettadiparma.it/italia-mondo/2026/10/09/news/salvini-per-noi-si-vota-a-fine-legislatura-nell-autunno-del-2027-973284/"},
            {"nome": "Corriere della Calabria", "url": "https://www.corrieredellacalabria.it/2026/10/09/salvini-per-noi-si-vota-a-fine-legislatura/"},
        ],
        "correlati": [
            {"url": "/notizie/legge-elettorale-voto-finale-camera-227-si-08-10-2026.html", "titolo": "Legge elettorale, sì definitivo con 227 voti"},
            {"url": "/notizie/salvini-contributo-volontario-banche-assicurazioni-5-miliardi-2027.html", "titolo": "Salvini e il contributo volontario di banche e assicurazioni"},
        ],
    },
    {
        "slug": "furto-antinori-cortona-30mila-bottiglie-09-10-2026",
        "titolo": "Cortona, furto da circa 5 milioni alle cantine Antinori",
        "sommario": "L’azienda riferisce la sottrazione di circa 30 mila bottiglie di pregio dal polo logistico di Cortona. Il colpo, scoperto lunedì, è stato raccontato oggi. Nessun arresto risulta ancora disposto.",
        "categoria": "Cronaca",
        "luogo": "Cortona",
        "formato": "standard",
        "image_key": "antinori",
        "image_alt": "Magazzino di bottiglie senza etichette leggibili, di notte; illustrazione editoriale, non una foto del furto.",
        "paragrafi": [
            "Marchesi Antinori ha subito un furto di vino di pregio nel polo logistico di Cortona, in provincia di Arezzo. Il Sole 24 Ore e la Repubblica, che citano il Financial Times e l’amministratore delegato Renzo Cotarella, indicano circa 30 mila bottiglie e un valore intorno ai 5 milioni di euro.",
            "Secondo la ricostruzione riferita dall’azienda, sette uomini mascherati sono entrati nel magazzino nella notte tra sabato e domenica, hanno disattivato l’allarme e hanno caricato il vino su due autotreni. Il furto è stato scoperto lunedì mattina, quando sono arrivati i dipendenti. Le telecamere avrebbero ripreso la scena.",
            "Cotarella, citato dal Sole, ha detto che si tratta di persone esperte anche di vino, a giudicare dalle etichette scelte. Ha indicato, in via ancora da verificare, circa 10-12 mila bottiglie di Solaia, altrettante di Tignanello e altre referenze come il Guado al Tasso, comprese magnum e formati speciali. I prezzi al dettaglio citati vanno da circa 150 a 500 euro a bottiglia.",
            "La polizia sta indagando. Al momento le fonti non riferiscono arresti. Cotarella ha detto di non sapere come una quantità simile possa essere rivenduta senza essere notata.",
        ],
        "dati_chiave": [
            {"valore": "30 mila", "etichetta": "bottiglie indicate come sottratte"},
            {"valore": "5 milioni", "etichetta": "euro, valore stimato"},
            {"valore": "0", "etichetta": "arresti riferiti finora"},
        ],
        "fonti": [
            {"nome": "Il Sole 24 Ore", "url": "https://www.ilsole24ore.com/art/vino-furto-5-milioni-cantine-antinori-cortona-AJTjFJeB"},
            {"nome": "la Repubblica", "url": "https://www.repubblica.it/il-gusto/2026/10/09/news/vino_storico_furto_antinori_rubate_bottiglie_di_pregio_per_5_milioni_di_euro-425636021/"},
        ],
        "correlati": [
            {"url": "/notizie/firenze-globale-mostra-francesco-carletti-9-ottobre-2026.html", "titolo": "Firenze globale, la mostra su Carletti"},
        ],
    },
    {
        "slug": "santanche-diffamazione-giudice-invia-atti-consulta-09-10-2026",
        "titolo": "Santanchè, il giudice invia gli atti alla Consulta",
        "sommario": "Nel processo per diffamazione il tribunale di Roma solleva un conflitto di attribuzione dopo il no del Senato all’autorizzazione a procedere. La difesa aveva chiesto il non luogo a procedere.",
        "categoria": "Politica",
        "luogo": "Roma",
        "formato": "standard",
        "image_key": "santanche",
        "image_alt": "Aula di tribunale vuota con un fascicolo chiuso; illustrazione editoriale, non il processo.",
        "paragrafi": [
            "Il giudice monocratico di Roma ha disposto l’invio degli atti alla Corte costituzionale nel procedimento che vede imputata Daniela Santanchè per diffamazione. Lo riferiscono ANSA, la Repubblica e LaPresse. Il giudice Emilia Conforti ha sollevato un conflitto di attribuzione.",
            "Il Senato, a luglio, aveva riconosciuto l’insindacabilità delle opinioni espresse in Aula e aveva negato l’autorizzazione a procedere. In udienza la difesa ha chiesto di prenderne atto e di dichiarare il non luogo a procedere. Il giudice non ha chiuso il processo: ha chiesto alla Consulta di dichiarare che quella valutazione non spettava al Senato.",
            "L’accusa riguarda un intervento del 5 luglio 2023. Secondo il capo di imputazione, parlando in Senato dell’inchiesta che la riguardava, Santanchè avrebbe offeso la reputazione di Giuseppe Zeno, azionista di minoranza di Visibilia Editore. Le frasi contestate descrivono i suoi trasferimenti e restano, in questa fase, un’imputazione, non un fatto accertato.",
            "Santanchè è senatrice ed è stata ministra del Turismo. Il rinvio alla Consulta sospende la decisione sul se il processo possa proseguire. Non è una sentenza sulla diffamazione.",
        ],
        "dati_chiave": [
            {"valore": "Consulta", "etichetta": "destinataria degli atti"},
            {"valore": "Luglio", "etichetta": "voto del Senato sull’autorizzazione"},
            {"valore": "2023", "etichetta": "anno dell’intervento contestato"},
        ],
        "fonti": [
            {"nome": "ANSA", "url": "https://www.mattinopadova.it/italia/santanche-accusata-di-diffamazione-tribunale-ricorre-alla-consulta-mkdwyaxj"},
            {"nome": "la Repubblica", "url": "https://roma.repubblica.it/cronaca/2026/10/09/news/daniela_santanche_processo_diffamazione_consulta-425636977/"},
            {"nome": "LaPresse", "url": "https://lapresse.us/news/2026/10/09/santanche-case-judge-refers-case-to-constitutional-court-over-conflict-of-jurisdiction/"},
        ],
        "correlati": [
            {"url": "/notizie/meloni-senato-14-ottobre-2026-consiglio-europeo.html", "titolo": "Meloni in Senato il 14 ottobre"},
        ],
    },
    {
        "slug": "firenze-incendio-deposito-autolinee-toscane-12-autobus-09-10-2026",
        "titolo": "Firenze, incendio nel deposito degli autobus: 12 mezzi distrutti",
        "sommario": "Le fiamme sono divampate nella notte in viale XI Agosto. Altri sette bus sono danneggiati. Non risultano persone coinvolte e gli accertamenti sono aperti.",
        "categoria": "Cronaca",
        "luogo": "Firenze",
        "formato": "standard",
        "image_key": "firenze",
        "image_alt": "Deposito di autobus di notte con vigili del fuoco e mezzi anneriti; illustrazione editoriale, non il punto esatto dell’incendio.",
        "paragrafi": [
            "Un incendio nel deposito di Autolinee Toscane in viale XI Agosto, a Firenze, ha distrutto 12 autobus e ne ha danneggiati altri 7. Il bilancio è lo stesso su Il Tirreno, LaPresse e il Corriere Fiorentino. Non risultano persone coinvolte.",
            "I vigili del fuoco sono intervenuti alle 2.10 di venerdì 9 ottobre, insieme alla polizia di Stato e alla protezione civile. Hanno lavorato quattro squadre, con quattro autobotti e il mezzo aeroportuale Efestus, che ha un serbatoio da 8.100 litri d’acqua e 500 litri di liquido schiumogeno. Sono arrivati rinforzi dal distaccamento di Firenze Ovest, dalla sede centrale, dall’aeroporto, da Calenzano e dal comando di Prato. Le fiamme non si sono estese agli altri bus del deposito.",
            "Sono in corso gli accertamenti di polizia giudiziaria. Il Corriere riferisce che, secondo le prime stime, non si tratterebbe di un incendio doloso: è un’indicazione iniziale, non una conclusione. L’azienda ha avvertito che oggi possono esserci disagi sul servizio urbano di Firenze, senza un elenco di corse soppresse.",
            "Il Tirreno riporta anche il giudizio della Regione Toscana, che ha definito l’episodio un atto gravissimo. Il deposito resta il punto degli accertamenti.",
        ],
        "dati_chiave": [
            {"valore": "12", "etichetta": "autobus distrutti"},
            {"valore": "7", "etichetta": "autobus danneggiati"},
            {"valore": "2.10", "etichetta": "ora dell’intervento dei vigili del fuoco"},
        ],
        "fonti": [
            {"nome": "Il Tirreno", "url": "https://www.iltirreno.it/firenze/cronaca/2026/10/09/news/firenze-maxi-incendio-nel-deposito-degli-autobus-12-mezzi-distrutti-e-7-danneggiati-1.100927548"},
            {"nome": "LaPresse", "url": "https://www.lapresse.it/cronaca/2026/10/09/firenze-incendio-in-deposito-at-distrugge-12-autobus/"},
            {"nome": "Corriere Fiorentino", "url": "https://corrierefiorentino.corriere.it/notizie/cronaca/26_ottobre_09/firenze-maxi-incendio-nel-deposito-di-at-12-autobus-distrutti-c9d34673-e9da-42d5-b2d4-adb2c7486xlk.shtml"},
        ],
        "correlati": [
            {"url": "/notizie/tromba-aria-trapanese-marsala-petrosino-due-feriti-9-ottobre-2026.html", "titolo": "Tromba d’aria nel Trapanese"},
            {"url": "/notizie/maltempo-allerta-arancione-lazio-campania-9-ottobre-2026.html", "titolo": "Allerta arancione in Lazio e Campania"},
        ],
    },
]


def main() -> None:
    for article in ARTICLES:
        slug = article["slug"]
        image = {
            "key": f"{slug}-v{VERSION}",
            "alt": article.pop("image_alt"),
            "prompt": "illustrazione editoriale fotorealistica senza testo",
            "variants": variants(SOURCES[article.pop("image_key")], slug),
            "disclosure": site.CAPTION,
            "generator": "Imagine",
            "aiGenerated": True,
            "documentaryPhoto": False,
            "officialArtwork": False,
            "sensitiveContext": False,
            "weatherMap": False,
            "reenactedEvent": False,
        }
        written = site.write_article(article, image, VERSION)
        site.register_image(image, written, VERSION)
        print("wrote", written)


if __name__ == "__main__":
    main()
