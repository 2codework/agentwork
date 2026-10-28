"""Original offline adapter tests, not creative product tests."""
import copy,hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creative_gaps',ROOT/'scripts/creative_gaps.py');G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
class CreativeGapTests(unittest.TestCase):
 def setUp(self):self.raw=json.loads((ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text())
 def reject(self,fn):
  fn(self.raw)
  with self.assertRaises((ValueError,KeyError,TypeError)):G.adapt(self.raw)
 def test_raw_preserved(self):
  before=copy.deepcopy(self.raw);cases=G.adapt(self.raw);self.assertEqual(before,self.raw);self.assertEqual(len(cases),6)
  for c,r in zip(cases,before['candidates']):self.assertEqual(c['raw_record'],r)
 def test_raw_byte_manifest(self):self.assertEqual(len(G.load(ROOT)),6)
 def test_classifications(self):
  cases=G.adapt(self.raw);self.assertEqual(sum(c['creative_learning']['entity_type']=='deterministic_software_workflow' for c in cases),4)
  self.assertEqual(sum(c['creative_learning']['entity_type']=='agentic_application_feature' for c in cases),1)
  self.assertEqual(sum(c['creative_learning']['entity_type']=='conversational_ai_assistant' for c in cases),1)
 def test_mapping(self):
  for c in G.adapt(self.raw):
   nid,kind=G.MAPPING[c['id']];self.assertEqual(c['modelatlas_node_ids'],[nid]);self.assertEqual(c['modelatlas_links'][0]['id'],nid);self.assertEqual(c['modelatlas_links'][0]['status'],'editorial_mapping')
 def test_all_boundaries_visible(self):
  for c,r in zip(G.adapt(self.raw),self.raw['candidates']):
   text='\n'.join([c['summary'],c['prompt'],c['risks'],c['license'],c['cost'],c['agent_boundary'],c['applicable_versions']]+[s['body'] for s in c['steps']]+c['rubric'])
   for value in r['visible_documented_path']+r['original_exercise']['acceptance_checks']+[r['access_and_payment'],r['license_and_rights'],r['automation_boundary']]:self.assertIn(value,text)
 def test_rollback_and_express(self):
  text=json.dumps(G.adapt(self.raw),ensure_ascii=False)
  for word in ['当前session','Version history','compositions/files','刷新','协作者','批准','Chats','中国','未列中文','未确认']:self.assertIn(word,text)
 def test_font_observations_both_retained(self):
  c=next(c for c in G.adapt(self.raw) if c['id']=='gap-indesign-preflight');s=next(s for s in c['sources'] if s['title']=='font-rights');self.assertIn('原观察：opened_primary',s['claim']);self.assertIn('独立QA：tool_open_error',s['claim'])
 def test_baseline_132_and_top_level_frozen(self):
  f=json.loads((ROOT/'tests/fixtures/creative-learning-baseline.json').read_text());d=json.loads((ROOT/'site/data.json').read_text());h=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  self.assertEqual(len(f['cases']),132);self.assertEqual({c['id']:h(c) for c in d['cases'] if c['id'] in f['cases']},f['cases']);self.assertEqual({k:h(v) for k,v in d.items() if k!='cases'},f['other_top_level']);self.assertEqual({c['id'] for c in d['cases']}-set(f['cases']),set(G.MAPPING));self.assertEqual(len(d['cases']),138)
 def test_book_case_and_sources(self):
  book=(ROOT/'BOOK.md').read_text()
  for c in G.adapt(self.raw):
   self.assertIn('## '+c['title'],book)
   for s in c['sources']:self.assertIn(s['url'],book)
 def test_no_actual_run(self):self.assertTrue(all(c['creative_learning']['execution_status']=='never-run' and c['evidence']=='synthetic' and c['lifecycle']=='unknown' for c in G.adapt(self.raw)))
 def test_unknown_schema(self):self.reject(lambda d:d.update(schema_version='unknown'))
 def test_duplicate_case(self):self.reject(lambda d:d['candidates'].__setitem__(1,copy.deepcopy(d['candidates'][0])))
 def test_duplicate_source(self):self.reject(lambda d:d['sources'].__setitem__(1,copy.deepcopy(d['sources'][0])))
 def test_missing_source(self):self.reject(lambda d:d['candidates'][0].update(source_ids=['missing']))
 def test_unsafe_source(self):self.reject(lambda d:d['sources'][0].update(url='javascript:alert(1)'))
 def test_invented_date(self):self.reject(lambda d:d['candidates'][0]['lifecycle'].update(release_date='2026-10-28'))
 def test_agent_misclassification(self):self.reject(lambda d:d['candidates'][2].update(entity_type='agentic_application_feature'))
 def test_run_claim(self):self.reject(lambda d:d['candidates'][0]['verification'].update(product_run=True))
 def test_missing_steps(self):self.reject(lambda d:d['candidates'][0].update(visible_documented_path=[]))
 def test_missing_acceptance(self):self.reject(lambda d:d['candidates'][0]['original_exercise'].update(acceptance_checks=[]))
 def test_source_evidence_upgrade(self):self.reject(lambda d:d['sources'][0].update(status='product_tested'))
if __name__=='__main__':unittest.main()

class OriginalExercisePlanTests(unittest.TestCase):
 def test_shared_original_plan_hash_and_fields(self):
  b=(ROOT/'learning/creative-gaps/exercise-plans.json').read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),G.PLAN_SHA256)
  plans=json.loads(b);cases=G.load(ROOT);self.assertEqual(len(cases),6)
  for c in cases:
   p=plans['plans'][c['id']];self.assertEqual(c['original_exercise_plan'],p);visible=json.dumps({k:v for k,v in c.items() if k not in ['raw_record','original_exercise_plan']},ensure_ascii=False)
   for token in [p['task'],plans['note']]+p['steps']+p['expected_artifacts']+p['stop_conditions']:self.assertIn(token,visible)
   self.assertEqual(len([s for s in c['steps'] if s['title'].startswith('原创练习步骤')]),4)
 def test_plan_rejects_execution_and_missing_step(self):
  raw=json.loads((ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text());cases=G.adapt(raw);p=json.loads((ROOT/'learning/creative-gaps/exercise-plans.json').read_text());p['execution_status']='passed'
  with self.assertRaises(ValueError):G.attach_exercises(cases,p)
  p['execution_status']='never-run';p['plans']['gap-underlord-review']['steps'].pop()
  with self.assertRaises(ValueError):G.attach_exercises(cases,p)


class CreativeRawAliasingRegressionTests(unittest.TestCase):
 def test_loaded_raw_exactly_equals_each_r2_candidate(self):
  raw=json.loads((ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text())
  originals={c['id']:c for c in raw['candidates']}
  for c in G.load(ROOT):self.assertEqual(c['raw_record'],originals[c['id']])
 def test_attach_does_not_mutate_input_or_share_rubric_with_raw(self):
  raw=json.loads((ROOT/'learning/creative-gaps/raw/creative-learning-gap-research-r2/creative-learning-gap-research-r2.json').read_text());cases=G.adapt(raw);before=copy.deepcopy(cases)
  plans=json.loads((ROOT/'learning/creative-gaps/exercise-plans.json').read_text());out=G.attach_exercises(cases,plans)
  self.assertEqual(cases,before)
  for c,old in zip(out,before):
   self.assertEqual(c['raw_record'],old['raw_record']);self.assertIsNot(c['rubric'],c['raw_record']['original_exercise']['acceptance_checks'])
   saved=copy.deepcopy(c['raw_record']);c['rubric'].append('regression-only mutation probe');self.assertEqual(c['raw_record'],saved)
  self.assertEqual(cases,before)
