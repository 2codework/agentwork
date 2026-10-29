'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),test=require('node:test'),path=require('node:path');
const p=require('../web/task-first.js'),root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/task-first-data.json')));
class E{constructor(tag,text=''){this.tagName=tag.toUpperCase();this.children=[];this.attrs={};this.events={};this._text=text;this.open=false;}append(...nodes){for(const n of nodes){this.children.push(n);n.parentElement=this;}}set textContent(t){this._text=String(t);this.children=[];}get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}replaceChildren(...n){this.children=[];this._text='';this.append(...n);}addEventListener(k,v){this.events[k]=v;}focus(){this.focused=true;}}
function all(n){return [n,...n.children.flatMap(all)];}
async function boot(search='',narrow=false,pathname='/agentwork/index.html',hash='',fixture=data){const ids={screen:new E('div'),status:new E('p'),main:new E('main')},events={},copied=[],requests=[],location={search,pathname,hash,replace:url=>location.replaced=url},doc={createElement:t=>new E(t),createTextNode:t=>new E('#text',t),createDocumentFragment:()=>new E('fragment'),getElementById:id=>ids[id],querySelectorAll:()=>[],documentElement:new E('html'),title:''};const ctx={document:doc,location,URL,URLSearchParams,matchMedia:()=>({matches:!narrow,addEventListener(){}}),window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},history:{pushState:(a,b,url)=>{location.search=url.includes('?')?'?'+url.split('?')[1]:'';},replaceState(){}},fetch:async url=>{requests.push(url);return {ok:true,json:async()=>structuredClone(fixture)};},navigator:{clipboard:{writeText:async t=>copied.push(t)}}};for(const file of ['reader.js','task-first.js'])vm.runInNewContext(fs.readFileSync(path.join(root,'web',file),'utf8'),ctx);await new Promise(r=>setImmediate(r));return {ids,events,copied,requests,location,doc,plain:t=>ctx.markdownDOM(t,doc).textContent};}


const videoTask=()=>{const w=data.workflows.find(w=>w.id==='video-fact-preserving-cut');assert.ok(w,'admitted video task');return w;};
const section=b=>all(b.ids.screen).find(n=>n.attrs['data-step']);
const click=n=>{assert.ok(n,'navigation target');n.events.click({preventDefault(){}});};
const href=n=>n.attrs.href||n.href||'';
const src=n=>n.attrs.src||n.src||'';
const STEPS=['prepare','tool','setup','prompt','example','check'];

test('video, rough cut and fact preservation find the eleventh actual task',async()=>{
 const w=videoTask();assert.equal(data.workflows.length,11);assert.equal(w.video_workflow,true);
 for(const q of ['视频','粗剪','保留事实',w.title]){
  const b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(w.category));
  assert.equal(b.ids.status.textContent,'');assert.ok(all(b.ids.screen).some(n=>n.attrs['data-workflow-id']===w.id),q);
 }
});

test('video six stages preserve source order and original query through repeated returns and history',async()=>{
 const w=videoTask(),q='  粗 剪  ',category=w.category,b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(category),true);
 const enter=()=>click(all(all(b.ids.screen).find(n=>n.attrs['data-workflow-id']===w.id)).find(n=>n.tagName==='A'));enter();
 for(let round=0;round<2;round++){
  for(const [i,key]of STEPS.entries()){
   const state=p.readRoute(b.location.search);assert.equal(state.work,w.id);assert.equal(state.step,key);assert.equal(state.q,q);assert.equal(state.category,category);
   const s=section(b);assert.equal(s.attrs['data-step'],key);assert.equal(all(b.ids.screen).filter(n=>n.attrs['data-step']).length,1);
   assert.ok(all(s).some(n=>n.tagName==='H2'&&n.textContent===w.sections[key].title));assert.equal(w.sections[key].source_step,i+1);
   assert.equal(all(b.ids.screen).filter(n=>n.attrs['aria-current']==='step').length,1);assert.equal(all(b.ids.screen).find(n=>n.attrs.class==='step-menu').open,false);
   if(key!=='check')click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent.startsWith('下一步')));
  }
  const last=b.location.search;b.location.search=p.taskLink(w.id,{q,category},'setup').split('index.html')[1];b.events.popstate();assert.equal(section(b).attrs['data-step'],'setup');
  b.location.search=last;b.events.popstate();click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='再选一件工作'));
  assert.equal(p.readRoute(b.location.search).q,q);assert.equal(p.readRoute(b.location.search).category,category);if(round===0)enter();
 }
});

