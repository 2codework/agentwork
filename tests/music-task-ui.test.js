'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),test=require('node:test'),path=require('node:path');
const p=require('../web/task-first.js'),root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/task-first-data.json')));
class E{constructor(tag,text=''){this.tagName=tag.toUpperCase();this.children=[];this.attrs={};this.events={};this._text=text;this.open=false;}append(...nodes){for(const n of nodes){this.children.push(n);n.parentElement=this;}}set textContent(t){this._text=String(t);this.children=[];}get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}replaceChildren(...n){this.children=[];this._text='';this.append(...n);}addEventListener(k,v){this.events[k]=v;}focus(){this.focused=true;}}
function all(n){return [n,...n.children.flatMap(all)];}
async function boot(search='',narrow=false,pathname='/agentwork/index.html',hash='',fixture=data){const ids={screen:new E('div'),status:new E('p'),main:new E('main')},events={},copied=[],location={search,pathname,hash,replace:url=>location.replaced=url},doc={createElement:t=>new E(t),createTextNode:t=>new E('#text',t),createDocumentFragment:()=>new E('fragment'),getElementById:id=>ids[id],querySelectorAll:()=>[],documentElement:new E('html'),title:''};const ctx={document:doc,location,URL,URLSearchParams,matchMedia:()=>({matches:!narrow,addEventListener(){}}),window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},history:{pushState:(a,b,url)=>{location.search=url.includes('?')?'?'+url.split('?')[1]:'';},replaceState(){}},fetch:async()=>({ok:true,json:async()=>structuredClone(fixture)}),navigator:{clipboard:{writeText:async t=>copied.push(t)}}};for(const file of ['reader.js','task-first.js'])vm.runInNewContext(fs.readFileSync(path.join(root,'web',file),'utf8'),ctx);await new Promise(r=>setImmediate(r));return {ids,events,copied,location,doc,plain:t=>ctx.markdownDOM(t,doc).textContent};}

const music=()=>{const w=data.workflows.find(w=>w.id==='music-intro-ab');assert.ok(w,'admitted music workflow exists');return w;};
const section=b=>all(b.ids.screen).find(n=>n.attrs['data-step']);
const click=n=>{assert.ok(n,'navigation target exists');n.events.click({preventDefault(){}});};
const href=n=>n.attrs.href||n.href||'';

test('music is an actual searchable homepage task, including category and exact title',async()=>{
 const w=music();assert.equal(data.workflows.length,10);assert.equal(w.music_workflow,true);
 for(const q of ['音乐','配乐',w.title]){const b=await boot('?q='+encodeURIComponent(q));assert.equal(b.ids.status.textContent,'');const cards=all(b.ids.screen).filter(n=>n.attrs['data-workflow-id']);assert.ok(cards.some(n=>n.attrs['data-workflow-id']===w.id),q);}
 const b=await boot('?q=音乐&category='+encodeURIComponent(w.category));assert.ok(all(b.ids.screen).some(n=>n.attrs['data-workflow-id']===w.id));
});

test('music search, step changes, back history and task return preserve exact original query',async()=>{
 const w=music(),q='  音 乐  ',category=w.category,b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(category));
 const card=all(b.ids.screen).find(n=>n.attrs['data-workflow-id']===w.id);click(all(card).find(n=>n.tagName==='A'));
 for(let round=0;round<2;round++){
  for(const step of ['prepare','tool','setup','prompt','example','check']){
   const state=p.readRoute(b.location.search);assert.equal(state.q,q);assert.equal(state.category,category);assert.equal(state.work,w.id);assert.equal(state.step,step);
   const selected=all(b.ids.screen).filter(n=>n.attrs['aria-current']==='step');assert.equal(selected.length,1);assert.ok(selected[0].textContent.includes(step==='prepare'?'准备创作要求':w.sections[step].title));
   if(step!=='check')click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent.startsWith('下一步')));
  }
  const checkURL=b.location.search;b.location.search=p.taskLink(w.id,{q,category},'setup').split('index.html')[1];b.events.popstate();assert.equal(section(b).attrs['data-step'],'setup');
  b.location.search=checkURL;b.events.popstate();click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='再选一件工作'));
  assert.equal(p.readRoute(b.location.search).q,q);assert.equal(p.readRoute(b.location.search).category,category);
  if(round===0){const card=all(b.ids.screen).find(n=>n.attrs['data-workflow-id']===w.id);click(all(card).find(n=>n.tagName==='A'));}
 }
});

