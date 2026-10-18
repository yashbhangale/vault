import path from "node:path"

/** Resolve private-note attachments, including OneNote assets placed at vault root. */
export function referencedAttachments(text, notePath, assets) {
  const targets = [
    ...text.matchAll(/!?\[\[([^\]\n]+)\]\]/g),
    ...text.matchAll(/!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^)\n]+)\s*\)/g),
    ...text.matchAll(/^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)/gm),
    ...text.matchAll(/(?:src|href)=["']([^"']+)["']/gi),
  ].map((match) => match[1])
  const found = new Set()
  for (let raw of targets) {
    raw = raw
      .split("|")[0]
      .trim()
      .replace(/^<|>$/g, "")
      .replace(/\s+["'][\s\S]*$/, "")
    if (/^[a-z][a-z\d+.-]*:/i.test(raw) || raw.startsWith("//")) continue
    raw = raw.split("#")[0]
    try {
      raw = decodeURIComponent(raw)
    } catch {
      continue
    }
    if (!raw) continue
    const relative = path.posix.normalize(path.posix.join(path.posix.dirname(notePath), raw))
    const absolute = raw.replace(/^\//, "")
    for (const asset of assets) {
      if (asset === relative || asset === absolute || asset.endsWith(`/${absolute}`))
        found.add(asset)
    }
  }
  return found
}
