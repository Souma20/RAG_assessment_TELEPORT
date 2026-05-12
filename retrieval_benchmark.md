# Retrieval Benchmark

This benchmark compares raw vector search with query-expanded retrieval.

## Similarity Metric

Cosine similarity is used because semantic search depends more on vector direction than magnitude. All vectors are L2-normalized, so ranking can be computed with a dot product.

## Strategy Comparison

### Query: How does the system handle peak load?

Expanded query: `How does the system handle peak load? peak traffic spike autoscaling horizontal scaling queue depth backpressure request shedding cached responses capacity`

| Rank | Strategy A: Raw Vector Search | Score | Strategy B: AI-Enhanced Retrieval | Score |
| --- | --- | ---: | --- | ---: |
| 1 | Resilience and failure handling (`resilience`) | 0.158 | Peak-load autoscaling (`capacity_peak_load`) | 0.467 |
| 2 | Peak-load autoscaling (`capacity_peak_load`) | 0.110 | Resilience and failure handling (`resilience`) | 0.127 |
| 3 | Latency and SLOs (`latency_slo`) | 0.109 | Latency and SLOs (`latency_slo`) | 0.061 |

### Query: How do we measure whether search results are good?

Expanded query: `How do we measure whether search results are good? retrieval quality evaluation recall at k mean reciprocal rank manual relevance labels benchmark queries retrieval quality evaluation recall at k mean reciprocal rank manual relevance labels benchmark queries`

| Rank | Strategy A: Raw Vector Search | Score | Strategy B: AI-Enhanced Retrieval | Score |
| --- | --- | ---: | --- | ---: |
| 1 | Security controls (`security`) | 0.209 | Retrieval evaluation (`evaluation`) | 0.601 |
| 2 | Vector index design (`vector_index`) | 0.063 | Security controls (`security`) | 0.135 |
| 3 | Retrieval evaluation (`evaluation`) | 0.063 | Latency and SLOs (`latency_slo`) | 0.067 |

### Query: How are private tenant documents kept out of retrieval results?

Expanded query: `How are private tenant documents kept out of retrieval results? security access control authorization tenant scope policy labels metadata filters unauthorized passages`

| Rank | Strategy A: Raw Vector Search | Score | Strategy B: AI-Enhanced Retrieval | Score |
| --- | --- | ---: | --- | ---: |
| 1 | Security controls (`security`) | 0.264 | Security controls (`security`) | 0.510 |
| 2 | Vector index design (`vector_index`) | 0.120 | Vector index design (`vector_index`) | 0.186 |
| 3 | Embedding pipeline (`embedding_pipeline`) | 0.106 | Embedding pipeline (`embedding_pipeline`) | 0.175 |

## JSON Output

