"""Port discovery and file synchronization utilities.

This module provides functions for finding available ports and writing
port information to files for Electron process discovery.
"""
import socket
import tempfile
from pathlib import Path


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

    Uses tempfile.gettempdir() for cross-platform compatibility:
    - macOS/Linux: /tmp
    - Windows: %TEMP% (typically C:\\Users\\<username>\\AppData\\Local\\Temp)

    Returns:
        Path object pointing to the port file location
    """
    filename = "doc-research-ml-port.txt"
    return Path(tempfile.gettempdir()) / filename


def write_port_file(port: int, path: Path | None = None) -> None:
    """Write the port number to a file for Electron to discover.

    Args:
        port: The port number to write
        path: Optional file path to write to. If not provided, uses
            get_port_file_path() to determine the location.
    """
    if path is None:
        path = get_port_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(port))


def remove_port_file(path: Path | None = None) -> None:
    """Remove the port file (cleanup on shutdown).

    Args:
        path: Optional file path to remove. If not provided, uses
            get_port_file_path() to determine the location.
    """
    if path is None:
        path = get_port_file_path()
    if path.exists():
        path.unlink()
