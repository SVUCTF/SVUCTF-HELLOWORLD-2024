x = "akf`|d4fe0ece*1562*3>?1*>?1b*d>?ecc27b004z"
flag = ""

for char in x:
    s = chr(ord(char) ^ 7)
    flag += s

print("Decrypted flag:", flag)
