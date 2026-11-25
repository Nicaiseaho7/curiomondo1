#!/usr/bin/env python3
"""Migrate only the exact known CurioMondo v17 ad formats. Dry-run by default."""
import argparse
import html
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

GUARD=re.compile(r'(/assets/js/cm-ad-guard-v1\.js\?v=)(17|18)(?=["\'])')
TARGETS={
 "box300": ("300","250","55b96d02a3c1e223d77eb5a2ac3e48bb"),
 "banner468": ("468","60","336aa28e4c164e4758ab957aebbb1524"),
 "banner320": ("320","50","d1ee0ffe21c637886bfe8efc32572e6b"),
 "native": ("360","420","81e6446ad1091f193a3bcc8fbb538b94"),
 "adcash": ("300","250","12487982"),
}
ATTRS=r"""(?:[^"'<>]|"[^"]*"|'[^']*')*"""
WRAP=re.compile(r'(<(?P<tag>aside|div)\b(?=[^>]*\bdata-cm-ad=["\'](?P<kind>box300|banner468|banner320|native|adcash)["\'])'+ATTRS+r'>)\s*(<iframe\b'+ATTRS+r'>)\s*</iframe>\s*(</(?P=tag)\s*>)',re.I|re.S)
HAS_SHIM=re.compile(r"<script>\s*document\.write=function\(h\)\{[^<]*document\.writeln=document\.write;\s*</script>",re.I)

class Tags(HTMLParser):
 def __init__(self, s):
  self.tags=[]; super().__init__(convert_charrefs=True); self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))

def migrate(src, allow_adcash=False):
 if not GUARD.search(src):return src,0
 # One v17 template put the next slot inside an unclosed HTML attribute.
 # Repair only the observed pair of literal fragments, before parsing slots.
 old_open = '</div><aside class="cm-safe-ad" id="cm-adcash-slot"'
 old_tail = '</aside></body></html>"></iframe></aside></body></html>'
 marker = "container-81e6446ad1091f193a3bcc8fbb538b94'></div><aside"
 if src.count(marker)==1 and src.count(old_open)==1 and src.count(old_tail)==1:
  src=src.replace(old_open,'</div></body></html>"></iframe></aside><aside class="cm-safe-ad" id="cm-adcash-slot"',1)
  src=src.replace(old_tail,'</aside></body></html>',1)
 count=0
 def replace(m):
  nonlocal count
  start,_,kind,frame,end=m.groups()
  if 'data-cm-inline' in start:return m[0]
  a=Tags(frame).tags[0][1]; content=a.get('srcdoc','')
  w,h,key=TARGETS[kind]
  if a.get('sandbox')!='allow-scripts' or a.get('src') or not content:return m[0]
  if kind=='native' and (a.get('width'),a.get('height'))==('336','300'):w,h='336','300'
  if (a.get('width'),a.get('height'))!=(w,h):return m[0]
  if not re.search(r'<body\b',content,re.I) or re.search(r'runPop|runVideoSlider|ad-provider|magsrv|exosrv|<base\b',content,re.I):return m[0]
  script_urls=[attrs['src'] for tag,attrs in Tags(content).tags if tag=='script' and 'src' in attrs]
  expected= 'https://acscdn.com/script/aclib.js' if kind=='adcash' else f'https://bauval.org/{21 if kind=="native" else 22}/{key}'
  if script_urls != [expected]:return m[0]
  if kind=='adcash':
   if not re.search(r"aclib\.runBanner\(\{zoneId:['\"]12487982['\"]\}\)",content):return m[0]
   if not allow_adcash:
    count+=1
    return start[:-1]+ ' data-cm-inline="disabled" hidden>'+end
  elif kind!='native' and not re.search(r"key:['\"]"+key+r"['\"]",content):return m[0]
  # The network's classic ad snippet runs synchronously in the isolated HTML parser.
  # Unlike v17, do not replace document.write with an out-of-order shim.
  content=HAS_SHIM.sub('',content,count=1)
  if 'document.write=function' in content:return m[0]
  count+=1
  payload=html.escape(content,quote=True)
  return start[:-1]+f' data-cm-inline="1" data-cm-inline-width="{w}" data-cm-inline-height="{h}">'+f'<template data-cm-inline-source data-cm-html="{payload}"></template>'+end
 out=WRAP.sub(replace,src)
 if count:
  out=GUARD.sub(r'\g<1>18',out)
 return out,count

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',type=Path,default=Path('.'))
 p.add_argument('--apply',action='store_true')
 p.add_argument('--adcash-approvato',action='store_true',help='Solo con approvazione scritta Adcash per uso in iframe.')
 a=p.parse_args()
 root=a.root.resolve()
 paths=[root/'index.html']
 for directory in ('notizie','approfondimenti','domanda-del-giorno','biblioteca','categorie','pagine','scadenze','concerti','scioperi'):
  paths.extend((root/directory).rglob('*.html'))
 changed=[]; warnings=[]; totals=0
 for path in sorted(set(paths)):
  if not path.is_file():continue
  before=path.read_bytes().decode('utf-8')
  after,n=migrate(before,a.adcash_approvato)
  if GUARD.search(before):
   # An unconverted known wrapper must not be silently declared fixed.
   for m in WRAP.finditer(after):
    if 'data-cm-inline' not in m[1]: warnings.append((path.relative_to(root),m['kind']))
  if n:changed.append((path,after));totals+=n
 print(f'Pagine={len(changed)}; spazi={totals}; Adcash={"approvato" if a.adcash_approvato else "inattivo"}; non riconosciuti={len(warnings)}; apply={a.apply}')
 for path,kind in warnings[:25]: print(path,kind,file=sys.stderr)
 if warnings:return 2
 if not changed and not any('v=18' in p.read_text(encoding='utf-8',errors='ignore') for p in paths if p.exists()):return 3
 if a.apply:
  for path,data in changed:path.write_bytes(data.encode('utf-8'))
 return 0
if __name__=='__main__':sys.exit(main())
