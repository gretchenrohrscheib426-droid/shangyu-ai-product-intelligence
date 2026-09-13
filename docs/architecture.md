# Actual V2 architecture

![Actual architecture](assets/architecture.svg)

The Vue 3 frontend sends a query to FastAPI. SearchService selects the V2 evidence coordinator. **Insight and Media run concurrently; Query waits for their findings.** Forum runs after verification, and Report is started with the same research topic after all four JSON artifacts exist.

Insight executes two explicit MySQL queries, joins posts and comments by note_id, filters scope, then builds the actual LLM input. Media calls Tavily. Query uses upstream targets and Tavily with an official-source preference. DeepSeek powers all five research/report roles; KEYWORD_OPTIMIZER shares configured service values but a separate optimizer call is not claimed in the V2 run.

The event bus delivers engine_progress, engine_result and forum_message over SSE. ENGINE_ERROR is implemented but not triggered by the successful final run. State and reports are written to per-task storage. Completed reports restore after restart; in-memory event replay does not.

This release's source extracts are a subset. The original Vue/FastAPI shell, DB schema and crawler are excluded. There is no extra agent, new RAG system, new database or new model training.
