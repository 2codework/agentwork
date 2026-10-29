"""Task-first beginner reading layer. No product execution or external calls."""
import hashlib,json,re,shutil,sys
import office_expansion,music_task,video_task,study_task
from pathlib import Path
from urllib.parse import urlsplit
from product_books import inventory,local,load,require,registered_bytes,no_symlink_ancestors,safe_name
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES={'meeting-actions':'文档与会议','weekly-report':'文档与会议','clean-orders':'表格与数据','six-slide-outline':'内容创作','competitor-research':'客户与销售','fix-small-bug':'代码与产品','customer-reply':'客户与销售','three-day-content':'内容创作','design-handoff':'代码与产品'}
PRODUCT_IDS={'腾讯 WorkBuddy':'tencent-workbuddy','WPS 灵犀专业版':'wps-lingxi-pro','OpenAI Codex CLI（已有终端工具）':'openai-codex'}
def text(obj,key):
    require(isinstance(obj,dict) and isinstance(obj.get(key),str) and obj[key].strip(),'missing readable field: '+key)
def texts(obj,key,nonempty=True):
    value=obj.get(key);require(isinstance(value,list) and (value or not nonempty),'missing readable list: '+key)
    require(all(isinstance(v,str) and v.strip() for v in value),'invalid readable list: '+key)
def sources_registry(items):
    require(isinstance(items,list) and items,'missing sources');out={}
    for s in items:
        for k in ['id','title','url']:text(s,k)
        u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'unsafe source link')
        require(s['id'] not in out,'duplicate source ID');out[s['id']]=s
    return out
def resolve(ids,registry):
    require(isinstance(ids,list) and ids and all(isinstance(x,str) and x in registry for x in ids),'unresolved source')
    return [registry[x] for x in ids]
def preflight_destination(root,dest):
    """Quiescent-checkout preflight, not protection against concurrent races."""
    no_symlink_ancestors(dest)
    registry=load(local(root,'publication-destinations.json'))
    require(registry.get('schema_version')==1,'publication destination schema')
    names=registry['directories']['docs' if dest.name=='docs' else 'site']
    require(isinstance(names,list) and len(names)==len(set(names)),'destination registry entries')
    for name in names:safe_name(name)
    allowed=set(names);directories={str(p) for name in names for p in Path(name).parents if str(p)!='.'}
    if not dest.exists():return
    found=inventory(dest)
    require(set(found).issubset(allowed),'unregistered publication destination')
    for path in dest.rglob('*'):
        if path.is_dir():require(path.relative_to(dest).as_posix() in directories,'unregistered publication directory')
def preflight_page_assets(page,assets):
    """Validate known publisher page inputs before writes; not a build transaction."""
    for tag in re.findall(r'<script\b[^>]*>|<link\b(?=[^>]*\brel="stylesheet")[^>]*>',page.read_text(),re.I):
        attr='src' if tag.lower().startswith('<script') else 'href'
        match=re.search(r'\b'+attr+r'="([^"]+)"',tag)
        require(match is not None,'missing asset path')
        url=urlsplit(match.group(1));require(not url.scheme and not url.netloc,'remote asset')
        local(assets,url.path)

def preflight_build(root):
    # Known task-publisher inputs and both output inventories are checked before writes.
    source=registered_bytes(root/'learning/task-first/r1')
    if load(local(root/'learning/task-first/r1','index.json')).get('office_expansion_pack'):
        require(load(local(root/'learning/task-first/r1','index.json'))['office_expansion_pack']=='office-expansion/proposed-workflows.json','unknown office expansion pack')
        office_expansion.catalog(root)
    require(load(local(root/'learning/task-first/r1','index.json')).get('music_pack')=='music/workflow.json','unknown music pack')
    music_task.catalog(root)
    require(load(local(root/'learning/task-first/r1','index.json')).get('video_pack')=='video/workflow.json','unknown video pack')
    video_task.catalog(root)
    require(load(local(root/'learning/task-first/r1','index.json')).get('study_pack')=='study/workflow.json','unknown study pack')
    study_task.catalog(root)
    webfiles=inventory(root/'web')
    registered=set(load(local(root,'publication-destinations.json'))['directories']['site'])
    require(set(webfiles).issubset(registered),'unregistered planned web output')
    require({'task-guides/'+name for name in source}.issubset(registered),'unregistered planned task output')
    for filename in ['index.html','product-books.html','library.html','product-library.html']:
        preflight_page_assets(local(root/'web',filename),root/'web')
    for folder in ['site','docs']:preflight_destination(root,root/folder)
    no_symlink_ancestors(root/'BOOK.md')
    require(not (root/'BOOK.md').exists() or (root/'BOOK.md').is_file(),'nonregular BOOK destination')

