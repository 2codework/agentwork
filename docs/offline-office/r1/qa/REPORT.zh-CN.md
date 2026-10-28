# 离线会议行动项练习独立QA

**PASS：3项必须修复与1项澄清均关闭；仅限原创离线规则模拟。**

- 冻结源码 SHA256：`aa26200ed333ab9cb7f05d3f461a07ae2c322bf28329d54ee88a85365769de33`。
- ZIP SHA256：`9f20ed0318765e8e02938f334e71b83cfe3a626afc3c675410c9e2777f575484`。
- 自编CLI反例 25 项，源目录与独立解包分别通过。
- 330种schema类型变异无未捕获异常；所有业务报告dispatch_allowed=false。
- 深JSON、5000位整数、重复键、UTF8/文件上限、FIFO/symlink、同步事实伪造、审批过期和reject/0边界通过。
- 解包复跑作者19测试；13成员路径、类型、hash核验通过；两次独立打包与原ZIP逐字节一致。

## 已修复
- D1：Fixed complete six-fact contract anchored in reviewed source FIXED_ROWS; jointly changed input/submission rejected.
- D2：Regular file, final symlink and special-file checks; O_NOFOLLOW/O_NONBLOCK plus inode/device race check; FIFO rejected promptly.
- D3：ValueError/RecursionError produce invalid-input exit2; malformed encoding/json and numeric limits tested.
- D4：README explicitly separates synthetic review tests from manual user review; check-golden only good/bad; no automatic approve generation.

## 限制
- Only Linux Python3.12 actually exercised; Python3.10+ and other POSIX environments not runtime-certified; missing safe-open flags fail closed.
- Upper directory and reviewed source must be trusted; not a malicious-filesystem sandbox.
- Hashes bind bytes, not identity/signature; HUMAN-DEMO is not authenticated reviewer identity.
- Synthetic approve/reject state tests are not real human approval and grant no dispatch authority.
- Original design review retained as historical finding; final README/CHANGELOG describe resolved implementation.
- No network/product/model/SDK execution, credentials, Mac operation, canonical integration, push or deployment.
