"""APEC Tracking - Enhanced Configuration
Keyword groups based on research team Q2 analysis. Extended metadata extraction.
"""

# ============================================================
# Tracking Keywords
# ============================================================
KEYWORDS = {
    "数据跨境与隐私保护": [
        "APEC CBPR", "Global CBPR Forum", "CBPR 2.0", "Cross-Border Privacy Rules",
        "APEC cross-border data flow", "APEC cross border data", "APEC data privacy framework",
        "APEC data privacy subgroup", "APEC ECSG data privacy", "APEC DESG data",
        "APEC data protection", "APEC data certification",
        "APEC personal information protection", "APEC personal data protection",
        "APEC personal privacy", "APEC privacy protection", "APEC privacy framework",
        "APEC privacy shield", "APEC data subject rights", "APEC consent mechanism",
        "APEC data breach notification", "APEC sensitive data", "APEC children data protection",
        "APEC data transfer compliance", "APEC cross-border data compliance",
        "APEC data localization", "APEC data sovereignty", "APEC data adequacy",
        "APEC trusted data flow", "APEC data free flow with trust",
        "APEC 跨境数据流动", "APEC 数据跨境", "APEC 数据隐私", "APEC 数据保护",
        "APEC 个人信息保护", "APEC 个人隐私", "APEC 隐私保护", "APEC 数据合规",
        "APEC 数据本地化", "APEC 数据主权", "APEC 数据有序流动", "APEC 数据出境",
        "APEC 个人信息出境", "APEC 隐私框架", "APEC 敏感个人信息",
        "APEC DDTP", "APEC digital trade rules", "APEC 数字贸易规则",
    ],
    "AI治理": [
        "APEC AI governance", "APEC AI Initiative 2026", "APEC AI safety",
        "APEC AI standard", "APEC artificial intelligence governance",
        "APEC artificial intelligence safety", "APEC AI ethics", "APEC responsible AI",
        "APEC AI framework", "APEC AI regulation", "APEC AI US China",
        "APEC AI standards rivalry", "APEC 人工智能治理", "APEC 人工智能安全",
        "APEC 人工智能标准", "APEC AI 治理", "APEC TELWG AI", "APEC telecom AI",
        "APEC digital week AI", "APEC digital minister AI",
    ],
    "互联互通": [
        "APEC connectivity blueprint", "APEC 互联互通蓝图", "APEC 互联互通",
        "APEC digital connectivity", "APEC infrastructure connectivity",
        "APEC 基础设施互联互通",
    ],
    "数字经济": [
        "APEC digital economy", "APEC digital economy roadmap", "APEC AIDER",
        "APEC 数字经济", "APEC digital infrastructure", "APEC internet economy",
        "APEC digital transformation", "APEC 数字化转型", "APEC digital inclusion",
        "APEC 数字包容", "APEC 数字鸿沟", "APEC digital divide",
        "APEC digital trade", "APEC paperless trade", "APEC e-commerce",
        "APEC 跨境电商", "APEC 电子口岸", "APEC 电子提单", "APEC digital services",
        "APEC 数字服务", "APEC AI plus", "APEC digital innovation", "APEC 数字创新",
        "APEC fintech", "APEC 金融科技",
    ],
    "电信与网络治理": [
        "APEC TELWG", "APEC TEL WG", "APEC Telecommunications Working Group",
        "APEC telecom security", "APEC telecom standard", "APEC telecom infrastructure",
        "APEC communications security", "APEC 5G security", "APEC ICT security",
        "APEC 电信工作组", "APEC 电信安全", "APEC 通信安全", "APEC 5G安全",
        "APEC DESG", "APEC 数字经济转向组", "APEC ECSG", "APEC TELMIN",
        "APEC ICT Minister", "APEC CIIP", "APEC critical information infrastructure",
        "APEC cybersecurity", "APEC network security", "APEC CERT", "APEC CSIRT",
        "APEC 网络安全", "APEC 网络犯罪", "APEC 关键信息基础设施",
    ],
    "供应链安全": [
        "APEC supply chain", "APEC supply chain resilience", "APEC supply chain security",
        "APEC ICT supply chain", "APEC 供应链", "APEC 供应链安全", "APEC 供应链韧性",
    ],
    "地缘政治": [
        "APEC trade war", "APEC tariff", "APEC protectionism", "APEC FTAAP",
        "APEC trade facilitation", "APEC multilateral", "APEC economic cooperation",
        "APEC economic outlook", "APEC regional trends", "APEC trade minister",
        "APEC trade policy", "APEC free trade", "APEC 关税", "APEC 贸易便利化",
        "APEC 多边", "APEC 单边", "APEC 贸易部长", "APEC 经济合作",
        "APEC 经济展望", "APEC 区域趋势", "APEC 地缘",
    ],
}

