"""Configuration for the Document Research ML Service.

Provides configuration class with host, port, and logging settings.
"""
import os
import platform
from pathlib import Path
from dataclasses import dataclass
from typing import Literal


@dataclass
class Config:
    """Configuration settings for the ML service."""

    host: str = "127.0.0.1"
    port: int = 0  # 0 means dynamically assigned
    log_level: Literal["critical", "error", "warning", "info", "debug"] = "info"

    # Health check constants
    health_check_interval: float = 1.0  # seconds
    max_startup_time: float = 5.0  # seconds

    # Environment overrides
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables with defaults."""
        return cls(
            host=os.getenv("ML_SERVICE_HOST", "127.0.0.1"),
            port=int(os.getenv("ML_SERVICE_PORT", "0")),
            log_level=os.getenv("ML_SERVICE_LOG_LEVEL", "info"),
        )


def get_app_data_path() -> Path:
    """Get platform-appropriate application data directory.

    Returns:
        Path to the application data directory for the current platform.
        Creates the directory if it doesn't exist.

    Platform locations:
        macOS:     ~/Library/Application Support/document-research
        Windows:   ~/AppData/Local/document-research
        Linux:     ~/.local/share/document-research
    """
    app_name = "document-research"
    system = platform.system()

    if system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support" / app_name
    elif system == "Windows":
        base = Path.home() / "AppData" / "Local" / app_name
    else:  # Linux and others
        base = Path.home() / ".local" / "share" / app_name

    # Create directory if it doesn't exist
    base.mkdir(parents=True, exist_ok=True)
    return base


# Default configuration instance
config = Config.from_env()

# ChromaDB storage directory (persistent vector database storage)
CHROMA_DIR = get_app_data_path() / "chroma"

# Ensure ChromaDB directory exists
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# Upload directory for temporary PDF storage
UPLOAD_DIR = Path("/tmp/doc-research-uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
