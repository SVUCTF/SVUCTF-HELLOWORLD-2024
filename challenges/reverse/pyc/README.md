---
title: PYC
author: COOK
difficulty: Normal
category: Reverse
image:
port:
writeup_author: pn1fg
tags:
  - pyc
  - xor
reference:
---

# PYC

## 题目描述

## 题目解析

- 源码：[python.py](build/python.py)

查看文件类型：

```
$ file python.pyc

python.pyc: python 3.6 byte-compiled
```

这是一个 Python 源代码文件编译后生成的字节码文件，本题考察 pyc 文件的反编译。

使用 `pycdc` 进行反编译：

```python
$ pycdc python.pyc

# Source Generated with Decompyle++
# File: python.pyc (Python 3.6)

x = 'akf`|d4fe0ece*1562*3>?1*>?1b*d>?ecc27b004z'
flag = ''
flag = input('Please Input Flag:')
s = ''
for i in flag:
    m = ord(i) ^ 7
    s += chr(m)

if s == x:
    print('GOOD!!!')
else:
    print('NO!!!')
```

程序执行流程：

1. 输入 flag
1. 遍历字符串每个字符的 ASCII 值与数字 7 进行异或
1. 将结果转换为字符，拼接到字符串 `s` 中
1. 将得到的字符串 `s` 与预定义的字符串 `x` 进行比较
1. 相同输出 `GOOD!!!`，不同输出 `NO!!!`

异或 (XOR) 操作是可逆的，进行两次相同的异或操作，可以得到原来的数据。

据此，编写解密程序 [solve.py](./writeup/solve.py)：

```python
x = "akf`|d4fe0ece*1562*3>?1*>?1b*d>?ecc27b004z"
flag = ""

for char in x:
    s = chr(ord(char) ^ 7)
    flag += s

print("Decrypted flag:", flag)
```

Flag: `flag{c3ab7bdb-6215-4986-986e-c98bdd50e773}`
