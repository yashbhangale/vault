#!/usr/bin/env python3
"""Deterministic vault audit. Reads link syntax and metadata, not note prose into model context."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import yaml
from engine import REPO,VAULT,load,digest
from hinglish import HUB,FM,canonical_hash

notes=[];allfiles=set();by_stem=defaultdict(list);by_name=defaultdict(list);metadata_errors=[]
for p in VAULT.rglob('*'):
 if not p.is_file() or p.is_symlink() or any(x.startswith('.') for x in p.relative_to(VAULT).parts):continue
 rel=p.relative_to(VAULT).as_posix();allfiles.add(rel);by_name[p.name.lower()].append(rel)
 if p.suffix=='.md':notes.append((p,rel));by_stem[p.stem.lower()].append(rel)

broken=[];ambiguous=[];inbound=Counter();links=0
for p,rel in notes:
 if rel.startswith(('10 Archive/','00 System/Legacy Indexes/')):continue
 text=p.read_text(encoding='utf-8',errors='replace')
 text=re.sub(r'(?ms)^```.*?^```','',text)
 head=re.match(r'^---\r?\n([\s\S]*?)\r?\n---',text)
 if head:
  try:data=yaml.safe_load(head.group(1)) or {}
  except yaml.YAMLError as err:metadata_errors.append({'path':rel,'error':str(err).splitlines()[0]});data={}
 else:data={}
 if rel.startswith(('05 Knowledge/','06 Projects/','08 Resources/')) and not rel.startswith('05 Knowledge/Indexes/'):
  missing=[k for k in ('title','type','area','source') if not data.get(k)]
  if missing:metadata_errors.append({'path':rel,'missing':missing})
 for target in re.findall(r'!?\[\[([^\]\n]+)\]\]',text):
  raw=target.split('|')[0].split('#')[0].strip()
  if not raw:continue
  raw=unquote(raw).lstrip('/')
  candidates=[raw,raw+'.md',raw+'.base']
  possible=[x for x in candidates if x in allfiles]
  if not possible:
   possible=(by_name.get(raw.lower(),[]) or by_stem.get((raw[:-3] if raw.lower().endswith('.md') else raw).lower(),[])) if '/' not in raw else []
  links+=1
  if not possible:broken.append({'from':rel,'target':target,'syntax':'wiki'})
  elif len(possible)>1:ambiguous.append({'from':rel,'target':target,'candidates':possible[:4]})
  else:inbound[possible[0]]+=1
 for target in re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)',text):
  raw=target.strip().strip('<>').split('#')[0]
  if not raw or re.match(r'^[a-z][a-z\d+.-]*:',raw,re.I) or raw.startswith('//'):continue
  raw=unquote(raw)
  resolved=raw.lstrip('/') if raw.startswith('/') else (Path(rel).parent/raw).as_posix()
  resolved=Path(resolved).as_posix()
  while '/..' in resolved or resolved.startswith('../'):
   from os.path import normpath
   resolved=normpath(resolved).replace('\\','/')
   break
  candidates=[resolved,resolved+'.md',resolved+'.base']
  possible=next((x for x in candidates if x in allfiles),None)
  links+=1
  if not possible:broken.append({'from':rel,'target':target,'syntax':'markdown'})
  else:inbound[possible]+=1

state=load();errors=[{'path':k,'error':r.get('error')} for k,r in state['items'].items() if r.get('status')=='error']
stale_outputs=[k for k,r in state['items'].items() if r.get('status')=='processed' and (not r.get('output') or not (VAULT/r['output']).is_file() or digest(VAULT/r['output'])!=r.get('output_sha256') or r.get('last_processed_hash')!=r.get('sha256'))]
stale_hinglish=[]
for p in HUB.rglob('*.md'):
 m=FM.match(p.read_text())
 if not m:continue
 d=yaml.safe_load(m.group(1)) or {};canonical=d.get('canonical_path')
 if canonical and (not (VAULT/canonical).exists() or canonical_hash(Path(canonical))!=d.get('canonical_sha256')):stale_hinglish.append(p.relative_to(VAULT).as_posix())
by_hash=defaultdict(list)
for k,r in state['items'].items():by_hash[r.get('sha256')].append(k)
duplicates=[v for v in by_hash.values() if len(v)>1]
orphan=[rel for _,rel in notes if rel.startswith('05 Knowledge/') and not rel.startswith('05 Knowledge/Indexes/') and not inbound[rel]]
summary={'notes':len(notes),'links_checked':links,'broken_links':broken,'ambiguous_links':ambiguous,'metadata_errors':metadata_errors,'processing_errors':errors,'stale_outputs':stale_outputs,'stale_hinglish':stale_hinglish,'duplicate_raw_candidates':duplicates,'orphan_knowledge_notes':orphan}
out=REPO/'reports/second-brain-audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in summary.items()},indent=2))
if broken[:6]:print('First broken links:',json.dumps(broken[:6],ensure_ascii=False))
