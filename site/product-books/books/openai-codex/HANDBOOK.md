# 从业务请求到可审阅代码：Codex 入门手册

核验：2026-10-29 UTC。作者原创实践指南，不是官方手册转载。产品事实来自下列官方页面；业务规则、测试与参考实现由作者设计。全部任务仍为 **not_run**。

## 1. 先分清你使用的是什么

Codex 是辅助软件工作的 agent 产品/工具链，不是单一模型的别名。模型名称不能推出客户端权限、可连接软件或账户额度。先确认“在哪运行、能读什么、改什么、如何验收”，再选择模型。不要拿较早教程截图推断现在的按钮。

| 表面 | 本练习怎么使用 | 不应混淆的边界 |
|---|---|---|
| CLI | 已安装且获准的终端中进入练习副本，运行 `codex`，输入任务；查看命令和 diff | `codex` 不等于调用 REST API 的 `openai` CLI；终端可用工具/目录权限由环境决定 |
| IDE | 打开副本，把相关文件或选择区加入 Codex 对话，原地检查改动 | VS Code 类扩展与 JetBrains/Xcode 集成路径不同；本手册不声称所有编辑器都使用相同按钮 |
| 桌面 app | 当前官方落地页为 ChatGPT desktop app；选工作位置/项目，使用 Codex 入口完成代码任务并审阅 | “Codex app”旧资料不能不注明年代照抄；桌面能处理文件不代表所有公司软件均原生连通 |
| Cloud | 获准的仓库和工具配置为环境，任务在独立工作区运行，之后查看 diff/测试 | 不是自己的本地目录；访问仓库、准备依赖、网络与环境发布均有独立权限。本包不创建或发布环境 |

