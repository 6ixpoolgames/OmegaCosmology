"""Check active repository layout/links, excluding immutable imported prose."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors, checked = [], 0
    active = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'manuscript/README.md', ROOT / 'manuscript/v4.1/README.md']
    for folder in ('docs', 'formal', 'research/platform', 'research/studies'):
        active.extend((ROOT / folder).rglob('*.md'))
    active += [ROOT / 'research/ROADMAP.md', ROOT / 'research/tasks/002-next-generation-platform.md', ROOT / 'sources/v4.1/README.md', ROOT / 'archive/README.md']
    for path in active:
        text = path.read_text(encoding='utf-8')
        if text.count('```') % 2:
            errors.append({'path': path.relative_to(ROOT).as_posix(), 'error': 'unbalanced fenced block'})
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.split('#', 1)[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            target = unquote(target.strip('<>'))
            checked += 1
            if not (path.parent / target).resolve().exists():
                errors.append({'path': path.relative_to(ROOT).as_posix(), 'target': target, 'error': 'missing local link'})
    reference = json.loads((ROOT / 'sources/v4.1/MANIFEST.json').read_text(encoding='utf-8'))
    if reference['edition'] != 'v4.1':
        errors.append({'error': 'wrong canonical starting reference'})
    for row in reference['files']:
        if row.get('working_copy') and not (ROOT / row['working_copy']['path']).is_file():
            errors.append({'error': 'missing working manuscript copy', 'path': row['working_copy']['path']})
    ignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
    if '.local/' not in ignore or 'runs/*' not in ignore:
        errors.append({'error': 'private/generated output exclusion missing'})
    print(json.dumps({'status': 'failed' if errors else 'passed', 'active_documents': len(active),
                      'local_links_checked': checked, 'errors': errors}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