test('only preparation previews the fixed synthetic input without autoplay or external media',async()=>{
 const w=videoTask(),b=await boot('?work='+w.id+'&step=prepare'),s=section(b),ns=all(s),v=ns.filter(n=>n.tagName==='VIDEO');
 assert.equal(v.length,1);assert.ok('controls' in v[0].attrs);assert.equal(v[0].attrs.preload,'none');assert.ok(!('autoplay' in v[0].attrs));assert.ok(!('loop' in v[0].attrs));
 const media=all(v[0]).filter(n=>n.tagName==='SOURCE');assert.equal(media.length,1);assert.equal(src(media[0]),w.asset_base+'assets/paper-plane-synthetic-input-90s.mp4');assert.equal(media[0].attrs.type,'video/mp4');
 const tracks=all(v[0]).filter(n=>n.tagName==='TRACK');assert.equal(tracks.length,1);assert.equal(tracks[0].attrs.kind,'captions');assert.equal(tracks[0].attrs.srclang,'en');assert.equal(tracks[0].attrs.label.replace(/\s/g,''),'合成片段字幕（非ASR）');assert.equal(src(tracks[0]),w.asset_base+'assets/captions.en.vtt');
 const before=ns.slice(0,ns.indexOf(v[0])).filter(n=>n.children.length===0).map(n=>n.textContent).join(' ');assert.match(before,/合成/);assert.match(before,/听觉.*(尚未|未|pending)|尚未.*听|未.*听评/);assert.match(before,/非.?ASR|不是.?ASR/);
 for(const file of ['assets/paper-plane-synthetic-input-90s.mp4','assets/captions.en.srt','assets/script.en.txt','assets/facts.json']){assert.ok(ns.some(n=>n.tagName==='A'&&href(n)===w.asset_base+file),file);assert.ok(fs.existsSync(path.join(root,'site',w.asset_base+file)));}
 assert.equal(b.requests.length,1);assert.ok(!String(b.requests[0]).startsWith('http'));assert.equal(ns.filter(n=>['INPUT','FORM','IFRAME'].includes(n.tagName)).length,0);
 for(const key of STEPS.slice(1)){const other=await boot('?work='+w.id+'&step='+key);assert.equal(all(section(other)).filter(n=>n.tagName==='VIDEO').length,0);}
});

test('source prompt is copied exactly at stage three and no false completed video appears',async()=>{
 const w=videoTask(),b=await boot('?work='+w.id+'&step=setup'),s=section(b),source=fs.readFileSync(path.join(root,'learning/task-first/r1/video/GUIDE.zh-CN.md'),'utf8');
 const original=source.match(/```text\n([\s\S]*?)```/)[1];assert.equal(w.prompt,original);assert.ok(s.textContent.includes(original));
 const button=all(s).find(n=>n.tagName==='BUTTON'&&n.textContent.includes('复制'));assert.ok(button);await button.events.click();assert.equal(b.copied.at(-1),original);
 assert.ok(s.textContent.indexOf(b.plain(w.sections.setup.body))<s.textContent.indexOf(original));assert.ok(s.textContent.indexOf(b.plain(w.sections.setup.after))>s.textContent.indexOf(original));
 assert.match(original,/Do not discard/);assert.match(original,/your report is not proof/);
 for(const key of STEPS){const page=await boot('?work='+w.id+'&step='+key);const text=page.ids.screen.textContent;assert.doesNotMatch(text,/这是作者写好的核对样例|作者完整参考（未在产品运行）|候选 A|候选 B|确认已附加示例文件/);assert.equal(all(page.ids.screen).filter(n=>n.tagName==='BUTTON'&&!n.textContent.startsWith('复制')).length,0);}
});

