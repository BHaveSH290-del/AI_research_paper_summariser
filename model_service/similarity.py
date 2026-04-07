"""Sentence similarity matrix computation."""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity_matrix(tfidf_matrix):
    """Compute pairwise cosine similarity matrix."""
    if tfidf_matrix is None:
        return np.array([[]])
    sim = cosine_similarity(tfidf_matrix)
    # Remove self-loops bias in ranking.
    np.fill_diagonal(sim, 0.0)
    return sim
