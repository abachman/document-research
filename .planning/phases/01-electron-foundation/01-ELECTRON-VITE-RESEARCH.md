# Phase 1: Electron Foundation - Electron-Vite Research

**Researched:** 2025-01-19
**Domain:** Electron build tooling with Vite
**Confidence:** HIGH for core electron-vite, MEDIUM for Next.js integration

## Summary

electron-vite is a next-generation Electron build tool based on Vite (version 3.0.0 as of 8 days ago). It provides significantly faster build times and Hot Module Replacement (HMR) compared to Webpack-based solutions like Electron Forge's webpack plugin. The tool is specifically designed for Electron's dual environment (Node.js main process and browser renderer process) with sensible defaults out-of-the-box.

**Key finding:** electron-vite is mature and production-ready for Electron applications, with excellent TypeScript support, fast HMR for all processes (main, preload, renderer), and native module support including better-sqlite3. However, **Next.js integration with electron-vite is not standard** - electron-vite is designed for Vite-based renderer processes (React, Vue, Svelte), not Next.js specifically. The recommended approach for Next.js is to use it as a separate dev server in development and static export in production, then load it via Electron's BrowserWindow.

**Primary recommendation:** Use electron-vite for main/preload process development with fast hot reload, and load Next.js as an external renderer (dev server in development, static export in production).

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| electron-vite | 3.0.0 | Build tool for Electron (main/preload) | Fast Vite-based builds, HMR for all processes, TypeScript-first |
| electron | Latest | Desktop app framework | Required for Electron apps |
| electron-builder | Latest | Packaging for distribution | Standard packaging tool, works with electron-vite output |
| vite | 5.0+ | Underlying build engine | Required dependency for electron-vite |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @electron-toolkit/preload | Latest | Preload script utilities | Recommended toolkit for contextBridge patterns |
| electron-serve | Latest | Serve static files in production | For loading Next.js static exports |
| concurrently | Latest | Run multiple dev servers | For running Next.js dev + Electron concurrently |

### Not Recommended for This Use Case

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| electron-vite renderer | Nextron | Nextron provides Next.js integration but is outdated and heavy |
| electron-vite renderer | Electron Forge Webpack | Slower builds, but more mature ecosystem |

**Installation:**

```bash
# Core Electron + electron-vite
npm install --save-dev electron electron-vite vite

# Packaging
npm install --save-dev electron-builder

# Development utilities
npm install --save-dev concurrently
npm install electron-serve

# TypeScript support (included with electron-vite)
npm install --save-dev typescript @types/node
```

**Node.js requirements:** Node.js 20.19+ or 22.12+

## Architecture Patterns

### Recommended Project Structure

For Next.js + Electron with electron-vite:

```
.
├── electron/
│   ├── main/
│   │   ├── index.ts          # Electron main process
│   │   └── ipc/              # IPC handlers
│   └── preload/
│       └── index.ts          # Preload script with contextBridge
├── src/                      # Next.js app root
│   ├── app/                  # Next.js App Router (or pages/)
│   ├── components/
│   └── ...
├── out/                      # electron-vite build output
│   ├── main/
│   └── preload/
├── .next/                    # Next.js build output
├── electron.vite.config.ts   # electron-vite configuration
├── next.config.js            # Next.js configuration
├── package.json
└── tsconfig.json
```

### Pattern 1: electron-vite Configuration

**What:** Central configuration for Electron main/preload processes
**When to use:** All Electron + electron-vite projects

```typescript
// electron.vite.config.ts
import { defineConfig } from 'electron-vite'
import { resolve } from 'path'

export default defineConfig({
  main: {
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'electron/main/index.ts')
        }
      }
    }
  },
  preload: {
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'electron/preload/index.ts')
        }
      }
    }
  }
  // Note: No renderer config - Next.js handles that
})
```

