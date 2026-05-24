"""Google News RSS 采集器（不依赖API Key）"""

import re
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

import feedparser
import requests

from scraper import config

# 搜索引擎/搜索页面域名（拒绝这些URL）
_SEARCH_DOMAINS = {
    "bing.com", "www.bing.com", "google.com", "www.google.com",
    "search.yahoo.com", "baidu.com", "www.baidu.com", "news.google.com",
}

# 不可靠的域名模式
_BAD_URL_PATTERNS = [
    r"/search\?q=", r"/search\?", r"bing\.com/search",
]


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
            if " - " in title:
                title, source_name = title.rsplit(" - ", 1)
            else:
                source_name = "Google News"

            link = _extract_real_url(entry)
            if not link:
                continue

            summary = entry.get("summary", entry.get("description", ""))
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if not title:
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
                "summary": _clean_summary(summary)[:300] if summary else "",
                "categories": categories,
            })
    except Exception:
        pass

    return articles


def _extract_real_url(entry):
    """从Google News RSS条目中提取真实文章URL"""
    # feedparser会把真实URL放在link字段，但也可能包装成Google重定向
    link = entry.get("link", "").strip()

    # 如果是Google News重定向URL，尝试从参数中提取真实URL
    if "news.google.com/rss/articles" in link:
        parsed = urlparse(link)
        qs = parse_qs(parsed.query)
        real_url = qs.get("url", [None])[0]
        if real_url:
            link = real_url

    # 拒绝搜索引擎URL
    if not link:
        return ""
    domain = urlparse(link).netloc.lower().replace("www.", "")
    if domain in _SEARCH_DOMAINS:
        return ""
    for pattern in _BAD_URL_PATTERNS:
        if re.search(pattern, link):
            return ""

    return link


def _clean_summary(text):
    """清理摘要中的HTML标签"""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


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
