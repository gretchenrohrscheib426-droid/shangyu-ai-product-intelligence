"""Auditable, read-only post/comment inputs for product feedback research."""
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.config import settings


def clean(text):
    value = str(text or '')
    value = re.sub(r'(?:sk-|tvly-)[A-Za-z0-9_-]+', '[密钥已隐藏]', value)
    value = re.sub(r'(?<!\d)1[3-9]\d{9}(?!\d)', '[电话已隐藏]', value)
    value = re.sub(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b', '[邮箱已隐藏]', value)
    return re.sub(r'@[^\s#@]+', '[提及用户已隐藏]', value)


def iso_time(value):
    if not value:
        return None
    if isinstance(value, (int, float)) or str(value).isdigit():
        n = float(value)
        return datetime.fromtimestamp(n / 1000 if n > 1e11 else n, timezone(timedelta(hours=8))).isoformat()
    return value.isoformat() if hasattr(value, 'isoformat') else str(value)


def relevance(post):
    """Two explainable levels: lexical recall and contextual disambiguation.

    Scores are rule confidence, NOT calibrated probabilities. No post IDs in rules.
    """
    text = ' '.join(str(post.get(k) or '') for k in ('title', 'content', 'tags')).lower()
    topic = bool(re.search(r'豆包|doubao', text))
    signals = re.findall(r'ai|大模型|人工智能|deepseek|agent|智能体|办公|学习|写作|代码|编程|工作|科研|飞书|功能', text)
    exclusions = [
        (r'拉💩|拉屎|生活小妙招', '无关生活内容，标签豆包不足以证明AI体验'),
        (r'一年级小豆包|弟弟一年级|食品|红豆馅', '儿童昵称或食品歧义'),
        (r'学习机.*|晚自习.*听歌|看动漫', '主体为娱乐硬件，缺少豆包AI学习办公体验'),
        (r'笔神作文', '主体为其他产品推广，不能归属豆包官方能力'),
        (r'geo|精准获客|必推承诺|纯属娱乐', '营销优化或戏谑，超出学习办公用户体验研究范围'),
    ]
    for pattern, why in exclusions:
        if re.search(pattern, text, re.I):
            return {'relevant': False, 'score': .15, 'reason': why, 'topic': '其他语境', 'signals': signals, 'kind': 'excluded'}
    # Short emotional feedback can concern the product even without literal "AI".
    contextual = bool(re.search(r'情绪价值|广告.*智能体|会员|掉链子|汇报.*数据|这个功能', text))
    ok = topic and (bool(signals) or contextual)
    commercial = bool(re.search(r'订单|交易|pdf.*word|ai搭子就选ta|野生体验家', text, re.I))
    return {'relevant': ok, 'score': .9 if ok else .35,
            'reason': '主题词与AI/学习办公语境共同出现' + ('；推广内容仅作背景，不能作为独立体验证据' if commercial else '') if ok else '没有足够AI产品语境',
            'topic': '豆包AI学习办公体验' if ok else '待判断',
            'signals': signals, 'kind': 'promotional_context' if commercial else 'user_feedback'}


def select_informative_comments(comments, limit=8):
    """Deterministic, polarity-neutral selection; keep reasons for every row."""
    selected, audit, candidates = [], [], []
    seen = set()
    for comment in comments:
        text = comment['content'].strip()
        plain = re.sub(r'\[[^\]]*\]|[^\w\u4e00-\u9fff]', '', text)
        reason = None
        if len(plain) < 3 or re.fullmatch(r'[哈呵嘿啊哦嗯来了赞棒顶好笑哭不错]+', plain):
            reason = 'low_information'
        elif text in seen:
            reason = 'duplicate_text'
        elif re.search(r'互关|回关|加微|私信领取|接单|代做|引流|有需要找我|无私分享发发发', text):
            reason = 'promotion_or_unrelated'
        elif re.search(r'喜欢我的人|霸总文|爱人不是他|诱惑迁移|总结一下', text):
            reason = 'off_scope_chat_or_bot_command'
        seen.add(text)
        score = len(re.findall(r'不|错|问题|代码|用|功能|怎么|能|想|希望|需要|会员|贵|免费|学习|工作|写|文档|记忆|付费|额度|限|比|下载|支持|界面|请问|求分享', text))
        if not reason and score == 0:
            reason = 'no_experience_signal'
        row = {'comment_id': comment['comment_id'], 'decision': 'filtered' if reason else 'candidate', 'reason': reason, 'information_score': score}
        audit.append(row)
        if not reason:
            candidates.append((score, min(comment['like_count'], 100), len(plain), comment, row))
    for _, _, _, comment, row in sorted(candidates, key=lambda x: x[:3], reverse=True):
        if len(selected) < limit:
            selected.append(comment); row.update(decision='used', reason='experience_signal_in_relevant_parent_context')
        else:
            row.update(decision='filtered', reason='per_post_limit')
    return selected, audit


def load_feedback(folder, query, now=None):
    import pymysql
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    now = now or datetime.now(timezone(timedelta(hours=8)))
    start = now - timedelta(days=90)
    conn = pymysql.connect(host=settings.DB_HOST, port=settings.DB_PORT,
        user=settings.DB_USER, password=settings.DB_PASSWORD, database=settings.DB_NAME,
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT note_id,title,`desc`,time,tag_list,source_keyword,user_id FROM xhs_note ORDER BY time,note_id')
            posts = cursor.fetchall()
            cursor.execute('SELECT comment_id,note_id,content,like_count,create_time,user_id FROM xhs_note_comment ORDER BY create_time,comment_id')
            comments = cursor.fetchall()
    finally:
        conn.close()
    # Account identifiers exist only in memory to map anonymous contributors.
    users = {}; groups = {}
    def anonymous(raw):
        key = str(raw or '')
        if not key:
            return None
        if key not in users: users[key] = '匿名贡献者' + str(len(users) + 1)
        return users[key]
    by_post = {}
    for c in comments:
        likes = str(c['like_count'] or '0')
        row = {'comment_id': str(c['comment_id']), 'content': clean(c['content']),
               'like_count': int(likes) if likes.isdigit() else 0, 'time': iso_time(c['create_time']),
               'contributor': anonymous(c['user_id'])}
        by_post.setdefault(str(c['note_id']), []).append(row)
    raw, accepted, rejected, records, comment_audit, registry = [], [], [], [], [], {}
    for p in posts:
        pid = str(p['note_id'])
        row = {'post_id': pid, 'title': clean(p['title']), 'content': clean(p['desc']),
               'publish_time': iso_time(p['time']), 'source_url': 'https://www.xiaohongshu.com/explore/' + pid,
               'matched_keyword': p['source_keyword'], 'tags': p['tag_list'],
               'contributor': anonymous(p['user_id']), 'comments': by_post.get(pid, [])}
        raw.append(row)
        verdict = relevance(row)
        dt = datetime.fromisoformat(row['publish_time']) if row['publish_time'] else None
        if not dt or not start <= dt <= now:
            verdict.update(relevant=False, score=0, reason='outside_90_day_window')
        eligible = verdict['relevant'] and verdict['score'] >= .7 and verdict['kind'] == 'user_feedback'
        records.append({'id': pid, 'title': row['title'], 'relevance_score': verdict['score'],
                        'decision': 'include' if eligible else 'context_only' if verdict['relevant'] else 'reject', **verdict})
        if not eligible:
            rejected.append({'post': row, 'verdict': verdict})
            comment_audit.extend({'comment_id': c['comment_id'], 'decision': 'filtered', 'reason': 'parent_not_in_primary_sample'} for c in row['comments'])
            continue
        chosen, audit = select_informative_comments(row['comments'])
        comment_audit.extend(audit)
        row = {**row, 'comments': chosen}; accepted.append(row)
        eid = 'P:' + pid
        registry[eid] = {'id': eid, 'post_id': pid, 'comment_id': None, 'text': row['title'] + '\n' + row['content'],
                         'url': row['source_url'], 'published_at': row['publish_time'], 'contributor': row['contributor'], 'kind': 'user_post'}
        for comment in chosen:
            eid = 'C:' + comment['comment_id']
            registry[eid] = {'id': eid, 'post_id': pid, 'comment_id': comment['comment_id'], 'text': comment['content'],
                             'url': row['source_url'], 'published_at': comment['time'], 'contributor': comment['contributor'], 'kind': 'user_comment'}
    used = sum(len(p['comments']) for p in accepted)
    audit = {'total_raw_posts': len(raw), 'relevant_posts': len(accepted), 'rejected_posts': len(raw)-len(accepted),
             'topic_related_posts': sum(r['relevant'] for r in records), 'context_only_posts': sum(r['decision']=='context_only' for r in records),
             'total_comments': len(comments), 'used_comments': used, 'filtered_comments': len(comments)-used,
             'records': records, 'comment_decisions': comment_audit,
             'time_range': {'start': start.isoformat(), 'end': now.isoformat()},
             'observed_time_range': {'start': min((p['publish_time'] for p in accepted), default=None), 'end': max((p['publish_time'] for p in accepted), default=None)}}
    for name, value in [('raw_feedback.json', raw), ('feedback_input.json', accepted), ('relevance_audit.json', audit),
                        ('rejected_samples.json', rejected), ('evidence_registry.json', registry)]:
        (folder/name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    return accepted, registry, audit
