import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml

SOURCE=Path(__file__).resolve().parent

class SecondBrainTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.repo=Path(self.temp.name);self.scripts=self.repo/'scripts/second_brain';self.scripts.mkdir(parents=True)
  for name in ('engine.py','ingest.py','hinglish.py','journal.py','enrich.py','capture_local.py','google_capture.py'):shutil.copyfile(SOURCE/name,self.scripts/name)
  (self.repo/'content/01 Raw/Telegram/photos').mkdir(parents=True)
  (self.repo/'content/01 Raw/OneNote').mkdir(parents=True)
  (self.repo/'content/01 Raw/Manual Captures').mkdir(parents=True)
  (self.repo/'content/05 Knowledge/Kubernetes').mkdir(parents=True)
 def cli(self,script,*args,expect=0):
  p=subprocess.run([sys.executable,str(self.scripts/script),*map(str,args)],cwd=self.repo,capture_output=True,text=True)
  self.assertEqual(p.returncode,expect,p.stdout+'\n'+p.stderr)
  return json.loads(p.stdout)
 def put(self,rel,body):
  p=self.repo/'content'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body);return p
 def state(self):return json.loads((self.repo/'content/00 System/Manifests/processing-state.json').read_text())['items']

 def test_dashboard_capture_preserves_original_and_registers_provenance(self):
  external=self.repo/'capture.md';body='A thought captured through the local workspace.\n';external.write_text(body)
  result=self.cli('capture_local.py','--file',external)
  raw=self.repo/'content'/result['raw_path'];self.assertEqual(raw.read_text(),body)
  self.assertEqual(external.read_text(),body)
  row=self.state()[result['raw_path']];self.assertEqual(row['status'],'processed')
  self.assertEqual(row['sha256'],hashlib.sha256(body.encode()).hexdigest())

 def test_incremental_sources_duplicates_retry_and_history(self):
  food=self.put('01 Raw/Telegram/Lunch - 20261018120000000.md','Lunch: rice and dal.')
  workout=self.put('01 Raw/Telegram/Gym - 20261018130000000.md','Workout: running.')
  image=self.repo/'content/01 Raw/Telegram/photos/photo_1_0 - 20261018131500123.jpg';image.write_bytes(b'jpeg fixture')
  transcript=self.put('01 Raw/YouTube Transcripts/video.md','---\ntitle: Scheduling overview\n---\nWatch https://youtu.be/dQw4w9WgXcQ at [00:03:12].')
  clip=self.put('01 Raw/Web Clippings/article.md','Article: a useful concept.')
  onenote=self.put('01 Raw/OneNote/page.md','---\nonenote-id: page-123\ntitle: Source page\n---\nHandwriting export is in the attached file.')
  self.put('01 Raw/Manual Captures/duplicate-a.md','same text')
  self.put('01 Raw/Manual Captures/duplicate-b.md','same text')
  bad=self.put('01 Raw/Manual Captures/bad.md','failure fixture')
  target=self.repo/'content/02 Processed/Manual Captures/bad.md';target.mkdir(parents=True)
  source_hash=hashlib.sha256(food.read_bytes()).hexdigest()
  first=self.cli('engine.py','process',expect=1)
  self.assertEqual(first['new'],9);self.assertEqual(first['processed'],8);self.assertEqual(first['failed'],1)
  rows=self.state();self.assertEqual(rows['01 Raw/Manual Captures/bad.md']['status'],'error')
  self.assertEqual(rows['01 Raw/Telegram/photos/photo_1_0 - 20261018131500123.jpg']['capture_timestamp'],'2026-10-18T13:15:00.123')
  self.assertEqual(rows['01 Raw/Telegram/Lunch - 20261018120000000.md']['kind'],'food-entry')
  journal=self.repo/'content/03 Journal/Daily/2026-10-18.md'
  self.assertTrue(journal.exists())
  self.assertIn('food-entry',journal.read_text())
  self.assertIn('workout-entry',journal.read_text())
  self.assertIn('![[01 Raw/Telegram/photos/photo_1_0 - 20261018131500123.jpg]]',journal.read_text())
  image_record=self.repo/'content/02 Processed/Telegram/photos/photo_1_0 - 20261018131500123.jpg.md'
  self.assertIn('![[01 Raw/Telegram/photos/photo_1_0 - 20261018131500123.jpg]]',image_record.read_text())
  self.assertEqual(rows['01 Raw/Telegram/Gym - 20261018130000000.md']['kind'],'workout-entry')
  self.assertEqual(rows['01 Raw/OneNote/page.md']['source_id'],'onenote:page-123')
  self.assertEqual(rows['01 Raw/Manual Captures/duplicate-b.md']['duplicate_of'],'01 Raw/Manual Captures/duplicate-a.md')
  self.assertEqual(hashlib.sha256(food.read_bytes()).hexdigest(),source_hash)
  processed=self.repo/'content/02 Processed/YouTube Transcripts/video.md'
  self.assertIn('00:03:12',processed.read_text());self.assertIn('dQw4w9WgXcQ',processed.read_text())
  self.assertIn('[[01 Raw/YouTube Transcripts/video]]',processed.read_text())
  self.assertEqual(self.cli('engine.py','process')['processed'],0)
  self.assertEqual(journal.read_text().count('![[01 Raw/Telegram/photos/photo_1_0 - 20261018131500123.jpg]]'),1)
  target.rmdir();retry=self.cli('engine.py','retry');self.assertEqual(retry['processed'],1)
  old_output=food.read_text();food.write_text(old_output+'\nDinner: soup.')
  changed=self.cli('engine.py','process');self.assertEqual(changed['changed'],1);self.assertEqual(changed['processed'],1)
  history=self.state()['01 Raw/Telegram/Lunch - 20261018120000000.md']['history'];self.assertEqual(len(history),1)
  archives=list((self.repo/'content/10 Archive/Processed Versions').rglob('*.md'));self.assertEqual(len(archives),1)
  self.assertEqual(self.cli('engine.py','verify')['broken_outputs'],[])
  self.assertEqual(self.cli('engine.py','process')['hashed'],0)
  self.assertTrue((self.repo/'content/02 Processed/Telegram/_index.md').exists())
  self.assertEqual(self.state()['01 Raw/Web Clippings/article.md']['kind'],'web-clipping')
  self.assertIsNone(self.state()['01 Raw/Web Clippings/article.md'].get('capture_timestamp'))

 def test_reviewed_enrichment_preserves_provenance(self):
  self.put('01 Raw/OneNote/source.md','---\nonenote-id: source-42\n---\nThis page describes three ways to connect to the internet.')
  self.cli('engine.py','process')
  output=self.repo/'content/02 Processed/OneNote/source.md'
  original=output.read_text()
  rejected=subprocess.run([sys.executable,str(self.scripts/'enrich.py'),'01 Raw/OneNote/source.md'],cwd=self.repo,capture_output=True,text=True)
  self.assertNotEqual(rejected.returncode,0)
  edited=original.replace('enrichment_status: pending','enrichment_status: reviewed')
  edited+='\n## Reviewed synthesis\n\nThe source describes three connectivity choices. This note keeps the source link and avoids adding unsupported prices.\n'
  output.write_text(edited)
  accepted=self.cli('enrich.py','01 Raw/OneNote/source.md')
  self.assertTrue(accepted['changed'])
  self.assertEqual(self.cli('engine.py','verify')['broken_outputs'],[])
  self.assertEqual(self.cli('engine.py','process')['processed'],0)

 def test_image_embed_survives_reprocessing_without_duplicate_journal_entry(self):
  image=self.repo/'content/01 Raw/Telegram/photos/snapshot - 20261018131500123.jpg'
  image.write_bytes(b'first image')
  self.cli('engine.py','process')
  journal=self.repo/'content/03 Journal/Daily/2026-10-18.md'
  embed='![[01 Raw/Telegram/photos/snapshot - 20261018131500123.jpg]]'
  self.assertEqual(journal.read_text().count(embed),1)
  self.assertEqual(self.cli('engine.py','process')['processed'],0)
  self.assertEqual(journal.read_text().count(embed),1)
  image.write_bytes(b'changed image')
  self.assertEqual(self.cli('engine.py','process')['processed'],1)
  self.assertEqual(journal.read_text().count(embed),1)

 def test_manual_ingest_and_hinglish_staleness(self):
  external=self.repo/'clip.md';external.write_text('The source article explains pods.')
  imported=self.cli('ingest.py','--source','web','--file',external,'--url','https://example.com/article','--title','Pod article','--author','A. Writer')
  self.assertEqual(imported['status'],'imported')
  self.cli('engine.py','process')
  output=self.repo/'content/02 Processed/Web Clippings/clip.md';text=output.read_text();self.assertIn('https://example.com/article',text);self.assertIn('A. Writer',text)
  self.put('05 Knowledge/Kubernetes/Pods.md','---\ntitle: Pods\n---\nA pod runs containers.\n')
  prepared=self.cli('hinglish.py','prepare','05 Knowledge/Kubernetes/Pods.md')
  dest=self.repo/'content'/prepared['hinglish_path'];dest.parent.mkdir(parents=True,exist_ok=True)
  front={'title':'Pods in Hinglish','type':'hinglish-transcription','canonical_path':prepared['canonical'],'canonical_sha256':prepared['canonical_sha256'],'transcription_status':'current'}
  dest.write_text('---\n'+yaml.safe_dump(front)+'---\n\nPod containers ko ek saath run karta hai. [[05 Knowledge/Kubernetes/Pods]]\n')
  self.cli('hinglish.py','finalize','05 Knowledge/Kubernetes/Pods.md')
  self.assertEqual(self.cli('hinglish.py','check')['stale'],[])
  original=self.repo/'content/05 Knowledge/Kubernetes/Pods.md';original.write_text(original.read_text()+'\nNew English detail.\n')
  stale=self.cli('hinglish.py','check',expect=1)['stale'];self.assertEqual(stale,[prepared['hinglish_path']])
  self.assertIn('Read in Hinglish',original.read_text())

if __name__=='__main__':unittest.main()
