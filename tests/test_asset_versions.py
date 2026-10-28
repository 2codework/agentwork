"""Published cache coherence contracts; no network or browser required."""
import hashlib, importlib.util, re, subprocess, tempfile, unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('asset_versions_test',ROOT/'scripts/asset_versions.py'); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.urls=[];self.data=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='script':self.urls.append(a['src'])
  if tag=='link' and a.get('rel')=='stylesheet':self.urls.append(a['href'])
  if tag=='html':self.data=a.get('data-data-url')
class AssetVersions(unittest.TestCase):
 def test_every_generated_asset_and_data_pin_matches_bytes(self):
  output=ROOT/('site' if (ROOT/'site').exists() else 'dist')
  tags=Tags();tags.feed((output/'index.html').read_text());self.assertTrue(tags.urls);self.assertTrue(tags.data)
  for url in tags.urls+[tags.data]:
   u=urlsplit(url);self.assertFalse(u.scheme or u.netloc);self.assertFalse(u.path.startswith('/'))
   self.assertEqual(parse_qs(u.query),{'v':[hashlib.sha256((output/u.path).read_bytes()).hexdigest()]})
  self.assertEqual((output/'index.html').read_bytes(),(ROOT/'docs/index.html').read_bytes())
 def test_pin_idempotent_and_rekeys_changed_bytes(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)
   for name in ['a.js','a.css','data.json']:(p/name).write_text('{}')
   (p/'index.html').write_text('<html><link rel="stylesheet" href="a.css"><script src="a.js" defer></script></html>')
   module.pin(p);first=(p/'index.html').read_bytes();module.pin(p);self.assertEqual(first,(p/'index.html').read_bytes())
   (p/'a.js').write_text('changed');module.pin(p);self.assertNotEqual(first,(p/'index.html').read_bytes())
 def test_actual_fetch_uses_html_pin_and_dev_only_fallback(self):
  js=(ROOT/'web/app.js').read_text();expression=re.search(r'await fetch\(([^;]+?)\);',js).group(1)
  helper=next(line for line in js.splitlines() if line.startswith('function pinnedDataURL()'))
  program='const assert=require("assert/strict");let value="data.json?v="+"a".repeat(64),document={documentElement:{getAttribute:()=>value}};'+helper+'assert.equal('+expression+',value);for(const bad of ["", "data.json", "https://evil.example/data.json?v="+"a".repeat(64),"//evil.example/data.json", "../data.json?v="+"a".repeat(64),"data.json?v=bad", "data.json?v="+"a".repeat(64)+"#x"]){value=bad;assert.throws(()=>'+expression+');}value=null;assert.equal('+expression+',"data.json");document={};assert.equal('+expression+',"data.json");'
  subprocess.run(['node','-e',program],check=True)
