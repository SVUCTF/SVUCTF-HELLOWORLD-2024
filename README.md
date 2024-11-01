<div align="center">

# SVUCTF-HELLOWORLD-2024

本仓库用于存储和构建 SVUCTF-HELLOWORLD-2024 的题目镜像。

Powered by GZCTF and GZTime

![poster](assets/poster.png)

感谢 [@liseihoka](https://github.com/liseihoka) 帮助制作封面，封面潮得可怕

</div>

## 说明

本仓库用于存储和构建 SVUCTF-HELLOWORLD-2024 的题目镜像、题解。

欢迎各位选手以 Pull Request 的形式提交自己的 write-up 。

若大家对本仓库有任何疑问或改进建议，欢迎提 Issue 。

所有幕后花絮可在 [behind-the-scenes](./behind-the-scenes/README.md) 中找到。

比赛时间：北京时间 2024 年 10 月 26 日 09:00 ～ 10 月 31 日 20:00 （共 5 天 11 小时）

## 目录

- [题目](#%E9%A2%98%E7%9B%AE)
    - [Misc](#Misc)
    - [PPC](#PPC)
    - [Pwn](#Pwn)
    - [Reverse](#Reverse)
    - [Web](#Web)
- [难度与分值](#%E9%9A%BE%E5%BA%A6%E4%B8%8E%E5%88%86%E5%80%BC)
- [来自参赛者的题解](#%E6%9D%A5%E8%87%AA%E5%8F%82%E8%B5%9B%E8%80%85%E7%9A%84%E9%A2%98%E8%A7%A3)
- [致谢](#%E8%87%B4%E8%B0%A2)

项目结构：

```
.github/workflows/
    └── <category>.<name>.yml
assets/                             # 资源文件，如封面图
base/                               # 基础镜像
behind-the-scenes/                  # 幕后花絮
challenges/                         # 所有题目
    ├── web/                        # 题目分类
    │   ├── challenge1/             # 题目
    │   │   ├── build/              # 构建文件
    │   │   │   ├── Dockerfile
    │   │   │   └── more...
    │   │   ├── attachments/        # 附件
    │   │   ├── writeup/            # 题解文件    
    │   │   └── README.md           # 题目信息（含题解文本）
    │   └── more...
    └── more...
player-write-ups/                   # 来自参赛者的题解
```

## 题目

部分题目在比赛中划分了更细的分类，但在仓库中没作更改，如 [猫咪小测](./challenges/misc/neko_quiz/README.md) 仍在 Misc 分类而不是 OSINT。

### Misc

|                              题目描述与题解                              |   难度    |                        附件                         |                      源代码                      |                                                                   镜像                                                                   |                 标签                  |   出题人    |
| :---------------------------------------------------------------: | :-----: | :-----------------------------------------------: | :-------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------: | :------: |
|            [签到一下](challenges/misc/check_in/README.md)             |  Baby   |    [附件](challenges/misc/check_in/attachments)     |                       -                       |                                                                   -                                                                    |              encoding               |   Rr19   |
|          [RunMe\[C\]](challenges/misc/runme_c/README.md)          |  Baby   |     [附件](challenges/misc/runme_c/attachments)     |     [源代码](challenges/misc/runme_c/build)      |                                                                   -                                                                    |                                     | 13m0n4de |
|         [RunMe\[C3\]](challenges/misc/runme_c3/README.md)         |  Baby   |    [附件](challenges/misc/runme_c3/attachments)     |     [源代码](challenges/misc/runme_c3/build)     |                                                                   -                                                                    |                                     | 13m0n4de |
|     [RunMe\[Python\]](challenges/misc/runme_python/README.md)     |  Baby   |  [附件](challenges/misc/runme_python/attachments)   |                       -                       |                                                                   -                                                                    |                                     | 13m0n4de |
|        [RunMe\[ELF\]](challenges/misc/runme_elf/README.md)        |  Baby   |    [附件](challenges/misc/runme_elf/attachments)    |    [源代码](challenges/misc/runme_elf/build)     |                                                                   -                                                                    |                                     | 13m0n4de |
|        [RunMe\[EXE\]](challenges/misc/runme_exe/README.md)        |  Baby   |    [附件](challenges/misc/runme_exe/attachments)    |    [源代码](challenges/misc/runme_exe/build)     |                                                                   -                                                                    |                                     | 13m0n4de |
|         [web?](challenges/misc/html_ascii_art/README.md)          | Trivial | [附件](challenges/misc/html_ascii_art/attachments)  |                       -                       |                                                                   -                                                                    |                                     |   Rr19   |
|              [野宫](challenges/misc/nonomi/README.md)               | Trivial |     [附件](challenges/misc/nonomi/attachments)      |                       -                       |                                                                   -                                                                    |                 gif                 |   Rr19   |
|              [不是哥们？](challenges/misc/yygq/README.md)              | Trivial |      [附件](challenges/misc/yygq/attachments)       |                       -                       |                                                                   -                                                                    |              encoding               |   Rr19   |
| [Wireworld - LEVEL 0](challenges/misc/wireworld_level0/README.md) | Trivial |                         -                         | [源代码](challenges/misc/wireworld_level0/build) | [ghcr.io/svuctf/svuctf-helloworld-2024/wireworld_level0:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/wireworld_level0:latest) |                                     | 13m0n4de |
| [Wireworld - LEVEL 1](challenges/misc/wireworld_level1/README.md) | Trivial |                         -                         | [源代码](challenges/misc/wireworld_level1/build) | [ghcr.io/svuctf/svuctf-helloworld-2024/wireworld_level1:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/wireworld_level1:latest) |                                     | 13m0n4de |
|          [乾坤大挪移](challenges/misc/base64_video/README.md)          |  Easy   |  [附件](challenges/misc/base64_video/attachments)   |                       -                       |                                                                   -                                                                    | base64, steganography, file_carving |   Rr19   |
|           [红之墓](challenges/misc/gravekeeper/README.md)            |  Easy   |   [附件](challenges/misc/gravekeeper/attachments)   |                       -                       |                                                                   -                                                                    |           wav, morse_code           |   Rr19   |
|      [神秘的猪眼烧烤街道](challenges/misc/barbecue_street/README.md)       |  Easy   | [附件](challenges/misc/barbecue_street/attachments) |                       -                       |                                                                   -                                                                    |                OSINT                |   ksks   |
|           [??????](challenges/misc/cuneiform/README.md)           |  Easy   |    [附件](challenges/misc/cuneiform/attachments)    |                       -                       |                                                                   -                                                                    |              cuneiform              |   Rr19   |
|             [Music](challenges/misc/music/README.md)              | Normal  |      [附件](challenges/misc/music/attachments)      |                       -                       |                                                                   -                                                                    |  base16, steganography, silenteye   |   Rr19   |
|         [你好世界](challenges/misc/inverted_world/README.md)          | Normal  | [附件](challenges/misc/inverted_world/attachments)  |                       -                       |                                                                   -                                                                    |            steganography            |   Rr19   |
|            [猫咪问答](challenges/misc/neko_quiz/README.md)            | Normal  |                         -                         |    [源代码](challenges/misc/neko_quiz/build)     |        [ghcr.io/svuctf/svuctf-helloworld-2024/neko_quiz:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/neko_quiz:latest)        |                OSINT                | 13m0n4de |

### PPC

|                        题目描述与题解                        |   难度   | 附件  |                   源代码                    |                                                               镜像                                                               |    标签     |          出题人          |
| :---------------------------------------------------: | :----: | :-: | :--------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: | :-------: | :-------------------: |
| [1337 Machine](challenges/ppc/leet_machine/README.md) | Normal |  -  | [源代码](challenges/ppc/leet_machine/build) | [ghcr.io/svuctf/svuctf-helloworld-2024/leet_machine:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/leet_machine:latest) | pwntools  |       13m0n4de        |
|    [Soyo && Cat](challenges/ppc/concat/README.md)     | Medium |  -  |    [源代码](challenges/ppc/concat/build)    |       [ghcr.io/svuctf/svuctf-helloworld-2024/concat:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/concat:latest)       | ABNF, RFC | 13m0n4de && liseihoka |

### Pwn

|                         题目描述与题解                         |   难度    |                       附件                       |                    源代码                    |                                                                镜像                                                                |      标签       |   出题人    |
| :-----------------------------------------------------: | :-----: | :--------------------------------------------: | :---------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------: | :-----------: | :------: |
|          [Netcat](challenges/pwn/nc/README.md)          |  Baby   |                       -                        |      [源代码](challenges/pwn/nc/build)       |            [ghcr.io/svuctf/svuctf-helloworld-2024/nc:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/nc:latest)            |               | 13m0n4de |
|     [欸我 Flag 呢](challenges/pwn/nc_hidden/README.md)     |  Baby   |                       -                        |   [源代码](challenges/pwn/nc_hidden/build)   |     [ghcr.io/svuctf/svuctf-helloworld-2024/nc_hidden:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/nc_hidden:latest)     |               | 13m0n4de |
|          [猜数字](challenges/pwn/srand/README.md)          | Trivial |     [附件](challenges/pwn/srand/attachments)     |     [源代码](challenges/pwn/srand/build)     |         [ghcr.io/svuctf/svuctf-helloworld-2024/srand:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/srand:latest)         | pseudo_random | 13m0n4de |
| [Ret2shellcode](challenges/pwn/ret2shellcode/README.md) |  Easy   | [附件](challenges/pwn/ret2shellcode/attachments) | [源代码](challenges/pwn/ret2shellcode/build) | [ghcr.io/svuctf/svuctf-helloworld-2024/ret2shellcode:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/ret2shellcode:latest) | ret2shellcode | 13m0n4de |
|  [Ret2text\[64\]](challenges/pwn/ret2text64/README.md)  | Normal  |  [附件](challenges/pwn/ret2text64/attachments)   |  [源代码](challenges/pwn/ret2text64/build)   |    [ghcr.io/svuctf/svuctf-helloworld-2024/ret2text64:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/ret2text64:latest)    |   ret2text    | 13m0n4de |
|  [Ret2text\[32\]](challenges/pwn/ret2text32/README.md)  | Normal  |  [附件](challenges/pwn/ret2text32/attachments)   |  [源代码](challenges/pwn/ret2text32/build)   |    [ghcr.io/svuctf/svuctf-helloworld-2024/ret2text32:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/ret2text32:latest)    |   ret2text    | 13m0n4de |
|           [ROP](challenges/pwn/rop/README.md)           | Medium  |      [附件](challenges/pwn/rop/attachments)      |      [源代码](challenges/pwn/rop/build)      |           [ghcr.io/svuctf/svuctf-helloworld-2024/rop:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/rop:latest)           |      rop      | 13m0n4de |

### Reverse

|                     题目描述与题解                     |   难度   |                      附件                      |                   源代码                   | 镜像  |     标签      |  出题人  |
| :---------------------------------------------: | :----: | :------------------------------------------: | :-------------------------------------: | :-: | :---------: | :---: |
| [Welcome](challenges/reverse/welcome/README.md) |  Baby  | [附件](challenges/reverse/welcome/attachments) | [源代码](challenges/reverse/welcome/build) |  -  |             | COOK  |
|     [UPX](challenges/reverse/upx/README.md)     |  Easy  |   [附件](challenges/reverse/upx/attachments)   |   [源代码](challenges/reverse/upx/build)   |  -  |     upx     | COOK  |
|     [PYC](challenges/reverse/pyc/README.md)     | Normal |   [附件](challenges/reverse/pyc/attachments)   |   [源代码](challenges/reverse/pyc/build)   |  -  |  pyc, xor   | COOK  |
| [StreamLock](challenges/reverse/rc4/README.md)  | Medium |   [附件](challenges/reverse/rc4/attachments)   |   [源代码](challenges/reverse/rc4/build)   |  -  | rc4, base64 | pn1fg |

### Web

|                       题目描述与题解                       |   难度    | 附件  |                   源代码                   |                                                              镜像                                                              |        标签        |   出题人   |
| :-------------------------------------------------: | :-----: | :-: | :-------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------: | :--------------: | :-----: |
|       [Param](challenges/web/param/README.md)       |  Baby   |  -  |    [源代码](challenges/web/param/build)    |       [ghcr.io/svuctf/svuctf-helloworld-2024/param:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/param:latest)       |       http       |  SMJB   |
|     [ezHTTP](challenges/web/ez_http/README.md)      |  Baby   |  -  |   [源代码](challenges/web/ez_http/build)   |     [ghcr.io/svuctf/svuctf-helloworld-2024/ez_http:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/ez_http:latest)     |  http, headers   |  SMJB   |
|       [babyRCE](challenges/web/rce/README.md)       | Trivial |  -  |     [源代码](challenges/web/rce/build)     |         [ghcr.io/svuctf/svuctf-helloworld-2024/rce:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/rce:latest)         |     php, rce     |  SMJB   |
|      [Method](challenges/web/method/README.md)      |  Easy   |  -  |   [源代码](challenges/web/method/build)    |      [ghcr.io/svuctf/svuctf-helloworld-2024/method:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/method:latest)      |       http       | 13m0nde |
|   [PHP Class](challenges/web/php_class/README.md)   | Normal  |  -  |  [源代码](challenges/web/php_class/build)  |   [ghcr.io/svuctf/svuctf-helloworld-2024/php_class:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/php_class:latest)   |       php        |  SMJB   |
|      [ezRCE](challenges/web/ez_rce/README.md)       | Normal  |  -  |   [源代码](challenges/web/ez_rce/build)    |      [ghcr.io/svuctf/svuctf-helloworld-2024/ez_rce:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/ez_rce:latest)      | php, rce, bypass |  SMJB   |
| [Unserialize](challenges/web/unserialize/README.md) | Medium  |  -  | [源代码](challenges/web/unserialize/build) | [ghcr.io/svuctf/svuctf-helloworld-2024/unserialize:latest](https://ghcr.io/svuctf/svuctf-helloworld-2024/unserialize:latest) | php, unserialize |  SMJB   |

## 难度与分值

| 题目难度     | Baby | Trivial | Easy | Normal | Medium |
| :------- | :--- | :------ | :--- | :----- | :----- |
| 题目分值     | 200  | 400     | 700  | 1100   | 1600   |
| 题目最低分值比例 | 50%  | 50%     | 50%  | 50%    | 50%    |
| 题目最低分值   | 100  | 200     | 350  | 550    | 800    |
| 难度系数     | 6.0  | 8.0     | 10.0 | 12.0   | 14.0   |

## 来自参赛者的题解

选手需要使用 Pull Request 提交自己的题解文件，并在下面表格中添加自己的一栏信息。

注意：选手提交的 write-up 的主要内容需要在本仓库存档，仅仅提供到自己博客的题解链接的 Pull Requests 不会被合并。

选手提交的 write-up 中可以添加自己的博客链接，以及指定 License（如不指定，则默认与本仓库相同，见 [许可证](#%E8%AE%B8%E5%8F%AF%E8%AF%81) 一节）。

题解格式可以参考下方示例。

| 题解                                              | 备注       | 包含题目          |
| :---------------------------------------------- | :------- | :------------ |
| [选手或队伍名称](./player-write-ups/example/README.md) | 总排名第 N 名 | 题目一、题目二、题目... |

## 致谢

- [GZCTF](https://github.com/GZTimeWalker/GZCTF/)：比赛平台

## 许可证

该项目采用 GPL-3.0 许可证，查看 [LICENSE](LICENSE) 文件了解更多细节。
