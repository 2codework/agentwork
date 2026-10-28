# 创意工作流缺口增量 R2

核验日：2026-10-28。9案；基线97案。不是全球全集。仅公开官方文档核验与原创教材设计，**没有产品执行、离线模拟执行或效果实测**。

## 有用结论
- 新增CAD参数约束、3D交接/物理碰撞、逐帧动画、母版与讲义分版、窄带修复与双遍响度回执。
- 8案需提议新增工具节点（共6个）；FFmpeg案复用已有 `vid-ffmpeg`，不把普通工具称为模型或自主Agent。
- FreeCAD引用仓库已于2026-04-01归档；OpenSCAD页标v2021.01。未知发布日期保留null。
- 所有沙盒练习为待执行设计；下述验收条件不是通过结果。

## CAD：全约束草图到可改尺寸的教学零件 (`creative-r2-freecad-constrained-part`)
**角色**：工业设计师、CAD助教。**目标**：把几何需求变成可追溯特征树，而非仅生成外观图。
**新增价值**：97案例没有参数化CAD/全约束特征树；不同于产品图片合成。
**前置**：未来需经授权的 FreeCAD 安装；记录实际版本；毫米尺寸表；仅非承重虚构零件
**输入**：40×30×5毫米块和一个半径3毫米孔的原创尺寸卡
### 待执行步骤
1. 新建文档，切到 Part Design，创建 Body。
2. 在 XY 平面新建闭合矩形草图；将一角约束到原点，水平/垂直及长宽约束为40和30毫米；确认自由度为0。
3. 关闭草图，Pad 5毫米；保存基线。
4. 在顶面新建圆，半径3毫米，圆心距草图原点20/15毫米；全约束后 Pocket 选 Through all。
5. 另存变体，将矩形长度改为50毫米；检查孔位置和特征树错误，记录设计意图是否要求重新居中。
**输出**：待执行 FCStd 基线/变体；尺寸-约束-特征对照表
**验收**：草图0自由度；Pad/Pocket无错误；变更有人工设计意图签核
**失败与恢复**：草图端点重叠但不重合：检查 Coincident，不盲加约束；过约束：退回最近约束并记录；面附着/尺寸变化后重建失败：停在最后有效版本，人工修复引用
**安全沙盒（未运行）**：纸面列出40→50变化后哪些尺寸应变；故意省略圆心位置约束并预测自由度风险。 预期：识别圆可移动，不宣称实体建模已通过。
**版本/历史**：历史教程0.17+，当前UI/拓扑行为未实测；归档日期不代表软件停更。
**许可**：软件/文档/零件权利分开核验；不复制教程图片，不用于工程安全认证。
**节点映射**：design-freecad-partdesign [proposed_separate_node]
**来源**：[FreeCAD archived PartDesign tutorial](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Creating_a_simple_part_with_PartDesign.md)（访问核验2026-10-28）

