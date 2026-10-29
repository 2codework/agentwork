from pathlib import Path
import json,hashlib,csv,re
from decimal import Decimal
P=Path(__file__).resolve().parent
load=lambda f:json.loads((P/f).read_text())
d=load('recipes.json');b=load('product-book.json');sources=load('sources.json')
assert len(d['recipes'])==len(b['recipes'])==8 and len(sources)==16
ids={s['id'] for s in sources};hashes=0;negative=0;total_outputs=0
# This validates authored references ONLY; no product adapter/tool invocation.
def delivery_gate(required,files):
 return all(name in files and isinstance(files[name],str) and bool(files[name].strip()) for name in required)
for r in d['recipes']:
 assert r['execution_status']==r['ui_execution']=='not_run' and r['runner_implemented'] is False
 assert r['reference_kind']=='complete_author_reference' and r['reference_coverage']['uncovered_files']==[]
 assert set(r['source_ids'])<=ids
 assert len(r['rubric'])==5 and sum(x['points'] for x in r['rubric'])==100
 assert r['hard_gates'] and r['business_hard_failures']
 for x in r['inputs']:
  p=(P/x['path']).resolve();assert p.is_relative_to(P)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'];hashes+=1
 files={Path(f).name:(P/f).read_text() for f in r['reference_files']}
 assert set(files)==set(r['expected_outputs'])
 assert delivery_gate(r['expected_outputs'],files);total_outputs+=len(files)
 for missing in r['expected_outputs']:
  bad=dict(files);del bad[missing];assert not delivery_gate(r['expected_outputs'],bad);negative+=1
  bad=dict(files);bad[missing]=' \n';assert not delivery_gate(r['expected_outputs'],bad);negative+=1
 assert 'not_run' in files['audit.md'] and '人工授权证据' in files['audit.md']
 for name,body in files.items():
  if name.endswith('.csv'):
   rows=list(csv.reader(body.splitlines()));assert len(rows)>1 and all(len(row)==len(rows[0]) for row in rows)
 for name in ['cost','privacy','authorization','version_scope']:
  x=next(z for z in b['recipes'] if z['recipe_id']==r['id']);assert isinstance(x[name],str) and x[name]
 assert x['observed_results'] is None and x['product_execution']==x['ui_execution']=='not_run'
 assert x['runner_implemented'] is False and x['third_party']
 for i,step in enumerate(x['steps']):
  assert step['status']==r['ui_steps'][i]['status'] and step['source_id']==r['ui_steps'][i].get('source_id')
# Count fixed body region using predetermined basic CJK rule.
post=(P/'recipes/content/author-reference-complete/post.md').read_text()
body=post.split('## 正文\n',1)[1].split('\n## ',1)[0]
count=len(re.findall(r'[\u4e00-\u9fff]',body));assert 150<=count<=220,count
# Independent reference numeric checks, not executing fixture code.
folder=P/'recipes/data/author-reference-complete'
clean=list(csv.DictReader((folder/'clean.csv').open()));exc=list(csv.DictReader((folder/'exceptions.csv').open()));summary=list(csv.DictReader((folder/'summary.csv').open()))
assert [int(x['row_id']) for x in clean]==[1,2,4,5]
assert [int(x['row_id']) for x in exc]==[3,6,7]
assert all(Decimal(x['net'])==Decimal(x['gross'])-Decimal(x['refund']) for x in clean)
expected={('CNY','东'):Decimal(190),('CNY','西'):Decimal(80),('USD','西'):Decimal(50)}
observed={(x['currency'],x['region']):Decimal(x['net']) for x in summary};assert observed==expected
# The oracle must reject common wrong candidates, including a one-unit error.
wrong_cases=[{('CNY','东'):Decimal(190),('CNY','西'):Decimal(160),('USD','西'):Decimal(50)}, {('CNY','东'):Decimal(190),('CNY','西'):Decimal(81),('USD','西'):Decimal(50)}, {('ALL','ALL'):Decimal(320)}]
for candidate in wrong_cases:assert candidate!=expected;negative+=1
# Operational evidence is deliberately absent: not_run reference audit cannot pass a real run gate.
def run_gate(record):
 return record.get('product_execution') in ['passed','failed'] and all(record.get(k) for k in ['plan','approval','tool_log','before_hashes','after_hashes','human_citation_review'])
assert not run_gate({'product_execution':'not_run'});negative+=1
full=dict(product_execution='passed',plan='test-only dummy',approval='test-only dummy',tool_log='test-only dummy',before_hashes={'x':'a'},after_hashes={'x':'a'},human_citation_review='test-only dummy')
for key in ['plan','approval','tool_log','before_hashes','after_hashes','human_citation_review']:
 bad=dict(full);bad[key]=None;assert not run_gate(bad);negative+=1
result={'structure':'passed','complete_author_reference_cases':8,'complete_reference_files':total_outputs,'input_hashes_verified':hashes,'negative_tests_passed':negative,'content_body_basic_cjk_count':count,'author_data_oracle':'passed','product_execution':'not_run','ui_execution':'not_run','runner_implemented':False,'scope':'研究包/参考文件结构与作者数值锚点；未自动判定人工事实/语气/引用覆盖，不是产品验收','real_run_evidence_gate':'not_passed_not_run'}
(P/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
