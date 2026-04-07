"""PDF text extraction and structural detection."""
import re
import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text page by page. Ignores images.
    Handles non-text PDFs by returning empty string.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        reader = PdfReader(str(path))
        text_parts = []

        for page in reader.pages:
            try:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            except Exception as e:
                logger.warning(f"Could not extract page: {e}")
                continue

        full_text = "\n\n".join(text_parts)
        full_text = clean_extraction_artifacts(full_text)

        # Basic heuristic: if we got very little text, it may be scanned/image PDF
        if len(full_text.strip()) < 100 and len(reader.pages) > 1:
            logger.warning("Very little text extracted. PDF may be scanned/image-based.")

        return full_text

    except Exception as e:
        logger.exception(f"PDF extraction failed: {e}")
        raise ValueError(f"Failed to read PDF: {e}") from e


def detect_structure(text: str) -> dict[str, str | None]:
    """
    Detect common research paper sections.
    Returns dict with keys: abstract, introduction, method, conclusion.
    """
    sections = {
        "abstract": None,
        "introduction": None,
        "method": None,
        "conclusion": None,
    }

    # Case-insensitive section headers (common patterns)
    patterns = {
        "abstract": r"(?i)(?:^|\n)\s*(?:abstract|summary)\s*\n+(.+?)(?=\n\s*(?:introduction|1\.|keywords|index terms)|$)",
        "introduction": r"(?i)(?:^|\n)\s*(?:introduction|1\.\s*introduction)\s*\n+(.+?)(?=\n\s*(?:2\.|method|related work|background)|$)",
        "method": r"(?i)(?:^|\n)\s*(?:method|methodology|approach|2\.)\s*\n+(.+?)(?=\n\s*(?:3\.|experiments|results|evaluation)|$)",
        "conclusion": r"(?i)(?:^|\n)\s*(?:conclusion|conclusions|summary|discussion)\s*\n+(.+?)(?=\n\s*(?:references|acknowledg|appendix)|$)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if len(content) > 50:  # Filter trivial matches
                sections[key] = content[:2000]  # Limit length

    return sections


def clean_extraction_artifacts(text: str) -> str:
    """Remove common PDF extraction artifacts."""
    if not text:
        return ""

    # Hyphenation at line breaks (e.g., "con-\ntinuation")
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Multiple spaces
    text = re.sub(r" +", " ", text)

    # Preserve section breaks: multiple newlines -> double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
