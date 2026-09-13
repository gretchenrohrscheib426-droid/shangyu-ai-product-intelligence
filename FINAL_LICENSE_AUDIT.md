# Final license audit

## Result: PASS for PORTFOLIO_ONLY; full upstream redistribution remains blocked

This result applies only to the exact reduced file allowlist. The owner explicitly authorized public portfolio publication after all gates pass. No MIT/Apache license was added. Original additions remain under default copyright without a new general reuse grant. Public source visibility is not a claim of unrestricted open-source licensing. GitHub explains the difference between [public visibility and licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

|Component|Source|Observed terms|Redistribute / modify / public / commercial|Release treatment|
|---|---|---|---|---|
|Original platform and SentinelSpider wrapper|[JxKim upstream](https://github.com/JxKim/sentiment_analysis_platform)|No root LICENSE in inspected archive|Not established in each category|Entire upstream app, changed upstream files and original UI excluded|
|MediaCrawler|[Official source and license](https://github.com/NanmiCoder/MediaCrawler/blob/main/LICENSE)|NON-COMMERCIAL LEARNING LICENSE 1.1|Specified learning permissions are conditional; broad public sublicensing not established; commercial use requires consent|Complete crawler, notices-bearing source and login assets excluded; attribution retained|
|Nine local V2 additions|[Recorded provenance](docs/code-provenance.json)|Original local additions with AI assistance, absent from frozen upstream|Owner permits this public portfolio; no additional general reuse/modification/commercial grant|Included source references; two receive documented citation URL hardening|
|Pure extracts, audit scripts, tests, documents, SVG diagrams|Current local portfolio work|Default copyright; no blanket license|Same publication authorization; no general reuse grant|Included; code security patches separated from original run claims|
|Three report crops and social preview|Locally generated report, exact source/crop hashes|Original local rendering; no raw posts or third-party UI/logo|Publication authorized within reviewed portfolio; no new general asset license|Included after pixel and metadata review|
|Font glyph rendering / font files|Local Source Han SIL OFL notice|OFL 1.1|Font redistribution has conditions; rendered document use permitted|No font file or subset distributed|
|Chart.js and other renderer vendors|[Upstream vendor tree](https://github.com/JxKim/sentiment_analysis_platform/tree/master/engines/ReportEngine/renderers/libs)|MIT header for Chart.js; remaining vendor grants not fully cleared|Individual terms apply; no blanket clearance|All vendor binaries/source excluded|
|Course images, logos, original frontend assets|Upstream material|No explicit reuse grant found|Not established|Excluded|
|Python/Node packages and model weights|Package-specific authors/providers|Mixed dependency metadata; model terms not fully reviewed|Individual terms apply|No environments, dependency installations, caches or weights distributed; metadata inventory only|
|Social/web content|Original creators and platforms|No bulk dataset publication grant assumed|No bulk redistribution claimed|Aggregate metrics, minimized paraphrases labeled as examples; no raw comment set or identifiers|

No third-party copyright notice was deleted from a redistributed third-party source file: those files are not redistributed at all. See [NOTICE](NOTICE.md), [third-party inventory](THIRD_PARTY_NOTICES.md) and [excluded content](PUBLIC_EXCLUDED_FILES.md). Re-audit if adding any excluded source or asset. This is a scoped engineering publication review, not a legal opinion covering the private full platform.
