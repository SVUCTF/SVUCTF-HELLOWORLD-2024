from pwn import *

context.log_level = "debug"

io = remote("localhost", 1337)

LEET_DICT = {"a": "4", "e": "3", "g": "6", "i": "1", "o": "0", "s": "5", "t": "7"}


def convert_to_leet(sentence):
    return "".join(LEET_DICT.get(char, char) for char in sentence.lower())


# 等待并通过初始提示
io.recvuntil("按下回车键开始系统修复...".encode())
io.sendline(b"")

for i in range(100):
    io.recvuntil("输入文本: ".encode())
    sentence = io.recvline().decode().strip()

    leet_sentence = convert_to_leet(sentence)

    io.sendlineafter("输出 LEET 文本 > ".encode(), leet_sentence.encode())

    response = io.recvline().decode()
    if "转换成功" not in response:
        log.failure(f"转换失败: {response}")
        break

io.interactive()
