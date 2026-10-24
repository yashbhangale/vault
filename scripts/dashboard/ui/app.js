const main = document.querySelector("#main")
const notice = document.querySelector("#notice")
const search = document.querySelector("#search")
let context,
  overview,
  poller,
  refreshTimer,
  currentPath = "",
  captureDraft = ""
let sourceLimit = 50
const sourceNames = {
  calendar: "Calendar",
  tasks: "Tasks",
  gmail: "Mail",
  youtube: "Saved videos",
  "youtube-history": "Imported watch history",
}
const escape = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c],
  )
const noteURL = (path) => "#note=" + encodeURIComponent(path)
const fileURL = (path) => "/api/file?path=" + encodeURIComponent(path)
const safeURL = (value) => {
  try {
    const url = new URL(value)
    return ["http:", "https:"].includes(url.protocol) ? escape(url.href) : ""
  } catch {
    return ""
  }
}
const external = (url, label) =>
  safeURL(url)
    ? `<a href="${safeURL(url)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>`
    : escape(label)
const when = (value, options = {}) => {
  const parsed = new Date(value)
  return value && !Number.isNaN(parsed.getTime())
    ? new Intl.DateTimeFormat("en-IN", { timeZone: "Asia/Kolkata", ...options }).format(parsed)
    : "Not checked yet"
}
const updated = (value) =>
  when(value, { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })
const empty = (text) => `<p class="empty">${escape(text)}</p>`

