# Doubao AI Assistant — Product Feedback Case Study

## Research Goal

Understand how people use Doubao for learning and office tasks, which experiences help or frustrate them, and which product or operations ideas deserve a concrete follow-up test. The workflow connects user feedback, external information and fact verification before proposing action.

## Data Scope

|Scope|Records|
|---|---|
|Collected public feedback|24 posts / 83 comments|
|Primary analysis input|12 primary posts / 15 comments|

Collection used the existing Xiaohongshu integration. MySQL joins connected posts with their comments; relevance and information filters selected the analysis input. The requested window was June 15–September 13, 2026; collected posts were dated September 1–12. Public examples paraphrase reviewed findings and omit raw profiles and identifiers.

## What Users Were Trying To Do

|Scenario|Evidence from the reviewed feedback|What it suggests|
|---|---|---|
|Spreadsheet / reporting|A comment described using the assistant to organize spreadsheet data for reporting.|Use a concrete table-to-report task when testing utility and correction effort.|
|Scientific drawing|Feedback described drawing and iterative revision through instructions.|Study how users explain a desired change and decide whether the revision is acceptable.|
|Coding / learning|Contributors expressed differing experiences with coding and learning tasks.|Separate task, language and version when collecting feedback so incompatible experiences are not pooled.|

The table summarizes source statements; it does not quote users verbatim or rank scenario prevalence.

## What Worked

- **Spreadsheet organization:** a user described a convenient reporting workflow. This is a useful task to reproduce in a usability study.
- **Iterative drawing:** feedback described adjusting a drawing through successive instructions. It provides a concrete starting point for studying revision guidance.

These are positive reported experiences. Speed and accuracy gains were not independently measured.

## Friction / Pain Points

|Observed feedback|Product question to investigate|
|---|---|
|Negative coding and learning experiences alongside different opinions|Which task, input, language and version explain the difference?|
|A question about quota consumption|Do users understand when an action consumes an entitlement?|
|A scan-with-no-response question|Can users identify the correct operation path and recover when no response appears?|

The reports identify investigation targets. Reproduction and version details are needed to determine causes.

## Product Opportunities

### Clearer guidance for revising scientific drawings

|Step|Reasoning|
|---|---|
|Problem|Users need to communicate and evaluate successive drawing changes.|
|Evidence|The reviewed drawing feedback describes iterative edits.|
|Hypothesis|Task and revision guidance could help users express changes and reach an acceptable result.|
|How to validate|Compare a defined drawing task with and without guidance; observe task success, revision effort and remaining errors.|

This is the product hypothesis retained by the analysis. General learning complaints are not used as evidence for the drawing idea.

## Operations Opportunities

### Collect reproducible coding feedback

|Step|Reasoning|
|---|---|
|Problem|Mixed coding opinions are difficult to turn into a reproducible issue.|
|Evidence|Reviewed contributors expressed different coding experiences.|
|Hypothesis|A feedback form organized by task, language, version and failure example could improve triage.|
|How to validate|Pilot the form and review whether submissions contain enough detail for reproduction and routing.|

### Make operation and entitlement guidance easier to use

|Step|Reasoning|
|---|---|
|Problem|Users asked about quota consumption and scanning without a response.|
|Evidence|These questions appear in the reviewed comments.|
|Hypothesis|Clearer instructions about operation paths and entitlement rules could help users complete the task.|
|How to validate|First verify the current rules and reproduce the path; then test task completion and comprehension with proposed help content.|

Both are operations hypotheses for validation, not measured retention or growth outcomes.

## Evidence Quality

Insight retains the user-feedback basis; Media contributes URL/snippet sources; Query checks product claims; Forum separates evidence gaps from conflicts; Report preserves supporting cards. Official sources and community contributions receive different grades, including community pages hosted under an official domain.

Official terms support AI cloud-file storage. User productivity claims, tutorial details and recent-launch statements require different evidence and are not established by those terms. Missing source dates remain unknown. [Detailed evaluation and denominators](evaluation.md) · [Source grading](../portfolio_code/source_quality.py).

## Bad Cases

|Failure|What changed|Why it matters|
|---|---|---|
|Comments missing from post-only retrieval|Join posts and comments explicitly, then inspect the model payload.|Users' concrete task descriptions can enter the analysis.|
|Media had URLs but an empty summary|Reject empty structured output and retain source snippets.|Downstream verification receives usable search context.|
|Forum treated differing opinions as factual conflict|Require verified conflicting claims and preserve role attribution.|A disagreement becomes an investigation question instead of a fabricated conclusion.|

[Full Bad Case review](bad-cases.md).

## Limitations

One platform and a convenience sample support exploratory task hypotheses, not population trends. Collected dates do not cover the requested window continuously. No image/video inspection, independent blind labeling or controlled V1/V2 comparison was performed; rules were developed on the same sample. LLM analysis used assistant review, and proposed changes have not yet demonstrated usability or business gains. [Evaluation](evaluation.md) explains the small development evaluation and its boundaries.
