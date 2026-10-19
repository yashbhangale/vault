import fs from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"
import yaml from "js-yaml"
import { isPublic } from "./policy.mjs"
import { referencedAttachments } from "./attachments.mjs"
import { escape } from "minimatch"

const repo = fileURLToPath(new URL("../../", import.meta.url))
const root = path.join(repo, "content")
const config = JSON.parse(await fs.readFile(new URL("./config.json", import.meta.url), "utf8"))
const mode = process.argv[2] ?? "audit"
if (!["audit", "refresh", "check"].includes(mode)) throw new Error("Use audit, refresh, or check")
const write = mode === "refresh"
const notes = []
const assets = []
const errors = []
let metadataChanges = 0
let generatedChanges = 0

// Read metadata only. Bodies are read again only for a note that needs new properties.
async function header(file) {
  const handle = await fs.open(file, "r")
  const decoder = new TextDecoder("utf-8", { fatal: true })
  let prefix = ""
  try {
    while (true) {
      const buffer = Buffer.alloc(4096)
      const { bytesRead } = await handle.read(buffer, 0, buffer.length, null)
      prefix += decoder.decode(buffer.subarray(0, bytesRead), { stream: bytesRead > 0 })
      const eol = prefix.includes("\r\n") ? "\r\n" : "\n"
      if (prefix.length >= 4 && !prefix.startsWith(`---${eol}`)) return { data: {}, end: 0, eol }
      const match = prefix.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)
      if (match) {
        const data = yaml.load(match[1], { schema: yaml.JSON_SCHEMA }) ?? {}
        if (typeof data !== "object" || Array.isArray(data))
          throw new Error("Frontmatter must be a mapping")
        return { data, end: match[0].length, eol }
      }
      if (!bytesRead) {
        if (prefix.startsWith("---")) throw new Error("Unclosed frontmatter")
        return { data: {}, end: 0, eol }
      }
      if (prefix.length > 262144) throw new Error("Frontmatter exceeds 256 KB")
    }
  } finally {
    await handle.close()
  }
}

function defaults(relative, data) {
  const parts = relative.split("/")
  const top = parts[0]
  const stem = path.posix.basename(relative, ".md")
  let [area, , type] = config.areas[top] ?? ["uncategorized", "Uncategorized", "note"]
  if (top === "05 Knowledge") {
    area =
      parts[1] === "Cloud and DevOps"
        ? "cloud-devops"
        : parts[1] === "Programming"
          ? "programming"
          : parts[1] === "AI"
            ? "product-ai"
            : "personal-learning"
  }
  if (top === "08 Resources") {
    area =
      parts[1] === "Career" ? "career" : parts[1] === "Books" ? "personal-learning" : "resources"
  }
  const source = relative.startsWith("01 Raw/Telegram/")
    ? "telegram"
    : relative.startsWith("01 Raw/OneNote/") || data["onenote-id"]
      ? "onenote"
      : "obsidian"
  return {
    title: stem,
    tags: [area],
    type: relative.endsWith(".excalidraw.md") ? "drawing" : type,
    area,
    topic: parts.length > 2 ? parts[2] : top,
    status: source !== "obsidian" || top === "01 Raw" ? "inbox" : "unreviewed",
    source,
  }
}

