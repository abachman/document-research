# Document Research

Local PDF document research tool with semantic search powered by local ML models.

## Overview

Document Research is a desktop application that allows you to upload, organize, search, and annotate PDF documents entirely on your local machine. The application uses local ML models for semantic understanding, so your documents never leave your computer.

**Key Features:**

- Local-only processing (no cloud services, no data leaves your machine)
- Semantic search powered by ChromaDB vector embeddings
- Token-aware text chunking for accurate content extraction
- Modern Electron desktop application with Next.js UI
- Standalone Python ML service for testing and development

## Prerequisites

- **Node.js** 18+ (for Electron/Next.js)
- **Python 3.13+** (IMPORTANT: ChromaDB is incompatible with Python 3.14)
- **npm** or **yarn**

> **Note:** The Python ML service requires Python 3.13 specifically. ChromaDB dependencies (Pydantic v1, onnxruntime) are not compatible with Python 3.14.

## Quick Start (Electron App)

```bash
# Install dependencies
npm install

# Start development server (Next.js + Electron)
npm run dev
```

This will:
1. Start the Next.js development server on port 3000
2. Launch the Electron application
3. Start the Python ML service automatically on first use

The Electron app handles Python service startup automatically, so you don't need to manage it manually.

## Python Service

The Python ML service can be run standalone for testing and development. The service provides HTTP endpoints for PDF processing, text extraction, and semantic search.

### Installation

```bash
cd python-service
pip install -r requirements.txt
```

### Starting the Service

```bash
cd python-service
python main.py
```

The service will:
- Find an available port automatically
- Write the port to `/tmp/doc-research-ml-port.txt` (or `%TEMP%\doc-research-ml-port.txt` on Windows)
- Log startup information to stdout

**Expected output:**

```
Port file written to: /tmp/doc-research-ml-port.txt
Starting ML service on 127.0.0.1:XXXXX
Startup time: X.XXXs
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:XXXXX
```

### Stopping the Service

Press `Ctrl+C` to stop the service. The port file will be automatically cleaned up.

**On shutdown:**
```
[Shutdown] Received signal SIGINT (2)
[Shutdown] Cleaning up port file...
[Shutdown] Port file removed: /tmp/doc-research-ml-port.txt
[Shutdown] ML service stopped
```

## Python Service Testing

The following examples show how to test the Python ML service manually using curl.

### 1. Health Check

```bash
# Get the port from the port file
PORT=$(cat /tmp/doc-research-ml-port.txt)  # macOS/Linux
# or type %TEMP%\doc-research-ml-port.txt on Windows

# Check service health
curl http://127.0.0.1:$PORT/health
```

**Expected response:**

```json
{
  "status": "ok",
  "service": "document-research-ml",
  "version": "0.1.0"
}
```

### 2. Upload a PDF

```bash
curl -X POST http://127.0.0.1:$PORT/api/pdf/upload \
  -F "file=@/path/to/document.pdf"
```

**Expected response:**

```json
{
  "status": "processing",
  "doc_id": "uuid-here",
  "filename": "document.pdf",
  "chunk_count": 0,
  "metadata": {
    "file_path": "/tmp/doc-research-uploads/uuid.pdf"
  }
}
```

**Note:** Processing happens in the background. Wait 1-2 seconds before querying to allow text extraction and chunking to complete.

### 3. Query Document Chunks

```bash
curl http://127.0.0.1:$PORT/api/pdf/documents/{doc_id}
```

Replace `{doc_id}` with the UUID from the upload response.

**Expected response:**

```json
{
  "doc_id": "uuid-here",
  "chunks": [
    {
      "id": "chunk-id",
      "text": "chunk content...",
      "metadata": {
        "page_num": 1,
        "char_offset": 0,
        "doc_id": "uuid"
      }
    }
  ],
  "count": 10
}
```

### 4. Delete Document

```bash
curl -X DELETE http://127.0.0.1:$PORT/api/pdf/documents/{doc_id}
```

**Expected response:**

```json
{
  "success": true,
  "doc_id": "uuid-here",
  "count": -1,
  "message": "Document uuid-here deleted from vector store"
}
```

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| POST | `/api/pdf/upload` | Upload and process PDF |
| GET | `/api/pdf/documents/{doc_id}` | Get document chunks |
| DELETE | `/api/pdf/documents/{doc_id}` | Delete document |

**Interactive API documentation:**

Once the service is running, visit `http://127.0.0.1:{PORT}/docs` for interactive Swagger UI documentation.

## Development

```bash
# Start only Next.js dev server
npm run dev:next

# Start only Electron (requires Next.js running)
npm run dev:electron

# Build for production
npm run build

# Build platform-specific distributables
npm run build:mac    # macOS
npm run build:win    # Windows
npm run build:linux  # Linux
```

## Tech Stack

**Frontend:**
- Electron - Desktop application framework
- Next.js - React framework with Pages Router
- React - UI library
- Tailwind CSS - Styling
- TypeScript - Type safety

**Backend (ML Service):**
- FastAPI - Python web framework
- Uvicorn - ASGI server
- ChromaDB - Vector database for embeddings
- PyMuPDF - PDF text extraction
- tiktoken - Token-aware text chunking (GPT-4 tokenizer)

**Data Storage:**
- SQLite - Document metadata (via better-sqlite3)
- ChromaDB - Vector embeddings for semantic search

## Project Structure

```
document-research/
├── electron/              # Electron main process
├── python-service/        # Python ML service
│   ├── api/              # FastAPI endpoints
│   ├── services/         # Business logic
│   ├── models/           # Data schemas
│   └── utils/            # Utilities
├── pages/                # Next.js pages
└── public/               # Static assets
```

## License

MIT
