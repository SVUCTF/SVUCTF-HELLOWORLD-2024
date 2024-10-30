---
title: 乾坤大挪移
author: Rr19
difficulty: Easy
category: Misc
image:
port:
writeup_author: 13m0n4de
tags:
  - base64
  - steganography
  - file_carving
reference:
---

# 乾坤大挪移

## 题目描述

## 题目解析

附件没有拓展名，实际上是一个文本文件，可以直接用文本编辑器查看。

```
$ file 有胆你就来
有胆你就来: ASCII text, with very long lines (65536), with no line terminators
```

文件中的内容为 [Data URLs](https://developer.mozilla.org/en-US/docs/Web/URI/Schemes/data) 格式，这种格式可以将文件（这里是 MP4 视频）直接嵌入到文档中，语法如下：

```
data:[<media-type>][;base64],<data>
```

以附件为例：

| data | :   | video/mp4 | ;   | base64 | ,   | AAAAIGZ0eXB...   |
| ---- | --- | --------- | --- | ------ | --- | ---------------- |
| 协议   |     | MIME 类型   |     | 编码方式   |     | Base64 编码组成的文件内容 |

Data URLs 常用于在 HTML 中嵌入小型媒体文件，来避免额外的 HTTP 请求。

于是可以编写一段 HTML，使用 `video` 标签加载它，将其保存为 `.html` 后缀的文件。使用浏览器打开。

```
<video controls="">
    <source src="data:video/mp4;base64,XXXXXXX" type="video/mp4">
    Your browser does not support the video tag.
    </source>
</video>
```

视频中没有什么信息，可以选择右键保存视频文件继续分析。

![html_video](./writeup/html_video.png)

当然一开始就直接将 Base64 数据解码保存到文件中也是可以的。

```
$ cat 有胆你就来 | sed 's/^data:video\/mp4;base64,//' | base64 -d > output.mp4
$ file output.mp4 
output.mp4: ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]
```

如果查看视频 EXIF 信息会发现报有错误尾缀数据的警告：

```
$ exiftool output.mp4
Warning                         : Unknown trailer with truncated '\x14\x00\x09\x00' data at offset 0x6a2a3
Image Size                      : 540x556
Megapixels                      : 0.300
Avg Bitrate                     : 393 kbps
Rotation                        : 0
```

说明文件可能在尾部嵌入了其他文件，可以使用 [Binwalk](https://github.com/ReFirmLabs/binwalk) 或 [Foremost](https://github.com/gerryamurphy/Foremost) 等工具自动识别和分离：

```
$ binwalk output.mp4 -e
```

分离出一个带有密码的 Zip 文件。

使用十六进制查看器，看到压缩包文件内容后也跟着额外的数据，文本 `key:5201314`，代表压缩包密码。

```
$ xxd 6A2A3.zip
00000000: 504b 0304 1400 0900 6300 abb8 2559 abda  PK......c...%Y..
00000010: b7e0 3900 0000 1d00 0000 0800 0b00 666c  ..9...........fl
00000020: 6167 2e74 7874 0199 0700 0100 4145 0308  ag.txt......AE..
00000030: 00e1 8d62 4a2e 13f7 d28c 0f1a f9ca 42c7  ...bJ.........B.
00000040: e26e b993 d359 5b40 cbd0 7ac4 060d e68d  .n...Y[@..z.....
00000050: fc43 de91 5bc4 e145 dd33 1c8b d77b 5d8f  .C..[..E.3...{].
00000060: 57cc 5cd2 9bba efb5 62bd 504b 0708 abda  W.\.....b.PK....
00000070: b7e0 3900 0000 1d00 0000 504b 0102 1f00  ..9.......PK....
00000080: 1400 0900 6300 abb8 2559 abda b7e0 3900  ....c...%Y....9.
00000090: 0000 1d00 0000 0800 2f00 0000 0000 0000  ......../.......
000000a0: 2000 0000 0000 0000 666c 6167 2e74 7874   .......flag.txt
000000b0: 0a00 2000 0000 0000 0100 1800 2c49 ae07  .. .........,I..
000000c0: a5ff da01 2c49 ae07 a5ff da01 552a a1fd  ....,I......U*..
000000d0: a4ff da01 0199 0700 0100 4145 0308 0050  ..........AE...P
000000e0: 4b05 0600 0000 0001 0001 0065 0000 007a  K..........e...z
000000f0: 0000 000d 006b 6579 3a35 3230 3133 3134  .....key:5201314
00000100: 0d0a                                     ..
```

解压查看 flag.txt，得到 Flag：`flag{This_is_@ctually_a_fl@g}`
