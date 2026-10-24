"""Materialize connector-issued transfers; signed URLs stay in ignored plans."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.part')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def materialize(job):
    target = (ROOT / job['path']).resolve()
    if not target.is_relative_to(ROOT) or target.is_relative_to(ROOT / '.git'):
        raise ValueError('Transfer target outside the archive workspace')
    expected = job.get('expected_bytes')
    if target.exists():
        data = target.read_bytes()
        if expected is not None and len(data) != expected:
            return {'id': job['id'], 'status': 'existing_size_mismatch', 'path': job['path']}
        return {'id': job['id'], 'status': 'reused', 'path': job['path'],
                'bytes': len(data), 'sha256': sha256(data).hexdigest()}
    target.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            with urlopen(Request(job['download_url'], headers={'User-Agent': 'OmegaArchive/1'}), timeout=45) as response:
                data = response.read()
            if expected is not None and len(data) != expected:
                return {'id': job['id'], 'status': 'download_size_mismatch',
                        'path': job['path'], 'bytes': len(data), 'expected_bytes': expected}
            temporary = target.with_suffix(target.suffix + '.part')
            temporary.write_bytes(data)
            temporary.replace(target)
            return {'id': job['id'], 'status': 'downloaded', 'path': job['path'],
                    'bytes': len(data), 'sha256': sha256(data).hexdigest()}
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            if attempt == 2:
                return {'id': job['id'], 'status': 'failed', 'path': job['path'],
                        'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)}
            time.sleep(attempt + 1)
    raise AssertionError('Unreachable retry state')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    receipts = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(materialize, job): job for job in plan['jobs']}
        for future in as_completed(futures):
            receipts.append(future.result())
            write_json(args.receipts, {'schema': 'omega.archive.transfer-receipts/1', 'files': receipts})
    counts = {s: sum(r['status'] == s for r in receipts) for s in {r['status'] for r in receipts}}
    print(json.dumps({'files': len(receipts), 'statuses': counts,
                      'bytes': sum(r.get('bytes', 0) for r in receipts)}))
    return any(r['status'] not in ('downloaded', 'reused') for r in receipts)


if __name__ == '__main__':
    sys.exit(main())
