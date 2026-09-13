// Original offline document builder. This is not the omitted Vue application build.
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const results=JSON.parse(readFileSync(resolve(root,'evaluation/sample_results.json'),'utf8'));
const esc=x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const fields={raw_posts:'Real collected posts',raw_comments:'Real collected comments',primary_posts:'Primary posts analyzed',input_comments:'Comments sent to analysis',core_cited:'Core findings with citations',core_n:'Core findings reviewed',pdf_pages:'Private verified PDF pages'};
const rows=Object.entries(fields).map(([k,label])=>`<tr><th>${esc(label)}</th><td>${esc(results[k])}</td></tr>`).join('');
const body=`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Shangyu — public case summary</title><style>body{max-width:850px;margin:48px auto;padding:20px;font:18px/1.6 system-ui;color:#202b3c}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd4df;padding:12px;text-align:left}img{max-width:100%}</style><h1>Shangyu</h1><p>Multi-Agent AI Product Sentiment &amp; User Feedback Intelligence Platform</p><p><strong>Static public case summary.</strong> Aggregate results from the inspected private Doubao case; this page does not call an LLM or reproduce the application UI.</p><table>${rows}</table><p>${esc(results.measurement_limit)}</p><p>Core coverage is ${results.core_cited}/${results.core_n}; this does not prove user experiences objectively true. Product and operations recommendations remain hypotheses.</p><img src="../architecture.svg" alt="Actual V2 dependency order"><p><a href="../../case-study-doubao.md">Case study</a> · <a href="../../LEGAL_AND_LICENSE.md">Portfolio-only license scope</a></p></html>`;
mkdirSync(resolve(root,'docs/assets/demo'),{recursive:true});
writeFileSync(resolve(root,'docs/assets/demo/public-demo.html'),body);
console.log('PASS: offline aggregate document built; no paid services or Vue build.');
