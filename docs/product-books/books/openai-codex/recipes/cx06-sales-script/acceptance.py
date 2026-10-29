# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'policy.md': '81ec9ece4ed17fb10b27e20cf4190c4a0cbc251d8e22b3e30fc6fb5769133f6f', 'orders.csv': '355eba83032013b918dfbb0d47782d9b2050fd21546a35fb3fef60545f4097a2', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'summarize.py', 'policy.md', 'AGENTS.md', 'orders.csv', 'expected.json'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
import tempfile
m=load('summarize');assert m.summarize(ROOT/'orders.csv')=={'net_cents':{'north':800,'south':700},'duplicate_rows':1}
for rows in ['x,north,1,paid\nx,north,2,paid\n','x,north,-1,paid\n','x,north,1,unknown\n']:
 with tempfile.TemporaryDirectory() as d:
  p=pathlib.Path(d)/'bad.csv';p.write_text('id,region,amount_cents,status\n'+rows)
  try:m.summarize(p)
  except ValueError:pass
  else:raise AssertionError('invalid row accepted')
assert (ROOT/'orders.csv').read_text()=='id,region,amount_cents,status\na,north,1000,paid\nb,south,700,paid\nc,north,200,refund\na,north,1000,paid\nd,south,300,cancelled\n'

import subprocess
want={'net_cents':{'north':800,'south':700},'duplicate_rows':1}
assert json.loads((ROOT/'expected.json').read_text())==want, 'incorrect expected.json'
cli=subprocess.run([sys.executable,'-B',str(ROOT/'summarize.py'),str(ROOT/'orders.csv')],capture_output=True,text=True,timeout=10)
assert cli.returncode==0, cli.stderr
assert json.loads(cli.stdout)==want, 'CLI must emit the expected JSON object'
with tempfile.TemporaryDirectory() as temp:
    zero=pathlib.Path(temp)/'zero.csv';zero.write_text('id,region,amount_cents,status\nz,north,0,paid\n')
    assert m.summarize(zero)=={'net_cents':{'north':0},'duplicate_rows':0}

print('PASS: totals, dedup, conflicting and invalid inputs; CSV unchanged')
