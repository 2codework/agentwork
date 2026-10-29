# AgentWork ZCode：两个独立产品目录与八项岗位手册

**状态：multiple_distinct_products_catalogued。generic alias zcode为ambiguous，不设默认，不推断用户选择。**

所有输入/参考输出为作者原创合成；product_execution=not_run。内容许可待负责人确认保持不变。仅资料和离线fixture验证；不是全部版本和全部功能全集。

## 身份与版本
智谱/Z.ai ZCode（zai-zcode）：桌面3.16.3；源码README 3.16.2；GitHub Releases渲染3.14.3，不能混用渠道。
Amir Hayek Zcode（amir-hayek-zcode）：0.28.0 beta，macOS Tahoe26.2+，需完整Xcode；面向Apple原生应用，未提供内置源码编辑器，外部Agent/Skill接入。仅身份卡完成，教程待补，不计入八项。

先读GETTING_STARTED.md。fixtures各目录input是完整输入；reference是作者参考，不是产品输出。

## 智谱/Z.ai ZCode｜开发者：修复退款金额边界

让订单退款函数不因超额/负数产生错账；只模拟整数分。

输入：`fixtures/refund-fix/input`；参考：`fixtures/refund-fix/reference`

### 原创任务提示
```text
阅读@refund.py和@README.md。修复边界，保持函数名。补test_refund.py覆盖正常、零额、刚好全退、超额、负数、浮点、布尔。不要接支付接口。输出rationale.md记录变更理由。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. 在输出目录运行 python -m unittest -v；所有8个子场景均覆盖。
2. diff只涉及refund.py、test_refund.py与rationale.md；无网络/支付调用。
3. 负例：bool、浮点、负金额、超额都必须ValueError；不能为了通过而把无效输入截为0。

### 人工rubric
1. 0-2分：规则与异常类型准确；满分覆盖bool陷阱。
2. 0-2分：测试断言输出而非只检查无报错；总分至少3且无越权。

### 失败恢复
1. 若现有环境没有Python则标blocked，不安装。
2. 测试失败先复制traceback，按单个边界修复；不要更改需求以迎合实现。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜产品经理：需求拆成可验收开发规格

把含糊的预约取消规则交给研发，避免擅自决定争议项。

输入：`fixtures/pm-spec/input`；参考：`fixtures/pm-spec/reference`

### 原创任务提示
```text
依据@brief.md编写spec.md和acceptance.json。只做开发规格，不冒充订单系统执行。显式列出时区与管理员权限待决；验收包含24小时等于边界、提前23小时59分、重复取消和名额释放。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. acceptance.json可解析，恰有A1-A4且A1/A2结果不同。
2. spec.md明确时区、管理员待决，不填假结论。
3. 负例：A2不得全退；A3不得二次退款/再次释放席位；未知时区和管理员例外不得自动定案。

### 人工rubric
1. 0-2分：Given/When/Then能让QA写测试。
2. 0-2分：退款失败/重复请求有讨论但不偷增已批准需求；>=3通过。

### 失败恢复
1. 如果模型自行选UTC，要求移到假设并保留阻塞，不把假设称已确认。
2. 规则冲突时只列冲突及决策人，不生成生产策略。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜测试：为优惠券函数建立回归集

让测试发现门槛比较错误，而不是机械覆盖代码。

输入：`fixtures/qa-boundaries/input`；参考：`fixtures/qa-boundaries/reference`

### 原创任务提示
```text
读取@coupon.py与@rules.md。只创建test_coupon.py与bug.md，使用unittest表驱动三个边界。运行前说明预期10000会失败。记录bug.md含期望/实际/最小复现，不能修代码或把失败改绿。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. python -m unittest -v应非零退出，10000子场景失败；这是练习预期，不是产品失败。
2. coupon.py内容必须与input逐字一致。
3. 负例：原实现10000返回10000，测试必须失败；把期望改成10000或改coupon.py均判不通过。

### 人工rubric
1. 0-2分：测试由业务规则而非错误实现推导。
2. 0-2分：bug能复现且不夸大影响范围；>=3通过。

### 失败恢复
1. 若全部通过，检查是否擅改源文件或错误期望，恢复input后重跑。
2. 若导入失败，核对工作目录，不将环境失败记为业务缺陷。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜数据运营：离线汇总订单CSV

审计口径一致地计算已支付销售额，并隔离坏数据。

输入：`fixtures/ops-csv/input`；参考：`fixtures/ops-csv/reference`

### 原创任务提示
```text
为@orders.csv写stdlib Python summarize.py。输出summary.json与errors.csv，坏数据不按0默默吞掉。不要用云表格、数据库或pip。脚本应在重复执行时覆盖同名输出而非追加翻倍。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. 运行python summarize.py两次，summary.json解析为paid_count=2,revenue_cents=2000。
2. errors.csv仅一条O4；原始orders.csv哈希不变。
3. 负例：O2取消不计收入；O4非法金额不得默默计0；第二次运行不增行、不翻倍。

