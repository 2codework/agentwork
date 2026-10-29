raise SystemExit("One-time r2 remediation is frozen; use check_structure/validate_pack/test_regressions to verify.")
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
def read(p):return json.loads((R/p).read_text())
def write(p,x):(R/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Domain contract: zero-value rows are valid, preserving integer-only nonnegative cents.
f=R/'recipes/cx06-sales-script/fixture/policy.md';f.write_text(f.read_text().replace('金额正整数分','金额非负整数分（允许 0）'))
# Add deliverable/behavior assertions, not subjective prose gates.
extras={
'cx04-legacy-map':'''\nassert {ex['input'] for ex in d['examples']} == set(json.loads((ROOT/'samples.json').read_text())), 'must cover supplied inputs exactly'\nassert len(d['examples']) == len(json.loads((ROOT/'samples.json').read_text()))\nassert {s['file'] for s in d['change_seams']} == {'parser.py','scoring.py'}\nassert all(isinstance(s['purpose'],str) and s['purpose'].strip() for s in d['change_seams'])\nassert (ROOT/'ONBOARDING.md').read_text().strip(), 'empty onboarding'\n''',
'cx05-money-migration':'''\nassert (ROOT/'MIGRATION.md').read_text().strip(), 'missing or empty migration document'\nassert d['approval_required_before']=='cutover'\nassert d['mapping']=={'id':'id','amount_cents':'money.amount_cents','currency':'CNY'}\n''',
'cx06-sales-script':'''\nimport subprocess\nwant={'net_cents':{'north':800,'south':700},'duplicate_rows':1}\nassert json.loads((ROOT/'expected.json').read_text())==want, 'incorrect expected.json'\ncli=subprocess.run([sys.executable,'-B',str(ROOT/'summarize.py'),str(ROOT/'orders.csv')],capture_output=True,text=True,timeout=10)\nassert cli.returncode==0, cli.stderr\nassert json.loads(cli.stdout)==want, 'CLI must emit the expected JSON object'\nwith tempfile.TemporaryDirectory() as temp:\n    zero=pathlib.Path(temp)/'zero.csv';zero.write_text('id,region,amount_cents,status\\nz,north,0,paid\\n')\n    assert m.summarize(zero)=={'net_cents':{'north':0},'duplicate_rows':0}\n''',
'cx07-triage-prototype':'''\nassert (ROOT/'MANUAL-QA.md').read_text().strip(), 'missing or empty manual QA checklist'\n'''
}
for id,extra in extras.items():
 f=R/f'recipes/{id}/acceptance.py';text=f.read_text()
 # Print only after all checks, so failed runs never print a misleading PASS first.
 lines=text.splitlines();prints=[line for line in lines if line.startswith("print('PASS:")];text='\n'.join(line for line in lines if not line.startswith("print('PASS:"))+'\n'+extra+'\n'+'\n'.join(prints)+'\n'
 # Refresh gate hash for changed synthetic policy only.
 if id=='cx06-sales-script':
  import re,ast
  match=re.search(r'^_preserved=(.*)$',text,re.M);pres=ast.literal_eval(match.group(1));pres['policy.md']=hashlib.sha256((R/f'recipes/{id}/fixture/policy.md').read_bytes()).hexdigest();text=text[:match.start()]+f'_preserved={pres!r}'+text[match.end():]
 f.write_text(text)
book=read('product-book.json');pack=read('recipes.json');pack['suite']='agentwork-codex-playbooks-r2'
formats={
'cx01-shipping-bug':('Python unified diff and source','Python shipping.py patch'),
'cx02-discount-tests':('Python unittest source and unified diff','Python test_pricing.py unittest suite'),
'cx03-tenant-review':('JSON review and unified diff','JSON review.json with findings and limitations'),
'cx04-legacy-map':('JSON architecture, Markdown onboarding and unified diff','architecture.json plus ONBOARDING.md'),
'cx05-money-migration':('JSON migration plan, Markdown narrative and unified diff','migration-plan.json plus MIGRATION.md; plan only'),
'cx06-sales-script':('Python script, expected JSON and unified diff','summarize.py function/CLI plus expected.json'),
'cx07-triage-prototype':('HTML prototype, Markdown manual QA and unified diff','index.html plus MANUAL-QA.md; no hosted deployment'),
'cx08-ci-diagnosis':('YAML workflow patch, Markdown diagnosis and unified diff','workflow YAML patch plus DIAGNOSIS.md; hosted CI not run')}
ver='2026-10-29 official documentation snapshot; actual client/model/account/workspace unexecuted. Prefer existing CLI/IDE local. Cloud/app differ; no universal UI or unlimited-free claim.'
product=book['product'];product['version_scope_details']=product['version_scope'];product['version_scope']=ver
for s in product['sources']:s['accessed_at']=s['accessed_at'][:10]
for r in book['recipes']:
 r['product_id']='openai-codex';r['runner_implemented']=False
 r['reference_format'],r['expected_product_artifact_format']=formats[r['recipe_id']]
 r['structured_details']={key:r[key] for key in ['role','authorization','cost','privacy','version_scope']}
 r['role']='；'.join(r['role'])
 r['authorization']='仅允许读合成副本、改指定产物与执行已审阅 stdlib 检查；网络、安装、外部仓库、发布/PR、目录外改动须新批准；禁止秘密/私人会话/生产数据/绕过 sandbox/篡改测试。详见 structured_details.authorization。'
 r['cost']='作者离线检查无模型调用；未来真实运行受订阅额度/credits 或 API 计费，当前 not_run、实际成本未知；限一次初始任务及一次定向修复，额度/权限阻塞即停。详见 structured_details.cost。'
 r['privacy']='仅原创合成数据；不读取秘密或私人会话，不接生产数据，不获准外传。详见 structured_details.privacy。'
 r['version_scope']=ver
 for s in r['sources']:s['accessed_at']=s['accessed_at'][:10]
 for item in r['input_artifacts']:item['sha256']=hashlib.sha256((R/item['path']).read_bytes()).hexdigest()
 r['expected_output_artifacts']=[{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'description':'作者合成参考文件/patch，非 Codex 输出'} for p in r['expected_output']['files']+[r['expected_output']['patch_path']]]
 if r['recipe_id']=='cx06-sales-script':r['objective_checks']+=['expected.json 与 CLI 输出对象均为 north=800/south=700/duplicate_rows=1；0 分有效输入通过。']
 if r['recipe_id']=='cx04-legacy-map':r['objective_checks']+=['样例集合必须完整匹配 samples.json，不允许重复替代；change_seams 指向 parser.py/scoring.py。']
 if r['recipe_id']=='cx05-money-migration':r['objective_checks']+=['MIGRATION.md 非空，映射与切换批准字段正确。']
 if r['recipe_id']=='cx07-triage-prototype':r['objective_checks']+=['MANUAL-QA.md 非空；内容仍需人工审阅，浏览器/读屏未执行。']
 for old in pack['recipes']:
  if old['id']==r['recipe_id']:old['objective_checks']=r['objective_checks'];old['runner_implemented']=False
write('product-book.json',book);write('recipes.json',pack)
# Match stricter framework while retaining all detailed objects as additional declared fields.
schema=read('schema.json');p=schema['properties']['product']['properties'];p['version_scope']={'type':'string'};p['version_scope_details']={'type':'object'}
props=schema['properties']['recipes']['items']['properties']
for key in ['role','authorization','cost','privacy','version_scope','product_id','reference_format','expected_product_artifact_format']:props[key]={'type':'string'}
props['runner_implemented']={'const':False};props['structured_details']={'type':'object'};props['expected_output_artifacts']=props['input_artifacts']
schema['properties']['recipes']['items']['required']+=['product_id','runner_implemented','reference_format','expected_product_artifact_format','structured_details','expected_output_artifacts']
write('schema.json',schema)
# Freeze authoring history: r1 generators remain provenance, not an r2 rebuild command.
for name in ['build_pack.py','adapt_product_book.py']:
 f=R/name;f.write_text('raise SystemExit("Historical r1 authoring source only; r2 is frozen. Do not regenerate over remediation.")\n'+f.read_text())
for name in ['README.md','HANDBOOK.md']:
 f=R/name;f.write_text(f.read_text().replace('agentwork-codex-playbooks-r1','agentwork-codex-playbooks-r2').replace('练习包 r1','练习包 r2'))
