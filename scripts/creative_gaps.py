"""Six source-reviewed, never-run creative lessons; no software or API execution."""
import copy,hashlib,json,shutil
from urllib.parse import urlsplit
MAPPING={'gap-underlord-review':('creative-underlord','agentic_application_feature'),'gap-express-targeted':('creative-express-ai-assistant','conversational_ai_assistant'),'gap-ableton-comp':('creative-ableton-live','deterministic_software_workflow'),'gap-muse-parts':('creative-musescore-studio','deterministic_software_workflow'),'gap-kden-proxy':('vid-kdenlive','deterministic_software_workflow'),'gap-indesign-preflight':('creative-indesign','deterministic_software_workflow')}
NOTICE='仅文档依据和原创待执行练习；documentation-only / never-run。两项AI应用能力不是基础模型，四项普通工具不是Agent。不代表全行业全集。对应技术链接是编辑学习关系，不证明产品能力或实测成效。'
def need(ok,message):
 if not ok:raise ValueError(message)
def safe(url):
 u=urlsplit(url);return u.scheme=='https' and bool(u.hostname) and not u.username and not u.password and not any(c.isspace() for c in url)
EXPRESS_ID='gap-express-targeted'
EXPRESS_OLD_CHECK='把日期/地址/品牌色列为不变量并逐项对照'
EXPRESS_CURRENT_CHECK='仅允许活动时间由周六14:00改为周日15:00；书名、地点、品牌色及其余内容和布局保持不变并逐项对照。'
EXPRESS_EDIT_NOTE='当前展示编辑修正（2026-10-29）：活动时间是唯一允许变动字段；修正验收措辞，不是供应商资料更新。原始研究及其检查日期保留。'
def current_display_checks(cid,checks):
 result=copy.deepcopy(checks)
 if cid==EXPRESS_ID:
  need(result.count(EXPRESS_OLD_CHECK)==1,'Express current-display source sentence changed; manual review required')
  result[result.index(EXPRESS_OLD_CHECK)]=EXPRESS_CURRENT_CHECK
 return result
def adapt(raw):
 d=copy.deepcopy(raw);need(d['schema_version']=='creative-learning-gap-research-r2.v1','unknown schema');need(len(d['sources'])==23 and len(d['candidates'])==6,'cardinality')
 refs={s['id']:s for s in d['sources']};need(len(refs)==23,'duplicate source')
 for s in refs.values():need(safe(s['url']),'unsafe source URL');need(s['status'] in ['opened_primary','tool_open_error','redirect_with_search_body_conflict','independently_opened_primary'],'source evidence upgrade')
 cases=[];seen=set()
 for c in d['candidates']:
  cid=c['id'];need(cid in MAPPING and cid not in seen,'unknown/duplicate case');seen.add(cid);nid,kind=MAPPING[cid]
  need(c['entity_type']==kind and c['is_foundation_model'] is False,'classification mismatch');need(c['lifecycle']['release_date'] is None,'invented release date')
  need(c['original_exercise']['status']=='proposed_not_executed','exercise execution upgrade');need(c['verification']==dict(documentation_review=True,product_run=False,account_login=False,api_key_used=False,output_quality_verified=False),'verification upgrade')
  need(c['source_ids'] and all(s in refs for s in c['source_ids']),'missing source');need(c['visible_documented_path'] and all(isinstance(x,str) and x for x in c['visible_documented_path']),'empty steps');need(len(c['original_exercise']['acceptance_checks'])>=3,'missing acceptance')
  for k in ['access_and_payment','license_and_rights','automation_boundary','gap_vs_existing']:need(isinstance(c[k],str) and c[k],'missing boundary')
  text=json.dumps(c,ensure_ascii=False)
  if cid=='gap-underlord-review':need(all(x in text for x in ['当前session','Version history','compositions/files','协作者','批准','刷新']),'rollback boundary')
  if cid=='gap-express-targeted':need(all(x in text for x in ['中国','Chats','Teams/Enterprise/Education','未列中文','未确认']),'Express boundary')
  sources=[]
  for sid in c['source_ids']:
   s=refs[sid];sources.append(dict(title=sid,url=s['url'],evidence='reference' if s['status'] in ['tool_open_error','redirect_with_search_body_conflict'] else 'primary',checked_at=s['checked_at'],claim=s['supported_claim']+'；原观察：'+s['status']+'；独立QA：'+s.get('independent_qa',{}).get('qa_status','unknown')+'；限制：'+s.get('limitations',''),raw_source=s))
  checks=current_display_checks(cid,c['original_exercise']['acceptance_checks']);intro='分类：'+kind+'。'+NOTICE
  outputs='待审练习记录：输入资产与授权清单；版本/账号/预算检查；逐步操作计划；预期验收表（未观察）；失败恢复与人工批准点；来源/未知项清单。不得虚构实测输出。'
  prompt='仅设计教学练习，不运行产品、购买/试用、上传、克隆声音、外发或发布。\n'+intro+'\n原始输入：'+c['original_exercise']['fixture']+'\n目标：'+c['gap_vs_existing']+'\n步骤依据：\n'+'\n'.join(c['visible_documented_path'])+'\n预期验收：\n'+'\n'.join(checks)+'\n缺账号/许可/预算/素材授权则停止并列缺项；不能将软件权限当操作授权。'
  cases.append(dict(id=cid,title=c['title'],summary=intro+' '+c['gap_vs_existing'],roles=['创意学习者','音乐制作人' if c['domain']=='音乐' else '视频编辑' if c['domain']=='视频' else '设计师'],industries=[c['domain'],'创意教育'],evidence='synthetic',synthetic=True,steps=[dict(title='待执行步骤 '+str(i),body=x,check='未执行不标通过；对照整体验收、许可与人工审批条件逐项记录。') for i,x in enumerate(c['visible_documented_path'],1)],sources=sources,source_ids=c['source_ids'],input=c['original_exercise']['fixture'],prompt=prompt,output=outputs,rubric=checks,risks=c['automation_boundary']+'\n许可：'+c['license_and_rights']+'\n账号与费用：'+c['access_and_payment'],license=c['license_and_rights'],cost=c['access_and_payment'],agent_boundary=intro+' '+c['automation_boundary'],permissions='本练习仅纸面设计；执行、上传、计费、恢复协作项目、下载受限素材和对外发布均未获本练习自动授权。',failure_recovery='在输入、账号、许可、预算或输出核验不满足时停止，保留原件，不把失败静默替换为成功。\n'+'\n'.join(checks),checked_at=d['checked_at'],evidence_note=NOTICE+(' '+EXPRESS_EDIT_NOTE if cid==EXPRESS_ID else ''),lifecycle='unknown',lifecycle_as_of='未核查',applicable_versions=c['lifecycle']['history']+'；精确首发日期unknown，来源更新日期不是产品首发。',replacement_case='',historical_context=c['lifecycle']['history'],practice_status='documentation-only / never-run；原创教学提案，不是实测最佳实践。',modelatlas_node_ids=[nid],modelatlas_links=[dict(id=nid,title=c['product_name']+'（对应技术/工具）',url='https://2codework.github.io/modelatlas/?node='+nid,status='editorial_mapping')],creative_learning=dict(entity_type=kind,execution_status='never-run',proof_level='documentation-only',mapping_relation='editorial_learning_relation',link_semantics='editorial_mapping_not_product_execution'),raw_record=c))
 need(seen==set(MAPPING),'missing case');return cases

