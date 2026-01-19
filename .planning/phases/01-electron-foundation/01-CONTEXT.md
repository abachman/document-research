# Phase 1: Electron Foundation - Context

**Gathered:** 2026-01-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Desktop application wrapper — establishing the Electron desktop foundation with IPC bridge and application menu. This phase packages Next.js as a desktop window, enables renderer-to-main communication via IPC, and provides native application menus. PDF processing, ML service, and document management are later phases.

</domain>

<decisions>
## Implementation Decisions

### Development workflow
- **Hot reload**: Enabled for Next.js renderer changes
- **DevTools**: Claude's discretion (default to open in dev, configurable)
- **Start process**: Two-step process — separate commands for Next.js dev server and Electron
- **Main process hot reload**: Fast rebuild with tooling (esbuild or similar) for main.js/preload changes
- **Packaging**: Claude's discretion (choose simpler, more standard approach)

### IPC bridge scope
- **Scope**: Minimal bridge for Phase 1 — expand in later phases as needed
- **Error handling**: Forward full errors to renderer (for debugging)
- **Batching**: No batching — one operation per IPC call (simpler)

### Claude's Discretion
- Chrome DevTools default behavior in development
- Production build packaging approach
- Exact tooling for main process hot rebuild (esbuild, electron-forge, etc.)
- IPC channel naming and structure
- Window state persistence implementation details

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard Electron development approaches.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-electron-foundation*
*Context gathered: 2026-01-19*
