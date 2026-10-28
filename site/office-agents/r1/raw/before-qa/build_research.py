import json,pathlib,hashlib,subprocess
P=pathlib.Path('office-agent-research-r1'); checked='2026-10-28'
sources=[]
def S(id,title,url,version='未显示文档发布日期/版本；以访问日为准',evidence='official_documentation'):
 sources.append(dict(id=id,title=title,url=url,source_checked_date=checked,document_version_or_date=version,evidence=evidence));return id
S('zap-migrate','Migrating from Agents to AI by Zapier','https://help.zapier.com/hc/en-us/articles/47402591569805-Migrating-from-Agents-to-AI-by-Zapier','页面显示 Updated 26 days ago；不推算精确发布日期')
S('zap-approval','Add approval steps to your agent’s instructions','https://help.zapier.com/hc/en-us/articles/41776074420493-Add-approval-steps-to-your-agent-s-instructions')
S('zap-build','Build an agent in Zapier Agents','https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents')
S('make-new','Meet the new Make AI Agents app','https://help.make.com/meet-the-new-make-ai-agents-app','New；页面标记 open beta')
S('make-create','Create your first AI agent','https://help.make.com/create-your-first-ai-agent','Make AI Agent (New)；滚动文档')
S('rel-intro','Relevance AI Introduction','https://relevanceai.com/docs/get-started/introduction')
S('rel-approval','Approval Mode','https://relevanceai.com/docs/build/agents/give-your-agent-tasks/approval-mode')
S('notion-custom','Custom Agents in Notion','https://www.notion.com/help/custom-agents')
S('notion-perm','Custom Agents sharing and permissions','https://www.notion.com/en-gb/help/custom-agents-sharing-and-permissions')
S('glean-tools','Overview and concepts: tools','https://docs.glean.com/agents/actions/introduction-to-actions',evidence='official_documentation_search_full_text; direct_open_empty')
S('copilot-tools','Add tools to custom agents','https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent')
S('copilot-auth','Configure user authentication for tools','https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication')
S('omni','Using Omni AI in Airtable','https://support.airtable.com/articles/1744327578-using-omni-ai-in-airtable','Last updated October 26, 2026')
S('lindy-home','What is Lindy?','https://docs.lindy.ai/')
S('lindy-integrations','Integrations','https://docs.lindy.ai/integrations/overview')
S('lindy-drafts','Email Drafting','https://docs.lindy.ai/features/inbox-management/email-drafting')
S('n8n-hitl','Human-in-the-loop for tools','https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md','旧 URL advanced-ai/human-in-the-loop-tools/ 重定向到此页')
S('rovo-slack','Use the Rovo app for Slack','https://support.atlassian.com/rovo/docs/using-the-atlassian-rovo-slack-app/')
R=[]
def A(id,name,kind,lifecycle,tasks,permission,confirm,steps,example,limits,src,access='需授权账户/连接；具体套餐、区域可用性及价格未核验',unknown=None):
 R.append(dict(id=id,name=name,entity_type=kind,is_model=False,domain='office_agent_system',lifecycle=lifecycle,source_checked_date=checked,proof_level='documentation-only',runtime_verified=False,global_completeness=False,supported_workflows=tasks,permission_boundary=permission,confirmation_boundary=confirm,access_and_pricing=access,human_supervised_steps=steps,synthetic_example=example,limitations=limits,source_ids=src,unknowns=unknown or ['未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测'],integration_status='raw_research_not_canonical'))
