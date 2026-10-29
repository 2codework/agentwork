"""Reconstruct three exact historical generated files; historical hashes stay fixed."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import creative_gaps as G
def need(ok):
 if not ok:raise ValueError('unexpected Express display delta')
def historical_bytes(root,name,data):
 if name not in ('BOOK.md','site/data.json','docs/data.json'):return data
 original=json.loads((root/'tests/fixtures/express-original-display.json').read_text())
 current=json.loads(json.dumps(original))
 for key in ('prompt','failure_recovery'):
  need(current[key].count(G.EXPRESS_OLD_CHECK)==1)
  current[key]=current[key].replace(G.EXPRESS_OLD_CHECK,G.EXPRESS_CURRENT_CHECK,1)
 need(current['rubric'].count(G.EXPRESS_OLD_CHECK)==1)
 current['rubric'][current['rubric'].index(G.EXPRESS_OLD_CHECK)]=G.EXPRESS_CURRENT_CHECK
 current['evidence_note']+=' '+G.EXPRESS_EDIT_NOTE
 if name.endswith('data.json'):
  doc=json.loads(data);targets=[c for c in doc['cases'] if c['id']==G.EXPRESS_ID]
  need(len(targets)==1 and targets[0]==current)
  # Exact serialized target span, not a global sentence replacement.
  serial=lambda c:json.dumps(c,ensure_ascii=False,separators=(',',':')).encode()
  old,new=serial(original),serial(current)
  need(data.count(new)==1)
  return data.replace(new,old,1)
 text=data.decode()
 header='## '+original['title']+'\n'
 need(text.count(header)==1)
 start=text.index(header);end=text.find('\n## ',start+len(header))
 if end<0:end=len(text)
 section=text[start:end]
 # BOOK renders the complete prompt and one rubric bullet, not failure_recovery.
 pairs=[(current['prompt'],original['prompt']),
        ('- 验收：'+G.EXPRESS_CURRENT_CHECK,'- 验收：'+G.EXPRESS_OLD_CHECK),
        ('**证据边界：** '+current['evidence_note'],'**证据边界：** '+original['evidence_note'])]
 for new,old in pairs:
  need(section.count(new)==1);section=section.replace(new,old,1)
 need(G.EXPRESS_CURRENT_CHECK not in section and G.EXPRESS_EDIT_NOTE not in section)
 return (text[:start]+section+text[end:]).encode()