### 人工rubric
1. 0-2分：金额用整数分且不含取消订单。
2. 0-2分：错误隔离/重复运行/输入不变均明确；>=3通过。

### 失败恢复
1. CSV列缺失应停下报告schema不符，不能猜列。
2. 写权限失败改输出到获准的新目录，不chmod生产路径。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜设计交接：令牌规格落地静态卡片

把设计参数落实成可评审HTML，不声称能直接编辑Figma。

输入：`fixtures/design-handoff/input`；参考：`fixtures/design-handoff/reference`

### 原创任务提示
```text
按@tokens.json与@brief.md生成独立index.html。按钮用原生button和可见focus样式。点击后显示已预约并disabled，此为纯本地演示不是实际下单。附handoff.md逐条对应设计要求和人工核查项。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。
5. 本地工作区HTML右键Open in built-in browser；本任务不导入Chrome数据、不上传文件、不访问真实订单页。

### 客观验收
1. 静态检查存在lang、viewport、button、role=status、focus-visible；没有http外链。
2. 浏览器人工在320×700、1280×800检查；Tab→Enter→重复点击：只出现一次状态，不产生网络请求。
3. 负例：重复点击不重复状态；禁止远程请求；无可见键盘焦点或320px横向溢出即不通过。

### 人工rubric
1. 0-2分：层级清楚、文本不截断。
2. 0-2分：焦点/禁用/演示标记清楚；>=3通过且键盘路径必过。

### 失败恢复
1. 如果浏览器控制禁用：Settings → Browser开启后新建任务；旧会话不沿用开关。
2. 如果仅源码检查，不填视觉通过；人工另开页面验收。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats), [zai-browser](https://zcode.z.ai/en/docs/browser-use)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜技术写作：从真实CLI同步README

修复文档漂移并给新同事可复制的离线例子。

输入：`fixtures/docs-maintenance/input`；参考：`fixtures/docs-maintenance/reference`

### 原创任务提示
```text
依据@tool.py修订@README.md。先查看argparse定义，写准确命令、期望输出、漏参数报错和依赖说明。不要为迎合旧文档给代码新增--user，不修改tool.py。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. python tool.py --name Ada的stdout恰为Hello, Ada!换行。
2. python tool.py退出码2；tool.py不变；README不再推荐--user。
3. 负例：缺--name非零；--user Ada必须拒绝；不得为旧文档兼容而擅改代码。

### 人工rubric
1. 0-2分：说明能直接复现。
2. 0-2分：错误路径与版本边界清晰，无虚构安装依赖；>=3通过。

### 失败恢复
1. 若文档与运行矛盾先保留命令/退出码，辨别python解释器和cwd。
2. 不把本机路径或用户名写进公开示例。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜安全评审：路径穿越风险与修复计划

在本地合成片段中找出越界风险，输出可追踪评审，不跑攻击。

输入：`fixtures/security-review/input`；参考：`fixtures/security-review/reference`

