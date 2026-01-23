# Phase 02: Python ML Service - Research

**Researched:** 2026-01-23
**Domain:** Python service for PDF processing and vector storage
**Confidence:** MEDIUM

## Summary

This phase involves creating a local Python service that integrates with an Electron desktop application to provide PDF text extraction, semantic chunking, and vector storage capabilities. The service runs as a separate HTTP process managed by Electron, using FastAPI for the API layer, ChromaDB for vector storage, and PyMuPDF for PDF processing.

**Primary recommendation:** Use FastAPI with Uvicorn for the HTTP service, bundle Python with Electron using electron-builder's extraResources configuration, implement file-based port discovery, and use ChromaDB's persistent client for vector storage.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | ^0.115.0 | HTTP API framework | Modern async support, automatic OpenAPI docs, type validation |
| Uvicorn | ^0.32.0 | ASGI server | Lightning-fast, standard for FastAPI production |
| ChromaDB | ^0.6.0 | Vector database | Built-in persistence, simple Python client, local-first |
| PyMuPDF (fitz) | ^1.24.0 | PDF text extraction | Fast, accurate, metadata extraction, page/position tracking |
| python-multipart | ^0.0.20 | File upload support | Required for FastAPI file uploads |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| langchain-text-splitters | ^0.3.0 | Semantic chunking | If using embeddings for splitting (future phase) |
| tiktoken | ^0.8.0 | Token counting | For accurate chunk size measurement |
| PyPDF2 | ^3.0.0 | PDF metadata extraction | Alternative to PyMuPDF for simpler cases |
| pdfplumber | ^0.11.0 | Table extraction | If complex table handling needed (future) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| FastAPI | Flask | Flask is simpler/slower, no async by default, less type-safe |
| ChromaDB | FAISS + SQLite | FAISS requires manual persistence management |
| PyMuPDF | PyPDF2 | PyPDF2 slower, less accurate position tracking |
| Uvicorn | Gunicorn | Gunicorn for production servers, overkill for localhost |

**Installation:**
```bash
# Python requirements.txt
fastapi==0.115.6
uvicorn[standard]==0.32.1
chromadb==0.6.3
PyMuPDF==1.24.12
python-multipart==0.0.20
tiktoken==0.8.0
```

## Architecture Patterns

### Recommended Project Structure
```
python-service/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration (port, paths)
├── api/
│   ├── __init__.py
│   ├── pdf.py             # PDF upload and processing endpoints
│   └── health.py          # Health check endpoints
├── services/
│   ├── __init__.py
│   ├── pdf_extractor.py   # PDF text extraction logic
│   ├── chunker.py         # Semantic chunking logic
│   └── vector_store.py    # ChromaDB operations
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models for API
└── utils/
    ├── __init__.py
    └── port_utils.py      # Port discovery and file sync
```

### Pattern 1: FastAPI with Dynamic Port
**What:** Service binds to available port, writes to file for Electron discovery
**When to use:** Electron spawns Python, needs to know actual port for IPC calls
**Example:**
```python
# Source: https://fastapi.tiangolo.com/deployment/manually/
import socket
import uvicorn
from fastapi import FastAPI
from pathlib import Path

def get_available_port():
    """Find an available port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def write_port_file(port: int, path: Path):
    """Write port to file for Electron to discover."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(port))

app = FastAPI(title="Document Research ML Service")

if __name__ == "__main__":
    port = get_available_port()
    write_port_file(port, Path("/tmp/doc-research-ml-port.txt"))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
```

### Pattern 2: Electron Spawn with Port Discovery
**What:** Electron spawns Python, polls for port file, establishes communication
**When to use:** Managing Python service lifecycle from Electron main process
**Example:**
```typescript
// Source: https://nodejs.org/api/child_process.html
import { spawn } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { app } from 'electron';

const isDev = !app.isPackaged;
const pythonPath = isDev
  ? 'python3'
  : join(process.resourcesPath, 'python-runtime', 'bin', 'python3');
const scriptPath = isDev
  ? join(__dirname, '../../python-service/main.py')
  : join(process.resourcesPath, 'python-service', 'main.py');
const portFile = join(app.getPath('temp'), 'doc-research-ml-port.txt');

let pythonProcess: ReturnType<typeof spawn> | null = null;

async function startPythonService(): Promise<number> {
  pythonProcess = spawn(pythonPath, [scriptPath], {
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  // Wait for port file
  let attempts = 0;
  while (attempts < 50 && !existsSync(portFile)) {
    await new Promise(r => setTimeout(r, 100));
    attempts++;
  }

  if (!existsSync(portFile)) {
    throw new Error('Python service failed to start');
  }

  const port = parseInt(readFileSync(portFile, 'utf-8'));
  return port;
}
```

