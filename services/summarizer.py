"""Summarization using Hugging Face Inference API (primary)."""
import logging
import os

from config.settings import MAX_SUMMARY_LENGTH, MAX_INPUT_TOKENS

logger = logging.getLogger(__name__)

# HF BART models have ~1024 token input limit
_CHARS_PER_TOKEN = 4


def get_model_loaded() -> bool:
    """Ready when HF token is set."""
    return bool(os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN"))


# --- SUMY EXTRACTIVE SUMMARIZATION (commented out) ---
# def _summarize_extractive(text: str, target_sentences: int = 12) -> str:
#     ... (see git history if needed)


def _summarize_huggingface(text: str, max_length: int) -> str:
    """Summarize using Hugging Face Inference API."""
    from huggingface_hub import InferenceClient

    token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
    client = InferenceClient(token=token)

    # HF BART has ~1024 token limit; truncate to be safe
    max_chars = min(MAX_INPUT_TOKENS * _CHARS_PER_TOKEN, 4096)
    if len(text) > max_chars:
        text = text[:max_chars] + "..."

    model = os.getenv("HF_SUMMARY_MODEL", "facebook/bart-large-cnn")

    result = client.summarization(
        text,
        model=model,
        clean_up_tokenization_spaces=True,
    )

    # Handle different response formats (summary_text, generated_text, or list)
    if hasattr(result, "summary_text"):
        summary = result.summary_text
    elif hasattr(result, "generated_text"):
        summary = result.generated_text
    elif isinstance(result, list) and result:
        summary = result[0].get("summary_text", result[0].get("generated_text", ""))
    elif isinstance(result, dict):
        summary = result.get("summary_text", result.get("generated_text", ""))
    else:
        summary = str(result) if result else ""
    return (summary or "").strip()


def summarize_text(
    text: str,
    max_length: int = MAX_SUMMARY_LENGTH,
    min_length: int = 30,
) -> str:
    """
    Summarize using Hugging Face Inference API.
    HUGGINGFACE_API_KEY or HF_TOKEN is required.
    """
    if not get_model_loaded():
        raise RuntimeError(
            "HUGGINGFACE_API_KEY or HF_TOKEN is required. "
            "Get a free key at https://huggingface.co/settings/tokens"
        )

    return _summarize_huggingface(text, max_length)
