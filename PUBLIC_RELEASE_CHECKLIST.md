# Public release checklist

- [x] No API keys found in the release candidate
- [x] No cookies
- [x] No passwords
- [x] No private host paths
- [x] No raw private data or original social identifiers
- [x] No unlicensed third-party source included in the reduced portfolio; new additions traced
- [x] README matches real behavior and explains excluded private application
- [x] Screenshots are real and minimized; original report text unchanged
- [x] Metrics are verified with denominators and evaluation limits
- [x] Demo data is minimized / paraphrased and clearly labeled
- [x] License and component inventory checked; uncertain components excluded
- [x] CI does not call paid APIs, social platforms or real databases
- [x] Local file/link/build/import/test checks complete
- [x] No payload over 10 MB, database, dependency installation or model weights
- [x] Local Git status reviewed; no remote, commit or upload
- [x] Owner conditionally authorizes reviewed public portfolio; default copyright retained without blanket reuse grant
- [x] Public repository name and visibility specified; exact allowlist audited
- [x] Authenticate GitHub CLI and resolve active account before publication
- [ ] GitHub Actions actually run after authorized upload (currently NOT RUN)

Checked on 2026-09-13. See [validation](evaluation/release_validation.json) and [manifest](publish_manifest.json). All pre-publication gates passed; post-publication Actions verification remains pending. A scanner PASS is not a legal or privacy guarantee. Full platform redistribution remains blocked; the reduced portfolio license gate passes. Re-run checks and regenerate hashes after edits. Public upload is conditionally authorized by the owner after final staged verification.
