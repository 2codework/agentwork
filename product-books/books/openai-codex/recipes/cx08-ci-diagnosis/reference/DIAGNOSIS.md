# CI 诊断
ci.log 明确在启动测试前因 service 不存在失败；实际模块在 services/billing。
最小改动仅 working-directory，保留测试命令与退出码语义。
在该目录执行 python -m unittest discover -s tests -p test_*.py 可本地检查。
本包不触发 GitHub Actions；线上 runner、网络与 Action 版本尚未验证。
不使用 continue-on-error、不删除测试；获准提交后仍需查看真实 CI 结果。
