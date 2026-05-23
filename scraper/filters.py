"""文章过滤器 - 去重、白名单、关键词匹配"""

from urllib.parse import urlparse

from scraper import config


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
    """只保留标题或摘要包含核心议题关键词的文章（使用与classify相同的宽松匹配）"""
    # 与config.classify_article共用同一套CORE_MATCH关键词
    CORE_MATCH = [
        "cbpr", "cross-border privacy", "cross border data",
        "data privacy", "data protection", "data flow", "跨境数据", "数据跨境",
        "ai governance", "ai safety", "artificial intelligence", "ai standard",
        "ai adoption", "人工智能", "AI治理",
        "digital economy", "digital trade", "digital transformation",
        "e-commerce", "fintech", "paperless trade", "数字经济", "数字贸易", "跨境电商",
        "connectivity", "infrastructure", "互联互通",
        "supply chain", "供应链", "ict supply",
        "cybersecurity", "cyber security", "cybercrime", "critical infrastructure",
        "网络安全", "网络犯罪", "关键信息基础设施",
        "trade war", "tariff", "protectionism", "ftaap",
        "trade facilitation", "multilateral", "关税", "贸易便利化", "多边",
        "APEC",  # 兜底：标题含APEC的都留下
    ]

    result = []
    for a in articles:
        text = (a.get("title", "") + " " + a.get("summary", "")).lower()
        for kw in CORE_MATCH:
            if kw.lower() in text:
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
