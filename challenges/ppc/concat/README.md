# Soyo && Cat

- 作者：13m0n4de
- 参考：-
- 难度：-
- 分类：PPC
- 镜像：-
- 端口：-

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

```
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

」

## 题目解析

<analysis>
