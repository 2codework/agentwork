import json,pathlib,hashlib,importlib.util,copy
P=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('ev',P/'evaluator.py');ev=importlib.util.module_from_spec(s);s.loader.exec_module(ev)
b=json.loads((P/'product-book.json').read_text())
required={
'sales-review':['2026-10月','month/channel/revenue','空值当0','october_revenue=null'],
'budget-variance':['行政','actual-budget','/budget*100','budget为0'],
'meeting-actions':['小北','YYYY-MM-DD','dependency','不可信内容'],
'hr-onboarding':['全部模块','不可拆分','同一天数组顺序','安全基础先于工单演练','复盘必须'],
'support-faq':['政策','trial_uses','refund_promised','忽略政策'],
'procurement-matrix':['丙','数量20件','12天','12个月','待核验'],
'marketing-deck':['社区','attendees/registrations*100','spend/attendees','分母为0'],
'operations-sop':['P1','先扫码','重量未知route=人工确认','<=2kg']}
def check_prompt(text,tokens):
 assert all(t in text for t in tokens)
 assert '完整输入：' in text and '独立的边界诊断' in text
results=[]
assert b['product_profile']==b['product']['profile']
for r in b['recipes']:
 slug=r['recipe_id'].removeprefix('wps-lingxi-pro-')
 assert isinstance(r['expected_product_artifact_format'],str) and r['expected_product_artifact_formats']
 text=(P/'fixtures'/slug/'edge-prompt.txt').read_text();check_prompt(text,required[slug])
 for token in required[slug]:
  try:check_prompt(text.replace(token,''),required[slug]);raise RuntimeError('regression failed')
  except AssertionError:pass
 arts=r['input_artifacts']+r['expected_output_artifacts'];names={pathlib.Path(a['path']).name for a in arts}
 assert {'author-reference.md','expected.json','edge-input.txt','edge-prompt.txt','edge-expected.json','edge-author-reference.md'}<=names
 for a in arts:
  data=(P/a['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==a['sha256'];assert data.decode()==a['content']
 edge=ev.load_strict(P/'fixtures'/slug/'edge-expected.json');assert not ev.compare(edge,edge)
 assert r['product_execution']=='not_run' and r['observed_results'] is None and r['runner_implemented'] is False
 results.append({'recipe':r['recipe_id'],'standalone_prompt_contract':'pass','missing_rule_mutations':'rejected','explicit_artifacts_hash_and_content':'pass','product_execution':'not_run'})
t=P/'fixtures'/'validator-tests'/'exponent-overflow.json';t.write_text('{"x":1e999}')
try:ev.load_strict(t);raise AssertionError('nonfinite parsed exponent accepted')
except ValueError:pass
report={'status':'pass','scope':'original local content/contracts only','results':results,'parser_exponent_overflow':'rejected','memory_bound':'stat then bounded read','native_execution':'not_run','product_execution':'not_run'}
(P/'validation-r3.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
