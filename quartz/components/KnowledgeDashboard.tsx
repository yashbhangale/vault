import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { Date, getDate } from "./Date"
import style from "./styles/knowledgeDashboard.scss"
// @ts-ignore
import script from "./scripts/knowledgeDashboard.inline"

const subjects = [
  ["cloud-devops", "Cloud & DevOps", "Infrastructure, containers, networking and operations."],
  ["programming", "Programming", "Languages, algorithms and software fundamentals."],
  ["projects", "Projects", "Things built, experiments and implementation notes."],
  ["product-ai", "Product & AI", "AI tools, product ideas and practical exploration."],
  ["personal-learning", "Personal learning", "Ideas, reading and lessons to return to."],
  ["drawings", "Drawings", "Visual explanations and working diagrams."],
]

export default (() => {
  const KnowledgeDashboard: QuartzComponent = ({
    fileData,
    allFiles,
    cfg,
  }: QuartzComponentProps) => {
    if (fileData.slug !== "index") return null
    // allFiles has already passed Quartz's publication filters. Never load private manifests here.
    const notes = allFiles.filter((f) => f.slug !== "index" && f.frontmatter?.type !== "index")
    const hubs = allFiles.filter((f) => String(f.slug).startsWith("05-Knowledge/Indexes/"))
    const href = (slug: FullSlug) => resolveRelative(fileData.slug!, slug)
    const recent = [...notes]
      .filter((f) => getDate(cfg, f))
      .sort(
        (a, b) =>
          getDate(cfg, b)!.getTime() - getDate(cfg, a)!.getTime() ||
          String(a.slug).localeCompare(String(b.slug)),
      )
      .slice(0, 5)
    const shortcuts = [
      ["DevOps", "05-Knowledge/Cloud-and-DevOps/DevOps"],
      ["Kubernetes", "05-Knowledge/Cloud-and-DevOps/Kubernates-notes/0.-kubernates-index"],
      ["Terraform", "05-Knowledge/Cloud-and-DevOps/Terraform/0.Terraform"],
      ["Java", "05-Knowledge/Programming/Java/1.-Basic-Java"],
    ]
      .map(([label, slug]) => ({ label, file: notes.find((f) => f.slug === slug) }))
      .filter((x) => x.file)
    const map = hubs.find((f) => String(f.slug).endsWith("/Sitemap"))
    return (
      <div class="knowledge-dashboard">
        <header class="dashboard-welcome">
          <h1>Your knowledge, within reach.</h1>
          <p>Find a note, pick up a subject, or return to what you were learning.</p>
        </header>
        <button
          class="dashboard-search"
          data-dashboard-search=""
          aria-label="Search all published notes"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.7"
            aria-hidden="true"
          >
            <circle cx="10.5" cy="10.5" r="6.5" />
            <path d="m16 16 5 5" />
          </svg>
          <span>Search your knowledge base</span>
          <kbd>Ctrl / ⌘ K</kbd>
        </button>
        <div class="dashboard-suggestions">
          <span>Try a topic</span>
          {["AWS", "Kubernetes", "Terraform", "Python"].map((term) => (
            <button data-dashboard-search={term}>{term}</button>
          ))}
        </div>
        <section class="dashboard-workspace" aria-label="Daily workspace">
          <div>
            <h2>Your daily workspace</h2>
            <p>Calendar, tasks, captures and your full vault. Available on your computer.</p>
          </div>
          <a href="http://127.0.0.1:4173/" rel="noreferrer">
            Open local workspace
          </a>
        </section>
        <div class="dashboard-columns">
          <section aria-labelledby="dashboard-topics">
            <div class="dashboard-section-heading">
              <h2 id="dashboard-topics">Browse by subject</h2>
              <span>{notes.length} published notes</span>
            </div>
            <ul class="dashboard-subjects">
              {subjects.map(([area, label, description]) => {
                const hub = hubs.find((f) => String(f.slug).endsWith("/" + area))
                const count = notes.filter((f) => f.frontmatter?.area === area).length
                if (!hub || !count) return null
                return (
                  <li>
                    <a class="internal" href={href(hub.slug!)}>
                      <div>
                        <h3>{label}</h3>
                        <p>{description}</p>
                      </div>
                      <span class="dashboard-count">
                        {count}
                        <svg
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="1.5"
                          aria-hidden="true"
                        >
                          <path d="M5 12h14m-6-6 6 6-6 6" />
                        </svg>
                      </span>
                    </a>
                  </li>
                )
              })}
            </ul>
            {map && (
              <a class="internal dashboard-map" href={href(map.slug!)}>
                Explore the full knowledge map
              </a>
            )}
          </section>
          <aside class="dashboard-return" aria-label="Quick access">
            <section>
              <h2>Start here</h2>
              <ul class="dashboard-shortcuts">
                {shortcuts.map(({ label, file }) => (
                  <li>
                    <a class="internal" href={href(file!.slug!)}>
                      {label}
                      <span>Open notes</span>
                    </a>
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h2>Recently updated</h2>
              <ul class="dashboard-recent">
                {recent.map((f) => (
                  <li>
                    <a class="internal" href={href(f.slug!)}>
                      {f.frontmatter?.title ?? f.slug}
                    </a>
                    <Date date={getDate(cfg, f)!} locale={cfg.locale} />
                  </li>
                ))}
              </ul>
              {recent.length === 0 && <p>Updated notes will appear here.</p>}
            </section>
          </aside>
        </div>
        <footer class="dashboard-footnote">
          <span>Built from your notes. Search runs in your browser.</span>
          <a href="https://github.com/yashbhangale">GitHub</a>
          <a href="https://hiremefor.cloud">Portfolio</a>
        </footer>
      </div>
    )
  }
  KnowledgeDashboard.css = style
  KnowledgeDashboard.afterDOMLoaded = script
  return KnowledgeDashboard
}) satisfies QuartzComponentConstructor
