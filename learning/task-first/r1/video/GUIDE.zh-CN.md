# 把90秒讲解做成约45秒粗剪，保住三条事实

**有条件练习，Descript未实跑；45秒成片未生成。** 现在有[真实90秒合成输入可下载](assets/paper-plane-synthetic-input-90s.mp4)，但作者及技术QA均未主观听评。你需要先播放确认，而不是把“文件生成了”当成“每句话都听得懂”。本课只做剪辑，不生成新声音、不克隆、不加音乐或外部素材、不发布。

## 第1步：确认条件，下载并亲自听一次

使用Descript桌面Web的个人或组织授权账号，打开 [web.descript.com](https://web.descript.com)，推荐Chrome/Edge等Chromium浏览器；本课不针对手机小屏，官方不支持Firefox，Safari可能有兼容问题。这里不需要MCP、API key或安装Skill，内置Underlord侧栏足够。[Web说明](https://help.descript.com/getting-started/descript-for-web)

必须是**单一英文**。官方转录页明确不支持中文，单文件混合语言也不支持；不要把中文视频上传后期待同样结果。地区完整可用名单本课未确认，无法合规使用则停止，不绕过限制。[转录语言](https://help.descript.com/script-editing/supported-transcription-languages)

先看账户Usage与预算。2026-10-29查到的Free套餐为媒体60分钟/月、100一次性AI credits、Underlord有限使用，免费额度不保证够完成本课；账户实际资格、旧套餐及当日费用以产品为准，不需要为本课自动升级。每次Underlord请求的推理和调用工具可能都消耗额度，成本不固定，连“先给计划”也可能收费；提示中的预算不是硬性扣费上限。不能接受单次未知消耗，就只做纸面练习或手工剪辑。[价格](https://www.descript.com/pricing)／[Underlord费用与入口](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript)

下载以下文件，放在一个练习文件夹，保留MP4未改动副本：

- [MP4：90秒输入，约2MB](assets/paper-plane-synthetic-input-90s.mp4)
- [完整英文原文](assets/script.en.txt)
- [句级SRT](assets/captions.en.srt)
- [完整17句时间表](assets/TIMELINE.zh-CN.md)与[三事实标记](assets/facts.json)

这是原创教学文字/色块配本地Flite通用`slt`合成旁白，不是真人录像或实际实验结果。工具/声库各自权利保留；不宣称商用全面清权、CC BY或公有领域。SRT是已知合成段时间表，**不是Descript转录**，不要提前导入它来假装自动转录准确。

**现在在设备播放器从头听完90秒。** 拿原文核对，尤其三组必留内容：

|事实|输入合成区间|亲自确认听清的意思|
|---|---:|---|
|F1|19.057–28.072秒|两款用同尺寸同类型纸，各一张；仅折法不同（same、only）|
|F2|44.460–50.350秒|每款三次，共六次（three、six）|
|F3|67.764–76.839秒|六个距离全部记录，包括短飞行；不因结果差丢弃（including、Do not discard）|

这些区间按合成PCM段边界给出，包含短停顿，不是逐词发声边界。听不清任一数字、否定词或句尾就停：不要靠看字幕猜它说对了，可改用自己有权处理的清楚英文录制。自备原片需约90秒、事实完全存在、没有音乐或隐私，并重记时间码；本表不能直接套用。

## 第2步：建独立项目，导入后查真正的自动转录

在drive view右上 **New project** 选择视频类型，命名 `Paper plane — rough cut practice`，核对保存workspace，不选有他人协作的在用项目。默认个人私有位置可能被管理员调整，不能省略检查。[新项目](https://help.descript.com/getting-started/create-a-new-project)

把MP4拖进**script面板**，上传同时启动自动转录。只在Project面板点Upload只会先上传，两条入口不同。等上传和转录完成，别把原文/SRT的存在当作它已经转录正确。[导入](https://help.descript.com/add-and-manage-media/local)

一边播放，一边对照Descript实际转录，特别检查F1–F3与否定词。听写错误时双击错词→工具栏 **Correct**（或C）→输入实际听到的词→Correct；它改显示文字，不改音视频。普通删除文字会剪掉媒体，别混用。[Correct](https://help.descript.com/script-editing/correct-your-transcript)

记录剪前版本时间、实际片长及Usage；只有原声音本来清楚、转录也核准后才继续。若中文/混语、上传失败、素材权限未知或没有可用AI额度，停在此处。本fixture是H.264/AAC 720p且远低于Free单文件1GB上限；自备片仍需核对编码，不能只看扩展名。[格式限制](https://help.descript.com/add-and-manage-media/supported-file-types)

## 第3步：只给一次受限粗剪请求

右侧栏点 **Underlord**，不必切换高价模型或接插件。确认允许它改这个独立练习项目，粘贴下面整段。本提示特别说明保留**已有合成旁白**，而不是要求它另造声音；若用自己的真人录制，把第一段的synthetic narration改成original recorded narration即可。

```text
Make a rough cut of the current 90-second English practice video.
This input already contains generic synthetic narration and original text cards.
Keep the existing audio and video only. Do not create any new speech.
Target duration: 45 seconds. Keep normal playback speed and the current aspect ratio.

These three facts must remain audible with their meaning intact:
F1: Both planes use one sheet of the same size and type of paper.
    Only the fold design changes.
F2: Each design gets three throws; there are six throws in total.
F3: Record all six distances, including short flights.
    Do not discard a result because it looks disappointing.

Keep the instruction to keep people out of the flight path if possible.
Remove repeated explanation, the long introduction, unnecessary pauses,
and the trailing silence first. Do not invent results or claim a winner.
Keep the synthetic-practice disclosure on the existing cards visible.
Do not change a fact card to contradict the audio.

Do not use AI speech, voice cloning, Regenerate, translation, stock media,
B-roll generation, background music, effects, speed changes, or web search.
Do not modify other compositions, create a share link, or publish anything.

If 45 seconds cannot be reached without losing a required fact, cutting words
unnaturally, or generating new speech, preserve the facts and report the
unmet duration target. Never silently remove a number, a qualifier, or a negation.
After editing, list removed sections, resulting duration, and the locations
of F1, F2 and F3. I will verify the actual media myself; your report is not proof.
```

助手可能不遵守约束，不能因为它回复“完成”便继续导出。一次请求后先审；最多再给一次明确、窄范围的修正，仍不满足就停止或手工处理。这是本课止损策略，不是产品硬限制。

## 第4步：逐句听、逐切点看，验收而非相信总结

用实际时间线读时长，再完整播放剪后版本。可填写[验收记录](CHECKLIST.zh-CN.md)。

1. 本课粗剪目标“约45秒”接受44–46秒；不是保证严格45.000秒。若业务要求精确时长，另做帧级验收，不把容差当精度。
2. 分别填写三事实的**剪后**起止时间，听清same/only/three/six/including/not；字幕或卡片有文字、声音却被剪掉，仍不通过。
3. 每个切点前后听看数秒，确认词头词尾、自然断句、无黑帧或音画错配。此fixture为文字卡，没有真人口型，不能据它验证口型同步能力。切后卡片仍须与所听事实相配。
4. 没有新增声音、音乐、外部画面或变速，现有合成身份标识没有被隐藏；未被拼接成“已经证明哪款最好”。
5. 记录实际Usage变化，达到预算上限或结果不明确就停止继续提示，不自动充值。

若只剩无关长开头，可在已核准转录中选文字→Delete/Backspace手工删除，它会剪对应媒体；**不在Correct模式做剪辑**。每删一段重听切点，不能靠Regenerate补词。[文本剪辑](https://help.descript.com/getting-started/edit-like-a-doc)

## 第5步：失败先恢复，不用更多生成掩盖错误

- **事实/否定词缺失、画面错配或新生成声音：** 不导出当成成片。当前会话右侧Underlord找到该回复，下方 **Revert** 回到检查点；普通单步可用左上Undo或Ctrl/Cmd+Z，恢复后重新播放核对。
- **已经刷新或关闭：** Revert检查点不保证保留，改用左上菜单 **File → Version history**，选剪前版本先预览。确认后 **Restore → Restore Version**。恢复影响整个项目所有compositions/files，不只是当前片段；有协作者时先获批准，不能覆盖他人修改。不能承诺退款。[Revert](https://help.descript.com/ai-assistant/revert)／[Version History](https://help.descript.com/working-in-projects/version-history)
- **输入读词含糊：** 回第1步，不能用Correct把真实错误声音“修成正确”。改用清楚且有权处理的原片，或只交未完成记录。
- **没有Underlord/额度耗尽/格式失败：** 不购买试错、不重复上传扣分钟；记具体缺项，可留纸面方案。没有权限便停止。

## 第6步：只导出本地审稿MP4，再打开检查

通过人工验收后右上 **Export → Video → Local export**；范围为 **Current composition**，避免选成Current selection或All compositions。选账号允许分辨率，Free最高720p，不承诺Free无水印。点击Export保存MP4；别选无声GIF、网页分享、YouTube发布。[本地导出](https://help.descript.com/export-and-share/video-gif)

在设备上重新打开文件，完整播放，检查实际时长、三事实和切点；文件存在不等于导出正确。记录文件名、大小、分辨率、水印、日期及剪后事实时间码。最后保留未编辑输入、可编辑项目、导出MP4和检查表。

**成功标准是你实际听看并验证的一份粗剪，不是本教材已经给出的结果。** 本包只有90秒合成输入；Descript上传、转录、剪辑、恢复及45秒导出都尚未由教材作者执行。不要删除这个执行边界。
