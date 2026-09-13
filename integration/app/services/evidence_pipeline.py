"""V2 scheduling for the existing five roles; no extra agent or database."""
import json
import threading
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from loguru import logger
from app.services.event_bus import publish
from app.services import research_session as sessions


def dispatch(query):
    if not sessions.job_lock.acquire(blocking=False):
        return {'success':False,'message':'已有研究或报告任务运行中，请等待完成'}
    try:
        from app.routers import events
        from app.services import forum_service
        forum_service.stop_forum_engine();forum_service._forum_messages.clear()
        with events._replay_lock:events._replay_buffer.clear()
        with events._latest_results_lock:events._latest_results.clear()
        task=sessions.begin(query)
        task['quality_version']=2
        folder=sessions.ROOT/'data/analysis_runs'/task['task_id']
        folder.mkdir(parents=True,exist_ok=False)
        task['analysis_directory']=str(folder)
        task['engines']={name:'running' for name in ('insight','media','query')}
        sessions.save(task)
        publish('task_started',{'task_id':task['task_id'],'query':query})
        threading.Thread(target=run,args=(task,),daemon=True).start()
        return {'success':True,'message':'已启动所有引擎搜索','query':query,'task_id':task['task_id']}
    except Exception:
        sessions.job_lock.release();raise


