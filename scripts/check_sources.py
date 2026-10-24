"""Verify unchanged imported source snapshots against their migration inventory."""
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'sources/manifest.json').read_text(encoding='utf-8'))
    seen, errors = set(), []
    for row in manifest['files']:
        name = row['path']
        relative = PurePosixPath(name)
        path = ROOT.joinpath(*relative.parts).resolve()
        if (relative.is_absolute() or '..' in relative.parts or name in seen
                or not path.is_relative_to((ROOT / 'sources').resolve())):
            errors.append({'path': name, 'error': 'unsafe or duplicate source entry'})
            continue
        seen.add(name)
        if not path.is_file():
            errors.append({'path': name, 'error': 'missing'})
        elif path.stat().st_size != row['bytes'] or sha256(path.read_bytes()).hexdigest() != row['sha256']:
            errors.append({'path': name, 'error': 'byte mismatch'})
    print(json.dumps({'status': 'failed' if errors else 'passed',
                      'checked_files': len(seen), 'errors': errors}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
