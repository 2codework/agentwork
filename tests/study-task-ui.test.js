'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),test=require('node:test'),path=require('node:path');
const p=require('../web/task-first.js'),root=path.resolve(__dirname,'..'),data=JSON.parse(fs.readFileSync(path.join(root,'site/task-first-data.json')));
class E{constructor(tag,text=''){this.tagName=tag.toUpperCase();this.children=[];this.attrs={};this.events={};this._text=text;this.open=false;}append(...nodes){for(const n of nodes){this.children.push(n);n.parentElement=this;}}set textContent(t){this._text=String(t);this.children=[];}get textContent(){return this._text+this.children.map(n=>n.textContent).join('');}setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k]??null;}removeAttribute(k){delete this.attrs[k];}replaceChildren(...n){this.children=[];this._text='';this.append(...n);}addEventListener(k,v){this.events[k]=v;}focus(){this.focused=true;}}
function all(n){return [n,...n.children.flatMap(all)];}
async function boot(search='',narrow=false,pathname='/agentwork/index.html',hash='',fixture=data){const ids={screen:new E('div'),status:new E('p'),main:new E('main')},events={},copied=[],requests=[],stored=[],location={search,pathname,hash,replace:url=>location.replaced=url},doc={createElement:t=>new E(t),createTextNode:t=>new E('#text',t),createDocumentFragment:()=>new E('fragment'),getElementById:id=>ids[id],querySelectorAll:()=>[],documentElement:new E('html'),title:''};const ctx={localStorage:{getItem(){return null;},setItem(...args){stored.push(args);}},document:doc,location,URL,URLSearchParams,matchMedia:()=>({matches:!narrow,addEventListener(){}}),window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},history:{pushState:(a,b,url)=>{location.search=url.includes('?')?'?'+url.split('?')[1]:'';},replaceState(){}},fetch:async url=>{requests.push(url);return {ok:true,json:async()=>structuredClone(fixture)};},navigator:{clipboard:{writeText:async t=>copied.push(t)}}};for(const file of ['reader.js','task-first.js'])vm.runInNewContext(fs.readFileSync(path.join(root,'web',file),'utf8'),ctx);await new Promise(r=>setImmediate(r));return {ids,events,copied,requests,stored,location,doc,plain:t=>ctx.markdownDOM(t,doc).textContent};}


const studyTask=()=>{const w=data.workflows.find(w=>w.id==='study-three-cards');assert.ok(w,'admitted study task');return w;};
const source=name=>fs.readFileSync(path.join(root,'learning/task-first/r1/study',name),'utf8');
const section=b=>all(b.ids.screen).find(n=>n.attrs['data-step']);
const click=n=>{assert.ok(n,'navigation target');n.events.click({preventDefault(){}});};
const href=n=>n.attrs.href||n.href||'';
const STEPS=['prepare','tool','setup','prompt','example','check'];

test('study cards and model application API are searchable as the twelfth task',async()=>{
 const w=studyTask();assert.equal(data.workflows.length,13);assert.equal(w.study_workflow,true);assert.equal(w.schema,'study-workflow/1');assert.equal(w.interaction_mode,'paste-material');
 for(const q of ['学习','复习卡','模型应用API',w.title]){const b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(w.category));assert.equal(b.ids.status.textContent,'');assert.ok(all(b.ids.screen).some(n=>n.attrs['data-workflow-id']===w.id),q);}
});

test('study local six stages preserve query category across repeated returns and history',async()=>{
 const w=studyTask(),q=' 复习卡 ',category=w.category,b=await boot('?q='+encodeURIComponent(q)+'&category='+encodeURIComponent(category),true);
 for(let round=0;round<2;round++){
  const card=all(b.ids.screen).find(n=>n.attrs['data-workflow-id']===w.id);click(all(card).find(n=>n.tagName==='A'));
  for(let i=0;i<STEPS.length;i++){
   const current=p.readRoute(b.location.search);assert.equal(current.q,q);assert.equal(current.category,category);assert.equal(current.step,STEPS[i]);assert.equal(section(b).attrs['data-step'],STEPS[i]);
   assert.equal(all(section(b)).find(n=>n.tagName==='H2').textContent,w.sections[STEPS[i]].title);
   if(i===0)assert.equal(all(b.ids.screen).find(n=>n.attrs.class==='step-menu').open,false);
   if(i<5)click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent.startsWith('下一步')));
  }
  click(all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='再选一件工作'));assert.equal(p.readRoute(b.location.search).q,q);assert.equal(p.readRoute(b.location.search).category,category);
 }
 b.location.search='?work='+w.id+'&step=example&q='+encodeURIComponent(q)+'&category='+encodeURIComponent(category);b.events.popstate();assert.equal(section(b).attrs['data-step'],'example');assert.equal(p.readRoute(b.location.search).q,q);
});

