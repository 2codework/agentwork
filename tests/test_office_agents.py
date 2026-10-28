import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import office_agents as O
class OfficeTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'learning/office-agents/r1/raw';self.r=json.loads((p/'office-agents.json').read_text());self.c=json.loads((p/'raw-cases.json').read_text())
 def test_cardinality_and_preservation(self):
  old=copy.deepcopy((self.r,self.c));cases,b=O.adapt(self.r,self.c);self.assertEqual(old,(self.r,self.c));self.assertEqual((len(cases),len(b['nodes']),len(b['sources']),len(b['events'])),(11,11,18,0));self.assertEqual(len({n['platform_family_id'] for n in b['nodes']}),10)
 def test_links_and_no_mcp_route(self):
  cases,b=O.adapt(self.r,self.c)
  for c,n in zip(cases,b['nodes']):
   self.assertEqual(c['modelatlas_node_ids'],[n['id']]);self.assertNotIn('lesson_markdown',c);self.assertNotIn('tutorial_markdown',n);self.assertIn('never-run',c['evidence_note']);self.assertTrue(n['office_agent']['confirmation_boundary'])
 def test_reject_runtime_claim(self):
  self.r['records'][0]['runtime_verified']=True
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_reject_case_run(self):
  self.c['cases'][0]['execution_status']='passed'
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_reject_model(self):
  self.r['records'][0]['is_model']=True
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_reject_source(self):
  self.r['records'][0]['source_ids']=['absent']
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_reject_missing_entity(self):
  self.r['records'].pop()
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_reject_unsafe_url(self):
  self.r['sources'][0]['url']='https://user:pass@example.org'
  with self.assertRaises(ValueError):O.adapt(self.r,self.c)
 def test_raw_qa_seal_load(self):
  self.assertEqual(len(O.load(ROOT)[0]),11)
if __name__=='__main__':unittest.main()
