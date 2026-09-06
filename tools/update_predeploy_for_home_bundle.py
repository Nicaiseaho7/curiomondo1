#!/usr/bin/env python3
from pathlib import Path

p = Path('tools/predeploy.py')
s = p.read_text(encoding='utf-8')

old_sequence = '''featured_href=home.xpath('//a[contains(@class,"featured")]/@href')
rail_hrefs=home.xpath('//div[contains(@class,"auto-rail")]/a/@href')
sequence_hrefs=list(featured_href)+list(rail_hrefs)+list(all_news_urls)
chronological=[url for url,_ in sorted(card_eligible_dates.items(),key=lambda kv: kv[1],reverse=True)]
expected_sequence=chronological[:len(sequence_hrefs)]
if sequence_hrefs!=expected_sequence:
    for i,(got,want) in enumerate(zip(sequence_hrefs,expected_sequence)):
        if got!=want:
            errors.append(f'sequenza cronologica homepage non continua alla posizione {i+1}: trovato {got} ({card_eligible_dates.get(got)}) invece di {want} ({card_eligible_dates.get(want)}) — significa che una notizia più recente è stata saltata/nascosta')
            break
    if len(sequence_hrefs)!=len(expected_sequence):
        errors.append(f'homepage (apertura+Ultime notizie+Tutte le notizie) contiene {len(sequence_hrefs)} notizie ma le notizie pubblicate idonee sono {len(chronological)}: verificare articoli mancanti o duplicati')
'''

new_sequence = '''featured_href=home.xpath('//a[contains(@class,"featured")]/@href')
rail_hrefs=home.xpath('//div[contains(@class,"auto-rail")]/a/@href')
chronological=[url for url,_ in sorted(card_eligible_dates.items(),key=lambda kv: kv[1],reverse=True)]
# v291: Ultima ora è una scelta editoriale distinta dalla continuità cronologica.
# Dopo aver escluso l'hero, Ultime notizie + Tutte le notizie devono restare senza salti.
if featured_href and featured_href[0] not in card_eligible_dates:
    errors.append(f'Ultima ora non idonea alle card editoriali: {featured_href[0]}')
chronological_after_featured=[url for url in chronological if url not in set(featured_href)]
sequence_hrefs=list(rail_hrefs)+list(all_news_urls)
expected_sequence=chronological_after_featured[:len(sequence_hrefs)]
if sequence_hrefs!=expected_sequence:
    for i,(got,want) in enumerate(zip(sequence_hrefs,expected_sequence)):
        if got!=want:
            errors.append(f'sequenza cronologica Ultime notizie → Tutte le notizie non continua alla posizione {i+1}: trovato {got} ({card_eligible_dates.get(got)}) invece di {want} ({card_eligible_dates.get(want)})')
            break
    if len(sequence_hrefs)!=len(expected_sequence):
        errors.append(f'Ultime notizie + Tutte le notizie contengono {len(sequence_hrefs)} notizie ma le notizie pubblicate idonee, esclusa Ultima ora, sono {len(chronological_after_featured)}: verificare articoli mancanti o duplicati')
'''

old_azure = '''azure_css_path=root/'assets/css/home-azure-v274.css'
if not home.xpath('//link[contains(@href,"home-azure-v274.css")]'): errors.append('stile palette azzurra v274 non collegato in home')
if not home.xpath('//meta[@name="theme-color"][@content="#1877f2"]'): errors.append('theme-color v274 non impostato sul blu Facebook')
if not azure_css_path.exists(): errors.append('foglio palette azzurra v274 assente')
else:
    azure_css=azure_css_path.read_text(errors='replace')
    for marker in ('.ticker{','.ticker-label{','margin:0!important','border-radius:0!important','#d71936','#1877f2'):
        if marker not in azure_css: errors.append(f'contratto LIVE v274 incompleto: {marker}')
'''

new_azure = '''azure_css_path=root/'assets/css/home-azure-v274.css'
home_bundle_path=root/'assets/css/home-bundle-v291.css'
azure_direct=bool(home.xpath('//link[contains(@href,"home-azure-v274.css")]'))
bundle_linked=bool(home.xpath('//link[contains(@href,"home-bundle-v291.css")]'))
if not azure_direct and not bundle_linked:
    errors.append('palette azzurra v274 non collegata direttamente né tramite bundle home v291')
if bundle_linked:
    if not home_bundle_path.exists():
        errors.append('bundle CSS homepage v291 collegato ma assente')
    elif 'source: assets/css/home-azure-v274.css' not in home_bundle_path.read_text(errors='replace'):
        errors.append('bundle CSS homepage v291 non contiene la palette azzurra v274')
if not home.xpath('//meta[@name="theme-color"][@content="#1877f2"]'): errors.append('theme-color v274 non impostato sul blu Facebook')
if not azure_css_path.exists(): errors.append('foglio palette azzurra v274 assente')
else:
    azure_css=azure_css_path.read_text(errors='replace')
    for marker in ('.ticker{','.ticker-label{','margin:0!important','border-radius:0!important','#d71936','#1877f2'):
        if marker not in azure_css: errors.append(f'contratto LIVE v274 incompleto: {marker}')
'''

changed = False
if old_sequence in s:
    s = s.replace(old_sequence, new_sequence)
    changed = True
elif 'sequenza cronologica Ultime notizie → Tutte le notizie non continua' not in s:
    raise SystemExit('Blocco cronologia predeploy non trovato')

if old_azure in s:
    s = s.replace(old_azure, new_azure)
    changed = True
elif 'bundle CSS homepage v291 non contiene la palette azzurra v274' not in s:
    raise SystemExit('Blocco palette predeploy non trovato')

if changed:
    p.write_text(s, encoding='utf-8')
    print('predeploy aggiornato a v291')
else:
    print('predeploy già aggiornato a v291')
