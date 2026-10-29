# r1 QA逐项修订

状态：提交独立复验，非自批准。r1完整保留，r2不改canonical。

1. **片段不足**：8例全部补齐声明Markdown/CSV scope，共28产物。meeting补minutes与录制待确认；content补180汉字正文、review；project补weekly；data补clean/exceptions/report；support补四工单replies；research补memo/gaps；design补handoff、风险与五步焦点验收；dev补严重性与完整修复建议。每例补audit。reference_kind=complete_author_reference、covered/uncovered文件集合明确；author_reference入口指向全部文件，旧片段仅历史保留。
2. **转换丢失**：统一包逐步保留status/source_id；保留source_recipe原记录及synthetic/surface/practice_status/third_party/author_reference/dedup；新增product_id、authorization字符串、ui_execution=not_run、runner_implemented=false。
3. **80分绕过**：全部必交文件存在非空可读、引用覆盖人工核验、audit及真实运行计划/授权/工具日志/输入前后哈希齐全均前置硬门槛。任一缺失直接失败。附66项负例检查（每文件删除/清空、错误数值、缺运行证据）；人工事实/语气/引用不自动通过。内容正文固定计U+4E00–U+9FFF，180字，标题/CTA独立段/依据不计。业务风险硬失败逐例列明。
4. **格式scope**：reference_format与expected_product_artifact_format明确Markdown/CSV，不宣称Office原生、可视化、Figma或真实Git。全部产品/UI not_run，observed_results=null，不编实测。
5. **去重**：DEDUP新增当前AgentWork138 cases与ModelAtlas254 nodes的路径、SHA和字面检索；保留语义重叠限制。
6. **隐私/更新/许可**：privacy_policy_review=blocked_dynamic_content；不推断训练或驻留；手册提醒“检查更新”可下载安装，不能作只读查版本；license_pending，不改许可证。

验证范围：本地文件/JSON/SHA、作者参考数字和声明式门槛。真实产品adapter未实现，真实运行授权证据为not_run而非伪造。本报告不替代独立QA。
