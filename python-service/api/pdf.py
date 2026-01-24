"""PDF upload and processing API endpoints.

This module provides HTTP endpoints for uploading PDF files, extracting text,
and chunking the content for vector storage.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uuid
from pathlib import Path
import shutil
from typing import Dict
import logging

from services.pdf_extractor import extract_pdf_pages
from services.chunker import chunk_text_by_tokens
from services.vector_store import (
    get_documents_collection,
    add_document_chunks,
    query_by_document,
    delete_document
)
from models.schemas import UploadResponse

# Configure logging
logger = logging.getLogger(__name__)

# Create router for PDF endpoints
router = APIRouter(prefix="/api/pdf")

# Directory for uploaded PDFs
UPLOAD_DIR = Path("/tmp/doc-research-uploads")

# Ensure upload directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def process_and_store_pdf(doc_id: str, file_path: str) -> None:
    """Process PDF and store chunks in ChromaDB vector store.

    This background task extracts text from the PDF, chunks it by tokens,
    and stores the chunks in ChromaDB with metadata for retrieval.

    Args:
        doc_id: Unique document identifier (UUID).
        file_path: Path to the uploaded PDF file.

    Note:
        This function runs asynchronously in the background to avoid
        blocking the HTTP response thread, preventing timeouts on large PDFs.
    """
    try:
        # Extract pages from PDF
        pages_data = extract_pdf_pages(file_path)

        # Chunk text by tokens
        chunks = chunk_text_by_tokens(
            pages_data["pages"],
            max_tokens=500,
            overlap=50
        )

        # Add doc_id to each chunk for metadata filtering
        for chunk in chunks:
            chunk["doc_id"] = doc_id

        # Get ChromaDB collection
        collection = get_documents_collection()

        # Store chunks in vector store
        result = add_document_chunks(collection, doc_id, chunks)

        logger.info(
            f"Stored {result['count']} chunks for document {doc_id} "
            f"from {file_path}"
        )

    except Exception as e:
        logger.error(f"Failed to process and store PDF {doc_id}: {str(e)}")
        # Note: In production, you might want to store failure status
        # in a database for user feedback


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> UploadResponse:
    """Upload and process a PDF file.

    This endpoint accepts a PDF file upload, saves it to disk, and initiates
    background processing to extract text, chunk it, and store in ChromaDB.
    Background processing prevents HTTP timeout on large PDFs.

    The PDF is stored in /tmp/doc-research-uploads/ with the doc_id as filename.
    Chunks are stored in ChromaDB with doc_id metadata for retrieval.

    Args:
        file: Uploaded PDF file (must have .pdf extension)
        background_tasks: FastAPI BackgroundTasks for async processing

    Returns:
        UploadResponse with status "processing", doc_id, filename.
        chunk_count is 0 until background processing completes.

    Raises:
        HTTPException 400: If file is not a PDF
        HTTPException 500: If file save fails

    Note:
        Query GET /documents/{doc_id} after 1-2 seconds to verify processing.
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

        # Add background task to process PDF and store in ChromaDB
        background_tasks.add_task(process_and_store_pdf, doc_id, str(file_path))

        # Return immediately with "processing" status
        return UploadResponse(
            status="processing",
            doc_id=doc_id,
            filename=file.filename,
            chunk_count=0,  # Will be available after background task completes
            metadata={"file_path": str(file_path)}
        )

    except Exception as e:
        # Handle file save errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )


@router.get("/documents/{doc_id}")
async def get_document(doc_id: str) -> Dict[str, any]:
    """Get document chunks from ChromaDB by doc_id.

    Retrieves all stored chunks for a document using metadata filtering.
    Returns chunk texts, metadata, and IDs for the document.

    Args:
        doc_id: Document ID (UUID) to retrieve

    Returns:
        JSON with:
            - doc_id: Document ID
            - chunks: List of chunk data with text, metadata, and id
            - count: Number of chunks retrieved

    Raises:
        HTTPException 404: If no chunks found for document
        HTTPException 500: If query fails
    """
    try:
        collection = get_documents_collection()
        results = query_by_document(collection, doc_id, n_results=100)

        if results["count"] == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document {doc_id} not found or still processing"
            )

        # Format chunks for response
        chunks = [
            {
                "id": results["ids"][i],
                "text": results["documents"][i],
                "metadata": results["metadatas"][i]
            }
            for i in range(results["count"])
        ]

        return {
            "doc_id": doc_id,
            "chunks": chunks,
            "count": results["count"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve document: {str(e)}"
        )


@router.delete("/documents/{doc_id}")
async def delete_document_endpoint(doc_id: str) -> Dict[str, any]:
    """Delete document chunks from ChromaDB by doc_id.

    Removes all chunks associated with a document from the vector store.
    This is a simple delete without archival.

    Args:
        doc_id: Document ID (UUID) to delete

    Returns:
        JSON with:
            - success: True if deletion succeeded
            - doc_id: Deleted document ID
            - count: -1 (ChromaDB doesn't return delete count)

    Note:
        Archival to separate collection not implemented.
        Chunks are permanently deleted. Will be enhanced in future phase.

    Raises:
        HTTPException 500: If deletion fails
    """
    try:
        collection = get_documents_collection()
        result = delete_document(collection, doc_id)

        return {
            "success": result["success"],
            "doc_id": result["doc_id"],
            "count": result["count"],
            "message": f"Document {doc_id} deleted from vector store"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
