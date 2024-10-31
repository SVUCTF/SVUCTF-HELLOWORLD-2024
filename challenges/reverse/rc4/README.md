---
title: StreamLock
author: pn1fg
difficulty: Medium
category: Reverse
image:
port:
writeup_author: pn1fg
tags:
  - rc4
  - base64
reference:
---

# StreamLock

## 题目描述

室友最近一直在看《吞噬星空》，我想要给他写一个番外，终于......

罗锋发现了一座神秘古老的大楼，门锁落满了灰尘，门旁躺着一个年久失修的机器人，机器人的零部件经历了岁月风霜的腐蚀已经无法正常工作。

罗锋擦了擦机器人的显示屏幕，突然！！！机器人发出阵阵兹兹的电流声，落满灰尘的门锁亮了起来......

## 题目解析

- 源码：[stream_lock.c](build/stream_lock.c)

查看文件类型：

```
$ file stream_lock

stream_lock: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=368e678a1aa96ff2179259bfe9696611a9566de7, for GNU/Linux 4.4.0, not stripped
```

64位，ELF 可执行文件

反编译 `main` 函数：

```c
$ r2 -AA stream_lock
[0x000010c0]> s main
[0x000015f5]> pdg

int __fastcall main(int argc, const char **argv, const char **envp)
{
  unsigned int v4; // [rsp+4h] [rbp-22Ch]
  char *s1; // [rsp+18h] [rbp-218h]
  char s[256]; // [rsp+20h] [rbp-210h] BYREF
  char v7[264]; // [rsp+120h] [rbp-110h] BYREF
  unsigned __int64 v8; // [rsp+228h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  printf("Input flag: ");
  fgets(s, 256, _bss_start);
  s[strcspn(s, "\n")] = 0;
  v4 = strlen(s);
  init("svuctf", v7, 6LL);
  encrypt(s, v7, v4);
  s1 = (char *)malloc(4 * ((int)(v4 + 2) / 3) + 1);
  base64_encode(s, s1, v4);
  if ( !strcmp(s1, "cShiGz8rdlXyFRggqjmEyOm4S5dblDTev+C5AM3FlRc=") )
    puts("Congratulations!");
  else
    puts("Try again!");
  free(s1);
  return 0;
}
```

程序首先预定义一串字符串，让用户输入一个 flag，并且移除换行符。

紧接着调用 `init` 函数与 `encrypt` 函数对字符串 flag 进行某种加密操作。

然后调用 `base64_encode` 函数对 `encrypt` 函数的结果进行 Base64 编码操作，最后与预定义的字符串进行比较。

反编译`init`函数：

```c
[0x000015f5]> s sym.init
[0x00001409]> pdg

unsigned __int64 __fastcall init(__int64 a1, __int64 a2, int a3)
{
  unsigned __int64 result; // rax
  unsigned __int8 v4; // [rsp+17h] [rbp-Dh]
  int i; // [rsp+18h] [rbp-Ch]
  int v6; // [rsp+1Ch] [rbp-8h]
  int j; // [rsp+20h] [rbp-4h]

  for ( i = 0; i <= 255; ++i )
  {
    result = i + a2;
    *(_BYTE *)result = i;
  }
  LOBYTE(v6) = 0;
  for ( j = 0; j <= 255; ++j )
  {
    v6 = (unsigned __int8)(*(_BYTE *)(j + a2) + v6 + *(_BYTE *)(j % a3 + a1));
    v4 = *(_BYTE *)(j + a2);
    *(_BYTE *)(j + a2) = *(_BYTE *)(v6 + a2);
    result = v4;
    *(_BYTE *)(a2 + v6) = v4;
  }
  return result;
}
```

程序连用两个 `for` 循环，第一个 `for` 循环是对数组进行初始化操作，第二个 `for` 循环是对刚刚初始化过的数组进行加密，加密的时候循环利用了主函数中传过来的字符串 `svuctf`。

分析到这，知识储备量大的同学就可以看出其实这是一个 RC4 的加密，而这个函数的作用就是初始化 S 盒并且利用密钥打乱 S 盒。

看不出的同学也不要紧，题目的名字与题目描述也给了我们提示，StreamLock 流锁，描述中也提到了门锁，上网冲浪即可搜到一些关键词「流密码，流加密算法」，也可识别出本题的加密方式是 RC4。

反编译 `encrypt` 函数：

```c
[0x00001409]> s sym.encrypt
[0x000014e9]> pdg

__int64 __fastcall encrypt(__int64 a1, __int64 a2, int a3)
{
  __int64 result; // rax
  char v4; // [rsp+16h] [rbp-Eh]
  int v5; // [rsp+18h] [rbp-Ch]
  int v6; // [rsp+1Ch] [rbp-8h]
  unsigned int i; // [rsp+20h] [rbp-4h]

  LOBYTE(v5) = 0;
  LOBYTE(v6) = 0;
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= a3 )
      break;
    v5 = (unsigned __int8)(v5 + 1);
    v6 = (unsigned __int8)(*(_BYTE *)(v5 + a2) + v6);
    v4 = *(_BYTE *)(v5 + a2);
    *(_BYTE *)(v5 + a2) = *(_BYTE *)(v6 + a2);
    *(_BYTE *)(a2 + v6) = v4;
    *(_BYTE *)((int)i + a1) ^= *(_BYTE *)((unsigned __int8)(*(_BYTE *)(v5 + a2) + *(_BYTE *)(v6 + a2)) + a2);
  }
  return result;
}
```

根据上面的分析，我们知道了这是 `RC4` 加密，那 `encrypt` 函数就是本题真正的加密函数。

程序每次通过修改 `v5` 和 `v6` 的值交换 `a2` 中的元素，然后生成一个伪随机字节 `v4`。该字节用于与 `a1[n]` 做异或运算，从而加密每个字节。

最后加密的数据存放在 `result` 中并返回主函数。

编写解密程序 [solve.py](./writeup/solve.py)：

```python
import base64


def rc4_init(key):
    S = list(range(256))
    j = 0
    key_length = len(key)

    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def rc4_decrypt(data, key):
    S = rc4_init(key)
    i = j = 0
    output = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]
        output.append(byte ^ K)

    return bytes(output)


if __name__ == "__main__":
    key = b"svuctf"
    encrypted_data_b64 = "cShiGz8rdlXyFRggqjmEyOm4S5dblDTev+C5AM3FlRc="

    encrypted_data = base64.b64decode(encrypted_data_b64)

    decrypted_data = rc4_decrypt(encrypted_data, key)

    print("解密后的数据：", decrypted_data.decode("latin-1"))
```

Flag: `flag{Stream_1s_n0t_a_Dream_RC4!}`
