encrypted_flag = "kqfl{q6k8_60_0m5w2_d5z_s88i_ud2m5s}"
shift = 5
flag = ""

for char in encrypted_flag:
    if char.isalpha():
        ascii_offset = ord("A") if char.isupper() else ord("a")
        flag += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
    elif char.isdigit():
        flag += str((int(char) - shift) % 10)
    else:
        flag += char

print(flag)