def run(task):
    from engines.common.evidence_runtime import EvidenceRuntime, save
    folder=Path(task['analysis_directory']);runtime=EvidenceRuntime(folder)
    lock=threading.Lock();results={};registries={};errors={}
    now=datetime.now(timezone(timedelta(hours=8)))
    if (folder/'run.json').exists():
        now=datetime.fromisoformat(json.loads((folder/'run.json').read_text(encoding='utf-8'))['window']['end'])
    window={'start':(now-timedelta(days=90)).isoformat(),'end':now.isoformat()}
    save(folder,'run.json',{'task_id':task['task_id'],'query':task['query'],'window':window,'quality_version':2})
    def progress(engine,message,pct):
        row={'engine':engine,'status':'processing','message':message,'progress_pct':pct}
        with lock:
            with (folder/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
            with (sessions.ROOT/'logs'/f'{engine}.log').open('a',encoding='utf-8') as f:f.write(f"V2 {task['task_id']} {message}\n")
        publish('engine_progress',row)
    def finish(engine,result,registry,report):
        results[engine]=result;registries.update(registry)
        output=Path(task['directory'])/engine;output.mkdir(parents=True,exist_ok=True)
        history=[{'query':task['query'],'url':r['url'],'title':r.get('title') or r['id'],'content':r['text'],
                  'source_id':r['id'],'post_id':r.get('post_id'),'comment_id':r.get('comment_id'),
                  'published_date':r.get('published_at')} for r in registry.values()]
        state={'query':task['query'],'quality_version':2,'is_completed':True,'findings':result,'final_report':report,
               'paragraphs':[{'title':engine,'research':{'search_history':history,'latest_summary':json.dumps(result,ensure_ascii=False)}}]}
        save(output,'state_'+task['task_id']+'.json',state)
        (output/('report_'+task['task_id']+'.md')).write_text(report,encoding='utf-8')
        progress(engine,'完成；结构化证据已保存',100)
        publish('engine_result',{'engine':engine,'final_report':report,'citations':history})
        task['engines'][engine]='completed'
        summary={'type':'agent','sender':engine.title()+' Engine','source':engine,
                 'content':json.dumps(result,ensure_ascii=False)}
        publish('forum_message',summary)
    def failure(engine,exc):
        errors[engine]=type(exc).__name__+': '+str(exc)
        task['engines'][engine]='error'
        save(folder,engine+'_error.json',{'error_type':type(exc).__name__,'message':str(exc),
             'frames':[{'file':Path(f.filename).name,'line':f.lineno} for f in traceback.extract_tb(exc.__traceback__)]})
        publish('engine_error',{'engine':engine,'error':str(exc)})
        logger.error('V2 {} failed: {}',engine,type(exc).__name__)
    def insight():
        try:
            from engines.InsightEngine.product_analysis import analyze
            finish('insight',*analyze(runtime,task['query'],lambda m,p:progress('insight',m,p)))
        except Exception as exc:failure('insight',exc)
    def media():
        try:
            from engines.MediaEngine.product_analysis import analyze
            finish('media',*analyze(runtime,task['query'],window,lambda m,p:progress('media',m,p)))
        except Exception as exc:failure('media',exc)
    try:
        progress('query','等待Insight与Media关键结论后进行事实核验',0)
        threads=[threading.Thread(target=insight),threading.Thread(target=media)]
        for t in threads:t.start()
        for t in threads:t.join()
        if errors:raise ValueError('上游研究失败，Query不生成空上下文报告')
        from engines.QueryEngine.verification import verify
        finish('query',*verify(runtime,task['query'],results['insight'],results['media'],lambda m,p:progress('query',m,p)))
        from engines.ForumEngine.evidence_synthesis import synthesize
        synthesis=synthesize(runtime,results['insight'],results['media'],results['query'])
        content=json.dumps(synthesis,ensure_ascii=False)
        (Path(task['directory'])/'forum.log').write_text(content,encoding='utf-8')
        publish('forum_message',{'type':'host','sender':'Forum Host','content':content,'source':'host'})
        save(folder,'all_evidence_registry.json',registries)
        task['status']='completed';task['forum_status']='completed'
    except Exception as exc:
        if task['engines']['query']!='completed':failure('query',exc)
        else:
            save(folder,'forum_error.json',{'error_type':type(exc).__name__,'message':str(exc)})
            publish('forum_message',{'type':'error','sender':'Forum Host','content':'证据综合失败：'+type(exc).__name__,'source':'host'})
        task['status']='error'
    finally:
        save(folder,'pipeline_validation.json',{'engines':task['engines'],'status':task['status'],'errors':errors,'forum':task.get('forum_status','NOT_COMPLETED')})
        sessions.save(task)
        sessions.job_lock.release()


def resume_forum(task):
    from engines.common.evidence_runtime import EvidenceRuntime, read, save
    from engines.ForumEngine.evidence_synthesis import synthesize
    folder=Path(task['analysis_directory'])
    try:
        result=synthesize(EvidenceRuntime(folder), read(folder,'insight_findings.json'),read(folder,'media_evidence.json'),read(folder,'verified_claims.json'))
        content=json.dumps(result,ensure_ascii=False)
        (Path(task['directory'])/'forum.log').write_text(content,encoding='utf-8')
        publish('forum_message',{'type':'host','sender':'Forum Host','content':content,'source':'host'})
        task['status']='completed'; task['forum_status']='completed'
    except Exception as exc:
        task['status']='error'; task['forum_status']='error'
        save(folder,'forum_error.json',{'error_type':type(exc).__name__})
    finally:
        sessions.save(task); sessions.job_lock.release()


def resume(task_id, stage='research'):
    if stage not in ('research','forum'): raise ValueError('不支持的恢复阶段')
    task=sessions.current()
    if not task or task['task_id'] != task_id or task.get('quality_version') != 2:
        raise ValueError('只能恢复当前V2任务')
    if not sessions.job_lock.acquire(blocking=False):
        raise ValueError('已有任务运行中')
    task['status']='running'
    if stage == 'research': task['engines']={name:'running' for name in ('insight','media','query')}
    task['forum_status']='running'
    sessions.save(task)
    publish('task_started',{'task_id':task['task_id'],'query':task['query']})
    threading.Thread(target=resume_forum if stage == 'forum' else run,args=(task,),daemon=True).start()
    return {'success':True,'task_id':task_id,'message':'从阶段检查点继续；相同输入复用已保存输出'}
