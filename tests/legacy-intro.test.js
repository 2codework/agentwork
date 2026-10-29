const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {fixture,all,text,anchors}=require('./legacy-dom-fixture.js');
const root=path.join(__dirname,'..'),baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/legacy-case-anchors.json')));
test('all 138 original anchor IDs retain exact tag and complete semantic text',()=>{
 const f=fixture(root);assert.equal(f.ctx.fixtureData.cases.length,138);
 for(const c of f.ctx.fixtureData.cases){f.run('navigate({case:'+JSON.stringify(c.id)+'})');assert.deepEqual(anchors(f),baseline.cases[c.id],c.id);}
});
test('all 138 show original outputs, risks and required permissions before original evidence',()=>{
 const f=fixture(root);let permissions=0;
 for(const c of f.ctx.fixtureData.cases){
  f.run('navigate({case:'+JSON.stringify(c.id)+'})');const nodes=all(f.ids.content),intro=nodes.find(n=>n.id==='case-task-introduction'),req=nodes.find(n=>n.id==='case-start-requirements'),original=nodes.find(n=>n.id==='case-original-introduction');
  assert.ok(intro&&req&&original,c.id);assert.equal(original.open,undefined);assert.ok(text(req).includes(c.risks),c.id);
  for(const k of ['permissions','permission_boundary','cost','license'])if(c[k])for(const v of Array.isArray(c[k])?c[k]:[c[k]])assert.ok(text(req).includes(v),c.id+':'+k);
  if(c.permissions)permissions++;
  for(const v of c.original_exercise_plan?.expected_artifacts||[c.output])assert.ok(text(intro).includes(v),c.id);
  assert.ok(text(original).includes(c.summary));assert.ok(text(original).includes(c.evidence_note||'合成练习未证明真实部署或收益。'));
  assert.ok(intro.parentElement.children.indexOf(intro)<intro.parentElement.children.indexOf(original));
 }
 assert.equal(permissions,54);
});
test('goals use exact structured task or exact lesson goal; never-run is not a blanket prohibition',()=>{
 const f=fixture(root);
 f.run("navigate({case:'gap-express-targeted'})");let nodes=all(f.ids.content),intro=nodes.find(n=>n.id==='case-task-introduction');
 assert.match(text(intro),/只把时间从周六14:00改为周日15:00/);assert.match(text(intro),/本站未在产品中验证/);assert.doesNotMatch(text(intro),/仅纸面/);
 f.run("navigate({case:'mcp-lab-tools'})");intro=all(f.ids.content).find(n=>n.id==='case-task-introduction');assert.match(text(intro),/算出7\+5=12/);
 f.run("navigate({case:'meeting-action-log'})");const req=all(f.ids.content).find(n=>n.id==='case-start-requirements');assert.match(text(req),/不能据此认为免费/);
});
test('old collapsed anchor reveals all ancestors and preserves original text',()=>{
 const f=fixture(root);f.run("navigate({case:'gap-express-targeted'})");
 const nodes=all(f.ids.content),original=nodes.find(n=>n.id==='case-original-introduction'),target=all(original).find(n=>/^reading-/.test(n.id||''));
 f.ctx.target=target;f.run('revealReadingTarget(target)');assert.equal(original.open,true);assert.equal(target.scrolled,true);
});
test('every legacy anchor is unique and can reveal its original collapsed ancestors',()=>{
 const f=fixture(root);let count=0;
 for(const c of f.ctx.fixtureData.cases){
  f.run('navigate({case:'+JSON.stringify(c.id)+'})');
  const nodes=all(f.ids.content).filter(n=>/^(section-|reading-(?:sub-)?\d)/.test(n.id||''));
  assert.equal(new Set(nodes.map(n=>n.id)).size,nodes.length,c.id);
  for(const target of nodes){
   for(let p=target;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=false;
   f.ctx.target=target;f.run('revealReadingTarget(target)');
   for(let p=target;p;p=p.parentElement)if(p.tagName==='DETAILS')assert.equal(p.open,true,c.id+':'+target.id);
   count++;
  }
 }
 assert.equal(count,3123);
});
test('unknown or duplicate lesson goals fall back without fabricating summaries; new fields remain text',()=>{
 const f=fixture(root);
 f.ctx.fake={title:'Fallback',output:'draft',lesson_markdown:'### 学习目标\none\n### 学习目标\ntwo'};
 assert.equal(f.run('caseReadingIntro(fake).goal'),'Fallback');
 const c=JSON.parse(JSON.stringify(f.ctx.fixtureData.cases[0]));
 c.id='hostile-intro';c.title='<img src=x onerror=alert(1)>';c.original_exercise_plan={task:'<script>unsafe</script>',expected_artifacts:['<iframe>'],stop_conditions:['<img>']};c.permissions=['<svg onload=evil>'];f.ctx.fake=c;
 f.run('data.cases.push(fake);navigate({case:fake.id})');
 const nodes=all(f.ids.content);assert.ok(text(f.ids.content).includes('<script>unsafe</script>'));
 assert.equal(nodes.filter(n=>['SCRIPT','IMG','IFRAME','SVG'].includes(n.tagName)).length,0);
});
test('Back/Forward reopens old anchor inside moved evidence instead of landing in collapsed content',async()=>{
 const f=fixture(root);f.ctx.fetch=async()=>({ok:true,json:async()=>f.ctx.fixtureData});f.ctx.localStorage={getItem:()=>null,setItem(){}};f.ctx.requestAnimationFrame=cb=>cb();await f.run('init()');
 f.run("navigate({case:'gap-express-targeted'})");
 const original=all(f.ids.content).find(n=>n.id==='case-original-introduction');
 const anchor=all(original).find(n=>/^reading-/.test(n.id||''));
 f.ctx.location.search='?case=gap-express-targeted';f.ctx.location.hash='#'+anchor.id;
 f.ctx.window.events.popstate();
 const restored=all(f.ids.content).find(n=>n.id==='case-original-introduction');
 assert.equal(restored.open,true);
 assert.equal(all(restored).find(n=>n.id===anchor.id).scrolled,true);
});

test('three introductory jumps occupy separate explicit grid rows with unchanged destinations',()=>{
 const f=fixture(root);f.run("navigate({case:'gap-express-targeted'})");
 const group=all(f.ids.content).find(n=>n.className==='reader-intro-jumps');
 assert.ok(group);assert.equal(group.children.length,3);
 assert.deepEqual(group.children.map(n=>[n.tagName,n.textContent,n.href]),[
  ['A','任务与预期产物','#case-task-introduction'],
  ['A','开始前确认','#case-start-requirements'],
  ['A','原介绍与证据状态','#case-original-introduction']
 ]);
 const css=fs.readFileSync(path.join(root,'web/style.css'),'utf8');
 const rule=css.match(/\.detail-toc \.reader-intro-jumps\{([^}]+)\}/);
 assert.ok(rule);assert.match(rule[1],/display:grid/);assert.match(rule[1],/grid-template-columns:minmax\(0,1fr\)/);assert.match(rule[1],/gap:3px/);assert.match(rule[1],/grid-column:1 \/ -1/);
});
