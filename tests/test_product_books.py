import copy, hashlib, importlib.util, json, tempfile, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('product_books',ROOT/'scripts/product_books.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def register_test_files(root):
 # Explicitly register ONLY test-created regular fixtures; never used by publishing.
 folder=root/'product-books';idx=m.load(folder/'index.json')
 idx['publication_files']={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in m.inventory(folder).items() if name!='index.json'}
 (folder/'index.json').write_text(json.dumps(idx))

class ProductBooks(unittest.TestCase):
 def setUp(self): self.data=m.catalog();self.task=copy.deepcopy(self.data['tasks'][0])
 def test_four_independent_base_contracts(self):
  self.assertEqual(4,len(self.data['tasks']))
  self.assertEqual(4,len({t['task_id'] for t in self.data['tasks']}))
  self.assertTrue(all(t['product_id'] is None and t['observed_results'] is None for t in self.data['tasks']))
 def test_all_author_references_pass_and_wrong_outputs_fail(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'output.json'
   for t in self.data['tasks']:
    p.write_text(json.dumps(t['expected_output']));self.assertEqual('passed',m.check(t['task_id'],p)['offline_contract'])
    p.write_text('{}')
    with self.assertRaisesRegex(ValueError,'mismatch'):m.check(t['task_id'],p)
 def test_boolean_is_not_number(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.json';v=copy.deepcopy(self.task['expected_output']);v['budget_approved']=0;p.write_text(json.dumps(v))
   with self.assertRaisesRegex(ValueError,'mismatch'):m.check(self.task['task_id'],p)
 def test_strict_json(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.json'
   for v in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}']:
    p.write_text(v)
    with self.assertRaises(ValueError):m.load(p)
 def test_unsafe_paths(self):
  for name in ['../README.md','/etc/passwd','x/../y','x\\y','x:y','x//y','./fixtures/orders.csv']:
   with self.assertRaises(ValueError):m.local(ROOT/'product-books',name)
 def test_symlink_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'real').write_text('x');(p/'link').symlink_to(p/'real')
   with self.assertRaisesRegex(ValueError,'symlink'):m.local(p,'link')
 def test_negative_evidence_mutations(self):
  for key,value in [('product_execution','passed'),('observed_results',{}),('expected_output_origin','model_output'),('evidence_tier','real_world'),('runner_implemented',True)]:
   t=copy.deepcopy(self.task);t[key]=value
   with self.assertRaises(ValueError):m.validate_record(t,ROOT/'product-books')
 def test_hash_failure(self):
  self.task['input_artifacts'][0]['sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'hash mismatch'):m.validate_record(self.task,ROOT/'product-books')
 def test_missing_recovery(self):
  del self.task['steps'][0]['failure_recovery']
  with self.assertRaisesRegex(ValueError,'failure_recovery'):m.validate_record(self.task,ROOT/'product-books')
 def test_deterministic_archive_and_clean_extract(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);m.publish(ROOT,p);first=(p/'product-bench-offline-r1.zip').read_bytes();m.publish(ROOT,p);self.assertEqual(first,(p/'product-bench-offline-r1.zip').read_bytes())
   out=p/'extracted'
   with zipfile.ZipFile(p/'product-bench-offline-r1.zip') as z:z.extractall(out)
   self.assertEqual(4,len(m.catalog(out)['tasks']))
 def test_legacy_exact_count(self):
  self.assertEqual(138,len(json.loads((ROOT/'site/data.json').read_text())['cases']))
 def test_development_book_contract_and_rejection(self):
  import shutil
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);shutil.copytree(ROOT/'product-books',root/'product-books')
   fixture=root/'product-books/books/dev';fixture.mkdir(parents=True,exist_ok=True)
   (fixture/'input.txt').write_text('synthetic test only')
   rec=copy.deepcopy(self.task);rec.update(recipe_id='development-only',product_id='development-only',task_id=None,evidence_tier='documentation_review',sources=[dict(id='test-source',title='Development test',url='https://example.com/',accessed_at='2026-10-29',claim_scope='Test only, never published')],input_artifacts=[dict(path='input.txt',description='test fixture',sha256=hashlib.sha256((fixture/'input.txt').read_bytes()).hexdigest())])
   b=dict(schema_version='1.0',product=dict(product_id='development-only',vendor='Test vendor',name='Test product',display_name='Development only',status='researched',version_scope='test',sources=rec['sources']),recipes=[rec]);(fixture/'product-book.json').write_text(json.dumps(b))
   idx=m.load(root/'product-books/index.json');idx['books'].append('books/dev/product-book.json');idx.pop('editorial_navigation',None);(root/'product-books/index.json').write_text(json.dumps(idx));register_test_files(root);self.assertTrue(m.catalog(root)['books'])
   b['recipes'][0]['task_id']='unregistered-task';(fixture/'product-book.json').write_text(json.dumps(b));register_test_files(root)
   with self.assertRaisesRegex(ValueError,'unresolved task'):m.catalog(root)
 def test_source_unsafe(self):
  s=dict(id='a',title='a',url='https://user:pass@example.com',accessed_at='2026-10-29',claim_scope='a')
  with self.assertRaises(ValueError):m.source(s)
class Hardening(unittest.TestCase):
 def setUp(self):
  import shutil
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'root';self.root.mkdir()
  shutil.copytree(ROOT/'product-books',self.root/'product-books');(self.root/'scripts').mkdir();shutil.copy(ROOT/'scripts/product_books.py',self.root/'scripts/product_books.py')
  self.out=Path(self.tmp.name)/'out';self.out.mkdir();self.task=copy.deepcopy(m.catalog(self.root)['tasks'][0])
 def book(self):
  folder=self.root/'product-books/books/development';folder.mkdir(parents=True)
  old=self.root/'product-books'/self.task['input_artifacts'][0]['path'];(folder/'input.txt').write_bytes(old.read_bytes())
  rec=copy.deepcopy(self.task);rec.update(recipe_id='development',product_id='development',task_id=None,sources=[dict(id='development',title='Development only',url='https://example.com',accessed_at='2026-10-29T05:32:00Z',claim_scope='test fixture')]);rec['input_artifacts'][0]['path']='input.txt'
  book=dict(schema_version='1.0',product=dict(product_id='development',vendor='Development only',name='Development only',display_name='Development only',status='researched',version_scope='test',sources=rec['sources']),recipes=[rec])
  idx=m.load(self.root/'product-books/index.json');idx['books']=['books/development/product-book.json'];idx['guides']=[];idx.pop('editorial_navigation',None);(self.root/'product-books/index.json').write_text(json.dumps(idx))
  return folder,book,rec
 def save(self,folder,book):
  (folder/'product-book.json').write_text(json.dumps(book));register_test_files(self.root)
 def test_unregistered_regular_file_rejected_before_publish(self):
  (self.root/'product-books/unregistered.txt').write_text('unregistered')
  with self.assertRaisesRegex(ValueError,'inventory mismatch'):m.publish(self.root,self.out)
  self.assertEqual([],list(self.out.iterdir()))
 def test_unregistered_external_symlink_rejected_before_publish(self):
  sentinel=Path(self.tmp.name)/'external';sentinel.write_text('SAFE TEST SENTINEL')
  (self.root/'product-books/link').symlink_to(sentinel)
  with self.assertRaisesRegex(ValueError,'symlink'):m.publish(self.root,self.out)
  self.assertEqual([],list(self.out.iterdir()))
 def test_registered_file_changed_to_symlink_rejected(self):
  p=self.root/'product-books/fixtures/orders.csv';data=p.read_bytes();p.unlink();outside=Path(self.tmp.name)/'outside';outside.write_bytes(data);p.symlink_to(outside)
  with self.assertRaisesRegex(ValueError,'symlink'):m.publish(self.root,self.out)
 def test_directory_symlink_rejected(self):
  (self.root/'product-books/foreign').symlink_to(self.out,target_is_directory=True)
  with self.assertRaisesRegex(ValueError,'symlink'):m.catalog(self.root)
 def test_symlink_ancestor_rejected(self):
  linked=Path(self.tmp.name)/'linked';linked.symlink_to(self.root,target_is_directory=True)
  with self.assertRaisesRegex(ValueError,'symlink'):m.catalog(linked)
 def test_nonregular_fifo_rejected_without_reading(self):
  import os
  os.mkfifo(self.root/'product-books/pipe')
  with self.assertRaisesRegex(ValueError,'nonregular'):m.catalog(self.root)
 def test_wrong_registered_hash_rejected(self):
  (self.root/'product-books/fixtures/orders.csv').write_text('changed')
  with self.assertRaisesRegex(ValueError,'publication hash mismatch'):m.catalog(self.root)
 def test_destination_symlink_rejected(self):
  sentinel=Path(self.tmp.name)/'sentinel';sentinel.write_text('SAFE')
  (self.out/'product-books-data.json').symlink_to(sentinel)
  with self.assertRaisesRegex(ValueError,'symlink'):m.publish(self.root,self.out)
  self.assertEqual('SAFE',sentinel.read_text())
 def test_checker_symlink_rejected_before_output(self):
  p=self.root/'scripts/product_books.py';p.unlink();p.symlink_to(ROOT/'scripts/product_books.py')
  with self.assertRaisesRegex(ValueError,'symlink'):m.publish(self.root,self.out)
  self.assertEqual([],list(self.out.iterdir()))
 def test_nested_invalid_types_rejected(self):
  for field,value in [('objective_checks',[None]),('objective_checks',[{}]),('objective_checks',[123]),('human_rubric',[123]),('human_rubric',[{}]),('human_rubric',[{'criterion':'x','points':True,'how_to_check':'x'}]),('expected_output',False),('expected_output',[]),('expected_output',{}),('expected_output',' '),('steps',[None]),('input_artifacts',[None]),('expected_output_artifacts',[None]),('sources',[None])]:
   with self.subTest(field=field,value=value):
    task=copy.deepcopy(self.task);task[field]=value
    with self.assertRaises(ValueError):m.validate_record(task,self.root/'product-books')
 def test_malformed_index_and_queue_rejected(self):
  original=m.load(self.root/'product-books/index.json')
  for key,value in [('books','oops'),('tasks',[None]),('research_queue',[None]),('research_queue',[{'product_id':'x'}]),('research_queue','x')]:
   idx=copy.deepcopy(original);idx[key]=value;(self.root/'product-books/index.json').write_text(json.dumps(idx))
   with self.subTest(key=key):
    with self.assertRaises(ValueError):m.catalog(self.root)
 def test_source_date_or_timestamp_preserved(self):
  source=dict(id='s',title='s',url='https://example.com',accessed_at='2026-10-29T05:32:00Z',claim_scope='test');m.source(source);self.assertEqual('2026-10-29T05:32:00Z',source['accessed_at'])
  for value in ['2026-99-99','2026-10-29T05:32:00','tomorrow']:
   source['accessed_at']=value
   with self.assertRaises(ValueError):m.source(source)
 def test_exact_mapping_accepts_different_product_prompt(self):
  folder,book,rec=self.book();rec['task_id']=self.task['task_id'];rec['task_contract_sha256']=m.contract_sha256(self.task);rec['prompt']='Product-specific user interface workflow, same fixed contract.';self.save(folder,book)
  self.assertEqual(rec['task_id'],m.catalog(self.root)['books'][0]['recipes'][0]['task_id'])
 def test_unrelated_mapping_rejected_even_with_copied_fingerprint(self):
  folder,book,rec=self.book();rec['task_id']=self.task['task_id'];rec['task_contract_sha256']=m.contract_sha256(self.task)
  for field,value in [('business_goal','unrelated'),('expected_output',{'unrelated':True}),('objective_checks',['unrelated']),('human_rubric',['unrelated']),('reference_format','unrelated')]:
   baseline=copy.deepcopy(rec[field]);rec[field]=value;self.save(folder,book)
   with self.subTest(field=field):
    with self.assertRaisesRegex(ValueError,'binding mismatch'):m.catalog(self.root)
   rec[field]=baseline
  (folder/'input.txt').write_text('DIFFERENT SAFE INPUT');rec['input_artifacts'][0]['sha256']=hashlib.sha256((folder/'input.txt').read_bytes()).hexdigest();self.save(folder,book)
  with self.assertRaisesRegex(ValueError,'binding mismatch'):m.catalog(self.root)
 def test_mapping_needs_explicit_fingerprint(self):
  folder,book,rec=self.book();rec['task_id']=self.task['task_id'];self.save(folder,book)
  with self.assertRaisesRegex(ValueError,'binding mismatch'):m.catalog(self.root)
 def test_rich_fields_and_all_reference_paths_preserved(self):
  folder,book,rec=self.book();rec['source_recipe']={'ui_steps':[{'status':'documented_not_ui_tested','source_id':'s'}],'third_party':{'warning':'do not connect'},'numbers':[1,2]};rec['structured_details']={'cost':{'unknown':True}};original=copy.deepcopy(rec)
  (folder/'full-reference.md').write_text('Full original author reference, never product output.');rec['reference_files']=['full-reference.md'];rec['expected_output']={'reference_files':['full-reference.md'],'coverage':'text only'};self.save(folder,book)
  result=m.catalog(self.root)['books'][0]['recipes'][0]
  for key in ['source_recipe','structured_details']:self.assertEqual(original[key],result[key])
  self.assertEqual(rec['reference_files'],result['reference_files']);self.assertEqual(rec['expected_output'],result['expected_output']);self.assertEqual(1,len(result['expected_output_artifacts']));a=result['expected_output_artifacts'][0];self.assertEqual(hashlib.sha256((folder/a['path']).read_bytes()).hexdigest(),a['sha256'])
  m.publish(self.root,self.out)
  with zipfile.ZipFile(self.out/'product-bench-offline-r1.zip') as z:self.assertEqual((folder/'full-reference.md').read_bytes(),z.read('product-books/books/development/full-reference.md'))
if __name__=='__main__':unittest.main()