A('office-ai-by-zapier','AI by Zapier（agentic step）','hosted_workflow_agent_service','现行迁移目标；不等于底层模型', ['在 Zap 中进行分类、推理、工具调用和结构化输出'], '通过连接账户操作；管理员可禁用 agentic/tool calling。', '逐工具 Require approval before running 需主动开启；默认不暂停确认。发布审批与运行审批不同。', ['先列读写工具并使用虚构输入','写工具开启逐次审批，检查输出字段','人工比较工具参数后决定是否运行；上线另行授权'], {'input':'虚构工单 T-41：要求修改收货备注','expected':'分类 delivery_change；提出改动，不自动对真实订单写入'}, ['迁移不拆分工具为独立 Zap 步骤','旧 Agent 与新 Zap 同时启用可能重复执行','全 Zap 测试也消耗任务；本研究不测试'], ['zap-migrate'], '任务制计费已记录；金额与账户额度未核验')
A('office-zapier-agents','Zapier Agents','hosted_agent_service','迁移中历史入口；官方未给停用日期，不能标成已关闭', ['按触发器或交互执行连接应用动作','查询连接知识源'], '只使用提供给 Agent 的工具及账户连接；不得把指令视为连接权限。', '旧文档支持在指令中加入暂停征求确认，并配置消息动作；不把自然语言指令当独立强制安全控制。', ['盘点旧 Agent 触发器、知识源与工具','用合成工单写暂停检查点','评估迁移差异，保留人工审批；不直接双跑生产'], {'input':'虚构客户问发票状态','expected':'查阅样例状态，生成待审核回复'}, ['当前迁移目标为 AI by Zapier','不能假设旧版全部功能迁移等价'], ['zap-build','zap-approval','zap-migrate'])
A('office-make-ai-agents-new','Make AI Agents (New)','hosted_workflow_agent_platform','New，官方发布页仍标 open beta；不要混入旧版教程', ['在场景中选择模块、子场景、MCP 与子 Agent 工具','处理输入文件并返回结构化结果'], 'Agent 只能调用启用的工具；工具背后连接权限须单独审查。', '已读文档未证明统一逐工具强制审批开关；采用禁用写工具、先输出建议、人工另行执行的教学边界。', ['新建未启用的场景并填写合成请求','添加只读工具和少量知识文件，禁用写工具','检查执行步骤与结构化结果，人工处理后续变更'], {'input':'三条虚构项目进展记录','expected':'输出 risk、owner、next_action，缺失 owner 标未知'}, ['聊天测试会调用工具，不是无副作用预览','子 Agent 嵌套只支持一层','知识上传也会消耗 tokens'], ['make-new','make-create'], '官方称所有套餐可用 Make AI Provider，自带 provider 连接需付费套餐；金额未核验', ['通用审批机制未由本次来源确认','未实测；open beta 功能与价格会变化'])
A('office-relevance-ai','Relevance AI Agents','low_no_code_agent_platform','当前官方文档可访问；版本未标', ['构建工具驱动的 Agent 与多 Agent 团队','分类、查询与受监督的跨工具工作流'], '为 Agent 显式连接工具；各工具账户权限和审批模式需要分别设置。', '每个工具可设 Autopilot 或 Human-in-the-Loop；后者要求显式批准才能使用。', ['设计虚构供应商问题分流 Agent','连接最少工具，将写入工具设 HITL','检查拟执行工具并批准/拒绝，再审结果'], {'input':'虚构采购请求 Q-12 缺少数量','expected':'要求补充数量，不建立真实采购单'}, ['审批配置不等于结果正确或合规认证','不同界面版本命名需现场核对'], ['rel-intro','rel-approval'])
A('office-notion-custom-agents','Notion Custom Agents','workspace_agent_service','当前文档；与按需 Notion Agent 分开', ['按触发器、计划进行页面/数据库整理','跨授权 Notion 与连接工具生成团队更新'], '拥有独立资源权限，不继承触发者权限；使用者可能经 Agent 读取或编辑自己无直接访问权的资源。', '已读来源未证明所有写入逐次确认；授权资源和共享 Agent 本身都是风险边界。教学只授只读源，产出由人审核。', ['创建仅自己可用的 Agent','Tools and Access 只加入虚构项目页，先不启用计划','运行整理要求，检查输出及分享对象后人工保存/共享'], {'input':'虚构 A/B 项目页各两项状态','expected':'周报草稿，未注明日期的项列为待核实'}, ['共享 Agent 可扩大可见性；删掉个人页面权限不一定阻止经 Agent 获取','不能用当前用户权限继承的表述'], ['notion-custom','notion-perm'])
A('office-glean-workflow-agents','Glean Workflow agents','enterprise_workflow_agent_service','当前官方工具文档；与 Assistant、Autonomous Agents 分开', ['检索上下文后创建工单/文档并分享链接','查询指标并组织项目更新'], '管理员启用并认证工具，构建者选择流程工具；依赖配置的应用身份权限。', '文档中个人 Always allow/Needs approval 设置明确适用于 Glean Assistant；不能直接宣称覆盖所有 Workflow/Autonomous Agent。流程写入审批需具体配置核验。', ['管理员确认允许的只读工具和身份','构建读取样例进展→产出草稿流程','不启用未核验的写步骤；人工检查后写入目标系统'], {'input':'虚构 Jira 事项 DEMO-1 与状态说明','expected':'项目更新草稿和建议跟进项'}, ['索引 connector 不等于实时执行 tool','个人 Assistant 审批设置不能外推为自动 Agent 默认'], ['glean-tools'], unknown=['Workflow agent 各触发方式的强制审批边界需专项核验','价格、地区与租户功能未知；未实测'])
A('office-copilot-studio','Microsoft Copilot Studio custom agents','low_code_agent_platform','当前 custom agent 工具文档；不是 Copilot 模型', ['通过配置的知识、工具和主题编排业务对话','将请求路由到连接器或工作流'], '工具可用 End user 或 Maker-provided 身份，不能假定总是用户权限；管理员治理另计。', 'Ask the end user before running 默认 No；必须为敏感工具显式开启。该选项描述的是终端用户聊天体验。', ['为虚构服务申请建立 Agent 和输入字段','选择最终用户身份并开启敏感工具确认','核对申请对象和字段，拒绝错误参数；异步触发另核验'], {'input':'虚构设备支持申请，部门未填','expected':'补问部门后生成工单建议，确认前不提交'}, ['聊天确认不能自动外推到所有自治触发','Maker-provided 凭证可能扩大执行身份范围'], ['copilot-tools','copilot-auth'])
A('office-airtable-omni','Airtable Omni','workspace_agent_assistant','官方更新 2026-10-26', ['多步整理/修改数据与构建应用','分析文档、解释自动化失败'], '镜像交互用户在 base/interface 的权限，字段和表权限仍约束修改。', '删除表/interface 页面前确认；读过外部网页内容后修改 base 前确认。接口发布及开启 automation 留给用户；不能宣称所有写入都确认。', ['使用隔离的虚构项目 base','请 Omni 汇总数据并说明拟改字段','人核验记录和权限，再决定变更；不要自动发布共享界面'], {'input':'虚构任务 A 已完成、B 延迟两日','expected':'状态汇总，B 标为需人工跟进'}, ['不能配置 workspace/base 权限或导出数据','撤销有范围限制，不能依赖全量回滚'], ['omni'], '所有套餐可访问；完整使用需要 AI credits 与启用 AI；金额未核验')
A('office-lindy','Lindy','hosted_personal_team_agent_service','当前文档；旧 Academy action-configuration 已重定向', ['收件箱草稿、会议准备、团队研究和例行任务'], '个人连接仅本人用；团队连接以被共享账户身份工作。连接开通时其动作整体启用。', '集成 guardrails 只覆盖共享 Slack 线程写操作；不覆盖读取、Web chat、Slack DM、iMessage/SMS。个人 Email Drafting 例程另规定草稿由用户审改发送。', ['选择 Email Drafting 例程而非泛化发送任务','用虚构来信确定语气和升级规则','审核 drafts 文件夹中收件人、事实和正文；由人发送'], {'input':'虚构客户希望改期，未给时区','expected':'草稿询问时区，不直接发送会议邀请'}, ['不能把共享线程 guardrail 说成全渠道安全网','集成级规则不能区分同一集成的不同账户'], ['lindy-home','lindy-integrations','lindy-drafts'])
A('office-n8n-ai-agent','n8n AI Agent node + human review','workflow_orchestration_component','当前滚动文档；运行软件版本未核验', ['工具驱动工作流，选择性人工审批','处理分类结果并拟议写入操作'], '节点使用配置的凭证；须最小化工具与审批渠道权限。', '工具接到 human review 节点后执行前暂停；Approve 用模型给定输入执行，Deny 取消该操作并通知 AI；只保护接入的工具。', ['创建合成工单输入及 Agent 节点','将写工具接入 human review 并展示 tool name/parameters','人工拒绝错误目标，确认拒绝不写入后再评估上线'], {'input':'虚构 T-9 建议状态 resolved 但证据不足','expected':'审核者拒绝，目标状态不变'}, ['批准输入不等于输入正确','必须明确拒绝后的行为；真实暂停/取消未实测'], ['n8n-hitl'], '需要配置 n8n、模型及工具/审批渠道连接；部署方式、许可及总成本未核验')
A('office-rovo-slack','Atlassian Rovo agents in Slack','workspace_agent_client_surface','当前 Slack app 文档；不等同底层模型', ['在 Slack 检索与整理上下文','拟创建/更新 Jira、发布 Confluence 或调用连接工具'], 'DM/私密回复按用户权限；公开回复按 Rovo 自身访问范围；行动按用户权限。', '创建/更新 Jira、发布 Confluence 或第三方动作前预览并要求确认；即使公开线程，动作向用户私下确认。', ['先在私密回复中请求虚构事项摘要','要求起草 DEMO 工单，核对项目与负责人','确认正确动作后才允许提交；公开分享另行检查'], {'input':'虚构入职事项：测试账户未开通','expected':'工单预览，负责人缺失时先补问'}, ['更改 Agent 权限不会撤回已发回复','Slack 语义不能外推到所有 Rovo 客户端'], ['rovo-slack'])
baselines=[]
for repo,rel,field in [('agentwork','site/data.json','cases'),('modelatlas','dist/data.json','nodes')]:
 root=pathlib.Path('github-migration-r1/public')/repo;p=root/rel;d=json.loads(p.read_text());raw=p.read_bytes()
 baselines.append(dict(repository='https://github.com/2codework/'+repo,local_path=str(p),head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),remote_main_verified_via='GitHub connector branches/main at 2026-10-28 20:41 UTC',count=len(d[field]),sha256=hashlib.sha256(raw).hexdigest()))
 # Entity labels are checked, not arbitrary mentions.
 labels=[]
 def walk(o):
  if isinstance(o,dict):
   labels.extend(str(o[k]).lower() for k in ('id','name','title') if k in o)
   for v in o.values():walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(d)
 for r in R:
  r.setdefault('dedup_checks',{})[repo]={'named_entity_title_match':any(r['name'].lower()==x for x in labels)}
