"""Closed author teaching negatives, not valid JSON; no glob exceptions.
Original creative registry is separate and unchanged. Quiescent files only.
"""
import hashlib, json, math
from pathlib import Path
ROWS = [('product-books/books/wps-lingxi-pro/fixtures/validator-tests/duplicate.json', '1c53ee0df7b12fd4d65b976120c7fa6b847dc41dffd7f0331c3237a1ceab1756', 'duplicate JSON key: a'), ('product-books/books/wps-lingxi-pro/fixtures/validator-tests/nan.json', '0ce896293703c00486a61416514acc94d2919f4bd42141dedcca7ddfb97ec422', 'non-finite JSON constant: NaN'), ('product-books/books/wps-lingxi-pro/fixtures/validator-tests/infinity.json', '02c7562cb7c8ca861c2534a206877f2e085e3ff3ce60362735791b0c1b4582b4', 'non-finite JSON constant: Infinity'), ('product-books/books/wps-lingxi-pro/fixtures/validator-tests/oversize.json', '9d78de4e5b12fc166bed811cd230621ea1e1e353553fe31b92a73bfbf45d68ee', 'oversize whitespace-only payload'), ('product-books/books/wps-lingxi-pro/fixtures/validator-tests/exponent-overflow.json', 'cb013dcc16fe0e5ca4b3588e94fedb08d57d0671c0bc216f27e5cd61b59d77b0', 'non-finite parsed float')]
REGISTRY_SHA256 = 'f848510beaffe289618d3511235ca2601b02a210fff952b2f04312304ab25ff7'

def require(ok,message):
    if not ok: raise ValueError(message)

def registry(rows=None):
    rows=ROWS if rows is None else rows
    require(len(rows)==5 and len({row[0] for row in rows})==5,'product negative registry duplicate/count mismatch')
    require(hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==REGISTRY_SHA256,'product negative registry changed')
    return {name:(digest,reason) for name,digest,reason in rows}

def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key: '+key);out[key]=value
    return out

def invalid(value): raise ValueError('non-finite JSON constant: '+value)
def finite_float(value):
    result=float(value);require(math.isfinite(result),'non-finite parsed float');return result

def loads(text): return json.loads(text,object_pairs_hook=unique,parse_constant=invalid,parse_float=finite_float)

def check(path,directory):
    name=path.relative_to(directory).as_posix();registered=registry()
    if name not in registered:return False
    digest,reason=registered[name];data=path.read_bytes()
    require(hashlib.sha256(data).hexdigest()==digest,'product negative fixture bytes changed: '+name)
    if reason=='oversize whitespace-only payload':
        require(len(data)==1048577 and not data.strip(),'product oversize negative changed')
        try:loads(data.decode('utf-8'))
        except json.JSONDecodeError:return True
        raise ValueError('product oversize fixture became valid')
    try:loads(data.decode('utf-8'))
    except ValueError as error:
        require(str(error)==reason,'product negative rejection reason changed: '+name);return True
    raise ValueError('product negative fixture unexpectedly valid: '+name)
