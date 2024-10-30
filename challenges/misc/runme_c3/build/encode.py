def encrypt_char(c, magic):
    value = ord(c)
    value = ((value << 4) | (value >> 4)) & 0xFF
    value ^= magic & 0xFF
    return value


def encrypt_flag(flag, magic):
    encrypted = []
    for i in range(0, len(flag), 4):
        chunk = flag[i : i + 4].ljust(4, "\x00")
        value = 0
        for j in range(4):
            value |= encrypt_char(chunk[j], magic) << (8 * j)
        encrypted.append(value)
    return encrypted


flag = "flag{C3_1s_4w3s0m3!}"
MAGIC = 0xC3

encrypted_flag = encrypt_flag(flag, MAGIC)

print("const uint[] ENCRYPTED_FLAG = {")
print("    " + ", ".join("0x{:06x}".format(x) for x in encrypted_flag))
print("};")
