# Yash's Obsidian second brain

Open [`content/`](content/) as the Obsidian vault. The same Markdown publishes selected Knowledge, Projects, and Resources through Quartz. Local Raw, Processed, Journal, Trackers, Areas, career resources, Outputs, Archive, and System material stays out of the website. Private layers and processing manifests are ignored by Git; keep a separate trusted backup or private sync for them.

The vault has three working layers: [`01 Raw/`](content/01%20Raw/) holds originals, [`02 Processed/`](content/02%20Processed/) holds source-linked structured records, and [`05 Knowledge/`](content/05%20Knowledge/) holds maintained knowledge. Journal, Trackers, Projects, Areas, Resources, Outputs, and Archive each have a dedicated folder. The [architecture guide](<content/00 System/Instructions/Architecture.md>) and [workflows](<content/00 System/Instructions/Workflows.md>) explain the roles and metadata. Root [`AGENTS.md`](AGENTS.md) gives Codex the operating rules.

Images appear inline in processed image records and dated Telegram journal entries using Obsidian embeds (`![[01 Raw/.../image.jpg]]`). The original file remains in Raw; a plain image link alone does not satisfy the note format.

```sh
python3 scripts/second_brain/engine.py discover   # New/changed raw files, no output writes
python3 scripts/second_brain/engine.py process    # Structure only eligible files
python3 scripts/second_brain/engine.py retry      # Retry failed items
python3 scripts/second_brain/engine.py verify     # Verify processed output hashes
python3 scripts/second_brain/enrich.py '01 Raw/OneNote/page.md' # Accept a reviewed edit
python3 scripts/second_brain/audit.py             # Link and metadata report
python3 scripts/second_brain/search.py index      # Incremental local search index
python3 scripts/second_brain/search.py query Kubernetes
python3 scripts/second_brain/review.py weekly
python3 scripts/second_brain/hinglish.py prepare '05 Knowledge/Cloud and DevOps/DevOps.md'
npm run build                                 # Refresh public topic indexes and build Quartz
```

For a new web clipping or YouTube transcript, use [`ingest.py`](scripts/second_brain/ingest.py) to copy the original into Raw with the URL and available metadata. See [integration findings](<content/00 System/Instructions/Integrations.md>). Telegram and OneNote destination settings were updated locally; restart Obsidian before testing new deliveries. The processor does not download, transcribe audio, OCR images, or invent summaries. Its structured records expose a clear pending-synthesis field for targeted Codex review.

An unchanged processing run stats files without reading their content; it hashes new or changed candidates. The compact state is in `content/00 System/Manifests/processing-state.json`, and events append to `processing-events.ndjson`. Bulk migration used a verified, local recovery archive in `.recovery/` and recorded a hash-based move plan in the manifests folder. `reports/second-brain-audit.json` contains unresolved links and duplicate candidates. There are older missing-note placeholders and missing attachments; the audit keeps them visible instead of creating false content.

Codex has a daily intake heartbeat and a Sunday weekly-review heartbeat attached to this chat. They need the local computer and desktop app running to access this vault. They stay quiet while there is no new work or actionable change.

Requirements: Node 22+ and Python 3 with PyYAML. `npm ci` installs Quartz dependencies. Tests: `python3 -m unittest scripts/second_brain/test_engine.py`, `node scripts/knowledgebase/knowledgebase.test.mjs`, `npm run kb:check`, `python3 scripts/second_brain/engine.py verify`, and `npm run build`.
