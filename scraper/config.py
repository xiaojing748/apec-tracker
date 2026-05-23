"""
APEC 动态追踪 - 配置文件
关键词基于课题组Q2研判参考来源汇编，覆盖CBPR 2.0、AI治理、互联互通蓝图、地缘政治
"""

# ============================================================
# 追踪关键词
# ============================================================
KEYWORDS = {
    "数据跨境与隐私保护": [
        # CBPR体系
        "APEC CBPR",
        "Global CBPR Forum",
        "CBPR 2.0",
        "Cross-Border Privacy Rules",
        "APEC cross-border data flow",
        "APEC cross border data",
        "APEC data privacy framework",
        "APEC data privacy subgroup",
        "APEC ECSG data privacy",
        "APEC DESG data",
        "APEC data protection",
        "APEC data certification",
        # 个人信息与隐私保护
        "APEC personal information protection",
        "APEC personal data protection",
        "APEC personal privacy",
        "APEC privacy protection",
        "APEC privacy framework",
        "APEC privacy shield",
        "APEC data subject rights",
        "APEC consent mechanism",
        "APEC data breach notification",
        "APEC sensitive data",
        "APEC children data protection",
        # 数据跨境合规
        "APEC data transfer compliance",
        "APEC cross-border data compliance",
        "APEC data localization",
        "APEC data sovereignty",
        "APEC data adequacy",
        "APEC trusted data flow",
        "APEC data free flow with trust",
        # 中文
        "APEC 跨境数据流动",
        "APEC 数据跨境",
        "APEC 数据隐私",
        "APEC 数据保护",
        "APEC 个人信息保护",
        "APEC 个人隐私",
        "APEC 隐私保护",
        "APEC 数据合规",
        "APEC 数据本地化",
        "APEC 数据主权",
        "APEC 数据有序流动",
        "APEC 数据出境",
        "APEC 个人信息出境",
        "APEC 隐私框架",
        "APEC 敏感个人信息",
        # 相关技术方案
        "APEC DDTP",
        "APEC digital trade rules",
        "APEC 数字贸易规则",
    ],
    "AI治理": [
        # AI标准与治理
        "APEC AI governance",
        "APEC AI Initiative 2026",
        "APEC AI safety",
        "APEC AI standard",
        "APEC artificial intelligence governance",
        "APEC artificial intelligence safety",
        "APEC AI ethics",
        "APEC responsible AI",
        "APEC AI framework",
        "APEC AI regulation",
        # 中美竞争
        "APEC AI US China",
        "APEC AI standards rivalry",
        # 中文
        "APEC 人工智能治理",
        "APEC 人工智能安全",
        "APEC 人工智能标准",
        "APEC AI 治理",
        # TELWG相关
        "APEC TELWG AI",
        "APEC telecom AI",
        # 成都数字周
        "APEC digital week AI",
        "APEC digital minister AI",
    ],
    "互联互通": [
        # 蓝图
        "APEC connectivity blueprint",
        "APEC 互联互通蓝图",
        "APEC 互联互通",
        "APEC digital connectivity",
        "APEC infrastructure connectivity",
        "APEC 基础设施互联互通",
    ],
    "数字经济": [
        # 数字经济核心
        "APEC digital economy",
        "APEC digital economy roadmap",
        "APEC AIDER",
        "APEC 数字经济",
        "APEC digital infrastructure",
        "APEC internet economy",
        "APEC digital transformation",
        "APEC 数字化转型",
        "APEC digital inclusion",
        "APEC 数字包容",
        "APEC 数字鸿沟",
        "APEC digital divide",
        # 贸易数字化
        "APEC digital trade",
        "APEC paperless trade",
        "APEC e-commerce",
        "APEC 跨境电商",
        "APEC 电子口岸",
        "APEC 电子提单",
        "APEC digital services",
        "APEC 数字服务",
        # 创新
        "APEC AI plus",
        "APEC digital innovation",
        "APEC 数字创新",
        "APEC fintech",
        "APEC 金融科技",
    ],
    "网络犯罪": [
        "APEC cybercrime",
        "APEC cybersecurity",
        "APEC cyber security",
        "APEC network security",
        "APEC 网络安全",
        "APEC 网络犯罪",
        "APEC CIIP",
        "APEC critical infrastructure",
        "APEC 关键信息基础设施",
        "APEC 关键基础设施保护",
        "APEC CERT",
        "APEC CSIRT",
        "APEC incident response",
        "APEC cyber threat",
        "APEC 网络威胁",
    ],
    "供应链安全": [
        # 供应链
        "APEC supply chain resilience",
        "APEC supply chain connectivity",
        "APEC supply chain security",
        "APEC supply chain",
        "APEC 供应链",
        "APEC 供应链韧性",
        "APEC 供应链安全",
        # 数字供应链
        "APEC digital supply chain",
        "APEC ICT supply chain",
        "APEC 数字供应链",
    ],
    "地缘政治": [
        # 供应链
        "APEC supply chain resilience",
        "APEC supply chain connectivity",
        "APEC supply chain",
        "APEC 供应链",
        "APEC 供应链韧性",
        # 贸易
        "APEC trade facilitation",
        "APEC FTAAP",
        "APEC free trade area",
        "APEC economic cooperation",
        "APEC trade war",
        "APEC tariff",
        "APEC 贸易便利化",
        "APEC 关税",
        # 多边
        "APEC multilateral",
        "APEC 多边",
        "APEC economic outlook",
        "APEC RCEP CPTPP",
    ],
}

