from pathlib import Path
p=Path(__file__).parent
b=(p/'build.py').read_text()
b=b.replace("D['recipes']=cases",'''# r3 acceptance and completeness corrections
for r in cases:
 root=P/r['fixture_root']/'reference'
 slug=r['id'].removeprefix('zai-zcode-')
 negatives={
 'refund-fix':'负例：bool、浮点、负金额、超额都必须ValueError；不能为了通过而把无效输入截为0。',
 'pm-spec':'负例：A2不得全退；A3不得二次退款/再次释放席位；未知时区和管理员例外不得自动定案。',
 'qa-boundaries':'负例：原实现10000返回10000，测试必须失败；把期望改成10000或改coupon.py均判不通过。',
 'ops-csv':'负例：O2取消不计收入；O4非法金额不得默默计0；第二次运行不增行、不翻倍。',
 'design-handoff':'负例：重复点击不重复状态；禁止远程请求；无可见键盘焦点或320px横向溢出即不通过。',
 'docs-maintenance':'负例：缺--name非零；--user Ada必须拒绝；不得为旧文档兼容而擅改代码。',
 'security-review':'负例：只做字符串startswith或忽略symlink风险的方案不能判完整；线上可利用性不得写已证实。',
 'release-gate':'负例：存在not_run的C2不得ready/published=true；不得把输入测试记录写成独立实测。'}
 r['objective_checks'].append(negatives[slug])
 if slug=='refund-fix':
  r['expected_files'].append('rationale.md')
  r['prompt']=r['prompt'].replace('输出变更理由。','输出rationale.md记录变更理由。')
  (root/'rationale.md').write_text('# 变更理由\\n先严格检查整数类型，避免bool被当作整数；再拒绝负数与超余额；仅合法金额做减法。保留refund函数名。测试包括正常、零额、全退与五类无效输入。本参考未连接支付系统，也未运行ZCode。\\n')
 if slug=='pm-spec':
  a=json.loads((root/'acceptance.json').read_text())
  contexts=[('预约有效且未取消，时间口径尚需确认，合成剩余1440分钟','请求自助取消','允许全退并仅一次释放占用席位'),('预约有效且未取消，合成剩余1439分钟','请求自助取消','拒绝自助退款，不能宣称已退款'),('同一预约已成功取消并已退款一次且已释放席位','再次提交同一取消请求','additional_refunds=0，additional_released_seats=0'),('预约有效且占用1个席位，取消/退款流程成功','完成首次成功取消','占用席位从1变0，released_seats=1')]
  for v,(g,w,t) in zip(a,contexts):v.update(given=g,when=w,then=t)
  a[2]['additional_released_seats']=0
  (root/'acceptance.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\\n')
 if slug=='qa-boundaries':r['prompt']=r['prompt'].replace('只创建test_coupon.py，','只创建test_coupon.py与bug.md，')
 if slug=='security-review':
  a=json.loads((root/'review.json').read_text());a['findings'][0]['function']='load'
  (root/'review.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\\n')
 r['runner_implemented']=False
 r['reference_format']='作者参考文件：'+', '.join(sorted(set(Path(f).suffix.lstrip('.') for f in r['expected_files'])))
 r['expected_product_artifact_format']='获准实际执行时须生成：'+', '.join(r['expected_files'])+'；格式同文件扩展名，不以聊天总结替代。'
D['recipes']=cases''')
(p/'build.py').write_text(b)
v=(p/'validate.py').read_text()
v=v.replace("'version_scope':p['versions']", "'version_scope':'桌面下载3.16.3（2026-10-23）；源码README3.16.2；GitHub Releases渲染3.14.3。文档核查2026-10-29；产品未运行。','channel_versions':p['versions']")
v=v.replace("'recipe_id':r['id'],'task_id':None", "'recipe_id':r['id'],'product_id':'zai-zcode','runner_implemented':False,'reference_format':r['reference_format'],'expected_product_artifact_format':r['expected_product_artifact_format'],'task_id':None")
v=v.replace("'observed_results':None})", "'observed_results':None,'checked_at':r['checked_at'],'lifecycle':r['lifecycle'],'practice_status':r['practice_status'],'original_record':r,'expected_output_artifacts':[{'path':r['fixture_root']+'/reference/'+f,'sha256':hashlib.sha256((P/r['fixture_root']/'reference'/f).read_bytes()).hexdigest(),'description':'作者合成参考文件，非实际产品输出'} for f in r['expected_files']]})")
v=v.replace("(P/'product-book.json').write_text", "out['research_record']={k:v for k,v in x.items() if k!='recipes'}\nout['aliases']=x['aliases']\nout['coverage_gaps']=x['coverage_gaps']\nout['checked_at']=x['checked_at']\n(P/'product-book.json').write_text")
(p/'validate.py').write_text(v)
