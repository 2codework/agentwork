import unittest,sys,json,hashlib,copy,tempfile,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import office_expansion as office
import task_first
FOLDER=ROOT/'learning/task-first/r1/office-expansion'
RAW=json.loads((FOLDER/'proposed-workflows.json').read_text())
class OfficeExpansion(unittest.TestCase):
 def test_exact_admitted_ids_and_source_phase_bindings(self):
  rows=office.catalog(ROOT);self.assertEqual({w['id'] for w in rows},set(office.IDS));self.assertEqual(len(rows),3)
  for original,w in zip(RAW['recipes'],rows):
   for k,v in original.items():self.assertEqual(w[k],v)
   self.assertEqual(w['reading_phases']['source_record_sha256'],office.record_hash(original))
   self.assertEqual(w['source_phase_mapping']['example'],['result','example'])
 def test_all_seven_inputs_ten_outputs_and_six_zips_are_complete(self):
  rows=office.catalog(ROOT);self.assertEqual(sum(len(w['input_files']) for w in rows),7);self.assertEqual(sum(len(w['output_files']) for w in rows),10)
  for w in rows:
   for key,items in [('download_bundle',w['input_files']),('reference_bundle',w['output_files'])]:
    office.verify_zip(FOLDER,w[key],items)
    self.assertTrue((ROOT/'site'/(w['asset_base']+w[key])).is_file())
 def test_phase_payloads_ids_and_nested_types_reject_independently_of_admission_pin(self):
  for kind in ['missing','reordered','null','result','check','text','extra']:
   w=copy.deepcopy(RAW['recipes'][0])
   if kind=='missing':w['phases'].pop()
   elif kind=='reordered':w['phases'][4],w['phases'][5]=w['phases'][5],w['phases'][4]
   elif kind=='null':w['phases'][1]=None
   elif kind=='result':w['phases'][4]['steps']=['pretend executed']
   elif kind=='check':w['phases'][6]['checks']=[False]
   elif kind=='text':w['phases'][3]['text']=False
   else:w['phases'][5]['hidden_execution']=True
   with self.subTest(kind=kind),self.assertRaises(ValueError):office.validate_phases(w)
 def test_file_paths_hashes_origins_and_text_list_types_reject(self):
  for value in [None,{},[None],[123],[]]:
   with self.subTest(value=value),self.assertRaises(ValueError):office.texts(value)
  for kind in ['path','hash','origin','duplicate','content']:
   items=copy.deepcopy(RAW['recipes'][0]['output_files'])
   if kind=='path':items[0]['path']='outputs/../secret.md'
   elif kind=='hash':items[0]['sha256']='0'*64
   elif kind=='origin':items[0]['origin']='product_result'
   elif kind=='duplicate':items.append(items[0])
   else:items[0]['content']='truncated'
   with self.subTest(kind=kind),self.assertRaises(ValueError):office.verify_files(FOLDER,items,'outputs')
 def test_omitted_or_added_zip_member_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)
   for kind in ['missing','extra']:
    with zipfile.ZipFile(p/'sample.zip','w') as z:
     if kind=='extra':
      for a in RAW['recipes'][0]['output_files']:z.writestr(a['name'],a['content'])
      z.writestr('../outside','no')
    with self.subTest(kind=kind),self.assertRaises(ValueError):office.verify_zip(p,'sample.zip',RAW['recipes'][0]['output_files'])
 def test_projection_has_no_private_absolute_paths_or_worker_reports(self):
  self.assertFalse((ROOT/'learning/office-expansion').exists())
  for p in FOLDER.rglob('*'):
   if p.is_file() and p.suffix in ['.json','.md']:self.assertNotIn('/workspace/',p.read_text())
  self.assertFalse((FOLDER/'validation.json').exists());self.assertFalse((FOLDER/'build.py').exists())
 def test_registered_changes_do_not_bypass_admission_or_projection(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);folder=root/'learning/task-first/r1/office-expansion';shutil.copytree(FOLDER,folder)
   p=folder/'proposed-workflows.json';raw=copy.deepcopy(RAW);raw['recipes'][0]['prompt']='false success';p.write_text(json.dumps(raw))
   meta=json.loads((folder/'projection.json').read_text());meta['public_file_sha256'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest();(folder/'projection.json').write_text(json.dumps(meta))
   with self.assertRaisesRegex(ValueError,'admitted record bytes'):office.catalog(root)
if __name__=='__main__':unittest.main()
