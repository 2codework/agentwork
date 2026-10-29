# 智谱/Z.ai ZCode 入门：先确认边界再开工

本章只适用 `zai-zcode`，不是 Amir Hayek Zcode。checked_at 2026-10-29。当前官方桌面分发3.16.3；文档持续更新，所有产品步骤均未实测。资料审阅≠产品运行。

1. 先由有授权的用户从官方安装页选择匹配系统与CPU的包。本文不执行安装；不建议为了运行而关闭杀毒或绕过系统信任检查。无获准可用客户端时停在资料练习。
2. 已安装用户在首次引导选择项目目录。只复制单项fixtures/input作为新工作区，不选公司仓库；reference是作者答案，勿提供给Agent。各练习相互独立。
3. 在Connect选择本人获准的Z.ai/BigModel连接；也可在输入框模型名→Manage Models管理既有通道。登录、密钥和付费由用户本人完成；本教程不代操作。Coding Plan只适用于编码场景，勿挪作批量办公推理服务。不要将密钥写入练习文件。
4. 选择Ask before changes；复杂任务先Plan。输入@引用本练习文件，再粘贴recipe提示。计划批准不代表允许推送、联网或读取工作区外目录；每次核对完整动作。
5. 用户可在工作区根维护AGENTS.md写明“不联网、不安装、不提交，先列测试”；这是项目约束提示，不是安全沙箱。这里只需要根文件，不假设嵌套规则自动合并。
6. 审核输出文件与验证命令；逐项批准只读/离线检查。查看工作区文件树，预览输出；自己的答案和reference不要求字节完全相同，但须满足业务断言与人工rubric。
7. 记录模型、客户端版本、工作区、用量前后、命令、退出码、未测项。Usage Stats区分本机App Usage与远端Coding Plan额度，不混成费用账单；金额与试用权益以账户现时页面为准。
8. 练习结束保留实际日志和diff，不把聊天说“完成”当证据。权限拒绝时缩小范围，不切Full access绕过；普通问题自动继续与权限批准不同，敏感练习可关闭Settings → General → Automatically continue questions。本批不启用Memory、远程、Bot、第三方插件或导入浏览器登录态。

## 新手恢复表
- 没有模型/额度：停在草稿，检查获准通道；不自动购买。
- 命令找不到：记录解释器缺失；不要装依赖，本练习均可先纸面审阅。
- 拒绝权限：说明原因为何，重新给更窄计划；拒绝不是“测试通过”。
- 模型漏上下文：在新任务明确@文件，重新声明限制；不要附整盘目录。
- UI标签不同：核版本与官方文档，标步骤待验证；不猜隐藏按钮。
- 重跑：重新复制input；不要覆盖真实未提交成果。代码错误可局部修，需求不明必须标未决。

官方出处：[安装](https://zcode.z.ai/en/docs/install)、[模型](https://zcode.z.ai/en/docs/configuration)、[Agent](https://zcode.z.ai/en/docs/agents)、[安全确认](https://zcode.z.ai/en/docs/safety-confirm)、[用量](https://zcode.z.ai/en/docs/usage-stats)。
