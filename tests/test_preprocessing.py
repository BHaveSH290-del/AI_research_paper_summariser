"""Tests for text preprocessing."""
import pytest
from utils.preprocessing import clean_text, estimate_tokens


def test_clean_text_removes_citations():
    text = "According to Smith et al. [1] and (Jones, 2020), the results show."
    cleaned = clean_text(text)
    assert "[1]" not in cleaned
    assert "(Jones, 2020)" not in cleaned


def test_clean_text_normalizes_whitespace():
    text = "Too   many    spaces   here"
    cleaned = clean_text(text)
    assert "  " not in cleaned


def test_estimate_tokens():
    text = "This is a test sentence with ten words in it now."
    # ~10 words * ~5 chars = 50 chars -> ~12 tokens
    tokens = estimate_tokens(text)
    assert 5 <= tokens <= 20
