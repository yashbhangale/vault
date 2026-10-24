---
title: Web workspace
type: guide
publish: false
---

# Open your full vault in a browser

The browser workspace supports owner-only Google sign-in behind an HTTPS Cloudflare Tunnel. Its intended address is `https://workspace.yashbhangale.site/`; this address becomes usable after the Web OAuth client and tunnel are configured. The vault and existing read-only Google sync credentials stay on this laptop. The workspace is available from other devices while this laptop is awake, online, and running both services. GitHub Pages continues to contain only the filtered public Quartz build.

The workspace runs as the `vault-dashboard.service` systemd user service and starts with this computer's user services. It reads vault files directly and checks for new capture data every minute; a Quartz rebuild is not required to see new captures.

## Use the workspace

- **Today:** scheduled events for the local day, open tasks, source health and recent notes. Plans and completed activity stay distinct.
- **All notes:** browse all eleven vault areas or search filenames and Markdown content. Filters include Raw, Processed, Journal, Projects, Knowledge, Resources and Archive. Internal credential folders, manifests, hidden files and symlink escapes are excluded.
- **Calendar / Tasks / Mail / Saved videos:** filter source records, follow original app links and inspect the immutable source snapshot. Source reads retain their configured windows. Mail currently captures headers and snippets; playlist entries are not watch history.
- **Journal:** read existing daily notes. Use Quick capture to record a new thought, or keep writing in Obsidian.
- **Reader:** rendered Markdown, tables, code, source links, inline vault images and original-file downloads. Audio and video have native browser players when the format is supported. Unavailable or ambiguous wikilinks are labelled. Note embeds open as links. PDFs and other attachments can be downloaded. Excalidraw remains its Markdown/source representation.
- **Quick capture:** save text or a link as a new immutable Manual Capture, then run the existing provenance-aware processor and search indexer. Failed actions retain the draft in the page; ingestion runs under the Google collector's lock.
- **Sync & sources:** refresh one source or all four, inspect capture status, and pause or resume the existing hourly timer. These actions run fixed local commands; imported content cannot supply commands. Google access remains read-only. Use the original Google apps to edit events, send mail or complete tasks.

In online mode, “Open Quartz knowledge site” opens [the public knowledge site](https://notes.yashbhangale.site/). Without online configuration, the workspace uses [the local Quartz preview](http://127.0.0.1:4174/vault/). Each runs on a separate origin from the private API.

## Start and maintain

```sh
# Manual local start (stop the service first if it is already running)
npm run dashboard

# Manual online start with private configuration
node --env-file=private/dashboard/online.env scripts/dashboard/server.mjs

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

## Owner-only online setup

Create a Google OAuth client of type **Web application**, separate from the Desktop client used by the read-only collector. Register exactly `https://workspace.yashbhangale.site/auth/callback` as its redirect URI. Download the JSON into `private/dashboard/google-web-client.json`; keep the directory mode `700` and files mode `600`. Never paste credentials into notes, chat, or Git.

Create `private/dashboard/online.env` locally with these non-secret settings (the JSON path points to the secret file):

```sh
VAULT_DASHBOARD_ORIGIN=https://workspace.yashbhangale.site
VAULT_GOOGLE_WEB_CLIENT=/home/yash/vault/private/dashboard/google-web-client.json
VAULT_DASHBOARD_OWNER=yashbhangale9@gmail.com
```

The service installer reads that optional environment file. Partial or invalid online configuration prevents the app from starting. Online mode accepts only its configured public Host header; a loopback URL is no longer the user-facing address. Every workspace page, file, and API requires a session. Google sign-in requests only `openid email`, uses state, nonce and PKCE, verifies Google's signed identity token, and permits only the configured verified owner email. Sessions expire after eight hours or on sign-out; restarting the server also ends sessions. Cookies are Secure, HttpOnly and SameSite=Lax.

Install the official `cloudflared` executable at `~/.local/bin/cloudflared` and create a dedicated named tunnel. Store its credentials and ingress YAML under `private/dashboard/`. The only ingress hostname should map `workspace.yashbhangale.site` to `http://127.0.0.1:4173`, followed by a `http_status:404` catch-all. Do not share the tunnel with unrelated ingress configurations. Authenticate the backend before adding its public DNS route.

```sh
node scripts/dashboard/service.mjs install
node scripts/dashboard/tunnel-service.mjs install
systemctl --user is-active vault-dashboard.service vault-workspace-tunnel.service
journalctl --user -u vault-workspace-tunnel.service -n 30 --no-pager

# Disconnect remote access while keeping local capture running
node scripts/dashboard/tunnel-service.mjs disable
```

A Cloudflare tunnel transports owner-authenticated browser responses; it does not upload a copy of the vault or Google's collector token to the homelab. Cloudflare terminates HTTPS as the site's hosting proxy. Never publish the private folders into Quartz's static build. Local mode without online configuration remains a convenience interface for this computer and does not authenticate local processes.

## Verification

```sh
npm run dashboard:test
.venv/bin/python -m unittest discover -s scripts/second_brain -p 'test_*.py'
.venv/bin/python scripts/second_brain/engine.py verify
npm run build
```

Relevant implementation: `scripts/dashboard/server.mjs`, `vault.mjs`, `ui/`, `google-login.mjs`, `service.mjs`, `tunnel-service.mjs`, and `scripts/second_brain/capture_local.py`. Google setup remains in [[00 System/Instructions/Google capture]].
