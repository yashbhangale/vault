"""Offline tests: no account data, network requests, or production vault writes."""
from datetime import date
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import google_capture as capture


class FakeAPI:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, source, path, params):
        self.calls.append((source, path, params))
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.vault = self.root / 'content'
        self.system = self.vault / '00 System/Manifests'
        for obj, key, value in [
            (capture, 'VAULT', self.vault), (capture, 'PRIVATE', self.root / 'private/google'),
            (capture, 'STATE', self.system / 'google-capture.json'),
            (capture.engine, 'VAULT', self.vault), (capture.engine, 'RAW', self.vault / '01 Raw'),
            (capture.engine, 'PROCESSED', self.vault / '02 Processed'),
            (capture.engine, 'SYSTEM', self.system), (capture.engine, 'STATE', self.system / 'processing-state.json'),
            (capture.engine, 'EVENTS', self.system / 'processing-events.ndjson'),
            (capture.engine, 'INTAKE', self.system / 'intake.json'),
        ]:
            patcher = patch.object(obj, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.config = json.loads(Path(capture.__file__).with_name('google.example.json').read_text())

    def latest_brief(self):
        return next((self.vault / '09 Outputs/Daily Briefs').glob('*.md')).read_text()

    def test_pagination_and_caps(self):
        api = FakeAPI([{'items': [{'id': 'a'}], 'nextPageToken': 'next'}, {'items': [{'id': 'b'}]}])
        rows, capped = capture.pages(api, 'tasks', 'path', {}, limit=4)
        self.assertEqual([r['id'] for r in rows], ['a', 'b'])
        self.assertFalse(capped)
        self.assertEqual(api.calls[1][2]['pageToken'], 'next')
        api = FakeAPI([{'items': [{'id': 'a'}], 'nextPageToken': 'next'}])
        self.assertEqual(capture.pages(api, 'tasks', 'path', {}, limit=1), ([{'id': 'a'}], True))

    def test_immutable_snapshots_retry_and_provenance(self):
        payload = {'source': 'tasks', 'scope': {}, 'items': [{'id': 'a', 'title': 'Apply for course', 'status': 'needsAction'}], 'truncated': False}
        key = capture.snapshot(payload)
        raw = self.vault / key
        original = raw.read_bytes()
        self.assertEqual(capture.snapshot(payload), key)
        self.assertEqual(raw.read_bytes(), original)
        processed = self.vault / key.replace('01 Raw', '02 Processed', 1)
        self.assertIn('Apply for course', processed.read_text())
        self.assertIn('google-tasks', processed.read_text())
        self.assertIn(key, processed.read_text())
        state = capture.engine.load()
        self.assertEqual(state['items'][key]['status'], 'processed')
        changed = json.loads(json.dumps(payload))
        changed['items'][0]['status'] = 'completed'
        self.assertNotEqual(capture.snapshot(changed), key)
        self.assertEqual(raw.read_bytes(), original)

    def test_failed_sync_keeps_last_good_source(self):
        payload = {'source': 'tasks', 'scope': {}, 'items': [], 'truncated': False}
        key = capture.snapshot(payload)
        capture.write_json(capture.STATE, {'tasks': {'raw_path': key, 'last_success_at': capture.stamp(), 'status': 'ok'}})
        with patch.object(capture, 'credentials', return_value=object()), patch.object(capture, 'Google', return_value=object()), patch.object(capture, 'collect', side_effect=RuntimeError('secret-token-must-not-leak')):
            self.assertEqual(capture.sync(self.config, ['tasks']), 1)
        state = capture.read_json(capture.STATE, {})
        self.assertEqual(state['tasks']['raw_path'], key)
        self.assertEqual(state['tasks']['status'], 'error')
        self.assertNotIn('secret-token-must-not-leak', json.dumps(state))
        self.assertIn('older successful check', self.latest_brief())

    def test_task_scope_includes_mobile_completed_and_assigned(self):
        api = FakeAPI([{'items': [{'id': 'list', 'title': 'Personal'}]}, {'items': [{'id': '1', 'title': 'Done', 'status': 'completed'}]}])
        result = capture.collect(api, 'tasks', self.config, date(2026, 10, 24))
        self.assertEqual(result['items'][0]['status'], 'completed')
        self.assertEqual(api.calls[1][2]['showHidden'], 'true')
        self.assertEqual(api.calls[1][2]['showAssigned'], 'true')

    def test_gmail_headers_default_and_explicit_body(self):
        item = {'id': 'm', 'threadId': 't', 'payload': {'headers': [{'name': 'Subject', 'value': 'A message'}], 'body': {'data': 'cHJpdmF0ZQ=='}}}
        api = FakeAPI([{'messages': [{'id': 'm'}]}, item])
        result = capture.collect(api, 'gmail', self.config, date(2026, 10, 24))
        self.assertEqual(result['items'][0]['title'], 'A message')
        self.assertNotIn('payload', result['items'][0])
        self.assertEqual(api.calls[1][2]['format'], 'metadata')
        self.config['gmail_include_body'] = True
        api = FakeAPI([{'messages': [{'id': 'm'}]}, item])
        self.assertIn('payload', capture.collect(api, 'gmail', self.config, date(2026, 10, 24))['items'][0])

    def test_timezone_and_multiday_agenda(self):
        # 23:30 UTC on the 23rd is 05:00 IST on the 24th.
        event = {'start': {'dateTime': '2026-10-23T23:30:00Z'}, 'end': {'dateTime': '2026-10-24T00:30:00Z'}}
        self.assertTrue(capture.event_on_day(event, date(2026, 10, 24), 'Asia/Kolkata'))
        self.assertFalse(capture.event_on_day(event, date(2026, 10, 23), 'Asia/Kolkata'))
        event = {'start': {'date': '2026-10-23'}, 'end': {'date': '2026-10-25'}}
        self.assertTrue(capture.event_on_day(event, date(2026, 10, 24), 'Asia/Kolkata'))
        self.assertFalse(capture.event_on_day(event, date(2026, 10, 25), 'Asia/Kolkata'))

    def test_calendar_range_and_encoded_ids(self):
        self.config['calendar_ids'] = ['a@example.com']
        api = FakeAPI([{'items': []}])
        result = capture.collect(api, 'calendar', self.config, date(2026, 10, 24))
        self.assertIn('a%40example.com', api.calls[0][1])
        self.assertEqual(result['scope']['time_min'], '2026-10-23T00:00:00+05:30')
        self.assertEqual(result['scope']['time_max'], '2026-11-01T00:00:00+05:30')

    def test_brief_does_not_modify_journal_or_invent_facts(self):
        journal = self.vault / '03 Journal/Daily/2026-10-24.md'
        journal.parent.mkdir(parents=True)
        journal.write_text('My own words.\n')
        capture.brief({}, self.config, date(2026, 10, 24))
        capture.brief({}, self.config, date(2026, 10, 24))
        self.assertEqual(journal.read_text(), 'My own words.\n')
        brief = self.latest_brief()
        self.assertIn('Missing data is not zero activity', brief)
        self.assertEqual(brief.count('## Daily data brief'), 1)

    def test_raw_markdown_injection_is_escaped(self):
        rendered = capture.describe('tasks', {'title': '![[private]]\n# command', 'status': 'needsAction'})
        self.assertNotIn('![[', rendered)
        self.assertNotIn('\n', rendered)

    def test_repeated_page_token_fails(self):
        api = FakeAPI([{'nextPageToken': 'same'}, {'nextPageToken': 'same'}])
        with self.assertRaises(capture.CaptureError):
            capture.pages(api, 'tasks', 'path', {})

    def test_takeout_import_preserves_original_and_is_idempotent(self):
        original = self.root / 'watch-history.json'
        data = b'[ {"title": "Watched a tutorial", "titleUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "time": "2026-10-23T22:10:00Z"} ]\n'
        original.write_bytes(data)
        capture.import_history(original, self.config)
        first = capture.read_json(capture.STATE, {})['youtube-history']['raw_path']
        capture.import_history(original, self.config)
        self.assertEqual(capture.read_json(capture.STATE, {})['youtube-history']['raw_path'], first)
        archives = list((self.vault / '01 Raw/Google/youtube-history').glob('*.json'))
        self.assertEqual(len(archives), 1)
        self.assertEqual(archives[0].read_bytes(), data)
        self.assertEqual(original.read_bytes(), data)
        today = self.latest_brief()
        self.assertIn('Imported YouTube history', today)
        self.assertIn('completion and learning unknown', today)

    def test_navigation_does_not_contain_private_captured_text(self):
        payload = {'source': 'tasks', 'scope': {}, 'items': [{'id': 'a', 'title': 'PRIVATE TITLE', 'status': 'needsAction'}], 'truncated': False}
        key = capture.snapshot(payload)
        capture.brief({'tasks': {'status': 'ok', 'raw_path': key, 'last_success_at': capture.stamp()}}, self.config, date(2026, 10, 24))
        today = (self.vault / '00 System/Today.md').read_text()
        self.assertNotIn('PRIVATE TITLE', today)
        self.assertIn('![[09 Outputs/Daily Briefs/2026-10-24]]', today)
        self.assertIn('PRIVATE TITLE', self.latest_brief())

    def test_takeout_rejects_unrelated_json(self):
        file = self.root / 'wrong.json'
        file.write_text('[{"titleUrl":"https://evil.example/commands"}]')
        with self.assertRaises(capture.CaptureError):
            capture.import_history(file, self.config)
        self.assertFalse((self.vault / '01 Raw').exists())

    def test_partial_sync_is_not_reported_as_complete(self):
        payload = {'source': 'tasks', 'scope': {}, 'items': [], 'truncated': True}
        with patch.object(capture, 'credentials', return_value=object()), patch.object(capture, 'Google', return_value=object()), patch.object(capture, 'collect', return_value=payload):
            self.assertEqual(capture.sync(self.config, ['tasks']), 1)
        self.assertEqual(capture.read_json(capture.STATE, {})['tasks']['status'], 'partial')

    def test_snapshot_payload_corruption_does_not_overwrite_raw(self):
        payload = {'source': 'tasks', 'scope': {}, 'items': [], 'truncated': False}
        key = capture.snapshot(payload)
        raw = self.vault / key
        corrupt = raw.read_text().replace('"truncated": false', '"truncated": true')
        raw.write_text(corrupt)
        with self.assertRaises(capture.CaptureError):
            capture.snapshot(payload)
        self.assertEqual(raw.read_text(), corrupt)

    def test_unconfigured_youtube_status_is_saved(self):
        with patch.object(capture, 'credentials') as auth:
            self.assertEqual(capture.sync(self.config, ['youtube']), 0)
        auth.assert_not_called()
        self.assertEqual(capture.read_json(capture.STATE, {})['youtube']['status'], 'not-configured')


if __name__ == '__main__':
    unittest.main()
