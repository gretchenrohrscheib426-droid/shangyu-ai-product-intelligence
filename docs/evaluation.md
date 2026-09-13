# Evidence quality evaluation

**Scope: small development evaluation on a small in-sample development set, with assistant-assisted labels; not an independent benchmark.** These measurements assess evidence handling in the inspected case, not general model performance.

|Metric|Measured result|Interpretation|
|---|---|---|
|Relevance precision|17/17 = 100%; development set n=24|Assistant-assisted labels; same-data development regression, not blind generalization|
|Core citation coverage|5/5 = 100%|Known ID, matching URL and literal quote; not objective truth of self-report|
|Unsupported core claims|0|Assistant semantic review of bounded source statements|
|Seeded fact audit|20 statements: 17 Supported, 3 Partially supported|Pool: 18 rendered cards + 4 sample counts; seed20260913; no independent human review|
|Comment input utilization|15/83 = 18.07%|Filtered comments actually sent to Insight|
|Comment citation utilization|8/83 = 9.64%; 8/15 = 53.33%|Unique comments cited in final report|
|Source quality|Media S1/D9; Query additions S2/D2|Unknown authorship conservatively D; source counts overlap across roles|

Aggregate results are in [sample_results.json](../evaluation/sample_results.json); source-file hashes in [provenance.json](../evaluation/provenance.json). Real raw data and the complete golden set are intentionally withheld. Public unit tests validate the contracts on clearly labeled fixtures and cannot reproduce the private data metrics.

The private app passed 23 offline regressions and live export checks. The public offline tests are documented separately in [CI scope](ci.md). V1/V2 queries differ, so do not claim a controlled performance gain. Classification rules, quoted text and Forum summaries can still be wrong; source review remains necessary.
