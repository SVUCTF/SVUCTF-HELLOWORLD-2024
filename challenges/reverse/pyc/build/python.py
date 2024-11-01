x = "akf`|d4fe0ece*1562*3>?1*>?1b*d>?ecc27b004z"
flag = ""

flag = input("Please Input Flag:")

s = ""

for i in flag:
    m = ord(i) ^ 0x7
    s += chr(m)

if s == x:
    print("GOOD!!!")
else:
    print("NO!!!")
