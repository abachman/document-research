"""Port discovery and file synchronization utilities.

This module provides functions for finding available ports and writing
port information to files for Electron process discovery.
"""
import socket
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

    Returns:
        Path object pointing to the port file location
    """
    filename = "doc-research-ml-port.txt"
    return Path("/tmp") / filename


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
