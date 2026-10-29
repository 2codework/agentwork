from pathlib import Path
import json, hashlib
P=Path(__file__).parent
D=json.loads((P.parent/'agentwork-zcode-playbooks-r1/identity.json').read_text())
D.update(status='multiple_distinct_products_catalogued', selected_product_id=None, aliases={'zcode':{'status':'ambiguous','product_ids':['zai-zcode','amir-hayek-zcode'],'default':None}})
D.pop('blocker'); D.pop('clarification_question'); D['ambiguity']='目录分别收录两个官方产品，不推断用户选了哪一家。'
for c in D['candidates']: c['catalogue_status']='playbooks_available' if c['product_id']=='zai-zcode' else 'identity_only_tutorials_pending'
for i,u,n in [('zai-models','configuration','模型连接与套餐边界；Coding Plan仅编码场景。'),('zai-browser','browser-use','内置浏览器限桌面；可打开本地HTML；目前不支持文件上传。'),('zai-usage','usage-stats','App Usage与Coding Plan两类用量口径不同。')]: D['sources'].append({'id':i,'url':'https://zcode.z.ai/en/docs/'+u,'note':n,'evidence':'primary','checked_at':'2026-10-29'})
D['deduplication']={'checked_at':'2026-10-29','method':'读取当前canonical JSON，全字段不区分大小写搜索zcode/z-code/z code；记录文件哈希及条目数','files':[]}
for name,key in [('agentwork','cases'),('modelatlas','nodes')]:
 f=P.parent/f'github-migration-r1/public/{name}/docs/data.json'; b=f.read_bytes(); x=json.loads(b)
 D['deduplication']['files'].append({'path':str(f),'sha256':hashlib.sha256(b).hexdigest(),'record_count':len(x[key]),'matched_records':[v.get('id') for v in x[key] if any(t in json.dumps(v).lower() for t in ['zcode','z-code','z code'])]})
common_rules='仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。'
cases=[]
def add(slug,title,role,goal,inputs,prompt,outputs,checks,rubric,recovery,extra=[]):
 root=P/'fixtures'/slug
 for group,files in [('input',inputs),('reference',outputs)]:
  for name,body in files.items():
   f=root/group/name; f.parent.mkdir(parents=True,exist_ok=True); f.write_text(body)
 r={'id':'zai-zcode-'+slug,'product_id':'zai-zcode','title':'智谱/Z.ai ZCode｜'+title,'roles':[role],'business_goal':goal,'evidence':'synthetic','product_execution':'not_run','reference_output_origin':'author_created_not_product_output','checked_at':'2026-10-29','applicable_versions':'桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。','lifecycle':'unknown','practice_status':'原创教学设计，非效果认证或行业最佳实践','fixture_root':'fixtures/'+slug,'input_files':list(inputs),'expected_files':list(outputs),'prompt':prompt+'\n'+common_rules,'official_operation_path':['完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。','在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。','粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。','在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。']+extra,'objective_checks':checks,'human_rubric':rubric,'failure_recovery':recovery,'permissions':common_rules,'cost_boundary':'练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。','privacy_boundary':'输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。','sources':['zai-agent','zai-task','zai-safety','zai-models','zai-usage']+(['zai-browser'] if extra else [])}
 cases.append(r)
