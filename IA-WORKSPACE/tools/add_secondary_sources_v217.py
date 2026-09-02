#!/usr/bin/env python3
"""Add verified independent secondary sources to the five latest stories."""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]
SECONDARY = {
    'niger-attacco-aeroporto-presidenza-niamey-29-agosto-2026.html': (
        'Associated Press — esplosioni, dispiegamento delle forze e quadro di sicurezza a Niamey',
        'https://apnews.com/article/77d0c701e5729f2779580ea557e0a2c3',
    ),
    'cremona-tromba-aria-grandine-danni-29-agosto-2026.html': (
        'RaiNews TGR Lombardia — danni alla torre civica, alla cattedrale e alle abitazioni',
        'https://www.rainews.it/tgr/lombardia/video/2026/08/tromba-daria-su-cremona-danneggiate-torre-civica-e-cattedrale-8bdc1a86-b3b1-4100-9e25-fd92e4cd0463.html',
    ),
    'iran-economia-guerra-sanzioni-commercio-29-agosto-2026.html': (
        'Axios — analisi indipendente sull’intensificazione della pressione economica su Teheran',
        'https://www.axios.com/2026/08/24/trump-iran-sanctions-bessent-economy',
    ),
    'qatarenergy-stop-gas-edison-italia-novembre-29-agosto-2026.html': (
        'The National — conferma indipendente della sospensione e dei cinque carichi aggiuntivi',
        'https://www.thenationalnews.com/business/energy/2026/08/28/qatarenergy-extends-lng-supply-suspension-to-italy-until-november/',
    ),
}

for filename, (label, url) in SECONDARY.items():
    path = ROOT / 'notizie' / filename
    source = path.read_text()
    if url in source:
        continue
    marker = '</ul><p><small>Testo originale CurioMondo.'
    item = f'<li><a href="{html.escape(url)}" rel="noopener noreferrer" target="_blank">{html.escape(label)}</a></li>'
    source = source.replace(marker, item + marker, 1)
    path.write_text(source)
