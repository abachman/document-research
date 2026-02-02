"""Main entry point for the Document Research ML Service.

FastAPI application that starts on an available port and exposes HTTP endpoints
for PDF processing and semantic search.
"""
import sys
import signal
import time

# Set PYTHONUNBUFFERED for real-time logging
sys.stdout.reconfigure(line_buffering=True)

from fastapi import FastAPI
import uvicorn

from config import Config, config
from utils.port_utils import get_available_port, write_port_file, remove_port_file, get_port_file_path
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


# Global to track port file path for cleanup
_port_file_path = None


def shutdown_handler(signum: int, frame) -> None:
    """Handle shutdown signals gracefully.

    Removes port file and logs shutdown message.
    Called for SIGTERM (production) and SIGINT (Ctrl+C).
    """
    global _port_file_path

    signal_name = signal.Signals(signum).name
    print(f"\n[Shutdown] Received signal {signal_name} ({signum})", flush=True)
    print("[Shutdown] Cleaning up port file...", flush=True)

    if _port_file_path:
        remove_port_file()
        print(f"[Shutdown] Port file removed: {_port_file_path}", flush=True)

    print("[Shutdown] ML service stopped", flush=True)
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, shutdown_handler)  # Production termination
signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C in development


if __name__ == "__main__":
    # Track startup time for debugging
    startup_start = time.time()

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

    # Store globally for cleanup in signal handler
    _port_file_path = str(port_file)

    startup_duration = time.time() - startup_start
    print(f"Port file written to: {port_file}", flush=True)
    print(f"Starting ML service on {cfg.host}:{port}", flush=True)
    print(f"Startup time: {startup_duration:.3f}s", flush=True)

    # Start uvicorn server
    try:
        uvicorn.run(
            app,
            host=cfg.host,
            port=port,
            log_level=cfg.log_level,
        )
    except Exception as e:
        print(f"[Error] Uvicorn startup failed: {e}", flush=True)
        # Clean up port file on startup error
        remove_port_file()
        sys.exit(1)
