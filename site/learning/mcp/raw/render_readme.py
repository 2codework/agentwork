import json
from pathlib import Path
R=Path(__file__).parent
bundle=json.loads((R/'cases.json').read_text())
src=json.loads((R/'sources.json').read_text())
src['sources']=[s for s in src['sources'] if s['id']!='sdk-migrate']
(R/'sources.json').write_text(json.dumps(src,ensure_ascii=False,indent=2)+'\n')
S={s['id']:s for s in src['sources']}
text='''# MCP、Skill 与提示词：十二个离线操作课

核查日期：2026-10-28。对象：想把“知道术语”变成“能读消息、能找错误、能写验收”的学习者。

这不是链接目录，也不是 SDK 安装演示。本书用原创合成 JSON、手工推演与标准库测试，练习真实协议中的关键边界。**这里只实际运行了原创离线模拟契约，不是 MCP SDK、真实服务、OAuth、模型或端到端部署实测。** 不需要账号、付费模型、密钥或特定操作系统。网络仅用于编写时核查公开官方资料；运行课程无需网络。

## 先理解整体

主机管理用户交互与策略；客户端是主机中的协议连接方；服务端提供工具、资源、模板等能力。模型可以建议调用，但生成参数不等于获得执行权限。提示词是一次任务的语言输入；skill把方法、适用条件和可选材料组织成可复用包；MCP规范定义互操作消息。三者可协作，但任何文字都不能自行提升权限。

安全不是“再加一句提示词”：数据与指令隔离、实际权限判断、输入输出校验、审核和副作用控制必须由应用落实。本课的确定性白名单示例不构成对任意模型的防注入保证。

## 版本不要混写

| 固定范围 | 本书用途 | 生命周期说明 |
|---|---|---|
| MCP 2025-06-18 | 迁移课保留历史变化 | 历史；不是当前最新 |
| MCP 2025-11-25 | 第02–06、10课线协议 | 历史固定版本；保留initialize握手 |
| MCP 2026-07-28 | 第12课与迁移目标 | 核查日官方现行规范线；逐请求元数据、无旧握手 |
| TypeScript SDK v1.x 文档 | 理解旧版资料 | 官方标注maintenance，支持到2025-11-25 |
| TypeScript SDK v2 文档 | 了解当前迁移路径 | 官方标注stable；这里未选择精确补丁包、未安装或运行 |
| Agent Skills未编号规范 | 第09课格式 | 固定核查快照2026-10-28；宿主支持需另查 |

[现行规范](https://modelcontextprotocol.io/specification/2026-07-28)、[现行变更说明](https://modelcontextprotocol.io/specification/2026-07-28/changelog)、[SDK v1维护线](https://ts.sdk.modelcontextprotocol.io/)、[SDK v2文档线](https://ts.sdk.modelcontextprotocol.io/v2/)。协议日期和SDK包版本不是一个概念。真实实现前应另选精确包版本与锁文件，不能从本书推定安装组合已验证。

## 如何操作

1. 在本目录运行 `python validate.py`。预期为 `cases_passed: 12`，各课输出见下文。
2. 运行 `python -m unittest discover -s tests -v`。本次记录为18个测试通过；其中一个测试逐一检查12个fixture。
3. 单课运行示例：`python validate.py --case mcp-lab-tools`。
4. 阅读对应 `fixtures/` JSON，再手算、标记角色或修改临时副本。`validate.py` 的Python函数 `evaluate` 可验证内存副本；测试文件提供修改例子。不要修改历史原件后仍称它是原版本。
5. 对照下文验收，不把校验输出当真实外部系统执行结果。

`fixtures` 外层的 `direction`、`kind`、`expected` 是本书自定义记录格式，不是MCP消息。只有其中 `message` 对象才是线协议示意。roles/scope/injection/skill/migration是本书自定义练习JSON，并非MCP方法。`lesson://`是合成资源标识，不连接任何主机。

### 校验范围与不覆盖项

校验器主动采用狭窄子集：仅客户端发起请求；每份历史fixture都完整初始化；只有固定加法工具；只验这里使用的整数schema；取消立即移出本模拟在途集；现代fixture仅tools/list。它不是完整JSON Schema解释器，不实现传输、分页面遍历、OAuth、真实取消竞态、扩展协商、server/discover、MRTR、SDK依赖或模型行为。它对未知取消、迟到响应的拒绝是**严格教学fixture完整性规则**，不是声称规范要求所有真实端点同样拒绝（旧版规范允许忽略未知或已完成取消，并要求妥善处理竞态）。

## 课程

'''
for c in bundle['cases']:
 text+=f"## {c['title']}\n\n**目标：** {c['goal']}\n\n**前置：** {'；'.join(c['prerequisites'])}\n\n**适用版本：** {c['applicable_versions']}  \n**生命周期：** {c['lifecycle']}（{c['lifecycle_as_of']}）\n\n"
 text+='### 合成输入\n\n```json\n'+c['input']+'\n```\n\n'
 text+='### 可直接使用的审阅提示词\n\n```text\n'+c['prompt']+'\n```\n\n'
 text+='### 分步操作\n\n'
 for i,s in enumerate(c['steps'],1):text+=f"{i}. {s['body']}\n   - 验收：{s['check']}\n"
 text+=f"\n单课命令：`python validate.py --case {c['id']}`\n\n### 预期输出\n\n这是本地教学报告，不是服务端执行凭据。\n\n```json\n{c['output']}\n```\n\n### 验收与常见错误\n\n"
 text+='\n'.join('- 验收：'+s for s in c['rubric'])+'\n'
 text+='\n'.join('- 常见错误：'+s for s in c['common_errors'])+'\n\n'
 text+='**权限边界：** '+c['permissions']+'\n\n**失败处理：** 先在临时副本修正被指出的字段或顺序，再运行本地测试。外部操作结果若未知，先查询状态；不要将本地重放规则套用于真实写操作。\n\n'
 text+='**出处与核查：** '+'；'.join(f"[{S[s]['title']}]({S[s]['url']})（版本：{S[s]['version']}；访问：{S[s]['checked_at']}；生命周期：{S[s]['lifecycle']}）" for s in c['source_ids'])+'。\n\n'
 text+='**关联建议：** AgentWork case `'+c['id']+'`；ModelAtlas '+', '.join('`'+n+'`' for n in c['modelatlas_node_ids'])+'。这些是学习关联，不是模型能力或性能证据。\n\n'
