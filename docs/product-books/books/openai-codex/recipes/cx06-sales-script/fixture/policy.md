金额非负整数分（允许 0）；paid 加，refund 减，cancelled 忽略。完全相同的重复 id 只算一次并计 duplicate_rows。相同 id 内容冲突须 ValueError，负金额/未知状态也 ValueError。不改源 CSV。
