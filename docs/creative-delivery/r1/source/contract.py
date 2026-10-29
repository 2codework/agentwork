"""Original fixed teaching contract; no external resource or authorization lookup."""
import hashlib
import json
import re

TRACKS = ('shots', 'captions', 'music', 'graphics')
REVISION = 'paper-demo-r2'
ROWS = (
 ('shots','S1',0,8000,'纸圆进入'),
 ('shots','S2',8000,16000,'方块转动'),
 ('shots','S3',16000,24000,'两者停下'),
 ('captions','C1',1000,3000,'纸圆来了。'),
 ('captions','C2',9000,11000,'方块转身。'),
 ('captions','C3',13000,15000,'两者并排。'),
 ('captions','C4',21000,23000,'停在这里。'),
 ('music','M1',0,24000,'原创音乐文字占位，不代表实际音频'),
 ('graphics','G1',0,4000,'纸圆与方块'),
 ('graphics','G2',18000,22000,'练习结束'),
)
SOURCE = {
 'schema_version':'creative-cut-source/1', 'project_id':'paper-demo',
 'revision':'paper-demo-r1', 'duration_ms':24000,
 'assets':[dict(asset_id='asset-'+i.lower(),provenance_kind='synthetic_fixture',description=text) for _,i,_,_,text in ROWS],
 'tracks':[dict(track_id=t,items=[dict(item_id=i,asset_id='asset-'+i.lower(),start_ms=a,end_ms=b,source_start_ms=0,source_end_ms=b-a,text=text) for track,i,a,b,text in ROWS if track==t]) for t in TRACKS],
}
EDIT = dict(schema_version='creative-cut-edit/1',project_id='paper-demo',edit_id='cut-middle-4s',from_revision='paper-demo-r1',to_revision=REVISION,remove_start_ms=8000,remove_end_ms=12000,target_duration_ms=20000)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

# Embedded value constants are the trust root; these digests are pinned below at authoring.
SOURCE_SHA256 = '1b6ee82693865c669e3c22b434302f5fb8a9c4cc106a6bf4e8e6b5b0897d64f5'
EDIT_SHA256 = '055936e3b2a4db5a3df1807008432781d9514736e06c0b601bc19f660e7ff4ef'

class Invalid(ValueError):
    def __init__(self, code):
        self.code=code
        super().__init__(code)

def generic(value, depth=0):
    if isinstance(value,(dict,list)):
        depth+=1
        if depth>8: raise Invalid('SCHEMA_DEPTH')
        if len(value)>(16 if isinstance(value,dict) else 32): raise Invalid('SCHEMA_LIMIT')
        if isinstance(value,dict):
            for k,v in value.items(): generic(k,depth); generic(v,depth)
        else:
            for v in value: generic(v,depth)
    elif type(value) is str:
        if len(value)>256: raise Invalid('SCHEMA_LIMIT')
        if any(0xD800<=ord(c)<=0xDFFF for c in value): raise Invalid('SCHEMA_VALUE')

def obj(value, fields):
    if type(value) is not dict: raise Invalid('SCHEMA_TYPE')
    if set(value)!=set(fields): raise Invalid('SCHEMA_KEYS')
    for k,kind in fields.items():
        v=value[k]
        if kind=='int':
            if type(v) is not int: raise Invalid('SCHEMA_TYPE')
            if not 0<=v<=24000: raise Invalid('SCHEMA_VALUE')
        elif kind in ('id','sha','str') or kind.startswith('='):
            if type(v) is not str: raise Invalid('SCHEMA_TYPE')
            if kind=='id' and not re.fullmatch(r'[A-Za-z0-9_.-]{1,48}',v): raise Invalid('SCHEMA_VALUE')
            if kind=='sha' and not re.fullmatch(r'[0-9a-f]{64}',v): raise Invalid('SCHEMA_VALUE')
            if kind.startswith('=') and v!=kind[1:]: raise Invalid('SCHEMA_VALUE')
        elif type(v) is not {'array':list,'object':dict}[kind]: raise Invalid('SCHEMA_TYPE')

TIMES = dict(start_ms='int',end_ms='int',source_start_ms='int',source_end_ms='int')

def schema(value, kind):
    generic(value)
    if kind=='source':
        obj(value,dict(schema_version='=creative-cut-source/1',project_id='id',revision='id',duration_ms='int',assets='array',tracks='array'))
        for a in value['assets']: obj(a,dict(asset_id='id',provenance_kind='=synthetic_fixture',description='str'))
        for t in value['tracks']:
            obj(t,dict(track_id='id',items='array'))
            for i in t['items']: obj(i,dict(item_id='id',asset_id='id',text='str',**TIMES))
    elif kind=='edit':
        obj(value,dict(schema_version='=creative-cut-edit/1',project_id='id',edit_id='id',from_revision='id',to_revision='id',remove_start_ms='int',remove_end_ms='int',target_duration_ms='int'))
    else:
        obj(value,dict(schema_version='=creative-cut-submission/1',project_id='id',revision='id',edit_sha256='sha',tracks='array',delivery='object'))
        for t in value['tracks']:
            obj(t,dict(track_id='id',revision='id',fragments='array'))
            if len(t['fragments'])>16: raise Invalid('SCHEMA_LIMIT')
            for f in t['fragments']: obj(f,dict(fragment_id='id',original_id='id',asset_id='id',text='str',**TIMES))
        d=value['delivery']; obj(d,dict(revision='id',edit_sha256='sha',tracks='array'))
        for t in d['tracks']: obj(t,dict(track_id='id',sha256='sha'))
