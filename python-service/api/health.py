"""Health check endpoints for the ML service.

Provides health status endpoint for Electron to verify service availability.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint returning service status.

    Returns:
        JSON response with status, service name, and version
    """
    return {
        "status": "ok",
        "service": "document-research-ml",
        "version": "0.1.0",
    }
