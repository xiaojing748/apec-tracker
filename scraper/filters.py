"""Article filters - deduplicate, whitelist, keyword match + metadata enhancement"""

from urllib.parse import urlparse
from scraper import config


def deduplicate(articles):
    seen = set()
    unique = []
    for a in articles:
        url = a.get("url", "").strip().lower().rstrip("/")
        if url and url not in seen:
            seen.add(url)
            unique.append(a)
    return unique


def filter_by_domain(articles):
    result = []
    for a in articles:
        domain = _extract_domain(a.get("url", ""))
        if not domain:
            continue
        if domain in config.BLOCKED_DOMAINS or any(
            domain.endswith(d) for d in config.BLOCKED_DOMAINS
        ):
            continue
        if domain in config.ALLOWED_DOMAINS or any(
            domain.endswith(d) for d in config.ALLOWED_DOMAINS
        ):
            result.append(a)
    return result


def filter_by_keywords(articles):
    CORE_KW = [
        "cbpr", "cross-border privacy", "cross border data",
        "data privacy", "data protection", "data flow", "跨境数据", "数据跨境",
        "ai governance", "ai safety", "artificial intelligence", "ai standard",
        "ai adoption", "人工智能", "AI治理",
        "telwg", "telecommunications", "telecom", "desg", "ecsg",
        "data privacy subgroup", "telmin", "ciip", "critical information",
        "电信工作组", "电信安全", "通信安全", "数字经济转向组",
        "digital economy", "digital trade", "digital transformation",
        "e-commerce", "fintech", "paperless trade", "数字经济", "数字贸易", "跨境电商",
        "connectivity", "infrastructure", "互联互通",
        "supply chain", "供应链", "ict supply",
        "cybersecurity", "cyber security", "cybercrime",
        "网络安全", "网络犯罪",
        "trade war", "tariff", "protectionism", "ftaap",
        "trade facilitation", "multilateral", "trade minister",
        "economic outlook", "regional trends",
        "关税", "贸易便利化", "多边", "贸易部长", "经济合作",
        "APEC",
    ]
    result = []
    for a in articles:
        text = (a.get("title", "") + " " + a.get("summary", "")).lower()
        for kw in CORE_KW:
            if kw.lower() in text:
                result.append(a)
                break
    return result


def enhance_metadata(articles):
    """Add extended metadata (doc_type, apec_bodies, geo_focus, policy_tags, relevance)"""
    return [config.enhance_article(a) for a in articles]


def apply(articles):
    url_valid = [a for a in articles if _is_valid_url(a.get("url", ""))]
    unique = deduplicate(url_valid)
    domain_filtered = filter_by_domain(unique)
    keyword_filtered = filter_by_keywords(domain_filtered)
    enhanced = enhance_metadata(keyword_filtered)
    return enhanced


def _extract_domain(url):
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


_SEARCH_DOMAINS = {"bing.com", "google.com", "search.yahoo.com", "baidu.com"}


def _is_valid_url(url):
    if not url:
        return False
    lower = url.lower()
    if "/search" in lower:
        return False
    domain = _extract_domain(url)
    if domain in _SEARCH_DOMAINS:
        return False
    return True
