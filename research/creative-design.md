# 设计Agent研究增量（独立待集成）

核验日：2026-10-28。13个合成教学流程、12个技术节点、21个官方来源。没有运行模型/API、登录账号、触碰私有素材、修改r1或远端。

## 先看结论

- Figma MCP不能一概描述为只读；远端写画布仍有beta及席位约束。
- Canva旧Connect入口已迁往统一SDK文档。Photoshop v1已被官方标deprecated；保留历史，新增工作指向v2。
- DTCG旧入口落到禁止用于实现的preview；固定2025.10正式版本，且不能称其为W3C标准。
- 自动出图、模板填充、API和MCP不是同义的“真agent”；本专题描述受控agent编排方案而非宣称工具自主工作。
- 所有端到端案例均未实测。unknown价格/许可/资格不能靠品牌知名度补齐。

## 仓库映射与证据边界

依据CONTENT_SCHEMA.md；cases保留必需字段与生命周期；新适配器尚未实现，不能声称可直接导入。
依据systems.json节点/edges/source结构；保留模型/工具/标准类型；新增type/category需未来适配器确认。
跨仓库关系均在JSON cross_repo_relations中，以稳定ID关联，不假装两仓库已经接受新增类型。所有新增流程为原创教学，不宣称行业最优。

## 共同权限与权利门

只用合成输入。后续执行需要用户批准环境、账号、资产、操作范围与预算；读取共享文件不等于获准上传模型。图像商用、再分发、字体、肖像和商标分别核验。生成模型不保证不侵权；凭证不替代授权。不得把第三方图片、权重或文档全文打包入仓库。

## 技术节点

