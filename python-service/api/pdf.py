"""PDF upload and processing API endpoints.

This module provides HTTP endpoints for uploading PDF files, extracting text,
and chunking the content for vector storage.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
from pathlib import Path
import shutil
from typing import Dict

from services.pdf_extractor import extract_pdf_pages
from services.chunker import chunk_text_by_tokens
from models.schemas import UploadResponse

# Create router for PDF endpoints
router = APIRouter(prefix="/api/pdf")

# Directory for uploaded PDFs
UPLOAD_DIR = Path("/tmp/doc-research-uploads")

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """Upload and process a PDF file.

    This endpoint accepts a PDF file upload, extracts text from all pages,
    chunks the text by tokens, and returns metadata about the processed document.

    The PDF is stored temporarily in /tmp/doc-research-uploads/ with the
    doc_id as the filename. Vector storage will be added in Plan 02-03.

    Args:
        file: Uploaded PDF file (must have .pdf extension)

    Returns:
        UploadResponse with status, doc_id, filename, chunk_count, metadata

    Raises:
        HTTPException 400: If file is not a PDF
        HTTPException 500: If PDF processing fails
    """
    # Validate file extension
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted. Please upload a file with .pdf extension."
        )

    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    # Save uploaded file
    file_path = UPLOAD_DIR / f"{doc_id}.pdf"

    try:
        # Write uploaded file to disk
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract pages from PDF
        pages_data = extract_pdf_pages(str(file_path))

        # Chunk text by tokens
        chunks = chunk_text_by_tokens(
            pages_data["pages"],
            max_tokens=500,
            overlap=50
        )

        # Add doc_id to each chunk (for later vector storage)
        for chunk in chunks:
            chunk["doc_id"] = doc_id

        # Build response
        # Note: status is "processed" not "stored" - storage will be added in Plan 02-03
        return UploadResponse(
            status="processed",
            doc_id=doc_id,
            filename=file.filename,
            chunk_count=len(chunks),
            metadata=pages_data["metadata"]
        )

    except ValueError as e:
        # Handle PDF extraction errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
