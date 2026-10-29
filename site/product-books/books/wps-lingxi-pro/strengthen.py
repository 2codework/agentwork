import pathlib,json,copy
P=pathlib.Path(__file__).parent;d=json.loads((P/'playbooks.json').read_text());b=json.loads((P/'product-book.json').read_text())
edges={
'sales-review':('15000,9000',',9000',{'complete':False,'missing':['2026-10/线上/revenue'],'october_revenue':None},'缺失收入不当0；10月收入与依赖它的增长率不可确认。'),
'budget-variance':('行政,4000,4000','行政,0,4000',{'department':'行政','variance':4000,'variance_pct':None},'行政预算0，实际4000，差异4000；偏差率不可计算。'),
'meeting-actions':('10月25日给结果','给结果',{'owner':'小北','due_date':None,'dependency':'原型'},'测试负责人仍为小北，但没有截止日；不能从基线复制10月25日。'),
'hr-onboarding':('D2容量3小时；D3容量2小时','D2容量2小时；D3容量3小时',{'feasible':True,'schedule':{'D1':['产品演示'],'D2':['安全基础'],'D3':['工单演练','复盘']}},'经明确修改输入后有解；D3内部顺序先演练后复盘。'),
'support-faq':('试用额度20次。','',{'trial_days':7,'trial_uses':None,'refund_promised':False},'额度未知，不沿用基线20次；7天仍可引用，退款仍不能承诺。'),
'procurement-matrix':('丙,110,7,24','丙,110,7,',{'vendor':'丙','eligibility':'待核验','warranty_months':None},'保修缺失，不能认为满足12月或沿用24月。'),
'marketing-deck':('社区,500,50,30','社区,500,50,0',{'channel':'社区','attendance_rate_pct':0,'cost_per_attendee':None},'到场率0%，单位到场成本不可计算；图中不能表现为0元成本。'),
'operations-sop':('P1 1.5kg 有标签','P1 重量未知 有标签',{'parcel':'P1','route':'人工确认','weight_kg':None},'重量未知，先扫码再交人工确认；不可默认A线。')}
for r in d['recipes']:
 slug=r['id'].removeprefix('wps-lingxi-pro-');folder=P/'fixtures'/slug;old,new,want,ref=edges[slug]
 inp=r['input']['full_text'].replace(old,new);assert inp!=r['input']['full_text']
 (folder/'edge-input.txt').write_text(inp)
 (folder/'edge-expected.json').write_text(json.dumps(want,ensure_ascii=False,indent=2)+'\n')
 prompt='只依据下面修改后的完整合成输入处理边界测试，不读取基线答案。不得联网、外发或改真实系统。输出 edge-result.json；只含以下键：'+', '.join(want)+'. 数值缺失使用null，布尔用true/false。\n'+inp
 (folder/'edge-prompt.txt').write_text(prompt)
 (folder/'edge-author-reference.md').write_text('# 作者边界参考，非产品实测\n'+ref+'\n\n```json\n'+json.dumps(want,ensure_ascii=False,indent=2)+'\n```\n')
 r['negative_test']['reproducible_variant']={'input':str((folder/'edge-input.txt').relative_to(P)),'prompt':str((folder/'edge-prompt.txt').relative_to(P)),'expected':str((folder/'edge-expected.json').relative_to(P)),'author_reference':str((folder/'edge-author-reference.md').relative_to(P)),'command':'python evaluator.py '+slug+' /path/to/edge-result.json --edge','execution':'not_run'}
 r['rubric']['human']+=['逐项检查目标原生文件可打开、布局可读；与完整作者参考内容和result.json一致。此人工检查未执行。']
 for x in b['recipes']:
  if x['recipe_id']==r['id']:x['negative_test']=r['negative_test'];x['rubric']=r['rubric'];x['human_rubric']=r['rubric']['human']
for s in d['sources']:
 if s['id']=='lx-privacy':s['retrieval_limitation']='本轮web search返回政策正文摘录与2026-09-10日期；直接open正文0行。独立审查未能重复读取正文，精确政策日期/具体承诺标search_index_only，需执行前直接确认。'
 if s['id']=='cmcc-privacy':s['scope_caution']='政策含云电脑继承权限语境；不据此认定本地桌面全部行为或所有端隐私范围相同。'
d['product_profile']['privacy_evidence_conflict']['verification_limitation']='政策内容来自官方域名搜索索引；直接正文无法稳定读取。精确条款与生效日期待使用前复核；不据此作零上传或不训练的普遍保证。'
for c in d['identity_resolution']['candidates']:
 if c['id']=='cmcc-lingxi-assistant':c['privacy_cost']+=' 已读取政策含云电脑权限语境，不能无条件套用于全部原生桌面行为。'
for name,x in [('playbooks.json',d),('product-book.json',b),('sources.json',d['sources']),('identity.json',d['identity_resolution'])]:(P/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
with (P/'README.md').open('a') as f:f.write('\n### 取证限制与负例\nWPS隐私政策正文在搜索索引可见、直接打开0行；精确2026-09-10日期和具体承诺仅search_index_only，不当作独立完整正文核验。中国移动政策涉及云电脑继承权限，不推论所有桌面端等价。每题新增完整edge-input/prompt/expected/author-reference，真实产品均not_run。\n')
