"""Topic-aware source tiers; hostname boundaries prevent suffix spoofing."""
from urllib.parse import urlsplit, urlunsplit

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


def normalize_result(item, query, window):
    url = item.get('url') or ''
    parsed = urlsplit(url)
    if parsed.scheme not in ('http','https') or not parsed.hostname:
        return None
    canonical = urlunsplit((parsed.scheme, parsed.netloc.lower(), parsed.path, parsed.query, ''))
    published = item.get('published_date') or None
    in_window = None
    if published:
        try:
            from dateutil.parser import parse
            day = parse(published).date().isoformat()
            in_window = window['start'][:10] <= day <= window['end'][:10]
        except (ValueError, TypeError, OverflowError):
            pass
    return {'title':item.get('title') or '', 'url':canonical, **classify(canonical),
            'published_at':published,'snippet':item.get('content') or '',
            'score':item.get('score'), 'query':query,'within_window':in_window,
            'date_limitation':None if in_window is not None else 'API未提供可验证的发布日期，仅作当前检索线索，不声称90天内发布'}
