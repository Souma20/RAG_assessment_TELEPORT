"""Assessment dataset."""

TECHNICAL_PARAGRAPHS = [
    {
        "id": "capacity_peak_load",
        "title": "Peak-load autoscaling",
        "text": (
            "The serving layer handles peak load through horizontal autoscaling, "
            "queue-based backpressure, and request shedding for non-critical traffic. "
            "During a spike, replicas are added when CPU, memory, and queue depth cross "
            "their target thresholds. Cached responses absorb repeated read traffic."
        ),
    },
    {
        "id": "latency_slo",
        "title": "Latency and SLOs",
        "text": (
            "The API targets a p95 latency of 300 milliseconds for retrieval requests. "
            "Latency is monitored with distributed traces, percentile dashboards, and "
            "alerts that fire when the error budget burn rate increases."
        ),
    },
    {
        "id": "embedding_pipeline",
        "title": "Embedding pipeline",
        "text": (
            "Documents are chunked into passages, cleaned, embedded with a text embedding "
            "model, and persisted with metadata. Re-embedding is triggered when the model "
            "version, chunking policy, or source document content changes."
        ),
    },
    {
        "id": "vector_index",
        "title": "Vector index design",
        "text": (
            "The vector index stores normalized dense vectors and retrieves nearest "
            "neighbors with cosine similarity. Metadata filters restrict searches by "
            "tenant, document type, and freshness window before ranking."
        ),
    },
    {
        "id": "query_rewrite",
        "title": "Query expansion",
        "text": (
            "A generative model can rewrite short or ambiguous user questions into "
            "embedding-friendly search text. The rewrite adds likely synonyms, domain "
            "terms, and operational context without changing the user's intent."
        ),
    },
    {
        "id": "resilience",
        "title": "Resilience and failure handling",
        "text": (
            "The retrieval service degrades gracefully when dependencies fail. If the "
            "embedding service is unavailable, the application returns cached results "
            "or a controlled fallback response and records the incident for review."
        ),
    },
    {
        "id": "security",
        "title": "Security controls",
        "text": (
            "Access control is enforced before retrieval. User identity, tenant scope, "
            "document labels, and policy rules are checked so that search results never "
            "include unauthorized passages."
        ),
    },
    {
        "id": "evaluation",
        "title": "Retrieval evaluation",
        "text": (
            "Retrieval quality is evaluated with recall at k, mean reciprocal rank, and "
            "manual relevance labels. Benchmark queries should include ambiguous wording, "
            "operational questions, and domain-specific terms."
        ),
    },
]
