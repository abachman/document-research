"""Configuration for the Document Research ML Service.

Provides configuration class with host, port, and logging settings.
"""
import os
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


# Default configuration instance
config = Config.from_env()
