# 审计参考（作者编写，不是产品运行日志）
reference_origin=author_reference；product_execution=not_run；ui_execution=not_run；runner_implemented=false。
## 资料与生成边界
仅用本例列出的inputs；未执行产品任务，未发起连接器、网络、安装、脚本、消息、发布、付费、仓库操作。此句描述研究包编写范围，不是对未来产品行为的证明。
## 输入/输出记录
- 输入：recipes/support/inputs/policy.md；SHA256 486b038871ed02852efaf599c2818b3a642a0d649500376ac4e9077ac193f62e
- 输入：recipes/support/inputs/tickets.csv；SHA256 971f670e9524560e81be52169569ffeb57cb1c9e0bb9607f52cd4e769659c867

- 必交参考：replies.md
- 必交参考：routing.csv
- 必交参考：audit.md

## 人工授权证据
没有产品任务计划或确认事件，值为not_run。将来产品运行须附计划、用户仅批准outputs的确认记录、权限/工具动作记录、输入前后哈希；缺任何一项不得通过。不能复制此参考冒充真实授权日志。
## 事实核查锚点
T1可申请需审核；T2升级；T3旧政策未知核查；T4不索密且按正常申请条件起草。
## 待确认/风险
冲突升级不补造政策; 敏感字段移出草稿，不复制到审计
## 自检
所有必交文件需存在、非空、引用可回溯；未决项保持未知。人工语气/授权/事实判断不能由机器存在性检查代替。
