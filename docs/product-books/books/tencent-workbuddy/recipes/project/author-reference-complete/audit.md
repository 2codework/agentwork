# 审计参考（作者编写，不是产品运行日志）
reference_origin=author_reference；product_execution=not_run；ui_execution=not_run；runner_implemented=false。
## 资料与生成边界
仅用本例列出的inputs；未执行产品任务，未发起连接器、网络、安装、脚本、消息、发布、付费、仓库操作。此句描述研究包编写范围，不是对未来产品行为的证明。
## 输入/输出记录
- 输入：recipes/project/inputs/tasks.csv；SHA256 e7c02c8129ae456ea73f66edd81a5d866cf95422c0a177ea9e8f2141f9f7a846
- 输入：recipes/project/inputs/context.md；SHA256 33d2d172fb55c3b7a77934097ae225a9af29a599255e131a0684adfad6843891

- 必交参考：status.csv
- 必交参考：weekly.md
- 必交参考：audit.md

## 人工授权证据
没有产品任务计划或确认事件，值为not_run。将来产品运行须附计划、用户仅批准outputs的确认记录、权限/工具动作记录、输入前后哈希；缺任何一项不得通过。不能复制此参考冒充真实授权日志。
## 事实核查锚点
P1完成有R1；P2今日到期且账号阻塞，不叫逾期；P3未逾期但依赖风险；P4逾期负责人待定；上线未批。
## 待确认/风险
重述基准日与严格小于口径重算; 冲突留待核不静默改数据
## 自检
所有必交文件需存在、非空、引用可回溯；未决项保持未知。人工语气/授权/事实判断不能由机器存在性检查代替。
