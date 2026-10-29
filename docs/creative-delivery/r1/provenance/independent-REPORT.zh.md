# 创意删段交付练习：独立实现QA r1

## 结果

**accept_scoped_implementation：0个发现的阻断。** 只接受本次冻结的原创合成JSON实验室实现；不授权canonical接入、网站部署、媒体交付或发布。

- 独立CLI：**50/50**（包含good、F01–F12全部子例及额外负测）。
- 独立补充：**1394/1394**，其中345个区间×4轨=1380项逐毫秒oracle检查；其余为非法区间、同步换题、原始SHA、缺平台能力失败关闭。
- 解包后的作者测试：**25 unittest PASS**；**24 golden PASS**。这些是额外回归证据，不替代独立oracle。
- 两次新目录打包一致、等于冻结ZIP；拒覆盖已有目录，新增未列合成提交/缓存不进入包。
- 55项冻结制品SHA核对；36个ZIP成员逐项检查后独立解包，无.git。执行后作者冻结制品与解包文件字节均不变。

## 精确输入身份

|输入|SHA256|
|---|---|
|`creative-delivery-lab-implementation-r1/FINAL_FREEZE.json`|`c675b4abef76926276b9a1ac05d914e3eba288633a5cc8fe90a5aec31d0fb8bc`|
|`package-a/creative-delivery-lab-r1.zip`|`c1cdcd93b0cee224d76bc589d5622840e3030409da82ea3973e927a8e3049cbf`|
|r3权威CONTRACT|`4159c5c4a399a1e2eabd47b99429d982e7ba2c3a238eff4db07d10e98231568b`|
|独立手算HAND_ORACLE.r3.json|`2e5f306a8e6a8b198d74ec8f036d3a3633176835f09e9f92ec3b9e694d6241c8`|

作者FINAL_FREEZE之后才运行代码，运行位置为本QA目录下`unpacked/creative-delivery-lab`。23:54恢复提示后先读取现有IDENTITY/CLI结果，保留首轮50例日志，没有重复未需重跑的动作。

## 独立性与数学正确性

独立CLI的good由先前手算oracle组装，edit对象独立写出，摘要只按冻结域做标准JSON/SHA256，不导入生产validator/expected。所有坏例在执行前按r3预先定义，并统一重绑摘要，唯F09故意替换旧摘要。

补充oracle逐个枚举 `[start,end)` 内整数毫秒单元，以窗标签分组，求其首尾单元和资产对应位置；不复用生产max/min区间求交。固定随机种子20261028，10个边界值全部正长成对组合45组，再加300组随机区间；四轨均测试。caption跨窗根据逐单元标签集合独立分类为需创作。测试0/8000/12000/24000及相邻1ms、全删、跨两窗、源偏移、k1/k2命名、长度守恒、文本/源身份保留及输入不被修改。

固定10个目标fragment与独立oracle一致。S2源[4000,8000)、音乐后段[12000,24000)得到正确目的位置；另测M1错源[8000,20000)保持同长度仍拒，S2已知错asset-s3仍拒。没有仅按总时长通过。

## r3失败组与归因

- F01–F12所有子例：退出码、完整primary集合和derived集合均符合冻结契约；报告错误字段shape、primary cause=null、derived cause指向本报告主因均检查。
- F07b准确1ms gap：主因SHOT_COVERAGE_GAP，目的与长度为derived；F07a缺条目只MISSING_FRAGMENT。
- F06a旧图卡越目标片尾：OUT_OF_BOUNDS主因、目的差异derived。F05源长16秒对目的12秒：SOURCE_INTERVAL_MISMATCH主因、长度derived。
- F09旧音乐摘要仅TRACK_DIGEST_MISMATCH；另有普通提交语义变更+陈旧摘要，摘要正确归于早先TEXT_CHANGED。
- F13只纯函数验证跨剪口字幕；CLI --input/--edit参数均退出2，未开放固定题目替换。
- F14使用本QA自己的合成副本测试source+submission、edit+submission、三者同时变更，均FIXED_FIXTURE_MISMATCH退出2；只改source/edit空白则通过且raw摘要标识实际bytes。没有修改生产信任根。

## 有界读入、安全与边界

已执行：UTF-8非法/BOM、重复key、NaN/Infinity、未知path/URL字段、bool/负数/float、零长/越界、深度9和20000、超长文本、65536字节恰好接受与65537拒绝；symlink/FIFO/目录/不存在文件均在4秒超时门限内终态拒绝。缺O_NOFOLLOW能力模拟后失败关闭；作者解包测试还覆盖身份替换和读取中变更。有限读取实现审查确认先常规文件/身份检查、非阻塞无跟随open、最多limit+1读取、同一bytes解析与哈希、读取后stat再核对。

静态审查`lab.py/contract.py/timeline.py/package_lab.py`：仅标准库及同包模块，无网络调用、输入内路径解析、eval/exec或动态用户import。未知path/URL作为schema额外字段拒绝；指令文本仅TEXT_CHANGED且不执行。设备文件拒绝依据常规文件检查代码审查，未打开真实设备做实测；不宣称抵御敌对上级目录或可修改执行代码的攻击者。

所有被测试常规JSON报告中固定mode/technical_status及publish_allowed=false、media_rendered=false、human_av_review=not_performed、legal_clearance=not_assessed；bool类型也检查，不接受数值0冒充false。CLI_USAGE按契约仅stderr用法/退出2，不输出JSON；消费端不得把缺JSON当通过。包工具只有本地打包，不代表媒体或法律验收。

## ZIP与复现

36成员无重复、绝对路径、`..`、反斜线或.git；均常规文件，固定2020-01-01时间戳、排序，内容逐项匹配冻结manifest。仅提取到新的QA目录。包内无作者fixture写入工具，学习者提交/缓存/日志不进包。

在解包代码上实际运行unittest、check-golden、good/bad CLI、参数拒绝；随后生成两包，第二包前加入QA合成未列文件仍保持原ZIP SHA，拒绝覆盖已有输出目录。9条命令全部达到预期退出码，原输入不变。

## 证据位置

- `IDENTITY.json`：55文件与36 ZIP成员身份。
- `independent_cli_qa.py`、`execution/RESULTS.json`、`execution/*.json/*.stdout/*.stderr`：独立输入原bytes及每例输出。特殊文件保留为QA symlink/FIFO/目录，manifest不尝试读取它们。
- `independent_math.py`、`supplemental_qa.py`、`supplemental/RESULTS.json`：1394检查；F14各副本及报告保留。
- `reproduce/RESULTS.json`、`reproduce/*.stdout/*.stderr`：精确命令、退出码、Python/OS、包复现与只读证据。
- `EVIDENCE_SHA256.json`：证据常规文件SHA和特殊文件类型记录。

实测环境：Python 3.12.14，Linux 6.18.55 x86_64/glibc2.41。Windows/macOS、其他Python版本、GUI/网页/移动端、真实字幕格式、媒体质量、版权/法律/无障碍、厂商模型效果均**never-run / 不在范围**。未读取真实用户素材、调用模型/SDK/第三方、访问Mac、修改canonical或发布。
