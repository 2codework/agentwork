# 验证范围与复现

已实际执行：`python check_structure.py`（本包 JSON schema 所用关键字的 stdlib 子集校验、唯一 ID、输入 SHA-256、路径与官方来源）；`python validate_pack.py`（8 个原始 fixture 预期拒绝；8 个 fixture + 作者 reference 增量通过）。

- cx01：阈值/偏远/负值，7 个边界。
- cx02：参考 unittest 在原函数通过，在舍入、范围上界、漏折扣 3 个故意错误变体中失败。
- cx03：缺 tenant 过滤的复现与报告定位；源函数保持原状，不作安全审计保证。
- cx04：数据流锚点、三个文档样例与源码一致；文档语义仍人工审核。
- cx05：笔数/金额守恒、逐 id 映射、批准顺序、兼容窗口、回滚字段；没有执行迁移。
- cx06：净额/去重、冲突/非法拒绝、CSV 保持原状。
- cx07：HTML 静态结构/常见外部调用检查；**未执行 JavaScript、浏览器、读屏或视觉 QA**，不证明完整可访问性或无所有潜在网络行为。
- cx08：本地 stdlib unittest 发现并通过 1 测试；YAML 仅窄字段检查，**未运行托管 GitHub Actions**，不证明 Actions 版本/runner 可用。

每个 acceptance 先核对受保护 fixture 文件 hash，再限制非生成文件的路径集合（忽略 `.git` 与 `__pycache__`），防止靠改输入或偷偷加业务文件过关。执行 acceptance 会导入/运行任务代码，它不是安全沙箱；仅对已检查的合成/可信副本执行，未知输出先隔离和人工审阅。

运行结果见 validation-report.json 与 validation.log。所有 product_execution=not_run、observed_results=null；人工 rubric 未执行。作者参考输出的 PASS 不是 Codex 成功率，不可用作产品排名。

封包 SHA-256 见 SHA256SUMS.json（排除自身与 Python 缓存）。验证方法：`python verify_hashes.py`。之后任何修改应重验并重新封包；该 hash 是完整性摘要，不是签名或来源认证。

## r2 补强
统一框架严格记录验证 8/8 通过。所有必交参考文件缺失与业务错误的负回归见 negative-regressions.json；修复详情见 REMEDIATION.md。role/授权/成本/隐私/版本的结构化细节保留在 structured_details。
