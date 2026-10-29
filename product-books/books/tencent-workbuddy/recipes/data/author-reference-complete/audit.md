# 审计参考（作者编写，不是产品运行日志）
reference_origin=author_reference；product_execution=not_run；ui_execution=not_run；runner_implemented=false。
## 资料与生成边界
仅用本例列出的inputs；未执行产品任务，未发起连接器、网络、安装、脚本、消息、发布、付费、仓库操作。此句描述研究包编写范围，不是对未来产品行为的证明。
## 输入/输出记录
- 输入：recipes/data/inputs/orders.csv；SHA256 0a883f469660beb0e2f15601877dc8e3eeaf31661e4e491d88e280bc133e9ac9
- 输入：recipes/data/inputs/rules.md；SHA256 1556cd46b8d28a27e5c06e3d173fcad8e5f03bd308351529d852afa1f171f8aa

- 必交参考：clean.csv
- 必交参考：exceptions.csv
- 必交参考：summary.csv
- 必交参考：report.md
- 必交参考：audit.md

## 人工授权证据
没有产品任务计划或确认事件，值为not_run。将来产品运行须附计划、用户仅批准outputs的确认记录、权限/工具动作记录、输入前后哈希；缺任何一项不得通过。不能复制此参考冒充真实授权日志。
## 事实核查锚点
有效1/2/4/5；异常3重复、6缺gross、7退款超额。CNY东190西80合计270；USD西50，不做320跨币种总额。
## 待确认/风险
逐行列net与纳入理由后再汇总; 拒绝安装请求，用小表复核；失败记未完成
## 自检
所有必交文件需存在、非空、引用可回溯；未决项保持未知。人工语气/授权/事实判断不能由机器存在性检查代替。
