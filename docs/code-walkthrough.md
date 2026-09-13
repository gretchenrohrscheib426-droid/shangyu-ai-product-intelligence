# Code walkthrough: ten useful review entries

All linked integration modules were newly added in V2. They are source references, not a complete runnable platform. Original orchestration architecture remains credited to upstream.

1. [V2 coordinator](../integration/app/services/evidence_pipeline.py): real dependency order and SSE publishing.
2. [Feedback data adapter](../integration/engines/InsightEngine/tools/product_feedback.py): explicit SQL, joins, anonymity, selection reasons.
3. [Insight](../integration/engines/InsightEngine/product_analysis.py): model payload and evidence-gated findings.
4. [Media](../integration/engines/MediaEngine/product_analysis.py): bounded Tavily search and nonempty-context checks.
5. [Query](../integration/engines/QueryEngine/verification.py): upstream claim targets and verification boundary.
6. [Forum](../integration/engines/ForumEngine/evidence_synthesis.py): synthesis contracts and conflict checks.
7. [Report](../integration/engines/ReportEngine/evidence_report.py): structured inputs and deterministic evidence cards.
8. [Runtime](../integration/engines/common/evidence_runtime.py): call ledger, cached stages and JSON validation.
9. [Source grading](../portfolio_code/source_quality.py): host boundary and community downgrade.
10. [Offline contracts](../portfolio_code/evidence_contract.py): executable quote and evidence-count rules.

Original `app/services/search_service.py`, `frontend/src/stores/search.ts` and `frontend/src/composables/useSSE.ts` remain private because they modify or derive from omitted upstream code. Their roles are documented rather than falsely linked as included source.
