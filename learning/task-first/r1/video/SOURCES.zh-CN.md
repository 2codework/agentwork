# 来源、版本与素材说明

核验日期：2026-10-29。Descript帮助页当前称Underlord Beta，但未展示固定安装版本号或统一更新时间；这里不把核验日期当产品发布日期。界面、套餐与额度会变，账户实际显示不符时停止并查官方说明。

## 产品官方资料

- [Descript Web](https://help.descript.com/getting-started/descript-for-web)：浏览器入口与兼容条件。
- [支持转录语言](https://help.descript.com/script-editing/supported-transcription-languages)：英文受支持、中文未支持、单文件不支持混合语言；SRT不是自动转录证据。
- [套餐价格](https://www.descript.com/pricing)：Free及套餐额度。本课不保证免费余额足够，不要求购买。
- [Underlord](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript)：右侧栏入口、AI推理/工具费用、模型条件。提示不保证精准时长或事实保持。
- [创建项目](https://help.descript.com/getting-started/create-a-new-project)、[本地上传](https://help.descript.com/add-and-manage-media/local)、[支持格式](https://help.descript.com/add-and-manage-media/supported-file-types)：视频输入与script转录路线。
- [Correct](https://help.descript.com/script-editing/correct-your-transcript)、[文本剪辑](https://help.descript.com/getting-started/edit-like-a-doc)：修转录文字与实际剪媒体的区别。
- [Revert](https://help.descript.com/ai-assistant/revert)、[Version history](https://help.descript.com/working-in-projects/version-history)：会话检查点与跨会话全项目恢复。
- [本地视频导出](https://help.descript.com/export-and-share/video-gif)：Export→Video→Local export，MP4及Free720p边界。

## 输入来源与权利边界

英文脚本和文字卡为本项目原创教学内容；纸飞机练习是合成设定，不是实际实验结果。音频用云端本地预装Flite的通用`slt`声库（注册名`cmu_us_slt`）合成，无模仿特定人物的请求、无克隆操作，不表示声库底层从未使用真人录音，也不表示任何真人对本片背书。

[Flite官方项目](https://github.com/festvox/flite)与[许可说明](https://github.com/festvox/flite/blob/master/COPYING)说明软件条件；[cmu_us_slt官方源文件](https://raw.githubusercontent.com/festvox/flite/master/lang/cmu_us_slt/cmu_us_slt.c)确认声库身份与CMU许可头。软件、声库、字体各自权利保留。本读者包不分发软件/模型/字体文件，也不把软件许可直接宣布为MP4的CC BY或公有领域许可；不提供商用全面清权保证。

## 已验证什么、没有验证什么

技术与独立复核确认：90秒H.264/AAC、720p、17句完整输入和SRT一致、事实段未被截短；同一环境重建MP4字节相同。真实抽帧显示事实卡可读。完整音频解码不报错，峰值-2.8dBFS；这都**不能代替人耳确认可懂度、准确读词或无感知失真**。

主观听觉尚未验证，因此教程第1步要求读者实际播放。SRT按已知合成片段边界对齐，不是ASR或逐词对齐。Descript从未由本包作者执行；45秒输出未生成。可下载MP4 SHA256为：

`b1cc953778cff1667dffa48639ada5e91edbd4d299f1602c5cd9657f73355a2b`

文件完整性详见[SHA清单](assets/SHA256.json)。保持同一文件身份即可复用素材，不应把技术记录改写为产品执行或听评结果。
