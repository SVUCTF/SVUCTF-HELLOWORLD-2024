data = """
|S||00111011|01001110||
|*||00011111|01100001||
|Z||11000110|11001101||
|F||01101001|10001010||
|-||01100010|10110000||
|)||00111111|10000110||
|_||00110010|01000010||
|/||00011011|01001011||
|a||01100001|01111000||
|C||01001110|01110100||
|3||00110110|01100100||
|#||00101111|01111011||
|F||00011010|00110011||
|G||10101110|11100000||
|L||01101010|10010111||
|!||00000011|01000110||
|5||00001101|01001011||
|z||11100001|11100100||
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
