# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-19)

**Core value:** Users can upload, organize, search, and annotate PDF documents entirely on their local machine with semantic understanding powered by local ML models.
**Current focus:** Phase 3: Document Management

## Current Position

Phase: 3 of 5 (Document Management)
Plan: Not started
Status: Ready to plan
Last activity: 2026-01-24 — Completed Phase 2: Python ML Service

Progress: [██████████░░] 24% (9/38 plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 9
- Average duration: ~4 min
- Total execution time: ~35 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Electron Foundation | 5 | <3 min | <1 min |
| 2. Python ML Service | 4 | 23 min | 5.75 min |
| 3. Document Management | 0 | 0 | - |
| 4. Semantic Search | 0 | 0 | - |
| 5. Reading & Annotation | 0 | 0 | - |

**Recent Trend:**
- Last 5 plans: 02-01 (3 min), 02-02 (4 min), 02-03 (8 min), 02-04 (8 min)
- Trend: Python service integration with increasing complexity

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

**From 02-04 (Electron integration with Python service):**
- Lazy initialization for Python service - starts on first IPC call, not app startup
- File-based port discovery with polling (100ms intervals, 5 second timeout)
- Auto-restart on crash up to 3 times before emitting fatal error
- Raw Python files bundled via electron-builder (not PyInstaller) for v1
- Users must have Python 3.13+ installed (acceptable for v1 technical audience)
- Cross-platform temp directory using tempfile.gettempdir() (handles macOS/Linux/Windows)
- Signal handlers (SIGTERM/SIGINT) for graceful shutdown with port file cleanup

**From 02-03 (ChromaDB vector storage integration):**
- Use Python 3.13 for python-service - ChromaDB (Pydantic v1, onronruntime) incompatible with Python 3.14
- ChromaDB persistent storage in platform-specific app data directory (~/Library/Application Support/document-research/chroma on macOS)
- Background task processing for PDF upload to prevent HTTP timeout
- Single 'documents' collection with doc_id filter for all document chunks
- Cosine similarity distance metric for vector embeddings (hnsw:space)

**From 02-02 (PDF text extraction with token-aware chunking):**
- Use PyMuPDF (fitz) for PDF text extraction (faster and more accurate than PyPDF2)
- Token-aware chunking with tiktoken cl100k_base encoding (GPT-4 tokenizer)
- Chunks set to ~500 tokens with 50 token overlap for context preservation
- Position tracking (page_num, char_offset) maintained for PDF navigation
- PDF upload endpoint returns structured response with doc_id, chunk_count, metadata
- Service layer pattern - services/ package for business logic separate from API

**From 02-01 (Python HTTP API foundation):**
- Dynamic port binding to avoid conflicts (service picks free port on startup)
- File-based service discovery for Electron (port written to /tmp/doc-research-ml-port.txt)
- FastAPI with uvicorn for HTTP service (async support, type safety, auto docs)
- Modular structure with api/ and utils/ packages for extensibility
- PYTHONUNBUFFERED=1 for real-time logging

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

Last session: 2026-01-24 (Phase 2 execution)
Completed: All 4 plans in Phase 2 (Python ML Service)

**Phase 2 Summary:**
- 02-01: Python HTTP API service with FastAPI, dynamic port binding, health check
- 02-02: PDF text extraction with PyMuPDF, token-aware chunking with tiktoken
- 02-03: ChromaDB persistent vector storage with background processing
- 02-04: Electron integration with lazy initialization, IPC handlers, type-safe API

**Phase 2 Decisions:**
- Use Python 3.13 (ChromaDB incompatible with Python 3.14)
- Lazy service initialization (starts on first PDF operation)
- Raw Python files bundled, not PyInstaller (users need Python installed)

**Next:** Phase 3: Document Management — Plan document upload, browsing, and tagging UI

───────────────────────────────────────────────────────────────

## Next Steps

**Phase 3: Document Management** — Upload, browse, and organize PDFs with tags

/gsd:discuss-phase 3 — gather context and clarify approach

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /gsd:plan-phase 3 — skip discussion, plan directly
- /gsd:verify-work — manual acceptance testing before continuing
