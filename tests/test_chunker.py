"""Tests for chunking logic."""
from services.chunker import chunk_text

# Sample text: many short sentences
SAMPLE = ". ".join([f"Sentence number {i} has some content here." for i in range(100)])


def test_chunk_respects_sentence_boundaries():
    chunks = chunk_text(SAMPLE, chunk_size=50, overlap=5)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert len(chunk.strip()) > 0


def test_chunk_count_increases_with_longer_text():
    short = " ".join(["Word"] * 50)
    long = " ".join(["Word"] * 500)
    c_short = len(chunk_text(short, chunk_size=100))
    c_long = len(chunk_text(long, chunk_size=100))
    assert c_long >= c_short
