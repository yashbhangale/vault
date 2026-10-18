#!/usr/bin/env python3
"""Copy a transcript or clipping into Raw, retaining the source file and provenance."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
from urllib.parse import urlparse
from engine import REPO, VAULT, SYSTEM, INTAKE

parser=argparse.ArgumentParser()
parser.add_argument('--source',required=True,choices=['youtube','web','manual'])
parser.add_argument('--file',required=True,type=Path)
parser.add_argument('--url')
parser.add_argument('--title')
parser.add_argument('--author')
parser.add_argument('--published')
parser.add_argument('--captured')
args=parser.parse_args()
src=args.file.expanduser().resolve()
if not src.is_file():parser.error('Input file does not exist')
if args.url and urlparse(args.url).scheme not in ('http','https'):parser.error('URL must be HTTP(S)')
folder={'youtube':'YouTube Transcripts','web':'Web Clippings','manual':'Manual Captures'}[args.source]
dest=VAULT/'01 Raw'/folder/src.name
if dest.resolve()==src:parser.error('File is already in the raw destination')
dest.parent.mkdir(parents=True,exist_ok=True)
if dest.exists():
 original=hashlib.sha256(src.read_bytes()).hexdigest(); existing=hashlib.sha256(dest.read_bytes()).hexdigest()
 if original==existing:
  print(json.dumps({'status':'already-present','raw_path':dest.relative_to(VAULT).as_posix()}));raise SystemExit(0)
 dest=dest.with_name(dest.stem+'--'+original[:12]+dest.suffix)
 if dest.exists():parser.error('A different file has the same collision-safe destination')
temp=dest.with_name(dest.name+'.tmp');shutil.copyfile(src,temp);os.replace(temp,dest)
if hashlib.sha256(src.read_bytes()).digest()!=hashlib.sha256(dest.read_bytes()).digest():raise RuntimeError('Copy verification failed')
SYSTEM.mkdir(parents=True,exist_ok=True)
metadata=json.loads(INTAKE.read_text()) if INTAKE.exists() else {}
row={'source':args.source,'original_filename':src.name,'import_timestamp':datetime.now(timezone.utc).isoformat(timespec='seconds')}
for key in ('url','title','author','published','captured'):
 val=getattr(args,key)
 if val:row['source_url' if key=='url' else key]=val
key=dest.relative_to(VAULT).as_posix();metadata[key]=row
staged=INTAKE.with_suffix('.json.tmp');staged.write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n');os.replace(staged,INTAKE)
print(json.dumps({'status':'imported','raw_path':key,'bytes':dest.stat().st_size}))
