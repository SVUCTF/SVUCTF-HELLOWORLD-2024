---
title: Welcome
author: COOK
difficulty: Baby
category: Reverse
image:
port:
writeup_author: pn1fg
tags:
reference:
---

# Welcome

## 题目描述

## 题目解析

源码：[welcome.c](./build/welcome.c)

在 CTF 中，Re 类题目大致形式为：程序接收用户的一个输入，并在程序中对它进行一系列校验算法，如果通过校验则提示成功，此时的输入即Flag。这些校验的算法可能是已经编写在册的加密方案，也可能是作者自创的某种算法，这类题目要求参赛选手具备一定的算法能力。

首先，让我们查看文件类型：

```
$ file welcome.exe
welcome.exe: PE32+ executable (console) x86-64, for MS Windows, 19 sections
```

通过 `file` 命令可以看出，题目提供的 `welcome.exe` 是一个 64 位的 Windows PE 格式可执行文件。

要分析程序的执行流程，我们需要使用反汇编工具将二进制数据转换为可读的汇编指令。

我这里使用的工具是 Radare2，当然你们使用 IDA 看的会更舒服。

反汇编后的第一步就是寻找程序入口，也就是寻找程序的主函数。使用 `afl` 命令可以列出所有函数。

```asm
$ r2 -AA welcome.exe
[0x004014f0]> afl
0x004014f0    1     34 dbg.mainCRTStartup
0x004016b0    6    206 dbg.__security_init_cookie
0x00401180   44    786 dbg.__tmainCRTStartup
0x00401000    1      1 dbg.__mingw_invalidParameterHandler
0x00401010   14    262 dbg.pre_c_init
0x00401130    1     73 dbg.pre_cpp_init
0x00402bd0    1      6 sym.__getmainargs
0x004014c0    1     34 dbg.WinMainCRTStartup
0x00401520    1     25 dbg.atexit
0x00402b98    1      6 sym._onexit
0x00401540    1     12 sym.__gcc_register_frame
0x00401550    1      1 sym.__gcc_deregister_frame
0x00401560    1     27 dbg.flag
0x00402b50    1      6 sym.puts
0x0040157b    1     60 dbg.main
0x00401670    3     26 dbg.__main
0x004015c0    4     58 dbg.__do_global_dtors
0x00401600    8    103 dbg.__do_global_ctors
0x00401690    1      7 dbg.my_lconv_init
0x004016a0    1      3 dbg._setargv
0x00401790    4    248 dbg.__report_gsfailure
0x00401890    4     38 dbg.__dyn_tls_dtor
0x00402630   18    208 dbg.__mingw_TLScallback
0x004018c0   12    118 sym.__dyn_tls_init
0x00401950    1      3 dbg.__tlregdtor
0x00401960   10    218 dbg._matherr
0x00401a60    1      3 dbg._fpreset
0x00401a70    1    112 dbg.__report_error
0x00401ae0   26    503 sym.__write_memory.part.0
0x00401cf0   36    732 dbg._pei386_runtime_relocator
0x00401fe0    3     65 dbg.__mingw_raise_matherr
0x00402030    1     12 dbg.__mingw_setusermatherr
0x00402040   27    387 dbg.__mingw_SEH_error_handler
0x00402200   12    228 dbg.__mingw_init_ehandler
0x00402300   31    406 dbg._gnu_exception_handler
0x004024b0    7    107 sym.__mingwthr_run_key_dtors.part.0
0x00402520    5    118 dbg.___w64_mingwthr_add_key_dtor
0x004025a0   12    119 dbg.___w64_mingwthr_remove_key_dtor
0x00402b70    1      6 sym.free
0x00402710    3     30 sym._ValidateImageBase.part.0
0x00402730    3     12 sym._ValidateImageBase
0x00402750    7     72 sym._FindPESection
0x004027a0    9    143 dbg._FindPESectionByName
0x00402840    9    129 dbg.__mingw_GetSectionForAddress
0x004028d0    4     43 dbg.__mingw_GetSectionCount
0x00402900   10    108 dbg._FindPESectionExec
0x00402970    3     40 dbg._GetPEImageBase
0x004029a0   10    129 dbg._IsNonwritableInCurrentImage
0x00402a30   16    175 dbg.__mingw_enum_import_library_names
0x00402be0    1     31 dbg.__acrt_iob_func
0x00402c40    1      6 sym.__iob_func
0x00402c00    1      8 dbg.mingw_get_invalid_parameter_handler
0x00402c10    1     11 dbg.mingw_set_invalid_parameter_handler
0x00402c20    1     11 dbg.__p__acmdln
0x00402c30    1     11 dbg.__p__fmode
0x00402d10    1      5 sym.register_frame_ctor
0x00402ba8    1      6 sym._cexit
0x00402b58    1      6 sym.memcpy
0x00402b60    1      6 sym.malloc
0x00402b90    1      6 sym.abort
0x00402b88    1      6 sym.calloc
0x00402b78    1      6 sym.fprintf
0x00402b48    1      6 sym.signal
0x00402b38    1      6 sym.strncmp
0x00402bc0    1      6 sym.__set_app_type
0x00402bb0    1      6 sym._amsg_exit
0x00402bb8    1      6 sym.__setusermatherr
0x00402ba0    1      6 sym._initterm
0x00402b68    1      6 sym.fwrite
0x00402b80    1      6 sym.exit
0x00402b40    1      6 sym.strlen
0x00402b30    1      6 sym.vfprintf
0x00402af0    3     50 fcn.00402af0
```

