# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-19)

**Core value:** Users can upload, organize, search, and annotate PDF documents entirely on their local machine with semantic understanding powered by local ML models.
**Current focus:** Phase 2: Python ML Service

## Current Position

Phase: 2 of 5 (Python ML Service)
Plan: 2 of 7 in current phase
Status: In progress
Last activity: 2026-01-23 — Completed 02-02-PLAN.md (PDF text extraction with token-aware chunking)

Progress: [███████░░░] 18% (7/38 plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 7
- Average duration: <2 min
- Total execution time: <9 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Electron Foundation | 5 | <3 min | <1 min |
| 2. Python ML Service | 2 | 7 min | 3.5 min |
| 3. Document Management | 0 | 0 | - |
| 4. Semantic Search | 0 | 0 | - |
| 5. Reading & Annotation | 0 | 0 | - |

**Recent Trend:**
- Last 5 plans: 01-01 (<1 min), 01-02 (<1 min), 01-03 (<1 min), 01-04 (<1 min), 01-05 (<1 min), 02-01 (3 min), 02-02 (4 min)
- Trend: Fast configuration tasks transitioning to Python service features

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

**From 02-02 (PDF text extraction with token-aware chunking):**
- PyMuPDF over PyPDF2 for faster and more accurate position tracking
- tiktoken cl100k_base encoding (GPT-4 tokenizer) for chunk boundaries
- 500 token chunks with 50 token overlap for context preservation
- Position tracking (page_num, char_offset) for future PDF navigation
- Service layer pattern - services/ package for business logic separate from API
- Token-aware chunking using tiktoken encoding for ML-friendly text splits
- tiktoken>=0.8.0 to use latest version with Python 3.14 wheels

**From 02-01 (Python HTTP API service):**
- Dynamic port binding with file sync - use socket.bind((host, 0)) to find available port automatically
- Port file written to /tmp/doc-research-ml-port.txt for Electron discovery
- PYTHONUNBUFFERED=1 for real-time logging visibility during development
- Modular structure with api/ and utils/ packages for extensibility
- FastAPI router pattern - separate routers in api/ package, include in main app

**From 01-05 (Type-safe IPC bridge):**
- Expose only specific database methods (queryDatabase, execDatabase, initDatabase) via contextBridge
- Never expose raw ipcRenderer to renderer process (security best practice)
- Use TypeScript interfaces with Window augmentation for autocomplete
- Include JSDoc comments with usage examples for developer experience

**From 01-04 (SQLite database and IPC handlers):**
- Use .js extension for ESM imports from .ts files (TypeScript transpilation requirement)
- Return structured responses {success, data/error} from IPC handlers for consistent error handling
- Validate sender frame URL to prevent unauthorized access (app://-, localhost:3000 only)

**From 01-03 (Electron main process and preload script):**
- sandbox: false in webPreferences for development - will enable true for production security after testing
- Preload script includes full IPC API methods (sendMessage, send, on, removeAllListeners) - will be used in 01-05
- did-fail-load handler retries on Next.js dev server not ready - prevents race condition blank window

**From 01-02 (electron-vite configuration):**
- No renderer config in electron-vite - Next.js handles renderer separately (dev server in dev, static export in production)
- TypeScript config minimal update - existing tsconfig.json already compatible with electron-vite (esnext module, bundler resolution, esModuleInterop, skipLibCheck)

**From 01-01 (research):**
- Use electron-vite for main/preload processes (fast HMR, TypeScript-first)
- Load Next.js as external renderer via BrowserWindow.loadURL()
- Use Pages Router for Next.js (more stable static export than App Router)

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

None yet.

## Session Continuity

Last session: 2026-01-23 (plan 02-02 execution)
Stopped at: Completed 02-02-PLAN.md (PDF text extraction with token-aware chunking)
Resume file: None

**Next:** Plan 02-03 - ChromaDB vector storage for document chunks
