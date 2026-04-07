"""Pipeline controller for TextRank summarization."""
import time
from typing import Dict, List

from model_service.preprocessing import preprocess_sentences, split_sentences
from model_service.ranking import rank_sentences
from model_service.similarity import compute_similarity_matrix
from model_service.vectorization import build_tfidf_matrix


def _remove_redundancy(sentences: List[str]) -> List[str]:
    """Basic dedup filter preserving order."""
    seen = set()
    result: List[str] = []
    for sent in sentences:
        key = " ".join(sent.lower().split())
        if key in seen:
            continue
        seen.add(key)
        result.append(sent)
    return result


def summarize_text_textrank(text: str, num_sentences: int = 5) -> Dict:
    """Run full TextRank pipeline and return summary payload."""
    start = time.perf_counter()

    if not text or not text.strip():
        return {
            "summary": "",
            "selected_sentences": [],
            "processing_time": 0.0,
        }

    sentences = split_sentences(text)
    if len(sentences) <= 2:
        # Very short input; return as-is.
        summary = " ".join(sentences)
        return {
            "summary": summary,
            "selected_sentences": sentences,
            "processing_time": round(time.perf_counter() - start, 4),
        }

    original_sentences, normalized_sentences = preprocess_sentences(sentences)
    tfidf_matrix = build_tfidf_matrix(normalized_sentences)
    sim_matrix = compute_similarity_matrix(tfidf_matrix)
    scores = rank_sentences(sim_matrix)

    if not scores:
        selected = original_sentences[: max(1, min(num_sentences, len(original_sentences)))]
    else:
        n = max(1, min(num_sentences, len(original_sentences)))
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        top_indices = sorted(idx for idx, _ in ranked)  # preserve original order
        selected = [original_sentences[idx] for idx in top_indices]

    selected = _remove_redundancy(selected)
    summary = " ".join(selected)

    return {
        "summary": summary,
        "selected_sentences": selected,
        "processing_time": round(time.perf_counter() - start, 4),
    }
