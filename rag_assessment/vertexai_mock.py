"""Mocks for the Vertex AI SDK classes named in the assessment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .embedding import EmbeddingModel, HashingEmbeddingModel


@dataclass(frozen=True)
class MockEmbedding:
    values: list[float]


class MockTextEmbeddingModel:
    """Drop-in style mock for vertexai.language_models.TextEmbeddingModel."""

    def __init__(self, embedder: EmbeddingModel | None = None) -> None:
        self._embedder = embedder or HashingEmbeddingModel()

    @classmethod
    def from_pretrained(cls, _: str) -> "MockTextEmbeddingModel":
        return cls()

    def get_embeddings(self, texts: Iterable[str]) -> list[MockEmbedding]:
        vectors = self._embedder.embed(texts)
        return [MockEmbedding(vector.tolist()) for vector in vectors]


@dataclass(frozen=True)
class MockGenerationResponse:
    text: str


class MockGenerativeModel:
    """Rule-based query expander with the same shape as a Vertex generative model."""

    EXPANSIONS = {
        "peak load": (
            "peak traffic spike autoscaling horizontal scaling queue depth "
            "backpressure request shedding cached responses capacity"
        ),
        "handle load": (
            "peak traffic spike autoscaling horizontal scaling queue depth "
            "backpressure request shedding capacity"
        ),
        "search quality": (
            "retrieval quality evaluation recall at k mean reciprocal rank "
            "relevance labels benchmark queries"
        ),
        "measure": (
            "retrieval quality evaluation recall at k mean reciprocal rank "
            "manual relevance labels benchmark queries"
        ),
        "results are good": (
            "retrieval quality evaluation recall at k mean reciprocal rank "
            "manual relevance labels benchmark queries"
        ),
        "secure": (
            "security access control authorization tenant scope policy labels "
            "unauthorized passages"
        ),
        "private tenant": (
            "security access control authorization tenant scope policy labels "
            "metadata filters unauthorized passages"
        ),
        "latency": (
            "p95 latency distributed traces percentile dashboards error budget "
            "burn rate alerts"
        ),
    }

    def __init__(self, _: str = "gemini-mock") -> None:
        pass

    def generate_content(self, prompt: str) -> MockGenerationResponse:
        lowered = prompt.lower()
        additions = [
            expansion
            for key, expansion in self.EXPANSIONS.items()
            if key in lowered
        ]
        expanded = prompt if not additions else f"{prompt} {' '.join(additions)}"
        return MockGenerationResponse(expanded)