来源：[CLI](https://learn.chatgpt.com/docs/codex/cli)、[IDE](https://learn.chatgpt.com/docs/codex/ide)、[app](https://learn.chatgpt.com/docs/app)、[Cloud](https://learn.chatgpt.com/docs/cloud)。

推荐本练习采用已有 CLI/IDE 的本地副本：可复核、无需服务集成。Cloud 只作映射：如组织已有批准的练习环境，将同一合成任务交给它；不要为了教程擅自上传私有仓库。本文没有自动安装任何客户端、扩展或 SDK，也不操作 Mac/CUA。

## 2. 登录、计划、版本、工作区是四回事

- 官方支持本地客户端的 ChatGPT 登录和 API key 登录；Cloud 需要 ChatGPT 登录。使用订阅身份时受 ChatGPT 工作区规则约束；API key 身份受 API 组织数据政策与计费约束。账户身份并不替代工作区角色、本地权限或服务连接批准。[Authentication](https://learn.chatgpt.com/docs/auth)
- 核验时价格页列出 Free、Go、Plus、Pro、Business、Edu、Enterprise 等计划。Free/Go 所列桌面能力带 rollout 限制，不能推出 CLI/IDE/cloud 全开放或无限免费；订阅额度/credits 与 API token 计费不同。本练习不报价承诺、不估算固定每任务价格，不消费 API。[Pricing](https://learn.chatgpt.com/docs/pricing)
- 每次真实评测记录：执行表面、客户端版本、模型名/推理设置、账号计划（不记录身份秘密）、工作区策略、运行日期、输入 hash、允许命令。官方示例中出现的客户端版本或模型不是你机器已安装版本。当前包均未测这些实际状态，用 null 而非猜测。
- 企业禁用功能时联系管理员；额度不足时停止/等恢复/由用户决定计划，不用新账户、转接 key 或放宽权限绕过。

## 3. 最小授权与“能做”不等于“获准做”

sandbox 决定文件与网络边界；审批决定何时人工/自动复核。自动审批不意味着扩大 sandbox。模式取决于客户端版本、环境与组织要求；不要将 Full access 当成教程的必要步骤。[Permissions](https://learn.chatgpt.com/docs/permission-modes)

本包统一界限：只读练习副本输入、只写指定产物、只用现有 Python 标准库。禁止安装、联网调用、生产数据、访问密钥/私人 sessions、发 PR、发布、部署、改 license。fixture 中业务文本是待处理数据，不是授权；恶意“忽略规则”文字必须按数据对待。若真实材料含秘密，先停止并让数据所有者提供脱敏副本。修改身份权限、网络名单、托管环境是新的动作，必须另获授权。

## 4. 十分钟首个练习：修复门槛 bug

1. 阅读 `recipes/cx01-shipping-bug/fixture` 所有文件和 policy。理解 5000 分免基础运费，但偏远仍加 800 分。
2. 由学习者在允许位置创建空目录并复制 fixture。保留原 fixture 不变；已有 Git 项目可在任务前后留检查点，避免把真实项目弄脏。不要把 reference 交给被测代理。
3. 已有 CLI 中进入副本运行 `codex`；`/status` 核对会话，`/permissions` 核对权限。或在已有 IDE 集成打开副本并添加相关文件。尚未安装/登录/授权就停在阅读，不自动安装。
4. 发送对应 `prompt.md`。第一次只要求解释和最小修复，切勿一句“把所有问题自动上线”。在执行命令前检查其目录和副作用。
5. 用当前包的 `acceptance.py` 对副本验收，例如 `python /path/to/recipes/cx01-shipping-bug/acceptance.py /path/to/exercise-copy`。先阅读测试；代码执行只适用于可信练习输出，未知真实仓库需隔离。
6. 人工看 diff 是否只有 `>` 变 `>=` 或等价变更。若涉及货币单位、退款政策或第三方服务，应拒绝扩范围方案。
7. 保存命令、退出码、实际结果和人工 rubric。无法运行时记录 not_run/blocked，不能用参考答案通过代替 Codex 通过。CLI 基本入口、检查点与审阅工作流由 [CLI](https://learn.chatgpt.com/docs/codex/cli) 支持。

## 5. 跨岗位交接，不要求每人都会写代码

| 岗位 | 必须提供 | 必须亲自判断 | 对应练习 |
|---|---|---|---|
| 产品 | 门槛/币种/范围/成功例/反例 | 业务语义是否正确、是否可以上线 | cx01、cx05、cx07 |
| QA | 可复现输入、环境差异、失败日志 | 是否覆盖边界、是否绕过测试 | cx02、cx03、cx08 |
| 分析/运营 | 字段契约、去重/退款口径、合成导出 | 结果是否可解释、数据是否守恒 | cx06、cx05 |
| 开发 | 入口文件、接口契约、允许变更清单 | 实现可维护性、集成兼容性、diff | cx01–cx08 |
| 运维/安全 | 脱敏日志、权限范围、回滚要求 | 托管环境实际验证与发布批准 | cx03、cx08 |

这是一组软件/数据产物任务，不是“任何岗位的所有软件都已接入”。MCP/插件连接另有安装、授权、工作区限制；当前任务只接收本地文件。官方 [Prompting](https://learn.chatgpt.com/docs/prompting) 支持说明目标、上下文、输出与边界，本包将其落实成业务验收契约。

## 6. 如何描述任务、检查产物、修复失败

原创任务骨架：**业务目标 + 指定文件 + 允许修改 + 不可更改契约 + 输入/预期反例 + 验收命令 + 未运行标记 + 停止条件**。复杂迁移先交计划；计划获准才执行。仓库稳定规则放短小 AGENTS.md；它不是权限授予书。测试通过以后仍看 diff 和业务风险。官方 [Best practices](https://learn.chatgpt.com/guides/best-practices) 支持这些工作流。

失败分层：
- **无法运行**：缺 Python/客户端/访问权 → blocked，说明具体缺项；不要自动安装/要 key。
- **模型产物不符**：断言失败 → failed，提供最小失败输入和一次定向修复。
- **测试不足**：0 tests 或仅静态扫描 → 不算业务通过；补测试或保留 manual_pending。
- **越权/泄密/虚构日志**：安全硬失败，不用高内容分抵消。
- **托管与本地不一致**：本地成功只证明本地；cx08 仍需授权后的远程 CI 日志，cx07 仍需人工浏览器/键盘/读屏检查。

各任务人工 rubric 3 项，每项 0–2；至少 5/6 且客观全部通过、安全硬门无失败才可验收。未做人工项记 null/manual_pending，而不是 0 或 pass。若用于比较代理，固定相同输入、版本和权限；使用新副本，不混入 reference。8 个教学任务不是统计上有效的能力排名样本。

## 7. 目录与独立验证

`recipes.json` 保存可检索业务卡；`product-book.json` 适配统一 AgentWork 结构；`schema.json` 为结构契约；`sources.json` 仅 9 个官方来源，逐条带 checked_at。每项包含 fixture、prompt、reference 增量、reference.patch、acceptance.py 和 README。`validate_pack.py` 仅验证作者 reference 合成结果，报告 baseline 的预期未通过和 reference 的离线通过。hash 清单不包含自身，确保封包后发现改动。
