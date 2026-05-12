"""In-memory vector storage and cosine search."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SearchResult:
    """One retrieval result."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


class NumpyVectorStore:
    """Small vector database backed by normalized NumPy arrays."""

    def __init__(self) -> None:
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._metadata: list[dict[str, Any]] = []
        self._vectors: np.ndarray | None = None

    def add(
        self,
        ids: list[str],
        texts: list[str],
        vectors: np.ndarray,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        if len(ids) != len(texts) or len(ids) != len(vectors):
            raise ValueError("ids, texts, and vectors must have the same length")

        metas = metadata or [{} for _ in ids]
        normalized = self._normalize(vectors)

        self._ids.extend(ids)
        self._texts.extend(texts)
        self._metadata.extend(metas)
        self._vectors = (
            normalized
            if self._vectors is None
            else np.vstack([self._vectors, normalized])
        )

    def search(self, query_vector: np.ndarray, top_k: int = 3) -> list[SearchResult]:
        if self._vectors is None or not self._ids:
            raise ValueError("vector store is empty")
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        query = self._normalize(query_vector.reshape(1, -1))[0]
        scores = self._vectors @ query
        order = np.argsort(scores)[::-1][:top_k]

        return [
            SearchResult(
                id=self._ids[index],
                score=float(scores[index]),
                text=self._texts[index],
                metadata=self._metadata[index],
            )
            for index in order
        ]

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        vectors = np.asarray(vectors, dtype=np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)
