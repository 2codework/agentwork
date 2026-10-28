# 内容规范 v1

`content/cases.json` 顶层含 `schema_version: 1`、`book[]`、`cases[]`。

正文：`id, title, body, exercise` 均为非空字符串。案例：

| 字段 | 约束 |
|---|---|
| id | 唯一小写 ASCII 字母、数字、连字符，1–80 字符；发布后保持稳定 |
| title, summary | 中文优先的非空纯文本 |
| roles, industries | 非空字符串数组 |
| evidence | synthetic / primary / secondary |
| synthetic | 布尔值，与 synthetic 证据严格一致 |
| steps | 非空数组，每项 title, body, check 均非空 |
| sources | title, url, evidence；HTTPS 无凭据链接，evidence 为 primary / secondary / reference |

非合成案例必须有来源。`primary` 只表示一手材料，不表示独立审计或效果证明；`secondary` 不是部署证据；`synthetic` 必须明确是教学设计。具体主张与证据等级需人工复核，构建不能替代事实核查。

`research/*.json` 保留研究worker的原始结构；`normalize.py` 分别明确映射 roles、industries、learning，并将每条完整原记录保留为 raw_record，来源完整保留为 raw_source。缺少必需字段、来源 ID 或未知适配器会报错。生成案例卡含输入、提示词、整体 rubric、风险、来源核查日期；roles/industries 提示词由本项目原创通用模板生成，步骤级验收是整体 rubric 的提醒，不声称原研究逐步实测。这不把研究设计升级为已实测案例。研究文件只允许本轮原创总结与可公开引用，不允许私有资料。

额外案例字段：input/prompt/output/risks/checked_at/evidence_note 为纯文本，rubric 为验收字符串数组。所有信息同时生成到 BOOK.md 与 site/data.json；网页通过纯文本显示。

进度备份：`{"schema_version":1,"completed":{"case-id":"ISO 8601 timestamp"}}`，可附 exported_at。未知案例 ID 忽略；导入合并覆盖相同 ID 时间，不上传。

## 生命周期与最佳实践（独立于来源日期）

每个案例必须包含：
- `lifecycle`: `current`（已核查现行）、`superseded`（已有替代）、`deprecated`（不建议采用）、`historical`（仅历史参考）、`unknown`（尚未核查）。首批全为 unknown，不能由 checked_at 推导为 current。
- `applicable_versions`: 产品/标准/组织流程的适用版本与条件；不确定就说明未核查。
- `lifecycle_as_of`: 本次生命周期判断日期；unknown 用“未核查”，其余状态必须给出日期。
- `replacement_case`: 同仓库替代案例 ID；无已核实替代时空字符串，不猜测。
- `historical_context`: 首次收录、历史背景、失效原因/条件或未知边界。
- `practice_status`: 是否有权威行业指南、适用范围及证据支持“最佳实践”；未核验时只称原创教学模板。

历史案例应保留来源、当时适用版本、迁移说明与失败风险，不因过时直接删除。过时与替代判断必须有明确来源和人工审阅。来源发布日期、访问日期、案例首次收录日期和生命周期确认日期不得互相替代。

进度日期只接受本应用导出格式 `YYYY-MM-DDTHH:mm:ss.sssZ`，并做 ISO roundtrip 校验以拒绝 2 月 30 日等不存在日期；无时区或不同格式需要先规范化，不能静默猜测。

每个操作模板至少有：合成输入→提示词→具体步骤→输出模板→可判断的 rubric→失败恢复/风险→权限审批→来源与生命周期。步骤不构成外部操作授权；行业“最佳”主张须另附可核验证据。
