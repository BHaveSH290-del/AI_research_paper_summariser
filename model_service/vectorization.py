"""TF-IDF sentence vectorization."""
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_matrix(normalized_sentences: List[str]):
    """Vectorize sentences with TF-IDF."""
    if not normalized_sentences:
        return None
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(normalized_sentences)
