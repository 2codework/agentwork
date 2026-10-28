# assistant-workspace-research-r1 — QA修订

8项有限官方文档研究，全部 documentation-only / never-run，canonical未修改。

- research.json：实体、权限、日期边界、合成任务与验收
- GUIDE.zh-CN.md：中文指南
- sources.json / EVIDENCE.md：原观察与独立QA观察；不是全文快照
- before-qa/：原始9文件与sha256.json，原始字节保存
- QA-REVISION.json：逐实体/来源修订处置
- unknowns.json：首发抓取失败与Labs复核超时均保留，不再重试
- dedup.json：此前117案例/222节点快照（初始观察211），非最新集成基线
- build.py：仅从研究JSON渲染指南；不改canonical或调用产品。

当前帮助页的不可用提示不等于核实所有账号/代理功能停用；retirement=null。Perplexity日期08/04/26与02/05/26原字符串保留，规范事件日unknown/null。文档更新时间只记录观察。等待独立复核及父任务新基线，未开始集成。
