"""Perform the explicit, reversible v4.1 repository preparation once."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'Omega'


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def copy(source, target):
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError('Destination outside repository')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and digest(source) != digest(target):
        raise ValueError(f'Refusing to overwrite {target.relative_to(ROOT)}')
    if not target.exists():
        shutil.copy2(source, target)
    return {'path': target.relative_to(ROOT).as_posix(), 'bytes': target.stat().st_size,
            'sha256': digest(target), 'original_path': str(source)}


def main():
    seed_root = ROOT / 'archive/repository-seed/2026-10-24'
    seed_manifest = seed_root / 'MANIFEST.json'
    if not seed_manifest.exists():
        paths = ['README.md', 'AGENTS.md', 'docs/current-position.md', 'docs/repository-plan.md',
                 'docs/provenance.md', 'docs/experiment-workflow.md', 'docs/testbed-foundation-contract.md',
                 'research/ROADMAP.md', 'research/claims.json', 'research/tasks/001-continuation-contract.md']
        paths += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'manuscript').glob('*.md')]
        paths += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'research/testbed').glob('*') if p.is_file()]
        rows = [copy(ROOT / name, seed_root / name) for name in paths]
        seed_manifest.write_text(json.dumps({'schema': 'omega.local-source-archive/1',
            'date': '2026-10-24', 'reason': 'Preserve v2-era repository preparation and October testbed drafts before v4.1 alignment',
            'files': rows}, indent=2) + '\n', encoding='utf-8')
        for p in (ROOT / 'manuscript').glob('*.md'):
            if p.name == 'README.md':
                continue
            archived = seed_root / p.relative_to(ROOT)
            if p.resolve().is_relative_to(ROOT / 'manuscript') and digest(p) == digest(archived):
                p.unlink()  # Individual old working copies, already archived and hash-verified.
            else:
                raise ValueError('Old manuscript copy was not safely archived')

    legacy = ROOT / 'archive/legacy-testbed'
    imported = []
    source_base = OLD / 'docs/research_notes/lushness_testbed'
    for p in (source_base / 'next_generation').glob('*.md'):
        imported.append(copy(p, legacy / 'next_generation' / p.name))
    support = ['SPECIFICATION_r2.md', 'ACCESS_MODEL.md', 'ACCESS_ASSESSMENT.md',
               'ACCESS_RESULTS_SUMMARY.json', 'JOINT_ENGINEERING.md',
               'SOL_AVAILABLE_WORK_ACCESS_AUDIT_SPEC_r1.md']
    for name in support:
        imported.append(copy(source_base / 'generative_ecology' / name, legacy / 'generative_ecology' / name))
    (legacy / 'MANIFEST.json').write_text(json.dumps({'schema': 'omega.local-source-archive/1',
        'date': '2026-10-24', 'reason': 'Source-preserving import of reviewed platform designs and selected prior evidence',
        'files': imported}, indent=2) + '\n', encoding='utf-8')

    specs = ROOT / 'research/platform/specs'
    specs.mkdir(parents=True, exist_ok=True)
    current = ['ARCHITECTURE_VISION_SPEC_r3.md', 'SOL_IMPLEMENTATION_HANDOFF_r2.md', 'FORMAL_SOURCE_CHECK_r1.md']
    imports = []
    for name in current:
        source = legacy / 'next_generation' / name
        text = source.read_text(encoding='utf-8')
        text = text.replace('../generative_ecology/', '../../../archive/legacy-testbed/generative_ecology/')
        text = text.replace('`omega_v2/testbed_next/`', '`src/omega_cosmology/testbed/`')
        text = text.replace('Package | Separate `omega_v2/testbed_next/`', 'Package | Separate `src/omega_cosmology/testbed/`')
        notice = ('\n> Repository adaptation, 24 October 2026: selected for the v4.1-based '
                  '`omega-cosmology` preparation. Package paths and imported-reference links '
                  'are adapted; the unchanged source is in `archive/legacy-testbed/`. '
                  'Design readiness does not claim engine implementation.\n')
        first, rest = text.split('\n', 1)
        target = specs / name
        if target.exists():
            raise ValueError('Active adapted specification already exists; revise explicitly')
        target.write_text(first + '\n' + notice + '\n' + rest, encoding='utf-8')
        imports.append({'path': target.relative_to(ROOT).as_posix(), 'source': source.relative_to(ROOT).as_posix(),
                        'source_sha256': digest(source), 'initial_adapted_sha256': digest(target),
                        'changes': 'Repository package path, source links and explicit import status'})
    (specs / 'IMPORTS.json').write_text(json.dumps({'schema': 'omega.design-import/1', 'files': imports}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'prepared', 'archived_design_files': len(imported),
                      'active_specifications': len(imports), 'seed_archive': seed_manifest.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    main()
