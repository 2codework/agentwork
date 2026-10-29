# AgentWork

**把智能体变成可验证的工作能力。** 中文开放实践手册与浏览器本地学习平台，面向岗位、行业和具体任务。

## 当前状态

网站：https://2codework.github.io/agentwork/ 。此仓库维护源码；线上对应提交以 Actions / Pages 结果为准，本地测试不等于线上验收。不是全行业大全；不保证无人值守自进化或全天候运行。

- 学习内容涵盖入门、任务拆解、安全与权限、文档表格演示、岗位、行业、评估、团队协作与维护贡献；章节以网站导航及生成的 `site/data.json` / `docs/data.json` 为准。
- 实践卡数量与分类以网站统计及生成的 `site/data.json` / `docs/data.json` 为准。合成练习、文档审阅和离线模拟不等于原版工具执行、实机复现或实际部署；每项证据与执行状态分别标注。
- 全文搜索（当前选择的阅读区）、岗位/行业筛选（实践区），来源与证据区分。
- 案例独立标注生命周期、适用版本、替代路径与最佳实践证据状态；案例独立评估，未知保持 unknown，不冒充现行行业最佳实践。
- 本地打卡、JSON 备份与合并导入，无登录、后端、分析埋点、上传或跨设备自动同步。

## 本地运行

