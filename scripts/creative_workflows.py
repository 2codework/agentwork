"""Explicit R2 teaching adapter. Source review is never product execution."""
import copy
import json
import re
import shutil
from urllib.parse import urlsplit

NODE_INFO = {
 'design-freecad-partdesign': ('FreeCAD Part Design · 参数化教学工具', 'FreeCAD', 'creative-design'),
 'design-openscad': ('OpenSCAD · 代码几何教学工具', 'OpenSCAD', 'creative-design'),
 'design-godot-asset-pipeline': ('Godot · 3D资产与碰撞教学工具', 'Godot', 'creative-design'),
 'design-godot-spriteframes': ('Godot SpriteFrames · 逐帧动画教学工具', 'Godot', 'creative-design'),
 'design-libreoffice-impress': ('LibreOffice Impress · 演示交付教学工具', 'LibreOffice', 'creative-design'),
 'music-audacity-spectral': ('Audacity · 频谱编辑教学工具', 'Audacity', 'creative-music'),
}
EXPECTED = {
 'creative-r2-freecad-constrained-part':'design-freecad-partdesign',
 'creative-r2-openscad-parameter-guard':'design-openscad',
 'creative-r2-gltf-handoff':'design-godot-asset-pipeline',
 'creative-r2-game-collision':'design-godot-asset-pipeline',
 'creative-r2-sprite-sheet':'design-godot-spriteframes',
 'creative-r2-impress-master':'design-libreoffice-impress',
 'creative-r2-impress-handouts':'design-libreoffice-impress',
 'creative-r2-spectral-hum':'music-audacity-spectral',
 'creative-r2-loudness-two-pass':'vid-ffmpeg',
}
def require(ok,message):
 if not ok: raise ValueError(message)
