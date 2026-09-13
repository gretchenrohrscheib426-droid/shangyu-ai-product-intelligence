# From collected records to model input

Historical approved collection: Xiaohongshu → MediaCrawler within SentinelSpider → MySQL. The user completed login manually. No collection/login activity was performed for this release.

V2: explicit SELECT of posts and comments → join by note_id → topic/context classification → comment information/duplicate/per-post filters → anonymized registry → selected JSON payload → DeepSeek → literal evidence validation → findings. MySQL rows do not enter the LLM automatically.

|Layer|Meaning|Public treatment|
|---|---|---|
|Raw data|Collected post/comment records, before analysis filters|Excluded|
|Relevant data|Topic related; primary user feedback separated from promotion/background|Aggregate counts only|
|LLM summary|Model organization of bounded evidence|Minimized examples and measured output counts|
|Verified fact|A specific external statement supported by suitable sources|Keep source quality, time and scope limits|
|Inference|A potential product/operations opportunity|Label as hypothesis and include validation plan|

The reviewed run has 24 posts/83 comments: 17 topic-related posts, 12 primary and 5 context-only; 7 noise. Fifteen comments enter Insight, nine are cited in Insight findings and eight in the final report. Each figure has its own denominator. Source IDs and anonymous contributor labels remain in private evidence; public examples use unrelated aliases.

Comments from excluded parents (40), low information (9), no experience signal (7), off-scope chat/commands (5), duplication (3), promotion/unrelated (2), per-post cap (2) account for 68 excluded comments. The remaining 15 are selected. The cap is 8 per post in analysis, distinct from collection settings.
