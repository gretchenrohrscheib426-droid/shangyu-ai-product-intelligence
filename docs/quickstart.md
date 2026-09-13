# Running the public portfolio and the full local system

## Public Portfolio Quick Start

Use Python 3.11+ and Node 22+. The public code supports offline fixture tests, example outputs and a static portfolio preview. No API key, database, crawler login or npm package installation is needed.

```sh
python -B -m unittest discover -s tests -v
python -B scripts/check_release.py
npm run build
npm run dev
```

Open `<preview-origin>`/docs/assets/demo/public-demo.html; the preview origin is the loopback host on port 8765. `npm run build` renders the aggregate case document, and `npm run dev` serves it. Neither command starts the Vue workbench, launches research or calls the five engines.

[Example input](../examples/example_query.json), [Insight output](../examples/example_insight_output.json) and [report output](../examples/example_report_output.json) explain the data contracts. They are labeled teaching examples; the tests exercise pure validation logic.

PowerShell helpers: [doctor](../scripts/doctor.ps1), [start](../scripts/start.ps1), [stop](../scripts/stop.ps1) and [tests](../scripts/test.ps1). Start accepts `-Node`; doctor/tests accept `-Python` and `-Node` for explicit runtime paths. The [Docker example](../docker-compose.example.yml) also serves only the read-only portfolio preview.

## Full Local System

The full locally validated system depends on upstream components that are not redistributed here because of licensing constraints. Obtain the [upstream repository](https://github.com/JxKim/sentiment_analysis_platform) under suitable rights and follow its setup instructions. The included integration modules document local additions; they are not an application installer.

|Layer|Environment used in the validated local setup|
|---|---|
|API and research|Python 3.11, FastAPI, engine dependencies; separate crawler environment|
|Workbench|Vue 3 / TypeScript frontend, Node build tooling|
|Feedback storage|MySQL 8 with upstream schema and authorized collected records|
|Model service|Configured DeepSeek models for the engine roles|
|Search service|Tavily for external sources and verification|
|Report export|WeasyPrint and its required rendering dependencies|

The local setup used frontend port 5173 and API port 5000, with MySQL exposed only on a loopback mapping. Follow upstream dependency requirements for the version you obtain.

### Configuration overview

The blank [.env.example](../.env.example) names the settings; the public preview does not load them.

|Settings|Purpose in the complete local setup|
|---|---|
|DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME|Private MySQL connection|
|INSIGHT_ENGINE / MEDIA_ENGINE / QUERY_ENGINE / FORUM_HOST / REPORT_ENGINE / KEYWORD_OPTIMIZER groups|Each group has API_KEY, BASE_URL and MODEL_NAME fields for configured model access|
|TAVILY_API_KEY|Real external search|
|QUALITY_PIPELINE_V2 / LIVE_CALLS_ENABLED|Pipeline and live-call controls to review in the upstream/private configuration|

Keep credentials, browser state and collected data outside the public repository. New model/search requests may incur provider charges; public CI performs none. See [architecture](architecture.md), [API map](api.md), [privacy](privacy.md) and [license scope](LEGAL_AND_LICENSE.md).
