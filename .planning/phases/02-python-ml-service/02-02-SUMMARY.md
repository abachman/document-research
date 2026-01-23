---
phase: 02-python-ml-service
plan: 02
subsystem: pdf-processing
tags: [pymupdf, tiktoken, fastapi, pdf-extraction, token-chunking, file-upload]

# Dependency graph
requires:
  - phase: 02-python-ml-service
    plan: 02-01
    provides: FastAPI HTTP service with dynamic port binding, modular structure
provides:
  - PDF text extraction with position tracking using PyMuPDF
  - Token-aware text chunking with tiktoken (500 tokens, 50 overlap)
  - PDF upload HTTP endpoint (POST /api/pdf/upload)
  - Pydantic schemas for type-safe API responses
affects:
  - 02-python-ml-service/02-03 (ChromaDB vector storage will store these chunks)
  - 02-python-ml-service/02-04 (Electron will call this upload endpoint)
  - 04-semantic-search/04-01 (Chunks will be embedded for semantic search)

# Tech tracking
tech-stack:
  added: [PyMuPDF 1.24.12, tiktoken 0.12.0, pydantic]
  patterns: [service layer pattern, token-aware chunking, position tracking for PDF navigation]

key-files:
  created: [python-service/services/pdf_extractor.py, python-service/services/chunker.py, python-service/api/pdf.py, python-service/models/schemas.py]
  modified: [python-service/main.py, python-service/requirements.txt]

key-decisions:
  - "PyMuPDF over PyPDF2 for faster and more accurate position tracking"
  - "tiktoken cl100k_base encoding (GPT-4 tokenizer) for chunk boundaries"
  - "500 token chunks with 50 token overlap for context preservation"
  - "Position tracking (page_num, char_offset) for future PDF navigation"
  - "tiktoken>=0.8.0 to use latest version with Python 3.14 wheels"

patterns-established:
  - "Pattern 1: Service layer pattern - services/ package for business logic separate from API"
  - "Pattern 2: Token-aware chunking - use tiktoken encoding for ML-friendly text splits"
  - "Pattern 3: Position tracking - track page_num and char_offset for PDF navigation"

# Metrics
duration: 4min
completed: 2026-01-23
---

# Phase 2: Plan 2 Summary

**PDF text extraction with token-aware chunking via HTTP upload endpoint using PyMuPDF and tiktoken**

## Performance

- **Duration:** 4 min
- **Started:** 2026-01-23T21:29:44Z
- **Completed:** 2026-01-23T21:34:19Z
- **Tasks:** 3
- **Files modified:** 8

## Accomplishments

- Created PDF text extraction service using PyMuPDF (fitz) with position tracking
- Implemented token-aware chunking service using tiktoken cl100k_base encoding
- Built PDF upload HTTP endpoint with file validation and metadata extraction
- Added Pydantic models for type-safe API responses (UploadResponse, Chunk)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create PDF extraction service with PyMuPDF** - `33ec6c4` (feat)
2. **Task 2: Create token-aware chunking service** - `b3448b6` (feat)
3. **Task 3: Create PDF upload API endpoint** - `efae8bb` (feat)

**Plan metadata:** TBD (docs: complete plan)

## Files Created/Modified

- `python-service/services/__init__.py` - Services package init file
- `python-service/services/pdf_extractor.py` - PDF text extraction with position tracking (extract_pdf_pages function)
- `python-service/services/chunker.py` - Token-aware chunking with sliding window (chunk_text_by_tokens function)
- `python-service/api/pdf.py` - PDF upload endpoint POST /api/pdf/upload
- `python-service/models/__init__.py` - Models package init file
- `python-service/models/schemas.py` - Pydantic models: UploadResponse, Chunk
- `python-service/main.py` - Updated to include PDF router
- `python-service/requirements.txt` - Added PyMuPDF==1.24.12, tiktoken>=0.8.0

## Decisions Made

**PyMuPDF over PyPDF2:**
- Faster text extraction with better accuracy
- More reliable position tracking for PDF navigation
- Actively maintained with good Python 3 support

**tiktoken cl100k_base encoding:**
- GPT-4's tokenizer provides better chunk boundaries for ML models
- cl100k_base is widely adopted for embeddings and LLM applications
- Token-based splitting is more accurate than character-based for ML

**500 token chunks with 50 token overlap:**
- 500 tokens is a good balance between context size and embedding quality
- 50 token overlap preserves context between chunks for better search results
- Sliding window approach ensures no text is missed at boundaries

**Position tracking:**
- Track page_num (1-based) and char_offset for each chunk
- Enables future features like PDF viewer navigation from search results
- Supports Phase 4 semantic linking back to source PDF locations

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed tiktoken installation for Python 3.14**

- **Found during:** Task 2 (token-aware chunking service)
- **Issue:** tiktoken==0.8.0 required Rust compiler to build from source on Python 3.14
- **Fix:** Updated to tiktoken>=0.8.0, which installed version 0.12.0 with pre-built wheels for Python 3.14
- **Files modified:** python-service/requirements.txt
- **Verification:** `pip3 install tiktoken` succeeded, imports work correctly
- **Committed in:** `b3448b6` (part of Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Version bump necessary for Python 3.14 compatibility. No functional change to API or behavior.

## Issues Encountered

**Issue 1: Tiktoken build failure on Python 3.14**
- **Problem:** tiktoken 0.8.0 doesn't have pre-built wheels for Python 3.14, requires Rust compiler
- **Solution:** Used tiktoken>=0.8.0 to install latest version (0.12.0) which has Python 3.14 wheels
- **Impact:** Minor version bump, backward compatible API

## User Setup Required

**Python dependencies must be installed:**

```bash
cd python-service
pip3 install -r requirements.txt
```

This is required for:
- PyMuPDF for PDF text extraction
- tiktoken for token-aware chunking
- pydantic for API schema validation

## Next Phase Readiness

**Ready for next phase:**

- PDF upload endpoint working with text extraction and chunking
- Chunk metadata includes doc_id, page_num, chunk_index, char_offset
- Service layer pattern established for easy extension
- Upload directory (/tmp/doc-research-uploads) created for temporary storage

**Next steps (02-03):**

- Add ChromaDB vector storage for chunks
- Store chunks with metadata in Chroma collection
- Add background task processing for large PDFs
- Implement chunk retrieval by doc_id

**Next steps (02-04):**

- Electron process will call POST /api/pdf/upload
- Parse UploadResponse to get doc_id and chunk_count
- Store document metadata in SQLite database

**Blockers/Concerns:**

None - PDF processing pipeline is working and ready for ChromaDB integration in Plan 02-03.

---
*Phase: 02-python-ml-service*
*Completed: 2026-01-23*
