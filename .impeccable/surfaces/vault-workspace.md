# Local vault workspace

Mode: Operate, with a Read view for notes. This extends the established Quartz dashboard into a local daily workspace. The user requested full-vault browsing and source controls, then explicitly deferred authentication. The functional layout follows the specified work: Today, source views, all notes, reader, quick capture and sync controls. This is an extension of the incumbent world, not a replacement visual direction.

## Existing world

Preserve Quartz's charcoal `#111315`, warm ivory `#e8e3d5`, yellow `#ffbc00`, and teal `#56cece` in dark mode. Light mode inherits cream `#f5f2e9`, charcoal, amber `#805900` and teal `#176b6b`. Operate typography uses a legible sans stack without fetching external fonts. Controls use a consistent 6px radius, visible keyboard focus and quiet separators. No new illustrative assets or style world are needed.

## Interface contract

- A persistent left navigation, global local-vault search and a compact source-refresh action. Mobile navigation becomes a horizontally scrollable row; primary controls remain reachable.
- Today leads with the day's agenda and open tasks, not productivity scores or inferred completion. Recent notes and a direct journal/capture path complete the view.
- All notes uses folder navigation and a searchable file list. The reader renders Markdown safely with inline vault images, native supported media, provenance links and original downloads.
- Source views filter the actual collected data and show freshness and capture scope. Sync controls refresh fixed sources and pause/resume the existing timer.
- Capture is an inline form with a retained draft on failure. Original files and manifests remain governed by the existing engine.
- Current real account captures power the local page. Private QA screenshots must stay ignored by Git. No demonstration content is written into production Raw.

## Technical boundary

Only loopback listeners. The private workspace is `http://127.0.0.1:4173/`; the public Quartz preview is isolated on `http://127.0.0.1:4174/vault/`. No login or credentials were implemented for this web interface. Published Quartz exclusions are unchanged. The public homepage gains a local-workspace link and no private data fetches.

Targets: `scripts/dashboard/ui/index.html`, `style.css`, `app.js`, `scripts/dashboard/server.mjs`, `vault.mjs`, `quartz/components/KnowledgeDashboard.tsx`, and its existing stylesheet.

## Verification evidence

Review the live local dashboard on desktop and mobile, plus light mode and the all-notes/reader/source/control states. Backend tests cover private-path rejection, symlink escapes, script injection, CSRF/Host checks, safe fixed commands, search and public-preview separation. Preserve the existing public Quartz appearance and verify its build and publication boundary.

Completed checks: nine dashboard tests and twenty-one collector tests passed; production source-index hashes remained unchanged during collector tests. TypeScript and Quartz build passed. Live search returned sixteen Kubernetes matches; an existing note rendered with seven inline images; the completed-task filter showed seventy-five completed tasks; a source-specific Tasks refresh completed through the browser. Desktop and compact dark/light captures are stored as ignored local QA files under `.impeccable/review/workspace-*.png`. The finish reviewer requested mobile agenda → tasks → recent notes ordering; that fix was confirmed in new captures and received `disposition: ship` in the scored verdict. No authentication, internet deployment, remote private-data upload, or synthetic production capture was performed.
