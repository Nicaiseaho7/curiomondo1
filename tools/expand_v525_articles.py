#!/usr/bin/env python3
"""Porta i quattro articoli v525 alla lunghezza standard prevista."""
from pathlib import Path
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
EXTRA = {
 "milano-indossa-kippa-presidio-piazza-san-carlo-22-settembre-2026.html": [
  "La scelta della kippà come simbolo del presidio ha trasformato un elemento dell’identità religiosa in un gesto pubblico di vicinanza. Gli organizzatori hanno invitato anche i non ebrei a partecipare, mantenendo l’iniziativa aperta alla cittadinanza.",
  "La manifestazione si è svolta senza che fossero segnalati incidenti rilevanti. Le richieste emerse dalla piazza riguardano sicurezza, condanna dell’antisemitismo e libertà di manifestare la propria appartenenza religiosa negli spazi pubblici."],
 "juventus-multa-10000-euro-minuto-silenzio-mazzola-22-settembre-2026.html": [
  "La presa di distanza del club era arrivata subito dopo la partita. Nel valutare l’importo, il Giudice sportivo ha quindi considerato non soltanto il comportamento contestato, ma anche le iniziative adottate dalla Juventus e la reazione prevalente del pubblico.",
  "Il minuto di raccoglimento era stato disposto dalla FIGC per ricordare Mazzola su tutti i campi. Il provvedimento disciplinare chiude il profilo sportivo immediato, senza impedire ulteriori iniziative educative o comunicative da parte del club."],
 "fenerbahce-virtus-bologna-eurolega-25-settembre-2026.html": [
  "Il Fenerbahçe gioca davanti al proprio pubblico e la Virtus affronta quindi anche il fattore ambientale di una delle arene più esigenti del circuito. La scheda ufficiale non anticipa però affluenza, formazione o condizioni dei singoli giocatori.",
  "Per seguire correttamente l’incontro, i tifosi devono fare riferimento agli aggiornamenti dei canali ufficiali. Le indicazioni su trasmissione e disponibilità della rosa possono cambiare fino alla vigilia e non vanno confuse con il calendario già confermato."],
 "davis-cup-italia-corea-sud-quarti-bologna-25-novembre-2026.html": [
  "La collocazione del quarto al 25 novembre lascia all’Italia un giorno iniziale di osservazione del torneo. Non attribuisce però un vantaggio automatico: la Davis Cup si decide su singolari e doppio nell’arco della stessa sfida.",
  "I biglietti sono già disponibili attraverso il portale dell’evento, con condizioni dedicate indicate dalla FITP. Disponibilità e prezzi possono variare per sessione, perciò vanno verificati direttamente sul canale ufficiale prima dell’acquisto.",
  "L’accoppiamento offre infine un riferimento concreto alla preparazione degli azzurri, ma ogni valutazione tecnica dovrà attendere l’elenco ufficiale dei convocati."],
}
for filename, paragraphs in EXTRA.items():
 p=ROOT/'notizie'/filename; d=html.fromstring(p.read_text(encoding='utf-8'))
 body=d.xpath('//article[contains(@class,"art-body")]')[0]
 present = " ".join(body.itertext())
 for text in paragraphs:
  if text not in present: etree.SubElement(body,'p').text=text
 p.write_text(html.tostring(d,encoding='unicode',method='html',doctype='<!doctype html>')+'\n',encoding='utf-8')
print({'expanded':len(EXTRA)})