### 原创任务提示
```text
对@download.py做静态安全审阅，生成review.json与fix-plan.md。风险要引用函数/行和不受信输入到文件读取的路径，给无攻击执行的合成测试建议。不要读/etc或任何真实敏感目录。区分确认的代码缺少检查与未经验证的线上可利用性。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. review.json含SEC-1、download.py、line=3；明确production_exploitability=not tested。
2. download.py不变；无敏感文件读取或网络命令。
3. 负例：只做字符串startswith或忽略symlink风险的方案不能判完整；线上可利用性不得写已证实。

### 人工rubric
1. 0-2分：源到sink路径准确，不用危言耸听替代证据。
2. 0-2分：包含symlink/竞态残余风险与测试建议；>=3通过。

### 失败恢复
1. 若Agent想读取真实敏感文件立即Reject，改为临时目录测试设计。
2. 若输出称已修复，要求改成未实现计划并核diff。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 智谱/Z.ai ZCode｜交付负责人：本地变更生成发布评审包

明确哪些变化可交付、哪些阻塞，不自动提交或部署。

输入：`fixtures/release-gate/input`；参考：`fixtures/release-gate/reference`

### 原创任务提示
```text
根据@changes.json与@policy.md写发布说明和gate.json。说明面向用户，闸门面向工程；准确反映C2未测，因此整体blocked。不能把C1通过推广为全量通过，不能生成实际git提交/发布动作。
仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。
```

### 操作路径
1. 完成GETTING_STARTED.md前置检查，将input目录复制为独立练习工作区；不要把reference给Agent。
2. 在ZCode选项目目录，新建任务，用@引用本项输入文件；按复杂度选Plan或Ask before changes。
3. 粘贴本项原创提示，先审计划；仅对列明路径的修改和离线检查逐次Allow，越界Reject。
4. 在工作区文件树预览输出；把实际结果与本项检查、reference和人工rubric比较，不能用Agent自述代替检查。

### 客观验收
1. gate.json decision=blocked, blocking_ids=[C2], published=false。
2. release-notes明确C1的pass来自输入记录，而非Agent独立实测。
3. 负例：存在not_run的C2不得ready/published=true；不得把输入测试记录写成独立实测。

### 人工rubric
1. 0-2分：用户影响描述准确，不夸张收益。
2. 0-2分：阻塞项、下一步与发布授权边界完整；>=3通过。

### 失败恢复
1. 若报告写ready，返回policy逐条重判。
2. 如果缺测试日志，保留not_run，不补造时间戳或截图。

权限：仅编辑当前合成练习目录；不联网、不装依赖、不访问凭据、不提交不推送不发布。任何命令先展示完整命令和工作目录。失败时保留错误证据，不以跳过测试制造通过。

成本：练习只处理小型合成输入；先查看Usage Stats与所选模型通道额度。设两轮修正上限，超限暂停复盘，不自动升级套餐或换收费通道。额度/价格以账户即时页面为准。

隐私：输入均为作者合成。模型可能接收上下文；不上传真实客户、仓库秘密或浏览器登录态。不把本地工作区等同数据不出设备。

状态：未运行产品；作者参考输出。适用版本：桌面文档快照2026-10-29；下载页3.16.3；UI可能跨版本变化，未运行该版本。

来源：[zai-agent](https://zcode.z.ai/en/docs/agents), [zai-task](https://zcode.z.ai/en/docs/task-management), [zai-safety](https://zcode.z.ai/en/docs/safety-confirm), [zai-models](https://zcode.z.ai/en/docs/configuration), [zai-usage](https://zcode.z.ai/en/docs/usage-stats)；checked_at 2026-10-29。

## 覆盖缺口
- Amir Hayek Zcode仅身份/能力/版本限制已收录，尚无完整岗位手册。
- 未覆盖Z.ai所有历史版本、远程、Bot、MCP、插件市场和多代理配置。
- CRM/ERP/邮件/日历/在线表格的原生集成未核验；相关岗位这里只做开发规格、离线数据脚本、静态原型和仓库文档，不冒充办公系统全流程。

## 一手来源（16）
- [zai-company](https://www.zhipuai.cn/zh)：智谱官网产品列表链接 zcode.z.ai，关联品牌 Z.ai。
- [zai-home](https://zcode.z.ai/en)：ZCode 官方产品入口。
- [zai-repo](https://github.com/zai-org/ZCode)：仓库自述为 Z.ai coding agent harness，链接 zcode.z.ai。
- [zai-readme](https://github.com/zai-org/ZCode/blob/main/README.en.md)：README 更新记录 2026-10-19 v3.16.2；桌面、浏览器、终端界面。
- [zai-releases](https://github.com/zai-org/ZCode/releases)：本次渲染最新标签为 v3.14.3；不等同桌面分发最新。
- [zai-changelog](https://zcode.z.ai/en/changelog)：桌面 changelog 3.16.3，2026-10-23；与源码渠道版本分开记录。
- [zai-install](https://zcode.z.ai/en/docs/install)：当前下载3.16.3；macOS Apple Silicon/Intel，Windows x64/ARM64，Linux x64/ARM64。
- [zai-welcome](https://zcode.z.ai/en/docs/welcome)：官方定位为开发环境，规划、编码、调试和验证。
- [zai-agent](https://zcode.z.ai/en/docs/agents)：工作区、文件引用、AGENTS.md、执行模式等文档。
- [zai-task](https://zcode.z.ai/en/docs/task-management)：任务和文件管理文档。
- [zai-safety](https://zcode.z.ai/en/docs/safety-confirm)：安全确认文档；不把文档描述视作实测安全保证。
- [hayek-home](https://zcodeapp.com/)：官网署名 Amir Hayek，0.28.0 beta，Mac上开发Apple平台应用，需完整Xcode。
- [hayek-releases-repo](https://github.com/hayek/Zcode-releases)：官网Download指向该发布仓库的0.28.0安装包；仅阅读发布仓库，未安装。
- [zai-models](https://zcode.z.ai/en/docs/configuration)：模型连接与套餐边界；Coding Plan仅编码场景。
- [zai-browser](https://zcode.z.ai/en/docs/browser-use)：内置浏览器限桌面；可打开本地HTML；目前不支持文件上传。
- [zai-usage](https://zcode.z.ai/en/docs/usage-stats)：App Usage与Coding Plan两类用量口径不同。
