---
phase: quick
plan: 001
type: execute
wave: 1
depends_on: []
files_modified: [README.md]
autonomous: true
user_setup: []

must_haves:
  truths:
    - "README.md exists at project root"
    - "README contains project title and description"
    - "README contains Quick Start section for running the Electron app"
    - "README contains Python Service Testing section for standalone testing"
    - "README contains Prerequisites section (Node.js, Python 3.13+, npm)"
    - "README contains Python Service section with install/start/stop instructions"
  artifacts:
    - path: "README.md"
      provides: "Project documentation and setup instructions"
      min_lines: 80
  key_links:
    - from: "README.md"
      to: "python-service/requirements.txt"
      via: "pip install instruction"
      pattern: "pip install.*requirements.txt"
    - from: "README.md"
      to: "python-service/main.py"
      via: "python main.py instruction"
      pattern: "python.*main.py"
---

<objective>
Write a comprehensive README.md that provides:
1. Project overview with title and description
2. Quick Start section for running the Electron desktop application
3. Python Service Testing section for standalone testing of the ML service

Purpose: Enable new developers and users to quickly understand the project and get started running both the main application and testing the Python ML service independently
Output: Complete README.md at project root (~100+ lines)
</objective>

<execution_context>
@./.claude/get-shit-done/workflows/execute-plan.md
@./.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@package.json
@python-service/main.py
@python-service/requirements.txt
@python-service/api/pdf.py
@python-service/api/health.py
@python-service/utils/port_utils.py
</context>

<tasks>

<task type="auto">
  <name>Write comprehensive README.md</name>
  <files>README.md</files>
  <action>Create README.md with the following structure:

## Header
- Project title: "# Document Research"
- Tagline: "Local PDF document research tool with semantic search powered by local ML models"
- Brief description paragraph

## Prerequisites
- Node.js (for Electron/Next.js)
- Python 3.13+ (IMPORTANT: ChromaDB is incompatible with Python 3.14)
- npm or yarn

## Quick Start (Electron App)
```bash
# Install dependencies
npm install

# Start development server (Next.js + Electron)
npm run dev
```

## Python Service
This section describes the standalone Python ML service for manual testing/development.

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
- Write the port to /tmp/doc-research-ml-port.txt (or %TEMP%\doc-research-ml-port.txt on Windows)
- Log startup information to stdout

Expected output:
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
Press Ctrl+C to stop the service. The port file will be automatically cleaned up.

## Python Service Testing

### 1. Health Check
```bash
# Get the port from the port file
PORT=$(cat /tmp/doc-research-ml-port.txt)  # macOS/Linux
# or type %TEMP%\doc-research-ml-port.txt on Windows

# Check service health
curl http://127.0.0.1:$PORT/health
```

Expected response:
```json
{"status": "ok", "service": "document-research-ml", "version": "0.1.0"}
```

### 2. Upload a PDF
```bash
curl -X POST http://127.0.0.1:$PORT/api/pdf/upload \
  -F "file=@/path/to/document.pdf"
```

Expected response:
```json
{
  "status": "processing",
  "doc_id": "uuid-here",
  "filename": "document.pdf",
  "chunk_count": 0,
  "metadata": {"file_path": "/tmp/doc-research-uploads/uuid.pdf"}
}
```

Note: Processing happens in the background. Wait 1-2 seconds before querying.

### 3. Query Document Chunks
```bash
curl http://127.0.0.1:$PORT/api/pdf/documents/{doc_id}
```

Replace {doc_id} with the UUID from the upload response.

Expected response:
```json
{
  "doc_id": "uuid-here",
  "chunks": [
    {
      "id": "chunk-id",
      "text": "chunk content...",
      "metadata": {"page_num": 1, "char_offset": 0, "doc_id": "uuid"}
    }
  ],
  "count": 10
}
```

### 4. Delete Document
```bash
curl -X DELETE http://127.0.0.1:$PORT/api/pdf/documents/{doc_id}
```

Expected response:
```json
{
  "success": true,
  "doc_id": "uuid-here",
  "count": -1,
  "message": "Document uuid-here deleted from vector store"
}
```

## API Endpoints Reference
- GET / - Service information
- GET /health - Health check
- POST /api/pdf/upload - Upload and process PDF
- GET /api/pdf/documents/{doc_id} - Get document chunks
- DELETE /api/pdf/documents/{doc_id} - Delete document

## Development
- `npm run dev:next` - Start only Next.js dev server
- `npm run dev:electron` - Start only Electron (requires Next.js running)
- `npm run build` - Build for production

## Tech Stack
- Frontend: Electron + Next.js + React
- Backend: Python FastAPI
- ML/Data: ChromaDB, tiktoken, PyMuPDF
</action>
<verify>File exists at /Users/adambachman/workspace/document-research/README.md with 80+ lines and contains all required sections</verify>
<done>README.md is complete with Quick Start, Python Service setup, and Testing sections</done>
</task>

</tasks>

<verification>
- README.md exists at project root
- Contains project title and description
- Contains Prerequisites section with Python 3.13+ requirement
- Contains Quick Start section for Electron app
- Contains Python Service section with install/start/stop instructions
- Contains Python Service Testing section with curl examples for all endpoints
- Contains API Endpoints Reference
- File is 80+ lines
</verification>

<success_criteria>
README.md exists, is comprehensive, and enables a new developer to:
1. Understand what the project is
2. Install prerequisites
3. Start the Electron application
4. Start and test the Python ML service independently
</success_criteria>

<output>
After completion, create `.planning/quick/001-readme/001-SUMMARY.md`
</output>
