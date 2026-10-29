"""Dependency-free, deterministic AgentWork static builder."""
import json, re, shutil, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from normalize import normalize
import asset_versions
import mcp_learning
import creative_workflows
import creative_gaps
import office_agents
import assistant_workspace
import regional_office
import offline_office_lab
import creative_delivery_lab
import product_books
import task_first
from pathlib import Path
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]

def validate(data):
    assert data.get('schema_version') == 1, 'Unsupported schema'
    seen = set()
    for chapter in data['book']:
        assert all(isinstance(chapter.get(k), str) and chapter[k].strip() for k in ['id','title','body','exercise']), 'Invalid chapter'
    for c in data['cases']:
        assert re.fullmatch(r'[a-z0-9-]{1,80}', c['id']) and c['id'] not in seen, 'Invalid/duplicate ID'
        seen.add(c['id'])
        for k in ['title', 'summary', 'evidence']:
            assert isinstance(c[k], str) and c[k].strip(), k
        assert c['evidence'] in ['synthetic', 'primary', 'secondary'], 'Invalid evidence'
        assert isinstance(c['synthetic'], bool)
        assert c['lifecycle'] in ['current','superseded','deprecated','historical','unknown'], 'Invalid lifecycle'
        for field in ['applicable_versions','lifecycle_as_of','historical_context','practice_status']:
            assert isinstance(c[field],str) and c[field].strip(), field
        assert isinstance(c['replacement_case'],str)
        if c['lifecycle'] != 'unknown':
            assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',c['lifecycle_as_of']), 'Lifecycle verification date required'
        assert (c['evidence'] == 'synthetic') == c['synthetic'], 'Synthetic mismatch'
        for k in ['roles', 'industries']:
            assert isinstance(c[k], list) and c[k] and all(isinstance(v, str) and v for v in c[k]), k
        assert isinstance(c['steps'], list) and c['steps']
        for step in c['steps']:
            assert all(isinstance(step.get(k), str) and step[k].strip() for k in ['title','body','check'])
        assert isinstance(c['sources'], list)
        if not c['synthetic']: assert c['sources'], 'Evidence needs sources'
        for source in c['sources']:
            assert source['title'] and source['evidence'] in ['primary','secondary','reference']
            u = urlparse(source['url'])
            assert u.scheme == 'https' and u.hostname and not u.username and not u.password, 'Unsafe source URL'
    return data

def build():
    task_first.preflight_build(ROOT)
    data = validate(json.loads((ROOT/'content/cases.json').read_text()))
    data['chapters'] = []
    for p in sorted((ROOT/'research').glob('*.json')):
        doc = json.loads(p.read_text())
        data['cases'].extend(normalize(p.stem,doc))
        data['chapters'].append({'id':p.stem,'title':{'roles':'岗位地图','learning':'学习方法','industries':'行业地图'}.get(p.stem,p.stem), 'data':doc})
    chapters, lessons, _ = mcp_learning.load(ROOT)
    data["book"].extend(chapters)
    data["cases"].extend(lessons)
    creative_cases, _ = creative_workflows.load(ROOT)
    data["cases"].extend(creative_cases)
    office_cases, _ = office_agents.load(ROOT)
    data["cases"].extend(office_cases)
    data["cases"].extend(assistant_workspace.load(ROOT))
    data["cases"].extend(regional_office.load(ROOT))
    data["cases"].extend(creative_gaps.load(ROOT))
    validate(data)
    write_book(data)
    dest = ROOT/'site'
    dest.mkdir(exist_ok=True)
    for p in (ROOT/'web').iterdir():
        if p.is_file(): shutil.copyfile(p, dest/p.name)
    (dest/'data.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',',':'))+'\n')
    mcp_learning.publish(ROOT,dest)
    creative_workflows.publish(ROOT,dest)
    office_agents.publish(ROOT,dest)
    assistant_workspace.publish(ROOT,dest)
    regional_office.publish(ROOT,dest)
    offline_office_lab.publish(ROOT,dest)
    creative_gaps.publish(ROOT,dest)
    creative_delivery_lab.publish(ROOT,dest)
    product_books.publish(ROOT,dest)
    task_first.publish(ROOT,dest)
    (dest/'.nojekyll').touch()
    shutil.copy2(ROOT/'BOOK.md',dest/'BOOK.md')
    asset_versions.pin(dest)
    shutil.copytree(dest,ROOT/'docs',dirs_exist_ok=True)
    print(f'Built {len(data["cases"])} cases + {len(data["chapters"])} research chapters → site/')
def write_book(data):
    lines=['# AgentWork · 开放实践手册', '', '> 自动从 content/ 与 research/ 生成；不要手工维护此文件。MCP 深教程整合候选，既有站点已上线；合成练习非真实部署证据。', '']
    for chapter in data['book']:
        lines += ['## '+chapter['title'], '', chapter['body'], '', '**练习：** '+chapter['exercise'], '']
    for case in data['cases']:
        if 'lesson_markdown' in case:
            lines += ['## '+case['title'],case['lesson_markdown'], '- 对应技术：'+case['modelatlas_links'][0]['url'], '<details><summary>原始资料 · 历史采集快照</summary>', '```json', json.dumps(case['raw_record'],ensure_ascii=False,indent=2), '```', '</details>']
            continue
        lines += ['## '+case['title'], '', case['summary'], '', '**证据边界：** '+case.get('evidence_note','原创合成案例，未实测'), '']
        for key,label in [('input','合成输入'),('prompt','提示词'),('output','输出模板'),('risks','风险与授权'),('checked_at','来源核查日期'),('lifecycle','生命周期'),('applicable_versions','适用版本'),('lifecycle_as_of','生命周期确认时间'),('replacement_case','替代案例'),('historical_context','历史与适用边界'),('practice_status','最佳实践证据状态')]:
            if key in case: lines += ['### '+label, '',case[key], '']
        for i,step in enumerate(case['steps']): lines += [f"### {i+1}. {step['title']}", '',step['body'], '', '**验收：** '+step['check'], '']
        for x in case.get('modelatlas_links',[]): lines+=['- 对应技术（编辑学习关系）：['+x['title']+']('+x['url']+')']
        for key in ['agent_boundary','cost','compute_cost','permissions']:
            if key in case: lines+=['- '+key+'：'+str(case[key])]
        for item in case.get('rubric',[]): lines += ['- 验收：'+item]
        for source in case['sources']: lines += ['- 来源：'+source['title']+' — '+source['url']+'（核查：'+source.get('checked_at','未提供')+'）', source.get('claim','')]
        if 'raw_record' in case: lines += ['', '<details><summary>完整研究记录（保留所有原字段）</summary>', '', '```json', json.dumps(case['raw_record'],ensure_ascii=False,indent=2), '```', '</details>', '']
    (ROOT/'BOOK.md').write_text('\n'.join(lines).rstrip()+'\n')
if __name__ == '__main__': build()
