import fs from "node:fs/promises"
import path from "node:path"
import crypto from "node:crypto"
import { execFile } from "node:child_process"
import { promisify } from "node:util"
import { unified } from "unified"
import remarkParse from "remark-parse"
import remarkGfm from "remark-gfm"
import { toHast } from "mdast-util-to-hast"
import { toHtml } from "hast-util-to-html"
import matter from "gray-matter"

const exec = promisify(execFile)
export const folders = [
  "00 System",
  "01 Raw",
  "02 Processed",
  "03 Journal",
  "04 Trackers",
  "05 Knowledge",
  "06 Projects",
  "07 Areas",
  "08 Resources",
  "09 Outputs",
  "10 Archive",
]
const readable = new Set([".md", ".txt", ".srt", ".vtt", ".json", ".csv", ".base"])
export const digest = (text) => crypto.createHash("sha256").update(text).digest("hex")

export class Vault {
  constructor(root) {
    this.root = path.resolve(root)
    this.content = path.join(this.root, "content")
    this.cache = null
    this.cacheAt = 0
  }

  async file(relative) {
    if (typeof relative !== "string" || relative.includes("\\") || relative.includes("\0"))
      throw new Error("Invalid vault path")
    const parts = relative.split("/")
    if (
      !folders.includes(parts[0]) ||
      parts.some((p) => !p || p.startsWith(".")) ||
      relative.startsWith("00 System/Manifests/")
    )
      throw new Error("This path is outside the readable vault")
    const full = await fs.realpath(path.join(this.content, relative))
    const realRoot = await fs.realpath(this.content)
    if (!full.startsWith(realRoot + path.sep) || !(await fs.stat(full)).isFile())
      throw new Error("Invalid vault file")
    // Check the resolved path as well, so a symlink cannot bypass exclusions.
    const resolved = path.relative(realRoot, full).split(path.sep).join("/")
    if (
      !folders.includes(resolved.split("/")[0]) ||
      resolved.startsWith("00 System/Manifests/") ||
      resolved.split("/").some((p) => p.startsWith("."))
    )
      throw new Error("This file is not readable")
    return full
  }

  async index() {
    if (this.cache && Date.now() - this.cacheAt < 5000) return this.cache
    const files = []
    const walk = async (relative) => {
      const entries = await fs
        .readdir(path.join(this.content, relative), { withFileTypes: true })
        .catch(() => [])
      for (const entry of entries) {
        if (entry.name.startsWith(".") || entry.isSymbolicLink() || /[\r\n]/.test(entry.name))
          continue
        const rel = relative + "/" + entry.name
        if (rel === "00 System/Manifests") continue
        if (entry.isDirectory()) await walk(rel)
        else if (entry.isFile()) {
          const stat = await fs.stat(path.join(this.content, rel))
          const stem = entry.name.replace(/\.[^.]+$/, "")
          const snapshotTitle =
            /^[a-f0-9]{64}$/.test(stem) && rel.includes("/Google/")
              ? `${rel.split("/Google/")[1].split("/")[0]} snapshot · ${stat.mtime.toISOString().slice(0, 10)}`
              : stem
          files.push({
            path: rel,
            title: snapshotTitle,
            folder: rel.split("/")[0],
            ext: path.extname(entry.name).toLowerCase(),
            updated: stat.mtime.toISOString(),
            bytes: stat.size,
          })
        }
      }
    }
    for (const folder of folders) await walk(folder)
    this.cache = files.sort(
      (a, b) => b.updated.localeCompare(a.updated) || a.path.localeCompare(b.path),
    )
    this.cacheAt = Date.now()
    return this.cache
  }

  async search(query = "", folder = "") {
    if (query.length > 200 || (folder && !folders.includes(folder)))
      throw new Error("Invalid search")
    const files = await this.index()
    const lower = query.toLocaleLowerCase()
    let matches = new Set()
    const targets = [...new Set(files.map((file) => file.folder))].filter(
      (name) => !folder || name === folder,
    )
    if (query.trim().length >= 2 && targets.length) {
      try {
        const { stdout } = await exec(
          "rg",
          [
            "--no-ignore",
            "--files-with-matches",
            "--fixed-strings",
            "--ignore-case",
            "--glob",
            "*.md",
            "--glob",
            "!00 System/Manifests/**",
            "--",
            query,
            ...targets,
          ],
          { cwd: this.content, maxBuffer: 4 * 1024 * 1024, timeout: 15000 },
        )
        matches = new Set(stdout.trim().split("\n"))
      } catch (error) {
        if (error.code !== 1 && error.code !== "ENOENT") throw error
      }
    }
    const rows = files.filter(
      (file) =>
        (!folder || file.folder === folder) &&
        (!query || file.path.toLocaleLowerCase().includes(lower) || matches.has(file.path)),
    )
    return {
      total: rows.length,
      files: rows.slice(0, 1000),
      truncated: rows.length > 1000,
      folders: folders.map((name) => ({
        name,
        count: files.filter((file) => file.folder === name).length,
      })),
    }
  }

