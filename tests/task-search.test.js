'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const p=require('../web/task-first.js'),data=JSON.parse(fs.readFileSync(path.join(__dirname,'../site/task-first-data.json'))),rows=data.workflows;
const ids=(q,category='')=>p.matching(rows,{q,category}).map(w=>w.id);
test('all homepage placeholder examples find their existing actual lesson',()=>{for(const [q,id]of [['整理订单','clean-orders'],['会议纪要','meeting-actions'],['周报','weekly-report']])assert.deepEqual(ids(q),[id]);});
test('all twelve exact lesson titles remain searchable without new source keywords',()=>{assert.equal(rows.length,12);for(const w of rows)assert.ok(ids(w.title).includes(w.id),w.title);});
test('bounded ordinary phrases cover each actual goal and do not mutate records',()=>{const before=JSON.stringify(rows);for(const [q,id]of [['整理会议记录','meeting-actions'],['帮我写一份周报','weekly-report'],['清洗表格','clean-orders'],['PPT大纲','six-slide-outline'],['竞品分析','competitor-research'],['修复bug','fix-small-bug'],['客服回复','customer-reply'],['内容排期','three-day-content'],['设计交接清单','design-handoff']])assert.deepEqual(ids(q),[id]);assert.equal(JSON.stringify(rows),before);});
test('case, spacing and fullwidth normalization affect matching only',()=>{for(const q of ['整理 订单',' 整 理　订 单 ','\t整理订单\n','整理\n订单'])assert.deepEqual(ids(q),['clean-orders']);assert.deepEqual(ids(' ｐＰＴ 大纲 '),['six-slide-outline']);assert.deepEqual(ids(' ＣＯＤＥＸ '),['fix-small-bug']);const route={q:'  整 理 订单  ',category:'表格与数据',tool:'tencent-workbuddy'};const snapshot=JSON.stringify(route);p.matching(rows,route);assert.equal(JSON.stringify(route),snapshot);assert.equal(p.readRoute('?'+p.taskLink('clean-orders',route).split('?')[1]).q,route.q);});
test('explicit multi-goal separators use union while category remains mandatory',()=>{for(const q of ['整理订单、会议纪要','整理订单，会议纪要','整理订单,会议纪要','整理订单；会议纪要'])assert.deepEqual(ids(q),['meeting-actions','clean-orders']);assert.deepEqual(ids('整理订单、会议纪要','表格与数据'),['clean-orders']);assert.deepEqual(ids('整理订单','客户与销售'),[]);assert.deepEqual(ids('整理订单、整理订单'),['clean-orders']);});
test('unmatched goals and unsupported image, publishing and refund actions do not become aliases',()=>{for(const q of ['不存在的任务XYZ','生成图片','制作设计稿','自动发布公众号','自动退款','帮我黑进账户'])assert.deepEqual(ids(q),[],q);});
test('empty normalized query retains exact twelve tasks and category filtering',()=>{assert.equal(ids(' \t ').length,12);assert.deepEqual(ids('','表格与数据'),['clean-orders']);});

test('one explicit study word-order alias does not enable general permutation search or mutate data',()=>{
 const before=JSON.stringify(rows);assert.deepEqual(ids('应用模型API'),['study-three-cards']);assert.deepEqual(ids('模型应用API'),['study-three-cards']);
 // Existing substring matching already matches two other strings; retain those baseline outcomes.
 for(const q of ['API模型应用','应用API模型'])assert.deepEqual(ids(q),['study-three-cards'],q);
 for(const q of ['模型API应用','API应用模型'])assert.deepEqual(ids(q),[],q);
 assert.deepEqual(ids('应用模型API','表格与数据'),[]);assert.equal(JSON.stringify(rows),before);
});
