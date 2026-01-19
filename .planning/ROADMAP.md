# Roadmap: Local-First Document Research Library

## Overview

A browser-based, single-user, local-first PDF document library and reader with semantic search, highlighting, and notetaking capabilities. Packaged as an Electron desktop application with an embedded Next.js frontend and local Python service for ML processing.

This roadmap delivers the application through five phases: establishing the Electron desktop foundation, building the Python ML service for PDF processing and embeddings, implementing document management with tagging, adding semantic search with local Qwen models, and completing the reading experience with PDF rendering and annotations.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Electron Foundation** - Desktop app wrapper with IPC bridge and application menu
- [ ] **Phase 2: Python ML Service** - Local HTTP API for PDF processing and vector storage
- [ ] **Phase 3: Document Management** - Upload, browse, and organize PDFs with tags
- [ ] **Phase 4: Semantic Search** - Qwen-powered search with embeddings and reranking
- [ ] **Phase 5: Reading & Annotation** - PDF rendering with highlights, notes, and cross-document linking

## Phase Details

### Phase 1: Electron Foundation

**Goal**: Application runs as a desktop app with IPC bridge for local data access

**Depends on**: Nothing (first phase)

**Requirements**: ELEC-01, ELEC-02, ELEC-03

**Success Criteria** (what must be TRUE):
1. Application launches as a desktop window showing the Next.js frontend
2. Renderer process can communicate with Electron main process via IPC
3. Application menu provides File, Edit, View, and Help menus with basic commands

**Plans**: 3 plans in 2 waves

Plans:
- [ ] 01-01-PLAN.md — Electron wrapper packages Next.js app as desktop application
- [ ] 01-02-PLAN.md — IPC bridge enables renderer process to access SQLite via secure contextBridge
- [ ] 01-03-PLAN.md — Application menu provides basic commands (File, Edit, View, Help)

### Phase 2: Python ML Service

**Goal**: Local Python service handles PDF processing and vector storage

**Depends on**: Phase 1

**Requirements**: PYTH-01, PYTH-02, PYTH-03, PYTH-04

**Success Criteria** (what must be TRUE):
1. Python service starts automatically when Electron application launches
2. Python service responds to HTTP requests on localhost
3. Uploaded PDFs are processed with text extracted in semantically-aware chunks
4. Text chunks and embeddings are stored in embedded Chroma database

**Plans**: TBD

Plans:
- [ ] 02-01: Python service provides HTTP API for ML endpoints on localhost
- [ ] 02-02: Python service extracts text from uploaded PDFs with semantic boundary chunking
- [ ] 02-03: Python service integrates embedded Chroma database for vector storage
- [ ] 02-04: Python service auto-starts when Electron application launches

### Phase 3: Document Management

**Goal**: Users can upload, browse, and organize PDF documents

**Depends on**: Phase 2

**Requirements**: DOCB-01, DOCB-02, DOCB-03, DOCB-04, DOCB-05, DOCB-06

**Success Criteria** (what must be TRUE):
1. User can upload PDF files through the document browsing interface
2. Document browsing view displays all PDFs in the collection
3. User can delete PDF files from the collection
4. User can add tags to documents for organization
5. User can remove tags from documents
6. User can filter documents by tag to find specific documents

**Plans**: TBD

Plans:
- [ ] 03-01: Document browsing view displays all PDFs in collection
- [ ] 03-02: User can upload PDF files to document collection
- [ ] 03-03: User can delete PDF files from document collection
- [ ] 03-04: User can add tags to documents for organization
- [ ] 03-05: User can remove tags from documents
- [ ] 03-06: User can filter documents by tag

### Phase 4: Semantic Search

**Goal**: Users can search documents with semantic understanding powered by local ML models

**Depends on**: Phase 3

**Requirements**: PYTH-05, PYTH-06, PYTH-07, PYTH-08, SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05, SRCH-06, SRCH-07

**Success Criteria** (what must be TRUE):
1. User can enter search queries in the dedicated search interface
2. Search returns 25 results ranked by relevance
3. Each search result displays document title, matching text chunk, and relevance score
4. Search uses semantic embeddings from Qwen 3 4B model
5. Search results are reranked using Qwen 3 4B reranking model for improved relevance

**Plans**: TBD

Plans:
- [ ] 04-01: Python service uses Qwen 3 4B model for text embeddings
- [ ] 04-02: Python service uses Qwen 3 4B model for reranking search results
- [ ] 04-03: Python service stores PDF text chunks and embeddings in Chroma
- [ ] 04-04: Python service returns ranked search results with relevance scores
- [ ] 04-05: User can perform semantic search across document collection
- [ ] 04-06: Search returns 25 ranked results sorted by relevance
- [ ] 04-07: Each search result displays document title
- [ ] 04-08: Each search result displays matching text chunk
- [ ] 04-09: Each search result displays relevance score
- [ ] 04-10: Search results are reranked using Qwen 3 4B reranking model
- [ ] 04-11: Search page provides dedicated UI for querying and viewing results

### Phase 5: Reading & Annotation

**Goal**: Users can read PDFs and create highlights, notes, and cross-document links

**Depends on**: Phase 4

**Requirements**: READ-01, READ-02, READ-03, READ-04, READ-05, READ-06, READ-07, READ-08, ANNO-01, ANNO-02, ANNO-03, ANNO-04, ANNO-05, ANNO-06

**Success Criteria** (what must be TRUE):
1. Reading view displays PDF on left and annotations pane on right
2. PDF renders correctly using PDF.js
3. User can select text in PDF to create highlights
4. User can select text in PDF to create notes
5. Annotations pane shows highlights in yellow and notes in blue
6. Clicking annotation in pane scrolls PDF to that position
7. User can add external URL links to annotations
8. User can add internal deep links to other documents
9. Clicking internal deep link opens target document at linked position
10. All annotations persist in SQLite database

**Plans**: TBD

Plans:
- [ ] 05-01: Reading view displays two-pane layout (PDF on left, annotations on right)
- [ ] 05-02: PDF is rendered using PDF.js in left pane
- [ ] 05-03: User can select text in PDF to create highlight
- [ ] 05-04: User can select text in PDF to create note
- [ ] 05-05: Annotations pane displays all highlights for current document in yellow
- [ ] 05-06: Annotations pane displays all notes for current document in blue
- [ ] 05-07: Clicking highlight in annotations pane scrolls PDF to that position
- [ ] 05-08: Clicking note in annotations pane scrolls PDF to that position
- [ ] 05-09: Highlight stores selected text and its position in SQLite
- [ ] 05-10: Note stores selected text, its position, and user's note in SQLite
- [ ] 05-11: User can add external URL links to annotations
- [ ] 05-12: User can add internal deep links to other documents in collection
- [ ] 05-13: Clicking internal deep link opens target document in reading view at linked position
- [ ] 05-14: SQLite database stores all annotations via better-sqlite3 in Electron main process

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Electron Foundation | 0/3 | Not started | - |
| 2. Python ML Service | 0/4 | Not started | - |
| 3. Document Management | 0/6 | Not started | - |
| 4. Semantic Search | 0/11 | Not started | - |
| 5. Reading & Annotation | 0/14 | Not started | - |
