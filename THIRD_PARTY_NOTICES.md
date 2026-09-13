# Third-party inventory and treatment

This portfolio does not redistribute dependency installations or upstream code. License findings describe inspected local material; unknown is not permission. See [detailed review](docs/LEGAL_AND_LICENSE.md).

|Component|Source|Observed license|Redistribution / modification / commercial use|Treatment|
|---|---|---|---|---|
|Upstream platform and SentinelSpider wrapper|[JxKim](https://github.com/JxKim/sentiment_analysis_platform)|No root license found in audited snapshot|Not established / not established / not established|Full code and modified upstream files excluded|
|MediaCrawler|[NanmiCoder](https://github.com/NanmiCoder/MediaCrawler)|NON-COMMERCIAL LEARNING LICENSE 1.1|Conditional learning copying/modification; broad public sublicense not established; commercial use requires written consent|Entire component and its login/session assets excluded|
|Source Han font|[Adobe](https://github.com/adobe-fonts/source-han-serif)|Local SIL OFL 1.1 notice|Conditional redistribution/modification with notices and reserved-name constraints; document use allowed|Font binaries and subset files excluded|
|Chart.js|[Chart.js](https://github.com/chartjs/Chart.js)|Local header says MIT|Subject to original terms and notices|Vendor file excluded|
|jsPDF / html2canvas / Sankey / MathJax|[local vendor inventory source](https://github.com/JxKim/sentiment_analysis_platform/tree/master/engines/ReportEngine/renderers/libs)|Individual grants not fully re-verified in this release audit|Not treated as cleared|All bundled vendor files excluded|
|Course images, logos, favicon, UI screenshots|Upstream course and frontend assets|No explicit grant located|Not established|Excluded; use original locally generated report crops|
|Vue, FastAPI, Python/Node dependencies|Package metadata; see inventory|Mixed package-specific metadata|Individual terms apply; not sublicensed here|No node_modules, wheels, environment or full dependency distribution|
|Model weights and sentiment tools|Upstream tools and model providers|Multiple/not fully reviewed|Not established for this package|Excluded|
|Public webpage/social content|Original authors and platforms|No blanket dataset redistribution grant|No bulk redistribution assumed|Aggregate counts, paraphrased minimal examples, no raw user profiles or original IDs|

`docs/dependency-inventory.json` records available package license metadata; it is not a full transitive legal clearance. No dependency code is bundled. Retaining copyright notices alone would not cure missing redistribution permission.
