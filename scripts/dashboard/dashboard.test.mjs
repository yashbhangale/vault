import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import os from "node:os"
import http from "node:http"
import { createDashboard, createQuartzPreview } from "./server.mjs"

async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "vault-dashboard-"))
  const put = async (relative, content) => {
    const file = path.join(root, relative)
    await fs.mkdir(path.dirname(file), { recursive: true })
    await fs.writeFile(file, content)
  }
  await put(
    "content/05 Knowledge/Pods.md",
    "---\ntitle: Kubernetes pods\n---\n# Pods\n\nA useful concept. [[03 Journal/Daily/2026-10-25|Daily source]]\n\n![[01 Raw/photo.png]]\n\n<script>alert(1)</script>\n\n[bad](javascript:alert%281%29)",
  )
  await put(
    "content/03 Journal/Daily/2026-10-25.md",
    "# My day\nAn uncommonneedle in a private journal.",
  )
  await put("content/01 Raw/photo.png", Buffer.from([1, 2, 3]))
  await put("content/00 System/Manifests/token.json", '{"secret":"SHOULD NEVER APPEAR"}')
  await put("content/00 System/Manifests/google-capture.json", "{}")
  await put("private/google/token.json", '{"secret":"PRIVATE TOKEN"}')
  await put("public/index.html", "<!doctype html><title>Quartz fixture</title><h1>Knowledge</h1>")
  await fs.symlink(
    path.join(root, "private/google/token.json"),
    path.join(root, "content/01 Raw/outside.json"),
  )
  await fs.symlink(
    path.join(root, "content/00 System/Manifests/token.json"),
    path.join(root, "content/01 Raw/manifest.json"),
  )
  const calls = []
  const run = async (file, args) => {
    calls.push([file, args])
    return { stdout: args.includes("is-active") ? "active\n" : "{}" }
  }
  const server = createDashboard({ root, run })
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve))
  const base = "http://127.0.0.1:" + server.address().port
  t.after(async () => {
    server.closeAllConnections()
    await new Promise((resolve) => server.close(resolve))
    await fs.rm(root, { recursive: true, force: true })
  })
  const get = async (url) => (await fetch(base + url)).json()
  const context = await get("/api/context")
  const post = (url, body, headers = {}) =>
    fetch(base + url, {
      method: "POST",
      headers: {
        Origin: base,
        "X-Vault-Token": context.token,
        "Content-Type": "application/json",
        ...headers,
      },
      body: JSON.stringify(body),
    })
  return { root, base, get, post, calls, put }
}

test("lists public and private notes without credentials, manifests, or symlinks", async (t) => {
  const { get } = await fixture(t)
  const listing = await get("/api/notes")
  assert.ok(listing.files.some((file) => file.path.startsWith("03 Journal/")))
  assert.ok(listing.files.some((file) => file.path.startsWith("01 Raw/")))
  assert.ok(!JSON.stringify(listing).includes("Manifests"))
  assert.ok(!JSON.stringify(listing).includes("outside.json"))
})

test("direct requests cannot traverse paths or resolve symlinks to credentials", async (t) => {
  const { base } = await fixture(t)
  for (const file of [
    "../private/google/token.json",
    "01 Raw/../../private/google/token.json",
    "00 System/Manifests/token.json",
    "01 Raw/outside.json",
    "01 Raw/manifest.json",
  ]) {
    const response = await fetch(base + "/api/file?path=" + encodeURIComponent(file))
    assert.ok(response.status >= 400, file)
    assert.ok(!(await response.text()).includes("PRIVATE TOKEN"))
  }
})

test("reader escapes untrusted HTML, rejects javascript URLs and resolves vault links and images", async (t) => {
  const { get } = await fixture(t)
  const note = await get("/api/note?path=" + encodeURIComponent("05 Knowledge/Pods.md"))
  assert.equal(note.title, "Kubernetes pods")
  assert.ok(!note.html.includes("<script>"))
  assert.ok(!note.html.includes('href="javascript:'))
  assert.ok(note.html.includes("/#note=03%20Journal"))
  assert.ok(note.html.includes("/api/file?path=01%20Raw%2Fphoto.png"))
  assert.ok(note.html.includes("Daily source"))
})

