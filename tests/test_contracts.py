"""Synthetic fixtures only. No model, crawler, database or network access."""
import unittest,json
from pathlib import Path
from portfolio_code.evidence_contract import evidence_cards,resolve_quote
from portfolio_code.source_quality import classify
from scripts.check_release import secret_findings

class Contracts(unittest.TestCase):
    def source(self,text='请问这个功能怎么用',contributor='anonymous-example'):
        return {'id':'example-01','text':text,'url':'https://example.org/feedback','post_id':'example-post','comment_id':'example-comment','contributor':contributor,'published_at':None}
    def test_actual_quote_required(self):
        r=self.source();audit=[]
        self.assertFalse(evidence_cards([{'finding':'unsupported refund request','evidence':[{'id':r['id'],'quote':'希望退款'}]}],{r['id']:r},'needs',audit));self.assertTrue(audit)
    def test_explicit_request_survives(self):
        r=self.source();c=evidence_cards([{'finding':'A question about usage','type':'explicit_need','evidence':[{'id':r['id'],'quote':r['text']}]}],{r['id']:r},'needs',[])
        self.assertEqual(c[0]['evidence_count'],1)
    def test_same_contributor_is_not_two_users(self):
        r=self.source();s={**r,'id':'example-02'}
        c=evidence_cards([{'finding':'A proposed new feature','type':'inferred_need','evidence':[{'id':x['id'],'quote':x['text']} for x in (r,s)]}],{x['id']:x for x in (r,s)},'needs',[])
        self.assertEqual(c,[])
    def test_no_reordered_ellipsis(self):
        text='提供文件管理能力，支持整理文档并保存生成结果'
        self.assertEqual(resolve_quote(text,'提供文件管理能力……保存生成结果'),text)
        self.assertIsNone(resolve_quote(text,'保存生成结果……提供文件管理能力'))
    def test_host_boundary(self):
        self.assertEqual(classify('https://doubao.com/')['source_grade'],'S')
        self.assertEqual(classify('https://doubao.com.evil.example/')['source_grade'],'D')
    def test_community_is_not_official(self):
        self.assertEqual(classify('https://developer.volcengine.com/articles/example')['source_grade'],'D')
    def test_aggregate_denominators(self):
        d=json.loads((Path(__file__).resolve().parents[1]/'evaluation/sample_results.json').read_text(encoding='utf-8'))
        self.assertEqual(d['primary_posts']+d['context_only_posts']+d['noise_posts'],d['raw_posts'])
        self.assertEqual(sum(d['comment_filter_counts'].values()),d['raw_comments'])
        self.assertLessEqual(d['report_cited_comments'],d['input_comments'])
    def test_scanner_detects_secret_without_echoing_it(self):
        token='sk'+'-'+'A'*32
        findings=secret_findings(token)
        self.assertTrue(findings);self.assertNotIn(token,json.dumps(findings))
    def test_empty_env_and_documentation_are_not_leaks(self):
        self.assertEqual(secret_findings('TAVILY_API_KEY=\nNever publish cookies or Authorization headers.'),[])
    def test_literal_credential_is_detected(self):
        value='Authorization'+' = '+chr(34)+'B'*28+chr(34)
        self.assertTrue(secret_findings(value))
    def test_unquoted_env_credential_is_detected(self):
        self.assertTrue(secret_findings('TAVILY_API_KEY'+'='+'C'*24))
    def test_cookie_header_is_detected(self):
        self.assertTrue(secret_findings('Cookie'+': '+chr(34)+'session='+'D'*20+chr(34)))
    def test_no_blank_reference_accepted(self):
        r=self.source();self.assertFalse(evidence_cards([{'finding':'unsupported','evidence':[{'id':r['id'],'quote':''}]}],{r['id']:r},'theme',[]))

if __name__=='__main__':unittest.main()