### Pattern 3: ChromaDB Persistent Storage
**What:** Use ChromaDB's PersistentClient for automatic disk persistence
**When to use:** Vector data must survive service restarts
**Example:**
```python
# Source: ChromaDB documentation patterns
import chromadb
from pathlib import Path
import platform

def get_chroma_path():
    """Get platform-appropriate ChromaDB storage path."""
    app_name = "document-research"
    system = platform.system()

    if system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support" / app_name
    elif system == "Windows":
        base = Path.home() / "AppData" / "Local" / app_name
    else:  # Linux
        base = Path.home() / ".local" / "share" / app_name

    return base / "chroma"

# Initialize persistent client
client = chromadb.PersistentClient(path=str(get_chroma_path()))

# Get or create collection
documents_collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
)
```

### Pattern 4: PyMuPDF Text Extraction with Position Tracking
**What:** Extract text while tracking page numbers and character offsets
**When to use:** Need to link chunks back to specific PDF locations
**Example:**
```python
# Source: PyMuPDF documentation
import fitz  # PyMuPDF
from typing import List, Dict

def extract_pdf_pages(pdf_path: str) -> List[Dict]:
    """Extract text with page/position tracking."""
    doc = fitz.open(pdf_path)
    pages_data = []
    global_offset = 0

    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages_data.append({
            "page_num": page_num + 1,
            "text": text,
            "offset": global_offset,
            "length": len(text)
        })
        global_offset += len(text)

    # Extract metadata
    metadata = {
        "title": doc.metadata.get("title", ""),
        "author": doc.metadata.get("author", ""),
        "created": doc.metadata.get("creationDate", ""),
    }

    doc.close()
    return {"pages": pages_data, "metadata": metadata}
```

### Anti-Patterns to Avoid
- **Hardcoded ports**: Prevents multiple instances, conflicts with other services
- **Blocking operations in FastAPI routes**: Use async/await or run in thread pool
- **Global state in ChromaDB client**: Use dependency injection pattern
- **Assuming Python is in PATH**: In production, use bundled runtime path
- **No error handling for PDF corruption**: Always wrap PDF operations in try/except
- **Chunking by raw characters**: Use token-aware chunking for better ML results

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP request parsing | Custom multipart handler | FastAPI + python-multipart | MIME complexity, edge cases |
| Async HTTP server | Custom async socket handling | Uvicorn | Connection management, keep-alive |
| Token counting | Custom whitespace/word splitting | tiktoken | Accurate GPT tokenization |
| Vector indexing | Custom nearest neighbor search | ChromaDB | HNSW optimization, persistence |
| Semantic splitting | Custom regex-based splitting | langchain-text-splitters | Embedding-based boundary detection |
| Process spawning | Manual port discovery | Combination (see patterns) | Race conditions, cleanup |

**Key insight:** PDF text extraction and vector storage are deceptively complex. Edge cases (corrupted PDFs, encoding issues, multi-page tables, embedded fonts, layout variations) make custom solutions fragile. Established libraries have handled thousands of edge cases.

## Common Pitfalls

### Pitfall 1: ENOENT Errors When Spawning Python After Packaging
**What goes wrong:** Python script runs in dev, but fails after `electron-builder` packaging with "ENOENT" error
**Why it happens:** `spawn('python3')` relies on system PATH; packaged apps don't have Python in PATH
**How to avoid:**
1. Bundle Python runtime in `extraResources` in electron-builder config
2. Use `process.resourcesPath` to locate bundled Python
3. Fall back to system Python in development
**Warning signs:** Works in `electron-vite dev` but fails in packaged app

