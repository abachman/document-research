# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-19)

**Core value:** Users can upload, organize, search, and annotate PDF documents entirely on their local machine with semantic understanding powered by local ML models.
**Current focus:** Phase 2: Python ML Service

## Current Position

Phase: 2 of 5 (Python ML Service)
Plan: 3 of 7 in current phase
Status: In progress
Last activity: 2026-01-24 — Completed 02-03-PLAN.md (ChromaDB vector storage integration)

Progress: [████████░░░] 21% (8/38 plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 8
- Average duration: <2 min
- Total execution time: <17 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Electron Foundation | 5 | <3 min | <1 min |
| 2. Python ML Service | 3 | 15 min | 5 min |
| 3. Document Management | 0 | 0 | - |
| 4. Semantic Search | 0 | 0 | - |
| 5. Reading & Annotation | 0 | 0 | - |

**Recent Trend:**
- Last 5 plans: 01-05 (<1 min), 02-01 (3 min), 02-02 (4 min), 02-03 (8 min)
- Trend: Python ML service features taking longer as complexity increases

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

**From 02-03 (ChromaDB vector storage integration):**
- Python 3.13 required for python-service - ChromaDB (Pydantic v1, onnxruntime) incompatible with Python 3.14
- Single ChromaDB collection with doc_id metadata filtering instead of separate collections per document
- Background task processing for PDF uploads to prevent HTTP timeout on large files
- Platform-specific app data paths for ChromaDB persistence (macOS: ~/Library/Application Support)
- Cosine similarity distance metric for vector embeddings (hnsw:space)

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

Last session: 2026-01-24 (plan 02-03 execution)
Stopped at: Completed 02-03-PLAN.md (ChromaDB vector storage integration)
Resume file: None

**Next:** Plan 02-04 - Electron integration with Python ML service
