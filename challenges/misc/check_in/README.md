---
title: 签到一下
author: Rr19
difficulty: Baby
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
  - encoding
reference:
---

# 签到一下

## 题目描述

## 题目解析

先 Base32 解码再 Base64 解码：

```
$ echo "LJWXQ2C2GN2FQYKHIYYFQMSONBRGYODYLAZU42DFKY4C6WBSLJZVSV3DF5TFCPJ5" | base32 -d | base64 -d
flag{What_can_1_say_?_flag?}
```

Flag: `flag{What_can_1_say_?_flag?}`
