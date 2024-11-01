---
title: PHP Class
author: SMJB
difficulty: Normal
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/php_class:latest
port: 80
writeup_author: 13m0n4de
tags:
  - php
reference:
---

# PHP Class

## 题目描述

## 题目解析

以下是对题目源码的详细解释：

```php
<?php

include("flag.php"); // 引入 flag.php

highlight_file(__FILE__); // 输出当前文件源码

// 定义 SVUCTF 类
class SVUCTF
{
    // 定义类属性，public 代表可以被外部访问和修改
    public $username = "admin";
    public $password = "H3ll0_W0rld!";
    public $vip = false;

    // 登录方法，接收用户名和密码两个参数
    public function login($u, $p)
    {
        // 如果密码为预定义的 vip 用户名和密码，设置 vip 属性为 true
        if ($this->username === $u && $this->password === $p) {
            $this->vip = true;
        }
        return $this->vip; // 返回 vip 属性的值
    }
}

if (isset($_GET["username"]) && isset($_GET["password"])) { // 检查是否传入 GET 参数
    $svu = new SVUCTF(); // 创建 SVUCTF 实例
    if ($svu->login($_GET["username"], $_GET["password"])) { // 调用实例的 login 方法
        echo ("Welcome, " . $svu->username . ".<br>");
        echo ("Flag: " . $flag); // flag 变量来自 flag.php
    } else {
        echo ("You are not VIP!");
    }
} else {
    echo ("Input your params!");
}
```

所以只需要 GET 传入正确的用户名和密码：

```
http://<IP>:<PORT>/?username=admin&password=H3ll0_W0rld!
```

## 其他

验题的时候很纠结，看着是想要考察对于 PHP 类的基本知识，但只要识别出需要发送的 GET 请求数据就能获得 Flag，据说确实有选手是这么写的。

但如果专注于 PHP 类的知识，把类做得复杂，代码审计量就有点过头了，甚至越过了反序列化那题的难度。

难度给到了 Normal，对于题目设计初衷来说确实符合，但事实可能不然。

比较尴尬的题目。
