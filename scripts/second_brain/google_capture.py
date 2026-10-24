#!/usr/bin/env python3
"""Read-only Google collectors. Credentials and captures stay on this machine.

No LLM, hosted workflow service, Google writes, or external telemetry. Google
receives only OAuth requests and the API queries needed to read the account.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import quote
from zoneinfo import ZoneInfo

import yaml
import engine

ROOT = engine.REPO
VAULT = engine.VAULT
PRIVATE = ROOT / 'private/google'
CONFIG = PRIVATE / 'config.json'
TOKEN = PRIVATE / 'token.json'
CLIENT = PRIVATE / 'client-secret.json'
STATE = engine.SYSTEM / 'google-capture.json'
SOURCES = ('calendar', 'gmail', 'tasks', 'youtube')
SCOPES = {
    'calendar': 'https://www.googleapis.com/auth/calendar.events.readonly',
    'gmail': 'https://www.googleapis.com/auth/gmail.readonly',
    'tasks': 'https://www.googleapis.com/auth/tasks.readonly',
    'youtube': 'https://www.googleapis.com/auth/youtube.readonly',
}
BASES = {
    'calendar': 'https://www.googleapis.com/calendar/v3/',
    'gmail': 'https://gmail.googleapis.com/gmail/v1/users/me/',
    'tasks': 'https://tasks.googleapis.com/tasks/v1/',
    'youtube': 'https://www.googleapis.com/youtube/v3/',
}


class CaptureError(RuntimeError):
    """Safe diagnostic text authored by this collector, never by remote data."""


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, value):
    atomic(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


@contextmanager
def lock():
    PRIVATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (PRIVATE / 'capture.lock').open('a') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise CaptureError('A Google capture is already running') from None
        yield


def configuration():
    if not CONFIG.exists():
        raise CaptureError('Run google_capture.py init first')
    config = read_json(CONFIG, {})
    ZoneInfo(config['timezone'])
    limit = config.get('max_items_per_collection', 1000)
    if type(limit) is not int or not 1 <= limit <= 10000:
        raise ValueError('max_items_per_collection must be between 1 and 10000')
    days = config.get('calendar_days_ahead', 7)
    if type(days) is not int or not 1 <= days <= 90:
        raise ValueError('calendar_days_ahead must be between 1 and 90')
    for key in ('calendar_ids', 'youtube_playlist_ids'):
        if not isinstance(config.get(key), list) or not all(isinstance(x, str) and x for x in config[key]):
            raise ValueError(key + ' must be a list of nonempty IDs')
    if not config['calendar_ids']:
        raise ValueError('Choose at least one calendar ID')
    if any(x in ('HL', 'WL') for x in config['youtube_playlist_ids']):
        raise ValueError('Watch History and Watch Later cannot be read through the YouTube API')
    if not isinstance(config.get('gmail_query'), str) or not config['gmail_query'].strip():
        raise ValueError('gmail_query must be a nonempty Gmail search expression')
    if type(config.get('gmail_include_body', False)) is not bool:
        raise ValueError('gmail_include_body must be true or false')
    return config


def credentials(sources, interactive=False):
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise CaptureError('Install scripts/second_brain/requirements-google.txt in .venv') from None
    scopes = [SCOPES[source] for source in sources]
    creds = Credentials.from_authorized_user_file(str(TOKEN)) if TOKEN.exists() else None
    if creds and not creds.has_scopes(scopes):
        if not interactive:
            raise CaptureError('Missing read scopes; rerun auth for the desired sources')
        creds = None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not interactive:
            raise CaptureError('Google sign-in required; run google_capture.py auth')
        if not CLIENT.exists():
            raise CaptureError('Save your Desktop OAuth client JSON as private/google/client-secret.json')
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), scopes)
        creds = flow.run_local_server(host='127.0.0.1', port=0, timeout_seconds=180,
                                      prompt='consent', access_type='offline')
    atomic(TOKEN, creds.to_json())
    os.chmod(TOKEN, 0o600)
    return creds


class Google:
    def __init__(self, creds):
        from google.auth.transport.requests import AuthorizedSession
        self.session = AuthorizedSession(creds)

    def get(self, source, path, params):
        response = self.session.get(BASES[source] + path, params=params, timeout=45)
        if not response.ok:
            # Do not log response bodies, URLs, queries, or access tokens.
            raise CaptureError(f'{source}: HTTP {response.status_code}; check API enablement, consent, and quota')
        return response.json()


def pages(api, source, path, params, key='items', limit=1000):
    """Paginate to an explicit cap. A capped fetch is never reported as complete."""
    rows, token, seen = [], None, set()
    while True:
        query = dict(params)
        if token:
            query['pageToken'] = token
        result = api.get(source, path, query)
        batch = result.get(key, [])
        remaining = limit - len(rows)
        rows.extend(batch[:remaining])
        token = result.get('nextPageToken')
        if len(batch) > remaining or (token and len(rows) >= limit):
            return rows, True
        if not token:
            return rows, False
        if token in seen:
            raise CaptureError(f'{source}: repeated pagination token')
        seen.add(token)


def collect(api, source, config, today):
    limit = config['max_items_per_collection']
    rows, capped = [], False
    if source == 'calendar':
        tz = ZoneInfo(config['timezone'])
        start = datetime.combine(today - timedelta(days=1), time.min, tz)
        end = datetime.combine(today + timedelta(days=config['calendar_days_ahead'] + 1), time.min, tz)
        scope = {'calendar_ids': config['calendar_ids'], 'time_min': start.isoformat(), 'time_max': end.isoformat()}
        for calendar in config['calendar_ids']:
            items, truncated = pages(api, source, 'calendars/' + quote(calendar, safe='') + '/events', {
                'timeMin': scope['time_min'], 'timeMax': scope['time_max'],
                'singleEvents': 'true', 'orderBy': 'startTime', 'maxResults': 2500,
                'timeZone': config['timezone'], 'showDeleted': 'false',
            }, limit=limit)
            capped |= truncated
            for item in items:
                if item.get('status') == 'cancelled':
                    continue
                rows.append({k: item[k] for k in ('id', 'summary', 'start', 'end', 'status', 'htmlLink', 'description', 'location', 'updated') if k in item} | {'calendar_id': calendar})
    elif source == 'gmail':
        scope = {'query': config['gmail_query'], 'include_body': config.get('gmail_include_body', False)}
        messages, capped = pages(api, source, 'messages', {'q': scope['query'], 'maxResults': 500}, key='messages', limit=limit)
        for message in messages:
            params = {'format': 'full' if scope['include_body'] else 'metadata'}
            if not scope['include_body']:
                params['metadataHeaders'] = ['Subject', 'From', 'To', 'Date']
            item = api.get(source, 'messages/' + quote(message['id'], safe=''), params)
            headers = {h['name'].lower(): h['value'] for h in item.get('payload', {}).get('headers', [])}
            row = {k: item[k] for k in ('id', 'threadId', 'labelIds', 'internalDate', 'snippet') if k in item}
            row.update({'title': headers.get('subject', '(no subject)'), 'from': headers.get('from'), 'date_header': headers.get('date')})
            if scope['include_body']:
                # API payload, including base64url MIME parts; no attachment downloads.
                row['payload'] = item.get('payload', {})
            rows.append(row)
    elif source == 'tasks':
        scope = {'show_completed': True, 'show_hidden': True, 'show_assigned': True, 'show_deleted': False}
        lists, capped = pages(api, source, 'users/@me/lists', {'maxResults': 1000}, limit=limit)
        for tasklist in lists:
            items, truncated = pages(api, source, 'lists/' + quote(tasklist['id'], safe='') + '/tasks', {
                'maxResults': 100, 'showCompleted': 'true', 'showHidden': 'true', 'showAssigned': 'true', 'showDeleted': 'false',
            }, limit=limit)
            capped |= truncated
            for item in items:
                rows.append({k: item[k] for k in ('id', 'title', 'notes', 'status', 'due', 'completed', 'updated', 'parent', 'links', 'webViewLink') if k in item} | {'list_id': tasklist['id'], 'list_title': tasklist.get('title')})
    else:
        scope = {'playlist_ids': config['youtube_playlist_ids'], 'meaning': 'saved playlist membership; not watch history'}
        for playlist in config['youtube_playlist_ids']:
            items, truncated = pages(api, source, 'playlistItems', {'playlistId': playlist, 'part': 'snippet,contentDetails', 'maxResults': 50}, limit=limit)
            capped |= truncated
            for item in items:
                snippet = item.get('snippet', {})
                rows.append({'id': item['id'], 'playlist_id': playlist, 'title': snippet.get('title'),
                             'video_id': item.get('contentDetails', {}).get('videoId'),
                             'added_at': snippet.get('publishedAt'), 'channel': snippet.get('videoOwnerChannelTitle')})
    rows.sort(key=lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False))
    return {'source': source, 'scope': scope, 'items': rows, 'truncated': capped}


def clean(value):
    # Remote text is data, never instructions or executable Markdown.
    text = re.sub(r'\s+', ' ', str(value or ''))
    return re.sub(r'([\\`*_<>{}\[\]#|!])', r'\\\1', text)


def describe(source, row):
    title = clean(row.get('summary') or row.get('title') or '(untitled)')
    if source == 'calendar':
        start = row.get('start', {})
        return f"{clean(start.get('dateTime') or start.get('date'))} — {title} (scheduled; attendance unknown)"
    if source == 'gmail':
        reference = quote(str(row.get('threadId') or row.get('id') or ''), safe='')
        return f"{title} — {clean(row.get('from'))} — {clean(row.get('snippet'))} [Open Gmail](https://mail.google.com/mail/#all/{reference})"
    if source == 'tasks':
        return f"{title} — {clean(row.get('status'))}; due {clean((row.get('due') or '')[:10]) or 'not supplied'}"
    if source == 'youtube-history':
        return f"{clean(row.get('time'))} — {title} — history entry; completion and learning unknown; {clean(row.get('url'))}"
    video = str(row.get('video_id') or '')
    reference = f' [Open video](https://www.youtube.com/watch?v={video})' if engine.VIDEO_ID.fullmatch(video) else ''
    return f"{title} — saved in playlist; video ID {clean(video)}{reference}"


def snapshot(payload):
    """Content-addressed immutable source; failed/repeated imports are recoverable."""
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    sha = hashlib.sha256(canonical.encode()).hexdigest()
    source = payload['source']
    relative = Path('01 Raw/Google') / source / (sha + '.md')
    path = VAULT / relative
    captured = stamp()
    if not path.exists():
        meta = {'title': f'Google {source} snapshot', 'type': 'google-snapshot', 'source': 'google-' + source,
                'captured': captured, 'publish': False, 'payload_sha256': sha}
        body = '\n'.join('- ' + describe(source, row) for row in payload['items']) or 'No records returned within this scope.'
        text = '---\n' + yaml.safe_dump(meta, sort_keys=False) + '---\n\n# Captured records\n\n' + body
        text += '\n\n<!-- payload -->\n```json\n' + json.dumps(payload, ensure_ascii=False, indent=2) + '\n```\n'
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents rewriting any archived source.
        with path.open('x', encoding='utf-8') as stream:
            stream.write(text)
    existing = path.read_text()
    if extract_payload(existing) != payload:
        raise CaptureError('Raw snapshot collision or corruption; preserve source and investigate')
    intake = engine.intake()
    key = relative.as_posix()
    if key not in intake:
        meta, _ = engine.frontmatter(existing)
        intake[key] = {'source': 'google-' + source, 'captured': meta['captured'],
                       'import_timestamp': captured, 'original_filename': path.name}
        write_json(engine.INTAKE, intake)
        engine.event('google-captured', raw=key, payload_sha256=sha, source=source)
    # Only process this collector's file; do not sweep unrelated pending captures.
    state = engine.load()
    pending, _ = engine.discover(state, selected=key)
    _, failed = engine.process(state, pending)
    engine.save(state)
    if failed:
        raise CaptureError('Capture preserved; processing failed. Inspect processing manifest and retry')
    return key


def extract_payload(text):
    marker = '\n<!-- payload -->\n```json\n'
    return json.loads(text.split(marker, 1)[1].rsplit('\n```', 1)[0])


def load_payload(row):
    relative = row.get('raw_path')
    if not relative:
        return None
    path = (VAULT / relative).resolve()
    if not path.is_relative_to((VAULT / '01 Raw/Google').resolve()):
        raise ValueError('Unexpected snapshot location')
    return extract_payload(path.read_text())


def render_brief(state, config, day):
    """Deterministic evidence view; does not infer priorities or completed activity."""
    lines = ['## Daily data brief', '', f'For {day.isoformat()} · {config["timezone"]}', '',
             'Choose your top three actions in your own daily note. These are source observations, not an AI plan.', '',
             '### Capture health', '', '| Source | State | Last successful check (UTC) |', '| --- | --- | --- |']
    sources = list(SOURCES) + (['youtube-history'] if 'youtube-history' in state else [])
    for source in sources:
        row = state.get(source, {})
        status = row.get('status', 'not-connected')
        success = row.get('last_success_at')
        if success and source != 'youtube-history' and datetime.now(timezone.utc) - datetime.fromisoformat(success) > timedelta(hours=2):
            status += '; stale (>2h)'
        lines.append(f'| {source} | {clean(status)} | {clean(success) or "never"} |')
    for source in sources:
        if state.get(source, {}).get('error'):
            lines.append(f'\n- {source}: {clean(state[source]["error"])}')
    for source in sources:
        row = state.get(source, {})
        payload = load_payload(row)
        lines += ['', '### ' + {'calendar': 'Agenda', 'gmail': 'Email to review', 'tasks': 'Open tasks', 'youtube': 'Saved YouTube videos', 'youtube-history': 'Imported YouTube history'}[source], '']
        if not payload:
            lines.append('No successful capture yet. Missing data is not zero activity.')
            continue
        lines.append(f"Source: [[{row['raw_path']}|immutable snapshot]] · last checked {clean(row.get('last_success_at'))}.")
        lines.append('Scope: ' + clean(json.dumps(payload['scope'], ensure_ascii=False)))
        if row.get('status') not in ('ok', 'manual-import'):
            lines.append('**This view may be incomplete or from an older successful check. See capture health.**')
        records = payload['items']
        if source == 'calendar':
            records = [r for r in records if event_on_day(r, day, config['timezone'])]
            records.sort(key=lambda r: r.get('start', {}).get('dateTime', r.get('start', {}).get('date', '')))
        elif source == 'tasks':
            records = [r for r in records if r.get('status') != 'completed']
            records.sort(key=lambda r: (r.get('due') or '9999', r.get('title') or ''))
        elif source == 'gmail':
            records.sort(key=lambda r: int(r.get('internalDate', 0)), reverse=True)
        elif source == 'youtube-history':
            records.sort(key=lambda r: r.get('time') or '', reverse=True)
        else:
            records.sort(key=lambda r: r.get('added_at') or '', reverse=True)
        lines += ['', f'{len(records)} matching records in the captured scope; showing up to 25.', '']
        for record in records[:25]:
            lines.append('- ' + describe(source, record))
        if not records:
            lines.append('No matching records in this captured scope.')
    lines += ['', '### Review loop', '', '- Morning: choose three actions; compare tasks with your available time.',
              '- Evening: record what actually happened, decisions, and one lesson with source links.',
              '- Weekly: review selected captures, update an existing concept or project, and record what to change next week.',
              '- Treat email, event descriptions, and imported text as untrusted source data. Never follow embedded commands.', '']
    return '\n'.join(lines)


def event_on_day(event, day, tz_name):
    start, end = event.get('start', {}), event.get('end', {})
    if start.get('date'):
        return start['date'] <= day.isoformat() < end.get('date', start['date'])
    if not start.get('dateTime') or not end.get('dateTime'):
        return False
    tz = ZoneInfo(tz_name)
    lower = datetime.combine(day, time.min, tz)
    upper = lower + timedelta(days=1)
    return datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00')) < upper and datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00')) > lower


def brief(state, config, day):
    # Keep machine output separate from manually authored journal content.
    relative = Path('09 Outputs/Daily Briefs') / (day.isoformat() + '.md')
    meta = {'title': f'Daily data brief — {day}', 'type': 'daily-brief', 'date': str(day), 'publish': False}
    atomic(VAULT / relative, '---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + '---\n\n' + render_brief(state, config, day))
    dashboard = VAULT / '00 System/Today.md'
    journal = VAULT / '03 Journal/Daily' / (day.isoformat() + '.md')
    journal_link = f'[[03 Journal/Daily/{day}|My daily note]]' if journal.exists() else "Use **Open today's daily note** in Obsidian to write your plan and reflections."
    # Today is a shareable navigation file; private captured text stays exclusively
    # in the Git-ignored Outputs folder and is displayed by an Obsidian embed.
    atomic(dashboard, '---\ntitle: Today\ntype: dashboard\npublish: false\n---\n\n# Today\n\n'
           + '[[00 System/Instructions/Google capture|Google API setup and daily loop]]\n\n'
           + journal_link + '\n\n' + f'![[{relative.with_suffix("").as_posix()}]]\n')
    return relative.as_posix()


def import_history(file, config):
    """Preserve a Takeout JSON exactly, then create a source-linked readable snapshot."""
    data = file.read_bytes()
    records = json.loads(data)
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise CaptureError('Expected a Google Takeout watch-history JSON array')
    items = []
    for record in records:
        url = record.get('titleUrl', '')
        # Takeout includes deleted/unavailable entries without a URL; preserve those too.
        if url and not engine.video_id(url):
            raise CaptureError('History contains a non-YouTube video URL; select only watch-history.json')
        items.append({'title': record.get('title'), 'url': url, 'time': record.get('time')})
    sha = hashlib.sha256(data).hexdigest()
    original = VAULT / '01 Raw/Google/youtube-history' / (sha + '.json')
    original.parent.mkdir(parents=True, exist_ok=True)
    if not original.exists():
        with original.open('xb') as stream:
            stream.write(data)
    if hashlib.sha256(original.read_bytes()).hexdigest() != sha:
        raise CaptureError('Export archive hash mismatch; preserve files and investigate')
    intake = engine.intake()
    rel = original.relative_to(VAULT).as_posix()
    if rel not in intake:
        intake[rel] = {'source': 'google-youtube-history', 'original_filename': file.name, 'import_timestamp': stamp()}
        write_json(engine.INTAKE, intake)
        engine.event('google-history-import', raw=rel, sha256=sha)
    state = engine.load()
    pending, _ = engine.discover(state, selected=rel)
    _, failed = engine.process(state, pending)
    engine.save(state)
    if failed:
        raise CaptureError('Original export preserved; processing failed. Inspect processing manifest')
    payload = {'source': 'youtube-history', 'scope': {'original_export': rel, 'original_sha256': sha,
               'meaning': 'manual Takeout export; no live watch tracking; no completion inference'},
               'items': sorted(items, key=lambda r: json.dumps(r, sort_keys=True)), 'truncated': False}
    key = snapshot(payload)
    capture_state = read_json(STATE, {})
    capture_state['youtube-history'] = {'status': 'manual-import', 'raw_path': key, 'last_success_at': stamp(), 'count': len(items)}
    write_json(STATE, capture_state)
    brief(capture_state, config, datetime.now(ZoneInfo(config['timezone'])).date())
    print(json.dumps({'imported': len(items), 'original_export': rel, 'snapshot': key}))


def sync(config, sources):
    today = datetime.now(ZoneInfo(config['timezone'])).date()
    state = read_json(STATE, {})
    failures = 0
    api = None
    auth_error = None
    active = [s for s in sources if s != 'youtube' or config['youtube_playlist_ids']]
    if active:
        try:
            api = Google(credentials(active))
        except Exception as exc:
            auth_error = str(exc) if isinstance(exc, CaptureError) else 'Sign-in or token refresh failed; run auth and check local setup'
    for source in sources:
        row = state.setdefault(source, {})
        row['last_attempt_at'] = stamp()
        if source == 'youtube' and not config['youtube_playlist_ids']:
            row.update(status='not-configured', error='Add an ordinary learning playlist ID to config.json')
            write_json(STATE, state)
            continue
        try:
            if auth_error:
                raise CaptureError(auth_error)
            payload = collect(api, source, config, today)
            key = snapshot(payload)
            row.update(status='partial' if payload['truncated'] else 'ok', raw_path=key,
                       last_success_at=stamp(), count=len(payload['items']), error=None)
            if payload['truncated']:
                failures += 1
            engine.event('google-sync', source=source, raw=key, status=row['status'], count=row['count'])
        except Exception as exc:
            # Preserve last good capture. Class-only diagnostics avoid accidental private data in logs.
            message = str(exc) if isinstance(exc, CaptureError) else f'{type(exc).__name__}: capture failed; check sign-in, API configuration, and processing manifest'
            row.update(status='error', error=message)
            failures += 1
            engine.event('google-sync-error', source=source, error_type=type(exc).__name__)
        write_json(STATE, state)
    output = brief(state, config, today)
    print(json.dumps({'brief': output, 'sources': {s: state[s]['status'] for s in sources}, 'failures': failures}))
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'auth', 'sync', 'brief', 'status', 'import-history'])
    parser.add_argument('--file', type=Path, help='Google Takeout watch-history.json, used only by import-history')
    parser.add_argument('--sources', nargs='+', choices=SOURCES, default=list(SOURCES))
    args = parser.parse_args()
    try:
        with lock():
            if args.command == 'init':
                if not CONFIG.exists():
                    shutil.copyfile(Path(__file__).with_name('google.example.json'), CONFIG)
                    os.chmod(CONFIG, 0o600)
                print('Local config ready: private/google/config.json. Next: save Desktop OAuth client JSON, then run auth.')
                return 0
            config = configuration()
            if args.command == 'auth':
                credentials(args.sources, interactive=True)
                print('Read-only Google authorization saved locally. Next: sync.')
            elif args.command == 'status':
                state = read_json(STATE, {})
                print(json.dumps({'oauth_client_present': CLIENT.exists(), 'token_present': TOKEN.exists(),
                                  'sources': {s: state.get(s, {}).get('status', 'not-connected') for s in SOURCES}}, indent=2))
            elif args.command == 'import-history':
                if not args.file or not args.file.is_file():
                    raise CaptureError('Supply --file /path/to/watch-history.json')
                import_history(args.file, config)
            elif args.command == 'brief':
                print(brief(read_json(STATE, {}), config, datetime.now(ZoneInfo(config['timezone'])).date()))
            else:
                return sync(config, args.sources)
        return 0
    except Exception as exc:
        # Auth libraries may embed tokens in exceptions: never print their text.
        message = str(exc) if isinstance(exc, CaptureError) else f'{type(exc).__name__}: operation failed. Check the local setup guide and capture status.'
        print(message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
