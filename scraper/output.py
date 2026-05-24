"""输出模块 - 增量合并采集结果到 data/articles.json"""

import json
import os
import re
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


def clean_old_year_articles(articles):
    """移除标题年份早于发布日期的旧文章（如"2024 Report"被误标为今天）"""
    current_year = datetime.now().year
    cleaned = []
    removed = 0
    for a in articles:
        title = a.get("title", "")
        date = a.get("date", "")
        years_in_title = [int(y) for y in re.findall(r"\b(20\d{2})\b", title)]
        if years_in_title:
            max_year = max(years_in_title)
            date_year = int(date[:4]) if date else current_year
            if max_year < date_year:
                removed += 1
                continue
        cleaned.append(a)
    if removed:
        print(f"  清理 {removed} 篇旧年份文章（标题年份与发布日期不符）")
    return cleaned


def write_json(articles):
    """写入合并后的全部文章"""
    path = get_data_path()

    # 清理旧年份文章
    articles = clean_old_year_articles(articles)

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
