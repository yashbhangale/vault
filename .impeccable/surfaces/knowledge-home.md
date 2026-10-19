# Knowledge home

Scope: a navigation dashboard for the existing Quartz homepage and a private, plugin-free Obsidian Home. Product intent is recorded in `PRODUCT.md`: search and common destinations first, real metadata, minimal repeated reading. This extends the incumbent interface; it establishes no new visual identity or system-wide design rules. No deployment was performed.

## Existing authority

`quartz.config.ts` owns the current light/dark palette and typography. The dashboard uses its existing `--light`, `--lightgray`, `--darkgray`, `--dark`, `--secondary`, `--highlight`, and `--bodyFont` variables. `quartz/components/styles/knowledgeDashboard.scss` owns surface-specific spacing, sizing, borders, hover and keyboard-focus states. Retain these sources of truth rather than introducing parallel tokens.

The homepage uses a wider center, subject rows and a quick-access column. At 800px and below it stacks vertically. Changes to sidebar placement, article visibility and motion are scoped to the dashboard's presence. Existing reading pages retain their layout. Obsidian Home uses ordinary Markdown links, tables and built-in navigation commands.

## Behavior

`quartz/components/KnowledgeDashboard.tsx` renders only for the `index` slug, wired through `quartz.layout.ts`. Its search button and suggested topics open the existing Quartz search through `quartz:search`; listeners are cleaned up on SPA navigation. Subject counts come from published note metadata. Empty subjects and missing shortcut targets are omitted. Up to five dated notes appear in Recently updated, ordered by Quartz's configured date selection; the empty state is explicit.

`content/00 System/Home.md` provides private quick access, editable return links, a learning desk and a daily loop. Users can bookmark it with Obsidian's built-in command; no community plugin is required.

## Privacy boundary

The public dashboard consumes Quartz's already-filtered `allFiles`, never private manifests or the complete vault. Preserve the existing exclusions and publication filters in `quartz.config.ts`. Private Home has `publish: false` and resides within excluded `00 System`. Its personal links must not be copied into the public component. Raw captures remain source material and are not rewritten for this surface.

## Update flow

- Edit public subject labels and shortcut choices in `KnowledgeDashboard.tsx`; edit private shortcuts directly in Home.
- Maintain note metadata and existing index generators. `npm run kb:refresh` regenerates topic indexes; `npm run build` runs that refresh before Quartz builds the site.
- Use the existing second-brain process for changed captures; preserve provenance and manifests. Obsidian browser views continue using their existing definitions.
- After changes, run the build, check dashboard destinations and publication boundaries, and inspect desktop/mobile and light/dark rendering. Verify normal reading pages as well as Home.

## Verification evidence

Reported by the completing agent:

- Passed `npm run build`, `npx tsc --noEmit`, `node --test scripts/knowledgebase/knowledgebase.test.mjs`, `npm run kb:check`, and `git diff --check`.
- Second-brain verification covered 97 records with no broken outputs. The private Home audit found zero broken links. All 16 dashboard internal links resolved in generated HTML, and private Home was absent from public output.
- Browser checks covered desktop 1440×1000 and mobile 390×844 in dark mode. The AWS suggestion opened search with `AWS` and 12 result cards; Escape closed it. Final desktop rendering had no horizontal overflow. Screenshots: `.impeccable/review/desktop.png` and `.impeccable/review/mobile.png`.
- The independent review returned Ship with no material findings.

Limitations: screenshots cover dark mode only; actual Obsidian rendering was not inspected. No deployment was performed.
