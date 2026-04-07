"""Smart chunking and recursive summarization."""
import re

from config.settings import CHUNK_WORDS, CHUNK_OVERLAP_WORDS
from services.summarizer import summarize_text
from utils.preprocessing import estimate_tokens


def chunk_text(text: str, chunk_size: int = CHUNK_WORDS, overlap: int = CHUNK_OVERLAP_WORDS) -> list[str]:
    """
    Split text into chunks at sentence boundaries.
    Avoid breaking sentences. Maintain coherence.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks: list[str] = []
    current: list[str] = []
    current_words = 0

    for sent in sentences:
        sent_words = len(sent.split())
        if current_words + sent_words > chunk_size and current:
            chunk_text_str = " ".join(current)
            chunks.append(chunk_text_str)

            # Overlap: keep last few sentences for context
            overlap_words = 0
            overlap_sents: list[str] = []
            for s in reversed(current):
                w = len(s.split())
                if overlap_words + w <= overlap:
                    overlap_sents.insert(0, s)
                    overlap_words += w
                else:
                    break
            current = overlap_sents
            current_words = overlap_words

        current.append(sent)
        current_words += sent_words

    if current:
        chunks.append(" ".join(current))

    return chunks


def recursive_summarize(chunks: list[str]) -> str:
    """
    1. Summarize each chunk
    2. Combine summaries
    3. If combined still too long, summarize again
    4. Return final coherent summary
    """
    if not chunks:
        return ""

    summaries = [summarize_text(c) for c in chunks]
    combined = " ".join(summaries)

    # If combined summary exceeds model limit, summarize again
    while estimate_tokens(combined) > 900 and len(summaries) > 1:
        # Re-chunk combined summary and summarize
        mid = len(summaries) // 2
        left = " ".join(summaries[:mid])
        right = " ".join(summaries[mid:])
        summaries = [summarize_text(left), summarize_text(right)]
        combined = " ".join(summaries)

    if estimate_tokens(combined) > 900:
        return summarize_text(combined)

    return summarize_text(combined)
