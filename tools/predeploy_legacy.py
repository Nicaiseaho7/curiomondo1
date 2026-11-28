"""Keep exact, reviewed historical debt visible without blocking unrelated releases."""
import hashlib
import json
from collections import Counter
from pathlib import Path


def split_legacy(root, messages, refs):
    lock_path = Path(__file__).with_name('predeploy_legacy.json')
    locked = json.loads(lock_path.read_text(encoding='utf-8'))
    blocking, legacy = [], []
    seen = Counter()
    digests = {}
    for message in messages:
        row = locked['findings'].get(message)
        if not row:
            blocking.append(message)
            continue
        seen[message] += 1
        if seen[message] > row['count']:
            blocking.append(message)
            continue
        paths = row['paths']
        if 'cover' in row and set(refs.get(row['cover'], [])) != set(paths):
            blocking.append(message)
            continue
        for path, expected in paths.items():
            if path not in digests:
                file = root/path
                digests[path] = hashlib.sha256(file.read_bytes()).hexdigest() if file.is_file() else None
            if digests[path] != expected:
                blocking.append(message)
                break
        else:
            legacy.append(message)
    return blocking, legacy
