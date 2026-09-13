# 尚舆

**尚舆｜多 Agent AI 产品舆情与用户反馈洞察平台**

[English](README.md) · [豆包案例](docs/case-study-doubao.md) · [代码导航](docs/code-walkthrough.md)

基于真实社媒数据、LLM与Web Search的多Agent产品研究平台，用于用户反馈分析、舆情观察、事实核验、Bad Case复盘和产品机会挖掘。

**真实案例：豆包AI助手用户体验、口碑与产品机会分析。24条真实帖子 / 83条评论；2026-09-13重新读取MySQL核对。**

技术栈：Python / FastAPI / Vue3 / MySQL / DeepSeek / Tavily / SSE / WeasyPrint。

![真实V2架构](docs/assets/architecture.svg)

已实跑：真实社媒输入、多角色研究、评论分析、Web检索与限定事实核验、证据卡、Bad Case评测、SSE进度、HTML/Markdown/PDF导出。

![真实研究范围截图](docs/assets/screenshots/research-scope.png)

**发布模式：PORTFOLIO_ONLY。** 部分第三方组件因原始许可条款而排除。本包含本地新增代码参考、离线纯函数、案例和文档，不是完整平台源码。原始数据、登录状态、Logo和授权不明的原始UI资源不公开。

## 项目概览 / 为什么做
多数LLM演示关注生成，本项目关注数据质量、证据质量、来源核验、Bad Case以及如何形成可验证产品假设。舆情观察是探索性用途，不声称已验证全网实时监控。

## 豆包案例 / 真实结果
|Measured private case|Result|
|---|---|
|Fresh database scope|24 posts / 83 comments|
|Primary model input|12 posts / 15 comments|
|Relevant development predictions|17/17; total n=24|
|Core citation coverage|5/5|
|Fact audit|17 supported / 3 partially supported; n=20|
|Product / operations hypotheses|1 / 2|
|Verified exports|HTML / Markdown / 15-page PDF|

17/17是24条开发集内的相关性结果，不是模型准确率；5/5引用覆盖不代表用户说法客观真实。实际帖子集中在9月1日至12日，不代表连续覆盖90天。V1/V2问题措辞不同，不能写成严格A/B提升。

## 架构 / 多Agent流程
Vue3→FastAPI/SearchService→Insight和Media并行→Query读取上游后核验→Forum综合→Report。Query有依赖顺序，不为展示并行而先写百科。[架构](docs/architecture.md) · [工作流](docs/assets/workflow.svg)。

## Agent职责
Insight回答用户样本说什么；Media保留外部说法；Query核验产品事实；Forum处理呼应、冲突和未知；Report组织证据及假设。[输入、工具和失败模式](docs/agent-design.md)。

## 真实数据链 / 证据感知分析
已授权采集→MySQL→主帖评论关联→相关性/信息量筛选→实际JSON输入→引文/ID校验→结构化结论。数据库有记录不等于模型读过。保留原话、样本归纳、官方事实和Inference的区别。[数据链](docs/data-pipeline.md)。

## V1到V2 / Bad Case与迭代
发现无关帖子、评论未充分使用、Media空上下文、弱来源和过度概括；改为相关性过滤、评论关联、来源等级、事实核验、证据卡和Bad Case评测。失败和纠偏有记录，最终仍含助手语义复核。[真实复盘](docs/bad-cases.md)。

## 我的工作
Windows环境复现、DeepSeek/Tavily集成、真实采集结果核对、API与导出调试、V2证据链改造、评测、案例和求职材料，过程使用AI编码辅助。上游提供原始架构、五角色、UI、提示词与爬虫集成，不能声称全部从零自研。[归属声明](NOTICE.md)。

## 产品经理视角
用于VOC整理、用户研究问题、功能线索、产品机会和内容运营假设；风险/情绪监测仍是探索性应用，不编造用户占比、增长收益或因果效果。

## 大模型应用视角
展示角色编排、工具调用、结构化输出、状态保存、SSE、外部搜索、事实核验及报告生成。多Agent有协调与费用代价，未证明一定优于单模型。

## 评测
[评测方法](docs/evaluation.md) · [真实汇总](evaluation/sample_results.json) · [私有证据哈希](evaluation/provenance.json)。公开fixture明确标为Example data，不能替代真实样本评估。

## Demo
以下为真实生成报告裁剪图，不是假UI或运行中Agent截图。[图片来源](docs/assets/screenshots/README.md)。

![报告封面](docs/assets/screenshots/report-cover.png)
![报告局限性](docs/assets/screenshots/report-limitations.png)

[静态匿名汇总页](docs/assets/demo/public-demo.html)仅用于展示；原始完整报告与83条评论不公开。

## 技术栈 / 目录 / 代码导航
原私有平台使用Python3.11、FastAPI、Vue3/TypeScript/Pinia/Element Plus/Vite、MySQL8、DeepSeek、Tavily、WeasyPrint。公开包离线检查仅用Python标准库，Node仅构建文档。integration为本地新增参考源码，portfolio_code为可执行纯函数，docs/evaluation/examples/scripts分别保存文档、评测、最小示例和检查脚本。[十个入口](docs/code-walkthrough.md)。

## 快速开始
Python3.11+、Node22+，在本包目录运行：

```powershell
python -m unittest discover -s tests -v
npm run build
npm run dev
```

打开 `<preview-origin>`/docs/assets/demo/public-demo.html 。这是静态案例摘要，不是未附带的Vue平台；无需Key、数据库或npm依赖。[详细中文步骤](docs/quickstart.zh-CN.md)。

## 配置 / API
.env.example仅列空变量，测试不读取私密配置。[API说明](docs/api.md)描述原私有平台；compose只启动文档服务器。完整运行须另行取得原项目权限与依赖，本包不提供虚构的git clone地址。

## 局限性
单平台小样本、外部API依赖、来源质量不一、日期缺失、未读图像视频；LLM输出需复核。不针对生产级大规模爬虫。独立盲测、跨产品泛化和商业收益尚未测量。

## 负责任使用
仅用于研究与学习，遵守平台条款和MediaCrawler自身许可，控制请求频率，不绕过验证码或访问控制，不采集私有信息，不进行未授权商业抓取。不提交Key、Cookie、认证数据、私人画像或原始评论集；公开示例脱敏并改写。[隐私](docs/privacy.md) · [安全](docs/security.md)。CI不调用付费接口或真实数据库。首次发布提交的两项GitHub Actions均已通过，详见[发布记录](PUBLISHED_RELEASE_RECORD.md)。预览及私有平台均面向本地开发，未证明具备适合公网生产的认证、限流与RBAC。

## 许可证与归属
不统一添加MIT/Apache许可。原平台完整再分发未获明确授权，受限第三方组件已排除，采用展示模式并保留[上游归属](https://github.com/JxKim/sentiment_analysis_platform)。[最终许可审计](FINAL_LICENSE_AUDIT.md) · [第三方声明](THIRD_PARTY_NOTICES.md) · [manifest](publish_manifest.json)。原创新增内容采用默认版权，不额外授予开源再使用许可。

[面试提纲](docs/interview-notes.zh-CN.md) · [三类岗位简历表述](docs/resume-bullets.md)。