test("full-text search finds journal content as well as filenames", async (t) => {
  const { get } = await fixture(t)
  const result = await get("/api/notes?q=uncommonneedle")
  assert.equal(result.total, 1)
  assert.equal(result.files[0].folder, "03 Journal")
})

test("cross-origin writes, missing tokens and rebinding hosts are blocked", async (t) => {
  const { base, post } = await fixture(t)
  assert.equal((await post("/api/sync", {}, { Origin: "https://evil.example" })).status, 403)
  assert.equal((await post("/api/sync", {}, { "X-Vault-Token": "" })).status, 403)
  const rawRequest = (headers) =>
    new Promise((resolve, reject) => {
      const request = http.get(base + "/api/context", { headers }, (response) => {
        response.resume()
        resolve(response.statusCode)
      })
      request.on("error", reject)
    })
  assert.equal(await rawRequest({ Host: "evil.example" }), 403)
  assert.equal(await rawRequest({ "Sec-Fetch-Site": "cross-site" }), 403)
})

test("a public-site link may open the shell but cannot read private API data", async (t) => {
  const { base } = await fixture(t)
  const headers = {
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
  }
  const request = (route) =>
    new Promise((resolve, reject) => {
      const call = http.get(base + route, { headers }, (response) => {
        let body = ""
        response.on("data", (chunk) => {
          body += chunk
        })
        response.on("end", () => resolve({ status: response.statusCode, body }))
      })
      call.on("error", reject)
    })
  const shell = await request("/")
  assert.equal(shell.status, 200)
  assert.ok(shell.body.includes("Opening your workspace"))
  assert.ok(!shell.body.includes("uncommonneedle"))
  assert.equal((await request("/api/context")).status, 403)
  assert.equal((await request("/api/overview")).status, 403)
})

test("sync only runs fixed commands with explicitly allowed sources", async (t) => {
  const { post, get, calls } = await fixture(t)
  assert.equal((await post("/api/sync", { sources: ["gmail;rm"] })).status, 400)
  const response = await post("/api/sync", { sources: ["tasks"] })
  assert.equal(response.status, 202)
  for (let attempt = 0; attempt < 20; attempt++) {
    if ((await get("/api/jobs"))[0].status !== "running") break
    await new Promise((resolve) => setTimeout(resolve, 5))
  }
  assert.equal((await get("/api/jobs"))[0].status, "done")
  assert.ok(calls.some(([, args]) => args.includes("sync") && args.includes("tasks")))
  assert.ok(calls.some(([, args]) => args.includes("index")))
})

test("missing captures have an explicit disconnected state rather than invented activity", async (t) => {
  const { get } = await fixture(t)
  const overview = await get("/api/overview")
  assert.equal(overview.sources.gmail.status, "not-connected")
  assert.deepEqual(overview.sources.gmail.items, [])
  assert.equal(overview.sources.gmail.stale, true)
})

test("unsafe attachments download rather than execute inline", async (t) => {
  const { put, base } = await fixture(t)
  await put("content/01 Raw/unsafe.svg", '<svg onload="alert(1)"></svg>')
  const response = await fetch(base + "/api/file?path=" + encodeURIComponent("01 Raw/unsafe.svg"))
  assert.equal(response.status, 200)
  assert.match(response.headers.get("content-disposition"), /^attachment/)
  assert.equal(response.headers.get("x-content-type-options"), "nosniff")
})

test("Quartz runs on a separate origin with only the filtered public build", async (t) => {
  const { root, base } = await fixture(t)
  const quartz = createQuartzPreview({ root })
  await new Promise((resolve) => quartz.listen(0, "127.0.0.1", resolve))
  t.after(async () => {
    quartz.closeAllConnections()
    await new Promise((resolve) => quartz.close(resolve))
  })
  const preview = "http://127.0.0.1:" + quartz.address().port
  const page = await fetch(preview + "/vault/")
  assert.equal(page.status, 200)
  assert.ok((await page.text()).includes("Quartz fixture"))
  assert.equal((await fetch(preview + "/vault/api/overview")).status, 404)
  const redirect = await fetch(base + "/vault/", { redirect: "manual" })
  assert.equal(redirect.status, 302)
  assert.ok(redirect.headers.get("location").includes(":4174/"))
})
