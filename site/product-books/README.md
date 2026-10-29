# 产品使用书与基础评测 r1

这是新增、独立的教材层。旧 `data.json`、138 案例、原书稿与冻结 ZIP 不作为新成绩重计。产品手册只有经过审阅接纳后才进入 `index.json` 的 books；研究队列不是已交付教程。不得用同名简称自动选择厂商。

## 两层结构

- `tasks/`：独立基础任务，输入及哈希、作者参考、固定客观检查和人工量表。一个任务可映射多个产品，不得累加为多个独立评测成绩。
- `books/<product-id>/product-book.json`：产品操作层。一个业务配方一个 recipe_id，product_id 必填；仅在输入、目标、检查完全相同且被接纳时填写 task_id，否则 null。
- `expected_output_origin=author_reference` 是作者编写答案，绝不是模型输出。
- `product_execution=not_run`、`observed_results=null` 是当前证据边界。真实运行记录应另开记录，含产品/版本/输入哈希/时间/原始输出/授权与费用，不得覆盖作者参考或把本地检查结果写成产品运行。

## 离线复现

无需账号、网络、模型、SDK、安装软件或付费。使用已有 Python 3.10+：

```sh
python3 scripts/product_books.py validate
python3 scripts/product_books.py check awbench-clean-orders-v1 output.json
```

在解压目录运行；下载包保留 product-books 与 scripts 的相对结构。先阅读任务 JSON 的 prompt 和完整 fixtures，再把**自己的输出**保存为 UTF-8 JSON。检查器仅对照固定 JSON 契约，对象键顺序不计，数组顺序和类型计；不会运行提交的代码。代码修复题只做补丁文本和样例契约检查，不等于功能测试。离线检查通过不代表真实产品好用、性能、安全、部署或业务收益。

输入行号约定：订单 CSV 表头为第1行。所有人物称谓、日期、订单号和金额均为原创合成。四项基础任务与旧六事实会议包ID/字节独立，不改写旧来源证据。

## 接纳规范

sources 为完整 HTTPS 来源对象，含 id/title/url/accessed_at/claim_scope。官方文档支持的事实和作者建议分开。每步骤必须有 instruction/check/failure_recovery；input_artifacts 的相对路径不能逃出包目录，字节必须匹配 SHA-256。

完整产品包约定详见 `SCHEMA.md`。研究覆盖有限，待研究不表示已覆盖；没有无依据排名。许可证沿用仓库既有候选状态，本补包不宣称第三方资料再许可、不新增许可决定。

### r2 安全与映射修复

产品文件采用显式SHA库存，未知文件、符号链接及特殊文件会在公开复制/ZIP前拒绝。基础任务映射除ID还需精确契约摘要，产品提示词可不同；不匹配保持null。检查条目和人工量表不是运行成绩；human_fact/human_count始终需人工审阅。源码r2仍使用稳定的离线包链接文件名，ZIP内容哈希随版本变化，旧站点其他冻结ZIP完全不动。
