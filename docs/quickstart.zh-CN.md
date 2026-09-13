# 快速开始：展示包与完整平台分开

本包为PORTFOLIO_ONLY，使用Python 3.11+与Node 22+。不需要Key、登录、数据库或爬虫。

```powershell
python -m unittest discover -s tests -v
python scripts/check_release.py
npm run build
npm run dev
```

打开 `<preview-origin>`/docs/assets/demo/public-demo.html ，展示真实汇总指标与明确标注的案例内容。它是静态案例摘要，不是重新调用模型的完整工作台。build只构建展示文档，不冒充Vue构建；不需要npm install。脚本支持显式-Python参数。

完整平台源码、爬虫和原始数据因许可/隐私原因不附带。须单独取得原项目的适当使用权限，再按其依赖和配置说明部署。原私有工作区已有真实Vue构建，可单独验证，但不能把未附带前端的本包描述成一条命令运行完整五引擎。docker-compose.example.yml只启动只读文档服务器。

不自动复制真实.env，不开放公网，不新增采集。重新研究可能产生外部API费用；本包测试完全离线。公开仓库已创建，可从[GitHub仓库](https://github.com/gretchenrohrscheib426-droid/shangyu-ai-product-intelligence)下载或克隆已审核的Portfolio内容。

`<preview-origin>`表示本机回环地址、端口8765；start.ps1通过-Node指定Node程序，doctor/test通过-Python和-Node指定解释器。
