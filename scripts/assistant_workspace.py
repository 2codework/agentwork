"""Official-source reviewed assistant learning adapter. Offline, never product execution."""
import copy,json,hashlib,shutil
from urllib.parse import urlsplit
EXPECTED={'assistant-chatgpt-agent','assistant-chatgpt-deep-research','assistant-claude-cowork','assistant-claude-research','assistant-gemini-apps-deep-research','assistant-perplexity-projects','assistant-perplexity-research','assistant-perplexity-create-files-apps'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def adapt(research,sources):
 r=copy.deepcopy(research);ss=copy.deepcopy(sources);items=r['items'];sm={s['id']:s for s in ss}
 require(len(items)==8 and {x['id'] for x in items}==EXPECTED,'assistant cardinality');require(len(sm)==16,'assistant sources')
 for s in ss:
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'assistant unsafe URL')
 for sid in ('p-projects-change','p-feb-change'):
  require(sm[sid]['event_date'] is None and sm[sid]['normalized_date'] is None,'assistant ambiguous source date normalized')
 require(sm['p-projects-change']['raw_date']=='08/04/26' and sm['p-feb-change']['raw_date']=='02/05/26','assistant raw date changed')
 require(sm['p-labs']['evidence_status']=='unknown','assistant failed source upgraded')
 cases=[]
 for x in items:
  require(x['execution']['status']=='never-run' and all(x['execution'][k] is False for k in ['model_called','account_login','real_automation','user_files_uploaded','user_mac_operated']),'assistant execution claim')
  require(x['learning_task']['original_synthetic'] is True,'assistant synthetic');require(x['entity_type'] in {'historical_executable_agent_surface','research_feature','executable_agent_product_surface','research_workspace','artifact_creation_feature'},'assistant type')
  require(x['source_ids'] and all(s in sm for s in x['source_ids']),'assistant missing source')
  if x['id']=='assistant-chatgpt-agent':
   require(x['dates']['retirement'] is None and x['lifecycle_status']=='documentation_unavailability_notice_with_conflicting_legacy_text','assistant agent lifecycle overclaim')
  if x['id'].startswith('assistant-perplexity-'):
   require(x['dates']['normalized_date'] is None,'assistant ambiguous date normalized')
  task=x['learning_task'];permission='；'.join(x['permissions_and_human_confirmation_zh']);unknown='；'.join(x['unknowns_zh']);limits='；'.join(x['limitations_zh']);dates=json.dumps(x['dates'],ensure_ascii=False)
  source_notes=['文档观察（非事件日期）：'+sm[s]['title']+'；'+json.dumps(sm[s].get('document_observations',[]),ensure_ascii=False)+'；'+sm[s]['evidence_summary_zh'] for s in x['source_ids']]
  boundary=dict(entity_type=x['entity_type'],platform_family_id=x['name'].split()[0],execution_status='never-run',proof_level='documentation-only',permission_boundary=permission,confirmation_boundary='仅离线计划；产品行为是否逐次确认依具体工具/策略，不一概保证。'+permission,lifecycle_note=x['lifecycle_status']+'；'+dates,limitations=x['limitations_zh'],unknowns=x['unknowns_zh'],source_notes=source_notes,synthetic_input=task['input_policy'],expected_not_observed='预期而非观察：'+'；'.join(task['acceptance_zh']))
  cases.append(dict(id='assistant-case-'+x['id'].removeprefix('assistant-'),title=x['name']+'：'+task['title_zh'],summary=x['version_scope_zh']+'；documentation-only / never-run。文档状态：'+x['lifecycle_status']+'。未知：'+unknown,roles=['研究与知识管理','办公室运营'],industries=['跨行业办公'],evidence='synthetic',synthetic=True,execution_status='never-run',runtime_verified=False,is_model=False,proof_level='documentation-only',steps=[dict(title='离线设计 '+str(i+1),body=t,check='仅审查设计，不执行产品；'+task['acceptance_zh'][i%len(task['acceptance_zh'])]) for i,t in enumerate(task['steps_zh'])],sources=[dict(title=sm[s]['title'],url=sm[s]['url'],evidence='primary',checked_at=sm[s]['accessed_at'],claim=sm[s]['evidence_summary_zh']+'；来源QA：'+sm[s]['qa_review']['verdict']+'；仅文档边界，未操作产品。',raw_source=sm[s]) for s in x['source_ids']],source_ids=['assistant-src-'+s for s in x['source_ids']],input=task['input_policy']+'\n原创任务：'+task['title_zh'],prompt='仅纸面设计，不启动产品、不登录、不调用模型、不连接账号，不上传用户文件。\n'+'\n'.join(task['steps_zh'])+'\n停止条件：'+task['stop_condition_zh'],output='预期输出（非实测）：'+'；'.join(task['acceptance_zh']),rubric=task['acceptance_zh'],risks='权限与确认：'+permission+'\n限制：'+limits+'\n未知：'+unknown+'\n停止条件：'+task['stop_condition_zh'],permission_boundary=permission,agent_boundary=x['entity_type']+'；不是基础模型；研究功能、工作区容器和执行产品表面不可混同。',cost=x['availability_zh']+'；价格unknown，未核验，不购买或升级。',checked_at=r['checked_at'],evidence_note='documentation-only / never-run；原创合成练习，不是实测、全球全集或收益证据。',lifecycle='unknown',lifecycle_as_of='文档观察不等于已验证产品生命周期',applicable_versions=x['version_scope_zh'],replacement_case='',historical_context=x['availability_zh']+'\n文档状态：'+x['lifecycle_status']+'\n日期分型：'+dates+'\n'+'\n'.join(source_notes),practice_status='original_teaching_template_not_executed',modelatlas_node_ids=[x['id']],modelatlas_links=[dict(id=x['id'],title=x['name'],url='https://2codework.github.io/modelatlas/?node='+x['id'])],assistant_workspace=boundary,raw_record=x))
 return cases

def load(root):
 p=root/'learning/assistant-workspace/r1';raw=p/'raw';qa=json.loads((p/'qa/REVISION-RECHECK.json').read_text())
 require(qa['verdict']=='accept_with_documented_unknowns','assistant QA disposition')
 for name,digest in qa['revised_input_sha256'].items():
  require('/' not in name and name not in {'.','..'},'assistant unsafe seal path');require(hashlib.sha256((raw/name).read_bytes()).hexdigest()==digest,'assistant approved raw changed: '+name)
 for name,digest in json.loads((raw/'before-qa/sha256.json').read_text()).items():
  require('/' not in name and name not in {'.','..'},'assistant unsafe original path');require(hashlib.sha256((raw/'before-qa'/name).read_bytes()).hexdigest()==digest,'assistant original snapshot changed: '+name)
 return adapt(json.loads((raw/'research.json').read_text()),json.loads((raw/'sources.json').read_text()))
def publish(root,out):shutil.copytree(root/'learning/assistant-workspace/r1',out/'assistant-workspace/r1',dirs_exist_ok=True)
