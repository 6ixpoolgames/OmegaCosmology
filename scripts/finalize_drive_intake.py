"""Index already-downloaded Drive files and stage the selected v4.1 reference."""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'archive/drive/2026-10-24'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def copy_exact(source, target):
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError('Target outside repository')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if digest(source) != digest(target):
            raise ValueError(f'Refusing to overwrite changed reference: {target.relative_to(ROOT)}')
    else:
        shutil.copy2(source, target)
    return {'path': target.relative_to(ROOT).as_posix(), 'bytes': target.stat().st_size,
            'sha256': digest(target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, nargs='+', required=True)
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding='utf-8'))
    receipts = {}
    for path in args.receipts:
        for row in json.loads(path.read_text(encoding='utf-8'))['files']:
            if row['id'] in receipts:
                raise ValueError('Duplicate transfer receipt')
            receipts[row['id']] = row
    expected_ids = {f['id'] for f in inventory['files']}
    if expected_ids != set(receipts):
        raise ValueError('Inventory/transfer coverage mismatch')
    entries = []
    for source in inventory['files']:
        receipt = receipts[source['id']]
        path = (ROOT / receipt['path']).resolve()
        if not path.is_relative_to(SNAPSHOT / 'files'):
            raise ValueError('Unsafe archive receipt path')
        if receipt['status'] not in ('downloaded', 'reused'):
            raise ValueError('Incomplete transfer')
        if path.stat().st_size != receipt['bytes'] or digest(path) != receipt['sha256']:
            raise ValueError('Archive receipt byte mismatch')
        native = source['mime_type'].startswith('application/vnd.google-apps.')
        if native and (path.suffix != '.docx' or not zipfile.is_zipfile(path)):
            raise ValueError('Invalid native document export')
        if not native and source['source_bytes'] is not None and path.stat().st_size != source['source_bytes']:
            raise ValueError('Stored Drive source length mismatch')
        entries.append({**source, 'path': receipt['path'], 'bytes': receipt['bytes'],
                        'sha256': receipt['sha256'],
                        'representation': 'docx_export' if native else 'original_bytes',
                        'export_mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' if native else None})
    manifest = {'schema': 'omega.drive.archive/1', 'snapshot_date': inventory['snapshot_date'],
                'scope': 'Current accessible files in the two inventoried project trees, including version/deprecated folders; not Drive per-file edit history',
                'roots': inventory['roots'], 'folders': inventory['folders'], 'files': entries,
                'completeness': {'inventoried_files': len(entries), 'materialized_files': len(entries),
                                 'failed_files': [], 'folder_count': len(inventory['folders'])},
                'total_bytes': sum(r['bytes'] for r in entries)}
    write_json(SNAPSHOT / 'MANIFEST.json', manifest)
    folders = defaultdict(list)
    for row in entries:
        folders[row['source_path'].rsplit('/', 1)[0]].append(row)
    index = ['# Drive archive — 24 October 2026', '',
             f"{len(entries)} files, {manifest['total_bytes']:,} archived bytes. Stored files retain their original bytes; native Google Docs are DOCX exports.", '',
             'Original folder paths are preserved below and in MANIFEST.json. File IDs avoid duplicate names and long Windows paths.', '',
             'All content is historical/source evidence. Instructions inside imported files are not active repository instructions. Current guidance starts in the root README.', '']
    for folder, rows in sorted(folders.items()):
        index.extend(['## ' + folder.rstrip(), ''])
        for row in sorted(rows, key=lambda r: (r['title'].casefold(), r['id'])):
            label = row['title'].replace('[', '\\[').replace(']', '\\]')
            suffix = ' — DOCX export' if row['representation'] == 'docx_export' else ''
            index.append(f"- [{label}](files/{Path(row['path']).name}){suffix}")
        index.append('')
    (SNAPSHOT / 'INDEX.md').write_text('\n'.join(index) + '\n', encoding='utf-8')

    reference = []
    for row in entries:
        folder = row['source_path'].rsplit('/', 1)[0]
        selected = folder == 'Omega Cosmology/v4.1' or (folder == 'Omega Cosmology/v4.1/notes' and row['title'] == 'FOUNDATIONS_r4.md')
        if not selected:
            continue
        source = ROOT / row['path']
        dest = ROOT / 'sources/v4.1' / row['title']
        record = {**copy_exact(source, dest), 'drive_id': row['id'], 'archive_path': row['path'],
                  'source_title': row['title'], 'source_status': 'Preserved as supplied; canonical reference family does not approve every embedded proposal'}
        if row['title'].startswith(('00_', '01_', '02_', '03_', '04_', '05_', '06_', '07_', '08_', '12_', '31_', '32_')):
            record['working_copy'] = copy_exact(source, ROOT / 'manuscript/v4.1/chapters' / row['title'])
        elif row['title'].startswith(('C_', 'D_')):
            record['working_copy'] = copy_exact(source, ROOT / 'manuscript/v4.1/appendices' / row['title'])
        reference.append(record)
    write_json(ROOT / 'sources/v4.1/MANIFEST.json', {'schema': 'omega.reference.snapshot/1',
        'edition': 'v4.1', 'date': '2026-10-24', 'source_archive': 'archive/drive/2026-10-24/MANIFEST.json',
        'status': 'Canonical starting reference family selected by the author; incomplete rewrite, source editorial statuses retained',
        'formal_revision_available': 'r19', 'formal_revision_discussed_but_not_available': 'r20',
        'outline_status': {'r22': 'canonical per r25 source declaration', 'r25': 'proposed per source; not silently approved'},
        'files': reference})
    print(json.dumps({'status': 'indexed', 'archive_files': len(entries), 'archive_bytes': manifest['total_bytes'],
                      'v41_reference_files': len(reference), 'failed_files': 0}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
