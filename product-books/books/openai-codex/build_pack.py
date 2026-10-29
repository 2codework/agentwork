raise SystemExit("Historical r1 authoring source only; r2 is frozen. Do not regenerate over remediation.")
from pathlib import Path
import json, textwrap, hashlib, difflib
R=Path(__file__).resolve().parent
STAMP='2026-10-29T05:34:00Z'
def put(path,text):
 p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(textwrap.dedent(text).lstrip('\n'),encoding='utf8')
def js(path,obj): put(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
sources=[
('cli','Codex CLI','https://learn.chatgpt.com/docs/codex/cli','本地读代码、编辑、命令、codex 交互入口与检查点；不是 API CLI。'),
('ide','Codex IDE extension','https://learn.chatgpt.com/docs/codex/ide','编辑器文件/选择区上下文、本地改动审阅及云委派；集成方式因 IDE 不同。'),
('cloud','Codex Cloud','https://learn.chatgpt.com/docs/cloud','仓库与工具构成环境，独立任务工作区，审阅结果；环境设置和 GitHub 访问需要授权。'),
('app','ChatGPT desktop app','https://learn.chatgpt.com/docs/app','当前桌面入口文档；选择工作位置与项目、审阅文件。旧 Codex app 入口已重定向。'),
('pricing','Pricing','https://learn.chatgpt.com/docs/pricing','订阅计划/credits/额度与 API 计费不同；Free/Go 桌面能力受 rollout 限制，不代表各表面无限免费。'),
('auth','Authentication','https://learn.chatgpt.com/docs/auth','ChatGPT 与 API key 登录、cloud 的 ChatGPT 需求、工作区角色与本地权限分别约束。'),
('permissions','Permissions','https://learn.chatgpt.com/docs/permission-modes','sandbox 和 approvals 两层；自动审批不扩大 sandbox，版本/环境/组织策略影响可用模式。'),
('prompting','Prompting','https://learn.chatgpt.com/docs/prompting','目标、上下文、产物和边界；插件/连接可用性依赖计划与工作区。'),
('practice','Best practices','https://learn.chatgpt.com/guides/best-practices','复杂任务先计划、AGENTS.md 持久约定、测试与人工审阅。'),
]
js('sources.json',{'checked_at':STAMP,'retrieval':'official-domain web search then actual page open; bundled public manual refreshed and relevant sections read','sources':[{'id':i,'title':t,'url':u,'checked_at':STAMP,'status':'opened','claim_scope':c,'evidence_type':'official_documentation','not_evidence_of':'account-specific entitlement or successful task execution'} for i,t,u,c in sources]})
recipes=[]
def add(id,title,roles,brief,files,reference,tests,prompt,checks,rubric,recovery,minutes=20):
 base=f'recipes/{id}'
 for name,txt in files.items():put(base+'/fixture/'+name,txt)
 for name,txt in reference.items():put(base+'/reference/'+name,txt)
 put(base+'/acceptance.py',tests)
 put(base+'/prompt.md',prompt)
 patches=[]
 for name,txt in reference.items():
  old=textwrap.dedent(files.get(name,'')).lstrip('\n').splitlines(keepends=True)
  new=textwrap.dedent(txt).lstrip('\n').splitlines(keepends=True)
  patches.extend(difflib.unified_diff(old,new,fromfile='a/'+name,tofile='b/'+name))
 put(base+'/reference.patch',''.join(patches))
 rec={'id':id,'title':title,'roles':roles,'business_goal':brief,'product':'OpenAI Codex','status':'not_run','reference_provenance':'author_created_synthetic_not_codex_output','checked_at':STAMP,'recommended_surface':'CLI local (already installed and authenticated); IDE local alternative','surface_prerequisites':['Python 3.10+ available; stdlib only','authorized synthetic project copy','eligible account, selected workspace and usage budget checked by learner','no installation or credential setup performed by this package'], 'fixture_path':base+'/fixture','reference_path':base+'/reference','prompt_path':base+'/prompt.md','acceptance_path':base+'/acceptance.py','estimated_learning_minutes':minutes,'objective_checks':checks,'human_rubric':rubric,'recovery':recovery,'source_ids':['cli','ide','practice','permissions','auth','pricing'],'safety':{'allow':['read copied fixture','write specified output files in copied fixture','run provided stdlib checks after review'],'require_new_approval':['network access','dependency installation','external repository connection','publishing or pull request creation','changes outside exercise copy'],'deny':['secrets or personal session reads','production data','disable sandbox to pass tests','silently modify tests or reference answers']},'cost':{'offline_validation':'No model/API calls; existing Python only','codex_run':'not_run; may consume subscription quota/credits or API usage if learner later elects to run','limit':'one initial task and at most one targeted repair, then inspect manually; stop on quota/permission blocker'},'run_record':{'surface':None,'client_version':None,'model':None,'account_plan':None,'workspace_policy':None,'commands':[],'actual_output':None,'cost_actual':None}}
 recipes.append(rec)
 steps=f'''# {title}\n\n{brief}\n\n状态：**not_run**。reference 是作者手工编写的合成参考产物，不是 Codex 结果。\n\n## 岗位协作\n'''+''.join(f'- {r}\n' for r in roles)+f'''\n## 跟做（执行前先读根目录 HANDBOOK.md）\n1. 在你已有、获准使用的 CLI/IDE 环境复制 fixture 到新的练习目录；不要复制 reference 给被测代理。检查合成文件内容和 AGENTS.md；无真实客户/账号数据。\n2. 记录表面、客户端版本、当前模型、日期、计划及工作区策略；确认允许范围和预算。未安装/未授权则停在静态阅读，不在本包自动安装。\n3. CLI：进入练习副本并输入 `codex`，使用 `/status` 与 `/permissions` 核对当前状态；IDE：打开该副本，明确附加 prompt 指定文件，使用已启用的 Codex 对话。两者任选其一，不能把 IDE 的按钮照搬到 CLI。\n4. 发送 [原创任务 prompt](prompt.md)。先看计划/将运行命令；批准仅限副本内改动和给定离线测试；出现额外网络、密钥或系统安装请求就停止并缩小任务。\n5. 阅读改动与最终摘要，将输出留在练习副本。执行 `python /绝对路径/{base}/acceptance.py /绝对路径/练习副本`。这只能检查明确的断言，不替代下列人工 rubric。\n6. 比较 [参考 diff](reference.patch)，允许语义等价实现；不要求字面复制。记录实际命令、退出码、失败与重试、人工评分。没有运行的项保留 not_run，不能填 pass。\n\n## 客观验收\n'''+''.join(f'- {c}\n' for c in checks)+'''\n## 人工 rubric（各 0–2 分）\n'''+''.join(f'- {r}\n' for r in rubric)+'''\n通过：客观检查全部通过，人工至少 5/6 分，且无越权/泄密/伪造执行证据。任一安全硬门失败即不通过。\n\n## 失败恢复\n'''+''.join(f'- {r}\n' for r in recovery)+'''\n- 保存失败日志和差异；从原 fixture 新副本重试，不覆盖基线。若测试环境缺失，标 blocked，不声称功能失败；若输出不符，标 failed。未经批准不升级权限、不安装依赖、不连接服务。\n- 先一次任务，再最多一次针对错误的修复；没有足够额度即停止。离线测试免费于模型调用，但将来真实 Codex 运行受账户额度/计费约束。\n\n## 来源与核验\n'''+''.join(f'- [{t}]({u})（{STAMP}；仅支持产品能力/工作流，不背书本练习业务规则）\n' for i,t,u,c in sources if i in rec['source_ids'])
 put(base+'/README.md',steps)
 return rec
PRE='''import sys, pathlib, importlib.util, json, unittest
ROOT=pathlib.Path(sys.argv[1]).resolve()
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
'''
AG='''# Exercise rules
Synthetic training data only. Python standard library only. Work only inside this copy.
No network, dependency installation, credentials, external services, publication or production writes.
Preserve acceptance criteria. Report commands actually run separately from proposed commands.
'''
# 1
ship='''def fee(subtotal_cents, remote=False):
    if subtotal_cents < 0:
        raise ValueError("negative subtotal")
    base = 0 if subtotal_cents > 5000 else 500
    return base + (800 if remote else 0)
'''
add('cx01-shipping-bug','修复免邮阈值导致的客服投诉',['产品：给出满 50 元而非超过 50 元的规则；验收 49.99/50/50.01。','开发：只修 fee；QA：复核偏远附加费不受免邮影响。'],'电商订单刚好达到免邮门槛仍被收费，做最小可回滚修复。',{'AGENTS.md':AG,'shipping.py':ship,'policy.md':'币种为虚构 CNY，金额整数分；满 5000 分免基础运费；否则 500 分。偏远始终加 800 分；负数抛 ValueError。\n'},{'shipping.py':ship.replace('> 5000','>= 5000')},PRE+'''m=load('shipping')
for amount,remote,want in [(0,False,500),(4999,False,500),(5000,False,0),(5001,False,0),(5000,True,800),(4999,True,1300)]:
 assert m.fee(amount,remote)==want,(amount,remote,want)
try:m.fee(-1)
except ValueError:pass
else:raise AssertionError('negative subtotal must fail')
print('PASS: seven business boundary checks')
''','''请读取 policy.md 与 shipping.py，修复满额免邮边界。只改 shipping.py，保留函数接口、整数分计算和负值错误；不要引入库或联网。先指出导致 5000 分错误的行，给最小 patch，运行你实际能执行的边界检查，最终分开列出“已运行”与“建议运行”。若不能执行请明确 not_run，不要声称测试通过。''',['六组门槛/偏远组合值与负值异常正确','接口不变、无新依赖'],['业务：准确解释 >= 与 > 的差异（0/1/2）。','最小改动：无无关重构，保留负值与附加费（0/1/2）。','证据：给实际执行命令及结果，不捏造（0/1/2）。'],['若把偏远也免掉，回到 policy.md 将基础运费和附加费分开。','若改成浮点元金额，拒绝该 patch，恢复整数分接口。'])
# 2
price='''def discounted(cents, percent):
    if cents < 0 or not 0 <= percent <= 100:
        raise ValueError("out of range")
    return (cents * (100-percent) + 50) // 100
'''
tests='''import unittest
from pricing import discounted
class PricingTests(unittest.TestCase):
    def test_no_discount(self): self.assertEqual(discounted(123,0),123)
    def test_free(self): self.assertEqual(discounted(123,100),0)
    def test_half_up(self): self.assertEqual(discounted(1,50),1)
    def test_normal(self): self.assertEqual(discounted(199,10),179)
    def test_invalid(self):
        for cents,p in [(-1,0),(100,-1),(100,101)]:
            with self.assertRaises(ValueError): discounted(cents,p)
if __name__=='__main__': unittest.main()
'''
add('cx02-discount-tests','为促销整数舍入补测试',['QA：从金额舍入政策设计边界，不只覆盖普通折扣。','产品：确认半分向上取整；开发：不改生产代码，评估测试是否杀死回归。'],'为结算函数补可运行 unittest，避免未来重构改变半分舍入。',{'AGENTS.md':AG,'pricing.py':price,'policy.md':'cents 为非负整数，percent 为 0..100 的整数百分比。最终分四舍五入（半分向上）。非法范围 ValueError。\n'},{'test_pricing.py':tests},PRE+'''import tempfile, shutil, subprocess
assert (ROOT/'test_pricing.py').exists()
def run(folder):
 return subprocess.run([sys.executable,'-m','unittest','discover','-s','.','-p','test_pricing.py'],cwd=folder,capture_output=True,text=True,timeout=10)
r=run(ROOT); assert r.returncode==0,r.stderr
baseline=(ROOT/'pricing.py').read_text()
mutants=[baseline.replace('+ 50','+ 0'),baseline.replace('<= percent <= 100','<= percent <= 101'),baseline.replace('return (cents * (100-percent) + 50) // 100','return cents')]
for mutant in mutants:
 with tempfile.TemporaryDirectory() as d:
  p=pathlib.Path(d);shutil.copy(ROOT/'test_pricing.py',p/'test_pricing.py');(p/'pricing.py').write_text(mutant)
  assert run(p).returncode!=0,'tests missed mutant'
print('PASS: suite passes original and kills three intentional mutants')
''','''只新增 test_pricing.py，使用 unittest，不能修改 pricing.py。根据 policy.md 覆盖 0%/100% 折扣、半分向上、普通金额与三种非法范围。测试应在 python -m unittest discover -s . -p test_pricing.py 下运行。说明哪些错误实现会被抓到；不要只对当前实现做快照，不安装覆盖率工具。''',['原实现通过；三个故意错误变体必须非零退出','原 pricing.py 保持不变（另由 reviewer diff 检查）'],['边界：测试名和断言对应业务规则（0/1/2）。','独立性：无需网络/外部框架，不靠读取源代码断言（0/1/2）。','有效性：说明为何舍入、上界及漏折扣变体被抓（0/1/2）。'],['若 unittest 显示 0 tests，核对文件名与 TestCase 继承。','若某变体存活，增加针对该行为的断言，不修改变体或生产逻辑。'])
# 3
review='''def visible_invoices(invoices, tenant_id):
    return [row for row in invoices if row["status"] == "open"]
'''
report={'findings':[{'severity':'high','file':'invoices.py','line':2,'issue':'missing tenant filter','reproduction':{'tenant':'A','actual_ids':['a1','b1'],'expected_ids':['a1']},'impact':'Tenant A can see tenant B open invoice metadata.','recommendation':'Filter by both tenant_id and open status; preserve closed filtering.'}],'limitations':['Only synthetic repository reviewed; authentication outside this function is unknown.']}
add('cx03-tenant-review','审查多租户发票查询而不擅自改代码',['安全/QA：提供租户隔离契约；仅审核合成读取函数。','开发：确认调用方是否有额外权限；产品：判定跨租户信息暴露的严重性。'],'在上线前发现租户隔离回归，交付有复现依据的审查报告，不自动部署修复。',{'AGENTS.md':AG,'invoices.py':review,'invoices.json':json.dumps([{'id':'a1','tenant_id':'A','status':'open'},{'id':'b1','tenant_id':'B','status':'open'},{'id':'a2','tenant_id':'A','status':'closed'}]),'contract.md':'visible_invoices 只能返回传入 tenant_id 的 open 发票。不要修代码，仅提交 review.json，字段 findings 和 limitations。\n'},{'review.json':json.dumps(report,indent=2)+'\n'},PRE+'''data=json.loads((ROOT/'invoices.json').read_text());m=load('invoices')
assert [r['id'] for r in m.visible_invoices(data,'A')]==['a1','b1'],'review fixture changed'
r=json.loads((ROOT/'review.json').read_text()); f=r['findings'][0]
assert f['file']=='invoices.py' and f['line']==2
assert f['reproduction']['actual_ids']==['a1','b1'] and f['reproduction']['expected_ids']==['a1']
assert f['severity'] in ['high','critical'] and r['limitations']
assert (ROOT/'invoices.py').read_text()==''' + repr(review)+'''
print('PASS: reproduction, source preservation and report anchors; severity prose needs human review')
''','''这是隔离的合成代码审查。读取 contract.md、invoices.py、invoices.json，禁止修改代码。将有证据的问题写入 review.json（findings: severity,file,line,issue,reproduction{tenant,actual_ids,expected_ids},impact,recommendation；limitations）。区分已证实函数行为和未知调用方上下文；不虚构利用过程，不调用线上服务。优先报告真实隔离问题而非风格偏好。''',['复现 A 请求错误包含 b1；报告定位 invoices.py 第 2 行','原始函数未修改；报告说明未知上下文'],['准确：发现缺租户过滤而非编造 SQL 注入（0/1/2）。','可行动：建议双条件过滤且保留 closed 逻辑（0/1/2）。','校准：解释数据暴露影响，声明调用方未知（0/1/2）。'],['若只报风格，要求依据 contract.md 给输入/实际/预期。','若已修改代码，保存 diff 后从干净副本重新只审查。'])
# 4
legacy={'AGENTS.md':AG,'app.py':'from parser import parse\nfrom scoring import score\ndef process(text):\n    return score(parse(text))\n','parser.py':'def parse(text):\n    return [int(x.strip()) for x in text.split(",") if x.strip()]\n','scoring.py':'def score(values):\n    return {"count": len(values), "total": sum(values)}\n','samples.json':'["1, 2,3", "", "bad"]\n'}
arch={'entry':'app.py:3','flow':['app.process','parser.parse','scoring.score'],'examples':[{'input':'1, 2,3','output':{'count':3,'total':6}},{'input':'','output':{'count':0,'total':0}},{'input':'bad','error':'ValueError'}],'unknowns':['No caller or persistence layer supplied.'],'change_seams':[{'file':'parser.py','purpose':'input validation'},{'file':'scoring.py','purpose':'additional metrics'}]}
add('cx04-legacy-map','向新同事解释遗留批处理仓库',['新开发：需要入口、数据流和可修改位置。','产品/分析：提供样例，确认空输入含义；QA：复跑样例验证文档。'],'将三模块遗留仓库解释为可核验的交接材料，避免凭文件名猜数据库/服务架构。',legacy,{'architecture.json':json.dumps(arch,indent=2)+'\n','ONBOARDING.md':'# CSV-like scoring pipeline\n入口 app.py:3 的 process 将文本交给 parser.parse，再调用 scoring.score。\n解析器忽略空片段，把其余片段转为整数；非法文本抛 ValueError。\n空字符串是 count=0,total=0；没有数据库、网络调用或持久化代码证据。\n输入验证改 parser.py；增加统计项改 scoring.py。先补相应边界测试，再评估下游兼容性。\n'},PRE+'''sys.path.insert(0,str(ROOT));m=load('app');d=json.loads((ROOT/'architecture.json').read_text())
assert d['entry']=='app.py:3' and d['flow']==['app.process','parser.parse','scoring.score']
for ex in d['examples']:
 if 'error' in ex:
  try:m.process(ex['input'])
  except ValueError:assert ex['error']=='ValueError'
  else:raise AssertionError('missing error')
 else:assert m.process(ex['input'])==ex['output']
assert len(d['examples'])==3 and d['unknowns'] and (ROOT/'ONBOARDING.md').exists()
print('PASS: anchors and all documented examples agree with code')
''','''仅新增 ONBOARDING.md 和 architecture.json，不改三个 Python 模块。解释入口、完整调用顺序、输入格式、三个 samples 的结果/异常、可扩展位置与未知边界。JSON 字段 entry(文件:行)、flow(完整符号数组)、examples(input/output 或 error)、unknowns、change_seams。Markdown 写给入职开发和产品同事。每个事实必须由文件或执行例子支持，不要假设数据库、部署方式或性能规模。''',['入口及三段调用顺序正确','三个样例与实际 stdlib 执行一致，含空串和错误'],['可信：文件锚点准确，不虚构基础设施（0/1/2）。','可读：产品同事能理解输入输出（0/1/2）。','交接：明确扩展点、异常和未知（0/1/2）。'],['若 import 找不到 parser，先核对测试工作目录/Python 路径，不安装同名外部包。','文档和代码冲突时以合成源码及样例执行为准，并写清限制。'])
# 5
migration={'AGENTS.md':AG,'v1.json':'[{"id":"o1","amount_cents":1250},{"id":"o2","amount_cents":0}]\n','v2-contract.json':'{"required":["id","money"],"money":{"amount_cents":"nonnegative integer","currency":"CNY"},"compatibility":"v1 reader stays during transition"}\n','constraints.md':'只能规划，不改数据。保留旧读者一周；测试样本金额和笔数守恒。仅演练后人工批准才能切换；失败恢复旧读者和原始快照。\n'}
plan={'phases':['inventory','snapshot','dual_read','dry_run','approval','cutover','monitor','retire_v1'],'mapping':{'id':'id','amount_cents':'money.amount_cents','currency':'CNY'},'invariants':{'record_count':2,'sum_cents':1250},'approval_required_before':'cutover','rollback':{'trigger':'count or amount mismatch','restore':'v1 reader plus immutable snapshot'},'compatibility_days':7,'execution_status':'not_run','example_v2':[{'id':'o1','money':{'amount_cents':1250,'currency':'CNY'}},{'id':'o2','money':{'amount_cents':0,'currency':'CNY'}}]}
add('cx05-money-migration','给业务负责人写金额结构迁移计划',['产品：确认币种与一周兼容窗口，批准切换。','开发/运维：提供依赖与回滚责任；QA/分析：验证笔数、金额守恒。'],'把单个金额字段改为结构化 money 前，先制定可审计的演练与回滚计划，不操作真实数据库。',migration,{'migration-plan.json':json.dumps(plan,indent=2)+'\n','MIGRATION.md':'# 金额字段迁移：仅计划\n先清点读写调用方与负责人；保存不可变 v1 快照。新增双读兼容，旧读者保留 7 天。\n在隔离副本将 amount_cents 映射至 money.amount_cents 并加 currency=CNY，不进行浮点换算。\n演练核对 2 笔、1250 分及逐 id 一致。QA 提供差异；产品与运维批准后才能切换。\n监控计数、金额与读取失败；不一致即回滚 v1 reader 和快照；满足一周兼容及负责人验收后才退役 v1。\n真实依赖清单、RTO/RPO 和上线时间尚未提供，需补齐，未执行迁移。\n'},PRE+'''d=json.loads((ROOT/'migration-plan.json').read_text());v1=json.loads((ROOT/'v1.json').read_text())
assert d['invariants']=={'record_count':len(v1),'sum_cents':sum(x['amount_cents'] for x in v1)}
assert d['example_v2']==[{'id':x['id'],'money':{'amount_cents':x['amount_cents'],'currency':'CNY'}} for x in v1]
assert d['phases'].index('approval')<d['phases'].index('cutover')<d['phases'].index('retire_v1')
assert d['compatibility_days']==7 and d['execution_status']=='not_run' and d['rollback']['trigger'] and d['rollback']['restore']
print('PASS: conservation, mapping, approval ordering and rollback fields; feasibility remains human-reviewed')
''','''只写 MIGRATION.md 与 migration-plan.json；不要执行数据迁移。依据给定 v1、v2 契约和 constraints 写清 inventory/snapshot/dual_read/dry_run/approval/cutover/monitor/retire_v1 阶段、字段映射、守恒断言、兼容天数、回滚触发与恢复对象、尚缺信息。JSON 字段 phases,mapping,invariants{record_count,sum_cents},approval_required_before,rollback{trigger,restore},compatibility_days,execution_status,example_v2。样例不是上线结果；execution_status 必须 not_run。''',['两条记录和 1250 分守恒，v2 样例逐 id 对应','切换前批准、一周兼容、回滚字段齐全'],['完整：阶段依赖与回滚可理解（0/1/2）。','保守：不把样例当上线，不猜 SLA（0/1/2）。','业务：金额单位币种保留，不丢零值（0/1/2）。'],['若方案建议直接覆盖原数据，改为不可变快照与隔离演练。','缺少真实调用方清单/RTO 时标待确认，不替业务批准。'],30)
# 6
csv='id,region,amount_cents,status\na,north,1000,paid\nb,south,700,paid\nc,north,200,refund\na,north,1000,paid\nd,south,300,cancelled\n'
script='''import csv, json, sys

def summarize(path):
    totals={}; seen={}; duplicates=0
    with open(path,newline='',encoding='utf8') as f:
        for row in csv.DictReader(f):
            key=row['id']
            if key in seen:
                if seen[key] != row: raise ValueError('conflicting duplicate')
                duplicates+=1; continue
            seen[key]=dict(row)
            amount=int(row['amount_cents'])
            if amount<0 or row['status'] not in ('paid','refund','cancelled'): raise ValueError('invalid row')
            if row['status']=='cancelled': continue
            totals[row['region']]=totals.get(row['region'],0)+(amount if row['status']=='paid' else -amount)
    return {'net_cents':dict(sorted(totals.items())), 'duplicate_rows':duplicates}
if __name__=='__main__': print(json.dumps(summarize(sys.argv[1]),sort_keys=True))
'''
add('cx06-sales-script','从合成订单导出生成区域净额脚本',['分析：定义退款负号、重复 id 与取消口径。','运营：提供脱敏导出；QA：手算总额并提供冲突重复反例。'],'把可重复的销售口径落为 stdlib 脚本，而非仅给一句汇总数字。',{'AGENTS.md':AG,'orders.csv':csv,'policy.md':'金额正整数分；paid 加，refund 减，cancelled 忽略。完全相同的重复 id 只算一次并计 duplicate_rows。相同 id 内容冲突须 ValueError，负金额/未知状态也 ValueError。不改源 CSV。\n'},{'summarize.py':script,'expected.json':'{"net_cents":{"north":800,"south":700},"duplicate_rows":1}\n'},PRE+'''import tempfile
m=load('summarize');assert m.summarize(ROOT/'orders.csv')=={'net_cents':{'north':800,'south':700},'duplicate_rows':1}
for rows in ['x,north,1,paid\\nx,north,2,paid\\n','x,north,-1,paid\\n','x,north,1,unknown\\n']:
 with tempfile.TemporaryDirectory() as d:
  p=pathlib.Path(d)/'bad.csv';p.write_text('id,region,amount_cents,status\\n'+rows)
  try:m.summarize(p)
  except ValueError:pass
  else:raise AssertionError('invalid row accepted')
assert (ROOT/'orders.csv').read_text()=='''+repr(csv)+'''
print('PASS: totals, dedup, conflicting and invalid inputs; CSV unchanged')
''','''创建 summarize.py，公开 summarize(path) 返回 {net_cents:{region:整数分},duplicate_rows:整数}，并支持 python summarize.py orders.csv 输出 JSON。只用 Python stdlib，按 policy.md 对退款、取消、重复和冲突处理。写 expected.json 作为手算样例；不改 CSV，不接真实业务数据库。说明此处净额不是财务利润/审计报表。''',['north=800、south=700、重复 1 行','冲突重复/负值/未知状态拒绝，原 CSV 不变'],['口径：正确区分净额与利润（0/1/2）。','健壮：错误输入给明确失败，不静默吞掉（0/1/2）。','可复用：函数与 CLI 均清晰，金额全程整数（0/1/2）。'],['若重复叠加或退款加正数，先手算四个有效 id 再修。','遇到缺字段真实数据应停并补数据契约，不能默认视零。'])
# 7
html='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>合成工单队列原型</title>
<style>body{font:18px sans-serif;max-width:48rem;margin:2rem auto;padding:1rem}button,select{font:inherit;padding:.5rem}li{padding:.8rem;border-bottom:1px solid #777}:focus-visible{outline:3px solid #1264ab}</style></head>
<body><main><h1>合成工单队列</h1><p>仅本地演示，不发送、不保存客户数据。</p>
<label for="status">状态筛选</label><select id="status"><option value="all">全部</option><option value="open">待处理</option><option value="closed">已完成</option></select>
<p id="count" role="status" aria-live="polite"></p><ul id="tickets"></ul><p id="empty" hidden>没有符合条件的工单</p>
</main><script>
const rows=[{id:'T1',title:'合成退款咨询',status:'open'},{id:'T2',title:'合成物流咨询',status:'closed'}];
const select=document.querySelector('#status');
function render(){const visible=rows.filter(x=>select.value==='all'||x.status===select.value);const list=document.querySelector('#tickets');list.replaceChildren();visible.forEach(x=>{const li=document.createElement('li');li.textContent=x.id+' '+x.title+' '+x.status;list.append(li)});document.querySelector('#count').textContent=visible.length+' 条工单';document.querySelector('#empty').hidden=visible.length!==0}
select.addEventListener('change',render);render();
</script></body></html>
'''
add('cx07-triage-prototype','把客服需求变成离线产品原型',['产品：提供两条合成工单、筛选与空态需求，不能要求接入 CRM。','设计/QA：键盘可用性与空态检查；开发：审阅无外部资源和无数据发送。'],'让业务方通过单 HTML 原型讨论需求，不假装已上线完整客服系统。',{'AGENTS.md':AG,'brief.md':'制作 index.html 单文件工单原型。仅 T1 合成退款咨询 open 和 T2 合成物流咨询 closed。全部/待处理/已完成筛选，显示计数与空态。原生 label/select、可见键盘焦点、aria-live 计数；无网络/提交/持久化。空态可通过测试时临时把 rows 置空验证。\n'},{'index.html':html,'MANUAL-QA.md':'# 人工验收，尚未执行\n打开本地 index.html：默认 2 条；筛 open 仅 T1 且 1 条；closed 仅 T2 且 1 条。\n键盘 Tab 到下拉框，方向键切换，焦点清楚，屏幕阅读器读出 label 和计数变化。\n在临时测试副本将 rows 改为空数组，显示空态和 0 条；恢复后复核。\n检查窄屏 320px 不水平溢出；检查无请求与无持久化。生产用户认证、存储、工单变更都不在原型范围。\n'},PRE+'''from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
t=(ROOT/'index.html').read_text();p=P();p.feed(t)
assert any(tag=='html' and a.get('lang')=='zh-CN' for tag,a in p.tags)
assert any(tag=='label' and a.get('for')=='status' for tag,a in p.tags)
assert any(tag=='select' and a.get('id')=='status' for tag,a in p.tags)
assert any(a.get('aria-live')=='polite' for tag,a in p.tags)
assert {a.get('value') for tag,a in p.tags if tag=='option'}=={'all','open','closed'}
for forbidden in ['fetch(', 'XMLHttpRequest', 'localStorage', 'https://', 'http://', '<iframe', '<form']:
 assert forbidden not in t,forbidden
assert ':focus-visible' in t and 'T1' in t and 'T2' in t and '没有符合条件' in t
print('PASS: static structure only; JavaScript behavior and visual/accessibility QA NOT RUN')
''','''按 brief.md 制作单文件 index.html 与 MANUAL-QA.md。不能联网、不能安装、不能添加表单提交或持久化。使用原生语义元素，工单显示用 textContent 而非拼接外来 HTML。交付时区分静态结构检查与尚未执行的浏览器/键盘/屏幕阅读器验证，不声称仅靠源码检查已可访问。''',['HTML 语言、label/select 关联、三筛选值与 aria-live 存在','不包含网络/存储/提交常见入口；静态检查不证明行为'],['业务：手动确认两工单筛选、计数与空态（0/1/2；未做记未评）。','体验：320px、键盘焦点和读屏手动验证（0/1/2；未做记未评）。','范围：明确仅原型，不声称 CRM 集成/上线（0/1/2）。'],['若要真实 CRM/账户登录，先停止并另立授权/数据契约；本练习不扩展。','JS/视觉未测时标 manual_pending，不允许用静态通过替代。'],30)
# 8
ci='''name: synthetic-ci
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m unittest discover -s tests -p 'test_*.py'
        working-directory: service
'''
ci_good=ci.replace('working-directory: service','working-directory: services/billing')
add('cx08-ci-diagnosis','从合成 CI 日志定位错误工作目录',['运维/开发：提供脱敏 workflow、目录树和完整失败段。','QA：区分测试失败与找不到工作目录；产品：了解修复不改业务逻辑。'],'修复 CI 中工作目录拼写错误，不靠删除测试或放宽退出码让构建变绿。',{'AGENTS.md':AG,'.github/workflows/test.yml':ci,'ci.log':'Run python -m unittest discover -s tests -p test_*.py\nError: working directory service does not exist\nExit code: 1\n','services/billing/billing.py':'def total(items):\n    return sum(items)\n','services/billing/tests/test_billing.py':'import unittest\nfrom billing import total\nclass TestBilling(unittest.TestCase):\n    def test_total(self): self.assertEqual(total([2,3]),5)\n'}, {'.github/workflows/test.yml':ci_good,'DIAGNOSIS.md':'# CI 诊断\nci.log 明确在启动测试前因 service 不存在失败；实际模块在 services/billing。\n最小改动仅 working-directory，保留测试命令与退出码语义。\n在该目录执行 python -m unittest discover -s tests -p test_*.py 可本地检查。\n本包不触发 GitHub Actions；线上 runner、网络与 Action 版本尚未验证。\n不使用 continue-on-error、不删除测试；获准提交后仍需查看真实 CI 结果。\n'},PRE+'''import subprocess
p=ROOT/'.github/workflows/test.yml';t=p.read_text()
assert 'working-directory: services/billing' in t and 'continue-on-error' not in t
assert "python -m unittest discover -s tests -p 'test_*.py'" in t
r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py'],cwd=ROOT/'services/billing',capture_output=True,text=True,timeout=10)
assert r.returncode==0 and 'Ran 1 test' in r.stderr,r.stderr
assert (ROOT/'DIAGNOSIS.md').exists()
print('PASS: local Python test command; hosted CI NOT RUN; YAML structure checked narrowly')
''','''读取 ci.log、workflow 与 services 目录，给出失败发生在测试前还是测试内的证据。仅修 workflow 工作目录并写 DIAGNOSIS.md。不升级 Actions，不加 continue-on-error，不删除测试，不触发远程流水线。允许本地执行现有 stdlib unittest；最终分别说明本地测试结果与 GitHub Actions 未运行。''',['working-directory 正确且无吞错设置','原测试命令在实际目录发现并通过 1 测试；托管 CI 未运行'],['诊断：依据日志区分环境路径和业务断言（0/1/2）。','修复：仅必要路径变更，不掩盖错误（0/1/2）。','证据：不把本地 unittest 等同远程 CI 成功（0/1/2）。'],['若仍 0 tests，检查发现目录与文件模式；不把 0 tests 当成功。','线上失败需要新的脱敏日志；不能本地猜测权限/网络后直接放宽策略。'])
js('recipes.json',{'schema_version':1,'checked_at':STAMP,'suite':'agentwork-codex-playbooks-r1','execution_status':'not_run','recipes':recipes})
put('README.md','''# AgentWork · Codex 岗位与业务练习包 r1

这是作者整理的中文入门手册 + 8 个原创合成微型仓库/文件任务，不是 OpenAI 官方教材、认证或能力榜单。
当前全部 Codex 任务 **not_run**；只运行作者编写的 Python 标准库检查。`reference` 为作者参考答案而非代理输出。

- [入门手册与表面区别](HANDBOOK.md)
- [任务目录 JSON](recipes.json) · [官方来源](sources.json) · [结构契约](schema.json)
- [本地去重与来源说明](RESEARCH.md) · [验证边界](VALIDATION.md)
- 每项 `fixture` 是原始输入；`reference` 仅包含预期新增/修改文件；`reference.patch` 供审阅。
- 离线复验：`python validate_pack.py`。临时目录合成参考结果并运行 stdlib 检查，不运行 Codex/LLM/API/SDK。
- 如未来实测，请复制 fixture，不给被测代理 reference；记录表面/版本/模型/计划/策略、实际命令及成本，不覆盖此基线。
- 尚未执行浏览器、屏幕阅读器或托管 CI；不得把静态验证称为端到端成功。

本包不修改 canonical、license 或发布状态。既有 AgentWork 的 license-pending 不是新授权；本包仅为待审阅内容候选。
''')

# Add input integrity checks after writing task-specific validators.
for r in recipes:
 f=R/r['fixture_path'];e=R/r['reference_path'];t=R/r['acceptance_path']
 expected={str(x.relative_to(f)):hashlib.sha256(x.read_bytes()).hexdigest() for x in f.rglob('*') if x.is_file() and not (e/x.relative_to(f)).exists()}
 allowed=set(expected)|{str(x.relative_to(f)) for x in f.rglob('*') if x.is_file()}|{str(x.relative_to(e)) for x in e.rglob('*') if x.is_file()}
 prefix="import pathlib, sys, hashlib\nsys.dont_write_bytecode=True\n_gate_root=pathlib.Path(sys.argv[1]).resolve()\n"+f"_preserved={expected!r}\n_allowed={allowed!r}\n"+"for _name,_digest in _preserved.items():\n    assert hashlib.sha256((_gate_root/_name).read_bytes()).hexdigest()==_digest,('protected input modified',_name)\nfor _p in _gate_root.rglob('*'):\n    if _p.is_file() and '__pycache__' not in _p.parts and '.git' not in _p.parts:\n        assert str(_p.relative_to(_gate_root)) in _allowed,('unexpected file',str(_p.relative_to(_gate_root)))\n"
 t.write_text(prefix+t.read_text())
