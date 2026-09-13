# Agent responsibilities and boundaries

|Role|Responsibility|Input|Tools|Output|Failure modes / limits|
|---|---|---|---|---|---|
|Insight|What did this user sample say?|Filtered post title/body and joined comments|Read-only MySQL; DeepSeek; quote/ID checks|insight_findings.json|Ambiguous keywords, promotional text, sparse comments; self-reports are not product tests|
|Media|What do external sources say?|Topic and bounded search queries|Tavily; DeepSeek; normalization|media_evidence.json|Empty results, weak provenance, missing dates; snippets are not full-page reading|
|Query|Which upstream product claims can be verified?|Insight/Media findings with IDs|Tavily; source tiers; DeepSeek|verified_claims.json|Official domain can host community content; exact product/version not always known|
|Forum|Where is evidence aligned, contradictory or missing?|Three actual structured results|DeepSeek; upstream-ID checks|forum_synthesis.json|Opinion differences mislabeled as contradictions; attribution errors require review|
|Report|Select supported conclusions and propose testable opportunities|Four JSON artifacts|DeepSeek selection; deterministic HTML/MD/PDF rendering|report_evidence.json and exports|Bad IDs rejected; short representative quotes may require full saved-text review|

Why several roles instead of one prompt: user experience, external statements and factual verification require different inputs and standards. Separate artifacts make source loss and contradictions inspectable. This is an engineering tradeoff with extra cost and coordination; no experiment proves five agents outperform one model. The shared evidence contract matters more than the number of roles.
