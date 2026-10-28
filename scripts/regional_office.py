"""Finite regional office document adapter; no product execution."""
import copy,hashlib,json,shutil
from pathlib import PurePosixPath
from urllib.parse import urlsplit
PLATFORM_FAMILIES={'regional-dify':'Dify','regional-coze-studio':'Coze','regional-feishu-aily-enterprise':'Feishu','regional-dingtalk-yida-assistant':'DingTalk','regional-zoho-zia-agents':'Zoho','regional-bailian-agent-app':'Alibaba Cloud','regional-tencent-agent-platform':'Tencent Cloud'}
KINDS={'self-hostable-agent-application-platform','self-hostable-agent-development-platform','hosted-enterprise-agent-feature','hosted-low-code-office-assistant-feature','hosted-agent-platform','hosted-agent-application-platform','hosted-agent-development-platform'}
def require(ok,msg):
 if not ok: raise ValueError(msg)
def adapt(research):
 r=copy.deepcopy(research);ss=r['sources'];sm={s['id']:s for s in ss};items=r['entities']
 require(len(items)==7 and {x['id'] for x in items}==set(PLATFORM_FAMILIES),'regional entity cardinality')
 require(len(sm)==len(ss)==16,'regional source cardinality')
 for s in ss:
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'regional unsafe URL')
 require(sm['dingtalk-delegation']['status']=='search-excerpt-open-failed' and '502' in sm['dingtalk-delegation']['limits'],'regional weak evidence upgraded')
 cases=[]
 for x in items:
  t=x['exercise'];nid=x['id'];kind=x['entity_type']
  require(kind in KINDS and x['is_foundation_model'] is False,'regional invalid type')
  require(x['runtime_status']=='never-run' and x['runtime_verified'] is False and t['status']=='never-run','regional execution claim')
  require(x['evidence_status']=='documentation-only' and t['origin']=='original-synthetic','regional proof claim')
  require(x['source_ids'] and all(s in sm for s in x['source_ids']),'regional source missing')
  require(all(t[k] for k in ['inputs','steps','output_acceptance','failure_risks','human_gate']),'regional exercise missing')
  if nid=='regional-feishu-aily-enterprise':require('豆包工作伙伴' not in x['aliases'] and '关系未知' in x['version_lifecycle'],'regional naming upgraded')
  if nid=='regional-bailian-agent-app':require('2025-04-21' in t['steps'][0] and '预览' in t['steps'][0],'regional access gate missing')
  notes=[sm[s]['title']+'：'+sm[s]['supported_claim']+'；证据状态：'+sm[s]['status']+'；限制：'+sm[s]['limits'] for s in x['source_ids']]
  boundary=dict(entity_type=kind,platform_family_id=PLATFORM_FAMILIES[nid],execution_status='never-run',proof_level='documentation-only',permission_boundary=x['permission_boundary'],confirmation_boundary=t['human_gate'],tenant_connector_requirements=x['tenant_connector_requirements'],license=x['license'],lifecycle_note=x['version_lifecycle'],unknowns=x['unknowns'],source_notes=notes)
  cases.append(dict(id='regional-case-'+nid.removeprefix('regional-'),title=x['name']+'：'+t['title'],summary=x['documented_capability']+'；documentation-only / never-run。未知：'+'；'.join(x['unknowns']),roles=['办公室运营','研究与知识管理'],industries=['跨行业办公'],evidence='synthetic',synthetic=True,execution_status='never-run',runtime_verified=False,is_model=False,proof_level='documentation-only',steps=[dict(title='离线设计 '+str(i+1),body=s,check='预期而非实测：'+t['output_acceptance'][i%len(t['output_acceptance'])]) for i,s in enumerate(t['steps'])],sources=[dict(title=sm[s]['title'],url=sm[s]['url'],evidence='primary',status=sm[s]['status'],limits=sm[s]['limits'],checked_at=sm[s]['checked_at'],claim=notes[i],raw_source=sm[s]) for i,s in enumerate(x['source_ids'])],source_ids=['regional-src-'+s for s in x['source_ids']],input='原创合成输入；不上传：\n'+'\n'.join(t['inputs']),prompt='仅纸面设计：不登录、不调用模型、不上传、不安装、不执行真实流程。\n'+'\n'.join(t['steps'])+'\n'+t['human_gate'],output='预期输出（非实测）：'+'；'.join(t['output_acceptance']),rubric=t['output_acceptance'],risks='权限：'+x['permission_boundary']+'\n确认：'+t['human_gate']+'\n租户/连接器：'+x['tenant_connector_requirements']+'\n许可：'+x['license']+'\n风险：'+'；'.join(t['failure_risks'])+'\n未知：'+'；'.join(x['unknowns']),license=x['license'],permission_boundary=x['permission_boundary'],agent_boundary=kind+'；非基础模型；组件、托管服务、自托管平台不等同。',cost='价格未知：'+x['pricing']+'；地域资格：'+x['regional_availability'],checked_at=x['verified_at'],evidence_note='documentation-only / never-run；原创合成练习，不是实测或部署成效。',lifecycle='unknown',lifecycle_as_of='仅文档观察，未实测生命周期',applicable_versions=x['version_lifecycle'],replacement_case='',historical_context=x['region_context']+'\n租户与连接器：'+x['tenant_connector_requirements']+'\n版本：'+x['version_lifecycle']+'\n来源强弱：'+'\n'.join(notes),practice_status='original_teaching_template_not_executed',modelatlas_node_ids=[nid],modelatlas_links=[dict(id=nid,title=x['name'],url='https://2codework.github.io/modelatlas/?node='+nid)],regional_office=boundary,raw_record=x))
 return cases
def load(root):
 p=root/'learning/regional-office/r1'
 for name,digest in json.loads((p/'qa/artifact-sha256.json').read_text()).items():
  require('/' not in name and name not in ('.','..'),'regional unsafe QA seal path')
  require(hashlib.sha256((p/'qa'/name).read_bytes()).hexdigest()==digest,'regional QA seal changed: '+name)
 qa=json.loads((p/'qa/qa.json').read_text())
 require(qa['status']=='sealed-independent-documentation-qa' and qa['verdict_counts']=={'accept':7,'fix':0,'unknown_entity':0},'regional QA disposition')
 for name,digest in qa['input_sha256'].items():
  q=PurePosixPath(name);require(not q.is_absolute() and '..' not in q.parts and '\\' not in name,'regional unsafe seal path')
  require(hashlib.sha256((p/'raw'/name).read_bytes()).hexdigest()==digest,'regional approved raw changed: '+name)
 return adapt(json.loads((p/'raw/regional-office.json').read_text()))
def publish(root,out):
 shutil.copytree(root/'learning/regional-office/r1',out/'regional-office/r1',dirs_exist_ok=True)
 shutil.copyfile(root/'REGIONAL_OFFICE.md',out/'REGIONAL_OFFICE.md')
