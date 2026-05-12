"""Local embedding models used by the retrieval pipeline."""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Protocol

import numpy as np


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


class EmbeddingModel(Protocol):
    """Small interface compatible with local and Vertex-like embedders."""

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        """Return one vector per text."""


@dataclass
class HashingEmbeddingModel:
    """Deterministic local embedding model.

    It is intentionally transparent for assessment purposes: tokens are hashed
    into a fixed-dimensional vector and weighted with sublinear term frequency.
    The output is L2-normalized so cosine similarity can be computed by dot
    product in the vector store.
    """

    dimensions: int = 384

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        vectors = [self._embed_one(text) for text in texts]
        return np.vstack(vectors).astype(np.float32)

    def _embed_one(self, text: str) -> np.ndarray:
        tokens = TOKEN_RE.findall(text.lower())
        counts = Counter(tokens)
        vector = np.zeros(self.dimensions, dtype=np.float32)

        for token, count in counts.items():
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign * (1.0 + math.log(count))

        norm = np.linalg.norm(vector)
        if norm:
            vector /= norm
        return vector


class SentenceTransformerEmbeddingModel:
    """Optional wrapper around sentence-transformers when a local model exists."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        return self._model.encode(
            list(texts),
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype(np.float32)