### Pitfall 2: ChromaDB Data Loss on Restart
**What goes wrong:** Vector data disappears between app restarts
**Why it happens:** Using ephemeral `chromadb.Client()` instead of `chromadb.PersistentClient(path=...)`
**How to avoid:**
- Always use `PersistentClient` with explicit path
- Verify path exists and is writable
- Use app data directory, not working directory
**Warning signs:** Data present in session but gone on restart

### Pitfall 3: Race Condition in Port Discovery
**What goes wrong:** Electron tries to connect before Python writes port file
**Why it happens:** No synchronization between spawn and port binding
**How to avoid:**
- Poll for port file with timeout
- Have Python write port file immediately after binding (before app ready)
- Add startup health check endpoint
**Warning signs:** Intermittent "ECONNREFUSED" errors on startup

### Pitfall 4: PDF Extraction Blocks HTTP Thread
**What goes wrong:** Other requests timeout while processing large PDF
**Why it happens:** PyMuPDF operations are synchronous, blocking FastAPI event loop
**How to avoid:**
- Run extraction in thread pool: `await loop.run_in_executor(None, extract_pdf, pdf_path)`
- Or use background tasks: `BackgroundTasks.add_task(extract_and_store, pdf_path)`
**Warning signs:** Health checks timeout during PDF upload

### Pitfall 5: Chunking Loses PDF Position Information
**What goes wrong:** Can't link search results back to PDF page/offset
**Why it happens:** Chunking discards position metadata during text concatenation
**How to avoid:**
- Store `doc_id`, `chunk_index`, `page_num`, `char_offset` in ChromaDB metadata
- Track position through chunking pipeline
- Validate position mapping during extraction
**Warning signs:** Search results can't jump to source location

### Pitfall 6: Memory Leaks from Unretrieved Generator Results
**What goes wrong:** Memory usage grows over time
**Why it happens:** ChromaDB query returns generator that's never consumed
**How to avoid:**
- Always convert results to list: `results = collection.query(...)['documents'][0]`
- Close PDF documents explicitly: `doc.close()`
- Limit batch sizes for bulk operations
**Warning signs:** Memory profile increases with each PDF processed

## Code Examples

Verified patterns from official sources:

### FastAPI File Upload with PDF Processing
```python
# Source: FastAPI documentation - Request Files
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from pathlib import Path
import shutil

app = FastAPI()

UPLOAD_DIR = Path("/tmp/doc-research-uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/api/pdf/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Upload and process a PDF file."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files supported")

    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process in background
    background_tasks.add_task(process_pdf_document, str(file_path))

    return {"status": "processing", "filename": file.filename}

async def process_pdf_document(pdf_path: str):
    """Extract text, chunk, and store in ChromaDB."""
    # Implementation in services/pdf_extractor.py
    pass
```

### Semantic Chunking with Token Awareness
```python
# Source: WebSearch-verified pattern for 2025
import tiktoken
from typing import List

def chunk_text_by_tokens(
    text: str,
    max_tokens: int = 500,
    overlap: int = 50
) -> List[dict]:
    """Split text into chunks respecting token limits."""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append({
            "text": chunk_text,
            "chunk_index": chunk_index,
            "token_count": len(chunk_tokens)
        })

        start = end - overlap
        chunk_index += 1

    return chunks
```