def nonempty(v): return isinstance(v,str) and bool(v.strip())
def strings(v): return isinstance(v,list) and bool(v) and all(nonempty(x) for x in v)
def adapt(raw):
 d=copy.deepcopy(raw)
 require(len(d['cases'])==9 and len(d['sources'])==12,'R2 cardinality')
 require(re.fullmatch(r'\d{4}-\d{2}-\d{2}',d['checked_at']) is not None,'checked date')
 sources={s['id']:s for s in d['sources']}
 require(len(sources)==12,'duplicate source')
 for s in sources.values():
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password and not any(c.isspace() for c in s['url']),'unsafe source')
  require(s['publication_date'] is None,'unreviewed publication date')
  require(s['access_status']=='web_open_verified' and s['access_checked_at']==d['checked_at'],'source review boundary')
  require(all(nonempty(s[k]) for k in ['title','version','verified_scope']),'missing source scope')
 cases=[];seen=set()
 for c in d['cases']:
  cid=c['id'];require(cid in EXPECTED and cid not in seen,'unknown/duplicate case');seen.add(cid)
  require(c['lifecycle']==('historical_documentation_retained' if cid=='creative-r2-freecad-constrained-part' else 'documented_candidate'),'unreviewed lifecycle')
  require(all(c['verification'][k] is False for k in ['offline_simulation_executed','product_executed','actual_tested']),'unreviewed execution claim')
  require(c['safe_sandbox_exercise']['status']=='proposed_not_run','unreviewed sandbox')
  for k in ['title','goal','version_caveats','licensing_caveats','agent_boundary','permissions','non_duplicate_rationale']:require(nonempty(c[k]),'missing '+k)
  for k in ['roles','prerequisites','inputs','outputs','failure_modes_and_recovery','acceptance_criteria','source_ids']:require(strings(c[k]),'missing '+k)
  require(all(s in sources for s in c['source_ids']),'missing source')
  require(c['modelatlas_links']==[{'node_id':EXPECTED[cid],'status':'existing_verified' if EXPECTED[cid]=='vid-ffmpeg' else 'proposed_separate_node','type':'tool'}],'unknown mapping')
  require([s['order'] for s in c['steps']]==list(range(1,len(c['steps'])+1)) and bool(c['steps']),'invalid step order')
  require(all(nonempty(s['action']) for s in c['steps']),'empty step')
  sandbox=c['safe_sandbox_exercise'];require(nonempty(sandbox['task']) and nonempty(sandbox['expected']),'missing sandbox')
  risks=c['permissions']+'\n失败与恢复：\n'+'\n'.join(c['failure_modes_and_recovery'])+'\n许可边界：'+c['licensing_caveats']+'\n版本边界：'+c['version_caveats']
  prompt='仅设计本练习，不执行软件、安装、上传、打印或外发。\n前置：\n'+'\n'.join(c['prerequisites'])+'\n合成输入：\n'+'\n'.join(c['inputs'])+'\n纸面沙盒（未运行）：'+sandbox['task']+'\n预期而非结果：'+sandbox['expected']+'\n输出：\n'+'\n'.join(c['outputs'])+'\n'+c['agent_boundary']
  nid=EXPECTED[cid];title=NODE_INFO[nid][0] if nid in NODE_INFO else 'FFmpeg（已有普通工具节点）'
  cases.append(dict(id=cid,title=c['title'],summary=c['goal'],roles=c['roles'],industries=['音乐与音频' if nid.startswith('music-') or nid=='vid-ffmpeg' else '创意设计与教育'],evidence='synthetic',synthetic=True,steps=[dict(title='待执行步骤 '+str(s['order']),body=s['action'],check='对照整体验收逐项记录；未执行不标通过。') for s in c['steps']],sources=[dict(title=sources[s]['title'],url=sources[s]['url'],evidence='primary',checked_at=sources[s]['access_checked_at'],claim=sources[s]['verified_scope']+'；'+sources[s]['version']+'；仅文档核验，非操作结果。',raw_source=sources[s]) for s in c['source_ids']],source_ids=c['source_ids'],input='\n'.join(c['inputs']),prompt=prompt,output='\n'.join(c['outputs']),rubric=c['acceptance_criteria'],risks=risks,failure_recovery='\n'.join(c['failure_modes_and_recovery']),license=c['licensing_caveats'],permissions=c['permissions'],cost='本轮未运行；未来授权执行前核对安装、素材及计算预算。',checked_at=d['checked_at'],evidence_note='官方文档支持工具范围；尺寸、参数目标、步骤及验收为原创教学适配，产品与沙盒均未执行。',lifecycle='unknown',lifecycle_as_of='未核查',applicable_versions=c['version_caveats'],replacement_case='',historical_context='documented_candidate只表示待执行教学提案，不表示工具现行或已弃用。',practice_status='original_teaching_template_not_executed',agent_boundary=c['agent_boundary'],workflow_type=c['workflow_type'],modelatlas_node_ids=[nid],modelatlas_links=[dict(id=nid,title=title,url='https://2codework.github.io/modelatlas/?node='+nid)],raw_record=c))
 require(seen==set(EXPECTED),'missing case')
 nodes=[]
 for nid,(title,vendor,category) in NODE_INFO.items():
  related=[c for c in d['cases'] if EXPECTED[c['id']]==nid];refs=list(dict.fromkeys(s for c in related for s in c['source_ids']))
  nodes.append(dict(id=nid,title=title,type='tool',category=category,vendor=vendor,description_zh='普通创作软件/组件的文档核验教学入口，不是AI模型或自主Agent。覆盖：'+'；'.join(c['goal'] for c in related),version='；'.join(dict.fromkeys(c['version_caveats'] for c in related)),checked_at=d['checked_at'],verification_status='source_reviewed_not_replicated',source_ids=refs,lifecycle='unknown',availability='未实机核验',license='；'.join(dict.fromkeys(c['licensing_caveats'] for c in related)),cost='未执行；安装、素材与计算预算执行前确认。',historical_context='文档版本/归档状态不等于软件生命周期；实际兼容性未测。',steps_zh=[c['title']+'：'+s['action'] for c in related for s in c['steps']],misconceptions=['步骤和验收是待执行教学设计，不是产品实测或自动Agent能力。'],raw_workflow_records=related))
 bundle=dict(schema_version='creative.workflows.r2.adapted.v1',title='创意工作流R2 · 文档支持的未执行教学适配',checked_at=d['checked_at'],scope='九案与六个普通工具入口；不是全行业全集，不证明自主代理或产品效果。',nodes=nodes,edges=[],events=[],sources=[dict(s,checked_at=s['access_checked_at']) for s in d['sources']],cases=[dict(id=c['id'],title=c['title'],modelatlas_node_ids=[EXPECTED[c['id']]]) for c in d['cases']],raw_research=d,coverage_gaps=['本轮创意增量为九个未执行教学设计；实际CAD、物理、动画、印刷及音频验收仍未执行。'])
 return cases,bundle

def load(root):
 return adapt(json.loads((root/'learning/creative/r2/creative-workflows-r2.json').read_text()))
def publish(root,out):
 shutil.copytree(root/'learning/creative/r2',out/'creative-workflows/r2',dirs_exist_ok=True)