由于这个可执行文件没有去除符号信息，我们可以直接找到 `main` 函数，查看 `main` 函数汇编代码：

```asm
[0x004014f0]> s sym.main
[0x0040157b]> pdf
            ;-- main:
            ; CALL XREF from dbg.__tmainCRTStartup @ 0x4013af(x)
┌ 60: int dbg.main (int argc, char **argv, char **envp);
│           0x0040157b      55             push rbp                    ; welcome.c:5 ; int main();
│           0x0040157c      4889e5         mov rbp, rsp
│           0x0040157f      4883ec20       sub rsp, 0x20
│           0x00401583      e8e8000000     call dbg.__main
│           0x00401588      488d0d8d2a..   lea rcx, str.Hello_Everyone_CTFer_ ; welcome.c:6 ; 0x40401c ; "Hello Everyone CTFer!" ; const char *s
│           0x0040158f      e8bc150000     call sym.puts               ; int puts(const char *s)
│           0x00401594      488d0d9d2a..   lea rcx, str.This_is_where_you_can_play_to_your_hearts_content_ ; welcome.c:7 ; 0x404038 ; "This is where you can play to your heart's content!" ; const char *s
│           0x0040159b      e8b0150000     call sym.puts               ; int puts(const char *s)
│           0x004015a0      488d0dc52a..   lea rcx, str.Go_find_the_hidden_flag ; welcome.c:8 ; 0x40406c ; "Go find the hidden flag" ; const char *s
│           0x004015a7      e8a4150000     call sym.puts               ; int puts(const char *s)
│           0x004015ac      b800000000     mov eax, 0                  ; welcome.c:10
│           0x004015b1      4883c420       add rsp, 0x20               ; welcome.c:11
│           0x004015b5      5d             pop rbp
└           0x004015b6      c3             ret
```

对应的 C 语言伪代码为：

```C
[0x0040157b]> pdg

ulong dbg.main(void)

{
    uchar *puVar1;
    ulong uStack_30;
    uchar auStack_28 [32];

    // int main();
    *(*0x20 + -0x30) = 0x401588;
    dbg.__main();
    puVar1 = *0x20 + -0x28;
    *(*0x20 + -0x28 + -8) = 0x401594;
    sym.puts("Hello Everyone CTFer!");
    *(puVar1 + -8) = 0x4015a0;
    sym.puts("This is where you can play to your heart\'s content!");
    *(puVar1 + -8) = 0x4015ac;
    sym.puts("Go find the hidden flag");
    return 0;
}
```

`main` 函数只有三个`puts`语句，打印了一些字符串，用于输出一些提示信息。
序
继续浏览程序的函数，看到了一个显眼的 `flag` 函数，其伪代码如下：

```c
[0x0040157b]> s sym.flag
[0x00401560]> pdg

void dbg.flag(void)

{
    ulong auStack_30 [5];

    // void flag();
    *(*0x20 + -0x28 + -8) = 0x401574;
    sym.puts("flag{W31c0m3_T0_SVUCTF!!!!}");
    return;
}
```

程序中 `puts` 函数输出的字符串就是本题 Flag。

Flag: `flag{W31c0m3_T0_SVUCTF!!!!}`
