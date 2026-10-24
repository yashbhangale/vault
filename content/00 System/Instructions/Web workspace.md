---
title: Local web workspace
type: guide
publish: false
---

# Open your full vault in a browser

Open [Yash’s workspace](http://127.0.0.1:4173/) on this computer. Authentication was explicitly deferred. The server binds only to `127.0.0.1`; it is not an internet-facing site. The existing GitHub Pages deployment still contains only the filtered public Quartz build. No private data or credentials were uploaded.

The workspace runs as the `vault-dashboard.service` systemd user service and starts with this computer's user services. It reads vault files directly and checks for new capture data every minute; a Quartz rebuild is not required to see new captures.

## Use the workspace

- **Today:** scheduled events for the local day, open tasks, source health and recent notes. Plans and completed activity stay distinct.
- **All notes:** browse all eleven vault areas or search filenames and Markdown content. Filters include Raw, Processed, Journal, Projects, Knowledge, Resources and Archive. Internal credential folders, manifests, hidden files and symlink escapes are excluded.
- **Calendar / Tasks / Mail / Saved videos:** filter source records, follow original app links and inspect the immutable source snapshot. Source reads retain their configured windows. Mail currently captures headers and snippets; playlist entries are not watch history.
- **Journal:** read existing daily notes. Use Quick capture to record a new thought, or keep writing in Obsidian.
- **Reader:** rendered Markdown, tables, code, source links, inline vault images and original-file downloads. Audio and video have native browser players when the format is supported. Unavailable or ambiguous wikilinks are labelled. Note embeds open as links. PDFs and other attachments can be downloaded. Excalidraw remains its Markdown/source representation.
- **Quick capture:** save text or a link as a new immutable Manual Capture, then run the existing provenance-aware processor and search indexer. Failed actions retain the draft in the page; ingestion runs under the Google collector's lock.
- **Sync & sources:** refresh one source or all four, inspect capture status, and pause or resume the existing hourly timer. These actions run fixed local commands; imported content cannot supply commands. Google access remains read-only. Use the original Google apps to edit events, send mail or complete tasks.

The existing Quartz site opens from the workspace on [its local preview](http://127.0.0.1:4174/vault/). It runs on a separate browser origin, so its scripts cannot read the private workspace API. The Quartz homepage links back to the local workspace. On another person's computer, that loopback link addresses their computer, not yours.

## Start and maintain

```sh
# Manual start (stop the service first if it is already running)
npm run dashboard

# Install/start with this user's services
node scripts/dashboard/service.mjs install

# Inspect or stop automatic startup
node scripts/dashboard/service.mjs status
node scripts/dashboard/service.mjs disable

# Restart after editing backend code
systemctl --user restart vault-dashboard.service

# Review operational logs
journalctl --user -u vault-dashboard.service -n 30 --no-pager
```

Ports default to `4173` for private workspace and `4174` for the isolated Quartz preview. Manual launches can override them with `VAULT_DASHBOARD_PORT` and `VAULT_QUARTZ_PORT`. Neither listener accepts connections on external network interfaces.

Browser actions require the current page's action token and same-origin request headers. The server rejects unexpected Host headers, cross-site requests, path traversal and credential/manifests access. Raw HTML in Markdown is displayed as text. Executable attachments, including SVG and HTML, download rather than run in the private reader. The public Quartz preview only serves `public/`.

This is a local convenience interface without user authentication, not a security boundary against other users or processes on this computer. Hosting the complete vault online requires a server with actual authentication and HTTPS; do not expose these ports publicly or copy private folders into the public Quartz build.

## Verification

```sh
npm run dashboard:test
.venv/bin/python -m unittest discover -s scripts/second_brain -p 'test_*.py'
.venv/bin/python scripts/second_brain/engine.py verify
npm run build
```

Relevant implementation: `scripts/dashboard/server.mjs`, `vault.mjs`, `ui/`, `service.mjs`, and `scripts/second_brain/capture_local.py`. Google setup remains in [[00 System/Instructions/Google capture]].
