"""Verbatim pure-function extracts; provenance in docs/code-provenance.json."""
import re
from portfolio_code.safe_url import safe_url

BANNED = ('最核心', '普遍', '绝大多数', '用户整体', '社会普遍', '全网', '主流用户', '已经形成', '显著趋势')

def resolve_quote(text, quote):
    if quote in text:
        return quote
    # Model ellipses may omit real words, but cannot add or reorder evidence.
    parts = [p.strip() for p in re.split(r'…+|\.{3,}', quote) if p.strip()]
    if len(parts) < 2 or any(len(p) < 4 for p in parts):
        return None
    cursor = 0; start = None
    for part in parts:
        found = text.find(part, cursor)
        if found < 0: return None
        if start is None: start = found
        cursor = found + len(part)
    return text[start:cursor] if cursor - start <= 500 else None

def evidence_cards(items, registry, category, audit):
    cards = []
    for index, item in enumerate(items or []):
        if not isinstance(item, dict):
            audit.append({'category': category, 'reason': 'not_object', 'candidate': item}); continue
        finding = str(item.get('finding') or '')
        refs = item.get('evidence') or []
        valid, reasons = [], []
        for ref in refs:
            source = registry.get(ref.get('id')) if isinstance(ref, dict) else None
            quote = str(ref.get('quote') or '') if isinstance(ref, dict) else ''
            quote = resolve_quote(source['text'], quote) if source else None
            if not source or not quote or len(quote.strip()) < 4:
                reasons.append('证据ID或逐字引用不匹配')
            elif source['id'] not in {r['id'] for r in valid}:
                valid.append({'id': source['id'], 'quote': quote, 'url': source['url'], 'published_at': source.get('published_at')})
        if not finding or not valid or reasons or any(w in finding for w in BANNED):
            audit.append({'category': category, 'candidate': item, 'reason': reasons or ['空证据或无依据外推措辞']}); continue
        contributors = {registry[r['id']].get('contributor') for r in valid} - {None}
        kind = item.get('type')
        if category == 'needs':
            if kind == 'explicit_need' and not any(re.search(r'希望|需要|想要|能不能|有没有|怎么|求|想问|请问|哪里|干啥|恢复.+吧|要是', r['quote']) for r in valid):
                kind = 'inferred_need'
            if kind != 'explicit_need' and len(contributors) < 2:
                audit.append({'category':category,'candidate':item,'reason':'推导需求不足两个独立匿名贡献者，保留为待验证机会，不能冒充用户需求'}); continue
        card = {'id': category + '_' + str(index+1), 'finding': finding, 'evidence_count': len(valid),
                'post_ids': sorted({registry[r['id']]['post_id'] for r in valid if registry[r['id']].get('post_id')}),
                'comment_ids': sorted({registry[r['id']]['comment_id'] for r in valid if registry[r['id']].get('comment_id')}),
                'independent_contributors': len(contributors), 'sources': valid,
                'representative_quotes': [r['quote'] for r in valid],
                'confidence': 'medium' if len(contributors) >= 2 else 'low',
                'statement_type': 'sample_observation',
                'limitations': ['小红书便利样本，不能外推总体；用户自述未独立验证']}
        if kind: card['type'] = kind
        cards.append(card)
    return cards

def cards_markdown(title, cards):
    lines = ['# ' + title]
    for card in cards:
        lines += ['\n### ' + card['finding'], f"Evidence: {card['evidence_count']} | Confidence: {card['confidence']} | ID: {card['id']}"]
        for ref in card['sources']:
            lines += ['> ' + ref['quote'].replace('\n', ' '), f"\nSource: [{ref['id']}]({safe_url(ref['url'])}) | {ref.get('published_at') or '日期未提供'}"]
    return '\n\n'.join(lines)
