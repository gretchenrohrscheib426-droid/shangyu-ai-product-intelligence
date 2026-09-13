# Excluded publication content

|Not public|Reason|
|---|---|
|Full original app, upstream modifications, MediaCrawler, SentinelSpider|Redistribution rights unclear or restricted|
|Original Vue UI, logos, course images, vendor JS and fonts|Separate rights; not cleared for this package|
|Environment files, keys, passwords, authentication headers|Credentials|
|Cookies, browser profiles, storage state, login state and QR images|Account/login access and personal information|
|Raw posts/comments, user profiles, database files/dumps, spreadsheets and crawler exports|No bulk-data authorization; original identifiers excluded|
|Runtime, private evidence, logs, full HTML/Markdown/PDF reports|Private paths, prompts, source links or user text|
|Model weights, environments, dependency installations, caches and dist|Unnecessary generated or licensed payloads|
|Private baseline diffs, audit tool binaries and audit working directories|Local audit artifacts, not portfolio content|
|Prior ZIP candidates and packaging helpers outside this repository|Superseded or local-only material; never stage a parent directory|

Only files listed in [PUBLIC_FILE_ALLOWLIST.txt](PUBLIC_FILE_ALLOWLIST.txt) may be staged. The authenticated Git metadata needed for publishing is separate from the archive payload; commits are scanned before push. Examples are synthetic / anonymized examples, not the raw study dataset.
