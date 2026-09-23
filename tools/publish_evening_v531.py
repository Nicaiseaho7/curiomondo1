#!/usr/bin/env python3
"""Publish the verified September 23 evening batch, preserving update dates."""
import hashlib
import json
import sys
from pathlib import Path
from lxml import html, etree
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 531
IMAGES = {
    'weinstein': ('bceb8679-1954-481d-a96f-fed91cccafe6', 'Ritratto neutro di Harvey Weinstein, somiglianza sintetica non documentaria.'),
    'nucleare': ('6ee25f58-0dd2-4be9-96f1-96fa10f2083f', 'La facciata di Palazzo Madama a Roma con le bandiere italiana ed europea, illustrazione IA.'),
    'iran': ('a2a887ae-1fa1-4efb-9d65-5140c4b6ae65', 'Ritratto neutro di Mohsen Rezaei, somiglianza sintetica non documentaria.'),
    'italia': ('20da0446-7996-4427-828c-a62969602ad9', 'Illustrazione IA di una calciatrice della Nazionale italiana Under 20 con la divisa azzurra, basata sul riferimento FIGC.'),
    'pnrr': ('bf0296f8-d648-473e-945e-018db70db5fc', 'Palazzo Chigi a Roma, illustrazione editoriale IA non documentaria.'),
    'crosetto': ('8ad829ef-c988-4f76-8879-b23f818c3e39', 'Ritratto neutro di Guido Crosetto, somiglianza sintetica non documentaria.'),
    'scuola': ('35410a3e-a61e-494b-90b9-db1347263abf', 'Ritratto di Giorgia Meloni, somiglianza sintetica non documentaria.'),
    'ungheria': ('3d103e0b-0086-4fe6-8cbc-63ffdc276118', 'Bandiere europea e ungherese davanti alla sede della Commissione, illustrazione editoriale IA.'),
    'luna': ('21f5c074-716a-480c-b1b3-97eae72858fa', 'Jared Isaacman con il simbolo NASA, somiglianza sintetica non documentaria.'),
    'sancataldo': ('810185ba-dd08-46bb-a185-099c547ef5bf', 'Uno smartphone con il simbolo YouTube, illustrazione IA senza persone o riferimenti identificativi ai minori.'),
    'baku': ('0783192b-e743-469a-939e-7c1a2f3bf879', 'Andrea Kimi Antonelli in tuta Mercedes con Baku sullo sfondo, somiglianza sintetica non documentaria.'),
    'colonnine': ('8bd50873-b110-4e84-8480-1c73400b3c3b', 'Auto elettrica collegata a una colonnina domestica, illustrazione IA; il marchio raffigurato è esemplificativo.'),
}