test('music uses six local labels and no inherited attachment or author-audio claims',async()=>{
 const w=music();for(const key of ['prepare','tool','setup','prompt','example','check']){
  const b=await boot('?work='+w.id+'&step='+key,true);assert.equal(b.ids.status.textContent,'');const s=section(b);assert.equal(s.attrs['data-step'],key);
  assert.ok(all(s).some(n=>n.tagName==='H2'&&n.textContent===(key==='prepare'?'准备创作要求':w.sections[key].title)));
  assert.doesNotMatch(s.textContent,/确认已附加示例文件|下载下面的练习材料，先不上传真实工作资料|这是作者写好的核对样例|作者完整参考（未在产品运行）/);
  assert.equal(all(b.ids.screen).find(n=>n.attrs.class==='step-menu').open,false);
  assert.equal(all(b.ids.screen).filter(n=>n.attrs['data-step']).length,1);
  assert.equal(all(b.ids.screen).filter(n=>n.tagName==='H1').length,1);
 }
 const tool=await boot('?work='+w.id+'&step=tool');assert.match(section(tool).textContent,/18/);assert.match(section(tool).textContent,/Keep Activity/);assert.match(section(tool).textContent,/地区/);assert.match(section(tool).textContent,/额度/);
 assert.ok(all(section(tool)).some(n=>href(n)==='https://gemini.google.com/'));
 const setup=await boot('?work='+w.id+'&step=setup');assert.match(section(setup).textContent,/新.*对话/);assert.match(section(setup).textContent,/Create music/);
 for(const asset of w.assets.filter(a=>a.name.startsWith('prompt-')))assert.ok(!section(setup).textContent.includes(asset.content));
});

test('A and B prompts are complete exact copy blocks interleaved with their own setup and download actions',async()=>{
 const w=music(),b=await boot('?work='+w.id+'&step=prompt'),s=section(b),text=s.textContent;let previous=-1;
 assert.deepEqual(w.sections.prompt.rounds.map(r=>r.label),['A','B']);
 for(const round of w.sections.prompt.rounds){
  const asset=w.assets.find(a=>a.name===round.asset);assert.ok(asset);
  const block=all(s).find(n=>n.attrs['data-music-asset']===asset.name);assert.ok(block);
  const button=all(block).find(n=>n.tagName==='BUTTON');await button.events.click();assert.equal(b.copied.at(-1),asset.content);
  assert.equal(asset.content,fs.readFileSync(path.join(root,'learning/task-first/r1/music',asset.name),'utf8'));
  const before=b.plain(round.before),after=b.plain(round.after),bi=text.indexOf(before),pi=text.indexOf(asset.content),ai=text.indexOf(after,pi+asset.content.length);
  assert.ok(bi>previous&&bi<pi&&pi<ai,round.label+' phase order');previous=ai;
  if(round.label==='A'){assert.match(before,/仍在.*对话/);assert.match(w.sections.setup.body,/新.*对话/);assert.match(w.sections.setup.body,/Create music/);}else{assert.match(before,/新.*对话/);assert.match(before,/Create music/);}assert.match(after,/MP3/);
  assert.ok(all(block).some(n=>href(n)===w.asset_base+asset.name&&'download' in n.attrs));
 }
 assert.doesNotMatch(text,/确认已附加/);
});