# 2026 APEC中国年关键词
CHINA_2026_KEYWORDS = [
    # SOM系列
    "APEC SOM1 Harbin",
    "APEC SOM 1 2026",
    "APEC SOM2 Shanghai",
    "APEC SOM 2 2026",
    "APEC SOM3 Dalian",
    "APEC SOM 3 2026",
    "APEC 哈尔滨 SOM",
    "APEC 上海 SOM",
    "APEC 大连 SOM",
    # MRT
    "APEC MRT Suzhou",
    "APEC trade minister responsible",
    "APEC 贸易部长 苏州",
    "APEC 苏州 贸易",
    # 成都
    "APEC Chengdu digital week",
    "APEC digital week 2026",
    "APEC 成都 数字周",
    "APEC 数字 AI 部长",
    # 深圳
    "APEC Shenzhen leaders",
    "APEC Shenzhen summit",
    "APEC 深圳 领导人",
    "APEC 深圳 峰会",
    # 博鳌
    "APEC Boao 2026",
    "APEC 博鳌 2026",
    # 总体
    "APEC 2026 China host year",
    "APEC 2026 China",
    "APEC China 2026",
    "APEC 2026 中国年",
    "APEC 2026 东道主",
    # ABAC
    "APEC ABAC 2026",
    "APEC CEO Summit 2026",
    "APEC 工商咨询",
    # TELWG
    "APEC TELWG",
    "APEC 电信工作组",
    # 35周年/20周年
    "APEC 35周年",
    "APEC FTAAP 20周年",
]

