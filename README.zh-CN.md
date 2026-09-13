# 尚舆｜多Agent AI产品舆情与用户反馈洞察平台

通过多Agent研究、网络检索与事实核验，将真实用户反馈转化为有证据支撑的产品洞察。

[English](README.md) · [真实案例](docs/case-study-doubao.md) · [系统架构](docs/architecture.md)

**真实案例：豆包AI助手**  
**24篇真实帖子 · 83条真实评论**  
DeepSeek + Tavily + MySQL  
Insight / Media / Query / Forum / Report

![豆包真实报告：数据范围与研究时间](docs/assets/screenshots/research-scope.png)

## 项目做什么

- **真实数据：**围绕24篇帖子、83条评论，整理可追溯的用户反馈案例。
- **Agent协作：**Insight + Media → Query → Forum → Report，连接用户声音、媒体信息、事实核验和自动报告。
- **证据驱动迭代：**通过噪声过滤、评论整合、来源分级与主张核验，让产品判断有据可查。

## 为什么复现并改进这个项目

AI产品的用户反馈分散在帖子、评论与媒体信息中。LLM容易漏掉细节，也容易把少数观点概括成普遍结论。我复现尚舆，希望把数据、检索与证据链连接起来，让研究过程和判断依据都能被检查。

## 工作流程

![多Agent架构与证据流转](docs/assets/architecture.svg)

**Insight**读取MySQL用户反馈，**Media**通过Tavily检索外部信息，两者并行执行。**Query**核验上游产品主张，**Forum**整理相互支持的发现与证据缺口，**Report**生成HTML / Markdown / PDF报告。SSE将执行进度持续传递到前端。

## 真实案例：豆包AI助手

**数据范围：24篇帖子 / 83条评论。**围绕学习与办公场景，识别用户在做什么、遇到什么痛点、提出哪些需求，以及值得验证的产品机会。案例覆盖表格报表、科研绘图与编程反馈，展示从证据到下一步行动的推导。[阅读案例](docs/case-study-doubao.md)。

## V1 → V2

|V1问题|V2改进|
|---|---|
|检索混入噪声|相关性过滤|
|评论利用不足|评论关联与整合|
|Media上下文为空|检索链路修复与非空输出检查|
|来源可信度不足|来源分级|
|LLM过度概括|证据卡与限定范围的主张|

[Bad Case复盘](docs/bad-cases.md) · [证据质量与评测](docs/evaluation.md)

## 产品价值

尚舆可支持：

- 用户声音（VOC）初筛与反馈聚类
- 产品问题发现与功能假设生成
- 内容及运营规划、有证据支撑的产品研究

## 我的贡献

环境复现、DeepSeek与Tavily接入、通过现有采集集成完成真实数据采集、MySQL验证、流程与导出调试、证据质量迭代和Bad Case分析。开发与复核过程使用了AI辅助。

上游架构单独保留归属，包括原始五角色设计、UI、提示词与爬虫集成。[贡献边界](NOTICE.md)。

## 技术栈

Python · FastAPI · Vue 3 · MySQL · DeepSeek · Tavily · SSE · WeasyPrint

## 演示

本地真实运行已生成 **HTML / Markdown / PDF**。下图是最终报告的真实裁剪，未修改文字与数字。

![豆包最终报告输出](docs/assets/screenshots/report-cover.png)

[报告截图来源](docs/assets/screenshots/README.md) · [离线案例摘要](docs/assets/demo/public-demo.html)

## 代码导读

- [流程协调器](integration/app/services/evidence_pipeline.py)：角色依赖、阶段状态与SSE。
- [反馈适配器](integration/engines/InsightEngine/tools/product_feedback.py)：SQL关联与样本筛选。
- [来源分级](portfolio_code/source_quality.py)与[证据契约](portfolio_code/evidence_contract.py)：可检查的规则。
- [报告组装](integration/engines/ReportEngine/evidence_report.py)：结构化发现与来源卡。

[全部引擎入口](docs/code-walkthrough.md)

## 公开Portfolio快速开始

公开仓库是本地已验证系统中可按许可公开的Portfolio子集。

使用Python 3.11+和Node 22+，运行离线测试并构建示例摘要：

```sh
python -B -m unittest discover -s tests -v
npm run build
npm run dev
```

`npm run dev`在本机回环地址的8765端口启动**静态Portfolio预览**，不会启动五引擎应用或执行搜索；无需API Key或数据库。[详细快速开始](docs/quickstart.zh-CN.md) · [离线示例](examples/example_query.json)。

## 完整本地系统

完整且已在本地验证的系统依赖上游组件，这些组件因许可证限制未在此重新分发。

请先查看[上游仓库](https://github.com/JxKim/sentiment_analysis_platform)，再阅读[环境要求与配置概览](docs/quickstart.zh-CN.md#完整本地系统)及[API说明](docs/api.md)。完整系统使用Vue工作台、FastAPI、MySQL，并单独配置DeepSeek与Tavily服务。

## 局限与负责任使用

本案例为单平台便利小样本，输出用于提出需要人工复核的研究假设。详细指标来自同批开发样本和助手辅助标注，不是独立基准测试，详见[评测说明](docs/evaluation.md)。尚未证明持续监测、生产可用性或业务收益。

仅用于研究与学习，遵守平台条款及爬虫许可，控制请求频率，不绕过验证码或访问控制。公开内容排除了原始用户数据与凭证；CI离线执行，预览面向本地开发。[隐私](docs/privacy.md) · [安全](docs/security.md)。

## 许可证与归属

[上游项目](https://github.com/JxKim/sentiment_analysis_platform)保留原始架构与应用归属。受限组件已排除；原创新增内容采用默认版权，不统一授予MIT/Apache或商业再使用许可。[LICENSE](LICENSE) · [NOTICE](NOTICE.md) · [第三方声明](THIRD_PARTY_NOTICES.md) · [许可范围](docs/LEGAL_AND_LICENSE.md)。
