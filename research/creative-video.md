# 视频、动画与电影 Agent：原创教学研究 r1

核验日期：2026-10-28。只读一手文献研究，**未原生实测、未生成影片、未调用付费或真实账号**。

视频/动画/电影Agent专题：12个原创案例、16个技术节点；代表性研究而非穷尽目录。

## 核心边界
模型≠工具≠Agent。开源代码≠权重无限制商用≠零算力成本。长片应按镜头、场景、章节组织，而不是宣称单次生成整片。

## 一条完整生产链
脚本 → 分镜 → 授权素材 → 图生视频/视频编辑 → 角色一致性 → 剪辑时间线 → 字幕/原创配音 → 证据型质检 → 人工批准 → 版本归档。
各阶段输出不可变ID和批准记录；预算/权限/质检不通过时停在上一批准版本。

## 原创案例（未执行）

### video-brief-storyboard · 从一分钟原创短故事到可拍分镜
**合成输入**：原创故事：纸机器人阿棱在温室发现滴水，通过移动空杯保存雨水；无真实人物、品牌或现有影视角色。目标60秒，6镜头。
**提示词**：将故事拆为6镜头；每镜写shot_id、时长、动作、景别、机位、起止状态、音效、禁改属性。只用一个主要动作，不添加科学结论。
1. **脚本约束**：列出起因、行动、结果各一句，建立阿棱为蓝色纸立方体、右侧白圆标记的角色卡。 验收：不得增添第二主角，三段因果可复述。
2. **分镜与连续性**：画6张原创线框草图，镜头时长8/10/10/12/12/8秒；把杯子左右位置和水位写入状态表。 验收：总时长60秒，前镜结束状态等于后镜开始状态。
3. **静态预演**：用草图和临时字幕排出animatic；只审节奏，不把静帧宣称成模型生成电影。 验收：观众无需旁白即可指出移动杯子的原因。
4. **审片冻结**：记录每镜通过/重做理由，冻结脚本v1与素材清单；生成阶段另行授权。 验收：全部镜头有输入与验收记录。
**失败恢复**：剧情漂移时回到三句梗概；镜头过长则拆动作，不靠延长生成硬凑。
**成本**：CPU可完成文本与静态预演；LLM和视频调用为可选且未执行。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-vimax, vid-filmagent, vid-otio
**来源**：[ViMax](https://github.com/HKUDS/ViMax)；[FilmAgent](https://filmagent.github.io/)；[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)

### video-product-i2v · 虚构产品15秒图生视频演示
**合成输入**：原创无品牌黄色保温杯正面、侧面、盖子三张自绘图；虚构说明只写外观，不宣称保温时长。
**提示词**：基于已批准首帧做单次缓慢环绕；杯体保持圆柱、无新增字样；每镜只改变相机或盖子一个因素。
1. **资产审查**：对三视图建立asset_id和尺寸，透明/反射细节改为可验证的简化材质。 验收：无商标与侵权包装，三视图颜色一致。
2. **低成本镜头测试**：设计3段5秒镜头，先选一个模型支持的短片配置；记录seed、分辨率、帧数和参考图SHA。 验收：不把seed当一致性保证；只批准轮廓稳定小样。
3. **字幕后置**：镜内不生成卖点文字，剪辑阶段叠加“外观概念演示”。 验收：盖子没有穿模，杯把不增减，字幕可读。
4. **导出比较**：输出横版与竖版草案，保留原画幅检查裁切。 验收：15秒±1帧；产品无关键区域被切掉。
**失败恢复**：形状漂移退回静态三视图加相机推拉；不反复生成直到耗尽预算。
**成本**：Wan示例硬件门槛见节点；先批准一次小样，再根据实际每秒成本设置预算。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-wan22, vid-comfyui, vid-ffmpeg
**来源**：[Wan2.2](https://github.com/Wan-Video/Wan2.2)；[ComfyUI](https://github.com/Comfy-Org/ComfyUI)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)

### video-training-chapters · 十分钟培训课拆成可维护章节
**合成输入**：原创虚构工具“纸盒台账”的离线示范屏幕与600字讲义；10分钟课程含5章，每章一个任务。
**提示词**：按学习目标而非热词剪辑，给每章起止时间、原讲义证据、练习和错误示范；不得删除必要前提。
1. **教学脚本**：先写学员能完成的5个动作，每章安排演示、暂停练习、答案各一段。 验收：每个目标都有对应可观察操作。
2. **录制与配音计划**：使用无账号离线假界面；人声采用自写旁白自行录制的方案，未实际采集。 验收：无客户数据、密码、通知弹窗。
3. **转录剪辑**：建立时间码文字稿，将迟疑停顿标为可剪，将警告与前提标为不可剪。 验收：每次剪切保留句意；章节边界不切掉句首。
4. **维护发布包**：每章单独版本化，更新第二章只重导出对应段与总片。 验收：练习答案与画面版本匹配，输出带字幕及无字幕版。
**失败恢复**：ASR错术语以讲义校正；边界错切回原素材时间码；不重生成整片。
**成本**：CPU编辑可行但耗时未知；转录模型内存/速度按版本实测，不承诺实时。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-kdenlive, vid-whisper, vid-otio
**来源**：[Kdenlive speech to text](https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html)；[Whisper](https://github.com/openai/whisper)；[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)

### video-character-continuity · 原创动画角色跨镜头一致性
**合成输入**：原创阿棱角色卡：蓝立方体、右侧白圆标记、短橙脚；4张自行绘制角度参考；四镜头取杯故事。
**提示词**：逐镜检查颜色、标记侧别、肢体数量、道具持有与朝向；不通过则说明证据帧位置，不主观打高分。
1. **锁角色锚点**：写角色不变量与允许变化项，建立每镜起止姿势；统一光色参考。 验收：不变量可从图中人工检查而非只有形容词。
2. **单镜候选**：按模型已核实的参考条件生成计划，每镜最多两个候选，先关键帧再运动。 验收：候选记录独立ID；禁止借用真实人脸。
3. **接镜检查**：逐镜对照首/中/尾帧与前后接缝，特别检查白圆标记是否镜像。 验收：4镜关键锚点无矛盾；抽帧通过后仍全速看片。
4. **局部恢复**：仅重做失败镜，必要时改成遮挡转场或静态插图。 验收：复审相邻两镜，防止局部重做带来新跳轴。
**失败恢复**：自动相似度只能预筛，不能证明身份一致；反复失败改传统关键帧动画。
**成本**：候选数×镜头数×重试计费；4镜×2候选是本教学预算上限，不是性能保证。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-wan22, vid-ltx2, vid-vimax
**来源**：[Wan2.2](https://github.com/Wan-Video/Wan2.2)；[LTX-2](https://github.com/Lightricks/LTX-2)；[ViMax](https://github.com/HKUDS/ViMax)

### video-silent-animation-loop · 无对白教育动画循环
**合成输入**：原创太阳、云、纸风车三层插画；8秒循环展示风车转动，不模拟真实气象。
**提示词**：固定镜头，只让风车匀速转一圈；云位置固定；首尾视觉状态相同；不出现文字或人物。
1. **拆图层**：将背景和风车分为独立原创资产，定义旋转中心和循环周期。 验收：中心不漂移，所有元素有授权记录。
2. **两路线对照**：方案A为传统关键帧旋转；方案B为历史运动模块生成计划，仅讨论未执行。 验收：比较可控性与成本，不默认生成模型更好。
3. **循环接缝**：检查最后一帧到第一帧的位移和亮度，允许只对非语义背景做过渡。 验收：正常播放看不到明显跳动，主体不融化。
4. **教学交付**：保存无声循环、制作说明和闪烁检查记录。 验收：标为概念动画，避免声称物理正确模拟。
**失败恢复**：循环失败回退关键帧旋转；不要用帧插值掩盖物体变形。
**成本**：传统2D旋转CPU预算低；AnimateDiff需匹配基础权重与运动模块，显存未知。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-animatediff, vid-ffmpeg
**来源**：[AnimateDiff](https://github.com/guoyww/AnimateDiff)；[AnimateDiff paper](https://arxiv.org/abs/2307.04725)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)

### video-long-film-previs · 原创短片的长叙事预演
**合成输入**：原创12分钟虚拟短片《最后一张纸》，三场景两虚构纸角色；主题为修复旧纸盒，不改编已有作品。
**提示词**：输出场景因果表与镜头依赖图；按场景制作，不要求单次模型生成12分钟；所有对白原创。
1. **长故事压缩**：列12个一分钟叙事节拍；每节拍标角色目标、冲突、解决及上一节拍依赖。 验收：删掉任一节拍能解释影响，不堆无关镜头。
2. **预算与资产复用**：将同一布景和道具资产复用，先做3分钟代表性animatic估算剩余工作。 验收：估算注明假设，未测数据不写成耗时结论。
3. **分角色审查**：编剧检查因果，摄影检查机位，制片检查授权与预算；人类解决相冲突建议。 验收：三类审查记录保留，Agent不得自行扩大预算。
4. **分场冻结**：场景逐个锁定并归档时间线，最终检查所有跨场道具与对白连续性。 验收：12分钟版本有镜头来源与修改日志。
**失败恢复**：长片漂移回到节拍表；API或资产许可未核清则停在预演，不声称已完成电影。
**成本**：生成长片成本按镜头重试估算，研究论文的虚拟环境效果不能换算商业制作成本。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-filmagent, vid-vimax, vid-otio
**来源**：[FilmAgent](https://filmagent.github.io/)；[ViMax](https://github.com/HKUDS/ViMax)；[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)

### video-edit-original-footage · 原素材重剪为30秒科普预告
**合成输入**：原创模拟素材清单：种子入土、浇水、发芽三段各20秒；讲义写明画面是示意，不是真实时间流逝。
**提示词**：选出总长30秒、保留因果的片段；只输出时间码与剪辑理由，不虚构素材中不存在的开花画面。
1. **建索引**：每段记事件、可见证据、音轨、时间码、禁止推断项，保留原片只读。 验收：描述可回溯到具体段落。
2. **编辑决策**：给出入点出点和排序，明确是否加速及加速标识。 验收：不得通过倒序或删前提制造错误因果。
3. **剪辑预览**：用时间线而非覆写源文件操作，配无夸张承诺字幕。 验收：30秒±1帧，转场无黑帧或断句。
4. **前后对比**：审查摘要与原讲义差异；对未显示现象标缺素材。 验收：没有添加“实拍”“实验成功”误导字样。
**失败恢复**：检索错片即回查原时间码；素材不足做说明卡而非生成伪证。
**成本**：仅编辑不必调用视频生成模型；Agent后端/API成本未知且本轮不使用。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-videoagent-edit, vid-ffmpeg, vid-otio
**来源**：[HKUDS VideoAgent](https://github.com/HKUDS/VideoAgent)；[VideoAgent editing paper](https://arxiv.org/abs/2606.23327)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)；[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)

### video-caption-accessibility · 双语字幕与无障碍版本
**合成输入**：原创90秒演示旁白，含术语“纸盒编号A17”和静音段；人工真值稿已设为练习输入。
**提示词**：输出原文字幕、译文、时间码与不确定词；静音不补字，数字逐项核对；补充与理解相关的非语言声音说明。
1. **建立真值**：人工写术语表与说话段落，先标静音和重叠语音，再选择识别语言。 验收：A17不可变成A70；静音不出现幻觉句。
2. **对齐与翻译**：转录后先校文本再对齐，翻译保持警告和否定；不启用需令牌的分离模型。 验收：字幕时间不倒退、不越片尾；人名不猜。
3. **可读性检查**：教学目标每屏最多2行，中文每行≤18字；目标展示速度≤8字/秒，超出重断句。 验收：这些是本练习可调整标准，不冒充通用法规。
4. **无障碍交付**：输出可切换字幕、烧录预览和声音说明稿，分别审查遮挡。 验收：关键按钮、动作不被字幕遮住。
**失败恢复**：对齐字典外词用人工时间码；重叠语音分段人工校对；不要把说话人编号当真实姓名。
**成本**：识别/对齐CPU或GPU均需测；下载模型及人工校对有成本，无令牌路径为本任务限制。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-whisper, vid-whisperx, vid-kdenlive
**来源**：[Whisper](https://github.com/openai/whisper)；[WhisperX](https://github.com/m-bain/whisperX)；[Kdenlive speech to text](https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html)

### video-narration-sync · 不克隆音色的配音与节奏
**合成输入**：原创40秒纸盒分类说明稿；假想本人新录旁白或许可明确非模仿TTS，角色为无嘴纸机器人。
**提示词**：按句分配镜头时长；保留呼吸停顿；不要模仿名人或现有角色音色，不做真人嘴型替换。
1. **旁白设计**：把说明分为四句，每句只包含一条操作；建立发音表。 验收：无未经证实性能声称，措辞与画面一致。
2. **音频优先**：先审核原创旁白时长，再安排B-roll；同步生成仅作为需另审许可的候选。 验收：声音素材归属与同意范围明确。
3. **对齐剪辑**：句子起止与动作对齐，转场放在停顿处，不压缩到词语失真。 验收：每句对应动作，终句没有截断尾音。
4. **混音质检**：检查爆音、突变、背景遮盖及单声道可懂度；记录实际峰值和测量工具。 验收：播放设备实听通过，不杜撰响度标准达标。
**失败恢复**：口型或同步不稳用非人形旁白镜头；声线许可不明则使用字幕，绝不代入真实人物。
**成本**：音视频联合生成通常额外算力；录音、剪辑、配乐版权不因开源模型而免费。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-ltx2, vid-wan22, vid-ffmpeg
**来源**：[LTX-2](https://github.com/Lightricks/LTX-2)；[Wan2.2](https://github.com/Wan-Video/Wan2.2)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)

### video-qc-evidence · 视频Agent的证据型质检
**合成输入**：原创60秒成片假想缺陷表：第2镜标记镜像、第4镜字幕超边、第5镜静音；另有一处暂时无法判断的道具跳变。
**提示词**：对每个问题输出时间码、观察证据、严重度、是否需人工；无法判断就unknown；不要只给整体美观分。
1. **设检查集**：准备合成缺陷真值，覆盖黑帧、重复帧、断音、字错、授权缺失与误导标签。 验收：包含干净对照段，能估计误报。
2. **分层检测**：技术检查读取媒体属性，语义检查对照脚本，抽帧用于预筛。 验收：不能声称抽帧排除所有瞬时缺陷。
3. **人工复核**：逐条回放候选时间段；对unknown保留待办，不用模型自信覆盖。 验收：报告真阳性/误报/漏报样例而非只有平均分。
4. **阻断交付**：版权不明、伪造事实、重要字幕错字为阻断项；修复后重跑相关检查。 验收：每项有负责人、修复版本及复审结论。
**失败恢复**：质检模型漏检时扩大采样或全片人工回放；模型不能充当法律、肖像授权的最终裁判。
**成本**：检测token和帧数有成本，长视频分层筛选不是保证零漏检。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-videoagent-understand, vid-ffmpeg, vid-whisper
**来源**：[VideoAgent long-form understanding](https://arxiv.org/abs/2403.10517)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)；[Whisper](https://github.com/openai/whisper)

### video-archive-reproducible · 项目归档与局部重做
**合成输入**：原创项目含6镜头、4张角色图、1份旁白、2种画幅与字幕；只归档合成素材。
**提示词**：输出manifest：文件SHA256、来源与许可、prompt、seed、模型/运行时revision、时间线、父版本、审批与失败记录；缺值写unknown。
1. **冻结清单**：源素材只读，工作输出分离；每镜建立稳定ID，manifest不含密钥与个人路径。 验收：所有时间线引用可解析。
2. **版本差分**：修第3镜字幕只新增字幕与交付版本，记录父版本和原因。 验收：不覆盖原批准文件，差分范围准确。
3. **可迁移检查**：交换时间线检查入出点、帧率与媒体定位；特效兼容性列为人工核验。 验收：OTIO文件存在不代表所有剪辑软件效果无损兼容。
4. **恢复演练设计**：在空目录重新定位素材并核对hash，未知模型revision阻止声称完全复现。 验收：输出恢复报告、缺失项与可用静态降级包。
**失败恢复**：文件失链从manifest找原资产；模型已下架保留成片与配置，迁移重渲染视为新版本。
**成本**：存储、备份、数据传输和恢复工时必须预算；seed相同也不保证跨硬件逐位一致。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-otio, vid-comfyui, vid-ffmpeg
**来源**：[OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)；[ComfyUI](https://github.com/Comfy-Org/ComfyUI)；[FFmpeg](https://ffmpeg.org/ffmpeg.html)

### video-historical-edit-migration · 历史视频微调迁移教学
**合成输入**：原创2秒纸船驶过蓝纸背景的设计稿；比较旧单视频微调与现代参考图生成，不下载运行任何外部代码。
**提示词**：建立对照表：训练是否需要、参考条件、运动保真、可控编辑、硬件、许可、环境；未知写unknown，禁止虚构获胜分数。
1. **还原历史假设**：分别记录论文版本、当时基础模型和训练输入，保留历史配置而不自动升级依赖。 验收：不把“历史”改写成维护者正式弃用。
2. **列替代路线**：免训练I2V适合尝试运动，传统动画适合精确路径；不是一比一模型替换。 验收：只有LTX迁移标记有维护者明确入口变化来源。
3. **设计公平比较**：同一原创角色、相同时长和输出分辨率，报告训练加推理总时间与失败率。 验收：无执行则表格为空，只有计划不能给成绩。
4. **保存迁移决策**：保留旧条目，另建替代案例链接、不可迁移项及许可差异。 验收：旧内容可查询，推荐与证据分离。
**失败恢复**：依赖不兼容停在文档级复盘；不要未经授权安装旧依赖或强行执行来源代码。
**成本**：微调有额外训练成本；现代生成不自动更便宜，比较必须同时记人工重做与显存。
**权限/风险**：可在隔离环境规划合成输入；下载/安装/模型推理/付费/上传/发布与账户访问均未授权且未执行；新操作另审。 全为原创合成教学输入与未执行设计；不使用真实账户、付费API、Mac、第三方执行代码或真实人脸/声音。不得做深伪、侵权剧本改编或伪实拍；发布前独立核素材/模型/声音/肖像/字体/音乐许可。
**生命周期**：unknown；适用版本：来源快照见source_ids；完整链路兼容版本未实测。；非行业最佳实践背书。
**技术关联**：vid-tune-a-video, vid-animatediff, vid-wan22, vid-ltx-video, vid-ltx2
**来源**：[Tune-A-Video](https://github.com/showlab/Tune-A-Video)；[Tune-A-Video paper](https://arxiv.org/abs/2212.11565)；[AnimateDiff](https://github.com/guoyww/AnimateDiff)；[Wan2.2](https://github.com/Wan-Video/Wan2.2)；[LTX-Video](https://github.com/Lightricks/LTX-Video)；[LTX-2](https://github.com/Lightricks/LTX-2)

## 技术节点与生命周期

### vid-wan22 · Wan2.2 文/图/音驱动视频 (model_family)
生成镜头的模型家族，不负责项目权限、预算、剪辑交付或事实核验。
- 状态：current_documentation_reviewed；适用版本：2.2
- 成本：官方TI2V-5B示例至少24GB VRAM；A14B I2V/S2V示例80GB。实际耗时、电费、租赁价未知；不得把此门槛套用全部变体。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-wan

### vid-ltx-video · LTX-Video 历史入口 (model_family)
维护者已把主要开发入口转至LTX-2；旧版用于版本迁移教学。
- 状态：superseded_per_maintainer；适用版本：LTX-Video legacy
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-ltxv

### vid-ltx2 · LTX-2 音视频生成 (model_family)
音视频生成与训练实现，后端、权重许可和资源要求需逐版本固定。
- 状态：current_documentation_reviewed；适用版本：LTX-2 family; revision not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-ltx2

### vid-cogvideox · CogVideoX (model_family)
视频扩散Transformer路线；代码与不同规模权重的许可边界须分开。
- 状态：current_documentation_reviewed；适用版本：CogVideoX-2B/5B / v3 2025-03-26
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-cog, vid-src-cogpaper

### vid-animatediff · AnimateDiff 运动模块 (method)
在图像扩散基础上引入运动模块的历史代表方法；不是退役断言。
- 状态：historical_pinned_specification；适用版本：revision unknown / v2 2024-02-08
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-animatediff, vid-src-animatepaper

### vid-tune-a-video · Tune-A-Video 单视频微调 (method)
历史单视频微调研究；与免训练图生视频是不同成本/控制路线。
- 状态：historical_pinned_specification；适用版本：ICCV 2023 implementation / v2 2023-03-17
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-tune, vid-src-tunepaper

### vid-comfyui · ComfyUI 图式运行时 (runtime)
节点图连接模型和处理步骤；增加目标、状态、反馈及权限控制才构成本文Agent设计。
- 状态：current_documentation_reviewed；适用版本：revision not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-comfy

### vid-whisper · Whisper 语音识别 (model_family)
用于字幕初稿，不生成声音；逐字与时间码仍需校对。
- 状态：current_documentation_reviewed；适用版本：revision not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-whisper

### vid-whisperx · WhisperX 对齐流程 (tool)
识别与时间对齐工具；说话人编号不证明真实身份。
- 状态：current_documentation_reviewed；适用版本：revision not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-whisperx

### vid-ffmpeg · FFmpeg 媒体处理 (tool)
按明确输入参数执行剪裁、混流、编码，不自主决定叙事。
- 状态：current_documentation_reviewed；适用版本：online documentation; local binary unknown
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-ffmpeg

### vid-otio · OpenTimelineIO 时间线交换 (standard_or_format)
序列化编辑决策与素材引用；素材归档和渲染另做。
- 状态：current_documentation_reviewed；适用版本：revision not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-otio

### vid-kdenlive · Kdenlive 字幕与转录剪辑 (tool)
依据配置的识别引擎制作字幕与选片，人工保留最终剪辑决定。
- 状态：current_documentation_reviewed；适用版本：26.08 manual
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-kdenlive

### vid-filmagent · FilmAgent 虚拟制片研究 (agent_system)
多角色在受限3D虚拟环境协作，需与实际电影拍摄能力区分。
- 状态：current_documentation_reviewed；适用版本：research project page
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-filmagent

### vid-vimax · ViMax 制片编排 (agent_system)
把策划、角色、镜头和生成连接起来；API配置示例不保证本地无付费互换。
- 状态：current_documentation_reviewed；适用版本：v1.2.0 announcement; head not pinned
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-vimax

### vid-videoagent-edit · VideoAgent 编辑框架（HKUDS） (agent_system)
多Agent编辑研究系统，不等于同名2024长视频问答项目。
- 状态：current_documentation_reviewed；适用版本：head not pinned / v1 metadata reviewed
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-videoagent, vid-src-videoagentpaper

### vid-videoagent-understand · VideoAgent 长视频理解（2024） (agent_system)
检索视觉证据进行问答的研究系统，不应列作视频生成模型。
- 状态：historical_pinned_specification；适用版本：paper metadata reviewed
- 成本：GPU/CPU、运行时与显存需求未实测；按固定版本小样测量。
- 许可：代码、权重、输入素材、字体音乐、插件分别核验；未完成法律/商用审核
- 来源：vid-src-understand

## 来源登记（发布日期不等于核验日）
- **vid-src-wan** [Wan2.2](https://github.com/Wan-Video/Wan2.2)；日期：2025-07-28；版本：2.2；定位：README: model table / TI2V / I2V / S2V。官方公开推理代码与权重；5B TI2V示例24GB显存，A14B I2V及S2V示例80GB；这是指定配置的门槛，不是所有流程的成本。
- **vid-src-ltxv** [LTX-Video](https://github.com/Lightricks/LTX-Video)；日期：未核验；版本：LTX-Video legacy；定位：README: New LTX-2。维护者声明LTX-2是主要开发入口；保留旧流程用于历史比较，迁移必须重核权重和接口。
- **vid-src-ltx2** [LTX-2](https://github.com/Lightricks/LTX-2)；日期：未核验；版本：LTX-2 family; revision not pinned；定位：README / LICENSE / LICENSE-2 / LICENSE-2_x。官方音视频生成与LoRA训练仓库；存在多份许可，不能从开放代码推断全部权重无条件商用。
- **vid-src-cog** [CogVideoX](https://github.com/zai-org/CogVideo)；日期：2024-08-06；版本：CogVideoX-2B/5B；定位：README: Model-License / News。旧THUDM URL跳转此官方仓库；2B与5B权重许可不同，代码Apache-2.0并不覆盖所有权重。
- **vid-src-cogpaper** [CogVideoX paper](https://arxiv.org/abs/2408.06072)；日期：2024-08-12；版本：v3 2025-03-26；定位：abstract / submission history。视频时空VAE和扩散Transformer方法；论文版本性能不等于每个历史权重规格。
- **vid-src-animatediff** [AnimateDiff](https://github.com/guoyww/AnimateDiff)；日期：未核验；版本：revision unknown；定位：README / license。运动模块框架，不是完整制片Agent；基础图像权重与LoRA许可另查。
- **vid-src-animatepaper** [AnimateDiff paper](https://arxiv.org/abs/2307.04725)；日期：2023-07-10；版本：v2 2024-02-08；定位：abstract / submission history。为同一基础图像模型家族增加可迁移运动模块；历史方法教学保留，不声称官方弃用。
- **vid-src-tune** [Tune-A-Video](https://github.com/showlab/Tune-A-Video)；日期：未核验；版本：ICCV 2023 implementation；定位：README。单视频微调研究实现；不能默认兼容最新环境。
- **vid-src-tunepaper** [Tune-A-Video paper](https://arxiv.org/abs/2212.11565)；日期：2022-12-22；版本：v2 2023-03-17；定位：abstract / submission history。单视频微调与结构引导的历史路线。
- **vid-src-comfy** [ComfyUI](https://github.com/Comfy-Org/ComfyUI)；日期：未核验；版本：revision not pinned；定位：README。图式推理编排工具；自定义节点是代码供应链边界，图本身不等于自主Agent。
- **vid-src-whisper** [Whisper](https://github.com/openai/whisper)；日期：未核验；版本：revision not pinned；定位：README。自动语音识别工具/模型；不是配音或音色克隆。
- **vid-src-whisperx** [WhisperX](https://github.com/m-bain/whisperX)；日期：未核验；版本：revision not pinned；定位：README: Diarization / Limitations。支持对齐流程；重叠语音及字典外内容有局限；说话人分离路径需要额外模型协议和令牌，本任务不启用。
- **vid-src-ffmpeg** [FFmpeg](https://ffmpeg.org/ffmpeg.html)；日期：未核验；版本：online documentation; local binary unknown；定位：official command documentation。媒体处理工具；使用前核验构建参数和编码器许可。
- **vid-src-otio** [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)；日期：未核验；版本：revision not pinned；定位：README。剪辑时间线交换数据与API，不是视频渲染器。
- **vid-src-kdenlive** [Kdenlive speech to text](https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html)；日期：未核验；版本：26.08 manual；定位：Speech Recognition。官方文档描述转录、字幕和按转录选片；功能需先配置识别引擎与模型。
- **vid-src-filmagent** [FilmAgent](https://filmagent.github.io/)；日期：未核验；版本：research project page；定位：abstract / Unity Environment。虚拟3D空间的多角色制片研究；不能外推为任意实拍场景或免费端到端电影制作。
- **vid-src-vimax** [ViMax](https://github.com/HKUDS/ViMax)；日期：2026-07-20；版本：v1.2.0 announcement; head not pinned；定位：README: News / Quick Start。Agent编排脚本分镜及生成；示例要求LLM/图像/视频API配置，不能等同已支持无账号本地免费替代。
- **vid-src-videoagent** [HKUDS VideoAgent](https://github.com/HKUDS/VideoAgent)；日期：未核验；版本：head not pinned；定位：README。视频理解、编辑、重制Agent框架；仅核验文档，无独立复现。
- **vid-src-videoagentpaper** [VideoAgent editing paper](https://arxiv.org/abs/2606.23327)；日期：2026-06-22；版本：v1 metadata reviewed；定位：abstract / metadata。编辑Agent研究；不导入作者成绩为通用质量承诺。
- **vid-src-understand** [VideoAgent long-form understanding](https://arxiv.org/abs/2403.10517)；日期：2024-03-15；版本：paper metadata reviewed；定位：abstract / metadata。长视频理解问答Agent，与HKUDS编辑框架同名但不是同一项目。

## 接入建议
cases字段接近content/cases.json v1；必须新增显式video适配器并保留raw_record，不修改现有roles/industries/learning适配器的默认假设。补充failure_recovery、compute_cost、permission_boundary进可见正文，防止归一化丢失。
nodes/edges/sources可独立提取为研究bundle；本文件直接导入ModelAtlas仅显示节点，不自动显示案例。不得将case id写成悬空node edge。
模型生成信号；工具执行操作；运行时组织图；Agent有目标、状态、规划、反馈、权限与终止。媒体格式不是模型；同名项目必须组织+年份消歧。
跨仓ID建议见JSON integration.cross_links；不写远端、不修改原repo。

## 维护与未完成验证
- 未实测任何生成、编辑、转录或Agent原生链路；未安装第三方代码或下载权重。
- 未核实全量模型具体许可证条款、价格与各操作系统兼容性；Blender官方手册抓取返回402，未引用其具体功能。
- Runway、Veo、Sora等付费/账号服务未执行；不以本轮检索暗示全行业覆盖。
- 未实测任何长片角色一致性、口型、完整版权清理或无障碍标准合规。
- 记录原来源与日期，不覆盖历史事实。
- 核查更新来源并生成差异，未证实状态设unknown。
- 在另行授权的合成小样环境验证，仅记录真实运行证据。
- 审查失败与成本，人工批准后才更新展示层与交叉链接。

## 结构验证
- JSON解析、来源和跨仓节点引用检查通过。
- AgentWork现有validate()验证12例通过；ModelAtlas现有normalize()验证16节点、9关系、20来源通过。仅调用纯校验函数，未运行build，禁止字节码写入，未改原仓库或远端。
- 上述结构验证不等于视频链路运行或质量验收。每案license和tool_model_agent_distinction另见JSON字段。
