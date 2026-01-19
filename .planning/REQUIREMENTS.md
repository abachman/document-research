# Requirements: Local-First Document Research Library

**Defined:** 2026-01-19
**Core Value:** Users can upload, organize, search, and annotate PDF documents entirely on their local machine with semantic understanding powered by local ML models.

## v1 Requirements

### Electron Integration

- [ ] **ELEC-01**: Electron wrapper packages Next.js app as desktop application
- [ ] **ELEC-02**: IPC bridge enables renderer process to access SQLite via Server Actions
- [ ] **ELEC-03**: Application menu provides basic commands (File, Edit, View, Help)

### Python Service

- [ ] **PYTH-01**: Python service provides HTTP API for ML endpoints on localhost
- [ ] **PYTH-02**: Python service extracts text from uploaded PDFs with semantic boundary chunking
- [ ] **PYTH-03**: Python service integrates embedded Chroma database for vector storage
- [ ] **PYTH-04**: Python service auto-starts when Electron application launches
- [ ] **PYTH-05**: Python service uses Qwen 3 4B model for text embeddings
- [ ] **PYTH-06**: Python service uses Qwen 3 4B model for reranking search results
- [ ] **PYTH-07**: Python service stores PDF text chunks and embeddings in Chroma
- [ ] **PYTH-08**: Python service returns ranked search results with relevance scores

### Document Browsing

- [ ] **DOCB-01**: User can upload PDF files to document collection
- [ ] **DOCB-02**: User can delete PDF files from document collection
- [ ] **DOCB-03**: Document browsing view displays all PDFs in collection
- [ ] **DOCB-04**: User can add tags to documents for organization
- [ ] **DOCB-05**: User can remove tags from documents
- [ ] **DOCB-06**: User can filter documents by tag

### Document Search

- [ ] **SRCH-01**: User can perform semantic search across document collection
- [ ] **SRCH-02**: Search returns 25 ranked results sorted by relevance
- [ ] **SRCH-03**: Each search result displays document title
- [ ] **SRCH-04**: Each search result displays matching text chunk
- [ ] **SRCH-05**: Each search result displays relevance score
- [ ] **SRCH-06**: Search results are reranked using Qwen 3 4B reranking model
- [ ] **SRCH-07**: Search page provides dedicated UI for querying and viewing results

### Reading View

- [ ] **READ-01**: Reading view displays two-pane layout (PDF on left, annotations on right)
- [ ] **READ-02**: PDF is rendered using PDF.js in left pane
- [ ] **READ-03**: User can select text in PDF to create highlight
- [ ] **READ-04**: User can select text in PDF to create note
- [ ] **READ-05**: Annotations pane displays all highlights for current document in yellow
- [ ] **READ-06**: Annotations pane displays all notes for current document in blue
- [ ] **READ-07**: Clicking highlight in annotations pane scrolls PDF to that position
- [ ] **READ-08**: Clicking note in annotations pane scrolls PDF to that position

### Annotations

- [ ] **ANNO-01**: Highlight stores selected text and its position in SQLite
- [ ] **ANNO-02**: Note stores selected text, its position, and user's note in SQLite
- [ ] **ANNO-03**: User can add external URL links to annotations
- [ ] **ANNO-04**: User can add internal deep links to other documents in collection
- [ ] **ANNO-05**: Clicking internal deep link opens target document in reading view at linked position
- [ ] **ANNO-06**: SQLite database stores all annotations via better-sqlite3 in Electron main process

## v2 Requirements

### Keyword Search

- **SRCH-V2-01**: User can perform keyword/exact phrase search across document collection
- **SRCH-V2-02**: Hybrid search combines keyword and semantic results

### Advanced Annotation Management

- **ANNO-V2-01**: User can edit existing annotations
- **ANNO-V2-02**: User can delete existing annotations

## Out of Scope

| Feature | Reason |
|---------|--------|
| Multi-user support | Single-user local application |
| Cloud sync or backup | Local-first by design |
| User authentication | Single user on own machine |
| Mobile support | Desktop application only |
| Real-time collaboration | Single user only |
| Document formats beyond PDF | PDF only for v1 |
| Auto-update mechanism | User can manually update; adds complexity |
| Nested folders | Tag-based organization chosen instead |
| Online/cloud ML APIs | Local-first requirement |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ELEC-01 | Phase 1 | Pending |
| ELEC-02 | Phase 1 | Pending |
| ELEC-03 | Phase 1 | Pending |
| PYTH-01 | Phase 2 | Pending |
| PYTH-02 | Phase 2 | Pending |
| PYTH-03 | Phase 2 | Pending |
| PYTH-04 | Phase 2 | Pending |
| DOCB-01 | Phase 3 | Pending |
| DOCB-02 | Phase 3 | Pending |
| DOCB-03 | Phase 3 | Pending |
| DOCB-04 | Phase 3 | Pending |
| DOCB-05 | Phase 3 | Pending |
| DOCB-06 | Phase 3 | Pending |
| SRCH-01 | Phase 4 | Pending |
| SRCH-02 | Phase 4 | Pending |
| SRCH-03 | Phase 4 | Pending |
| SRCH-04 | Phase 4 | Pending |
| SRCH-05 | Phase 4 | Pending |
| SRCH-06 | Phase 4 | Pending |
| SRCH-07 | Phase 4 | Pending |
| PYTH-05 | Phase 4 | Pending |
| PYTH-06 | Phase 4 | Pending |
| PYTH-07 | Phase 4 | Pending |
| PYTH-08 | Phase 4 | Pending |
| READ-01 | Phase 5 | Pending |
| READ-02 | Phase 5 | Pending |
| READ-03 | Phase 5 | Pending |
| READ-04 | Phase 5 | Pending |
| READ-05 | Phase 5 | Pending |
| READ-06 | Phase 5 | Pending |
| READ-07 | Phase 5 | Pending |
| READ-08 | Phase 5 | Pending |
| ANNO-01 | Phase 5 | Pending |
| ANNO-02 | Phase 5 | Pending |
| ANNO-03 | Phase 5 | Pending |
| ANNO-04 | Phase 5 | Pending |
| ANNO-05 | Phase 5 | Pending |
| ANNO-06 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 35 total
- Mapped to phases: 35
- Unmapped: 0

---
*Requirements defined: 2026-01-19*
*Last updated: 2026-01-19 after roadmap creation*
