# r3冻结契约：实现与独立QA共同输入

此文件在与PLAN不一致时优先。仅设计，无生产实现或测试结果。所有时间为毫秒、左闭右开。本课没有媒体文件。

## 固定完整源表与独立手算目标

project_id=`paper-demo`；source revision=`paper-demo-r1`；目标revision=`paper-demo-r2`。track_id固定为shots、captions、music、graphics。文字均为原创占位内容。下表`原时间→源时间`：

|track|item_id|asset_id|原timeline|source|text|
|---|---|---|---|---|---|
|shots|S1|asset-s1|0,8000|0,8000|纸圆进入|
|shots|S2|asset-s2|8000,16000|0,8000|方块转动|
|shots|S3|asset-s3|16000,24000|0,8000|两者停下|
|captions|C1|asset-c1|1000,3000|0,2000|纸圆来了。|
|captions|C2|asset-c2|9000,11000|0,2000|方块转身。|
|captions|C3|asset-c3|13000,15000|0,2000|两者并排。|
|captions|C4|asset-c4|21000,23000|0,2000|停在这里。|
|music|M1|asset-m1|0,24000|0,24000|原创音乐文字占位，不代表实际音频|
|graphics|G1|asset-g1|0,4000|0,4000|纸圆与方块|
|graphics|G2|asset-g2|18000,22000|0,4000|练习结束|

所有资产表条目分别是`{asset_id, provenance_kind: synthetic_fixture, description: 上表text}`。资产文本与条目文本相同，无授权字段。源文件所有值须匹配代码内常量，不能把可改sidecar当信任根。

固定edit：edit_id=`cut-middle-4s`；from_revision=`paper-demo-r1`；to_revision=`paper-demo-r2`；remove_start_ms=8000；remove_end_ms=12000；target_duration_ms=20000。

独立手算期望（原ID/asset/text继承上表；不得运行生产变换函数生成该真值）：

|track|fragment_id|original_id|dest_start,end|source_start,end|
|---|---|---|---|---|
|shots|S1.k1|S1|0,8000|0,8000|
|shots|S2.k2|S2|8000,12000|4000,8000|
|shots|S3.k2|S3|12000,20000|0,8000|
|captions|C1.k1|C1|1000,3000|0,2000|
|captions|C3.k2|C3|9000,11000|0,2000|
|captions|C4.k2|C4|17000,19000|0,2000|
|music|M1.k1|M1|0,8000|0,8000|
|music|M1.k2|M1|8000,20000|12000,24000|
|graphics|G1.k1|G1|0,4000|0,4000|
|graphics|G2.k2|G2|14000,18000|0,4000|

总计10片段；C2完全删除。S2仅留下原镜头后4秒。音乐源坐标在接点从8000跳至12000，不能由结构正确推断声音自然。

## 完整字段schema（无可选字段、无额外键）

通用：所有容器嵌套≤8、每对象键≤16、每数组≤32；字符串≤256 Unicode码点；标识符长度1–48、ASCII `[A-Za-z0-9_.-]+`；SHA为64位小写十六进制；所有时间type精确为int（非bool），范围0–24000。单文件≤65,536字节，UTF-8无BOM。计数限额先于语义。

|对象|必填键及类型|
|---|---|
|source顶层|schema_version(string，固定creative-cut-source/1), project_id(ID), revision(ID), duration_ms(int), assets(array), tracks(array)|
|asset|asset_id(ID), provenance_kind(string，固定synthetic_fixture), description(string)|
|source.track|track_id(ID), items(array)|
|source.item|item_id(ID), asset_id(ID), start_ms(int), end_ms(int), source_start_ms(int), source_end_ms(int), text(string)|
|edit顶层|schema_version(string，creative-cut-edit/1), project_id(ID), edit_id(ID), from_revision(ID), to_revision(ID), remove_start_ms(int), remove_end_ms(int), target_duration_ms(int)|
|submission顶层|schema_version(string，creative-cut-submission/1), project_id(ID), revision(ID), edit_sha256(SHA), tracks(array), delivery(object)|
|submission.track|track_id(ID), revision(ID), fragments(array，≤16)|
|fragment|fragment_id(ID), original_id(ID), asset_id(ID), start_ms(int), end_ms(int), source_start_ms(int), source_end_ms(int), text(string)|
|delivery|revision(ID), edit_sha256(SHA), tracks(array)|
|delivery.track|track_id(ID), sha256(SHA)|

