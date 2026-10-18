#!/usr/bin/env python3
"""Repair only links with an exact destination in the verified migration map."""
import json
import os
from pathlib import Path
import re
from urllib.parse import quote,unquote
from migrate import ROOT,PLAN

mapping={row['from']:row['to'] for row in json.loads(PLAN.read_text())['files']}
changes=0;files=0
for p in ROOT.rglob('*.md'):
 rel=p.relative_to(ROOT).as_posix()
 if rel.startswith(('01 Raw/','10 Archive/','00 System/Legacy Indexes/')):continue
 text=p.read_text(errors='replace')
 def replace(m):
  global changes
  old=m.group(2).strip('<>')
  path,sep,frag=old.partition('#');plain=unquote(path).lstrip('/')
  if plain not in mapping:return m.group(0)
  dest=mapping[plain]
  if not (ROOT/dest).exists():return m.group(0)
  new=os.path.relpath(dest,p.parent.relative_to(ROOT)).replace('\\','/')
  new=quote(new,safe='/.-_~')+(sep+frag if sep else '')
  changes+=1
  return m.group(1)+'<'+new+'>'+m.group(3)
 updated=re.sub(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^)\n]+)(\))',replace,text)
 if updated!=text:p.write_text(updated);files+=1
print(json.dumps({'rewritten_links':changes,'files':files}))
