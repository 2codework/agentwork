import copy,json,sys,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import regional_office as R
class RegionalTests(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/'learning/regional-office/r1/raw/regional-office.json').read_text())
 def test_count_no_mutation_and_identity(self):
  before=copy.deepcopy(self.r);rows=R.adapt(self.r);self.assertEqual(before,self.r);self.assertEqual(len(rows),7)
  for c in rows:
   n=c['raw_record']['id'];self.assertEqual(c['modelatlas_node_ids'],[n]);self.assertEqual(c['regional_office']['platform_family_id'],R.PLATFORM_FAMILIES[n]);self.assertEqual(c['id'],'regional-case-'+n.removeprefix('regional-'));self.assertFalse(c['is_model']);self.assertEqual(c['execution_status'],'never-run')
 def test_seals(self):self.assertEqual(len(R.load(ROOT)),7)
 def test_runtime_rejected(self):
  self.r['entities'][0]['runtime_verified']=True
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_model_rejected(self):
  self.r['entities'][0]['entity_type']='model'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_missing_source(self):
  self.r['entities'][0]['source_ids']=['missing']
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_weak_source_upgrade_rejected(self):
  next(s for s in self.r['sources'] if s['id']=='dingtalk-delegation')['status']='opened'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_aily_alias_rejected(self):
  next(e for e in self.r['entities'] if e['id']=='regional-feishu-aily-enterprise')['aliases'].append('豆包工作伙伴')
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_region_gate_rejected(self):
  next(e for e in self.r['entities'] if e['id']=='regional-bailian-agent-app')['exercise']['steps'][0]='start'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_unsafe_url_rejected(self):
  self.r['sources'][0]['url']='https://user:pass@example.org'
  with self.assertRaises(ValueError):R.adapt(self.r)
 def test_book_and_outputs(self):
  data=json.loads((ROOT/'site/data.json').read_text());self.assertEqual(len(data['cases']),132)
  book=(ROOT/'BOOK.md').read_text()
  for c in R.adapt(self.r):
   for k in ['title','input','risks','historical_context','output']:self.assertIn(c[k],book)
  self.assertEqual((ROOT/'REGIONAL_OFFICE.md').read_bytes(),(ROOT/'learning/regional-office/r1/raw/regional-office.zh.md').read_bytes())
  self.assertEqual((ROOT/'REGIONAL_OFFICE.md').read_bytes(),(ROOT/'docs/REGIONAL_OFFICE.md').read_bytes())
 def test_old_cases_exact(self):
  old=json.loads(subprocess.check_output(['git','show','90b10f0e0e165c35ca7f3b7fa69a1a42216c9985:docs/data.json'],cwd=ROOT));new=json.loads((ROOT/'docs/data.json').read_text());self.assertEqual(new['cases'][:125],old['cases'])
  for k in old:
   if k!='cases':self.assertEqual(new[k],old[k],k)
if __name__=='__main__':unittest.main()
