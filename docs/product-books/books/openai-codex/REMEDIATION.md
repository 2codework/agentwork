# r2 独立复核修复记录

时间：2026-10-29 UTC。从 r1 创建新的 r2 目录；r1 字节未改，canonical 未改，无推送/发布。

## 统一契约

每题补 product_id=openai-codex、runner_implemented=false、reference_format、expected_product_artifact_format。role/authorization/cost/privacy/version_scope 为非空可读摘要；完整原数组/对象保存在 structured_details，不丢授权、风险、成本与版本细节。产品级原版本对象存 version_scope_details。source.accessed_at 为 YYYY-MM-DD，sources.json 保留精确 checked_at。每题补 expected_output_artifacts 的路径、SHA-256、作者来源说明，覆盖所有参考文件和 patch。

官方来源与原研究事实未改；9 个官方页面由独立 reviewer 再确认支持文中限定的能力/流程。r1 reviewer 已在临时副本确认 8 基线按预期失败、8 patch 干净应用并与参考文件逐字一致且验收通过。本 r2 保留全部资料而加强验收；这些都不是 Codex 产品实测。

## 验收补强

- cx04：三个样例必须完整匹配 samples.json，不得用三次相同输入充数；change_seams 必须包含两个已知模块与非空目的。
- cx05：MIGRATION.md 必须存在且非空；字段映射与 cutover 前审批字段须正确。
- cx06：金额口径统一为“非负整数分（允许 0）”；新增零值检查；expected.json 必须正确；实际执行作者参考 CLI，检查退出码与 JSON 输出。
- cx07：MANUAL-QA.md 必须存在且非空；静态检查仍不代表 JS、视觉或读屏已验证。
- 上述客观要求可机器检查；文档质量、业务可行性、界面可访问性仍属于未执行的人工 rubric，不用存在性检查冒充语义质量。
- 将成功提示放在所有断言之后；失败不可先输出误导性 PASS。

## 验证

`check_structure.py` 验证本包 schema 子集；统一框架 `scripts/product_books.py::validate_record(recipe, r2_root, True)` 严格验证 8 题。`validate_pack.py` 验证 8 基线拒绝/8 作者参考通过。`test_regressions.py` 检查每个必交参考文件缺失，以及错误 JSON/CLI、重复样例、缺字段、错误映射、零值误拒、空文档、输入篡改和额外路径等反例。

`build_pack.py` 与 `adapt_product_book.py` 仅保留 r1 创作史，已加阻止执行的 guard，避免旧生成器覆盖新契约；remediate_r2.py 是一次性修复记录，同样冻结。复验使用上述 check/validate/test/verify 脚本，而不是覆盖式重新创作。

当前 product_execution=not_run、observed_results=null、runner_implemented=false。没有产品 adapter、LLM/API/SDK、托管 CI、浏览器/读屏执行。数据全部合成；没有触碰会话目录、秘密、Mac/CUA 或许可文件。
