// Loopback-only, read-only static portfolio preview; not a research API.
import {createServer} from 'node:http';
import {readFile,stat,realpath} from 'node:fs/promises';
import {resolve,dirname,relative,sep,extname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const types={'.html':'text/html; charset=utf-8','.md':'text/plain; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.json':'application/json'};
export function createPortfolioServer(directory=root){
return createServer(async(req,res)=>{try{
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);return res.end();}
  let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname==='/'){res.writeHead(302,{'Location':'/docs/assets/demo/public-demo.html'});return res.end();}
  if(pathname.includes('\\')||pathname.includes(':')||pathname.includes('\0')){res.writeHead(403);return res.end();}
  const canonicalRoot=await realpath(directory);
  const requested=resolve(canonicalRoot,'.'+pathname),requestedRel=relative(canonicalRoot,requested);
  const denied=rel=>rel.startsWith('..'+sep)||rel==='..'||rel.split(sep).some(x=>x.startsWith('.'));
  if(denied(requestedRel)){res.writeHead(403);return res.end();}
  const allowlist=new Set((await readFile(resolve(canonicalRoot,'PUBLIC_FILE_ALLOWLIST.txt'),'utf8')).split(/\r?\n/).filter(Boolean));
  if(!allowlist.has(requestedRel.split(sep).join('/'))){res.writeHead(403);return res.end();}
  const file=await realpath(requested),rel=relative(canonicalRoot,file);
  if(denied(rel)){res.writeHead(403);return res.end();}
  if(!(await stat(file)).isFile()){res.writeHead(404);return res.end();}
  res.writeHead(200,{'Content-Type':types[extname(file)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'",'Referrer-Policy':'no-referrer'});
  res.end(req.method==='HEAD'?undefined:await readFile(file));
}catch{res.writeHead(404);res.end('Not found');}});
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const port=Number(process.argv[2]||8765);
 if(!Number.isInteger(port)||port<1||port>65535)throw new Error('Invalid preview port');
 const host=process.env.PORTFOLIO_CONTAINER==='1'?'0.0.0.0':'127.0.0.1';
 createPortfolioServer().listen(port,host,()=>console.log(`Portfolio document preview started on port ${port}`));
}
