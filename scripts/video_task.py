"""Closed static video lesson projection. Never imports a product or media client."""
import hashlib,json,re
from urllib.parse import urlsplit
from product_books import require,load,local,inventory
MANIFEST='61b51ae723e13432fff35a9e00bed185cbd91d239869db7dcbd0829a086432b6'
PROJECTION_PIN='2e6088843ad6abd1b9503d823531bdc7a5faa7bb79917abaf1b538f0f8338b77'
MEDIA='assets/paper-plane-synthetic-input-90s.mp4'
MEDIA_SHA='b1cc953778cff1667dffa48639ada5e91edbd4d299f1602c5cd9657f73355a2b'
MEDIA_BYTES=2089879
PHASES=['prepare','tool','setup','prompt','example','check']
def digest(data):return hashlib.sha256(data).hexdigest()
def text(value):require(isinstance(value,str) and bool(value.strip()),'video readable text required')
def srt_to_vtt(value):
 # Preserve cue order, IDs, text and milliseconds; change only container header and timestamp separator.
 require('\r' not in value,'expected admitted LF SRT')
 blocks=value.strip().split('\n\n');last=0
 for i,b in enumerate(blocks,1):
  lines=b.splitlines();require(len(lines)>=3 and lines[0]==str(i),'video subtitle sequence')
  match=re.fullmatch(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})',lines[1]);require(match is not None,'video subtitle timing syntax')
  v=list(map(int,match.groups()));start=((v[0]*60+v[1])*60+v[2])*1000+v[3];end=((v[4]*60+v[5])*60+v[6])*1000+v[7]
  require(last<=start<end<=90000,'video subtitle time range/order');last=end
  require(not any('<' in line or '-->' in line for line in lines[2:]),'video subtitle text must be plain')
 return 'WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2',value)
def catalog(root):
 folder=root/'learning/task-first/r1/video';files=inventory(folder);projection=load(local(folder,'projection.json'))
 require(digest(local(folder,'projection.json').read_bytes())==PROJECTION_PIN,'video admitted projection pin')
 require(projection['source_manifest_sha256']==MANIFEST,'video source manifest binding')
 pins=projection['public_file_sha256'];require(set(files)==set(pins)|{'projection.json'},'video closed publication inventory')
 for name,sha in pins.items():require(digest(local(folder,name).read_bytes())==sha,'video public bytes changed: '+name)
 media=local(folder,MEDIA);require(media.stat().st_size==MEDIA_BYTES and digest(media.read_bytes())==MEDIA_SHA,'video media fixed size/hash')
 srt=local(folder,'assets/captions.en.srt').read_text();require(local(folder,'assets/captions.en.vtt').read_text()==srt_to_vtt(srt),'video caption derivation drift')
 guide=local(folder,'GUIDE.zh-CN.md').read_text();prompts=re.findall(r'```text\n(.*?)```',guide,re.S);require(len(prompts)==1,'video unique source prompt')
 prompt=local(folder,'prompt.txt').read_text();require(prompt==prompts[0],'video exact source prompt')
 w=load(local(folder,'workflow.json'));require(w['schema']=='video-workflow/1' and w['id']=='video-fact-preserving-cut','video workflow identity')
 require(w['product_execution']=='not_run' and w['output_generated'] is False and w['listening_test']=='pending','video execution scope')
 require(list(w['sections'])==PHASES,'video six ordered phases');require([w['sections'][k]['source_step'] for k in PHASES]==list(range(1,7)),'video source phase binding')
 for k in ['title','outcome','audience','product','product_id','category','material_label','access_cost','privacy']:text(w[k])
 ledger=load(local(folder,'source-ledger.json'));registry={}
 for s in ledger['sources']:
  text(s['id']);text(s['url']);text(s['title']);u=urlsplit(s['url'])
  require(u.scheme=='https' and u.hostname in {'help.descript.com','www.descript.com','web.descript.com','github.com','raw.githubusercontent.com'} and not u.username and not u.password,'unsafe video official source')
  require(s['id'] not in registry,'duplicate video source');registry[s['id']]=s
 for obj in [w,*w['sections'].values()]:require(obj['source_ids'] and set(obj['source_ids']).issubset(registry),'unresolved video source')
 for phase in w['sections'].values():text(phase['title']);text(phase['body'])
 require(w['sections']['setup']['prompt_asset']=='prompt.txt','video prompt phase asset')
 n=dict(w);n.update(video_workflow=True,asset_base='task-guides/video/',media={'path':MEDIA,'captions_path':'assets/captions.en.vtt','sha256':MEDIA_SHA,'bytes':MEDIA_BYTES},prompt=prompt,checklist=local(folder,'CHECKLIST.zh-CN.md').read_text(),input_files=[],connection_guide_ids=[],source_artifact='task-guides/video/GUIDE.zh-CN.md',source_details=[dict(registry[k],checked_on='2026-10-29') for k in w['source_ids']],sample_note='只有 90 秒原创合成输入与空白验收表。输入主观听觉尚未验收；Descript 未执行，45 秒成片未生成，字幕不是 ASR 结果。',delivery_preview='下载 90 秒英文合成输入，自己检查后再决定导入 Descript。约 45 秒只是粗剪目标；本站没有剪后参考成片或预填成绩。')
 return n
