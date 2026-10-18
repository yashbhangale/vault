"""Idempotent dated activity links based only on timestamped source evidence."""
from pathlib import Path
import os
import re
import yaml


def link(path):
 p=Path(path)
 return (p.with_suffix('') if p.suffix.lower()=='.md' else p).as_posix()

def update_activity(vault:Path,row:dict,fields:dict):
 old_date=row.get('journal_date')
 new_date=fields.get('journal_date') if fields.get('type') in ('food-entry','workout-entry','image') and row.get('source_type')=='telegram' else None
 marker=row['source_id'].replace('--','')
 start=f'<!-- capture:{marker}:start -->';end=f'<!-- capture:{marker}:end -->'
 for date in set(filter(None,[old_date,new_date])):
  file=vault/'03 Journal/Daily'/f'{date}.md'
  if not file.exists() and date==new_date:
   file.parent.mkdir(parents=True,exist_ok=True)
   meta={'title':date,'type':'daily-note','date':date,'source':'journal','publish':False}
   text='---\n'+yaml.safe_dump(meta,sort_keys=False)+'---\n\n# '+date+'\n\n## Events\n\n## Photos\n\n## Food\n\n## Workout\n\n## Habits\n\n## Reflections and lessons\n\n## Related captures\n'
  elif file.exists():text=file.read_text()
  else:continue
  text=re.sub(re.escape(start)+r'[\s\S]*?'+re.escape(end)+r'\n?', '',text)
  if date==new_date:
   heading='## Food' if fields['type']=='food-entry' else '## Workout' if fields['type']=='workout-entry' else '## Photos'
   if fields['type']=='image':
    block=f'{start}\n- [[{link(row["output"])}|Photo record]] (source: [[{link(row["raw_path"])}|original image]])\n\n![[{row["raw_path"]}]]\n{end}\n'
   else:
    block=f'{start}\n- [[{link(row['output'])}|{fields["type"]}]] from [[{link(row['raw_path'])}|source capture]].\n{end}\n'
   if heading not in text:text+='\n'+heading+'\n'
   text=text.replace(heading+'\n',heading+'\n\n'+block,1)
  temp=file.with_name(file.name+'.tmp');temp.write_text(text);os.replace(temp,file)
 row['journal_date']=new_date
