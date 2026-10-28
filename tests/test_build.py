import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
class BuildTests(unittest.TestCase):
 def setUp(self): self.data=json.loads((ROOT/'content/cases.json').read_text())
 def reject(self,mutate):
  mutate(self.data)
  with self.assertRaises((AssertionError,KeyError,TypeError)): b.validate(self.data)
 def test_lifecycle(self): self.reject(lambda d:d['cases'][0].update(lifecycle='latest'))
 def test_current_needs_verification(self): self.reject(lambda d:d['cases'][0].update(lifecycle='current'))
 def test_valid(self): self.assertIs(b.validate(self.data),self.data)
 def test_duplicate(self): self.reject(lambda d:d['cases'].append(copy.deepcopy(d['cases'][0])))
 def test_unsafe_id(self): self.reject(lambda d:d['cases'][0].update(id='../file'))
 def test_evidence(self): self.reject(lambda d:d['cases'][0].update(evidence='verified'))
 def test_synthetic_mismatch(self): self.reject(lambda d:d['cases'][0].update(synthetic=False))
 def test_no_steps(self): self.reject(lambda d:d['cases'][0].update(steps=[]))
 def test_empty_check(self): self.reject(lambda d:d['cases'][0]['steps'][0].update(check=''))
 def test_unsafe_source(self): self.reject(lambda d:d['cases'][0].update(sources=[dict(title='bad',url='javascript:alert(1)',evidence='reference')]))
 def test_no_sources(self): self.reject(lambda d:d['cases'][0].update(synthetic=False,evidence='primary'))
 def test_build_deterministic(self):
  b.build(); first=(ROOT/'site/data.json').read_bytes();b.build();self.assertEqual(first,(ROOT/'site/data.json').read_bytes())
 def test_safe_rendering(self):
  js=(ROOT/'web/app.js').read_text();self.assertNotIn('innerHTML',js);self.assertNotIn('eval(',js)
 def test_no_remote_dependencies(self):
  html=(ROOT/'web/index.html').read_text();self.assertNotIn('src="https:',html);self.assertNotIn('href="https:',html)
if __name__=='__main__':unittest.main()
