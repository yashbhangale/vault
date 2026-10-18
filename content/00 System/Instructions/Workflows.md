---
title: Second Brain Workflows
publish: false
type: guide
---

# Triage

Run `python3 scripts/second_brain/engine.py discover`. Inspect only the selected new/changed paths and errors from the compact manifest. Keep Raw untouched. A duplicate hash is a candidate, not permission to delete a source.

# Process

Run `python3 scripts/second_brain/engine.py process`. It writes and verifies one structured record per changed source. For an explicitly selected file use `--file '01 Raw/…'`; use `retry` after an error is fixed. Read the selected raw file and processed record if you are enriching the record with an LLM. For a transcript, retain timestamps and cite the exact source. Update an existing Knowledge concept where new evidence belongs; add reciprocal links when relevant. After source review, set `enrichment_status: reviewed` in that processed record and run `python3 scripts/second_brain/enrich.py '01 Raw/…'` to verify provenance and record the reviewed output hash. Do not mark model synthesis complete without actually reviewing the source.

Embed images directly in their processed notes and relevant journal entries using an exclamation mark before a full-path Obsidian wikilink to the Raw image; do not leave only a clickable link. Keep the original image in Raw and retain its source link alongside the embed. A date-stamped Telegram image gets an inline journal image on its capture date. Add a visual description only after viewing the actual image; do not infer an event, identity, or relationship from proximity alone.

# Query

Start with the public Knowledge map, Obsidian Bases, or `rg -l 'term' 'content/05 Knowledge' 'content/06 Projects' 'content/08 Resources'`. Open only likely matches, then follow their source links. Answer with note paths and timestamps where present. Say when a source lacks a claimed detail.

# Review

Run `python3 scripts/second_brain/review.py weekly` or `monthly`. The report links recorded journal and activity facts. Add conclusions only after reading those selected records. The script does not infer missing meals, workouts, mood, or project progress.

# Audit

Run `python3 scripts/second_brain/audit.py`, `python3 scripts/second_brain/engine.py verify`, `python3 scripts/second_brain/hinglish.py check`, and `npm run kb:check`. The JSON audit lists broken/ambiguous links, duplicate candidates, stale outputs, and metadata issues. Existing missing-note placeholders remain flagged for manual review rather than receiving invented pages.

# Hinglish

Follow [[00 System/Instructions/Hinglish|the Hinglish workflow]] for one explicit note. The assistant supplies the natural Roman-script adaptation, while the helper resolves paths, hashes, and backlinks.
