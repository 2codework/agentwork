import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('normalizer',R/'scripts/normalize.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
class Creative(unittest.TestCase):
 def setUp(self):self.d=json.loads((R/'research/creative-music.json').read_text())
 def test_lossless_original(self):
  orig=copy.deepcopy(self.d);result=N.normalize('creative-music',self.d);self.assertEqual(self.d,orig)
  for c,raw in zip(result,orig['cases']):self.assertEqual(c['raw_record'],raw)
 def test_dangling_node_fails(self):
  self.d['cases'][0]['modelatlas_node_ids']=['missing']
  with self.assertRaisesRegex(ValueError,'Dangling'):N.normalize('creative-music',self.d)
 def test_duplicate_source_fails(self):
  self.d['sources'].append(self.d['sources'][0])
  with self.assertRaisesRegex(ValueError,'Duplicate'):N.normalize('creative-music',self.d)
 def test_missing_source_fails(self):
  self.d['cases'][0]['source_ids']=['missing']
  with self.assertRaisesRegex(ValueError,'Missing'):N.normalize('creative-music',self.d)
 def test_reader_loaded_before_app(self):
  html=(R/'web/index.html').read_text();self.assertLess(html.index('reader.js'),html.index('app.js'))
