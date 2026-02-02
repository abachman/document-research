"""Token-aware text chunking service using tiktoken.

This module provides text chunking functionality that respects token boundaries
using OpenAI's tiktoken encoder. Chunking by tokens (rather than characters or
sentences) ensures better results for ML models and vector embeddings.

The chunking uses a sliding window approach with overlap to preserve context
between chunks.
"""

import tiktoken
from typing import List, Dict

# Default chunking parameters
MAX_TOKENS = 500
OVERLAP = 50


def chunk_text_by_tokens(
    pages: List[Dict],
    max_tokens: int = 500,
    overlap: int = 50
) -> List[Dict]:
    """Chunk text from pages into token-aware chunks with overlap.

    This function flattens page text into a continuous stream, then chunks it
    by token count using tiktoken's cl100k_base encoding (GPT-4 tokenizer).

    Each chunk includes metadata for tracking:
    - chunk_index: Sequential index of the chunk
    - token_count: Number of tokens in the chunk
    - page_num: Which page the chunk starts on
    - char_offset: Character offset where the chunk starts

    Args:
        pages: List of page dicts with 'text', 'page_num', 'offset' keys
        max_tokens: Maximum tokens per chunk (default: 500)
        overlap: Token overlap between adjacent chunks (default: 50)

    Returns:
        List of chunk dicts containing text, chunk_index, token_count,
        page_num, char_offset. Note: doc_id is added by the caller.

    Example:
        >>> pages = [
        ...     {'page_num': 1, 'text': 'First page text', 'offset': 0},
        ...     {'page_num': 2, 'text': 'Second page text', 'offset': 15}
        ... ]
        >>> chunks = chunk_text_by_tokens(pages)
        >>> chunks[0]
        {'text': 'First page text...', 'chunk_index': 0, 'token_count': 45,
         'page_num': 1, 'char_offset': 0}
    """
    # Handle edge case: empty pages
    if not pages:
        return []

    # Flatten pages into continuous text with position tracking
    full_text_parts = []
    position_map = []  # Maps char_offset -> (page_num, page_offset)

    current_offset = 0
    for page in pages:
        text = page.get("text", "")
        if text:
            full_text_parts.append(text)
            position_map.append({
                "page_num": page["page_num"],
                "page_offset": page["offset"],
                "char_start": current_offset,
                "char_end": current_offset + len(text)
            })
            current_offset += len(text)

    # Handle edge case: no text extracted
    if not full_text_parts:
        return []

    # Concatenate all text
    full_text = "".join(full_text_parts)

    # Handle edge case: empty text
    if not full_text.strip():
        return []

    # Get tiktoken encoding (cl100k_base is GPT-4's tokenizer)
    encoding = tiktoken.get_encoding("cl100k_base")

    # Encode full text to tokens
    tokens = encoding.encode(full_text)

    # Handle edge case: text too short to tokenize
    if not tokens:
        return []

    # Chunk tokens with sliding window
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(tokens):
        # Get chunk tokens
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]

        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)

        # Find which page this chunk belongs to
        # Map token start position to character position
        # (Approximation: tokens are roughly 4 characters each)
        char_start_estimate = int(start * len(full_text) / len(tokens))

        # Find the page containing this character position
        page_num = 1
        char_offset = 0
        for pos in position_map:
            if pos["char_start"] <= char_start_estimate < pos["char_end"]:
                page_num = pos["page_num"]
                char_offset = pos["page_offset"] + (char_start_estimate - pos["char_start"])
                break
        else:
            # Fallback: use last page
            page_num = position_map[-1]["page_num"]
            char_offset = position_map[-1]["page_offset"]

        # Build chunk dict
        chunk = {
            "text": chunk_text,
            "chunk_index": chunk_index,
            "token_count": len(chunk_tokens),
            "page_num": page_num,
            "char_offset": char_offset,
            # Note: doc_id is added by the caller (API endpoint)
        }
        chunks.append(chunk)

        # Move start forward with overlap
        start += (max_tokens - overlap)
        chunk_index += 1

        # Break if we've covered all tokens
        if start >= len(tokens):
            break

    return chunks
