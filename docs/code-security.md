# Publication code security review

Scope: executable portfolio scripts and pure contracts, plus the included integration source references. Omitted application endpoints were inspected for context but are not certified for public deployment.

|Boundary|Observed behavior / change|Validation|
|---|---|---|
|LLM/post/search text → shell|No eval, exec, os.system or shell=True call in included Python; model output is parsed as JSON|AST call review; no paid code imported in CI|
|Input → SQL|Two fixed SELECT statements with literal table names in product_feedback.py; user/model query not concatenated into SQL|AST confirms literal SQL and SELECT-only statements; table names are fixed|
|Citation URL → HTML/Markdown|Text/attributes HTML-escaped; final release adds http/https-only safe_url, rejects control characters/userinfo, encodes Markdown delimiters|Protocol and delimiter regression tests; applied only to release copies|
|HTTP path → local file|Allowlist membership, decoded path checks, canonical realpath containment, hidden-segment and Windows alternate-stream checks; no writes|HTTP regressions include outside symlink, traversal, unlisted file and hidden Git file|
|Uploaded data|Public portfolio has no upload/template API; non-GET/HEAD returns 405|HTTP method regression|
|Private download/template context|Private report download selects a stored task; V2 report filenames are fixed. Current private template input is JSON text, not a file-execution endpoint|No public certification; private API has no demonstrated public auth/RBAC/rate/body-limit guarantees|
|Write paths in integration references|Internal coordinator supplies task folders and fixed stage names; these helpers are not public file APIs|Do not wire arbitrary user paths to these helpers|
|Preview start/stop|Hidden process, process-start-time/PID validation, command identity check, loopback default|Windows start/stop smoke check; only owned process stopped|
|Docker|Read-only source, no secrets, no-new-privileges, loopback host port; same allowlisted Node server|Compose structure check|
|CI|Pure imports, fixtures, syntax/build/security scans only; no app imports, database or provider keys|Workflow review and local command run|

The URL helper does not fetch any resource; it is not a full SSRF policy for a future network fetcher. Code snippets that save private runtime data must stay in a private deployment. Never expose the original full platform or preview directly as a production service. The report shown in screenshots predates release-only hardening; no new live result is claimed.
