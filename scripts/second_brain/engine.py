#!/usr/bin/env python3
"""Incremental, local-only Raw -> Processed pipeline. No API calls or model invocation."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlparse, parse_qs
import yaml
from journal import update_activity

REPO = Path(__file__).resolve().parents[2]
VAULT = REPO / 'content'
RAW = VAULT / '01 Raw'
PROCESSED = VAULT / '02 Processed'
SYSTEM = VAULT / '00 System/Manifests'
STATE = SYSTEM / 'processing-state.json'
EVENTS = SYSTEM / 'processing-events.ndjson'
INTAKE = SYSTEM / 'intake.json'
VERSION = '1.3'
STAMP = re.compile(r' - (\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{3})(?=\.[^.]+$)')
VIDEO_ID = re.compile(r'^[A-Za-z0-9_-]{11}$')
TIME_CODE = re.compile(r'(?<!\d)(?:\[)?((?:\d{1,2}:)?[0-5]\d:[0-5]\d)(?:\])?(?!\d)')
URL = re.compile(r'https?://[^\s)>]+')
IMAGE = {'.jpg','.jpeg','.png','.gif','.webp','.svg','.heic'}
AUDIO = {'.ogg','.oga','.opus','.mp3','.m4a','.wav'}
VIDEO = {'.mp4','.mov','.webm'}
TEXT = {'.md','.txt','.srt','.vtt','.html'}


def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest(p:Path):
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
 return h.hexdigest()


def intake():
 return json.loads(INTAKE.read_text()) if INTAKE.exists() else {}


def load():
 if STATE.exists():
  result=json.loads(STATE.read_text());
  if result.get('version')!=1:raise RuntimeError('Unknown manifest version')
  return result
 return {'version':1,'processor_version':VERSION,'items':{}}


def save(data):
 SYSTEM.mkdir(parents=True,exist_ok=True)
 p=STATE.with_suffix('.json.tmp');p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');os.replace(p,STATE)


def event(kind,**fields):
 SYSTEM.mkdir(parents=True,exist_ok=True)
 with EVENTS.open('a') as stream:stream.write(json.dumps({'at':now(),'kind':kind,**fields},ensure_ascii=False)+'\n')


def capture_time(name):
 match=STAMP.search(name)
 if not match:return None
 try:
  year,mon,day,hour,minute,sec,millis=map(int,match.groups())
  value=datetime(year,mon,day,hour,minute,sec,millis*1000)
  return value.isoformat(timespec='milliseconds')
 except ValueError:return None


def frontmatter(text):
 match=re.match(r'^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)',text)
 if not match:return {},text
 try:
  data=yaml.safe_load(match.group(1)) or {}
  return data if isinstance(data,dict) else {},text[match.end():]
 except yaml.YAMLError:return {},text


def source_type(rel):
 parts=rel.parts
 if len(parts)>1 and parts[0]=='01 Raw':
  if parts[1]=='Google' and len(parts)>2:return 'google-'+parts[2].lower().replace(' ','-')
  return {'Telegram':'telegram','OneNote':'onenote','YouTube Transcripts':'youtube','Web Clippings':'web','Manual Captures':'manual'}.get(parts[1],'manual')
 return 'manual'


def unique_source_id(rel,meta):
 source=source_type(rel)
 if source=='onenote' and meta.get('onenote-id'):return f'onenote:{meta["onenote-id"]}'
 # Filename is the stable identifier for plugin captures; content hash detects changes.
 return source+':'+hashlib.sha256(rel.as_posix().encode()).hexdigest()[:20]


def video_id(link):
 try:parsed=urlparse(link)
 except ValueError:return None
 host=(parsed.hostname or '').lower()
 candidate=parsed.path.lstrip('/') if host in ('youtu.be','www.youtu.be') else parse_qs(parsed.query).get('v',[''])[0] if host in ('youtube.com','www.youtube.com','m.youtube.com') else ''
 return candidate if VIDEO_ID.fullmatch(candidate) else None


def classify(text,meta,source):
 if source.startswith('google-'):return 'google-snapshot'
 if source=='youtube':return 'youtube-transcript'
 if source=='web':return 'web-clipping'
 if source=='onenote':return 'onenote-page'
 if source=='telegram':
  lower=text.lower()
  if re.search(r'\b(?:breakfast|lunch|dinner|meal|ate|food)\b',lower):return 'food-entry'
  if re.search(r'\b(?:workout|gym|exercise|reps|sets)\b',lower):return 'workout-entry'
  return 'telegram-message'
 return 'manual-capture'


def output_path(rel):
 relative=rel.relative_to('01 Raw')
 return Path('02 Processed')/(relative.as_posix()+'.md') if rel.suffix.lower()!='.md' else Path('02 Processed')/relative


def ref(target):return f'[[{(target.with_suffix("") if target.suffix.lower()==".md" else target).as_posix()}]]'


def render(rel,p,sha,source_id,captured,source_meta=None):
 meta={};body='';suffix=p.suffix.lower();source=source_type(rel);source_meta=source_meta or {}
 if suffix in TEXT:
  text=p.read_text(encoding='utf-8',errors='replace');meta,body=frontmatter(text)
 else: text=''
 meta={**source_meta,**meta}
 kind=classify(body,meta,source) if suffix in TEXT else 'image' if suffix in IMAGE else 'audio' if suffix in AUDIO else 'video' if suffix in VIDEO else 'attachment'
 title=str(meta.get('title') or p.stem)
 links=[m.group(0) for m in URL.finditer(body)] if body else []
 link=meta.get('source_url') or (next((x for x in links if video_id(x)),None) if source=='youtube' else next(iter(links),None))
 vid=video_id(link) if link else None
 # Use source metadata first. A validated Telegram filename is only a fallback.
 cap=meta.get('captured') or meta.get('created') or meta.get('date') or captured
 stamps=list(dict.fromkeys(TIME_CODE.findall(body)))[:30] if source=='youtube' else []
 lines=[line.strip() for line in body.splitlines() if line.strip() and not line.lstrip().startswith(('![[','![','```','---'))]
 excerpt=' '.join(lines[:3])[:300] if suffix in TEXT else ''
 fields={'title':title,'type':kind,'source':source,'source_id':source_id,'raw_path':rel.as_posix(),'raw_sha256':sha,'processing_version':VERSION,'processing_status':'structured','enrichment_status':'pending'}
 if cap:fields['captured_at']=str(cap)
 if link:fields['source_url']=link
 for key in ('author','published','language','channel'):
  if meta.get(key):fields[key]=str(meta[key])
 if vid:fields['video_id']=vid
 if meta.get('onenote-id'):fields['onenote-id']=meta['onenote-id']
 if stamps:fields['transcript_timestamps']=stamps
 if kind in ('food-entry','workout-entry','image') and source=='telegram' and cap:
  # Link to journal only when a capture date is supplied by source metadata or validated filename.
  m=re.match(r'^\d{4}-\d{2}-\d{2}',str(cap))
  if m:fields['journal_date']=m.group(0)
 header=yaml.safe_dump(fields,sort_keys=False,allow_unicode=True,width=1000)
 output=['---',header.rstrip(),'---','','# '+title,'',f'**Original:** {ref(rel)}','',f'**Kind:** {kind}  ','**Status:** Structured; synthesis pending.','']
 if link:output+=['**Source URL:** '+link,'']
 if stamps:output+=['## Transcript markers','',', '.join(stamps),'']
 if excerpt:output+=['## Source excerpt','',excerpt,'']
 if kind=='google-snapshot':
  # Index deterministic readable records; preserve the API payload only in Raw.
  readable=body.split('\n<!-- payload -->',1)[0].strip()
  if readable:output+=['## Captured records','',readable,'']
 if suffix in IMAGE:
  output+=['## Media','',f'!{ref(rel)}','','No image description has been inferred.','']
 elif suffix in AUDIO|VIDEO:
  output+=['## Media','',f'Open the original {suffix.lstrip(".").upper()} file from the Raw archive. No transcription has been inferred.','']
 output+=['## Connections','',f'- Source: {ref(rel)}']
 if fields.get('journal_date'):output.append(f'- Journal date: {ref(Path("03 Journal/Daily")/(fields["journal_date"]+".md"))}')
 output+=['','## Synthesis','',f'Pending source-grounded review. Add concepts, claims, and related links here without changing {ref(rel)}.','']
 return '\n'.join(output),fields


def discover(state,selected=None,force_hashes=False):
 current={};pending=[];seen={};intake_data=intake();known_hashes={v.get('sha256'):k for k,v in state['items'].items() if v.get('status')=='processed' and v.get('sha256')};stats={'unchanged_without_read':0,'hashed':0,'new':0,'changed':0,'duplicates':0,'missing':0}
 for p in sorted(RAW.rglob('*')):
  if not p.is_file() or p.is_symlink() or p.name.endswith('.source.json'):continue
  rel=p.relative_to(VAULT);key=rel.as_posix()
  if selected and key!=selected and p.name!=selected:continue
  st=p.stat();old=state['items'].get(key);same=bool(old and old.get('size')==st.st_size and old.get('mtime_ns')==st.st_mtime_ns)
  if same and not force_hashes and old.get('sha256'):
   h=old['sha256'];stats['unchanged_without_read']+=1
  else:
   h=digest(p);stats['hashed']+=1
  meta={}
  if p.suffix.lower() in TEXT and (not old or old.get('sha256')!=h):
   # Only inspect selected new/changed text content, never the whole vault.
   meta,_=frontmatter(p.read_text(encoding='utf-8',errors='replace'))
  meta={**intake_data.get(key,{}),**meta}
  id=old.get('source_id') if old and old.get('source_id') else unique_source_id(rel,meta)
  captured=old.get('capture_timestamp') if old else None
  if not captured:captured=capture_time(p.name)
  record={**(old or {}),'source_id':id,'raw_path':key,'source_type':source_type(rel),'original_filename':p.name,'size':st.st_size,'mtime_ns':st.st_mtime_ns,'sha256':h,'capture_timestamp':captured,'first_seen_at':old.get('first_seen_at') if old else now(),'processor_version':VERSION}
  record.pop('import_timestamp',None)
  if intake_data.get(key,{}).get('import_timestamp'):record['import_timestamp']=intake_data[key]['import_timestamp']
  if not old:stats['new']+=1
  elif old.get('sha256')!=h:stats['changed']+=1
  if old and old.get('sha256')!=h:
   record.setdefault('history',[]).append({'sha256':old.get('sha256'),'processed_at':old.get('last_processed_at'),'output':old.get('output')})
   record['status']='pending'
  elif not old:record['status']='pending'
  duplicate=seen.get(h) or known_hashes.get(h)
  if duplicate==key:duplicate=None
  if duplicate:record['duplicate_of']=duplicate;stats['duplicates']+=1
  current[key]=record;seen.setdefault(h,key)
  compatible=(VERSION,'1.2','1.1') if p.suffix.lower()=='.md' else (VERSION,'1.2')
  if record.get('status')!='processed' or record.get('last_processed_hash')!=h or record.get('last_processed_version') not in compatible or not record.get('output') or not (VAULT/record['output']).exists():pending.append(key)
 for key,old in state['items'].items():
  if key not in current and (not selected or key==selected):
   current[key]={**old,'status':'missing'};stats['missing']+=1
 if selected:
  state['items'].update(current)
 else:state['items']=current
 return pending,stats


def update_source_index(state,source):
 names={'telegram':'Telegram','onenote':'OneNote','youtube':'YouTube Transcripts','web':'Web Clippings','manual':'Manual Captures'}
 folder=names.get(source,source)
 records=sorted((row for row in state['items'].values() if row.get('source_type')==source and row.get('status')=='processed'),key=lambda row:(row.get('capture_timestamp') or '',row['raw_path']))
 target=PROCESSED/folder/'_index.md';target.parent.mkdir(parents=True,exist_ok=True)
 lines=['---',f'title: {json.dumps(folder+" processed index")}', 'type: index','publish: false','---','',f'# {folder}','',f'{len(records)} processed records.']
 for row in records:lines.append(f'- {ref(Path(row["output"]))} — {row.get("kind","record")}'+(f' ({row["capture_timestamp"]})' if row.get('capture_timestamp') else ''))
 text='\n'.join(lines)+'\n'
 if not target.exists() or target.read_text()!=text:
  staged=target.with_name(target.name+'.tmp');staged.write_text(text);os.replace(staged,target)


def process(state,pending,retry_failed=False,limit=None):
 processed=0;errors=0;intake_data=intake();affected=set()
 for key in pending[:limit]:
  row=state['items'][key]
  if row.get('status')=='error' and not retry_failed:continue
  p=VAULT/key;rel=Path(key);target=VAULT/output_path(rel)
  try:
   body,fields=render(rel,p,row['sha256'],row['source_id'],row.get('capture_timestamp'),intake_data.get(key))
   # Distinct raw files have distinct records, even if the content hash matches.
   if row.get('duplicate_of'):
    body+=f'\n**Duplicate candidate:** {ref(Path(row["duplicate_of"]))}. Review before merging.\n'
   old_output=VAULT/row['output'] if row.get('output') else None
   if old_output and old_output.exists():
    if digest(old_output)!=row.get('output_sha256'):raise RuntimeError('Processed output was edited; merge manually before reprocessing')
    if old_output!=target or row.get('last_processed_hash')!=row['sha256'] or row.get('output_sha256')!=hashlib.sha256(body.encode()).hexdigest():
     archive=VAULT/'10 Archive/Processed Versions'/hashlib.sha256(key.encode()).hexdigest()[:16]/((row.get('last_processed_version') or 'unknown')+'-'+(row.get('output_sha256') or 'unknown')[:16]+'.md')
     archive.parent.mkdir(parents=True,exist_ok=True)
     if archive.exists() and digest(archive)!=row['output_sha256']:raise RuntimeError('Archive collision')
     if not archive.exists():archive.write_bytes(old_output.read_bytes())
   target.parent.mkdir(parents=True,exist_ok=True)
   tmp=target.with_name(target.name+'.tmp');tmp.write_text(body,encoding='utf-8');os.replace(tmp,target)
   actual=digest(target)
   if actual!=hashlib.sha256(body.encode()).hexdigest():raise RuntimeError('Output verification failed')
   if old_output and old_output!=target and old_output.exists() and digest(old_output)==row.get('output_sha256'):
    old_output.unlink()
   row.update({'status':'processed','last_processed_hash':row['sha256'],'last_processed_at':now(),'last_processed_version':VERSION,'output':target.relative_to(VAULT).as_posix(),'output_sha256':actual,'kind':fields['type'],'error':None})
   update_activity(VAULT,row,fields)
   event('processed',source_id=row['source_id'],raw=key,output=row['output'],sha256=row['sha256'])
   processed+=1;affected.add(row['source_type'])
  except Exception as exc:
   row.update({'status':'error','error':str(exc),'last_error_at':now()});event('error',raw=key,error=str(exc));errors+=1
  save(state)
 for source in affected:update_source_index(state,source)
 return processed,errors


def main():
 parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['discover','process','status','retry','verify']);parser.add_argument('--file');parser.add_argument('--limit',type=int);parser.add_argument('--verify-hashes',action='store_true');args=parser.parse_args()
 state=load()
 if args.mode=='status':
  from collections import Counter
  print(json.dumps({'items':len(state['items']),'states':Counter(v.get('status') for v in state['items'].values())},indent=2));return
 selected=args.file
 if args.mode=='verify':
  bad=[]
  for key,row in state['items'].items():
   if selected and key!=selected:continue
   if row.get('status')=='processed' and (not row.get('output') or not (VAULT/row['output']).exists() or digest(VAULT/row['output'])!=row.get('output_sha256')):bad.append(key)
  print(json.dumps({'verified':len(state['items'])-len(bad),'broken_outputs':bad},indent=2));sys.exit(1 if bad else 0)
 pending,stats=discover(state,selected,args.verify_hashes)
 if args.mode=='retry':pending=[key for key in pending if state['items'][key].get('status')=='error']
 if args.mode in ('process','retry'):
  done,failed=process(state,pending,retry_failed=args.mode=='retry',limit=args.limit)
  stats.update({'selected':len(pending),'processed':done,'failed':failed})
 else:stats['selected']=len(pending)
 save(state);print(json.dumps(stats,indent=2));sys.exit(1 if stats.get('failed') else 0)

if __name__=='__main__':main()
