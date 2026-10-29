import copy,importlib.util,json,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lesson_type_builder',ROOT/'scripts/build.py');B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
class LessonTypeGuardTests(unittest.TestCase):
 def setUp(self):self.data=json.loads((ROOT/'site/data.json').read_text())
 def test_current_138_and_missing_are_unchanged(self):
  before=copy.deepcopy(self.data);self.assertIs(B.validate(self.data),self.data);self.assertEqual(self.data,before)
  self.assertEqual(sum('lesson_markdown' not in c for c in self.data['cases']),126)
 def test_invalid_types_and_empty_values_rejected(self):
  for value in [None,False,True,0,7,0.5,[],{}, {'html':'<script>bad</script>'},'', ' \n\t']:
   with self.subTest(value=value):
    d=copy.deepcopy(self.data);c=next(c for c in d['cases'] if c['id']=='mcp-lab-tools');c['lesson_markdown']=value
    with self.assertRaisesRegex(ValueError,'lesson_markdown.*mcp-lab-tools'):B.validate(d)
 def test_nonblank_string_not_trimmed(self):
  c=self.data['cases'][0];c['lesson_markdown']=' \n### 原文\n  ';B.validate(self.data);self.assertEqual(c['lesson_markdown'],' \n### 原文\n  ')
 def test_final_merge_rejects_before_book_or_outputs(self):
  original=B.mcp_learning.load
  def injected(root):
   book,cases,bundle=original(root);cases[0]['lesson_markdown']={};return book,cases,bundle
  with patch.object(B.mcp_learning,'load',side_effect=injected),patch.object(B,'write_book') as write:
   with self.assertRaisesRegex(ValueError,'lesson_markdown'):B.build()
   write.assert_not_called()
