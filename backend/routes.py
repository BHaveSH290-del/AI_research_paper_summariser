"""API routes."""
import os
import time
import hashlib
import logging
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

from config.settings import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_CONTENT_TYPES
from services.pdf_processor import extract_text_from_pdf
from services.summarizer import summarize_text, get_model_loaded
from services.chunker import chunk_text, recursive_summarize
from utils.preprocessing import clean_text, estimate_tokens

logger = logging.getLogger(__name__)
router = APIRouter()

# Optional: in-memory cache for repeated uploads
_summary_cache: dict[str, dict] = {}


class SummaryResponse(BaseModel):
    summary_text: str
    original_word_count: int
    summary_word_count: int
    processing_time: float


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


def _get_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _validate_pdf(file: UploadFile, content: bytes) -> None:
    """Validate PDF file."""
    # Check magic bytes for PDF (%PDF)
    if not content.startswith(b"%PDF"):
        raise HTTPException(400, "Invalid file. File does not appear to be a valid PDF.")
    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(400, "Invalid file type. Only PDF is accepted.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB")
    if len(content) < 100:
        raise HTTPException(400, "File appears corrupted or empty.")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "hf_ready": get_model_loaded(),
    }


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_paper(file: UploadFile = File(...)):
    """Upload PDF, extract text, and generate summary."""
    start_time = time.perf_counter()

    # Read file content
    content = await file.read()
    _validate_pdf(file, content)

    if not get_model_loaded():
        raise HTTPException(
            503,
            "HUGGINGFACE_API_KEY or HF_TOKEN is required. Get a free key at huggingface.co/settings/tokens",
        )

    # Optional: check cache
    file_hash = _get_file_hash(content)
    if file_hash in _summary_cache:
        cached = _summary_cache[file_hash]
        return SummaryResponse(**cached)

    # Secure temporary storage
    safe_name = f"{file_hash[:16]}_{file.filename or 'document.pdf'}"
    upload_path = UPLOAD_DIR / safe_name

    try:
        upload_path.write_bytes(content)

        # Phase: PDF extraction
        t0 = time.perf_counter()
        raw_text = extract_text_from_pdf(str(upload_path))
        t_extract = time.perf_counter() - t0
        logger.info(f"Extraction time: {t_extract:.2f}s")

        if not raw_text or len(raw_text.strip()) < 50:
            raise HTTPException(400, "Could not extract readable text. PDF may be scanned or image-based.")

        # Phase: Preprocessing
        t1 = time.perf_counter()
        cleaned = clean_text(raw_text)
        t_clean = time.perf_counter() - t1
        logger.info(f"Cleaning time: {t_clean:.2f}s")

        original_word_count = len(cleaned.split())

        # Phase: Chunking and summarization
        t2 = time.perf_counter()
        if estimate_tokens(cleaned) <= 1024:
            summary = summarize_text(cleaned)
        else:
            chunks = chunk_text(cleaned)
            summary = recursive_summarize(chunks)
        t_inference = time.perf_counter() - t2
        logger.info(f"Inference time: {t_inference:.2f}s")

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Summarization failed")
        raise HTTPException(500, f"Processing failed: {str(e)}")
    finally:
        if upload_path.exists():
            upload_path.unlink(missing_ok=True)

    processing_time = time.perf_counter() - start_time
    summary_word_count = len(summary.split())

    result = SummaryResponse(
        summary_text=summary,
        original_word_count=original_word_count,
        summary_word_count=summary_word_count,
        processing_time=round(processing_time, 2),
    )

    # Optional: cache result
    _summary_cache[file_hash] = result.model_dump()

    return result
