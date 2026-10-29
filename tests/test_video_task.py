"""Source/asset/phase checks only; no Descript execution or subjective listening."""
import unittest,hashlib,json,re,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import video_task,task_first
sha=lambda b:hashlib.sha256(b).hexdigest()
def record(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
class Video(unittest.TestCase):
 def test_original_ten_objects_guides_and_old_ids_remain_exact(self):
  old=json.loads((ROOT/'tests/fixtures/video-original-ten.json').read_text());new=task_first.catalog();self.assertEqual(len(new['workflows']),11)
  self.assertEqual({w['id']:record(w) for w in new['workflows'] if not w.get('video_workflow')},old['workflows'])
  for k in ['guides','chooser','legacy_case_ids']:self.assertEqual(record(new[k]),old[k])
 def test_source_assets_exact_size_hash_and_published_bytes(self):
  folder=ROOT/'learning/task-first/r1/video';projection=json.loads((folder/'projection.json').read_text());video_task.catalog(ROOT)
  for name,digest in projection['reader_original_sha256'].items():
   self.assertEqual(sha((folder/name).read_bytes()),digest)
   for out in ['site','docs']:self.assertEqual((folder/name).read_bytes(),(ROOT/out/'task-guides/video'/name).read_bytes())
  media=folder/video_task.MEDIA;self.assertEqual(media.stat().st_size,2089879);self.assertEqual(sha(media.read_bytes()),'b1cc953778cff1667dffa48639ada5e91edbd4d299f1602c5cd9657f73355a2b')
  self.assertEqual([p.name for p in folder.rglob('*.mp4')],['paper-plane-synthetic-input-90s.mp4'])
 def test_prompt_preserves_every_original_character(self):
  w=video_task.catalog(ROOT);guide=(ROOT/'learning/task-first/r1/video/GUIDE.zh-CN.md').read_text();prompt=re.findall(r'```text\n(.*?)```',guide,re.S)
  self.assertEqual(len(prompt),1);self.assertEqual(w['prompt'],prompt[0]);self.assertEqual(sha(w['prompt'].encode()),'c0d13905d1e9624d99c9efcd6355732d4dd7bf7c21bddb2410613b504237d5b2')
  self.assertEqual([s['source_step'] for s in w['sections'].values()],[1,2,3,4,5,6]);self.assertEqual(w['sections']['setup']['prompt_asset'],'prompt.txt')
  self.assertIn('中文',w['sections']['prepare']['body']);self.assertIn('不支持',w['sections']['prepare']['body']);self.assertIn('Correct',w['sections']['tool']['body']);self.assertIn('Revert',w['sections']['example']['body']);self.assertIn('Local export',w['sections']['check']['body'])
 def test_vtt_exact_cue_preservation_and_fail_closed_parser(self):
  folder=ROOT/'learning/task-first/r1/video';srt=(folder/'assets/captions.en.srt').read_text();vtt=(folder/'assets/captions.en.vtt').read_text()
  self.assertEqual(vtt,video_task.srt_to_vtt(srt));self.assertEqual(len(re.findall(r' --> ',vtt)),17)
  self.assertEqual(vtt.removeprefix('WEBVTT\n\n'),re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2',srt))
  for bad in [srt.replace('1\n','2\n',1),srt.replace('00:00:00,000','bad',1),srt.replace('00:00:08,378','00:00:00,000',1),srt.replace('Here','<script>Here',1)]:
   with self.assertRaises(ValueError):video_task.srt_to_vtt(bad)
 def test_closed_pack_rejects_missing_extra_changed_symlink_and_manifest_edits(self):
  for mode in ['extra','missing','media','caption','symlink','projection']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);folder=root/'learning/task-first/r1/video';shutil.copytree(ROOT/'learning/task-first/r1/video',folder)
    if mode=='extra':(folder/'unexpected.mp4').write_bytes(b'no')
    elif mode=='missing':(folder/'GUIDE.zh-CN.md').unlink()
    elif mode=='media':(folder/video_task.MEDIA).write_bytes(b'no')
    elif mode=='caption':(folder/'assets/captions.en.vtt').write_text('WEBVTT\n\nwrong')
    elif mode=='symlink':(folder/'prompt.txt').unlink();(folder/'prompt.txt').symlink_to(ROOT/'BOOK.md')
    else:(folder/'projection.json').write_text('{}')
    with self.assertRaises(ValueError):video_task.catalog(root)
 def test_exact_source_phase_binding_not_just_keywords(self):
  folder=ROOT/'learning/task-first/r1/video';w=video_task.catalog(ROOT);guide=(folder/'GUIDE.zh-CN.md').read_text();parts=re.split(r'^## 第\d步：[^\n]+\n',guide,flags=re.M)[1:];self.assertEqual(len(parts),6)
  for key,part in zip(video_task.PHASES,parts):
   expected=part.strip();expected=re.sub(r'\]\((?!https://)([^)]+)\)',lambda m:'](task-guides/video/'+m[1]+')',expected)
   if key=='setup':
    before,rest=expected.split('```text\n');prompt,after=rest.split('```',1)
    self.assertEqual(w['sections'][key]['body'].strip(),before.strip());self.assertEqual(w['sections'][key]['after'].strip(),after.strip())
   else:self.assertEqual(w['sections'][key]['body'].strip(),expected)
 def test_public_projection_has_no_internal_paths_and_no_output_claim(self):
  folder=ROOT/'learning/task-first/r1/video';w=video_task.catalog(ROOT)
  self.assertEqual(w['product_execution'],'not_run');self.assertFalse(w['output_generated']);self.assertEqual(w['listening_test'],'pending');self.assertNotIn('sample_output',w)
  for p in folder.rglob('*'):
   if p.is_file() and p.suffix!='.mp4':
    text=p.read_text();self.assertNotIn('/workspace/',text);self.assertNotIn('/home/agent/',text);self.assertNotIn('internal/',text)
 def test_csp_unmodified_and_no_external_media_or_upload_controls(self):
  html=(ROOT/'web/index.html').read_text();csp=re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"',html)[1]
  self.assertEqual(csp,"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'none'")
  js=(ROOT/'web/task-first.js').read_text();section=js.split('function videoSection(')[1].split('function workflowSection(')[0]
  self.assertNotIn('autoplay',section);self.assertNotIn("type:'file'",section);self.assertNotIn('fetch(',section);self.assertIn("preload:'none'",section);self.assertNotIn('innerHTML',js)
if __name__=='__main__':unittest.main()
