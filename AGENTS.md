# Vault operating rules

This repository is an Obsidian vault in `content/` and a Quartz website. Work locally. Never send private vault content, credentials, or raw captures to an external service without the user's explicit authorization.

- `content/01 Raw/` is the source archive. Read selected captures; do not rewrite or delete them. Use `python3 scripts/second_brain/engine.py process` to structure new or changed files. The manifest in `content/00 System/Manifests/` records hashes, provenance, status, and output paths.
- `content/02 Processed/` holds derived source records. They link to Raw and can be enriched with sourced summaries. `content/05 Knowledge/` holds maintained concepts and indexes. Update an existing concept when new evidence arrives and link both sides when helpful.
- When an image belongs in a journal or processed note, display it inline with an Obsidian embed such as `![[01 Raw/Telegram/photos/example.jpg]]`. A plain `[[image]]` link alone is insufficient. Keep the original in Raw, add a short grounded caption when reviewed, and never assume a photo proves an activity or identity. Apply this to future image captures and notes, not only the current day.
- `03 Journal`, `04 Trackers`, `06 Projects`, `07 Areas`, `08 Resources`, `09 Outputs`, and `10 Archive` have distinct roles. See `content/00 System/Instructions/Architecture.md`.
- For a query, search the public topic index or local search first, then read only relevant files. Cite source paths and transcript timestamps where present. Never invent missing dates, quotes, food metrics, workouts, or relationships.
- For “Make a Hinglish transcription of this note”, follow `content/00 System/Instructions/Hinglish.md`. Translate only the selected note, preserve code/commands/URLs, and track the English source hash.
- Triage with `python3 scripts/second_brain/engine.py discover`; process with `process`; retry errors with `retry`; validate with `verify`. Audit with `python3 scripts/second_brain/audit.py`. Maintain the source ledger and append-only event log.
- Publishing: `00 System`, Raw, Processed, Journal, Trackers, Areas, Outputs, and Archive are excluded from Quartz by default. Review public Knowledge, Projects, and Resources before publication. Run `npm run build` after changes and inspect the output.
- Before any new bulk move, update the migration map, make a verified recovery snapshot, check collisions/hashes, and verify links after the move. Never permanently delete unique source material.