def load(root):
 folder=root/'learning/creative-gaps';manifest=json.loads((folder/'raw-sha256.json').read_text());raw=folder/'raw';actual={p.relative_to(raw).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in raw.rglob('*') if p.is_file()};need(actual==manifest,'raw bytes mismatch')
 plan_bytes=(folder/'exercise-plans.json').read_bytes()
 need(hashlib.sha256(plan_bytes).hexdigest()==PLAN_SHA256,'original exercise plan bytes mismatch')
 return attach_exercises(adapt(json.loads((raw/'creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text())),json.loads(plan_bytes))
def publish(root,out):shutil.copytree(root/'learning/creative-gaps',out/'creative-learning-evidence',dirs_exist_ok=True)


def attach_exercises(cases,plans):
 need(plans['schema_version']=='creative.original.exercises.r1' and plans['execution_status']=='never-run','plan execution/schema upgrade')
 need(set(plans['plans'])==set(MAPPING),'plan mapping mismatch')
 need(isinstance(plans['note'],str) and '不是厂商推荐' in plans['note'],'missing synthetic numeric boundary')
 result=copy.deepcopy(cases)
 for c in result:
  plan=plans['plans'][c['id']]
  need(isinstance(plan['task'],str) and plan['task'],'missing task')
  need(len(plan['steps'])==4 and all(isinstance(s,str) and s for s in plan['steps']),'missing four exercise steps')
  for key in ['expected_artifacts','stop_conditions']:need(isinstance(plan[key],list) and plan[key] and all(isinstance(v,str) and v for v in plan[key]),'missing '+key)
  c['original_exercise_plan']=copy.deepcopy(plan)
  c['input'] += '\n原创具体任务：'+plan['task']+'\n'+plans['note']
  c['prompt'] += '\n\n原创纸面练习（never-run）：'+plan['task']+'\n'+plans['note']+'\n'+'\n'.join(str(i)+'. '+v for i,v in enumerate(plan['steps'],1))+'\n停止条件：'+'；'.join(plan['stop_conditions'])
  c['steps'] += [dict(title='原创练习步骤 '+str(i)+'（未执行）',body=v,check='本步骤仅计划；'+plans['note']) for i,v in enumerate(plan['steps'],1)]
  c['output'] += '\n待产出而非已产出：'+'；'.join(plan['expected_artifacts'])
  c['rubric'] += ['预期交付物（未观察）：'+v for v in plan['expected_artifacts']]+['停止条件：'+v for v in plan['stop_conditions']]
  c['risks'] += '\n原创练习停止条件：'+'；'.join(plan['stop_conditions'])
 return result

PLAN_SHA256='d3c8810688583dc4ca356137983b6205cb6e51b13a8dde5a91caac6f52215ede'
