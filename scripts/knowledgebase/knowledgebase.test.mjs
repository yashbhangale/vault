import assert from "node:assert/strict"
import { test } from "node:test"
import fs from "node:fs/promises"
import os from "node:os"
import path from "node:path"
import { spawnSync } from "node:child_process"
import { fileURLToPath } from "node:url"
import { isPublic, ignorePatterns } from "./policy.mjs"
import { referencedAttachments } from "./attachments.mjs"
import { minimatch } from "minimatch"

const repo = fileURLToPath(new URL("../../", import.meta.url))
const config = JSON.parse(await fs.readFile(new URL("./config.json", import.meta.url), "utf8"))

test("publication policy excludes private pages, flags, and source-folder assets", () => {
  for (const folder of config.privateFolders) {
    assert.equal(isPublic({ path: `${folder}/note.md`, data: { publish: true } }, config), false)
    assert.ok(
      ignorePatterns(config).some((pattern) => minimatch(`${folder}/photos/photo.png`, pattern)),
    )
  }
  for (const data of [
    { publish: false },
    { publish: "false" },
    { private: true },
    { private: "true" },
    { visibility: "private" },
    { draft: true },
    { draft: "true" },
  ]) {
    assert.equal(isPublic({ path: "05 Knowledge/Programming/SQL/note.md", data }, config), false)
  }
  assert.equal(isPublic({ path: "05 Knowledge/Programming/SQL/note.md", data: {} }, config), true)
  assert.equal(
    isPublic({ path: "01 Raw/Manual Captures/gemini key creds example.md", data: {} }, config),
    false,
  )
})

test("private attachment discovery handles imports, root assets, encodings, and references", () => {
  const text =
    '![[photo.png|300]] ![ink](</ink image.svg>) [pdf](../files/a.pdf)\n<img src="/html.png">\n[image]: /reference.png\n![remote](https://example.com/public.png)'
  const assets = [
    "OneNote/photo.png",
    "ink image.svg",
    "files/a.pdf",
    "html.png",
    "reference.png",
    "public.png",
  ]
  assert.deepEqual(
    [...referencedAttachments(text, "OneNote/note.md", assets)].sort(),
    assets.filter((asset) => asset !== "public.png").sort(),
  )
  assert.deepEqual(
    [...referencedAttachments("![ink](/ink%20image.svg)", "note.md", assets)],
    ["ink image.svg"],
  )
})

test("refresh preserves existing properties and bodies, supports dry run, and is idempotent", async () => {
  const temp = await fs.mkdtemp(path.join(os.tmpdir(), "vault-kb-test-"))
  try {
    await fs.mkdir(path.join(temp, "scripts"))
    await fs.cp(
      path.join(repo, "scripts/knowledgebase"),
      path.join(temp, "scripts/knowledgebase"),
      { recursive: true },
    )
    await fs.symlink(path.join(repo, "node_modules"), path.join(temp, "node_modules"))
    await fs.mkdir(path.join(temp, "content/01 Raw/OneNote"), { recursive: true })
    await fs.mkdir(path.join(temp, "content/05 Knowledge/Programming/SQL"), { recursive: true })
    await fs.mkdir(path.join(temp, "reports"))
    const body = "\n# SQL\n\nKeep these bytes.\n"
    const original =
      "---\n# Keep my comment\ntitle: Custom title\ntags: [existing]\naliases: [SQL alias]\ncustom:\n  nested: value\n---\n" +
      body
    const note = path.join(temp, "content/05 Knowledge/Programming/SQL/note.md")
    await fs.writeFile(note, original)
    await fs.writeFile(
      path.join(temp, "content/01 Raw/OneNote/import.md"),
      "---\nonenote-id: abc-123\n---\n![[private.svg]]\n",
    )
    await fs.writeFile(path.join(temp, "content/private.svg"), "private asset")
    const run = (mode) =>
      spawnSync(process.execPath, ["scripts/knowledgebase/index.mjs", mode], {
        cwd: temp,
        encoding: "utf8",
      })
    assert.equal(run("audit").status, 0)
    assert.equal(await fs.readFile(note, "utf8"), original)
    assert.equal(run("check").status, 1)
    const refresh = run("refresh")
    assert.equal(refresh.status, 0, refresh.stderr)
    const updated = await fs.readFile(note, "utf8")
    assert.ok(updated.startsWith(original.slice(0, original.indexOf("\n---", 4) + 1)))
    assert.ok(updated.endsWith(`---\n${body}`))
    assert.ok(updated.includes('area: "programming"'))
    const imported = await fs.readFile(path.join(temp, "content/01 Raw/OneNote/import.md"), "utf8")
    assert.ok(imported.includes("onenote-id: abc-123"))
    assert.ok(!imported.includes('source: "onenote"'))
    assert.ok(
      !(
        await fs.readFile(path.join(temp, "content/05 Knowledge/Indexes/Sitemap.md"), "utf8")
      ).includes("import.md"),
    )
    assert.deepEqual(
      JSON.parse(
        await fs.readFile(path.join(temp, "scripts/knowledgebase/private-assets.json"), "utf8"),
      ),
      ["private.svg"],
    )
    const check = run("check")
    assert.equal(check.status, 0, check.stdout + check.stderr)
    assert.equal(await fs.readFile(note, "utf8"), updated)
    // Withholding the final note must also clear its previously generated hub.
    await fs.writeFile(note, updated.replace("---\n", "---\npublish: false\n"))
    const withheld = run("refresh")
    assert.equal(withheld.status, 0, withheld.stderr)
    const hub = await fs.readFile(
      path.join(temp, "content/05 Knowledge/Indexes/programming.md"),
      "utf8",
    )
    assert.ok(!hub.includes("Custom title"))
    assert.equal(run("check").status, 0)
  } finally {
    await fs.rm(temp, { recursive: true, force: true })
  }
})
