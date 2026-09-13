"""V2 Query: verify claims supplied by Insight/Media, not a product encyclopedia."""
import re
from engines.common.evidence_runtime import save, evidence_cards, cards_markdown
from engines.MediaEngine.product_analysis import search_sources, registry_for


def verify(runtime, query, insight, media, progress):
    origins = {c['id']:c for c in insight['themes'] + insight['pain_points'] + media['claims']}
    candidates = [{'id':c['id'],'claim':c['finding'],'type':c['statement_type']} for c in origins.values()]
    progress('读取Insight关键观点与Media事实；优先官方核验',10)
    # Fixed bounded searches derive their scope from the research question and findings.
    queries = ['豆包 官方 学习 办公 文档 写作 功能介绍',
               '豆包 官方 '+ ' '.join(c['claim'][:35] for c in candidates[:2]),
               '豆包 官方 '+ ' '.join(c['claim'][:35] for c in candidates[-2:])]
    sources = search_sources(runtime,'query',queries,insight['sample_scope']['time_range'],
                             ['doubao.com','bytedance.com','volcengine.com'])
    if not sources:
        fallback = ['豆包 官网 AI 写作 文档 学习 功能', '豆包 官方 AI云盘 文档 PPT 表格']
        sources = search_sources(runtime,'query_official_background',fallback,insight['sample_scope']['time_range'],
                                 ['doubao.com','bytedance.com','volcengine.com'],date_filter=False)
        queries += fallback
    registry = registry_for(sources)
    # Supplement with actual Media sources, keeping the tier of each source.
    registry.update(registry_for(media['sources']))
    progress('逐条核对来源；用户体验不能由官方宣传证明或否定',50)
    output = runtime.call('query','QUERY_ENGINE',{'question':query,'candidates':candidates,'sources':list(registry.values())},'''你负责事实核验，而不是编写百科。最多核验4条与学习办公产品体验直接相关的事实。
从candidates确定核验目标，保留origin_ids。用户主观体验本身不可由官方宣传验证；应核验相应官方功能/场景是否存在，且不能因此声称用户体验已证实。
输出{"claims":[{"claim":"单一可核验陈述","origin_ids":["候选id"],"status":"verified|partially_verified|unverified|conflicting","confidence":"high|medium|low","evidence":[{"id":"W:id","quote":"连续逐字摘要片段，最多60汉字"}],"notes":"证据支持的边界；主体/版本/日期不明确时说明"}]}。
只用提供的证据；verified至少有S/A直接支持，C/D只能unverified或partially_verified。冲突需列出相反证据。
不要核验无关架构、用户规模或公司八卦。不把豆包工作、工作伙伴、豆包AI开放平台混为同一产品。不用当前无发布日期网页证明90天内发布。''',4000)
    claims=[];rejected=[]
    for index,item in enumerate(output.get('claims',[])[:4]):
        origin_ids=[x for x in item.get('origin_ids',[]) if x in origins]
        if not origin_ids:
            rejected.append({'candidate':item,'reason':'没有来自上游的核验目标'});continue
        cards=evidence_cards([{'finding':item.get('claim'),'evidence':item.get('evidence',[])}],registry,'verified_claim',rejected)
        card=cards[0] if cards else {'finding':item.get('claim',''),'evidence_count':0,'sources':[],'representative_quotes':[],'post_ids':[],'comment_ids':[]}
        grades=[registry[r['id']]['source_grade'] for r in card['sources']]
        status=item.get('status','unverified')
        if status not in ('verified','partially_verified','unverified','conflicting'):status='unverified'
        if not card['sources']:status='unverified'
        if status=='verified' and not any(g in ('S','A') for g in grades):status='unverified'
        if status=='conflicting' and len(card['sources'])<2:status='unverified'
        claim={**card,'id':'V'+str(index+1),'claim':card['finding'],'origin_ids':origin_ids,'status':status,
               'confidence':'medium' if status=='verified' else 'low','source_grades':grades,
               'claim_relevance_score':1.0,'relevance_basis':'derived_from_upstream_research_claims',
               'notes':item.get('notes',''),'statement_type':'verified_product_fact' if status=='verified' else 'unverified_product_claim'}
        if not any(g in ('S','A') for g in grades):claim['notes']+='；弱来源，待官方验证'
        claims.append(claim)
    result={'claims':claims,'search_queries':queries,'sources':sources,'rejected_claims':rejected,
            'limitations':['核验官方功能存在不等于核验用户体验；仅依赖搜索摘要，未执行产品功能实测']}
    save(runtime.folder,'verified_claims.json',result)
    progress('完成关键事实核验',95)
    report=cards_markdown('关键产品事实核验',claims)
    report+='\n\n'+'\n'.join(f"{c['id']}: {c['status']}；{c['notes']}" for c in claims)
    return result,registry,report
