"""Main entry point for the Document Research ML Service.

FastAPI application that starts on an available port and exposes HTTP endpoints
for PDF processing and semantic search.
"""
import sys

# Set PYTHONUNBUFFERED for real-time logging
sys.stdout.reconfigure(line_buffering=True)

from fastapi import FastAPI
import uvicorn

from config import Config, config
from utils.port_utils import get_available_port, write_port_file, get_port_file_path
from api.health import router as health_router
from api.pdf import router as pdf_router

# Create FastAPI application
app = FastAPI(
    title="Document Research ML Service",
    description="Local ML service for PDF processing and semantic search",
    version="0.1.0",
)

# Include health check router
app.include_router(health_router, tags=["health"])

# Include PDF router
app.include_router(pdf_router, tags=["pdf"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint providing service information."""
    return {
        "service": "document-research-ml",
        "version": "0.1.0",
        "status": "running",
    }


if __name__ == "__main__":
    # Get configuration
    cfg = Config.from_env()

    # Find available port if not specified
    if cfg.port == 0:
        port = get_available_port(cfg.host)
    else:
        port = cfg.port

    # Write port to file for Electron discovery
    port_file = get_port_file_path()
    write_port_file(port, port_file)

    print(f"Port file written to: {port_file}", flush=True)
    print(f"Starting ML service on {cfg.host}:{port}", flush=True)

    # Start uvicorn server
    uvicorn.run(
        app,
        host=cfg.host,
        port=port,
        log_level=cfg.log_level,
    )
