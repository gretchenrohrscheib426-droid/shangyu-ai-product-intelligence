"""Verbatim classification extract; date parsing remains in the private integration."""
from urllib.parse import urlsplit

DOMAINS = {
    'S': ('doubao.com','bytedance.com','volcengine.com'),
    'A': ('xinhuanet.com','news.cn','people.com.cn','cctv.com','chinanews.com.cn','reuters.com','apnews.com'),
    'B': ('36kr.com','jiemian.com','huxiu.com','ithome.com','geekpark.net','thepaper.cn','techcrunch.com'),
    'C': ('baike.baidu.com','wikipedia.org','baike.com','wikiwand.com'),
}

def classify(url):
    host = (urlsplit(url or '').hostname or '').lower()
    if host == 'developer.volcengine.com':
        return {'domain':host,'source_grade':'D'}  # Community authors are not official product statements.
    grade = next((g for g, domains in DOMAINS.items() if any(host == d or host.endswith('.'+d) for d in domains)), 'D')
    return {'domain':host,'source_grade':grade}