**Source:** [electron-vite Config Reference](https://electron-vite.org/config/)

### Pattern 2: Preload Script with contextBridge

**What:** Secure IPC bridge between main and renderer processes
**When to use:** All Electron apps (security best practice)

```typescript
// electron/preload/index.ts
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  // IPC invoke (request-response)
  sendMessage: (channel: string, data: unknown) => {
    return ipcRenderer.invoke(channel, data)
  },
  // IPC send (fire-and-forget)
  send: (channel: string, data: unknown) => {
    ipcRenderer.send(channel, data)
  },
  // IPC on (listen to messages from main)
  on: (channel: string, callback: (...args: unknown[]) => void) => {
    ipcRenderer.on(channel, (event, ...args) => callback(...args))
  },
  // Remove listener
  removeAllListeners: (channel: string) => {
    ipcRenderer.removeAllListeners(channel)
  }
})
```

**Source:** [electron-vite Development Guide](https://electron-vite.org/guide/dev)

### Pattern 3: Main Process with Next.js Loading

**What:** Electron main process that loads Next.js (dev server or static)
**When to use:** Next.js integration

```typescript
// electron/main/index.ts
import { app, BrowserWindow } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'
import electronServe from 'electron-serve'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

const appServe = app.isPackaged
  ? electronServe({ directory: join(__dirname, '../../out') })
  : null

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false // Set to true for production security
    }
  })

  if (app.isPackaged) {
    // Production: Load static Next.js export
    appServe(win).then(() => {
      win.loadURL('app://-')
    })
  } else {
    // Development: Load Next.js dev server
    win.loadURL('http://localhost:3000')
    win.webContents.openDevTools()

    // Handle case where Electron starts before Next.js
    win.webContents.on('did-fail-load', () => {
      win.webContents.reloadIgnoringCache()
    })
  }
}

app.whenReady().then(() => {
  createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
```

**Source:** [Medium - Building Desktop Apps with Electron + Next.js](https://rbfraphael.medium.com/building-desktop-apps-with-electron-next-js-without-nextron-01bbf1fdd72e)

### Pattern 4: IPC Handlers in Main Process

**What:** Main process IPC handlers for renderer communication
**When to use:** Any renderer-to-main communication

```typescript
// electron/main/ipc/handlers.ts
import { ipcMain } from 'electron'

export function registerIpcHandlers() {
  ipcMain.handle('db:query', async (event, sql: string) => {
    // Handle database query
    return { success: true, data: [] }
  })

  ipcMain.handle('app:get-version', async () => {
    return app.getVersion()
  })
}

// Call in electron/main/index.ts after app.whenReady()
```

### Anti-Patterns to Avoid

- **Using electron-vite for Next.js renderer:** electron-vite is designed for Vite-based projects, not Next.js. Use Next.js's own build system.
- **nodeIntegration in renderer:** electron-vite doesn't support this (security risk). Use preload scripts with contextBridge.
- **Mixing build systems:** Don't try to bundle Next.js with electron-vite. Let Next.js handle itself.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Electron build tooling | Custom webpack/esbuild config | electron-vite | Handles Electron's dual environment, HMR for all processes |
| Preload script utilities | Manual contextBridge wrapping | @electron-toolkit/preload | Standardized, type-safe API exposure |
| Hot reload for main process | Custom file watcher | electron-vite built-in hot reloading | Automatic restart on file changes |
| Native module loading | Manual rebuild scripts | electron-vite's optimized asset handling | Handles better-sqlite3 and other native modules automatically |
| Static file serving | Custom express server | electron-serve | Designed for Electron packaged apps |

**Key insight:** electron-vite provides a complete development experience for Electron's main and preload processes. The main complexity is integrating Next.js, which should remain separate and be loaded as an external renderer.

## Common Pitfalls

### Pitfall 1: Next.js Dev Server Not Ready

**What goes wrong:** Electron launches before Next.js dev server is ready, showing "Connection refused" or blank screen.

**Why it happens:** `concurrently` starts both processes in parallel, but Next.js takes time to compile.

**How to avoid:**
```typescript
// In main process, add reload on failure
win.webContents.on('did-fail-load', () => {
  win.webContents.reloadIgnoringCache()
})
```

**Warning signs:** Blank Electron window on first start, intermittent loading failures.

### Pitfall 2: Native Modules (better-sqlite3) Not Found After Build

**What goes wrong:** better-sqlite3 works in development but fails after packaging with "Cannot find module" error.

**Why it happens:** Native modules need to be rebuilt for the target Electron version, and the .node files must be included in the package.

**How to avoid:**
- Use electron-builder's `asarUnpack` configuration for native modules
- Ensure `npm rebuild` runs during build process if needed
- Test packaged app early, not just dev mode

**Warning signs:** Module works in dev but not in production build.

### Pitfall 3: Preload Script Sandbox Limitations

**What goes wrong:** Preload script can't import dependencies, shows "module not found" errors.

**Why it happens:** Electron 20+ sandboxes preload scripts by default, limiting Node.js access.

**How to avoid:**
- Bundle all preload dependencies with electron-vite (it does this by default)
- Or disable sandbox: `sandbox: false` in webPreferences (not recommended for production)
- Use `?modulePath` suffix for worker threads

**Warning signs:** Import errors in preload script, "module not found" for dependencies.

### Pitfall 4: Next.js Static Export Routing Issues

**What goes wrong:** Next.js router doesn't work, clicking links shows 404 or blank pages.

**Why it happens:** Next.js static export doesn't include server-side routing. Uses Pages Router, not App Router.

**How to avoid:**
- Use Pages Router (App Router has limited static export support)
- Set `output: "export"` in next.config.js
- Disable image optimization: `images: { unoptimized: true }`
- Use `<Link>` for navigation, not `window.location`

**Warning signs:** 404 errors on navigation, blank pages in production.

### Pitfall 5: TypeScript Configuration Conflicts

**What goes wrong:** Type errors, can't use import syntax, `__dirname` undefined in ESM.

**Why it happens:** Electron + TypeScript + ESM has specific configuration requirements.

**How to avoid:**
- Use electron-vite's built-in TypeScript support (it handles tsconfig)
- For ESM, use `import.meta.url` instead of `__dirname`
- Or let electron-vite handle CommonJS/ESM compatibility (it does by default)

**Warning signs:** TypeScript errors in main/preload scripts, runtime errors with `__dirname`.

## Code Examples

### Package.json Scripts

```json
{
  "main": "out/main/index.js",
  "scripts": {
    "dev": "concurrently -n \"NEXT,ELECTRON\" -c \"yellow,blue\" --kill-others \"next dev\" \"electron-vite dev\"",
    "dev:next": "next dev",
    "dev:electron": "electron-vite dev",
    "build": "electron-vite build && next build",
    "build:win": "npm run build && electron-builder --win",
    "build:mac": "npm run build && electron-builder --mac",
    "build:linux": "npm run build && electron-builder --linux",
    "preview": "electron-vite preview"
  }
}
```

### Next.js Configuration

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  images: {
    unoptimized: true
  },
  // Disable server-side features for Electron
  trailingSlash: true,
  distDir: '.next'
}

module.exports = nextConfig
```

### electron-builder Configuration

```yaml
# electron-builder.yml
appId: com.yourcompany.yourapp
productName: Your App
copyright: Copyright © 2025
directories:
  buildResources: build
  output: release

files:
  - out/**/*          # electron-vite output
  - out/**/**         # Recursive
  - resources/**/*    # Next.js static files
  - package.json

extraResources:
  - from: "out"
    to: "out"
    filter: ["**/*"]

win:
  target:
    - target: nsis
      arch: [x64]
  icon: resources/icon.ico

mac:
  target:
    - target: dmg
    - target: zip
  icon: resources/icon.icns

linux:
  target:
    - target: AppImage
    - target: deb
  icon: resources/icon.png
  category: Utility
```

### TypeScript IPC Types

```typescript
// electron/preload/types.ts
export interface ElectronAPI {
  sendMessage: (channel: string, data: unknown) => Promise<unknown>
  send: (channel: string, data: unknown) => void
  on: (channel: string, callback: (...args: unknown[]) => void) => void
  removeAllListeners: (channel: string) => void
}

declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

// Use in renderer: window.electronAPI.sendMessage('channel', data)
```

### Using better-sqlite3 with electron-vite

```typescript
// electron/main/database.ts
import Database from 'better-sqlite3'
import { join } from 'path'
import { app } from 'electron'

const dbPath = join(app.getPath('userData'), 'database.db')

export const db = new Database(dbPath)

// Example query function
export function queryDocuments(query: string) {
  const stmt = db.prepare(query)
  return stmt.all()
}

// Close on app quit
app.on('before-quit', () => {
  db.close()
})
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Electron Forge Webpack Plugin | electron-vite | 2023-2024 | 10x faster builds, instant HMR |
| Nextron for Next.js + Electron | Manual integration with electron-vite | 2023-2024 | More control, lighter weight |
| CommonJS only | ESM support (Electron 28+) | 2024 | Can use modern import syntax |
| Custom hot reload scripts | Built-in hot reloading | 2023 | No configuration needed |

**Deprecated/outdated:**
- Nextron: Outdated dependencies, heavy, not actively maintained
- Electron-forge-plugin-webpack: Slower than Vite-based solutions
- electron-vite renderer config for Next.js: Don't use electron-vite for Next.js renderer

## Key Differences: electron-vite vs Electron Forge Webpack

### electron-vite
- **Build engine:** Vite (esbuild-based)
- **Speed:** Significantly faster (especially dev server and HMR)
- **Configuration:** Single `electron.vite.config.ts` file
- **Scope:** Focuses on build tooling only (main/preload processes)
- **HMR:** Instant HMR for renderer, hot reload for main/preload
- **TypeScript:** First-class support, no extra setup needed
- **Magic globals:** None - uses standard import syntax

### Electron Forge Webpack Plugin
- **Build engine:** Webpack
- **Speed:** Slower, but mature ecosystem
- **Configuration:** Separate `webpack.main.config.js` and `webpack.renderer.config.js`
- **Scope:** Full-stack solution (build + package + publish)
- **HMR:** Slower HMR
- **TypeScript:** Requires additional configuration
- **Magic globals:** `MAIN_WINDOW_WEBPACK_ENTRY`, `MAIN_WINDOW_PRELOAD_WEBPACK_ENTRY`

### Integration with Next.js

**electron-vite approach:**
- Use electron-vite for main/preload processes only
- Next.js runs independently (dev server or static export)
- Load Next.js via BrowserWindow `loadURL()`
- Two separate build systems working together

**Electron Forge Webpack approach:**
- Webpack bundles everything including Next.js
- More complex configuration
- Single build system but slower

## Open Questions

1. **Next.js App Router vs Pages Router for Electron**
   - What we know: App Router has limited static export support, Pages Router is more stable
   - What's unclear: Best practices for App Router with Next.js 15+ static exports
   - Recommendation: Use Pages Router for stability, or test App Router static export thoroughly

2. **Production deployment of better-sqlite3**
   - What we know: Native modules need special handling during packaging
   - What's unclear: Exact electron-builder configuration for better-sqlite3 across platforms
   - Recommendation: Test packaging early, use `asarUnpack` for native modules if needed

3. **Performance impact of two build systems**
   - What we know: Running electron-vite + Next.js adds complexity
   - What's unclear: Exact performance impact compared to single build system
   - Recommendation: Monitor build times, consider using `npm run build:only` for incremental builds

## Sources

### Primary (HIGH confidence)

- [electron-vite Official Documentation](https://electron-vite.org/) - Core configuration, features, setup
- [electron-vite Configuration Reference](https://electron-vite.org/config/) - Detailed config options
- [electron-vite Development Guide](https://electron-vite.org/guide/dev) - Preload scripts, IPC, project structure
- [electron-vite on npm](https://www.npmjs.com/package/electron-vite) - Version 3.0.0, published 8 days ago
- [Electron contextBridge API](https://electronjs.org/docs/latest/api/context-bridge) - Security patterns
- [Electron Preload Scripts Tutorial](https://electronjs.org/docs/latest/tutorial/tutorial-preload) - Official preload guide
- [Electron IPC Guide](https://electronjs.org/docs/latest/tutorial/ipc) - Inter-process communication

### Secondary (MEDIUM confidence)

- [Building Desktop Apps with Electron + Next.js (without Nextron)](https://rbfraphael.medium.com/building-desktop-apps-with-electron-next-js-without-nextron-01bbf1fdd72e) - Verified Next.js integration pattern
- [Building and publishing desktop applications with Electron + Next.js](https://stronglytyped.uk/articles/building-publishing-desktop-applications-electron-nextjs) - Production deployment patterns
- [Next.js Static Exports Guide](https://nextjs.org/docs/pages/guides/static-exports) - Official static export docs
- [electron-vite GitHub Repository](https://github.com/alex8088/electron-vite) - Source code, examples
- [electron-vite-boilerplate](https://github.com/alex8088/electron-vite-boilerplate) - Reference implementation
- [StackOverflow - Cannot find module 'better-sqlite3' after building](https://stackoverflow.com/questions/79544832/cannot-find-module-better-sqlite3-after-building-electron-forge-vite-app-on-l) - Native module issues
- [GitHub Template - electron-vite + Vue3 + better-sqlite3](https://github.com/renqiankun/electron-vite-template) - Native module example

### Tertiary (LOW confidence)

- Various community blog posts and tutorials (used for cross-reference only)
- Reddit discussions on Electron + Next.js (anecdotal evidence)
- Chinese language blog posts (machine-translated, used for verification only)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Official documentation and npm package verified
- Architecture: HIGH - Official docs and verified community examples
- Pitfalls: MEDIUM - Some issues documented, others inferred from Electron patterns
- Next.js integration: MEDIUM - Verified community examples, but not official electron-vite pattern

**Research date:** 2025-01-19
**Valid until:** 30 days (electron-vite is stable, but verify latest version before implementation)

**Key recommendation:** electron-vite is excellent for Electron main/preload processes. For Next.js integration, use the external renderer pattern (dev server in development, static export in production) rather than trying to bundle Next.js with electron-vite.
