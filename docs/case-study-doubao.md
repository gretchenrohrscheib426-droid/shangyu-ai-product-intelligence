# Doubao AI Assistant Case Study

## 1. Research Question
What do this limited sample's learning and office experiences suggest about use cases, frustrations and testable product opportunities? Preserve distinctions between user statements, external facts and model inference.

## 2. Data Scope
24 real posts and 83 comments, freshly counted in MySQL for this audit. Seventeen posts were topic related; twelve primary posts and fifteen comments entered analysis. The 90-day query window was 2026-06-15 to 09-13, but actual posts clustered on 09-01 to 09-12. This is not a continuous 90-day trend study.

## 3. Collection
Prior user-authorized small-sample Xiaohongshu collection using the existing crawler integration. The user completed login. The release process only read counts and saved validation, with no new crawling or paid research. Raw records stay private.

## 4. Data Quality Issues
Ambiguous product keywords admitted lifestyle content; promotion needed separation; post-only retrieval missed useful comments. Filtering generated explicit per-record reasons rather than deleting database rows.

## 5. User Scenarios
Evidence: bounded post/comment statements about spreadsheet reporting, scientific drawing and coding. Judgment: these scenarios appear in this sample; they do not establish prevalence. Product meaning: choose concrete tasks for subsequent usability tests instead of a generic satisfaction survey.

## 6. Positive Feedback
Evidence: some contributors described convenient spreadsheet organization or iterative drawing edits. Judgment: positive self-reports, not independently measured speed or accuracy gains. Product meaning: observe repeat tasks and measure correction effort before claiming a benefit.

## 7. Pain Points
Evidence: negative learning/coding statements, a quota-consumption comment and a scan-with-no-response question. Judgment: specific causes and versions are mostly absent. Product meaning: collect reproducible failure details; do not convert a complaint into a confirmed defect.

## 8. User Needs
Evidence: three explicit questions/requests; two concern guidance and one cross-scenario request concerns restoring a feature. Judgment: guidance needs are interview leads; the feature-restoration request is not promoted as a central office-learning need. No inferred need passed the independent-contributor threshold.

## 9. Media Evidence
Ten nonempty URL/snippet sources from three real Tavily searches. One was official; nine were conservatively graded D. Missing publication dates stayed unknown. Media availability and report length were not used as proxies for quality.

## 10. Fact Verification
Four upstream targets: one verified, three partially verified. Official terms support AI cloud-file storage; they do not confirm subjective productivity, every tutorial claim, a specific app entry or a recent launch. Two added official sources were distinguished from community posts on an official domain.

## 11. Product Opportunities
One accepted Inference: test clearer iteration guidance for scientific drawing. Evidence is the drawing feedback; the experiment should compare task success and revision effort. Generic learning complaints do not validate the drawing opportunity.

## 12. Operations Opportunities
Two accepted Inferences: collect coding feedback by task/language/version, and test clearer operation/entitlement guidance. Validate quota rules, scan failure causes and actual entry paths before writing help content. These are hypotheses, not demonstrated growth outcomes.

## 13. Bad Cases
The important iteration was evidence loss and attribution repair, not longer prompts. Empty Media summaries, missing comments, weak source grades and false Forum conflict were preserved and corrected. Final Forum has no forced consensus or factual conflict.

## 14. Limitations
Single platform, small convenience sample, no image/video inspection, no blind human labels and no controlled A/B. Rule tuning used the same labeled set. Public examples are paraphrases and cannot reproduce the private study. LLM reasoning and editorial review still introduce subjectivity.

## 15. What I Learned
Data quality, evidence lineage and explicit uncertainty are product requirements. Clear role contracts let a reviewer inspect why a conclusion survived validation. My contribution was reproduction, integration, diagnostics and evidence-quality improvements with AI assistance; the upstream five-role architecture is credited separately.
