# Troubleshooting

- Full app imports fail in integration/: expected; third-party shell is omitted. Run portfolio_code tests only, or use an authorized private checkout.
- Blank API configuration: intentional. This package needs no keys; do not copy private .env into it.
- Port8765 busy: select another port with start.ps1 -Port; never stop unrelated processes.
- Python or Node missing: point -Python to an existing compatible interpreter; no global install is performed by these scripts.
- Public data metrics differ from fixture tests: fixtures are minimal examples; private aggregate measurements have separate provenance.
- No multi-agent-running image: none was retained with cleared public asset rights; no success UI is reconstructed.
- CI results: inspect the exact commit and run links in [the publication record](compliance/PUBLISHED_RELEASE_RECORD.md); absence of a badge does not indicate a failed run.
- Full Vue frontend build is excluded from public CI. A separate local build of the private application is recorded as such.
