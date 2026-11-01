#!/usr/bin/env python3
"""Verify packaged bytes against manifest.json; not a digital signature."""
import hashlib
import json
import sys
from pathlib import Path


def verify(root: Path) -> list[str]:
    root = root.resolve()
    data = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    errors = []
    for item in data['files']:
        path = (root / item['path']).resolve()
        if root not in path.parents:
            errors.append(f'Unsafe path: {item["path"]}')
            continue
        if not path.is_file():
            errors.append(f'Missing: {item["path"]}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            errors.append(f'Hash mismatch: {item["path"]}')
    return errors


if __name__ == '__main__':
    try:
        errors = verify(Path(sys.argv[1] if len(sys.argv) > 1 else '.'))
        print(json.dumps({'verified': not errors, 'errors': errors}, indent=2))
        raise SystemExit(1 if errors else 0)
    except (OSError, ValueError, KeyError) as exc:
        print(f'Verification error: {exc}', file=sys.stderr)
        raise SystemExit(2)
