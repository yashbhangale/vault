import http from "node:http"
import fs from "node:fs/promises"
import path from "node:path"
import crypto from "node:crypto"
import { fileURLToPath } from "node:url"
import { execFile } from "node:child_process"
import { promisify } from "node:util"
import { Vault } from "./vault.mjs"

const exec = promisify(execFile)
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..")
const UI = path.join(ROOT, "scripts/dashboard/ui")
const mime = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".pdf": "application/pdf",
  ".mp3": "audio/mpeg",
  ".ogg": "audio/ogg",
  ".m4a": "audio/mp4",
  ".wav": "audio/wav",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
}
const allowedSources = ["calendar", "tasks", "gmail", "youtube"]

export function createDashboard({ root = ROOT, run = exec } = {}) {
  const vault = new Vault(root)
  const token = crypto.randomBytes(32).toString("hex")
  const jobs = new Map()
  let busy = false
  const python = path.join(root, ".venv/bin/python")
  const script = (name) => path.join(root, "scripts/second_brain", name)
  const command = async (file, args) =>
    run(file, args, { cwd: root, maxBuffer: 2 * 1024 * 1024, timeout: 30 * 60 * 1000 })
  const job = (kind, work) => {
    if (busy) throw new Error("Another dashboard action is running. Wait for it to finish.")
    busy = true
    const id = crypto.randomUUID()
    const row = { id, kind, status: "running", started: new Date().toISOString() }
    jobs.set(id, row)
    if (jobs.size > 20) jobs.delete(jobs.keys().next().value)
    Promise.resolve()
      .then(work)
      .then((result) => {
        row.status = "done"
        row.result = result
      })
      .catch(() => {
        row.status = "error"
        row.error =
          "The action did not complete. Check source health, API setup, or the local service log and retry."
      })
      .finally(() => {
        row.ended = new Date().toISOString()
        busy = false
        vault.cacheAt = 0
      })
    return row
  }
  const schedule = async () => {
    const active = await run("systemctl", ["--user", "is-active", "vault-google.timer"], {
      timeout: 5000,
    })
      .then(({ stdout }) => stdout.trim() === "active")
      .catch(() => false)
    return { active }
  }
  const server = http.createServer(async (req, res) => {
    const send = (status, value, type = "application/json") => {
      res.writeHead(status, {
        "Content-Type":
          type + (type.startsWith("text/") || type === "application/json" ? "; charset=utf-8" : ""),
      })
      res.end(type === "application/json" ? JSON.stringify(value) : value)
    }
    res.setHeader("Cache-Control", "no-store")
    res.setHeader("X-Content-Type-Options", "nosniff")
    res.setHeader("X-Frame-Options", "DENY")
    res.setHeader("Cross-Origin-Resource-Policy", "same-origin")
    res.setHeader("Referrer-Policy", "no-referrer")
    res.setHeader(
      "Content-Security-Policy",
      "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self'; font-src 'self'; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
    )
    try {
      const localPort = server.address()?.port
      const hosts = new Set([`127.0.0.1:${localPort}`, `localhost:${localPort}`])
      if (!hosts.has(req.headers.host) || req.headers["sec-fetch-site"] === "cross-site")
        return send(403, { error: "This workspace is available only on this computer." })
      const url = new URL(req.url, "http://" + req.headers.host)
      if (!["GET", "HEAD", "POST"].includes(req.method))
        return send(405, { error: "Method not supported" })
      if (req.method === "POST") {
        if (
          req.headers.origin !== "http://" + req.headers.host ||
          req.headers["x-vault-token"] !== token
        )
          return send(403, { error: "Refresh the workspace before trying this action." })
        let raw = ""
        for await (const chunk of req) {
          raw += chunk
          if (Buffer.byteLength(raw) > 128 * 1024)
            return send(413, { error: "Capture must be smaller than 128 KB." })
        }
        const body = raw ? JSON.parse(raw) : {}
        if (url.pathname === "/api/sync") {
          const sources = body.sources || allowedSources
          if (
            !Array.isArray(sources) ||
            !sources.length ||
            sources.some((source) => !allowedSources.includes(source))
          )
            return send(400, { error: "Choose a valid source." })
          return send(
            202,
            job("Sync sources", async () => {
              await command(python, [script("google_capture.py"), "sync", "--sources", ...sources])
              await command(python, [script("search.py"), "index"])
              return "Sources and search index updated."
            }),
          )
        }
        if (url.pathname === "/api/schedule") {
          if (typeof body.enabled !== "boolean")
            return send(400, { error: "Choose enable or pause." })
          return send(
            202,
            job(body.enabled ? "Resume hourly sync" : "Pause hourly sync", async () => {
              await command("systemctl", [
                "--user",
                body.enabled ? "enable" : "disable",
                "--now",
                "vault-google.timer",
              ])
              return body.enabled ? "Hourly sync is on." : "Hourly sync is paused."
            }),
          )
        }
        if (url.pathname === "/api/capture") {
          if (typeof body.text !== "string" || !body.text.trim() || body.text.length > 100000)
            return send(400, { error: "Write a capture first (up to 100,000 characters)." })
          const text = body.text
          return send(
            202,
            job("Save capture", async () => {
              const folder = path.join(root, "private/dashboard/intake")
              await fs.mkdir(folder, { recursive: true, mode: 0o700 })
              const file = path.join(
                folder,
                `capture-${Date.now()}-${crypto.randomBytes(4).toString("hex")}.md`,
              )
              await fs.writeFile(file, text, { mode: 0o600, flag: "wx" })
              try {
                const { stdout } = await command(python, [
                  script("capture_local.py"),
                  "--file",
                  file,
                ])
                const imported = JSON.parse(stdout)
                await command(python, [script("search.py"), "index"])
                return { message: "Capture saved and processed.", path: imported.raw_path }
              } finally {
                await fs.unlink(file).catch(() => {})
              }
            }),
          )
        }
        return send(404, { error: "Action not found" })
      }
      if (url.pathname === "/api/context") return send(200, { token, localOnly: true })
      if (url.pathname === "/api/overview") return send(200, await vault.overview())
      if (url.pathname === "/api/notes")
        return send(
          200,
          await vault.search(url.searchParams.get("q") || "", url.searchParams.get("folder") || ""),
        )
      if (url.pathname === "/api/note")
        return send(200, await vault.note(url.searchParams.get("path")))
      if (url.pathname === "/api/resolve")
        return send(200, { path: await vault.resolve(url.searchParams.get("target") || "") })
      if (url.pathname === "/api/schedule") return send(200, await schedule())
      if (url.pathname === "/api/jobs") return send(200, [...jobs.values()])
      if (url.pathname === "/api/file") {
        const full = await vault.file(url.searchParams.get("path"))
        const extension = path.extname(full).toLowerCase()
        const type = mime[extension] || "application/octet-stream"
        if (
          !mime[extension] ||
          extension === ".html" ||
          extension === ".js" ||
          extension === ".css"
        )
          res.setHeader(
            "Content-Disposition",
            "attachment; filename*=UTF-8''" + encodeURIComponent(path.basename(full)),
          )
        const stat = await fs.stat(full)
        if (stat.size > 100 * 1024 * 1024)
          return send(413, { error: "Open files larger than 100 MB directly from the vault." })
        res.setHeader("Content-Security-Policy", "default-src 'none'; sandbox")
        return send(200, await fs.readFile(full), type)
      }
      if (url.pathname === "/" || url.pathname === "/index.html")
        return send(200, await fs.readFile(path.join(UI, "index.html")), "text/html")
      if (["/app.js", "/style.css"].includes(url.pathname))
        return send(
          200,
          await fs.readFile(path.join(UI, url.pathname.slice(1))),
          mime[path.extname(url.pathname)],
        )
      // Serve the existing published Quartz build under its configured /vault base.
      if (url.pathname === "/vault" || url.pathname.startsWith("/vault/")) {
        // Keep Quartz's scripts on a different origin from private vault APIs.
        res.writeHead(302, {
          Location:
            "http://127.0.0.1:" +
            (process.env.VAULT_QUARTZ_PORT || 4174) +
            url.pathname +
            url.search,
        })
        return res.end()
      }
      return send(404, { error: "Page not found" })
    } catch (error) {
      const notFound = error.code === "ENOENT"
      send(notFound ? 404 : 400, {
        error: notFound
          ? "This file is no longer available. Refresh and try again."
          : "Unable to open this request. Choose a vault file or refresh and retry.",
      })
    }
  })
  server.requestTimeout = 30000
  server.headersTimeout = 10000
  return server
}