text+='''## 与 AgentWork / ModelAtlas 的对应方式

已对照两项目现有公开内容结构；本目录独立，不直接覆盖原内容。

- AgentWork：`cases.json`沿用`schema_version: 1`、`book[]`、`cases[]`及`steps.title/body/check`；既有字段`input/prompt/output/risks/rubric`可直接展示。保留`goal/prerequisites/common_errors/permissions/source_ids/fixture/modelatlas_node_ids`作为扩展字段；接入时必须将它们映射到书页/案例卡，不能只保存在原始JSON中却不展示。
- 生命周期：历史课保留旧版本，不自动重命名“最新版”；`replacement_case`留空，因为当前课不是旧课每个特性的完整替代。
- ModelAtlas：已有`sys-mcp`、`sys-skills`、`sys-promptcontracts`、`agents`节点适合作为入口。建议新增12个tutorial节点，而不是把本书写成模型发布事件。`integration-suggestions.json`列出建议ID、现有锚点与课程来源；这些关联均为editorial learning relation，不是技术派生或实测能力关系。
- 若记录协议发布事件，用来源明确支持的标准版本日期；访问日期不是发布日期。Agent Skills无编号规范和SDK滚动文档的发布日期未知，不虚构日期。

## 后续真正集成时的验收清单

保留完整历史输入；将目标、前置、提示词、失败恢复和权限边界实际呈现；校验所有关联ID可达；对现代/历史版本分别验收；选定精确SDK依赖后才写运行说明；先做授权隔离环境的真实兼容测试，最后再决定是否加入模型。没有做过的步骤标“未测试”，不要把本目录通过升级为真实服务可用。

## 文件与证据

- `cases.json`：十二课结构化内容；`README.md`：完整教学正文。
- `sources.json`：官方来源、核查日、版本、生命周期与支持范围。
- `fixtures/`：十二份原创合成输入与预期教学报告。
- `validate.py`、`tests/test_contract.py`：原创标准库校验器与独立测试。
- `verification.json`、`test-results.txt`：本次离线运行记录。

内容为原创教学设计，官方材料用于核查协议与格式规则。未复制第三方完整教程、skill包或内部资料；不承诺“覆盖所有MCP功能”。下一层可扩展范围包括真实SDK、transport、分页、订阅、现代协商、MRTR与扩展，但应分别取得环境与权限，并独立记录结果。
'''
(R/'README.md').write_text(text)
suggestions={'schema_version':'mcp.learning.integration-suggestions.v1','checked_at':'2026-10-28','status':'suggestions_only_not_merged','agentwork_mapping':'cases.json uses schema_version 1; render all pedagogical extension fields','modelatlas_tutorial_nodes':[]}
for c in bundle['cases']:
 suggestions['modelatlas_tutorial_nodes'].append({'id':c['id']+'-tutorial','title':c['title'],'type':'tutorial','category':'agents','description_zh':c['goal'],'prerequisites':c['modelatlas_node_ids'],'source_ids':c['source_ids'],'version':c['applicable_versions'],'checked_at':c['checked_at'],'verification_status':'offline_contract_only','agentwork_case_id':c['id'],'relation_evidence_type':'editorial_learning_order','lifecycle':c['lifecycle']})
(R/'integration-suggestions.json').write_text(json.dumps(suggestions,ensure_ascii=False,indent=2)+'\n')
