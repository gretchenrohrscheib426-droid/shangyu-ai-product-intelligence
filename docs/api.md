# Private platform API reference

These routes were inspected in the working application; the portfolio server does **not** implement them.

|Method / path|Purpose|Notes|
|---|---|---|
|POST /api/search|Start a topic research task|JSON query; asynchronous task ID; may call paid services|
|GET /api/search/preflight|Presence-only configuration check|Never expose actual keys|
|GET /api/search/latest|Load persisted latest engine results|V2 state/report artifacts|
|POST /api/search/resume|Resume current V2 research or forum stage|Stage cache and request caps apply|
|GET /api/events/stream|SSE event stream|Verified router path|
|POST /api/report/generate|Start same-topic report after engine readiness|JSON query; returns report task ID|
|GET /api/report/status|Current report task and readiness|Completed report restored from saved metadata|
|GET /api/report/result/{task_id}|HTML view|Completed task required|
|GET /api/report/export/md/{task_id}|Markdown export|Download verified|
|GET /api/report/export/pdf/{task_id}|PDF export|Short sanitized download filename|

SSE event names use lowercase on the wire: engine_progress, engine_result, engine_error, forum_message. Uppercase names in acceptance descriptions refer to these event categories. The successful run did not trigger engine_error. No authentication/production-security claim is made for the local API.