## CAD：带边界校验的参数化环形垫片 (`creative-r2-openscad-parameter-guard`)
**角色**：参数化设计师、创意编程教师。**目标**：先拒绝非法参数，再产生可复查几何。
**新增价值**：新增代码驱动几何参数边界，非已有视觉token迁移。
**前置**：未来需授权 OpenSCAD；记录版本；原创非功能性展示尺寸
**输入**：三组原创参数
### 待执行步骤
1. 建立外径20、内径8、高度3三个变量，声明单位毫米。
2. 使用 assert 要求外径>内径>0且高度>0。
3. difference 中放外圆柱；内圆柱向下偏移0.1毫米且高度增加0.2毫米，避免共面边界。
4. 先预览，再完整渲染；检查孔贯通、轮廓连续；本轮不运行。
5. 对内径8、12、22建立参数表：22必须拒绝；保存源码和预期，不送打印。
**输出**：待执行 .scad 源码；合法/非法参数与预期矩阵
**验收**：非法参数先失败；孔不封闭；记录版本和尺寸单位
**失败与恢复**：等径或负值：assert 拒绝；共面导致布尔问题：保留微小贯穿余量；预览正常不代表最终实体正确：要求完整渲染复核
**安全沙盒（未运行）**：手工计算三组内外径关系，拒绝22；不启动 CAD。 预期：2组合法，1组拒绝；不是打印验证。
**版本/历史**：速查表明确v2021.01；不声称最新发行版。
**许可**：速查表显示CC-BY；引用链接而不复制版面；源码/输出模型与第三方库许可分开。
**节点映射**：design-openscad [proposed_separate_node]
**来源**：[OpenSCAD CheatSheet](https://openscad.org/cheatsheet/)（访问核验2026-10-28）

## 3D：从美术源文件到游戏 glTF 交接 (`creative-r2-gltf-handoff`)
**角色**：技术美术、3D设计师。**目标**：验证网格、纹理和尺度在跨工具交接中未丢失。
**新增价值**：现有视频图生模型和项目归档不覆盖3D资源格式/单位交接。
**前置**：未来授权的 Godot；预先自制GLB/GLTF，不需本轮Blender执行；记录源应用/导出器版本与资产权利
**输入**：原创1米立方体和自绘双色贴图的待建资产包
### 待执行步骤
1. 建立资产清单：主文件、纹理、参考尺寸、材质名。
2. 把GLB或GLTF+BIN+纹理完整复制到空白项目专用目录。
3. 等待导入；选资源打开 Import/Advanced，检查根节点类型与缩放。
4. 对照参考检查尺寸、朝向、法线与贴图；不要用OBJ承载骨骼动画。
5. 另存使用该资产的Godot场景；变更源文件后再导入并比较清单。
**输出**：导入设置记录；资产缺失/尺度差异清单；待执行场景
**验收**：尺度与参考一致；无丢纹理；源文件未被覆盖
**失败与恢复**：缺贴图：检查相对路径和完整资产包；尺度错误：记录Root Scale及Apply Root Scale，勿反复叠乘；blend直接导入依赖外部Blender：缺依赖时改由有授权者提供GLB，不绕过环境限制
**安全沙盒（未运行）**：纸面删除一个纹理引用，检查交接清单能否发现缺件。 预期：明确拒收缺件包。
**版本/历史**：stable滚动文档；正式实践固定Godot与导出器版本。
**许可**：仅原创几何与纹理；引擎许可不授予第三方模型/字体权利。
**节点映射**：design-godot-asset-pipeline [proposed_separate_node]
**来源**：[Godot available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)（访问核验2026-10-28）；[Godot import configuration](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html)（访问核验2026-10-28）

## 游戏资产：静态场景与动态道具碰撞分别验收 (`creative-r2-game-collision`)
**角色**：技术美术、游戏关卡设计师。**目标**：避免用渲染网格的外观代替碰撞行为验证。
**新增价值**：与3D外观交接不同：独立验证物理类型和碰撞语义；97案例无此任务。
**前置**：未来授权Godot和原创简模；静态地板/动态方块的角色表
**输入**：地板与方块角色表
### 待执行步骤
1. 导入两件原创简模并打开Advanced Import Settings。
2. 对地板节点启用Generate > Physics，Body Type选Static；按需求选Trimesh。
3. 对动态道具选Dynamic并选原始/凸形状，不将Trimesh用于动态体。
4. 在隔离测试场景预览碰撞形状，人工比对边界和穿透风险。
5. 未来运行掉落试验，保存接触/穿透结果；若失败先简化碰撞形状，不直接发布。
**输出**：碰撞类型配置表；待执行测试场景与失败记录
**验收**：动态体不使用Trimesh；角色与碰撞类型一致；运行结果空白直至实际测试
**失败与恢复**：动态Trimesh不适用：换凸/原始形状；凸分解过细：降低精度并重新检查几何；视觉正确但穿透：检查实际碰撞体，不标实测通过
**安全沙盒（未运行）**：给三张角色卡分配Static/Dynamic及允许形状，故意加入Dynamic+Trimesh。 预期：拒绝不匹配组合。
**版本/历史**：菜单以stable文档为依据；没有帧率或物理稳定性测量。
**许可**：使用原创几何，不使用文档中的第三方椅子模型。
**节点映射**：design-godot-asset-pipeline [proposed_separate_node]
**来源**：[Godot advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)（访问核验2026-10-28）

## 动画：原创精灵表切帧与循环验收 (`creative-r2-sprite-sheet`)
**角色**：2D动画师、游戏美术。**目标**：把逐格美术转成可调帧率的动画资源。
**新增价值**：不是扩散式视频循环：新增可编辑逐帧资源与游戏引擎切帧。
**前置**：未来授权Godot；原创128×32像素四帧横向精灵表，无第三方角色
**输入**：自绘四帧呼吸圆点
### 待执行步骤
1. 在空白场景添加AnimatedSprite2D，新建SpriteFrames资源。
2. 打开资源，选Add frames from a Sprite Sheet并指定原创图片。
3. 设置横4纵1，按顺序选帧；命名idle。
4. 设8FPS与循环，预览首尾衔接；记录透明边缘和角色锚点是否跳动。
5. 增加第二个动作时另建动画名；保留原帧序与FPS记录，不通过加速掩盖漏帧。
**输出**：待执行SpriteFrames资源；帧序/FPS验收表
**验收**：四帧顺序正确；每轮0.5秒为本练习目标；透明边缘与循环需未来视觉验收
**失败与恢复**：网格错误：确认图片尺寸可整除；边缘跳动：统一锚点与透明留白；首尾重复造成停顿：人工决定是否删除冗余帧
**安全沙盒（未运行）**：用帧编号0,1,2,3计算8FPS的一轮时长，并检查错序0,2,1,3。 预期：周期0.5秒；错序需人工复核，未做视觉预览。
**版本/历史**：Godot4命名AnimatedSprite2D；旧版本类名和界面需迁移。
**许可**：不下载官方教程示例素材；自绘，不模仿受保护角色。
**节点映射**：design-godot-spriteframes [proposed_separate_node]
**来源**：[Godot 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)（访问核验2026-10-28）

## 演示设计：母版变更的局部与全局影响控制 (`creative-r2-impress-master`)
**角色**：演示设计师、品牌运营。**目标**：统一视觉层级而不误覆盖特殊页面。
**新增价值**：既有design-slides-story侧重事实到叙事/API；此案专门处理母版影响范围。
**前置**：未来授权LibreOffice Impress；记录安装版；自制6页演示和原创母版
**输入**：原创6页课程与两类页面映射
### 待执行步骤
1. 复制源演示建立工作副本；标出5页常规页与1页特殊页。
2. View > Master Slide设置共用标题样式和背景元素，退出母版视图。
3. 选常规页，使用Change Slide Master/Load加载自制母版；先仅对当前页应用。
4. 确认无溢出后再有意选择全局替换；特殊页保留单独母版或单页重设。
5. 逐页检查标题、页脚、文本边界和对比；保存变更清单与原稿。
**输出**：待执行可编辑演示；母版-页面映射与差异记录
**验收**：特殊页保留设计；标题与页脚不溢出；可编辑源保留
**失败与恢复**：误勾全局：撤回并恢复副本；直接格式覆盖母版：检查例外，不宣称一键修复；字体替换：记录并人工调整
**安全沙盒（未运行）**：给6页标母版ID，在纸面模拟只改1页和改全部。 预期：影响范围不同，特殊页不能默默覆盖。
**版本/历史**：访问页显示26.8 Help；不同平台菜单名称可能有差异。
**许可**：自制模板及可用字体；帮助文本MPL2.0不等于所有模板许可相同。
**节点映射**：design-libreoffice-impress [proposed_separate_node]
**来源**：[Impress master view](https://help.libreoffice.org/latest/en-US/text/simpress/01/03150000.html)（访问核验2026-10-28）；[Impress changing master](https://help.libreoffice.org/latest/en-US/text/simpress/guide/masterpage.html)（访问核验2026-10-28）

## 演示交付：讲义与讲者备注分版防泄漏 (`creative-r2-impress-handouts`)
**角色**：培训设计师、培训运营。**目标**：把投影稿、学员讲义与内部备注明确分离。
**新增价值**：新增面向受众的交付版式/备注隔离，不重复幻灯叙事或字幕无障碍。
**前置**：未来授权Impress；不连接实体打印机；虚构6页内容；内部备注仅写虚构提醒
**输入**：原创6页演示；虚构备注
### 待执行步骤
1. 创建交付清单，区分学员版与讲者版。
2. File > Print中Document选Handouts，设每页3张；先只预览不发送。
3. 在Handout视图配置Notes and Handouts的页眉页脚，标注学员版并Apply to All。
4. 另一次选择Notes制作讲者版预览，检查备注可见性；不要混为学员讲义。
5. 人工检查页序、字号及是否含备注；只在确认本地打印到文件能力后未来另存两个文件，否则记录阻塞。
**输出**：两份待执行交付设置；学员/讲者泄漏检查表
**验收**：学员版不含内部备注；页序完整；没有未授权打印/外发
**失败与恢复**：讲义太小：减少每页张数；误选Notes：取消作业并重新预览；本地无打印到文件：不发送打印、不假称已生成PDF
**安全沙盒（未运行）**：分拣三条虚构备注到学员可见/仅讲者，模拟选错Notes。 预期：学员版不得包含内部备注。
**版本/历史**：26.8帮助；打印对话框/输出文件能力依OS变化。
**许可**：不分发模板字体或第三方插图；讲义版权与软件版权独立。
**节点映射**：design-libreoffice-impress [proposed_separate_node]
**来源**：[Impress printing presentations](https://help.libreoffice.org/latest/en-US/text/simpress/guide/printing.html)（访问核验2026-10-28）

## 音频后期：窄带嗡声的最小破坏修复 (`creative-r2-spectral-hum`)
**角色**：音频后期师、播客剪辑师。**目标**：仅处理定位到的窄带干扰，不把降噪当作万能人声恢复。
**新增价值**：现有播客后期是Auphonic多轨处理；新增局部时频编辑的破坏边界。
**前置**：未来授权Audacity；未来自制测试音/原创录音；不含真实敏感对话
**输入**：拟自制50Hz嗡声叠加原创测试信号
### 待执行步骤
1. 保存未处理副本，记录轨道和项目采样率。
2. 切到Spectrogram并启用Spectral Selection。
3. 圈定嗡声所在时间和窄频带，记下上下频率；保持在轨道Nyquist内。
4. 使用专用Spectral edit效果预览处理；不要用普通Delete代替频带编辑。
5. 在相同监听电平比较前后，检查目标频带及邻近内容；损伤明显则撤销并缩小范围。
**输出**：待执行修复副本；频段/时间/参数与人工听评表
**验收**：时间区域外不得误删；频带合理；未听评不得称修复成功
**失败与恢复**：交通/铃声宽带复杂：不承诺可修复，转人工判断；普通删除影响全频：撤销；越过Nyquist或项目/轨道采样率不符：修正选择
**安全沙盒（未运行）**：对48kHz轨道标出50Hz目标带和30kHz非法选择。 预期：Nyquist为24kHz，30kHz选择应拒绝；没有生成/聆听音频。
**版本/历史**：Development Manual不等于已安装版本；先核对效果菜单。
**许可**：只用原创测试信号；录音授权、软件与插件许可分别核验。
**节点映射**：music-audacity-spectral [proposed_separate_node]
**来源**：[Audacity spectral selection](https://manual.audacityteam.org/man/spectral_selection.html)（访问核验2026-10-28）

## 音频交付：双遍响度归一化与测量回执 (`creative-r2-loudness-two-pass`)
**角色**：音频交付工程师、视频后期师。**目标**：将测量、处理与重新测量分开，留下可审计参数。
**新增价值**：现有母带助手/Auphonic不是显式双遍测量回执；已有vid-ffmpeg可复用，不增假模型。
**前置**：未来授权FFmpeg且含loudnorm；原创PCM WAV、明确的本练习目标：I=-16,LRA=11,TP=-1.5，非平台通用标准
**输入**：原创PCM WAV与目标卡
### 待执行步骤
1. 记录输入哈希、声道、版本和48kHz输出目标；先保存副本。
2. 第一遍以loudnorm I=-16:LRA=11:TP=-1.5:print_format=json测量到null输出，保留日志。
3. 将测得I/LRA/TP/thresh及target_offset填入第二遍对应measured_*与offset参数；保持同一输入和目标。
4. 指定linear=true与-ar 48000输出新PCM WAV；查日志确认实际模式，不能假设必定线性。
5. 对输出再测量并人工听评；与交付约定比较，失败保留记录而非覆盖原件。
**输出**：待执行归一化WAV；两遍参数及复测日志
**验收**：记录实际线性/动态模式；48kHz输出核对；输出复测和听评未完成不得称交付通过
**失败与恢复**：线性条件不满足会回退动态：记录模式并人工判断；静音/非有限测量：停止，不盲填NaN；输入变更：重做第一遍；动态模式内部升采样：明确输出采样率
**安全沙盒（未运行）**：虚构输入I=-20、TP=-3，若线性增益+4dB则TP=+1，超过-1.5上限。 预期：识别不可直接线性放大；不得声称实际输出达标。
**版本/历史**：在线FFmpeg选项可能超出旧构建；正式执行前固定版本并查滤镜帮助。
**许可**：FFmpeg构建可能LGPL/GPL不同；不分发二进制。音频权利独立，示例目标非合规保证。
**节点映射**：vid-ffmpeg [existing_verified]
**来源**：[FFmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)（访问核验2026-10-28）；[FFmpeg legal](https://ffmpeg.org/legal.html)（访问核验2026-10-28）

## Agent边界与执行证据
Agent仅提议参数、校验清单和记录证据；软件执行明确操作，人类决定审美和最终交付。本轮没有实现或执行自主循环。
本轮只读公开文档+编写教材；未安装、调用产品/API、付费、登录、上传素材、使用Mac、改写仓库或制造实体。

## 精确阻塞记录
- web.open https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html — uncertain：工具返回 HTTP 402 Payment Required；不是确认的用户权限拒绝，也不推断网站实际收费；未绕过或用于证明能力。
- web.open https://docs.blender.org/manual/en/4.5/render/cycles/baking.html — uncertain：工具返回 HTTP 402 Payment Required；不是确认的用户权限拒绝，也不推断网站实际收费；未绕过或用于证明能力。
- web.open https://docs.blender.org/manual/en/4.5/animation/keyframes/introduction.html — uncertain：工具返回 HTTP 402 Payment Required；不是确认的用户权限拒绝，也不推断网站实际收费；未绕过或用于证明能力。

## 维护与历史
未知发布日期保持null；版本标签不是发布日期；历史来源保留并明确适用范围。
未来集成前新增6个工具节点并复用vid-ffmpeg；逐条执行需另有授权环境/素材，并记录版本、输入哈希、截图或日志、失败与人工验收。

## 官方来源登记（发布日期均未核实）
- `r2-freecad` [FreeCAD archived PartDesign tutorial](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Creating_a_simple_part_with_PartDesign.md)；版本：教程标注 0.17 or above；main 未固定 SHA；访问：2026-10-28；状态：web_open_verified。仓库页面明确标注 2026-04-01 归档；不是软件被废弃的证据。
- `r2-openscad` [OpenSCAD CheatSheet](https://openscad.org/cheatsheet/)；版本：v2021.01；访问：2026-10-28；状态：web_open_verified。官方站点速查表；链接到社区手册不等于本轮已核验该手册。
- `r2-godot-formats` [Godot available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)；版本：stable 滚动文档；具体版本未固定；访问：2026-10-28；状态：web_open_verified。旧 Godot 4.0/3.0 文档不可当作当前 FBX 导入依据。
- `r2-godot-config` [Godot import configuration](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html)；版本：stable 滚动文档；具体版本未固定；访问：2026-10-28；状态：web_open_verified。
- `r2-godot-advanced` [Godot advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)；版本：stable 滚动文档；具体版本未固定；访问：2026-10-28；状态：web_open_verified。Trimesh 只能配静态碰撞体；不能把精确三角碰撞直接用于动态物体。
- `r2-godot-sprite` [Godot 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)；版本：stable / AnimatedSprite2D；访问：2026-10-28；状态：web_open_verified。不下载文档示例美术；素材署名和许可需独立核验。
- `r2-impress-master` [Impress master view](https://help.libreoffice.org/latest/en-US/text/simpress/01/03150000.html)；版本：页面显示 LibreOffice 26.8 Help；访问：2026-10-28；状态：web_open_verified。
- `r2-impress-change` [Impress changing master](https://help.libreoffice.org/latest/en-US/text/simpress/guide/masterpage.html)；版本：页面显示 LibreOffice 26.8 Help；访问：2026-10-28；状态：web_open_verified。
- `r2-impress-handout` [Impress printing presentations](https://help.libreoffice.org/latest/en-US/text/simpress/guide/printing.html)；版本：页面显示 LibreOffice 26.8 Help；访问：2026-10-28；状态：web_open_verified。打印到文件能力取决于本地系统；本轮未验证 PDF 输出。
- `r2-audacity-spectral` [Audacity spectral selection](https://manual.audacityteam.org/man/spectral_selection.html)；版本：Development Manual；具体安装版未知；访问：2026-10-28；状态：web_open_verified。对单一恒定频率少量谐波更适合；普通剪切会忽略频率范围。
- `r2-ffmpeg-loudnorm` [FFmpeg loudnorm filter](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)；版本：在线文档；本地二进制未知；访问：2026-10-28；状态：web_open_verified。目标响度由交付合同决定；不能把示例值称为所有平台标准。
- `r2-ffmpeg-license` [FFmpeg legal](https://ffmpeg.org/legal.html)；版本：访问日页面；具体构建未知；访问：2026-10-28；状态：web_open_verified。分发二进制、链接库与音频素材权利是不同问题；非法律结论。

## 本地验证结果
9个唯一ID，与97案基线无ID冲突；12个来源引用全部解析；必需字段齐全；所有执行标志为false。人工比较目标与交付物排除既有案例重述。该检查仅验证研究材料结构，不验证软件/音频/视觉结果。
