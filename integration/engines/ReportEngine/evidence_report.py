"""Render product evidence cards; LLM selects/synthesizes, code owns citations/counts."""
import html
import json
import re
from pathlib import Path
from portfolio_code.safe_url import safe_url
from engines.common.evidence_runtime import save, read, EvidenceRuntime, BANNED


TITLE='豆包AI助手用户体验与产品机会分析'


def generate(folder, query, task):
    runtime=EvidenceRuntime(folder)
    insight=read(folder,'insight_findings.json');media=read(folder,'media_evidence.json')
    verified=read(folder,'verified_claims.json');forum=read(folder,'forum_synthesis.json')
    all_cards=sum((insight[k] for k in ('themes','pain_points','needs','positive_feedback','negative_feedback')),[]) + verified['claims']
    cards={c['id']:c for c in all_cards}
    eligible={k:v for k,v in cards.items() if v.get('sources') and v.get('status','verified')=='verified'}
    task.update_status('running',25)
    selection=runtime.call('report','REPORT_ENGINE',{'insight_findings':insight,'media_evidence':media,
        'verified_claims':verified,'forum_synthesis':forum},'''你是产品研究报告编辑。只使用提供的结构化证据，不新增事实。
返回{"core_ids":["选取3-5条现有Insight finding id或已verified的Query id，不可选未核验事实"],
"product_opportunities":[{"opportunity":"机会假设","finding_ids":["已有Insight结论ID"],"user_problem":"证据对应问题","suggested_direction":"待实验的方向","validation_needed":"具体如何验证"}],
"operation_opportunities":[同样结构]}。
每类机会最多2条，必须标为Inference，不能写成用户明确需求；没有证据可空。不能编造数字或官方功能。
核心优先办公/学习使用证据、评论中的痛点、正负体验差异。选择已有结论，不重写漂亮长文。
不要把广告/角色扮演的情绪诉求直接转成学习办公主需求；可作为跨场景旁证并明确边界。''',3500)
    core=[];reject=[]
    for cid in dict.fromkeys(selection.get('core_ids',[])):
        if cid in eligible: core.append(eligible[cid])
        else: reject.append({'id':cid,'reason':'不可追溯或未核验的核心候选'})
    if not core: raise ValueError('没有合格的核心结论，拒绝生成伪完整报告')
    opportunities={}
    for category in ('product_opportunities','operation_opportunities'):
        opportunities[category]=[]
        for item in selection.get(category,[])[:2]:
            ids=item.get('finding_ids',[])
            if not ids or not all(i in eligible for i in ids) or any(b in item.get('opportunity','') for b in BANNED):
                reject.append({'candidate':item,'reason':'机会缺少合格证据链'});continue
            refs={r['id']:r for i in ids for r in eligible[i]['sources']}
            opportunities[category].append({**item,'evidence_count':len(refs),'sources':list(refs.values()),
                'statement_type':'Inference','confidence':'low','limitation':'需要用户访谈或任务实验，不能视为已证实需求或收益'})
    document={'version':2,'metadata':{'title':TITLE,'topic':query},'sample_scope':insight['sample_scope'],
        'core_findings':core,'insight':insight,'media':media,'verification':verified,'forum':forum,
        **opportunities,'rejected_report_candidates':reject,
        'limitations':insight['limitations']+media['limitations']+verified['limitations']}
    save(folder,'report_evidence.json',document)
    markdown,body=render(document)
    style='''@page { size:A4; margin:18mm 17mm 18mm; @bottom-center {content:counter(page);font-size:9pt;color:#64748b;} }
    body{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;color:#172033;line-height:1.7;font-size:10pt;max-width:960px;margin:30px auto;padding:0 20px}
    h1{font-size:24pt;line-height:1.35}h2{font-size:17pt;border-bottom:1px solid #cad5e2;padding-bottom:7px;break-after:avoid}h3{font-size:12pt;break-after:avoid}
    a{color:#235782;overflow-wrap:anywhere;word-break:break-all}p,li{overflow-wrap:anywhere}blockquote{margin:10px 0;padding:6px 12px;background:#f3f6f9;border-left:3px solid #7d98b5;white-space:pre-wrap}
    .card{margin:15px 0;padding:12px;border:1px solid #d5dde6;border-radius:4px;break-inside:avoid} .meta{font-size:9pt;color:#52657b}table{border-collapse:collapse;width:100%;margin:12px 0}td,th{padding:7px;border:1px solid #cbd5e1;text-align:left}tr{break-inside:avoid}thead{display:table-header-group}.cover{break-after:page;padding-top:25mm}.section{margin-top:25px}@media print{body{margin:0;padding:0;max-width:none}}'''
    full='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>'+TITLE+'</title><style>'+style+'</style><body>'+body+'</body></html>'
    dest=Path(folder)/'report';dest.mkdir(exist_ok=True)
    (dest/'report.md').write_text(markdown,encoding='utf-8')
    (dest/'report.html').write_text(full,encoding='utf-8')
    task.html_content=full;task.report_file_path=str(dest/'report.html');task.report_file_name='report.html'
    task.markdown_file_path=str(dest/'report.md');task.markdown_file_name='report.md'
    task.ir_file_path=str(Path(folder)/'report_evidence.json');task.state_file_path=task.ir_file_path
    task.update_status('running',85)
    from weasyprint import HTML
    HTML(string=full,base_url=str(dest)).write_pdf(str(dest/'report.pdf'))
    save(folder,'report_task.json',task.to_dict())
    return document


