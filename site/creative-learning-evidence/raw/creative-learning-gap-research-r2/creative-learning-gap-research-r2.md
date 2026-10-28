# 创意学习缺口研究 R2（独立QA后修订）

## 结论先行
优先补 **Underlord 可回滚粗剪、Adobe Express AI Assistant 局部设计修改**，并用四个普通创作交付工作流把“生成之后怎么办”讲清楚。两者都是应用能力而非基础模型；后四项不是 Agent。共六项候选，仅研究，未整合、未运行产品，不宣称覆盖全行业。

## 已有覆盖与去重
首轮读取为AgentWork 125案例、ModelAtlas 230节点；并行维护期间数据更新，成包时重新取样为132案例、237节点（以JSON基线哈希为准）。已读设计13案、音乐14案、视频12案与R2九案；已有图像生成、模板、字幕、分轨、混音、母带、CAD/3D等。精确缺口词在两份当前数据均为零；Kdenlive是已有工具的新用法，应复用节点。哈希与匹配结果见JSON。

## 视频Agent：Underlord粗剪的差异审查与回滚
**分类：** agentic_application_feature；Descript Underlord
**为什么值得补：** 既有FilmAgent/ViMax为研究编排，HKUDS VideoAgent与Kdenlive案例不覆盖商用会话剪辑的积分/回滚。
**可见用法：** 打开已有授权项目的Underlord侧栏 → 给明确剪辑目标、禁止改动和长度约束 → 对照转录稿逐处检查编辑：当前session可在对应Underlord响应下Revert；刷新或关闭项目后改用File > Version history。先预览所选历史版本，核对整个项目全部compositions/files及协作者变更；确认恢复影响获准后才Restore Version。
**原创练习与验收（未执行）：** 先设计原始稿/剪后稿差异表，关键事实零删改；检查断句、画面跳切与字幕同步；不以工具自述判成功；记录提示前后Usage，达到自定预算即停；未经批准不发布
**账号/付费：** Descript账户与计划；Free有限Underlord，付费能力/高阶模型不同；每次推理+工具均可能计费，同提示成本不固定。
**许可：** 服务条款而非开源模型许可；素材/人物同意/输出权利单独核验，不声称输出天然无版权风险。
**自动化边界：** 这是官方agentic应用功能，不是某单一模型。仅UI学习设计；本轮不调用API/MCP、不上传、不支付、不克隆声音、不发布。
**历史/日期：** 帮助页当前Beta；v2历史公告日期未知，旧Labs开关与模型名不保留为现行操作。 首发日期未核实时保留unknown。
**官方依据：** [underlord-help](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript)、[underlord-product](https://www.descript.com/underlord)、[underlord-v2](https://feedback.descript.com/changelog/announcingunderlord-v2)、[underlord-revert](https://help.descript.com/ai-assistant/revert)、[underlord-terms](https://www.descript.com/terms)

## 设计AI助手：局部修改与人工接管
**分类：** conversational_ai_assistant；Adobe Express AI Assistant
**为什么值得补：** 不同于已覆盖Firefly图像API、Photoshop API和Canva模板填充；补会话中保持设计不变量与手工接管。
**可见用法：** 在主页用提示生成虚构活动海报并补齐占位信息 → 选择候选后只修改指定文字/元素，保留其余布局 → 需要时Open in editor并关闭AI Assistant转手工编辑；只准备下载审稿
**原创练习与验收（未执行）：** 把日期/地址/品牌色列为不变量并逐项对照；检查字体、对比度、文字溢出与非目标区变化；协作者不能看到私有Chats，因此交付独立变更说明，而非假设聊天会共享
**账号/付费：** 个人Free/Premium、桌面web、渐进Beta；Teams/Enterprise/Education不支持。现行页排除中国等地区，支持English/Bahasa Indonesia/Brazilian Portuguese/Hindi，未列中文。具体积分规则本次未确认。
**许可：** Adobe服务与素材/字体规则另核；本轮未核完全部生成与Stock许可，商业再分发资格unknown，不替代法务审查。
**自动化边界：** 称会话AI助手，不称基础模型或无限自治Agent。只设计受控提示和人工审批；不承诺跨应用自动化/API。
**历史/日期：** 2025-10-28 beta公告仅作历史；2026-10-22现行帮助页仍Beta。旧FAQ缓存计费表与直接打开结果冲突。 首发日期未核实时保留unknown。
**官方依据：** [express-overview](https://helpx.adobe.com/express/web/ai-assistant/adobe-express-ai-assistant-overview.html)、[express-how](https://helpx.adobe.com/express/web/ai-assistant/get-started-with-the-adobe-express-ai-assistant.html)、[express-history](https://news.adobe.com/news/2025/10/adobe-max-2025-express-ai-assistant)、[express-faq-redirect](https://helpx.adobe.com/express/web/ai-assistant/adobe-express-ai-assistant-faq.html)

## 音乐制作：多录次拼接与联动编辑验收
**分类：** deterministic_software_workflow；Ableton Live comping / linked-track editing
**为什么值得补：** 现有生成、分轨、混音、母带与频谱修复未讲真实多录次选段。
**可见用法：** Arrangement View显示Take Lanes；Automation Mode时先退出 → 在Draw Mode将录次选段编入主轨 → 需要多麦同步编辑时核对Standard/Suite的linked-track能力
**原创练习与验收（未执行）：** 原创8小节两次录音只是自定练习，不是厂商建议；保留全部原始录次与选段表；逐个接点试听爆音/呼吸截断，多麦对照相位与同步
**账号/付费：** 付费许可/授权软件；在线授权需要Ableton账户，亦有离线路径。Comping支持Intro/Standard/Suite，联动轨编辑限Standard/Suite；不泛化到Lite。
**许可：** 软件许可不授予录音、采样、插件素材再分发权；确切EULA条款未完整复核。
**自动化边界：** 普通DAW编辑功能，不是音乐Agent或生成模型；未证实API自治控制，不运行产品。
**历史/日期：** 官方FAQ称自Live 11起提供comping；首发日期unknown。 首发日期未核实时保留unknown。
**官方依据：** [ableton-comp](https://help.ableton.com/hc/en-us/articles/360019092580-Comping-in-Live-FAQ)、[ableton-auth](https://help.ableton.com/hc/en-us/articles/209773585-Authorizing-Live-Online)、[ableton-buy](https://help.ableton.com/hc/en-us/articles/209772965-Buying-Live-FAQ)

## 音乐交付：总谱到演奏分谱
**分类：** deterministic_software_workflow；MuseScore Studio Parts
**为什么值得补：** 现有音乐案例偏音频，缺少排练/演奏所需的可读分谱交付。
**可见用法：** Parts打开默认或自定义分谱 → File Export选择各分谱并决定分开或合并 → 输出PDF供排练前人工审阅
**原创练习与验收（未执行）：** 原创四声部短曲，逐谱核对乐器名/小节数/休止；人工检查翻页、断行与碰撞，不将自动生成等同可演奏；保存源文件和分谱清单并区分音频试听与纸面谱面验收
**账号/付费：** 官方下载Studio免费且无需账户/订阅；不把MuseScore.com乐谱服务或额外音源混同桌面软件。
**许可：** Studio代码GPL 3.0；乐谱著作权、字体和音源单独许可，不自动继承GPL。
**自动化边界：** 排版软件，不是生成音乐模型/Agent；只做手册UI流程，不宣称插件/CLI已核验。
**历史/日期：** Parts页明确MuseScore 4，日期未知；不混用旧版File Export Parts菜单。 首发日期未核实时保留unknown。
**官方依据：** [muse-parts](https://handbook.musescore.org/basics/parts)、[muse-install](https://handbook.musescore.org/en_gb/introduction/download-and-installation)、[muse-license](https://github.com/musescore/MuseScore)

## 视频剪辑：代理预览与原片交付验证
**分类：** deterministic_software_workflow；Kdenlive Proxy Clips
**为什么值得补：** 既有Kdenlive节点覆盖转录字幕；没有代理编辑与原片渲染身份检查。
**可见用法：** 项目设置启用代理 → 素材箱选择Proxy Clip，观察P标记 → 保留原素材；最终渲染按文档使用原文件
**原创练习与验收（未执行）：** 自有高分辨率短片制作代理与源片映射清单；对比切点、时长与帧率；代理低清不是导出质量验收；设计源文件缺失的失败场景：不得把代理静默冒充交付，停止并恢复源文件
**账号/付费：** 免费开源本地编辑器；所选工作流不涉及付费云服务/模型key。无账户步骤出现在所核UI文档，账号要求推断限此流程。
**许可：** 官方仓库显示GPL-3.0，组件许可按具体版本核验；软件许可不授予素材/编码专利权。
**自动化边界：** 普通确定性编辑流程，不是视频Agent；未验证外部编排接口。
**历史/日期：** 当前读取26.08手册；这是版本标签非发布时间；旧猜测代理路径工具打开报错不等于功能停用。 首发日期未核实时保留unknown。
**官方依据：** [kden-proxy](https://docs.kdenlive.org/en/user_interface/menu/media_menu.html)、[kden-license](https://github.com/KDE/kdenlive)

## 设计交付：印前预检、打包与字体授权隔离
**分类：** deterministic_software_workflow；Adobe InDesign Package / Preflight
**为什么值得补：** 已有演示、海报和C2PA；缺少印刷源文件交接的缺链、字体与隐藏资产泄露检查。
**可见用法：** File Package检查摘要，有错返回Window Output Preflight → 只选择需交付的链接/IDML/PDF等，不默认包含隐藏非打印素材 → 核查字体许可后生成待审批包与报告
**原创练习与验收（未执行）：** 设计自有海报并设置缺图/缺字体反例，先阻断再修复；审查隐藏层、非打印内容、联系信息是否应出包；分离嵌入PDF与字体文件再分发；指定收件方须自行许可的字体；IDML兼容仍需实际重开渲染，不能凭勾选判成功
**账号/付费：** Creative Cloud会员与Adobe账户；官方试用7日不取消转收费。本研究未注册试用、订阅或付款。
**许可：** Adobe Fonts文件不可拷贝移动；其他字体依各EULA与收件方许可。Package按钮不是再分发授权。
**自动化边界：** 排版交付软件，不是设计Agent；不使用脚本/API/Server，不自动发印厂。
**历史/日期：** 打包帮助更新2026-06-02、字体说明2025-11-12；首发unknown，不将旧CS手册当现行。 首发日期未核实时保留unknown。
**官方依据：** [indesign-package](https://helpx.adobe.com/indesign/desktop/print/preflight/package-files-for-output.html)、[font-rights](https://helpx.adobe.com/fonts/web/getting-and-using-fonts/package-font-files.html)、[indesign-pay](https://www.adobe.com/products/indesign/free-trial-download.html)

## 证据卫生与后续整合闸门
1. Adobe Express FAQ缓存的额度表未作为已确认现行事实。直接打开跳到overview且无credits，公开记录冲突。
2. Kdenlive代理专页URL工具打开失败，使用另一已打开的官方Media Menu。不是产品失败或停用证据。
3. Underlord历史v2公告没有可确认绝对日期，date=null；历史临时Labs开关不写入现行步骤。
4. 素材均要求原创/授权；仅链接公开资料，不搬运非公开文件或完整文档。
5. 若后续获准整合，先适配案例/产品分类、复用Kdenlive节点，保留原始证据，再做链接和schema测试；产品效果另需授权运行和人工听/看验收。
6. 未完成项为额度/部分许可的资料核验与所有实际执行，不以“文档可读”宣称流程成功。

## R2修订与证据保留

- 原始R1三文件逐字节保存在 `before-qa/`，SHA256见 `changes.json`，未覆写。
- Underlord Revert检查点只在当前session可用；刷新/关闭项目后改Version History。恢复影响整个项目全部compositions/files；先预览、审查协作者变化并获准后才Restore，恢复后人工验收，不保证永久保留或积分退款。全部仍未执行。[官方回滚](https://help.descript.com/ai-assistant/revert)、[官方版本历史](https://help.descript.com/working-in-projects/version-history)
- font-rights首次研究成功与独立QA本轮UnexpectedStatusCode并存记录。未重试或改写原页状态；新增[独立字体许可FAQ](https://helpx.adobe.com/fonts/web/font-licensing/font-licensing.html)只支持自身结论。
- Express FAQ缓存/重定向冲突与Kdenlive原失败均保留；精确计费、账号实际资格、全部素材许可与产品效果仍unknown。
- 独立QA其余五项accept仅指资料/分类可接纳，不等于实测或法律许可认证。仍仅供后续选择整合，不修改canonical。
