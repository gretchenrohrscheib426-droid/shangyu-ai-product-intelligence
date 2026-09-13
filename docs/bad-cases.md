# Real bad cases and corrective work

|Observed problem|Evidence / root cause|Change|Measured result / caveat|
|---|---|---|---|
|Keyword noise|A bodily-routine tip shared the ambiguous product keyword; raw retrieval was not topic validation. Platform recommendation causality was not independently proven.|Topic/context filtering|Seven posts rejected as noise in the inspected set; not a generalization score|
|Comments omitted|V1 post search did not join comments; 0 comment-ID rows in its saved Insight history|Explicit note_id join and payload inspection|15 comments supplied, 9 cited by Insight, 8 by report|
|Media empty context|Saved V1 had 14 unique URLs but empty latest_summary; failed structured handling allowed an empty downstream summary|Reject empty/non-object output; preserve failures|V2 10 nonempty source snippets and 4 validated lines of evidence|
|Over-generalization|Forum described a broad core topic and optimistic mood from thin evidence|Bounded wording, source cards and semantic review|Core5/5 traceable; this does not prove elimination of hallucination|
|Weak Query sources|Tutorials and personal writeups cannot independently confirm product capability; a community subdomain was initially graded official|Domain boundaries, community downgrade and editorial notes|1 verified and 3 partially verified product statements|
|Repeated reflection|Prior host messages repeated a summary without new evidence|Fixed-snapshot stopping rule and stage checkpoints|No repeated Insight LLM rewrite for unchanged evidence|
|False conflict / wrong attribution|Early Forum output mixed opposing opinions with factual conflict; later mixed a tutorial with user feedback|Verified-conflict requirement; explicit role attribution; real corrective host calls|Final consensus0/conflicts0; candidates retained privately|
|Valid requests rejected|Questions about use cases or a screen location failed an overly narrow explicit-need rule|Broader request grammar and regression tests|3 explicit requests retained; no unsupported inferred need added|
|PDF download canceled|Full research query was used as a long download filename on Windows|Short sanitized report title|Real frontend PDF download completed|

Raw bad-case texts, source IDs and failed model outputs remain private. This table is a paraphrased engineering account, not fabricated before/after screenshots. Public fixtures test the rule contracts only.
