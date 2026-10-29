# Input-integrity gate; synthetic trusted exercise only, not a sandbox for arbitrary code.
import pathlib, sys, hashlib
sys.dont_write_bytecode=True
_gate_root=pathlib.Path(sys.argv[1]).resolve()
_preserved={'brief.md': 'f5d889a670d1bcf29accdbbdd35028b5e2c7822cce9a4f4da42a89f35efa2002', 'AGENTS.md': '9a920422c3ded2fb23211670145105cc44007b56949012c1bc53f13d0368c8d7'}
_allowed={'brief.md', 'MANUAL-QA.md', 'index.html', 'AGENTS.md'}
for _name,_digest in _preserved.items():
    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)
for _p in _gate_root.rglob('*'):
    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:
        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))
import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
t=(ROOT/'index.html').read_text();p=P();p.feed(t)
assert any(tag=='html' and a.get('lang')=='zh-CN' for tag,a in p.tags)
assert any(tag=='label' and a.get('for')=='status' for tag,a in p.tags)
assert any(tag=='select' and a.get('id')=='status' for tag,a in p.tags)
assert any(a.get('aria-live')=='polite' for tag,a in p.tags)
assert {a.get('value') for tag,a in p.tags if tag=='option'}=={'all','open','closed'}
for forbidden in ['fetch(', 'XMLHttpRequest', 'localStorage', 'https://', 'http://', '<iframe', '<form']:
 assert forbidden not in t,forbidden
assert ':focus-visible' in t and 'T1' in t and 'T2' in t and '没有符合条件' in t

assert (ROOT/'MANUAL-QA.md').read_text().strip(), 'missing or empty manual QA checklist'

print('PASS: static structure only; JavaScript behavior and visual/accessibility QA NOT RUN')
