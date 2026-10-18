#!/usr/bin/env python3
"""One-time, planned vault migration. Run plan, then apply against unchanged hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, quote

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / 'content'
PLAN = ROOT / '00 System/Manifests/migration-plan.json'
# Move whole legacy trees without flattening their internal structure.
FOLDERS = {
    'Telegram': '01 Raw/Telegram',
    'OneNote': '01 Raw/OneNote',
    '3.Inbox': '01 Raw/Manual Captures/Inbox',
    'Untitled': '01 Raw/Manual Captures/Untitled',
    '6.Daily-Notes': '03 Journal/Daily',
    '4.office': '07 Areas/Work',
    'resume': '07 Areas/Career/Resume',
    'linkedin': '07 Areas/Career/LinkedIn',
    '11.switch': '08 Resources/Career/Switch',
    'For Job': '08 Resources/Career/Job Search',
    'Projects': '06 Projects',
    'thecloudops.store': '06 Projects/thecloudops.store',
    '1.DevOps - Cloud': '05 Knowledge/Cloud and DevOps',
    '2.DSA': '05 Knowledge/Programming/DSA',
    'Java Learning': '05 Knowledge/Programming/Java',
    'SQL': '05 Knowledge/Programming/SQL',
    'ReactJS': '05 Knowledge/Programming/ReactJS',
    'NodeJs': '05 Knowledge/Programming/NodeJs',
    'python learning': '05 Knowledge/Programming/Python',
    '9.Product Management': '07 Areas/Product Management',
    '10.prompt engineering': '05 Knowledge/AI/Prompt Engineering',
    '7.self help': '05 Knowledge/Personal Growth',
    '5.Books': '08 Resources/Books',
    'Excalidraw': '08 Resources/Drawings',
    '0.Templates': '00 System/Templates',
    '00.Knowledgebase': '00 System/Legacy Indexes',
}
ROOT_FILES = {
    'Docker file.md': '05 Knowledge/Cloud and DevOps/Docker/Docker file.md',
    'Git Flow.md': '05 Knowledge/Cloud and DevOps/git/Git Flow.md',
    'Install kubectl.md': '05 Knowledge/Cloud and DevOps/Kubernates notes/Install kubectl.md',
    'Minikube.md': '05 Knowledge/Cloud and DevOps/Kubernates notes/Minikube.md',
    'Hinglish_sagemaker_guide_to_deploy_model.md': '05 Knowledge/Cloud and DevOps/AWS/Hinglish_sagemaker_guide_to_deploy_model.md',
    'High Level Architecture i can refer.md': '05 Knowledge/Architecture/High Level Architecture i can refer.md',
    'Hinglish_Code_walkthrough_fast_prod_new_py.md': '06 Projects/Code walkthrough fast_prod_new.py.md',
    'aistylistdocker.md': '06 Projects/aistylistdocker.md',
    'Gov exams analysis.md': '08 Resources/Career/Gov exams analysis.md',
    '2026-09-10.md': '03 Journal/Daily/2026-09-10.md',
    '2026-09-11.md': '03 Journal/Daily/2026-09-11.md',
    'Oneture 23 sept  meeting.md': '07 Areas/Work/Oneture 23 sept  meeting.md',
    'Stocks.md': '07 Areas/Finance/Stocks.md',
    'Rough.md': '01 Raw/Manual Captures/Rough.md',
    'Untitled.md': '01 Raw/Manual Captures/Untitled.md',
    'Trying things locally.md': '01 Raw/Manual Captures/Trying things locally.md',
    'gemini key creds of yashbhangale2003@gmail.com acc.md': '01 Raw/Manual Captures/gemini key creds of yashbhangale2003@gmail.com acc.md',
}
# All other root assets are imports/captures; keep filenames exactly.
RESERVED = {'index.md','organize_vault.py','Code walkthrough fast_prod_new.py'}


def sha(file: Path) -> str:
    h = hashlib.sha256()
    with file.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''): h.update(block)
    return h.hexdigest()


def dest(rel: str) -> str | None:
    parts = rel.split('/')
    if parts[0] in FOLDERS:
        target = FOLDERS[parts[0]]
        return '/'.join([target, *parts[1:]])
    if len(parts) == 1:
        if rel in ROOT_FILES: return ROOT_FILES[rel]
        if rel in RESERVED: return None
        if rel.endswith('.md'): return f'01 Raw/Manual Captures/{rel}'
        return f'01 Raw/Attachments/{rel}'
    return None


def plan() -> dict:
    records=[]
    targets={}
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(x.startswith('.') for x in p.relative_to(ROOT).parts): continue
        rel=p.relative_to(ROOT).as_posix()
        new=dest(rel)
        if not new or new==rel: continue
        if new in targets: raise RuntimeError(f'Collision: {rel} and {targets[new]} -> {new}')
        targets[new]=rel
        if (ROOT/new).exists() and new not in targets.values(): raise RuntimeError(f'Target exists: {new}')
        records.append({'from':rel,'to':new,'sha256':sha(p),'bytes':p.stat().st_size})
    return {'version':1,'count':len(records),'files':records}


def mapped_path(old: str, mapping: dict[str,str]) -> str:
    return mapping.get(old,old)


def update_links(text: str, old_note: str, new_note: str, mapping: dict[str,str], original_files: set[str]) -> str:
    # Leave raw source bytes untouched. Their original citations remain in the backup;
    # processed records refer to their new canonical paths.
    if new_note.startswith('01 Raw/'): return text
    def wiki(m):
        raw=m.group(2)
        path, sep, suffix=raw.partition('|')
        anchor=''
        if '#' in path: path,anchor=path.split('#',1); anchor='#'+anchor
        key=path.lstrip('/')
        candidates=[key, key+'.md']
        match=next((c for c in candidates if c in mapping),None)
        if not match: return m.group(0)
        new=mapping[match]
        if not key.endswith('.md') and new.endswith('.md'):new=new[:-3]
        return m.group(1)+new+anchor+(sep+suffix if sep else '')+m.group(3)
    text=re.sub(r'(!?\[\[)([^\]\n]+)(\]\])',wiki,text)
    def markdown(m):
        target=m.group(2).strip()
        bracket=target.startswith('<') and target.endswith('>')
        raw=target[1:-1] if bracket else target
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',raw) or raw.startswith('//') or raw.startswith('#'): return m.group(0)
        raw_path,hashmark,frag=raw.partition('#')
        decoded=unquote(raw_path)
        if decoded.startswith('/'):
            old_target=decoded.lstrip('/')
            absolute=True
        else:
            old_target=os.path.normpath(str(PurePosixPath(old_note).parent / decoded)).replace('\\','/')
            absolute=False
        if old_target not in original_files: return m.group(0)
        new_target=mapped_path(old_target,mapping)
        if absolute: new_url='/'+new_target
        else: new_url=os.path.relpath(new_target,str(PurePosixPath(new_note).parent)).replace('\\','/')
        new_url=quote(new_url,safe='/.-_~')
        if hashmark:new_url+='#'+frag
        return m.group(1)+('<'+new_url+'>' if bracket or ' ' in new_url else new_url)+m.group(3)
    return re.sub(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^)\n]+)(\))',markdown,text)


def apply(saved:dict):
    files=saved['files']; mapping={r['from']:r['to'] for r in files}
    if len(mapping)!=saved['count']:raise RuntimeError('Plan count mismatch')
    for record in files:
        p=ROOT/record['from']; t=ROOT/record['to']
        if not p.is_file() or t.exists() or sha(p)!=record['sha256']:raise RuntimeError(f'Source changed or target exists: {record["from"]}')
    original_files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    for record in files:
        src=ROOT/record['from']; target=ROOT/record['to']; target.parent.mkdir(parents=True,exist_ok=True); src.rename(target)
    # Remove now-empty old directories without touching anything left in them.
    for old in sorted(FOLDERS,key=len,reverse=True):
        p=ROOT/old
        if p.exists():
            for d in sorted((x for x in p.rglob('*') if x.is_dir()),key=lambda x:len(x.parts),reverse=True):
                if not any(d.iterdir()):d.rmdir()
            if p.exists() and not any(p.iterdir()):p.rmdir()
    changed=[]
    for p in ROOT.rglob('*.md'):
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith('01 Raw/') or any(x.startswith('.') for x in p.relative_to(ROOT).parts):continue
        old=next((source for source,target in mapping.items() if target==rel),rel)
        original=p.read_text(errors='replace')
        updated=update_links(original,old,rel,mapping,original_files)
        if updated!=original:p.write_text(updated);changed.append(rel)
    for record in files:
        target=ROOT/record['to']
        if record['to'].startswith('01 Raw/') and sha(target)!=record['sha256']:raise RuntimeError(f'Raw hash changed: {record["to"]}')
    report={'moved':len(files),'raw_files_preserved':sum(r['to'].startswith('01 Raw/') for r in files),'notes_with_rewritten_links':len(changed),'link_rewrites':changed}
    (PLAN.parent/'migration-result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='link_rewrites'},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('mode',choices=['plan','apply']); args=parser.parse_args()
    if args.mode=='plan':
        result=plan(); PLAN.parent.mkdir(parents=True,exist_ok=True);PLAN.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'planned_moves':result['count'],'bytes':sum(r['bytes'] for r in result['files'])},indent=2))
    else: apply(json.loads(PLAN.read_text()))
