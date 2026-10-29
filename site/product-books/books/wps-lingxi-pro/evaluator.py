"""Strict original sidecar evaluator. No product/network execution or Office validation."""
import json,sys,pathlib,math
P=pathlib.Path(__file__).parent
MAX_BYTES=1048576
def load_strict(path):
 file=pathlib.Path(path)
 if file.stat().st_size>MAX_BYTES:raise ValueError('JSON exceeds 1 MiB limit')
 with file.open('rb') as stream:data=stream.read(MAX_BYTES+1)
 if len(data)>MAX_BYTES:raise ValueError('JSON exceeds 1 MiB limit')
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('duplicate key: '+k)
   out[k]=v
  return out
 def constant(x):raise ValueError('nonfinite constant: '+x)
 def finite_float(x):
  value=float(x)
  if not math.isfinite(value):raise ValueError('nonfinite parsed float: '+x)
  return value
 return json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=constant,parse_float=finite_float)
def compare(want,got,path='$'):
 errors=[]
 if isinstance(want,dict):
  if not isinstance(got,dict):return [path+': expected object']
  for k in set(got)-set(want):errors.append(path+'.'+k+': unexpected key')
  for k,v in want.items():
   if k not in got:errors.append(path+'.'+k+': missing')
   else:errors+=compare(v,got[k],path+'.'+k)
 elif isinstance(want,list):
  if not isinstance(got,list) or len(want)!=len(got):return [path+': array length/type mismatch']
  for i,(v,g) in enumerate(zip(want,got)):errors+=compare(v,g,path+'['+str(i)+']')
 elif isinstance(want,bool) or want is None:
  if got is not want:errors.append(path+': boolean/null mismatch')
 elif isinstance(want,(float,int)):
  if isinstance(got,bool) or not isinstance(got,(float,int)) or not math.isfinite(got) or abs(want-got)>0.0001:errors.append(path+': number mismatch')
 elif type(got)!=type(want) or got!=want:errors.append(path+': value mismatch')
 return errors
if __name__=='__main__':
 if len(sys.argv) not in (3,4) or (len(sys.argv)==4 and sys.argv[3]!='--edge'):raise SystemExit('usage: python evaluator.py <slug> <actual.json> [--edge]')
 slug=sys.argv[1]
 if slug not in {p.name for p in (P/'fixtures').iterdir() if p.is_dir()}:raise SystemExit('unknown slug')
 try:
  want=load_strict(P/'fixtures'/slug/('edge-expected.json' if len(sys.argv)==4 else 'expected.json'))
  got=load_strict(sys.argv[2]);errors=compare(want,got)
 except (ValueError,OSError,UnicodeError,RecursionError) as e:errors=['invalid JSON: '+str(e)]
 print(json.dumps({'scope':'structured_sidecar_only','product_execution':'not_established','passed':not errors,'errors':errors},ensure_ascii=False,indent=2))
 raise SystemExit(bool(errors))
