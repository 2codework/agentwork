"""Targeted editorial correction; no product execution or source-date upgrade."""
import copy, hashlib, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('creative_gaps',ROOT/'scripts/creative_gaps.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
class ExpressDisplayTests(unittest.TestCase):
 def test_exact_scope_raw_and_date(self):
  cases=G.load(ROOT);c=next(c for c in cases if c['id']==G.EXPRESS_ID)
  self.assertIn(G.EXPRESS_OLD_CHECK,c['raw_record']['original_exercise']['acceptance_checks'])
  self.assertIn(G.EXPRESS_CURRENT_CHECK,c['rubric'])
  for key in ('prompt','failure_recovery'):
   self.assertIn(G.EXPRESS_CURRENT_CHECK,c[key]);self.assertNotIn(G.EXPRESS_OLD_CHECK,c[key])
  self.assertIn(G.EXPRESS_EDIT_NOTE,c['evidence_note'])
  self.assertEqual(c['checked_at'],'2026-10-28')
  self.assertIn('周六14:00改为周日15:00',c['original_exercise_plan']['task'])
 def test_fail_closed_changed_missing_duplicate_source_sentence(self):
  for checks in ([G.EXPRESS_OLD_CHECK+'。'],[],[G.EXPRESS_OLD_CHECK]*2,[G.EXPRESS_CURRENT_CHECK]):
   with self.subTest(checks=checks),self.assertRaisesRegex(ValueError,'manual review'):
    G.current_display_checks(G.EXPRESS_ID,checks)
 def test_other_id_not_overridden_and_no_mutation(self):
  checks=[G.EXPRESS_OLD_CHECK];before=copy.deepcopy(checks)
  self.assertEqual(G.current_display_checks('gap-underlord-review',checks),checks)
  self.assertEqual(G.current_display_checks(G.EXPRESS_ID,checks),[G.EXPRESS_CURRENT_CHECK])
  self.assertEqual(checks,before)
 def test_generated_other_137_and_target_unrelated_fields_exact(self):
  f=json.loads((ROOT/'tests/fixtures/express-current-display-baseline.json').read_text())
  for path in ('site/data.json','docs/data.json'):
   d=json.loads((ROOT/path).read_text());self.assertEqual(len(d['cases']),138)
   self.assertEqual({c['id']:digest(c) for c in d['cases'] if c['id']!=G.EXPRESS_ID},f['cases'])
   c=next(c for c in d['cases'] if c['id']==G.EXPRESS_ID)
   self.assertEqual({k:digest(v) for k,v in c.items() if k not in ('rubric','prompt','failure_recovery','evidence_note')},f['target_unchanged_fields'])
   self.assertEqual({k:digest(v) for k,v in d.items() if k!='cases'},f['top_level'])
 def test_book_shows_editorial_date_not_vendor_update(self):
  self.assertIn(G.EXPRESS_EDIT_NOTE,(ROOT/'BOOK.md').read_text())

class HistoricalDisplayGuardTests(unittest.TestCase):
 def test_original_hashes_still_required(self):
  from express_display_guard import historical_bytes
  pins=json.loads((ROOT/'tests/fixtures/creative-delivery-baseline.json').read_text())['sha256']
  for name in ('BOOK.md','site/data.json','docs/data.json'):
   self.assertEqual(hashlib.sha256(historical_bytes(ROOT,name,(ROOT/name).read_bytes())).hexdigest(),pins[name])
 def test_mutations_cannot_pass_historical_hash(self):
  from express_display_guard import historical_bytes
  pins=json.loads((ROOT/'tests/fixtures/creative-delivery-baseline.json').read_text())['sha256']
  for name in ('BOOK.md','site/data.json','docs/data.json'):
   data=(ROOT/name).read_bytes()
   variants=[data.replace(G.EXPRESS_CURRENT_CHECK.encode(),b'changed',1),
             data.replace(G.EXPRESS_EDIT_NOTE.encode(),b'wrong date',1),data+b' ']
   if name.endswith('data.json'):
    d=json.loads(data);d['cases'][0]['title']+='changed'
    variants.append(json.dumps(d,ensure_ascii=False,separators=(',',':')).encode())
    d=json.loads(data);c=next(c for c in d['cases'] if c['id']==G.EXPRESS_ID);del c['failure_recovery']
    variants.append(json.dumps(d,ensure_ascii=False,separators=(',',':')).encode())
   for mutated in variants:
    try:restored=historical_bytes(ROOT,name,mutated)
    except ValueError:continue
    self.assertNotEqual(hashlib.sha256(restored).hexdigest(),pins[name])
