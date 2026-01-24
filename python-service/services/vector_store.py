"""ChromaDB vector storage service for document chunks.

This module provides a persistent vector database using ChromaDB to store
and query document chunks extracted from PDFs. Chunks are stored with metadata
for retrieval and future semantic search.

Storage is persistent across service restarts using chromadb.PersistentClient.
"""

import chromadb
from typing import List, Dict, Optional, Any
from pathlib import Path

from config import CHROMA_DIR


# Module-level cache for ChromaDB client (lazy initialization)
_chroma_client: Optional[chromadb.PersistentClient] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create the ChromaDB persistent client.

    The client is cached at module level for reuse across calls.
    Uses PersistentClient to ensure data survives service restarts.

    Returns:
        ChromaDB PersistentClient instance with data stored in CHROMA_DIR.

    Raises:
        IOError: If CHROMA_DIR cannot be created or accessed.
    """
    global _chroma_client

    if _chroma_client is None:
        # Ensure ChromaDB directory exists
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        # Create persistent client (data survives restarts)
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    return _chroma_client


def get_documents_collection() -> chromadb.Collection:
    """Get or create the documents collection for storing PDF chunks.

    Uses a single collection named 'documents' for all chunks.
    Chunks are filtered by doc_id in metadata when querying.

    Collection configuration:
        - Name: 'documents'
        - Distance metric: cosine similarity (hnsw:space)

    Returns:
        ChromaDB Collection instance for document chunks.

    Note:
        Embeddings are not set here - they will be added in Phase 4
        when implementing semantic search with Qwen embeddings.
    """
    client = get_chroma_client()

    # Get or create collection with cosine similarity
    collection = client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}  # Cosine similarity for embeddings
    )

    return collection


def add_document_chunks(
    collection: chromadb.Collection,
    doc_id: str,
    chunks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Add document chunks to the vector store.

    Extracts text, IDs, and metadata from chunks and adds them to ChromaDB.
    Each chunk is stored with doc_id, chunk_index, page_num, and char_offset.

    Args:
        collection: ChromaDB collection instance.
        doc_id: Unique document identifier (UUID).
        chunks: List of chunk dictionaries with keys:
            - text: str - The chunk text content
            - chunk_index: int - Sequential index of the chunk
            - page_num: int - PDF page number (1-based)
            - char_offset: int - Character offset in the page

    Returns:
        Dict with success status and count of chunks added.

    Note:
        Embeddings parameter is omitted - ChromaDB will use default embeddings
        until Phase 4 when custom Qwen embeddings are integrated.
    """
    if not chunks:
        return {"success": True, "count": 0}

    # Extract arrays for ChromaDB
    documents = [c["text"] for c in chunks]
    ids = [f"{doc_id}_chunk_{c['chunk_index']}" for c in chunks]
    metadatas = [{
        "doc_id": doc_id,
        "chunk_index": c["chunk_index"],
        "page_num": c.get("page_num", 0),
        "char_offset": c.get("char_offset", 0)
    } for c in chunks]

    # Add to collection
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    return {
        "success": True,
        "count": len(chunks),
        "doc_id": doc_id
    }


def query_by_document(
    collection: chromadb.Collection,
    doc_id: str,
    n_results: int = 10
) -> Dict[str, Any]:
    """Query chunks for a specific document by doc_id.

    Retrieves all chunks for a document using metadata filtering.
    Uses empty query text for metadata-only retrieval (no semantic search).

    Args:
        collection: ChromaDB collection instance.
        doc_id: Document ID to query.
        n_results: Maximum number of results to return (default: 10).

    Returns:
        Dict with:
            - documents: List of chunk texts
            - metadatas: List of metadata dicts
            - ids: List of chunk IDs
            - count: Number of chunks returned

    Note:
        This is metadata-only retrieval. Semantic search with embeddings
        will be added in Phase 4.
    """
    # Query by doc_id filter (empty query text for metadata-only retrieval)
    results = collection.query(
        query_texts=[""],  # Empty for metadata-only retrieval
        n_results=n_results,
        where={"doc_id": doc_id}
    )

    # Handle empty results gracefully
    if not results or not results["ids"][0]:
        return {
            "documents": [],
            "metadatas": [],
            "ids": [],
            "count": 0
        }

    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
        "ids": results["ids"][0],
        "count": len(results["ids"][0])
    }


def delete_document(
    collection: chromadb.Collection,
    doc_id: str
) -> Dict[str, Any]:
    """Delete all chunks for a document from the vector store.

    Removes chunks matching the doc_id from the collection.
    This is a simple delete - archival to a separate collection
    is deferred to a future phase.

    Args:
        collection: ChromaDB collection instance.
        doc_id: Document ID to delete.

    Returns:
        Dict with success status. Note: ChromaDB doesn't return
        delete count, so count is set to -1 (unknown).

    Note:
        Archival to separate collection not implemented - chunks are
        permanently deleted. This will be enhanced in a future phase.
    """
    collection.delete(where={"doc_id": doc_id})

    return {
        "success": True,
        "count": -1,  # ChromaDB doesn't return delete count
        "doc_id": doc_id
    }
