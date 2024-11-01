---
title: RunMe[ELF]
author: 13m0n4de
difficulty: Baby
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
reference:
---

# RunMe\[ELF\]

## 题目描述

运行失败了？别着急，这是个 Linux 程序。配置一个 Linux 环境（虚拟机或 WSL），就能顺利拿到 Flag。

## 题目解析

配置好 Linux 环境（无论你是虚拟机还是 WSL 还是直接装在物理机上），将附件传入。

移动到同一目录，在终端中执行：

```
$ ./runme
```

如果你得到了无法执行之类的错误，说明从平台下载下来是不带执行权限的，需要添加权限后执行：

```
$ chmod +x runme
$ ./runme
flag{chm0d_+x_ftw!}
```

Flag: `flag{chm0d_+x_ftw!}`

初学者推荐安装一个 Kali Linux 的虚拟机，其中会带有一些 CTF 常用工具。

建议去[官网](https://www.kali.org/get-kali/#kali-virtual-machines)下载 Vmware 版的虚拟机文件，这样比较方便。
