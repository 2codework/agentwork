import copy
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate_fixture, evaluate

def fixture(name='debug'):
    return json.loads((ROOT / 'fixtures' / ('mcp-lab-' + name + '.json')).read_text())

class ContractTests(unittest.TestCase):
    def test_all_fixtures(self):
        for p in (ROOT / 'fixtures').glob('*.json'):
            with self.subTest(p=p.name):
                validate_fixture(json.loads(p.read_text()))
    def test_wrong_id(self):
        f=fixture(); f['input'][-1]['message']['id']=999
        with self.assertRaisesRegex(ValueError, 'pending'): evaluate(f)
    def test_bad_argument(self):
        f=fixture(); f['input'][-2]['message']['params']['arguments']['a']='7'
        with self.assertRaisesRegex(ValueError, 'argument'): evaluate(f)
    def test_before_initialize(self):
        f=fixture(); f['input']=f['input'][3:]
        with self.assertRaisesRegex(ValueError, 'before initialize'): evaluate(f)
    def test_result_error_exclusive(self):
        f=fixture(); f['input'][-1]['message']['error']={'code':-1,'message':'bad'}
        with self.assertRaisesRegex(ValueError, 'XOR'): evaluate(f)
    def test_bad_total(self):
        f=fixture(); f['input'][-1]['message']['result']['structuredContent']['total']=13
        with self.assertRaisesRegex(ValueError, 'total'): evaluate(f)
    def test_wrong_version(self):
        f=fixture(); f['input'][1]['message']['result']['protocolVersion']='2026-07-28'
        with self.assertRaisesRegex(ValueError, 'unsupported'): evaluate(f)
    def test_cancel_initialize(self):
        f=fixture('cancel'); f['input']=[f['input'][0], {'direction':'client_to_server','message':{'jsonrpc':'2.0','method':'notifications/cancelled','params':{'requestId':1}}}]
        with self.assertRaisesRegex(ValueError, 'cancel initialize'): evaluate(f)
    def test_cancel_unknown(self):
        f=fixture('cancel'); f['input'][-1]['message']['params']['requestId']=44
        with self.assertRaisesRegex(ValueError, 'in-flight'): evaluate(f)
    def test_duplicate_id(self):
        f=fixture(); f['input'][-2]['message']['id']=2
        with self.assertRaisesRegex(ValueError, 'duplicate'): evaluate(f)
    def test_boolean_id(self):
        f=fixture(); f['input'][0]['message']['id']=True
        with self.assertRaisesRegex(ValueError, 'ID'): evaluate(f)
    def test_modern_missing_meta(self):
        f=fixture('modern'); f['input'][0]['message']['params']={}
        with self.assertRaisesRegex(ValueError, 'version missing'): evaluate(f)
    def test_modern_missing_result_type(self):
        f=fixture('modern'); del f['input'][1]['message']['result']['resultType']
        with self.assertRaisesRegex(ValueError, 'resultType'): evaluate(f)
    def test_scope_still_needs_approval(self):
        f=fixture('scope'); f['input']['granted_scopes'].append('inventory:write')
        self.assertEqual(evaluate(f)['denied'], ['delete_inventory'])
    def test_injection_allowlist(self):
        f=fixture('injection'); f['input']['allowed_fields'].append('note')
        with self.assertRaisesRegex(ValueError, 'only permits'): evaluate(f)
    def test_skill_name(self):
        f=fixture('skill'); f['input']['directory']='different'
        with self.assertRaisesRegex(ValueError, 'metadata'): evaluate(f)
    def test_history_preserved(self):
        f=fixture('migration'); f['input']['archived_versions']=[]
        with self.assertRaisesRegex(ValueError, 'history'): evaluate(f)
    def test_metadata_and_sources(self):
        cases=json.loads((ROOT/'cases.json').read_text())['cases']
        sources=json.loads((ROOT/'sources.json').read_text())['sources']
        ids={s['id'] for s in sources}
        self.assertEqual(len(cases),12)
        self.assertEqual(len({c['id'] for c in cases}),12)
        for c in cases:
            self.assertTrue(set(c['source_ids']) <= ids)
            self.assertTrue(c['synthetic'])
            for key in ('goal','prerequisites','input','prompt','steps','output','rubric','common_errors','permissions','applicable_versions','lifecycle','checked_at'):
                self.assertTrue(c[key],key)
            self.assertTrue((ROOT/c['fixture']).is_file())
        for s in sources:
            self.assertTrue(s['url'].startswith('https://'))
            self.assertEqual(s['checked_at'],'2026-10-28')

if __name__=='__main__': unittest.main()
