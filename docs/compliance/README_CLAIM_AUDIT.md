# README factual review

This table records the original publication review. The current READMEs present the product and case first; detailed metrics are in [Evaluation](../evaluation.md). The underlying values and contribution boundaries are unchanged. Both original READMEs were reviewed line by line. Metrics below were rechecked against the current MySQL counts, actual run outputs and saved validation; claims about code were checked against included/private source. Text hashes and line review rows are retained in the private audit snapshot. Examples are not presented as full production output.

|Claim|Evidence and restriction|Result|
|---|---|---|
|24 real posts / 83 real comments|Fresh read-only MySQL count; matches relevance_audit.json|PASS|
|12 primary posts / 15 analyzed comments|Actual relevance/input audit; 17 topic-related includes 5 context-only|PASS|
|17/17 relevance precision|24-item same-data development set; assistant-assisted labels, not model accuracy or blind test|PASS|
|5/5 core citations|Saved core-evidence validation; not objective truth of user self-report|PASS|
|17 supported / 3 partial, sample 20|Seeded saved V2 fact audit; no independent human reviewer|PASS|
|Five roles and their order|Insight + Media parallel, then dependent Query, Forum, Report; not three-way parallel|PASS|
|Real DeepSeek / Tavily integration|Saved real response/search/usage files; no new calls for publication|PASS|
|SSE and exports|Final saved validation confirms progress/result/forum plus HTML/MD/PDF; engine_error was not triggered in successful run|PASS|
|1 product / 2 operations opportunities|Report evidence identifies these as Inference, not measured business improvements|PASS|
|V1 → V2 changes|Source additions and bad-case records; different prompts, not controlled A/B|PASS|
|My Work vs upstream|Original architecture/UI/crawler attributed; local reproduction/integration/V2 work disclosed as AI assisted|PASS|
|Production / accuracy / independent / from-scratch wording|Occurrences are explicit limits or negations; no unsupported enterprise, scale, uptime or whole-system originality claim|PASS|
|Public package behavior|Offline contracts and static summary; original app and private data excluded|PASS|

The new release-only security patches are not evidence of a newly completed live study. The sample is single-platform, small, self-selected and not a continuous 90-day trend sample. Citation and precision denominators are explicit. A plan is not counted as an implemented result.
