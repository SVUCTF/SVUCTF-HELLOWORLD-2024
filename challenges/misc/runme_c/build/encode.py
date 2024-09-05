flag = "flag{Y0u_C4n_C_1t_N0w!}"
enc_data = []

for index, char in enumerate(flag):
    enc_code = ord(char) ^ (index * 7) % 256
    enc_data.append(f"0x{enc_code:02x}")

print(",".join(enc_data))
