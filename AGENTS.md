# Portfolio-only workspace

Do not add upstream platform/crawler/vendor code without checking its license.
Do not copy private data, credentials, logs, screenshots with personal information, or host paths.
No real network research, paid APIs, crawling, login or database access in CI/tests.
Distinguish synthetic/paraphrased examples from the measured private run.
Preserve contribution attribution. The integration directory is reference code, not a complete runnable app.
Run scripts/check_release.py, scripts/security_scan.py and offline unit/security tests. Only publish an exact reviewed allowlist after all final gates pass and the owner has authorized the target repository and visibility. Never publish parent directories, private audit material, unreviewed files or provider secrets.
