# r2 → r3修复记录

1. product.version_scope改为非空可读字符串；完整原版本数组保留channel_versions。
2. 每recipe补product_id、runner_implemented=false、reference_format与expected_product_artifact_format，业务真实成品与作者参考明确分开。
3. expected_output_artifacts列出每个参考文件的路径/SHA256/说明；保留完整内容，不让适配器猜测。
4. research_record保留两个厂商身份、generic alias/default:null、渠道版本、去重、覆盖缺口、许可；每recipe original_record保留lifecycle/practice/date等。role/authorization/cost/privacy均非空字符串。
5. 退款补rationale.md并同步prompt/声明输出；PM A1-A4补given/when/then，重复取消明确已退款/已释放前置与不再次释放；QA明确只创建test与bug两个文件，不改实现；security finding补函数load。
6. 八项均补具体负例验收。独立QC的r2证据保留在原目录，本包不篡改。
7. 自有fixture检查通过；QA coupon边界故意失败符合预期；没有运行厂商软件、模型、账号、security攻击或浏览器。人工rubric/视觉仍not_run。
8. 已使用当前framework product_books.py的validate_record逐条验8个recipe及产品/来源字段；固定校验器哈希记录在FRAMEWORK_VALIDATION.json。该检查不等于全站集成通过。

内容许可仍待负责人确认。r3仅写独立目录，不改canonical，不推送。

## r3 → r4
独立QA发现退款diff允许集合未纳入新增rationale.md；现统一为refund.py、test_refund.py、rationale.md，源数据、导出steps/check、BOOK一致。r3不改，r4重新生成并锁哈希。
