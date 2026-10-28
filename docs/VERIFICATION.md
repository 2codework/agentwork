# 本地验证记录

日期：2026-10-28。范围：本轮原创 AgentWork 候选工程，不含其他项目。

通过的实际命令：

```text
python3 -m unittest discover -s tests -v
Ran 19 tests ... OK
node --check web/app.js
(exit 0)
node tests/progress.test.js
Progress validation: 13 assertions passed
python3 scripts/build.py
Built 46 cases + 3 research chapters → site/
```

数据构成：9 个原创书本章节；2 个原创详细合成样例；研究适配 16 个岗位、14 个行业、14 个学习案例。所有 46 个案例均为合成教学设计，未声称端到端实机复现或真实收益。三份原始 JSON 与 Markdown 快照保留；生成器保留 case/source 完整原字段。BOOK.md 与站点来自同一构建。

未执行：浏览器视觉/键盘/屏幕阅读器 QA、真实浏览器 localStorage 中断测试、远端 CI、GitHub 仓库创建、推送、Pages 部署、生产数据处理。单元测试不能替代这些阶段。

发布待办：选定组织/仓库；负责人确认许可和公开范围；独立 QA；检查确切远端提交及真实发布 URL。未发起付费资源、联网执行案例、外部通知或第三方代码安装。

追加修复：导入日期使用严格 UTC 毫秒格式与 roundtrip 校验；拒绝不存在的日历日期和无时区输入，接受有效闰日。客服样例整体验收已区分反例前 6 行与加入第 7 条后 7 条复核。46 个案例新增独立生命周期字段，首批全 unknown；来源快照未修改。
