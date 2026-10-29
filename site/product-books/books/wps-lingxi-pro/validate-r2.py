import json,pathlib,hashlib,importlib.util,copy
P=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('ev',P/'evaluator.py');ev=importlib.util.module_from_spec(s);s.loader.exec_module(ev)
b=json.loads((P/'product-book.json').read_text());checks=[]
for r in b['recipes']:
 assert r['product_id']=='wps-lingxi-pro' and r['task_id'] is None
 assert r['runner_implemented'] is False and r['product_execution']=='not_run' and r['observed_results'] is None
 for k in ['reference_format','expected_product_artifact_format','step_evidence','negative_test','rubric','evaluator_command','evidence_boundary']:assert r[k]
 ref=r['complete_author_reference'];data=(P/ref['path']).read_bytes();assert len(data)>900 and hashlib.sha256(data).hexdigest()==ref['sha256']
 slug=r['recipe_id'].removeprefix('wps-lingxi-pro-');folder=P/'fixtures'/slug
 want=ev.load_strict(folder/'expected.json');assert not ev.compare(want,want)
 for name in ['negative-missing-key.json','negative-wrong-type.json']:assert ev.compare(want,ev.load_strict(folder/name))
 extra=copy.deepcopy(want);extra['unexpected']=1;assert ev.compare(want,extra)
 edge=r['negative_test']['reproducible_variant'];e=ev.load_strict(P/edge['expected']);assert not ev.compare(e,e)
 for k in ['input','prompt','author_reference']:assert (P/edge[k]).stat().st_size>0
 checks.append({'recipe_id':r['recipe_id'],'complete_reference':'present','framework_contract':'pass','negative_fixtures':'pass','reproducible_edge_fixture':'pass','product_execution':'not_run','native_artifact_review':'not_run'})
# Parser regression cases are synthetic local files, never product outputs.
t=P/'fixtures'/'validator-tests';t.mkdir(exist_ok=True)
for name,content in [('duplicate.json','{"a":1,"a":2}'),('nan.json','{"a":NaN}'),('infinity.json','{"a":Infinity}'),('oversize.json',' '*1048577)]:
 path=t/name;path.write_text(content)
 try:ev.load_strict(path);raise AssertionError(name+' wrongly accepted')
 except ValueError:pass
assert ev.compare({'a':True},{'a':1})
assert ev.compare({'a':{'b':1}},{'a':{'b':1,'extra':2}})
report={'status':'pass','scope':'local author-material/contract/evaluator tests only','recipes':checks,'strict_json_tests':['duplicate rejected','NaN rejected','Infinity rejected','oversize rejected','bool not number','nested extra key rejected'],'product_execution':'not_run','native_artifacts_created':False}
(P/'validation-r2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
