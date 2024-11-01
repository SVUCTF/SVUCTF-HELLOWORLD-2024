---
title: Method
author: 13m0nde
difficulty: Easy
category: Web
image: ghcr.io/svuctf/svuctf-helloworld-2024/method:latest
port: 80
writeup_author: 13m0n4de
tags:
  - http
reference:
---

## 题目描述

## 题目解析

这是一道关于 HTTP 请求方法的题目。flag 被分成了多个部分，需要使用不同的 HTTP 方法（包括一个自定义方法）来获取每个部分。

### HTTP 请求方法基础

HTTP 请求方法是 HTTP 协议的基础组成部分，用于表明客户端希望对服务器上的资源执行什么样的操作。

每种方法都有其特定的语义，详细信息可以参考 [HTTP 请求方法](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods)。

常见的 HTTP 方法包括：

- GET：获取资源
- POST：提交资源
- PUT：上传或更新资源
- DELETE：删除资源
- OPTIONS：获取服务器支持的 HTTP 方法列表
- HEAD：获取资源的元信息
- PATCH：对资源进行部分修改
- TRACE：追踪请求-响应的传输路径

（如果你还不清楚如何发送 HTTP 请求，可以查看 [Param 题解](../param/README.md) 中对于 HTTP 请求和相关工具的介绍）

## 解题过程

发送 GET 请求：

```
$ curl "http://<IP>:<PORT>/"
```

发送 POST 请求：

```
$ curl "http://<IP>:<PORT>/" -X POST
```

发送 PUT 请求：

```
$ curl "http://<IP>:<PORT>/" -X PUT
```

发送 DELETE 请求：

```
$ curl "http://<IP>:<PORT>/" -X DELETE
```

发送 OPTIONS 请求：

```
$ curl "http://<IP>:<PORT>/" -X OPTIONS
```

OPTIONS 的返回头中，会给出所有允许的请求方法，返回头内容可以使用 `-v` 参数显示：

```
$ curl "http://<IP>:<PORT>/" -X OPTIONS -v

* Request completely sent off
< HTTP/1.1 200 OK
< Server: gunicorn
< Date: Fri, 01 Nov 2024 21:12:08 GMT
< Connection: close
< Content-Type: text/html; charset=utf-8
< Content-Length: 34
< Allow: GET, POST, PUT, DELETE, OPTIONS, SVUCTF
```

得知自定义方法为 `SVUCTF`。

发送 SVUCTF 请求：

```
$ curl "http://<IP>:<PORT>/" -X SVUCTF
```
