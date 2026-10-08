#!/usr/bin/env python3
"""Prepara un lotto unico per trasferimento Git, senza leggere il manifest."""
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageOps
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 806

def main():
    payload = json.loads((ROOT / 'tools/editorial-payloads/news-20261008-v806.json').read_text())
    paths = json.loads(Path(sys.argv[1]).read_text())
    articles = []
    # Tempi reali del lotto locale: il trasferimento non è una pubblicazione live.
    now = datetime.now(ZoneInfo('Europe/Rome')).replace(microsecond=0)
    for i, article in enumerate(payload):
        article['formato'] = 'flash'
        article['parole_chiave_titolo'] = [article['titolo'].split(',')[0].split(':')[0]]
        article['dati_chiave'] = [dict(icona='◆', valore=v, etichetta=t) for v, t in article.pop('dati')]
        target = ROOT / 'notizie' / (article['slug'] + '.html')
        if target.exists():
            articles.append(article)
            continue
        source = Path(paths[article.pop('image_index')])
        image = Image.open(source).convert('RGB')
        image = ImageOps.fit(image, (1600, 900), method=Image.Resampling.LANCZOS)
        variants = []
        for w in (480, 800, 1200):
            target = ROOT / f'assets/images/editorial-auto/{article["slug"]}-v{VERSION}-{w}.webp'
            image.resize((w, round(w * 9 / 16)), Image.Resampling.LANCZOS).save(target, 'WEBP', quality=90, method=6)
            variants.append(dict(w=w, h=round(w * 9 / 16), src='/' + str(target.relative_to(ROOT)), sha256=hashlib.sha256(target.read_bytes()).hexdigest(), bytes=target.stat().st_size))
        record = dict(key=f'{article["slug"]}-v{VERSION}', alt=article.pop('alt'), prompt=article['titolo'] + '. Illustrazione editoriale fotorealistica dedicata, non documentaria, senza testo aggiunto.', variants=variants, disclosure=site.CAPTION, generator='OpenAI image generation', aiGenerated=True, documentaryPhoto=False, officialArtwork=False, sensitiveContext=False, weatherMap=False)
        if article.pop('public', False):
            record['syntheticLikeness'] = 'public-figure'
        site.write_article(article, record, VERSION)
        site.register_image(record, article['slug'], VERSION)
        # Separare l'ordine del lotto senza inventare un orario futuro.
        published = (now - timedelta(seconds=len(payload) - 1 - i)).isoformat()
        target = ROOT / 'notizie' / (article['slug'] + '.html')
        doc = html.fromstring(target.read_text())
        for node in doc.xpath('//script[@type="application/ld+json"]'):
            data = json.loads(node.text)
            if data.get('@type') == 'NewsArticle':
                data['datePublished'] = data['dateModified'] = published
                node.text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        for node in doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " meta ")]'):
            node.text = f'{datetime.fromisoformat(published).strftime("%d/%m/%Y · %H:%M")} · {article["luogo"]} · 1 min di lettura'
        target.write_text(html.tostring(doc, encoding='unicode', method='html', doctype='<!doctype html>') + '\n')
        articles.append(article)
    site.sync_surfaces(articles, '/notizie/' + articles[-1]['slug'] + '.html', VERSION, update_manifest=False)

if __name__ == '__main__':
    main()
