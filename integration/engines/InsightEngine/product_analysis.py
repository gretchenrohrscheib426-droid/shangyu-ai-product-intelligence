"""V2 Insight stage: associated comments -> findings -> rendered report."""
from engines.common.evidence_runtime import save, evidence_cards, cards_markdown
from .tools.product_feedback import load_feedback


def analyze(runtime, query, progress):
    progress('检索', 10)
    posts, registry, audit = load_feedback(runtime.folder, query)
    if not posts:
        raise ValueError('没有有效用户反馈样本，不能生成完整Insight')
    progress('总结：标题、正文与信息评论进入同一证据结构', 40)
    prompt = '''你负责Insight：只回答这批用户在说什么。严格区分用户原话、样本事实、模型归纳与推测。
不得外推总体，不得使用最核心、普遍、绝大多数、用户整体、社会普遍、全网、主流用户、已经形成、显著趋势。
标题可以支持“作者声称”，不能臆测图像/视频内容。关注学习/办公；豆包工作、工作伙伴等名称是用户自述，不自动等同官方产品。
请输出themes,pain_points,needs,positive_feedback,negative_feedback五个数组，每组最多4条，可为空。
每条结构为{"finding":"限定样本的具体陈述","evidence":[{"id":"原证据ID","quote":"连续逐字原文片段，至少4字"}],"type":"explicit_need或inferred_need，仅needs使用"}。
优先引用评论中的具体失败场景、使用体验与需求；不能只看标题。不得编写证据ID、引用、数字。
明确需求必须有用户明确请求；推导需求需至少两名不同匿名贡献者描述同类痛点。没有证据的功能建议不放needs。
另输出limitations数组。每条finding保持单一可审计判断，避免把多个不相干证据凑在一起。'''
    output = runtime.call('insight', 'INSIGHT_ENGINE', {'query':query,'sample_counts':{k:audit[k] for k in ('relevant_posts','used_comments')},
        'evidence': list(registry.values())}, prompt)
    rejected = []
    result = {k:evidence_cards(output.get(k), registry, k, rejected) for k in
              ('themes','pain_points','needs','positive_feedback','negative_feedback')}
    result['sample_scope'] = {'platform':'xiaohongshu','raw_posts':audit['total_raw_posts'],'relevant_posts':audit['relevant_posts'],
        'raw_comments':audit['total_comments'],'used_comments':audit['used_comments'],'time_range':audit['time_range'],
        'observed_time_range':audit['observed_time_range']}
    result['limitations'] = ['单平台、小样本、评论覆盖有限、非随机抽样；模型归纳可能有误差；未获取图片/视频；正文仅有标签者不能推测具体体验'] + output.get('limitations', [])
    result['noise_samples'] = [r for r in audit['records'] if r['decision'] != 'include']
    result['rejected_claims'] = rejected
    result['reflection'] = {'no_new_evidence':True,'reason':'已在固定本地有效样本上完成一次分析；不重复调用LLM改写同一总结'}
    if not result['themes']:
        save(runtime.folder,'insight_failed_findings.json',result)
        raise ValueError('Insight没有通过证据校验的主题')
    save(runtime.folder,'insight_findings.json',result)
    progress('反思：没有新证据，结束重复总结', 90)
    cards = sum((result[k] for k in ('themes','pain_points','needs','positive_feedback','negative_feedback')), [])
    report = cards_markdown('用户反馈洞察（有限样本）', cards)
    report += '\n\n## 数据范围\n\n' + str(result['sample_scope']) + '\n\n## 局限性\n\n' + '\n'.join(result['limitations'])
    return result, registry, report
