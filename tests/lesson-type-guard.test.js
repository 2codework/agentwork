const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {fixture,all,text}=require('./legacy-dom-fixture.js'),root=path.join(__dirname,'..');
const shape=n=>({tag:n.tagName,text:n.textContent||'',id:n.id||'',class:n.className||'',href:n.href||'',open:Boolean(n.open),type:n.type||'',checked:Boolean(n.checked),children:(n.children||[]).map(shape)});
test('all 138 valid detail DOM trees remain exact, including their old anchors and state',()=>{
 const f=fixture(root),baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/lesson-type-valid-dom-baseline.json')));assert.equal(Object.keys(baseline).length,138);
 for(const c of f.ctx.fixtureData.cases){f.run('navigate({case:'+JSON.stringify(c.id)+'})');assert.equal(crypto.createHash('sha256').update(JSON.stringify(shape(f.ids.content))).digest('hex'),baseline[c.id],c.id);}
});
const bad=[null,false,true,0,7,0.5,[],{}, {html:'<img src=x onerror=evil><script>evil</script>'},'', ' \n\t'];
test('all present invalid values are isolated without tutorial/download/copy/complete controls',()=>{
 const f=fixture(root),base=f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools');
 for(const value of bad){
  f.ctx.current={...base,lesson_markdown:value};
  assert.equal(f.run('lessonMarkdownState(current)'),'invalid');assert.equal(f.run('caseReadingIntro(current).goal'),base.title);assert.equal(f.run('caseReadingIntro(current).outputs.length'),0);
  const card=f.run('card(current)');assert.match(text(card),/课程正文格式异常/);
  f.run("$('content').replaceChildren();detail(current)");const nodes=all(f.ids.content);
  assert.match(text(f.ids.content),/资料来源（不是已验证教程）/);
  assert.ok(!nodes.some(n=>['INPUT','BUTTON','PRE','SCRIPT','IMG','IFRAME'].includes(n.tagName)));
  assert.ok(!nodes.some(n=>/\.zip/.test(n.href||'')));assert.ok(!text(f.ids.content).includes('[object Object]'));
  assert.equal(f.run('exactOfflinePrerequisites(current)'),false);
 }
});
test('missing is legal and valid string is not coerced or trimmed',()=>{
 const f=fixture(root);f.ctx.current={};assert.equal(f.run('lessonMarkdownState(current)'),'missing');
 f.ctx.current={lesson_markdown:' \n# Original \n'};assert.equal(f.run('lessonMarkdownState(current)'),'valid');assert.equal(f.ctx.current.lesson_markdown,' \n# Original \n');
});
test('list to bad detail return and Back/Forward retain filters and do not break another case or progress',async()=>{
 const f=fixture(root);f.ctx.fetch=async()=>({ok:true,json:async()=>f.ctx.fixtureData});f.ctx.localStorage={getItem:()=>null,setItem(){}};f.ctx.requestAnimationFrame=cb=>cb();await f.run('init()');
 const target=f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools');target.lesson_markdown={};
 f.run("progress={'meeting-action-log':'2026-10-28T12:00:00.000Z'};navigate({q:'MCP',topic:'mcp',page:1});navigate({case:'mcp-lab-tools'})");
 assert.match(text(f.ids.content),/课程正文格式异常/);
 const back=all(f.ids.content).find(n=>n.tagName==='A'&&n.textContent==='← 返回结果');const params=new URLSearchParams(back.href.slice(1));assert.equal(params.get('q'),'MCP');assert.equal(params.get('topic'),'mcp');assert.equal(params.get('case'),null);
 f.ctx.location.search=back.href;f.ctx.window.events.popstate();assert.doesNotMatch(text(f.ids.content),/课程正文格式异常/);
 f.ctx.location.search='?case=mcp-lab-tools&q=MCP&topic=mcp';f.ctx.window.events.popstate();assert.match(text(f.ids.content),/课程正文格式异常/);
 f.run("navigate({case:'meeting-action-log',q:'',topic:''})");assert.doesNotMatch(text(f.ids.content),/课程正文格式异常/);assert.equal(f.run("progress['meeting-action-log']"),'2026-10-28T12:00:00.000Z');
});
test('initial deep link with malformed lesson loads an isolated error rather than site-wide failure',async()=>{
 for(const value of [{html:'<script>evil</script>'},null,false,0,[],' \n']){
  const f=fixture(root);f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools').lesson_markdown=value;
  f.ctx.location.search='?case=mcp-lab-tools&q=MCP';
  f.ctx.fetch=async()=>({ok:true,json:async()=>f.ctx.fixtureData});f.ctx.localStorage={getItem:()=>null,setItem(){}};f.ctx.requestAnimationFrame=cb=>cb();
  await f.run('init()');assert.match(text(f.ids.content),/课程正文格式异常/);assert.doesNotMatch(f.ids.status.textContent,/加载失败/);
  assert.equal(f.ids['view-title'].textContent,f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools').title);
  f.run("navigate({case:'meeting-action-log',q:''})");assert.doesNotMatch(text(f.ids.content),/课程正文格式异常/);
 }
});
