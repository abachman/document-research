# Local-First Document Research Library

## What This Is

A browser-based, single-user, local-first PDF document library and reader with semantic search, highlighting, and notetaking capabilities. Packaged as an Electron desktop application with an embedded Next.js frontend and local Python service for ML processing.

## Core Value

Users can upload, organize, search, and annotate PDF documents entirely on their local machine with semantic understanding powered by local ML models—no cloud services required.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Electron app wrapper with embedded Next.js frontend
- [ ] Local Python service for PDF processing and ML models
- [ ] Document browsing view with upload, delete, and tag-based organization
- [ ] PDF text extraction via Python service (semantic boundary chunking)
- [ ] Document search view with word/phrase and semantic search
- [ ] Qwen 3 4B embedding model integration via Python service
- [ ] Qwen 3 4B reranking model for refining search results
- [ ] Chroma database (embedded in Python) for text chunks and embeddings
- [ ] Search results display: 25 ranked results with document title, text chunk, and relevance score
- [ ] Document reading view with two-pane layout (PDF left, annotations right)
- [ ] PDF.js integration for browser-based PDF rendering
- [ ] Text selection in PDF for creating highlights and notes
- [ ] SQLite storage for highlights (text, position) and notes (text, position, user note)
- [ ] Annotations pane showing highlights (yellow) and notes (blue) for current document
- [ ] Click-to-navigate: clicking annotation scrolls PDF to that position
- [ ] External URL links in annotations
- [ ] Internal deep links to other documents in the collection
- [ ] Next.js Server Functions (Server Actions) preferred over API routes

### Out of Scope

- Multi-user support — Single-user local application
- Cloud sync or backup — Local-first, no cloud dependencies
- User authentication — Single user on their own machine
- Mobile support — Desktop application only
- Real-time collaboration — Single user only
- Document formats beyond PDF — PDF only for v1

## Context

**Technical Environment:**
- Next.js 16.1.2 with App Router and TypeScript
- React 19.2.3 for UI components
- Tailwind CSS v4 for styling
- pnpm for package management
- Existing codebase is a fresh Next.js scaffold with no document processing logic yet

**Architecture Pattern:**
- Electron desktop app embedding Next.js frontend
- Local Python service (FastAPI/Flask) for:
  - PDF text extraction
  - Qwen 3 4B embedding model inference
  - Qwen 3 4B reranking model inference
  - Embedded Chroma database for vector storage
- SQLite (via better-sqlite3) for annotations in Electron main process
- Next.js Server Actions for client-server communication within Electron

**Key Integration Points:**
- Next.js ↔ Python service via HTTP (localhost)
- Next.js ↔ SQLite via Server Actions accessing Electron's main process
- PDF.js running in browser/renderer process for PDF display

**Known Issues from Codebase Mapping:**
- Built API routes exist in `.next/` but no source files (stale build artifacts)
- Default Next.js starter template content needs customization
- No error handling, loading states, or error pages implemented yet
- No test framework configured

## Constraints

- **Tech Stack**: Next.js + Electron + Python service (ML models) — Required for architecture compatibility
- **ML Models**: Qwen 3 4B embedding and reranking models — Required for semantic search
- **Vector DB**: Chroma embedded in Python service — Required for local vector storage
- **Annotations**: SQLite via Electron main process — Required for local-first storage
- **PDF Rendering**: PDF.js — Required for browser-based rendering
- **Offline Capability**: All processing must be local — No cloud API dependencies
- **Deployment**: Packaged as Electron desktop app — Not a web application

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Electron over Tauri | More mature ecosystem, easier JavaScript integration for Next.js embedding | — Pending |
| Tag-based over folder organization | More flexible for single-user collections, easier to search/filter | — Pending |
| Separate Python service | ML models and PDF processing are Python-native, easier to run locally than Node.js ports | — Pending |
| Semantic boundary chunking | Better search relevance than fixed-size chunks, context-aware splits | — Pending |
| Server Actions over API routes | Simpler for Electron-embedded Next.js, less HTTP overhead | — Pending |
| SQLite in Electron main process | Secure local storage, accessible from renderer via IPC, reliable for single-user | — Pending |
| No sync/backup | Local-first by design, user manages their own data backup strategy | — Pending |

---
*Last updated: 2026-01-19 after initialization*
