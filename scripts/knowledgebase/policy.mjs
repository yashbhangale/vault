import { minimatch } from "minimatch"

export function ignorePatterns(config) {
  return [...config.ignorePatterns, ...config.privateFolders.map((folder) => `${folder}/**`)]
}

export function isPublic(note, config) {
  const data = note.data
  return (
    !ignorePatterns(config).some((pattern) => minimatch(note.path, pattern, { dot: true })) &&
    ![true, "true"].includes(data.draft) &&
    ![true, "true"].includes(data.private) &&
    ![false, "false"].includes(data.publish) &&
    data.visibility !== "private"
  )
}
