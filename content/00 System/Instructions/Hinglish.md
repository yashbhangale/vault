---
title: Hinglish Workflow
publish: false
type: guide
---

# On-demand Hinglish note

When the user says “Make a Hinglish transcription of this note,” resolve a path, selected file, or unique title using `python3 scripts/second_brain/hinglish.py prepare TARGET`. If a title is ambiguous, ask which note. If the source is already Hinglish, avoid a duplicate and explain why. Do not start a batch translation.

Read only that note. Write natural Hindi-English prose in Roman script under the deterministic path printed by the helper, inside `02 Processed/Hinglish/`. Preserve meaning, technical terms, code fences, commands, filenames, URLs, examples, and citations. Do not invent content. Keep the raw source intact.

The new file needs YAML `type: hinglish-transcription`, `canonical_path`, `canonical_sha256`, `source_raw` when present, and `transcription_status: current`, plus a link back to English. Run `python3 scripts/second_brain/hinglish.py finalize TARGET` to verify the copy and add its link near the top of the English note. `python3 scripts/second_brain/hinglish.py check` reports copies whose canonical source hash changed; leave those copies untouched until explicitly asked to update them.
