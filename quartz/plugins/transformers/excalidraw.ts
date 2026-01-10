import { QuartzTransformerPlugin } from "../types"
import { Root } from "mdast"
import { visit } from "unist-util-visit"

export interface ExcalidrawOptions {
  // Width of the embedded Excalidraw drawing
  width?: string
  // Whether to center the drawing
  center?: boolean
}

const defaultOptions: ExcalidrawOptions = {
  width: "100%",
  center: true,
}

/**
 * Transformer plugin to handle Excalidraw files in Quartz
 * Converts .excalidraw.md files to display SVG exports
 */
export const Excalidraw: QuartzTransformerPlugin<Partial<ExcalidrawOptions> | undefined> = (
  userOpts,
) => {
  const opts = { ...defaultOptions, ...userOpts }

  return {
    name: "Excalidraw",
    markdownPlugins() {
      return [
        () => {
          return (tree: Root, file) => {
            const filePath = file.data.filePath as string

            // Check if this is an Excalidraw markdown file
            if (filePath?.endsWith(".excalidraw.md")) {
              // Look for frontmatter that indicates this is an Excalidraw file
              visit(tree, "yaml", (node: any) => {
                const content = node.value as string
                if (content.includes("excalidraw-plugin")) {
                  // Mark this file as an Excalidraw file
                  file.data.excalidrawFile = true
                }
              })

              // Add a note at the top of Excalidraw files
              if (file.data.excalidrawFile) {
                tree.children.unshift({
                  type: "html",
                  value: `<div class="excalidraw-notice" style="background: #f0f7ff; border-left: 4px solid #3b82f6; padding: 1rem; margin-bottom: 1.5rem; border-radius: 4px;">
                    <p style="margin: 0;"><strong>📐 Excalidraw Drawing</strong></p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9em; color: #666;">
                      This is an Excalidraw diagram. For best results, enable SVG auto-export in Obsidian's Excalidraw plugin settings.
                    </p>
                  </div>`,
                })
              }
            }

            // Handle embedded Excalidraw files in other markdown files
            visit(tree, "image", (node: any, index, parent) => {
              const url = node.url as string

              // Check if this is an Excalidraw file reference
              if (url?.includes(".excalidraw")) {
                // Try to find the corresponding SVG file
                const svgUrl = url.replace(/\.excalidraw(\.md)?$/, ".excalidraw.svg")

                // Update the image URL to point to the SVG
                node.url = svgUrl

                // Wrap the image in a centered div if requested
                if (opts.center && parent) {
                  const wrapper = {
                    type: "html",
                    value: `<div style="text-align: center; margin: 2rem 0;">`,
                  }
                  const closingWrapper = {
                    type: "html",
                    value: `</div>`,
                  }

                  // @ts-ignore
                  parent.children.splice(index, 0, wrapper)
                  // @ts-ignore
                  parent.children.splice(index + 2, 0, closingWrapper)
                }
              }
            })

            // Handle wikilinks to Excalidraw files
            visit(tree, "link", (node: any) => {
              const url = node.url as string

              // Check if this is a link to an Excalidraw file
              if (url?.includes(".excalidraw")) {
                // Try to convert to SVG reference
                const svgUrl = url.replace(/\.excalidraw(\.md)?$/, ".excalidraw.svg")
                node.url = svgUrl
              }
            })
          }
        },
      ]
    },
  }
}

