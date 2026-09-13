"""Additional offline content/privacy scan. Only locations and rule names are emitted."""
from pathlib import Path
import re,json,math,collections,argparse

PATTERNS={
 'provider_or_masked_key':r'\b(?:sk[-_]|tvly-|ghp_|github_pat_|AIza|AKIA)[A-Za-z0-9*._-]{3,}',
 'private_key_block':r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
 'jwt':r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}',
 'masked_suffix':r'\*{4,}[A-Za-z0-9]{2,}',
 'bearer':r'(?i)\bbearer[ \t]+[A-Za-z0-9+/_=.-]{12,}',
 'credential_url':r'https?://[^\s/@:]+:[^\s/@]+@',
 'db_credential_url':r'(?:mysql|postgres(?:ql)?|mongodb(?:\+srv)?|redis)://[^\s/@:]+:[^\s/@]+@',
 'host_path':r'(?i)(?:[A-Z]:[\\/](?:Users|AIProjects)[\\/]|/(?:Users|home)/[A-Za-z0-9_-]+/)',
 'phone':r'(?<![A-Za-z0-9])1[3-9]\d{9}(?![A-Za-z0-9])',
 'email':r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
 'raw_social_id':r'''["'](?:user_id|note_id|comment_id|post_id)["']\s*:\s*["'][a-f0-9]{20,}["']''',
 'raw_social_link':r'xiaohongshu\.com/(?:explore|user/profile)/[a-f0-9]{20,}',
 'credential_literal':r'''(?i)(?<![A-Za-z0-9_])["']?(?:[A-Z_]*api[_-]?key|[A-Z_]*secret|[A-Z_]*token|authorization|password|passwd|cookie|web_session|sessionid|webId|xsec_token|a1)["']?[ \t]*[:=][ \t]*["']([^"'\r\n]{4,})["']''',
 'credential_env':r'''(?im)^[ \t]*(?:[A-Z_]*API[_-]?KEY|[A-Z_]*SECRET|[A-Z_]*TOKEN|DB_PASSWORD|PASSWORD|PASSWD|COOKIE|WEB_SESSION|SESSIONID|DATABASE_URL)[ \t]*=[ \t]*([^\r\n]+)$''',
}
KEYWORDS=re.compile(r'(?i)sk[-_]|api[_-]?key|secret|token|bearer|authorization|password|passwd|cookie|web_session|sessionid|access_token|refresh_token|database_url|BEGIN.*PRIVATE KEY|ghp_|github_pat_|AIza|AKIA|xsec_token|webId|\ba1\b')
ALLOWED={'','YOUR_API_KEY','your_key_here','<YOUR_API_KEY>'}
DENIED_DIRS={'.venv','venv','node_modules','__pycache__','dist','runtime','evidence','logs','cookies','user_data_dir','browser_data','browser_profile','models','.auth','login_state','crawler_data','database','backup','.run'}
DENIED_EXT={'.log','.db','.sqlite','.sqlite3','.sql','.dump','.csv','.xlsx','.jsonl','.parquet','.bin','.safetensors','.pt','.pth','.onnx','.key','.pem','.zip'}

def inspect_text(text,name):
 findings=[]; review=[]
 for rule,pattern in PATTERNS.items():
  for m in re.finditer(pattern,text):
   if rule in ('credential_literal','credential_env'):
    value=m.group(1).strip().strip('\"\'')
    if value in ALLOWED or value.startswith(('${','{{','getattr(','settings.')):continue
   if rule=='email' and m.group().endswith('@example.org'):continue
   if rule=='credential_env' and re.fullmatch(r'''['"].*['"]\s*\+.*''',m.group(1)):continue
   findings.append({'file':name,'line':text.count('\n',0,m.start())+1,'rule':rule})
 for m in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text):
  if m.group() not in ('127.0.0.1','0.0.0.0'):
   findings.append({'file':name,'line':text.count('\n',0,m.start())+1,'rule':'non_loopback_address'})
 # Provider/assignment/JWT rules and external Gitleaks cover encoded credentials;
 # entropy review operates on identifier-sized segments rather than whole URL paths.
 for m in re.finditer(r'(?<![A-Za-z0-9])[A-Za-z0-9_+=-]{32,}(?![A-Za-z0-9])',text):
  value=m.group();freq=collections.Counter(value);entropy=-sum(n/len(value)*math.log2(n/len(value)) for n in freq.values())
  if entropy<3.3:continue
  line=text.count('\n',0,m.start())+1
  context=text[max(0,text.rfind('\n',0,m.start())):text.find('\n',m.end()) if '\n' in text[m.end():] else len(text)]
  if re.fullmatch('[a-fA-F0-9]{32,64}',value) and re.search(r'(?i)sha256|sha|commit|reference|fingerprint|91bbd617',context):kind='declared_content_hash_or_commit'
  elif value in ('lightningcss-linux-arm-gnueabihf','managing-your-repositorys-settings-and-features'):kind='reviewed_public_package_or_document_identifier'
  elif re.fullmatch('[a-z_0-9]+|[A-Z_0-9]+',value) and '_' in value:kind='descriptive_identifier'
  else:kind='REVIEW_REQUIRED'
  review.append({'file':name,'line':line,'length':len(value),'entropy':round(entropy,2),'classification':kind})
 return findings,review,len(KEYWORDS.findall(text))

def scan(root):
 root=Path(root);findings=[];entropy=[];keywords=0;files=0
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if '.git' in rel.parts:continue # Git blobs and commit metadata are checked separately.
  if p.is_symlink():findings.append({'file':rel.as_posix(),'rule':'symlink'});continue
  if p.is_dir():
   if p.name in DENIED_DIRS:findings.append({'file':rel.as_posix(),'rule':'private_directory'})
   continue
  files+=1
  if p.stat().st_size>10485760:findings.append({'file':rel.as_posix(),'rule':'large_file'})
  if p.suffix.lower() in DENIED_EXT:findings.append({'file':rel.as_posix(),'rule':'private_payload'})
  if p.name.startswith('.env') and p.name!='.env.example':findings.append({'file':rel.as_posix(),'rule':'private_env'})
  if p.name in ('storage_state.json','cookies.json','session.json'):findings.append({'file':rel.as_posix(),'rule':'login_state'})
  if p.suffix.lower() in ('.png','.jpg','.jpeg'):continue # Metadata and pixels checked by image audit.
  try:text=p.read_bytes().decode('utf-8-sig')
  except UnicodeError:findings.append({'file':rel.as_posix(),'rule':'unexpected_binary'});continue
  f,e,k=inspect_text(text,rel.as_posix());findings+=f;entropy+=e;keywords+=k
 return {'files_checked':files,'keyword_mentions_reviewed':keywords,'findings':findings,'entropy_candidates':entropy,'status':'FAIL' if findings or any(x['classification']=='REVIEW_REQUIRED' for x in entropy) else 'PASS'}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]));parser.add_argument('--output');args=parser.parse_args()
 result=scan(args.root)
 if args.output:Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps(result,indent=2));raise SystemExit(result['status']!='PASS')
