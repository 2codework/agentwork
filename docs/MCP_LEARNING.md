# MCP 课程适配与边界

完整原包存放于 `learning/mcp/raw/`，原字节保持不变；历史采集措辞不代表当前整合状态。`overlay.json` 为额外核验说明，ZIP 中以 `VERIFIED-OVERLAY.json` 提供。未重写原包，不将协议版本日期当作发布日期。未新增版本事件。

`scripts/mcp_learning.py` 显式检查案例与 tutorial 字段集合、字符串/列表类型、固定路径、fixture 输入输出、来源引用、ID、版本与离线状态；拒绝未知扩展字段。修改 schema 必须同时修改适配器及负例测试，不允许猜字段或静默丢弃。

两站默认读者正文来自同一适配器 `lesson_markdown`，包含目标、前置、权限、错误、提示词、输入输出、三步与验收、来源、版本、未实测与失败处理。JSON 与代码使用 textContent 渲染，禁止 HTML/JS 执行。历史 raw 在折叠区；下载不会自动运行。Markdown 书稿同源生成。

现行 MCP 2026-07-28 与历史 2025-11-25 initialize 分开。Skills 已发布、SEP-2640 Final 依据官方 overview 与工作组；检索不等于激活，代码执行/权限授予逐 skill 审批，宿主支持另查。没有 SDK/真实服务/OAuth/模型调用。18 个测试仅验证原创狭窄模拟契约，不能作为兼容或真实效果证明。没有权利清理/许可保证。

CI 仍仅 push/PR，contents:read，无 schedule。原始实验命令、完整模拟范围及取消竞态限制见课程包 README。发布与部署由维护者在独立 QA 后处理。
