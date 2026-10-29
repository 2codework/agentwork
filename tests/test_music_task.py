import hashlib,json,sys,unittest,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import music_task,task_first

def sha(data):return hashlib.sha256(data).hexdigest()
def record(obj):return sha(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
class Music(unittest.TestCase):
 def test_original_nine_complete_records_and_guides_are_unchanged(self):
  before=json.loads((ROOT/'tests/fixtures/music-original-nine.json').read_text());after=task_first.catalog()
  self.assertEqual(len(after['workflows']),11)
  self.assertEqual({w['id']:record(w) for w in after['workflows'] if not w.get('music_workflow') and not w.get('video_workflow')},before['workflows'])
  for key in ['guides','chooser','legacy_case_ids']:self.assertEqual(record(after[key]),before[key])
 def test_exact_admitted_assets_and_downloads(self):
  w=music_task.catalog(ROOT);self.assertEqual(w['connection_guide_ids'],[]);self.assertEqual(len(w['assets']),6)
  expected={'brief.txt':'59b47e4871599dd02f93db778398628a302be3d0fb3e6f28a93b59d3e135249e','prompt-A-r1.txt':'80c8c03c50708a8808644576479fb1a97728935a89bb01f1e3cd7c802cae5c59','prompt-B-r1.txt':'14f76724d650bcd70757b86dc14b4a0d84707e63a78ffbc363e09ec258c24295','listening-record.csv':'b1fef3a250bed1b74145ee0e9a4bcfb918e234731a6c598c9141e1b929c4f98b','decision-template.txt':'404b262d1c17ce5ee80f2b4146e0ee7283c0c887f13d4a5c86988cb0ebc1063e','folder-example.txt':'448d2ab4a2ee04e1680b7527bcf73695658355bf8047fe83b0b5dea67eee3cbd'}
  for asset in w['assets']:
   self.assertEqual(asset['sha256'],expected[asset['name']]);self.assertEqual(sha(asset['content'].encode()),expected[asset['name']])
   for out in ['site','docs']:self.assertEqual(sha((ROOT/out/w['asset_base']/asset['name']).read_bytes()),expected[asset['name']])
 def test_no_fabricated_audio_or_reference_output(self):
  w=music_task.catalog(ROOT);self.assertNotIn('sample_output',w);self.assertFalse(w['audio_generated']);self.assertEqual(w['product_execution'],'not_run');self.assertEqual(w['listening_test'],'not_run')
  self.assertEqual(list(w['sections']),music_task.PHASES)
  self.assertFalse(any(Path(p).suffix in ['.mp3','.wav','.ogg','.mp4'] for p in (ROOT/'learning/task-first/r1/music').rglob('*')))
 def test_closed_projection_rejects_extra_changed_missing_symlink(self):
  for mode in ['extra','changed','missing','symlink','projection']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);folder=root/'learning/task-first/r1/music';shutil.copytree(ROOT/'learning/task-first/r1/music',folder)
    if mode=='extra':(folder/'unregistered.txt').write_text('no')
    if mode=='changed':(folder/'brief.txt').write_text('no')
    if mode=='missing':(folder/'reader.md').unlink()
    if mode=='symlink':(folder/'reader.md').unlink();(folder/'reader.md').symlink_to(ROOT/'BOOK.md')
    if mode=='projection':
     p=folder/'projection.json';d=json.loads(p.read_text());d['public_file_sha256']['brief.txt']='0'*64;p.write_text(json.dumps(d))
    with self.assertRaises(ValueError):music_task.catalog(root)
 def test_public_projection_has_no_internal_paths_or_qa_material(self):
  folder=ROOT/'learning/task-first/r1/music'
  for path in folder.iterdir():
   text=path.read_text();self.assertNotIn('/workspace/',text);self.assertNotIn('/home/agent/',text)
   self.assertNotIn('independent-qa-r2/',text);self.assertNotIn('agentwork-learning-coverage-audit-r1/',text)
  self.assertFalse((folder/'REPORT.zh-CN.md').exists());self.assertFalse((folder/'VALIDATION.json').exists())
if __name__=='__main__':unittest.main()