# ============================================================

# ============================================================
# 2026??????
# ============================================================
CHINA_2026_KEYWORDS = [
    "APEC 2026 China", "APEC China 2026", "APEC host year 2026",
    "APEC China host", "APEC 2026 host economy",
    "APEC ???", "APEC 2026 ??", "APEC ????",
    "APEC ???", "APEC ????", "APEC 2026 ??",
    "APEC Suzhou", "APEC ??", "APEC Shanghai", "APEC ??",
    "APEC Beijing 2026", "APEC ??2026",
]


# Domain Whitelist / Blacklist
# ============================================================
ALLOWED_DOMAINS = [
    "apec.org", "www.apec.org",
    "xinhuanet.com", "www.xinhuanet.com", "news.cn", "www.news.cn",
    "people.com.cn", "gmw.cn", "www.gmw.cn", "cnr.cn", "www.cnr.cn",
    # ????/????
    "gov.cn", "www.gov.cn", "sousuo.gov.cn",
    "mfa.gov.cn", "www.mfa.gov.cn", "so.mfa.gov.cn",
    "qstheory.cn", "www.qstheory.cn",
    "cac.gov.cn", "www.cac.gov.cn",
    "cctv.com", "www.cctv.com", "news.cctv.com",
    "jfdaily.com", "www.jfdaily.com", "ce.cn", "www.ce.cn",
    "chinanews.com", "www.chinanews.com", "english.news.cn",
    "reuters.com", "www.reuters.com", "ap.org", "apnews.com", "www.apnews.com",
    "thediplomat.com", "www.thediplomat.com", "usnews.com", "www.usnews.com",
    "oecd.org", "www.oecd.org", "wto.org", "www.wto.org",
    "csis.org", "www.csis.org", "eastwestcenter.org", "www.eastwestcenter.org",
    "pecc.org", "www.pecc.org",
    "trustarc.com", "www.trustarc.com", "babl.ai", "www.babl.ai",
    "worldtrustmark.org", "www.worldtrustmark.org",
]

BLOCKED_DOMAINS = [
    "facebook.com", "twitter.com", "x.com", "reddit.com",
    "youtube.com", "instagram.com", "tiktok.com", "linkedin.com",
    "wikipedia.org", "zhihu.com", "weibo.com",
]

# ============================================================
# Collection Settings
# ============================================================
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 2
MAX_ARTICLES_PER_SOURCE = 50
MAX_DAYS_LOOKBACK = 150
BING_API_KEY = ""

# ============================================================
# Core Classification
# ============================================================

CORE_MATCH = {
    "数据跨境与隐私保护": ["cbpr", "cross-border privacy", "cross border data",
                        "data privacy", "data protection", "data flow",
                        "跨境数据", "数据跨境", "数据隐私", "个人信息", "隐私保护"],
    "AI治理": ["ai governance", "ai safety", "artificial intelligence",
               "ai standard", "ai ethic", "ai initiative", "ai adoption",
               "人工智能", "AI治理", "AI安全"],
    "电信与网络治理": ["telwg", "telecommunications working group", "telecom security",
                   "telecom standard", "telecom infrastructure", "desg",
                   "digital economy steering", "ecsg", "data privacy subgroup",
                   "telmin", "ict minister", "ciip", "critical information",
                   "cert", "csirt", "incident response",
                   "电信工作组", "电信安全", "通信安全", "5g安全",
                   "数字经济转向组", "数据隐私小组", "关键信息基础设施"],
    "数字经济": ["digital economy", "digital trade", "digital transformation",
               "e-commerce", "fintech", "paperless trade",
               "数字经济", "数字贸易", "数字化转型", "跨境电商", "数字服务"],
    "互联互通": ["connectivity", "infrastructure", "digital infrastructure",
               "互联互通", "基础设施"],
    "供应链安全": ["supply chain", "供应链", "ict supply", "resilience"],
    "地缘政治": ["trade war", "tariff", "protectionism", "ftaap",
               "trade facilitation", "multilateral", "economic cooperation",
               "economic outlook", "regional trends", "trade minister",
               "trade policy", "free trade",
               "关税", "贸易便利化", "多边", "单边", "贸易部长",
               "经济合作", "经济展望", "区域趋势", "地缘"],
}

