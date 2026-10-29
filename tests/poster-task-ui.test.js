'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),test=require('node:test'),path=require('node:path');
const p=require('../web/task-first.js'),root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/task-first-data.json')));
class E{constructor(tag,text=''){this.tagName=tag.toUpperCase();this.children=[];this.attrs={};this.events={};this._text=text;this.open=false;}append(...nodes){for(const n of nodes){this.children.push(n);n.parentElement=this;}}set textContent(t){this._text=String(t);this.children=[];}get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}replaceChildren(...n){this.children=[];this._text='';this.append(...n);}addEventListener(k,v){this.events[k]=v;}focus(){this.focused=true;}}
function all(n){return [n,...n.children.flatMap(all)];}
async function boot(search='',narrow=false,pathname='/agentwork/index.html',hash='',fixture=data){const ids={screen:new E('div'),status:new E('p'),main:new E('main')},events={},copied=[],requests=[],location={search,pathname,hash,replace:url=>location.replaced=url},doc={createElement:t=>new E(t),createTextNode:t=>new E('#text',t),createDocumentFragment:()=>new E('fragment'),getElementById:id=>ids[id],querySelectorAll:()=>[],documentElement:new E('html'),title:''};const ctx={document:doc,location,URL,URLSearchParams,matchMedia:()=>({matches:!narrow,addEventListener(){}}),window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},history:{pushState:(a,b,url)=>{location.search=url.includes('?')?'?'+url.split('?')[1]:'';},replaceState(){}},fetch:async url=>{requests.push(url);return {ok:true,json:async()=>structuredClone(fixture)};},navigator:{clipboard:{writeText:async t=>copied.push(t)}}};for(const file of ['reader.js','task-first.js'])vm.runInNewContext(fs.readFileSync(path.join(root,'web',file),'utf8'),ctx);await new Promise(r=>setImmediate(r));return {ids,events,copied,requests,location,doc,plain:t=>ctx.markdownDOM(t,doc).textContent};}


const posterTask=()=>{const w=data.workflows.find(w=>w.id==='poster-change-time');assert.ok(w,'admitted poster task');return w;};
const section=b=>all(b.ids.screen).find(n=>n.attrs['data-step']);
const click=n=>{assert.ok(n,'navigation target');n.events.click({preventDefault(){}});};
const href=n=>n.attrs.href||n.href||'';
const src=n=>n.attrs.src||n.src||'';
const STEPS=['prepare','tool','setup','prompt','example','check'];

test('poster, image editing and design discover the thirteenth concrete task',async()=>{
 const w=posterTask();assert.equal(data.workflows.length,13);assert.equal(w.poster_workflow,true);assert.equal(w.schema,'poster-workflow/1');assert.equal(w.interaction_mode,'image-edit-original');
 for(const q of ['海报','改图','设计',w.title]){const b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(w.category));assert.equal(b.ids.status.textContent,'');assert.ok(all(b.ids.screen).some(n=>n.attrs['data-workflow-id']===w.id),q);}
});

test('poster six local phases preserve source order, query and category through repeats and history',async()=>{
 const w=posterTask(),q='  海 报  ',category=w.category,b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(category),true);
 const enter=()=>click(all(all(b.ids.screen).find(n=>n.attrs['data-workflow-id']===w.id)).find(n=>n.tagName==='A'));enter();
 for(let round=0;round<2;round++){
  for(const [i,key]of STEPS.entries()){
   const state=p.readRoute(b.location.search);assert.equal(state.work,w.id);assert.equal(state.step,key);assert.equal(state.q,q);assert.equal(state.category,category);
   const s=section(b);assert.equal(s.attrs['data-step'],key);assert.equal(all(b.ids.screen).filter(n=>n.attrs['data-step']).length,1);assert.ok(all(s).some(n=>n.tagName==='H2'&&n.textContent===w.sections[key].title));assert.equal(w.sections[key].source_step,i+1);
   assert.equal(all(b.ids.screen).filter(n=>n.attrs['aria-current']==='step').length,1);assert.equal(all(b.ids.screen).find(n=>n.attrs.class==='step-menu').open,false);
   if(key!=='check')click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent.startsWith('下一步')));
  }
  const last=b.location.search;b.location.search=p.taskLink(w.id,{q,category},'setup').split('index.html')[1];b.events.popstate();assert.equal(section(b).attrs['data-step'],'setup');b.location.search=last;b.events.popstate();
  click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='再选一件工作'));assert.equal(p.readRoute(b.location.search).q,q);assert.equal(p.readRoute(b.location.search).category,category);if(round===0)enter();
 }
});

