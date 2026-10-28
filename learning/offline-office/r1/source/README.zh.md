# 会议行动项：原创纯离线规则练习 r1

**这不是LLM、自然语言理解、MCP合规或真实产品效果评测。** 本练习将人工预标注的6条合成会议事实转为可核对的交付物，止于本地已审阅草稿；不发送消息、不创建日历、不分派工作。`dispatch_allowed`始终为false。

## 前提与边界

已有 Python 3.10+，仅标准库，无pip/API key/模型/账号/网络/真实个人数据。安全读取依赖POSIX的`O_NOFOLLOW`与`O_NONBLOCK`，缺少时退出2，不降级；本次仅在Linux Python 3.12实际验证，未验证Windows/macOS/所有Python版本。不自动安装任何软件。

`lab.py`只读明确指定的常规文件并输出stdout。拒绝最终路径分量为符号链接、FIFO/设备等特殊文件；lstat/open/fstat检查文件身份变化，非阻塞打开避免替换FIFO导致等待。上级目录应是学习者控制的普通目录；这不是可对抗恶意文件系统/源码篡改的沙箱。读取上限64KiB，严格字段与数量限制，不解释输入中的路径、URL或指令。

测试在本练习目录创建临时目录并清理；`-B`禁止pycache。构建脚本会在明确指定的新输出目录写ZIP及清单，拒绝覆盖已有输出目录。保存stdout应显式写入新文件，勿覆盖输入。

## 5步完成一次练习

进入解包的`meeting-action-lab`目录。

1. 阅读`fixtures/meeting.json`，尤其F1建议、F2协助意愿不等于决定/负责人；F5才是明确决定；F6须保留F3和F4依赖。全部角色/会议均虚构。
2. 复制`fixtures/submission-template.json`为你自己命名的新JSON文件，手工填写6行。每行固定item_id I1–I6，对应fact_id F1–F6；引用必须逐字一致，未知负责人/日期为JSON `null`。输出不是任意自然语言答案，字段必须按契约填写。
3. 先运行下面的故障演示，再对你自己的文件运行validate，根据错误修改。
4. 正确后，复制空的`fixtures/review-template.json`到新文件`my-review.json`。**由人阅读清单后**填入报告中的input_sha256和submission_sha256，并选择approve或reject。reject必须给原因。模板不预填批准，程序不会生成或代替人工批准。
5. 运行review，读取`status`和`approved`。输入或提交任意字节（包括空白）改变后旧审阅立即失效，需要重新阅读和明确决定。即使批准仍不可外发。

```sh
python3 -B lab.py validate --input fixtures/meeting.json --submission fixtures/submission-bad.json
# 退出1：恰好KIND_MISMATCH、UNCONFIRMED_OWNER、DEPENDENCY_MISMATCH三错
python3 -B lab.py validate --input fixtures/meeting.json --submission fixtures/submission-good.json
# 退出0：status=pass, errors=[]；good是供对照的作者答案，不是模型生成结果
python3 -B lab.py validate --input fixtures/meeting.json --submission my-submission.json
python3 -B lab.py review --input fixtures/meeting.json --submission my-submission.json --review my-review.json
python3 -B lab.py check-golden
python3 -B -m unittest discover -s tests -v
```

退出码：0表示本条命令合法完成，**不等于批准**；合法reject退出0、status=needs-revision、approved=false。1表示内容验收失败或审阅过期；2表示参数、文件、编码、JSON、schema不合法。缺CLI参数由argparse打印用法并退出2，不打印JSON报告。其他正常报告均含mode=rule-simulation及dispatch_allowed=false。

## 输入与预期输出

输入严格为作者固定六事实；`lab.py`内`FIXED_ROWS`是教学信任根，fixtures和golden不是独立可信来源。篡改输入的建议标签再同步修改提交也不能通过；允许JSON格式空白变化，但原始字节哈希改变。改源码同时换答案不在验证保证范围。哈希是版本绑定，不是身份认证或签名；HUMAN-DEMO是教学标签，不是真实审阅者验证。

submission字段：schema_version、meeting_id、items；每项为item_id、fact_id、quote、kind、owner、due_date、depends_on、acceptance。验收标准固定字符串见事实卡；依赖集合可换顺序、不可丢失/重复。日期须真实有效ISO YYYY-MM-DD。未知字段、重复JSON键、NaN/Infinity等拒绝。

- `expected/good-report.json`：6事实/6项/0错，status=pass。
- `expected/bad-report.json`：I1建议被改决定、I2虚构负责人、I6漏掉F4，共3错。
- `expected/reviewed-draft.json`：**仅用于合成单元测试的预期输出**，不是人工批准文件、不是实际已批准记录。

报告不复制任意输入全文或reject原因；只列路径/错误代码/事实ID和哈希。review必须先通过内容校验，再匹配输入和提交双SHA；无默认批准途径。

## 复验与包

`check-golden`只检查good/bad两份固定报告，不构造批准。unittest中的approve/reject数据是临时合成测试，不代表实际人工批准；额外独立断言固定三错、固定事实不可被联合改写，避免把可改golden当唯一真值。

从本目录运行（输出目录必须不存在）：

```sh
python3 -B package_lab.py --out ../my-repro-package
```

输出固定时间戳、固定文件权限、按路径排序、ZIP_STORED的可复现ZIP和SHA256.json；不含缓存、日志、真实数据或my-review。清单覆盖ZIP和每个包成员。构建两次到不同新目录，ZIP SHA应相同。实际运行命令/退出码及解包复验在包外`verification/`，防止结果文件互相引用造成不可复现。

## 与AgentWork的关联及限制

基线HEAD `90b10f0e0e165c35ca7f3b7fa69a1a42216c9985` 的125案例未修改。本练习补`meeting-action-log`的执行验收环节，与`mcp-lab-scope`/`mcp-lab-injection`仅概念关联，不是第13节MCP课或任何办公产品实测。不声称行业最佳实践、真实部署、收益、模型能力或生产级权限安全。

后续改进须增加可观察反例，保留旧基准与变更依据。涉及真实数据、账号、外发或模型须停止并另获授权。此次无canonical接入、部署或发布。