def main():
    articles = json.loads((ROOT / 'tools/news_batch_20260923_evening.json').read_text())
    cfg_path = ROOT / 'assets/data/homepage-config-v504.json'
    cfg = json.loads(cfg_path.read_text())
    feed_path = ROOT / 'assets/data/home-feed-v210.json'
    feed = json.loads(feed_path.read_text())
    registry_path = ROOT / 'assets/data/editorial-images-v210.json'
    registry = json.loads(registry_path.read_text())
    urls = {f"/notizie/{a['slug']}.html" for a in articles}
    registry['items'] = [i for i in registry['items'] if i.get('article') not in urls]
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2)+'\n')
    for a in articles:
        a['fonti'] = [{'url': u, 'descrizione': d} for u,d in a['fonti']]
        a['dati_chiave'] = [{'valore': v, 'etichetta': l} for v,l in a.pop('stats')]
        a['parole_chiave_titolo'] = a.get('parole_chiave_titolo', [])
        ident, alt = IMAGES[a['id']]
        source = ROOT.parent / f'generated_images/exec-{ident}.png'
        img = Image.open(source).convert('RGB')
        variants = []
        for w in (480,800,1200):
            path = ROOT / f"assets/images/editorial-auto/{a['slug']}-v{VERSION}-{w}.webp"
            img.resize((w,round(w/1.5)),Image.Resampling.LANCZOS).save(path,'WEBP',quality=87,method=6)
            variants.append({'w':w,'src':'/'+str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
        image = {'key':f"{a['slug']}-v{VERSION}",'alt':alt,'variants':variants,'disclosure':site.CAPTION,'generator':'OpenAI image tool','sensitiveContext':bool(a.get('sensitive'))}
        if a.get('public'): image['syntheticLikeness'] = 'public-figure'
        if a.get('public') and a.get('sensitive'):
            image.update(portraitOnly=True,portraitFormat='neutral-isolated',reenactedEvent=False,prompt='Neutral editorial portrait, isolated public figure, plain studio background; no reenactment, no scene of violence.')
            image['alt'] = image['alt'].replace('Ritratto neutro','Ritratto editoriale neutrale')
        target = ROOT / f"notizie/{a['slug']}.html"
        previous = target.read_text() if a.get('update') else None
        if previous:
            previous_ld = site._news_json(html.fromstring(previous))
            target.unlink()
        try:
            slug, page = site.render_article(a,image,VERSION)
        finally:
            if previous: target.write_text(previous)
        doc = html.fromstring(page)
        if previous:
            script = doc.xpath('//script[@type="application/ld+json"]')[0]
            ld = json.loads(script.text)
            ld['datePublished'] = previous_ld['datePublished']
            script.text = json.dumps(ld,ensure_ascii=False,separators=(',',':'))
            meta = doc.xpath('//div[@class="meta"]')[0]
            meta.text = f"Pubblicato il {site._italian_date(ld['datePublished'])} · Aggiornato il {site._italian_date(ld['dateModified'])} · {a['luogo']} · "
            a['published'] = ld['datePublished']
        if a['id'] == 'weinstein':
            doc.xpath('//div[@class="badge"]')[0].text = 'Mondo / Cronaca'
            a['category_full'] = 'Mondo / Cronaca'
        if a['id'] == 'baku':
            block = html.fromstring('<section class="cm-evergreen-reader"><span class="cm-kicker">Per capire meglio</span><h2>Come si rimonta in Formula 1</h2><p>Strategia, pneumatici e Virtual Safety Car: le scelte che possono cambiare una gara.</p><a href="/approfondimenti/come-si-rimonta-formula-1-strategia-vsc-pneumatici.html">Leggi l’approfondimento →</a></section>')
            doc.xpath('//article[@class="art-body"]')[0].addnext(block)
        target.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode'),encoding='utf-8')
        site.register_image(image,slug,VERSION)
        url = f'/notizie/{slug}.html'
        cfg['articles'][url] = {'firstPublishedAt':a['published'],'homepagePriority':95 if a['id'] in ('weinstein','nucleare','pnrr','scuola') else 80,'primaryCategory':a['categoria'].lower()}
        for item in feed['items']:
            if item.get('url') == url: item['excerpt'] = a['sommario']
    cfg['version'] = VERSION
    cfg_path.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
    feed_path.write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
    site.sync_surfaces(articles,f"/notizie/{articles[0]['slug']}.html",VERSION)
    manifest_path = ROOT/'curiomondo-site-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['site']['current_site_version'] = manifest['site']['site_version'] = VERSION
    manifest['site_version'] = VERSION
    manifest['version'] = manifest['release_version'] = f'v{VERSION}'
    manifest['last_release'] = {'version':VERSION,'date':'2026-09-23','type':'evening-news-batch','news_added':[a['slug'] for a in articles if not a.get('update')],'news_updated':[a['slug'] for a in articles if a.get('update')],'change':'Dieci notizie nuove e aggiornamenti su scuola e bonus colonnine'}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for name in ('CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json'):
        path = ROOT/name
        state = json.loads(path.read_text())
        state.update(site_version=VERSION,version=str(VERSION),currentVersion=VERSION,release_date='2026-09-23',last_update='evening-news-v531')
        if 'articleCount' in state: state['articleCount'] += 10
        if 'generatedEditorialImages' in state: state['generatedEditorialImages'] += 12
        path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
    print('Published 10 new articles and 2 updates locally; live validation pending.')

if __name__ == '__main__':
    main()
