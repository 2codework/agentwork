"""Compact transport encoding; no source, evidence or progress schema changes."""
import hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUTPUT='site'

def strict(data):
 def pairs(items):
  result={}
  for key,value in items:
   if key in result: raise ValueError('duplicate key')
   result[key]=value
  return result
 def invalid(value): raise ValueError(value)
 return json.loads(data,object_pairs_hook=pairs,parse_constant=invalid)

class CompactDataTests(unittest.TestCase):
 def test_strict_encoding_and_output_semantics(self):
  raw=(ROOT/OUTPUT/'data.json').read_bytes(); data=strict(raw)
  self.assertEqual(raw,(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode())
  # Complete output parity; baseline-to-candidate equality is audited separately.
  self.assertEqual(data,strict((ROOT/'docs/data.json').read_bytes()))
  self.assertEqual(data,strict(json.dumps(data,ensure_ascii=False,indent=2)))
 def test_both_outputs_and_pins(self):
  raw=(ROOT/OUTPUT/'data.json').read_bytes()
  self.assertEqual(raw,(ROOT/'docs/data.json').read_bytes())
  digest=hashlib.sha256(raw).hexdigest()
  for folder in (OUTPUT,'docs'):
   html=(ROOT/folder/'index.html').read_text()
   self.assertEqual(re.findall(r'data-data-url="([^"]+)"',html),['data.json?v='+digest])

 def test_compact_roundtrip_preserves_string_whitespace_and_types(self):
  fixture={'中文':'  原文  \n下一行\t不去空白','unknown':None,'items':['b','a',False,0,{'nested':'a b'}]}
  compact=(json.dumps(fixture,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
  self.assertEqual(strict(compact),fixture)
  self.assertIn('原文'.encode(),compact)
  for invalid in ('{"id":1,"id":2}','{"value":NaN}','{"value":Infinity}'):
   with self.assertRaises(ValueError):strict(invalid)
