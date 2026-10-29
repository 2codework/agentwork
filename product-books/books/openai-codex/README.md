# AgentWork · Codex 岗位与业务练习包 r2

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

修复与独立审核闭环见 [REMEDIATION.md](REMEDIATION.md)。`python test_regressions.py` 运行作者参考反例；不是产品 runner。