def render(doc):
    escape=html.escape
    scope=doc['sample_scope']
    md=['# '+TITLE,'\n基于真实用户反馈的有限样本研究；V2证据版。']
    body=['<div class="cover"><h1>'+TITLE+'</h1><p>基于真实用户反馈的有限样本研究 · V2证据版</p>',
          f"<p>主要样本 {scope['relevant_posts']} 条帖子 · 分析评论 {scope['used_comments']} 条</p>",
          '<p>区分：用户原话 / 样本归纳 / 外部事实 / Inference</p><p>研究结论仅适用于本轮样本，不代表整体用户、趋势或市场份额。</p></div>']
    def heading(title):md.append('\n## '+title);body.append('<h2>'+escape(title)+'</h2>')
    def paragraph(text):
        # Portable PDF fonts cover Chinese; preserve emoji meaning as a marker, keeping raw evidence unchanged.
        text=re.sub(r'[\U0001f000-\U0001faff\u2600-\u27bf]+', '[表情]', str(text)).replace('\ufe0f','')
        md.append(text);body.append('<p>'+escape(text)+'</p>')
    def card(c):
        text=c.get('finding') or c.get('opportunity') or ''
        md.append('\n### '+text)
        meta=f"Evidence: {c.get('evidence_count',0)} | Sources: {len({s['url'] for s in c.get('sources',[])})} | Confidence: {c['confidence']} | {c.get('statement_type','sample_observation')}"
        md.append(meta);body.append('<div class="card"><h3>'+escape(text)+'</h3><p class="meta">'+escape(meta)+'</p>')
        if c.get('type'): paragraph({'explicit_need':'明确需求','inferred_need':'推导需求'}.get(c['type'],c['type']))
        for r in c.get('sources',[]):
            q=r['quote'];url=safe_url(r['url']);when=r.get('published_at') or '发布日期未提供'
            md.extend(['> '+q.replace('\n',' '),f"Source: [{r['id']}]({url}) · {when}"])
            body.append('<blockquote>'+escape(q)+'</blockquote><p class="meta">Source: <a href="'+escape(url,quote=True)+'">'+escape(r['id'])+'</a> · '+escape(when)+'</p>')
        if c.get('notes'):paragraph(c['notes'])
        for key in ('user_problem','suggested_direction','validation_needed'):
            if c.get(key):paragraph(key+': '+c[key])
        body.append('</div>')
    heading('1. 研究范围')
    rows=[('平台','小红书'),('原始帖子',scope['raw_posts']),('原始评论',scope['raw_comments']),('主要有效帖子',scope['relevant_posts']),('进入分析评论',scope['used_comments']),
          ('研究窗口',scope['time_range']['start'][:10]+' 至 '+scope['time_range']['end'][:10]),
          ('样本实际日期',scope['observed_time_range']['start'][:10]+' 至 '+scope['observed_time_range']['end'][:10])]
    md += ['|项目|实际值|','|---|---|']+[f'|{k}|{v}|' for k,v in rows]
    body.append('<table><thead><tr><th>项目</th><th>实际值</th></tr></thead><tbody>'+''.join('<tr><td>'+escape(k)+'</td><td>'+escape(str(v))+'</td></tr>' for k,v in rows)+'</tbody></table>')
    paragraph('评论去重和信息量筛选不代表随机抽样；推广内容只作背景。帖子或评论数量不能替代独立用户比例。')
    heading('2. 核心结论')
    for c in doc['core_findings']:card(c)
    for label,key in [('3. 主要用户场景','themes'),('4. 用户认可点','positive_feedback'),('5. 用户痛点与负面体验','pain_points'),('6. 用户需求：明确与推导','needs')]:
        heading(label)
        if not doc['insight'][key]:paragraph('本轮没有足够证据支持可列出的结论，保留未知。')
        for c in doc['insight'][key]:
            card(c)
    heading('7. 外部信息核验与跨引擎综合')
    paragraph('Media状态：'+doc['media']['status']+'；真实有效外部来源：'+str(doc['media']['valid_sources']))
    paragraph('官方资料能够核验功能声明，不能据此证明或否定用户的主观体验。没有发布日期的来源不用于声称近90天更新。')
    for c in doc['verification']['claims']:
        paragraph('核验状态：'+c['status']);card(c)
    for key in ('consensus','conflicts','unsupported_claims','questions_for_report'):
        paragraph(key+':')
        if not doc['forum'][key]:paragraph('本轮未检出；不意味着不存在。')
        for x in doc['forum'][key]:paragraph(x['finding']+'（'+', '.join(x['finding_ids'])+'）：'+x['reason'])
    for label,key in [('8. 产品机会（Inference）','product_opportunities'),('9. 运营机会（Inference）','operation_opportunities')]:
        heading(label)
        for c in doc[key]:card(c)
        if not doc[key]:paragraph('证据不足，暂不提出机会。')
    heading('10. Bad Case与质量控制')
    for r in doc['insight']['noise_samples']:paragraph(r['title']+' → '+r['decision']+'：'+r['reason'])
    paragraph('程序拦截候选数：'+str(len(doc['insight']['rejected_claims'])+len(doc['rejected_report_candidates']))+'。原候选与理由保存在JSON审计文件，不删除原数据库记录。')
    paragraph('V1的主帖检索未关联评论；空结构化总结会继续流入报告。V2先保存匿名原始证据，再验证引用；无新证据不重复总结。')
    heading('11. 局限性')
    for x in doc['limitations']:paragraph(x)
    heading('来源索引')
    web={s['id']:s for s in doc['media']['sources']+doc['verification']['sources']}
    for sid,s in web.items():
        s={**s,'url':safe_url(s.get('url'))}
        md.append(f"- [{sid}: {s['title']}]({s['url']}) · Grade {s['source_grade']} · {s['published_at'] or '日期未知'}")
        body.append('<p><a href="'+escape(s['url'],quote=True)+'">'+escape(sid+': '+s['title'])+'</a> · Grade '+s['source_grade']+' · '+escape(s['published_at'] or '日期未知')+'</p>')
    return '\n\n'.join(md),'\n'.join(body)
