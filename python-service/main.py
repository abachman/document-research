"""Main entry point for the Document Research ML Service.

FastAPI application that starts on an available port and exposes HTTP endpoints
for PDF processing and semantic search.
"""
import socket
import sys
from pathlib import Path

# Set PYTHONUNBUFFERED for real-time logging
sys.stdout.reconfigure(line_buffering=True)

from fastapi import FastAPI
import uvicorn

from config import Config, config


def get_available_port(host: str = "127.0.0.1") -> int:
    """Find an available port on the specified host.

    Args:
        host: The host address to bind to (default: 127.0.0.1)

    Returns:
        An available port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def get_port_file_path() -> Path:
    """Get the platform-appropriate path for the port file.

    Returns:
        Path object pointing to the port file location
    """
    filename = "doc-research-ml-port.txt"
    return Path("/tmp") / filename


def write_port_file(port: int, path: Path) -> None:
    """Write the port number to a file for Electron to discover.

    Args:
        port: The port number to write
        path: The file path to write to
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(port))


# Create FastAPI application
app = FastAPI(
    title="Document Research ML Service",
    description="Local ML service for PDF processing and semantic search",
    version="0.1.0",
)


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
