data = """
|?||11011101|11110001||
|G||00010110|00100101||
|2||00101100|01001111||
|:||11001101|11010110||
|<||01001111|01100111||
|7||01111000|10000111||
|l||01101011|01111010||
|P||10010011|10110011||
|6||10101001|11100010||
|3||01001101|01111001||
|K||00111000|01100101||
|G||11010111|11111001||
|$||10001111|11001100||
|G||01101111|10010111||
|E||00000001|00011011||
|J||10000001|10110000||
|q||11110000|11111000||
|4||01111010|10101010||
|?||00100000|01010100||
|I||00000001|00110101||
""".strip()

flag = ""

for line in data.splitlines():
    _, orig_char, _, orig_binary, target_binary, _, _ = line.split("|")
    # print(orig_char, orig_binary, target_binary)
    orig_ascii = ord(orig_char)
    orig_binary = int(orig_binary, 2)
    target_binary = int(target_binary, 2)

    flag_ascii = orig_ascii + target_binary - orig_binary
    flag += chr(flag_ascii)

print(flag)