CHINA_MATCH = [
    "som1", "som2", "som3", "som 1", "som 2",
    "shanghai", "harbin", "dalian", "chengdu", "shenzhen",
    "host year", "china 2026", "abac",
    "中国年", "哈尔滨", "上海", "大连", "成都", "深圳",
    "mrt", "digital week", "ceo summit",
    "贸易部长", "数字周", "领导人", "峰会",
    "telwg", "desg", "ecsg",
]

# ============================================================
# Enhanced Metadata: Document Type, APEC Body, Geo, Policy
# ============================================================

DOC_TYPE_RULES = [
    ("official_statement", ["joint statement", "ministerial statement", "declaration",
         "联合声明", "部长声明", "宣言", "communique", "公报"]),
    ("press_release", ["press release", "news release", "新闻稿", "发布", "announces"]),
    ("meeting_minutes", ["meeting", "minutes", "summary record", "会议", "纪要"]),
    ("policy_document", ["policy", "framework", "guideline", "roadmap", "strategy",
         "政策", "框架", "指南", "路线图", "战略", "white paper", "白皮书"]),
    ("report", ["report", "analysis", "review", "assessment", "outlook",
         "报告", "分析", "评估", "展望", "trends"]),
    ("speech", ["speech", "remarks", "address", "keynote", "演讲", "致辞", "讲话"]),
    ("regulation", ["regulation", "rule", "standard", "law", "act",
         "法规", "规则", "标准", "法案"]),
    ("media_report", ["news", "coverage", "报道", "新闻"]),
    ("academic", ["paper", "journal", "research", "study", "学术", "研究"]),
]

APEC_BODY_RULES = [
    ("TELWG", ["telwg", "tel wg", "telecommunications working group", "电信工作组"]),
    ("DESG", ["desg", "digital economy steering group", "数字经济转向组"]),
    ("ECSG", ["ecsg", "e-commerce steering group", "电子商务转向组"]),
    ("DPS", ["dps", "data privacy subgroup", "数据隐私小组"]),
    ("SOM", ["som", "senior officials", "soms", "高官会"]),
    ("MRT", ["mrt", "ministers responsible for trade", "贸易部长"]),
    ("ABAC", ["abac", "business advisory council", "工商咨询理事会"]),
    ("CTI", ["cti", "committee on trade", "贸易投资委员会"]),
    ("SCCP", ["sccp", "sub-committee on customs", "海关分委会"]),
    ("BMG", ["bmg", "budget management", "预算管理委员会"]),
    ("HRDWG", ["hrdwg", "human resources", "人力资源工作组"]),
    ("PPWE", ["ppwe", "policy partnership women", "妇女政策伙伴"]),
    ("EPWG", ["epwg", "emergency preparedness", "应急准备"]),
    ("TELMIN", ["telmin", "telecommunications minister", "ict minister", "数字经济部长"]),
]

GEO_RULES = [
    ("china", ["china", "chinese", "beijing", "shanghai", "中国", "北京", "上海",
         "哈尔滨", "大连", "成都", "深圳"]),
    ("usa", ["united states", "america", "us ", "washington", "美国", "华盛顿"]),
    ("japan", ["japan", "japanese", "tokyo", "日本", "东京"]),
    ("korea", ["korea", "korean", "seoul", "韩国", "首尔"]),
    ("asean", ["asean", "southeast asia", "vietnam", "thailand", "indonesia",
         "东南亚", "东盟"]),
    ("australia", ["australia", "australian", "澳大利亚"]),
    ("russia", ["russia", "russian", "俄罗斯"]),
    ("canada", ["canada", "canadian", "加拿大"]),
    ("latin_america", ["chile", "peru", "mexico", "拉丁美洲", "智利", "秘鲁", "墨西哥"]),
    ("global", ["global", "multilateral", "international", "全球", "多边"]),
]

