---
title: Soyo && Cat
author: 13m0n4de && liseihoka
difficulty: Medium
category: PPC
image: ghcr.io/svuctf/svuctf-helloworld-2024/concat:latest
port: 70
writeup_author: 13m0n4de
tags:
  - ABNF
  - RFC
reference:
---

# Soyo && Cat

## 题目描述

soyo：「不要走，不是的，我，真的，把大家看得最重要，最喜欢的」\
soyo：「不要！」\
soyo：「拜托你了！」\
soyo：「小祥要是不在的话，我就」\
祥子：「松手」\
soyo：「要我怎么做你才能回来呢，只要我能做到的事情我什么都会去做的」\
祥子：「你真的...什么都会做么...」\
祥子：「在这个挑战中，你将使用一种特殊的符号系统来描述猫咪和容器（比如箱子）的位置关系。你的任务很简单：根据给出的场景描述，生成符合规定语法的文本表示。」\
soyo：「ん？」\
祥子：「例如『一只猫』：

```
cat
```

例如『两只猫在盒子里』：

```
[cat + cat]
```

以下是该语言的 [ABNF 表示法](https://zh.wikipedia.org/wiki/%E6%89%A9%E5%85%85%E5%B7%B4%E7%A7%91%E6%96%AF%E8%8C%83%E5%BC%8F)：

```abnf
SEQUENCE  =  POSITION / POSITION "=>" SEQUENCE
POSITION  =  ADJACENT
ADJACENT  =  OVER / ADJACENT "+" OVER
OVER      =  MULTIPLE / MULTIPLE "/" POSITION
MULTIPLE  =  CONCAT / NUMBER [ "*" ] MULTIPLE / NUMBER "/" MULTIPLE
CONCAT    =  SUBJECT [ NUMBER ] / [ PARTIAL ] CONTAINER [ PARTIAL ]
CONTAINER =  "[" OPT-POS "]" / "(" OPT-POS ")"
CONTAINER =/ "{" OPT-POS "}" / "<" OPT-POS ">"
OPT-POS   =  [ POSITION ]
SUBJECT   =  CAT / 1*ALPHA / "@"
CAT       =  "cat" / PARTIAL
PARTIAL   =  "c" / "a" / "t" / "ca" / "at"
ALPHA     =   %x41-5A / %x61-7A
NUMBER    =  1*DIGIT
DIGIT     =  "0" / "1" / "2" / "3" / "4"
DIGIT     =/ "5" / "6" / "7" / "8" / "9"
```

连接靶机：

```
nc <IP> <PORT>
```

」

## 题目解析

这是一道需要阅读 ABNF 语法规则的 PPC 题目。题目要求我们根据给定的场景描述，编写符合 ABNF 规则的字符串表示。

光看 ABNF 可能比较难，但如果找到这段 ABNF 的来源 —— [RFC 9402 - Concat Notation](https://datatracker.ietf.org/doc/html/rfc9402)，参考其中的案例，就会简单不少。

这份 RFC 文档是一篇愚人节作品，与[猫咪问答](../../misc/neko_quiz/README.md)中的 RFC 9564 一样。

不过在下面题目解析中，我们还是正经分析 ABNF 语法规则。

### ABNF 简介

ABNF (Augmented Backus-Naur Form) 是一种用于描述双向通信协议的标记语言。它广泛用于 Internet 规范，特别是 RFC 文档中。

#### 规则格式

```abnf
规则名称 = 规则定义
```

#### 常见操作符

- `/`：表示多个规则的任选其一
- `*`：表示重复（可以是零次或多次）
- `( )`：用于分组
- `[ ]`：表示可选项（零次或一次）
- `数字 * 规则`：表示规则重复指定次数

#### 示例

```abnf
command = "GET" / "POST"        ; command 可以是 GET 或 POST
digit = "0" / "1" / ... / "9"   ; digit 可以是 0-9 中的任意数字
number = 1*digit                ; number 是一个或多个 digit
ALPHA = %x41-5A / %x61-7A       ; A-Z / a-z
```

### 语法规则解析

#### 基本元素

- `SUBJECT`：主体元素
    - 可以是 `CAT`（猫）
    - 字母序列
    - 或 `@` （纱线球）
- `CAT`：猫
    - 完整的猫： `cat`
    - 部分的猫：`c`、`a`、`t`、`ca`、`at`
- `CONTAINER`：容器（比如盒子）
    - 方括号：`[]`
    - 圆括号：`()`
    - 花括号：`{}`
    - 尖括号：`<>`

#### 组合规则

- `SEQUENCE`：位置序列
    - 使用 `=>` 连接，表示状态的转换
    - 例如：`cat => [cat]` 表示猫进入盒子
- `POSITION`：相邻位置的组合
- `ADJACENT`：水平排列
    - 使用 `+` 连接
    - 例如：`cat + cat` 表示两只猫并排
- `OVER`：垂直排列
    - 使用 `/` 连接
    - 例如：`cat / cat` 表示两只猫上下叠
- `MULTIPLE`：重复表示法
    - 水平重复：`数字 * 对象`
        - 例如：`3 * cat` 等价于 `cat + cat + cat`
    - 垂直重复：`数字 / 对象`
        - 例如：`3 / cat` 等价于 `cat / cat / cat`
- `CONCAT`：基本的拼接操作

### 解题演示

| 场景描述                                                          | 文本表示                                   |
| ------------------------------------------------------------- | -------------------------------------- |
| 一只猫                                                           | `cat`                                  |
| 一只猫在盒子里                                                       | `[cat]`                                |
| 一只猫把头放进盒子里，另一只猫叠在这个盒子上                                        | `cat / [c]at`                          |
| 猫猫叠叠乐，三层叠放的盒子，每层盒子里都有一只猫，最上层的猫右侧还有个纱线球                        | `[cat + @] / [cat] / [cat]`            |
| 突然一只狗把刚刚猫猫叠叠乐的盒子撞飞了，猫咪也被吓跑了。描述从「猫猫叠叠乐」到「只剩下一只狗 (dog) 和纱线球」的过程 | `[cat + @] / [cat] / [cat] => dog + @` |

```
祥子：一只猫
soyo：cat
祥子：真是会虚情假意呢
------------------------------
祥子：一只猫在盒子里
soyo：[cat]
祥子：到现在都还执着于过去
------------------------------
祥子：一只猫把头放进盒子里，另一只猫叠在这个盒子上
soyo：cat / [c]at
祥子：真难看，你讲的话和做的事全都互相矛盾
------------------------------
祥子：猫猫叠叠乐，三层叠放的盒子，每层盒子里都有一只猫，最上层的猫右侧还有个纱线球
soyo：[cat + @] / [cat] / [cat]
祥子：CRYCHIC 已经毁了，绝对不可能再复活了
------------------------------
祥子：突然一只狗把刚刚猫猫叠叠乐的盒子撞飞了，猫咪也被吓跑了。描述从「猫猫叠叠乐」到「只剩下一只狗 (dog) 和纱线球」的过程
soyo：[cat + @] / [cat] / [cat] => dog + @
祥子：🤓☝️诶！但是我可以给你一个 Flag：
------------------------------
flag{SoyO_myg0_c0nC4T_256d8f8f4deb}
```

主打文案硬缝。

## 其他

解析器可能没有实现完全的语法规则，可以在 [grammar.rkt](./build/src/grammar.rkt) 查看实现的语法。

对于题目中的几个案例应该足够了。
