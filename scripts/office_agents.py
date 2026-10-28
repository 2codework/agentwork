"""Source-reviewed office agent teaching adapter. No remote calls or product execution."""
import copy,json,shutil,hashlib
from urllib.parse import urlsplit
EXPECTED={'office-ai-by-zapier','office-zapier-agents','office-make-ai-agents-new','office-relevance-ai','office-notion-custom-agents','office-glean-workflow-agents','office-copilot-studio','office-airtable-omni','office-lindy','office-n8n-ai-agent','office-rovo-slack'}
def require(ok,message):
 if not ok:raise ValueError(message)
def adapt(raw,labs):
 r=copy.deepcopy(raw);l=copy.deepcopy(labs)
 require(len(r['records'])==11 and {x['id'] for x in r['records']}==EXPECTED,'office entity cardinality')
 require(len({x['platform_family_id'] for x in r['records']})==10,'office family cardinality')
 require(len(l['cases'])==11 and {c['system_id'] for c in l['cases']}==EXPECTED,'office case cardinality')
 require(len({c['id'] for c in l['cases']})==11,'office duplicate case')
 sm={s['id']:s for s in r['sources']};require(len(sm)==18,'office source cardinality')
 for s in sm.values():
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'office source URL')
 def refs(ids):
  require(ids and all(i in sm for i in ids),'office missing source');return ['office-src-'+i for i in ids]
 cases=[];nodes=[]
 for n in r['records']:
  nid=n['id'];c=next(c for c in l['cases'] if c['system_id']==nid)
  require(n['is_model'] is False and n['runtime_verified'] is False and n['execution_status']=='never-run' and n['proof_level']=='documentation-only','office execution/model claim')
  require(c['synthetic'] is True and c['execution_status']=='never-run' and c['runtime_verified'] is False and c['proof_level']=='documentation-only','office case execution claim')
  require('tutorial_markdown' not in n and 'lesson_markdown' not in c,'office cannot route to MCP downloads')
  source_ids=refs(n['source_ids']);refs(c['source_ids'])
  source_notes=['文档：'+sm[i]['title']+'；'+sm[i]['document_version_or_date']+'；证据读取：'+sm[i]['evidence'] for i in n['source_ids']]
  boundary={'entity_type':n['entity_type'],'platform_family_id':n['platform_family_id'],'execution_status':'never-run','proof_level':'documentation-only','permission_boundary':n['permission_boundary'],'confirmation_boundary':n['confirmation_boundary'],'lifecycle_note':n['lifecycle'],'limitations':n['limitations'],'unknowns':n['unknowns'],'source_notes':source_notes,'synthetic_input':c['input'],'expected_not_observed':c['expected']}
  risks='权限：'+n['permission_boundary']+'\n确认：'+n['confirmation_boundary']+'\n局限：'+'；'.join(n['limitations'])+'\n未知：'+'；'.join(n['unknowns'])
  prompt='仅在纸面设计本合成练习，不连接真实账户、不执行工具、不发送或上传。\n'+'\n'.join(n['human_supervised_steps'])+'\n记录执行身份、目标、参数、审批和预期；没有执行则保持 never-run。'
  cases.append(dict(id=c['id'],title=c['title'],summary='命名办公 Agent 系统的人监督合成练习：'+'；'.join(n['supported_workflows'])+'。文档支持不等于已验证成效。',roles=['办公室运营','业务流程设计'],industries=['跨行业办公'],evidence='synthetic',synthetic=True,execution_status='never-run',runtime_verified=False,proof_level='documentation-only',steps=[dict(title='纸面步骤 '+str(i+1),body=step,check='仅检查计划是否明确权限、目标和确认边界；未执行不能记作通过。') for i,step in enumerate(c['steps'])],sources=[dict(title=sm[i]['title'],url=sm[i]['url'],evidence='primary',checked_at=sm[i]['source_checked_date'],claim=sm[i]['document_version_or_date']+'；'+sm[i]['evidence']+'；只支持文档范围，未操作产品。',raw_source=sm[i]) for i in c['source_ids']],source_ids=source_ids,input=c['input'],prompt=prompt,output='预期而非实测：'+c['expected'],rubric=c['acceptance'],risks=risks,permission_boundary=n['permission_boundary'],agent_boundary=n['entity_type']+'；不是基础模型，不把普通确定性自动化整体算 Agent。',cost=n['access_and_pricing'],checked_at=n['source_checked_date'],evidence_note='documentation-only / never-run；11 个命名实体、10 个平台家族的代表批次，不是全球全集；无真实部署或收益证据。',lifecycle='unknown',lifecycle_as_of='未以统一软件状态推断',applicable_versions=n['lifecycle'],replacement_case='',historical_context='保留旧/新实体及来源更新观察差异；文档更新时间不是产品发布日期。\n'+'\n'.join(source_notes),practice_status='original_teaching_template_not_executed',modelatlas_node_ids=[nid],modelatlas_links=[dict(id=nid,title=n['name'],url='https://2codework.github.io/modelatlas/?node='+nid)],office_agent=boundary,raw_record=dict(entity=n,case=c)))
  nodes.append(dict(id=nid,title=n['name'],type=n['entity_type'],category='office-agent-systems',vendor=n['platform_family_id'],description_zh='命名办公 Agent 系统/组件/客户端面，不是基础模型。文档支持：'+'；'.join(n['supported_workflows'])+'。代表性有限批次；无真实成效验证。',version=n['lifecycle'],checked_at=n['source_checked_date'],verification_status='source_reviewed_not_replicated',proof_level='documentation-only',runtime_verified=False,execution_status='never-run',is_model=False,platform_family_id=n['platform_family_id'],source_ids=source_ids,lifecycle='unknown',availability=n['access_and_pricing'],license='本批未核验产品许可/合同，不推定开源或免费。',cost=n['access_and_pricing'],historical_context='文档更新时间不等于产品发布日期；逐条来源时间与提取边界见办公系统专项说明。',steps_zh=n['human_supervised_steps'],misconceptions=['该平台不保证所有动作默认请求确认；以具体渠道、身份、工具设置为准。','11 实体/10 家族；不是全球完整目录；练习和产品均未执行。']+n['limitations']+n['unknowns'],office_agent=boundary,raw_office_record=n))
 bundle=dict(schema_version='office-agents.adapted.r1',title='办公 Agent 系统 · 11 命名实体/10家族代表批次',scope='文档支持的未执行合成练习；非全球完整、非基础模型或成效排名。',checked_at=r['source_checked_date'],nodes=nodes,edges=[],events=[],sources=[dict(s,id='office-src-'+s['id'],checked_at=s['source_checked_date'],evidence_scope=s['document_version_or_date']+'；'+s['evidence']+'；documentation-only') for s in r['sources']],cases=[dict(id=c['id'],title=c['title'],modelatlas_node_ids=c['modelatlas_node_ids']) for c in cases],raw_research=r,raw_cases=l,coverage_gaps=['办公 Agent 系统已有11命名实体/10家族代表批次；OpenAI、Anthropic及更多地区平台仍待专项核验，未覆盖全球全部服务或版本。'])
 return cases,bundle
def load(root):
 p=root/'learning/office-agents/r1/raw';qa=p.parent/'qa'
 require(json.loads((qa/'recheck.json').read_text())['disposition']=='pass_for_documentation_only_candidate_integration','office QA disposition')
 for name,digest in json.loads((qa/'final-hashes.json').read_text()).items():
  require('/' not in name and name not in ('.','..'),'office unsafe seal path')
  require(hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,'office approved raw changed: '+name)
 return adapt(json.loads((p/'office-agents.json').read_text()),json.loads((p/'raw-cases.json').read_text()))
def publish(root,out):shutil.copytree(root/'learning/office-agents/r1',out/'office-agents/r1',dirs_exist_ok=True)
