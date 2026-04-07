"""HTTP client for local model service."""
import os
from typing import Dict

import requests


MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://127.0.0.1:8001")


def summarize_via_model_service(text: str, num_sentences: int) -> Dict:
    """Call model service /summarize endpoint."""
    payload = {"text": text, "num_sentences": num_sentences}
    response = requests.post(
        f"{MODEL_SERVICE_URL}/summarize",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