async function api(url, body) {
  const response = await fetch(
    url,
    body === undefined
      ? {}
      : {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-Vault-Token": context.token },
          body: JSON.stringify(body),
        },
  )
  const value = await response.json()
  if (!response.ok)
    throw new Error(value.error || "Could not load this view. Refresh and try again.")
  return value
}
function message(text, error = false) {
  notice.textContent = text
  notice.className = error ? "error" : ""
  notice.hidden = false
}
function heading(title, description, date = false) {
  return `<header class="page-heading"><div><h1>${escape(title)}</h1><p>${escape(description)}</p></div>${date ? `<div class="date-stamp">${when(new Date(), { weekday: "long", day: "numeric", month: "long" })}<br>Asia / Kolkata</div>` : ""}</header>`
}
function section(title, href, label = "View all") {
  return `<div class="section-heading"><h2>${escape(title)}</h2>${href ? `<a href="${href}">${escape(label)}</a>` : ""}</div>`
}
function sourceInfo(name) {
  const row = overview.sources[name]
  if (!row) return empty("This source has not been configured yet.")
  return `<div class="source-intro"><span class="status-dot"></span><span>${escape(row.status)}${row.stale ? " · stale" : ""} · Last checked ${updated(row.checked)}</span>${row.raw ? `<a href="${noteURL(row.raw)}">Read source snapshot</a>` : ""}</div>${row.error ? `<p class="scope">${escape(row.error)}</p>` : ""}${row.truncated ? '<p class="scope">This capture reached its item limit and is incomplete.</p>' : ""}`
}
function onDay(event) {
  const start = event.start || {},
    end = event.end || {}
  if (start.date) return start.date <= overview.date && (end.date || start.date) > overview.date
  if (!start.dateTime || !end.dateTime) return false
  const lower = new Date(overview.date + "T00:00:00+05:30").getTime()
  return (
    new Date(start.dateTime).getTime() < lower + 86400000 &&
    new Date(end.dateTime).getTime() > lower
  )
}
function agendaRows(rows) {
  if (!rows.length)
    return empty("No events in this view. Calendar entries are plans; attendance is not inferred.")
  return (
    '<ul class="items">' +
    [...rows]
      .sort((a, b) =>
        String(a.start?.dateTime || a.start?.date).localeCompare(
          String(b.start?.dateTime || b.start?.date),
        ),
      )
      .map(
        (row) =>
          `<li class="item"><div class="time-label">${row.start?.date ? "All day" : when(row.start?.dateTime, { hour: "numeric", minute: "2-digit" })}</div><div class="item-main"><div class="item-title">${external(row.htmlLink, row.summary || "Untitled event")}</div><p>${row.start?.date || when(row.start?.dateTime, { day: "numeric", month: "short" })}${row.location ? " · " + escape(row.location) : ""}</p></div></li>`,
      )
      .join("") +
    "</ul>"
  )
}
function taskRows(rows) {
  if (!rows.length)
    return empty("No tasks match this view. Only task statuses reported by Google are shown.")
  return (
    '<ul class="items">' +
    rows
      .map(
        (row) =>
          `<li class="item"><span class="task-status ${row.status === "completed" ? "done" : ""}" aria-hidden="true"></span><div class="item-main"><div class="item-title">${row.webViewLink ? external(row.webViewLink, row.title || "Untitled task") : escape(row.title || "Untitled task")}</div><p>${escape(row.list_title || "Tasks")}${row.notes ? " · " + escape(row.notes) : ""}${row.status === "completed" ? " · Completed" : ""}</p></div><span class="due ${row.due && row.due.slice(0, 10) < overview.date && row.status !== "completed" ? "overdue" : ""}">${row.due ? escape(row.due.slice(0, 10)) : "No due date"}</span></li>`,
      )
      .join("") +
    "</ul>"
  )
}
function noteRows(files) {
  return files.length
    ? '<ul class="items note-list">' +
        files
          .map(
            (file) =>
              `<li class="item"><div class="item-main"><a class="item-title" href="${noteURL(file.path)}">${escape(file.title)}</a><div class="folder-label">${escape(file.folder)} · File updated ${updated(file.updated)}</div></div></li>`,
          )
          .join("") +
        "</ul>"
    : empty("Your notes will appear here once files are captured or written.")
}
function today() {
  const agenda = overview.sources.calendar?.items || []
  const tasks = [...(overview.sources.tasks?.items || [])]
    .filter((row) => row.status !== "completed")
    .sort((a, b) => (a.due || "9999").localeCompare(b.due || "9999"))
  const strip = Object.entries(overview.sources)
    .map(
      ([key, row]) =>
        `<a href="#${key === "youtube-history" ? "youtube" : key}" class="${row.stale || row.status !== "ok" ? "warning" : ""}">${escape(sourceNames[key])} <strong>${row.items.length}</strong>${row.stale ? " · stale" : row.status !== "ok" ? " · " + escape(row.status) : ""}</a>`,
    )
    .join("")
  main.innerHTML =
    heading(
      "Your day, connected.",
      "A place to see what’s coming, find what you know, and capture what matters.",
      true,
    ) +
    `<div class="source-strip">${strip}</div><div class="today-grid"><div class="today-column"><section class="today-agenda">${section("On your calendar", "#calendar")}${agendaRows(agenda.filter(onDay))}</section><section class="today-recent lower-section">${section("Recent notes", "#library")}${noteRows(overview.recent.slice(0, 4))}</section></div><div class="today-column"><section class="today-tasks">${section("Open tasks", "#tasks", `View all ${tasks.length}`)}${taskRows(tasks.slice(0, 7))}</section><section class="today-next lower-section">${section("Keep the day moving", "#capture", "Capture a thought")}<p class="empty">Choose your next action from your tasks. Record what actually happened in your journal, then turn useful captures into knowledge.</p><a href="#journal">Open your journal</a></section></div></div>`
}
async function library(folder = "", query = "") {
  const result = await api("/api/notes?" + new URLSearchParams({ folder, q: query }))
  const buttons = [
    { name: "", count: result.folders.reduce((sum, folder) => sum + folder.count, 0) },
    ...result.folders,
  ]
    .map(
      (row) =>
        `<button data-folder="${escape(row.name)}" class="${folder === row.name ? "active" : ""}">${escape(row.name || "Everything")}<span>${row.count}</span></button>`,
    )
    .join("")
  main.innerHTML =
    heading(
      folder === "03 Journal" ? "Your journal" : "Everything, within reach.",
      query
        ? `Search results for “${query}”. Titles, paths and Markdown content are searched locally.`
        : "Browse every vault area. Originals stay intact; each file opens in the reader.",
    ) +
    `<div class="library-layout"><nav class="folder-nav" aria-label="Vault folders">${buttons}</nav><section><div class="toolbar"><label for="library-query" class="sr-only">Find a note</label><input id="library-query" type="search" placeholder="Find a note, topic, or phrase" value="${escape(query)}"><span class="result-count">${result.total} files${result.truncated ? " · first 1,000 shown" : ""}</span></div><div id="file-results">${result.files.length ? result.files.map((file) => `<div class="file-row"><a href="${noteURL(file.path)}">${escape(file.title)}<small>${escape(file.path)} · ${escape(file.ext.slice(1).toUpperCase())}</small></a><time datetime="${file.updated}">${when(file.updated, { day: "numeric", month: "short" })}</time></div>`).join("") : empty("No files match this search. Try a shorter phrase or choose another folder.")}</div></section></div>`
  document.querySelectorAll("[data-folder]").forEach((button) =>
    button.addEventListener("click", () => {
      location.hash = "library?" + new URLSearchParams({ folder: button.dataset.folder, q: query })
    }),
  )
  const input = document.querySelector("#library-query")
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter")
      location.hash = "library?" + new URLSearchParams({ folder, q: input.value.trim() })
  })
}
function sourceView(name) {
  const row = overview.sources[name] || { items: [], scope: {} }
  const descriptions = {
    calendar:
      "Scheduled events from your configured calendars. Plans are separate from completed activity.",
    tasks:
      "Your Google Tasks, including completed tasks. Make changes in Google Tasks; this collector reads them.",
    gmail:
      "Captured message headers and snippets. Open Gmail to read a thread, reply, or take action.",
    youtube:
      "Videos saved in your configured playlists. A saved video does not imply it was watched or learned.",
  }
  const appLink = {
    calendar: ["https://calendar.google.com", "Open Google Calendar"],
    tasks: ["https://tasks.google.com", "Open Google Tasks"],
    gmail: ["https://mail.google.com", "Open Gmail"],
    youtube: ["https://www.youtube.com/feed/playlists", "Open YouTube playlists"],
  }[name]
  main.innerHTML =
    heading(sourceNames[name], descriptions[name]) +
    sourceInfo(name) +
    `<div class="toolbar"><label class="sr-only" for="source-query">Filter ${escape(sourceNames[name])}</label><input id="source-query" type="search" placeholder="Filter ${escape(sourceNames[name].toLowerCase())}" autocomplete="off">${external(...appLink)}</div><div id="source-filters" class="filters"></div><div id="source-count" class="scope"></div><div id="source-results"></div><button id="load-more" hidden>Show more</button>`
  const filters =
    name === "tasks"
      ? ["Open", "Completed", "All"]
      : name === "calendar"
        ? ["Today", "Captured window"]
        : name === "gmail"
          ? ["All messages", "Unread"]
          : ["All saved videos"]
  let selected = filters[0]
  sourceLimit = 50
  const draw = () => {
    const term = document.querySelector("#source-query").value.toLocaleLowerCase()
    let rows = row.items.filter((item) => JSON.stringify(item).toLocaleLowerCase().includes(term))
    if (name === "tasks") {
      rows = rows
        .filter(
          (item) =>
            selected === "All" || (item.status === "completed") === (selected === "Completed"),
        )
        .sort((a, b) => (a.due || "9999").localeCompare(b.due || "9999"))
    } else if (name === "calendar") {
      if (selected === "Today") rows = rows.filter(onDay)
    } else if (name === "gmail") {
      if (selected === "Unread") rows = rows.filter((item) => item.labelIds?.includes("UNREAD"))
      rows.sort((a, b) => Number(b.internalDate || 0) - Number(a.internalDate || 0))
    } else rows.sort((a, b) => (b.added_at || "").localeCompare(a.added_at || ""))
    document.querySelector("#source-count").textContent =
      `${rows.length} records in this view${row.scope.query ? " · Query: " + row.scope.query : ""}. Last checked ${updated(row.checked)}.`
    const shown = rows.slice(0, sourceLimit)
    const html =
      name === "tasks"
        ? taskRows(shown)
        : name === "calendar"
          ? agendaRows(shown)
          : shown.length
            ? '<ul class="items">' +
              shown
                .map((item) =>
                  name === "gmail"
                    ? `<li class="item"><div class="item-main"><div class="item-title">${external("https://mail.google.com/mail/#all/" + encodeURIComponent(item.threadId || item.id), item.title || "No subject")}</div><p>${escape(item.from || "Sender unavailable")} · ${updated(Number(item.internalDate))}</p><p>${escape(item.snippet || "No message snippet was returned.")}</p></div></li>`
                    : `<li class="item"><div class="item-main"><div class="item-title">${external("https://www.youtube.com/watch?v=" + encodeURIComponent(item.video_id || ""), item.title || "Unavailable video")}</div><p>${escape(item.channel || "Channel not supplied")} · Saved ${updated(item.added_at)}</p></div></li>`,
                )
                .join("") +
              "</ul>"
            : empty("No captured records match this view. Check the filters or refresh the source.")
    document.querySelector("#source-results").innerHTML = html
    document.querySelector("#load-more").hidden = rows.length <= sourceLimit
    document.querySelector("#source-filters").innerHTML = filters
      .map(
        (filter) =>
          `<button class="${filter === selected ? "active" : ""}" data-filter="${filter}">${filter}</button>`,
      )
      .join("")
    document.querySelectorAll("[data-filter]").forEach((button) =>
      button.addEventListener("click", () => {
        selected = button.dataset.filter
        sourceLimit = 50
        draw()
      }),
    )
  }
  document.querySelector("#source-query").addEventListener("input", () => {
    sourceLimit = 50
    draw()
  })
  document.querySelector("#load-more").addEventListener("click", () => {
    sourceLimit += 50
    draw()
  })
  draw()
}
async function reader(path) {
  const note = await api("/api/note?" + new URLSearchParams({ path }))
  currentPath = path
  const file = fileURL(path)
  let body
  if (note.media) {
    const ext = path.split(".").pop().toLowerCase()
    body = `<div class="media-view">${["png", "jpg", "jpeg", "gif", "webp"].includes(ext) ? `<img src="${file}" alt="${escape(note.title)}">` : ["mp3", "ogg", "m4a", "wav", "opus"].includes(ext) ? `<audio controls src="${file}"></audio>` : ["mp4", "webm", "mov"].includes(ext) ? `<video controls src="${file}"></video>` : empty("Open or download this attachment to view it in its native application.")}</div>`
  } else
    body = note.markdown
      ? `<article class="reader">${note.html}</article>`
      : `<pre class="source-code">${escape(note.text)}</pre>`
  main.innerHTML =
    `<div class="reader-toolbar"><a href="#library">Back to all notes</a><div>${!note.media ? '<button id="view-source">View Markdown source</button>' : ""}<a href="${file}" download>Download original</a></div></div>` +
    heading(note.title, "") +
    `<p class="reader-path">${escape(path)}</p><div class="metadata">${Object.entries(
      note.metadata || {},
    )
      .map(([key, value]) => `<span>${escape(key.replaceAll("_", " "))}: ${escape(value)}</span>`)
      .join("")}</div><div id="note-content">${body}</div>`
  let source = false
  document.querySelector("#view-source")?.addEventListener("click", (event) => {
    source = !source
    document.querySelector("#note-content").innerHTML = source
      ? `<pre class="source-code">${escape(note.text)}</pre>`
      : body
    event.target.textContent = source ? "Read rendered note" : "View Markdown source"
  })
}
function captureView() {
  main.innerHTML =
    heading(
      "Catch the thought.",
      "Write it once. Keep the original, create a source-linked record, and find it again later.",
    ) +
    `<form id="capture-form" class="capture-form"><label for="capture-text">What do you want to remember?</label><textarea id="capture-text" maxlength="100000" placeholder="An idea, something you learned, a decision, a useful link…" required>${escape(captureDraft)}</textarea><div class="form-footer"><p>Saved to Raw → Manual Captures, then processed locally.<br>Your existing sources are never overwritten.</p><button class="primary" type="submit">Save capture</button></div></form>`
  const input = document.querySelector("#capture-text")
  input.addEventListener("input", () => {
    captureDraft = input.value
  })
  document.querySelector("#capture-form").addEventListener("submit", async (event) => {
    event.preventDefault()
    const button = event.submitter || event.target.querySelector("button")
    button.disabled = true
    try {
      const saved = await action("/api/capture", { text: input.value })
      if (saved) {
        captureDraft = ""
        if (document.querySelector("#capture-text"))
          document.querySelector("#capture-text").value = ""
      }
    } finally {
      button.disabled = false
    }
  })
}
async function syncView() {
  const schedule = await api("/api/schedule")
  const jobs = await api("/api/jobs")
  main.innerHTML =
    heading(
      "Keep everything in sync.",
      "Check what was captured, refresh a source, or pause the hourly collector.",
    ) +
    `<div class="table-wrap"><table class="sync-table"><thead><tr><th>Source</th><th>Capture health</th><th>Records</th><th>Last successful check</th><th>Action</th></tr></thead><tbody>${Object.entries(
      overview.sources,
    )
      .map(
        ([name, row]) =>
          `<tr><td>${escape(sourceNames[name])}</td><td class="${row.status === "ok" && !row.stale ? "good" : "bad"}">${escape(row.status)}${row.stale ? " · stale" : ""}</td><td>${row.items.length}</td><td>${updated(row.checked)}</td><td>${name === "youtube-history" ? "Manual import" : `<button data-sync="${name}">Refresh</button>`}</td></tr>`,
      )
      .join(
        "",
      )}</tbody></table></div><div class="schedule-row"><div><h2>Hourly collection is ${schedule.active ? "on" : "paused"}</h2><p>Runs while this computer and its user services are available.<br>Your website views update from local files; no rebuild is needed for new captures.</p></div><button id="schedule-toggle">${schedule.active ? "Pause hourly sync" : "Resume hourly sync"}</button></div><div class="lower-section">${section("Recent actions")}<ul class="job-list">${
      jobs.length
        ? jobs
            .reverse()
            .map(
              (job) =>
                `<li>${escape(job.kind)}<span>${escape(job.status)} · ${updated(job.started)}</span></li>`,
            )
            .join("")
        : "<li>No actions run from this dashboard yet.</li>"
    }</ul></div><p class="scope">Google connections are read-only. Send mail, change events, or complete tasks in the original app. Watch history uses a separate Takeout import. Credentials and internal manifests are not served by this workspace.</p>`
  document
    .querySelectorAll("[data-sync]")
    .forEach((button) =>
      button.addEventListener("click", () =>
        action("/api/sync", { sources: [button.dataset.sync] }),
      ),
    )
  document
    .querySelector("#schedule-toggle")
    .addEventListener("click", () => action("/api/schedule", { enabled: !schedule.active }))
}
async function action(url, body) {
  if (poller) {
    message("An action is already running. Wait for it to finish.")
    return
  }
  const syncButton = document.querySelector("#sync-now")
  try {
    const job = await api(url, body)
    message(
      `${job.kind} is running. You can keep browsing; source refreshes can take a few minutes.`,
    )
    syncButton.disabled = true
    return await new Promise((resolve) => {
      poller = setInterval(async () => {
        try {
          const jobs = await api("/api/jobs"),
            row = jobs.find((row) => row.id === job.id)
          if (!row || row.status === "running") return
          clearInterval(poller)
          poller = null
          syncButton.disabled = false
          if (row.status === "error") {
            message(row.error, true)
            resolve(false)
          } else {
            message(
              typeof row.result === "string"
                ? row.result
                : row.result?.message || "Action complete.",
            )
            if (row.result?.path) location.hash = "note=" + encodeURIComponent(row.result.path)
            overview = await api("/api/overview")
            updateStatus()
            if (!["capture", "note"].includes(viewName())) await route()
            resolve(true)
          }
        } catch {
          clearInterval(poller)
          poller = null
          syncButton.disabled = false
          message("Connection interrupted. Refresh the page to check the action.", true)
          resolve(false)
        }
      }, 1500)
    })
  } catch (error) {
    message(error.message, true)
    return false
  }
}
function viewName() {
  const value = location.hash.slice(1)
  return value.startsWith("note=") ? "note" : value.split("?")[0] || "today"
}
function updateStatus() {
  document.querySelector("#nav-count").textContent = overview.files.toLocaleString("en-IN")
  const connected = Object.values(overview.sources).filter(
    (source) => source.status === "ok" && !source.stale,
  ).length
  document.querySelector("#footer-status").textContent =
    `${connected} sources current · ${overview.files.toLocaleString("en-IN")} vault files · Local only`
}
async function route() {
  const view = viewName(),
    raw = location.hash.slice(1),
    params = new URLSearchParams(raw.split("?")[1] || "")
  document.querySelectorAll("[data-view]").forEach((link) => {
    if (link.dataset.view === view || (view === "note" && link.dataset.view === "library"))
      link.setAttribute("aria-current", "page")
    else link.removeAttribute("aria-current")
  })
  main.setAttribute("aria-busy", "true")
  try {
    if (view === "today") today()
    else if (view === "library") await library(params.get("folder") || "", params.get("q") || "")
    else if (view === "journal") await library("03 Journal")
    else if (view === "note") await reader(decodeURIComponent(raw.slice(5)))
    else if (["calendar", "tasks", "gmail", "youtube"].includes(view)) sourceView(view)
    else if (view === "capture") captureView()
    else if (view === "sync") await syncView()
    else {
      main.innerHTML = heading(
        "This view is not available.",
        "Choose Today or All notes to continue.",
      )
    }
    document.title = `${view === "note" ? currentPath.split("/").pop().replace(/\.md$/, "") : sourceNames[view] || (view === "library" ? "All notes" : view[0].toUpperCase() + view.slice(1))} · Yash’s workspace`
  } catch (error) {
    main.innerHTML =
      heading("Couldn’t open this view.", error.message) + '<a href="#today">Return to Today</a>'
  } finally {
    main.removeAttribute("aria-busy")
  }
}
document.querySelector("#global-search").addEventListener("submit", (event) => {
  event.preventDefault()
  location.hash = "library?" + new URLSearchParams({ q: search.value.trim() })
})
document.querySelector(".skip-link").addEventListener("click", (event) => {
  event.preventDefault()
  main.focus()
  main.scrollIntoView({ block: "start" })
})
document.querySelector("#sync-now").addEventListener("click", () => action("/api/sync", {}))
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault()
    search.focus()
  }
})
window.addEventListener("hashchange", () => {
  void route()
})
const themeToggle = document.querySelector("#theme-toggle")
let theme = localStorage.getItem("vault-theme") || "dark"
function applyTheme() {
  document.documentElement.dataset.theme = theme
  themeToggle.textContent = theme === "dark" ? "Light theme" : "Dark theme"
  themeToggle.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`)
}
themeToggle.addEventListener("click", () => {
  theme = theme === "dark" ? "light" : "dark"
  localStorage.setItem("vault-theme", theme)
  applyTheme()
})
applyTheme()
try {
  context = await api("/api/context")
  overview = await api("/api/overview")
  updateStatus()
  await route()
  refreshTimer = setInterval(async () => {
    try {
      overview = await api("/api/overview")
      updateStatus()
      if (viewName() === "today") today()
    } catch {
      document.querySelector("#footer-status").textContent =
        "Connection interrupted · Refresh to reconnect"
    }
  }, 60000)
} catch (error) {
  main.innerHTML = heading(
    "The local workspace is unavailable.",
    error.message + " Start it with npm run dashboard.",
  )
}
