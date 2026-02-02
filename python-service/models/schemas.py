"""Pydantic schemas for API request/response validation.

These models define the structure of API requests and responses for the
Document Research ML Service.
"""

from pydantic import BaseModel
from typing import Dict


class UploadResponse(BaseModel):
    """Response model for PDF upload endpoint.

    Attributes:
        status: Processing status (e.g., "processed")
        doc_id: Unique identifier for the uploaded document
        filename: Original filename from upload
        chunk_count: Number of chunks extracted from the PDF
        metadata: PDF metadata (title, author, creationDate)
    """
    status: str
    doc_id: str
    filename: str
    chunk_count: int
    metadata: Dict[str, str]


class Chunk(BaseModel):
    """Model representing a text chunk with metadata.

    Attributes:
        text: The chunked text content
        chunk_index: Sequential index of this chunk
        token_count: Number of tokens in this chunk
        page_num: PDF page number where chunk starts
        char_offset: Character offset within the page
        doc_id: Document identifier (added by API endpoint)
    """
    text: str
    chunk_index: int
    token_count: int
    page_num: int
    char_offset: int
    doc_id: str
