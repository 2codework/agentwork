"""Closed plain-text study route; no product calls, grading or learner storage."""
import hashlib,re
from urllib.parse import urlsplit
from product_books import require,load,local,inventory
MANIFEST='5ad23f1ec5ca600232e9e94559cd801a5228fe48e2185f695c9195bf67bf6a18'
PROJECTION_PIN='d1e0cc697131cdb4a22a9de896b9848744bc187872ed9dd050e07caab3e4e5a5'
PHASES=['prepare','tool','setup','prompt','example','check']
ASSETS=['README.zh-CN.md','material.txt','card-prompt.txt','send-once.txt','reference-cards.md','self-test-questions.txt','self-test-answers.md','correction-prompt.txt','error-log.md','sources.md']
def digest(b):return hashlib.sha256(b).hexdigest()
def text(v):require(isinstance(v,str) and bool(v.strip()),'study readable text required')
def catalog(root):
 folder=root/'learning/task-first/r1/study';files=inventory(folder);projection=load(local(folder,'projection.json'))
 require(digest(local(folder,'projection.json').read_bytes())==PROJECTION_PIN,'study admitted projection pin')
 require(projection['source_manifest_sha256']==MANIFEST,'study source manifest binding')
 pins=projection['public_file_sha256'];require(set(files)==set(pins)|{'projection.json'},'study closed publication inventory')
 for name,sha in pins.items():require(digest(local(folder,name).read_bytes())==sha,'study public bytes changed: '+name)
 w=load(local(folder,'workflow.json'));require(w['schema']=='study-workflow/1' and w['id']=='study-three-cards' and w['interaction_mode']=='paste-material','study route identity/input mode')
 require(w['product_execution']=='not_run' and w['user_results']=='not_collected','study execution/score boundary')
 require(list(w['sections'])==PHASES,'study ordered six phases');require([w['sections'][k]['source_step'] for k in PHASES]==list(range(1,7)),'study source phase mapping')
 for k in ['title','outcome','audience','product','product_id','category','material_label','access_cost','privacy']:text(w[k])
 for phase in w['sections'].values():text(phase['title']);text(phase['body'])
 require(w['sections']['prompt']['prompt_asset']=='send-once.txt' and w['sections']['prompt']['reference_asset']=='reference-cards.md','study primary full-message contract')
 for key,name in [('questions_asset','self-test-questions.txt'),('answers_asset','self-test-answers.md'),('correction_asset','correction-prompt.txt'),('error_log_asset','error-log.md')]:require(w['sections']['example'][key]==name,'study self-test asset mapping')
 ledger=load(local(folder,'source-ledger.json'));registry={}
 for source in ledger['sources']:
  for key in ['id','title','url']:text(source[key])
  u=urlsplit(source['url']);require(u.scheme=='https' and u.hostname in {'support.google.com','gemini.google.com','www.anthropic.com','developers.openai.com','2codework.github.io'} and not u.username and not u.password,'unsafe study source URL')
  require(source['id'] not in registry,'duplicate study source');registry[source['id']]=source
 for obj in [w,*w['sections'].values()]:require(obj['source_ids'] and set(obj['source_ids']).issubset(registry),'unresolved study source')
 assets={name:local(folder,name).read_text() for name in ASSETS}
 expected=assets['card-prompt.txt'].rstrip()+'\n\n【固定材料】\n'+assets['material.txt'].rstrip()+'\n【固定材料结束】\n'
 require(assets['send-once.txt']==expected,'study exact assembled source message')
 n=dict(w);n.update(study_workflow=True,asset_base='task-guides/study/',study_assets=assets,input_files=[],connection_guide_ids=[],source_artifact='task-guides/study/README.zh-CN.md',source_details=[dict(registry[k],checked_on='2026-10-29') for k in w['source_ids']],sample_note='作者参考不是产品实跑回答；本课没有用户作答或成绩，不自动评分或安排系统提醒。自测答案应在写完自己的原答后再展开。',delivery_preview='三张经材料核对的卡片、两题自己的原答、错误日志与自己安排的复习日期；本站不预填成绩，不证明永久掌握。')
 return n
