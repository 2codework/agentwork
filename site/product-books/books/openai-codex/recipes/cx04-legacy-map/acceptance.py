# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'app.py': 'a933dfc0125a96f2b44827b4f9f95953a7d1101c83548de3af9ac39a81c25106', 'scoring.py': '14efabad8a2f634c0eaa2253c7dbfb80ccd14577cc42b91b3357d8f3f04bdab4', 'samples.json': 'aeb5011e730645461b7900b072cf4ca7aee1f58e7a1f042173f0bd3e76de1170', 'parser.py': '91ea7e44be618bd1107a8c5af0934a66ddd19033e6b16c6f2043b44eaf578fab', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'samples.json', 'parser.py', 'AGENTS.md', 'app.py', 'ONBOARDING.md', 'scoring.py', 'architecture.json'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
sys.path.insert(0,str(ROOT));m=load('app');d=json.loads((ROOT/'architecture.json').read_text())
assert d['entry']=='app.py:3' and d['flow']==['app.process','parser.parse','scoring.score']
for ex in d['examples']:
 if 'error' in ex:
  try:m.process(ex['input'])
  except ValueError:assert ex['error']=='ValueError'
  else:raise AssertionError('missing error')
 else:assert m.process(ex['input'])==ex['output']
assert len(d['examples'])==3 and d['unknowns'] and (ROOT/'ONBOARDING.md').exists()

assert {ex['input'] for ex in d['examples']} == set(json.loads((ROOT/'samples.json').read_text())), 'must cover supplied inputs exactly'
assert len(d['examples']) == len(json.loads((ROOT/'samples.json').read_text()))
assert {s['file'] for s in d['change_seams']} == {'parser.py','scoring.py'}
assert all(isinstance(s['purpose'],str) and s['purpose'].strip() for s in d['change_seams'])
assert (ROOT/'ONBOARDING.md').read_text().strip(), 'empty onboarding'

print('PASS: anchors and all documented examples agree with code')
