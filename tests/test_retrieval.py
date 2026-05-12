import numpy as np

from rag_assessment.data import TECHNICAL_PARAGRAPHS
from rag_assessment.embedding import HashingEmbeddingModel
from rag_assessment.retrieval import ContextAwareRetrievalEngine
from rag_assessment.vertexai_mock import MockTextEmbeddingModel


def test_ingest_and_raw_search_returns_ranked_results():
    engine = ContextAwareRetrievalEngine()
    engine.ingest(TECHNICAL_PARAGRAPHS)

    results = engine.search_raw("peak traffic autoscaling queue depth", top_k=3)

    assert len(results) == 3
    assert results[0].id == "capacity_peak_load"
    assert results[0].score >= results[1].score


def test_enhanced_search_expands_operational_query():
    engine = ContextAwareRetrievalEngine()
    engine.ingest(TECHNICAL_PARAGRAPHS)

    expanded_query, results = engine.search_enhanced(
        "How does the system handle peak load?",
        top_k=3,
    )

    assert "autoscaling" in expanded_query
    assert results[0].id == "capacity_peak_load"


def test_mock_text_embedding_model_matches_vertex_shape():
    model = MockTextEmbeddingModel(HashingEmbeddingModel(dimensions=16))

    embeddings = model.get_embeddings(["one document", "second document"])

    assert len(embeddings) == 2
    assert len(embeddings[0].values) == 16
    assert np.isclose(np.linalg.norm(embeddings[0].values), 1.0)
