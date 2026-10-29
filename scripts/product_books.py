#!/usr/bin/env python3
"""Original offline contracts, never product execution. Python standard library only."""
import argparse, hashlib, json, re, shutil, sys, zipfile, os, stat, math
from pathlib import Path
from datetime import datetime, date
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parents[1]

def require(ok, message):
    if not ok: raise ValueError(message)
def unique(pairs):
    out = {}
    for k,v in pairs:
        require(k not in out, 'duplicate JSON key: '+k); out[k]=v
    return out
def finite_float(value):
    result=float(value);require(math.isfinite(result),'non-finite parsed float');return result
def load(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('non-finite JSON')),parse_float=finite_float)
def safe_name(name):
    require(isinstance(name,str) and name and not any(c in name for c in ['\\',':','\0']), 'unsafe path')
    require(all(x not in ('','.','..') for x in name.split('/')), 'unsafe path')
    return name

def no_symlink_ancestors(path):
    for parent in [path,*path.parents]:
        require(not parent.is_symlink(), 'symlink path/ancestor: '+str(parent))

def local(root, name):
    safe_name(name); p=root/name; no_symlink_ancestors(p)
    require(p.is_file() and p.resolve().is_relative_to(root.resolve()), 'missing/local path: '+name)
    return p

def inventory(folder):
    """Closed ordinary-file inventory. Assumes a quiescent checkout, not raceproof."""
    no_symlink_ancestors(folder)
    require(folder.is_dir(),'missing source directory')
    found={}
    def visit(directory):
        with os.scandir(directory) as entries:
            for entry in sorted(entries,key=lambda e:e.name):
                path=Path(entry.path);name=path.relative_to(folder).as_posix();safe_name(name)
                mode=entry.stat(follow_symlinks=False).st_mode
                require(not stat.S_ISLNK(mode),'symlink in publication tree: '+name)
                if stat.S_ISDIR(mode): visit(path)
                else:
                    require(stat.S_ISREG(mode),'nonregular publication entry: '+name)
                    found[name]=path
    visit(folder)
    return found

def registered_bytes(folder):
    files=inventory(folder)
    require('index.json' in files,'missing publication index')
    idx=load(files['index.json']);require(isinstance(idx,dict),'index must be object')
    manifest=idx.get('publication_files');require(isinstance(manifest,dict) and manifest,'publication_files must be nonempty object')
    for name,digest in manifest.items():
        safe_name(name);require(name!='index.json','index cannot self-register')
        require(isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest),'invalid publication hash')
    require(set(files)==set(manifest)|{'index.json'},'publication inventory mismatch: unregistered or missing files')
    blobs={name:path.read_bytes() for name,path in files.items()}
    for name,digest in manifest.items(): require(hashlib.sha256(blobs[name]).hexdigest()==digest,'publication hash mismatch: '+name)
    return blobs

def text_fields(obj, fields):
    require(isinstance(obj,dict),'expected object')
    for f in fields: require(isinstance(obj.get(f),str) and obj[f].strip(), 'missing text: '+f)

def array(obj,key,nonempty=False):
    require(isinstance(obj.get(key),list) and (not nonempty or obj[key]),'invalid array: '+key)
    return obj[key]

def identifier(value):
    require(isinstance(value,str) and re.fullmatch('[a-z0-9-]{1,100}',value),'invalid ID')