POLICY_TAG_RULES = [
    ("CBPR", ["cbpr", "cross border privacy rules", "跨境隐私规则"]),
    ("AIDER", ["aider", "digital economy roadmap", "数字经济路线图"]),
    ("DFFT", ["dfft", "data free flow with trust", "可信数据自由流动"]),
    ("FTAAP", ["ftaap", "free trade area asia pacific", "亚太自贸区"]),
    ("DEPA", ["depa", "digital economy partnership", "数字经济伙伴关系"]),
    ("RCEP", ["rcep", "regional comprehensive economic", "区域全面经济伙伴关系"]),
    ("CPTPP", ["cptpp", "trans-pacific partnership", "全面与进步跨太平洋伙伴关系"]),
    ("Connectivity_Blueprint", ["connectivity blueprint", "互联互通蓝图"]),
    ("Digital_Trade", ["digital trade", "e-commerce", "paperless trade", "数字贸易"]),
    ("AI_Governance", ["ai governance", "ai framework", "ai ethics", "AI治理", "AI伦理"]),
    ("Cybersecurity", ["cybersecurity", "cyber security", "网络犯罪", "网络安全"]),
    ("Privacy_Framework", ["privacy framework", "data protection framework", "隐私框架"]),
]


def classify_article(title, description=""):
    text = (title + " " + description).lower()
    categories = []
    for cat, keywords in CORE_MATCH.items():
        for kw in keywords:
            if kw in text:
                categories.append(cat)
                break
    for kw in CHINA_MATCH:
        if kw in text:
            if "2026中国年" not in categories:
                categories.append("2026中国年")
            break
    if not categories:
        categories.append("其他APEC动态")
    return categories


def extract_doc_type(title, description=""):
    text = (title + " " + description).lower()
    types = []
    for dtype, keywords in DOC_TYPE_RULES:
        for kw in keywords:
            if kw in text:
                types.append(dtype)
                break
    return types or ["media_report"]


def extract_apec_bodies(title, description=""):
    text = (title + " " + description).lower()
    bodies = []
    for body, keywords in APEC_BODY_RULES:
        for kw in keywords:
            if kw in text:
                bodies.append(body)
                break
    return bodies


def extract_geo_focus(title, description=""):
    text = (title + " " + description).lower()
    geos = []
    for geo, keywords in GEO_RULES:
        for kw in keywords:
            if kw in text:
                geos.append(geo)
                break
    return geos or ["regional"]


def extract_policy_tags(title, description=""):
    text = (title + " " + description).lower()
    tags = []
    for tag, keywords in POLICY_TAG_RULES:
        for kw in keywords:
            if kw in text:
                tags.append(tag)
                break
    return tags


def calculate_relevance(title, description="", categories=None):
    if categories is None:
        categories = []
    text = (title + " " + description).lower()
    score = 0
    if "apec" in text:
        score += 40
    for cat_keywords in CORE_MATCH.values():
        for kw in cat_keywords:
            if kw in text:
                score += 10
                break
    score += min(len(categories) * 5, 20)
    if any(k in text for k in ["statement", "declaration", "communique", "声明", "公报"]):
        score += 15
    if "2026中国年" in categories or any(k in text for k in ["china 2026", "中国年", "host year"]):
        score += 10
    return min(max(score, 0), 100)


def enhance_article(article):
    title = article.get("title", "")
    description = article.get("summary", "")
    categories = article.get("categories", [])
    article.setdefault("doc_type", extract_doc_type(title, description))
    article.setdefault("apec_bodies", extract_apec_bodies(title, description))
    article.setdefault("geo_focus", extract_geo_focus(title, description))
    article.setdefault("policy_tags", extract_policy_tags(title, description))
    article.setdefault("relevance", calculate_relevance(title, description, categories))
    article.setdefault("notes", "")
    article.setdefault("starred", False)
    return article
