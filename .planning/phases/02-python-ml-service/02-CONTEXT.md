# Phase 2: Python ML Service - Context

**Gathered:** 2026-01-23
**Status:** Ready for planning

## Phase Boundary

Local Python service that starts when Electron app needs it, exposes HTTP endpoints for PDF upload and processing, extracts text with semantic chunking, and stores embeddings in Chroma. The service is managed by Electron but runs as a separate process.

## Implementation Decisions

### Service lifecycle
- Bundle Python runtime with the Electron app (electron-is-packager handles bundling)
- Lazy start: Python service starts on first IPC call from renderer, not app startup
- Auto-retry then alert: Attempt auto-restart up to N times on crash, then show error to user
- Dynamic port with file sync: Service picks free port on startup, writes to temp file; Electron reads file to discover port
- Log all failures for debugging

### Vector storage
- Single Chroma collection named 'documents' for all chunks
- Filter by doc_id in metadata when searching for specific documents
- Minimal metadata: doc_id, chunk_index, page_num only
- Embedded Chroma with persistent mode (SQLite-based, ~/.chroma location)
- Archive deleted documents to separate collection (not cascade delete, not soft delete)

### PDF processing behavior
- Semantic-aware chunking: split on paragraphs/sentences first, merge into ~500 token chunks
- Avoid splitting mid-sentence; adjust target size to respect semantic boundaries
- Chunk source tracking: page number + character offset (enables PDF link navigation later)
- Extract basic PDF metadata: title, author, creation date from PDF metadata

### Claude's Discretion
- Exact retry count for auto-restart (N times)
- Health check polling interval (if any)
- Exact port file location and format
- Chroma storage location within app data directory
- Exact semantic splitting algorithm (sentence vs paragraph detection)
- Chunk overlap strategy

## Specific Ideas

No specific requirements — open to standard approaches for Python/Chroma integration.

## Deferred Ideas

None — discussion stayed within phase scope.

---

*Phase: 02-python-ml-service*
*Context gathered: 2026-01-23*
