---
title: Second Brain Architecture
type: guide
publish: false
---

# Directory roles

| Path | Purpose |
| --- | --- |
| `00 System/` | Instructions, schemas, templates, manifests, integration notes, and Bases |
| `01 Raw/` | Immutable original Telegram, OneNote, manual, transcript, clipping, and attachment captures |
| `02 Processed/` | One structured, source-linked record per raw file; optional Hinglish adaptations |
| `03 Journal/` | One daily note per date, when facts exist |
| `04 Trackers/` | Food, workouts, habits, and measurements backed by dated entries |
| `05 Knowledge/` | Maintained concepts, research, and public topic indexes |
| `06 Projects/` | Finite goals, milestones, decisions, and next actions |
| `07 Areas/` | Ongoing responsibilities, including work and career |
| `08 Resources/` | Books, references, tools, and career resources |
| `09 Outputs/` | Dated reviews and reports |
| `10 Archive/` | Prior processed versions and superseded material |

Raw, Processed, Journal, Trackers, Areas, Outputs, Archive, and System are private in Quartz. Career resources are private too. Processed records are deterministic scaffolds. A Codex source review can enrich them and update relevant Knowledge pages with citations. The raw files are never edited in that step.

## Capture and processing

- Direct Google API collectors preserve private snapshots under `01 Raw/Google/`, process selected snapshots through the same source ledger, and generate a private daily brief embedded in [[00 System/Today|Today]]. Calendar, Gmail, Tasks, and the nine configured ordinary YouTube playlists have completed first captures; an hourly local timer is enabled on this machine. See [[00 System/Instructions/Google capture|Google capture]] for scope, sign-in, scheduling, and Takeout watch-history imports.
- Telegram Sync writes Markdown and media into `01 Raw/Telegram/`; inspect plugin state after an Obsidian restart before treating live delivery as verified.
- Obsidian Importer writes OneNote pages into `01 Raw/OneNote/`, saves `onenote-id`, places attachments under `01 Raw/OneNote/Attachments`, and skips already imported pages to protect originals. Reimport an updated page as a separate copy when needed.
- The OneNote Integration plugin is a local COM embed/browser, not an independent exporter. Its live OneNote access requires a supported desktop environment.
- No Obsidian Web Clipper or transcript capture extension was found in the inspected Brave profile. Use `python3 scripts/second_brain/ingest.py --source youtube --file transcript.txt --url 'https://www.youtube.com/watch?v=VIDEO_ID'` or `--source web --file clipping.md --url 'https://example.com/article'`. This copies the original into Raw and records available metadata. It does not download from the web.
- Run `python3 scripts/second_brain/engine.py process`. The engine stats unchanged files without opening them, hashes changed candidates, writes each output, verifies its hash, then records success. A manual edit to a processed record stops overwrite and records an error. Use `retry` after resolving it.
- To catch content changes hidden behind unchanged file timestamps, run `python3 scripts/second_brain/engine.py discover --verify-hashes` occasionally.

## Metadata

Raw files keep original bytes. `00 System/Manifests/processing-state.json` stores source ID, original path/name, SHA-256, size, source type, validated capture timestamp, import timestamp, status, processed path/hash/time/version, error, and history. `processing-events.ndjson` is append-only. `intake.json` stores metadata supplied with manual imports. A capture timestamp is never substituted with file modification time. Ambiguous filenames retain no extracted timestamp.

Processed notes have YAML `type`, `source`, `source_id`, `raw_path`, `raw_sha256`, `processing_version`, `processing_status`, and optional observed metadata such as `captured_at`, `source_url`, `video_id`, `onenote-id`, or transcript markers. `enrichment_status: pending` means a human or Codex has yet to synthesize claims. A processed note must cite Raw. A Knowledge claim should cite a processed note or Raw, with timestamps when available.

## Local operations

```sh
python3 scripts/second_brain/engine.py discover
python3 scripts/second_brain/engine.py process
python3 scripts/second_brain/engine.py retry
python3 scripts/second_brain/engine.py verify
python3 scripts/second_brain/audit.py
npm run kb:refresh
npm run build
```

Use `rg` against `content/05 Knowledge`, `content/06 Projects`, and `content/08 Resources` before opening raw material for a query. Read the relevant index and a small set of matching files. `reports/` and the manifest provide compact audit entry points.

The recovery snapshot is `.recovery/pre-second-brain-2026-10-18.tar.zst` with a matching SHA-256 file. The supplementary archive captures a Telegram import that arrived immediately afterward. Both archives stay local and are ignored by Git.

The source-grounded, incremental wiki workflow follows [Karpathy’s original LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): keep Raw immutable, revise maintained notes as evidence arrives, and log each ingest.
