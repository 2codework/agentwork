# r1实施修改依据

- 原计划只描述严格输入schema，但未锁定事实信任根。独立QA指出可同时改input+submission自洽作弊。实现加入源码FIXED_ROWS，逐项校验六事实全部语义字段；不是放宽验收。golden之外增加联合改写精确回归。
- 原计划未规定特殊文件读取。独立QA指出FIFO阻塞风险。加入常规文件预检查、O_NOFOLLOW/O_NONBLOCK、打开后fstat身份比对、64KiB限读；安全标志缺少则失败，不降级。平台支持范围据此收窄为有这些标志的POSIX环境，仅Linux已实测。
- 独立代码审查复现5000位整数触发json.loads普通ValueError，原实现未捕获。现按输入错误退出2并增加回归；未放宽JSON规范。
- reviewed-draft golden只作为合成测试期望输出；check-golden不会生成批准，review-template保持空decision和空哈希。批准样本仅测试时临时构造，不能冒充人工审阅记录。
- 输出确定性不含时间/随机ID/绝对路径；打包排除运行日志，运行日志独立保存，避免ZIP哈希与日志自引用。
