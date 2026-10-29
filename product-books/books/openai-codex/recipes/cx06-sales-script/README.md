# 从合成订单导出生成区域净额脚本

把可重复的销售口径落为 stdlib 脚本，而非仅给一句汇总数字。

状态：**not_run**。reference 是作者手工编写的合成参考产物，不是 Codex 结果。

## 岗位协作
- 分析：定义退款负号、重复 id 与取消口径。
- 运营：提供脱敏导出；QA：手算总额并提供冲突重复反例。

## 跟做（执行前先读根目录 HANDBOOK.md）
1. 在你已有、获准使用的 CLI/IDE 环境复制 fixture 到新的练习目录；不要复制 reference 给被测代理。检查合成文件内容和 AGENTS.md；无真实客户/账号数据。
2. 记录表面、客户端版本、当前模型、日期、计划及工作区策略；确认允许范围和预算。未安装/未授权则停在静态阅读，不在本包自动安装。
3. CLI：进入练习副本并输入 `codex`，使用 `/status` 与 `/permissions` 核对当前状态；IDE：打开该副本，明确附加 prompt 指定文件，使用已启用的 Codex 对话。两者任选其一，不能把 IDE 的按钮照搬到 CLI。
4. 发送 [原创任务 prompt](prompt.md)。先看计划/将运行命令；批准仅限副本内改动和给定离线测试；出现额外网络、密钥或系统安装请求就停止并缩小任务。
5. 阅读改动与最终摘要，将输出留在练习副本。执行 `python /绝对路径/recipes/cx06-sales-script/acceptance.py /绝对路径/练习副本`。这只能检查明确的断言，不替代下列人工 rubric。
6. 比较 [参考 diff](reference.patch)，允许语义等价实现；不要求字面复制。记录实际命令、退出码、失败与重试、人工评分。没有运行的项保留 not_run，不能填 pass。

## 客观验收
- north=800、south=700、重复 1 行
- 冲突重复/负值/未知状态拒绝，原 CSV 不变

## 人工 rubric（各 0–2 分）
- 口径：正确区分净额与利润（0/1/2）。
- 健壮：错误输入给明确失败，不静默吞掉（0/1/2）。
- 可复用：函数与 CLI 均清晰，金额全程整数（0/1/2）。

通过：客观检查全部通过，人工至少 5/6 分，且无越权/泄密/伪造执行证据。任一安全硬门失败即不通过。

## 失败恢复
- 若重复叠加或退款加正数，先手算四个有效 id 再修。
- 遇到缺字段真实数据应停并补数据契约，不能默认视零。

- 保存失败日志和差异；从原 fixture 新副本重试，不覆盖基线。若测试环境缺失，标 blocked，不声称功能失败；若输出不符，标 failed。未经批准不升级权限、不安装依赖、不连接服务。
- 先一次任务，再最多一次针对错误的修复；没有足够额度即停止。离线测试免费于模型调用，但将来真实 Codex 运行受账户额度/计费约束。

## 来源与核验
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
- [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
- [Pricing](https://learn.chatgpt.com/docs/pricing)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
- [Authentication](https://learn.chatgpt.com/docs/auth)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
- [Permissions](https://learn.chatgpt.com/docs/permission-modes)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
- [Best practices](https://learn.chatgpt.com/guides/best-practices)（2026-10-29T05:34:00Z；仅支持产品能力/工作流，不背书本练习业务规则）
