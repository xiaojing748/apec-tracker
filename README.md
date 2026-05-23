# APEC 2026 网络安全与数据治理 · 动态追踪看板

自动采集 APEC 网络安全、数据跨境流动、隐私保护等议题的最新动态，生成网页看板。每天北京时间 08:00 自动更新。

**看板地址**：`https://<用户名>.github.io/apec-tracker/`

## 追踪议题

- **数据跨境**：CBPR 2.0、跨境数据流动规则、数据隐私框架
- **AI治理**：AI安全治理、人工智能标准、AI伦理
- **互联互通**：数字基础设施、数字经济路线图、互联互通蓝图
- **地缘政治**：供应链韧性、贸易便利化、经济合作

## 数据来源

- APEC 官网 (apec.org) — RSS + 网页解析
- Google News RSS — 关键词搜索
- Bing News API — 关键词搜索（可选，需配置API Key）

所有信息保留原始链接，仅收录可信域名白名单来源。

## 项目结构

```
apec-tracker/
├── .github/workflows/update.yml    # GitHub Actions 定时运行
├── scraper/                        # Python 爬虫
│   ├── config.py                   # 关键词、域名白名单
│   ├── main.py                     # 主入口
│   ├── sources/                    # 数据源爬虫
│   ├── filters.py                  # 去重过滤
│   └── output.py                   # 输出JSON
├── web/                            # 网页看板
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/articles.json              # 采集数据（自动生成）
└── README.md
```

## 部署步骤

1. 将本项目推送到 GitHub 仓库（仓库名：`apec-tracker`，设为 Public）
2. 进入 Settings → Pages → Source 选 "GitHub Actions"
3. 进入 Actions 页面，手动触发一次 "Update APEC News"
4. 等待约2分钟，访问 `https://<用户名>.github.io/apec-tracker/`

## 可选：配置 Bing News API

在 `scraper/config.py` 中设置 `BING_API_KEY` 可启用 Bing News 源。
免费获取：[Azure Bing Search API](https://portal.azure.com)（1000次/月免费额度）
