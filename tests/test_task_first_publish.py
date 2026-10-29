"""Quiescent tree preflight regressions, not concurrent filesystem security."""
import unittest,tempfile,shutil,hashlib,os,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import task_first as tf
import build as builder
def snapshot(root):
 return {p.relative_to(root).as_posix():('link',os.readlink(p)) if p.is_symlink() else ('file',hashlib.sha256(p.read_bytes()).hexdigest()) if p.is_file() else ('dir',) for p in root.rglob('*') if '__pycache__' not in p.parts}
class PublishPreflight(unittest.TestCase):
 def test_all_output_targets_reject_before_any_mutation(self):
  names=['task-first-data.json','index.html','product-books.html','library.html','product-library.html','task-first.js','product-bench-offline-r1.zip','task-guides/workflows/downloads/clean-orders-inputs.zip']
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);sentinel=root/'sentinel';sentinel.write_bytes(b'EXTERNAL SAFE')
   for folder in ['site','docs']:
    dest=root/folder;shutil.copytree(ROOT/folder,dest)
    for name in names:
     with self.subTest(folder=folder,name=name):
      target=dest/name;original=target.read_bytes();target.unlink();target.symlink_to(sentinel);before=snapshot(dest)
      with self.assertRaisesRegex(ValueError,'symlink'):tf.publish(ROOT,dest)
      self.assertEqual(sentinel.read_bytes(),b'EXTERNAL SAFE');self.assertEqual(snapshot(dest),before)
      target.unlink();target.write_bytes(original)
 def test_build_checks_both_trees_before_book_or_any_output_mutation(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'root';root.mkdir()
   for name in ['web','learning/task-first/r1']:shutil.copytree(ROOT/name,root/name)
   shutil.copyfile(ROOT/'publication-destinations.json',root/'publication-destinations.json')
   (root/'BOOK.md').write_text('KEEP BOOK')
   for folder in ['site','docs']:(root/folder).mkdir();(root/folder/'index.html').write_text('KEEP OUTPUT')
   sentinel=Path(t)/'sentinel';sentinel.write_text('KEEP EXTERNAL')
   oldroot=builder.ROOT
   try:
    builder.ROOT=root
    for folder,name in [('site','index.html'),('docs','index.html'),('docs','product-bench-offline-r1.zip')]:
     target=root/folder/name;original=target.read_bytes() if target.exists() else None
     if target.exists():target.unlink()
     target.symlink_to(sentinel);before=snapshot(root)
     with self.subTest(folder=folder,name=name):
      with self.assertRaisesRegex(ValueError,'symlink'):builder.build()
      self.assertEqual(snapshot(root),before);self.assertEqual(sentinel.read_text(),'KEEP EXTERNAL')
     target.unlink()
     if original is not None:target.write_bytes(original)
   finally:builder.ROOT=oldroot
 def test_unregistered_file_empty_directory_and_ancestor_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   parent=Path(t);dest=parent/'out';shutil.copytree(ROOT/'site',dest)
   for name,isdir in [('unexpected.txt',False),('unregistered-empty',True)]:
    target=dest/name;target.mkdir() if isdir else target.write_text('extra');before=snapshot(dest)
    with self.assertRaisesRegex(ValueError,'unregistered'):tf.publish(ROOT,dest)
    self.assertEqual(snapshot(dest),before);target.rmdir() if isdir else target.unlink()
   alias=parent/'alias';alias.symlink_to(parent,target_is_directory=True);before=snapshot(dest)
   with self.assertRaisesRegex(ValueError,'symlink'):tf.publish(ROOT,alias/'out')
   self.assertEqual(snapshot(dest),before)
 def test_nonregular_destination_and_source_page_are_rejected_before_mutation(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'root';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   target=root/'site/task-first-data.json';original=target.read_bytes();target.unlink();target.mkdir();before=snapshot(root/'site')
   with self.assertRaises(ValueError):tf.publish(root,root/'site')
   self.assertEqual(snapshot(root/'site'),before);target.rmdir();target.write_bytes(original)
   page=root/'web/index.html';page.unlink();page.symlink_to(ROOT/'web/index.html');before=snapshot(root/'site')
   with self.assertRaisesRegex(ValueError,'symlink'):tf.publish(root,root/'site')
   self.assertEqual(snapshot(root/'site'),before)
 def test_missing_pin_dependency_does_not_partially_rewrite_output(self):
  with tempfile.TemporaryDirectory() as t:
   dest=Path(t)/'out';shutil.copytree(ROOT/'site',dest);(dest/'reader.js').unlink();before=snapshot(dest)
   with self.assertRaises(ValueError):tf.publish(ROOT,dest)
   self.assertEqual(snapshot(dest),before)
 def test_phase_source_fingerprint_is_enforced(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);shutil.copytree(ROOT/'learning/task-first/r1',root/'learning/task-first/r1');f=root/'learning/task-first/r1';p=f/'phase-presentation.json';d=json.loads(p.read_text());next(iter(d['workflows'].values()))['source_record_sha256']='0'*64;p.write_text(json.dumps(d));idx=json.loads((f/'index.json').read_text());idx['publication_files'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest();(f/'index.json').write_text(json.dumps(idx))
   with self.assertRaisesRegex(ValueError,'source binding'):tf.catalog(root)

class WholeBuildSourceAssets(unittest.TestCase):
 def test_known_source_page_unsafe_or_missing_assets_reject_before_any_write(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'root';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   (root/'BOOK.md').write_text('UNCHANGED BOOK MARKER')
   oldroot=builder.ROOT
   try:
    builder.ROOT=root
    for filename in ['index.html','product-books.html','library.html','product-library.html']:
     page=root/'web'/filename;original=page.read_text()
     for asset in ['../outside.js','https://example.invalid/outside.js','missing-dependency.js']:
      with self.subTest(filename=filename,asset=asset):
       import re
       mutated=re.sub(r'(<script\b[^>]*\bsrc=")[^"]+',lambda m:m.group(1)+asset,original,count=1)
       self.assertNotEqual(mutated,original);page.write_text(mutated);before=snapshot(root)
       with self.assertRaises(ValueError):builder.build()
       self.assertEqual(snapshot(root),before)
     page.write_text(original)
   finally:builder.ROOT=oldroot
 def test_valid_clean_build_keeps_preflight_compatible(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'root';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
   shutil.rmtree(root/'site');shutil.rmtree(root/'docs');oldroot=builder.ROOT
   try:builder.ROOT=root;builder.build()
   finally:builder.ROOT=oldroot
   for folder in ['site','docs']:
    for name in ['task-first-data.json','index.html','product-books.html','product-bench-offline-r1.zip']:
     self.assertEqual((root/folder/name).read_bytes(),(ROOT/folder/name).read_bytes())

if __name__=='__main__':unittest.main()
