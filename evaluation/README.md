# Evaluation materials

`sample_results.json` contains real aggregate results from the inspected private run, not synthetic metrics. `golden_relevance.example.json` is a two-row synthetic teaching fixture, not the private 24-item labeled set. `provenance.json` contains hashes of private source evidence without personal records.

Recompute fractions from aggregates with Python tests; this checks arithmetic, not independent reproduction of the research. See [methodology](../docs/evaluation.md) and [metric definitions](evaluation_metrics.md).