add('refund-fix','开发者：修复退款金额边界','后端开发','让订单退款函数不因超额/负数产生错账；只模拟整数分。',{'refund.py':'def refund(balance_cents, requested_cents):\n    return balance_cents - requested_cents\n','README.md':'余额与申请值必须为非负整数（bool不算整数）。超余额或非法类型抛ValueError；余额100，退款30返回70。\n'},'阅读@refund.py和@README.md。修复边界，保持函数名。补test_refund.py覆盖正常、零额、刚好全退、超额、负数、浮点、布尔。不要接支付接口。输出变更理由。',{'refund.py':'def refund(balance_cents, requested_cents):\n    if type(balance_cents) is not int or type(requested_cents) is not int:\n        raise ValueError("integer cents required")\n    if balance_cents < 0 or requested_cents < 0 or requested_cents > balance_cents:\n        raise ValueError("invalid amount")\n    return balance_cents - requested_cents\n','test_refund.py':'import unittest\nfrom refund import refund\nclass RefundTests(unittest.TestCase):\n    def test_valid(self):\n        for a,b,c in [(100,30,70),(100,0,100),(100,100,0)]: self.assertEqual(refund(a,b),c)\n    def test_invalid(self):\n        for a,b in [(1,2),(-1,0),(1,-1),(1.0,0),(True,0)]:\n            with self.assertRaises(ValueError): refund(a,b)\n'},['在输出目录运行 python -m unittest -v；所有8个子场景均覆盖。','diff只涉及refund.py、test_refund.py与rationale.md；无网络/支付调用。'],['0-2分：规则与异常类型准确；满分覆盖bool陷阱。','0-2分：测试断言输出而非只检查无报错；总分至少3且无越权。'],['若现有环境没有Python则标blocked，不安装。','测试失败先复制traceback，按单个边界修复；不要更改需求以迎合实现。'])
add('pm-spec','产品经理：需求拆成可验收开发规格','产品经理','把含糊的预约取消规则交给研发，避免擅自决定争议项。',{'brief.md':'合成需求：预约开始前24小时及以上可全退；不足24小时不能自助退款。暂未明确时区与管理员例外。取消后释放名额。用户重复点击不能重复退款。\n'},'依据@brief.md编写spec.md和acceptance.json。只做开发规格，不冒充订单系统执行。显式列出时区与管理员权限待决；验收包含24小时等于边界、提前23小时59分、重复取消和名额释放。',{'spec.md':'# 预约取消规格\n## 已知规则\n距离开始>=24小时允许全退；更晚拒绝自助退款。成功取消释放一次名额；重复取消不重复退款。\n## 待决\n时区与夏令时口径；管理员例外与授权主体。未决前禁止生产上线。\n## 开发边界\n退款与名额状态应可追踪，失败需保留重试/人工处理状态，不假设原子成功。\n','acceptance.json':json.dumps([{'id':'A1','remaining_minutes':1440,'self_refund':True},{'id':'A2','remaining_minutes':1439,'self_refund':False},{'id':'A3','action':'repeat_cancel','additional_refunds':0},{'id':'A4','action':'successful_cancel','released_seats':1}],ensure_ascii=False,indent=2)+'\n'},['acceptance.json可解析，恰有A1-A4且A1/A2结果不同。','spec.md明确时区、管理员待决，不填假结论。'],['0-2分：Given/When/Then能让QA写测试。','0-2分：退款失败/重复请求有讨论但不偷增已批准需求；>=3通过。'],['如果模型自行选UTC，要求移到假设并保留阻塞，不把假设称已确认。','规则冲突时只列冲突及决策人，不生成生产策略。'])
add('qa-boundaries','测试：为优惠券函数建立回归集','测试工程师','让测试发现门槛比较错误，而不是机械覆盖代码。',{'coupon.py':'def payable(cents):\n    return cents - 1000 if cents > 10000 else cents\n','rules.md':'输入是非负整数分。本轮只验9999、10000、10001：满10000减1000；其余原价。不要修改实现。\n'},'读取@coupon.py与@rules.md。只创建test_coupon.py，使用unittest表驱动三个边界。运行前说明预期10000会失败。记录bug.md含期望/实际/最小复现，不能修代码或把失败改绿。',{'test_coupon.py':'import unittest\nfrom coupon import payable\nclass CouponTests(unittest.TestCase):\n    def test_boundary(self):\n        for cents,want in [(9999,9999),(10000,9000),(10001,9001)]:\n            with self.subTest(cents=cents): self.assertEqual(payable(cents),want)\n','bug.md':'# 满额边界失效\n输入10000分，期望9000，实际10000。\n复现：python -m unittest -v；10000子场景失败。\n影响：刚好达到门槛未优惠；本轮只报告，不修改coupon.py。\n'},['python -m unittest -v应非零退出，10000子场景失败；这是练习预期，不是产品失败。','coupon.py内容必须与input逐字一致。'],['0-2分：测试由业务规则而非错误实现推导。','0-2分：bug能复现且不夸大影响范围；>=3通过。'],['若全部通过，检查是否擅改源文件或错误期望，恢复input后重跑。','若导入失败，核对工作目录，不将环境失败记为业务缺陷。'])
add('ops-csv','数据运营：离线汇总订单CSV','数据运营','审计口径一致地计算已支付销售额，并隔离坏数据。',{'orders.csv':'order_id,status,amount_cents\nO1,paid,1200\nO2,cancelled,900\nO3,paid,800\nO4,paid,invalid\n','README.md':'只汇总paid且amount_cents为非负十进制整数的行。无效行进入errors.csv，取消行忽略；输出行序保留。\n'},'为@orders.csv写stdlib Python summarize.py。输出summary.json与errors.csv，坏数据不按0默默吞掉。不要用云表格、数据库或pip。脚本应在重复执行时覆盖同名输出而非追加翻倍。',{'summarize.py':'import csv,json\nfrom pathlib import Path\nrows=list(csv.DictReader(Path("orders.csv").open()))\nvalid=[]; errors=[]\nfor row in rows:\n    if row["status"] != "paid": continue\n    if not row["amount_cents"].isascii() or not row["amount_cents"].isdigit():\n        errors.append(row); continue\n    valid.append(int(row["amount_cents"]))\nPath("summary.json").write_text(json.dumps({"paid_count":len(valid),"revenue_cents":sum(valid)},sort_keys=True)+"\\n")\nwith Path("errors.csv").open("w",newline="") as f:\n    w=csv.DictWriter(f,fieldnames=["order_id","status","amount_cents"]); w.writeheader(); w.writerows(errors)\n','summary.json':'{"paid_count": 2, "revenue_cents": 2000}\n','errors.csv':'order_id,status,amount_cents\nO4,paid,invalid\n'},['运行python summarize.py两次，summary.json解析为paid_count=2,revenue_cents=2000。','errors.csv仅一条O4；原始orders.csv哈希不变。'],['0-2分：金额用整数分且不含取消订单。','0-2分：错误隔离/重复运行/输入不变均明确；>=3通过。'],['CSV列缺失应停下报告schema不符，不能猜列。','写权限失败改输出到获准的新目录，不chmod生产路径。'])
add('design-handoff','设计交接：令牌规格落地静态卡片','前端/设计协作','把设计参数落实成可评审HTML，不声称能直接编辑Figma。',{'tokens.json':'{"background":"#ffffff","text":"#14213d","accent":"#005fcc","radius_px":12,"spacing_px":16}\n','brief.md':'单页预约卡：标题周末陶艺，价格180元，预约按钮与已预约状态。键盘可聚焦按钮，点击后禁用避免重复；320px宽不溢出。不引远程资源。\n'},'按@tokens.json与@brief.md生成独立index.html。按钮用原生button和可见focus样式。点击后显示已预约并disabled，此为纯本地演示不是实际下单。附handoff.md逐条对应设计要求和人工核查项。',{'index.html':'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>预约演示</title><style>*{box-sizing:border-box}body{margin:0;padding:16px;color:#14213d;background:#fff;font:18px system-ui}.card{max-width:360px;border:1px solid #14213d;border-radius:12px;padding:16px}button{background:#005fcc;color:white;padding:12px;border:0;border-radius:12px}button:focus-visible{outline:3px solid #14213d;outline-offset:3px}</style><main class="card"><h1>周末陶艺</h1><p>180元</p><p>本地演示，不会下单</p><button id="book">预约</button><p id="state" role="status"></p></main><script>document.querySelector("#book").onclick=function(){this.disabled=true;document.querySelector("#state").textContent="已预约（演示）"}</script></html>\n','handoff.md':'# 交接\n颜色/圆角/间距对应tokens.json；页面不加载外链。\n人工：320px无横向滚动，Tab可见焦点，Enter触发后禁用并出现状态；刷新会重置演示，非真实预约。\n'},['静态检查存在lang、viewport、button、role=status、focus-visible；没有http外链。','浏览器人工在320×700、1280×800检查；Tab→Enter→重复点击：只出现一次状态，不产生网络请求。'],['0-2分：层级清楚、文本不截断。','0-2分：焦点/禁用/演示标记清楚；>=3通过且键盘路径必过。'],['如果浏览器控制禁用：Settings → Browser开启后新建任务；旧会话不沿用开关。','如果仅源码检查，不填视觉通过；人工另开页面验收。'],['本地工作区HTML右键Open in built-in browser；本任务不导入Chrome数据、不上传文件、不访问真实订单页。'])
add('docs-maintenance','技术写作：从真实CLI同步README','技术文档维护','修复文档漂移并给新同事可复制的离线例子。',{'tool.py':'import argparse\np=argparse.ArgumentParser()\np.add_argument("--name",required=True)\na=p.parse_args()\nprint("Hello, "+a.name+"!")\n','README.md':'旧说明：python tool.py --user Ada\n'},'依据@tool.py修订@README.md。先查看argparse定义，写准确命令、期望输出、漏参数报错和依赖说明。不要为迎合旧文档给代码新增--user，不修改tool.py。',{'README.md':'# 问候CLI\n依赖：Python 3标准库；无需pip，无网络。\n运行：`python tool.py --name Ada`\n输出：`Hello, Ada!`\n参数：--name必填。遗漏参数时argparse显示required错误且非零退出。\n旧--user不受支持；请迁移到--name。\n'},['python tool.py --name Ada的stdout恰为Hello, Ada!换行。','python tool.py退出码2；tool.py不变；README不再推荐--user。'],['0-2分：说明能直接复现。','0-2分：错误路径与版本边界清晰，无虚构安装依赖；>=3通过。'],['若文档与运行矛盾先保留命令/退出码，辨别python解释器和cwd。','不把本机路径或用户名写进公开示例。'])
add('security-review','安全评审：路径穿越风险与修复计划','安全/代码评审','在本地合成片段中找出越界风险，输出可追踪评审，不跑攻击。',{'download.py':'from pathlib import Path\ndef load(root,name):\n    return (Path(root)/name).read_text()\n','scope.md':'只静态审阅：name来自请求参数。允许读取root下面的普通文本文件。不得读取真实系统文件、网络探测或修改实现。\n'},'对@download.py做静态安全审阅，生成review.json与fix-plan.md。风险要引用函数/行和不受信输入到文件读取的路径，给无攻击执行的合成测试建议。不要读/etc或任何真实敏感目录。区分确认的代码缺少检查与未经验证的线上可利用性。',{'review.json':json.dumps({'findings':[{'id':'SEC-1','file':'download.py','line':3,'issue':'untrusted name is joined then read without containment validation','confidence':'code-level confirmed','production_exploitability':'not tested'}]},indent=2)+'\n','fix-plan.md':'# 修复建议（未实现）\n解析root与候选路径，检查候选仍位于root内；拒绝绝对路径与越界。考虑符号链接及TOCTOU，不能仅字符串前缀检查。\n仅在临时合成目录测试：正常a.txt、../outside.txt、绝对路径、指向外部的符号链接。当前未执行这些测试，未验证生产暴露。\n'},['review.json含SEC-1、download.py、line=3；明确production_exploitability=not tested。','download.py不变；无敏感文件读取或网络命令。'],['0-2分：源到sink路径准确，不用危言耸听替代证据。','0-2分：包含symlink/竞态残余风险与测试建议；>=3通过。'],['若Agent想读取真实敏感文件立即Reject，改为临时目录测试设计。','若输出称已修复，要求改成未实现计划并核diff。'])
add('release-gate','交付负责人：本地变更生成发布评审包','工程经理/发布协调','明确哪些变化可交付、哪些阻塞，不自动提交或部署。',{'changes.json':'[{"id":"C1","type":"fix","summary":"退款拒绝超额","tests":"pass"},{"id":"C2","type":"feature","summary":"预约卡片键盘交互","tests":"not_run"}]\n','policy.md':'所有功能必须有测试证据才可发布；not_run不是pass。产出release-notes.md和gate.json，不提交或推送。\n'},'根据@changes.json与@policy.md写发布说明和gate.json。说明面向用户，闸门面向工程；准确反映C2未测，因此整体blocked。不能把C1通过推广为全量通过，不能生成实际git提交/发布动作。',{'release-notes.md':'# 待发布草稿\n- C1：退款金额校验加强，防止超额申请；输入记录测试pass，未由本教材独立重跑。\n- C2：预约卡片键盘交互；待测试，不可标为可发布。\n当前发布被C2测试证据缺失阻塞。无部署、无推送。\n','gate.json':'{"decision":"blocked","blocking_ids":["C2"],"next_action":"execute authorized keyboard interaction tests and attach evidence","published":false}\n'},['gate.json decision=blocked, blocking_ids=[C2], published=false。','release-notes明确C1的pass来自输入记录，而非Agent独立实测。'],['0-2分：用户影响描述准确，不夸张收益。','0-2分：阻塞项、下一步与发布授权边界完整；>=3通过。'],['若报告写ready，返回policy逐条重判。','如果缺测试日志，保留not_run，不补造时间戳或截图。'])
# r3 acceptance and completeness corrections
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
  (root/'rationale.md').write_text('# 变更理由\n先严格检查整数类型，避免bool被当作整数；再拒绝负数与超余额；仅合法金额做减法。保留refund函数名。测试包括正常、零额、全退与五类无效输入。本参考未连接支付系统，也未运行ZCode。\n')
 if slug=='pm-spec':
  a=json.loads((root/'acceptance.json').read_text())
  contexts=[('预约有效且未取消，时间口径尚需确认，合成剩余1440分钟','请求自助取消','允许全退并仅一次释放占用席位'),('预约有效且未取消，合成剩余1439分钟','请求自助取消','拒绝自助退款，不能宣称已退款'),('同一预约已成功取消并已退款一次且已释放席位','再次提交同一取消请求','additional_refunds=0，additional_released_seats=0'),('预约有效且占用1个席位，取消/退款流程成功','完成首次成功取消','占用席位从1变0，released_seats=1')]
  for v,(g,w,t) in zip(a,contexts):v.update(given=g,when=w,then=t)
  a[2]['additional_released_seats']=0
  (root/'acceptance.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 if slug=='qa-boundaries':r['prompt']=r['prompt'].replace('只创建test_coupon.py，','只创建test_coupon.py与bug.md，')
 if slug=='security-review':
  a=json.loads((root/'review.json').read_text());a['findings'][0]['function']='load'
  (root/'review.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
 r['runner_implemented']=False
 r['reference_format']='作者参考文件：'+', '.join(sorted(set(Path(f).suffix.lstrip('.') for f in r['expected_files'])))
 r['expected_product_artifact_format']='获准实际执行时须生成：'+', '.join(r['expected_files'])+'；格式同文件扩展名，不以聊天总结替代。'
D['recipes']=cases
D['coverage_gaps']=['Amir Hayek Zcode仅身份/能力/版本限制已收录，尚无完整岗位手册。','未覆盖Z.ai所有历史版本、远程、Bot、MCP、插件市场和多代理配置。','CRM/ERP/邮件/日历/在线表格的原生集成未核验；相关岗位这里只做开发规格、离线数据脚本、静态原型和仓库文档，不冒充办公系统全流程。']
(P/'playbooks.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
(P/'GETTING_STARTED.md').write_text('''# 智谱/Z.ai ZCode 入门：先确认边界再开工

本章只适用 `zai-zcode`，不是 Amir Hayek Zcode。checked_at 2026-10-29。当前官方桌面分发3.16.3；文档持续更新，所有产品步骤均未实测。资料审阅≠产品运行。

1. 先由有授权的用户从官方安装页选择匹配系统与CPU的包。本文不执行安装；不建议为了运行而关闭杀毒或绕过系统信任检查。无获准可用客户端时停在资料练习。
2. 已安装用户在首次引导选择项目目录。只复制单项fixtures/input作为新工作区，不选公司仓库；reference是作者答案，勿提供给Agent。各练习相互独立。
3. 在Connect选择本人获准的Z.ai/BigModel连接；也可在输入框模型名→Manage Models管理既有通道。登录、密钥和付费由用户本人完成；本教程不代操作。Coding Plan只适用于编码场景，勿挪作批量办公推理服务。不要将密钥写入练习文件。
4. 选择Ask before changes；复杂任务先Plan。输入@引用本练习文件，再粘贴recipe提示。计划批准不代表允许推送、联网或读取工作区外目录；每次核对完整动作。
5. 用户可在工作区根维护AGENTS.md写明“不联网、不安装、不提交，先列测试”；这是项目约束提示，不是安全沙箱。这里只需要根文件，不假设嵌套规则自动合并。
6. 审核输出文件与验证命令；逐项批准只读/离线检查。查看工作区文件树，预览输出；自己的答案和reference不要求字节完全相同，但须满足业务断言与人工rubric。
7. 记录模型、客户端版本、工作区、用量前后、命令、退出码、未测项。Usage Stats区分本机App Usage与远端Coding Plan额度，不混成费用账单；金额与试用权益以账户现时页面为准。
8. 练习结束保留实际日志和diff，不把聊天说“完成”当证据。权限拒绝时缩小范围，不切Full access绕过；普通问题自动继续与权限批准不同，敏感练习可关闭Settings → General → Automatically continue questions。本批不启用Memory、远程、Bot、第三方插件或导入浏览器登录态。

## 新手恢复表
- 没有模型/额度：停在草稿，检查获准通道；不自动购买。
- 命令找不到：记录解释器缺失；不要装依赖，本练习均可先纸面审阅。
- 拒绝权限：说明原因为何，重新给更窄计划；拒绝不是“测试通过”。
- 模型漏上下文：在新任务明确@文件，重新声明限制；不要附整盘目录。
- UI标签不同：核版本与官方文档，标步骤待验证；不猜隐藏按钮。
- 重跑：重新复制input；不要覆盖真实未提交成果。代码错误可局部修，需求不明必须标未决。

官方出处：[安装](https://zcode.z.ai/en/docs/install)、[模型](https://zcode.z.ai/en/docs/configuration)、[Agent](https://zcode.z.ai/en/docs/agents)、[安全确认](https://zcode.z.ai/en/docs/safety-confirm)、[用量](https://zcode.z.ai/en/docs/usage-stats)。
''')
lines=['# AgentWork ZCode：两个独立产品目录与八项岗位手册','', '**状态：multiple_distinct_products_catalogued。generic alias zcode为ambiguous，不设默认，不推断用户选择。**','', '所有输入/参考输出为作者原创合成；product_execution=not_run。内容许可待负责人确认保持不变。仅资料和离线fixture验证；不是全部版本和全部功能全集。','', '## 身份与版本','智谱/Z.ai ZCode（zai-zcode）：桌面3.16.3；源码README 3.16.2；GitHub Releases渲染3.14.3，不能混用渠道。','Amir Hayek Zcode（amir-hayek-zcode）：0.28.0 beta，macOS Tahoe26.2+，需完整Xcode；面向Apple原生应用，未提供内置源码编辑器，外部Agent/Skill接入。仅身份卡完成，教程待补，不计入八项。','','先读GETTING_STARTED.md。fixtures各目录input是完整输入；reference是作者参考，不是产品输出。']
for r in cases:
 lines+=['','## '+r['title'],'',r['business_goal'],'','输入：`'+r['fixture_root']+'/input`；参考：`'+r['fixture_root']+'/reference`','', '### 原创任务提示','```text',r['prompt'],'```']
 for key,title in [('official_operation_path','操作路径'),('objective_checks','客观验收'),('human_rubric','人工rubric'),('failure_recovery','失败恢复')]: lines+=['','### '+title]+[str(i+1)+'. '+v for i,v in enumerate(r[key])]
 lines+=['','权限：'+r['permissions'],'','成本：'+r['cost_boundary'],'','隐私：'+r['privacy_boundary'],'','状态：未运行产品；作者参考输出。适用版本：'+r['applicable_versions'],'','来源：'+', '.join('['+s+']('+next(x['url'] for x in D['sources'] if x['id']==s)+')' for s in r['sources'])+'；checked_at 2026-10-29。']
lines+=['','## 覆盖缺口']+['- '+x for x in D['coverage_gaps']]+['','## 一手来源（16）']+['- ['+s['id']+']('+s['url']+')：'+s['note'] for s in D['sources']]
(P/'BOOK.md').write_text('\n'.join(lines)+'\n')
