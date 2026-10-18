import assert from "node:assert/strict"
import { test } from "node:test"
import { VFile } from "vfile"
import type { Root } from "hast"
import type { BuildCtx } from "../../util/ctx"
import { RemovePrivate } from "./private"

test("RemovePrivate honors boolean and serialized flags without requiring explicit opt-in", () => {
  const plugin = RemovePrivate()
  const publish = (flags: Record<string, unknown>) => {
    const file = new VFile()
    file.data.frontmatter = { title: "Fixture", ...flags }
    return plugin.shouldPublish({} as BuildCtx, [{ type: "root", children: [] } as Root, file])
  }
  for (const flags of [
    { private: true },
    { private: "true" },
    { publish: false },
    { publish: "false" },
    { visibility: "private" },
  ]) {
    assert.equal(publish(flags), false)
  }
  assert.equal(publish({}), true)
  assert.equal(publish({ publish: true }), true)
  assert.equal(publish({ private: false, publish: "true" }), true)
})
