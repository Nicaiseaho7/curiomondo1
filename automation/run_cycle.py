#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, os, sys

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'automation/config.json').read_text())
MODE=sys.argv[1] if len(sys.argv)>1 else 'articles'
LOG=ROOT/'automation/logs'
LOG.mkdir(parents=True,exist_ok=True)

def report(status, **extra):
    payload={'time':datetime.now(timezone.utc).isoformat(),'mode':MODE,'status':status,**extra}
    p=LOG/f"{MODE}-latest.json"; p.write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    print(json.dumps(payload,ensure_ascii=False))

if MODE not in {'articles','library','health'}:
    report('blocked',reason='unknown_mode'); sys.exit(2)

if MODE=='health':
    report('ok',message='health cycle scaffold ready'); sys.exit(0)

# Publication deliberately remains fail-closed until the API/secrets + renderer are configured and tested.
enabled=os.getenv('CURIOMONDO_AUTO_PUBLISH','').lower()=='true'
key=bool(os.getenv('OPENAI_API_KEY'))
if not enabled:
    report('dry_run',reason='CURIOMONDO_AUTO_PUBLISH is not true',openai_key_present=key)
    sys.exit(0)
if not key:
    report('blocked',reason='OPENAI_API_KEY missing'); sys.exit(3)

# Phase 2 hook: the tested renderer will be called here after source verification.
report('blocked',reason='renderer_not_enabled_yet','message':'Infrastructure installed. Enable renderer only after controlled preview test.')
sys.exit(4)
