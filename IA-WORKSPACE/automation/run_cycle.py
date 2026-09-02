#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, os, sys

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'automation/config.json').read_text())
IMAGE_PROMPT_PATH=ROOT/CFG.get('articles',{}).get('image_generation_prompt','automation/prompts/image-generation-contract.txt')
if not IMAGE_PROMPT_PATH.exists():
    print(json.dumps({'status':'blocked','reason':'image_generation_prompt_missing','path':str(IMAGE_PROMPT_PATH)},ensure_ascii=False))
    sys.exit(5)
IMAGE_GENERATION_PROMPT=IMAGE_PROMPT_PATH.read_text(encoding='utf-8').strip()
IMAGE_POLICY_PATH=ROOT/CFG.get('articles',{}).get('image_policy','AI-EDITORIAL-IMAGE-PROTOCOL.md')
if not IMAGE_POLICY_PATH.exists():
    print(json.dumps({'status':'blocked','reason':'image_policy_missing','path':str(IMAGE_POLICY_PATH)},ensure_ascii=False))
    sys.exit(6)
IMAGE_POLICY=IMAGE_POLICY_PATH.read_text(encoding='utf-8').strip()
required_image_rules=('PUBLIC FIGURES AND SYNTHETIC LIKENESS','data-synthetic-likeness="public-figure"','data-sensitive-context="true|false"','ORDINARY public-figure news','SENSITIVE public-figure news','neutral isolated portrait','buildings and logos are allowed')
if any(rule not in IMAGE_GENERATION_PROMPT for rule in required_image_rules):
    print(json.dumps({'status':'blocked','reason':'public_figure_image_protocol_incomplete'},ensure_ascii=False))
    sys.exit(7)
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
    report('dry_run',reason='CURIOMONDO_AUTO_PUBLISH is not true',openai_key_present=key,image_prompt_loaded=True,image_prompt_path=str(IMAGE_PROMPT_PATH.relative_to(ROOT)),image_policy_loaded=True,image_policy_path=str(IMAGE_POLICY_PATH.relative_to(ROOT)))
    sys.exit(0)
if not key:
    report('blocked',reason='OPENAI_API_KEY missing'); sys.exit(3)

# Phase 2 hook: the tested renderer will be called here after source verification.
report('blocked',reason='renderer_not_enabled_yet',message='Infrastructure installed. Enable renderer only after controlled preview test.',image_prompt_loaded=True,image_prompt_path=str(IMAGE_PROMPT_PATH.relative_to(ROOT)),image_policy_loaded=True,image_policy_path=str(IMAGE_POLICY_PATH.relative_to(ROOT)))
sys.exit(4)
