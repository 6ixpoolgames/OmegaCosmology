"""Verify imported Drive/archive/reference bytes without network access."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def verify_rows(root, rows, allowed):
    errors, seen = [], set()
    allowed = tuple((root / p).resolve() for p in allowed)
    for row in rows:
        name = row['path']
        path = (root / name).resolve()
        if name in seen or not any(path.is_relative_to(p) for p in allowed):
            errors.append({'path': name, 'error': 'unsafe or duplicate archive path'})
            continue
        seen.add(name)
        if not path.is_file():
            errors.append({'path': name, 'error': 'missing'})
        elif path.stat().st_size != row['bytes'] or sha256(path.read_bytes()).hexdigest() != row['sha256']:
            errors.append({'path': name, 'error': 'byte mismatch'})
        elif row.get('representation') == 'docx_export':
            try:
                with zipfile.ZipFile(path) as z:
                    if '[Content_Types].xml' not in z.namelist() or 'word/document.xml' not in z.namelist():
                        errors.append({'path': name, 'error': 'not a DOCX document export'})
            except zipfile.BadZipFile:
                errors.append({'path': name, 'error': 'invalid DOCX export'})
    return errors


def main():
    errors, counts = [], {}
    manifests = [
        ('archive/drive/2026-10-24/MANIFEST.json', ('archive/drive/2026-10-24/files',)),
        ('archive/legacy-testbed/MANIFEST.json', ('archive/legacy-testbed',)),
        ('archive/repository-seed/2026-10-24/MANIFEST.json', ('archive/repository-seed/2026-10-24',)),
        ('sources/v4.1/MANIFEST.json', ('sources/v4.1',)),
    ]
    for name, allowed in manifests:
        value = json.loads((ROOT / name).read_text(encoding='utf-8'))
        errors.extend(verify_rows(ROOT, value['files'], allowed))
        counts[name] = len(value['files'])
        if name.startswith('archive/drive'):
            ids = [r['id'] for r in value['files']]
            if len(ids) != len(set(ids)):
                errors.append({'path': name, 'error': 'duplicate Drive source ID'})
            listed = {r['path'] for r in value['files']}
            actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / allowed[0]).iterdir() if p.is_file()}
            if actual != listed:
                errors.append({'path': name, 'error': 'payload inventory coverage mismatch'})
            folder_files = {i for folder in value['folders'] for i in folder['children'] if i in set(ids)}
            if folder_files != set(ids):
                errors.append({'path': name, 'error': 'folder/file inventory mismatch'})
            if value['completeness']['failed_files']:
                errors.append({'path': name, 'error': 'archive has failed files'})
            if sum(r['bytes'] for r in value['files']) != value['total_bytes']:
                errors.append({'path': name, 'error': 'archive total size mismatch'})
            if 'download_url' in json.dumps(value) or 'oaiusercontent.com' in json.dumps(value):
                errors.append({'path': name, 'error': 'transient download credential in public manifest'})
    print(json.dumps({'status': 'failed' if errors else 'passed', 'manifests': counts, 'errors': errors}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