需要 Python 3.10+；JS 检查另需 Node.js 18+。没有第三方运行/构建依赖，不需要安装软件包。

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node --check web/app.js
node tests/progress.test.js
python3 -m http.server 8000 --directory site
```

在浏览器打开本地 8000 端口。不要直接双击 HTML（浏览器可能阻止读取 JSON）。生成目录为 `site/`，路径全部相对，可用于 GitHub Pages 项目子路径。

## 结构

- `content/cases.json`：原创正文、练习与详细案例。
- `BOOK.md`：与网页同源自动生成，可离线直接阅读，勿手工编辑。
- `research/`：本轮研究快照及来源；不包含私有项目和用户历史。
- `scripts/build.py`：标准库 JSON 校验与静态构建；`normalize.py` 显式适配三种研究结构，失败即报错，保留全部原记录。
- `web/`：无框架界面；用户和内容文本不插入 HTML。
- `tests/`：构建、证据、安全约束与进度格式测试。
- `docs/`：内容规范、安全验收与发布说明；同时包含由 site/ 同步的 Pages 静态输出。
- `.github/workflows/checks.yml`：push/PR 只读门禁（无 schedule）；对应提交的实际结果须查阅 Actions。

## 进度与隐私

打卡记录以案例 ID 和完成时间存储在当前浏览器的 localStorage。私人/受限模式可能无法持久保存，此时页面会告警；请导出备份。导入在浏览器本地解析，最多 1 MB，只合并已存在案例 ID，需确认。清除数据、换设备或更换站点域名不会自动迁移记录。GitHub Pages 作为托管方可能记录普通网络访问，不能把“应用不上传进度”理解为匿名网络访问保证。

## 贡献与维护

先阅读 [贡献指南](CONTRIBUTING.md)、[内容规范](docs/CONTENT_SCHEMA.md) 与 [安全说明](SECURITY.md)。持续演进采用贡献→来源核验→测试→人工审阅→版本发布；不会自动抓取网页后直接发布。合成例子不代表真实企业的部署、效果或收益。

## 许可证候选

原创代码拟用 MIT；原创教材拟用 CC BY 4.0。作者署名为 AgentWork contributors。见 `LICENSE-CODE`、`LICENSE-CONTENT.md`；正式公开前由有权许可的负责人确认。第三方资料仅链接/必要短引，版权与许可证属于原权利人，不被本项目重新许可。

发布前请完成 [质量门禁](docs/QUALITY_GATES.md)；GitHub Pages 操作见 [部署说明](docs/DEPLOYMENT.md)。

## 创作专题 r0.2

网站：https://2codework.github.io/agentwork/ 。此仓库维护源码；线上对应提交以 Actions / Pages 结果为准，本地测试不等于线上验收。新增设计、音乐、视频资料以官方文档审阅为依据，未运行模型/付费 API/第三方工具，不承诺全量市场覆盖。

实践与技术使用经 ID 校验的 `?case=<id>` / `?node=<id>` 双向链接；模型、工具接口、标准、普通软件分别保留类型。书稿和网站由同一研究 JSON 构建。旧节点与案例保留；许可、费用、生命周期、来源和未实测状态不可省略。

## MCP、Skill 与提示词 · 十二课

新增 12 个原创深教程：角色、历史初始化、工具调用、资源与模板、错误、取消、权限、提示注入、Skill、调试、迁移与现行消息。每课在网站和同源书稿中完整保留目标、前置、输入输出、提示词、步骤、验收、错误、权限、来源与版本。MCP 2025-11-25 的 initialize 是历史教学；2026-07-28 对照采用逐请求元数据。Skills 扩展已发布、SEP-2640 Final；具体宿主支持仍待逐版本验证。

`learning/mcp/raw/` 原字节保留研究采集历史；`overlay.json` 是经核验的补充说明。页面默认展示显式适配后的教学正文，而非内部状态。ZIP 下载内含原包与 `VERIFIED-OVERLAY.json`；请同时阅读。只有原创标准库模拟契约经过测试，不是 MCP SDK、真实服务器、OAuth、模型或行业效果验证。没有安装、账号、付费或真实调用。

```sh
python learning/mcp/raw/validate.py
python -m unittest discover -s learning/mcp/raw/tests -v
```

不新增未经核验的版本事件或模型能力断言。保留全部旧案例、节点、日期覆盖层与互链；源网页的权利与适用条件不因本教程而改变。此仓库维护源码；线上对应提交以 Actions / Pages 结果为准，本地测试不等于线上验收。

## 区域办公平台学习补包

[7套区域办公平台人监督练习](REGIONAL_OFFICE.md)：Dify、Coze Studio、飞书 aily、钉钉宜搭、Zoho、百炼与腾讯云。准确区分托管/自托管/功能；来源、许可、租户和地域限制保留，全部 documentation-only / never-run。原研究与独立QA在 `learning/regional-office/r1/`，别名仅供搜索，不合并产品身份。

## 原创离线会议练习

从站点主导航“原创离线练习”或 `meeting-action-log` 案例打开 [练习页](docs/offline-office-lab.html)，下载 [固定源码ZIP](learning/offline-office/r1/meeting-action-lab-r1.zip) 与 [中文教程](learning/offline-office/r1/source/README.zh.md)。固定六条合成事实的标准库规则模拟，仅Linux已测；非模型、MCP或产品实测，不产生真实批准/外发。源码及独立QA原字节封存于 `learning/offline-office/r1/`。

## 原创离线创意交付练习

[24秒删去4秒后的跨轨交付](docs/creative-delivery-lab.html)：分镜、字幕、音乐占位和图卡的源/目的时间及版本一致性。下载[冻结36成员ZIP](learning/creative-delivery/r1/creative-delivery-lab-r1.zip)；仅已有Python标准库、合成JSON，无模型或真实媒体。作者25测试与24项golden、独立QA只验证自编规则，不是创作产品效果、版权许可或发布批准。138案例及原MCP/会议练习不变。

```sh
python -B scripts/creative_delivery_lab.py --check
```

构建及CI检查固定包字节、空目录解包25测试/24golden；页面检查将3种故意非法JSON负例按精确路径、SHA及拒绝原因单列，不把它们统计为有效JSON。所有其它JSON仍严格验证。源码位置`learning/creative-delivery/r1/source/`，历史验证摘要与限制见其`provenance/`；历史机器路径不是网站链接。接入候选本地通过不等于线上已发布。
