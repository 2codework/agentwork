# 办公 Agent 系统：原始研究 r1

检查日：2026-10-28。11 个命名实体/版本/客户端面，10 个平台家族。全部为 documentation-only；未实机复现，非全球全量、非成效排名。服务、平台、组件、客户端面与底层模型严格分开。

## 先看关键差异
- Zapier Agents 正向 AI by Zapier 迁移，尚无关闭日期；新工具默认不逐次确认。
- Notion Custom Agents 使用独立权限，不能写成继承触发者权限。
- Lindy 的共享 Slack 写入 guardrails 不是全渠道保护；个人草稿例程另有发送边界。
- Make New 的聊天测试会调用工具，不是安全的静态预览。
- Copilot Studio 的聊天工具确认默认关闭；Glean Assistant 的个人审批设置不能外推为所有自治 Agent 的保证。

## 基线与去重
- https://github.com/2codework/agentwork：`672dfec4f95bbb2ee224b287dda0293208b1dc50`，106 条；connector 已核实 remote main。基线 SHA256 `5550f8550d8bc42c610a1004e2bab4e789144edc65166aa7a747c92cf037c867`。
- https://github.com/2codework/modelatlas：`d4bd8c894b222bbad99ca9de21677985e127eff1`，200 条；connector 已核实 remote main。基线 SHA256 `cb4f49577746b067f1eef10dff3e6d18a6d2c6517eb0a2157bc5c94ef58c5da3`。

## AI by Zapier（agentic step）
- 类型：hosted_workflow_agent_service；不是模型。状态：现行迁移目标；不等于底层模型。
- 文档支持：在 Zap 中进行分类、推理、工具调用和结构化输出。
- 权限：通过连接账户操作；管理员可禁用 agentic/tool calling。
- 确认：逐工具 Require approval before running 需主动开启；默认不暂停确认。发布审批与运行审批不同。
- 接入/价格：任务制计费已记录；金额与账户额度未核验
- 人监督练习（原创合成，不是实测）：
  1. 先列读写工具并使用虚构输入
  2. 写工具开启逐次审批，检查输出字段
  3. 人工比较工具参数后决定是否运行；上线另行授权