unknowns={'scope':'11 个命名实体/版本/客户端面，10 个供应商/平台家族；不是全球全量，也不是 11 个基础模型。','execution':'只浏览官方资料与检查现有公开仓库对应本地数据；没有登录产品、付费调用、发送、创建账户或运行 Agent。','source_limits':['Glean 直接打开正文为空；官方搜索索引完整文本可读，单独标记证据来源','Lindy .md 路由内容类型不受浏览工具支持；正常 HTML 路由成功，不再使用旧 Academy 教程','GitHub 网页浏览 cache miss；官方 GitHub connector 成功核实 main SHA 与本地相同。'],'global_unknowns':['各地区实际可用性、企业合同、税费、全部套餐和实付价格未核验','没有实际部署效果、精度、节省时间或 ROI 证据','平台版本滚动更新；集成动作和权限须在授权后重新验证'],'future_admission':'先审计每一条命名实体和权限条件；AW 可收为合成练习，MA 应以 service/platform/client/component 类型纳入，不能登记为 model checkpoint。'}
obj={'schema_version':'office-agent-research.r1','source_checked_date':checked,'status':'raw_research_not_canonical','records':R,'sources':sources,'baselines':baselines,'unknowns':unknowns}
(P/'office-agents.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(P/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
(P/'unknowns.json').write_text(json.dumps(unknowns,ensure_ascii=False,indent=2)+'\n')
md=['# 办公 Agent 系统：原始研究 r1','', '检查日：2026-10-28。11 个命名实体/版本/客户端面，10 个平台家族。全部为 documentation-only；未实机复现，非全球全量、非成效排名。服务、平台、组件、客户端面与底层模型严格分开。','', '## 先看关键差异','- Zapier Agents 正向 AI by Zapier 迁移，尚无关闭日期；新工具默认不逐次确认。','- Notion Custom Agents 使用独立权限，不能写成继承触发者权限。','- Lindy 的共享 Slack 写入 guardrails 不是全渠道保护；个人草稿例程另有发送边界。','- Make New 的聊天测试会调用工具，不是安全的静态预览。','- Copilot Studio 的聊天工具确认默认关闭；Glean Assistant 的个人审批设置不能外推为所有自治 Agent 的保证。','', '## 基线与去重']
for b in baselines:md.append(f"- {b['repository']}：`{b['head']}`，{b['count']} 条；connector 已核实 remote main。基线 SHA256 `{b['sha256']}`。")
for r in R:
 md += ['', '## '+r['name'],f"- 类型：{r['entity_type']}；不是模型。状态：{r['lifecycle']}。",'- 文档支持：'+'；'.join(r['supported_workflows'])+'。','- 权限：'+r['permission_boundary'],'- 确认：'+r['confirmation_boundary'],'- 接入/价格：'+r['access_and_pricing'],'- 人监督练习（原创合成，不是实测）：']
 md += [f'  {i+1}. {step}' for i,step in enumerate(r['human_supervised_steps'])]
 md += ['- 合成输入：'+r['synthetic_example']['input']+'；期望：'+r['synthetic_example']['expected'],'- 局限：'+'；'.join(r['limitations']),'- 未知：'+'；'.join(r['unknowns']),'- 来源：'+'；'.join('['+s['title']+']('+s['url']+')' for s in sources if s['id'] in r['source_ids'])]
md+=['','## 准入建议','AgentWork：逐条合成案例进入候选审稿；ModelAtlas：以服务/平台/组件/客户端面纳入，不扩张为模型谱系。上述资料并未证明最佳实践或真实成效。','', '## 未知与资料限制',*['- '+x for x in unknowns['source_limits']+unknowns['global_unknowns']]]
(P/'office-agents.zh.md').write_text('\n'.join(md)+'\n')
# Original learning cases, separate from product records and canonical schema.
cases=[{'id':r['id']+'-lab','system_id':r['id'],'title':r['name']+'：人监督合成练习','proof_level':'documentation-only','synthetic':True,'steps':r['human_supervised_steps'],'input':r['synthetic_example']['input'],'expected':r['synthetic_example']['expected'],'acceptance':['没有把未知信息填成事实','敏感写入不越过该产品实际支持的批准边界','保留权限身份、目标、参数、审批及结果证据；未运行则标 never-run'],'source_ids':r['source_ids']} for r in R]
(P/'raw-cases.json').write_text(json.dumps({'schema_version':'office-agent-raw-cases.r1','cases':cases},ensure_ascii=False,indent=2)+'\n')
print('wrote',len(R),'entities',len(sources),'sources',len(cases),'raw cases')
