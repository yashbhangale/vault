---
title: Capture Integration Findings
publish: false
type: guide
---

# Telegram

The installed `telegram-sync` plugin is version 4.0.0. Its existing distribution rule originally wrote Markdown to `Telegram/{{content:30}} - {{messageTime:YYYYMMDDHHmmssSSS}}.md` and files to `Telegram/{{file:type}}s/{{file:name}} - {{messageTime:YYYYMMDDHHmmssSSS}}.{{file:extension}}`. Those two destinations now point under `01 Raw/Telegram/`. Bot credentials, allowed chats, message deletion policy, and other rule fields were preserved. Obsidian should be restarted so the running plugin loads the changed settings. A live post-restart delivery has not yet been observed.

Four media filenames and one message filename use a valid 17-digit time suffix. The processor validates the calendar date and preserves milliseconds. The suffix does not state a timezone, so the ledger records it without inventing one. Images and voice notes stay in Raw. No OCR, speech transcription, or message association is inferred without evidence.

# OneNote

Obsidian Importer 3.1.15 was configured with `OneNote` as output folder, vault-root attachment placement, duplicate handling set to `update`, and `onenote-id` saving. It now targets `01 Raw/OneNote/`, keeps `onenote-id`, places future attachments in `01 Raw/OneNote/Attachments`, and skips duplicates by default to protect original imports. Existing OneNote notes and attachments moved with their original bytes. The OneNote Integration plugin 1.3.10 identifies itself as a local COM embed/browser; its manifest does not establish an automatic export or cloud sync pipeline. On this Linux host, live COM behavior cannot be verified. Use Obsidian Importer for deliberate imports; preserve source IDs. If an updated page must be captured, import a separate copy and keep the prior raw version.

# Browser, YouTube, and web clippings

The inspected Brave extension profile contained no identifiable Obsidian Web Clipper or YouTube transcript capture extension. The local Google Chrome extension directory was absent. No existing transcript or web-clipping file was found in the vault. Therefore, no browser capture behavior or automatic synchronization is claimed.

Use `python3 scripts/second_brain/ingest.py --source youtube --file /path/to/transcript.txt --url 'https://www.youtube.com/watch?v=VIDEO_ID' --title 'Video title'` or replace `youtube` with `web` and supply a clipping file. Optional `--author`, `--published`, and `--captured` fields record only information you know. The command copies and verifies the original file in Raw and records the import in `intake.json`. It does not fetch a URL. The processor preserves detected transcript markers in the structured record; Codex can later synthesize specific claims with source timestamps.

The local settings files under `.obsidian` are ignored by Git. New machines need these destination settings configured again or supplied through the user's Obsidian sync mechanism. Keep credentials out of copied documentation.
