"""Generate the Strategy A vs Strategy B benchmark report."""

from __future__ import annotations

import json
from pathlib import Path

from .data import TECHNICAL_PARAGRAPHS
from .retrieval import ContextAwareRetrievalEngine


QUERIES = [
    "How does the system handle peak load?",
    "How do we measure whether search results are good?",
    "How are private tenant documents kept out of retrieval results?",
]


def render_report(comparison: list[dict]) -> str:
    lines = [
        "# Retrieval Benchmark",
        "",
        "This benchmark compares raw vector search with query-expanded retrieval.",
        "",
        "## Similarity Metric",
        "",
        "Cosine similarity is used because semantic search depends more on vector "
        "direction than magnitude. All vectors are L2-normalized, so ranking can be "
        "computed with a dot product.",
        "",
        "## Strategy Comparison",
        "",
    ]

    for item in comparison:
        lines.extend(
            [
                f"### Query: {item['query']}",
                "",
                f"Expanded query: `{item['expanded_query']}`",
                "",
                "| Rank | Strategy A: Raw Vector Search | Score | Strategy B: AI-Enhanced Retrieval | Score |",
                "| --- | --- | ---: | --- | ---: |",
            ]
        )
        for rank, (raw, enhanced) in enumerate(
            zip(item["strategy_a_raw"], item["strategy_b_enhanced"]),
            start=1,
        ):
            lines.append(
                "| {rank} | {raw_title} (`{raw_id}`) | {raw_score:.3f} | "
                "{enhanced_title} (`{enhanced_id}`) | {enhanced_score:.3f} |".format(
                    rank=rank,
                    raw_title=raw["metadata"]["title"],
                    raw_id=raw["id"],
                    raw_score=raw["score"],
                    enhanced_title=enhanced["metadata"]["title"],
                    enhanced_id=enhanced["id"],
                    enhanced_score=enhanced["score"],
                )
            )
        lines.append("")

    lines.extend(
        [
            "## JSON Output",
            "",
            "```json",
            json.dumps(comparison, indent=2),
            "```",
            "",
            "## Vertex AI Vector Search Migration",
            "",
            "For production, replace the mock embedding model with Vertex AI "
            "`TextEmbeddingModel`, batch-generate embeddings, import vectors and "
            "metadata into Vertex AI Vector Search, deploy the index to an endpoint, "
            "and replace the local NumPy nearest-neighbor call with Matching Engine "
            "queries. Keep query expansion as a separate orchestration step so it can "
            "be evaluated, cached, and guarded independently.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    engine = ContextAwareRetrievalEngine()
    engine.ingest(TECHNICAL_PARAGRAPHS)
    comparison = engine.compare(QUERIES, top_k=3)
    report = render_report(comparison)
    Path("retrieval_benchmark.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
