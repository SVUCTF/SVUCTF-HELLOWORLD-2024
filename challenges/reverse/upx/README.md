---
title: UPX
author: COOK
difficulty: Easy
category: Reverse
image:
port:
writeup_author: pn1fg
tags:
  - upx
reference:
---

## 题目描述

## 题目解析

- 源码：[upx.c](build/upx.c)

题目名字 UPX ，会探索的同学已经搜到了，这是一种程序的加壳技术，这里给同学们解释一下程序加壳。

### 壳的概念

壳是在一些计算机软件里也有一段专门负责保护软件不被非法修改或反编译的程序。

壳是在一个程序的外面再包裹上另外一段代码，保护里面的代码不被非法修改或反编译的程序。

它们一般都是先于程序运行，拿到控制权，然后完成它们保护软件的任务。

### 壳的分类

- 压缩壳
    - UPX
    - ASpack
    - PECompat
- 加密壳
    - APSrotector
    - Armadillo
    - EXEXCryptor
    - Themida

### 分析文件

通过上面的了解，我们知道本题程序有壳，检查一下（工具：`Detect It Easy`）：

```
$ file upx.exe && die upx.exe

upx.exe: PE32+ executable (console) x86-64, for MS Windows, 3 sections

Packer: upx.exe(4.24)[NRV2B_LE32,best]
```

64位 EXE 可执行程序，UPX 加壳，版本：4.24

脱壳（工具：`UPX`）

```
$ upx -d upx.exe

                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.4       Markus Oberhumer, Laszlo Molnar & John Reiser    May 9th 2024

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    357414 <-    125990   35.25%    win64/pe     upx.exe

Unpacked 1 file.
```

反编译 `main` 函数：

```c
$ r2 -AA upx.exe
[0x004014f0]> s sym.main
[0x0040157b]> pdg

ulong dbg.main(void)

{
    ulong uStack_30;
    uchar auStack_28 [32];

    // int main();
    *(*0x20 + -0x30) = 0x401588;
    dbg.__main();
    *(*0x20 + -0x28 + -8) = 0x401594;
    sym.printf("ohh,you are good!!!");
    return 0;
}
```

程序中只有一句字符串输出

反编译 `good` 函数：

```asm
[0x0040157b]> s sym.good
[0x00401560]> pdg

void dbg.good(void)

{
    ulong auStack_30 [5];

    // void good();
    *(*0x20 + -0x28 + -8) = 0x401574;
    sym.puts("ZmxhZ3s2YjRjMmU4NS04ZTcyLTQ2MWYtOTYxZi04MTQ1N2YxNDEzZmJ9Cg==");
    return;
}
```

程序中看到一串加密的字符串。

解密 Base64 得到 Flag。

Flag: `flag{6b4c2e85-8e72-461f-961f-81457f1413fb}`
