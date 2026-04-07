"""Local PDF text extraction for Flask app (text-based PDFs only)."""
from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extract text page-by-page from uploaded PDF bytes using pypdf only.

    This assumes the PDF has a normal text layer (not scanned-only).
    """
    if not file_bytes:
        return ""

    reader = PdfReader(BytesIO(file_bytes))
    parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text.strip())
    return "\n\n".join(parts).strip()