### design-figma-mcp · Figma MCP设计上下文与写画布
- 分类：tool_interface。供外部agent读取设计结构并执行受控写入的接口，不是独立模型。
- 版本/生命周期：rolling remote MCP; write beta；current_documentation_reviewed（2026-10-28）。
- 费用：部分写入beta免费，正式计费将变化；草稿外写入有Full seat条件，具体额度unknown；准确价格unknown。许可：proprietary service; complete contractual license unknown。
- 边界：MCP工具可用不代表批准改写全部设计文件。
- 来源：[Figma MCP introduction](https://developers.figma.com/docs/figma-mcp-server/), [Figma access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)

### design-firefly-image · Firefly图像生成与编辑
- 分类：model_service。图像能力服务；agent负责选择输入、检查约束与失败恢复。
- 版本/生命周期：Image5 / rolling API；current_documentation_reviewed（2026-10-28）。
- 费用：商业API计费与合同unknown；本轮零调用；准确价格unknown。许可：proprietary; output rights depend on applicable terms。
- 边界：生成的产品外观与字样需要人工验证，不能直接当实拍。
- 来源：[Firefly API](https://developer.adobe.com/firefly-services/docs/firefly-api/), [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)

### design-photoshop-v2 · Photoshop API v2确定性编辑编排
- 分类：tool_service。模板、图层及智能对象工作流的服务节点；不是全部操作都由生成模型完成。
- 版本/生命周期：v2 GA；current_documentation_reviewed（2026-10-28）。
- 费用：商业服务合同与单价unknown；准确价格unknown。许可：proprietary service; complete license unknown。
- 边界：linked资源失效会破坏模板，不能只保存PSD而忽略依赖。
- 来源：[Photoshop API](https://developer.adobe.com/firefly-services/docs/photoshop/), [Photoshop guides and migration](https://developer.adobe.com/firefly-services/docs/photoshop/guides/)

### design-photoshop-v1 · Photoshop API v1历史工作流
- 分类：historical_tool。保留旧模板和接口迁移知识，不作为新接入首选。
- 版本/生命周期：v1 deprecated; announced EOL 2026-07-31；deprecated（2026-10-28）。
- 费用：历史合同unknown；准确价格unknown。许可：unknown。
- 边界：不能把旧教程原样用于v2。
- 来源：[Photoshop guides and migration](https://developer.adobe.com/firefly-services/docs/photoshop/guides/)

### design-canva-template · Canva模板数据填充与导出
- 分类：tool_service。结构化模板自动化；内容规划和审校是agent层职责。
- 版本/生命周期：unified SDK / REST rolling docs；current_documentation_reviewed（2026-10-28）。
- 费用：账号、模板资格、商业计划与单价unknown；准确价格unknown。许可：Canva content license by asset category; API terms unknown。
- 边界：设计导出成功不代表每种素材都能再分发或用于logo。
- 来源：[Canva REST APIs](https://www.canva.dev/docs/apps/rest-apis/), [Canva autofill](https://www.canva.dev/docs/apps/rest-apis/autofill-guide/), [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/)

### design-dtcg · DTCG设计token交换
- 分类：specification。跨设计工具与代码的语义变量交换；不是模型或agent。
- 版本/生命周期：2025.10 final；current_documentation_reviewed（2026-10-28）。
- 费用：公开阅读；工程集成成本unknown；准确价格unknown。许可：W3C Community Final Specification Agreement; not W3C Standard。
- 边界：旧draft URL会漂移，不可当稳定实现契约。
- 来源：[DTCG Format 2025.10](https://www.designtokens.org/TR/2025.10/format/), [DTCG preview warning](https://www.designtokens.org/tr/drafts/format/)

### design-wcag · WCAG 2.2验收标准
- 分类：standard。界面验收约束；模型可以辅助发现问题而不能认证合规。
- 版本/生命周期：WCAG 2.2 Recommendation 2024-12-12；current_documentation_reviewed（2026-10-28）。
- 费用：公开阅读；审计人力成本unknown；准确价格unknown。许可：W3C document rules; not asset license。
- 边界：无自动错误不等于完整通过，仍需键盘和辅助技术检查。
- 来源：[WCAG 2.2](https://www.w3.org/TR/WCAG22/)

### design-inkscape-trace · Inkscape位图描摹
- 分类：ordinary_tool。经典矢量化流程，可被agent安排但本身无自主规划。
- 版本/生命周期：guide 1.3; installed version unknown；current_documentation_reviewed（2026-10-28）。
- 费用：本轮未安装；发布包费用unknown；准确价格unknown。许可：unknown。
- 边界：描摹不是原始曲线恢复，复杂照片不适合直接转logo。
- 来源：[Inkscape Beginners Guide: tracing](https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html)

### design-slides-api · Google Slides结构化排版
- 分类：tool_interface。把批准内容写入可编辑页面元素；API不是审美决策模型。
- 版本/生命周期：API v1；current_documentation_reviewed（2026-10-28）。
- 费用：配额、账号与收费unknown；准确价格unknown。许可：proprietary service; asset rights separate。
- 边界：文本框写入成功不表示无溢出，必须检查渲染结果。
- 来源：[Google Slides API](https://developers.google.com/workspace/slides/api/guides/overview)

### design-visual-regression · Playwright视觉回归
- 分类：evaluation_tool。基线截图对比帮助检测布局变化，不负责定义哪版更好。
- 版本/生命周期：rolling docs; release unknown；current_documentation_reviewed（2026-10-28）。
- 费用：Apache-2.0软件；CI/浏览器运行成本unknown；准确价格unknown。许可：Apache-2.0。
- 边界：不得用自动更新基线掩盖缺陷。
- 来源：[Playwright visual comparisons](https://playwright.dev/docs/test-snapshots), [Playwright license](https://github.com/microsoft/playwright/blob/main/LICENSE)

### design-storybook-a11y · Storybook组件可访问性检查
- 分类：evaluation_tool。在组件状态中检查可访问性问题，结合手工状态覆盖。
- 版本/生命周期：docs 10.6；current_documentation_reviewed（2026-10-28）。
- 费用：MIT软件；托管增值服务价格unknown；准确价格unknown。许可：MIT。
- 边界：默认状态通过不代表弹窗、错误态、加载态通过。
- 来源：[Storybook accessibility tests](https://storybook.js.org/docs/writing-tests/accessibility-testing), [Storybook license](https://github.com/storybookjs/storybook/blob/next/LICENSE)

### design-c2pa · C2PA素材来源链
- 分类：specification。记录可验证来源与编辑声明，辅助资产交付审计。
- 版本/生命周期：2.5 October 2026；current_documentation_reviewed（2026-10-28）。
- 费用：公开规范；签名证书/服务成本unknown；准确价格unknown。许可：规范条款与实现许可分开; exact implementation license unknown。
- 边界：凭证缺失不自动等于伪造；签名有效不等于版权可用。
- 来源：[C2PA specification 2.5](https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html)

## 可复制学习流程

以下步骤均为设计提案；“检查”是未来验收条件，不是本轮已经通过的测试。合成输入可直接交给任意合适助手做离线文本演练；需要产品操作时再审批。

### design-ui-flow · 预约界面从需求到可验收原型
**角色/模式：** UI/UX设计师 / agent_orchestrated_proposal
**合成输入：** 虚构预约站：3步（日期/人数/确认）；时段09:00与10:00，10:00已满；人数1–4；移动宽375、桌面1440。

**可复制提示：**

> 根据合成输入列状态机和屏幕清单。不要编造用户访谈。为满额、网络失败和返回修改设计明确反馈；先输出草图说明与验收表，不创建云文件。

**步骤与验收：**
1. 把事实、假设、待确认分栏；画出状态及转移，含重复提交。（检查：全部3步和失败态有入口出口）
2. 先以文本框图设计两种布局，说明任务优先级与取舍。（检查：不允许选择已满时段；人数上限明确）
3. 用获批设计组件生成可编辑原型草案，绑定交互而非只做静态截图。（检查：返回后数据保持；重复提交不生成重复预约）
4. 逐条走查正常、已满、断网、返回修改；未完成的转移标记缺失。（检查：键盘流程可完成且焦点可见）

**输出：** 状态表、屏幕清单、低保真布局、交互验收记录。
**失败恢复：** 发现状态遗漏先修状态机再改视觉；网络结果未知先查状态，不重复提交。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** rolling remote MCP; write beta; WCAG 2.2 Recommendation 2024-12-12；流程状态 unknown。
**跨库节点：** design-figma-mcp, design-wcag
**来源：** [Figma MCP introduction](https://developers.figma.com/docs/figma-mcp-server/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

### design-design-code · 组件感知的设计到代码交接
**角色/模式：** 设计工程师 / agent_orchestrated_proposal
**合成输入：** 虚构Card：标题/正文/主按钮；已有PrimaryButton组件；间距8/16/24；分别给320与1280宽结构描述。

**可复制提示：**

> 先列现有组件映射再规划实现。未知属性写unknown，禁造新组件替代现有按钮；输出变更计划、差异和测试矩阵。

**步骤与验收：**
1. 读取批准范围内单一frame结构和变量，避免整文件无边界抓取。（检查：已有按钮复用且属性映射可追踪）
2. 建立设计节点→代码组件→属性映射表；找不到则暂停映射。（检查：两宽度不横向溢出）
3. 生成局部实现草稿，保持语义标题与按钮，明确断点规则。（检查：长标题不盖住操作）
4. 按两宽度及长标题检查；截图差异与人工判定分开。（检查：没有依据截图发明不可见功能）

**输出：** 组件映射、局部代码提案、布局差异清单。
**失败恢复：** 上下文不足先请求较小frame或组件说明；不得将生成代码直接部署。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** rolling remote MCP; write beta; rolling docs; release unknown；流程状态 unknown。
**跨库节点：** design-figma-mcp, design-visual-regression
**来源：** [Figma MCP introduction](https://developers.figma.com/docs/figma-mcp-server/), [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)

### design-tokens-migration · 品牌token规范化与双主题
**角色/模式：** 设计系统维护者 / agent_orchestrated_proposal
**合成输入：** 合成token：brand=#125C45，text=#12221A，space8=8px；暗色主题text=#F5FFF8；错误别名a→b→a。

**可复制提示：**

> 以DTCG 2025.10为目标检查输入，给出语义命名、别名错误、迁移表和回滚方案。不要采用preview字段。

**步骤与验收：**
1. 区分原始值、语义角色、组件token，保留旧名映射。（检查：a/b环必须报错）
2. 检测类型缺失、别名环及无效引用；先拒绝循环再转换。（检查：旧token消费者被列出）
3. 提议明暗主题映射及平台输出，不假设所有工具无损导入。（检查：三组件两主题有检查记录）
4. 用按钮/卡片/错误提示三个组件比对迁移前后并审批破坏变更。（检查：来源版本固定为2025.10而非draft）

**输出：** tokens候选、旧新映射、引用图、兼容性报告。
**失败恢复：** 回滚至上次token快照；缺失字体/色彩空间转换规则不猜测。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** 2025.10 final; WCAG 2.2 Recommendation 2024-12-12；流程状态 unknown。
**跨库节点：** design-dtcg, design-wcag
**来源：** [DTCG Format 2025.10](https://www.designtokens.org/TR/2025.10/format/), [DTCG preview warning](https://www.designtokens.org/tr/drafts/format/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

### design-a11y-audit · 表单可访问性审校
**角色/模式：** 可访问性设计师 / agent_orchestrated_proposal
**合成输入：** 合成表单：只有占位符的邮箱框；红色边框提示错误；弹窗打开后焦点留在背景；按钮仅图标无名称。

**可复制提示：**

> 建立问题→影响→候选修复→人工检查表。不得只凭截图认证WCAG合规；区分自动可检和人工必检。

**步骤与验收：**
1. 给每项问题建立可重复前置条件和键盘操作。（检查：四项合成缺陷均定位）
2. 增加标签、文本错误、控件名称和弹窗焦点策略方案。（检查：错误不只靠颜色）
3. 设计默认/焦点/错误/禁用状态组件测试；自动检查结果原样保留。（检查：弹窗键盘路径和关闭后焦点有说明）
4. 人工用Tab/Shift+Tab/Esc与辅助技术核验，并由责任人确认范围。（检查：不输出全站认证结论）

**输出：** 修复建议与证据矩阵，未覆盖标准明确标记。
**失败恢复：** 无法运行辅助技术则结果为not_tested；不能将自动扫描空列表升级为通过。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** WCAG 2.2 Recommendation 2024-12-12; docs 10.6；流程状态 unknown。
**跨库节点：** design-wcag, design-storybook-a11y
**来源：** [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Storybook accessibility tests](https://storybook.js.org/docs/writing-tests/accessibility-testing)

### design-brand-kit · 虚构品牌视觉方向与权利清单
**角色/模式：** 品牌设计师 / agent_orchestrated_proposal
**合成输入：** 虚构品牌“苔光”：城市植物交换活动；温和、开放；只用几何叶片；不模仿现有商标；海报A4与1080方图。

**可复制提示：**

> 提出三种视觉方向，每种说明色彩/字重/栅格/可读性。以原创几何形为基础；所有字体和图像来源待核验。不要宣称商标可注册。

**步骤与验收：**
1. 提炼受众任务与不可变品牌约束；不冒充真实调研。（检查：三方向差异是结构而非只换色）
2. 给三种方向的文本moodboard和几何logo构成草图。（检查：小尺寸标识仍辨认）
3. 选一方向生成版式规则与素材登记表，商标清查另立任务。（检查：素材无来源时不得标可商用）
4. 按灰度、小尺寸、单色与长标题四场景审阅。（检查：没有复制现有品牌图形）

**输出：** 品牌方向、规范草案、资产许可清单、审阅差异。
**失败恢复：** 生成效果不稳定回到手工几何构图；品牌批准前不投放、不注册商标。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** Image5 / rolling API; unified SDK / REST rolling docs；流程状态 unknown。
**跨库节点：** design-firefly-image, design-canva-template
**来源：** [Firefly API](https://developer.adobe.com/firefly-services/docs/firefly-api/), [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/), [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)

### design-poster-localize · 多语种海报变体与模板填充
**角色/模式：** 平面设计师 / agent_orchestrated_proposal
**合成输入：** 虚构活动：苔光交换日，12月5日14:00，免费；英文标题Mosslight Exchange Day；1080×1080与1080×1920；保留顶部安全区。

**可复制提示：**

> 创建字段字典与中英两尺寸变体计划，日期逐字保留。先输出4份文本排版草稿；不上传、不发布。

**步骤与验收：**
1. 锁定事实字段、允许改写字段及字体覆盖范围。（检查：日期时间4份一致）
2. 把字段映射模板占位符，缺失字段停止该变体而不是留旧值。（检查：标题和正文可编辑）
3. 对4个变体逐一检查文字溢出、裁切、层级和安全区。（检查：长英文不遮挡信息）
4. 生成导出命名规则与人工批准表，批准后才考虑批量导出。（检查：每张都有素材许可登记）

**输出：** 字段JSON、4变体清单、溢出报告、批准表。
**失败恢复：** 模板权限不足返回人工填充指南；任务超时先查job结果再新建，避免重复计费。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** unified SDK / REST rolling docs；流程状态 unknown。
**跨库节点：** design-canva-template
**来源：** [Canva REST APIs](https://www.canva.dev/docs/apps/rest-apis/), [Canva autofill](https://www.canva.dev/docs/apps/rest-apis/autofill-guide/), [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/)

### design-vector-trace · 经典剪影矢量化与节点清理
**角色/模式：** 矢量设计师 / ordinary_tool_workflow
**合成输入：** 原创合成黑色叶片剪影：白底、无纹理、两处尖角；目标24px图标及A4印刷。

**可复制提示：**

> 描述单色描摹参数试验和节点清理流程，保留尖角；不要把照片自动描摹称为高质量logo恢复。

**步骤与验收：**
1. 先确认源图原创；复制原件作为只读对照。（检查：叶片内外轮廓闭合符合设计意图）
2. 用单色阈值候选比较轮廓，保留原始与生成路径分层。（检查：尖角未变圆）
3. 去除噪点和无意义节点，检查洞与尖角后保存可编辑SVG。（检查：没有外链位图伪装成纯矢量）
4. 在24px及大尺寸比较，复杂照片改用人工重绘或保留栅格。（检查：24px不糊成不可识别色块）

**输出：** 原图引用、SVG路径方案、阈值对照与尺寸验收。
**失败恢复：** 过度简化回到上一版本；不用提高节点数掩盖输入不适合。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** guide 1.3; installed version unknown；流程状态 unknown。
**跨库节点：** design-inkscape-trace
**来源：** [Inkscape Beginners Guide: tracing](https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html)

### design-product-composite · 产品合成背景与保真验收
**角色/模式：** 图像编辑师 / agent_orchestrated_proposal
**合成输入：** 虚构无商标白色圆柱杯，正面一条蓝线；合成背景“浅灰桌面与柔和侧光”；主体高度占画面60%。

**可复制提示：**

> 只规划背景替换和阴影，杯体轮廓、蓝线位置和比例不得改变；输出保护区与拒收规则，不生成或调用API。

**步骤与验收：**
1. 把产品轮廓与品牌细节列为锁定区域，背景列为可编辑区域。（检查：杯体与蓝线不走样）
2. 先给单张构图计划，再规划有限数量候选与预算上限。（检查：主体未被裁断）
3. 逐候选检查边缘光晕、接触阴影、蓝线漂移和比例变形。（检查：接触阴影方向一致）
4. 将可接受候选与原件并排审阅，标明合成非实拍。（检查：合成标注与输入来源齐全）

**输出：** 编辑计划、候选评审表、拒收原因、源资产记录。
**失败恢复：** 模型改变主体则改为锁定前景的确定性合成；达预算停止，不无限重试。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** Image5 / rolling API; v2 GA；流程状态 unknown。
**跨库节点：** design-firefly-image, design-photoshop-v2
**来源：** [Firefly API](https://developer.adobe.com/firefly-services/docs/firefly-api/), [Photoshop API](https://developer.adobe.com/firefly-services/docs/photoshop/), [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)

### design-image-repair · 局部图像修补与非目标区保护
**角色/模式：** 修图师 / agent_orchestrated_proposal
**合成输入：** 原创合成桌面图：纸张旁一处污点；纸上合成文字“DEMO 12”；只清除污点，不动文字与几何边缘。

**可复制提示：**

> 给出局部蒙版与非目标区保护检查。只修改指定污点，若文字变化即拒收；输出修改日志。

**步骤与验收：**
1. 确定污点边界，另列文字保护区；记录原件校验值。（检查：DEMO 12逐字保持）
2. 规划小蒙版与低影响编辑，先做一张而不是整图重生成。（检查：非目标区域无未经批准变化）
3. 对比非目标区与文字，标出所有额外变化并人工复核。（检查：修补不出现重复纹理）
4. 保留分层结果、原图和修改日志；仅交付核准版本。（检查：原件与参数保留）

**输出：** 蒙版说明、编辑前后差异表、可回滚分层交付计划。
**失败恢复：** 文字或边缘受损立即回退；采用手工局部修补方案，不能用整体美观抵消错误。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** Image5 / rolling API; v2 GA；流程状态 unknown。
**跨库节点：** design-firefly-image, design-photoshop-v2
**来源：** [Firefly API](https://developer.adobe.com/firefly-services/docs/firefly-api/), [Photoshop API](https://developer.adobe.com/firefly-services/docs/photoshop/)

### design-slides-story · 从事实表到可编辑演示
**角色/模式：** 演示设计师 / agent_orchestrated_proposal
**合成输入：** 虚构试验：A组10人7完成，B组10人8完成；仅演示，无显著性结论；3页：目的/结果/下一步；16:9。

**可复制提示：**

> 制作3页内容与布局JSON草案，按7/10及8/10正确呈现；不得宣称B优于A已证实。每页留来源与讲者备注。

**步骤与验收：**
1. 先列事实与不可推断项，再形成一页一主张故事线。（检查：数值7与8及分母10正确）
2. 按固定模板映射标题、正文、图表与备注，不烘焙成整页图片。（检查：不作未经验证显著性结论）
3. 逐页检查图表数值、阅读顺序、对齐与溢出。（检查：文字可编辑且无溢出）
4. 导出前检查页面图像和可编辑元素；发布/分享需审批。（检查：无授权素材不进入演示）

**输出：** 3页结构草稿、数据对照、备注、逐页QA表。
**失败恢复：** API对象ID冲突先读取现有页面；长文改写需保持事实，失败退回内容提纲。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** WCAG 2.2 Recommendation 2024-12-12; API v1；流程状态 unknown。
**跨库节点：** design-slides-api, design-wcag
**来源：** [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Google Slides API](https://developers.google.com/workspace/slides/api/guides/overview)

### design-visual-qa · 响应式视觉回归与差异分流
**角色/模式：** 设计QA / agent_orchestrated_proposal
**合成输入：** 合成网页组件：卡片3列→1列；宽320/768/1440；固定日期与字体；人为引入按钮溢出及2px间距变化。

**可复制提示：**

> 提出可重复截图基线方案，把真实缺陷与环境噪声分开。基线更新必须人工批准；不调用浏览器。

**步骤与验收：**
1. 固定环境、浏览器、字体、动画和数据；建立基线批准记录。（检查：溢出必被列为缺陷）
2. 按三宽度截取同状态比较，并用结构断言辅助判断。（检查：三断点全覆盖）
3. 将溢出列为阻塞，间距差异列为待设计判断，不自动忽略。（检查：环境不一致不能直接比较通过率）
4. 仅修复或解释后批准基线；输出失败截图引用与复现步骤。（检查：没有自动接受所有新截图）

**输出：** 环境锁定表、差异分类、复现步骤、基线审批。
**失败恢复：** 字体加载失败先修环境再比；保留旧基线，禁止用大容差遮盖布局缺陷。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** rolling docs; release unknown；流程状态 unknown。
**跨库节点：** design-visual-regression
**来源：** [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)

### design-asset-provenance · 资产权利与内容凭证交付
**角色/模式：** 设计运营 / agent_orchestrated_proposal
**合成输入：** 合成资产A原创几何图、B来源unknown、C带签名但无商业许可、D已获单项目许可；交付包需要公开再分发。

**可复制提示：**

> 分别给可交付/阻塞/待核验结论；来源签名和版权授权独立判断。不把缺凭证认定为伪造。

**步骤与验收：**
1. 建立来源、创作者、工具、编辑、许可范围和批准人的登记字段。（检查：B不误标可商用）
2. 核对凭证有效性与声明范围，单独核对商用/再分发权利。（检查：C签名有效不等于有授权）
3. 把B/C/D放入待核验或限制队列；不因看起来可信就放行。（检查：D单项目许可不自动再分发）
4. 导出原创资产及清单草案，元数据隐私审查后才考虑公开。（检查：声明unknown与invalid明确区分）

**输出：** 资产台账、凭证检查结果、许可阻塞表、交付清单。
**失败恢复：** 无法验证凭证保留原件和unknown；改用原创替代，不能去掉凭证掩盖来源。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** unified SDK / REST rolling docs; 2.5 October 2026；流程状态 unknown。
**跨库节点：** design-c2pa, design-canva-template
**来源：** [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/), [C2PA specification 2.5](https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html), [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)

### design-ps-legacy-migrate · 历史PSD批处理到v2迁移练习
**角色/模式：** 设计自动化工程师 / agent_orchestrated_proposal
**合成输入：** 合成旧任务：v1替换一张海报图片与标题；外链资源可能过期；目标只生成迁移映射不发送请求。

**可复制提示：**

> 保留v1历史接口说明并标deprecated，列v2迁移所需字段、未核验点和回滚条件。官方公告EOL为2026-07-31；不要猜测端点兼容或声称已测试服务响应。

**步骤与验收：**
1. 冻结旧任务定义与示例输出，标出旧endpoint来源。（检查：明确v1 deprecated）
2. 根据迁移文档逐操作映射；未确认操作写unknown并停止。（检查：正确记载公告EOL 2026-07-31）
3. 规划小样本比较：字体、图层位置、外链访问和输出格式。（检查：外链资源权限及有效期有检查）
4. 通过验收后才申请切换；失败保持旧档案但不建议扩大旧集成。（检查：新旧输出差异有批准入口）

**输出：** 旧新映射、依赖台账、回滚与验收计划。
**失败恢复：** 无法映射时保留人工操作方案；禁直接对生产PSD重试未知写入。
**审批：** 默认离线文本方案；任何账户接入、上传、写入、付费、分享另行批准
**版本/生命周期：** v2 GA; v1 deprecated; announced EOL 2026-07-31；流程状态 deprecated。
**跨库节点：** design-photoshop-v1, design-photoshop-v2
**来源：** [Photoshop API](https://developer.adobe.com/firefly-services/docs/photoshop/), [Photoshop guides and migration](https://developer.adobe.com/firefly-services/docs/photoshop/guides/)

## 维护与升级

发布前核验滚动功能、许可与配额。运行前固定产品版本、输入、提示、参数、环境与预算；运行后记录原始结果、人工修改、失败及费用。没有对照基线就不写提效百分比。每次迁移保留旧节点与来源，关系必须说明是编辑建议还是厂商实际集成。本轮没有创建定时任务。

## 官方来源与核验记录

- design-src-figma [Figma MCP introduction](https://developers.figma.com/docs/figma-mcp-server/)：rolling docs; exact release unknown；2026-10-28已打开；MCP提供设计上下文，也支持远端写原生画布；不是MCP本身自主制定任务。写入为beta且有席位条件。
- design-src-figma-access [Figma access](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/)：rolling docs; exact release unknown；2026-10-28已打开；功能受计划、席位与限流影响；执行前按当前账号复核。
- design-src-firefly [Firefly API](https://developer.adobe.com/firefly-services/docs/firefly-api/)：Image5; rolling API docs；2026-10-28已打开；含图像生成、合成、放大；文档列Image5及Instruct Edit；并非可靠性或质量实测。
- design-src-photoshop [Photoshop API](https://developer.adobe.com/firefly-services/docs/photoshop/)：API v2；2026-10-28已打开；v2为GA，支持linked smart objects，面向可编排编辑服务。
- design-src-ps-migration [Photoshop guides and migration](https://developer.adobe.com/firefly-services/docs/photoshop/guides/)：v1 legacy / v2 recommended；2026-10-28已打开；v1标deprecated，新工作推荐v2；补核官方弃用公告EOL为2026-07-31。
- design-src-canva [Canva REST APIs](https://www.canva.dev/docs/apps/rest-apis/)：rolling docs; exact release unknown；2026-10-28已打开；Connect旧入口重定向统一SDK；REST提供资产、设计等集成，preview不能视为稳定生产接口。
- design-src-canva-autofill [Canva autofill](https://www.canva.dev/docs/apps/rest-apis/autofill-guide/)：rolling docs; exact release unknown；2026-10-28已打开；官方提供数据填充品牌模板的工作流；具体资格与配额执行前重查。
- design-src-canva-rights [Canva Content License Agreement](https://www.canva.com/policies/content-license-agreement/)：核验日条款; legal review required；2026-10-28已打开；素材类别约束不同，混用按更严类别；免费素材也要核对具体来源与许可。
- design-src-tokens [DTCG Format 2025.10](https://www.designtokens.org/TR/2025.10/format/)：2025.10; 2025-10-28；2026-10-28已打开；稳定Final Community Group Report；不是W3C标准；定义交换token的格式。
- design-src-tokens-draft [DTCG preview warning](https://www.designtokens.org/tr/drafts/format/)：draft 2026-09-08；2026-10-28已打开；预览明确不可作为权威或实现依据；使用固定正式版。
- design-src-wcag [WCAG 2.2](https://www.w3.org/TR/WCAG22/)：Recommendation 2024-12-12；2026-10-28已打开；可测试的无障碍标准；2.2未废止2.0/2.1，推荐采用较新版本。
- design-src-inkscape [Inkscape Beginners Guide: tracing](https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html)：Guide 1.3; app version unknown；2026-10-28已打开；位图描摹生成路径，适合简单剪影；复杂颜色会生成大量对象，不保证完全一致。
- design-src-slides [Google Slides API](https://developers.google.com/workspace/slides/api/guides/overview)：Slides API v1 documentation；2026-10-28已打开；API可创建和修改演示文稿；batchUpdate可操作页面元素。
- design-src-playwright [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)：rolling docs; exact release unknown；2026-10-28已打开；截图比较依赖基线与环境一致；相同页面在不同系统等条件可能不同。
- design-src-storybook [Storybook accessibility tests](https://storybook.js.org/docs/writing-tests/accessibility-testing)：docs 10.6；2026-10-28已打开；提供组件无障碍测试文档；自动测试不替代全部人工评估。
- design-src-c2pa [C2PA specification 2.5](https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html)：2.5; October 2026；2026-10-28已打开；内容凭证包含签名、绑定、断言和验证；来源链不能单独证明创作内容为真或拥有版权。
- design-src-adobe-rights [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)：updated 2026-05-15；2026-10-28已打开；使用受生成AI指南约束；输入与输出仍须独立权利审核，不能由品牌名推导免责。
- design-src-pw-license [Playwright license](https://github.com/microsoft/playwright/blob/main/LICENSE)：main snapshot；2026-10-28已打开；Apache-2.0；不等于被测试页面素材授权。
- design-src-sb-license [Storybook license](https://github.com/storybookjs/storybook/blob/next/LICENSE)：next snapshot；2026-10-28已打开；MIT；保留软件许可，第三方组件与素材另核。

## 未解决范围

- 未比较真实生成质量、成本、速度或生产部署效果
- Inkscape官网教程与许可页面403；使用维护指南验证描摹功能，软件许可仍unknown
- Canva直接猜测autofill路径不可访问，已通过官方文档链接定位正确指南
- 未覆盖3D/CAD/工业设计/字体生成/印前色彩管理等后续专题
- 价格、区域可用性、账号权限和具体输出法律地位不由通用文档完整确定

## 独立复核修订（2026-10-28）

- Photoshop v1：[官方弃用公告](https://developer.adobe.com/firefly-services/docs/photoshop/getting-started/deprecation-announcement/)明确通知日2026-04-20、EOL 2026-07-31；已过公告EOL，仅保留历史迁移，不宣称测试端点失效。
- C2PA：[官方explainer §7.2.2](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)明确provenance单独不能证明内容真实、准确或符合事实；2.2解释文档用于边界说明，技术节点仍固定2.5。
- Figma：写画布为remote MCP能力，desktop不支持；草稿外写入需要Full seat。beta免费不代表永久免费。来源为前述Figma MCP introduction。
