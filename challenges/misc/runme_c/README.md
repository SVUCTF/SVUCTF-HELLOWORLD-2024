---
title: RunMe[C]
author: 13m0n4de
difficulty: Baby
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
reference:
---

# RunMe\[C\]

## 题目描述

作为计算机基础课程的第一课，C 语言是必备技能。本题你需要配置一个能够编译运行 C 语言程序的环境，并运行附件代码获取 Flag。

## 题目解析

附件源码：

```c
#include <stddef.h>
#include <stdio.h>

#define FLAG_LENGTH 23
#define KEY(i) ((i * 7) % 256)

int main(void) {
    const unsigned char enc_data[FLAG_LENGTH] = {
        0x66, 0x6b, 0x6f, 0x72, 0x67, 0x7a, 0x1a, 0x44, 0x67, 0x7c, 0x72, 0x23,
        0x0b, 0x18, 0x3d, 0x58, 0x04, 0x28, 0x30, 0xb5, 0xfb, 0xb2, 0xe7};
    char flag[FLAG_LENGTH + 1];

    for (size_t i = 0; i < FLAG_LENGTH; i++) {
        flag[i] = enc_data[i] ^ KEY(i);
    }
    flag[FLAG_LENGTH] = '\0';

    printf("%s\n", flag);
    return 0;
}
```

使用任何编译工具将 C 语言源文件编译成可执行文件，执行后即可得到 Flag。

Windows 上推荐安装 [MinGW-w64](https://www.mingw-w64.org/)，它是一个编译工具集合，提供了 GCC 编译环境。

举一个 Linux 命令行中使用 GCC 编译的例子，在 Windows 上命令行参数没太多差别。

```
$ gcc runme.c -o runme
$ ./runme
flag{Y0u_C4n_C_1t_N0w!}
```

Flag: `flag{Y0u_C4n_C_1t_N0w!}`

如果你用 IDE 软件帮你做这些也是可以的。

## 其他

有的选手因为 IDE 中自带编译器所支持的 C 语言标准过老或不完整，某些特性无法使用，比如无法在 for 循环初始化部分声明变量。

这个特性在 C99 标准中支持，而 C89 标准中不支持。

```c
// In C89
size_t i;
for (i = 0; i < FLAG_LENGTH; i++)

// In C99
for (size_t i = 0; i < FLAG_LENGTH; i++)
```

所以，手动修改代码，或使用更新的语言标准吧。
