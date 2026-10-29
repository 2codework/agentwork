import unittest,sys,json,hashlib,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import task_first as tf
class TaskFirst(unittest.TestCase):
 def test_six_complete_workflows_and_three_connections(self):
  d=tf.catalog();self.assertEqual(d['status'],'ready');self.assertEqual(len([w for w in d['workflows'] if not w.get('office_expansion') and not w.get('music_workflow') and not w.get('video_workflow')]),6);self.assertEqual(len([w for w in d['workflows'] if w.get('office_expansion')]),3);self.assertEqual(len(d['workflows']),11);self.assertEqual(len(d['guides']),3)
  for w in [w for w in d['workflows'] if not w.get('music_workflow') and not w.get('video_workflow')]:
   self.assertTrue(w['first_time']);self.assertTrue(w['prompt']);self.assertTrue(w['sample_output']);self.assertTrue(w['recovery'])
 def test_every_download_and_source_artifact_resolves(self):
  d=tf.catalog()
  for w in [w for w in d['workflows'] if not w.get('music_workflow') and not w.get('video_workflow')]:
   for a in w['input_files']:
    p=ROOT/'site'/(w['asset_base']+a['path']);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),a['sha256'])
   self.assertTrue((ROOT/'site'/(w['asset_base']+w['download_bundle'])).is_file())
   self.assertTrue((ROOT/'site'/w['source_artifact']).is_file())
 def test_full_author_objects_preserved_under_derived_fields(self):
  folder=ROOT/'learning/task-first/r1'
  raw=json.loads((folder/'workflows/workflows.json').read_text());d=tf.catalog()
  for old,new in zip(raw['recipes'],d['workflows']):
   for k,v in old.items():self.assertEqual(new[k],v,k)
  raw=json.loads((folder/'connections/connections.json').read_text())
  for old,new in zip(raw['routes'],d['guides']):
   for k,v in old.items():self.assertEqual(new[k],v,k)
 def test_closed_inventory_rejects_unregistered_changed_and_symlink_files(self):
  for mode in ['extra','changed','symlink']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
    root=Path(t);shutil.copytree(ROOT/'learning/task-first/r1',root/'learning/task-first/r1');folder=root/'learning/task-first/r1'
    if mode=='extra':(folder/'extra.txt').write_text('unexpected')
    elif mode=='changed':(folder/'workflows/workflows.json').write_text('{}')
    else:(folder/'bad').symlink_to(ROOT/'site/data.json')
    with self.assertRaises(ValueError):tf.catalog(root)
 def test_registered_bad_fields_still_rejected(self):
  for mode in ['source','input','guide']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
    root=Path(t);shutil.copytree(ROOT/'learning/task-first/r1',root/'learning/task-first/r1');folder=root/'learning/task-first/r1'
    name='connections/connections.json' if mode=='guide' else 'workflows/workflows.json';p=folder/name;d=json.loads(p.read_text())
    if mode=='source':d['sources'][0]['url']='javascript:alert(1)'
    elif mode=='input':d['recipes'][0]['input_files'][0]['path']='../outside'
    else:d['routes'][0]['steps']=[None]
    p.write_text(json.dumps(d));idx=json.loads((folder/'index.json').read_text());idx['publication_files'][name]=hashlib.sha256(p.read_bytes()).hexdigest();(folder/'index.json').write_text(json.dumps(idx))
    with self.assertRaises(ValueError):tf.catalog(root)
 def test_new_shell_is_small_local_and_task_first(self):
  html=(ROOT/'web/index.html').read_text();css=(ROOT/'web/task-first.css').read_text()
  self.assertIn('task-first.js',html);self.assertNotIn('app.js',html);self.assertNotIn('hero',html)
  self.assertIn('repeat(3,minmax(0,1fr))',css);self.assertIn('repeat(2,minmax(0,1fr))',css);self.assertIn('grid-template-columns:1fr',css)
  self.assertNotIn('innerHTML',(ROOT/'web/task-first.js').read_text())
if __name__=='__main__':unittest.main()
