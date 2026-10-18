import assert from "node:assert/strict"
import { test } from "node:test"
import { remark } from "remark"
import { VFile } from "vfile"
import type { Root } from "mdast"
import type { BuildCtx } from "../../util/ctx"
import { Excalidraw } from "./excalidraw"

test("ordinary drawing links keep their note target when no SVG export exists", async () => {
  const processor = remark().use(Excalidraw().markdownPlugins!({} as BuildCtx))
  const tree = processor.parse("[Drawing](/Excalidraw/example.excalidraw.md)")
  const result = (await processor.run(tree, new VFile({ path: "index.md" }))) as Root
  assert.equal(result.children[0].type, "paragraph")
  const paragraph = result.children[0]
  if (paragraph.type !== "paragraph") throw new Error("Expected paragraph")
  const link = paragraph.children[0]
  assert.equal(link.type, "link")
  if (link.type !== "link") throw new Error("Expected link")
  assert.equal(link.url, "/Excalidraw/example.excalidraw.md")
})
