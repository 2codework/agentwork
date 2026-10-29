"""Closed authored-poster lesson; no image generation or product execution."""
import hashlib,re,struct,xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from product_books import require,load,local,inventory
MANIFEST='b2e56232156db69074dffbc026e90d71a0af67fd141634e354fa13859bc95e83'
FIXTURE='64597d30a4a8ae68a687fa6803478bf7b931cf8d3295d3b3597345ae8255dfe4'
PROJECTION_PIN='1a85f40891a55af64bfc29069322775caa132c1f1ab26361d5b9caf9c52a4d6d'
PHASES=['prepare','tool','setup','prompt','example','check']
PNG={'assets/before.png':(139124,'b2c4a5a238ac1e7c61cbc5cdcf26ed7b70719171584ccc2b490fecfc284a8cdc'),'assets/after-authored.png':(138232,'67a80a77f74d1d9ce0bc30661cdc616ba687a74df5352d74f7595174d47d4514')}
def digest(v):return hashlib.sha256(v).hexdigest()
def text(v):require(isinstance(v,str) and bool(v.strip()),'poster readable text required')
def png_dimensions(data):
 require(data[:8]==b'\x89PNG\r\n\x1a\n' and data[12:16]==b'IHDR' and len(data)>=24,'poster PNG signature/IHDR')
 return struct.unpack('>II',data[16:24])
def safe_svg(body):
 require(not re.search(r'<!DOCTYPE|<!ENTITY|<\?',body,re.I),'poster SVG declarations forbidden')
 tree=ET.fromstring(body);require(tree.tag=='{http://www.w3.org/2000/svg}svg','poster SVG root')
 allowed={'svg','title','desc','style','rect','circle','text','line','g','path'}
 for node in tree.iter():
  require(node.tag.startswith('{http://www.w3.org/2000/svg}') and node.tag.split('}')[-1] in allowed,'poster SVG element not allowed')
  for key,value in node.attrib.items():
   require(not key.lower().startswith('on') and 'href' not in key.lower(),'poster SVG active attribute')
   require(not re.search(r'url\s*\(|javascript:|data:|https?://',value,re.I),'poster SVG external/active value')
  if node.tag.endswith('}style'):require(not re.search(r'url\s*\(|@import|expression|javascript:',node.text or '',re.I),'poster SVG CSS external/active content')
 require(tree.get('width')=='1080' and tree.get('height')=='1440' and tree.get('viewBox')=='0 0 1080 1440','poster SVG fixed canvas')
 return tree

def catalog(root):
 folder=root/'learning/task-first/r1/poster';files=inventory(folder);projection=load(local(folder,'projection.json'))
 require(digest(local(folder,'projection.json').read_bytes())==PROJECTION_PIN,'poster projection admission pin')
 require(projection['source_manifest_sha256']==MANIFEST and projection['fixture_manifest_sha256']==FIXTURE,'poster source/fixture binding')
 pins=projection['public_file_sha256'];require(set(files)==set(pins)|{'projection.json'},'poster closed asset inventory')
 for name,sha in pins.items():require(digest(local(folder,name).read_bytes())==sha,'poster source byte drift: '+name)
 for name,(size,sha) in PNG.items():
  b=local(folder,name).read_bytes();require(len(b)==size and digest(b)==sha and png_dimensions(b)==(1080,1440),'poster fixed PNG dimensions/bytes/hash')
 for name in ['assets/before.svg','assets/after-authored.svg']:safe_svg(local(folder,name).read_text())
 guide=local(folder,'GUIDE.zh-CN.md').read_text();prompts=re.findall(r'```text\n(.*?)```',guide,re.S);require(len(prompts)==2,'poster two original prompts')
 prompt=local(folder,'prompt.txt').read_text();correction=local(folder,'correction-prompt.txt').read_text();require([prompt,correction]==prompts,'poster exact prompt extraction')
 w=load(local(folder,'workflow.json'));require(w['schema']=='poster-workflow/1' and w['id']=='poster-change-time' and w['interaction_mode']=='image-edit-original','poster typed input route')
 require(w['product_execution']=='not_run' and w['output_generated'] is False,'poster execution boundary')
 require(list(w['sections'])==PHASES and [w['sections'][k]['source_step'] for k in PHASES]==list(range(1,7)),'poster source six phase mapping')
 require(w['images']=={'input':'assets/before.png','authored_reference':'assets/after-authored.png','width':1080,'height':1440},'poster input/reference identity')
 for k in ['title','outcome','product','product_id','audience','category','material_label','access_cost','privacy']:text(w[k])
 registry={}
 for s in load(local(folder,'source-ledger.json'))['sources']:
  for k in ['id','title','url']:text(s[k])
  u=urlsplit(s['url']);require(u.scheme=='https' and u.hostname in {'help.openai.com','chatgpt.com'} and not u.username and not u.password,'unsafe poster official source')
  require(s['id'] not in registry,'duplicate poster source');registry[s['id']]=s
 for obj in [w,*w['sections'].values()]:require(obj['source_ids'] and set(obj['source_ids']).issubset(registry),'unresolved poster source')
 for phase in w['sections'].values():text(phase['title']);text(phase['body'])
 require(w['sections']['setup']['prompt_asset']=='prompt.txt' and w['sections']['example']['correction_asset']=='correction-prompt.txt','poster prompt stage binding')
 n=dict(w);n.update(poster_workflow=True,asset_base='task-guides/poster/',images={'before':w['images']['input'],'reference':w['images']['authored_reference']},prompt=prompt,correction_prompt=correction,checklist=local(folder,'CHECKLIST.zh-CN.md').read_text(),input_files=[],connection_guide_ids=[],source_artifact='task-guides/poster/GUIDE.zh-CN.md',source_details=[dict(registry[k],checked_on='2026-10-29') for k in w['source_ids']],sample_note='原始输入和理想对照均由作者编写；ChatGPT 未实跑，没有真实模型输出或成功率。页脚仅说明输入来源，不否认后续使用 AI；按实际编辑另记来源。',delivery_preview='只允许把周六14:00改成周日15:00。作者理想对照不是AI输出；实际效果、尺寸、颜色与区外像素须由你核验，未满足就保留未完成。')
 return n
