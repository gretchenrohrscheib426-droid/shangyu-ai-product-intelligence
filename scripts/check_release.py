"""Offline publication checks. Findings report locations, never matched secret values."""
from pathlib import Path
import argparse, json, re, sys, ast
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser

class AssetLinks(HTMLParser):
    def __init__(self):super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):
        self.targets.extend(value for name,value in attrs if name in ('href','src') and value)

ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','__pycache__','.run','build'}
FORBIDDEN={'node_modules','.venv','venv','runtime','evidence','cookies','browser_data','user_data_dir','models'}
TEXT={'.py','.ps1','.mjs','.json','.md','.yml','.yaml','.toml','.txt','.html','.svg','.example'}

def secret_findings(text):
    patterns={
      'provider_token':r'\b(?:sk-[A-Za-z0-9]{12,}|tvly-[A-Za-z0-9-]{15,})',
      'bearer_value':r'(?i)\bBearer\s+[A-Za-z0-9._-]{16,}',
      'private_host_path':r'\b[A-Za-z]:[\\/](?:Users|AIProjects)[\\/]',
      'raw_social_url':r'xiaohongshu\.com/(?:explore|user/profile)/[a-f0-9]{20,}',
      'raw_social_identifier':r'''["'](?:user_id|note_id|comment_id)["']\s*:\s*["'][a-f0-9]{20,}["']''',
      'assigned_credential':r'''(?i)(?:api_key|DB_PASSWORD|web_session|Cookie|Authorization)["']?\s*[:=]\s*["'](?!example|placeholder|\$|\{)[A-Za-z0-9_./+=-]{16,}["']''',
      'env_credential_value':r'''(?im)^[ \t]*(?:[A-Z_]*API_KEY|DB_PASSWORD|WEB_SESSION|COOKIE|AUTHORIZATION)[ \t]*=[ \t]*[^\s#"'\$\{][^\r\n]{7,}$''',
      'cookie_header_value':r'''(?i)["']?(?:cookie|web_session)["']?\s*[:=]\s*["'][^"'\r\n]*=[^"'\r\n]+["']''',
    }
    return [{'rule':name,'line':text.count('\n',0,m.start())+1} for name,pattern in patterns.items() for m in re.finditer(pattern,text)]

def inspect(root=ROOT,secrets_only=False):
    failures=[];count=0
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(x in SKIP for x in rel.parts):continue
        if p.is_dir():
            if p.name in FORBIDDEN:failures.append({'file':str(rel),'rule':'forbidden_directory'})
            continue
        count+=1
        if p.is_symlink(): failures.append({'file':str(rel),'rule':'symlink_not_allowed'})
        if p.stat().st_size>10*1024*1024:failures.append({'file':str(rel),'rule':'over_10MB'})
        if p.name=='.env' or p.name.startswith('.env.') and p.name!='.env.example':failures.append({'file':str(rel),'rule':'private_env'})
        if p.suffix.lower() in ('.db','.sqlite','.sql','.key','.pem','.bin','.safetensors','.zip'):
            failures.append({'file':str(rel),'rule':'private_or_binary_payload'})
        if p.suffix.lower()=='.pdf' and not str(rel).replace('\\','/').startswith('docs/assets/demo/'):
            failures.append({'file':str(rel),'rule':'unapproved_pdf'})
        if p.suffix.lower() not in TEXT and p.name not in ('LICENSE','.gitignore','.dockerignore','.editorconfig','AGENTS.md'):continue
        text=p.read_text(encoding='utf-8-sig')
        failures.extend({'file':str(rel),**f} for f in secret_findings(text))
        if p.name=='.env.example':
            for number,line in enumerate(text.splitlines(),1):
                if '=' in line and not line.startswith('#') and line.split('=',1)[1].strip():
                    failures.append({'file':str(rel),'line':number,'rule':'nonempty_env_example'})
        if secrets_only:continue
        if p.suffix=='.json':
            try:json.loads(text)
            except ValueError:failures.append({'file':str(rel),'rule':'invalid_json'})
        if p.suffix=='.html':
            parser=AssetLinks();parser.feed(text)
            for target in parser.targets:
                if urlsplit(target).scheme or target.startswith('#'):continue
                dest=(p.parent/unquote(target.split('#',1)[0])).resolve()
                if not dest.is_relative_to(root.resolve()) or not dest.exists():failures.append({'file':str(rel),'rule':'broken_html_asset','target':target})
        if p.suffix=='.py':
            try:ast.parse(text)
            except SyntaxError:failures.append({'file':str(rel),'rule':'python_syntax'})
        if p.suffix=='.md':
            if not text.strip():failures.append({'file':str(rel),'rule':'empty_markdown'})
            if sum(line.startswith('```') for line in text.splitlines())%2:failures.append({'file':str(rel),'rule':'unbalanced_fence'})
            for target in re.findall(r'\]\(([^)]+)\)',text):
                target=target.split(' "',1)[0].strip('<>')
                if urlsplit(target).scheme or target.startswith('#'):continue
                dest=(p.parent/unquote(target.split('#',1)[0])).resolve()
                if not dest.is_relative_to(root.resolve()) or not dest.exists():failures.append({'file':str(rel),'rule':'broken_local_link','target':target})
        if '.github' in rel.parts and p.suffix=='.yml':
            if any(s in text for s in ('api.deepseek.com','api.tavily.com','MediaCrawler/main.py','docker compose up')):
                failures.append({'file':str(rel),'rule':'live_ci_call'})
    return {'files_checked':count,'status':'PASS' if not failures else 'FAIL','findings':failures,'scope':'offline file/link/syntax checks; no external URL fetch; no automatic license clearance'}

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('--secrets-only',action='store_true');args.add_argument('--output');opt=args.parse_args()
    result=inspect(secrets_only=opt.secrets_only)
    if opt.output:Path(opt.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(result['status']!='PASS')