schema阶段只检查类型、键集合、通用大小与格式、每时间数值范围；**start<end、源目的等长、片尾范围、身份集合、重复条目、准确文本和轨道数量为语义阶段**，故F07不会先退出2。source/edit后续全值匹配内置信任根，任何内容变异退出2 FIXED_FIXTURE_MISMATCH。submission期待恰好4轨、每轨ID唯一；delivery也是4个对应轨道ID。固定资产10项仅存在source，不允许submission覆盖资产表。

规范化摘要函数契约：对既定JSON值用ensure_ascii=False、sort_keys=True、separators=(',',':')编码为UTF-8后SHA256；**数组顺序不排序**。edit_sha256覆盖完整edit对象；delivery.track.sha256覆盖对应完整submission.track对象（含revision），不含delivery。所有数组必须使用上表轨道/条目顺序，顺序差异报ORDER_MISMATCH，不静默归一。报告中的raw_input_sha256、raw_edit_sha256、raw_submission_sha256覆盖原始文件字节，与规范化摘要区别展示。source/edit空白变化可接受但原始摘要变化；字段内容改变不接受。

## 错误层级、独立oracle与单错规范

报告包含errors数组，元素只允许code、track_id（未知则null）、item_id（未知则null）、field（未知则null）、severity(`primary|derived`)、cause_id（primary为null）、error_id。ID按稳定排序生成E001…，不含用户全文。code和字段均白名单，不回显不可信ID。主排序为阶段、固定轨道顺序、原始条目顺序、code；derived紧随所属primary。包中expected仅为已评审人工oracle的序列化，不能调用生产validator生成后自己比较。

1. IO/JSON/schema：退出2，只报首个致命错误。码：CLI_USAGE、INPUT_IO、INPUT_NOT_REGULAR、INPUT_CHANGED_DURING_READ、INPUT_TOO_LARGE、INPUT_ENCODING、JSON_SYNTAX、JSON_DUPLICATE_KEY、JSON_NONFINITE、SCHEMA_DEPTH、SCHEMA_LIMIT、SCHEMA_KEYS、SCHEMA_TYPE、SCHEMA_VALUE。CLI_USAGE可用argparse stderr而无JSON，其余JSON输出。过深/过大在业务前停止。
2. source/edit契约不符：退出2 FIXED_FIXTURE_MISMATCH。
3. submission身份/集合：退出1；REVISION_MISMATCH、PROJECT_MISMATCH、EDIT_DIGEST_MISMATCH、MISSING_TRACK、UNEXPECTED_TRACK、DUPLICATE_ID、UNKNOWN_ASSET、MISSING_FRAGMENT、REMOVED_ITEM_RETAINED、UNEXPECTED_FRAGMENT、ORDER_MISMATCH、DELIVERY_TRACK_SET_MISMATCH。非法重复ID停止该轨逐条比较；缺失片段不再报告它造成的gap。C2.k1/C2.k2作为已删原ID均只报REMOVED_ITEM_RETAINED。
4. 镜头覆盖：完整预期片段集合且唯一时检查。SHOT_COVERAGE_GAP/SHOT_COVERAGE_OVERLAP为primary；同一条目造成的DEST_INTERVAL_MISMATCH及SOURCE_DEST_LENGTH_MISMATCH列derived。其他轨间重叠不作一般禁止；本课仍按精确预期区间校验。
5. 逐条值：SOURCE_ID_MISMATCH同时适用于已知但不匹配的original_id与asset_id，以field区分（例如S2.k2引用已存在的asset-s3仍必须失败）；未知asset_id先报UNKNOWN_ASSET并抑制同字段身份比较。其余码为SOURCE_INTERVAL_MISMATCH、DEST_INTERVAL_MISMATCH、TEXT_CHANGED、INVALID_INTERVAL、SOURCE_DEST_LENGTH_MISMATCH、OUT_OF_BOUNDS。源区间错误导致长度差异时长度码derived于源错误；目的区间错误同理。零长/倒序以INVALID_INTERVAL为primary并抑制该条目数值比较派生噪声；超过目标片尾以OUT_OF_BOUNDS为primary、DEST_INTERVAL_MISMATCH为derived。
6. delivery摘要：TRACK_DIGEST_MISMATCH。若轨道有先前primary，则摘要差异为derived且cause引用该轨最早primary；否则为primary。摘要永不代替语义比较。delivery自身revision/edit字段分别按REVISION_MISMATCH/EDIT_DIGEST_MISMATCH，field含delivery前缀。

