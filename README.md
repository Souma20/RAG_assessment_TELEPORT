# Context-Aware Retrieval Engine

Local solution for the GenAI RAG and Vector Search assessment.

The project implements:

- document ingestion over a small technical dataset
- deterministic local embeddings that simulate `textembedding-gecko`
- an in-memory NumPy vector store using cosine similarity
- mocked Vertex AI `TextEmbeddingModel` and `GenerativeModel`
- two retrieval strategies:
  - Strategy A: raw vector search
  - Strategy B: query expansion followed by vector search
- a reproducible benchmark report in `retrieval_benchmark.md`

## Setup

From the repository root:

```powershell
python -m venv venv
newenv\Scripts\Activate
python -m pip install -r requirements.txt
```

## Run Benchmark

```powershell
python -m rag_assessment.benchmark
```

This prints the Strategy A vs Strategy B comparison and writes `retrieval_benchmark.md`.

## Test

```powershell
python -m pytest
```

## Submission Contents

The repository contains:

- `rag_assessment/embedding.py`: local embedding implementations
- `rag_assessment/vector_store.py`: NumPy vector store with cosine search
- `rag_assessment/vertexai_mock.py`: mocked Vertex AI embedding and generative classes
- `rag_assessment/retrieval.py`: ingestion and retrieval orchestration
- `rag_assessment/benchmark.py`: benchmark runner
- `tests/test_retrieval.py`: pytest coverage for retrieval and mocks
- `retrieval_benchmark.md`: generated comparison report

## Production Migration Notes

The local vector store is intentionally small and transparent. In production, the same orchestration boundary can point to Vertex AI embeddings and Vertex AI Vector Search:

1. Replace `MockTextEmbeddingModel` with `vertexai.language_models.TextEmbeddingModel.from_pretrained(...)`.
2. Batch document embedding generation and write vectors to Cloud Storage in Vertex AI Vector Search import format.
3. Create or update a Matching Engine index configured for cosine-compatible similarity.
4. Deploy the index to an index endpoint.
5. Replace `NumpyVectorStore.search(...)` with the deployed index endpoint nearest-neighbor query.

Cosine similarity is used because semantic retrieval usually cares about vector direction rather than vector magnitude. The code normalizes vectors before search, so cosine scoring becomes a fast dot product.
