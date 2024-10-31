---
title: Netcat
author: 13m0n4de
difficulty: Baby
category: Pwn
image: ghcr.io/svuctf/svuctf-helloworld-2024/nc:latest
port: 70
writeup_author: 13m0n4de
tags:
reference:
---

# Netcat

## 题目描述

> Hint: [萌新入门手册：如何使用 nc/ncat？](https://lug.ustc.edu.cn/planet/2019/09/how-to-use-nc/)

## 题目解析

PWN 类题目通常会给出：

- 靶机的 IP 和端口
- 一个程序文件（附件）

选手需要分析附件程序中的漏洞，攻击远程靶机以获取 Flag。

而这道题作为 PWN 分类下的签到题，设计相对简单：

- 端口上没有运行特定的程序，而是一个受限的 Linux Shell
- 选手只需要：
    - 学习使用 NetCat 连接远程服务
    - 运用基础的 Linux 命令找到 Flag

如何安装和使用 nc/ncat 可以参考提示里的文章链接。

连接靶机：

```
$ nc <IP> <PORT>
```

连接成功后，有无回显是要看出题人在远程服务器上的部署情况，本题就属于没有回显，连上直接进入一个 Linux Shell 中。

在其中可以执行一些 Linux 基本命令，如 `ls`、`cat`、`cd`、`pwd` 等。

使用 `pwd` 获取当前所在路径：

```
pwd
/
```

发现当前在根目录，使用 `ls` 命令列出当前目录下的文件：

```
ls
bin
dev
flag
lib
lib32
lib64
```

找到了 `flag` 文件，如果你不确定它是个文件，可以使用 `ls -la` 查看更多信息：

```
ls -la
total 32
drwxr-x---    1 1000     1000          4096 Oct 31 06:44 .
drwxr-x---    1 1000     1000          4096 Oct 31 06:44 ..
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:11 bin
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:11 dev
-rw-r--r--    1 1000     1000            43 Oct 31 06:44 flag
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:11 lib
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:11 lib32
drwxr-xr-x    1 1000     1000          4096 Oct 18 01:11 lib64
```

最后使用 `cat` 命令查看 `flag` 文件内容：

```
cat flag
flag{ea4734f0-0724-455a-a05b-9b2f23645d16}
```
