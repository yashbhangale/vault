#!/usr/bin/env python3
"""Incremental, private SQLite full-text index of maintained notes."""
import argparse
from pathlib import Path
import re
import sqlite3
import yaml
from engine import VAULT,SYSTEM

DB=SYSTEM/'search.sqlite'
FOLDERS=('02 Processed','03 Journal','04 Trackers','05 Knowledge','06 Projects','07 Areas','08 Resources','09 Outputs')

def connect():
 SYSTEM.mkdir(parents=True,exist_ok=True)
 db=sqlite3.connect(DB)
 db.execute('CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, mtime_ns INTEGER, size INTEGER)')
 db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS notes USING fts5(path UNINDEXED,title,body, tokenize='unicode61')")
 return db

def index(db):
 seen=set();changed=0;unchanged=0
 for folder in FOLDERS:
  for file in (VAULT/folder).rglob('*.md'):
   if not file.is_file() or file.is_symlink():continue
   rel=file.relative_to(VAULT).as_posix()
   if rel.startswith('05 Knowledge/Indexes/'):continue
   seen.add(rel);stat=file.stat();old=db.execute('SELECT mtime_ns,size FROM files WHERE path=?',(rel,)).fetchone()
   if old==(stat.st_mtime_ns,stat.st_size):unchanged+=1;continue
   text=file.read_text(encoding='utf-8',errors='replace')
   match=re.match(r'^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)',text)
   try:meta=yaml.safe_load(match.group(1)) or {} if match else {}
   except yaml.YAMLError:meta={}
   title=str(meta.get('title') or file.stem)
   body=text[match.end():] if match else text
   db.execute('DELETE FROM notes WHERE path=?',(rel,))
   db.execute('INSERT INTO notes(path,title,body) VALUES(?,?,?)',(rel,title,body))
   db.execute('INSERT OR REPLACE INTO files(path,mtime_ns,size) VALUES(?,?,?)',(rel,stat.st_mtime_ns,stat.st_size));changed+=1
 for (rel,) in db.execute('SELECT path FROM files'):
  if rel not in seen:
   db.execute('DELETE FROM notes WHERE path=?',(rel,));db.execute('DELETE FROM files WHERE path=?',(rel,))
 db.commit();return changed,unchanged

parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['index','query']);parser.add_argument('terms',nargs='*');parser.add_argument('--limit',type=int,default=10);args=parser.parse_args()
db=connect()
if args.mode=='index':
 changed,unchanged=index(db);print(f'indexed {changed} changed notes; skipped {unchanged} unchanged notes')
else:
 terms=' '.join(args.terms).strip()
 if not terms:parser.error('Enter search terms')
 words=re.findall(r'[\w-]+',terms,flags=re.UNICODE)
 if not words:parser.error('Enter words or identifiers')
 expression=' OR '.join('"'+word.replace('"','')+'"' for word in words)
 for path,title,snippet in db.execute("SELECT path,title,snippet(notes,2,'[',']',' … ',18) FROM notes WHERE notes MATCH ? ORDER BY bm25(notes) LIMIT ?",(expression,min(max(args.limit,1),30))):
  print(f'{path}\n  {title} — {snippet.strip()}')
