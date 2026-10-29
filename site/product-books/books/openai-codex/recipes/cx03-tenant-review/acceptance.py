# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'contract.md': 'b5983513f42140050a176d396144ce2cd7e70aba13f069c2a94eb2fa83c7b706', 'invoices.py': 'ae704c7b606de063280a64f73b5e71468c93196785009773249fb34aefab4582', 'invoices.json': '013bededd4f34dee74fb17cc087e799c6e57e065224148e06295ac95e4e03a8f', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'contract.md', 'invoices.json', 'AGENTS.md', 'review.json', 'invoices.py'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
data=json.loads((ROOT/'invoices.json').read_text());m=load('invoices')
assert [r['id'] for r in m.visible_invoices(data,'A')]==['a1','b1'],'review fixture changed'
r=json.loads((ROOT/'review.json').read_text()); f=r['findings'][0]
assert f['file']=='invoices.py' and f['line']==2
assert f['reproduction']['actual_ids']==['a1','b1'] and f['reproduction']['expected_ids']==['a1']
assert f['severity'] in ['high','critical'] and r['limitations']
assert (ROOT/'invoices.py').read_text()=='def visible_invoices(invoices, tenant_id):\n    return [row for row in invoices if row["status"] == "open"]\n'
print('PASS: reproduction, source preservation and report anchors; severity prose needs human review')
