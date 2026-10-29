"""Closed materials and paste-message study contract; not learning-outcome evaluation."""
import unittest,hashlib,json,sys,tempfile,shutil,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import study_task,task_first
sha=lambda b:hashlib.sha256(b).hexdigest()
def record(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
class Study(unittest.TestCase):
 def test_original_eleven_objects_guides_oldcases_exact(self):
  old=json.loads((ROOT/'tests/fixtures/study-original-eleven.json').read_text());new=task_first.catalog();self.assertEqual(len(new['workflows']),12)
  self.assertEqual({w['id']:record(w) for w in new['workflows'] if not w.get('study_workflow')},old['workflows'])
  for k in ['guides','chooser','legacy_case_ids']:self.assertEqual(record(new[k]),old[k])
 def test_public_original_ten_files_and_published_copies_exact(self):
  folder=ROOT/'learning/task-first/r1/study';projection=json.loads((folder/'projection.json').read_text());original=projection['public_original_sha256'];self.assertEqual(set(original),set(study_task.ASSETS))
  for name,digest in original.items():
   self.assertEqual(sha((folder/name).read_bytes()),digest)
   for out in ['site','docs']:self.assertEqual((folder/name).read_bytes(),(ROOT/out/'task-guides/study'/name).read_bytes())
 def test_primary_full_message_is_exact_single_assembly_not_placeholder(self):
  w=study_task.catalog(ROOT);a=w['study_assets'];message=a['send-once.txt']
  self.assertEqual(message,a['card-prompt.txt'].rstrip()+'\n\n【固定材料】\n'+a['material.txt'].rstrip()+'\n【固定材料结束】\n')
  self.assertEqual(message.count(a['material.txt'].strip()),1);self.assertEqual(message.count('\n【固定材料】\n'),1);self.assertEqual(message.count('\n【固定材料结束】'),1)
  self.assertNotIn('这里粘贴',message);self.assertEqual(w['sections']['prompt']['prompt_asset'],'send-once.txt')
  self.assertIn('替换输入框现有内容',w['sections']['prompt']['body']);self.assertIn('先不提交',w['sections']['setup']['body'])
 def test_explicit_schema_source_order_and_selftest_boundary(self):
  w=study_task.catalog(ROOT);self.assertEqual(w['schema'],'study-workflow/1');self.assertEqual(w['interaction_mode'],'paste-material')
  self.assertEqual([s['source_step'] for s in w['sections'].values()],[1,2,3,4,5,6]);self.assertEqual(w['product_execution'],'not_run');self.assertEqual(w['user_results'],'not_collected');self.assertNotIn('sample_output',w)
  s=w['sections']['example'];self.assertEqual(s['questions_asset'],'self-test-questions.txt');self.assertEqual(s['answers_asset'],'self-test-answers.md');self.assertNotIn(w['study_assets']['self-test-answers.md'],s['body'])
  self.assertIn('不要让AI代答',s['body']);self.assertIn('正常学习',w['sections']['prompt']['after_send']);self.assertIn('不因此',w['sections']['prompt']['after_send'])
  for term in ['真实的一条原答','没有真实错误时跳过','不是系统提醒']:
   self.assertIn(term,'\n'.join(str(x) for x in w['sections'].values()))
 def test_closed_input_registry_rejects_changes_symlinks_and_private_extras(self):
  for mode in ['extra','missing','send','answer','mode','symlink','projection']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);folder=root/'learning/task-first/r1/study';shutil.copytree(ROOT/'learning/task-first/r1/study',folder)
    if mode=='extra':(folder/'internal.json').write_text('{}')
    elif mode=='missing':(folder/'material.txt').unlink()
    elif mode=='send':(folder/'send-once.txt').write_text('placeholder')
    elif mode=='answer':(folder/'self-test-answers.md').write_text('score100')
    elif mode=='mode':
     p=folder/'workflow.json';d=json.loads(p.read_text());d['interaction_mode']='attach-files';p.write_text(json.dumps(d))
    elif mode=='symlink':(folder/'error-log.md').unlink();(folder/'error-log.md').symlink_to(ROOT/'BOOK.md')
    else:(folder/'projection.json').write_text('{}')
    with self.assertRaises(ValueError):study_task.catalog(root)
 def test_no_internal_paths_or_extra_source_network_surface(self):
  folder=ROOT/'learning/task-first/r1/study'
  for p in folder.iterdir():
   text=p.read_text();self.assertNotIn('/workspace/',text);self.assertNotIn('/home/agent/',text);self.assertNotIn('internal/',text)
  js=(ROOT/'web/task-first.js').read_text().split('function studySection(')[1].split('function workflowSection(')[0]
  for token in ['fetch(',"type:'file'",'localStorage','innerHTML','setTimeout','<iframe']:self.assertNotIn(token,js)
 def test_primary_materials_and_answers_are_separate_registered_artifacts(self):
  w=study_task.catalog(ROOT);a=w['study_assets'];self.assertNotIn(a['self-test-answers.md'].strip(),a['send-once.txt']);self.assertNotIn(a['reference-cards.md'].strip(),a['send-once.txt']);self.assertIn('我的答案：',a['self-test-questions.txt'])
  self.assertIn('真实',a['correction-prompt.txt']);self.assertEqual(w['connection_guide_ids'],[]);self.assertEqual(w['input_files'],[])
if __name__=='__main__':unittest.main()
