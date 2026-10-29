"""Authored image integrity and editorial scope, not AI image-edit success."""
import unittest,hashlib,json,re,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import poster_task,task_first
sha=lambda b:hashlib.sha256(b).hexdigest()
def record(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
class Poster(unittest.TestCase):
 def test_original_twelve_full_objects_and_old_guides_cases_unchanged(self):
  old=json.loads((ROOT/'tests/fixtures/poster-original-twelve.json').read_text());new=task_first.catalog();self.assertEqual(len(new['workflows']),13)
  self.assertEqual({w['id']:record(w) for w in new['workflows'] if not w.get('poster_workflow')},old['workflows'])
  for key in ['guides','chooser','legacy_case_ids']:self.assertEqual(record(new[key]),old[key])
 def test_all_eleven_original_reader_files_and_published_copies_exact(self):
  folder=ROOT/'learning/task-first/r1/poster';p=json.loads((folder/'projection.json').read_text());self.assertEqual(len(p['reader_original_sha256']),11)
  for name,digest in p['reader_original_sha256'].items():
   self.assertEqual(sha((folder/name).read_bytes()),digest)
   for out in ['site','docs']:self.assertEqual((folder/name).read_bytes(),(ROOT/out/'task-guides/poster'/name).read_bytes())
  for name,(size,digest) in poster_task.PNG.items():
   data=(folder/name).read_bytes();self.assertEqual(len(data),size);self.assertEqual(sha(data),digest);self.assertEqual(poster_task.png_dimensions(data),(1080,1440))
  with self.assertRaises(ValueError):poster_task.png_dimensions(b'not a png')
 def test_safe_authored_svg_and_one_time_change_with_r2_footer(self):
  folder=ROOT/'learning/task-first/r1/poster/assets';before=(folder/'before.svg').read_text();after=(folder/'after-authored.svg').read_text()
  self.assertEqual(before.replace('>周六14:00<','>周日15:00<'),after)
  for body in [before,after]:
   poster_task.safe_svg(body);self.assertIn('原始输入：作者编写的合成教学素材',body);self.assertNotIn('未使用AI',body)
  for bad in [before.replace('<svg ','<svg onload="alert(1)" ',1),before.replace('</svg>','<script>alert(1)</script></svg>'),before.replace('</svg>','<image href="https://evil.test/a.png"/></svg>'),before.replace('text {','@import "https://evil.test/a.css"; text {'),before.replace('<svg','<!DOCTYPE svg [<!ENTITY x "bad">]><svg',1)]:
   with self.assertRaises(ValueError):poster_task.safe_svg(bad)
 def test_exact_two_prompts_and_original_six_source_bodies(self):
  folder=ROOT/'learning/task-first/r1/poster';guide=(folder/'GUIDE.zh-CN.md').read_text();w=poster_task.catalog(ROOT);prompts=re.findall(r'```text\n(.*?)```',guide,re.S)
  self.assertEqual([w['prompt'],w['correction_prompt']],prompts);self.assertEqual(len(prompts),2)
  parts=re.split(r'^## \d\. [^\n]+\n',guide,flags=re.M)[1:];self.assertEqual(len(parts),6)
  for key,part in zip(poster_task.PHASES,parts):
   expected=re.sub(r'\]\((?!https://)([^)]+)\)',lambda m:'](task-guides/poster/'+m[1]+')',part.strip())
   if key in ['setup','example']:
    pre,rest=expected.split('```text\n');_,after=rest.split('```',1);self.assertEqual(w['sections'][key]['body'].strip(),pre.strip());self.assertEqual(w['sections'][key]['after'].strip(),after.strip())
   else:self.assertEqual(w['sections'][key]['body'].strip(),expected)
  self.assertIn('页脚仅描述原始输入来源',w['prompt']);self.assertIn('不代表本次编辑没有使用AI',w['prompt'])
 def test_unknown_input_types_and_tampered_assets_fail_closed(self):
  for mode in ['extra','missing','png','svg','projection','mode','symlink']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);folder=root/'learning/task-first/r1/poster';shutil.copytree(ROOT/'learning/task-first/r1/poster',folder)
    if mode=='extra':(folder/'model-output.png').write_bytes(b'no')
    elif mode=='missing':(folder/'GUIDE.zh-CN.md').unlink()
    elif mode=='png':(folder/'assets/before.png').write_bytes(b'no')
    elif mode=='svg':(folder/'assets/before.svg').write_text('<svg onload="evil"/>')
    elif mode=='projection':(folder/'projection.json').write_text('{}')
    elif mode=='mode':
     p=folder/'workflow.json';d=json.loads(p.read_text());d['interaction_mode']='generated-output';p.write_text(json.dumps(d))
    else:(folder/'prompt.txt').unlink();(folder/'prompt.txt').symlink_to(ROOT/'BOOK.md')
    with self.assertRaises(ValueError):poster_task.catalog(root)
 def test_source_scope_no_private_paths_or_generated_result(self):
  folder=ROOT/'learning/task-first/r1/poster';w=poster_task.catalog(ROOT);self.assertEqual(w['product_execution'],'not_run');self.assertFalse(w['output_generated']);self.assertNotIn('sample_output',w)
  self.assertEqual(w['images'],{'before':'assets/before.png','reference':'assets/after-authored.png'});self.assertEqual(w['connection_guide_ids'],[])
  for p in folder.rglob('*'):
   if p.is_file() and p.suffix!='.png':
    value=p.read_text();self.assertNotIn('/workspace/',value);self.assertNotIn('/home/agent/',value);self.assertNotIn('internal/',value)
  self.assertIn('中国大陆',w['sections']['prepare']['body']);self.assertIn('不一定精确',w['sections']['tool']['body']);self.assertIn('未核验',w['sections']['prompt']['body']);self.assertIn('优先',w['sections']['example']['after'])
if __name__=='__main__':unittest.main()