- 合成输入：虚构工单 T-41：要求修改收货备注；期望：分类 delivery_change；提出改动，不自动对真实订单写入
- 局限：迁移不拆分工具为独立 Zap 步骤；旧 Agent 与新 Zap 同时启用可能重复执行；全 Zap 测试也消耗任务；本研究不测试
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Migrating from Agents to AI by Zapier](https://help.zapier.com/hc/en-us/articles/47402591569805-Migrating-from-Agents-to-AI-by-Zapier)

## Zapier Agents
- 类型：hosted_agent_service；不是模型。状态：迁移中历史入口；官方未给停用日期，不能标成已关闭。
- 文档支持：按触发器或交互执行连接应用动作；查询连接知识源。
- 权限：只使用提供给 Agent 的工具及账户连接；不得把指令视为连接权限。
- 确认：旧文档支持在指令中加入暂停征求确认，并配置消息动作；不把自然语言指令当独立强制安全控制。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 盘点旧 Agent 触发器、知识源与工具
  2. 用合成工单写暂停检查点
  3. 评估迁移差异，保留人工审批；不直接双跑生产
- 合成输入：虚构客户问发票状态；期望：查阅样例状态，生成待审核回复
- 局限：当前迁移目标为 AI by Zapier；不能假设旧版全部功能迁移等价
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Migrating from Agents to AI by Zapier](https://help.zapier.com/hc/en-us/articles/47402591569805-Migrating-from-Agents-to-AI-by-Zapier)；[Add approval steps to your agent’s instructions](https://help.zapier.com/hc/en-us/articles/41776074420493-Add-approval-steps-to-your-agent-s-instructions)；[Build an agent in Zapier Agents](https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents)

## Make AI Agents (New)
- 类型：hosted_workflow_agent_platform；不是模型。状态：New，官方发布页仍标 open beta；不要混入旧版教程。
- 文档支持：在场景中选择模块、子场景、MCP 与子 Agent 工具；处理输入文件并返回结构化结果。
- 权限：Agent 只能调用启用的工具；工具背后连接权限须单独审查。
- 确认：已读文档未证明统一逐工具强制审批开关；采用禁用写工具、先输出建议、人工另行执行的教学边界。
- 接入/价格：官方称所有套餐可用 Make AI Provider，自带 provider 连接需付费套餐；金额未核验
- 人监督练习（原创合成，不是实测）：
  1. 新建未启用的场景并填写合成请求
  2. 添加只读工具和少量知识文件，禁用写工具
  3. 检查执行步骤与结构化结果，人工处理后续变更
- 合成输入：三条虚构项目进展记录；期望：输出 risk、owner、next_action，缺失 owner 标未知
- 局限：聊天测试会调用工具，不是无副作用预览；子 Agent 嵌套只支持一层；知识上传也会消耗 tokens
- 未知：通用审批机制未由本次来源确认；未实测；open beta 功能与价格会变化
- 来源：[Meet the new Make AI Agents app](https://help.make.com/meet-the-new-make-ai-agents-app)；[Create your first AI agent](https://help.make.com/create-your-first-ai-agent)

## Relevance AI Agents
- 类型：low_no_code_agent_platform；不是模型。状态：当前官方文档可访问；版本未标。
- 文档支持：构建工具驱动的 Agent 与多 Agent 团队；分类、查询与受监督的跨工具工作流。
- 权限：为 Agent 显式连接工具；各工具账户权限和审批模式需要分别设置。
- 确认：每个工具可设 Autopilot 或 Human-in-the-Loop；后者要求显式批准才能使用。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 设计虚构供应商问题分流 Agent
  2. 连接最少工具，将写入工具设 HITL
  3. 检查拟执行工具并批准/拒绝，再审结果
- 合成输入：虚构采购请求 Q-12 缺少数量；期望：要求补充数量，不建立真实采购单
- 局限：审批配置不等于结果正确或合规认证；不同界面版本命名需现场核对
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Relevance AI Introduction](https://relevanceai.com/docs/get-started/introduction)；[Approval Mode](https://relevanceai.com/docs/build/agents/give-your-agent-tasks/approval-mode)

## Notion Custom Agents
- 类型：workspace_agent_service；不是模型。状态：当前文档；与按需 Notion Agent 分开。
- 文档支持：按触发器、计划进行页面/数据库整理；跨授权 Notion 与连接工具生成团队更新。
- 权限：拥有独立资源权限，不继承触发者权限；使用者可能经 Agent 读取或编辑自己无直接访问权的资源。
- 确认：已读来源未证明所有写入逐次确认；授权资源和共享 Agent 本身都是风险边界。教学只授只读源，产出由人审核。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 创建仅自己可用的 Agent
  2. Tools and Access 只加入虚构项目页，先不启用计划
  3. 运行整理要求，检查输出及分享对象后人工保存/共享
- 合成输入：虚构 A/B 项目页各两项状态；期望：周报草稿，未注明日期的项列为待核实
- 局限：共享 Agent 可扩大可见性；删掉个人页面权限不一定阻止经 Agent 获取；不能用当前用户权限继承的表述
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Custom Agents in Notion](https://www.notion.com/help/custom-agents)；[Custom Agents sharing and permissions](https://www.notion.com/en-gb/help/custom-agents-sharing-and-permissions)

## Glean Workflow agents
- 类型：enterprise_workflow_agent_service；不是模型。状态：当前官方工具文档；与 Assistant、Autonomous Agents 分开。
- 文档支持：检索上下文后创建工单/文档并分享链接；查询指标并组织项目更新。
- 权限：管理员启用并认证工具，构建者选择流程工具；依赖配置的应用身份权限。
- 确认：文档中个人 Always allow/Needs approval 设置明确适用于 Glean Assistant；不能直接宣称覆盖所有 Workflow/Autonomous Agent。流程写入审批需具体配置核验。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 管理员确认允许的只读工具和身份
  2. 构建读取样例进展→产出草稿流程
  3. 不启用未核验的写步骤；人工检查后写入目标系统
- 合成输入：虚构 Jira 事项 DEMO-1 与状态说明；期望：项目更新草稿和建议跟进项
- 局限：索引 connector 不等于实时执行 tool；个人 Assistant 审批设置不能外推为自动 Agent 默认
- 未知：Workflow agent 各触发方式的强制审批边界需专项核验；价格、地区与租户功能未知；未实测
- 来源：[Overview and concepts: tools](https://docs.glean.com/agents/actions/introduction-to-actions)

## Microsoft Copilot Studio custom agents
- 类型：low_code_agent_platform；不是模型。状态：当前 custom agent 工具文档；不是 Copilot 模型。
- 文档支持：通过配置的知识、工具和主题编排业务对话；将请求路由到连接器或工作流。
- 权限：工具可用 End user 或 Maker-provided 身份，不能假定总是用户权限；管理员治理另计。
- 确认：Ask the end user before running 默认 No；必须为敏感工具显式开启。该选项描述的是终端用户聊天体验。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 为虚构服务申请建立 Agent 和输入字段
  2. 选择最终用户身份并开启敏感工具确认
  3. 核对申请对象和字段，拒绝错误参数；异步触发另核验
- 合成输入：虚构设备支持申请，部门未填；期望：补问部门后生成工单建议，确认前不提交
- 局限：聊天确认不能自动外推到所有自治触发；Maker-provided 凭证可能扩大执行身份范围
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Add tools to custom agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent)；[Configure user authentication for tools](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication)

## Airtable Omni
- 类型：workspace_agent_assistant；不是模型。状态：官方更新 2026-10-26。
- 文档支持：多步整理/修改数据与构建应用；分析文档、解释自动化失败。
- 权限：镜像交互用户在 base/interface 的权限，字段和表权限仍约束修改。
- 确认：删除表/interface 页面前确认；读过外部网页内容后修改 base 前确认。接口发布及开启 automation 留给用户；不能宣称所有写入都确认。
- 接入/价格：所有套餐可访问；完整使用需要 AI credits 与启用 AI；金额未核验
- 人监督练习（原创合成，不是实测）：
  1. 使用隔离的虚构项目 base
  2. 请 Omni 汇总数据并说明拟改字段
  3. 人核验记录和权限，再决定变更；不要自动发布共享界面
- 合成输入：虚构任务 A 已完成、B 延迟两日；期望：状态汇总，B 标为需人工跟进
- 局限：不能配置 workspace/base 权限或导出数据；撤销有范围限制，不能依赖全量回滚
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Using Omni AI in Airtable](https://support.airtable.com/articles/1744327578-using-omni-ai-in-airtable)

## Lindy
- 类型：hosted_personal_team_agent_service；不是模型。状态：当前文档；旧 Academy action-configuration 已重定向。
- 文档支持：收件箱草稿、会议准备、团队研究和例行任务。
- 权限：个人连接仅本人用；团队连接以被共享账户身份工作。连接开通时其动作整体启用。
- 确认：集成 guardrails 只覆盖共享 Slack 线程写操作；不覆盖读取、Web chat、Slack DM、iMessage/SMS。个人 Email Drafting 例程另规定草稿由用户审改发送。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 选择 Email Drafting 例程而非泛化发送任务
  2. 用虚构来信确定语气和升级规则
  3. 审核 drafts 文件夹中收件人、事实和正文；由人发送
- 合成输入：虚构客户希望改期，未给时区；期望：草稿询问时区，不直接发送会议邀请
- 局限：不能把共享线程 guardrail 说成全渠道安全网；集成级规则不能区分同一集成的不同账户
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[What is Lindy?](https://docs.lindy.ai/)；[Integrations](https://docs.lindy.ai/integrations/overview)；[Email Drafting](https://docs.lindy.ai/features/inbox-management/email-drafting)

## n8n AI Agent node + human review
- 类型：workflow_orchestration_component；不是模型。状态：当前滚动文档；运行软件版本未核验。
- 文档支持：工具驱动工作流，选择性人工审批；处理分类结果并拟议写入操作。
- 权限：节点使用配置的凭证；须最小化工具与审批渠道权限。
- 确认：工具接到 human review 节点后执行前暂停；Approve 用模型给定输入执行，Deny 取消该操作并通知 AI；只保护接入的工具。
- 接入/价格：需要配置 n8n、模型及工具/审批渠道连接；部署方式、许可及总成本未核验
- 人监督练习（原创合成，不是实测）：
  1. 创建合成工单输入及 Agent 节点
  2. 将写工具接入 human review 并展示 tool name/parameters
  3. 人工拒绝错误目标，确认拒绝不写入后再评估上线
- 合成输入：虚构 T-9 建议状态 resolved 但证据不足；期望：审核者拒绝，目标状态不变
- 局限：批准输入不等于输入正确；必须明确拒绝后的行为；真实暂停/取消未实测
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Human-in-the-loop for tools](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md)

## Atlassian Rovo agents in Slack
- 类型：workspace_agent_client_surface；不是模型。状态：当前 Slack app 文档；不等同底层模型。
- 文档支持：在 Slack 检索与整理上下文；拟创建/更新 Jira、发布 Confluence 或调用连接工具。
- 权限：DM/私密回复按用户权限；公开回复按 Rovo 自身访问范围；行动按用户权限。
- 确认：创建/更新 Jira、发布 Confluence 或第三方动作前预览并要求确认；即使公开线程，动作向用户私下确认。
- 接入/价格：需授权账户/连接；具体套餐、区域可用性及价格未核验
- 人监督练习（原创合成，不是实测）：
  1. 先在私密回复中请求虚构事项摘要
  2. 要求起草 DEMO 工单，核对项目与负责人
  3. 确认正确动作后才允许提交；公开分享另行检查
- 合成输入：虚构入职事项：测试账户未开通；期望：工单预览，负责人缺失时先补问
- 局限：更改 Agent 权限不会撤回已发回复；Slack 语义不能外推到所有 Rovo 客户端
- 未知：未登录核验、未执行真实任务；吞吐、质量、成本及权限实现未实测
- 来源：[Use the Rovo app for Slack](https://support.atlassian.com/rovo/docs/using-the-atlassian-rovo-slack-app/)

## 准入建议
AgentWork：逐条合成案例进入候选审稿；ModelAtlas：以服务/平台/组件/客户端面纳入，不扩张为模型谱系。上述资料并未证明最佳实践或真实成效。

## 未知与资料限制
- Glean 直接打开正文为空；官方搜索索引完整文本可读，单独标记证据来源
- Lindy .md 路由内容类型不受浏览工具支持；正常 HTML 路由成功，不再使用旧 Academy 教程
- GitHub 网页浏览 cache miss；官方 GitHub connector 成功核实 main SHA 与本地相同。
- 各地区实际可用性、企业合同、税费、全部套餐和实付价格未核验
- 没有实际部署效果、精度、节省时间或 ROI 证据
- 平台版本滚动更新；集成动作和权限须在授权后重新验证

## 下一批缺口（未准入、未核验）
- OpenAI ChatGPT agent：待单独读取官方 OpenAI 资料与去重，不在本批准入；未断言当前接入、价格或能力。
- Anthropic Claude 办公代理/用户所称 Cowork：名称、生命周期、权限与运行面待官方来源核验，不在本批准入。
- Google、Salesforce、ServiceNow 等办公 Agent 系统及亚洲供应商：另批核对具体命名实体；不以供应商品牌直接充当可用 Agent。
