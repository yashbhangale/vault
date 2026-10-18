#!/usr/bin/env python3
"""Path/hash/backlink support for Codex's on-demand Hinglish adaptation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import yaml
from engine import VAULT

HUB=VAULT/'02 Processed/Hinglish'
LINK=re.compile(r'^\*\*Hinglish:\*\* \[\[[^\n]+\]\]\n?',re.M)
FM=re.compile(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n')


def resolve(target):
 p=Path(target)
 if p.is_absolute():
  try:rel=p.relative_to(VAULT)
  except ValueError:raise ValueError('Note must be inside the vault')
 elif (VAULT/p).is_file():rel=p
 else:
  name=p.name.lower();matches=[x.relative_to(VAULT) for x in VAULT.rglob('*.md') if x.name.lower()==name or x.stem.lower()==name]
  if len(matches)!=1:raise ValueError('Ambiguous or missing note: '+json.dumps([x.as_posix() for x in matches[:20]]))
  rel=matches[0]
 if not (VAULT/rel).is_file():raise ValueError('Note does not exist')
 if rel.as_posix().startswith('02 Processed/Hinglish/') or rel.stem.lower().startswith('hinglish_'):raise ValueError('Selected note is already a Hinglish copy or clearly titled Hinglish')
 text=(VAULT/rel).read_text()
 match=FM.match(text)
 if match:
  data=yaml.safe_load(match.group(1)) or {}
  if data.get('type')=='hinglish-transcription' or str(data.get('language','')).lower()=='hinglish':raise ValueError('Selected note is already marked Hinglish')
 return rel,data if match else {}


def canonical_hash(rel):
 text=(VAULT/rel).read_text()
 return hashlib.sha256(LINK.sub('',text).encode()).hexdigest()


def counterpart(rel):
 if rel.as_posix().startswith('05 Knowledge/'):
  rest=rel.relative_to('05 Knowledge')
 elif rel.as_posix().startswith('02 Processed/'):
  rest=Path('Processed')/rel.relative_to('02 Processed')
 else:rest=Path('Notes')/rel
 return HUB/rest


def main():
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['prepare','finalize','check']);parser.add_argument('target',nargs='?');args=parser.parse_args()
 if args.mode=='check':
  stale=[];checked=0
  for p in HUB.rglob('*.md'):
   m=FM.match(p.read_text())
   if not m:continue
   data=yaml.safe_load(m.group(1)) or {};original=data.get('canonical_path')
   if not original:continue
   checked+=1
   if not (VAULT/original).exists() or data.get('canonical_sha256')!=canonical_hash(Path(original)):stale.append(p.relative_to(VAULT).as_posix())
  print(json.dumps({'checked':checked,'stale':stale},indent=2));raise SystemExit(1 if stale else 0)
 if not args.target:parser.error('A target note path or unique title is required')
 try:rel,data=resolve(args.target)
 except ValueError as err:parser.error(str(err))
 dest=counterpart(rel);result={'canonical':rel.as_posix(),'canonical_sha256':canonical_hash(rel),'hinglish_path':dest.relative_to(VAULT).as_posix(),'source_raw':data.get('raw_path')}
 if args.mode=='prepare':
  result['exists']=dest.exists()
  if dest.exists():
   m=FM.match(dest.read_text());previous=yaml.safe_load(m.group(1)) if m else {}
   result['stale']=previous.get('canonical_sha256')!=result['canonical_sha256']
  print(json.dumps(result,indent=2));return
 if not dest.exists():parser.error('Write the Hinglish adaptation at the prepared path first')
 text=dest.read_text();m=FM.match(text)
 if not m:parser.error('Hinglish file needs YAML frontmatter')
 meta=yaml.safe_load(m.group(1)) or {}
 if meta.get('type')!='hinglish-transcription' or meta.get('canonical_path')!=rel.as_posix() or meta.get('canonical_sha256')!=result['canonical_sha256']:parser.error('Hinglish frontmatter does not match the current canonical note')
 if meta.get('transcription_status')!='current':parser.error('Transcription must be marked current')
 if len(text[m.end():].strip())<30:parser.error('Transcription body is too short to verify')
 back=f'[[{rel.with_suffix("").as_posix()}]]'
 if back not in text:parser.error('Hinglish note must link back to the canonical note')
 original=(VAULT/rel).read_text();head=FM.match(original)
 link=f'**Hinglish:** [[{dest.relative_to(VAULT).with_suffix("").as_posix()}|Read in Hinglish]]\n'
 updated=LINK.sub('',original)
 if head:updated=updated[:head.end()]+link+updated[head.end():]
 else:updated=link+updated
 (VAULT/rel).write_text(updated)
 print(json.dumps({'linked':True,**result},indent=2))

if __name__=='__main__':main()
