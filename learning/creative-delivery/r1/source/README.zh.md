# 删去4秒后，跨轨交付还一致吗？

原创、纯离线、确定性规则教学。**不是模型/Agent效果评测，不执行剪辑软件，不读或生成任何媒体。** 所有输入是自写文字占位，只有JSON时间坐标。本课自编契约不是WebVTT、SRT、OTIO或产品交换格式。SOURCE的来源声明仅教学记录，绝不是法律授权证据。

## 前提与安全边界

已有Python 3.10+，仅标准库，无pip、账号、key、网络或自动安装。安全文件读取依赖POSIX O_NOFOLLOW/O_NONBLOCK，缺失则退出2，不静默降级；当前作者实测平台见包外verification证据，不宣称所有Python/Windows/macOS兼容。不要提供真实媒体、个人信息或用户目录。

CLI只读固定fixtures/source.json、edit.json和显式指定的提交常规文件，输出stdout。拒绝最后路径分量symlink、FIFO/设备；非阻塞open和lstat/fstat检查；单文件最多65536字节，深度/字段/类型/数值/字符串限制见CONTRACT。上级目录须由学习者控制；这不是恶意文件系统、源码篡改或特权对手的沙箱。字符串不是指令，不执行其中的路径、网址或代码。不要把输出重定向覆盖输入。

## 5步学习

1. 读source表：24秒项目删去原[8000,12000)，目标20秒。左闭右开，整数毫秒，速度恒为1，无转场或变速。
2. 复制`fixtures/submission-template.json`到新文件`my-submission.json`。依CONTRACT手填四轨。S2仅留原镜头后4秒；C2删除；M1需两个源时间不连续的片段。k1/k2指保留窗，不是幸存片段重新编号。
3. 先运行固定坏例，对照主因与派生码，再修自己的提交。交付摘要使用CONTRACT明确的完整track对象规范化SHA；只重算摘要不能掩盖错误时间/源身份。
4. 对照作者答案`submission-good.json`与独立手算`expected/HAND_ORACLE.r3.json`，再运行所有golden和测试。作者答案不是模型生成结果。
5. 理解结构pass仍有8000ms接点待观看/试听。本课没有音频或画面，因此人工音画验收始终not_performed，不捏造已观看或版权已清除。

```sh
python3 -B lab.py validate --submission fixtures/submission-F07b.json
# 退出1：SHOT_COVERAGE_GAP主因；目的区间及长度不一致为derived
python3 -B lab.py validate --submission fixtures/submission-F08.json
# 退出1：存活C3文本被改，TEXT_CHANGED
python3 -B lab.py validate --submission fixtures/submission-good.json
# 退出0：结构规则pass，但publish_allowed始终false
python3 -B lab.py validate --submission my-submission.json
python3 -B lab.py check-golden
python3 -B -m unittest discover -s tests -v
```

模板故意缺少片段，运行会失败；不提供默认approve或自动修复。项目/轨道/清单revision必须完整写`paper-demo-r2`。必须自己阅读规则完成填表，模板不是一键正确答案。

## 失败与退出码

expected/cases.json预先从冻结r3契约写出24项期望（good+23坏），非生产validator自生期望。每个非F09坏例先做指定变异，再统一重算交付摘要；F09特意保留旧音乐摘要。F01至F12子例涵盖字幕未平移/漏删、源区间错、音轨丢段、旧图卡版号、1ms空洞、文本漂移、摘要旧、重复/未知ID、额外轨、非法数值及JSON等。

F13只在纯函数测试中构造跨剪口字幕，必须返回CAPTION_EDIT_REQUIRES_AUTHORING，不自动拆字；CLI没有--input或--edit参数。F14在测试临时副本同时篡改固定题目与提交，必须FIXED_FIXTURE_MISMATCH，不能同步改答案通关。原source/edit文件字节随包保留；允许语义不变空白变化，但报告原始字节SHA会变。

退出0=本课结构校验通过；1=内容/规则失败；2=参数/文件/JSON/schema无效。JSON报告固定publish_allowed=false、media_rendered=false、human_av_review=not_performed、legal_clearance=not_assessed；无批准、发送或发布状态机。CLI缺参数或非法参数由argparse向stderr写用法并退出2。SHA仅做版本和字节一致性，不是签名或真实性证明。

## 包与复验

```sh
python3 -B package_lab.py --out ../my-new-package
```

父目录须已存在、输出目录必须不存在。仅固定作者允许成员，无用户提交、缓存、日志或个人路径。固定ZIP_STORED、时间戳/权限/排序。输出ZIP和逐成员SHA256.json。另建新目录重复打包应字节相同；拒绝覆盖已有输出目录。测试只在临时目录写合成文件并清理；F14需要临时副本，绝不篡改本目录。打包是本地制品，不是互联网发布。

CONTRACT保留批准实施前的设计文案，表示规则来源而非当前测试结果。执行结果只看包外verification中带退出码/平台的日志与manifest。README不把预计测试说成已运行。

## 不保证什么

结构时间正确不保证剪辑自然、对白不断词、音量正常、画面可读、可访问性合规、版权授权或真实产品兼容。没有媒体解码/监听/渲染、ASR、模型调用、SDK、收费或外发。需要这些能力时停止本课，另行明确范围与授权。
