"""Text cleaning and token estimation."""
import re


def clean_text(text: str) -> str:
    """
    Clean text for summarization:
    - Remove citations [1], (Smith, 2020)
    - Remove references section
    - Remove figure/table captions
    - Normalize spacing
    - Remove special characters (excessive)
    """
    if not text:
        return ""

    # Remove inline citations like [1], [2,3], [Smith et al., 2020]
    text = re.sub(r"\[\s*\d+(?:\s*,\s*\d+)*\s*\]", "", text)
    text = re.sub(r"\(\s*[A-Z][a-z]+(?:\s+et\s+al\.?)?\s*,\s*\d{4}\s*\)", "", text)
    text = re.sub(r"\([A-Z][a-z]+\s+&\s+[A-Z][a-z]+,\s*\d{4}\)", "", text)

    # Remove references section (starts with References, Bibliography, etc.)
    ref_pattern = r"(?i)\n\s*(?:references?|bibliography|works?\s*cited)\s*\n.*"
    text = re.sub(ref_pattern, "", text, flags=re.DOTALL)

    # Remove figure/table captions: Figure 1: ..., Table 2: ...
    text = re.sub(r"(?i)(?:figure|fig\.?|table|tab\.?)\s*\d+\s*[:\-]\s*[^\n]+", "", text)

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()

    # Remove excessive special chars (keep basic punctuation)
    text = re.sub(r"[^\w\s.,;:!?\-'\"()]", " ", text)
    text = re.sub(r" +", " ", text)

    return text.strip()


def estimate_tokens(text: str) -> int:
    """
    Rough token count: ~4 chars per token for English.
    Used to decide chunking.
    """
    return len(text) // 4
