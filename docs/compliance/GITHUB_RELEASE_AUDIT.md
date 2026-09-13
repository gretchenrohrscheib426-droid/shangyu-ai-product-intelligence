# Pre-publication factual audit

Audited on 2026-09-13 before writing the release READMEs. Mode: **PORTFOLIO_ONLY**. At that initial packaging stage no upload was authorized; the later conditional publication request supersedes that status. This document describes the privately running platform and the narrower public candidate separately.

|Question|Verified finding|Release treatment|
|---|---|---|
|Implemented|Five existing research/report roles, V2 structured evidence, MySQL joins, source tiers, SSE, three export formats|Explain actual code paths; include only locally added, provenance-recorded code|
|Actually run|Latest V2 validation completed; 23 offline tests; live DeepSeek/Tavily; HTML/MD/PDF HTTP200 with matching file hashes; report restored after backend restart|Publish aggregate measurements and validation-file hashes, not private logs|
|Design only|Independent blind evaluation, broad cross-product relevance, production concurrency and continuous monitoring|Mark planned/not measured|
|Limitations|One platform, convenience sample, 90-day window but posts concentrated in a short interval, missing media dates, no image/video reading|Prominent README limitations|
|Real collected data|Fresh read-only MySQL count at audit: **24 posts / 83 comments**; matches current run validation|Publish counts only; exclude raw dataset and original identifiers|
|Analysis subset|17 topic-related posts; 12 primary posts and 15 comments sent to Insight; 5 context-only posts; 7 noise posts|Distinguish these denominators|
|Model inference|1 product and 2 operations opportunity hypotheses; not proven demand or business impact|Label Inference and specify validation|
|Upstream work|JxKim/sentiment_analysis_platform, reference 91bbd617686f8188c2fc114957dbd1e8bd600df0: application architecture, engines, UI and crawler integration|Attribute; do not claim from-scratch authorship|
|Local work|Windows reproduction/integration, real-run verification, V2 comment/relevance/evidence pipeline, source checks, report/export fixes and audits, with AI coding assistance|Document contribution boundaries and human involvement|
|Third-party rights|No root LICENSE in local upstream snapshot; nested MediaCrawler non-commercial learning license; font/vendor/model assets have separate terms|Exclude full upstream, crawlers, vendor code, fonts, model weights, logos and course materials|
|Not public|Keys, sessions/cookies, user profiles, full comments, DB dumps, private paths/logs, original report containing source identifiers|Exclude; use minimized paraphrased examples and aggregate report crops|

## Evidence basis

The source snapshot, current MySQL count and local validation files were read again for this release. The V2 run used 8 real DeepSeek and 8 real Tavily requests including corrective iterations; no additional paid calls or crawling were performed while packaging. The conservative reservation was 10.61198 RMB, not a provider invoice.

Relevance precision 17/17 on a 24-item development set is not model accuracy or a blind holdout score. Core citation coverage is 5/5; a seeded 20-statement assistant-assisted review found 17 Supported and 3 Partially supported. These assess bounded source claims, not objective truth of user experiences. V1 and V2 prompts differ, so comparison is not a controlled A/B experiment.

## Publication decision

Full-source redistribution is not cleared. The candidate contains locally added code with provenance and independently authored documentation/tooling; modified upstream files are not included. No MIT or Apache blanket grant is added. The final phase uses default copyright for original additions and the owner's conditional public-portfolio authorization; no new blanket reuse grant is made. Original UI/logo screenshots are excluded because asset rights are unresolved. Actual locally generated report crops are used instead; they do not depict live-running agents.

The package can be reviewed locally. Current gate results and readiness are recorded in [the security audit](FINAL_SECURITY_AUDIT.json) and [the file manifest](../../publish_manifest.json). GitHub Actions are prepared but cannot have been executed on GitHub before upload.
