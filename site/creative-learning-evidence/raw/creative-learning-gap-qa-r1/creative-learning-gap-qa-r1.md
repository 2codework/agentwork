# 创作缺口六项独立来源 QA r1

核验：2026-10-28。范围仅原六候选，不扩展产品目录。原研究包与21条source-checks只读，未改canonical；原始SHA256见 `original-sha256.txt`。公开官方web复核，不进入账号、运行软件、调用模型、上传媒体或操作Mac。所有教程仍是未执行设计，来源支持不等于效果认证。

## 两项AI候选

### gap-underlord-review — fix（补回滚会话边界后可接纳）

官方帮助仍称Beta；每提示推理和所用工具有积分消耗，同样提示消耗可不同。产品页明确agentic co-editor，支持应用功能分类，不是基础模型；Free有限使用不等于无限免费。模型选择器、精确价格和旧版临时开关不冻结为教程保证。[帮助](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript)、[产品](https://www.descript.com/underlord)、[v2历史公告](https://feedback.descript.com/changelog/announcingunderlord-v2)

**必须补充**：Revert检查点仅当前session；刷新/关闭项目后走Version History，另有单步Undo。现研究“官方回滚入口恢复”不算错误，但作为可执行学习路径缺少这一重要边界。建议将第三步明确改为“当次会话用Revert；刷新/关闭后按Version History恢复；恢复成功须人工核对，不承诺积分退回”。最后一点是保守验收限制，来源未证明退款。[回滚文档](https://help.descript.com/ai-assistant/revert)

素材/人物同意和输出审核不能由软件权限替代；条款的输出权利限法律可保护范围，不保证独有、不侵权或适用性。当前“服务条款而非模型开源许可、逐项素材权利核验”可接纳；不解释为法律意见。[条款§8](https://www.descript.com/terms)

### gap-express-targeted — accept（价格/积分、商业素材权利unknown保留）

2026-10-22帮助正文支持会话创建/修改、切手工编辑；个人Free/Premium渐进Beta、桌面web非移动app，Teams/Enterprise/Education尚不支持。公开地区排除中国等，语言列表不含中文。不能提升为无限自治agent或给用户保证可用。[概览](https://helpx.adobe.com/express/web/ai-assistant/adobe-express-ai-assistant-overview.html)

提示、补资料、四候选、局部修改/手工接管、下载流程有来源支持；Chats私有且不共享给协作者，独立交付变更说明合理。[操作](https://helpx.adobe.com/express/web/ai-assistant/get-started-with-the-adobe-express-ai-assistant.html)

2025-10-28为已证实历史Beta公告；企业将来计划不是当前资格。release_date=null可保守保留，但历史公告日期应与首发/GA分栏。[公告](https://news.adobe.com/news/2025/10/adobe-max-2025-express-ai-assistant)

FAQ原记录是搜索缓存与打开重定向冲突，本轮不重试，不把概览独立成功算FAQ成功；精确价格/积分与商业再分发权继续unknown，不从缓存写每日次数或积分豁免。

## 四项普通工具流程

详见合并JSON及ordinary来源检查：分类必须为普通软件/确定性工作流，不因人监督实践站点名称而升级为Agent、AI生成效果或性能认证。Kdenlive应复用既有vid-kdenlive，不新增重复工具实体。

## 证据边界

`source-checks.json`合并记录每条原source ID的本轮状态；原记录中的成功/失败历史不被覆盖。新的独立来源只能支持自身检查结论。任何无法打开的页面记本轮unknown，禁止将搜索摘要当全文成功。未复核完的确切EULA、第三方字体/音源/媒体权利、价格、账户与运行效果保留unknown。

## 最终六项结论与新增来源

- Underlord：fix，补当次session及全项目恢复/协作审批边界。
- Express：accept，积分价格/账号/完整商用素材许可unknown保留。
- Ableton、MuseScore、Kdenlive、InDesign：accept，普通确定性流程且never-run；素材/字体/音色/组件权利不外推。

Version History先预览；Restore会提示协作者冲突，影响整个项目所有compositions和files，不能只按当前片段批准。[官方版本历史](https://help.descript.com/working-in-projects/version-history)

原font-rights页本轮UnexpectedStatusCode，不重试不改原历史；独立字体FAQ支持不转移/打包Adobe Fonts、编辑接收方需独立许可、PDF嵌入与字体文件传递不同。[独立官方字体许可FAQ](https://helpx.adobe.com/fonts/web/font-licensing/font-licensing.html)

23条本轮记录覆盖21原ID，加上述2独立来源。其中18原页本轮成功，1原页本轮失败，2原有失败/冲突未重试。原始三文件SHA256复核一致；未更改任何原始文件或canonical。
