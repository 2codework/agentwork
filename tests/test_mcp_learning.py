import copy,importlib.util,json,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mcp_adapter',ROOT/'scripts/mcp_learning.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
class MCPLearning(unittest.TestCase):
 def test_complete_reader_projection(self):
  _,cases,bundle=M.load(ROOT)
  self.assertEqual(len(cases),12);self.assertEqual(len(bundle['nodes']),12)
  for c,n in zip(cases,bundle['nodes']):
   self.assertEqual(c['raw_record']['id'],c['id'])
   for field in ['goal','permissions','input','output','prompt','evidence_note','applicable_versions']:
    self.assertIn(c[field],c['lesson_markdown'])
   for field in ['prerequisites','common_errors','rubric']:
    for item in c[field]:self.assertIn(item,c['lesson_markdown'])
   for step in c['steps']:self.assertIn(step['body'],c['lesson_markdown']);self.assertIn(step['check'],c['lesson_markdown'])
   self.assertEqual(n['tutorial_markdown'],c['lesson_markdown'])
   self.assertTrue(c['modelatlas_links'][0]['url'].endswith('?node='+n['id']))
   self.assertTrue(n['agentwork_links'][0]['url'].endswith('?case='+c['id']))
   for source in c['sources']:self.assertIn(source['url'],c['lesson_markdown']);self.assertIn(source['claim'],c['lesson_markdown'])
 def mutate(self,fn,path='cases.json'):
  with tempfile.TemporaryDirectory() as temp:
   r=Path(temp);shutil.copytree(ROOT/'learning',r/'learning');p=r/'learning/mcp/raw'/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d))
   with self.assertRaises((ValueError,TypeError,KeyError)):M.load(r)
 def test_bad_goal(self):self.mutate(lambda d:d['cases'][0].update(goal=[]))
 def test_bad_prerequisites(self):self.mutate(lambda d:d['cases'][0].update(prerequisites='JSON'))
 def test_bad_errors(self):self.mutate(lambda d:d['cases'][0].update(common_errors=[{}]))
 def test_bad_permissions(self):self.mutate(lambda d:d['cases'][0].update(permissions=True))
 def test_unknown_extension(self):self.mutate(lambda d:d['cases'][0].update(unknown_extension='hidden'))
 def test_bad_fixture_path(self):self.mutate(lambda d:d['cases'][0].update(fixture='../bad'))
 def test_fixture_mismatch(self):self.mutate(lambda d:d['cases'][0].update(output='{}'))
 def test_bad_source_ref(self):self.mutate(lambda d:d['cases'][0].update(source_ids=['missing']))
 def test_bad_suggestion(self):self.mutate(lambda d:d['modelatlas_tutorial_nodes'][0].update(verification_status='actually_run'),'integration-suggestions.json')
 def test_skills_overlay_does_not_rewrite_history(self):
  _,cases,_=M.load(ROOT);c=next(c for c in cases if c['id']=='mcp-lab-skill')
  self.assertIn('SEP-2640',c['lesson_markdown']);self.assertNotIn('skills-extension',c['raw_record']['source_ids'])
  self.assertEqual(c['raw_record'],next(c for c in json.loads((ROOT/'learning/mcp/raw/cases.json').read_text())['cases'] if c['id']=='mcp-lab-skill'))
