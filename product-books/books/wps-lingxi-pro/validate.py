import json,pathlib,hashlib,copy,importlib.util,itertools
P=pathlib.Path(__file__).parent
d=json.loads((P/'playbooks.json').read_text());checks=[]
assert len(d['recipes'])==8
assert d['content_license']=='pending' and d['execution']=='not_run'
assert d['identity_resolution']['resolution']=='multiple_distinct_products_catalogued'
assert d['identity_resolution']['canonical_alias_assignment'] is None
assert len(d['sources'])<=16
assert len({r['id'] for r in d['recipes']})==8
sources={s['id'] for s in d['sources']};protocol={p['id'] for p in d['onboarding']}
spec=importlib.util.spec_from_file_location('evaluator',P/'evaluator.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
for r in d['recipes']:
 assert r['execution']=='not_run' and r['expected']['status']=='expected_not_observed'
 assert r['prompt'] and r['input']['synthetic'] and r['rubric']['human'] and r['negative_test']
 assert set(r['sources'])<=sources
 assert all(s['protocol_ref'] in protocol for s in r['steps'])
 assert (P/r['input']['path']).read_text()==r['input']['full_text']
 want=json.loads((P/r['expected']['fixture_path']).read_text())
 assert want==r['expected']['machine_sidecar']
 assert not ev.compare(want,want)
 bad=copy.deepcopy(want);del bad[next(iter(bad))];assert ev.compare(want,bad)
 bad=copy.deepcopy(want);bad[next(iter(bad))]={'bad':'type'};assert ev.compare(want,bad)
 checks.append({'recipe':r['id'],'structure':'pass','evaluator_expected_fixture_selftest':'pass','evaluator_missing_key_negative':'pass','evaluator_wrong_type_negative':'pass','product_execution':'not_run','human_artifact_review':'not_run'})
# Independently prove the HR unsatisfiability using all distinct module orders and bins.
modules={'安全基础':2,'产品演示':3,'工单演练':2,'复盘':1}
solutions=[]
for order in itertools.permutations(modules):
 if order.index('安全基础')>order.index('工单演练') or order[-1]!='复盘':continue
 for i in range(5):
  for j in range(i,5):
   bins=[order[:i],order[i:j],order[j:]]
   if all(sum(modules[m] for m in b)<=cap for b,cap in zip(bins,[3,3,2])):solutions.append(bins)
assert not solutions
report={'status':'pass','scope':'artifact structure and original evaluator selftests only','product_execution':'not_run','official_ui_execution':'not_run','recipe_count':len(checks),'checks':checks,'hr_constraint_exhaustive_check':'no feasible ordering for 3/3/2 capacities and indivisible modules','source_count':len(sources)}
(P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