```json
[
  {
    "query": "How does the system handle peak load?",
    "expanded_query": "How does the system handle peak load? peak traffic spike autoscaling horizontal scaling queue depth backpressure request shedding cached responses capacity",
    "strategy_a_raw": [
      {
        "id": "resilience",
        "score": 0.15806113183498383,
        "text": "The retrieval service degrades gracefully when dependencies fail. If the embedding service is unavailable, the application returns cached results or a controlled fallback response and records the incident for review.",
        "metadata": {
          "title": "Resilience and failure handling"
        }
      },
      {
        "id": "capacity_peak_load",
        "score": 0.10956612974405289,
        "text": "The serving layer handles peak load through horizontal autoscaling, queue-based backpressure, and request shedding for non-critical traffic. During a spike, replicas are added when CPU, memory, and queue depth cross their target thresholds. Cached responses absorb repeated read traffic.",
        "metadata": {
          "title": "Peak-load autoscaling"
        }
      },
      {
        "id": "latency_slo",
        "score": 0.10858539491891861,
        "text": "The API targets a p95 latency of 300 milliseconds for retrieval requests. Latency is monitored with distributed traces, percentile dashboards, and alerts that fire when the error budget burn rate increases.",
        "metadata": {
          "title": "Latency and SLOs"
        }
      }
    ],
    "strategy_b_enhanced": [
      {
        "id": "capacity_peak_load",
        "score": 0.4673998951911926,
        "text": "The serving layer handles peak load through horizontal autoscaling, queue-based backpressure, and request shedding for non-critical traffic. During a spike, replicas are added when CPU, memory, and queue depth cross their target thresholds. Cached responses absorb repeated read traffic.",
        "metadata": {
          "title": "Peak-load autoscaling"
        }
      },
      {
        "id": "resilience",
        "score": 0.12690618634223938,
        "text": "The retrieval service degrades gracefully when dependencies fail. If the embedding service is unavailable, the application returns cached results or a controlled fallback response and records the incident for review.",
        "metadata": {
          "title": "Resilience and failure handling"
        }
      },
      {
        "id": "latency_slo",
        "score": 0.06143677607178688,
        "text": "The API targets a p95 latency of 300 milliseconds for retrieval requests. Latency is monitored with distributed traces, percentile dashboards, and alerts that fire when the error budget burn rate increases.",
        "metadata": {
          "title": "Latency and SLOs"
        }
      }
    ]
  },
  {
    "query": "How do we measure whether search results are good?",
    "expanded_query": "How do we measure whether search results are good? retrieval quality evaluation recall at k mean reciprocal rank manual relevance labels benchmark queries retrieval quality evaluation recall at k mean reciprocal rank manual relevance labels benchmark queries",
    "strategy_a_raw": [
      {
        "id": "security",
        "score": 0.20851443707942963,
        "text": "Access control is enforced before retrieval. User identity, tenant scope, document labels, and policy rules are checked so that search results never include unauthorized passages.",
        "metadata": {
          "title": "Security controls"
        }
      },
      {
        "id": "vector_index",
        "score": 0.06314451992511749,
        "text": "The vector index stores normalized dense vectors and retrieves nearest neighbors with cosine similarity. Metadata filters restrict searches by tenant, document type, and freshness window before ranking.",
        "metadata": {
          "title": "Vector index design"
        }
      },
      {
        "id": "evaluation",
        "score": 0.0631445124745369,
        "text": "Retrieval quality is evaluated with recall at k, mean reciprocal rank, and manual relevance labels. Benchmark queries should include ambiguous wording, operational questions, and domain-specific terms.",
        "metadata": {
          "title": "Retrieval evaluation"
        }
      }
    ],
    "strategy_b_enhanced": [
      {
        "id": "evaluation",
        "score": 0.6014856100082397,
        "text": "Retrieval quality is evaluated with recall at k, mean reciprocal rank, and manual relevance labels. Benchmark queries should include ambiguous wording, operational questions, and domain-specific terms.",
        "metadata": {
          "title": "Retrieval evaluation"
        }
      },
      {
        "id": "security",
        "score": 0.13503140211105347,
        "text": "Access control is enforced before retrieval. User identity, tenant scope, document labels, and policy rules are checked so that search results never include unauthorized passages.",
        "metadata": {
          "title": "Security controls"
        }
      },
      {
        "id": "latency_slo",
        "score": 0.06711965054273605,
        "text": "The API targets a p95 latency of 300 milliseconds for retrieval requests. Latency is monitored with distributed traces, percentile dashboards, and alerts that fire when the error budget burn rate increases.",
        "metadata": {
          "title": "Latency and SLOs"
        }
      }
    ]
  },
  {
    "query": "How are private tenant documents kept out of retrieval results?",
    "expanded_query": "How are private tenant documents kept out of retrieval results? security access control authorization tenant scope policy labels metadata filters unauthorized passages",
    "strategy_a_raw": [
      {
        "id": "security",
        "score": 0.26375219225883484,
        "text": "Access control is enforced before retrieval. User identity, tenant scope, document labels, and policy rules are checked so that search results never include unauthorized passages.",
        "metadata": {
          "title": "Security controls"
        }
      },
      {
        "id": "vector_index",
        "score": 0.11980829387903214,
        "text": "The vector index stores normalized dense vectors and retrieves nearest neighbors with cosine similarity. Metadata filters restrict searches by tenant, document type, and freshness window before ranking.",
        "metadata": {
          "title": "Vector index design"
        }
      },
      {
        "id": "embedding_pipeline",
        "score": 0.1059994250535965,
        "text": "Documents are chunked into passages, cleaned, embedded with a text embedding model, and persisted with metadata. Re-embedding is triggered when the model version, chunking policy, or source document content changes.",
        "metadata": {
          "title": "Embedding pipeline"
        }
      }
    ],
    "strategy_b_enhanced": [
      {
        "id": "security",
        "score": 0.5098769664764404,
        "text": "Access control is enforced before retrieval. User identity, tenant scope, document labels, and policy rules are checked so that search results never include unauthorized passages.",
        "metadata": {
          "title": "Security controls"
        }
      },
      {
        "id": "vector_index",
        "score": 0.185916930437088,
        "text": "The vector index stores normalized dense vectors and retrieves nearest neighbors with cosine similarity. Metadata filters restrict searches by tenant, document type, and freshness window before ranking.",
        "metadata": {
          "title": "Vector index design"
        }
      },
      {
        "id": "embedding_pipeline",
        "score": 0.1752432882785797,
        "text": "Documents are chunked into passages, cleaned, embedded with a text embedding model, and persisted with metadata. Re-embedding is triggered when the model version, chunking policy, or source document content changes.",
        "metadata": {
          "title": "Embedding pipeline"
        }
      }
    ]
  }
]
```

## Vertex AI Vector Search Migration

For production, replace the mock embedding model with Vertex AI `TextEmbeddingModel`, batch-generate embeddings, import vectors and metadata into Vertex AI Vector Search, deploy the index to an endpoint, and replace the local NumPy nearest-neighbor call with Matching Engine queries. Keep query expansion as a separate orchestration step so it can be evaluated, cached, and guarded independently.
