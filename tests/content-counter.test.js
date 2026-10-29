'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),test=require('node:test'),path=require('node:path');
const p=require('../web/task-first.js'),root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/task-first-data.json')));
class E{constructor(tag,text=''){this.tagName=tag.toUpperCase();this.children=[];this.attrs={};this.events={};this._text=text;this.open=false;}append(...nodes){for(const n of nodes){this.children.push(n);n.parentElement=this;}}set textContent(t){this._text=String(t);this.children=[];}get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}replaceChildren(...n){this.children=[];this._text='';this.append(...n);}addEventListener(k,v){this.events[k]=v;}focus(){this.focused=true;}}
function all(n){return [n,...n.children.flatMap(all)];}
async function boot(search='',narrow=false,pathname='/agentwork/index.html',hash='',fixture=data,sourceOverride=null){const ids={screen:new E('div'),status:new E('p'),main:new E('main')},events={},copied=[],requests=[],stored=[],location={search,pathname,hash,replace:url=>location.replaced=url},doc={createElement:t=>new E(t),createTextNode:t=>new E('#text',t),createDocumentFragment:()=>new E('fragment'),getElementById:id=>ids[id],querySelectorAll:()=>[],documentElement:new E('html'),title:''};const ctx={localStorage:{getItem(){return null;},setItem(...args){stored.push(args);}},document:doc,location,URL,URLSearchParams,matchMedia:()=>({matches:!narrow,addEventListener(){}}),window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},history:{pushState:(a,b,url)=>{location.search=url.includes('?')?'?'+url.split('?')[1]:'';},replaceState(){}},fetch:async url=>{requests.push(url);return {ok:true,json:async()=>structuredClone(fixture)};},navigator:{clipboard:{writeText:async t=>copied.push(t)}}};for(const file of ['reader.js','task-first.js'])vm.runInNewContext(file==='task-first.js'&&sourceOverride!==null?sourceOverride:fs.readFileSync(path.join(root,'web',file),'utf8'),ctx);await new Promise(r=>setImmediate(r));return {ids,events,copied,requests,stored,location,doc,plain:t=>ctx.markdownDOM(t,doc).textContent};}


const counter=b=>all(b.ids.screen).filter(n=>n.attrs['data-content-counter']==='three-day-content');
const field=box=>all(box).find(n=>n.tagName==='TEXTAREA');
const result=box=>all(box).find(n=>n.attrs['data-count-result']);
const click=n=>n.events.click({preventDefault(){}});
test('exact inclusive BMP Han counting, whitespace, boundary lengths and long text',()=>{
 for(const n of [0,149,150,220,221,1000000])assert.equal(p.countContentHan('汉'.repeat(n)),n);
 assert.equal(p.countContentHan(' \n\tABC123，。😀𠀀㐀'),0);
 assert.equal(p.countContentHan(String.fromCodePoint(0x4dff,0x4e00,0x9fff,0xa000)),2);
 assert.equal(p.countContentHan('汉😀𠀀字㐀ABC123'),2);assert.equal(p.countContentHan('一二三四五六七八九十'),10);
});
test('only exact content check phase has one empty accessible counter immediately after checklist',async()=>{
 for(const w of data.workflows){const b=await boot('?work='+w.id+'&step=check');assert.equal(counter(b).length,w.id==='three-day-content'?1:0);}
 for(const step of ['prepare','tool','setup','prompt','example'])assert.equal(counter(await boot('?work=three-day-content&step='+step)).length,0);
 const b=await boot('?work=three-day-content&step=check'),box=counter(b)[0],input=field(box),parent=box.parentElement;
 assert.equal(input.value,'');assert.equal(parent.children[parent.children.indexOf(box)-1].tagName,'UL');
 assert.equal(all(box).find(n=>n.tagName==='LABEL').attrs.for,input.attrs.id);
 assert.equal(result(box).attrs['aria-live'],'polite');
 for(const phrase of ['不上传、不联网、不保存','不等于事实、权利或内容合格','不要粘标题','此范围以外的汉字'])assert.ok(box.textContent.includes(phrase));
});
test('input gives correct boundary feedback, inert text, clear and no network or persistence',async()=>{
 const b=await boot('?work=three-day-content&step=check'),box=counter(b)[0],input=field(box),initialRequests=[...b.requests];
 for(const n of [149,150,220,221]){input.value='汉'.repeat(n);input.events.input();assert.ok(result(box).textContent.includes(n+' 个汉字'));assert.ok(result(box).textContent.includes(n<150?'还差 1':n>220?'多出 1':'字数在150–220范围内'));}
 input.value='<img src=x onerror=alert(1)><script>evil()</script>汉😀𠀀';input.events.input();assert.ok(result(box).textContent.includes('1 个汉字'));assert.equal(all(box).filter(n=>['IMG','SCRIPT','IFRAME','FORM'].includes(n.tagName)).length,0);
 click(all(box).find(n=>n.tagName==='BUTTON'));assert.equal(input.value,'');assert.ok(input.focused);assert.ok(result(box).textContent.includes('当前：0'));
 assert.deepEqual(b.requests,initialRequests);assert.equal(b.stored.length,0);assert.equal(b.copied.length,0);
});
test('step switches, history returns and repeated rebuilding clear without losing query context',async()=>{
 const query='?work=three-day-content&step=check&q='+encodeURIComponent('内容排期');const b=await boot(query);
 for(let i=0;i<3;i++){const input=field(counter(b)[0]);input.value='汉'.repeat(160);input.events.input();
  b.location.search=query.replace('step=check','step=example');b.events.popstate();assert.equal(counter(b).length,0);
  b.location.search=query;b.events.popstate();assert.equal(counter(b).length,1);assert.equal(field(counter(b)[0]).value,'');assert.equal(p.readRoute(b.location.search).q,'内容排期');
 }
 const box=counter(b)[0];field(box).value='秘密正文';field(box).events.input();
 click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='再选一件工作'));assert.equal(counter(b).length,0);
 b.location.search=query;b.events.popstate();assert.equal(field(counter(b)[0]).value,'');assert.equal(b.stored.length,0);
});

test('all six phases of the other twelve workflows retain exact original DOM',async()=>{
 const bytes=fs.readFileSync(path.join(root,'tests/fixtures/content-counter-before.js.txt'));
 assert.equal(require('node:crypto').createHash('sha256').update(bytes).digest('hex'),'e9b960f37c3ba291aa341539d5ee03360968007b9716f565aa5f4ec0cd730bc3');
 const shape=n=>({tag:n.tagName,text:n._text,attrs:n.attrs,children:n.children.map(shape)});
 for(const w of data.workflows.filter(w=>w.id!=='three-day-content'))for(const step of ['prepare','tool','setup','prompt','example','check']){
  const url='?work='+w.id+'&step='+step+'&q=test';const before=await boot(url,false,'/agentwork/index.html','',data,bytes.toString('utf8')),after=await boot(url);
  assert.deepEqual(shape(after.ids.screen),shape(before.ids.screen),w.id+'/'+step);
 }
});
