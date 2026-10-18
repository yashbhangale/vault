#!/usr/bin/env python3
"""Accept a reviewed, source-grounded edit to one processed record."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import yaml
from engine import VAULT,load,save,event,digest

parser=argparse.ArgumentParser();parser.add_argument('raw_path');args=parser.parse_args()
key=args.raw_path.removeprefix('content/').lstrip('/')
state=load();row=state['items'].get(key)
if not row or row.get('status')!='processed':parser.error('No processed record for that Raw path')
raw=VAULT/key;output=VAULT/row['output']
if not raw.is_file() or digest(raw)!=row['sha256']:parser.error('Raw changed; process the new version first')
if not output.is_file():parser.error('Processed output missing')
text=output.read_text();m=re.match(r'^---\n([\s\S]*?)\n---\n',text)
if not m:parser.error('Processed note has no YAML frontmatter')
meta=yaml.safe_load(m.group(1)) or {}
if meta.get('raw_path')!=key or meta.get('raw_sha256')!=row['sha256']:parser.error('Processed note provenance mismatch')
if meta.get('enrichment_status')!='reviewed':parser.error('Mark enrichment_status: reviewed after source review')
if '[[02 Processed/' in text and '[[01 Raw/' not in text:parser.error('Processed note lacks a Raw link')
if len(text[m.end():].strip())<80:parser.error('Reviewed record is too short')
previous=row.get('output_sha256');actual=digest(output)
if actual!=previous:
 row.update({'output_sha256':actual,'enriched_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'enrichment_source_hash':row['sha256']})
 event('enriched',raw=key,output=row['output'],sha256=actual)
 save(state)
print(json.dumps({'accepted':True,'raw_path':key,'output':row['output'],'changed':actual!=previous}))
