"""Creative delivery integration: frozen bytes, isolated stdlib replay and strict page gates."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import creative_delivery_lab as lab
import check_pages as pages

class CreativeDeliveryTests(unittest.TestCase):
 def test_fixed_bytes_and_independent_unpack(self):
  m=lab.verify(ROOT,execute=True)
  self.assertEqual(m['source_member_count'],36);self.assertEqual(m['cases'],138)
 def test_all_historical_protected_bytes_unchanged(self):
  baseline=json.loads((ROOT/'tests/fixtures/creative-delivery-baseline.json').read_text())
  for name,digest in baseline['sha256'].items():
   with self.subTest(path=name):self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
  for out in ('site','docs'):
   data=json.loads((ROOT/out/'data.json').read_text());self.assertEqual(len(data['cases']),138)
   self.assertEqual(sum('lesson_markdown' in c for c in data['cases']),12)
 def test_published_lab_exact_copy(self):
  base=ROOT/'learning/creative-delivery/r1'
  for out in ('site','docs'):
   for p in base.rglob('*'):
    if p.is_file():self.assertEqual(p.read_bytes(),(ROOT/out/'creative-delivery/r1'/p.relative_to(base)).read_bytes())
 def test_frozen_tamper_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);dest=root/'learning/creative-delivery/r1';shutil.copytree(ROOT/'learning/creative-delivery/r1',dest)
   p=dest/'source/timeline.py';p.write_bytes(p.read_bytes()+b'\n')
   with self.assertRaises(ValueError):lab.verify(root)
 def test_page_contract(self):
  class P(HTMLParser):
   def __init__(self):super().__init__();self.tags=[];self.links=[]
   def handle_starttag(self,tag,attrs):
    d=dict(attrs);self.tags.append((tag,d))
    if tag=='a':self.links.append(d.get('href',''))
  html=(ROOT/'web/creative-delivery-lab.html').read_text();p=P();p.feed(html)
  self.assertEqual(sum(t=='h1' for t,a in p.tags),1)
  self.assertFalse(any(t in ('script','form','iframe') for t,a in p.tags))
  self.assertTrue(any(t=='html' and a.get('lang')=='zh-CN' for t,a in p.tags))
  self.assertTrue(any(t=='main' and a.get('id')=='main' for t,a in p.tags))
  self.assertIn('#main',p.links)
  self.assertIn('creative-delivery/r1/creative-delivery-lab-r1.zip',p.links)
  for case in ['video-archive-reproducible','video-caption-accessibility','music-accessible-captions','design-asset-provenance']:
   self.assertTrue(any('?case='+case in link for link in p.links))
  for token in ['publish_allowed','false','WebVTT','OTIO','65536','primary','derived','8000','12000','4000']:
   self.assertIn(token,html)
  self.assertNotIn('/workspace/',html)
 def small_site(self,root):
  for directory in ('dist','docs'):
   d=root/directory;d.mkdir();(d/'.nojekyll').touch();(d/'index.html').write_text('<main id="main">test</main>')
   for name in pages.CREATIVE_NEGATIVE_FIXTURES:
    p=d/name;p.parent.mkdir(parents=True,exist_ok=True)
    source=ROOT/'learning/creative-delivery/r1/source/fixtures'/p.name
    p.write_bytes(source.read_bytes())
 def test_negative_fixture_exact_closed_set(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.small_site(root);pages.check(root)
 def test_negative_fixture_changed_to_valid_or_byte_drift(self):
  for value in (b'{}',b' '):
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);self.small_site(root)
    name=next(iter(pages.CREATIVE_NEGATIVE_FIXTURES))
    for out in ('dist','docs'):(root/out/name).write_bytes(value)
    with self.assertRaisesRegex(ValueError,'frozen bytes changed'):pages.check(root)
 def test_negative_fixture_missing_or_relocated(self):
  for relocate in (False,True):
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);self.small_site(root);name=next(iter(pages.CREATIVE_NEGATIVE_FIXTURES))
    for out in ('dist','docs'):
     p=root/out/name
     if relocate:p.rename(p.with_name('moved.json'))
     else:p.unlink()
    with self.assertRaisesRegex(ValueError,'closed set missing'):pages.check(root)
 def test_other_invalid_json_and_same_name_elsewhere_fail(self):
  for name in ('other.json','submission-F12b.json'):
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);self.small_site(root)
    for out in ('dist','docs'):(root/out/name).write_text('{"a":NaN}')
    with self.assertRaisesRegex(ValueError,'non-finite JSON'):pages.check(root)
 def test_registry_omission_or_extra_fails(self):
  for extra in (False,True):
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);self.small_site(root);changed=dict(pages.CREATIVE_NEGATIVE_FIXTURES)
    if extra:changed['other.json']=next(iter(changed.values()))
    else:changed.pop(next(iter(changed)))
    with patch.object(pages,'CREATIVE_NEGATIVE_FIXTURES',changed):
     with self.assertRaisesRegex(ValueError,'registry changed'):pages.check(root)
 def test_ci_and_build_wire_checks(self):
  self.assertIn('python -B scripts/creative_delivery_lab.py --check',(ROOT/'.github/workflows/checks.yml').read_text())
  self.assertIn('creative_delivery_lab.publish(ROOT,dest)',(ROOT/'scripts/build.py').read_text())

if __name__=='__main__':unittest.main()
