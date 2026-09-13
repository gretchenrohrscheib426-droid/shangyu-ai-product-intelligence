import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,symlink,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve,sep} from 'node:path';
import {request} from 'node:http';
import {createPortfolioServer} from '../scripts/serve.mjs';

test('preview confines access to approved files and canonical root',async()=>{
 const base=await mkdtemp(join(tmpdir(),'portfolio-security-'));
 const root=join(base,'site'),outside=join(base,'outside');
 await mkdir(root);await mkdir(outside);await mkdir(join(root,'.git'));
 await writeFile(join(root,'ok.md'),'approved');await writeFile(join(root,'unexpected.md'),'unlisted');
 await writeFile(join(root,'.git','config'),'fixture');await writeFile(join(outside,'marker.md'),'outside');
 await symlink(outside,join(root,'linked'),'junction');
 await writeFile(join(root,'PUBLIC_FILE_ALLOWLIST.txt'),'ok.md\n.git/config\nlinked/marker.md\n');
 const server=createPortfolioServer(root);await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const get=(path,method='GET')=>new Promise((done,reject)=>{const q=request({host:'127.0.0.1',port:server.address().port,path,method},res=>{let body='';res.on('data',x=>body+=x);res.on('end',()=>done({status:res.statusCode,body,headers:res.headers}));});q.on('error',reject);q.end();});
 try {
  assert.equal((await get('/ok.md')).body,'approved');
  assert.equal((await get('/ok.md','POST')).status,405);
  assert.equal((await get('/.git/config')).status,403);
  assert.equal((await get('/unexpected.md')).status,403);
  assert.equal((await get('/linked/marker.md')).status,403);
  assert.notEqual((await get('/%2e%2e/outside/marker.md')).body,'outside');
  assert.equal((await get('/ok.md:stream')).status,403);
  assert.equal((await get('/%5coutside')).status,403);
  assert.equal((await get('/')).headers.location,'/docs/assets/demo/public-demo.html');
  assert.equal((await get('/ok.md')).headers['x-content-type-options'],'nosniff');
 }finally{
  await new Promise(r=>server.close(r));
  if(!resolve(base).startsWith(resolve(tmpdir())+sep)||!base.includes('portfolio-security-'))throw new Error('Unsafe fixture cleanup path');
  await rm(base,{recursive:true});
 }
});
