from pathlib import Path
import importlib.util,json,hashlib
P=Path(__file__).parent
f=P.parent/'agentwork-product-bench-r1/agentwork/scripts/product_books.py'
s=importlib.util.spec_from_file_location('product_books',f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
b=m.load(P/'product-book.json')
m.text_fields(b['product'],['product_id','vendor','name','display_name','version_scope'])
for src in b['product']['sources']: m.source(src)
for r in b['recipes']: m.validate_record(r,P,True)
assert b['aliases']['zcode']['default'] is None
assert len(b['research_record']['candidates'])==2
assert b['research_record']['content_license_status']=='pending_owner_confirmation_unchanged'
assert len(b['product']['channel_versions'])==3
# Non-product semantic assertions on author reference data.
a=json.loads((P/'fixtures/pm-spec/reference/acceptance.json').read_text())
assert all(all(v.get(k) for k in ['given','when','then']) for v in a)
assert a[2]['additional_released_seats']==0
assert 'load'==json.loads((P/'fixtures/security-review/reference/review.json').read_text())['findings'][0]['function']
assert (P/'fixtures/refund-fix/reference/rationale.md').stat().st_size>0
for r in b['recipes']:
 assert len(r['objective_checks'])>=3
 assert len(r['expected_output_artifacts'])==len(r['expected_output']['files'])
 assert r['product_execution']=='not_run' and r['observed_results'] is None
report={'status':'pass','checks':'8 framework records plus product/source/identity/channel preservation and semantic completeness assertions','validator_path':str(f),'validator_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'product_execution':'not_run','runner_implemented':False,'observed_results':None}
(P/'FRAMEWORK_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
