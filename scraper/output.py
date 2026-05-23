"""输出模块 - 增量合并采集结果到 data/articles.json"""

import json
import os
from datetime import datetime


def get_data_path():
    scraper_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(scraper_dir)
    data_dir = os.path.join(project_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "articles.json")


def load_existing():
    """读取已有的文章数据"""
    path = get_data_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("articles", [])
        except (json.JSONDecodeError, KeyError):
            return []
    return []


def merge_articles(existing, new_articles):
    """合并新旧文章，按URL去重，新数据覆盖旧数据"""
    # 用 dict 按 url 去重，新数据优先（保留最新采集的字段值）
    merged = {}
    for a in existing:
        url = a.get("url", "").strip().lower().rstrip("/")
        if url:
            merged[url] = a
    for a in new_articles:
        url = a.get("url", "").strip().lower().rstrip("/")
        if url:
            merged[url] = a  # 新数据覆盖旧数据
    result = list(merged.values())
    result.sort(key=lambda x: x.get("date", ""), reverse=True)
    return result


def write_json(articles):
    """写入合并后的全部文章"""
    path = get_data_path()

    # 统计本月/本周
    today = datetime.now().strftime("%Y-%m-%d")
    this_month = datetime.now().strftime("%Y-%m")

    monthly_count = sum(1 for a in articles if a.get("date", "").startswith(this_month))
    today_count = sum(1 for a in articles if a.get("date", "") == today)

    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "total_articles": len(articles),
        "today_count": today_count,
        "monthly_count": monthly_count,
        "articles": articles,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return path