  async resolve(target, current = "") {
    let decoded
    try {
      decoded = decodeURIComponent(target)
    } catch {
      decoded = target
    }
    const clean = decoded.split("#")[0].replace(/^\//, "")
    const files = await this.index()
    const candidates = [
      clean,
      clean + ".md",
      path.posix.normalize(path.posix.join(path.posix.dirname(current), clean)),
      path.posix.normalize(path.posix.join(path.posix.dirname(current), clean + ".md")),
    ]
    for (const candidate of candidates) {
      if (files.some((file) => file.path === candidate)) return candidate
    }
    const short = files.filter(
      (file) =>
        path.posix.basename(file.path) === clean || path.posix.basename(file.path, ".md") === clean,
    )
    return short.length === 1 ? short[0].path : null
  }

  async render(text, current) {
    const tree = unified().use(remarkParse).use(remarkGfm).parse(text)
    const local = (relative, image = false) =>
      image
        ? "/api/file?path=" + encodeURIComponent(relative)
        : "/#note=" + encodeURIComponent(relative)
    const rewrite = async (node) => {
      if (node.type === "html") {
        node.type = "text"
        node.value = node.value
        return
      }
      if (["link", "image", "definition"].includes(node.type)) {
        if (/^(https?:|mailto:)/i.test(node.url)) {
          if (node.type === "image") {
            node.type = "link"
            node.children = [{ type: "text", value: node.alt || "External image" }]
          }
        } else if (node.url.startsWith("#")) {
          /* ordinary in-note anchor */
        } else {
          const resolved = await this.resolve(node.url, current)
          node.url = resolved ? local(resolved, node.type === "image") : "#missing-note"
        }
      }
      if (!node.children) return
      const children = []
      for (const child of node.children) {
        if (child.type === "text" && /!?\[\[/.test(child.value)) {
          let cursor = 0
          const regex = /(!?)\[\[([^\]\n]+)\]\]/g
          for (const match of child.value.matchAll(regex)) {
            if (match.index > cursor)
              children.push({ type: "text", value: child.value.slice(cursor, match.index) })
            const [target, alias] = match[2].split("|")
            const resolved = await this.resolve(target, current)
            const label = alias || path.posix.basename(target)
            const image = match[1] && resolved && /\.(png|jpe?g|gif|webp)$/i.test(resolved)
            children.push(
              resolved
                ? image
                  ? { type: "image", url: local(resolved, true), alt: label }
                  : {
                      type: "link",
                      url: local(resolved),
                      children: [{ type: "text", value: label }],
                    }
                : { type: "text", value: label + " (missing or ambiguous)" },
            )
            cursor = match.index + match[0].length
          }
          if (cursor < child.value.length)
            children.push({ type: "text", value: child.value.slice(cursor) })
        } else {
          await rewrite(child)
          children.push(child)
        }
      }
      node.children = children
    }
    await rewrite(tree)
    return toHtml(toHast(tree))
  }

  async note(relative) {
    const full = await this.file(relative)
    const stat = await fs.stat(full)
    if (stat.size > 10 * 1024 * 1024)
      throw new Error("This file is large; download it to read locally")
    if (!readable.has(path.extname(full).toLowerCase()))
      return { path: relative, title: path.basename(relative), media: true, bytes: stat.size }
    const text = await fs.readFile(full, "utf8")
    const markdown = full.toLowerCase().endsWith(".md")
    let data = {},
      content = text
    if (markdown) {
      try {
        const parsed = matter(text)
        data = parsed.data
        content = parsed.content
      } catch {
        /* show source if frontmatter is malformed */
      }
    }
    return {
      path: relative,
      title: String(data.title || path.basename(relative, path.extname(relative))),
      updated: stat.mtime.toISOString(),
      hash: digest(text),
      markdown,
      text,
      html: markdown ? await this.render(content, relative) : null,
      metadata: Object.fromEntries(
        ["type", "source", "captured_at", "source_url", "enrichment_status", "processing_status"]
          .filter((key) => data[key] !== undefined)
          .map((key) => [key, String(data[key])]),
      ),
    }
  }

  async overview() {
    const read = async (relative, fallback) => {
      try {
        return JSON.parse(await fs.readFile(path.join(this.content, relative), "utf8"))
      } catch {
        return fallback
      }
    }
    const state = await read("00 System/Manifests/google-capture.json", {})
    const sources = {}
    for (const name of ["calendar", "tasks", "gmail", "youtube", "youtube-history"]) {
      const row = state[name]
      if (!row && name === "youtube-history") continue
      let payload = { items: [], scope: {} }
      if (row?.raw_path?.startsWith("01 Raw/Google/")) {
        try {
          const text = await fs.readFile(await this.file(row.raw_path), "utf8")
          payload = JSON.parse(text.split("\n<!-- payload -->\n```json\n")[1].split("\n```")[0])
        } catch {
          /* health still records the source's state */
        }
      }
      const stale =
        !row?.last_success_at || Date.now() - Date.parse(row.last_success_at) > 2 * 60 * 60 * 1000
      sources[name] = {
        status: row?.status || "not-connected",
        checked: row?.last_success_at || null,
        stale,
        error: row?.error || null,
        raw: row?.raw_path || null,
        items: payload.items || [],
        scope: payload.scope || {},
        truncated: !!payload.truncated,
      }
    }
    const files = await this.index()
    return {
      date: new Intl.DateTimeFormat("en-CA", {
        timeZone: "Asia/Kolkata",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(new Date()),
      timezone: "Asia/Kolkata",
      sources,
      recent: files
        .filter(
          (file) =>
            file.ext === ".md" &&
            !path.basename(file.path).startsWith("_") &&
            !file.folder.startsWith("00") &&
            !file.folder.startsWith("10"),
        )
        .slice(0, 8),
      files: files.length,
      folders: folders.map((name) => ({
        name,
        count: files.filter((file) => file.folder === name).length,
      })),
    }
  }
}