单错夹具统一由人工good副本变异指定字段/条目，**随后统一重算所有delivery轨道摘要**；只有F09最后故意将music摘要置为已定义r1音乐源track的规范化SHA。因此除F09外无stale digest噪声。重算摘要只是包装诚实绑定，不改变独立语义oracle。所有fixture预期先写，之后实现生产代码；不能看生产结果修改预期。

|fixture|精确变异|primary期望|允许derived|
|---|---|---|---|
|F01|C3.k2目的区间改13000,15000|DEST_INTERVAL_MISMATCH|无|
|F02|captions在C1后插入C2.k2，原ID C2、asset-c2、目的9000,11000、source0,2000、原文本|REMOVED_ITEM_RETAINED|无（集合失败不另报顺序）|
|F03|S2.k2源区间改0,4000|SOURCE_INTERVAL_MISMATCH|无|
|F04|删除M1.k2|MISSING_FRAGMENT|无|
|F05|M1.k2 source_start仅改8000，end24000|SOURCE_INTERVAL_MISMATCH|SOURCE_DEST_LENGTH_MISMATCH|
|F06a|G2目的改18000,22000|OUT_OF_BOUNDS|DEST_INTERVAL_MISMATCH|
|F06b|graphics.track revision改paper-demo-r1|REVISION_MISMATCH|无|
|F07a|删S2.k2|MISSING_FRAGMENT|无|
|F07b|S2.k2 start_ms仅改8001|SHOT_COVERAGE_GAP|DEST_INTERVAL_MISMATCH、SOURCE_DEST_LENGTH_MISMATCH|
|F08|C3.k2 text从“两者并排。”改“纸圆并排。”|TEXT_CHANGED|无|
|F09|仅music清单SHA置为r1 source music track的规范化SHA|TRACK_DIGEST_MISMATCH|无|
|F10a|在captions末尾复制完整C4.k2|DUPLICATE_ID|无|
|F10b|G1.k1 asset_id改asset-unknown|UNKNOWN_ASSET|无（不再逐字段比asset）|
|F10c|submission和delivery增加track_id=notes，revision=paper-demo-r2、fragments=[]且SHA正确|UNEXPECTED_TRACK|无（同一额外轨不另报delivery集合）|
|F11a/b/c|C1 start分别改true、-1、1.5|SCHEMA_TYPE/SCHEMA_VALUE/SCHEMA_TYPE，退出2|无|
|F11d|C1 end改1000|INVALID_INTERVAL|无|
|F11e|C4 end改20001|OUT_OF_BOUNDS|DEST_INTERVAL_MISMATCH、SOURCE_DEST_LENGTH_MISMATCH|
|F12|分别构造重复键、NaN、未知键、65537字节|JSON_DUPLICATE_KEY/JSON_NONFINITE/SCHEMA_KEYS/INPUT_TOO_LARGE，退出2|无|
|F13|纯timeline函数单测字幕7000,9000；不替换CLI源文件|CAPTION_EDIT_REQUIRES_AUTHORING|无；非CLI返回码|
|F14|临时复制题目后将C1源文本与提交同步改成“假文本”|FIXED_FIXTURE_MISMATCH，退出2|无|

F14只在测试隔离副本验证完整性；CLI没有--input/--edit参数，不能借此开放一般题目。测试修改源码中的信任根不在保证范围。F13算法错误为独立纯函数结果，不产生受支持CLI可运行fixture，页面必须注明。

所有正常JSON报告恒含schema_version=`creative-cut-report/1`、mode=`rule-simulation`、technical_status、publish_allowed=false、media_rendered=false、human_av_review=`not_performed`、legal_clearance=`not_assessed`、三项raw SHA（读不到为null）、errors、manual_checks=[`在8000ms剪口人工观看与试听；本课未执行`]。退出2 technical_status=invalid；退出1 fail；退出0 pass。不得产生approve、approved或真实发布许可字段。CLI_USAGE例外只发用法至stderr。

## 冻结与执行前门禁

r3由PLAN、CONTRACT、CHANGES三文档构成，SHA256.json列三者及恢复后的r1计划摘要；manifest不自哈希。实现者必须按冻结字节读取，遇歧义先反馈而非自行选择。独立QA须核对上述手算表、所有primary/derived预期和SHA后给出明确通过/待修；通过仅授权root决定是否进入实现，不表示测试通过。任何更改生成新版本并重算manifest，保留旧版本。
