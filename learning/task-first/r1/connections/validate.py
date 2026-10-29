import json, pathlib, tomllib, re, hashlib
P=pathlib.Path(__file__).parent
d=json.loads((P/'connections.json').read_text())
checks=[]
def ck(name, value):
 checks.append({'check':name,'passed':bool(value)})
 assert value,name
ck('three complete routes',len(d['routes'])==3)
ids={s['id'] for s in d['sources']}
for r in d['routes']:
 for key in ['id','title','audience','outcome','product','connection','accounts_cost','minimum_access','steps','prompt','test_input','expected_observations','recovery','disconnect','platform_notes','source_ids']:
  ck(r['id']+' required '+key,bool(r.get(key)))
 ck(r['id']+' valid source refs',set(r['source_ids'])<=ids)
 ck(r['id']+' recovery pairs',all(set(x)=={'symptom','action'} for x in r['recovery']))
 ck(r['id']+' prompt verbatim in Markdown',r['prompt'] in (P/'GUIDE.zh-CN.md').read_text())
for r in d['routes']:
 ck(r['id']+' official start URL',r['start_url'].startswith('https://'))
 ck(r['id']+' first-time onboarding',len(r['onboarding_steps'])>=3)
ck('internal narration absent in learner opening','执行 Mac' not in (P/'GUIDE.zh-CN.md').read_text().split('## 核验边界')[0])
m=d['routes'][1]
ck('TOML parses exact official URL',tomllib.loads(m['config'])['mcp_servers']['openaiDeveloperDocs']['url']=='https://developers.openai.com/mcp')
s=d['routes'][2]
ck('Skill complete metadata',s['config'].startswith('---\nname: meeting-action-list\ndescription: '))
ck('Skill location repo-scoped',s['config_filename']=='.agents/skills/meeting-action-list/SKILL.md')
ck('Skill explicit invocation',s['prompt'].startswith('$meeting-action-list\n'))
ck('No runtime proof claim', '不是产品实跑成绩' in d['verification_scope'])
ck('source dates explicit',all(x['checked_on']=='2026-10-29' for x in d['sources']))
ck('official URLs only',all(x['url'].startswith(('https://learn.chatgpt.com/','https://developers.openai.com/','https://chatgpt.com/')) for x in d['sources']))
ck('No license declaration added',d['license_status']=='No license declaration; no existing license changed.')
ck('Windows TOML parses',tomllib.loads(s['windows_disable_config'])['skills']['config'][0]['path'].startswith('C:/Users/'))
ck('example correction labeled',d['routes'][0]['followup_prompt_label']=='只用于本页虚构 L1–L5 示例')
ck('generic file correction included',d['routes'][0]['file_correction_prompt'] in (P/'GUIDE.zh-CN.md').read_text())
report={'scope':'author-side static checks only; no product runtime/install/login/API execution','checks':checks,'result':'PASS','count':len(checks)}
(P/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(P/'SHA256SUMS.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.iterdir()) if p.is_file() and p.name!='SHA256SUMS.json'},indent=2)+'\n')
print('PASS',len(checks))
