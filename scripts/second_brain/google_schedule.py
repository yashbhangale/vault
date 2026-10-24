#!/usr/bin/env python3
"""Install an hourly local systemd user timer after Google sign-in is ready."""
import argparse
from pathlib import Path
import subprocess
import sys
import google_capture as capture


def quoted(path):
    return '"' + str(path).replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%') + '"'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['install', 'status', 'disable'])
    args = parser.parse_args()
    if args.command == 'status':
        return subprocess.run(['systemctl', '--user', 'status', 'vault-google.timer', '--no-pager']).returncode
    if args.command == 'disable':
        return subprocess.run(['systemctl', '--user', 'disable', '--now', 'vault-google.timer']).returncode
    config = capture.configuration()
    if not capture.CLIENT.exists() or not capture.TOKEN.exists():
        parser.error('Complete Google OAuth sign-in before installing the timer')
    # Validate scopes/token refresh before starting unattended work.
    active = ['calendar', 'gmail', 'tasks'] + (['youtube'] if config['youtube_playlist_ids'] else [])
    capture.credentials(active)
    folder = Path.home() / '.config/systemd/user'
    folder.mkdir(parents=True, exist_ok=True)
    command = quoted(sys.executable) + ' ' + quoted(Path(capture.__file__).resolve()) + ' sync'
    index = quoted(sys.executable) + ' ' + quoted(Path(capture.__file__).with_name('search.py').resolve()) + ' index'
    capture.atomic(folder / 'vault-google.service', '[Unit]\nDescription=Private Google captures into Obsidian\n\n[Service]\nType=oneshot\n'
                   + 'ExecStart=' + command + '\nExecStartPost=' + index
                   + '\nUMask=0077\nTimeoutStartSec=45min\n')
    capture.atomic(folder / 'vault-google.timer', '[Unit]\nDescription=Hourly vault Google capture\n\n[Timer]\nOnCalendar=hourly\n'
                   'Persistent=true\nRandomizedDelaySec=120\n\n[Install]\nWantedBy=timers.target\n')
    subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', '--user', 'enable', '--now', 'vault-google.timer'], check=True)
    print('Hourly collector enabled. Runs while this computer and user service manager are available.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except capture.CaptureError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f'{type(exc).__name__}: timer setup failed; check Google sign-in and systemd user service availability.', file=sys.stderr)
        sys.exit(1)
