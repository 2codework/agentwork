# AgentWork

**把智能体变成可验证的工作能力。** 中文开放实践手册与浏览器本地学习平台，面向岗位、行业和具体任务。

## 当前状态

r1 已公开上线：https://2codework.github.io/agentwork/ 。当前文件是 r0.2 创作专题候选，未声明已部署；经独立 QA 后由维护者发布。不是全行业大全；不保证无人值守自进化或全天候运行。

- 九章入门→任务拆解→安全与权限→文档表格演示→岗位→行业→评估→团队协作→维护贡献。
- 85 个合成实践卡：保留原 46 个，新增设计 13、音乐 14、视频 12；均未实机复现，不是实际部署。
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
- `.github/workflows/checks.yml`：push/PR 只读门禁候选（无 schedule）；发布后须核验实际 Actions 结果。

## 进度与隐私

打卡记录以案例 ID 和完成时间存储在当前浏览器的 localStorage。私人/受限模式可能无法持久保存，此时页面会告警；请导出备份。导入在浏览器本地解析，最多 1 MB，只合并已存在案例 ID，需确认。清除数据、换设备或更换站点域名不会自动迁移记录。GitHub Pages 作为托管方可能记录普通网络访问，不能把“应用不上传进度”理解为匿名网络访问保证。

## 贡献与维护

先阅读 [贡献指南](CONTRIBUTING.md)、[内容规范](docs/CONTENT_SCHEMA.md) 与 [安全说明](SECURITY.md)。持续演进采用贡献→来源核验→测试→人工审阅→版本发布；不会自动抓取网页后直接发布。合成例子不代表真实企业的部署、效果或收益。

## 许可证候选

原创代码拟用 MIT；原创教材拟用 CC BY 4.0。作者署名为 AgentWork contributors。见 `LICENSE-CODE`、`LICENSE-CONTENT.md`；正式公开前由有权许可的负责人确认。第三方资料仅链接/必要短引，版权与许可证属于原权利人，不被本项目重新许可。

发布前请完成 [质量门禁](docs/QUALITY_GATES.md)；GitHub Pages 操作见 [部署说明](docs/DEPLOYMENT.md)。

## 创作专题 r0.2 候选

r1 已上线于 https://2codework.github.io/agentwork/ 。本目录是待独立 QA 的 r0.2 候选，不代表已经发布。新增设计、音乐、视频资料以官方文档审阅为依据，未运行模型/付费 API/第三方工具，不承诺全量市场覆盖。

实践与技术使用经 ID 校验的 `?case=<id>` / `?node=<id>` 双向链接；模型、工具接口、标准、普通软件分别保留类型。书稿和网站由同一研究 JSON 构建。旧节点与案例保留；许可、费用、生命周期、来源和未实测状态不可省略。
