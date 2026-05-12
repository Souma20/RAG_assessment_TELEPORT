"""RAG retrieval orchestration."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .embedding import EmbeddingModel, HashingEmbeddingModel
from .vector_store import NumpyVectorStore, SearchResult
from .vertexai_mock import MockGenerativeModel


class ContextAwareRetrievalEngine:
    """Manages ingestion and raw/enhanced semantic retrieval."""

    def __init__(
        self,
        embedder: EmbeddingModel | None = None,
        vector_store: NumpyVectorStore | None = None,
        query_expander: MockGenerativeModel | None = None,
    ) -> None:
        self.embedder = embedder or HashingEmbeddingModel()
        self.vector_store = vector_store or NumpyVectorStore()
        self.query_expander = query_expander or MockGenerativeModel()

    def ingest(self, documents: list[dict[str, Any]]) -> None:
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadata = [{"title": doc["title"]} for doc in documents]
        vectors = self.embedder.embed(texts)
        self.vector_store.add(ids, texts, vectors, metadata)

    def search_raw(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_vector = self.embedder.embed([query])[0]
        return self.vector_store.search(query_vector, top_k=top_k)

    def expand_query(self, query: str) -> str:
        return self.query_expander.generate_content(query).text

    def search_enhanced(self, query: str, top_k: int = 3) -> tuple[str, list[SearchResult]]:
        expanded_query = self.expand_query(query)
        query_vector = self.embedder.embed([expanded_query])[0]
        return expanded_query, self.vector_store.search(query_vector, top_k=top_k)

    def compare(self, queries: list[str], top_k: int = 3) -> list[dict[str, Any]]:
        comparison = []
        for query in queries:
            expanded_query, enhanced = self.search_enhanced(query, top_k=top_k)
            comparison.append(
                {
                    "query": query,
                    "expanded_query": expanded_query,
                    "strategy_a_raw": [asdict(result) for result in self.search_raw(query, top_k)],
                    "strategy_b_enhanced": [asdict(result) for result in enhanced],
                }
            )
        return comparison
