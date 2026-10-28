import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creative_r2',ROOT/'scripts/creative_workflows.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
class CreativeWorkflowsTests(unittest.TestCase):
 def setUp(self): self.raw=json.loads((ROOT/'learning/creative/r2/creative-workflows-r2.json').read_text())
 def reject(self,fn):
  fn(self.raw)
  with self.assertRaises((ValueError,KeyError,TypeError)):C.adapt(self.raw)
 def test_preserves_all_raw_and_does_not_mutate(self):
  before=copy.deepcopy(self.raw);cases,bundle=C.adapt(self.raw);self.assertEqual(self.raw,before);self.assertEqual(bundle['raw_research'],before)
  self.assertEqual(len(cases),9);self.assertEqual(len(bundle['nodes']),6)
  for c,raw in zip(cases,self.raw['cases']):self.assertEqual(c['raw_record'],raw)
 def test_visible_case_fields_retain_instruction_and_bounds(self):
  cases,_=C.adapt(self.raw)
  for c,r in zip(cases,self.raw['cases']):
   visible='\n'.join([c['prompt'],c['risks'],c['output'],c['applicable_versions'],c['agent_boundary']]+[s['body'] for s in c['steps']]+c['rubric'])
   for text in r['prerequisites']+r['inputs']+r['outputs']+r['failure_modes_and_recovery']+r['acceptance_criteria']+[r['licensing_caveats'],r['version_caveats'],r['safe_sandbox_exercise']['task'],r['safe_sandbox_exercise']['expected']]:self.assertIn(text,visible)
   self.assertNotIn('lesson_markdown',c)
 def test_unknown_lifecycle_not_tool_deprecation(self):
  cases,bundle=C.adapt(self.raw);self.assertTrue(all(c['lifecycle']=='unknown' for c in cases));self.assertTrue(all(n['lifecycle']=='unknown' and n['type']=='tool' for n in bundle['nodes']));self.assertEqual(cases[0]['raw_record']['lifecycle'],'historical_documentation_retained')
 def test_reuses_ffmpeg_no_invented_events(self):
  _,b=C.adapt(self.raw);self.assertNotIn('vid-ffmpeg',[n['id'] for n in b['nodes']]);self.assertEqual(b['events'],[]);self.assertEqual(b['edges'],[])
 def test_duplicate_case(self):self.reject(lambda d:d['cases'].__setitem__(1,copy.deepcopy(d['cases'][0])))
 def test_duplicate_source(self):self.reject(lambda d:d['sources'].__setitem__(1,copy.deepcopy(d['sources'][0])))
 def test_missing_source(self):self.reject(lambda d:d['cases'][0].update(source_ids=['missing']))
 def test_bad_mapping(self):self.reject(lambda d:d['cases'][0]['modelatlas_links'][0].update(node_id='missing'))
 def test_execution_claim(self):self.reject(lambda d:d['cases'][0]['verification'].update(product_executed=True))
 def test_sandbox_claim(self):self.reject(lambda d:d['cases'][0]['safe_sandbox_exercise'].update(status='passed'))
 def test_bad_lifecycle(self):self.reject(lambda d:d['cases'][0].update(lifecycle='current'))
 def test_unsafe_source(self):self.reject(lambda d:d['sources'][0].update(url='javascript:alert(1)'))
 def test_missing_acceptance(self):self.reject(lambda d:d['cases'][0].update(acceptance_criteria=[]))
 def test_missing_permissions(self):self.reject(lambda d:d['cases'][0].update(permissions=''))
 def test_invented_date(self):self.reject(lambda d:d['sources'][0].update(publication_date='2026-01-01'))
 def test_wrong_step_order(self):self.reject(lambda d:d['cases'][0]['steps'][0].update(order=5))
 def test_second_pass_statistics_and_dedup_correction(self):
  cases,_=C.adapt(self.raw);l=next(c for c in cases if c['id'].endswith('loudness-two-pass'));self.assertIn('print_format=json',l['steps'][3]['body']);self.assertIn('print_format=json',l['steps'][4]['body']);s=next(c for c in cases if c['id'].endswith('sprite-sheet'));self.assertIn('传统关键帧',s['raw_record']['non_duplicate_rationale'])
