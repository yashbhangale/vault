#!/usr/bin/env python3
"""Backfill inline Raw image embeds in existing processed image records."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path

from engine import VAULT, digest, event, load, save


def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--dry-run',action='store_true')
 args=parser.parse_args()
 state=load();updated=0;already_embedded=0
 for key,row in state['items'].items():
  if row.get('status')!='processed' or row.get('kind')!='image':continue
  raw=VAULT/key;output=VAULT/row['output']
  if not raw.is_file() or digest(raw)!=row['sha256']:
   raise RuntimeError(f'Raw image missing or changed: {key}')
  if not output.is_file() or digest(output)!=row['output_sha256']:
   raise RuntimeError(f'Processed image record missing or edited: {row["output"]}')
  body=output.read_text(encoding='utf-8')
  embed=f'![[{key}]]'
  if embed in body:
   already_embedded+=1;continue
  marker='## Media\n\n'
  if marker not in body:raise RuntimeError(f'No Media section: {row["output"]}')
  revised=body.replace(marker,marker+embed+'\n\n',1)
  if not args.dry_run:
   temp=output.with_name(output.name+'.tmp')
   temp.write_text(revised,encoding='utf-8')
   os.replace(temp,output)
   row['output_sha256']=digest(output)
   row['image_embed_added_at']=datetime.now(timezone.utc).isoformat(timespec='seconds')
   save(state)
   event('image_embed_added',raw=key,output=row['output'])
  updated+=1
 print(json.dumps({'updated':updated,'already_embedded':already_embedded,'dry_run':args.dry_run}))


if __name__=='__main__':main()