async function walk(dir) {
  for (const entry of (await fs.readdir(dir, { withFileTypes: true })).sort((a, b) =>
    a.name.localeCompare(b.name),
  )) {
    if (entry.name.startsWith(".") || entry.isSymbolicLink()) continue
    const file = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      await walk(file)
      continue
    }
    if (!entry.name.endsWith(".md")) {
      assets.push(path.relative(root, file).split(path.sep).join("/"))
      continue
    }
    const relative = path.relative(root, file).split(path.sep).join("/")
    try {
      const parsed = await header(file)
      const managed =
        relative.startsWith(`${config.hub}/`) ||
        relative.startsWith("01 Raw/") ||
        relative.startsWith("02 Processed/") ||
        relative.startsWith("03 Journal/") ||
        relative.startsWith("04 Trackers/") ||
        relative.startsWith("09 Outputs/") ||
        relative.startsWith("10 Archive/") ||
        relative.startsWith("00 System/") ||
        relative === "index.md" ||
        relative.startsWith("00 System/Templates/")
      const additions = Object.fromEntries(
        Object.entries(defaults(relative, parsed.data)).filter(([key]) => !(key in parsed.data)),
      )
      if (!managed && Object.keys(additions).length) {
        metadataChanges++
        if (write) {
          const original = await fs.readFile(file, "utf8")
          const extra = yaml
            .dump(additions, { lineWidth: -1, quotingType: '"', forceQuotes: true })
            .replaceAll("\n", parsed.eol)
          const updated = parsed.end
            ? original.slice(0, parsed.end).replace(/---(?:\r?\n)?$/, `${extra}---${parsed.eol}`) +
              original.slice(parsed.end)
            : `---${parsed.eol}${extra}---${parsed.eol}${original}`
          await fs.writeFile(file, updated)
        }
      }
      notes.push({ path: relative, data: managed ? parsed.data : { ...additions, ...parsed.data } })
    } catch (error) {
      errors.push({ path: relative, error: error.message })
    }
  }
}
await walk(root)
// Never regenerate indexes from a partial inventory.
if (errors.length) {
  console.error(JSON.stringify({ errors }, null, 2))
  process.exitCode = 1
} else {
  const privateAssets = new Set()
  for (const note of notes.filter((note) => !isPublic(note, config))) {
    const text = await fs.readFile(path.join(root, note.path), "utf8")
    for (const asset of referencedAttachments(text, note.path, assets)) privateAssets.add(asset)
  }
  const assetFile = path.join(repo, "scripts/knowledgebase/private-assets.json")
  const assetText =
    JSON.stringify(
      [...privateAssets].sort().map((asset) => escape(asset)),
      null,
      2,
    ) + "\n"
  if ((await fs.readFile(assetFile, "utf8").catch(() => "")) !== assetText) {
    generatedChanges++
    if (write) await fs.writeFile(assetFile, assetText)
  }
  const publicNotes = notes.filter(
    (note) =>
      !note.path.startsWith(`${config.hub}/`) && note.path !== "index.md" && isPublic(note, config),
  )
  const labels =
    config.areaLabels ??
    Object.fromEntries(Object.values(config.areas).map(([area, label]) => [area, label]))
  labels.uncategorized = "Unfiled notes"
  const byArea = Map.groupBy(publicNotes, (note) => note.data.area ?? "uncategorized")
  function link(note) {
    // Standard encoded Markdown links work with Quartz and Obsidian, even for filenames containing brackets.
    const target = "/" + encodeURI(note.path)
    const label = String(note.data.title ?? path.posix.basename(note.path, ".md"))
      .replace(/[\r\n]/g, " ")
      .replace(/[\\[\]]/g, "\\$&")
    return `[${label}](<${target}>)`
  }
  function page(title, description, body) {
    return `---\n${yaml.dump({ title, description, type: "index", area: "system", status: "maintained", source: "generated", tags: ["index"] }, { lineWidth: -1 })}---\n\n<!-- Generated by npm run kb:refresh. Edit scripts/knowledgebase/index.mjs instead. -->\n\n${body}\n`
  }
  async function output(relative, text) {
    const dest = path.join(root, relative)
    const old = await fs.readFile(dest, "utf8").catch(() => null)
    if (old === text) return
    generatedChanges++
    if (write) {
      await fs.mkdir(path.dirname(dest), { recursive: true })
      await fs.writeFile(dest, text)
    }
  }
  // Clear a previously generated hub when its last public note is withheld.
  for (const note of notes) {
    const area = path.posix.basename(note.path, ".md")
    if (
      note.path === `${config.hub}/${area}.md` &&
      note.data.source === "generated" &&
      labels[area] &&
      !byArea.has(area)
    ) {
      await output(
        note.path,
        page(
          labels[area],
          "No published notes in this subject.",
          `[Home](/index.md)\n\nNo published notes in this subject.`,
        ),
      )
    }
  }
  const areaEntries = [...byArea].sort(([a], [b]) => a.localeCompare(b))
  const mapLinks = []
  for (const [area, entries] of areaEntries) {
    const groups = Map.groupBy(entries, (note) => path.posix.dirname(note.path))
    const sections = [...groups]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(
        ([folder, items]) =>
          `## ${folder === "." ? "Unfiled" : folder}\n\n${items
            .sort((a, b) => String(a.data.title).localeCompare(String(b.data.title)))
            .map((note) => `- ${link(note)}`)
            .join("\n")}`,
      )
    const hub = `${config.hub}/${area}.md`
    await output(
      hub,
      page(
        labels[area] ?? area,
        `Browse ${entries.length} notes in ${labels[area] ?? area}.`,
        `[Home](/index.md) · [Knowledge map](/${config.hub}/Sitemap.md)\n\n${sections.join("\n\n")}`,
      ),
    )
    mapLinks.push(
      `- ${link({ path: hub, data: { title: labels[area] ?? area } })} — ${entries.length} ${entries.length === 1 ? "note" : "notes"}`,
    )
  }
  await output(
    `${config.hub}/Sitemap.md`,
    page(
      "Knowledge map",
      "Browse the knowledge base by subject and folder.",
      `[Home](/index.md)\n\n${publicNotes.length} published notes, organized by subject. Each subject index lists its notes by their original folder.\n\n${mapLinks.join("\n")}\n\nThe website also provides [an XML sitemap](https://yashbhangale.github.io/vault/sitemap.xml) and [an RSS feed](https://yashbhangale.github.io/vault/index.xml).`,
    ),
  )
  await output(
    "index.md",
    page(
      "Home",
      "Find a note, browse a subject, or return to recent learning.",
      `Find a note with search, or choose a subject below. On the website, press Ctrl/Cmd + K to search.\n\n## Browse by subject\n\n${mapLinks.join("\n")}\n\n[Full knowledge map](</${config.hub}/Sitemap.md>)`,
    ),
  )
  const summary = {
    notes: notes.length,
    privateAttachments: privateAssets.size,
    publicNotes: publicNotes.length,
    metadataChanges,
    generatedChanges,
    areas: Object.fromEntries(areaEntries.map(([area, entries]) => [area, entries.length])),
    uncategorized: publicNotes
      .filter((note) => note.data.area === "uncategorized")
      .map((note) => note.path),
    duplicateTitles: Object.entries(Object.groupBy(notes, (note) => String(note.data.title)))
      .filter(([, entries]) => entries.length > 1)
      .map(([title, entries]) => ({ title, paths: entries.map((note) => note.path) })),
  }
  if (write) {
    await fs.mkdir(path.join(repo, "reports"), { recursive: true })
    await fs.writeFile(
      path.join(repo, "reports/knowledgebase-audit.json"),
      JSON.stringify(summary, null, 2) + "\n",
    )
  }
  console.log(
    JSON.stringify({ mode, ...summary, duplicateTitles: summary.duplicateTitles.length }, null, 2),
  )
  if (mode === "check" && (metadataChanges || generatedChanges)) process.exitCode = 1
}
