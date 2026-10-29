# 版本 1.0 数据契约

`index.json`：schema_version / books（相对产品包入口路径）/ tasks（相对任务路径）/ research_queue（未接纳身份目录）。构建产生 `product-books-data.json`，只汇总已接纳条目，不改旧 data.json。

产品包：`{schema_version:"1.0", product:{product_id,vendor,name,display_name,status,version_scope,sources}, recipes:[...]}`。

基础任务或业务配方共同字段：task_id（配方可null）、product_id（基础题null）、title、role、business_goal、input_artifacts（path/sha256/description）、prompt、steps（title/instruction/check/failure_recovery）、expected_output_origin（固定author_reference）、expected_output、objective_checks（声明式列表）、human_rubric、authorization、cost、privacy、version_scope、sources、evidence_tier、product_execution（当前只允许not_run）、observed_results（当前固定null）。配方另有recipe_id。

文本字段非空字符串；参考输出可对象/文本；客观条件和人工量表可字符串或描述对象，不执行任意表达式。产品来源为{id,title,url,accessed_at,claim_scope}，HTTPS无用户口令。evidence_tier仅documentation_review或synthetic_contract。当前验证器有意拒绝实测声明；今后实测记录需经独立设计与审阅后接入，不能靠改枚举绕过。

基础任务固定检查用JSON类型敏感的规范化等值，拒绝重复键、NaN与Infinity、超过1MB提交；没有任意代码执行。构建时路径检查拒绝绝对、父路径、反斜杠、冒号及符号链接。基础题的独立ID不能与旧案例source ID混用。

运行与格式字段：runner_implemented=false 表示真实产品调用适配器未实现；reference_format 描述本包作者参考格式，expected_product_artifact_format 描述业务目标成品格式，两者不保证相同。JSON语义参考通过不能算docx/xlsx/pptx文件合格。

## r2 严格接纳与发布库存

`index.json.publication_files` 是除 index.json 本身以外的**完整、显式**产品书文件路径→SHA-256 映射。发布前先遍历全部源目录，用 lstat 拒绝所有文件/目录符号链接、非普通条目以及符号链接祖先；实际文件集合必须与登记集合完全相等。未知普通文件也拒绝，不会被顺便打包。仅验证后的字节进入公开目录及ZIP。发布器不自动更新库存；只有root在审阅明确文件清单后更新。此设计面向静止可信工作区，不宣称能抵抗并发恶意文件置换。

`objective_checks` / `human_rubric` 每项必须为非空文字或严格描述对象：普通描述为 id/description（可有kind）；人工量表为 criterion/points/how_to_check，points为非负有限数字而非bool。兼容声明式条件 human_fact(id/type/expected/source)、human_count(id/type/expected文字)、set_equals(id/type/target/expected非空数组)、group_sum(id/type/target/expected有限数值对象)。它们仅是**待验收条件**，尤其human_fact/human_count不是自动通过。框架不计算产品分数；产品原包的完整性门槛不能被分数替代。

参考顶层只接受非空对象或非空文字，拒绝null/bool/数组/数字。steps、artifacts、sources及research_queue逐层校验。日期可为合法 YYYY-MM-DD 或含时区的ISO时间戳；不截断原时间戳。

共享任务映射要求 recipe.task_contract_sha256 等于基础任务和该recipe各自计算出的契约摘要：输入SHA顺序、business_goal、作者参考及其格式、目标产物格式、客观条件、人工量表、参考文件SHA。此为精确JSON契约绑定，不声称自动理解自然语言语义。产品专属prompt、步骤、权限与版本不进入摘要，因此可以有不同产品操作。未精确匹配或未经映射审阅必须 task_id=null，不得仅填写一个现有ID。

规范化参考链接兼容 expected_output.files/example_files/reference_files、顶层reference_files及patch_path/fixture_path。每个路径限于已登记包内部；合并到 expected_output_artifacts 的新增path/hash链接不会删改原字段。原始product-book文件及丰富provenance、structured_details、source_recipe均保留；可读摘要不能替代它们。

## r3 手册与真实接纳资料

已接纳4产品32业务配方、5份完整原始手册，以及3项独立身份目录。计数互相独立，旧138案例与4基础契约不相加为独立产品成绩。index.guides逐项登记product_id/path/sha256/title/checked_at/source_scope/source_ids，正文由原始UTF-8字节读取，不删减；只用安全Markdown子集与结构化文字显示，不解析HTML或执行代码。源文件原字节和全部额外字段保持可下载。

criteria的id允许字母数字、连字符、下划线（非产品ID）；声明式human_fact可带source位置，缺省时仍为待人工判断的条件，不能当已核验事实或自动通过。允许同名产品身份分开目录，教程待补条目不计为已交付书。

原始WPS包有5个故意非法JSON解析器测试文件。scripts/product_negative_fixtures.py以精确路径/SHA/拒绝理由闭合登记，公开两副本共10项expected-invalid，不算有效JSON。普通JSON仍严格拒绝重复键、NaN、Infinity及正负指数溢出（有限科学计数法保留）；原有创意练习3类/6副本的例外登记及其检查函数保持不变。

## r4 可读导航层（不改研究原文）

`editorial-navigation.json` 单独登记32项角色显示映射和13项手册路由。每个role_tags数组用原role全文及SHA绑定，display_role仅为简短展示；原role及原产品包不变。QA统一归入“测试”，同一配方可有多角色匹配，但结果按配方唯一计数。手册路由仅允许已登记、已哈希、属于该产品的相对路径，映射至实际recipe ID或guide锚点；拒绝父路径、编码绕行、协议、未知文件。原手册链接文字与源文件保留。

产品专用Markdown子集只把可信路由解析器返回的已知本地链接变为导航，不改变旧学习区reader.js；HTTPS来源保持原限制。章节使用默认关闭的原生details和分级目录，当前章节及“先读入门/直接选任务”入口始终可见。离线DOM测试不声称实际手机布局、真实键盘或浏览器历史验收。
