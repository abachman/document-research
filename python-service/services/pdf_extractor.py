"""PDF text extraction service using PyMuPDF (fitz).

This module provides PDF text extraction with position tracking for PDF navigation.
The position tracking enables mapping extracted text back to specific pages and
character offsets for features like PDF viewer integration.
"""

import fitz
from typing import List, Dict, Any


def extract_pdf_pages(pdf_path: str) -> Dict[str, Any]:
    """Extract text from PDF pages with position tracking.

    This function opens a PDF file and extracts text from each page while tracking:
    - Page number (1-based)
    - Character offset (global position in the document)
    - Text length (for offset calculations)
    - PDF metadata (title, author, creation date)

    Args:
        pdf_path: Path to the PDF file to process

    Returns:
        Dictionary containing:
            - pages: List of dicts with page_num, text, offset, length
            - metadata: Dict with title, author, creationDate

    Raises:
        ValueError: If the PDF file cannot be opened or processed
        FileNotFoundError: If the PDF file does not exist

    Example:
        >>> result = extract_pdf_pages("document.pdf")
        >>> result["pages"][0]
        {'page_num': 1, 'text': 'Sample text...', 'offset': 0, 'length': 100}
        >>> result["metadata"]
        {'title': 'Document Title', 'author': 'Author Name', 'creationDate': 'D:20240101'}
    """
    doc = None
    try:
        # Open PDF document
        doc = fitz.open(pdf_path)

        if doc.page_count == 0:
            raise ValueError(f"PDF file has no pages: {pdf_path}")

        pages_data = []
        global_offset = 0

        # Iterate through pages with 1-based page numbers
        for page_num, page in enumerate(doc, start=1):
            # Extract text from page
            text = page.get_text("text")

            # Build page data dict with position tracking
            page_info = {
                "page_num": page_num,
                "text": text,
                "offset": global_offset,
                "length": len(text)
            }
            pages_data.append(page_info)

            # Update global offset for next page
            global_offset += len(text)

        # Extract metadata from PDF
        metadata = doc.metadata
        metadata_dict = {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "creationDate": metadata.get("creationDate", "")
        }

        return {
            "pages": pages_data,
            "metadata": metadata_dict
        }

    except FileNotFoundError as e:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}") from e
    except fitz.FileDataError as e:
        raise ValueError(f"Cannot open PDF file (may be corrupted): {pdf_path}") from e
    except Exception as e:
        raise ValueError(f"Error processing PDF file {pdf_path}: {str(e)}") from e
    finally:
        # Always close the document to prevent memory leaks
        if doc is not None:
            doc.close()
