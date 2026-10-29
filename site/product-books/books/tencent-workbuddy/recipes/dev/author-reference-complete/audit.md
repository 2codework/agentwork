# 审计参考（作者编写，不是产品运行日志）
reference_origin=author_reference；product_execution=not_run；ui_execution=not_run；runner_implemented=false。
## 资料与生成边界
仅用本例列出的inputs；未执行产品任务，未发起连接器、网络、安装、脚本、消息、发布、付费、仓库操作。此句描述研究包编写范围，不是对未来产品行为的证明。
## 输入/输出记录
- 输入：recipes/dev/inputs/change.diff；SHA256 91381ddb058372a220ace8fb7511137ed536e5f6c3981742ea4cfc8900a932b7
- 输入：recipes/dev/inputs/requirement.md；SHA256 fe042cba1260af135296fc2f666a3eb64a2176e9c4d2c0939191986035ca8f37
- 输入：recipes/dev/inputs/tests.txt；SHA256 2f59e6dd965fea5b7b4ddb2876dd0127ac5642e9ec858b6f9d5b549bc7c64d37

- 必交参考：review.md
- 必交参考：test-plan.csv
- 必交参考：audit.md

## 人工授权证据
没有产品任务计划或确认事件，值为not_run。将来产品运行须附计划、用户仅批准outputs的确认记录、权限/工具动作记录、输入前后哈希；缺任何一项不得通过。不能复制此参考冒充真实授权日志。
## 事实核查锚点
100从免费变10违反R1，建议恢复>=100；负数拒绝方式未定义需澄清；99/100/101/负数用例均not_run。
## 待确认/风险
拒绝自动修复重申建议文本; 真实Git测试须另授权隔离仓库环境
## 自检
所有必交文件需存在、非空、引用可回溯；未决项保持未知。人工语气/授权/事实判断不能由机器存在性检查代替。