test('download phase exposes only original blank records, no fabricated audio or generation control',async()=>{
 const w=music(),b=await boot('?work='+w.id+'&step=example'),s=section(b);
 for(const name of ['listening-record.csv','decision-template.txt','folder-example.txt']){
  const asset=w.assets.find(a=>a.name===name),block=all(s).find(n=>n.attrs['data-music-asset']===name);assert.ok(block);assert.ok(block.textContent.includes(asset.content));
  const a=all(block).find(n=>href(n)===w.asset_base+name);assert.ok(a);assert.ok('download' in a.attrs);assert.ok(fs.existsSync(path.join(root,'site',href(a))));
  const button=all(block).find(n=>n.tagName==='BUTTON');await button.events.click();assert.equal(b.copied.at(-1),asset.content);
 }
 assert.equal(all(s).filter(n=>['AUDIO','SOURCE','VIDEO','IMG','INPUT','FORM'].includes(n.tagName)).length,0);
 assert.equal(all(s).filter(n=>n.tagName==='BUTTON'&&!n.textContent.startsWith('复制')).length,0);
 assert.ok(!all(s).some(n=>/\.(mp3|wav|mp4)(?:$|\?)/i.test(href(n))));
 assert.match(s.textContent,/20秒|20 秒/);assert.match(s.textContent,/未制作|不是.*成品|不.*精确/);
 const check=await boot('?work='+w.id+'&step=check');assert.match(section(check).textContent,/4次|4 次|四次/);assert.match(section(check).textContent,/停止|停下/);
});

test('music text injection stays inert and never creates an upload or generation surface',async()=>{
 const fixture=structuredClone(data),w=fixture.workflows.find(w=>w.id==='music-intro-ab');assert.ok(w);
 const attack='<img src=x onerror=alert(1)><script>alert(1)</script>';
 w.sections.example.body+='\n'+attack+'\n[bad](javascript:alert(1))';w.assets.find(a=>a.name==='listening-record.csv').content+='\n'+attack;
 const b=await boot('?work='+w.id+'&step=example',false,'/agentwork/index.html','',fixture),s=section(b);
 assert.ok(s.textContent.includes(attack));assert.equal(all(s).filter(n=>['IMG','SCRIPT','IFRAME','AUDIO','INPUT'].includes(n.tagName)).length,0);
 assert.ok(!all(s).some(n=>href(n).startsWith('javascript:')));
});

test('music prompt backlinks have separate paragraph containers and retain exact context routes',async()=>{
 const w=music(),q='音乐 候选',route={q,category:w.category,tool:w.product_id};
 const b=await boot(p.taskLink(w.id,route,'prompt').split('index.html')[1]),s=section(b);
 const setup=all(s).find(n=>n.tagName==='A'&&n.textContent==='还没设置 A 对话？先新建对话再选音乐模式');
 const costs=all(s).find(n=>n.tagName==='A'&&n.textContent==='账号、费用与权限详情');
 assert.equal(setup.parentElement.tagName,'P');assert.equal(costs.parentElement.tagName,'P');
 assert.notEqual(setup.parentElement,costs.parentElement);assert.equal(setup.parentElement.children.length,1);assert.equal(costs.parentElement.children.length,1);
 assert.equal(href(setup),p.taskLink(w.id,route,'setup'));assert.equal(href(costs),p.taskLink(w.id,route,'tool'));
});
test('music preparation has Chinese display label and first brief definition without changing input copy',async()=>{
 const w=music(),b=await boot('?work='+w.id+'&step=prepare'),s=section(b);
 assert.match(s.textContent,/准备创作要求/);assert.match(s.textContent,/下面的创作要求（brief）/);
 assert.doesNotMatch(b.ids.screen.textContent,/准备文字 brief/);
 const file=w.assets.find(a=>a.name==='brief.txt'),block=all(s).find(n=>n.attrs['data-music-asset']==='brief.txt');
 await all(block).find(n=>n.tagName==='BUTTON').events.click();assert.equal(b.copied.at(-1),file.content);
 assert.equal(w.sections.prepare.title,'准备文字 brief');
});
