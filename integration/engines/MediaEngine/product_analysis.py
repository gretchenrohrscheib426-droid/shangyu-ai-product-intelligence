"""Bounded Tavily -> whitelisted raw fields -> evidence -> checked JSON summary."""
import hashlib
import re
from engines.common.evidence_runtime import save, read, evidence_cards, cards_markdown
from engines.common.source_quality import normalize_result


def search_sources(runtime, stage, queries, window, domains=None, date_filter=True):
    from tavily import TavilyClient
    client = TavilyClient(api_key=__import__('app.config',fromlist=['settings']).settings.TAVILY_API_KEY)
    normalized, seen, errors = [], set(), []
    for index, query in enumerate(queries):
        name = f'search/{stage}_{index}.json'
        if (runtime.folder/name).exists():
            raw = read(runtime.folder, name)
        else:
            runtime.reserve('search', {'stage':stage,'query':query,'top_k':4}, .2)
            try:
                response = client.search(query=query, max_results=4, search_depth='basic',
                    include_answer=False, include_raw_content=False,
                    **({'start_date':window['start'][:10], 'end_date':window['end'][:10]} if date_filter else {}),
                    **({'include_domains':domains} if domains else {}))
                raw = [{k:item.get(k) for k in ('url','title','content','score','published_date')} for item in response.get('results',[])]
                save(runtime.folder, name, raw)
            except Exception as exc:
                # Never log the SDK request or API key. Failure is a failed search, not empty success.
                errors.append({'query':query,'error_type':type(exc).__name__})
                continue
        for item in raw:
            row = normalize_result(item, query, window)
            if not row or not row['snippet'].strip() or (date_filter and row['within_window'] is False):
                continue
            if not date_filter:
                row['context_scope'] = '官方背景核验，不作为90天内产品更新证据'
            if not re.search('豆包|doubao', row['title'] + row['snippet'], re.I):
                continue
            key = row['url'].rstrip('/')
            title_key = re.sub(r'\W','',row['title']).lower()
            if key in seen or title_key in seen:
                continue
            seen.update((key,title_key))
            row['id'] = 'W:' + hashlib.sha256(key.encode()).hexdigest()[:12]
            normalized.append(row)
    save(runtime.folder, f'{stage}_normalized.json', normalized)
    save(runtime.folder, f'{stage}_search_errors.json', errors)
    return normalized


def registry_for(sources):
    return {s['id']:{'id':s['id'],'text':s['snippet'],'url':s['url'],'title':s['title'],
        'published_at':s['published_at'],'source_grade':s['source_grade'],'post_id':None,'comment_id':None,
        'kind':'web','contributor':None} for s in sources}


def analyze(runtime, query, window, progress):
    queries = ['豆包 AI 官方 学习 办公 产品功能', '豆包 AI 学习 办公 新功能 产品更新', '豆包 AI 办公 文档 写作 字节跳动 产品发布']
    progress('真实Tavily：固定3次检索，每次最多4项',10)
    sources = search_sources(runtime, 'media', queries, window)
    registry = registry_for(sources)
    result = {'search_queries':queries,'sources':sources,'valid_sources':len(sources),'status':'OK','claims':[],
              'window':window,'limitations':['摘要检索未必等同全文；未提供发布日期的来源不视为90天内更新证据']}
    if len(sources) < 2:
        result.update(status='INSUFFICIENT_EVIDENCE', reason='真实有效外部来源少于2条')
        save(runtime.folder,'media_evidence.json',result)
        return result, registry, '# 媒体证据不足\n\n' + result['reason']
    progress('真实摘要写入state；提取有限产品事实',50)
    output = runtime.call('media','MEDIA_ENGINE',{'query':query,'sources':sources},'''你负责Media：从真实检索摘要提取与学习、办公、文档、写作直接有关的最多4条重要产品事实线索。
输出{"claims":[{"finding":"单一事实，不夸大摘要支持范围","evidence":[{"id":"原W:ID","quote":"摘要中连续逐字短句"}]}]}。
摘要提到的第三方产品、豆包工作、工作伙伴，不可直接当作豆包官方同一产品。每条引用不超过60个汉字。
优先S/A来源。C/D只作线索。不要写用户规模/技术架构/产品百科。无证据则claims为空，不能造paragraph_latest_state。日期null保持未知，不能声称是近90天更新。''',4000)
    rejected=[]
    result['claims']=evidence_cards(output.get('claims'),registry,'media_claim',rejected)
    result['rejected_claims']=rejected
    for claim in result['claims']:
        claim['statement_type']='reported_product_claim'
        claim['source_grades']=sorted({registry[r['id']]['source_grade'] for r in claim['sources']})
        claim['confidence']='medium' if any(g in ('S','A') for g in claim['source_grades']) else 'low'
    if not result['claims']:
        result.update(status='INSUFFICIENT_EVIDENCE',reason='有检索结果，但没有通过引用校验的产品事实')
    save(runtime.folder,'media_evidence.json',result)
    progress('完成真实媒体证据归档',95)
    report = cards_markdown('外部媒体与产品信息',result['claims'])
    report += '\n\n有效来源：'+str(len(sources))+'\n\n'+str(result.get('reason',''))
    return result,registry,report
