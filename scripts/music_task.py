"""Closed, source-bound music teaching projection. No audio generation or network."""
import hashlib,json
from urllib.parse import urlsplit
from product_books import require,load,local,inventory
MANIFEST='c4875405285ab7ef7d40f9f2a8e26f153085c77bbdb7893820c5bca51df9f47c'
PROJECTION_PIN='5accade6df21b2dc7c7d3f100646a377287fed31cfa502c09f053e763ca00b9e'
PHASES=['prepare','tool','setup','prompt','example','check']
ASSETS=['brief.txt','prompt-A-r1.txt','prompt-B-r1.txt','listening-record.csv','decision-template.txt','folder-example.txt']
def digest(data):return hashlib.sha256(data).hexdigest()
def text(value):require(isinstance(value,str) and bool(value.strip()),'music readable text required')
def catalog(root):
 folder=root/'learning/task-first/r1/music'
 projection=load(local(folder,'projection.json'));files=inventory(folder)
 require(digest(local(folder,'projection.json').read_bytes())==PROJECTION_PIN,'music projection admission hash mismatch')
 require(projection['source_manifest_sha256']==MANIFEST,'music source manifest binding')
 pins=projection['public_file_sha256']
 require(set(files)==set(pins)|{'projection.json'},'music closed projection inventory')
 for name,sha in pins.items():require(digest(local(folder,name).read_bytes())==sha,'music projection bytes changed')
 w=load(local(folder,'workflow.json'));ledger=load(local(folder,'source-ledger.json'))
 require(w['id']=='music-intro-ab' and w['schema']=='music-workflow/1','music workflow identity')
 require(w['product_execution']=='not_run' and w['audio_generated'] is False and w['listening_test']=='not_run','music execution boundary')
 require(list(w['sections'])==PHASES,'music six ordered phases')
 registry={}
 for s in ledger['sources']:
  text(s['id']);text(s['url']);u=urlsplit(s['url'])
  require(u.scheme=='https' and u.hostname in {'support.google.com','blog.google','ai.google.dev','policies.google.com'} and not u.username and not u.password,'unsafe music source URL')
  require(s['id'] not in registry,'duplicate music source');registry[s['id']]=s
 for p in [w,*w['sections'].values()]:
  require(isinstance(p['source_ids'],list) and p['source_ids'] and set(p['source_ids']).issubset(registry),'unresolved music source')
 for k in ['title','outcome','audience','product','product_id','category','material_label','access_cost','privacy']:text(w[k])
 for phase in w['sections'].values():text(phase['title']);text(phase['body'])
 rounds=w['sections']['prompt']['rounds'];require([r['label'] for r in rounds]==['A','B'],'music prompt sequence')
 require([r['asset'] for r in rounds]==ASSETS[1:3],'music exact prompt assets')
 for r in rounds:text(r['before']);text(r['after'])
 assets=[]
 for name in ASSETS:
  body=local(folder,name).read_bytes();assets.append({'name':name,'path':name,'content':body.decode(),'sha256':digest(body)})
 n=dict(w);n.update(music_workflow=True,assets=assets,asset_base='task-guides/music/',source_artifact='task-guides/music/reader.md',connection_guide_ids=[],input_files=[],sample_note='本课提供操作说明与空白记录；未在产品运行、未生成音频、未做听评。请根据你实际得到的候选填写，不把模板当成绩。',delivery_preview='A / B 原始 MP3（由你实际生成后下载）、提示记录、空白听评表与选段说明。本站没有参考音频；约 1 分钟候选不是精确 20 秒成品。',source_details=[dict(registry[k],title=registry[k].get('title',registry[k]['id']),checked_on=ledger['read_date_utc']) for k in w['source_ids']])
 return n