def source(s):
    text_fields(s,['id','title','url','accessed_at','claim_scope'])
    stamp=s['accessed_at']
    require(re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?',stamp) is not None,'invalid source date/timestamp')
    try:
        if 'T' in stamp: datetime.fromisoformat(stamp.replace('Z','+00:00'))
        else: date.fromisoformat(stamp)
    except ValueError: raise ValueError('invalid source date/timestamp')
    u=urlsplit(s['url']); require(u.scheme=='https' and u.hostname and not u.username and not u.password,'unsafe source URL')

def criteria(items, human=False):
    for item in items:
        if isinstance(item,str): require(bool(item.strip()),'blank criterion')
        else:
            require(isinstance(item,dict),'criterion must be text or description object')
            if human and 'criterion' in item:
                text_fields(item,['criterion','how_to_check'])
                require(type(item.get('points')) in (int,float) and math.isfinite(item['points']) and item['points']>=0,'invalid rubric points')
            elif not human and 'type' in item:
                text_fields(item,['id','type']);require(re.fullmatch('[a-z0-9_-]{1,100}',item['id']),'invalid criterion ID');kind=item['type']
                require(kind in ['human_fact','human_count','set_equals','group_sum'],'unknown criterion type')
                require('expected' in item and item['expected'] is not None,'missing criterion expected')
                if kind=='human_fact':
                    if 'source' in item: text_fields(item,['source'])
                    require(type(item['expected']) in (str,int,float,bool,list,dict),'invalid fact expectation')
                    if isinstance(item['expected'],(str,list,dict)):require(bool(item['expected']),'empty fact expectation')
                elif kind=='human_count': text_fields(item,['expected'])
                elif kind=='set_equals':
                    text_fields(item,['target']);require(isinstance(item['expected'],list) and item['expected'],'set expectation must be nonempty array')
                else:
                    text_fields(item,['target']);require(isinstance(item['expected'],dict) and item['expected'],'group expectation must be nonempty object')
                    require(all(type(v) in (int,float) and math.isfinite(v) for v in item['expected'].values()),'group sums must be finite numbers')
            else:
                text_fields(item,['id','description']);identifier(item['id'])
                if 'kind' in item: text_fields(item,['kind'])

def validate_record(obj, root, recipe=False):
    text_fields(obj,['title','role','business_goal','prompt','authorization','cost','privacy','version_scope','evidence_tier','reference_format','expected_product_artifact_format'])
    require('product_id' in obj and (isinstance(obj['product_id'],str) if recipe else obj['product_id'] is None),'product_id required')
    if recipe: identifier(obj['product_id'])
    else: require(obj.get('schema_version')=='1.0','task version')
    key='recipe_id' if recipe else 'task_id';identifier(obj.get(key))
    require('task_id' in obj and (obj['task_id'] is None or isinstance(obj['task_id'],str)), 'task_id required')
    if obj['task_id'] is not None: identifier(obj['task_id'])
    require(obj.get('runner_implemented') is False,'product adapter is not implemented')
    require(obj.get('expected_output_origin')=='author_reference','reference origin')
    expected=obj.get('expected_output')
    require((isinstance(expected,dict) and bool(expected)) or (isinstance(expected,str) and bool(expected.strip())),'reference must be nonempty object or text')
    require(obj.get('product_execution')=='not_run' and 'observed_results' in obj and obj['observed_results'] is None,'unsupported product evidence')
    require(obj['evidence_tier'] in ['documentation_review','synthetic_contract'],'invalid evidence tier')
    artifacts=list(array(obj,'input_artifacts',True))
    if 'expected_output_artifacts' in obj: artifacts+=array(obj,'expected_output_artifacts')
    for a in artifacts:
        text_fields(a,['path','sha256','description'])
        require(re.fullmatch('[0-9a-f]{64}',a['sha256']),'invalid artifact hash')
        p=local(root,a['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],'input hash mismatch: '+a['path'])
    for step in array(obj,'steps',True): text_fields(step,['title','instruction','check','failure_recovery'])
    criteria(array(obj,'objective_checks',True));criteria(array(obj,'human_rubric',True),True)
    for item in array(obj,'sources',recipe): source(item)
    if 'ui_execution' in obj: require(obj['ui_execution']=='not_run','unsupported UI evidence')
    # Rich provenance/risk/raw_record objects are not projected away or rewritten.
    return obj

def contract_sha256(obj):
    """Exact semantic JSON contract, excluding product-specific prompt/UI workflow."""
    contract={k:obj[k] for k in ['business_goal','expected_output_origin','expected_output','objective_checks','human_rubric','reference_format','expected_product_artifact_format']}
    contract['input_sha256']=[a['sha256'] for a in obj['input_artifacts']]
    contract['reference_artifact_sha256']=[a['sha256'] for a in obj.get('expected_output_artifacts',[])]
    return hashlib.sha256(json.dumps(contract,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def validate_index(idx):
    require(isinstance(idx,dict) and idx.get('schema_version')=='1.0','index version')
    text_fields(idx,['scope'])
    for key in ['tasks','books']:
        names=array(idx,key,key=='tasks')
        for name in names:safe_name(name)
        require(len(names)==len(set(names)),'duplicate index path')
    if 'guides' in idx: array(idx,'guides')
    seen=set()
    for item in array(idx,'research_queue'):
        text_fields(item,['product_id','vendor','name','display_name','status','note']);identifier(item['product_id'])
        require(item['product_id'] not in seen,'duplicate queued identity');seen.add(item['product_id'])
        require(item['status'] in ['awaiting_review','catalog_only_playbooks_pending'],'invalid queued status')
        if 'sources' in item:
            for src in array(item,'sources'):source(src)

def catalog(root=ROOT):
    folder=root/'product-books'; registered_bytes(folder);idx=load(local(folder,'index.json'));validate_index(idx)
    for item in idx['research_queue']:
        if 'catalog_path' in item:
            identity=load(local(folder,item['catalog_path']))
            require(identity.get('product',{}).get('product_id')==item['product_id'],'catalog identity mismatch')
    tasks=[validate_record(load(local(folder,n)),folder) for n in idx['tasks']]
    require(len({t['task_id'] for t in tasks})==len(tasks),'duplicate task ID')
    task_ids={t['task_id']:t for t in tasks}; books=[]; product_ids=set(); recipe_ids=set()
    for name in idx['books']:
        path=local(folder,name); b=load(path);require(isinstance(b,dict),'book object required');product=b.get('product');require(isinstance(product,dict),'product object required')
        require(product.get('status')=='researched','unreviewed product status')
        require(b.get('schema_version')=='1.0','book version'); text_fields(product,['product_id','vendor','name','display_name','version_scope'])
        require(re.fullmatch('[a-z0-9-]{1,100}',product['product_id']) is not None,'invalid product ID')
        require(isinstance(b['recipes'],list) and b['recipes'],'public book requires delivered recipes; use research_queue for identity-only entries')
        array(product,'sources',True)
        require(product['product_id'] not in product_ids,'duplicate product');product_ids.add(product['product_id'])
        for s in product['sources']: source(s)
        for rec in b['recipes']:
            validate_record(rec,path.parent,True)
            require(rec['recipe_id'] not in recipe_ids,'duplicate recipe');recipe_ids.add(rec['recipe_id'])
            require(rec.get('product_id',product['product_id'])==product['product_id'],'product mismatch')
            require(rec['task_id'] is None or rec['task_id'] in task_ids,'unresolved task mapping')
        for rec in b['recipes']:
            # Lossless normalization: preserve all original fields, merge reference paths
            # into an additional explicit path/hash list. Do not infer product execution.
            expected=rec['expected_output'];refs=[]
            if isinstance(expected,dict):
                for key in ['files','example_files','reference_files']:
                    if key in expected:
                        require(isinstance(expected[key],list),'reference paths must be array')
                        for item in expected[key]:
                            if isinstance(item,str):refs.append(item)
                            else:
                                text_fields(item,['path']);refs.append(item['path'])
                refs.extend(expected[k] for k in ['patch_path','fixture_path'] if isinstance(expected.get(k),str))
            if 'reference_files' in rec:
                for item in array(rec,'reference_files'):
                    require(isinstance(item,str),'reference_files path must be text');refs.append(item)
            existing={a['path'] for a in rec.get('expected_output_artifacts',[])}
            rec.setdefault('expected_output_artifacts',[])
            for ref in dict.fromkeys(refs):
                file=local(path.parent,ref)
                if ref not in existing:
                    rec['expected_output_artifacts'].append({'path':ref,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'description':'作者参考文件（非产品输出）'})
            if rec['task_id'] is not None:
                fingerprint=contract_sha256(task_ids[rec['task_id']])
                require(rec.get('task_contract_sha256')==fingerprint and contract_sha256(rec)==fingerprint,'task contract binding mismatch; use null for unmatched recipe')
            else: require(rec.get('task_contract_sha256') is None,'null task cannot carry a binding')
        b['asset_base']='product-books/'+str(path.parent.relative_to(folder))+'/'
        books.append(b)
    for guide in idx.get('guides',[]):
        text_fields(guide,['product_id','path','sha256','title','checked_at','source_scope'])
        require(guide['product_id'] in product_ids,'guide product is not admitted')
        p=local(folder,guide['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==guide['sha256'],'guide hash mismatch')
        require(isinstance(guide.get('source_ids'),list) and all(isinstance(x,str) and x for x in guide['source_ids']),'invalid guide sources')
        book=next(b for b in books if b['product']['product_id']==guide['product_id'])
        require(set(guide['source_ids']).issubset({x['id'] for x in book['product']['sources']}),'unresolved guide source')
        book.setdefault('handbooks',[]).append(dict(guide,markdown=p.read_text(encoding='utf-8')))
    if 'editorial_navigation' in idx:
        nav=load(local(folder,idx['editorial_navigation']))
        require(isinstance(nav,dict) and nav.get('schema_version')=='1.0','navigation schema')
        facets=nav.get('role_facets');require(isinstance(facets,dict),'role facets must be object')
        records={r['recipe_id']:(b,r) for b in books for r in b['recipes']}
        require(set(facets)==set(records),'role facet coverage must match admitted recipes')
        for rid,facet in facets.items():
            b,rec=records[rid];text_fields(facet,['product_id','source_role','source_role_sha256','basis'])
            require(facet['product_id']==rec['product_id'] and facet['source_role']==rec['role'],'role source mismatch')
            require(hashlib.sha256(rec['role'].encode()).hexdigest()==facet['source_role_sha256'],'role source hash mismatch')
            tags=array(facet,'role_tags',True)
            require(all(isinstance(tag,str) and 0<len(tag)<=12 and tag.strip()==tag for tag in tags) and len(tags)==len(set(tags)),'invalid concise role tags')
            require('role_tags' not in rec and 'display_role' not in rec,'derived role field collision')
            rec['role_tags']=tags;rec['display_role']=' · '.join(tags)
        seen=set()
        for route in array(nav,'handbook_routes'):
            text_fields(route,['product_id','href','kind','target_id','source_path','source_sha256']);safe_name(route['href'])
            require((route['product_id'],route['href']) not in seen,'duplicate handbook route');seen.add((route['product_id'],route['href']))
            require(route['product_id'] in product_ids,'route product mismatch');b=next(b for b in books if b['product']['product_id']==route['product_id'])
            source_file=local(folder,route['source_path']);require(hashlib.sha256(source_file.read_bytes()).hexdigest()==route['source_sha256'],'route source hash mismatch')
            require(source_file==folder/'books'/route['product_id']/route['href'],'route path must stay in its product')
            if route['kind']=='recipe':require(route['target_id'] in {r['recipe_id'] for r in b['recipes']},'unresolved recipe route')
            else:require(route['kind']=='handbook' and route['target_id'] in {'guide-'+str(i) for i,_ in enumerate(b.get('handbooks',[]))},'unresolved handbook route')
            b.setdefault('handbook_routes',{})[route['href']]=dict(route)
    return dict(idx,books=books,tasks=tasks)

def differences(actual, expected, path='$'):
    """Bounded JSON-field diagnostics; never execute or echo submitted content."""
    if type(actual) is not type(expected): return [path+' (type)']
    if isinstance(expected,dict):
        result=[path+'.'+k+' (missing)' for k in expected.keys()-actual.keys()]
        result += [path+'.'+k+' (unexpected)' for k in actual.keys()-expected.keys()]
        for k in sorted(expected.keys() & actual.keys()): result.extend(differences(actual[k],expected[k],path+'.'+k))
        return sorted(result)[:12]
    if isinstance(expected,list):
        result=[] if len(actual)==len(expected) else [path+' (length)']
        for i,(a,e) in enumerate(zip(actual,expected)): result.extend(differences(a,e,path+'['+str(i)+']'))
        return result[:12]
    return [] if actual==expected else [path+' (value)']

def check(task_id, submission, root=ROOT):
    task=next((t for t in catalog(root)['tasks'] if t['task_id']==task_id),None)
    require(task is not None,'unknown task')
    require(submission.stat().st_size<=1000000,'submission too large')
    actual=load(submission)
    # bool/int must not compare equal; canonical JSON also makes object order irrelevant.
    encode=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
    require(encode(actual)==encode(task['expected_output']),'fixed author-reference contract mismatch: '+', '.join(differences(actual,task['expected_output'])))
    return {'task_id':task_id,'offline_contract':'passed','product_execution':'not_run','observed_results':None,'warning':'Only fixed synthetic JSON contract checked; no product was run and no quality ranking follows.'}

def publish(root,dest):
    # Validate the ENTIRE source inventory before any output or archive mutation.
    blobs=registered_bytes(root/'product-books');data=catalog(root)
    checker_bytes=local(root,'scripts/product_books.py').read_bytes()
    no_symlink_ancestors(dest);require(dest.is_dir(),'destination must exist')
    for name in ['product-markdown.js','product-books-data.json','product-bench-offline-r1.zip','product-books.html','product-books.css','product-books.js']:
        target=dest/name;no_symlink_ancestors(target)
        require(not target.exists() or target.is_file(),'nonregular publication destination')
    out=dest/'product-books';no_symlink_ancestors(out)
    if out.exists():
        inventory(out)  # Refuse symlink/nonregular output trees before removal.
        shutil.rmtree(out)
    out.mkdir()
    for name,content in sorted(blobs.items()):
        target=out/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
    (dest/'product-books-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    # Pin separate reader assets and data; never modify the old entrypoint pin contract.
    html=dest/'product-books.html'
    if html.exists():
        content=html.read_text()
        for filename in ['product-books.css','product-markdown.js','product-books.js']:
            digest=hashlib.sha256((dest/filename).read_bytes()).hexdigest()
            content=re.sub(re.escape(filename)+r'(?:\?v=[a-f0-9]+)?',filename+'?v='+digest,content)
        content=re.sub(r'\sdata-product-data-url="[^"]*"','',content)
        url='product-books-data.json?v='+hashlib.sha256((dest/'product-books-data.json').read_bytes()).hexdigest()
        content=content.replace('<html ', '<html data-product-data-url="'+url+'" ',1)
        html.write_text(content)
    # Reproducible archive: fixed timestamps, no dependency installation, no generated product answers.
    files={'product-books/'+name:content for name,content in blobs.items()}
    files['scripts/product_books.py']=checker_bytes
    with zipfile.ZipFile(dest/'product-bench-offline-r1.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,content in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,content)

def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('validate'); c=sub.add_parser('check');c.add_argument('task_id');c.add_argument('submission',type=Path)
    args=ap.parse_args()
    try:
        if args.cmd=='validate':
            d=catalog();print(json.dumps({'tasks':len(d['tasks']),'products':len(d['books']),'recipes':sum(len(b['recipes']) for b in d['books']),'product_execution':'not_run'}))
        else: print(json.dumps(check(args.task_id,args.submission),ensure_ascii=False))
    except (ValueError,KeyError,TypeError,OSError) as e: ap.exit(1,str(e)+'\n')
if __name__=='__main__': main()
