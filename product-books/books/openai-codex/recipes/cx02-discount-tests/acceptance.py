# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'policy.md': 'ff11f93e2ab6d651fb49adbaf8608a04869550f870ed5320908156a65d78ff48', 'pricing.py': '28673660bcea9c4cacd4cf59cc8191c2a64b7b98bb2f3ba0d4c6de6392881d9e', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'policy.md', 'test_pricing.py', 'AGENTS.md', 'pricing.py'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
import tempfile, shutil, subprocess
assert (ROOT/'test_pricing.py').exists()
def run(folder):
 return subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_pricing.py'],cwd=folder,capture_output=True,text=True,timeout=10)
r=run(ROOT); assert r.returncode==0,r.stderr
baseline=(ROOT/'pricing.py').read_text()
mutants=[baseline.replace('+ 50','+ 0'),baseline.replace('<= percent <= 100','<= percent <= 101'),baseline.replace('return (cents * (100-percent) + 50) // 100','return cents')]
for mutant in mutants:
 with tempfile.TemporaryDirectory() as d:
  p=pathlib.Path(d);shutil.copy(ROOT/'test_pricing.py',p/'test_pricing.py');(p/'pricing.py').write_text(mutant)
  assert run(p).returncode!=0,'tests missed mutant'
print('PASS: suite passes original and kills three intentional mutants')
