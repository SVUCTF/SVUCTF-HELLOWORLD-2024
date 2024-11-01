---
title: 1337 Machine
author: 13m0n4de
difficulty: Normal
category: PPC
image: ghcr.io/svuctf/svuctf-helloworld-2024/leet_machine:latest
port: 70
writeup_author: 13m0n4de
tags:
  - pwntools
reference:
---

# 1337 Machine

## 题目描述

教学楼的某个角落，你发现了一台古老而神秘的设备 —— 1337 Machine，这台机器曾经是顶尖的语言转换装置，能将普通文本完美地转化为 [Leet](https://zh.wikipedia.org/zh-cn/Leet) 文本。

然而，岁月的侵蚀使得这台机器变得极度不稳定。它的电路板正在冒烟，显示屏闪烁不定，发出令人不安的嗡鸣声。

突然，机器苏醒了！它开始疯狂地生成随机英文句子，仿佛在寻求某种解脱。屏幕上闪现出一条紧急消息：

「系统不稳定，需要立即进行 100 次成功的 Leet 转换以稳定 Flag 核心。」

> Hint: Leet（英文中亦称 leetspeak 或 eleet。Leet 拼写法：L337, 3L337, 31337 或 1337），又称黑客语，是指一种发源于西方国家的 BBS、在线游戏和黑客社群所使用的文字书写方式。通常是把拉丁字母转变成数字或是特殊符号，例如 E 写成 3、A 写成 @ 等。或是将单字写成同音的字母或数字，如 to 写成 2、for 写成 4 等等。

## 题目解析

### 分析题目

这是一道自动化编程题目，需要与远程服务进行交互。根据题目描述，这是一台需要修复的 1337 (Leet) 转换机器。

连接到远程服务后，机器会提供一个明确的转换规则表：

```
$ nc <IP> <PORT>

  .---------.
  |.-------.|
  ||>1337# ||
  ||       ||
  |"-------'|
.-^---------^-.
| ---~   ---~ |
"-------------'

==================================================
1337 Machine 唤醒中...
==================================================
系统日志: 检测到核心不稳定
系统日志: 启动紧急修复程序
系统日志: 需要执行 100 次成功的 LEET 转换以重新校准系统
系统日志: 检测到转换模块配置如下
a -> 4
e -> 3
g -> 6
i -> 1
o -> 0
s -> 5
t -> 7

按下回车键开始系统修复...
```

题目的核心机制很直观：

- 机器会随机生成英文句子
- 我们需要按照给定的规则将这些句子转换为 Leet 格式
- 这个过程需要成功完成 100 次才能获取 flag，并且有时间限制
- 每次转换都必须准确，任何错误都会导致程序终止

### 编写自动化脚本

由于需要处理 100 次转换，手动操作显然不切实际，需要编写脚本自动化整个过程。

使用 Python 的 [pwntools](https://docs.pwntools.com/en/stable/) 库编写解题脚本是最直接的方法。这个库提供了便捷的远程交互功能，比较适合这类 PPC 题目。

#### 第一步：建立连接

使用 pwntools 连接到远程服务：

```python
from pwn import *

io = remote("localhost", 1337)
```

这里使用 pwntools 的 `remote` 函数创建了一个连接对象，用于与服务器进行交互。

#### 第二步：实现转换规则

根据题目给出的转换规则，我们需要将特定字母转换为数字。可以用字典来存储这些映射关系：

```python
LEET_DICT = {"a": "4", "e": "3", "g": "6", "i": "1", "o": "0", "s": "5", "t": "7"}
```

然后编写一个转换函数：

```python
def convert_to_leet(sentence):
    return "".join(LEET_DICT.get(char, char) for char in sentence)
```

这个函数使用了字典的 `get` 方法，如果字符在字典中存在就进行转换，否则保持原字符不变。使用列表推导式和 `join` 方法可以简洁地完成字符串转换。

#### 第三步：处理初始化过程

程序开始时需要等待启动提示并发送回车：

```python
io.recvuntil("按下回车键开始系统修复...".encode())
io.sendline(b"")
```

#### 第四步：实现主要转换循环

接下来是主要的转换循环，需要重复 100 次：

```python
for _ in range(100):
    # 接收待转换的文本
    io.recvuntil("输入文本: ".encode())
    sentence = io.recvline().decode().strip()
    log.info(sentence)

    # 转换文本
    leet_sentence = convert_to_leet(sentence)
    log.info(leet_sentence)

    # 发送转换结果
    io.sendlineafter("输出 LEET 文本 > ".encode(), leet_sentence.encode())

    # 检查响应
    response = io.recvline().decode()
    if "转换成功" not in response:
        log.failure(f"转换失败: {response}")
        break

    # 打印分隔线方便查看
    log.info("-" * 40)
```

#### 第五步：获取 flag

完成转换后进入交互模式以获取 flag：

```python
io.interactive()
```

### 完整脚本

[solve.py](./writeup/solve.py)

```python
from pwn import *

io = remote("localhost", 1337)

LEET_DICT = {"a": "4", "e": "3", "g": "6", "i": "1", "o": "0", "s": "5", "t": "7"}


def convert_to_leet(sentence):
    return "".join(LEET_DICT.get(char, char) for char in sentence)


io.recvuntil("按下回车键开始系统修复...".encode())
io.sendline(b"")

for _ in range(100):
    io.recvuntil("输入文本: ".encode())
    sentence = io.recvline().decode().strip()
    log.info(sentence)

    leet_sentence = convert_to_leet(sentence)
    log.info(leet_sentence)

    io.sendlineafter("输出 LEET 文本 > ".encode(), leet_sentence.encode())
    response = io.recvline().decode()
    if "转换成功" not in response:
        log.failure(f"转换失败: {response}")
        break

    log.info("-" * 40)

io.interactive()
```

### 运行效果

脚本运行的输出大致如下：

```
[*] ----------------------------------------
[*] Red general similar someone peace question even.
[*] R3d 63n3r4l 51m1l4r 50m30n3 p34c3 qu35710n 3v3n.
[*] ----------------------------------------
[*] Dark standard guy read.
[*] D4rk 574nd4rd 6uy r34d.
[*] ----------------------------------------
[*] Switching to interactive mode
系统状态: 100/100

系统日志: 修复成功，Flag 核心已稳定
Flag: flag{test_flag}
```