test('only registered authored images appear, with input and ideal reference distinguished accessibly',async()=>{
 const w=posterTask(),prepare=await boot('?work='+w.id+'&step=prepare'),s=section(prepare),images=all(s).filter(n=>n.tagName==='IMG');assert.equal(images.length,1);assert.equal(src(images[0]),w.asset_base+'assets/before.png');
 assert.match(s.textContent,/原始|原图|输入/);assert.match(prepare.ids.screen.textContent,/未跑|未执行|未实跑/);assert.match(s.textContent,/地区/);assert.match(s.textContent,/额度/);
 assert.ok(all(s).some(n=>n.tagName==='A'&&href(n)===w.asset_base+'assets/before.png'&&'download' in n.attrs));
 const check=await boot('?work='+w.id+'&step=prompt'),c=section(check),comparisons=all(c).filter(n=>n.tagName==='IMG');assert.deepEqual(comparisons.map(src).sort(),[w.asset_base+'assets/before.png',w.asset_base+'assets/after-authored.png'].sort());
 assert.match(c.textContent,/作者/);assert.match(c.textContent,/对照|目标/);assert.match(c.textContent,/不是.*(AI|产品|实跑)|非.*(AI|实跑)|不证明/);
 for(const img of [...images,...comparisons]){assert.ok((img.attrs.alt||'').length>=8);assert.equal(Number(img.attrs.width),1080);assert.equal(Number(img.attrs.height),1440);assert.ok(!src(img).startsWith('http'));assert.ok(fs.existsSync(path.join(root,'site',src(img))));}
 const full=await boot('?work='+w.id+'&all=1');for(const img of all(full.ids.screen).filter(n=>n.tagName==='IMG'))assert.ok([w.asset_base+'assets/before.png',w.asset_base+'assets/after-authored.png'].includes(src(img)));
 assert.equal(prepare.requests.length,1);assert.ok(!String(prepare.requests[0]).startsWith('http'));
 const css=fs.readFileSync(path.join(root,'web/task-first.css'),'utf8').split('/* Local authored poster input/reference;')[1];assert.ok(css);assert.match(css,/width:100%/);assert.match(css,/height:auto/);assert.match(css,/repeat\(2,minmax\(0,1fr\)\)/);assert.match(css,/@media\(max-width:680px\)/);assert.match(css,/grid-template-columns:minmax\(0,1fr\)/);assert.doesNotMatch(css,/@import|url\(/);
});

test('main and retry requests copy exact accepted text including original-input provenance boundary',async()=>{
 const w=posterTask(),source=fs.readFileSync(path.join(root,'learning/task-first/r1/poster/GUIDE.zh-CN.md'),'utf8'),prompts=[...source.matchAll(/```text\n([\s\S]*?)```/g)].map(m=>m[1]);assert.equal(prompts.length,2);assert.equal(w.prompt,prompts[0]);assert.equal(w.correction_prompt,prompts[1]);
 for(const [key,expected]of [['setup',prompts[0]],['example',prompts[1]]]){const b=await boot('?work='+w.id+'&step='+key),s=section(b);assert.ok(s.textContent.includes(expected));const buttons=all(s).filter(n=>n.tagName==='BUTTON');for(const button of buttons)await button.events.click();assert.ok(b.copied.includes(expected));}
 assert.match(prompts[0],/原始输入：作者编写的合成教学素材/);assert.match(prompts[0],/不代表本次编辑没有使用AI/);assert.match(prompts[0],/周六14:00/);assert.match(prompts[0],/周日15:00/);
 const upload=await boot('?work='+w.id+'&step=tool');assert.match(section(upload).textContent,/before\.png/);assert.match(section(upload).textContent,/不是锁定|不一定精确|不意味着其他像素/);
});

test('local-result logging remains blank and no platform upload or fabricated output is supplied',async()=>{
 const w=posterTask(),b=await boot('?work='+w.id+'&step=check'),s=section(b),blank=fs.readFileSync(path.join(root,'learning/task-first/r1/poster/CHECKLIST.zh-CN.md'),'utf8');assert.ok(s.textContent.includes(blank));assert.ok(all(s).some(n=>n.tagName==='A'&&href(n)===w.asset_base+'CHECKLIST.zh-CN.md'&&'download' in n.attrs));
 for(const key of STEPS){const page=await boot('?work='+w.id+'&step='+key),ns=all(section(page));assert.equal(ns.filter(n=>['INPUT','FORM','IFRAME','VIDEO','AUDIO','OBJECT','EMBED'].includes(n.tagName)).length,0);assert.equal(ns.filter(n=>n.tagName==='BUTTON'&&!n.textContent.startsWith('复制')).length,0);}
 const full=await boot('?work='+w.id+'&all=1'),text=full.ids.screen.textContent;assert.match(text,/未核验/);assert.match(text,/最多|最后一次|第二次/);assert.match(text,/停止/);assert.match(text,/SVG/);assert.match(text,/可编辑层|可编辑项目/);
 for(const a of all(full.ids.screen).filter(n=>n.tagName==='A'&&/\.png(?:$|\?)/i.test(href(n))))assert.ok([w.asset_base+'assets/before.png',w.asset_base+'assets/after-authored.png'].includes(href(a)));
});

test('poster branch rejects unknown input identity and content markup stays inert',async()=>{
 const w=posterTask(),fixture=structuredClone(data),copy=fixture.workflows.find(x=>x.id===w.id),attack='<img src=x onerror=alert(1)><script>alert(1)</script>';
 copy.sections.setup.body+='\n'+attack+'\n[bad](javascript:alert(1))';const b=await boot('?work='+w.id+'&step=setup',false,'/agentwork/index.html','',fixture),s=section(b);assert.ok(s.textContent.includes(attack));assert.equal(all(s).filter(n=>['IMG','SCRIPT','IFRAME','INPUT','FORM'].includes(n.tagName)).length,0);assert.ok(!all(s).some(n=>href(n).startsWith('javascript:')));
 for(const [field,value]of [['interaction_mode','upload-anything'],['schema','poster-workflow/unknown'],['asset_base','https://evil.example/']]){const bad=structuredClone(data),v=bad.workflows.find(x=>x.id===w.id);v[field]=value;const page=await boot('?work='+w.id+'&step=setup',false,'/agentwork/index.html','',bad);assert.equal(all(section(page)).filter(n=>['IMG','BUTTON','INPUT'].includes(n.tagName)).length,0);}
 for(const [field,value]of [['before','https://evil.example/before.png'],['reference','../after.png'],['before','assets/unknown.png']]){const bad=structuredClone(data),v=bad.workflows.find(x=>x.id===w.id);v.images[field]=value;for(const key of ['prepare','prompt','setup']){const page=await boot('?work='+w.id+'&step='+key,false,'/agentwork/index.html','',bad);assert.ok(!all(section(page)).some(n=>n.tagName==='IMG'&&src(n)===value));assert.equal(all(section(page)).filter(n=>['IMG','BUTTON','INPUT'].includes(n.tagName)).length,0);}}
});

test('each displayed poster image has one native keyboard-reachable original-size link with truthful role',async()=>{
 const w=posterTask(),allowed={'assets/before.png':'原始输入 before.png','assets/after-authored.png':'作者理想对照 after-authored.png（非产品输出）'};
 for(const step of ['prepare','prompt']){
  const b=await boot('?work='+w.id+'&step='+step),s=section(b),figs=all(s).filter(n=>n.attrs['data-poster-image']);
  assert.equal(figs.length,step==='prepare'?1:2);
  for(const fig of figs){
   const name=fig.attrs['data-poster-image'],links=all(fig).filter(n=>n.attrs['data-poster-fullsize']);
   assert.equal(links.length,1);const a=links[0];assert.equal(a.tagName,'A');assert.equal(a.textContent,'查看大图（新标签页）');
   assert.equal(href(a),'task-guides/poster/'+name);assert.equal(new URL(href(a),'https://2codework.github.io/agentwork/').origin,'https://2codework.github.io');
   assert.equal(a.attrs.target,'_blank');assert.equal(a.attrs.rel,'noopener noreferrer');assert.equal(a.attrs['aria-label'],allowed[name]+'：查看大图（新标签页）');
   assert.ok(!('download' in a.attrs));assert.ok(!('tabindex' in a.attrs));assert.equal(a.events.click,undefined);
   const img=all(fig).find(n=>n.tagName==='IMG');assert.ok(img.attrs.alt);assert.equal(src(img),href(a));assert.ok(all(fig).find(n=>n.tagName==='FIGCAPTION').textContent);
   assert.ok(fs.existsSync(path.join(root,'site',href(a))));
  }
  b.events.popstate();assert.equal(all(section(b)).filter(n=>n.attrs['data-poster-fullsize']).length,figs.length);
  assert.ok(all(s).some(n=>n.tagName==='A'&&'download' in n.attrs&&href(n).endsWith(step==='prepare'?'assets/before.png':'assets/after-authored.png')));
 }
});
test('unregistered and unsafe image paths never gain a full-size link',async()=>{
 const w=posterTask();
 for(const value of ['https://evil.example/image.png','//evil.example/x.png','javascript:alert(1)','../before.png','assets/before.png?redirect=x','assets/before.png#x','assets/unknown.png','__proto__']){
  const fixture=structuredClone(data),item=fixture.workflows.find(x=>x.id===w.id);item.images.before=value;
  for(const step of ['prepare','prompt']){const b=await boot('?work='+w.id+'&step='+step,false,'/agentwork/index.html','',fixture);assert.equal(all(section(b)).filter(n=>n.attrs['data-poster-fullsize']).length,0,value);}
 }
});
test('all other twelve tasks retain their complete six-phase DOM',async()=>{
 const crypto=require('node:crypto'),baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/poster-other-tasks-dom-baseline.json')));
 const shape=n=>({tag:n.tagName,text:n._text,attrs:n.attrs,open:n.open,children:n.children.map(shape)});
 assert.equal(Object.keys(baseline).length,72);
 for(const w of data.workflows.filter(w=>!w.poster_workflow))for(const step of STEPS){const b=await boot('?work='+w.id+'&step='+step);assert.equal(crypto.createHash('sha256').update(JSON.stringify(shape(b.ids.screen))).digest('hex'),baseline[w.id+'/'+step],w.id+'/'+step);}
});
