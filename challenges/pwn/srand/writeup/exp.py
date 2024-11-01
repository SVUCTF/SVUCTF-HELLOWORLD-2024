from pwn import *
from ctypes import cdll

context.log_level = "debug"

libc = cdll.LoadLibrary("libc.so.6")

io = process("../attachments/game")

libc.srand(libc.time(0))
number = libc.rand() % 99999 + 1

io.sendlineafter(b"Please enter your guess: ", str(number).encode())
io.interactive()
