import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"
import knowledgebase from "./scripts/knowledgebase/config.json"
import privateAssets from "./scripts/knowledgebase/private-assets.json"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Yash’s Knowledge Base",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "en-US",
    baseUrl: "yashbhangale.github.io/vault/",
    // Folder exclusions protect notes AND attachments. Note flags protect Markdown only.
    ignorePatterns: [
      ...knowledgebase.ignorePatterns,
      ...privateAssets,
      ...knowledgebase.privateFolders.map((folder) => `${folder}/**`),
    ],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#f5f2e9",
          lightgray: "#dedbd2",
          gray: "#716e65",
          darkgray: "#44443f",
          dark: "#111315",
          secondary: "#805900",
          tertiary: "#176b6b",
          highlight: "rgba(128, 89, 0, 0.09)",
          textHighlight: "#ffdc70",
        },
        darkMode: {
          light: "#111315",
          lightgray: "#2e3438",
          gray: "#9a9f9d",
          darkgray: "#c2c2b9",
          dark: "#e8e3d5",
          secondary: "#ffbc00",
          tertiary: "#56cece",
          highlight: "rgba(255, 188, 0, 0.10)",
          textHighlight: "#ffbc0040",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
      Plugin.Excalidraw({
        width: "100%",
        center: true,
      }),
    ],
    filters: [Plugin.RemoveDrafts(), Plugin.RemovePrivate()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      //Plugin.CustomOgImages(),
    ],
  },
}

export default config
