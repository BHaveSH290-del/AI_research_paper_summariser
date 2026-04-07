"""Application configuration."""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# File upload limits (bytes) — ~25MB for safety with 40-page PDFs
MAX_FILE_SIZE = 25 * 1024 * 1024

# Allowed MIME types
ALLOWED_CONTENT_TYPES = {"application/pdf"}

# Hugging Face BART has ~1024 token input limit
MAX_INPUT_TOKENS = 1024
CHUNK_WORDS = 700
CHUNK_OVERLAP_WORDS = 100

# Summarization parameters
MAX_SUMMARY_LENGTH = 200
