# Shangyu

**Multi-Agent AI Product Sentiment & User Feedback Intelligence Platform**

Turn real-world user feedback into evidence-backed product insights through multi-agent research, web search and fact verification.

[中文文档](README.zh-CN.md) · [Case Study](docs/case-study-doubao.md) · [Architecture](docs/architecture.md)

**REAL-WORLD CASE · Doubao AI Assistant**  
**24 real posts · 83 real comments**  
DeepSeek + Tavily + MySQL  
Insight / Media / Query / Forum / Report

![Real Doubao report: data scope and research window](docs/assets/screenshots/research-scope.png)

## What It Does

- **Real Data:** organize 24 posts / 83 comments into a traceable user-feedback case.
- **Multi-Agent Pipeline:** Insight + Media → Query → Forum → Report, combining user voices, external information and verification.
- **Evidence-aware Iteration:** noise filtering, comment integration, source grading and claim verification connect findings to evidence.

## Why I Built / Reproduced This

AI product feedback is scattered across posts, comments and media. LLM summaries can lose useful details or turn a few opinions into broad conclusions. I reproduced Shangyu to connect collection, search and evidence checks in one inspectable research workflow.

## How It Works

![Multi-Agent architecture and evidence flow](docs/assets/architecture.svg)

**Insight** reads MySQL feedback while **Media** searches with Tavily; these roles run in parallel. **Query** verifies their product claims. **Forum** aligns findings and evidence gaps. **Report** produces HTML / Markdown / PDF, with SSE exposing progress throughout the workflow.

## Real-World Case: Doubao AI Assistant

**Data Scope: 24 posts / 83 comments.** Research focused on learning and office scenarios: what users were doing, pain points, needs and product opportunities. The case follows spreadsheet reporting, scientific drawing and coding feedback from evidence to proposed next steps. [Read the case study](docs/case-study-doubao.md).

## V1 → V2

|V1 Problem|V2 Improvement|
|---|---|
|Noise results|Relevance filtering|
|Comments underused|Comment integration|
|Empty Media context|Search pipeline repair and nonempty-output checks|
|Weak sources|Source grading|
|LLM over-generalization|Evidence cards and bounded claims|

[Bad Cases](docs/bad-cases.md) · [Evidence & Evaluation](docs/evaluation.md)

## Product Value

Shangyu can support:

- Voice-of-Customer triage and user feedback clustering
- Product issue discovery and feature hypothesis generation
- Content / operations planning and evidence-backed research

## My Contribution

Environment reproduction; DeepSeek and Tavily integration; real data collection through the existing integration; MySQL validation; pipeline and export debugging; evidence-quality iteration and Bad Case analysis. Development and review used AI assistance.

Upstream architecture is credited separately, including the original five-role design, UI, prompts and crawler integration. [Contribution boundaries](NOTICE.md).

## Tech Stack

Python · FastAPI · Vue 3 · MySQL · DeepSeek · Tavily · SSE · WeasyPrint

## Demo

The local run produced **HTML / Markdown / PDF outputs**. Below is a crop of the actual final report; screenshot text and numbers are unchanged.

![Final Doubao report output](docs/assets/screenshots/report-cover.png)

[Report screenshot provenance](docs/assets/screenshots/README.md) · [Offline case summary](docs/assets/demo/public-demo.html)

## Code Walkthrough

- [Coordinator](integration/app/services/evidence_pipeline.py): role dependencies, stage state and SSE.
- [Feedback adapter](integration/engines/InsightEngine/tools/product_feedback.py): SQL joins and sample selection.
- [Source grading](portfolio_code/source_quality.py) and [evidence contracts](portfolio_code/evidence_contract.py): inspectable checks.
- [Report assembly](integration/engines/ReportEngine/evidence_report.py): structured findings and source cards.

[All engine entry points](docs/code-walkthrough.md)

## Public Portfolio Quick Start

Public repository is a license-safe portfolio subset of the locally validated system.

With Python 3.11+ and Node 22+, run offline fixture tests and build the example summary:

```sh
python -B -m unittest discover -s tests -v
npm run build
npm run dev
```

`npm run dev` serves the **static portfolio preview** on the loopback host, port 8765. It does not start the five-engine application or perform a search. No API keys or database are needed. [Detailed quick start](docs/quickstart.md) · [Offline examples](examples/example_query.json).

## Full Local System

The full locally validated system depends on upstream components that are not redistributed here because of licensing constraints.

Start with the [upstream repository](https://github.com/JxKim/sentiment_analysis_platform), then review [environment requirements and configuration](docs/quickstart.md#full-local-system) and the [API map](docs/api.md). The local system uses a Vue workbench, FastAPI, MySQL and separately configured DeepSeek/Tavily services.

## Limitations & Responsible Use

The case is a single-platform convenience sample; findings support research hypotheses that need human review. Detailed measurements use a small in-sample development set with assistant-assisted labels, not an independent benchmark; see [Evaluation](docs/evaluation.md). Continuous monitoring, production readiness and business impact have not been established.

Use for research and learning, respect platform terms and crawler licensing, limit request rates, and never bypass CAPTCHAs or access controls. Raw user data and credentials are excluded. CI is offline; the preview is for local development. [Privacy](docs/privacy.md) · [Security](docs/security.md).

## License & Attribution

The [upstream project](https://github.com/JxKim/sentiment_analysis_platform) is credited for the original architecture and application. Restricted components are excluded; original additions retain default copyright without a blanket MIT/Apache or commercial reuse grant. [LICENSE](LICENSE) · [NOTICE](NOTICE.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [License scope](docs/LEGAL_AND_LICENSE.md).
