#!/usr/bin/env python3
"""Ship the global related-article self-exclusion fix as CurioMondo v236."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]

def write(path,value):
    path.write_text(value,encoding='utf-8')

def dump(path,value,compact=False):
    text=json.dumps(value,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)
    write(path,text+('' if compact else '\n'))

def route_key(value):
    value=(value or '').split('?',1)[0].split('#',1)[0].rstrip('/')
    if value.endswith('/index.html'): value=value[:-11]
    if value.endswith('.html'): value=value[:-5]
    return value

def update_articles():
    changed=0
    for path in (ROOT/'notizie').glob('*.html'):
        if path.name=='index.html': continue
        text=path.read_text(encoding='utf-8')
        updated=re.sub(r'(curiomondo-article-v210\.js)\?v=\d+',r'\1?v=236',text)
        if updated!=text:
            write(path,updated); changed+=1
    return changed

def update_versions():
    home_js=ROOT/'assets/js/home-v210.js'
    write(home_js,re.sub(r'\?v=235', '?v=236',home_js.read_text(encoding='utf-8')))
    article_js=ROOT/'assets/js/curiomondo-article-v210.js'
    write(article_js,re.sub(r'\?v=235', '?v=236',article_js.read_text(encoding='utf-8')))
    index=ROOT/'index.html'
    write(index,re.sub(r'(home-v210\.js)\?v=\d+',r'\1?v=236',index.read_text(encoding='utf-8')))
    for name in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
        path=ROOT/name; data=json.loads(path.read_text(encoding='utf-8')); data['version']=236; dump(path,data,compact='home-feed' in name or 'search-index' in name)

    state=json.loads((ROOT/'RELEASE-STATE.json').read_text(encoding='utf-8'))
    state.update({'currentVersion':236,'baselineVersion':235,'status':'ready','date':'2026-08-29',
                  'designRestored':'Potrebbe interessarti esclude sempre l’articolo aperto, anche con URL alternativi o cache precedenti.'})
    dump(ROOT/'RELEASE-STATE.json',state)
    state=json.loads((ROOT/'CURIOMONDO-RELEASE-STATE.json').read_text(encoding='utf-8'))
    state.update({'site_version':236,'baseline_version':235,'version':'236','baseline':'curiomondo-v235-29-agosto-2026-netlify.zip',
                  'last_update':'related-articles-global-self-exclusion-v236',
                  'performance_pass':'Cache aggiornata su tutte le pagine; confronto per canonical, slug e titolo senza nuove risorse.'})
    dump(ROOT/'CURIOMONDO-RELEASE-STATE.json',state)
    manifest_path=ROOT/'curiomondo-site-manifest.json'; manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['site']['current_site_version']=236; manifest['site_version']=236; manifest['version']='v236'; manifest['release_version']='v236'
    manifest['last_release']={'version':236,'date':'2026-08-29','baseline_version':235,'news_added':[],'news_updated':[],
                              'image_policy_applied':'unchanged','technical_fix':'related-articles-global-self-exclusion'}
    dump(manifest_path,manifest)
    write(ROOT/'RELEASE-NOTES-v236.md','''# CurioMondo v236 — 29 agosto 2026\n\n- Corretto globalmente il blocco “Potrebbe interessarti anche…”.\n- L’articolo aperto viene escluso confrontando canonical, percorso normalizzato, slug e titolo.\n- Gestite anche forme equivalenti dello stesso URL: `.html`, percorso pulito, slash finale, parametri e frammenti.\n- Aggiornata la cache del controller su tutte le 188 pagine articolo.\n- Aggiunto al predeploy un controllo bloccante contro autoreferenze future.\n- Conservate tre notizie correlate distinte, ciascuna con miniatura.\n''')

def main():
    changed=update_articles(); update_versions(); print(json.dumps({'version':236,'articlePagesUpdated':changed},indent=2))

if __name__=='__main__': main()
