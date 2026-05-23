"""
APEC 动态追踪 - 配置文件
集中管理所有关键词、域名白名单、议题分类等
"""

# ============================================================
# 追踪关键词（中英文混合，覆盖四大议题）
# ============================================================
KEYWORDS = {
    "数据跨境": [
        "APEC CBPR 2.0",
        "APEC CBPR",
        "APEC cross-border data flow",
        "APEC cross border data privacy",
        "APEC data privacy framework",
        "APEC data protection",
        "APEC digital trade rules",
        "APEC 跨境数据流动",
        "APEC 数据跨境",
        "APEC 数据隐私",
        "CBPR System",
    ],
    "AI治理": [
        "APEC AI governance",
        "APEC artificial intelligence safety",
        "APEC artificial intelligence regulation",
        "APEC AI ethics",
        "APEC AI standard",
        "APEC responsible AI",
        "APEC 人工智能治理",
        "APEC 人工智能安全",
        "APEC AI framework",
    ],
    "互联互通": [
        "APEC connectivity blueprint",
        "APEC digital connectivity",
        "APEC digital infrastructure",
        "APEC internet economy",
        "APEC digital economy roadmap",
        "APEC 互联互通",
        "APEC 数字经济",
        "APEC AIDER",
        "APEC digital innovation",
    ],
    "地缘政治": [
        "APEC supply chain resilience",
        "APEC supply chain connectivity",
        "APEC trade facilitation",
        "APEC economic cooperation",
        "APEC economic outlook",
        "APEC trade war",
        "APEC tariff",
        "APEC FTAAP",
        "APEC 供应链",
        "APEC 贸易便利化",
    ],
}

# 2026 APEC中国年特别关键词
CHINA_2026_KEYWORDS = [
    "APEC 2026 China",
    "APEC 2026 host year",
    "APEC SOM2 Shanghai",
    "APEC SOM 2 2026",
    "APEC MRT Suzhou",
    "APEC Chengdu digital week",
    "APEC digital minister",
    "APEC SOM3 Dalian",
    "APEC SOM 3 2026",
    "APEC Shenzhen leaders",
    "APEC China 2026 summit",
    "APEC 2026 中国",
    "APEC 上海 SOM",
    "APEC 成都 数字",
    "APEC 大连",
    "APEC 深圳 领导人",
    "APEC 2026 东道主",
]

# ============================================================
# 域名白名单（不在白名单的内容不收录）
# ============================================================
ALLOWED_DOMAINS = [
    # APEC 官方及关联机构
    "apec.org",
    "www.apec.org",
    # 中国政府官方
    "fmprc.gov.cn",
    "www.fmprc.gov.cn",
    "english.www.gov.cn",
    "gov.cn",
    # 权威媒体
    "xinhuanet.com",
    "www.xinhuanet.com",
    "english.news.cn",
    "reuters.com",
    "www.reuters.com",
    "ap.org",
    "apnews.com",
    "www.apnews.com",
    # 国际组织
    "oecd.org",
    "www.oecd.org",
    "wto.org",
    "www.wto.org",
    # 专业智库
    "csis.org",
    "www.csis.org",
    "eastwestcenter.org",
    "www.eastwestcenter.org",
]

# ============================================================
# 排除域名（明确不可信或无关的来源）
# ============================================================
BLOCKED_DOMAINS = [
    "facebook.com",
    "twitter.com",
    "x.com",
    "reddit.com",
    "youtube.com",
    "instagram.com",
    "tiktok.com",
    "linkedin.com",
    "wikipedia.org",
    "zhihu.com",
    "weibo.com",
]

# ============================================================
# 采集设置
# ============================================================
REQUEST_TIMEOUT = 30  # HTTP请求超时（秒）
REQUEST_DELAY = 2     # 请求间隔（秒），避免对服务器造成压力
MAX_ARTICLES_PER_SOURCE = 20  # 每个源最多采集条数
MAX_DAYS_LOOKBACK = 7  # 最多回溯天数
BING_API_KEY = ""  # Bing News Search API Key（可选，不填则跳过Bing源）


# ============================================================
# 议题分类函数
# ============================================================
def classify_article(title, description=""):
    """根据标题和摘要自动分类到议题"""
    text = (title + " " + description).lower()
    categories = []
    for category, words in KEYWORDS.items():
        for word in words:
            if word.lower() in text:
                categories.append(category)
                break
    if not categories:
        categories.append("其他APEC动态")
    return categories
