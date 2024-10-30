---
title: RunMe[EXE]
author: 13m0n4de
difficulty: Baby
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
reference:
---

# RunMe\[EXE\]

## 题目描述

下载并运行 exe 文件即可获得 Flag，但是……程序一闪而过看不清输出？

## 题目解析

双击执行 `runme.exe` ，出现一个一闪而过的黑框框，不要害怕自己运行了什么奇怪的病毒。

但是，**不要在本机上运行任何来源不明，功能不清的程序**是网络安全的第一课，哪怕是比赛的附件。

如果你点击下载，直接运行，只能感谢你十分信任我们啦。

这里出现的一闪而过的黑框中，其实输出了 Flag，但是由于输出后程序结束，窗口立刻就关闭了。

在 CMD 中运行，可以一直留下这个框框，也就能记下 Flag 了。

```
.\runme.exe
```

Flag: `flag{w0w_y0u_f0und_cmd!!!}`

如果你使用 Windows 10/11 ，那么你有更好看更好用的终端应用 [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) 可选。

终端应用和 Shell 是不同的概念，终端提供输入输出的界面，Shell 是实际解释和执行命令的程序。通俗来说，终端是你看到的窗口，Shell 是在窗口中实际工作的程序。

而 CMD 其实是二者的结合，即是一个终端界面（窗口），也包含了一个命令解释器 (`cmd.exe`)。

PowerShell 与 CMD 类似，也是二合一的。

而 Windows Terminal 纯粹是个窗口，可以运行各种 Shell (CMD、PowerShell)。

## 其他

之后的话大概不能直接将明文 Flag 存在可执行文件里了，可能有的选手是查看文件字符串得到的 Flag，有点违背题目设计初衷。
