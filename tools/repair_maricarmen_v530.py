#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notizie/maricarmen-87-anni-sfrattata-madrid-proteste-23-settembre-2026.html"
text = path.read_text(encoding="utf-8")
replacements = {
    "L’edificio è passato nel 2018 a Urbagestión Desarrollo e Inversión. Secondo il Sindicato de Inquilinas, la società aveva proposto un canone mensile di 2.650 euro, contro i circa 500 euro versati fino ad allora da Maricarmen. La donna percepisce una pensione indicata dalle fonti in circa 1.350 euro al mese e ha una disabilità riconosciuta del 50 per cento.":
    "L’edificio è passato nel 2018 a Urbagestión Desarrollo e Inversión. Secondo il Sindicato de Inquilinas, la società aveva proposto un canone di 2.650 euro, contro i circa 500 versati fino ad allora da Maricarmen. La donna percepisce una pensione indicata dalle fonti in circa 1.350 euro al mese e ha una disabilità riconosciuta del 50 per cento.",
    "Il contratto originario di affitto a canone regolato era stato firmato dai genitori nel 1956. Dopo la morte del padre era passato alla madre e, nel 2005, a Maricarmen. La controversia nasce dalla seconda successione nel contratto: la proprietà ne ha chiesto la cessazione, mentre la difesa dell’inquilina ha sostenuto che la normativa dell’epoca non permetteva alla madre di figurare come cointestataria.":
    "Il contratto di affitto era stato firmato dai genitori nel 1956. Dopo la morte del padre era passato alla madre e, nel 2005, a Maricarmen. La controversia nasce dalla seconda successione: la proprietà ne ha chiesto la cessazione, mentre la difesa dell’inquilina ha sostenuto che la normativa dell’epoca non permetteva alla madre di figurare come cointestataria.",
    "Alla vigilia dello sgombero una donatrice anonima si era offerta di coprire la differenza fra il vecchio canone e quello richiesto, oltre agli arretrati. La proposta non ha fermato il procedimento. Anche il Ministero spagnolo dell’Edilizia aveva chiesto alle amministrazioni locali di intervenire e aveva appoggiato la richiesta delle Nazioni Unite di sospendere cautelarmente il rilascio fino alla disponibilità di una soluzione abitativa adeguata.":
    "Alla vigilia dello sgombero una donatrice anonima si era offerta di coprire la differenza fra il vecchio canone e quello richiesto, oltre agli arretrati. La proposta non ha fermato il procedimento. Il Ministero dell’Edilizia aveva chiesto alle amministrazioni locali di intervenire e appoggiato la richiesta dell’ONU di sospendere il rilascio fino alla disponibilità di una soluzione abitativa adeguata.",
}
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
