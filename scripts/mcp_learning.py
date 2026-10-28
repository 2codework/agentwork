"""Explicit fail-closed MCP teaching adapter; original bytes remain under learning/mcp/raw."""
import copy,json,re,shutil,zipfile
from pathlib import Path

def require(ok,message):
    if not ok: raise ValueError('MCP learning: '+message)
def text(v): return isinstance(v,str) and bool(v.strip())
def strings(v): return isinstance(v,list) and bool(v) and all(text(x) for x in v)
def load(root):
    base=root/'learning/mcp'; raw=base/'raw'
    doc=json.loads((raw/'cases.json').read_text()); sources=json.loads((raw/'sources.json').read_text()); suggestions=json.loads((raw/'integration-suggestions.json').read_text()); overlay=json.loads((base/'overlay.json').read_text())
    require(doc.get('schema_version')==1,'unsupported cases schema')
    require(sources.get('schema_version')=='mcp.learning.sources.v1','unsupported source schema')
    require(suggestions.get('schema_version')=='mcp.learning.integration-suggestions.v1','unsupported suggestions schema')
    require(set(overlay)=={'schema_version','checked_at','skills_note','sources'} and overlay['schema_version']=='mcp.learning.overlay.v1','unsupported overlay schema')
    require(text(overlay['skills_note']) and overlay['checked_at']=='2026-10-28','invalid overlay')
    require(isinstance(overlay['sources'],list) and len(overlay['sources'])==2,'invalid overlay sources')
    all_sources=sources['sources']+overlay['sources']; bysource={s['id']:s for s in all_sources}
    require(len(bysource)==len(all_sources),'duplicate sources')
    for s in all_sources:
        require(all(text(s.get(k)) for k in ['id','title','url','scope','checked_at']),'source metadata')
        require(s['url'].startswith('https://') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',s['checked_at']),'source URL/date')
    cases=[];ids=set(); nodes=suggestions['modelatlas_tutorial_nodes']
    require(len(doc['cases'])==12 and len(nodes)==12,'expected twelve lessons')
    for c0,n in zip(doc['cases'],nodes):
        require(set(c0)=={'source_ids', 'checked_at', 'industries', 'practice_status', 'steps', 'lifecycle_as_of', 'verification_status', 'risks', 'evidence_note', 'title', 'sources', 'applicable_versions', 'goal', 'modelatlas_node_ids', 'summary', 'synthetic', 'common_errors', 'permissions', 'replacement_case', 'lifecycle', 'id', 'input', 'evidence', 'prompt', 'prerequisites', 'rubric', 'roles', 'historical_context', 'output', 'fixture'},'unknown or missing case extension field')
        require(set(n)=={'source_ids', 'checked_at', 'relation_evidence_type', 'lifecycle', 'type', 'category', 'id', 'description_zh', 'verification_status', 'agentwork_case_id', 'title', 'prerequisites', 'version'},'unknown or missing tutorial field')
        require(strings(n.get('prerequisites')) and strings(n.get('source_ids')) and n.get('checked_at')=='2026-10-28' and n.get('verification_status')=='offline_contract_only','invalid tutorial extensions')
        c=copy.deepcopy(c0)
        require(c['id'] not in ids and re.fullmatch('mcp-lab-[a-z-]+',c['id']),'case identity');ids.add(c['id'])
        for key in ['goal','permissions','input','output','prompt','fixture','applicable_versions','evidence_note','verification_status']:
            require(text(c.get(key)),'invalid '+key)
        for key in ['prerequisites','common_errors','rubric','source_ids','modelatlas_node_ids']:
            require(strings(c.get(key)),'invalid '+key)
        require(c['verification_status']=='offline_contract_only','invalid execution status')
        require(c['fixture']=='fixtures/'+c['id']+'.json','invalid fixture path')
        fixture=json.loads((raw/c['fixture']).read_text())
        require(json.loads(c['input'])==fixture['input'] and json.loads(c['output'])==fixture['expected'],'fixture mismatch')
        require(isinstance(c['steps'],list) and len(c['steps'])==3 and all(all(text(s.get(k)) for k in ['title','body','check']) for s in c['steps']),'steps')
        require(n.get('agentwork_case_id')==c['id'] and n.get('id')==c['id']+'-tutorial' and n.get('type')=='tutorial','tutorial identity')
        require(n.get('relation_evidence_type')=='editorial_learning_order' and n.get('source_ids')==c['source_ids'],'tutorial evidence')
        require(n.get('version')==c['applicable_versions'] and n.get('lifecycle')==c['lifecycle'],'tutorial version')
        if c['id']=='mcp-lab-skill': c['source_ids']+= [s['id'] for s in overlay['sources']]
        require(all(s in bysource for s in c['source_ids']),'source reference')
        c['sources']=[dict(title=bysource[s]['title'],url=bysource[s]['url'],evidence='primary',checked_at=bysource[s]['checked_at'],claim=bysource[s]['scope']) for s in c['source_ids']]
        c['raw_record']=c0
        c['failure_recovery']='先在临时副本修正被指出的字段或顺序，再运行本地测试。外部操作结果若未知，先查询状态；不要将本地重放规则套用于真实写操作。'
        c['permission_boundary']=c['permissions']
        c['modelatlas_links']=[{'title':c['title'],'url':'https://2codework.github.io/modelatlas/?node='+n['id']}]
        c['lesson_markdown']=lesson(c,overlay['skills_note'] if c['id']=='mcp-lab-skill' else '')
        cases.append(c)
    bundle={'schema_version':'mcp.learning.product.v1','checked_at':overlay['checked_at'],'nodes':[],'edges':[],'sources':[dict(s,id='course-'+s['id'],evidence_scope=s['scope']) for s in all_sources],'events':[],'tutorial_paths':[{'title':'MCP、Skill 与提示词 · 十二课（离线模拟契约）','node_ids':[n['id'] for n in nodes],'acceptance':'完整教程与合成输入输出；不是 SDK 兼容或真实效果认证。'}]}
    for n0,c in zip(nodes,cases):
        n=copy.deepcopy(n0);n['source_ids']=['course-'+s for s in c['source_ids']];n['tutorial_markdown']=c['lesson_markdown'];n['raw_record']=n0
        n['agentwork_links']=[{'id':c['id'],'title':c['title'],'url':'https://2codework.github.io/agentwork/?case='+c['id']}]
        n['misconceptions']=c['common_errors'];bundle['nodes'].append(n)
        for prerequisite in n['prerequisites']: bundle['edges'].append({'source':prerequisite,'target':n['id'],'type':'learning_prerequisite','evidence_type':'editorial_learning_order','verification_status':'editorial_learning_relation'})
    return doc['book'],cases,bundle

def lesson(c,note):
    lines=['### 学习目标',c['goal'],'### 前置知识']+['- '+x for x in c['prerequisites']]
    for key,label in [('applicable_versions','固定版本'),('lifecycle','生命周期'),('checked_at','核查日期'),('evidence_note','未实测边界'),('permissions','权限'),('risks','风险'),('failure_recovery','失败处理'),('practice_status','实践证据范围')]:lines+=['### '+label,c[key]]
    if note:lines+=['### 经核验的 Skills 补充说明',note]
    for key,label in [('input','合成输入'),('prompt','可复制审阅提示词'),('output','预期输出')]:lines+=['### '+label,'```'+('json' if key!='prompt' else 'text'),c[key],'```']
    lines+=['### 分步操作']
    for i,s in enumerate(c['steps'],1):lines += [str(i)+'. '+s['body'],'- 验收：'+s['check']]
    lines+=['### 整体验收']+['- '+x for x in c['rubric']]+['### 常见错误']+['- '+x for x in c['common_errors']]
    lines+=['### 离线运行','解压本页课程包后，在包目录运行。命令仅运行原创标准库模拟器，不连接 MCP 服务。','```sh','python validate.py --case '+c['id'],'python -m unittest discover -s tests -v','```','练习文件：'+c['fixture'],'模拟契约通过 ≠ SDK 兼容 ≠ OAuth/真实服务/模型效果验证。参见包内 README 的严格子集与取消竞态限制。','### 来源与支持范围']
    for s in c['sources']:lines+=['- ['+s['title']+']('+s['url']+') · 核查 '+s['checked_at']+' · '+s['claim']]
    return '\n\n'.join(lines)

def publish(root,out):
    shutil.copytree(root/'learning/mcp',out/'learning/mcp',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    with zipfile.ZipFile(out/'mcp-offline-labs.zip','w',zipfile.ZIP_DEFLATED) as z:
        info=zipfile.ZipInfo('VERIFIED-OVERLAY.json',(2026,10,28,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(root/'learning/mcp/overlay.json').read_bytes())
        for p in sorted((root/'learning/mcp/raw').rglob('*')):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
                info=zipfile.ZipInfo(str(p.relative_to(root/'learning/mcp/raw')),(2026,10,28,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
