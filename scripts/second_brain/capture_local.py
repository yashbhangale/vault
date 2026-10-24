#!/usr/bin/env python3
"""Serialize a dashboard capture with the Google collector's existing lock."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import engine
import google_capture


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=Path, required=True)
    args = parser.parse_args()
    try:
        with google_capture.lock():
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('ingest.py')), '--source', 'manual', '--file', str(args.file), '--captured', datetime.now(timezone.utc).isoformat()], capture_output=True, text=True, check=True)
            raw = json.loads(result.stdout)['raw_path']
            state = engine.load()
            pending, _ = engine.discover(state, selected=raw)
            _, failed = engine.process(state, pending)
            engine.save(state)
            if failed:
                raise RuntimeError('Processing failed; original capture is preserved in Raw')
            print(json.dumps({'raw_path': raw}))
    except Exception:
        print('Capture could not complete. If a sync is running, wait and retry; otherwise check the processing manifest.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