export function createQuartzPreview({ root = ROOT } = {}) {
  const server = http.createServer(async (req, res) => {
    res.setHeader("X-Content-Type-Options", "nosniff")
    res.setHeader("Referrer-Policy", "no-referrer")
    try {
      const port = server.address()?.port
      if (![`127.0.0.1:${port}`, `localhost:${port}`].includes(req.headers.host)) {
        res.writeHead(403)
        return res.end()
      }
      if (!["GET", "HEAD"].includes(req.method)) {
        res.writeHead(405)
        return res.end()
      }
      const url = new URL(req.url, "http://" + req.headers.host)
      if (!url.pathname.startsWith("/vault/")) {
        res.writeHead(302, { Location: "/vault/" })
        return res.end()
      }
      let relative = decodeURIComponent(url.pathname.slice("/vault/".length)) || "index.html"
      if (!path.extname(relative)) relative += ".html"
      const publicRoot = await fs.realpath(path.join(root, "public"))
      const full = await fs.realpath(path.join(publicRoot, relative))
      if (!full.startsWith(publicRoot + path.sep)) {
        res.writeHead(403)
        return res.end()
      }
      res.writeHead(200, {
        "Content-Type":
          mime[path.extname(full)] ||
          { ".svg": "image/svg+xml", ".json": "application/json" }[path.extname(full)] ||
          "application/octet-stream",
      })
      res.end(await fs.readFile(full))
    } catch {
      res.writeHead(404)
      res.end("Build Quartz with npm run build, then refresh this page.")
    }
  })
  return server
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.umask(0o077)
  const port = Number(process.env.VAULT_DASHBOARD_PORT || 4173)
  const server = createDashboard()
  const quartz = createQuartzPreview()
  quartz.listen(Number(process.env.VAULT_QUARTZ_PORT || 4174), "127.0.0.1")
  server.listen(port, "127.0.0.1", () =>
    console.log(`Vault workspace: http://127.0.0.1:${server.address().port} (local only)`),
  )
  const failed = (error) => {
    console.error(
      error.code === "EADDRINUSE"
        ? "Workspace port is in use. Set VAULT_DASHBOARD_PORT and VAULT_QUARTZ_PORT to unused ports."
        : "Workspace could not start.",
    )
    server.close()
    quartz.close()
    process.exitCode = 1
  }
  server.on("error", failed)
  quartz.on("error", failed)
}
