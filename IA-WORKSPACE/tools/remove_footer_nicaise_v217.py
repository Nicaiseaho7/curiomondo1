#!/usr/bin/env python3
"""Remove the Nicaise signature only when it is inside a footer."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
pattern = re.compile(
    r'(<footer\b[^>]*>)(\s*)<div\s+class="cm-nicaise-signature"[^>]*>.*?</div>',
    re.IGNORECASE | re.DOTALL,
)

changed = 0
for path in ROOT.rglob('*.html'):
    source = path.read_text(errors='replace')
    updated, count = pattern.subn(r'\1', source)
    if count:
        path.write_text(updated)
        changed += 1

print(f'footer aggiornati: {changed}')

builder = ROOT / 'tools/build_v213.py'
builder_source = builder.read_text()
builder_source = builder_source.replace(
    '<footer class="site-footer"><div class="cm-nicaise-signature" aria-label="Nicaise"><span class="cm-nicaise-word"><b>N</b>icaise</span><i aria-hidden="true"></i></div><nav class="site-footer-links"',
    '<footer class="site-footer"><nav class="site-footer-links"',
)
builder.write_text(builder_source)
