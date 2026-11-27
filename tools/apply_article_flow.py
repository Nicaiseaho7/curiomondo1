#!/usr/bin/env python3
"""Prepara le notizie esistenti per il layout. Senza --apply non scrive."""
from pathlib import Path
import argparse
import importlib.util
import sys

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('articles',nargs='*',help='File dalla radice; se omessi, tutte le pagine notizia.')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    path=root/'automation/newsroom/article_flow.py'
    spec=importlib.util.spec_from_file_location('cm_article_flow',path)
    flow=importlib.util.module_from_spec(spec);spec.loader.exec_module(flow)
    catalog=flow.load_catalog(root)
    if len(catalog.latest)<4: raise SystemExit('Feed o risorse del checkout incompleti: non modifico le pagine.')
    files=[(root/a).resolve() for a in args.articles] if args.articles else sorted((root/'notizie').glob('*.html'))
    changes=[];errors=[];unchanged=0;skipped=0
    for p in files:
        if not p.is_relative_to(root/'notizie') or p.suffix!='.html':
            errors.append(f'{p}: solo pagine notizia dalla radice');continue
        if p.name=='index.html': continue
        try:
            raw=p.read_text(encoding='utf-8')
            if 'class="art-body"' not in raw and "class='art-body'" not in raw and 'cm-news-flow-article' not in raw:
                skipped+=1;continue
            if 'name="robots" content="noindex' in raw or 'http-equiv="refresh"' in raw:
                skipped+=1;continue
            changed,different=flow.transform(raw,catalog,fallback_url='/'+p.relative_to(root).as_posix())
            if different: changes.append((p,changed))
            else: unchanged+=1
        except (OSError,ValueError) as error:
            errors.append(str(error))
    if errors:
        for e in errors[:24]: print(e,file=sys.stderr)
        print(f'{len(errors)} pagine da verificare; nessuna modifica scritta.',file=sys.stderr)
        return 1
    if args.apply:
        for p,content in changes:
            tmp=p.with_suffix('.cm-flow-tmp')
            tmp.write_text(content,encoding='utf-8')
            tmp.replace(p)
    print(f'{len(changes)} da/già aggiornate; {unchanged} invariate; {skipped} indici, alias o pagine non pertinenti. Scrittura: {args.apply}.')
    return 0

if __name__=='__main__': raise SystemExit(main())
