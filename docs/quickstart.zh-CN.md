# 公开Portfolio与完整本地系统

## 公开Portfolio快速开始

使用Python 3.11+和Node 22+，运行离线测试、查看示例输出并预览静态案例。无需API Key、MySQL、爬虫登录或安装npm依赖。

```sh
python -B -m unittest discover -s tests -v
python -B scripts/check_release.py
npm run build
npm run dev
```

打开 `<preview-origin>`/docs/assets/demo/public-demo.html；`<preview-origin>`指本机回环地址、端口8765。`npm run build`构建案例摘要，`npm run dev`提供静态预览，二者都不会启动Vue工作台、发起检索或运行五引擎。

[示例输入](../examples/example_query.json)、[Insight示例](../examples/example_insight_output.json)和[报告示例](../examples/example_report_output.json)用于解释数据契约，均有示例标注。离线测试执行纯验证逻辑。

PowerShell可使用[环境检查](../scripts/doctor.ps1)、[启动](../scripts/start.ps1)、[停止](../scripts/stop.ps1)和[测试](../scripts/test.ps1)脚本。启动脚本支持`-Node`，检查和测试脚本支持`-Python`、`-Node`指定运行环境。[Docker示例](../docker-compose.example.yml)同样只提供只读文档预览。

## 完整本地系统

完整且已验证的本地系统依赖未在此重新分发的上游组件。先取得[上游仓库](https://github.com/JxKim/sentiment_analysis_platform)的适当使用权限，并按对应版本说明安装；这里的integration代码用于展示新增集成逻辑，不是完整安装器。

|部分|已验证本地环境|
|---|---|
|API与研究引擎|Python 3.11、FastAPI、引擎依赖；爬虫使用独立环境|
|工作台|Vue 3 / TypeScript前端及Node构建工具|
|用户反馈存储|MySQL 8、上游数据表结构和获准采集的数据|
|模型与检索|DeepSeek模型配置、Tavily检索配置|
|报告导出|WeasyPrint及所需渲染依赖|

已验证环境使用前端5173端口、API 5000端口，MySQL仅映射到本机回环地址。实际依赖以取得的上游版本为准。

### 配置概览

空白[.env.example](../.env.example)列出了配置名，公开预览不会读取它。

- DB_HOST、DB_PORT、DB_USER、DB_PASSWORD、DB_NAME：本地数据库连接。
- INSIGHT_ENGINE、MEDIA_ENGINE、QUERY_ENGINE、FORUM_HOST、REPORT_ENGINE、KEYWORD_OPTIMIZER：每组包含API_KEY、BASE_URL、MODEL_NAME。
- TAVILY_API_KEY：真实外部检索。
- QUALITY_PIPELINE_V2、LIVE_CALLS_ENABLED：按完整系统配置核对流程与真实调用开关。

凭证、浏览器状态与原始数据保留在公开仓库之外。重新研究可能产生外部API费用，公开CI不会执行这类调用。[架构](architecture.md) · [API](api.md) · [隐私](privacy.md) · [许可范围](LEGAL_AND_LICENSE.md)。
