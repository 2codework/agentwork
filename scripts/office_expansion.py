"""Strict adapter for three admitted text-only exercises; never product execution."""
import hashlib,json,zipfile
from pathlib import Path
from urllib.parse import urlsplit
from product_books import require,load,local,inventory
IDS={'customer-reply':'客户与销售','three-day-content':'内容创作','design-handoff':'代码与产品'}
PHASES=['prepare','tools','setup','prompt','result','example','check']
def digest(data):return hashlib.sha256(data).hexdigest()
def record_hash(record):return digest(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def text(value):require(isinstance(value,str) and value.strip(),'office field must be nonempty text')
def texts(value):require(isinstance(value,list) and value and all(isinstance(v,str) and v.strip() for v in value),'office field must be nonempty text list')
def verify_files(folder,items,kind):
 require(isinstance(items,list) and items,'office files missing');seen=set()
 for a in items:
  require(isinstance(a,dict),'office file must be object')
  for key in ['name','path','content','sha256']:text(a.get(key))
  require(a['name']==Path(a['path']).name and a['name'] not in seen,'office filename mismatch/duplicate');seen.add(a['name'])
  require(a['path'].startswith(kind+'/'),'office artifact kind mismatch')
  p=local(folder,a['path']);require(digest(p.read_bytes())==a['sha256'],'office artifact hash mismatch')
  require(p.read_text()==a['content'],'office artifact content mismatch')
  if kind=='inputs':require(a.get('synthetic') is True,'office input must be synthetic')
  else:require(a.get('origin')=='author_reference','office output must be author reference')
def verify_zip(folder,name,items):
 with zipfile.ZipFile(local(folder,name)) as z:
  names=z.namelist();expected={a['name']:a for a in items}
  require(len(names)==len(set(names)) and set(names)==set(expected),'office ZIP inventory mismatch')
  for n in names:require(digest(z.read(n))==expected[n]['sha256'],'office ZIP content mismatch')
def validate_phases(w):
 phases=w.get('phases');require(isinstance(phases,list) and len(phases)==7,'office seven source phases required')
 require([p.get('id') if isinstance(p,dict) else None for p in phases]==PHASES,'office phase IDs/order mismatch')
 expected=[
  {'files':w['input_files']},
  {'choices':w['tools'],'first_time':w['first_time'],'cost':w['cost'],'privacy':w['privacy']},
  {'steps':w['setup']},{'steps':w['prompt_actions'],'text':w['prompt']},
  {'steps':w['result']},{'note':w['sample_note'],'files':w['output_files']},
  {'checks':w['checks'],'repair':w['repair']}]
 for phase,payload in zip(phases,expected):
  text(phase.get('title'));require(set(phase)=={'id','title'}|set(payload),'office phase field mismatch')
  for key,value in payload.items():require(phase[key]==value,'office phase payload mismatch: '+phase['id'])
def catalog(root):
 folder=root/'learning/task-first/r1/office-expansion'
 projection=load(local(folder,'projection.json'));files=inventory(folder)
 require(projection.get('schema_version')=='office-expansion-projection/1' and projection.get('mapping')=='PHASE-MAPPING.md','office projection schema/mapping')
 require(projection.get('source_ledger_sha256')=='9a2a890c39eee840e72d627ea67acad56be203abe61971f0721a9b8571079c5d','office original source ledger admission pin')
 pins=projection.get('public_file_sha256')
 require(isinstance(pins,dict) and set(files)==set(pins)|{'projection.json'},'office closed projection inventory')
 for name,sha in pins.items():require(digest(local(folder,name).read_bytes())==sha,'office projection file hash mismatch')
 # These pins identify the root-admitted portable content, not a live fetch or raw-package CI check.
 require(projection.get('raw_records_sha256')=='d5a49839f47319d5a79974e4568157889cb4d64768587d9b1c9605afbd8360f6','office admission record pin')
 require(projection.get('raw_manifest_sha256')=='5e5039ee6f9e35198b54f7818b0824b9144dd482a7c1e0c8a1e0e2413cd0c462','office admission manifest pin')
 require(digest(local(folder,'proposed-workflows.json').read_bytes())==projection['raw_records_sha256'],'office admitted record bytes changed')
 raw=load(local(folder,'proposed-workflows.json'));public_ledger=load(local(folder,'sources.json'))
 require(projection.get('public_source_ledger_sha256')=='28213bc70f19e62711a887ec24633a9f43c98b36d50e88acb9a1198ab0503097','office admitted portable source pin')
 require(digest(local(folder,'sources.json').read_bytes())==projection['public_source_ledger_sha256'],'office ledger binding mismatch')
 for field in ['source_files','accepted_input_and_reference_files']:
  for item in public_ledger[field]:
   from product_books import safe_name
   safe_name(item['path']);require(not item['path'].startswith('/'),'private absolute source path')
 sources={}
 for s in public_ledger['official_sources']:
  for key in ['id','title','url']:text(s.get(key))
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'unsafe office source')
  require(s['id'] not in sources,'duplicate office source');sources[s['id']]=s
 recipes=raw['recipes'];require(isinstance(recipes,list) and len(recipes)==3 and {w.get('id') for w in recipes}==set(IDS),'office exact three task IDs required')
 require(projection.get('editorial_categories')==IDS,'office category binding mismatch')
 mapping=raw['reader_phase_mapping']['steps']
 require([m.get('source_phases') for m in mapping]==[['prepare'],['tools'],['setup'],['prompt'],['result','example'],['check']],'office phase mapping mismatch')
 out=[]
 for w in recipes:
  for key in ['id','title','product','audience','outcome','cost','privacy','prompt','sample_note','sample_output','download_bundle','reference_bundle']:text(w.get(key))
  for key in ['first_time','setup','prompt_actions','result','checks','repair']:texts(w.get(key))
  require(w['product']=='腾讯 WorkBuddy' and w.get('product_execution')=='not_run' and w.get('ui_execution')=='not_run','office product/execution boundary')
  require(isinstance(w.get('tools'),dict),'office tool guidance required')
  for k in ['tools','mcp','skills']:text(w['tools'].get(k))
  require(w.get('materials')==w['input_files'] and w.get('tool_choices')==w['tools'],'office duplicated field mismatch')
  require(isinstance(w['sources'],list) and w['sources'] and all(isinstance(k,str) and k in sources for k in w['sources']),'unresolved office source')
  validate_phases(w);verify_files(folder,w['input_files'],'inputs');verify_files(folder,w['output_files'],'outputs')
  verify_zip(folder,w['download_bundle'],w['input_files']);verify_zip(folder,w['reference_bundle'],w['output_files'])
  require(w['sample_output']=='\n\n'.join('## '+a['name']+'\n'+a['content'] for a in w['output_files']),'office complete sample body mismatch')
  n=dict(w)
  n.update(access_cost=w['cost'],prerequisites=[w['audience']],steps=w['setup'],recovery=w['repair'],connection_guide_ids=[],category=IDS[w['id']],product_id='tencent-workbuddy',material_label=str(len(w['input_files']))+' 份练习材料',asset_base='task-guides/office-expansion/',source_artifact='task-guides/office-expansion/proposed-workflows.json',source_details=[sources[k] for k in w['sources']],office_expansion=True,reference_files=w['output_files'])
  n['reading_phases']={'source_record_sha256':record_hash(w),'source_fields':['phases'],'first_time':w['first_time'],'setup_steps':w['setup'],'prompt_steps':w['prompt_actions'],'result_steps':w['result']}
  n['source_phase_mapping']={'prepare':['prepare'],'tool':['tools'],'setup':['setup'],'prompt':['prompt'],'example':['result','example'],'check':['check']}
  out.append(n)
 return out
