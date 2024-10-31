---
title: 欸我 Flag 呢
author: 13m0n4de
difficulty: Baby
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/nc_hidden:latest
port: 70
writeup_author: 13m0n4de
tags:
reference:
---

# 欸我 Flag 呢

## 题目描述

## 题目解析

这题与 [NetCat](../nc/README.md) 大致相同，只是 Flag 文件被放在了隐藏目录中。

使用 `ls` 命令的 `-a` 选项列出全部文件，可以查看出 `ls` 看不到的 `.hidden` 目录：

```
ls
bin
dev
lib
lib32
lib64

ls -la
total 32
drwxr-x---    1 1000     1000          4096 Oct 31 06:59 .
drwxr-x---    1 1000     1000          4096 Oct 31 06:59 ..
drwxr-xr-x    2 1000     1000          4096 Oct 31 06:59 .hidden
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:40 bin
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:40 dev
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:40 lib
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:40 lib32
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:40 lib64
```

在 Linux 中，以 `.` 开头的文件被称为隐藏文件 (Hidden Files) 或点文件 (Dotfiles)，这些文件默认是隐藏的。

但这是一个命名约定，`ls` 命令默认会过滤掉以 `.` 开头的文件和目录，但文件本身并没有引入任何特殊机制。

`cd` 命令进入 `.hidden` 目录，`ls` 查看目录下文件，`cat` 获取 `flag` 文件的内容：

```
cd .hidden

pwd
/.hidden

ls
flag

cat flag
flag{86f6bd16-8ca6-4903-adf6-81d82814fc9e}
```
