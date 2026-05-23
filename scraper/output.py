"""输出模块 - 将采集结果写入 data/articles.json"""

import json
import os
from datetime import datetime


def write_json(articles, data_dir=None):
    """将文章列表写入JSON文件"""
    if data_dir is None:
        # 自动定位到项目根目录的 data/ 目录
        scraper_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(scraper_dir)
        data_dir = os.path.join(project_dir, "data")

    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "articles.json")

    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "total_articles": len(articles),
        "status": {
            "apec_org": "active",  # 将由main.py更新
            "bing_news": "active",
            "google_news": "active",
        },
        "articles": articles,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return output_path
