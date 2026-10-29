# 问候CLI
依赖：Python 3标准库；无需pip，无网络。
运行：`python tool.py --name Ada`
输出：`Hello, Ada!`
参数：--name必填。遗漏参数时argparse显示required错误且非零退出。
旧--user不受支持；请迁移到--name。
