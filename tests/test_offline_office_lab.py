"""Offline integration gates; no Git history, third-party SDK or account needed."""
import hashlib,json,subprocess,sys,tempfile,unittest,zipfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import offline_office_lab as L
LAB=ROOT/'learning/offline-office/r1'
class OfflineOfficeLabTests(unittest.TestCase):
 def test_frozen_source_qa_and_data(self):
  m=L.verify(ROOT)
  self.assertEqual(m['cases'],132)
  self.assertEqual(hashlib.sha256((LAB/'qa/FINAL-VALIDATION.json').read_bytes()).hexdigest(),'21eeace0d7fb96066590a2c14981b68d34a5762559609fe513299a89d307f0ff')
  for folder in ('site','docs'):
   frozen=json.loads((ROOT/'tests/fixtures/creative-learning-baseline.json').read_text())
   self.assertEqual(frozen['baseline_data_sha256'],m['baseline_data_sha256']) # historical lab-only byte contract retained
   data=json.loads((ROOT/folder/'data.json').read_text())
   digest=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   self.assertEqual({k:digest(v) for k,v in data.items() if k!='cases'},frozen['other_top_level'])
   self.assertEqual({c['id']:digest(c) for c in data['cases'] if c['id'] in frozen['cases']},frozen['cases'])
   self.assertEqual({c['id'] for c in data['cases']}-set(frozen['cases']),set(frozen['new_case_ids']))
   self.assertEqual(len(data['cases']),138)
  qa=json.loads((LAB/'qa/FINAL-VALIDATION.json').read_text())
  for name,h in qa['input_sha256'].items():self.assertEqual(hashlib.sha256((LAB/'source'/name).read_bytes()).hexdigest(),h)
 def test_zip_members_and_reproducibility(self):
  m=json.loads((LAB/'SHA256.json').read_text());z=LAB/m['archive']
  self.assertEqual(hashlib.sha256(z.read_bytes()).hexdigest(),'9f20ed0318765e8e02938f334e71b83cfe3a626afc3c675410c9e2777f575484')
  with zipfile.ZipFile(z) as archive:
   self.assertEqual(sorted(archive.namelist()),sorted(m['members']))
   self.assertEqual(len(archive.namelist()),13)
   for name,h in m['members'].items():
    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(),h)
    self.assertEqual(archive.read(name),(LAB/'source'/name.removeprefix('meeting-action-lab/')).read_bytes())
  with tempfile.TemporaryDirectory() as t:
   for suffix in ('a','b'):
    out=Path(t)/suffix
    result=subprocess.run([sys.executable,'-B',str(LAB/'source/package_lab.py'),'--out',str(out)],capture_output=True,text=True)
    self.assertEqual(result.returncode,0,result.stderr)
    self.assertEqual((out/m['archive']).read_bytes(),z.read_bytes())
 def test_unpack_runs_original_nineteen_tests(self):
  with tempfile.TemporaryDirectory() as t:
   with zipfile.ZipFile(LAB/'meeting-action-lab-r1.zip') as archive:archive.extractall(t)
   root=Path(t)/'meeting-action-lab'
   result=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=root,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr);self.assertIn('Ran 19 tests',result.stderr)
   result=subprocess.run([sys.executable,'-B','lab.py','check-golden'],cwd=root,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
 def test_publication_preserves_all_frozen_bytes(self):
  for out in ('site','docs'):
   for p in LAB.rglob('*'):
    if p.is_file():self.assertEqual(p.read_bytes(),(ROOT/out/'offline-office/r1'/p.relative_to(LAB)).read_bytes())
 def test_tampering_fails_closed(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);dest=root/'learning/offline-office/r1';shutil.copytree(LAB,dest)
   p=dest/'source/lab.py';p.write_bytes(p.read_bytes()+b'\n')
   with self.assertRaises(ValueError):L.verify(root)
 def test_accessible_page_and_entrypoints(self):
  from html.parser import HTMLParser
  class Page(HTMLParser):
   def __init__(self):super().__init__();self.tags=[];self.links=[]
   def handle_starttag(self,tag,attrs):
    d=dict(attrs);self.tags.append((tag,d))
    if tag=='a':self.links.append(d.get('href',''))
  page=Page();html=(ROOT/'web/offline-office-lab.html').read_text();page.feed(html)
  self.assertEqual(sum(t=='h1' for t,a in page.tags),1)
  self.assertTrue(any(t=='html' and a.get('lang')=='zh-CN' for t,a in page.tags))
  self.assertTrue(any(t=='main' and a.get('id')=='main' for t,a in page.tags))
  self.assertFalse(any(t in ('script','form','iframe') for t,a in page.tags))
  self.assertIn('#main',page.links);self.assertIn('offline-office/r1/meeting-action-lab-r1.zip',page.links)
  self.assertIn("['labs','离线练习']",(ROOT/'web/app.js').read_text())
  self.assertIn('offline-office-lab.html',(ROOT/'web/app.js').read_text())
  for token in ['dispatch_allowed','false','Linux','macOS','未验证','input_sha256','submission_sha256','不是身份认证或签名','不是恶意文件系统沙箱','不是模型生成结果']:self.assertIn(token,html)
if __name__=='__main__':unittest.main()