# ============================================================
# 域名白名单
# ============================================================
ALLOWED_DOMAINS = [
    # APEC 官方
    "apec.org",
    "www.apec.org",
    "globalcbpr.org",
    "www.globalcbpr.org",
    "pdb.apec.org",
    # 中国政府
    "fmprc.gov.cn",
    "www.fmprc.gov.cn",
    "english.www.gov.cn",
    "gov.cn",
    "miit.gov.cn",
    "www.miit.gov.cn",
    "mofcom.gov.cn",
    "www.mofcom.gov.cn",
    "chinawto.mofcom.gov.cn",
    "shanghai.gov.cn",
    "www.shanghai.gov.cn",
    # 官方智库/机构
    "chinapda.org.cn",
    "www.chinapda.org.cn",
    # 权威中文媒体
    "xinhuanet.com",
    "www.xinhuanet.com",
    "people.cn",
    "www.people.cn",
    "people.com.cn",
    "gmw.cn",
    "www.gmw.cn",
    "cnr.cn",
    "www.cnr.cn",
    "jfdaily.com",
    "www.jfdaily.com",
    "ce.cn",
    "www.ce.cn",
    "chinanews.com",
    "www.chinanews.com",
    "english.news.cn",
    # 权威国际媒体
    "reuters.com",
    "www.reuters.com",
    "ap.org",
    "apnews.com",
    "www.apnews.com",
    "thediplomat.com",
    "www.thediplomat.com",
    "usnews.com",
    "www.usnews.com",
    # 国际组织/智库
    "oecd.org",
    "www.oecd.org",
    "wto.org",
    "www.wto.org",
    "csis.org",
    "www.csis.org",
    "eastwestcenter.org",
    "www.eastwestcenter.org",
    "pecc.org",
    "www.pecc.org",
    # 专业来源
    "trustarc.com",
    "www.trustarc.com",
    "babl.ai",
    "www.babl.ai",
    "worldtrustmark.org",
    "www.worldtrustmark.org",
]

# 排除域名
BLOCKED_DOMAINS = [
    "facebook.com", "twitter.com", "x.com", "reddit.com",
    "youtube.com", "instagram.com", "tiktok.com", "linkedin.com",
    "wikipedia.org", "zhihu.com", "weibo.com",
]

# ============================================================
# 采集设置
# ============================================================
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 2
MAX_ARTICLES_PER_SOURCE = 50
MAX_DAYS_LOOKBACK = 150  # 覆盖2026年1月至今（约150天）
BING_API_KEY = ""


def classify_article(title, description=""):
    """根据标题和摘要自动分类到议题——支持短语和关键词部分匹配"""
    text = (title + " " + description).lower()
    categories = []

    # 核心词映射：当标题中出现这些词时自动归类
    CORE_MATCH = {
        "数据跨境与隐私保护": ["cbpr", "cross-border privacy", "cross border data",
                            "data privacy", "data protection", "data flow",
                            "跨境数据", "数据跨境", "数据隐私", "个人信息", "隐私保护"],
        "AI治理": ["ai governance", "ai safety", "artificial intelligence",
                   "ai standard", "ai ethic", "ai initiative", "ai adoption",
                   "人工智能", "AI治理", "AI安全"],
        "数字经济": ["digital economy", "digital trade", "digital transformation",
                   "e-commerce", "fintech", "paperless trade",
                   "数字经济", "数字贸易", "数字化转型", "跨境电商", "数字服务"],
        "互联互通": ["connectivity", "infrastructure", "digital infrastructure",
                   "互联互通", "基础设施"],
        "供应链安全": ["supply chain", "供应链", "ict supply"],
        "网络犯罪": ["cybersecurity", "cyber security", "cybercrime",
                   "critical infrastructure", "ciip", "incident response",
                   "网络安全", "网络犯罪", "关键信息基础设施", "网络威胁"],
        "地缘政治": ["trade war", "tariff", "protectionism", "ftaap",
                   "trade facilitation", "multilateral", "economic cooperation",
                   "关税", "贸易便利化", "多边", "单边"],
    }

    for cat, keywords in CORE_MATCH.items():
        for kw in keywords:
            if kw in text:
                categories.append(cat)
                break

    # 额外检查2026中国年
    CHINA_MATCH = [
        "som1", "som2", "som3", "som 1", "som 2",
        "shanghai", "suzhou", "harbin", "dalian", "chengdu", "shenzhen",
        "host year", "china 2026", "aboac",
        "中国年", "哈尔滨", "上海", "苏州", "大连", "成都", "深圳",
        "mrt", "digital week", "ceo summit",
        "贸易部长", "数字周", "领导人", "峰会",
    ]
    for kw in CHINA_MATCH:
        if kw in text:
            if "2026中国年" not in categories:
                categories.append("2026中国年")
            break

    if not categories:
        categories.append("其他APEC动态")
    return categories
