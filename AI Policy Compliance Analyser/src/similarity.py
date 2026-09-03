"""Semantic + lexical retrieval helpers.

No policy corpus or control corpus is bundled with the public project.
"""
from __future__ import annotations

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_COSINE_WEIGHT = 0.6
DEFAULT_TOP_K = 3
DEFAULT_COMPLIANT_THRESHOLD = 0.60
DEFAULT_PARTIAL_THRESHOLD = 0.55


def build_bm25_index(chunks: list[dict]) -> BM25Okapi:
    """Build a reusable BM25 index from chunk text."""
    return BM25Okapi([chunk["text"].lower().split() for chunk in chunks])


def normalised_bm25_scores(index: BM25Okapi, query: str) -> np.ndarray:
    """Return BM25 scores normalised to 0..1."""
    scores = np.asarray(index.get_scores(query.lower().split()), dtype=float)
    maximum = scores.max(initial=0.0)
    return scores / maximum if maximum > 0 else scores


def rank_chunks(
    chunks: list[dict],
    chunk_vectors: np.ndarray,
    control_vector: np.ndarray,
    query: str,
    cosine_weight: float = DEFAULT_COSINE_WEIGHT,
    top_k: int = DEFAULT_TOP_K,
) -> list[dict]:
    """Rank policy chunks using cosine similarity blended with BM25."""
    if not chunks:
        return []
    if len(chunks) != len(chunk_vectors):
        raise ValueError("chunks and chunk_vectors must have the same length")

    index = build_bm25_index(chunks)
    cosine_scores = cosine_similarity(chunk_vectors, control_vector.reshape(1, -1)).ravel()
    lexical_scores = normalised_bm25_scores(index, query)
    combined = cosine_weight * cosine_scores + (1 - cosine_weight) * lexical_scores

    indices = np.argsort(combined)[-top_k:][::-1]
    return [
        {
            **chunks[i],
            "cosine_score": float(cosine_scores[i]),
            "bm25_score": float(lexical_scores[i]),
            "combined_score": float(combined[i]),
        }
        for i in indices
    ]


def classify_score(
    score: float,
    compliant_threshold: float = DEFAULT_COMPLIANT_THRESHOLD,
    partial_threshold: float = DEFAULT_PARTIAL_THRESHOLD,
) -> str:
    """Map a score to a three-level coverage label."""
    if score >= compliant_threshold:
        return "Compliant"
    if score >= partial_threshold:
        return "Partially Compliant"
    return "Non-Compliant"


def top_k_mean(ranked_chunks: list[dict]) -> float:
    """Calculate the mean combined score of retrieved chunks."""
    if not ranked_chunks:
        return 0.0
    return float(np.mean([item["combined_score"] for item in ranked_chunks]))
