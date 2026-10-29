# ZCode 岗位教材 r4

阅读入口：GETTING_STARTED.md → BOOK.md → fixtures/<recipe>/input。

- `playbooks.json`：完整目录、16项官方来源、版本渠道差异、去重记录、8项智谱/Z.ai教材。
- `product-book.json`：框架适配入口，仅zai-zcode的8项recipes。
- `other-product-identity.json`：Amir Hayek Zcode独立身份/限制卡，教程尚待补，不计入8项。
- `fixtures/*/reference`：作者参考答案，绝非ZCode运行输出；请勿作为输入给Agent。
- `VALIDATION.json`：8项参考fixture离线检查；产品及人工rubric/浏览器视觉均未运行。
- `playbooks.schema.json`、`validate.py`：结构验证、引用验证与参考fixtures检查。
- `SHA256SUMS`：交付文件哈希；`sha256sum -c SHA256SUMS`核对。

本包允许研究两个同名产品而不替用户选定；generic zcode alias为ambiguous/default null。r1作为消歧过程审计保留，本r2不再把同名当作研究阻塞。

重建：`python build.py && python validate.py && python validate_framework.py && python validate.py`。validate依赖当前云环境已有jsonschema；未安装任何厂商软件或调用模型API。验证器只运行作者生成的本地Python小脚本，全部标准库、不联网；预期缺陷测试明确要求失败。HTML只做静态验证，视觉与键盘验收仍not_run。

安全：本包不授权安装、调用账户、付费、联网、推送、发布或处理真实业务数据。教材步骤供有授权的读者复现；本次没有实际产品运行。内容许可保持待负责人确认，不改canonical许可，不声称本轮涵盖全部版本和所有用法。

## r3修复
见REMEDIATION.md及FRAMEWORK_VALIDATION.json。r2保持不变；r3补全框架类型与元数据、参考交付物、G/W/T及负例验收。remediate.py为一次性迁移审计，不要重跑；日常只按上面的重建命令。

## r4最终一致性修复
退款允许修改集合补rationale.md，消除新增必需说明文件与旧两文件diff限制冲突；详见REMEDIATION.md。r3保留不变。
