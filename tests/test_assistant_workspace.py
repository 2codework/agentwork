import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import assistant_workspace as A
class AssistantTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'learning/assistant-workspace/r1/raw';self.r=json.loads((p/'research.json').read_text());self.s=json.loads((p/'sources.json').read_text())
 def test_cardinality_no_mutation_and_links(self):
  before=copy.deepcopy((self.r,self.s));c=A.adapt(self.r,self.s);self.assertEqual(before,(self.r,self.s));self.assertEqual(len(c),8)
  for row in c:
   self.assertEqual(row['modelatlas_node_ids'],[row['raw_record']['id']]);self.assertIn('未知',row['summary']);self.assertIn('never-run',row['summary']);self.assertNotIn('office_agent',row);self.assertNotIn('lesson_markdown',row);self.assertFalse(row['is_model']);self.assertIn('确认',row['risks'])
 def test_approved_load_preserves_snapshots(self):self.assertEqual(len(A.load(ROOT)),8)
 def test_agent_document_conflict_not_retirement(self):
  c=A.adapt(self.r,self.s)[0];self.assertIsNone(c['raw_record']['dates']['retirement']);self.assertIn('冲突',c['historical_context']);self.assertEqual(c['lifecycle'],'unknown')
 def test_reject_execution(self):
  self.r['items'][0]['execution']['model_called']=True
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_retirement(self):
  self.r['items'][0]['dates']['retirement']='2026-10-28'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_ambiguous_iso(self):
  self.r['items'][-1]['dates']['normalized_date']='2026-02-05'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_source_date(self):
  next(s for s in self.s if s['id']=='p-feb-change')['event_date']='2026-02-05'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_failed_source_upgrade(self):
  next(s for s in self.s if s['id']=='p-labs')['evidence_status']='verified'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_missing_source(self):
  self.r['items'][0]['source_ids']=['missing']
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_model_type(self):
  self.r['items'][0]['entity_type']='model'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_reject_url_credentials(self):
  self.s[0]['url']='https://user:pass@example.com'
  with self.assertRaises(ValueError):A.adapt(self.r,self.s)
 def test_generated_total_and_book(self):
  data=json.loads((ROOT/'site/data.json').read_text());self.assertEqual(len(data['cases']),138);self.assertEqual(len([x for x in data['cases'] if x.get('office_agent')]),11)
  book=(ROOT/'BOOK.md').read_text()
  for c in A.adapt(self.r,self.s):
   self.assertIn(c['title'],book);self.assertIn(c['risks'],book);self.assertIn(c['historical_context'],book)
if __name__=='__main__':unittest.main()
