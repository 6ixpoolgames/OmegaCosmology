"""Check the standalone workspace and reproduce its retained exact evidence."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / 'runs'):
        parser.error('Choose a fresh directory inside this repository\'s runs directory')
    out.mkdir(parents=True)
    env = {**os.environ, 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
    evidence = ROOT / 'research/probes/P001/evidence'
    checks = []

    def run(label, command):
        p = subprocess.run([sys.executable, *command], cwd=ROOT, env=env,
                           capture_output=True, text=True, encoding='utf-8', timeout=180)
        (out / (label + '.txt')).write_text(p.stdout + p.stderr, encoding='utf-8')
        checks.append({'name': label, 'command': [sys.executable, *command],
                       'exit_code': p.returncode})
        if p.returncode:
            raise RuntimeError(f'{label} failed; see {out / (label + ".txt")}')

    try:
        run('sources', ['scripts/check_sources.py'])
        run('archive', ['scripts/check_archive.py'])
        run('repository', ['scripts/check_repository.py'])
        run('testbed_dependencies', ['-c', 'import numpy, scipy; print("NumPy", numpy.__version__, "SciPy", scipy.__version__)'])
        run('tests', ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py', '-v'])
        run('baseline', ['scripts/run_baseline.py', '--out-dir', str(out / 'baseline')])
        run('P001', ['scripts/run_feedback_probe.py', '--out-dir', str(out / 'P001')])
        actual_summary = json.loads((out / 'P001/SUMMARY.json').read_text(encoding='utf-8'))
        for name, digest in actual_summary['input_sha256'].items():
            if sha256((ROOT / name).read_bytes()).hexdigest() != digest:
                raise RuntimeError(f'Current input hash mismatch: {name}')
        scientific = dict(actual_summary)
        scientific.pop('input_sha256')
        scientific.pop('python_version')
        if scientific != json.loads((evidence / 'EXPECTED.json').read_text(encoding='utf-8')):
            raise RuntimeError('P001 scientific summary differs from retained evidence')
        full = (out / 'P001/FULL_OBJECTS.json').read_bytes()
        if full != (evidence / 'FULL_OBJECTS.json').read_bytes():
            # Historical JSON may use CRLF on Windows. Scientific object equality
            # is cross-platform; the retained historical file keeps its byte hash.
            if json.loads(full) != json.loads((evidence / 'FULL_OBJECTS.json').read_bytes()):
                raise RuntimeError('P001 complete object differs from retained evidence')
        provenance = json.loads((evidence / 'PROVENANCE.json').read_text(encoding='utf-8'))
        for name, field in [('FULL_OBJECTS.json', 'retained_full_objects_sha256'),
                            ('EXPECTED.json', 'expected_semantic_summary_sha256')]:
            if sha256((evidence / name).read_bytes()).hexdigest() != provenance[field]:
                raise RuntimeError(f'Retained evidence changed: {name}')
        result = {'status': 'passed', 'python': platform.python_version(),
                  'checks': checks, 'P001_full_object_equal': True,
                  'P001_scientific_summary_equal': True,
                  'current_input_hashes_verified': True,
                  'limits': 'v4.1 archive integrity, inherited finite evidence and implemented finite-classical engineering tests; no cosmological or ethical validation'}
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        result = {'status': 'failed', 'checks': checks, 'error': str(exc)}
    (out / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return result['status'] != 'passed'


if __name__ == '__main__':
    sys.exit(main())