test('real verification stage exposes the complete blank checklist and only input media downloads',async()=>{
 const w=videoTask(),b=await boot('?work='+w.id+'&step=prompt'),s=section(b),blank=fs.readFileSync(path.join(root,'learning/task-first/r1/video/CHECKLIST.zh-CN.md'),'utf8');
 assert.ok(s.textContent.includes(blank));assert.match(blank,/未执行/);assert.match(blank,/不能复用输入时间码/);
 const button=all(s).find(n=>n.tagName==='BUTTON'&&n.textContent.includes('复制'));assert.ok(button);await button.events.click();assert.equal(b.copied.at(-1),blank);
 assert.ok(all(s).some(n=>n.tagName==='A'&&href(n)===w.asset_base+'CHECKLIST.zh-CN.md'&&'download' in n.attrs));
 const full=await boot('?work='+w.id+'&all=1');for(const a of all(full.ids.screen).filter(n=>n.tagName==='A'&&/\.mp4(?:$|\?)/i.test(href(n))))assert.equal(href(a),w.asset_base+'assets/paper-plane-synthetic-input-90s.mp4');
 assert.match(full.ids.screen.textContent,/45秒.*未生成|45 秒.*未生成|45秒输出未生成/);
 assert.match(full.ids.screen.textContent,/Revert/);assert.match(full.ids.screen.textContent,/Version history/);assert.match(full.ids.screen.textContent,/Current composition/);
});

test('video content markup is inert and malformed media identity cannot create an external source',async()=>{
 const w=videoTask(),fixture=structuredClone(data),copy=fixture.workflows.find(x=>x.id===w.id),attack='<img src=x onerror=alert(1)><script>alert(1)</script>';
 copy.sections.prompt.body+='\n'+attack+'\n[bad](javascript:alert(1))';const b=await boot('?work='+w.id+'&step=prompt',false,'/agentwork/index.html','',fixture),s=section(b);
 assert.ok(s.textContent.includes(attack));assert.equal(all(s).filter(n=>['IMG','SCRIPT','IFRAME','INPUT','FORM'].includes(n.tagName)).length,0);assert.ok(!all(s).some(n=>href(n).startsWith('javascript:')));
 for(const bad of ['https://evil.example/input.mp4','//evil.example/input.mp4','../input.mp4','assets/unknown.mp4','javascript:alert(1)']){
  const mutated=structuredClone(data),v=mutated.workflows.find(x=>x.id===w.id);v.media.path=bad;
  const page=await boot('?work='+w.id+'&step=prepare',false,'/agentwork/index.html','',mutated);
  assert.ok(!all(page.ids.screen).some(n=>['VIDEO','SOURCE'].includes(n.tagName)&&src(n)===bad));
  assert.equal(all(page.ids.screen).filter(n=>['VIDEO','SOURCE'].includes(n.tagName)).length,0,'unregistered input must not play');
 }
 for(const field of ['captions_path','asset_base']){const mutated=structuredClone(data),v=mutated.workflows.find(x=>x.id===w.id);if(field==='asset_base')v.asset_base='https://evil.example/';else v.media.captions_path='https://evil.example/captions.vtt';const page=await boot('?work='+w.id+'&step=prepare',false,'/agentwork/index.html','',mutated);assert.equal(all(page.ids.screen).filter(n=>['VIDEO','SOURCE','TRACK'].includes(n.tagName)).length,0,'unregistered media identity must not load');}
});
