---
status: complete
phase: 02-python-ml-service
source: 02-01-SUMMARY.md, 02-02-SUMMARY.md, 02-03-SUMMARY.md, 02-04-SUMMARY.md
started: 2026-01-30T23:00:00Z
updated: 2026-01-30T23:35:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Python service startup
expected: Running `cd python-service && python main.py` starts the service. You see "Port file written to..." message, "Starting ML service on http://127.0.0.1:XXXXX", and "Uvicorn running" indicating the server is ready. Service stays running until stopped with Ctrl+C.
result: pass

### 2. Health check endpoint
expected: With service running, `curl http://127.0.0.1:$(cat /tmp/doc-research-ml-port.txt)/health` returns JSON: `{"status": "ok", "service": "document-research-ml", "version": "0.1.0"}` with HTTP 200 status.
result: pass

### 3. PDF upload endpoint
expected: `curl -X POST -F "file=@test.pdf" http://127.0.0.1:PORT/api/pdf/upload` returns JSON with `doc_id` (UUID), `filename`, `chunk_count` (>0 for multi-page PDFs), and `status: "processing"`. The PDF is saved to `/tmp/doc-research-uploads/`.
result: pass

### 4. PDF text extraction
expected: After uploading a PDF and waiting ~2 seconds for background processing, querying the document returns chunks. Each chunk has `text` content, `page_num` (starting from 1), `token_count` (~500), and `char_offset`.
result: pass

### 5. Token-aware chunking
expected: The returned chunks are approximately 500 tokens each with 50 token overlap between adjacent chunks. No chunk exceeds 500 tokens significantly.
result: pass

### 6. ChromaDB persistence
expected: After uploading a PDF, stopping the service (Ctrl+C), restarting it, and querying again - the chunks are still returned from ChromaDB. The ChromaDB data is stored in `~/Library/Application Support/document-research/chroma` on macOS (platform-specific equivalent on other systems).
result: pass

### 7. Document retrieval endpoint
expected: `curl http://127.0.0.1:PORT/api/pdf/documents/{doc_id}` returns JSON with `doc_id`, array of `chunks` (each with `id`, `text`, `metadata`), and `count`. Returns 404 if document not found or still processing.
result: pass

### 8. Document deletion endpoint
expected: `curl -X DELETE http://127.0.0.1:PORT/api/pdf/documents/{doc_id}` returns JSON confirming deletion. Subsequent GET requests for that doc_id return 404.
result: pass

### 9. Port file cleanup on shutdown
expected: When stopping the service with Ctrl+C, the port file (`/tmp/doc-research-ml-port.txt`) is removed. Starting the service again creates a new port file with a (potentially different) port.
result: pass
note: Port file stored in platform-specific temp directory (macOS: /var/folders/.../T/, not /tmp/). Both Python and Electron use the same platform-appropriate API, so they agree on the location.

## Summary

total: 9
passed: 9
issues: 0
pending: 0
skipped: 0

## Gaps

[none]

## Notes

**Port file location:** On macOS, the temp directory is `/var/folders/.../T/` not `/tmp/`. Both Python's `tempfile.gettempdir()` and Electron's `app.getPath('temp')` return the correct platform-specific directory, so the services will find each other's port file correctly. Documentation should reference the platform-specific path rather than assuming `/tmp/`.
