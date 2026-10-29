import copy, hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
pb=module('product_books');negative=module('product_negative_fixtures')
class ProductIntegration(unittest.TestCase):
 def test_four_books_thirty_two_not_run_recipes_three_pending_identities(self):
  d=pb.catalog();self.assertEqual(4,len(d['books']));self.assertEqual(32,sum(len(b['recipes']) for b in d['books']));self.assertEqual({'cmcc-lingxi-assistant','regaing-lingxi','amir-hayek-zcode'},{p['product_id'] for p in d['research_queue']})
  for b in d['books']:
   self.assertEqual(8,len(b['recipes']))
   for r in b['recipes']:self.assertIsNone(r['task_id']);self.assertEqual('not_run',r['product_execution']);self.assertIsNone(r['observed_results']);self.assertFalse(r['runner_implemented'])
 def test_all_original_fields_lossless_in_catalog(self):
  d=pb.catalog();folder=ROOT/'product-books'
  for file,b in zip(d['books'],pb.load(folder/'index.json')['books']):
   raw=pb.load(folder/b)
   for key,value in raw.items():
    if key!='recipes':self.assertEqual(value,file[key])
   for original,derived in zip(raw['recipes'],file['recipes']):
    for key,value in original.items():self.assertEqual(value,derived[key],(derived['recipe_id'],key))
 def test_five_complete_readable_handbooks_exact_bytes(self):
  d=pb.catalog();guides=[h for b in d['books'] for h in b['handbooks']];self.assertEqual(5,len(guides))
  for h in guides:
   p=ROOT/'product-books'/h['path'];self.assertEqual(p.read_text(),h['markdown']);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),h['sha256']);self.assertTrue(h['markdown'].strip())
 def test_workbuddy_twenty_eight_complete_reference_artifacts(self):
  b=next(x for x in pb.catalog()['books'] if x['product']['product_id']=='tencent-workbuddy');refs=[a for r in b['recipes'] for a in r['expected_output_artifacts']];self.assertEqual(28,len(refs))
  for r in b['recipes']:self.assertTrue(r['hard_gates']);self.assertTrue(r['pass_rule']);self.assertTrue(any(a['path'].endswith('audit.md') for a in r['expected_output_artifacts']))
 def test_source_timestamps_and_full_lingxi_profile_retained(self):
  books={b['product']['product_id']:b for b in pb.catalog()['books']};self.assertTrue(any('T' in s['accessed_at'] for s in books['tencent-workbuddy']['product']['sources']));self.assertIn('privacy_evidence_conflict',books['wps-lingxi-pro']['product_profile']);self.assertEqual(4,len(books['wps-lingxi-pro']['onboarding']))
 def test_five_exact_negative_paths_reject_for_expected_reasons(self):
  reg=negative.registry();self.assertEqual(5,len(reg))
  for path in reg:self.assertTrue(negative.check(ROOT/'site'/path,ROOT/'site'));self.assertTrue(negative.check(ROOT/'docs'/path,ROOT/'docs'))
 def test_changed_negative_bytes_and_valid_substitution_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for path in negative.registry():
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True)
    for value in [b'{}',b'changed']:
     p.write_bytes(value)
     with self.assertRaisesRegex(ValueError,'bytes changed'):negative.check(p,root)
 def test_registry_extra_duplicate_or_changed_reason_rejected(self):
  rows=negative.ROWS
  for changed in [rows+[rows[0]],rows[:-1],rows[:-1]+[rows[0]],[(rows[0][0],rows[0][1],'wrong reason')]+rows[1:]]:
   with self.assertRaises(ValueError):negative.registry(changed)
 def test_unregistered_negative_is_not_exempt(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/'other.json';p.write_text('{"a":NaN}');self.assertFalse(negative.check(p,root))
   with self.assertRaises(ValueError):negative.loads(p.read_text())
 def test_signed_exponent_overflow_rejected_finite_scientific_accepted(self):
  for value in ['{"x":1e999}','{"x":-1e999}']:
   with self.assertRaisesRegex(ValueError,'non-finite parsed float'):negative.loads(value)
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'x.json';p.write_text(value)
    with self.assertRaisesRegex(ValueError,'non-finite parsed float'):pb.load(p)
  self.assertEqual({'x':1250.0},negative.loads('{"x":1.25e3}'))
 def test_original_creative_registry_and_function_unchanged(self):
  text=(ROOT/'scripts/check_pages.py').read_text();original=text[text.index('CREATIVE_NEGATIVE_FIXTURES ='):text.index('\ndef check(root=ROOT):')]
  self.assertEqual('8c67312086b630ec5d72c4024a43f3df6af28d09113763c8193c848df3e2c4da',hashlib.sha256(original.encode()).hexdigest())
if __name__=='__main__':unittest.main()
