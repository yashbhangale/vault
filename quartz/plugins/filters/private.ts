import { QuartzFilterPlugin } from "../types"

/** Apply explicit note-level privacy to HTML, search, RSS, tags and sitemap. */
export const RemovePrivate: QuartzFilterPlugin = () => ({
  name: "RemovePrivate",
  shouldPublish(_ctx, [_tree, file]) {
    const data: Record<string, unknown> = file.data.frontmatter ?? {}
    return (
      data.private !== true &&
      data.private !== "true" &&
      data.publish !== false &&
      data.publish !== "false" &&
      data.visibility !== "private"
    )
  },
})
