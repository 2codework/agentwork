# 研究范围、去重和证据

2026-10-29：先读取 OpenAI Docs skill；检查现有 AgentWork r1 案例目录（通用边界/评估章节），并在 assistant-workspace-integration-r2 的 AW content/data 与 MA content/data 可用路径中检索 Codex，未发现直接专用 recipes。该去重范围仅是所读快照，不代表对全部历史包/最终 canonical 做全库去重。新包不复制旧通用章，专注 8 项代码/数据微型仓库。未读取私人 sessions 或凭据。

本地公开帮助：运行 bundled fetch-codex-manual.mjs，将公开手册更新至允许的 `/tmp/aw-codex-docs`；只读取返回路径里的有关权限、认证、最佳实践段落。未运行 `codex` 或外部 agent 服务。手册缓存不作为交付附件，避免整篇复制。

联网：实际官方域名 search + open 页面，不以搜索摘要替代证据。旧 developers.openai.com/codex/{cli,ide,cloud,pricing,quickstart,security} 发生重定向。cli/ide/cloud/pricing 采用落地 URL；quickstart 现为通用 ChatGPT 入口，security 现为 Codex Security 产品，故未用其背书旧版 sandbox 语义。另核验 permissions、auth、app、prompting、best-practices。Markdown 页面 web 抓取出现 Unsupported content-type，改用 HTML 正文读取，非访问权限绕过。

sources.json 收录 9 条有用官方来源，全部实际打开；只存概括和精确链接，不搬运整页/内部 prompt。官方资料支持能力与流程；合成业务规则、fixtures、参考答案不由 OpenAI 背书。计划/版本/账户可用性需要真实执行时重核。未固定模型、未宣称免费无限任务。

作者离线验证与 Codex 执行严格分开。所有 product_execution/status=not_run，observed_results=null。没有跑 Codex、LLM、付费 API、上游 SDK、远程 CI、浏览器或读屏。当前可复用代码/文档是候选内容，未经新的 license 或 publish 批准，不发布到 canonical。
