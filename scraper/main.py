"""APEC 动态追踪 - 主爬虫入口
GitHub Actions 每天调用此脚本，采集 → 过滤 → 输出JSON
"""

import os
import sys
import time
from datetime import datetime

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.sources import apec_org, bing_news, google_news
from scraper.filters import apply as apply_filters
from scraper.output import write_json


def main():
    print(f"[{datetime.now()}] APEC动态追踪采集开始...")

    all_articles = []

    # 1. APEC 官网（RSS + HTML）
    print("  [1/3] 采集 APEC 官网...")
    try:
        apec_results = apec_org.fetch_news()
        print(f"        获取 {len(apec_results)} 条")
        all_articles.extend(apec_results)
        time.sleep(2)
    except Exception as e:
        print(f"        APEC官网采集出错: {e}")

    # 2. Google News RSS（无需API Key，总是可用）
    print("  [2/3] 采集 Google News...")
    try:
        google_results = google_news.search_all_keywords()
        print(f"        获取 {len(google_results)} 条")
        all_articles.extend(google_results)
        time.sleep(2)
    except Exception as e:
        print(f"        Google News采集出错: {e}")

    # 3. Bing News API（仅在配置了API Key时使用）
    print("  [3/3] 采集 Bing News...")
    try:
        bing_results = bing_news.search_all_keywords()
        print(f"        获取 {len(bing_results)} 条")
        all_articles.extend(bing_results)
    except Exception as e:
        print(f"        Bing News采集出错: {e}")

    # 过滤：去重 → 域名白名单 → 关键词匹配
    print(f"\n  采集完成，共 {len(all_articles)} 条（去重前）")
    filtered = apply_filters(all_articles)
    print(f"  过滤后剩余 {len(filtered)} 条")

    # 按日期排序，最新的在前
    filtered.sort(key=lambda x: x.get("date", ""), reverse=True)

    # 写入JSON
    output_path = write_json(filtered)
    print(f"  已写入: {output_path}")
    print(f"[{datetime.now()}] 采集完成！共收录 {len(filtered)} 条APEC动态")


if __name__ == "__main__":
    main()
