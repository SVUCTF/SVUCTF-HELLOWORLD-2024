---
title: RunMe[Python]
author: 13m0n4de
difficulty: Baby
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
reference:
---

# RunMe\[Python\]

## 题目描述

Python 是 CTF 中的瑞士军刀，无论哪个方向都能用到它。本题你需要配置一个能够解释运行 Python 程序的环境，并运行题目给出的代码获取 FLAG 。

## 题目解析

附件源码：

```python
encrypted_flag = "kqfl{q6k8_60_0m5w2_d5z_s88i_ud2m5s}"
shift = 5
flag = ""

for char in encrypted_flag:
    if char.isalpha():
        ascii_offset = ord("A") if char.isupper() else ord("a")
        flag += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
    elif char.isdigit():
        flag += str((int(char) - shift) % 10)
    else:
        flag += char

print(flag)
```

在 [Python 官网](https://www.python.org/downloads/) 下载安装与你操作系统对应的 Python 解释器（此题无版本要求，日常使用的话推荐最新的稳定版），之后运行附件文件即可。

```
$ python runme.py
flag{l1f3_15_5h0r7_y0u_n33d_py7h0n}
```

## 其他

如果你好奇 `encrypted_flag` 是怎么得出来的（或者说这题怎么出的），实际上这是一个凯撒密码 (Caesar Cipher) 的变体，加密时只需要把 `encrypted_flag` 改为实际 Flag，`shift` 改为 `-5`，即可得到 `kqfl{q6k8_60_0m5w2_d5z_s88i_ud2m5s}`。
