"""APEC 官方网站爬虫 - 从 apec.org 获取新闻和出版物"""

import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import feedparser
import requests
from bs4 import BeautifulSoup

from .. import config


def fetch_news():
    """从 APEC 官网 RSS 和新闻页面获取最新文章"""
    articles = []
    articles.extend(_fetch_rss())
    articles.extend(_fetch_news_page())
    return articles


def _fetch_rss():
    """从 APEC 官网 RSS Feed 获取新闻"""
    articles = []
    rss_urls = [
        "https://www.apec.org/feed",
        "https://www.apec.org/rss.xml",
    ]
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.MAX_DAYS_LOOKBACK)

    for rss_url in rss_urls:
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                pub_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

                if pub_date and pub_date < cutoff:
                    continue

                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = _clean_html(entry.get("summary", entry.get("description", "")))

                if title and link:
                    categories = config.classify_article(title, summary)
                    articles.append({
                        "title": title,
                        "url": link,
                        "source": "APEC官网",
                        "source_type": "官方公报",
                        "date": pub_date.strftime("%Y-%m-%d") if pub_date else datetime.now().strftime("%Y-%m-%d"),
                        "summary": summary[:300] if summary else "",
                        "categories": categories,
                    })
            break  # 如果第一个RSS成功就不试第二个
        except Exception:
            continue

    return articles


def _fetch_news_page():
    """从 APEC 新闻列表页面补充抓取"""
    articles = []
    news_urls = [
        "https://www.apec.org/news",
        "https://www.apec.org/publications",
    ]
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.MAX_DAYS_LOOKBACK)

    for url in news_urls:
        try:
            resp = requests.get(url, timeout=config.REQUEST_TIMEOUT, headers={
                "User-Agent": "Mozilla/5.0 (compatible; APECTracker/1.0; +https://github.com/apec-tracker)"
            })
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            for item in soup.select("article, .news-item, .publication-item, .card, .list-item"):
                title_el = item.select_one("h2, h3, h4, .title, a")
                if not title_el:
                    continue
                link_el = item.select_one("a[href]")
                date_el = item.select_one("time, .date, .published")

                title = title_el.get_text(strip=True)
                link = ""
                if link_el:
                    link = urljoin(url, link_el.get("href", ""))
                pub_date = _parse_date(date_el.get_text(strip=True)) if date_el else datetime.now()

                if not title or not link:
                    continue
                if pub_date < cutoff:
                    continue

                categories = config.classify_article(title)
                articles.append({
                    "title": title,
                    "url": link,
                    "source": "APEC官网",
                    "source_type": "官方公报",
                    "date": pub_date.strftime("%Y-%m-%d"),
                    "summary": "",
                    "categories": categories,
                })
        except Exception:
            continue

    return articles


def _clean_html(html_text):
    """去除HTML标签"""
    if not html_text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", html_text)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def _parse_date(date_str):
    """尝试解析多种日期格式"""
    formats = [
        "%Y-%m-%d", "%d %B %Y", "%B %d, %Y", "%d/%m/%Y",
        "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except (ValueError, AttributeError):
            continue
    return datetime.now()
