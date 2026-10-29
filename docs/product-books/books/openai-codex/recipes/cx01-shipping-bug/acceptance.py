# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'policy.md': '4b63a5959257e9854715d9dcc0bbe48c48ce7ea7047fc6cf64f304ed517e4ab0', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'shipping.py', 'policy.md', 'AGENTS.md'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
m=load('shipping')
for amount,remote,want in [(0,False,500),(4999,False,500),(5000,False,0),(5001,False,0),(5000,True,800),(4999,True,1300)]:
 assert m.fee(amount,remote)==want,(amount,remote,want)
try:m.fee(-1)
except ValueError:pass
else:raise AssertionError('negative subtotal must fail')
print('PASS: seven business boundary checks')
