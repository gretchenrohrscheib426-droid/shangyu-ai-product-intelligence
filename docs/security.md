# Security and publication boundaries

This is a local-development portfolio, not a secured public research service. Authentication, RBAC and rate limiting have not been demonstrated for internet deployment. Keep the original app and data private.

Publication checks combine official Gitleaks with full redaction and recursive decoding, a separate credential/entropy/privacy scanner, Git commit/blob inspection, strict payload exclusions, image metadata and visual review, provenance checks and offline security regressions. Empty values and explicit placeholders are allowed; masked real key fragments are not. Keyword mentions are classified as documentation or executable expressions, not blindly treated as leaks. File hashes are recorded as integrity values, not credentials.

The preview serves only the explicit allowlist and confines resolved paths to the repository. It denies hidden files, alternate streams, unlisted files, outside symlinks and writes. Model/search/user text is never executed as code. [Code review](code-security.md) explains remaining integration assumptions.

CI performs no paid research, login, collection or database access and receives no provider secrets. Use only synthetic fixtures. Never post credentials in issues or pull requests. If a real credential is found in public history, stop immediately and rotate it privately before addressing history; deleting the current file alone is insufficient.

The [final security audit](compliance/FINAL_SECURITY_AUDIT.md) is scoped to its recorded snapshot. Re-run all checks after changes. A scanner is heuristic; PASS is not an unlimited legal or security guarantee.