def catalog(root=ROOT):
    folder=root/'learning/task-first/r1'
    registered_bytes(folder);idx=load(local(folder,'index.json'))
    require(idx.get('schema_version')=='task-first/1.0','task-first schema')
    require(idx.get('status') in ['assembling','ready'],'task-first admission status')
    phase_doc=load(local(folder,'phase-presentation.json'));phases=phase_doc['workflows']
    path=local(folder,idx['workflow_pack']);raw=load(path);registry=sources_registry(raw['sources']);workflows=[]
    admitted=idx['admitted_workflow_ids'];require(isinstance(admitted,list) and len(admitted)==len(set(admitted)),'admission IDs')
    require(set(admitted).issubset({r['id'] for r in raw['recipes']}),'unknown admitted workflow')
    for original in raw['recipes']:
        if original['id'] not in admitted:continue
        w=dict(original)
        phase=phases.get(w['id']);require(isinstance(phase,dict),'missing reading phases')
        digest=hashlib.sha256(json.dumps(original,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(phase.get('source_record_sha256')==digest,'stale reading-phase source binding')
        for field in ['first_time','setup_steps','prompt_steps','result_steps']:texts(phase,field)
        w['reading_phases']=phase
        for k in ['id','title','product','audience','outcome','access_cost','prompt','sample_output','sample_note','privacy']:text(w,k)
        for k in ['prerequisites','first_time','steps','checks','recovery']:texts(w,k)
        require(w['id'] in CATEGORIES,'unknown task category');require(w['product'] in PRODUCT_IDS,'unknown documented product')
        require(isinstance(w.get('tools'),dict),'missing tool guidance')
        for k in ['tools','mcp','skills']:text(w['tools'],k)
        require(isinstance(w['input_files'],list) and w['input_files'],'missing complete sample input')
        for a in w['input_files']:
            for k in ['name','path','content','sha256']:text(a,k)
            require(a.get('synthetic') is True,'only synthetic starter input allowed')
            p=local(path.parent,a['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],'starter input hash mismatch')
            require(p.read_text()==a['content'],'starter input text mismatch')
        if w.get('download_bundle'):local(path.parent,w['download_bundle'])
        require(isinstance(w.get('connection_guide_ids'),list),'missing explicit connection requirement')
        w['category']=CATEGORIES[w['id']];w['product_id']=PRODUCT_IDS[w['product']]
        w['material_label']='代码与测试文件' if w['id']=='fix-small-bug' else '订单表格' if w['id']=='clean-orders' else '一份文字材料'
        w['asset_base']='task-guides/'+str(path.parent.relative_to(folder))+'/'
        w['source_artifact']='task-guides/'+idx['workflow_pack'];w['source_details']=resolve(w['sources'],registry)
        workflows.append(w)
    if 'office_expansion_pack' in idx:
        require(idx['office_expansion_pack']=='office-expansion/proposed-workflows.json','unknown office expansion pack')
        workflows.extend(office_expansion.catalog(root))
    require(idx.get('music_pack')=='music/workflow.json','unknown music pack')
    workflows.append(music_task.catalog(root))
    require(idx.get('video_pack')=='video/workflow.json','unknown video pack')
    workflows.append(video_task.catalog(root))
    require(idx.get('study_pack')=='study/workflow.json','unknown study pack')
    workflows.append(study_task.catalog(root))
    cp=local(folder,idx['connection_pack']);connection=load(cp);cs=sources_registry(connection['sources']);guides=[];seen=set()
    for original in connection['routes']:
        g=dict(original)
        for k in ['id','title','audience','outcome','product','accounts_cost','minimum_access','start_url','start_label','prompt','test_input','reference_output','disconnect']:text(g,k)
        require(g['id'] not in seen,'duplicate connection route');seen.add(g['id'])
        u=urlsplit(g['start_url']);require(u.scheme=='https' and u.hostname and not u.username and not u.password,'unsafe official entry')
        for k in ['onboarding_steps','steps','expected_observations','platform_notes']:texts(g,k)
        require(isinstance(g.get('recovery'),list) and g['recovery'],'missing setup recovery')
        for failure in g['recovery']:
            text(failure,'symptom');text(failure,'action')
        require(g.get('config') is None or isinstance(g['config'],str),'config must stay complete text')
        for k in ['commands','onboarding_commands','creator_prompt','file_prompt','followup_prompt','file_correction_prompt','windows_disable_config','disable_path_note']:
            if k in g:text(g,k)
        g['source_details']=resolve(g['source_ids'],cs);g['source_artifact']='task-guides/'+idx['connection_pack'];guides.append(g)
    for w in workflows:require(set(w['connection_guide_ids']).issubset(seen),'unresolved workflow connection')
    for card in connection['chooser']['cards']:require(card['route_id'] is None or card['route_id'] in seen,'unresolved chooser route')
    legacy=load(root/'site/data.json')
    require(len(legacy['cases'])==138,'legacy case count changed')
    return {'schema_version':'task-first/1.0','status':idx['status'],'workflows':workflows,'guides':guides,'chooser':connection['chooser'],'categories':list(dict.fromkeys(w['category'] for w in workflows)),'legacy_case_ids':[c['id'] for c in legacy['cases']],'source_scope':{'workflow_pack':idx['workflow_pack'],'connection_pack':idx['connection_pack'],'office_expansion_pack':idx.get('office_expansion_pack'),'verification':'documentation_and_author_examples_not_product_execution'}}
def pin_page(dest,filename,attribute,datafile):
    page=dest/filename;html=page.read_text()
    def tag(match):
        value=match.group(0);attr='src' if value.lower().startswith('<script') else 'href'
        def replace(m):
            url=urlsplit(m.group(1));require(not url.scheme and not url.netloc and not url.path.startswith('/'),'remote asset')
            path=local(dest,url.path);return attr+'="'+url.path+'?v='+hashlib.sha256(path.read_bytes()).hexdigest()+'"'
        return re.sub(r'\b'+attr+r'="([^"]+)"',replace,value)
    html=re.sub(r'<script\b[^>]*>|<link\b(?=[^>]*\brel="stylesheet")[^>]*>',tag,html,flags=re.I)
    html=re.sub(r'\s'+attribute+r'="[^"]*"','',html)
    html=html.replace('<html ','<html '+attribute+'="'+datafile+'?v='+hashlib.sha256((dest/datafile).read_bytes()).hexdigest()+'" ',1)
    page.write_text(html)
def publish(root,dest):
    folder=root/'learning/task-first/r1';blobs=registered_bytes(folder);data=catalog(root)
    preflight_destination(root,dest)
    registered=set(load(local(root,'publication-destinations.json'))['directories']['docs' if dest.name=='docs' else 'site'])
    require({'task-guides/'+name for name in blobs}.issubset(registered),'unregistered planned task output')
    inventory(root/'web')
    require(dest.is_dir(),'publication destination must exist')
    for filename in ['index.html','product-books.html','library.html','product-library.html']:
        page=local(root/'web',filename) if filename in ['index.html','product-books.html'] else local(dest,filename)
        preflight_page_assets(page,dest)
    for filename in ['data.json','product-books-data.json']:local(dest,filename)
    out=dest/'task-guides'
    if out.exists():inventory(out);shutil.rmtree(out)
    out.mkdir()
    for name,content in blobs.items():
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
    (dest/'task-first-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    for filename in ['index.html','product-books.html']:
        shutil.copyfile(root/'web'/filename,dest/filename)
        pin_page(dest,filename,'data-task-data-url','task-first-data.json')
    pin_page(dest,'library.html','data-data-url','data.json')
    pin_page(dest,'product-library.html','data-product-data-url','product-books-data.json')
if __name__=='__main__':
    d=catalog();print(json.dumps({'workflows':len(d['workflows']),'connection_guides':len(d['guides']),'status':d['status'],'product_execution':'not_run'}))
