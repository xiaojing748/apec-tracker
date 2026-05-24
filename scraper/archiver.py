"""文章存档模块 - 下载全文并按日期归档为markdown + JSON索引"""
import json
import os
import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from scraper import config

ARCHIVE_DIR = None
INDEX_FILE = None


def _init_paths():
    global ARCHIVE_DIR, INDEX_FILE
    scraper_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(scraper_dir)
    # 存档放在 docs/archive/ 下，兼容 GitHub Pages 从 docs/ 或根目录部署
    ARCHIVE_DIR = os.path.join(project_dir, "docs", "archive", "docs")
    INDEX_FILE = os.path.join(project_dir, "docs", "archive", "index.json")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)


def archive_all(articles, force=False):
    """归档所有文章：下载全文 → 保存markdown → 更新索引"""
    _init_paths()

    index_data = _load_index()
    existing_ids = {e["url"] for e in index_data.get("entries", [])}
    new_entries = []
    total = len(articles)
    success = 0

    for i, article in enumerate(articles):
        url = article.get("url", "")
        if not url or (url in existing_ids and not force):
            continue

        print(f"  [{i+1}/{total}] {article.get('title', '')[:60]}...")

        try:
            entry = _download_and_save(article)
            if entry:
                new_entries.append(entry)
                existing_ids.add(url)
                success += 1
            time.sleep(1.5)  # 礼貌间隔
        except Exception as e:
            print(f"        失败: {e}")

    # 合并索引
    all_entries = index_data.get("entries", []) + new_entries
    _update_index(all_entries)

    print(f"  归档完成: {success}/{total} 篇新增")
    return success


def _download_and_save(article):
    """下载单篇文章全文并保存为markdown"""
    url = article.get("url", "")
    title = article.get("title", "无标题")
    date_str = article.get("date", datetime.now().strftime("%Y-%m-%d"))
    source = article.get("source", "")
    summary = article.get("summary", "")
    categories = article.get("categories", [])

    # 下载全文
    full_text = _fetch_article_text(url)
    if not full_text:
        full_text = f"*无法获取全文，请访问原文：{url}*"

    # 生成文件名和路径
    slug = _slugify(title, 60)
    filename = f"{date_str}-{slug}.md"

    # 按日期建立目录: archive/docs/YYYY/MM/DD/
    date_dir = os.path.join(ARCHIVE_DIR, date_str[:4], date_str[5:7], date_str[8:10])
    os.makedirs(date_dir, exist_ok=True)
    filepath = os.path.join(date_dir, filename)

    # 写markdown文件
    md_content = f"""---
title: "{title}"
date: {date_str}
source: "{source}"
categories: {json.dumps(categories, ensure_ascii=False)}
url: "{url}"
---

# {title}

**来源:** {source}
**日期:** {date_str}
**分类:** {", ".join(categories)}
**原文链接:** [{url}]({url})

## 摘要

{summary if summary else "（无摘要）"}

## 全文

{full_text}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 返回索引条目，file路径相对于项目根目录
    scraper_dir = os.path.dirname(os.path.abspath(__file__))
    scraper_dir = os.path.dirname(scraper_dir)  # scraper/ 的父目录 = 项目根
    rel_path = os.path.relpath(filepath, scraper_dir).replace("\\", "/")

    return {
        "title": title,
        "date": date_str,
        "source": source,
        "categories": categories,
        "url": url,
        "file": rel_path,
        "has_fulltext": full_text and "无法获取全文" not in full_text,
    }


def _fetch_article_text(url):
    """尝试下载网页正文"""
    try:
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT, headers={
            "User-Agent": "Mozilla/5.0 (compatible; APECTracker/1.0)"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # 尝试多种可能的正文选择器
        selectors = [
            "article", ".article-body", ".article-content", ".post-content",
            ".entry-content", ".content-body", "main", ".main-content",
            "#content", ".news-content", ".story-body",
        ]

        paragraphs = []
        for sel in selectors:
            container = soup.select_one(sel)
            if container:
                # 移除脚本和样式
                for tag in container.select("script, style, nav, .nav, .sidebar, .related"):
                    tag.decompose()
                paragraphs = [p.get_text(strip=True) for p in container.find_all("p") if len(p.get_text(strip=True)) > 30]
                if paragraphs:
                    break

        if not paragraphs:
            # 回退：取所有段落
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 50]

        if paragraphs:
            return "\n\n".join(paragraphs[:30])  # 最多30段

        return ""
    except Exception:
        return ""


def _load_index():
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass
    return {"updated": "", "total": 0, "entries": []}


def _update_index(entries):
    """按日期排序保存索引"""
    entries.sort(key=lambda e: e.get("date", ""), reverse=True)
    index_data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(entries),
        "entries": entries,
    }
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)


def _slugify(text, max_len=60):
    """生成文件名slug"""
    slug = re.sub(r"[^\w一-鿿-]", " ", text.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug[:max_len]


def get_recent_archive_dates(days=30):
    """获取最近N天有归档文章的日期列表"""
    _init_paths()
    index_data = _load_index()
    dates = set()
    cutoff = datetime.now().strftime("%Y-%m-%d")
    for e in index_data.get("entries", []):
        d = e.get("date", "")
        if d <= cutoff:
            dates.add(d)
    return sorted(dates, reverse=True)[:days]
