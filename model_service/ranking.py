"""Graph construction and PageRank ranking."""
from typing import Dict

import networkx as nx
import numpy as np


def rank_sentences(similarity_matrix: np.ndarray) -> Dict[int, float]:
    """Build sentence graph and compute PageRank scores."""
    if similarity_matrix.size == 0:
        return {}

    graph = nx.from_numpy_array(similarity_matrix)
    if graph.number_of_nodes() == 0:
        return {}

    # PageRank for weighted graph.
    return nx.pagerank(graph, weight="weight")
