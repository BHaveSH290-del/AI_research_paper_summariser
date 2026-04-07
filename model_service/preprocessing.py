"""Sentence preprocessing for TextRank."""
import re
from typing import List, Tuple


STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "while", "is", "are", "was",
    "were", "be", "been", "being", "to", "of", "in", "on", "for", "with", "as",
    "by", "at", "from", "that", "this", "it", "its", "into", "than", "then",
}


def split_sentences(text: str) -> List[str]:
    """Split text into candidate sentences."""
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return []
    # Basic sentence boundary splitting.
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [p.strip() for p in parts if p and p.strip()]


def normalize_sentence(sentence: str, remove_stopwords: bool = True) -> str:
    """Lowercase and optionally remove punctuation/stopwords."""
    sent = sentence.lower()
    sent = re.sub(r"[^a-z0-9\s]", " ", sent)
    tokens = [tok for tok in sent.split() if tok]
    if remove_stopwords:
        tokens = [tok for tok in tokens if tok not in STOPWORDS]
    return " ".join(tokens)


def preprocess_sentences(sentences: List[str]) -> Tuple[List[str], List[str]]:
    """Return (original_sentences, normalized_sentences)."""
    normalized = [normalize_sentence(s) for s in sentences]
    return sentences, normalized
