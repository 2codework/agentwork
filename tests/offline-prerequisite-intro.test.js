const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {fixture,all,text}=require('./legacy-dom-fixture.js'),root=path.join(__dirname,'..');
const ids=['mcp-lab-roles','mcp-lab-initialize','mcp-lab-tools','mcp-lab-resources-prompts','mcp-lab-errors','mcp-lab-cancel','mcp-lab-scope','mcp-lab-injection','mcp-lab-skill','mcp-lab-debug','mcp-lab-migration','mcp-lab-modern'];
const required=['能阅读JSON对象与数组','Python 3.10+，仅标准库；无需账号、网络、SDK或模型'];
const note='本课使用已有的本地 Python 环境，不接入外部服务；自行扩展到其他服务时，另行核对授权和费用。';
function render(f,c){f.ctx.current=c;f.run("route={...route,case:current.id};$('content').replaceChildren();detail(current)");return all(f.ids.content).find(n=>n.id==='case-start-requirements');}
test('exact twelve source prerequisites surface unchanged with bounded local-environment note',()=>{
 const f=fixture(root);assert.deepEqual(f.ctx.fixtureData.cases.filter(c=>c.lesson_markdown).map(c=>c.id),ids);
 for(const id of ids){const c=f.ctx.fixtureData.cases.find(c=>c.id===id);assert.deepEqual(c.prerequisites,required);assert.equal(c.verification_status,'offline_contract_only');for(const v of required)assert.ok(c.lesson_markdown.includes('- '+v));
  const req=render(f,c);for(const v of required)assert.ok(text(req).includes(v));assert.ok(text(req).includes(note));assert.doesNotMatch(text(req),/不能据此认为免费或无需账号/);assert.doesNotMatch(text(req),/设备免费|电费免费|全部免费/);
 }
});
test('all other 126 prerequisite sections are exactly unchanged',()=>{
 const f=fixture(root),baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/nonlesson-prerequisites-baseline.json')));
 assert.equal(Object.keys(baseline).length,126);
 for(const [id,hash]of Object.entries(baseline)){const c=f.ctx.fixtureData.cases.find(c=>c.id===id);assert.equal(crypto.createHash('sha256').update(text(render(f,c))).digest('hex'),hash,id);}
});
test('negation, missing reordered duplicate or wrong-type arrays, unrecognized ID and state fail closed',()=>{
 const f=fixture(root),base=f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools');
 const changes=[
  c=>c.prerequisites[1]='Python 3.10+，仅标准库；不是无需账号、网络、SDK或模型',
  c=>c.prerequisites[1]='不保证'+c.prerequisites[1],
  c=>c.prerequisites.pop(),c=>c.prerequisites.reverse(),c=>c.prerequisites.push(c.prerequisites[1]),
  c=>c.prerequisites=required.join('\n'),c=>c.prerequisites=null,c=>c.prerequisites[1]={text:required[1]},
  c=>c.id='mcp-lab-unknown',c=>c.verification_status='product_run',c=>c.verification_status=null,c=>c.lesson_markdown=''
 ];
 for(const change of changes){const c=structuredClone(base);change(c);f.ctx.current=c;assert.equal(f.run('exactOfflinePrerequisites(current)'),false);const req=render(f,c),t=text(req||f.ids.content);if(c.lesson_markdown===''){assert.equal(req,undefined);assert.match(t,/课程正文格式异常/);}else assert.ok(t.includes('不能据此认为免费或无需账号'));assert.ok(!t.includes(note));assert.ok(!t.includes('这份离线练习的前置知识与环境'));}
});
test('specific future cost text takes priority over the missing-cost note',()=>{
 const f=fixture(root),c=structuredClone(f.ctx.fixtureData.cases.find(c=>c.id==='mcp-lab-tools'));c.cost='新增服务另行计费，不代表本地课程费用';const t=text(render(f,c));assert.ok(t.includes(c.cost));assert.ok(!t.includes(note));assert.ok(t.includes(required[1]));
});
