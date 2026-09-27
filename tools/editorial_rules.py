"""Regole di formato comuni ai gate; le fasce v502 sono orientative.

La verifica della sostanza e dell'indipendenza delle fonti resta editoriale.
Un flash breve non va riempito per superare una quota automatica.
"""
import re
from urllib.parse import urlparse

WORD_RE = re.compile(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b")
FORMAT_WORD_RANGES = {'flash': [100, 250], 'standard': [300, 700], 'feature': [800, 1500]}


def format_errors(body):
    if body is None:
        return ['corpo articolo assente']
    words = WORD_RE.findall(' '.join(body.itertext()))
    # Lo storico senza protocollo esplicito usa standard; il protocollo 4.0
    # deve continuare a dichiarare il formato nel markup.
    default_format = '' if body.get('data-editorial-protocol') == '4.0' else 'standard'
    fmt = body.get('data-article-format', default_format)
    errors = []
    if not words:
        errors.append('corpo articolo vuoto')
    if fmt not in FORMAT_WORD_RANGES:
        errors.append('formato editoriale non valido')
    elif fmt == 'flash' and len(words) >= 300:
        errors.append('testo di almeno 300 parole da classificare standard o feature')
    elif fmt != 'flash' and 0 < len(words) < 300:
        errors.append('testo sotto 300 parole da classificare flash')
    return errors


def external_source_urls(doc):
    """Le pagine istituzionali di CurioMondo non sono fonti della notizia."""
    values = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]//a/@href')
    return {
        value for value in values
        if urlparse(value).scheme in ('http', 'https')
        and urlparse(value).hostname not in ('curiomondo.it', 'www.curiomondo.it')
    }


def source_errors(doc, body):
    level = body.get('data-risk-level', '') if body is not None else ''
    if level and level not in ('A', 'B', 'C'):
        return ['livello di rischio non valido']
    required = 2 if level == 'A' else 1
    if len(external_source_urls(doc)) < required:
        return [f'fonti esterne insufficienti per rischio {level or "ordinario"}: richieste {required}']
    return []
