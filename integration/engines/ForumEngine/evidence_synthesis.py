"""One evidence-oriented host call once upstream structured findings exist."""
from engines.common.evidence_runtime import save


def synthesize(runtime, insight, media, verified):
    cards=sum((insight[k] for k in ('themes','pain_points','needs','positive_feedback','negative_feedback')),[]) + media['claims'] + verified['claims']
    ids={c['id'] for c in cards}
    card_map={c['id']:c for c in cards}
    output=runtime.call('forum','FORUM_HOST',{'findings':cards,'media_status':media['status']},'''你是Forum Host，只比较现有证据，不再重复三篇总结。
关注Insight和Media哪里一致、用户感受与官方能力声明是否存在落差、Query有哪些未证实或否定的判断、证据缺口是什么。
用户负面体验与官方宣传不同不自动构成事实冲突；对同一事实/版本的相反证据才是conflict。没有冲突就空数组。
输出consensus,conflicts,unsupported_claims,high_confidence_findings,questions_for_report五个数组，每组最多3条。
每条为{"finding":"一句话综合/问题","finding_ids":["真实上游id"],"reason":"支持与边界"}。
不能创造事实、百分比或新证据，不要把样本推广到整体用户。
再次约束：没有版本证据，不能声称同一版本；用户评价相反仅为观点差异，不进入conflicts。
high_confidence_findings只允许已verified的官方事实，不能放未验证的用户效果描述。
Query已verified的事实不能在unsupported_claims中说成没有官方证据；阅读实际sources，不猜测上游状态。
reported_product_claim是媒体或第三方文章，绝不是小红书用户反馈，不得互换归属。
consensus仅记录不同引擎对同一具体事实的呼应，不把宽泛方向一致、不同场景或正反观点差异凑成共识。
无足够交叉支持就返回空consensus；不要为填满分类编写结论。''',3500)
    result={};rejected=[]
    for category in ('consensus','conflicts','unsupported_claims','high_confidence_findings','questions_for_report'):
        result[category]=[]
        for item in output.get(category,[]):
            refs=item.get('finding_ids',[])
            if not refs or not set(refs)<=ids:
                rejected.append({'category':category,'candidate':item,'reason':'未知结论ID'});continue
            if category == 'conflicts' and not any(card_map[r].get('status') == 'conflicting' for r in refs):
                rejected.append({'category':category,'candidate':item,'reason':'没有事实核验冲突，仅用户感受分歧或待验证问题'});continue
            if category == 'high_confidence_findings' and not any(card_map[r].get('status') == 'verified' for r in refs):
                rejected.append({'category':category,'candidate':item,'reason':'没有已核验官方事实，不升级为高置信结论'});continue
            result[category].append(item)
    result['rejected_items']=rejected
    result['limitations']=['Forum为交叉阅读归纳，不能取代独立事实审查；共识不是统计代表性']
    save(runtime.folder,'forum_synthesis.json',result)
    return result