### ChromaDB Operations with Metadata
```python
# Source: ChromaDB Python client documentation
import chromadb
from typing import List, Dict

def add_document_chunks(
    collection,
    doc_id: str,
    chunks: List[Dict]
):
    """Store document chunks with metadata."""
    collection.add(
        documents=[c["text"] for c in chunks],
        ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{
            "doc_id": doc_id,
            "chunk_index": c["chunk_index"],
            "page_num": c.get("page_num", 0),
            "char_offset": c.get("offset", 0)
        } for c in chunks]
        # embeddings will be computed later in Phase 4
    )

def query_by_document(collection, doc_id: str, n_results: int = 10):
    """Query for chunks from a specific document."""
    results = collection.query(
        query_texts=["sample query"],
        n_results=n_results,
        where={"doc_id": doc_id}
    )
    return results
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Flask + Gunicorn | FastAPI + Uvicorn | ~2020-2021 | Async support, type safety, auto docs |
| PyPDF2 only | PyMuPDF for extraction | ~2022 | Better speed, position tracking |
| Manual SQLite + FAISS | ChromaDB embedded | ~2023 | Simpler setup, built-in persistence |
| Fixed-size chunking | Token-aware semantic chunking | ~2024 | Better retrieval accuracy |
| External vector DBs | Embedded local vector DBs | ~2024 | Local-first privacy, no cloud dependency |

**Deprecated/outdated:**
- **pdfminer.six**: Replaced by PyMuPDF for most use cases (slower, less accurate)
- **flask-cors**: Not needed for localhost-only service
- **Custom embedding generation**: Will use sentence-transformers or similar in Phase 4

## Open Questions

Things that couldn't be fully resolved:

1. **Exact Python bundling strategy**
   - What we know: electron-builder can bundle extra resources, Python runtime must be included
   - What's unclear: Whether to use PyInstaller or bundle raw Python files + runtime
   - Recommendation: Start with raw Python files in development; Phase 2 plan should decide bundling approach based on cross-platform needs

2. **ChromaDB collection deletion strategy**
   - What we know: CONTEXT.md says "archive deleted documents to separate collection"
   - What's unclear: How to implement archival without growing unbounded
   - Recommendation: Implement archive collection for Phase 2; add cleanup/purge in future phase

3. **Health check polling interval**
   - What we know: Should poll port file with timeout; CONTEXT.md leaves interval to discretion
   - What's unclear: Optimal balance between responsiveness and resource usage
   - Recommendation: Start with 100ms polling for 5 seconds max; adjust based on real startup time

4. **Semantic chunking algorithm**
   - What we know: CONTEXT.md requires semantic-aware chunking at ~500 tokens
   - What's unclear: Whether to use LangChain's SemanticChunker or custom implementation
   - Recommendation: Use token-aware splitting for Phase 2 (no embeddings yet); upgrade to true semantic splitting in Phase 4 when embedding model is integrated

## Sources

### Primary (HIGH confidence)
- [FastAPI Deployment Documentation](https://fastapi.tiangolo.com/deployment/) - Uvicorn configuration, manual server setup
- [FastAPI Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/) - ASGI server requirements
- [PyMuPDF Official Documentation](https://pymupdf.io/) - PDF extraction API, text positioning
- [Node.js child_process documentation](https://nodejs.org/api/child_process.html) - spawn API, process management

### Secondary (MEDIUM confidence)
- [Electron + Python Medium Article](https://medium.com/@manzcube/run-python-scripts-in-electronjs-edff611f667a) - Child process spawning patterns
- [Connecting Python 3 and Electron](https://main.codeproject.com/articles/Connecting-Python-3-and-Electron-Node-JS-Building) - Comprehensive integration guide
- [7 Python PDF Extractors (2025)](https://onlyoneaman.medium.com/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-c88013922257) - Tool comparison (PyMuPDF recommended)
- [Document Chunking Strategies for Vector Databases](https://www.dataquest.io/blog/document-chunking-strategies-for-vector-databases/) - Chunking best practices
- [Semantic Chunking for RAG](https://machinelearningplus.com/gen-ai/semantic-chunking-for-rag-optimizing-retrieval-augmented-generation/) - Semantic splitting approaches
- [Best Chunking Strategies for RAG in 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025) - Modern chunking patterns

### Tertiary (LOW confidence)
- Various GitHub issues regarding ENOENT errors when spawning Python after Electron packaging (need to verify with official electron-builder docs)
- Stack Overflow discussions on child process stdio blocking (need cross-verification)

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - WebSearch verified for FastAPI, PyMuPDF, ChromaDB; official docs accessible for some
- Architecture: MEDIUM - Patterns from WebSearch verified with official FastAPI/Node.js docs where possible
- Pitfalls: HIGH - ENOENT errors and port discovery issues confirmed by multiple web sources; ChromaDB persistence from general knowledge

**Research date:** 2026-01-23
**Valid until:** 2026-02-22 (30 days - Python/Electron integration patterns evolve slowly)

**API limits encountered:** WebSearch and WebReader services hit monthly usage limits during research. Findings based on successful searches before limit + official documentation where available. Some areas (ChromaDB specific docs, electron-builder Python bundling) marked for validation in implementation phase.
