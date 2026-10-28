import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from normalize import normalize
class ResearchTests(unittest.TestCase):
 def setUp(self): self.docs={p.stem:json.loads(p.read_text()) for p in (ROOT/'research').glob('*.json')}
 def test_counts_and_preservation(self):
  for name,doc in self.docs.items():
   cases=normalize(name,doc);self.assertEqual(len(cases),len(doc['cases']))
   for result,original in zip(cases,doc['cases']):
    self.assertEqual(result['raw_record'],original)
    self.assertTrue(result['synthetic']);self.assertTrue(result['prompt']);self.assertTrue(result['rubric']);self.assertTrue(result['checked_at'])
 def test_missing_source_rejected(self):
  d=copy.deepcopy(self.docs['roles']);d['cases'][0]['source_ids']=['missing']
  with self.assertRaises(ValueError):normalize('roles',d)
 def test_missing_field_rejected(self):
  d=copy.deepcopy(self.docs['learning']);del d['cases'][0]['rubric']
  with self.assertRaises(ValueError):normalize('learning',d)
 def test_unknown_adapter_rejected(self):
  with self.assertRaises(ValueError):normalize('unknown',self.docs['roles'])
 def test_no_unreviewed_tested_claim(self):
  d=copy.deepcopy(self.docs['learning']);d['cases'][0]['tested']=True
  with self.assertRaises(ValueError):normalize('learning',d)
if __name__=='__main__':unittest.main()
