# 修复“刚好满50元仍收运费”的小错误

一个只改一处条件的 shipping.py，以及4项测试结果和修复说明；不提交代码、不上线。

适合：刚接触AI编程、会打开终端的开发者或测试人员；完全不写代码的人可先读前5个任务。

## 1. 准备什么

- 先有能联网的电脑和你获准使用的产品账号。没有客户端请按下面“第一次打开”操作；本教程没有替你安装、登录或购买。

- 本例还需要已有Python 3与可用终端。

- [下载 shipping.py](inputs/fix-small-bug/shipping.py)

- [下载 test_shipping.py](inputs/fix-small-bug/test_shipping.py)

- [下载 README.txt](inputs/fix-small-bug/README.txt)

### 输入全文（也可直接复制）

#### shipping.py
```text
def shipping_fee(order_cents):
    """订单金额为非负整数分；满5000分免运费，否则收600分。"""
    if order_cents > 5000:
        return 0
    return 600

```

#### test_shipping.py
```text
import unittest
from shipping import shipping_fee

class ShippingTests(unittest.TestCase):
    def test_empty_order(self):
        self.assertEqual(shipping_fee(0), 600)
    def test_below_threshold(self):
        self.assertEqual(shipping_fee(4999), 600)
    def test_exact_threshold(self):
        self.assertEqual(shipping_fee(5000), 0)
    def test_above_threshold(self):
        self.assertEqual(shipping_fee(5001), 0)

if __name__ == "__main__":
    unittest.main()

```

#### README.txt
```text
虚构商店练习。Python 3标准库，无第三方依赖。输入是非负整数分。满5000分免运费，否则600分。运行：python -m unittest -v。只在练习副本运行，不用于真实结算。

```

## 2. 用什么，不用什么

OpenAI Codex CLI（已有终端工具）

- 工具：需要已有Python 3与Codex自带文件编辑、终端执行能力。不需要第三方Python包。

- MCP：不需要。本例不连GitHub、数据库或生产系统。

- Skill：不需要。一个边界判断修复，用明确规则和测试即可。

## 3. 打开哪里，怎么开始

### 第一次打开

- 还没有Codex：这条适合愿意使用终端的读者。先看 [Codex CLI官方快速开始](https://learn.chatgpt.com/docs/codex/cli)，由你本人选择对应系统的安装方式并完成；这里不代你运行安装脚本。Windows用户不要照抄其他系统命令。

- 在项目目录输入codex，首次按提示选择“Sign in with ChatGPT”或你获准的现有方式，自行完成登录。只用账号现有权益，不要求新建API key；组织禁用时找管理员，不绕过。

- Python 3若尚不可用，本页只做代码阅读；不要让AI为了这4项测试装一堆依赖。准备好后再从下方第1步开始。

### 已经可以使用，开始任务

1. 将本页3个输入文件下载到一个新建的空文件夹，例如“运费练习”；不要把参考答案放进去。

2. 复制这个文件夹为“运费练习-副本”，原输入留作备份。

3. 在副本文件夹打开终端，先确认能看到 shipping.py、test_shipping.py、README.txt，再输入 codex 并回车。

4. Codex打开后输入 /status 核对当前目录，输入 /permissions 查看权限；只允许这个副本目录的读写和测试，不开启全盘权限。

5. 粘贴完整提示词。遇到命令确认时核对是当前目录的 python -m unittest -v，不批准安装、联网、提交或部署。

6. 查看文件差异和测试输出；用下方清单验收。

只用虚构练习材料，不上传真实客户资料。AI服务可能消耗现有额度；账号功能、地区和组织许可需本人确认。没有额度时停止，不自动购买。首次安装与登录均由读者自行操作；暂不具备条件可做纸面练习，不能记为产品执行成功。

## 4. 复制这段提示词

```text
你现在只处理当前练习目录里的 shipping.py、test_shipping.py、README.txt。业务规则：输入为非负整数分，订单金额满5000分免运费，否则收600分。现在刚好5000分时收了600分，请找原因并做最小修复。先阅读文件并运行 python -m unittest -v，记录修复前失败；只修改shipping.py，不改测试期望、不改单位、不添加新功能。然后再次运行同一命令。最后给我代码差异、修复前后实际测试结果和一句原因说明。只用已有Python标准库，不联网、不装依赖、不读取目录外文件、不提交Git、不推送、不部署。如果命令不可用或权限不足，请停下说明，不能把未运行写成通过。
```

## 5. 完整参考结果

示例由作者编写，步骤据2026-10-29官方文档；未在产品内执行。

## 最小修改
```diff
-    if order_cents > 5000:
+    if order_cents >= 5000:
```

## 完整 shipping.py
```python
def shipping_fee(order_cents):
    """订单金额为非负整数分；满5000分免运费，否则收600分。"""
    if order_cents >= 5000:
        return 0
    return 600
```

## 作者参考测试结果
- 修复前：4项测试中，刚好5000分一项失败，实际600、预期0。
- 修复后：0、4999、5000、5001分四种输入，运费依次为600、600、0、0，4项通过。
- 原因：“满5000”包含5000本身，因此比较条件应为大于或等于。
- 范围：未增加负数、字符串等非法输入处理；这些不在本次约定中。

这是作者在本地验证的参考实现，不是Codex执行日志。你自己的任务必须保留实际命令与结果。


## 6. 怎么检查，出错怎么办

- 看差异：仅 > 变成 >=，测试文件没有被改。

- 四项测试都运行，而不是只试5000一个数字。

- 确认实际货币单位仍是分，不是把5000改成50。

- 如果没有Python或Codex，本例停在阅读，不能标“修好了”。

- 提示找不到codex：你尚未具备这条路线的前提；先看完整参考结果，不在本练习安装。

- 提示找不到python：若机器已有python3，可将命令换为python3 -m unittest -v；否则停止，不安装依赖。

- 测试仍失败：把完整错误文本贴回同一任务，要求只解释失败原因，再局部修复。

- 改动太大：丢弃练习副本，重新复制输入，强调只改一个条件；不要对真实仓库执行回滚命令。
