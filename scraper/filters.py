"""文章过滤器 - 去重、白名单、关键词匹配"""

from urllib.parse import urlparse

from . import config


def deduplicate(articles):
    """基于URL去重，保留每个URL的第一条"""
    seen = set()
    unique = []
    for a in articles:
        url = a.get("url", "").strip().lower().rstrip("/")
        if url and url not in seen:
            seen.add(url)
            unique.append(a)
    return unique


def filter_by_domain(articles):
    """只保留白名单域名的文章，排除黑名单域名"""
    result = []
    for a in articles:
        domain = _extract_domain(a.get("url", ""))
        if not domain:
            continue

        # 先检查黑名单
        if domain in config.BLOCKED_DOMAINS or any(
            domain.endswith(d) for d in config.BLOCKED_DOMAINS
        ):
            continue

        # 再检查白名单
        if domain in config.ALLOWED_DOMAINS or any(
            domain.endswith(d) for d in config.ALLOWED_DOMAINS
        ):
            result.append(a)

    return result


def filter_by_keywords(articles):
    """只保留标题或摘要包含至少一个关键词的文章"""
    all_words = []
    for words in config.KEYWORDS.values():
        all_words.extend(words)
    all_words.extend(config.CHINA_2026_KEYWORDS)

    result = []
    for a in articles:
        text = (a.get("title", "") + " " + a.get("summary", "")).lower()
        for w in all_words:
            if w.lower() in text:
                result.append(a)
                break
    return result


def apply(articles):
    """应用全部过滤：去重 → 域名过滤 → 关键词过滤"""
    unique = deduplicate(articles)
    domain_filtered = filter_by_domain(unique)
    keyword_filtered = filter_by_keywords(domain_filtered)
    return keyword_filtered


def _extract_domain(url):
    """从URL提取域名"""
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""