test('ordinary text setup does not submit placeholders and primary copy is exact send-once',async()=>{
 const w=studyTask(),setup=await boot('?work='+w.id+'&step=setup');assert.match(section(setup).textContent,/新对话|New chat/);assert.match(section(setup).textContent,/不发送|暂不|不提交/);
 const prompt=await boot('?work='+w.id+'&step=prompt'),s=section(prompt),expected=source('send-once.txt');
 assert.ok(s.textContent.includes(expected));assert.ok(!expected.includes('（这里粘贴'));assert.equal(expected.split('\n【固定材料】\n').length,2);assert.equal(expected.split('【固定材料结束】').length,3); // one instruction reference and one closing delimiter
 const copied=[];for(const button of all(s).filter(n=>n.tagName==='BUTTON')){await button.events.click();copied.push(prompt.copied.at(-1));}
 assert.ok(copied.includes(expected));assert.equal(expected,source('card-prompt.txt').trimEnd()+'\n\n【固定材料】\n'+source('material.txt').trimEnd()+'\n【固定材料结束】\n');
 assert.match(s.textContent,/替换/);assert.match(s.textContent,/不要追加|不追加|不要.*两份/);
 const tool=await boot('?work='+w.id+'&step=tool');assert.match(section(tool).textContent,/普通文字|普通.*聊天/);assert.match(section(tool).textContent,/预算.*0|预算为0/);assert.match(section(tool).textContent,/Workspace only/);
 for(const ui of [setup,prompt,tool]){assert.equal(all(section(ui)).filter(n=>['INPUT','FORM','TEXTAREA','VIDEO','AUDIO'].includes(n.tagName)).length,0);assert.equal(ui.requests.length,1);assert.deepEqual(ui.stored,[]);}
});

test('reference cards are normal stage-four learning, while self-test answers are closed and last',async()=>{
 const w=studyTask(),learning=await boot('?work='+w.id+'&step=prompt');assert.ok(section(learning).textContent.includes(learning.plain(source('reference-cards.md'))));
 assert.equal(all(section(learning)).filter(n=>n.attrs['data-study-answers']==='true').length,0);assert.deepEqual(learning.stored,[]);
 for(const query of ['?work='+w.id+'&step=example','?work='+w.id+'&all=1']){
  const b=await boot(query),s=all(b.ids.screen).find(n=>n.attrs['data-step']==='example'),answer=all(s).find(n=>n.attrs['data-study-answers']==='true');
  assert.ok(answer);assert.equal(answer.tagName,'DETAILS');assert.equal(answer.open,false);assert.ok(!('open' in answer.attrs));
  assert.ok(s.textContent.includes(source('self-test-questions.txt')));assert.ok(answer.textContent.includes(b.plain(source('self-test-answers.md'))));
  assert.ok(s.textContent.indexOf(source('self-test-questions.txt'))<s.textContent.indexOf(answer.textContent));
  assert.match(s.textContent,/自己|独立/);assert.match(s.textContent,/不要让AI代答|不要.*AI.*代答|不让.*AI.*代答/);
  assert.equal(all(s).filter(n=>['INPUT','TEXTAREA','FORM'].includes(n.tagName)).length,0);assert.deepEqual(b.stored,[]);
  b.events.popstate();const repeated=all(b.ids.screen).find(n=>n.attrs['data-study-answers']==='true');assert.equal(repeated.open,false);
 }
});

test('blank log and corrective template preserve originals without scores or auto actions',async()=>{
 const w=studyTask(),b=await boot('?work='+w.id+'&step=example'),s=section(b);
 assert.equal(fs.readFileSync(path.join(root,'site/task-guides/study/error-log.md'),'utf8'),source('error-log.md'));assert.ok(s.textContent.includes(source('correction-prompt.txt')));assert.match(s.textContent,/替换.*原答|原答.*替换/);
 assert.ok(all(s).some(n=>href(n)==='task-guides/study/error-log.md'));assert.ok(!all(s).some(n=>n.attrs.type==='submit'));
 const finish=await boot('?work='+w.id+'&step=check');assert.match(section(finish).textContent,/不.*自动分数|不给自动分数/);assert.match(section(finish).textContent,/不是系统提醒|不是.*提醒/);assert.deepEqual(finish.stored,[]);assert.equal(finish.requests.length,1);
});

