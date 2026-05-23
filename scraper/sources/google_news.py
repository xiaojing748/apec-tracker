"""Google News RSS 采集器（不依赖API Key）"""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import feedparser
import requests

from .. import config


def search_all_keywords():
    """对所有关键词组合搜索 Google News RSS"""
    articles = []
    all_keywords = _collect_all_keywords()

    for kw_group, keywords in all_keywords.items():
        for kw in keywords[:5]:  # 每组取前5个
            results = _search_rss(kw)
            articles.extend(results)

    return articles


def _search_rss(query):
    """通过 Google News RSS 搜索"""
    articles = []
    rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"

    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            # Google News RSS 的标题格式: "Title - Source"
            if " - " in title:
                title, source_name = title.rsplit(" - ", 1)
            else:
                source_name = "Google News"

            link = entry.get("link", "").strip()
            # 还原原始URL（Google News RSS会包装）
            summary = entry.get("summary", entry.get("description", ""))
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if not title or not link:
                continue
            if not _is_allowed_domain(link):
                continue

            categories = config.classify_article(title, summary or "")
            articles.append({
                "title": title,
                "url": link,
                "source": source_name.strip(),
                "source_type": "权威媒体",
                "date": pub_date.strftime("%Y-%m-%d") if pub_date else datetime.now().strftime("%Y-%m-%d"),
                "summary": summary[:300] if summary else "",
                "categories": categories,
            })
    except Exception:
        pass

    return articles


def _collect_all_keywords():
    """收集所有关键词，加入2026中国年关键词"""
    all_kw = dict(config.KEYWORDS)
    all_kw["2026中国年"] = config.CHINA_2026_KEYWORDS
    return all_kw


def _is_allowed_domain(url):
    """检查URL域名是否在白名单"""
    domain = urlparse(url).netloc.lower().replace("www.", "")
    return domain in config.ALLOWED_DOMAINS or any(
        domain.endswith(d) for d in config.ALLOWED_DOMAINS
    )
