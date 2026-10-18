#!/usr/bin/env python3
"""Source-linked weekly/monthly review of recorded facts only."""
import argparse
from datetime import date,datetime,timedelta
from zoneinfo import ZoneInfo
import json
from pathlib import Path
import re
from engine import VAULT,load

parser=argparse.ArgumentParser();parser.add_argument('period',choices=['weekly','monthly']);parser.add_argument('--end',help='ISO date; defaults to today');args=parser.parse_args()
end=date.fromisoformat(args.end) if args.end else datetime.now(ZoneInfo("Asia/Kolkata")).date()
if args.period=='weekly':start=end-timedelta(days=6);folder='Weekly'
else:start=end.replace(day=1);folder='Monthly'
rows=load()['items'];activities=[]
for row in rows.values():
 stamp=row.get('capture_timestamp');kind=row.get('kind')
 if kind not in ('food-entry','workout-entry') or not stamp or row.get('status')!='processed':continue
 try:day=date.fromisoformat(stamp[:10])
 except ValueError:continue
 if start<=day<=end:activities.append((day,row))
activities.sort(key=lambda x:(x[0],x[1].get('capture_timestamp','')))
journals=[]
for daynum in range((end-start).days+1):
 day=start+timedelta(days=daynum);p=VAULT/'03 Journal/Daily'/f'{day}.md'
 if p.is_file():journals.append(p.relative_to(VAULT))
projects_index=VAULT/'06 Projects/index.md'
name=f'{start.isoformat()} to {end.isoformat()}'
output=VAULT/'09 Outputs'/folder/f'{name}.md';output.parent.mkdir(parents=True,exist_ok=True)
lines=['---',f'title: "{args.period.title()} review {name}"',f'type: {args.period}-review',f'period_start: {start.isoformat()}',f'period_end: {end.isoformat()}','publish: false','---','',f'# {args.period.title()} review: {name}','',f'{len(journals)} journal days and {len(activities)} dated food/workout captures. Project changes are not dated reliably in the existing notes.','', '## Journal days','']
lines += [f'- [[{p.with_suffix("").as_posix()}]]' for p in journals] or ['No journal entries recorded.']
lines += ['','## Food and workouts','']
lines += [f'- {day.isoformat()}: {row["kind"]} — [[{Path(row["output"]).with_suffix("").as_posix()}|processed record]]; [[{Path(row["raw_path"]).with_suffix("").as_posix()}|source]]' for day,row in activities] or ['No dated food or workout captures recorded.']
lines += ['','## Projects','']
lines += ['- [[06 Projects/index|Project index]] — review current milestones and next actions.'] if projects_index.exists() else ['No dated project update log is available.']
lines += ['','## Reflections and next steps','', 'Add your own reflections after reviewing the linked records. No conclusions are inferred from missing entries.','']
text='\n'.join(lines)
if not output.exists() or output.read_text()!=text:output.write_text(text)
print(json.dumps({'path':output.relative_to(VAULT).as_posix(),'journals':len(journals),'activities':len(activities)}))