test('study schema rejects wrong interaction mode and markup remains inert',async()=>{
 const bad=structuredClone(data),w=bad.workflows.find(w=>w.id==='study-three-cards');w.interaction_mode='upload-files';
 const blocked=await boot('?work='+w.id+'&step=prompt',false,'/agentwork/index.html','',bad);assert.equal(all(blocked.ids.screen).filter(n=>n.tagName==='BUTTON').length,0);assert.equal(blocked.copied.length,0);
 const fixture=structuredClone(data),item=fixture.workflows.find(w=>w.id==='study-three-cards'),attack='<img src=x onerror=alert(1)><script>alert(1)</script>';item.sections.prepare.body+='\n'+attack+'\n[bad](javascript:alert(1))';
 const b=await boot('?work='+item.id+'&step=prepare',false,'/agentwork/index.html','',fixture),s=section(b);assert.ok(s.textContent.includes(attack));assert.equal(all(s).filter(n=>['IMG','SCRIPT','IFRAME','FORM','INPUT'].includes(n.tagName)).length,0);assert.ok(!all(s).some(n=>href(n).startsWith('javascript:')));
});

test('exact application-model-API alias reaches the study card and preserves the query on return',async()=>{
 const query='应用模型API',b=await boot('?q='+encodeURIComponent(query));
 const cards=all(b.ids.screen).filter(n=>n.attrs['data-workflow-id']);assert.equal(cards.length,1);assert.equal(cards[0].attrs['data-workflow-id'],'study-three-cards');
 const start=all(cards[0]).find(n=>n.tagName==='A');start.events.click({preventDefault(){}});assert.equal(new URLSearchParams(b.location.search).get('q'),query);
 const back=all(b.ids.screen).find(n=>n.tagName==='A'&&n.textContent==='← 选任务');assert.ok(back);back.events.click({preventDefault(){}});assert.equal(new URLSearchParams(b.location.search).get('q'),query);assert.equal(all(b.ids.screen).filter(n=>n.attrs['data-workflow-id']).length,1);
});

test('study only exact first sentences change; remaining prose and copied bytes stay original',async()=>{
 const w=studyTask();
 const oldPrepare='打开同目录 \x60material.txt\x60，完整读一遍L1–L8。',newPrepare='先读下方固定材料的 L1–L8；也可下载 material.txt 后阅读。';
 const oldPrompt='**推荐简路：复制完整的 \x60send-once.txt\x60。**',newPrompt='推荐简路：复制下方完整制卡消息。';
 for(const [key,oldText,newText]of [['prepare',oldPrepare,newPrepare],['prompt',oldPrompt,newPrompt]]){
  assert.ok(w.sections[key].body.startsWith(oldText));
  const b=await boot('?work='+w.id+'&step='+key),s=all(b.ids.screen).find(n=>n.attrs['data-step']===key);
  assert.ok(s.textContent.includes(newText));assert.ok(s.textContent.includes(b.plain(w.sections[key].body.slice(oldText.length))));
  assert.ok(!s.textContent.includes(oldText));if(key==='prompt'){assert.ok(!s.textContent.includes('\x60send-once.txt\x60'));assert.ok(all(s).some(n=>n.tagName==='A'&&n.textContent==='下载完整制卡消息（send-once.txt）'&&href(n)===w.asset_base+'send-once.txt'));}
  const button=all(s).find(n=>n.tagName==='BUTTON'&&n.textContent===(key==='prepare'?'复制固定材料（只供阅读核对）':'复制完整制卡消息（提示与材料已合并）'));
  await button.events.click();assert.equal(b.copied.at(-1),w.study_assets[key==='prepare'?'material.txt':'send-once.txt']);
 }
});
test('study exact-prefix projection does not rewrite a changed sentence or a lookalike workflow',async()=>{
 for(const change of [w=>w.sections.prepare.body='不同开头。'+w.sections.prepare.body,w=>w.id='study-three-cards-extra']){
  const fixture=structuredClone(data),w=fixture.workflows.find(w=>w.id==='study-three-cards');change(w);
  const b=await boot('?work='+w.id+'&step=prepare',false,'/agentwork/index.html','',fixture);
  assert.ok(b.ids.screen.textContent.includes(b.plain(w.sections.prepare.body)));
  assert.ok(!b.ids.screen.textContent.includes('先读下方固定材料的 L1–L8'));
 }
});
