# Excalidraw Setup Guide for Quartz

## Overview

I've added support for Excalidraw files in your Quartz notes application. The custom transformer plugin will:

1. Automatically detect `.excalidraw.md` files
2. Convert Excalidraw file references to SVG format
3. Add helpful notices on Excalidraw pages
4. Handle both embedded diagrams and wikilinks

## What Was Added

### 1. Custom Excalidraw Transformer Plugin
- **Location**: `quartz/plugins/transformers/excalidraw.ts`
- **Features**:
  - Detects Excalidraw markdown files
  - Converts `.excalidraw` and `.excalidraw.md` references to `.excalidraw.svg`
  - Adds visual notices on Excalidraw pages
  - Centers embedded diagrams

### 2. Updated Configuration
- **File**: `quartz.config.ts`
- **Added**: `Plugin.Excalidraw()` to the transformers array

## How to Enable SVG Auto-Export in Obsidian

To ensure your Excalidraw files display properly, you need to enable SVG auto-export:

### Step 1: Open Excalidraw Plugin Settings
1. In Obsidian, go to **Settings** (gear icon)
2. Navigate to **Community Plugins** → **Excalidraw**

### Step 2: Enable Auto-Export
1. Scroll down to **Embedding Excalidraw into your Notes and Exporting**
2. Find **Export Settings** → **Auto-Export Settings**
3. Enable **Auto-export SVG**
4. (Optional) You can also enable **Auto-export PNG** for fallback

### Step 3: Configure Export Settings
Recommended settings:
- **Auto-export SVG**: ✅ Enabled
- **SVG export scale**: 1 (or 2 for higher quality)
- **Keep .SVG filenames in sync with note name**: ✅ Enabled
- **Export both Dark and Light**: Optional (based on your preference)

### Step 4: Regenerate Existing Exports
For existing Excalidraw files:
1. Open each `.excalidraw.md` file in Obsidian
2. The plugin will automatically generate the `.svg` file
3. Or use the command palette: `Excalidraw: Export image`

## How It Works

### For New Excalidraw Files
When you create or edit an Excalidraw file in Obsidian with auto-export enabled:
- Obsidian creates: `drawing.excalidraw.md`
- Obsidian auto-exports: `drawing.excalidraw.svg`
- Quartz displays the SVG in your published site

### For References in Markdown
When you reference an Excalidraw file:

**Wikilink style:**
```markdown
![[my-diagram.excalidraw]]
```

**Markdown style:**
```markdown
![My Diagram](my-diagram.excalidraw.md)
```

The plugin automatically converts these to:
```markdown
![My Diagram](my-diagram.excalidraw.svg)
```

## Current Excalidraw Files in Your Vault

I found these Excalidraw files:
- `/content/1.DevOps - Cloud/1.DevOps_Index.excalidraw.md`
- `/content/3.Inbox/life-analysis2.excalidraw.md`
- `/content/4.office/azure cloud architecture for asynk.excalidraw.md`
- `/content/7.self help/Drawing 2024-12-18 11.31.58.excalidraw.md`
- `/content/Excalidraw/` folder (8 files)

### Action Required
For these existing files, you'll need to:
1. Open them in Obsidian (with auto-export SVG enabled)
2. The SVG files will be generated automatically
3. Rebuild your Quartz site

## Testing

To test if everything works:

1. **Build Quartz:**
   ```bash
   npx quartz build
   ```

2. **Or build and serve locally:**
   ```bash
   npx quartz build --serve
   ```

3. **Navigate to an Excalidraw page** and verify:
   - You see a blue notice box at the top
   - The diagram renders properly (if SVG exists)
   - Links to Excalidraw files work

## Troubleshooting

### Problem: Excalidraw files show as raw markdown
**Solution**: Make sure SVG files are generated and present in the same directory as the `.excalidraw.md` files.

### Problem: Diagrams don't display
**Solutions**:
1. Check if `.svg` files exist next to your `.excalidraw.md` files
2. Verify auto-export is enabled in Obsidian
3. Rebuild Quartz: `npx quartz build`

### Problem: Old diagrams still show incorrectly
**Solution**: 
1. Delete the `public` folder
2. Rebuild: `npx quartz build`

## Optional: Manual SVG Export

If you don't want to use auto-export, you can manually export:

1. Open the Excalidraw file in Obsidian
2. Click the menu icon (three dots)
3. Select **Export image** → **SVG**
4. Save it with the same name as your `.excalidraw.md` file but with `.svg` extension

## Configuration Options

You can customize the Excalidraw plugin behavior in `quartz.config.ts`:

```typescript
Plugin.Excalidraw({
  width: "100%",    // Width of embedded drawings
  center: true,     // Center the drawings
}),
```

## Additional Resources

- [Excalidraw Official Site](https://excalidraw.com/)
- [Obsidian Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [Quartz Documentation](https://quartz.jzhao.xyz/)

## Summary

✅ Excalidraw transformer plugin added  
✅ Configuration updated  
⏳ Next: Enable SVG auto-export in Obsidian  
⏳ Next: Regenerate SVGs for existing files  
⏳ Next: Test by building Quartz  

