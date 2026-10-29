# CSV-like scoring pipeline
入口 app.py:3 的 process 将文本交给 parser.parse，再调用 scoring.score。
解析器忽略空片段，把其余片段转为整数；非法文本抛 ValueError。
空字符串是 count=0,total=0；没有数据库、网络调用或持久化代码证据。
输入验证改 parser.py；增加统计项改 scoring.py。先补相应边界测试，再评估下游兼容性。
